import oracledb

from app.core.config import settings

def get_connection():

    connection = oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=settings.ORACLE_DSN
    )

    return connection