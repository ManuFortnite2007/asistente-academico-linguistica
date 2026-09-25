from dataclasses import dataclass
from pathlib import Path
from typing import Iterator


@dataclass(frozen=True)
class Caracter:
    """
    Representa un carácter leído de la entrada junto con su posición.
    """
    valor: str
    indice: int
    linea: int
    columna: int


class LectorTexto:
    """
    Módulo encargado de recibir una cadena o un archivo plano
    y permitir su lectura carácter por carácter.

    No utiliza librerías externas.
    """

    def __init__(self, contenido: str) -> None:
        self._contenido = contenido

    @classmethod
    def desde_cadena(cls, texto: str) -> "LectorTexto":
        if not isinstance(texto, str):
            raise TypeError("La entrada debe ser una cadena de texto.")
        return cls(texto)

    @classmethod
    def desde_archivo(
        cls,
        ruta: str | Path,
        codificacion: str = "utf-8"
    ) -> "LectorTexto":
        ruta = Path(ruta)

        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

        if not ruta.is_file():
            raise ValueError(f"La ruta no corresponde a un archivo: {ruta}")

        contenido = ruta.read_text(encoding=codificacion)
        return cls(contenido)

    @property
    def contenido(self) -> str:
        return self._contenido

    def recorrer(self) -> Iterator[Caracter]:
        """
        Recorre la entrada carácter por carácter y conserva
        índice, línea y columna.
        """
        linea = 1
        columna = 1

        for indice, valor in enumerate(self._contenido):
            yield Caracter(
                valor=valor,
                indice=indice,
                linea=linea,
                columna=columna
            )

            if valor == "\n":
                linea += 1
                columna = 1
            else:
                columna += 1
