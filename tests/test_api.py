#######################################
# Tests fonctionnels des endpoints API
#######################################


def test_root_returns_200(client):
    """Vérifie que GET / répond 200 et renvoie un message d'accueil."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_returns_healthy(client):
    """Vérifie que GET /health indique que le service est opérationnel."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_predict_returns_prediction_and_probability(client, sample_employee):
    """
    Vérifie qu'un POST /predict valide renvoie une prédiction binaire (0/1)
    et une probabilité comprise entre 0 et 1.
    """
    response = client.post("/predict", json=sample_employee)
    assert response.status_code == 200

    body = response.json()
    assert "prediction" in body
    assert "probability" in body
    assert body["prediction"] in (0, 1)
    assert 0.0 <= body["probability"] <= 1.0


def test_predict_accepts_lowercase_literals(client, sample_employee):
    """
    Vérifie que les Literal en minuscules sont acceptés
    grâce à la normalisation (to_upper) du schéma Pydantic.
    """
    payload = sample_employee.copy()
    payload["genre"] = "f"
    payload["heure_supplementaires"] = "oui"
    payload["departement"] = "commercial"

    response = client.post("/predict", json=payload)
    assert response.status_code == 200


def test_predict_rejects_invalid_genre(client, sample_employee):
    """Vérifie qu'un genre invalide (hors Literal) renvoie une erreur 422."""
    payload = sample_employee.copy()
    payload["genre"] = "X"

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_negative_salary(client, sample_employee):
    """Vérifie qu'un revenu mensuel négatif est refusé."""
    payload = sample_employee.copy()
    payload["revenu_mensuel"] = -100

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_rejects_missing_field(client, sample_employee):
    """Vérifie qu'un champ obligatoire manquant renvoie une erreur 422."""
    payload = sample_employee.copy()
    del payload["age"]

    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_batch_returns_list(client, sample_employee):
    """
    Vérifie que POST /predict/batch renvoie une prédiction
    et une probabilité pour chaque employé du lot.
    """
    payload = {"employees": [sample_employee, sample_employee]}

    response = client.post("/predict/batch", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert "predictions" in body
    assert len(body["predictions"]) == 2

    for item in body["predictions"]:
        assert item["prediction"] in (0, 1)
        assert 0.0 <= item["probability"] <= 1.0


def test_predict_batch_empty_list(client):
    """Vérifie qu'un batch vide renvoie une liste de prédictions vide."""
    response = client.post("/predict/batch", json={"employees": []})
    assert response.status_code == 200
    assert response.json() == {"predictions": []}
