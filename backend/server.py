#!/usr/bin/env python3
"""Punto de entrada para la aplicación Flask de Mi Mascota."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from backend.ficha_app import create_app
else:
    from .ficha_app import create_app

app = create_app()


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

    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
    if not frontend_dir.is_dir():
        raise SystemExit(f"No se encontró la carpeta del frontend: {frontend_dir}")

    app.run(
        host=opciones.host,
        port=opciones.puerto,
        debug=False,
        threaded=True,
    )


if __name__ == "__main__":
    main()
