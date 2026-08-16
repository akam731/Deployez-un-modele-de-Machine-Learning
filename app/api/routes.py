import pandas as pd

from app.database.database import get_db
from app.main import app
from app.model.model_manager import model_manager as ModelManager
from app.model.schema import BatchPredictionRequest, PredictionRequest

################################
# Route principale
################################
@app.get(
    "/", summary="Accueil de l'API",
    description="Vérifie que l'API est accessible et retourne un message de bienvenue."
)
async def root(): return { "message": "Bienvenue sur l'API ESN TechNova Partners."}

################################
# État de santé de l'API
################################
@app.get(
    "/health", summary="Vérification de l'état de l'API",
    description="Retourne l'état de santé de l'API. Cet endpoint permet de vérifier que le service est opérationnel."
)
async def health(): return { "status": "healthy"}

################################
# Route de prédiction unique
################################
@app.post("/predict", summary="Prédiction d'attrition pour un employé",
    description="Analyse les features d'un employé et estime le risque de départ")
async def predict(request: PredictionRequest):

    # Conversion de la requête validée en DataFrame (1 ligne)
    df = pd.DataFrame([request.model_dump()])

    # Prédiction binaire (0/1) et probabilité de départ
    prediction = ModelManager.predict(df)[0]
    probability = ModelManager.predict_proba(df)[0][1]

    # Sauvegarde des inputs et outputs en base de données
    get_db().save_prediction(request.model_dump(), prediction, probability)

    return {
        "prediction": int(prediction),
        "probability": float(probability),
    }

################################
# Route de prédictions multiples
################################
@app.post("/predict/batch", summary="Prédiction d'attrition pour plusieurs employés",
    description="Applique la prédiction à plusieurs employés en une seule requête.")
async def predict_batch(request: BatchPredictionRequest):

    # Aucun employé dans la requête : rien à prédire
    if not request.employees:
        return {"predictions": []}

    # Conversion de la liste d'employés en DataFrame (1 ligne par employé)
    df = pd.DataFrame([employee.model_dump() for employee in request.employees])

    # Prédictions et probabilités pour tout le lot
    predictions = ModelManager.predict(df)
    probabilities = ModelManager.predict_proba(df)[:, 1]

    # Sauvegarde des inputs et outputs en base de données
    db = get_db()
    results = []
    for employee, pred, proba in zip(request.employees, predictions, probabilities):
        p, pr = int(pred), float(proba)
        db.save_prediction(employee.model_dump(), p, pr)
        results.append({"prediction": p, "probability": pr})

    # Liste de résultats (une entrée par employé)
    return {"predictions": results}
