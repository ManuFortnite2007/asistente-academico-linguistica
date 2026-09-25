"""
Analizador léxico - estructura reservada.

En la siguiente fase esta clase recorrerá la entrada y generará
objetos Token usando autómatas construidos desde cero.
"""


class AnalizadorLexico:
    def __init__(self) -> None:
        self.tokens = []

    def analizar(self, texto: str):
        raise NotImplementedError(
            "El analizador léxico será implementado en la siguiente fase."
        )
