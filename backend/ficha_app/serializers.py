from typing import Any


def serializar_dueno(fila: dict[str, Any]) -> dict[str, Any]:
    """Convierte una fila de la tabla duenos al formato que usa la API."""
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "foto": fila["foto"],
        "contactos": {
            "whatsapp": {"texto": fila["whatsapp"], "url": fila["whatsapp_url"]},
            "telegram": {"texto": fila["telegram"], "url": fila["telegram_url"]},
            "facebook": {"texto": fila["facebook"], "url": fila["facebook_url"]},
            "instagram": {"texto": fila["instagram"], "url": fila["instagram_url"]},
            "tiktok": {"texto": fila["tiktok"], "url": fila["tiktok_url"]},
            "email": {
                "texto": fila["email"],
                "url": f"mailto:{fila['email']}" if fila["email"] else None,
            },
            "direccion": {"texto": fila["direccion"], "url": ""},
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
