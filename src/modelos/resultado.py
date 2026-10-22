"""Resultado único compartido por CLI, GUI y exportadores."""

from collections import Counter
from dataclasses import dataclass

from src.modelos.diagnostico import DiagnosticoLexico
from src.modelos.token import TipoToken, Token


@dataclass(frozen=True)
class ResultadoAnalisis:
    texto: str
    tokens: tuple[Token, ...]
    errores: tuple[DiagnosticoLexico, ...]

    @property
    def tokens_sin_fin(self) -> tuple[Token, ...]:
        return tuple(t for t in self.tokens if t.tipo is not TipoToken.FIN)

    @property
    def exitoso(self) -> bool:
        return not self.errores

    def resumen(self) -> dict[str, object]:
        conteo = Counter(token.tipo.name for token in self.tokens_sin_fin)
        return {
            "total_caracteres": len(self.texto),
            "total_tokens": len(self.tokens_sin_fin),
            "cantidad_por_categoria": dict(sorted(conteo.items())),
            "numero_errores": len(self.errores),
            "estado_final": "CORRECTO" if self.exitoso else "CON_ERRORES",
        }

    def como_dict(self) -> dict[str, object]:
        return {
            "tokens": [token.como_dict() for token in self.tokens],
            "errores": [error.como_dict() for error in self.errores],
            "resumen": self.resumen(),
        }
