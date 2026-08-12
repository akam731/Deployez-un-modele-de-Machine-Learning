# Base de données

## Structure

| Table | Rôle |
|-------|------|
| `datas` | Dataset de référence du modèle |
| `inputs` | Entrées envoyées à l’API / au modèle |
| `outputs` | Sorties du modèle (prédictions), liées aux `inputs` |

```text
datas
└── id

inputs
└── id

outputs
├── id
└── relation → inputs
```

---

## Script de création de la base de données

Fichier : `scripts/create_db.py`

### Fonctionnement

1. **Chaîne de connexion** — lit `DATABASE_URL` dans `.env`, ou demande une URL  
   (`postgresql://utilisateur:motdepasse@hote:port/nom_base`).
2. **Création de la base** — teste la connexion à la base cible, si elle n’existe pas, se connecte à la base système `postgres` et exécute `CREATE DATABASE`.
3. **Création des tables** — si au moins une table du schéma existe déjà, demande confirmation (les données seront supprimées), puis recrée le schéma, sinon crée les tables manquantes.

### Lancer le script

Depuis la racine du projet :

```bash
uv run python -m scripts.create_db
```
