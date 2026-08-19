from sqlalchemy import create_engine, text, Engine, inspect
from dotenv import load_dotenv
import os
from app.database.models import Inputs, Outputs
from sqlalchemy.orm import Session
import pandas as pd
from pathlib import Path
from app.database.db_connexion import db_connexion
from app.database.models import Base
from sqlalchemy.orm import sessionmaker


class database:
    """
    Class qui gère toutes les intéraction avec la base de données :
    création, suppression, création des tables, insertion des données...
    """

    conn: db_connexion  # Classe de connexion contenant toutes les informations de connexion de la base de données
    engine = None  # Moteur de la base de donnée (Permet la connexion)
    session: Session  # Session de connexion (Utilisé pour intéragir avec les données)

    def __init__(self, database_url=None):
        """
        Constructeur. Il vérifie et initialise la connexion avec la base de données
        :param database_url: Chaine de connexion à la base de données. Si vide, on récupère la variable d'environement DATABASE_URL
        """
        # Récupération de la chaine de connexion
        if database_url is None:
            load_dotenv()
            database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError("La variable d'environnement DATABASE_URL n'est pas définie")

        # Création du moteur de base de données
        self.engine = create_engine(database_url)
        # Création de la chaine de connexion
        self.conn = db_connexion(database_url)

        # Tentative de connexion pour vérifier la connexion à la base de données
        try:
            self.engine.connect()

            # Création de la session
            Session = sessionmaker(bind=self.engine)
            self.session = Session()

        except Exception as e:
            raise RuntimeError("Impossible de se connecter à la base de données.") from e

    def save_prediction(
            self,
            features: dict,
            prediction: int,
            probability: float,
    ) -> int:
        """
        Enregistre une entrée API (inputs) et sa sortie (outputs).
        Retourne l'id de l'input créé.
        """
        with Session(self.engine) as session:
            row_in = Inputs(**features, source="api")
            session.add(row_in)
            session.flush()

            row_out = Outputs(
                prediction=int(prediction),
                probability=float(probability),
                input_id=row_in.id,
            )
            session.add(row_out)
            session.commit()
            return row_in.id

    @staticmethod
    def load_dataset_dataframe() -> pd.DataFrame:
        """Charge et prépare le dataset de référence (CSV SIRH + sondages + eval)."""
        data_path = Path(__file__).parent.parent / "model" / "datas"
        try:
            sirh = pd.read_csv(data_path / "sirh.csv")
            eval_df = pd.read_csv(data_path / "eval.csv")
            sondages = pd.read_csv(data_path / "sondages.csv")
        except Exception as e:
            raise Exception(f"Les datasets ne sont pas accéssibles au chemin {data_path} ") from e

        sondages["id_employee"] = sondages["code_sondage"].astype(int)
        eval_df["id_employee"] = (
            eval_df["eval_number"].astype(str).str.replace("E_", "", regex=False).astype(int)
        )
        df = (
            sirh.merge(sondages, on="id_employee", how="inner")
            .merge(eval_df, on="id_employee", how="inner")
        )
        df["a_quitte_l_entreprise"] = (
            df["a_quitte_l_entreprise"].astype(str).str.strip().str.lower()
            .map({"oui": 1, "non": 0})
        )
        df["augementation_salaire_precedente"] = (
            df["augementation_salaire_precedente"]
            .astype(str).str.replace("%", "", regex=False).str.strip().astype(int)
        )
        return df

    def insert_values(self):
        """Insère le dataset de référence dans inputs + outputs (source=dataset)."""
        df = self.load_dataset_dataframe()
        feature_cols = [
            c.name
            for c in Inputs.__table__.columns
            if c.name not in ("id", "created_at", "source")
        ]

        with Session(self.engine) as session:
            for _, row in df.iterrows():
                features = {col: row[col] for col in feature_cols}
                label = int(row["a_quitte_l_entreprise"])
                row_in = Inputs(**features, source="dataset")
                session.add(row_in)
                session.flush()
                session.add(
                    Outputs(
                        prediction=label,
                        probability=1.0,
                        input_id=row_in.id,
                    )
                )
            session.commit()

        return True

    def create_views(self) -> None:
        """Exécute scripts/sql/create_views.sql (CREATE OR REPLACE VIEW)."""
        path = Path(__file__).resolve().parents[2] / "scripts" / "sql" / "create_views.sql"
        sql = path.read_text(encoding="utf-8")

        # Il y a plusieurs instructions donc on utilise un cursor dbapi
        with self.engine.begin() as conn:
            raw = conn.connection.dbapi_connection
            with raw.cursor() as cur:
                cur.execute(sql)

    def setup_tables(self, force: bool = False) -> bool:
        """
        Crée les tables d'une base de données en passant par la méthode static create_tables
        :param force:
        :return:
        """
        return database.create_tables(self.engine, force)

    @staticmethod
    def create_tables(engine: Engine, force: bool = False) -> bool:
        """
        Crée les tables manquantes. En les supprimant si elles existent déjà
        :return: statut de la création : True / False
        """
        try:
            inspector = inspect(engine)
            existing = inspector.get_table_names()
            expected = list(Base.metadata.tables.keys())
            if any(table in existing for table in expected):
                if not force:
                    return False
                else:
                    with engine.begin() as conn:
                        conn.execute(text("DROP VIEW IF EXISTS vue_predictions CASCADE"))
                    Base.metadata.drop_all(bind=engine)

            Base.metadata.create_all(bind=engine)
            return True

        except Exception as e:
            raise Exception(f"Impossible de créer les tables") from e

    @staticmethod
    def create_db(str_con: str) -> bool:
        """
        Crée une base de données PostgreSQL à partir de sa chaîne de connexion.

        :param str_con: Chaîne de connexion à la base de données.
        :return:
            True = base créée
            False = base déjà existante
        """

        # Récupération des paramètres de connexion
        conn_params = db_connexion(str_con)

        # On se connecte à la base système "postgres"
        admin_url = conn_params.url.set(database="postgres")
        # On crée le moteur de connexion à cette base
        admin_engine = create_engine(
            admin_url,
            isolation_level="AUTOCOMMIT"
        )

        try:
            with admin_engine.connect() as conn:
                # Vérification de l'existence
                exists = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": conn_params.db_name}, ).scalar()

                if exists:
                    return False

                # Création de la base de données
                conn.execute(text(f'CREATE DATABASE "{conn_params.db_name}"'))

                return True
        finally:
            admin_engine.dispose()

    @staticmethod
    def drop_db(str_con: str) -> bool:
        """
        Supprime une base de données PostgreSQL à partir de sa chaîne de connexion. (Utilisée pour simplifier les tests)

        :param str_con: Chaîne de connexion à la base cible.
        :return:
            True = base supprimée
            False = base inexistante
        :raises ValueError: si l'URL est invalide ou incomplète.
        """

        # Récupération des paramètres de connexion
        conn_params = db_connexion(str_con)

        # Impossible de DROP la base sur laquelle on est connecté
        admin_url = conn_params.url.set(database="postgres")
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

        try:
            with admin_engine.connect() as conn:
                exists = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :name"),
                    {"name": conn_params.db_name},
                ).scalar()

                if not exists:
                    return False

                # Ferme les connexions actives sur la base cible
                conn.execute(
                    text(
                        """
                        SELECT pg_terminate_backend(pid)
                        FROM pg_stat_activity
                        WHERE datname = :name
                          AND pid <> pg_backend_pid()
                        """
                    ),
                    {"name": conn_params.db_name},
                )

                conn.execute(text(f'DROP DATABASE "{conn_params.db_name}"'))
                return True
        finally:
            admin_engine.dispose()


# Singleton pour la production pour ne pas répéter la fonction __init__ à chaque appel
_db_instance: database | None = None


def get_db() -> database:
    """Singleton : une seule connexion réutilisée par l'API."""
    global _db_instance
    if _db_instance is None:
        _db_instance = database()  # lit DATABASE_URL
    return _db_instance
