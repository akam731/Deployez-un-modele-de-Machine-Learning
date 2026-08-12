from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
from app.database.models import Base
import os

class database:

    engine = None

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

        # Tentative de connexion pour vérifier la connexion à la base de données
        try:
            self.engine.connect()
        except Exception as e:
            raise RuntimeError("Impossible de se connecter à la base de données.".format(e))