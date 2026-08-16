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

- [Sommaire](#sommaire)
- [Présentation](#présentation)
- [Schéma de la base de données](#schéma-de-la-base-de-données)
  - [Relations](#relations)
- [Structure des tables](#structure-des-tables)
  - [Table `datas`](#table-datas)
  - [Table `inputs`](#table-inputs)
  - [Table `outputs`](#table-outputs)
- [Vues SQL](#vues-sql)
  - [`vue_predictions`](#vue_predictions)
  - [`vue_datas`](#vue_datas)
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

- le **dataset de référence** utilisé pour entraîner le modèle (`datas`)
- les **entrées API** envoyées au modèle (`inputs`)
- les **sorties du modèle** associées (`outputs`)

En production, la base est hébergée sur **Supabase**.<br>
En local ou en CI, elle peut tourner sur une instance PostgreSQL classique via la variable d'environnement `DATABASE_URL`.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="schema-bdd"></div>

## Schéma de la base de données

Schéma UML de la base de données réalisé sur https://dbdiagram.io/

![Schéma de la base de données](shema_bdd.png)

### Relations 
Il y a une relation 1–1 entre les tables Inputs et Outputs (`input_id` unique).
Elle permet de relier chaque sortie (Outputs) à son entrée (Inputs)


---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="structure-tables"></div>

## Structure des tables

| Table | Rôle |
|-------|------|
| `datas` | Dataset de référence du modèle (features + cible) |
| `inputs` | Entrées envoyées à l'API / au modèle |
| `outputs` | Prédictions du modèle, liées à un `input` |

Les colonnes **features** sont partagées entre `datas` et `inputs` via le mixin `EmployeeFeatures` (`app/database/models.py`), aligné sur le schéma Pydantic `PredictionRequest`.

<div id="table-datas"></div>

### Table `datas`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant |
| `a_quitte_l_entreprise` | Integer | Cible : `1` = départ, `0` = reste |
| + features | — | Mêmes colonnes que `PredictionRequest` (âge, genre, département, etc.) |

<div id="table-inputs"></div>

### Table `inputs`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant |
| `created_at` | DateTime (UTC) | Horodatage de la requête API |
| + features | — | Caractéristiques de l'employé envoyées à `/predict` |

<div id="table-outputs"></div>

### Table `outputs`

| Colonne | Type | Description |
|---------|------|-------------|
| `id` | Integer (PK) | Identifiant |
| `input_id` | Integer (FK, unique) | Lien vers `inputs.id` |
| `prediction` | Integer | `0` ou `1` |
| `probability` | Float | Probabilité de la classe prédite |
| `created_at` | DateTime (UTC) | Horodatage de la prédiction |

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="vues-sql"></div>

## Vues SQL

Créées par `scripts/sql/create_views.sql` via `database.create_views()`.

<div id="vue-predictions"></div>

### `vue_predictions`

Jointure `inputs` + `outputs` : une ligne = une requête API avec sa prédiction et sa probabilité.

<div id="vue-datas"></div>

### `vue_datas`

Union du dataset (`datas`) et des prédictions API (`inputs` + `outputs`), avec une colonne `source` :

- `dataset` → label réel (`a_quitte_l_entreprise`) ;
- `api` → prédiction + probabilité du modèle.

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
3. **Création des tables** — recrée le schéma si nécessaire (`datas`, `inputs`, `outputs`).
4. **Insertion du dataset** — charge les CSV (`sirh`, `sondages`, `eval`) dans `datas`.
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
| [`create_tables.sql`](../scripts/sql/create_tables.sql) | Création des tables `datas`, `inputs`, `outputs` |
| [`insert_datas.sql`](../scripts/sql/insert_datas.sql) | Insertion du dataset de référence dans `datas` |
| [`create_views.sql`](../scripts/sql/create_views.sql) | Création des vues `vue_predictions` et `vue_datas` |


> **Note :** `create_db.py` automatise ces étapes via SQLAlchemy (tables + CSV) et exécute `create_views.sql`. 
> Les fichiers SQL restent utiles si on préfère initialiser la base **manuellement**
---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="logging-predictions"></div>

## Logging des prédictions

Chaque appel à `/predict` ou `/predict/batch` enregistre :

1. les features dans `inputs` ;
2. la prédiction et la probabilité dans `outputs`.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="ressources"></div>

## Ressources

&middot; [README du projet](../README.md)<br>
&middot; [Documentation sur les tests](tests.md)<br>
&middot; [Exemples d'utilisation](usages.md) <br>
&middot; [URL de production](https://deployez-un-modele-de-machine-learning.onrender.com)