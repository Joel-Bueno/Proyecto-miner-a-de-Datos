"""Punto de entrada como modulo: python -m script.limpieza (desde la raiz del proyecto).

Equivalente a ejecutar main_limpieza.py; ambos llaman a PipelineLimpieza().run().
"""
from __future__ import annotations


def main() -> None:
    """Ejecuta el pipeline de limpieza de la fuente F1 (7 fases)."""
    from .pipeline import PipelineLimpieza

    PipelineLimpieza().run()


if __name__ == "__main__":
    main()