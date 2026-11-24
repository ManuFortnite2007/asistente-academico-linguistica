"""Exportación consistente de resultados léxicos a TXT, CSV y JSON."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from src.modelos.resultado import ResultadoAnalisis


class ExportadorResultados:
    @staticmethod
    def exportar(resultado: ResultadoAnalisis, ruta: str | Path, formato: str | None = None) -> Path:
        destino = Path(ruta)
        formato_final = (formato or destino.suffix.lstrip(".")).casefold()
        if formato_final not in {"txt", "csv", "json"}:
            raise ValueError("Formato no admitido. Use txt, csv o json.")
        destino.parent.mkdir(parents=True, exist_ok=True)
        getattr(ExportadorResultados, f"_a_{formato_final}")(resultado, destino)
        return destino

    @staticmethod
    def _a_json(resultado: ResultadoAnalisis, destino: Path) -> None:
        destino.write_text(
            json.dumps(resultado.como_dict(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _a_csv(resultado: ResultadoAnalisis, destino: Path) -> None:
        with destino.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(
                archivo, fieldnames=["tipo", "lexema", "linea", "columna", "normalizado"]
            )
            escritor.writeheader()
            escritor.writerows(token.como_dict() for token in resultado.tokens)

    @staticmethod
    def _a_txt(resultado: ResultadoAnalisis, destino: Path) -> None:
        lineas = [
            "TOKENS",
            "=" * 78,
            f"{'TIPO':<20} {'LEXEMA':<30} {'LÍNEA':>7} {'COLUMNA':>8}",
            "-" * 78,
        ]
        for token in resultado.tokens:
            lexema = token.lexema.replace("\n", "\\n").replace("\t", "\\t")
            lineas.append(f"{token.tipo.name:<20} {lexema[:30]:<30} {token.linea:>7} {token.columna:>8}")
        lineas.extend(["", "ERRORES", "=" * 78])
        lineas.extend(str(error) for error in resultado.errores)
        if not resultado.errores:
            lineas.append("Sin errores léxicos.")
        lineas.extend(["", "RESUMEN", "=" * 78])
        for clave, valor in resultado.resumen().items():
            lineas.append(f"{clave}: {valor}")
        destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
