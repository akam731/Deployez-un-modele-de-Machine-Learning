#######################################
# Tests unitaires du model_manager
#######################################

import pandas as pd

from app.model.model_manager import model_manager


def test_to_training_case_title_and_fixes():
    """
    Vérifie la normalisation de casse des catégories
    (Title Case + correctifs Marié(e) / Assistant de Direction).
    """
    assert model_manager.to_training_case("INFRA & CLOUD") == "Infra & Cloud"
    assert model_manager.to_training_case("MARIÉ(E)") == "Marié(e)"
    assert model_manager.to_training_case("ASSISTANT DE DIRECTION") == (
        "Assistant de Direction"
    )
    assert model_manager.to_training_case("oui") == "Oui"


def test_preprocess_aligns_columns_with_model(sample_employee):
    """
    Vérifie que le preprocessing produit exactement
    les colonnes attendues par le modèle entraîné.
    """
    df = pd.DataFrame([sample_employee])
    processed = model_manager.preprocess(df)

    expected = list(model_manager.get_model().feature_names_in_)
    assert list(processed.columns) == expected
    assert processed.shape == (1, len(expected))


def test_preprocess_creates_engineered_features(sample_employee):
    """
    Vérifie que le feature engineering crée bien les variables dérivées
    (fidelite, ratio_experience_age, satisfaction_globale, deja_promu).
    """
    df = pd.DataFrame([sample_employee])
    # On teste avant le reindex via les étapes intermédiaires
    df = model_manager.normalize_categories(df.copy())
    engineered = model_manager.feature_engineering(df)

    assert "fidelite" in engineered.columns
    assert "ratio_experience_age" in engineered.columns
    assert "satisfaction_globale" in engineered.columns
    assert "deja_promu" in engineered.columns
    assert engineered.loc[0, "deja_promu"] == 1


def test_predict_returns_binary_label(sample_employee):
    """Vérifie que predict renvoie une unique prédiction binaire (0 ou 1)."""
    df = pd.DataFrame([sample_employee])
    prediction = model_manager.predict(df)

    assert len(prediction) == 1
    assert int(prediction[0]) in (0, 1)


def test_predict_proba_sums_to_one(sample_employee):
    """
    Vérifie que predict_proba renvoie deux probabilités
    (classes 0 et 1) dont la somme vaut 1.
    """
    df = pd.DataFrame([sample_employee])
    proba = model_manager.predict_proba(df)[0]

    assert len(proba) == 2
    assert abs(float(proba.sum()) - 1.0) < 1e-6