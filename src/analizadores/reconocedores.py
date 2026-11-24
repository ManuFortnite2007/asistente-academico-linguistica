"""Fábricas de los AFD utilizados por el analizador léxico."""

from __future__ import annotations

from src.modelos.automata import Automata
from src.modelos.estado import Estado


def es_letra(caracter: str) -> bool:
    """Acepta letras Unicode; incluye vocales acentuadas y ñ."""
    return len(caracter) == 1 and caracter.isalpha()


def es_digito(caracter: str) -> bool:
    return len(caracter) == 1 and caracter.isdecimal()


def crear_afd_identificador() -> Automata:
    afd = Automata("Identificador")
    afd.agregar_estado(Estado("q0", es_inicial=True, descripcion="Inicio"))
    afd.agregar_estado(Estado("q1", es_final=True, descripcion="Identificador válido"))
    afd.agregar_transicion_clase("q0", "LETRA", es_letra, "q1")
    afd.agregar_transicion("q0", "_", "q1")
    afd.agregar_transicion_clase("q1", "LETRA", es_letra, "q1")
    afd.agregar_transicion_clase("q1", "DIGITO", es_digito, "q1")
    afd.agregar_transicion("q1", "_", "q1")
    return afd


def crear_afd_numero() -> Automata:
    afd = Automata("Número")
    afd.agregar_estado(Estado("q0", es_inicial=True, descripcion="Inicio"))
    afd.agregar_estado(Estado("q1", es_final=True, descripcion="Entero"))
    afd.agregar_estado(Estado("q2", descripcion="Punto decimal"))
    afd.agregar_estado(Estado("q3", es_final=True, descripcion="Decimal"))
    afd.agregar_transicion_clase("q0", "DIGITO", es_digito, "q1")
    afd.agregar_transicion_clase("q1", "DIGITO", es_digito, "q1")
    afd.agregar_transicion("q1", ".", "q2")
    afd.agregar_transicion_clase("q2", "DIGITO", es_digito, "q3")
    afd.agregar_transicion_clase("q3", "DIGITO", es_digito, "q3")
    return afd


def crear_afd_cadena() -> Automata:
    afd = Automata("Cadena")
    afd.agregar_estado(Estado("q0", es_inicial=True, descripcion="Inicio"))
    afd.agregar_estado(Estado("q1", descripcion="Contenido"))
    afd.agregar_estado(Estado("q2", descripcion="Escape"))
    afd.agregar_estado(Estado("q3", es_final=True, descripcion="Cierre"))
    afd.agregar_transicion("q0", '"', "q1")
    afd.agregar_transicion_clase(
        "q1", "CARACTER (excepto comilla, barra y salto)",
        lambda c: c not in {'"', "\\", "\n", "\r"}, "q1"
    )
    afd.agregar_transicion("q1", "\\", "q2")
    afd.agregar_transicion("q1", '"', "q3")
    afd.agregar_transicion_clase("q2", "ESCAPE: n,t,r,comilla,barra", lambda c: c in 'ntr"\\', "q1")
    return afd


def crear_automatas() -> dict[str, Automata]:
    return {
        "identificador": crear_afd_identificador(),
        "numero": crear_afd_numero(),
        "cadena": crear_afd_cadena(),
    }
