<!-- Point de scroll lors du clic sur les boutons 'Retour en haut' -->
<a id="readme-top"></a>

<div align="center">
  <h1>Base de données</h1>

  [README](../README.md)
    &middot;
  [Exemples d'utilisation](usages.md)

</div>

<div id="sommaire"></div>

## Sommaire

- [Présentation](#présentation)
- [Schéma de la base de données](#schéma-de-la-base-de-données)
- [Structure des tables](#structure-des-tables)
  - [Table `inputs`](#table-inputs)
  - [Table `outputs`](#table-outputs)
- [Vues SQL](#vues-sql)
  - [`vue_predictions`](#vue_predictions)
- [Initialisation de la base](#initialisation-de-la-base)
  - [Variables d'environnement](#variables-denvironnement)
  - [Script `create_db.py`](#script-create_dbpy)
  - [Mode interactif vs `--force`](#mode-interactif-vs---force)
  - [Scripts SQL (`scripts/sql/`)](#scripts-sql-scriptssql)
- [Logging des prédictions](#logging-des-prédictions)
- [Ressources](#ressources)

---

<div id="presentation"></div>

## Présentation

La base PostgreSQL stocke :

- les **entrées** (features employé) dans `inputs` — dataset de référence (`source='dataset'`) ou requêtes API (`source='api'`)
- les **sorties** associées dans `outputs` — label réel pour le dataset, prédiction du modèle pour l'API

En production, la base est hébergée sur **Supabase**.<br>
En local ou en CI, elle peut tourner sur une instance PostgreSQL classique via la variable d'environnement `DATABASE_URL`.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="schema-bdd"></div>

## Schéma de la base de données

Schéma UML de la base de données réalisé sur https://dbdiagram.io/

![Schéma de la base de données](shema_bdd.png)

### Relations

Il y a une relation 1–1 entre les tables `inputs` et `outputs` (`input_id` unique).
Elle permet de relier chaque sortie (`outputs`) à son entrée (`inputs`).

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="structure-tables"></div>

## Structure des tables

| Table | Rôle |
|-------|------|
| `inputs` | Caractéristiques employé (dataset ou requêtes API) |
| `outputs` | Label réel (dataset) ou prédiction modèle (API), lié 1–1 à un `input` |

Les colonnes **features** sont définies via le mixin `EmployeeFeatures` (`app/database/models.py`), aligné sur le schéma Pydantic `PredictionRequest`.

<div id="table-inputs"></div>

### Table `inputs`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant |
| `source` | String(20) | `dataset` (référence) ou `api` (requête live) |
| `created_at` | DateTime (UTC) | Horodatage de l'enregistrement |
| + features | — | Caractéristiques de l'employé (âge, genre, département, etc.) |

<div id="table-outputs"></div>

### Table `outputs`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant |
| `input_id` | Integer (FK, unique) | Lien vers `inputs.id` |
| `prediction` | Integer | `0` ou `1` — label réel (dataset) ou prédiction modèle (API) |
| `probability` | Float | `1.0` pour le dataset ; probabilité du modèle pour l'API |
| `created_at` | DateTime (UTC) | Horodatage |

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="vues-sql"></div>

## Vues SQL

Créées par `scripts/sql/create_views.sql` via `database.create_views()`.

<div id="vue-predictions"></div>

### `vue_predictions`

Jointure `inputs` + `outputs` : une ligne = une entrée avec sa sortie associée.

La colonne `source` permet de distinguer :

- `dataset` → label réel du jeu de référence (`prediction`, `probability=1.0`) ;
- `api` → prédiction et probabilité renvoyées par le modèle.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="initialisation"></div>

## Initialisation de la base

<div id="variables-environnement"></div>

### Variables d'environnement

Définir `DATABASE_URL` dans le fichier `.env` :

```text
DATABASE_URL=postgresql://utilisateur:motdepasse@hote:port/nom_base
```

<div id="script-create-db"></div>

### Script `create_db.py`

Fichier : `scripts/create_db.py`

Étapes exécutées :

1. **Connexion** — lit `DATABASE_URL` (`.env`) ou demande une URL.
2. **Création de la base** — crée la base PostgreSQL si elle n'existe pas.
3. **Création des tables** — recrée le schéma si nécessaire (`inputs`, `outputs`).
4. **Insertion du dataset** — charge les CSV (`sirh`, `sondages`, `eval`) dans `inputs` + `outputs` (`source='dataset'`).
5. **Création des vues** — exécute `create_views.sql`.

Depuis la **racine du projet** :

```bash
uv run python -m scripts.create_db
```

<div id="mode-force"></div>

### Mode interactif vs `--force`

| Mode | Commande | Usage                                                                           |
|------|----------|---------------------------------------------------------------------------------|
| Interactif | `uv run python -m scripts.create_db` | Validation de la base de données concernée (intéraction via `input` et `getpass`) |
| Non interactif | `uv run python -m scripts.create_db --force` | Utilise `DATABASE_URL` directement et ne pose aucune question                 |

---

<div id="scripts-sql"></div>

### Scripts SQL (`scripts/sql/`)

En complément du script Python, le projet fournit des **scripts SQL exécutables directement** dans un SGBD (pgAdmin, éditeur SQL Supabase, etc.) :

| Fichier | Rôle |
|---------|------|
| [`create_tables.sql`](../scripts/sql/create_tables.sql) | Création des tables `inputs`, `outputs` |
| [`insert_inputs.sql`](../scripts/sql/insert_inputs.sql) | Insertion du dataset de référence dans `inputs` + `outputs` |
| [`create_views.sql`](../scripts/sql/create_views.sql) | Création de la vue `vue_predictions` |

> **Note :** `create_db.py` automatise l'initialisation complète (tables, insertion du dataset depuis les CSV, vues).
> Les fichiers SQL restent utiles si on préfère initialiser la base **manuellement**.
---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="logging-predictions"></div>

## Logging des prédictions

Chaque appel à `/predict` ou `/predict/batch` enregistre :

1. les features dans `inputs` (`source='api'`) ;
2. la prédiction et la probabilité dans `outputs`.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="ressources"></div>

## Ressources

&middot; [README du projet](../README.md)<br>
&middot; [Documentation sur les tests](tests.md)<br>
&middot; [Exemples d'utilisation](usages.md) <br>
&middot; [URL de production](https://deployez-un-modele-de-machine-learning.onrender.com)
