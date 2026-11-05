import json
from typing import Any

import pymysql
from flask import (
    Blueprint,
    current_app,
    redirect,
    request,
    send_from_directory,
    url_for,
)

from .config import BACKEND_DIR
from .qr import generar_qr_svg, generar_qr_svg_texto
from .repository import (
    guardar_ruta_qr_mascota,
    obtener_dueno,
    obtener_dueno_detalle,
    obtener_duenos,
    obtener_mascota,
    obtener_mascotas,
)

FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
api = Blueprint("api", __name__)


def respuesta_json(datos: Any, estado: int = 200):
    return current_app.response_class(
        json.dumps(datos, ensure_ascii=False, indent=2),
        status=estado,
        mimetype="application/json",
    )


def respuesta_o_404(datos: Any, mensaje: str):
    if datos is None:
        return respuesta_json({"error": mensaje}, estado=404)
    return respuesta_json(datos)


@api.route("/", methods=["GET"])
def inicio():
    if request.args.get("id") or request.args.get("mascota"):
        return redirect(
            url_for("static", filename="ficha.html", **request.args.to_dict())
        )
    return send_from_directory(FRONTEND_DIR, "index.html")


@api.route("/api/dueno", methods=["GET"])
def dueno():
    return respuesta_o_404(obtener_dueno(), "No hay dueños cargados")


@api.route("/api/duenos", methods=["GET"])
def duenos():
    return respuesta_json(obtener_duenos())


@api.route("/api/duenos/<dueno_id>/mascotas", methods=["GET"])
def mascotas_de_dueno(dueno_id: str):
    if not dueno_id.isdigit():
        return respuesta_json({"error": "Ruta inválida"}, estado=400)

    dueno_id_numero = int(dueno_id)
    if obtener_dueno(dueno_id_numero) is None:
        return respuesta_json(
            {"error": f"No existe el dueño {dueno_id_numero}"},
            estado=404,
        )

    return respuesta_json(obtener_mascotas(dueno_id_numero))


@api.route("/api/duenos/<dueno_id>", methods=["GET"])
def detalle_dueno(dueno_id: str):
    if not dueno_id.isdigit():
        return respuesta_json({"error": "ID inválido"}, estado=400)
    dueno_id_numero = int(dueno_id)
    return respuesta_o_404(
        obtener_dueno_detalle(dueno_id_numero),
        f"No existe el dueño {dueno_id_numero}",
    )


@api.route("/api/mascotas", methods=["GET"])
def lista_mascotas():
    dueno_id = request.args.get("dueno_id")
    if dueno_id is None:
        return respuesta_json(obtener_mascotas())
    if not dueno_id.isdigit():
        return respuesta_json({"error": "dueno_id inválido"}, estado=400)
    return respuesta_json(obtener_mascotas(int(dueno_id)))


@api.route("/api/mascotas/<mascota_id>", methods=["GET"])
def detalle_mascota(mascota_id: str):
    if not mascota_id.isdigit():
        return respuesta_json({"error": "ID inválido"}, estado=400)
    mascota_id_numero = int(mascota_id)
    return respuesta_o_404(
        obtener_mascota(mascota_id_numero),
        f"No existe la mascota {mascota_id_numero}",
    )


@api.route("/api/qr/mascota/<mascota_id>", methods=["GET"])
def qr_mascota(mascota_id: str):
    if not mascota_id.isdigit():
        return respuesta_json({"error": "ID inválido"}, estado=400)

    mascota_id_numero = int(mascota_id)
    if obtener_mascota(mascota_id_numero) is None:
        return respuesta_o_404(
            None,
            f"No existe la mascota {mascota_id_numero}",
        )

    ruta_ficha = url_for(
        "static",
        filename="ficha.html",
        id=mascota_id_numero,
    )
    guardar_ruta_qr_mascota(mascota_id_numero, ruta_ficha)
    url_ficha = f"{request.url_root.rstrip('/')}{ruta_ficha}"
    svg = generar_qr_svg_texto(url_ficha)
    return current_app.response_class(svg, mimetype="image/svg+xml")


@api.route("/api/qr", methods=["GET"])
def qr_dueno():
    dueno_id = request.args.get("dueno_id")
    if dueno_id is not None and not dueno_id.isdigit():
        return respuesta_json({"error": "dueno_id inválido"}, estado=400)

    dueno_datos = (
        obtener_dueno(int(dueno_id)) if dueno_id is not None else obtener_dueno()
    )
    if dueno_datos is None:
        return respuesta_o_404(None, "No hay dueños cargados")

    svg = generar_qr_svg(dueno_datos)
    return current_app.response_class(svg, mimetype="image/svg+xml")
