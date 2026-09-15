"""Bitacora de decisiones del modulo proyecto (evidencia de cada transformacion).

Escribe md/BITACORA_DECISIONES.md con las decisiones de limpieza/cruce del
analisis de accesibilidad: que se cambio, cuantas filas afecto, como y por que.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd


@dataclass
class BitacoraProyecto:
    """Acumula las decisiones y las vierte a la tabla del informe."""

    registros: list[dict] = field(default_factory=list)

    def anotar(self, fuente: str, problema: str, cantidad: int | float,
               metodo: str, razon: str, impacto: str = "-") -> None:
        """Registra una decision: fuente, problema, cantidad afectada y metodo."""
        self.registros.append({
            "fuente": fuente,
            "problema": problema,
            "cantidad": int(cantidad) if isinstance(cantidad, float) and cantidad.is_integer() else cantidad,
            "metodo": metodo,
            "razon": razon,
            "impacto": impacto,
        })

    def tabla(self) -> pd.DataFrame:
        """Devuelve los registros como DataFrame (una fila por decision)."""
        return pd.DataFrame(self.registros)

    def a_markdown(self, ruta: Path = Path("md/BITACORA_DECISIONES.md")) -> Path:
        """Persiste la bitacora como tabla Markdown (sin dependencias extra)."""
        filas = self.tabla()
        if filas.empty:
            texto = "No hay decisiones registradas.\n"
        else:
            cab = "| fuente | problema | cantidad | metodo | razon | impacto |"
            sep = "|---|---|---|---|---|---|"
            cuerpo = [
                f"| {f['fuente']} | {f['problema']} | {f['cantidad']} | "
                f"{f['metodo']} | {f['razon']} | {f['impacto']} |"
                for f in self.registros
            ]
            texto = cab + "\n" + sep + "\n" + "\n".join(cuerpo) + "\n"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")
        return ruta