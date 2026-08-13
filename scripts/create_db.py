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

    # Insertion du dataset
    try:
        db.insert_values()
        print("Données insérées")
    except Exception as e:
        print(f"Une erreur est survenue lors de l'insertion des données : {e}")
        sys.exit(1)

    # TODO: Création des vues

    print("Terminé")


def create_tables(engine : Engine):
    """
    Crée les tables manquantes.
    Si reset=True : supprime puis recrée (détruit les données déjà présentes).
    """
    print("Création des tables.")
    try:
        if not database.create_tables(engine, False) :
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
            else:
                database.create_tables(engine, True)
                print("Tables créées")
    except Exception as e:
        print(f"Impossible de créer les tables : {e}")
        sys.exit(1)


def create_db(str_con: str) :
    """
    Crée la base de données à partir de sa chaine de connexion
    :param str_con: Chaine de connexion à la base de données
    """
    try:
        # On vérifie si la base de données existe déjà
        database(str_con)
        print("La base de données existe déjà.")
        return
    except :
        print("La base de données n'existe pas.")

    # Création de la base de données
    try:
        if database.create_db(str_con):
            print("Base de données créée avec succès.")
        else:
            print("La base de données existe déjà")
    except :
        print("Une erreur est survenue lors de la création de la base de données")
        sys.exit(1)



def get_con_str() -> str :
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

        if response == "n":
            print("Entrez la nouvelle chaîne de connexion : ", end="", flush=True)
            str_con = getpass("")
    else:
        # Aucune chaine de connexion trouvée
        str_con = getpass(
            "Aucune chaîne de connexion trouvée.\n"
            "Veuillez fournir la chaîne de connexion (postgresql://utilisateur:motdepasse@hote:port/nom_base) : "
        )

    return str_con


if __name__ == "__main__":
    main()