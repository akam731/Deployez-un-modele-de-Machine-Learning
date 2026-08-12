from sqlalchemy import create_engine, text, inspect, Engine
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
from app.database.database import database
from app.database.models import Base
from getpass import getpass
import os
import sys

# Constantes de couleur pour les messages
RED = "\033[91m"
RESET = "\033[0m"


def main():
    """ Gère le processus complet de la création de la base de données """

    # Récupère la chaine de connexion
    str_con = get_con_str()

    # Création de la base de données
    create_db(str_con)

    # Création des tables
    db = database(str_con)
    create_tables(db.engine)

    # TODO: Insertion du dataset

    # TODO: Création des vues

    print("Terminé")


def create_tables(engine : Engine):
    """
    Crée les tables manquantes.
    Si reset=True : supprime puis recrée (destructif).
    """
    print("Création des tables.")
    try:
        inspector = inspect(engine)
        existing = inspector.get_table_names()
        expected = list(Base.metadata.tables.keys())
        if any(table in existing for table in expected):
            print(
                f"{RED}Au moins une table existe déjà. "
                f"Si elle contient des données, elles seront toutes supprimées. "
                f"Êtes-vous sûr de continuer ? (y/n){RESET}"
            )
            response = input().strip().lower()
            while response not in ("y", "n"):
                response = input("Réponse invalide. Veuillez répondre par y ou n : ").strip().lower()
            if response == "n":
                print("Opération annulée.")
                sys.exit(1)
            Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    except Exception as e:
        print(f"Impossible de créer les tables : {e}")
        sys.exit(1)


def create_db(str_con: str):
    """
    Crée la base de données à partir de sa chaine de connexion
    :param str_con: Chaine de connexion à la base de données
    """
    try:
        # On vérifie si la base de données existe déjà
        database(str_con)
        print("La base de données existe déjà.")
        return
    except Exception:
        print("La base de données n'existe pas.")

    # On extrait de la chaine de connexion les données de l'hôte et de la base de données
    try:
        url = make_url(str_con)
    except Exception:
        print("Chaine de connexion invalide, impossible de poursuivre le processus. \n"
              "Le bon format est : postgresql://utilisateur:motdepasse@hote:port/nom_base.")
        sys.exit(1)

    host = url.host
    port = url.port or 5432
    user = url.username
    password = url.password
    db_name = url.database

    if not all([host, user, password, db_name]):
        print("URL incomplète : host, user, password et nom de base requis")
        sys.exit(1)

    # Connexion au serveur
    admin_url = url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
        ).scalar()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Base '{db_name}' créée sur {host}:{port}.")

    print("Base de données créée avec succès.")


def get_con_str():
    """
    Récupère la chaine de connexion à la base de données
    :return: Chaine de connexion à la base de données
    """
    # Récupération d'une éventuelle chaine de connexion en variables d'environnements
    load_dotenv()
    str_con = os.getenv("DATABASE_URL")

    if str_con:
        # Chaine de connexion trouvée
        response = input(
            "Une chaîne de connexion a été trouvée. "
            "Voulez-vous l'utiliser ? (y/n) : "
        ).strip().lower()

        while response not in ("y", "n"):
            response = input(
                "Réponse invalide. Veuillez répondre par y ou n : "
            ).strip().lower()

        print("oui")
        if response == "n":
            print("non")
            print("Entrez la nouvelle chaîne de connexion : ", end="", flush=True)
            str_con = getpass("")
            print("\nChaîne récupérée !")
    else:
        # Aucune chaine de connexion trouvée
        str_con = getpass(
            "Aucune chaîne de connexion trouvée.\n"
            "Veuillez fournir la chaîne de connexion (postgresql://utilisateur:motdepasse@hote:port/nom_base) : "
        )

    return str_con


if __name__ == "__main__":
    main()