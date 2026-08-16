<!-- Point de scroll lors du clic sur les boutons 'Retour en haut' -->
<a id="readme-top"></a>

<div align="center">
  <h1>Exemples d'utilisation</h1>

  [README](../README.md)
    &middot;
  [Documentation BDD](database.md)

</div>

<div id="sommaire"></div>

## Sommaire

- [Exemples par endpoint](#exemples-endpoints)
  - [`GET /`](#get-racine)
  - [`GET /health`](#get-health)
  - [`POST /predict`](#post-predict)
  - [`POST /predict/batch`](#post-predict-batch)
- [Erreurs de validation](#erreurs-validation)
- [Tester avec REST Client](#rest-client)
- [Ressources](#ressources)

---

<div id="exemples-endpoints"></div>

## Exemples par endpoint

<div id="get-racine"></div>

### `GET /`

Vérifie que l'API répond.

**Requête :**

```http
GET / HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Réponse (`200`) :**

```json
{
  "message": "Bienvenue sur l'API ESN TechNova Partners."
}
```

---

<div id="get-health"></div>

### `GET /health`

Contrôle de santé du service.

**Requête :**

```http
GET /health HTTP/1.1
Host: 127.0.0.1:8000
Accept: application/json
```

**Réponse (`200`) :**

```json
{
  "status": "healthy"
}
```

---

<div id="post-predict"></div>

### `POST /predict`

Prédit si un employé risque de quitter l'entreprise.

**Corps (JSON)** : schéma `PredictionRequest` — voir [`app/model/schema.py`](../app/model/schema.py).

**Exemple de requête :**

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

**Réponse (`200`) :**

```json
{
  "prediction": 1,
  "probability": 0.6207335136311712
}
```

---

<div id="post-predict-casse"></div>

### `POST /predict` — casse mixte

Les littéraux en minuscules ou mixtes sont acceptés et convertis automatiquement :

```json
{
  "age": 45,
  "genre": "f",
  "revenu_mensuel": 7800,
  "statut_marital": "divorcé(e)",
  "departement": "ressources humaines",
  "poste": "manager",
  "nombre_experiences_precedentes": 4,
  "annee_experience_totale": 20,
  "annees_dans_l_entreprise": 10,
  "annees_dans_le_poste_actuel": 3,
  "nombre_participation_pee": 2,
  "nb_formations_suivies": 5,
  "distance_domicile_travail": 8,
  "niveau_education": 4,
  "domaine_etude": "marketing",
  "frequence_deplacement": "occasionnel",
  "annees_depuis_la_derniere_promotion": 2,
  "annes_sous_responsable_actuel": 4,
  "satisfaction_employee_environnement": 4,
  "note_evaluation_precedente": 4,
  "niveau_hierarchique_poste": 3,
  "satisfaction_employee_nature_travail": 3,
  "satisfaction_employee_equipe": 2,
  "satisfaction_employee_equilibre_pro_perso": 3,
  "note_evaluation_actuelle": 4,
  "heure_supplementaires": "oui",
  "augementation_salaire_precedente": 12
}
```

---

<div id="post-predict-batch"></div>

### `POST /predict/batch`

Même logique que `/predict`, pour plusieurs employés.

**Corps (JSON)** : schéma `BatchPredictionRequest` — liste `employees` d'objets `PredictionRequest`.

**Exemple de requête :**

```json
{
  "employees": [
    {
      "age": 28,
      "genre": "M",
      "revenu_mensuel": 4120,
      "statut_marital": "CÉLIBATAIRE",
      "departement": "CONSULTING",
      "poste": "CONSULTANT",
      "nombre_experiences_precedentes": 2,
      "annee_experience_totale": 5,
      "annees_dans_l_entreprise": 2,
      "annees_dans_le_poste_actuel": 1,
      "nombre_participation_pee": 1,
      "nb_formations_suivies": 2,
      "distance_domicile_travail": 12,
      "niveau_education": 3,
      "domaine_etude": "TRANSFORMATION DIGITALE",
      "frequence_deplacement": "FREQUENT",
      "annees_depuis_la_derniere_promotion": 1,
      "annes_sous_responsable_actuel": 2,
      "satisfaction_employee_environnement": 3,
      "note_evaluation_precedente": 3,
      "niveau_hierarchique_poste": 1,
      "satisfaction_employee_nature_travail": 2,
      "satisfaction_employee_equipe": 4,
      "satisfaction_employee_equilibre_pro_perso": 2,
      "note_evaluation_actuelle": 3,
      "heure_supplementaires": "NON",
      "augementation_salaire_precedente": 15
    },
    {
      "age": 37,
      "genre": "F",
      "revenu_mensuel": 6500,
      "statut_marital": "MARIÉ(E)",
      "departement": "COMMERCIAL",
      "poste": "TECH LEAD",
      "nombre_experiences_precedentes": 3,
      "annee_experience_totale": 12,
      "annees_dans_l_entreprise": 5,
      "annees_dans_le_poste_actuel": 2,
      "nombre_participation_pee": 1,
      "nb_formations_suivies": 4,
      "distance_domicile_travail": 18,
      "niveau_education": 5,
      "domaine_etude": "ENTREPREUNARIAT",
      "frequence_deplacement": "AUCUN",
      "annees_depuis_la_derniere_promotion": 1,
      "annes_sous_responsable_actuel": 3,
      "satisfaction_employee_environnement": 1,
      "note_evaluation_precedente": 2,
      "niveau_hierarchique_poste": 2,
      "satisfaction_employee_nature_travail": 4,
      "satisfaction_employee_equipe": 3,
      "satisfaction_employee_equilibre_pro_perso": 1,
      "note_evaluation_actuelle": 3,
      "heure_supplementaires": "OUI",
      "augementation_salaire_precedente": 20
    }
  ]
}
```

**Réponse (`200`) :**

```json
{
  "predictions": [
    { "prediction": 1, "probability": 0.62 },
    { "prediction": 0, "probability": 0.31 }
  ]
}
```
---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="erreurs-validation"></div>

## Erreurs de validation

En cas de données invalides, l'API retourne un code **`422`** avec le détail Pydantic.

| Cas | Exemple | Erreur                                              |
|-----|---------|-----------------------------------------------------|
| Genre invalide | `"genre": "X"` | Valeur hors `F` / `M`                               |
| Salaire négatif | `"revenu_mensuel": -100` | Valeur positive uniquement                          |
| Batch vide | `"employees": []` | Liste vide acceptée — retourne `{"predictions": []}` |

**Exemple — genre invalide :**

```json
{
  "detail": [
    {
      "type": "literal_error",
      "loc": ["body", "genre"],
      "msg": "Input should be 'F' or 'M'",
      "input": "X"
    }
  ]
}
```

---

<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="rest-client"></div>

## Tester avec REST Client

Le fichier [`tests/test_routes.http`](../tests/test_routes.http) contient des requêtes prêtes à l'emploi.

**Utilisation :**

1. Lancer l'API : `uv run uvicorn app.main:app --reload --port 8000`
2. Ouvrir `tests/test_routes.http`
3. Cliquer sur `Run HTTP Request` au-dessus de chaque requête

---
<p align="right">(<a href="#readme-top">Retour en haut</a>)</p>

<div id="ressources"></div>

## Ressources

&middot; [README du projet](../README.md)<br>
&middot; [Documentation BDD](database.md)<br>
&middot; [Documentation tests](tests.md)<br>