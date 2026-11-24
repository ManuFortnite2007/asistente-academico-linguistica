"""Árboles y diagnósticos del analizador sintáctico."""
from dataclasses import dataclass

@dataclass(frozen=True)
class NodoSintactico:
    simbolo: str
    hijos: tuple = ()
    token: object = None

    def arbol_texto(self):
        lineas = []
        def rec(n, prefijo="", ultimo=True, raiz=False):
            texto = n.simbolo
            if n.token is not None:
                texto += f" : {n.token.lexema!r} ({n.token.linea}:{n.token.columna})"
            lineas.append(("" if raiz else prefijo + ("└── " if ultimo else "├── ")) + texto)
            siguiente = "" if raiz else prefijo + ("    " if ultimo else "│   ")
            for i, hijo in enumerate(n.hijos):
                rec(hijo, siguiente, i == len(n.hijos)-1)
        rec(self, raiz=True)
        return "\n".join(lineas)

    def como_dict(self):
        resultado = {"simbolo": self.simbolo, "hijos": [h.como_dict() for h in self.hijos]}
        if self.token is not None:
            resultado["token"] = self.token.como_dict()
        return resultado

@dataclass(frozen=True)
class DiagnosticoSintactico:
    codigo: str
    descripcion: str
    token_inesperado: str
    tipo_token: str
    linea: int
    columna: int
    esperados: tuple

    def __str__(self):
        return (f"{self.codigo} (línea {self.linea}, columna {self.columna}): "
                f"{self.descripcion}\n  Recibido: {self.tipo_token}({self.token_inesperado!r})"
                f"\n  Se esperaba: {', '.join(self.esperados)}")

@dataclass(frozen=True)
class ComandoAnalizado:
    linea: int
    texto: str
    arbol: NodoSintactico

@dataclass(frozen=True)
class ResultadoSintactico:
    comandos: tuple
    errores: tuple
    lineas_omitidas: tuple = ()

    @property
    def exitoso(self):
        return not self.errores and not self.lineas_omitidas
