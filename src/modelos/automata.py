"""Autómata finito determinista reutilizable por el lexer y la GUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable, Tuple

from src.modelos.estado import Estado


@dataclass(frozen=True)
class TransicionClase:
    """Transición descrita por un predicado de clasificación."""

    origen: str
    etiqueta: str
    destino: str
    acepta: Callable[[str], bool]


@dataclass(frozen=True)
class PasoAutomata:
    numero: int
    origen: str
    simbolo: str
    destino: str | None


@dataclass(frozen=True)
class ResultadoAutomata:
    entrada: str
    aceptada: bool
    estado_final: str
    pasos: tuple[PasoAutomata, ...]


class Automata:
    """AFD con transiciones exactas y por clases de caracteres.

    Las transiciones exactas conservan la API inicial. Las de clase
    expresan LETRA o DIGITO sin enumerar Unicode ni usar regex.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.estados: Dict[str, Estado] = {}
        self.transiciones: Dict[Tuple[str, str], str] = {}
        self.transiciones_clase: list[TransicionClase] = []

    def agregar_estado(self, estado: Estado) -> None:
        if estado.nombre in self.estados:
            raise ValueError(f"Ya existe un estado llamado '{estado.nombre}'.")
        if estado.es_inicial and self.estado_inicial() is not None:
            raise ValueError("El autómata solamente puede tener un estado inicial.")
        self.estados[estado.nombre] = estado

    def agregar_transicion(self, origen: str, simbolo: str, destino: str) -> None:
        self._validar_estados(origen, destino)
        if len(simbolo) != 1:
            raise ValueError("Cada transición exacta recibe un único símbolo.")
        clave = (origen, simbolo)
        if clave in self.transiciones:
            raise ValueError(f"Ya existe una transición para {origen} con {simbolo!r}.")
        self.transiciones[clave] = destino

    def agregar_transicion_clase(
        self,
        origen: str,
        etiqueta: str,
        acepta: Callable[[str], bool],
        destino: str,
    ) -> None:
        self._validar_estados(origen, destino)
        if not etiqueta.strip():
            raise ValueError("La transición debe tener una etiqueta.")
        if any(t.origen == origen and t.etiqueta == etiqueta for t in self.transiciones_clase):
            raise ValueError(f"Transición de clase duplicada: {origen}/{etiqueta}")
        self.transiciones_clase.append(TransicionClase(origen, etiqueta, destino, acepta))

    def _validar_estados(self, origen: str, destino: str) -> None:
        if origen not in self.estados:
            raise ValueError(f"Estado de origen inexistente: {origen}")
        if destino not in self.estados:
            raise ValueError(f"Estado de destino inexistente: {destino}")

    def estado_inicial(self) -> Estado | None:
        return next((e for e in self.estados.values() if e.es_inicial), None)

    def siguiente_estado(self, actual: str, simbolo: str) -> str | None:
        exacta = self.transiciones.get((actual, simbolo))
        if exacta is not None:
            return exacta
        for transicion in self.transiciones_clase:
            if transicion.origen == actual and transicion.acepta(simbolo):
                return transicion.destino
        return None

    def procesar(self, cadena: str) -> bool:
        return self.trazar(cadena).aceptada

    def trazar(self, cadena: str) -> ResultadoAutomata:
        inicial = self.estado_inicial()
        if inicial is None:
            raise RuntimeError("El autómata no tiene un estado inicial definido.")
        actual = inicial.nombre
        pasos: list[PasoAutomata] = []
        for numero, simbolo in enumerate(cadena, 1):
            siguiente = self.siguiente_estado(actual, simbolo)
            pasos.append(PasoAutomata(numero, actual, simbolo, siguiente))
            if siguiente is None:
                return ResultadoAutomata(cadena, False, actual, tuple(pasos))
            actual = siguiente
        return ResultadoAutomata(cadena, self.estados[actual].es_final, actual, tuple(pasos))

    def etiquetas_desde(self, estado: str) -> Iterable[tuple[str, str]]:
        for (origen, simbolo), destino in self.transiciones.items():
            if origen == estado:
                yield repr(simbolo), destino
        for transicion in self.transiciones_clase:
            if transicion.origen == estado:
                yield transicion.etiqueta, transicion.destino
