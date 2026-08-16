<!-- Point de scroll lors du clic sur les boutons 'Retour en haut' -->
<a id="readme-top"></a>

<div align="center">
  <h1>Tests</h1>

  [README](../README.md)
    &middot;
  [Documentation BDD](database.md)
    &middot;
  [Exemples d'utilisation](usages.md)

</div>

<div id="sommaire"></div>

## Sommaire

- [Présentation](#presentation)
- [Prérequis](#prerequis)
- [Lancer les tests](#lancer-tests)
- [Configuration pytest](#configuration-pytest)
- [Fichiers de tests](#fichiers-de-tests)
  - [`test_api.py`](#test-api)
  - [`test_model.py`](#test-model)
  - [`test_db.py`](#test-db)
  - [`conftest.py`](#conftest)
- [Couverture de code](#couverture)
- [Tests en CI](#tests-ci)
- [Ressources](#ressources)

---

<div id="presentation"></div>

## Présentation

La suite de tests vérifie trois axes du projet :

- **API** — endpoints, validation Pydantic, scénarios d'erreur ;
- **Modèle** — preprocessing, feature engineering, prédictions ;
- **Base de données** — connexion, création/suppression, tables, insertion du dataset, intégrité des données.

Les tests sont exécutés avec **pytest**. La couverture du package `app` doit atteindre **85 %** minimum.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="prerequis"></div>

## Prérequis

1. Environnement initialisé : `uv sync`
2. Variable `DATABASE_URL` définie dans `.env` (requise pour `test_db.py`)
3. Application prête à être testée (voir [README — Installation](../README.md#installation))

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="lancer-tests"></div>

## Lancer les tests

Depuis la **racine du projet** :

```bash
uv run pytest
```

Afficher le rapport HTML de couverture (Windows) :

```bash
start tests/coverage/htmlcov/index.html
```

Le dossier `tests/coverage/` est généré localement et ignoré par Git.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="configuration-pytest"></div>

## Configuration pytest

Les options sont centralisées dans [`pyproject.toml`](../pyproject.toml) (`[tool.pytest.ini_options]`) :

| Option | Rôle                                              |
|--------|---------------------------------------------------|
| `--cov=app` | Mesure la couverture des tests                    |
| `--cov-report=term-missing` | Affiche les lignes non couvertes dans le terminal |
| `--cov-fail-under=85` | Échoue si la couverture est inférieure à 85 %     |
| `--cov-report=html:tests/coverage/htmlcov` | Génère le rapport HTML                            |


Les tests DB utilisent une **base temporaire** créée puis supprimée automatiquement.
<br>Cela permet de ne pas détruire une base de données déjà existante.

<div id="conftest"></div>

### `conftest.py`

Fixtures partagées :

- **`client`** — `TestClient` FastAPI (appels API sans serveur réel)
- **`sample_employee`** — payload JSON valide réutilisé dans les tests API et modèle.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="couverture"></div>

## Couverture de code

Le rapport terminal indique le pourcentage global et les lignes manquantes.

Le rapport HTML détaillé est disponible dans :

```
tests/coverage/htmlcov/index.html
```

Seuil minimum configuré : **85 %** sur le package `app`.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="tests-ci"></div>

## Tests en CI

Le workflow [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) exécute automatiquement :

1. Démarrage d'un service **PostgreSQL 16**
2. `uv sync --frozen`
3. `uv run python -m scripts.create_db --force`
4. `uv run pytest`

La variable `DATABASE_URL` est injectée dans l'environnement du job CI.

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="ressources"></div>

## Ressources

&middot; [README du projet](../README.md)<br>
&middot; [Configuration pytest](../pyproject.toml)<br>
&middot; [Requêtes manuelles](../tests/test_routes.http)<br>
&middot; [Documentation BDD](database.md)