# Déployez un modèle de Machine Learning

## Description

Ce projet a pour objectif de déployer un modèle de Machine Learning.

L'API permet d'effectuer une prédiction à partir des caractéristiques fournies et d'exposer le modèle de manière sécurisée et documentée.

## Modèle choisi

Le modèle déployé est celui du projet : 4 - Classifiez automatiquement des informations.<br>
Il permet de prédire si un employé de l'entreprise ESN TechNova Partners risque de quitter l'entreprise ou non.

---

## Technologies

- Python 3.13
- FastAPI
- Uvicorn
- scikit-learn / joblib
- pandas
- Pydantic

---

## Architecture du projet

```text
Project/
│
├── app/
│   ├── api/
│   │   └── routes.py           # Endpoints de l'API
│   ├── model/
│   │   ├── model.joblib        # Modèle entraîné
│   │   ├── model_manager.py    # Chargement, preprocess, prédiction
│   │   └── schema.py           # Schémas Pydantic (requêtes)
│   └── main.py                 # Point d'entrée
│
├── tests/
│   ├── coverage/               # Contiens les rapports de couverture des tests
│   ├── conftest.py             # Fixtures pytest partagées
│   ├── test_api.py             # Tests fonctionnels des endpoints
│   ├── test_model_manager.py   # Tests unitaires du modèle / preprocess
│   └── test_routes.http        # Requêtes manuelles (REST Client)
│
├── .github/workflows/ci.yml    # CI
├── .env(.exemple)              # Variables d'environments
└── pyproject.toml              # Fichier de configuration UV
```

---

## Gestion des branches

| Branche | Rôle |
|---------|------|
| `main` | Version stable, prête à être déployée / présentée |
| `develop` | Intégration des fonctionnalités en cours de développement |
| `feature/*` | Une branche par fonctionnalité ou tâche (ex. `feature/ci-cd`), pouvant être supprimée |

---

## Variables d'environnement

Copier le fichier `.env.exemple` puis le renommer en `.env`.

Compléter ensuite les variables d'environnement nécessaires avant de lancer l'application.

---

## Installation

Créer l'environnement virtuel et installer les dépendances :

```bash
uv sync
```

---

## Lancer l'application

```bash
uv run uvicorn app.main:app --reload --port 8000
```

L'API est ensuite disponible à l'adresse :

```
http://127.0.0.1:8000
```

---

## Tests

Lancer les tests (avec couverture) :

```bash
uv run pytest
```


Afficher le rapport détaillé des tests :

```bash
start tests/coverage/htmlcov/index.html
```

---

## Documentation de l'API

FastAPI génère automatiquement une documentation interactive.

### Swagger UI

```
http://127.0.0.1:8000/docs
```

Cette interface interactive permet de :

- consulter les endpoints disponibles ;
- visualiser les schémas des requêtes et des réponses ;
- exécuter des requêtes directement depuis le navigateur.

### ReDoc

```
http://127.0.0.1:8000/redoc
```

Une autre présentation de la documentation OpenAPI.

---

## Endpoints

| Méthode | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Accueil : vérifie que l'API est accessible |
| GET | `/health` | Santé du service |
| POST | `/predict` | Prédiction d'attrition pour **un** employé |
| POST | `/predict/batch` | Prédiction d'attrition pour une **liste** d'employés |

### `GET /`

**Réponse :**

```json
{
  "message": "Bienvenue sur l'API ESN TechNova Partners."
}
```

### `GET /health`

**Réponse :**

```json
{
  "status": "healthy"
}
```

### `POST /predict`

Prédit si un employé risque de quitter l'entreprise.

**Corps (JSON)** : caractéristiques de l'employé (schéma `PredictionRequest`).

Exemple :

```json
{
  "age": 41,
  "genre": "F",
  "revenu_mensuel": 5993,
  "statut_marital": "CÉLIBATAIRE",
  "departement": "COMMERCIAL",
  "poste": "CADRE COMMERCIAL",
  "nombre_experiences_precedentes": 8,
  "annee_experience_totale": 8,
  "annees_dans_l_entreprise": 6,
  "annees_dans_le_poste_actuel": 4,
  "nombre_participation_pee": 0,
  "nb_formations_suivies": 0,
  "distance_domicile_travail": 1,
  "niveau_education": 2,
  "domaine_etude": "INFRA & CLOUD",
  "frequence_deplacement": "OCCASIONNEL",
  "annees_depuis_la_derniere_promotion": 0,
  "annes_sous_responsable_actuel": 5,
  "satisfaction_employee_environnement": 2,
  "note_evaluation_precedente": 3,
  "niveau_hierarchique_poste": 2,
  "satisfaction_employee_nature_travail": 4,
  "satisfaction_employee_equipe": 1,
  "satisfaction_employee_equilibre_pro_perso": 1,
  "note_evaluation_actuelle": 3,
  "heure_supplementaires": "OUI",
  "augementation_salaire_precedente": 11
}
```

**Réponse :**

```json
{
  "prediction": 1,
  "probability": 0.6207335136311712
}
```

- `prediction` : `1` = risque de départ, `0` = reste dans l'entreprise
- `probability` : probabilité associée à la classe "départ"

### `POST /predict/batch`

Même logique que `/predict`, pour plusieurs employés.

**Corps (JSON) :**

```json
{
  "employees": [
    { "...": "objet PredictionRequest" },
    { "...": "objet PredictionRequest" }
  ]
}
```

**Réponse :**

```json
{
  "predictions": [
    { "prediction": 1, "probability": 0.62 },
    { "prediction": 0, "probability": 0.31 }
  ]
}
```

Des requêtes d'exemple sont aussi disponibles dans `tests/test_routes.http`.

---

## Auteur

**Marteau Alexandre**<br>
Projet réalisé dans le cadre de la formation **OpenClassrooms – AI Engineer**.
