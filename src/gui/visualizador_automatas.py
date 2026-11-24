"""Visualizador Canvas y simulador paso a paso de los AFD reales."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from src.modelos.automata import Automata, ResultadoAutomata


class VisualizadorAutomatas(tk.Toplevel):
    def __init__(self, padre: tk.Misc, automatas: dict[str, Automata]) -> None:
        super().__init__(padre)
        self.title("Visualizador de autómatas finitos")
        self.geometry("960x650")
        self.configure(bg="#121212")
        self.automatas = automatas
        self.traza: ResultadoAutomata | None = None
        self.paso = 0

        controles = ttk.Frame(self, padding=10)
        controles.pack(fill="x")
        ttk.Label(controles, text="Autómata:").pack(side="left")
        self.nombre = tk.StringVar(value=next(iter(automatas)))
        selector = ttk.Combobox(
            controles, textvariable=self.nombre, values=list(automatas), state="readonly", width=18
        )
        selector.pack(side="left", padx=6)
        selector.bind("<<ComboboxSelected>>", lambda _e: self.preparar())
        ttk.Label(controles, text="Entrada:").pack(side="left", padx=(15, 0))
        self.entrada = ttk.Entry(controles, width=35)
        self.entrada.pack(side="left", padx=6)
        ttk.Button(controles, text="Preparar", command=self.preparar).pack(side="left", padx=3)
        ttk.Button(controles, text="Paso siguiente", command=self.avanzar).pack(side="left", padx=3)

        self.canvas = tk.Canvas(self, bg="#191919", highlightthickness=0, height=390)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        self.estado_texto = tk.StringVar(value="Escriba una entrada y pulse Preparar.")
        ttk.Label(self, textvariable=self.estado_texto, padding=(12, 6)).pack(fill="x")
        self.detalle = tk.Text(
            self, height=8, bg="#0d0d0d", fg="#eeeeee", insertbackground="white",
            relief="flat", font=("Consolas", 10), state="disabled"
        )
        self.detalle.pack(fill="x", padx=10, pady=(0, 10))
        self.preparar()

    def preparar(self) -> None:
        automata = self.automatas[self.nombre.get()]
        self.traza = automata.trazar(self.entrada.get())
        self.paso = 0
        self._dibujar(automata, automata.estado_inicial().nombre)  # type: ignore[union-attr]
        self._actualizar_detalle()

    def avanzar(self) -> None:
        if self.traza is None:
            self.preparar()
            return
        if self.paso < len(self.traza.pasos):
            self.paso += 1
        if self.paso:
            paso_actual = self.traza.pasos[self.paso - 1]
            actual = paso_actual.destino or paso_actual.origen
        else:
            actual = None
        if actual is None:
            actual = self.automatas[self.nombre.get()].estado_inicial().nombre  # type: ignore[union-attr]
        self._dibujar(self.automatas[self.nombre.get()], actual)
        self._actualizar_detalle()

    def _actualizar_detalle(self) -> None:
        assert self.traza is not None
        lineas = [f"Entrada: {self.traza.entrada!r}"]
        for paso in self.traza.pasos[:self.paso]:
            lineas.append(
                f"Paso {paso.numero}: {paso.origen} --{paso.simbolo!r}--> {paso.destino or 'RECHAZO'}"
            )
        if self.paso == len(self.traza.pasos):
            lineas.append("Resultado: " + ("ACEPTADA" if self.traza.aceptada else "RECHAZADA"))
        else:
            lineas.append(f"Paso {self.paso + 1} de {len(self.traza.pasos)}")
        self.estado_texto.set(lineas[-1])
        self.detalle.configure(state="normal")
        self.detalle.delete("1.0", "end")
        self.detalle.insert("1.0", "\n".join(lineas))
        self.detalle.configure(state="disabled")

    def _dibujar(self, automata: Automata, actual: str) -> None:
        self.canvas.delete("all")
        estados = list(automata.estados.values())
        ancho = max(self.canvas.winfo_width(), 850)
        separacion = ancho // (len(estados) + 1)
        posiciones = {estado.nombre: (separacion * (i + 1), 185) for i, estado in enumerate(estados)}
        self.canvas.create_text(18, 20, anchor="w", text=automata.nombre, fill="#f44336", font=("Segoe UI", 16, "bold"))

        # Agrupa etiquetas para no dibujar arcos duplicados entre el mismo par.
        grupos: dict[tuple[str, str], list[str]] = {}
        for origen in automata.estados:
            for etiqueta, destino in automata.etiquetas_desde(origen):
                grupos.setdefault((origen, destino), []).append(etiqueta)
        for (origen, destino), etiquetas in grupos.items():
            x1, y1 = posiciones[origen]
            x2, y2 = posiciones[destino]
            texto = ", ".join(etiquetas)
            if origen == destino:
                self.canvas.create_arc(x1 - 34, y1 - 82, x1 + 34, y1 - 12, start=15, extent=330, style="arc", outline="#a0a0a0", width=2)
                self.canvas.create_text(x1, y1 - 92, text=texto, fill="#dddddd", font=("Segoe UI", 8))
            else:
                direccion = 1 if x2 > x1 else -1
                self.canvas.create_line(x1 + 31 * direccion, y1, x2 - 31 * direccion, y2, arrow="last", fill="#a0a0a0", width=2)
                self.canvas.create_text((x1 + x2) / 2, y1 - 15, text=texto, fill="#dddddd", font=("Segoe UI", 8))

        inicial = automata.estado_inicial()
        if inicial:
            x, y = posiciones[inicial.nombre]
            self.canvas.create_line(x - 75, y, x - 34, y, arrow="last", fill="#f44336", width=2)
        for estado in estados:
            x, y = posiciones[estado.nombre]
            color = "#d32f2f" if estado.nombre == actual else "#303030"
            borde = "#ff6b6b" if estado.nombre == actual else "#dddddd"
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=color, outline=borde, width=3)
            if estado.es_final:
                self.canvas.create_oval(x - 24, y - 24, x + 24, y + 24, outline=borde, width=2)
            self.canvas.create_text(x, y, text=estado.nombre, fill="white", font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, y + 52, text=estado.descripcion, fill="#bbbbbb", width=130, font=("Segoe UI", 8))
