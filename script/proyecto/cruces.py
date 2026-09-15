"""Cruces: maestro_joven_uk (anio x region) y series integradas."""
from __future__ import annotations

import pandas as pd

from . import config


def cruce_maestro(precios_region: pd.DataFrame,
                  salario_region: pd.DataFrame,
                  anomalias_region: pd.DataFrame) -> pd.DataFrame:
    """Une precios (F1), salario joven regional (F4) y anomalias (F3) por
    (anio, region) dentro de la ventana de cruce completo VENTANA_CUADRO."""
    inicio, fin = config.VENTANA_CUADRO
    precios = precios_region[(precios_region["anio"] >= inicio) &
                             (precios_region["anio"] <= fin)]
    salario = salario_region[(salario_region["anio"] >= inicio) &
                             (salario_region["anio"] <= fin)]

    maestro = (precios.merge(salario, on=["anio", "region"], how="left")
                     .merge(anomalias_region, on=["anio", "region"], how="left"))

    maestro = maestro.sort_values(["region", "anio"]).reset_index(drop=True)
    maestro["precio_var_pct"] = (maestro.groupby("region", observed=True)
                                 ["precio_mediana"].pct_change() * 100)
    maestro["anos_salario"] = maestro["precio_mediana"] / maestro["salario_joven_region"]
    return maestro


def cruce_ciudades_tope(precios_ciudad: pd.DataFrame, ventana) -> pd.DataFrame:
    """Rango de los precios medios por ciudad en la ventana (para el informe)."""
    inicio, fin = ventana
    top = (precios_ciudad[(precios_ciudad["anio"] >= inicio) &
                          (precios_ciudad["anio"] <= fin)]
           .sort_values("precio_mediana", ascending=False)
           .groupby("region", observed=True)
           .head(5).reset_index(drop=True))
    return top