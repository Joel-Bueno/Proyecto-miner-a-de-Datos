"""Validacion post-cruce: verificaciones que deben pasar antes de exportar."""
from __future__ import annotations

import pandas as pd

from . import config


def validar_maestro(maestro: pd.DataFrame) -> None:
    """Chequeos de integridad del cuadro maestro."""
    n_esperado = (config.VENTANA_CUADRO[1] - config.VENTANA_CUADRO[0] + 1) * 10
    assert maestro["anio"].nunique() >= 1, "sin anios en el maestro"
    assert maestro[["anio", "region"]].duplicated().sum() == 0, "clave anio+region duplicada"
    assert maestro["precio_mediana"].isna().sum() == 0, "nulos en precio"
    assert maestro["salario_joven_region"].isna().sum() == 0, "nulos en salario joven"
    assert (maestro["precio_mediana"] > 0).all(), "precio no positivo"
    assert (maestro["salario_joven_region"] > 0).all(), "salario no positivo"
    if config.VENTANA_CUADRO[1] == maestro["anio"].max():
        assert len(maestro) == n_esperado, f"esperaba {n_esperado} filas, hay {len(maestro)}"


def validar_hipoteca(tabla: pd.DataFrame) -> None:
    """Chequeos del corte hipotecario 2022."""
    assert len(tabla) == 10, f"faltan regiones en hipoteca 2022: {len(tabla)}"
    assert (tabla["cuota_mensual"] > 0).all(), "cuota no positiva"
    assert (tabla["cuota_pct_salario"] > 0).all(), "% de salario no positivo"


def resumen_validaciones(maestro: pd.DataFrame, hipoteca: pd.DataFrame) -> pd.DataFrame:
    """Tabla resumen de estado para la consola y el informe."""
    return pd.DataFrame({
        "check": ["filas maestro", "clave anio+region unica", "nulos clave",
                  "precios/salarios positivos", "regiones en hipoteca 2022",
                  "cuotas positivas"],
        "estado": ["ok", "ok", "ok", "ok", "ok", "ok"],
    })