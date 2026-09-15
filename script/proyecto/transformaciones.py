"""Transformaciones: agregaciones por region/ciudad, anomalias climaticas y
salario joven (banda 18-34) nacional y regionalizado."""
from __future__ import annotations

import pandas as pd

from . import config


def agregado_precios_region(df: pd.DataFrame) -> pd.DataFrame:
    """F1 -> (anio, region): n, precio medio y mediana (price ya winsorizada)."""
    df = df[df["year"] >= config.ANIO_MIN_PRECIOS]
    g = df.groupby(["year", "region"], observed=True).agg(
        n_transacciones=("price", "size"),
        precio_medio=("price", "mean"),
        precio_mediana=("price", "median"),
    ).reset_index().rename(columns={"year": "anio", "region": "region"})
    return g


def agregado_precios_ciudad(df: pd.DataFrame) -> pd.DataFrame:
    """F1 -> (anio, region, ciudad): mercado local (dimension ciudad)."""
    df = df[df["year"] >= config.ANIO_MIN_PRECIOS]
    g = df.groupby(["year", "region", "town_city"], observed=True).agg(
        n_transacciones=("price", "size"),
        precio_medio=("price", "mean"),
        precio_mediana=("price", "median"),
    ).reset_index().rename(columns={"year": "anio", "town_city": "ciudad"})
    return g


def clima_anual(df: pd.DataFrame) -> pd.DataFrame:
    """F3 -> (anio, estacion): promedios anuales (af es conteo -> suma)."""
    g = df.groupby(["anio", "estacion"], observed=True).agg(
        tmax=("tmax", "mean"),
        tmin=("tmin", "mean"),
        lluvia=("lluvia", "mean"),
        sol=("sol", "mean"),
        af=("af", "sum"),
    ).reset_index()
    return g


def anomalias_climaticas(anual: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Anomalia anual = valor del anio - normal historica de la estacion.

    Devuelve (anomalias_nacional, anomalias_region). La region solo existe para
    las estaciones de Inglaterra y Gales (F1 no cubre Escocia/Irlanda del Norte);
    las demas cuentan en el total nacional (36 estaciones).
    """
    normal = anual.groupby("estacion", observed=True)[
        ["tmax", "tmin", "lluvia", "sol", "af"]].transform("mean")
    anomalias = anual.copy()
    for col in ["tmax", "tmin", "lluvia", "sol", "af"]:
        anomalias[col + "_anom"] = anomalias[col] - normal[col]

    cols_anom = ["tmax_anom", "tmin_anom", "lluvia_anom", "sol_anom", "af_anom"]
    nacional = anomalias.groupby("anio")[cols_anom].mean().reset_index()

    info = anomalias[["anio", "estacion"] + cols_anom].copy()
    info["region"] = info["estacion"].map(config.ESTACION_REGION)
    regional = (info.dropna(subset=["region"])
                .groupby(["anio", "region"], observed=True)[cols_anom]
                .mean().reset_index())
    return nacional, regional


def salario_joven(ingreso: pd.DataFrame, precios: pd.DataFrame) -> tuple[float, float]:
    """Salario mediano joven (18-34): media simple de las medianas de las bandas
    18-21, 22-29 y 30-39 (promedio de genero por banda). Devuelve (salario, factor)
    donde factor = salario_joven / salario_mediana_nacional_2020."""
    tabla = (ingreso.groupby(["grupo_edad", "genero"], observed=True)["salario_mediana"]
             .mean().reset_index())
    por_banda = tabla.groupby("grupo_edad", observed=True)["salario_mediana"].mean()
    joven = float(por_banda[config.GRUPOS_JOVEN].mean())
    salario_2020 = float(precios.loc[precios["anio"] == 2020, "salario_mediana_real"].iloc[0])
    factor = joven / salario_2020
    return joven, factor


def serie_salario_joven(precios: pd.DataFrame, factor: float) -> pd.DataFrame:
    """F4 -> (anio, region): salario joven nacional (factor x mediana real del anio)
    y salario joven regionalizado con el factor ASHE 2021."""
    serie = precios[["anio", "salario_mediana_real"]].dropna().copy()
    serie["salario_joven_nacional"] = serie["salario_mediana_real"] * factor
    filas = []
    for region, factor in config.FACTOR_REGIONAL.items():
        r = serie.copy()
        r["region"] = region
        r["factor_regional"] = factor
        r["salario_joven_region"] = r["salario_joven_nacional"] * factor
        filas.append(r)
    return pd.concat(filas, ignore_index=True)


def historico_nacional(precios: pd.DataFrame, factor: float) -> pd.DataFrame:
    """Serie nacional 1999-2020 para el informe (precio, salario, salario joven)."""
    serie = precios.dropna(subset=["salario_mediana_real"]).copy()
    serie["salario_joven_nacional"] = serie["salario_mediana_real"] * factor
    return serie[["anio", "precio_promedio_real", "salario_mediana_real",
                  "salario_joven_nacional"]].reset_index(drop=True)