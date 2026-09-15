"""Archivo principal: un solo .py que ejecuta todo y muestra los resultados por partes.

Uso desde la raiz del proyecto:
    python main_limpieza.py

Orquesta ``PipelineLimpieza`` (script/limpieza/pipeline.py) que corre las 7 fases en
orden (cargar -> duplicados -> categorias -> faltantes -> outliers -> validar -> exportar)
e imprime cada parte con su diagnostico y la bitacora final.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "script"))

from limpieza.pipeline import PipelineLimpieza  # noqa: E402


def main() -> None:
    PipelineLimpieza().run()


if __name__ == "__main__":
    main()