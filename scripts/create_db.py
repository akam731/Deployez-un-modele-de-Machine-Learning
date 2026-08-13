from sqlalchemy import Engine
from dotenv import load_dotenv
from app.database.database import database
from getpass import getpass
import os
import sys
import argparse

# Constantes de couleur pour les messages
RED = "\033[91m"
RESET = "\033[0m"

def parse_args():
    """
    Permer de paser les arguments fournis à la fonction main lors de la commande : uv run python -m scripts.create_db "str" --force
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "database_url",
        nargs="?",
        default=None,
        help="Fournis la chaine de connexion à la base de données souhaitée",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Sans cette attribut on passe en mode intéractif",
    )
    return parser.parse_args()

def main():
    """ Gère le processus complet de la création de la base de données """
    args = parse_args()

    # Récupère la chaine de connexion
    if args.force:
        # Mode non interactif
        str_con = args.database_url or os.getenv("DATABASE_URL")
        if not str_con:
            load_dotenv()
            str_con = os.getenv("DATABASE_URL")
        if not str_con:
            print("Mode --force : veuillez fournir database_url en paramètre ou DATABASE_URL dans le .env.")
            sys.exit(1)
    else:
        # Mode interactif (getpass / input)
        str_con = get_con_str()

    # Création de la base de données
    create_db(str_con)

    # Création des tables
    db = database(str_con)
    if args.force:
        print("Création des tables (--force).")
        database.create_tables(db.engine, force=True)
        print("Tables créées")
    else:
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