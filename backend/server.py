#!/usr/bin/env python3
"""
Servidor de la ficha de Duke.

Sirve el sitio estático y expone los datos guardados en MySQL:

    GET /api/dueno          -> primer dueño (compatibilidad con el frontend)
    GET /api/duenos         -> dueños con sus mascotas
    GET /api/duenos/<id>    -> dueño con sus mascotas
    GET /api/duenos/<id>/mascotas -> mascotas de un dueño
    GET /api/mascotas       -> listado de mascotas (filtro ?dueno_id=<id>)
    GET /api/mascotas/<id>  -> mascota con dueño, fotos y eventos médicos
    GET /api/qr             -> QR (SVG) del dueño (?dueno_id=<id> opcional)

Uso:
    python backend/server.py
    python backend/server.py --puerto 8080
"""

from __future__ import annotations

import argparse
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import pymysql
from pymysql.cursors import DictCursor

BACKEND_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BACKEND_DIR.parent / "frontend"
ENV_PATH = BACKEND_DIR / ".env"


def cargar_env(ruta: Path) -> None:
    """Carga variables desde un archivo .env sin dependencias externas."""
    if not ruta.is_file():
        return

    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue

        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip().strip("\"'"))


cargar_env(ENV_PATH)


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


def serializar_dueno(fila: dict[str, Any]) -> dict[str, Any]:
    """Convierte una fila de la tabla duenos al formato que usa la API."""
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "foto": fila["foto"],
        "contactos": {
            "whatsapp": {
                "texto": fila["whatsapp"],
                "url": fila["whatsapp_url"],
            },
            "telegram": {
                "texto": fila["telegram"],
                "url": fila["telegram_url"],
            },
            "facebook": {
                "texto": fila["facebook"],
                "url": fila["facebook_url"],
            },
            "instagram": {
                "texto": fila["instagram"],
                "url": fila["instagram_url"],
            },
            "tiktok": {
                "texto": fila["tiktok"],
                "url": fila["tiktok_url"],
            },
            "email": {
                "texto": fila["email"],
                "url": f"mailto:{fila['email']}" if fila["email"] else None,
            },
            "direccion": {
                "texto": fila["direccion"],
                "url": "",
            },
        },
    }


def serializar_mascota(fila: dict[str, Any]) -> dict[str, Any]:
    """Convierte una fila de la tabla mascotas al formato que usa la API."""
    return {
        "id": fila["id"],
        "dueno_id": fila["dueno_id"],
        "dueno_nombre": fila.get("dueno_nombre"),
        "nombre": fila["nombre"],
        "especie": fila["especie"],
        "raza": fila["raza"],
        "edad": fila["edad"],
        "fecha_nacimiento": (
            str(fila["fecha_nacimiento"]) if fila["fecha_nacimiento"] else None
        ),
        "foto": fila["foto"],
        "descripcion": fila["descripcion"],
        "personalidad": fila["personalidad"],
        "peso_kg": float(fila["peso_kg"]) if fila["peso_kg"] is not None else None,
        "altura_cm": (
            float(fila["altura_cm"]) if fila["altura_cm"] is not None else None
        ),
        "vacunas": fila["vacunas"],
        "alergias": fila["alergias"],
        "enfermedades": fila["enfermedades"],
        "veterinario": fila["veterinario"],
    }


def obtener_duenos() -> list[dict[str, Any]]:
    """Devuelve todos los dueños, cada uno con su lista de mascotas."""
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM duenos ORDER BY id")
        duenos = [serializar_dueno(fila) for fila in cursor.fetchall()]

        cursor.execute(
            """
            SELECT m.*, d.nombre AS dueno_nombre
            FROM mascotas m
            JOIN duenos d ON d.id = m.dueno_id
            ORDER BY m.dueno_id, m.id
            """
        )

        mascotas_por_dueno: dict[int, list[dict[str, Any]]] = {}
        for fila in cursor.fetchall():
            mascotas_por_dueno.setdefault(fila["dueno_id"], []).append(
                serializar_mascota(fila)
            )

        for dueno in duenos:
            dueno["mascotas"] = mascotas_por_dueno.get(dueno["id"], [])
            dueno["total_mascotas"] = len(dueno["mascotas"])

        return duenos


def obtener_dueno(dueno_id: int | None = None) -> dict[str, Any] | None:
    with conectar() as conexion, conexion.cursor() as cursor:
        if dueno_id is None:
            cursor.execute("SELECT * FROM duenos ORDER BY id LIMIT 1")
        else:
            cursor.execute("SELECT * FROM duenos WHERE id = %s", (dueno_id,))

        fila = cursor.fetchone()
        return serializar_dueno(fila) if fila else None


def obtener_dueno_detalle(dueno_id: int) -> dict[str, Any] | None:
    dueno = obtener_dueno(dueno_id)
    if dueno is None:
        return None

    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT m.*, d.nombre AS dueno_nombre
            FROM mascotas m
            JOIN duenos d ON d.id = m.dueno_id
            WHERE m.dueno_id = %s
            ORDER BY m.id
            """,
            (dueno_id,),
        )
        dueno["mascotas"] = [serializar_mascota(fila) for fila in cursor.fetchall()]

    return dueno


def obtener_mascotas(dueno_id: int | None = None) -> list[dict[str, Any]]:
    """Devuelve las mascotas, opcionalmente filtradas por dueño."""
    consulta = """
        SELECT m.*, d.nombre AS dueno_nombre
        FROM mascotas m
        JOIN duenos d ON d.id = m.dueno_id
    """
    parametros: tuple[Any, ...] = ()

    if dueno_id is not None:
        consulta += " WHERE m.dueno_id = %s"
        parametros = (dueno_id,)

    consulta += " ORDER BY m.id"

    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(consulta, parametros)
        return [serializar_mascota(fila) for fila in cursor.fetchall()]


def obtener_mascota(mascota_id: int) -> dict[str, Any] | None:
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            SELECT m.*, d.nombre AS dueno_nombre
            FROM mascotas m
            JOIN duenos d ON d.id = m.dueno_id
            WHERE m.id = %s
            """,
            (mascota_id,),
        )
        fila = cursor.fetchone()
        if fila is None:
            return None

        mascota = serializar_mascota(fila)

        cursor.execute("SELECT * FROM duenos WHERE id = %s", (mascota["dueno_id"],))
        dueno_fila = cursor.fetchone()
        mascota["dueno"] = serializar_dueno(dueno_fila) if dueno_fila else None

        cursor.execute(
            """
            SELECT id, ruta, descripcion, orden
            FROM mascota_fotos
            WHERE mascota_id = %s
            ORDER BY orden, id
            """,
            (mascota_id,),
        )
        mascota["fotos"] = cursor.fetchall()

        cursor.execute(
            """
            SELECT id, tipo, descripcion, fecha
            FROM mascota_eventos_medicos
            WHERE mascota_id = %s
            ORDER BY fecha DESC, id DESC
            """,
            (mascota_id,),
        )
        eventos = cursor.fetchall()
        for evento in eventos:
            evento["fecha"] = str(evento["fecha"]) if evento["fecha"] else None
        mascota["eventos_medicos"] = eventos

    return mascota


def generar_vcard(datos: dict[str, Any]) -> str:
    """Arma el contenido vCard que se codifica dentro del QR."""
    contactos = datos.get("contactos", {})
    lineas = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{datos.get('nombre', '')}",
    ]

    whatsapp = contactos.get("whatsapp", {}).get("texto")
    if whatsapp:
        lineas.append(f"TEL;TYPE=CELL:{whatsapp}")

    email = contactos.get("email", {}).get("texto")
    if email:
        lineas.append(f"EMAIL:{email}")

    direccion = contactos.get("direccion", {}).get("texto")
    if direccion:
        lineas.append(f"ADR:;;{direccion};;;;")

    for red in ("telegram", "facebook", "instagram", "tiktok"):
        url = contactos.get(red, {}).get("url")
        if url:
            lineas.append(f"URL:{url}")

    lineas.append("END:VCARD")
    return "\r\n".join(lineas)


def generar_qr_svg(datos: dict[str, Any]) -> bytes:
    """Genera un QR en SVG a partir de los datos del dueño."""
    import qrcode
    import qrcode.image.svg

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
        image_factory=qrcode.image.svg.SvgPathImage,
    )
    qr.add_data(generar_vcard(datos))
    qr.make(fit=True)
    return qr.make_image().to_string()


class Manejador(SimpleHTTPRequestHandler):
    """Sirve archivos estáticos y los endpoints de la API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def do_GET(self) -> None:
        url = urlparse(self.path)
        ruta = url.path.rstrip("/") or "/"

        try:
            if ruta == "/api/dueno":
                self._responder_o_404(obtener_dueno(), "No hay dueños cargados")
            elif ruta == "/api/duenos":
                self._responder_json(obtener_duenos())
            elif ruta.startswith("/api/duenos/") and ruta.endswith("/mascotas"):
                self._responder_mascotas_de_dueno(ruta)
            elif ruta.startswith("/api/duenos/"):
                self._responder_dueno(ruta)
            elif ruta == "/api/mascotas":
                self._responder_lista_mascotas(url.query)
            elif ruta.startswith("/api/mascotas/"):
                self._responder_mascota(ruta)
            elif ruta == "/api/qr":
                self._responder_qr(url.query)
            else:
                super().do_GET()
        except pymysql.MySQLError as error:
            self._responder_json(
                {
                    "error": "Error al consultar la base de datos",
                    "detalle": str(error),
                },
                estado=500,
            )

    def _responder_lista_mascotas(self, query: str) -> None:
        dueno_param = parse_qs(query).get("dueno_id", [None])[0]

        if dueno_param is None:
            self._responder_json(obtener_mascotas())
            return

        if not dueno_param.isdigit():
            self._responder_json({"error": "dueno_id inválido"}, estado=400)
            return

        self._responder_json(obtener_mascotas(int(dueno_param)))

    def _responder_mascotas_de_dueno(self, ruta: str) -> None:
        resto = ruta[len("/api/duenos/") :]
        partes = resto.split("/")

        if len(partes) != 2 or partes[1] != "mascotas" or not partes[0].isdigit():
            self._responder_json({"error": "Ruta inválida"}, estado=400)
            return

        dueno_id = int(partes[0])
        if obtener_dueno(dueno_id) is None:
            self._responder_json(
                {"error": f"No existe el dueño {dueno_id}"},
                estado=404,
            )
            return

        self._responder_json(obtener_mascotas(dueno_id))

    def _responder_dueno(self, ruta: str) -> None:
        dueno_id = self._id_de_ruta(ruta, "/api/duenos/")
        if dueno_id is None:
            self._responder_json({"error": "ID inválido"}, estado=400)
            return
        self._responder_o_404(
            obtener_dueno_detalle(dueno_id),
            f"No existe el dueño {dueno_id}",
        )

    def _responder_mascota(self, ruta: str) -> None:
        mascota_id = self._id_de_ruta(ruta, "/api/mascotas/")
        if mascota_id is None:
            self._responder_json({"error": "ID inválido"}, estado=400)
            return
        self._responder_o_404(
            obtener_mascota(mascota_id),
            f"No existe la mascota {mascota_id}",
        )

    def _responder_qr(self, query: str) -> None:
        dueno_param = parse_qs(query).get("dueno_id", [None])[0]

        if dueno_param is not None and not dueno_param.isdigit():
            self._responder_json({"error": "dueno_id inválido"}, estado=400)
            return

        dueno = (
            obtener_dueno(int(dueno_param))
            if dueno_param is not None
            else obtener_dueno()
        )

        if dueno is None:
            self._responder_o_404(None, "No hay dueños cargados")
            return

        try:
            svg = generar_qr_svg(dueno)
        except Exception as error:  # noqa: BLE001
            self.send_error(500, f"No se pudo generar el QR: {error}")
            return

        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Content-Length", str(len(svg)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(svg)

    def _responder_o_404(self, datos: Any, mensaje: str) -> None:
        if datos is None:
            self._responder_json({"error": mensaje}, estado=404)
        else:
            self._responder_json(datos)

    def _responder_json(self, datos: Any, estado: int = 200) -> None:
        cuerpo = json.dumps(datos, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    @staticmethod
    def _id_de_ruta(ruta: str, prefijo: str) -> int | None:
        resto = ruta[len(prefijo) :].strip("/")
        return int(resto) if resto.isdigit() else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor de la ficha de Duke")
    parser.add_argument("--host", default="0.0.0.0", help="Host (por defecto 0.0.0.0)")
    parser.add_argument(
        "--puerto",
        type=int,
        default=int(os.getenv("APP_PORT", "8000")),
        help="Puerto (por defecto 8000; configurable con APP_PORT)",
    )
    opciones = parser.parse_args()

    if not FRONTEND_DIR.is_dir():
        raise SystemExit(f"No se encontró la carpeta del frontend: {FRONTEND_DIR}")

    servidor = ThreadingHTTPServer((opciones.host, opciones.puerto), Manejador)
    print(f"Servidor iniciado en http://{opciones.host}:{opciones.puerto}")
    print("  Página:   /")
    print("  Dueño:    /api/dueno")
    print("  Dueños:   /api/duenos")
    print("  Mascotas: /api/mascotas")
    print("  QR:       /api/qr")
    print("Presioná Ctrl+C para detenerlo.")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
