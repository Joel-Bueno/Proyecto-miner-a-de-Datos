"""Carga defensiva de las 4 fuentes con dtypes y nombres normalizados."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import config


def cargar_hipotecas() -> pd.DataFrame:
    """F2: productos hipotecarios (Kaggle, snapshot 2022)."""
    df = pd.read_csv(config.RUTA_HIPOTECAS, index_col=0, parse_dates=["SCAN_DATE"])
    df = df.rename(columns={
        "SKU": "sku",
        "BANK_NAME": "banco",
        "MTG_PRODUCT_SUBTITLE": "subtitulo",
        "MTG_PRODUCT_TYPE_RAW": "tipo_crudo",
        "MTG_PRODUCT_TYPE": "tipo",
        "MTG_PRODUCT_YEARS": "plazo_anios",
        "MTG_INITIAL_RATE_PCT": "tasa_inicial_pct",
        "MTG_APR_PCT": "apr_pct",
        "MTG_REVERT_RATE": "tasa_reversion",
        "MTG_FEES_TOTAL": "comisiones_total",
        "MTG_INITIAL_RATE_MONTHS": "meses_inicial",
        "SCAN_DATE": "fecha_escaneo",
        "TID": "tid",
    })
    df["sku"] = df["sku"].astype("str")
    df["tid"] = df["tid"].astype("str")
    return df[config.COLS_HIPOTECAS]


def cargar_clima() -> pd.DataFrame:
    """F3: series mensuales de 36 estaciones Met Office (1931-2020, Kaggle)."""
    df = pd.read_csv(config.RUTA_CLIMA, na_values=["NA", "---", "*", "#", ""])
    df = df.rename(columns={
        "year": "anio",
        "month": "mes",
        "tmax": "tmax",
        "tmin": "tmin",
        "af": "af",
        "rain": "lluvia",
        "sun": "sol",
        "station": "estacion",
    })
    df["estacion"] = df["estacion"].str.strip().str.lower().astype("category")
    return df


def cargar_precios_salario() -> pd.DataFrame:
    """F4a: precio medio y salario mediana nacionales ajustados a 2020 (1975-2020)."""
    df = pd.read_csv(config.RUTA_PRECIOS_SALARIO, na_values=["null"])
    df = df.dropna(subset=["Year"])
    df = df[["Year", "Average house price adj. by inflation (pounds)",
             "Median Salary adj. by inflation (pounds)"]].copy()
    df.columns = ["anio", "precio_promedio_real", "salario_mediana_real"]
    return df


def cargar_ingreso_edad() -> pd.DataFrame:
    """F4b: salario mediano por grupo de edad y genero (brecha salarial 2021)."""
    df = pd.read_csv(config.RUTA_INGRESO_EDAD)
    df.columns = ["grupo_edad", "salario_mediana", "genero"]
    return df


def cargar_precios_limpios() -> pd.DataFrame:
    """F1: transacciones ya limpias (parquet de data/limpia, winsorizado a cuartiles)."""
    return pd.read_parquet(config.RUTA_TRANSACCIONES_LIMPIO)