from typing import Any

from .database import conectar
from .serializers import serializar_dueno, serializar_mascota


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


def guardar_ruta_qr_mascota(mascota_id: int, ruta_ficha: str) -> None:
    """Guarda la ruta de la ficha asociada al QR de una mascota."""
    with conectar() as conexion, conexion.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO mascota_qr (mascota_id, ruta_ficha)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE ruta_ficha = %s
            """,
            (mascota_id, ruta_ficha, ruta_ficha),
        )
