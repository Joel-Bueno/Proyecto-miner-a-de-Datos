"""Archivo principal del proyecto: ejecuta el analisis de accesibilidad joven.

Uso desde la raiz del proyecto:
    python main_proyecto.py

Orquesta ``PipelineProyecto`` (script/proyecto/pipeline.py), que cruza las 4
fuentes (transacciones, hipotecas, clima y precios/salario) en el cuadro
maestro_joven_uk (anio x region) en 8 partes, y entrega las salidas en
data/limpia + data/integrado, las figuras en md/figuras y la bitacora en
md/BITACORA_DECISIONES.md.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "script"))

from proyecto.pipeline import PipelineProyecto  # noqa: E402


def main() -> None:
    PipelineProyecto().run()


if __name__ == "__main__":
    main()