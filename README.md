<!-- Point de scroll lors du clic sur les boutons 'Retour en haut' -->
<a id="readme-top"></a>

<div align="center">
  <h1>Déployez un modèle de Machine Learning</h1>

  [Démo live](https://deployez-un-modele-de-machine-learning.onrender.com)
    &middot;
  [Exemples d'utilisation](docs/usages.md)

</div>

<div id="sommaire"></div>

## Sommaire

- [À propos du projet](#a-propos-du-projet)
- [Stack technique](#stack-technique)
- [Architecture du projet](#architecture-du-projet)
- [Installation](#installation)
- [Déploiement](#deploiement)
- [Gestion des données](#gestion-donnees)
- [Sécurité et gestion des accès](#securite)
- [Tests](#tests)
- [Endpoints](#endpoints)
- [Gestion du répertoire GitHub](#gestion-github)
- [Auteur](#auteur)
- [Ressources](#ressources)

---

<div id="a-propos-du-projet"></div>

## À propos du projet


Ce projet a pour objectif de déployer un modèle de Machine Learning.

L'API permet d'effectuer une prédiction à partir des caractéristiques fournies et d'exposer le modèle de manière sécurisée et documentée.

Le modèle déployé est celui du projet : 4 - Classifiez automatiquement des informations.<br>

Il permet de prédire si un employé de l'entreprise ESN TechNova Partners risque de quitter l'entreprise ou non.

[Lien du github](https://github.com/akam731/Deployez-un-modele-de-Machine-Learning/)

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="stack-technique"></div>

## Stack technique

<div id="api-backend"></div>

### API & Backend

* [![Python][Python]][Python-url] 
  * Langage le plus approprié pour un projet ML de sa conception jusqu'au déploiement
* [![FastAPI][FastAPI]][FastAPI-url]
  * API REST moderne, rapide, documentation OpenAPI automatique
* [![Uvicorn][Uvicorn]][Uvicorn-url]
  *  Pour exécuter FastAPI en local et en production
* [![Pydantic][Pydantic]][Pydantic-url]
  * Validation stricte des entrées

<div id="data-machine-learning"></div>

### Data & Machine Learning

* [![Scikit-learn][Scikit-learn]][Scikit-learn-url]
  * Pour la classification et l'inférence
* [![Pandas][Pandas]][Pandas-url]
  * Préparation des DataFrames pour le preprocessing et l'inférence
* [![Joblib][Joblib]][Joblib-url]
  * Chargement du modèle sérialisé

<div id="base-de-donnees"></div>

### Base de données

* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
  * Base relationnelle robuste
* [![SQLAlchemy][SQLAlchemy]][SQLAlchemy-url]
  * ORM Python
* [![Psycopg][Psycopg]][Psycopg-url]
  * Driver PostgreSQL officiel pour Python, compatible avec SQLAlchemy


<div id="stack-production"></div>

### Production
* [![Render][Render]][Render-url]
  * Hébergement de l'API FastAPI en production
* [![Supabase][Supabase]][Supabase-url]
  * PostgreSQL managé pour la base de données en production
  
<!-- Sources-->
[Python]: https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[FastAPI]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com/
[Uvicorn]: https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white
[Uvicorn-url]: https://www.uvicorn.org/
[Pydantic]: https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white
[Pydantic-url]: https://docs.pydantic.dev/
[Scikit-learn]: https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white
[Scikit-learn-url]: https://scikit-learn.org/
[Pandas]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/
[Joblib]: https://img.shields.io/badge/Joblib-Model%20Serialization-555555?style=for-the-badge
[Joblib-url]: https://joblib.readthedocs.io/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[SQLAlchemy]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Psycopg]: https://img.shields.io/badge/Psycopg-PostgreSQL%20Driver-336791?style=for-the-badge&logo=postgresql&logoColor=white
[Psycopg-url]: https://www.psycopg.org/
[Render]: https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white
[Render-url]: https://render.com/
[Supabase]: https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white
[Supabase-url]: https://supabase.com/
<!-- Fin des Sources-->

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="architecture-du-projet"></div>

## Architecture du projet

Présentation de l'architecture du projet, de chaque dossier et chaque fichier :

```text
Project/
│
├── app/
│   ├── api/
│   │   └── routes.py                 # Endpoints de l'API
│   ├── database/
│   │   ├── database.py               # Connexion / session SQLAlchemy
│   │   ├── db_connexion.py           # Utilitaire de connexion
│   │   └── models.py                 # Modèles ORM
│   ├── model/
│   │   ├── datas/                    # Jeux de données sources (CSV)
│   │   │   ├── sirh.csv
│   │   │   ├── sondages.csv
│   │   │   └── eval.csv
│   │   ├── model.joblib              # Modèle entraîné
│   │   ├── model_manager.py          # Utilitaire du modèle
│   │   └── schema.py                 # Schémas Pydantic
│   └── main.py                       # Point d'entrée FastAPI
│
├── scripts/
│   ├── create_db.py                  # Création de la BDD et des tables
│   └── sql/
│       ├── create_tables.sql         # Script SQL de création des tables
│       ├── insert_inputs.sql         # Script SQL d'insertion du dataset
│       └── create_views.sql          # Script SQL de création des vues
│
├── docs/
│   ├── database.md                   # Documentation de la base de données
│   ├── shema_bdd.png                 # Schéma de la base de données
│   ├── tests.md                      # Documentation des tests
│   └── usages.md                     # Exemples d'utilisation
│
├── tests/
│   ├── coverage/                     # Rapports de couverture (générés)
│   ├── conftest.py                   # Fixtures pytest partagées
│   ├── test_api.py                   # Tests fonctionnels des endpoints
│   ├── test_model.py                 # Tests unitaires du modèle / preprocess
│   ├── test_db.py                    # Tests liés à la base de données
│   └── test_routes.http              # Requêtes manuelles (REST Client)
│
├── .github/workflows/
│   ├── ci.yml                        # Intégration continue (dev)
│   └── cd.yml                        # Déploiement continu (prod)
│
├── .env.exemple                      # Variables d'environnement (exemple)
├── pyproject.toml                    # Configuration du projet / UV / pytest
└── README.md                         # Documentation du projet
```

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="installation"></div>

## Installation

<div id="variables-environnement"></div>

### 1. Variables d'environnement :

Copier le fichier `.env.exemple` puis le renommer en `.env`.

Insérer ensuite la bonne chaîne de connexion à votre base de données [PostgreSQL][PostgreSQL-url]
```
DATABASE_URL=postgresql://utilisateur:motdepasse@hote:port/nom_base
```

<div id="initialisation"></div>

### 2. Initialisation
Créer l'environnement virtuel et installer les dépendances :

```bash
uv sync
```

<div id="lancer-application"></div>

### 3. Lancer l'application

L'application est prète à être lancée, vous pouvez personnaliser le port d'exécution du serveur au besoin
```bash
uv run uvicorn app.main:app --reload --port 8000
```

 L'API est ensuite disponible à l'adresse :

```
http://127.0.0.1:8000
```

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="deploiement"></div>

## Déploiement

L'API est hébergée sur **[Render](https://render.com/)** et la base PostgreSQL sur **[Supabase](https://supabase.com/)**.

| Environnement | URL |
|---------------|-----|
| **Production** | https://deployez-un-modele-de-machine-learning.onrender.com |
| **Swagger** | https://deployez-un-modele-de-machine-learning.onrender.com/docs |

### Variables d'environnement (production)

Configurer sur Render :

| Variable | Rôle |
|----------|------|
| `DATABASE_URL` | Chaîne de connexion Supabase (PostgreSQL) |

### Pipeline CI/CD

| Étape | Déclencheur | Action |
|-------|-------------|--------|
| **CI** | Push sur `master`, `develop`, `feature/*` | Tests + couverture (PostgreSQL éphémère) |
| **CD** | CI réussie sur `master` | Déploiement Render via deploy hook |

Le secret `RENDER_DEPLOY_HOOK` est stocké dans les **GitHub Secrets** (voir [Gestion du répertoire GitHub](#gestion-github)).

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="gestion-donnees"></div>

## Gestion des données

### Flux de stockage

1. **Dataset de référence** — chargé dans `inputs` (`source='dataset'`) + `outputs` (label réel, `probability=1.0`), via `create_db.py` (CSV).
2. **Requête API** — chaque appel à `/predict` ou `/predict/batch` enregistre les features dans `inputs` (`source='api'`).
3. **Prédiction** — le résultat est stocké dans `outputs` (lien 1–1 avec `inputs`).

Détail complet : [docs/database.md](docs/database.md).

### Exemples de données en base

- **Dataset initial** : [`scripts/sql/insert_inputs.sql`](scripts/sql/insert_inputs.sql) (insertions SQL du jeu de référence).
- **Prédictions API** : créées automatiquement à chaque appel de prédiction.

### Besoins analytiques

La vue SQL `vue_predictions` agrège dataset et prédictions API (colonne `source`) pour alimenter un futur **tableau de bord** (Power BI, Metabase, Supabase SQL Editor, etc.).

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="securite"></div>

## Sécurité et gestion des accès

### Authentification

Cette V1 **n'implémente pas d'authentification utilisateur** (pas de login, JWT ni clé API).
L'accès est encadré par :

- la **validation stricte** des requêtes (schémas Pydantic) ;
- le déploiement sur une **URL dédiée** (Render), dans le cadre du projet.

Une évolution possible : clé API ou reverse proxy pour restreindre l'accès.

### Gestion des secrets

| Secret | Local | CI (GitHub Actions) | Production |
|--------|-------|---------------------|------------|
| `DATABASE_URL` | Fichier `.env` | Secret du dépôt | Variable Render |
| `RENDER_DEPLOY_HOOK` | — | Secret du dépôt | — |

Bonnes pratiques appliquées :

- `.env` dans `.gitignore` ;
- modèle [`.env.exemple`](.env.exemple) sans valeurs sensibles ;
- aucune credential en dur dans le code source ;
- connexion PostgreSQL et API servie en **HTTPS** en production.

> Pas de gestion de comptes utilisateurs : le hachage de mot de passe n'est pas applicable dans cette version.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="tests"></div>

## Tests


<p>L'application doit être <a href="#initialisation">initialisée</a> en amont pour pouvoir réaliser les tests. </p>

<div id="lancer-tests"></div>

### 1. Lancer les tests :

La couverture, les rapports et le seuil minimum (85 %) sont configurés 
dans le fichier [pyproject.toml](pyproject.toml)

```bash
uv run pytest
```

Le rapport de couverture est généré automatiquement dans le 
dossier [tests/coverage/](tests/coverage/)

<div id="rapport-couverture"></div>

### 2. Afficher le rapport détaillé :

La commande ouvre une page HTML contenant le rapport des tests et le rapport de couverture

```bash
start tests/coverage/htmlcov/index.html
```

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="endpoints"></div>

## Endpoints

URL de production :
https://deployez-un-modele-de-machine-learning.onrender.com

> L’API de production est hébergée sur [render](https://render.com). Lorsqu’elle reste inactive pendant un certain temps, elle passe en mode veille. À la prochaine requête, Render la réactive automatiquement.

Documentation interactive OpenAPI (Swagger / ReDoc) :

| Environnement | Swagger UI | ReDoc |
|---------------|------------|-------|
| Local | http://127.0.0.1:8000/docs | http://127.0.0.1:8000/redoc |
| Production | https://deployez-un-modele-de-machine-learning.onrender.com/docs | https://deployez-un-modele-de-machine-learning.onrender.com/redoc |

Ces interfaces permettent de consulter les endpoints, visualiser les schémas et exécuter des requêtes depuis le navigateur.

| Méthode | Endpoint | Description |
|----------|----------|-------------|
| GET | `/` | Accueil : vérifie que l'API est accessible |
| GET | `/health` | Santé du service |
| POST | `/predict` | Prédiction d'attrition pour **un** employé |
| POST | `/predict/batch` | Prédiction d'attrition pour une **liste** d'employés |

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="gestion-github"></div>

## Gestion du répertoire GitHub

<div id="branches"></div>

### Branches 

| Branche     | Rôle |
|-------------|------|
| `master`    | Version stable, prête à être déployée / présentée |
| `develop`   | Intégration des fonctionnalités en cours de développement |
| `feature/*` | Une branche par fonctionnalité ou tâche (ex. `feature/ci-cd`), pouvant être supprimée |

<div id="tags"></div>

### Tags

| Tag                       | Rôle                                                                    |
|---------------------------|-------------------------------------------------------------------------|
| `v0.1-structure-initiale` | Structure simple de FastAPI, aucune fonctionnalité de l'API implémentée |
| `v1.0`                    | API fonctionnelle, routes /predict et /predict/batch fonctionnelles     |
| `v2.0`                    | BDD PostgreSQL, logging des prédictions, docs et tests associés         |
| `v3.0`                    | Version finale avec une base de données optimisée                       |

<div id="cicd"></div>

### CI/CD

CI : Chaque push déclenche la CI (tests + couverture)
CD : Chaque push déclenche la CI (tests + couverture).
En cas de succès sur master, le workflow CD déploie l'API sur Render.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="auteur"></div>

## Auteur

**Marteau Alexandre**<br>
Projet réalisé dans le cadre de la formation **OpenClassrooms – AI Engineer**.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="ressources"></div>

## Ressources

&middot; [Documentation sur la base de données](docs/database.md)<br>
&middot; [Documentation sur les tests](docs/tests.md)<br>
&middot; [Exemples d'utilisation](docs/usages.md) <br>
&middot; [URL de production](https://deployez-un-modele-de-machine-learning.onrender.com)