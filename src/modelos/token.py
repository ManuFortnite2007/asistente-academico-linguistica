from dataclasses import dataclass
from enum import Enum, auto


class TipoToken(Enum):
    """
    Tipos preliminares para el vocabulario del asistente académico.
    Se ampliarán durante el desarrollo del analizador léxico.
    """
    DETERMINANTE = auto()
    SUSTANTIVO = auto()
    VERBO = auto()
    PREPOSICION = auto()
    ADJETIVO = auto()
    NUMERO = auto()
    OPERADOR = auto()
    IDENTIFICADOR = auto()
    DESCONOCIDO = auto()
    FIN = auto()


@dataclass(frozen=True)
class Token:
    """
    Unidad léxica producida por el futuro analizador léxico.
    """
    tipo: TipoToken
    lexema: str
    linea: int
    columna: int

    def __str__(self) -> str:
        return (
            f"Token(tipo={self.tipo.name}, "
            f"lexema={self.lexema!r}, "
            f"linea={self.linea}, "
            f"columna={self.columna})"
        )
