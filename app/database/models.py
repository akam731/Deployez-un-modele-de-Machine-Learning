from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


def utcnow():
    """Retourne la date/heure actuelle en UTC"""
    return datetime.now(timezone.utc)


class EmployeeFeatures:
    """
    Colonnes features partagées (alignées sur PredictionRequest).
    Héritées par Inputs pour éviter la duplication.
    """

    # SIRH
    age = Column(Integer, nullable=False)
    genre = Column(String(1), nullable=False)
    revenu_mensuel = Column(Float, nullable=False)
    statut_marital = Column(String(50), nullable=False)
    departement = Column(String(50), nullable=False)
    poste = Column(String(100), nullable=False)
    nombre_experiences_precedentes = Column(Integer, nullable=False)
    annee_experience_totale = Column(Integer, nullable=False)
    annees_dans_l_entreprise = Column(Integer, nullable=False)
    annees_dans_le_poste_actuel = Column(Integer, nullable=False)

    # Sondage
    nombre_participation_pee = Column(Integer, nullable=False)
    nb_formations_suivies = Column(Integer, nullable=False)
    distance_domicile_travail = Column(Integer, nullable=False)
    niveau_education = Column(Integer, nullable=False)
    domaine_etude = Column(String(100), nullable=False)
    frequence_deplacement = Column(String(50), nullable=False)
    annees_depuis_la_derniere_promotion = Column(Integer, nullable=False)
    annes_sous_responsable_actuel = Column(Integer, nullable=False)

    # Évaluation
    satisfaction_employee_environnement = Column(Integer, nullable=False)
    note_evaluation_precedente = Column(Integer, nullable=False)
    niveau_hierarchique_poste = Column(Integer, nullable=False)
    satisfaction_employee_nature_travail = Column(Integer, nullable=False)
    satisfaction_employee_equipe = Column(Integer, nullable=False)
    satisfaction_employee_equilibre_pro_perso = Column(Integer, nullable=False)
    note_evaluation_actuelle = Column(Integer, nullable=False)
    heure_supplementaires = Column(String(3), nullable=False)
    augementation_salaire_precedente = Column(Integer, nullable=False)


class Inputs(EmployeeFeatures, Base):
    """Entrées du modèle : dataset de référence ou requêtes API."""

    __tablename__ = "inputs"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(20), nullable=False, default="api")
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    output = relationship(
        "Outputs",
        back_populates="input",
        uselist=False,
    )


class Outputs(Base):
    """Sorties du modèle, liées à un input."""

    __tablename__ = "outputs"

    id = Column(Integer, primary_key=True, index=True)
    prediction = Column(Integer, nullable=False)  # 0 ou 1
    probability = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    input_id = Column(
        Integer,
        ForeignKey("inputs.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    input = relationship("Inputs", back_populates="output")
