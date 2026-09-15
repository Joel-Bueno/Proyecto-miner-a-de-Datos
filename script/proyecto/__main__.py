"""Punto de entrada del paquete: python -m script.proyecto"""
from __future__ import annotations

from .pipeline import PipelineProyecto


def main() -> None:
    """Ejecuta el pipeline completo del analisis de accesibilidad joven."""
    PipelineProyecto().run()


if __name__ == "__main__":
    main()