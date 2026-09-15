"""Modulo proyecto: analisis de accesibilidad de vivienda para jovenes (18-34).

Parte del proyecto de mineria de datos (Avance 1). Este paquete orquesta las
4 fuentes (transacciones, hipotecas, clima, precios/salario) y las cruza en el
cuadro maestro_joven_uk (anio x region). Orden del pipeline:
carga -> limpieza -> transformaciones -> cruce -> indicadores -> analisis clima
-> validacion -> figuras + bitacora.
"""
from __future__ import annotations