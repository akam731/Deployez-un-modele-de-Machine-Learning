#######################################
# Tests fonctionnels sur la DB
#######################################
from sqlalchemy import text
from app.database.database import database

def test_ping():
    """Vérifie que la base de données est bien trouvée"""
    db = database()
    with db.engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1