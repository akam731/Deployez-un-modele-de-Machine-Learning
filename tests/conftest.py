#######################################
# Fixtures partagées (chargées auto par pytest)
#######################################

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Client de test FastAPI pour appeler les endpoints sans serveur réel."""
    return TestClient(app)


@pytest.fixture
def sample_employee():
    """
    Employé plausible (JSON valide PredictionRequest)
    réutilisé dans les tests d'API et de model_manager.
    """
    return {
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
        "augementation_salaire_precedente": 11,
    }
