import pymysql
from flask import Flask, request

from .config import BACKEND_DIR
from .routes import api, respuesta_json

FRONTEND_DIR = BACKEND_DIR.parent / "frontend"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
    app.register_blueprint(api)

    @app.after_request
    def desactivar_cache_api(respuesta):
        if request.path.startswith("/api/"):
            respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @app.errorhandler(pymysql.MySQLError)
    def error_base_de_datos(error: pymysql.MySQLError):
        return respuesta_json(
            {
                "error": "Error al consultar la base de datos",
                "detalle": str(error),
            },
            estado=500,
        )

    return app
