#######################################
# Tests unitaires de db_connexion
#######################################
import pytest
from app.database.db_connexion import db_connexion


def test_db_connexion_parses_valid_url():
    """URL valide : host, user, password, db_name et port sont extraits."""
    conn = db_connexion("postgresql://laura:secret@localhost:7111/ma_base")

    assert conn.host == "localhost"
    assert conn.port == 7111
    assert conn.user == "laura"
    assert conn.password == "secret"
    assert conn.db_name == "ma_base"
    assert conn.url.database == "ma_base"


def test_db_connexion_default_port():
    """Sans port dans l'URL : port par défaut 5432."""
    conn = db_connexion("postgresql://alice:secret@localhost/ma_base")
    assert conn.port == 5432


def test_db_connexion_invalid_url_raises():
    """URL illisible : ValueError."""
    with pytest.raises(ValueError):
        db_connexion("pas-une-url")


def test_db_connexion_incomplete_url_raises():
    """URL sans mot de passe : ValueError."""
    with pytest.raises(ValueError):
        db_connexion("postgresql://alice@localhost/ma_base")



#######################################
# Tests fonctionnels sur la DB
#######################################
from sqlalchemy import inspect
from app.database.database import database
from app.database.models import Base
import os
import uuid
from sqlalchemy.engine import make_url


def db_url() -> str:
    """ Récupère la chaîne de connexion définie dans la variable d'environnement
    DATABASE_URL et remplace le nom de la base de données afin de créer une base
    unique et temporaire dédiée aux tests. Cela permet d'exécuter les tests sans
    impacter les bases de données existantes.
    """
    base = os.environ["DATABASE_URL"]
    url = make_url(base)
    test_db_name =  f"test_technova_db_{uuid.uuid4().hex}"
    print(f"Tests réalisés sur la base de données : {test_db_name}")
    return url.set(database=test_db_name).render_as_string(hide_password=False)

def test_create_db_and_drop_db_cycle():
    """
    Base absente - create_db True
    déjà là - create_db False
    drop_db True
    drop à nouveau - False.
    """
    url = db_url()
    assert database.drop_db(url) is bool  # nettoyage éventuel d'un run précédent
    assert database.create_db(url) is True
    assert database.create_db(url) is False
    assert database.drop_db(url) is True
    assert database.drop_db(url) is False

def test_create_db_invalid_url_raises():
    """URL invalide : ValueError via db_connexion."""
    with pytest.raises(ValueError):
        database.create_db("invalid")


def test_create_tables_on_empty_db():
    """Schéma absent : create_tables(force=False) crée les tables et retourne True."""
    db = database()
    Base.metadata.drop_all(bind=db.engine)

    assert database.create_tables(db.engine, force=False) is True

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing


def test_create_tables_refuses_without_force():
    """Schéma déjà présent : create_tables(force=False) retourne False sans drop."""
    db = database()
    database.create_tables(db.engine, force=True)

    assert database.create_tables(db.engine, force=False) is False

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing


def test_create_tables_force_recreates():
    """Schéma déjà présent : create_tables(force=True) recrée les tables et retourne True."""
    db = database()
    database.create_tables(db.engine, force=True)

    assert database.create_tables(db.engine, force=True) is True

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing