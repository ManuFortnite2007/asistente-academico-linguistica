"""Analizador léxico secuencial basado en AFD construidos manualmente."""

from __future__ import annotations

import unicodedata

from src.analizadores.reconocedores import crear_automatas
from src.modelos.automata import Automata
from src.modelos.diagnostico import DiagnosticoLexico
from src.modelos.resultado import ResultadoAnalisis
from src.modelos.token import TipoToken, Token


VOCABULARIO: dict[TipoToken, frozenset[str]] = {
    TipoToken.VERBO: frozenset({
        "mostrar", "agregar", "consultar", "buscar", "listar", "eliminar",
        "crear", "editar", "guardar", "abrir", "ver", "programar",
    }),
    TipoToken.SUSTANTIVO: frozenset({
        "tarea", "tareas", "horario", "horarios", "materia", "materias",
        "examen", "examenes", "proyecto", "proyectos", "calificacion",
        "calificaciones", "clase", "clases", "recordatorio", "recordatorios",
        "redes", "matematicas", "programacion", "fisica",
    }),
    TipoToken.ADJETIVO: frozenset({
        "pendiente", "pendientes", "completada", "completadas", "proximo",
        "proximos", "academico", "academica", "semanal", "final",
    }),
    TipoToken.PREPOSICION: frozenset({
        "a", "ante", "bajo", "con", "contra", "de", "desde", "durante",
        "en", "entre", "hacia", "hasta", "mediante", "para", "por", "segun",
        "sin", "sobre", "tras",
    }),
    TipoToken.DETERMINANTE: frozenset({
        "el", "la", "los", "las", "un", "una", "unos", "unas", "mi", "mis",
        "este", "esta", "estos", "estas",
    }),
}

OPERADORES_DOBLES = frozenset({"==", "!=", "<=", ">="})
OPERADORES_SIMPLES = frozenset({"+", "-", "*", "/", "=", "<", ">", ":"})
DELIMITADORES = frozenset({"(", ")", "[", "]", "{", "}", ",", ";", "."})
def normalizar_palabra(texto: str) -> str:
    """Minúsculas sin marcas diacríticas, conservando el lexema original."""
    descompuesto = unicodedata.normalize("NFD", texto.casefold())
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


class AnalizadorLexico:
    """Tokeniza texto completo y recupera errores avanzando siempre la entrada."""

    def __init__(self) -> None:
        self.automatas = crear_automatas()
        self.tokens: list[Token] = []
        self.errores: list[DiagnosticoLexico] = []

    def analizar(self, texto: str) -> ResultadoAnalisis:
        if not isinstance(texto, str):
            raise TypeError("La entrada del analizador debe ser una cadena.")
        self.tokens = []
        self.errores = []
        indice = 0
        linea = 1
        columna = 1

        while indice < len(texto):
            caracter = texto[indice]
            if caracter in " \t\f\v":
                indice += 1
                columna += 1
                continue
            if caracter in "\n\r":
                indice, linea, columna = self._consumir_salto(texto, indice, linea)
                continue
            if caracter == "#" or texto.startswith("//", indice):
                while indice < len(texto) and texto[indice] not in "\r\n":
                    indice += 1
                    columna += 1
                continue
            if caracter.isalpha() or caracter == "_":
                indice, columna = self._leer_palabra(texto, indice, linea, columna)
                continue
            if caracter.isdecimal():
                indice, columna = self._leer_numero(texto, indice, linea, columna)
                continue
            if caracter == '"':
                indice, linea, columna = self._leer_cadena(texto, indice, linea, columna)
                continue

            doble = texto[indice:indice + 2]
            if doble in OPERADORES_DOBLES:
                self.tokens.append(Token(TipoToken.OPERADOR, doble, linea, columna, doble))
                indice += 2
                columna += 2
                continue
            if caracter in OPERADORES_SIMPLES:
                self.tokens.append(Token(TipoToken.OPERADOR, caracter, linea, columna, caracter))
                indice += 1
                columna += 1
                continue
            if caracter in DELIMITADORES:
                self.tokens.append(Token(TipoToken.DELIMITADOR, caracter, linea, columna, caracter))
                indice += 1
                columna += 1
                continue

            self.errores.append(DiagnosticoLexico(
                "LEX001", "ERROR LEXICO", "Símbolo no reconocido por el lenguaje.",
                caracter, linea, columna,
                "Elimine el símbolo o sustitúyalo por un operador admitido.",
            ))
            indice += 1
            columna += 1

        self.tokens.append(Token(TipoToken.FIN, "", linea, columna, ""))
        return ResultadoAnalisis(texto, tuple(self.tokens), tuple(self.errores))

    def _leer_palabra(self, texto: str, inicio: int, linea: int, columna: int) -> tuple[int, int]:
        indice = inicio
        estado = self.automatas["identificador"].estado_inicial().nombre  # type: ignore[union-attr]
        while indice < len(texto):
            siguiente = self.automatas["identificador"].siguiente_estado(estado, texto[indice])
            if siguiente is None:
                break
            estado = siguiente
            indice += 1
        lexema = texto[inicio:indice]
        normalizado = normalizar_palabra(lexema)
        tipo = next(
            (categoria for categoria, palabras in VOCABULARIO.items() if normalizado in palabras),
            TipoToken.IDENTIFICADOR,
        )
        self.tokens.append(Token(tipo, lexema, linea, columna, normalizado))
        return indice, columna + len(lexema)

    def _leer_numero(self, texto: str, inicio: int, linea: int, columna: int) -> tuple[int, int]:
        indice = inicio
        estado = self.automatas["numero"].estado_inicial().nombre  # type: ignore[union-attr]
        while indice < len(texto):
            siguiente = self.automatas["numero"].siguiente_estado(estado, texto[indice])
            if siguiente is None:
                break
            estado = siguiente
            indice += 1
        lexema = texto[inicio:indice]
        if estado == "q2":
            self.errores.append(DiagnosticoLexico(
                "LEX003", "ERROR LEXICO", "Número decimal incompleto; falta un dígito tras el punto.",
                lexema, linea, columna, "Agregue al menos un dígito después del punto decimal.",
            ))
            return indice, columna + len(lexema)
        tipo = TipoToken.NUMERO_DECIMAL if estado == "q3" else TipoToken.NUMERO_ENTERO
        self.tokens.append(Token(tipo, lexema, linea, columna, lexema))
        return indice, columna + len(lexema)

    def _leer_cadena(
        self, texto: str, inicio: int, linea: int, columna: int
    ) -> tuple[int, int, int]:
        afd = self.automatas["cadena"]
        estado = afd.estado_inicial().nombre  # type: ignore[union-attr]
        estado = afd.siguiente_estado(estado, texto[inicio]) or estado
        indice = inicio + 1
        linea_actual = linea
        columna_actual = columna + 1
        cerrada = False
        while indice < len(texto):
            caracter = texto[indice]
            if caracter in "\r\n":
                break
            siguiente = afd.siguiente_estado(estado, caracter)
            if siguiente is None:
                # El único rechazo recuperable dentro de una línea ocurre en q2.
                if estado == "q2":
                    self.errores.append(DiagnosticoLexico(
                        "LEX004", "ERROR LEXICO", "Secuencia de escape no admitida.",
                        "\\" + caracter, linea_actual, columna_actual - 1,
                        'Use \\n, \\t, \\r, \\" o \\\\.',
                    ))
                    estado = "q1"
                    indice += 1
                    columna_actual += 1
                    continue
                break
            estado = siguiente
            indice += 1
            columna_actual += 1
            if estado == "q3":
                cerrada = True
                break

        lexema = texto[inicio:indice]
        if cerrada:
            self.tokens.append(Token(TipoToken.CADENA, lexema, linea, columna, lexema[1:-1]))
        else:
            self.errores.append(DiagnosticoLexico(
                "LEX002", "ERROR LEXICO", "Cadena sin comilla de cierre.",
                lexema, linea, columna, "Cierre la cadena con una comilla doble antes del fin de línea.",
            ))
        return indice, linea_actual, columna_actual

    @staticmethod
    def _consumir_salto(texto: str, indice: int, linea: int) -> tuple[int, int, int]:
        if texto[indice] == "\r" and indice + 1 < len(texto) and texto[indice + 1] == "\n":
            indice += 2
        else:
            indice += 1
        return indice, linea + 1, 1

    def automata(self, nombre: str) -> Automata:
        return self.automatas[nombre.casefold()]
