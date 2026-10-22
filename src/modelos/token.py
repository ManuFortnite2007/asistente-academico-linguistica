from dataclasses import asdict, dataclass
from enum import Enum, auto


class TipoToken(Enum):
    DETERMINANTE = auto()
    SUSTANTIVO = auto()
    VERBO = auto()
    PREPOSICION = auto()
    ADJETIVO = auto()
    IDENTIFICADOR = auto()
    NUMERO_ENTERO = auto()
    NUMERO_DECIMAL = auto()
    CADENA = auto()
    OPERADOR = auto()
    DELIMITADOR = auto()
    FIN = auto()

    # Alias compatible con la versión inicial.
    NUMERO = NUMERO_ENTERO


@dataclass(frozen=True)
class Token:
    """Unidad léxica con posición 1-based y forma normalizada."""
    tipo: TipoToken
    lexema: str
    linea: int
    columna: int
    normalizado: str | None = None

    @property
    def longitud(self) -> int:
        return len(self.lexema)

    def como_dict(self) -> dict[str, str | int | None]:
        datos = asdict(self)
        datos["tipo"] = self.tipo.name
        return datos

    def __str__(self) -> str:
        return (
            f"Token(tipo={self.tipo.name}, "
            f"lexema={self.lexema!r}, "
            f"linea={self.linea}, "
            f"columna={self.columna})"
        )
