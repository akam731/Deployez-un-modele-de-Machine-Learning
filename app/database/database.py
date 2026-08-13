from sqlalchemy import create_engine, text, Engine, inspect
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
import os
import sys

from app.database.db_connexion import db_connexion
from app.database.models import Base

class database:

    engine = None
    conn : db_connexion

    def __init__(self, database_url = None):
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
        except Exception as e:
            raise RuntimeError("Impossible de se connecter à la base de données.") from e


    def setup_tables(self, force: bool = False) -> bool :
        """
        Crée les tables d'une base de données en passant par la méthode static create_tables
        :param force:
        :return:
        """
        return database.create_tables(self.engine, force)

    @staticmethod
    def create_tables(engine: Engine, force: bool = False) -> bool :
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
                else :
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
                    text("SELECT 1 FROM pg_database WHERE datname = :name"),{"name": conn_params.db_name},).scalar()

                if exists:
                    return False

                # Création de la base de données
                conn.execute( text(f'CREATE DATABASE "{conn_params.db_name}"'))

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