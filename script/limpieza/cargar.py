"""Carga del origen con tipos optimizados (nada mas)."""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from . import config


def hallar_csv_origen(proyecto: Path | None = None) -> Path:
    """Localiza el unico CSV original en ``<proyecto>/db``."""
    if proyecto is None:
        proyecto = config.PROYECTO
    csvs = sorted((proyecto / "db").glob("*.csv"))
    if len(csvs) != 1:
        raise FileNotFoundError(
            f"Se esperaba un unico CSV original en {proyecto / 'db'}, se hallaron {len(csvs)}"
        )
    return csvs[0]


def cargar_dataset(ruta_csv: Path | None = None) -> pd.DataFrame:
    """Lee el CSV original sin tocarlo y devuelve un DataFrame con dtypes categoricos.

    - ``ruta_csv``: ruta al archivo; si no se pasa, se localiza el unico CSV de ``db/``.
    """
    if ruta_csv is None:
        ruta_csv = hallar_csv_origen()

    t0 = time.perf_counter()
    df = pd.read_csv(
        ruta_csv,
        dtype=config.DTYPE_CATEGORICOS,
        parse_dates=[config.COLUMNA_FECHA],
        low_memory=False,
    )
    df[config.CLAVE_PRIMARIA[0]] = df[config.CLAVE_PRIMARIA[0]].astype("string")
    print(f"carga {Path(ruta_csv).name} OK en {time.perf_counter() - t0:.1f} s -> {df.shape}")
    return df