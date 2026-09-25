from __future__ import annotations

from typing import Dict, Tuple

from src.modelos.estado import Estado


class Automata:
    """
    Implementación base de un autómata finito determinista.

    La clase todavía no representa el analizador final.
    Su objetivo en esta fase es establecer una arquitectura
    limpia y reutilizable para las siguientes entregas.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self.estados: Dict[str, Estado] = {}
        self.transiciones: Dict[Tuple[str, str], str] = {}

    def agregar_estado(self, estado: Estado) -> None:
        if estado.nombre in self.estados:
            raise ValueError(
                f"Ya existe un estado llamado '{estado.nombre}'."
            )

        if estado.es_inicial and self.estado_inicial() is not None:
            raise ValueError(
                "El autómata solamente puede tener un estado inicial."
            )

        self.estados[estado.nombre] = estado

    def agregar_transicion(
        self,
        origen: str,
        simbolo: str,
        destino: str
    ) -> None:
        if origen not in self.estados:
            raise ValueError(f"Estado de origen inexistente: {origen}")

        if destino not in self.estados:
            raise ValueError(f"Estado de destino inexistente: {destino}")

        if len(simbolo) != 1:
            raise ValueError(
                "Cada transición debe recibir exactamente un símbolo."
            )

        clave = (origen, simbolo)

        if clave in self.transiciones:
            raise ValueError(
                f"Ya existe una transición para {origen} con {simbolo!r}."
            )

        self.transiciones[clave] = destino

    def estado_inicial(self) -> Estado | None:
        for estado in self.estados.values():
            if estado.es_inicial:
                return estado
        return None

    def procesar(self, cadena: str) -> bool:
        inicial = self.estado_inicial()

        if inicial is None:
            raise RuntimeError(
                "El autómata no tiene un estado inicial definido."
            )

        actual = inicial.nombre

        for simbolo in cadena:
            siguiente = self.transiciones.get((actual, simbolo))

            if siguiente is None:
                return False

            actual = siguiente

        return self.estados[actual].es_final
