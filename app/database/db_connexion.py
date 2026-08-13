from sqlalchemy import URL
from sqlalchemy.engine import make_url

class db_connexion:
    """
    Contient les données de connexion à une base de données.
    Utilisée notamment par create_db et drop_db.
    """

    str_con: str
    host: str
    port: int
    user: str
    password: str
    db_name: str
    url : URL

    def __init__(self, str_con: str):
        """
        Crée une connexion à partir d'une chaîne de connexion.

        :param str_con: Chaîne de connexion PostgreSQL
        """

        try:
            url = make_url(str_con)
        except Exception as e:
            raise ValueError(
                "Chaîne de connexion invalide. "
                "Format attendu : "
                "postgresql://utilisateur:motdepasse@hote:port/nom_base"
            ) from e

        host = url.host
        port = url.port or 5432
        user = url.username
        password = url.password
        db_name = url.database

        if (
            host is None
            or user is None
            or password is None
            or db_name is None
        ): raise ValueError("URL incomplète : host, user, password et nom de base requis.")

        self.str_con = str_con
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.url = url