"""Parser LL(1) descendente recursivo: GIC de la Actividad 3."""
from collections import defaultdict
from src.modelos.token import Token, TipoToken as T
from src.modelos.sintaxis import NodoSintactico as N, DiagnosticoSintactico as D, ComandoAnalizado as C, ResultadoSintactico as R

ACCIONES = ("mostrar", "agregar", "consultar", "buscar")
VISUALES = ("tareas", "horarios", "materias", "examenes", "proyectos", "recordatorios", "calificaciones")
FILTROS = ("pendientes", "completadas", "proximos")
ALTAS = ("tarea", "materia", "examen", "proyecto", "recordatorio")
CONSULTABLES = ("horario", "horarios", "materia", "materias", "tarea", "tareas",
                "examen", "examenes", "calificacion", "calificaciones")
DETERMINANTES = ("el", "la", "los", "las")
NOMBRES = (T.CADENA, T.IDENTIFICADOR, T.SUSTANTIVO)
NUMERICOS = (T.NUMERO_ENTERO, T.NUMERO_DECIMAL)

class _Falla(Exception):
    def __init__(self, error):
        self.error = error

class _Sentencia:
    def __init__(self, tokens):
        self.tokens, self.i = tokens, 0

    @property
    def actual(self):
        return self.tokens[self.i]

    def norm(self):
        t = self.actual
        return t.normalizado if t.normalizado is not None else t.lexema.casefold()

    def es(self, tipo, palabra=None):
        return self.actual.tipo is tipo and (palabra is None or self.norm() == palabra)

    def error(self, esperados, codigo=None):
        t = self.actual
        codigo = codigo or ("SYN002" if t.tipo is T.FIN else "SYN001")
        mensaje = {"SYN001": "Token inesperado en la sentencia.",
                   "SYN002": "La sentencia terminó antes de completar la regla.",
                   "SYN003": "Sobran tokens después de una sentencia completa.",
                   "SYN004": "Acción no admitida en esta gramática."}[codigo]
        raise _Falla(D(codigo, mensaje, t.lexema, t.tipo.name, t.linea,
                       t.columna, tuple(dict.fromkeys(esperados))))

    def tomar(self, nombre, tipo, palabra=None):
        if not self.es(tipo, palabra):
            self.error((nombre,))
        t = self.actual
        if tipo is not T.FIN:
            self.i += 1
        return N(nombre, token=t)

    def nodo(self, simbolo, *hijos):
        return N(simbolo, tuple(hijos))

    def vacio(self, simbolo):
        return self.nodo(simbolo, N("ε"))

    def regla(self, simbolo, tipo, opciones):
        if self.es(tipo) and self.norm() in opciones:
            palabra = self.norm()
            return self.nodo(simbolo, self.tomar(palabra.upper(), tipo, palabra))
        self.error(opciones)

    def analizar(self):
        comando = self.comando()
        if self.actual.tipo is not T.FIN:
            self.error(("FIN",), "SYN003")
        return self.nodo("S", comando, self.tomar("FIN", T.FIN))

    def comando(self):
        if not self.es(T.VERBO) or self.norm() not in ACCIONES:
            self.error(ACCIONES, "SYN004")
        acciones = {"mostrar": self.mostrar, "agregar": self.agregar,
                    "consultar": self.consultar, "buscar": self.buscar}
        return self.nodo("Comando", acciones[self.norm()]())

    def mostrar(self):
        return self.nodo("Mostrar", self.tomar("MOSTRAR", T.VERBO, "mostrar"),
                         self.regla("ObjVisual", T.SUSTANTIVO, VISUALES), self.filtro())

    def filtro(self):
        if self.es(T.ADJETIVO) and self.norm() in FILTROS:
            return self.regla("Filtro", T.ADJETIVO, FILTROS)
        if self.es(T.DELIMITADOR, "["):
            return self.nodo("Filtro", self.lista())
        if self.es(T.FIN):
            return self.vacio("Filtro")
        self.error((*FILTROS, "[", "FIN"))

    def lista(self):
        apertura = self.tomar("CORCH_I", T.DELIMITADOR, "[")
        numero = self.numero()
        cola = self.cola_numeros()
        cierre = self.tomar("CORCH_D", T.DELIMITADOR, "]")
        return self.nodo("Lista", apertura, numero, cola, cierre)

    def cola_numeros(self):
        if self.es(T.DELIMITADOR, ","):
            return self.nodo("ColaNums", self.tomar("COMA", T.DELIMITADOR, ","),
                             self.numero(), self.cola_numeros())
        if self.es(T.DELIMITADOR, "]"):
            return self.vacio("ColaNums")
        self.error((",", "]"))

    def numero(self):
        if self.actual.tipo in NUMERICOS:
            tipo = self.actual.tipo
            nombre = "NUM_ENTERO" if tipo is T.NUMERO_ENTERO else "NUM_DECIMAL"
            return self.nodo("Num", self.tomar(nombre, tipo))
        self.error(("NUM_ENTERO", "NUM_DECIMAL"))

    def agregar(self):
        return self.nodo("Agregar", self.tomar("AGREGAR", T.VERBO, "agregar"), self.carga())

    def carga(self):
        if self.es(T.SUSTANTIVO, "calificacion"):
            return self.nodo("Carga", self.tomar("CALIFICACION", T.SUSTANTIVO, "calificacion"),
                             self.numero())
        if self.es(T.SUSTANTIVO) and self.norm() in ALTAS:
            return self.nodo("Carga", self.regla("TipoAlta", T.SUSTANTIVO, ALTAS), self.nombre())
        self.error((*ALTAS, "calificacion"))

    def consultar(self):
        return self.nodo("Consultar", self.tomar("CONSULTAR", T.VERBO, "consultar"),
                         self.determinante(), self.regla("ObjConsulta", T.SUSTANTIVO, CONSULTABLES),
                         self.referencia())

    def determinante(self):
        if self.es(T.DETERMINANTE) and self.norm() in DETERMINANTES:
            return self.regla("DetOpt", T.DETERMINANTE, DETERMINANTES)
        if self.es(T.SUSTANTIVO) and self.norm() in CONSULTABLES:
            return self.vacio("DetOpt")
        self.error((*DETERMINANTES, *CONSULTABLES))

    def referencia(self):
        if self.es(T.PREPOSICION, "de"):
            return self.nodo("RefOpt", self.tomar("DE", T.PREPOSICION, "de"), self.nombre())
        if self.es(T.FIN):
            return self.vacio("RefOpt")
        self.error(("de", "FIN"))

    def buscar(self):
        return self.nodo("Buscar", self.tomar("BUSCAR", T.VERBO, "buscar"),
                         self.regla("TipoBusqueda", T.SUSTANTIVO, ALTAS), self.nombre())

    def nombre(self):
        if self.actual.tipo in NOMBRES:
            tipo = self.actual.tipo
            return self.nodo("Nombre", self.tomar(tipo.name, tipo))
        self.error(("CADENA", "IDENTIFICADOR", "SUSTANTIVO"))

class AnalizadorSintactico:
    """Un comando por línea; continúa tras un fallo y omite líneas con error léxico."""
    def analizar(self, tokens, errores_lexicos=()):
        grupos = defaultdict(list)
        for t in tokens:
            if t.tipo is not T.FIN:
                grupos[t.linea].append(t)
        invalidas = {e.linea for e in errores_lexicos}
        comandos, errores = [], []
        for linea in sorted(grupos):
            if linea in invalidas:
                continue
            fila = grupos[linea]
            ultimo = fila[-1]
            fin = Token(T.FIN, "", linea, ultimo.columna + len(ultimo.lexema), "")
            try:
                arbol = _Sentencia(fila + [fin]).analizar()
                comandos.append(C(linea, " ".join(t.lexema for t in fila), arbol))
            except _Falla as fallo:
                errores.append(fallo.error)
        return R(tuple(comandos), tuple(errores), tuple(sorted(invalidas)))

    def analizar_texto(self, texto):
        from src.analizadores.analizador_lexico import AnalizadorLexico
        lexico = AnalizadorLexico().analizar(texto)
        return lexico, self.analizar(lexico.tokens, lexico.errores)
