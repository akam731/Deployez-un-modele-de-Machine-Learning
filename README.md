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

---

## Architecture du projet

```text
credit-scoring-api/
│
├── app/
│   ├── model/                  # Modèle Machine Learning
│   └── main.py                 # Point d'entrée
│
├── tests/                      # Tests unitaires et fonctionnels
│   └── test_routes.http        # Tests des endpoints de l'api
│
├── README.md                   # Documentation
├── .env(.exemple)              # Variables d'environnement
└── pyproject.toml              # Fichier de configuration UV
```

---

## Variables d'environnement

Copier le fichier `.env.example` puis le renommer en `.env`.

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
uv run uvicorn app.main:app --reload
```

L'API est ensuite disponible à l'adresse :

```
http://127.0.0.1:8000
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

## Endpoints

| Méthode | Endpoint | Description                                                      |
|----------|----------|------------------------------------------------------------------|
| GET | / | Endpoint par défaut, permet de vérifier que l'API est accessible |

---

## Auteur

**Marteau Alexandre**<br>
Projet réalisé dans le cadre de la formation **OpenClassrooms – AI Engineer**.