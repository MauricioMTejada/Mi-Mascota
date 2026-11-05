from typing import Any


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
    """Genera un QR en SVG con la vCard del dueño."""
    return generar_qr_svg_texto(generar_vcard(datos))


def generar_qr_svg_texto(contenido: str) -> bytes:
    """Genera un QR en SVG a partir de texto."""
    import qrcode
    import qrcode.image.svg

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
        image_factory=qrcode.image.svg.SvgPathImage,
    )
    qr.add_data(contenido)
    qr.make(fit=True)
    return qr.make_image().to_string()
