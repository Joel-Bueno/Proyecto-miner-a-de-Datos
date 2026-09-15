"""Configuracion unica del modulo proyecto: rutas, fuentes y reglas de negocio.

Rutas resueltas desde este archivo hacia la raiz del proyecto (regla D5: rutas
relativas), por lo que el pipeline corre desde cualquier carpeta.

Esquema de fuentes (4 CSV):
  F1 transacciones   -> uk_property_price (ya limpio en data/limpia/*.parquet)
  F2 hipotecas       -> UK_Mortgage_Rate.csv            (Kaggle, snapshot 2022)
  F3 clima           -> MET_Office_Weather_Data.csv     (Met Office, 36 estaciones)
  F4 precios/salario -> Average_UK_houseprices_and_salary.csv + Income_by_age_and_gender.csv
"""
from __future__ import annotations

from pathlib import Path

PROYECTO = Path(__file__).resolve().parents[2]

DATA_CRUDO = PROYECTO / "data" / "crudo"
DATA_LIMPIA = PROYECTO / "data" / "limpia"
DATA_INTEGRADO = PROYECTO / "data" / "integrado"
MD_FIGURAS = PROYECTO / "md" / "figuras"

# ----- rutas de origen (intocables, crudo) -----
RUTA_HIPOTECAS = DATA_CRUDO / "UK_Mortgage_Rate.csv"
RUTA_CLIMA = DATA_CRUDO / "MET_Office_Weather_Data.csv"
RUTA_PRECIOS_SALARIO = DATA_CRUDO / "Average_UK_houseprices_and_salary.csv"
RUTA_INGRESO_EDAD = DATA_CRUDO / "Income_by_age_and_gender.csv"

# F1 ya fue limpiada en el modulo limpieza (fas partes 1-7); se reutiliza:
RUTA_TRANSACCIONES_LIMPIO = DATA_LIMPIA / "uk_property_price_limpio.parquet"

# ----- rutas de salida (la etapa NO toca los origenes) -----
RUTA_HIPOTECAS_LIMPIO = DATA_LIMPIA / "hipotecas_limpio.parquet"
RUTA_CLIMA_LIMPIO = DATA_LIMPIA / "clima_limpio.parquet"
RUTA_PRECIOS_SALARIO_LIMPIO = DATA_LIMPIA / "precios_salario_limpio.parquet"

RUTA_PRECIOS_REGION = DATA_LIMPIA / "precios_region.parquet"
RUTA_PRECIOS_CIUDAD = DATA_LIMPIA / "precios_ciudad.parquet"

RUTA_ANOMALIAS_REGION = DATA_INTEGRADO / "anomalias_region.parquet"
RUTA_ANOMALIAS_NACIONAL = DATA_INTEGRADO / "anomalias_nacional.parquet"
RUTA_MAESTRO = DATA_INTEGRADO / "maestro_joven_uk.parquet"
RUTA_MAESTRO_MUESTRA = DATA_INTEGRADO / "maestro_joven_uk_muestra.csv"
RUTA_HIPOTECA_2022 = DATA_INTEGRADO / "hipoteca_2022.parquet"
RUTA_HIPOTECA_2022_MUESTRA = DATA_INTEGRADO / "hipoteca_2022.csv"
RUTA_HISTORICO = DATA_INTEGRADO / "historico_nacional.parquet"
RUTA_HISTORICO_MUESTRA = DATA_INTEGRADO / "historico_nacional.csv"

RUTA_BITACORA = PROYECTO / "md" / "BITACORA_DECISIONES.md"

# ----- reglas de negocio del analisis -----
ANIO_MIN_PRECIOS = 2015            # inicio de transacciones georreferenciadas
ANIO_HIPOTECA = 2022               # snapshot de productos hipotecarios
VENTANA_CUADRO = (2015, 2020)      # anios donde conviven transacciones+clima+salario
LTV = 0.90                         # prestamo tipico: 90 % del precio
PLAZO_ANIOS = 25                   # MTG_PRODUCT_YEARS constante en F2
UMBRAL_ACCESIBILIDAD = 0.30        # cuota hipotecaria <= 30 % del salario (regla 30 %)
SEED = 42                          # reproducibilidad del analisis

# Deflactor nominal 2022 -> real 2020 (Banco de Inglaterra, calculadora CPI,
# dic 2020 -> dic 2022). El salario de F4 esta ajustado a GBP 2020.
DEFLACTOR_2022_A_2020 = 1.137

# Joven = 18 a 34 anios. La fuente por edad usa bandas; se aproxima con las
# bandas 18-21, 22-29 y 30-39 (la inferior de 30-39 cubre 30-34).
GRUPOS_JOVEN = ["18 to 21", "22 to 29", "30 to 39"]

# Factores regionales aprox. de salario medio (referencia ASHE 2021, razon
# ingreso medio anual de la region / Reino Unido; redondeado a 2 decimales,
# citado en el informe como aproximacion para regionalizar la mediana nacional).
FACTOR_REGIONAL = {
    "London": 1.25,
    "South East": 1.06,
    "East of England": 1.01,
    "South West": 0.95,
    "East Midlands": 0.92,
    "West Midlands": 0.91,
    "North West": 0.91,
    "Yorkshire and The Humber": 0.88,
    "North East": 0.85,
    "Wales": 0.90,
}

# Estacion Met Office -> region ONS (solo Inglaterra y Gales cruzan con F1;
# Escocia e Irlanda del Norte quedan para las anomalias nacionales).
ESTACION_REGION = {
    "aberporth": "Wales",
    "bradford": "Yorkshire and The Humber",
    "camborne": "South West",
    "cambridge": "East of England",
    "cardiff": "Wales",
    "chivenor": "South West",
    "cwmystwyth": "Wales",
    "durham": "North East",
    "eastbourne": "South East",
    "heathrow": "London",
    "hurn": "South West",
    "lowestoft": "East of England",
    "manston": "South East",
    "newtonrigg": "North West",
    "oxford": "South East",
    "ringway": "North West",
    "rossonwye": "West Midlands",
    "shawbury": "West Midlands",
    "sheffield": "Yorkshire and The Humber",
    "southampton": "South East",
    "valley": "Wales",
    "waddington": "East Midlands",
    "whitby": "Yorkshire and The Humber",
    "yeovilton": "South West",
}

# Columnas esperadas por fuente (contrato de entrada).
COLS_HIPOTECAS = [
    "sku", "banco", "subtitulo", "tipo_crudo", "tipo", "plazo_anios",
    "tasa_inicial_pct", "apr_pct", "tasa_reversion", "comisiones_total",
    "meses_inicial", "fecha_escaneo", "tid",
]