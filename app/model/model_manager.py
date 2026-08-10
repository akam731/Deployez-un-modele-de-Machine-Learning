from pathlib import Path

import joblib
import pandas as pd


class model_manager:
    """Charge le modèle une seule fois (singleton) et le réexpose partout."""

    _model = None
    _model_path = Path(__file__).resolve().parent / "model.joblib"

    _ONE_HOT_COLS = [
        "statut_marital",
        "departement",
        "poste",
        "domaine_etude",
    ]

    _CATEGORY_COLS = [
        "statut_marital",
        "departement",
        "poste",
        "domaine_etude",
        "frequence_deplacement",
        "heure_supplementaires",
    ]

    ####################
    # Méthodes de classe
    ####################
    @classmethod
    def get_model(cls):
        """Retourne le modèle chargé."""
        if cls._model is None:
            cls._model = joblib.load(cls._model_path)
        return cls._model

    @classmethod
    def preprocess(cls, X: pd.DataFrame) -> pd.DataFrame:
        """Feature engineering + encodage + alignement des colonnes du modèle."""
        X = X.copy()
        X = cls.normalize_categories(X)
        X = cls.feature_engineering(X)
        X = cls.encoding(X)
        expected = list(cls.get_model().feature_names_in_)
        return X.reindex(columns=expected, fill_value=0)

    @classmethod
    def predict(cls, X):
        """Retourne les prédictions binaires (0/1)."""
        X = cls.preprocess(X)
        return cls.get_model().predict(X)

    @classmethod
    def predict_proba(cls, X):
        """Retourne les probabilités associées à chaque classe."""
        X = cls.preprocess(X)
        return cls.get_model().predict_proba(X)

    ####################
    # Préprocessing
    ####################
    @staticmethod
    def to_training_case(value: str) -> str:
        """
        Passe une catégorie en Title Case pour coller au dataset d'entraînement.
        """
        value = str(value).strip().title()
        # Ajustements pour coller exactement aux attentes du modèle
        value = value.replace("(E)", "(e)")
        value = value.replace(" De ", " de ")
        return value

    @classmethod
    def normalize_categories(cls, X: pd.DataFrame) -> pd.DataFrame:
        """
        Normalise les valeurs catégorielles pour coller au dataset d'entraînement.
        :param X: Données d'entrée du modèle
        :return: DataFrame avec les mêmes colonnes, mais avec les valeurs catégorielles normalisées
        """
        for col in cls._CATEGORY_COLS:
            if col in X.columns:
                X[col] = X[col].map(cls.to_training_case)
        return X

    @staticmethod
    def feature_engineering(X: pd.DataFrame) -> pd.DataFrame:
        """
        Réalise le feature engineering sur les données d'entrée pour préparer l'inférence.
        :param X: Données d'entrée
        :return: DataFrame après feature engineering
        """
        X["fidelite"] = (
            X["annees_dans_l_entreprise"]
            / (X["annee_experience_totale"] + 1)
        )

        X["ratio_experience_age"] = (
            X["annee_experience_totale"] / X["age"]
        )

        satisfaction_cols = [
            "satisfaction_employee_environnement",
            "satisfaction_employee_nature_travail",
            "satisfaction_employee_equipe",
            "satisfaction_employee_equilibre_pro_perso",
        ]
        X["satisfaction_globale"] = X[satisfaction_cols].mean(axis=1)

        X["deja_promu"] = (
            X["annees_depuis_la_derniere_promotion"]
            < X["annees_dans_l_entreprise"]
        ).astype(int)

        return X

    @classmethod
    def encoding(cls, X: pd.DataFrame) -> pd.DataFrame:
        """
        Encode les colonnes non numériques pour qu'elles soient exploitables par le modèle.
        :param X: Données d'entrée
        :return: DataFrame contenant uniquement des colonnes numériques
        """
        # Colonnes binaires
        X["genre"] = X["genre"].apply(lambda x: 1 if x == "F" else 0)
        X["heure_supplementaires"] = X["heure_supplementaires"].apply(
            lambda x: 1 if x == "Oui" else 0
        )

        # Pourcentage éventuel en string → int
        if X["augementation_salaire_precedente"].dtype == object:
            X["augementation_salaire_precedente"] = (
                X["augementation_salaire_precedente"]
                .astype(str)
                .str.replace("%", "", regex=False)
                .astype(int)
            )

        # Ordinal encoding
        frequence_mapping = {
            "Aucun": 0,
            "Occasionnel": 1,
            "Frequent": 2,
        }
        X["frequence_deplacement"] = X["frequence_deplacement"].map(
            frequence_mapping
        )

        # One-hot encoding
        cols_to_encode = [c for c in cls._ONE_HOT_COLS if c in X.columns]
        if cols_to_encode:
            X = pd.get_dummies(
                X,
                columns=cols_to_encode,
                drop_first=True,
                dtype=int,
            )

        return X
