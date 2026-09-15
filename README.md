# Accesibilidad de vivienda para jóvenes (18-34) en el Reino Unido

**Proyecto de Minería de Datos · UNIMINUTO Ibagué 2026-2 · Avance 1**

Análisis de **accesibilidad de vivienda para jóvenes (18-34)** por ciudad/región del
Reino Unido: cruce de **4 fuentes** (transacciones, hipotecas, clima y precios/salario)
para estimar cuántos años de salario cuesta comprar, qué esfuerzo hipotecario exige
cada región y qué papel juega el clima en la evolución de los precios.

Fases del proyecto (ciclo KDD + CRISP-DM, replicando el curso con el caso TelecomUNO):

| Fase | KDD | CRISP-DM | Estado |
|------|-----|----------|--------|
| 1. Introducción y objetivos | Selección | Comprensión del negocio | Completada |
| 2. Fuentes y tipos de datos | Selección y preprocesamiento I | Comprensión de datos | Completada |
| 3. Limpieza y cruzamiento | Preprocesamiento II | Preparación de datos | **En curso** |
| 4. (futura) Análisis y modelado | Minería | Modelado | Pendiente |

## Metodología (KDD + CRISP-DM)

**Qué metodologías utilizamos.** El proyecto se apoya en **dos marcos de forma
combinada** (KDD + CRISP-DM), tal como se justifica en `md/PROPUESTA_METODOLOGICA.md`
y en el `Avances.pdf`:

- **KDD** (Fayyad et al., 1996): el ciclo analítico del descubrimiento — *selección,
  preprocesamiento, transformación, minería e interpretación*.
- **CRISP-DM** (Wirth & Hipp, 2000): el ciclo de negocio — *entendimiento del negocio,
  entendimiento de los datos, preparación, modelado, evaluación y despliegue*.
- **SEMMA** se descartó: está ligada a la herramienta SAS y cubre solo la parte
  analítica, sin el ciclo de negocio.

**Por qué estos dos y no uno solo.**

1. **Cobertura del ciclo completo:** KDD aporta el detalle conceptual de las etapas
   analíticas y CRISP-DM lo enmarca en el negocio; usar uno solo deja un hueco (KDD
   sin despliegue, CRISP-DM sin el detalle de la teoría).
2. **Coincidencia con el curso:** la sesión 1 enruta la asignatura por CRISP-DM y pide
   el Avance 1 como la entrega de negocio, datos y preparación, exactamente lo que
   cubre este repositorio.
3. **Trazabilidad:** cada decisión se mapea a su etapa KDD y su fase CRISP-DM
   (columnas de la tabla de fases), una buena práctica de documentación.

**Cómo vamos (estado actual).**

- **Fases 1 y 2 completas:** pregunta y objetivos, fuentes, tipos de datos y contrato
  de datos de cada fuente.
- **Fase 3 (limpieza y cruzamiento) en curso:** faltantes MCAR/MAR/MNAR por fuente,
  comparación IQR vs z-score, winsorización de la tasa y construcción del cuadro
  maestro año × región.
- **Fase 4 (modelado) pendiente:** pronóstico de la serie regional de precios y
  salarios.

**Resultados del avance (fase 3).**

- Cuadro maestro `maestro_joven_uk`: **60 filas** (10 regiones × 6 años, 2015-2020)
  sin huecos en precio y salario.
- Faltantes: la tasa de hipotecas es **MAR** (depende del tipo de producto); el clima
  es **MCAR** instrumental (falla conjunta de reporte); el sol y el salario histórico
  son **MNAR** estructurales. No se imputa en esta fase.
- Outliers de la tasa inicial: **IQR (Tukey) detecta 762 productos (9,77 %)**; z-score
  con \|z\|>3 detecta 0. Se elige IQR y la tasa se winsoriza (**media 6,11 % → 6,04 %**).
- Salario joven: **GBP 25.353/año** (factor 0,805 sobre la mediana nacional),
  regionalizado con ASHE 2021 (ONS).
- Años de salario para comprar: de **6,2** (North East) a **14,2** (London).
- Esfuerzo hipotecario 2022: de **43,0 %** (North East) a **100,0 %** (London) del
  salario; **ninguna región cumple el umbral del 30 %.**
- Clima: anomalías anuales de lluvia/temperatura/heladas frente a la normal 1931-2020,
  correlacionadas con la variación de precios por región (`md/figuras/*.png`).

Detalle de decisiones: `md/BITACORA_DECISIONES.md` e `md/INFORME_AVANCE1.md`.

## Problema y objetivos

Los jóvenes compran cada vez menos vivienda. Objetivo: **¿cuánta vivienda puede pagar un
joven (18-34) en cada ciudad/región con su salario, con hipoteca o préstamo, y el clima
cómo se asocia con la evolución de precios?**

Indicadores del cruce `maestro_joven_uk` (año × región, 2015-2020):

- `anos_salario` — años completos de salario joven para comprar la vivienda mediana.
- Esfuerzo hipotecario 2022 — cuota mensual (PMT, 90 % LTV, 25 años, tasa inicial media
  **winsorizada con IQR**) como % del salario joven mensual (umbral 30 %).
- Anomalías climáticas — desviación anual de lluvia/temperatura/heladas frente a la
  normal histórica 1931-2020 y su correlación con la variación de precios.

**Calidad de datos tratada en la fase 3:** clasificación de faltantes por fuente
(**MCAR/MAR/MNAR** con su evidencia) y decisión de método de outliers (**IQR (Tukey) vs
z-score**: IQR no exige normalidad y detecta la cola real; z-score con |z|>3 no detecta
nada en la tasa inicial). Ver `script/proyecto/diagnostico.py`.

## Fuentes de datos

| # | Fuente | Periodo | Archivo | Enlace (Kaggle) |
|---|--------|---------|---------|-----------------|
| F1 | Propiedad (Land Registry, geocodificada) | 2015-2026 | `db/*` (en repo solo `_muestra`) | [uk-property-sale-prices-20152026-geo-enriched](https://www.kaggle.com/datasets/mansiaggarwal88/uk-property-sale-prices-20152026-geo-enriched?select=uk_property_price_paid_geo.csv) |
| F2 | Hipotecas (snapshot 2022) | 2022 | `data/crudo/UK_Mortgage_Rate.csv` | [uk-mortgage-rates-thousands-of-mortgage-products](https://www.kaggle.com/datasets/thedevastator/uk-mortgage-rates-thousands-of-mortgage-products) |
| F3 | Met Office (36 estaciones) | 1931-2020 | `data/crudo/MET_Office_Weather_Data.csv` | [uk-met-office-weather-data](https://www.kaggle.com/datasets/josephw20/uk-met-office-weather-data) |
| F4 | Precio medio + salario mediana (GBP 2020) | 1975-2020 | `data/crudo/Average_UK_houseprices_and_salary.csv` | [uk-median-house-prices-and-salary-19752020](https://www.kaggle.com/datasets/samuelcortinhas/uk-median-house-prices-and-salary-19752020) |
| F4b | Salario por edad y género (brecha 2021) | 2021 | `data/crudo/Income_by_age_and_gender.csv` | (misma fuente F4) |

Referencias: Land Registry Price Paid Data (OGL v3.0), Met Office historic station data,
Kaggle (transacciones F1, hipotecas F2, clima F3, precios-salario F4), Banco de Inglaterra.

## Estructura del proyecto

```
mineria/
├── main_proyecto.py            # ejecuta el analisis de accesibilidad (11 partes)
├── main_limpieza.py            # ejecuta la limpieza de F1 (7 fases)
├── Avances.pdf                 # documento del avance en normas APA 7 (PDF)
├── db/                         # F1 origin + muestras _muestra (locales y repo)
├── data/
│   ├── crudo/                  # F2, F3, F4 y F4b (pequenos, si se suben)
│   ├── limpia/                 # F1 limpia + limpias por fuente (parquet locales)
│   └── integrado/              # maestro_joven_uk + hipoteca_2022 + historico
├── script/
│   ├── limpieza/               # limpieza de F1 (cuartiles/IQR/MCAR/bitacora)
│   └── proyecto/               # 4 fuentes -> cruce maestro_joven_uk
│       ├── config.py           # rutas, reglas, factores regionales, estaciones
│       ├── cargar.py           # carga defensiva por fuente
│       ├── limpiar.py          # duplicados -> tipos -> nulos -> outliers
│       ├── diagnostico.py      # clasificacion MCAR/MAR/MNAR + IQR vs z-score
│       ├── transformaciones.py # agregados, anomalias, salario joven
│       ├── cruces.py           # maestro_joven_uk (anio x region)
│       ├── indicadores.py      # anos_salario, PMT, correlacion clima
│       ├── graficos.py         # 9 figuras PNG + tabla de fases
│       ├── validacion.py       # asserts post-cruce
│       ├── bitacora.py         # md/BITACORA_DECISIONES.md
│       └── pipeline.py         # orquestador de 11 partes
└── libros/                     # notebooks reproducibles (01-05 + 2 previos)
```

## Instalación

Requisitos: Python 3.10+ (desarrollado con Python 3.14).

```powershell
pip install -r script/requirements/requirements.txt
```

Extras de Jupyter para ejecutar/exportar los cuadernos:

```powershell
pip install -r script/requirements/requirements-notebooks.txt
```

## Ejecución

Todos los comandos desde la raíz del proyecto.

| Tarea | Comando |
|---|---|
| Analisis de accesibilidad (4 fuentes, 11 partes) | `python main_proyecto.py` |
| Limpieza de F1 (7 fases) | `python main_limpieza.py` |
| Ejecutar un cuaderno (in-place) | `python -m jupyter nbconvert --to notebook --execute --inplace "libros/03_Cruces_Affordability_Joven.ipynb" --ExecutePreprocessor.timeout=900` |
| Exportar un cuaderno a HTML | `python -m jupyter nbconvert --to html --execute "libros/05_Clima_y_Precios.ipynb" --ExecutePreprocessor.timeout=900` |

### Libros

- `01_Carga_4_Fuentes.ipynb` — contratos, esquemas, ventana de cruce y tabla de fases.
- `02_Limpieza_4_Datasets.ipynb` — MCAR/MAR/MNAR por fuente, IQR vs z-score y bitácora.
- `03_Cruces_Affordability_Joven.ipynb` — `maestro_joven_uk` y ciudades.
- `04_Hipoteca_Joven.ipynb` — esfuerzo hipotecario 2022 por región (tasa winsorizada).
- `05_Clima_y_Precios.ipynb` — anomalías climáticas vs precios.
- `Lectura.ipynb` / `Diagnostico_Limpieza.ipynb` — lectura y limpieza de F1 (previos).

## Salidas

- `data/integrado/maestro_joven_uk.parquet` — cuadro año × región (2015-2020) y tablas
  planas CSV.
- `Avances.pdf` — **documento del avance en normas APA 7** (portada, resumen, método,
  resultados, referencias).
- `md/INFORME_AVANCE1.md` — informe de la fase 3 (limpieza + cruzamiento, en curso).
- `md/PROPUESTA_METODOLOGICA.md` — propuesta editable (los autores generan el PDF).
- `md/BITACORA_DECISIONES.md` — decisiones de limpieza y cruce.
- `md/figuras/*.png` — 9 figuras del analisis + 2 de la limpieza F1 (+ tabla de fases).

**Sobre los datos (muestras):** el repositorio **no sube los archivos grandes completos**
(F1: el CSV de 2,22 GB y el parquet limpio de 434 MB son locales). En `db/` y
`data/limpia/` solo se sube **una muestra con sufijo `_muestra`** (primeras 2.000 filas)
de cada dataset, para que el repositorio sea liviano y el análisis sea reproducible en
forma parcial. Las fuentes F2-F4 son pequeñas (archivos Kaggle < 1,5 MB) y se incluyen
completas en `data/crudo/`. **Los datasets completos se descargan de los enlaces** de la
sección de fuentes: F1, F2, F3 y F4 (ver más abajo), y `main_limpieza.py` regenera la
versión limpia de F1 a partir del CSV original.

### Descarga de los datos completos

| Dataset | Muestra en el repo | Descarga completa |
|---|---|---|
| F1 transacciones (11,4 M filas, CSV 2,22 GB) | `db/uk_property_price_muestra.csv` | [Kaggle: uk-property-sale-prices-20152026-geo-enriched](https://www.kaggle.com/datasets/mansiaggarwal88/uk-property-sale-prices-20152026-geo-enriched?select=uk_property_price_paid_geo.csv) |
| F1 pre-limpieza | `db/uk_property_semiorganizado_muestra.csv` | (se genera con `main_limpieza.py` desde el CSV de Kaggle) |
| F2 hipotecas 2022 | completa en `data/crudo/` | [Kaggle: uk-mortgage-rates](https://www.kaggle.com/datasets/thedevastator/uk-mortgage-rates-thousands-of-mortgage-products) |
| F3 Met Office 1931-2020 | completa en `data/crudo/` | [Kaggle: uk-met-office-weather-data](https://www.kaggle.com/datasets/josephw20/uk-met-office-weather-data) |
| F4 precios + salario 1975-2020 | completa en `data/crudo/` | [Kaggle: uk-median-house-prices-and-salary-19752020](https://www.kaggle.com/datasets/samuelcortinhas/uk-median-house-prices-and-salary-19752020) |

> Todos los archivos con extensión `_muestra` son **muestras** (primeras 2.000 filas), no
> los datos completos.

## Documentos del curso

`contexto/presentacion1.html` · `presentacion2.html` · `presentacion3.html` — diapositivas
de las sesiones 1-3 (referencia local de fases, tipos de datos y limpieza). **No se suben
al repositorio.**

## Referencias

- F1 transacciones (Kaggle, 11,4 M): [uk-property-sale-prices-20152026-geo-enriched](https://www.kaggle.com/datasets/mansiaggarwal88/uk-property-sale-prices-20152026-geo-enriched?select=uk_property_price_paid_geo.csv)
- F2 hipotecas (Kaggle): [uk-mortgage-rates-thousands-of-mortgage-products](https://www.kaggle.com/datasets/thedevastator/uk-mortgage-rates-thousands-of-mortgage-products)
- F3 clima (Kaggle): [uk-met-office-weather-data](https://www.kaggle.com/datasets/josephw20/uk-met-office-weather-data)
- F4 precios/salario (Kaggle): [uk-median-house-prices-and-salary-19752020](https://www.kaggle.com/datasets/samuelcortinhas/uk-median-house-prices-and-salary-19752020)
- Met Office: [Historic station data](https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data)
- Land Registry: [Price Paid Data](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)