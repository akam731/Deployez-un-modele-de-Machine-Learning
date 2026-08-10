import pandas as pd

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
@app.post("/predict")
async def predict(request: PredictionRequest):

    # Conversion de la requête validée en DataFrame (1 ligne)
    df = pd.DataFrame([request.model_dump()])

    # Prédiction binaire (0/1) et probabilité de départ
    prediction = ModelManager.predict(df)[0]
    probability = ModelManager.predict_proba(df)[0][1]

    return {
        "prediction": int(prediction),
        "probability": float(probability)
    }

################################
# Route de prédictions multiples
################################
@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):

    # Aucun employé dans la requête : rien à prédire
    if not request.employees:
        return {"predictions": []}

    # Conversion de la liste d'employés en DataFrame (1 ligne par employé)
    df = pd.DataFrame([employee.model_dump() for employee in request.employees])

    # Prédictions et probabilités pour tout le lot
    predictions = ModelManager.predict(df)
    probabilities = ModelManager.predict_proba(df)[:, 1]

    # Liste de résultats (une entrée par employé)
    return {
        "predictions": [
            {
                "prediction": int(prediction),
                "probability": float(probability),
            }
            for prediction, probability in zip(predictions, probabilities)
        ]
    }
