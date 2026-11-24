"""Punto de entrada estable para consola e interfaz gráfica."""

import sys

from src.cli import ejecutar


def main() -> int:
    # Salida Unicode consistente en Windows, Linux y terminales redirigidas.
    for flujo in (sys.stdout, sys.stderr):
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8")
    return ejecutar()


if __name__ == "__main__":
    raise SystemExit(main())
