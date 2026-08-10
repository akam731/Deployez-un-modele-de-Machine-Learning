from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, Field


def to_upper(v):
    """
    Convertit les valeurs en majuscules pour que les données de type Literal soient non sensibles à la casse.
    """
    return v.strip().upper() if isinstance(v, str) else v


class PredictionRequest(BaseModel):
    """
    Schéma d'entrée pour la prédiction d'attrition.
    Colonnes des datasets SIRH, sondage et évaluation.
    Les Literal sont en majuscules et insensibles à la casse.
    """

    # SIRH
    age: int
    genre: Annotated[Literal["F", "M"], BeforeValidator(to_upper)]
    revenu_mensuel: Annotated[float, Field(gt=0)]
    statut_marital: Annotated[
        Literal["CÉLIBATAIRE", "MARIÉ(E)", "DIVORCÉ(E)"],
        BeforeValidator(to_upper),
    ]
    departement: Annotated[
        Literal["COMMERCIAL", "CONSULTING", "RESSOURCES HUMAINES"],
        BeforeValidator(to_upper),
    ]
    poste: Annotated[
        Literal[
            "CADRE COMMERCIAL",
            "ASSISTANT DE DIRECTION",
            "CONSULTANT",
            "TECH LEAD",
            "MANAGER",
            "SENIOR MANAGER",
            "REPRÉSENTANT COMMERCIAL",
            "DIRECTEUR TECHNIQUE",
            "RESSOURCES HUMAINES",
        ],
        BeforeValidator(to_upper),
    ]
    nombre_experiences_precedentes: Annotated[int, Field(ge=0)]
    annee_experience_totale: Annotated[int, Field(ge=0)]
    annees_dans_l_entreprise: Annotated[int, Field(ge=0)]
    annees_dans_le_poste_actuel: Annotated[int, Field(ge=0)]

    # Sondage
    nombre_participation_pee: Annotated[int, Field(ge=0)]
    nb_formations_suivies: Annotated[int, Field(ge=0)]
    distance_domicile_travail: Annotated[int, Field(ge=0)]
    niveau_education: Annotated[int, Field(ge=0)]
    domaine_etude: Annotated[
        Literal[
            "INFRA & CLOUD",
            "AUTRE",
            "TRANSFORMATION DIGITALE",
            "MARKETING",
            "ENTREPREUNARIAT",
            "RESSOURCES HUMAINES",
        ],
        BeforeValidator(to_upper),
    ]
    frequence_deplacement: Annotated[
        Literal["AUCUN", "OCCASIONNEL", "FREQUENT"],
        BeforeValidator(to_upper),
    ]
    annees_depuis_la_derniere_promotion: Annotated[int, Field(ge=0)]
    annes_sous_responsable_actuel: Annotated[int, Field(ge=0)]

    # Évaluation
    satisfaction_employee_environnement: Annotated[int, Field(ge=0)]
    note_evaluation_precedente: Annotated[int, Field(ge=0)]
    niveau_hierarchique_poste: Annotated[int, Field(ge=0)]
    satisfaction_employee_nature_travail: Annotated[int, Field(ge=0)]
    satisfaction_employee_equipe: Annotated[int, Field(ge=0)]
    satisfaction_employee_equilibre_pro_perso: Annotated[int, Field(ge=0)]
    note_evaluation_actuelle: Annotated[int, Field(ge=0)]
    heure_supplementaires: Annotated[
        Literal["OUI", "NON"],
        BeforeValidator(to_upper),
    ]
    augementation_salaire_precedente: Annotated[int, Field(ge=0)]


class BatchPredictionRequest(BaseModel):
    """
    Schéma d'entrée pour une prédiction d'attrition en lot.
    Contient une liste d'employés au format PredictionRequest.
    """

    employees: list[PredictionRequest]
