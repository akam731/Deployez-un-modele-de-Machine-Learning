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
from pathlib import Path
from sqlalchemy import inspect, text
from app.database.database import database
from app.database.models import Base
import os
import uuid
from dotenv import load_dotenv
from sqlalchemy.engine import make_url


def make_temp_db_url() -> str:
    """
    Construit une URL vers une base temporaire unique (sans la créer).
    Réutilise host/user/password de DATABASE_URL
    """
    load_dotenv()

    base = os.getenv("DATABASE_URL")
    if not base:
        raise RuntimeError(
            "DATABASE_URL manquante. Définis-la dans .env ou l'environnement."
        )

    url = make_url(base)
    test_db_name = f"test_technova_db_{uuid.uuid4().hex}"
    print(f"Tests réalisés sur la base de données : {test_db_name}")
    return url.set(database=test_db_name).render_as_string(hide_password=False)


@pytest.fixture
def temp_db():
    """Crée une base temporaire, yield (db, url), puis la supprime toujours."""
    url = make_temp_db_url()
    database.create_db(url)
    db = database(url)
    try:
        yield db, url
    finally:
        database.drop_db(url)


def test_create_db_and_drop_db_cycle():
    """
    Base absente → create_db True ;
    déjà là → create_db False ;
    drop_db True ;
    drop à nouveau → False.
    """
    url = make_temp_db_url()
    try:
        database.drop_db(url)  # s'assurer qu'elle est absente
        assert database.create_db(url) is True
        assert database.create_db(url) is False
        assert database.drop_db(url) is True
        assert database.drop_db(url) is False
    finally:
        database.drop_db(url)


def test_create_db_invalid_url_raises():
    """URL invalide : ValueError via db_connexion."""
    with pytest.raises(ValueError):
        database.create_db("invalid")


def test_create_tables_on_empty_db(temp_db):
    """Schéma absent : create_tables(force=False) crée les tables et retourne True."""
    db, _url = temp_db
    Base.metadata.drop_all(bind=db.engine)

    assert database.create_tables(db.engine, force=False) is True

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing


def test_create_tables_refuses_without_force(temp_db):
    """Schéma déjà présent : create_tables(force=False) retourne False sans drop."""
    db, _url = temp_db
    database.create_tables(db.engine, force=True)

    assert database.create_tables(db.engine, force=False) is False

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing


def test_create_tables_force_recreates(temp_db):
    """Schéma déjà présent : create_tables(force=True) recrée les tables et retourne True."""
    db, _url = temp_db
    database.create_tables(db.engine, force=True)

    assert database.create_tables(db.engine, force=True) is True

    existing = inspect(db.engine).get_table_names()
    for table in Base.metadata.tables:
        assert table in existing


def test_insert_values_loads_rows_into_datas(temp_db):
    """
    insert_values remplit la table datas à partir des 3 CSV.
    On recrée le schéma pour partir d'une table vide.
    """
    db, _url = temp_db
    database.create_tables(db.engine, force=True)
    result = db.insert_values()
    assert result is True
    with db.engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM datas")).scalar()
        target_values = conn.execute(
            text("SELECT DISTINCT a_quitte_l_entreprise FROM datas")
        ).scalars().all()
    assert count > 0
    assert set(target_values).issubset({0, 1})


def test_insert_values_row_has_expected_columns(temp_db):
    """Une ligne datas contient les features attendues (pas NULL sur un champ clé)."""
    db, _url = temp_db
    database.create_tables(db.engine, force=True)
    db.insert_values()
    with db.engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT age, genre, revenu_mensuel, departement,
                       a_quitte_l_entreprise, augementation_salaire_precedente
                FROM datas
                LIMIT 1
                """
            )
        ).mappings().one()
    assert row["age"] is not None
    assert row["genre"] in ("F", "M")
    assert row["revenu_mensuel"] > 0
    assert row["departement"] is not None
    assert row["a_quitte_l_entreprise"] in (0, 1)
    assert row["augementation_salaire_precedente"] >= 0