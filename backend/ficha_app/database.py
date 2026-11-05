import os

import pymysql
from pymysql.cursors import DictCursor


def conectar():
    """Abre una conexión a MySQL usando las variables de entorno."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DB", "ficha_mascotas"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )
