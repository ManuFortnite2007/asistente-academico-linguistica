"""Aplicación de escritorio oscura construida únicamente con Tkinter/ttk."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from src.analizadores.analizador_lexico import AnalizadorLexico
from src.core.exportador import ExportadorResultados
from src.gui.visualizador_automatas import VisualizadorAutomatas
from src.modelos.resultado import ResultadoAnalisis
from src.modelos.token import TipoToken


class AplicacionLexer(tk.Tk):
    COLORES = {
        "fondo": "#111111", "panel": "#1c1c1c", "texto": "#eeeeee",
        "secundario": "#aaaaaa", "acento": "#e53935", "seleccion": "#5b2020",
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("Lexer Pro · Asistente Académico")
        self.geometry("1240x790")
        self.minsize(960, 650)
        self.configure(bg=self.COLORES["fondo"])
        self.analizador = AnalizadorLexico()
        self.resultado: ResultadoAnalisis | None = None
        self._configurar_estilos()
        self._crear_interfaz()
        self.editor.insert("1.0", "mostrar tareas pendientes\nbuscar tarea \"Proyecto de redes\"")
        self._actualizar_lineas()

    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure(".", background=self.COLORES["panel"], foreground=self.COLORES["texto"], font=("Segoe UI", 10))
        estilo.configure("TButton", padding=(11, 7), background="#292929", foreground=self.COLORES["texto"])
        estilo.map("TButton", background=[("active", self.COLORES["acento"])])
        estilo.configure("Accent.TButton", background=self.COLORES["acento"], foreground="white")
        estilo.configure("Treeview", background="#181818", fieldbackground="#181818", foreground="#eeeeee", rowheight=25)
        estilo.configure("Treeview.Heading", background="#292929", foreground="white", font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview", background=[("selected", self.COLORES["seleccion"])])

    def _crear_interfaz(self) -> None:
        encabezado = tk.Frame(self, bg="#171717", height=58)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="LEXER PRO", bg="#171717", fg=self.COLORES["acento"], font=("Segoe UI", 18, "bold")).pack(side="left", padx=18, pady=12)
        tk.Label(encabezado, text="Analizador léxico · Comandos académicos", bg="#171717", fg="#bbbbbb", font=("Segoe UI", 10)).pack(side="left")
        barra = ttk.Frame(self, padding=(10, 8))
        barra.pack(fill="x")
        acciones = [
            ("Abrir archivo", self.abrir), ("Analizar texto", self.analizar),
            ("Limpiar entrada", self.limpiar), ("Guardar resultados", self.guardar),
            ("Ver autómata", self.ver_automata), ("Abrir ejemplos", self.abrir_ejemplo),
            ("Ayuda", self.ayuda),
        ]
        for texto, comando in acciones:
            ttk.Button(barra, text=texto, command=comando, style="Accent.TButton" if texto == "Analizar texto" else "TButton").pack(side="left", padx=3)

        panel = ttk.Panedwindow(self, orient="vertical")
        panel.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        superior = ttk.Frame(panel)
        inferior = ttk.Panedwindow(panel, orient="horizontal")
        panel.add(superior, weight=3)
        panel.add(inferior, weight=2)

        ttk.Label(superior, text="EDITOR DE ENTRADA", foreground=self.COLORES["acento"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(2, 5))
        cont_editor = tk.Frame(superior, bg="#0d0d0d")
        cont_editor.pack(fill="both", expand=True)
        self.numeros = tk.Text(cont_editor, width=5, padx=7, bg="#151515", fg="#666666", relief="flat", state="disabled", takefocus=0, font=("Consolas", 11))
        self.numeros.pack(side="left", fill="y")
        self.scroll_editor = ttk.Scrollbar(cont_editor)
        self.scroll_editor.pack(side="right", fill="y")
        self.editor = tk.Text(cont_editor, wrap="none", undo=True, bg="#0d0d0d", fg="#eeeeee", insertbackground="#e53935", selectbackground="#5b2020", relief="flat", padx=10, pady=8, font=("Consolas", 11), yscrollcommand=self._sincronizar_scroll)
        self.editor.pack(side="left", fill="both", expand=True)
        self.scroll_editor.configure(command=self._scroll_editor)
        self.editor.bind("<KeyRelease>", lambda _e: self._actualizar_lineas())
        self.editor.bind("<MouseWheel>", lambda _e: self.after_idle(self._actualizar_lineas))
        self._configurar_tags()

        tokens_frame = ttk.Frame(inferior, padding=(0, 8, 5, 0))
        errores_frame = ttk.Frame(inferior, padding=(5, 8, 0, 0))
        inferior.add(tokens_frame, weight=3)
        inferior.add(errores_frame, weight=2)
        ttk.Label(tokens_frame, text="TOKENS", foreground=self.COLORES["acento"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.tabla = ttk.Treeview(tokens_frame, columns=("tipo", "lexema", "linea", "columna"), show="headings")
        for columna, titulo, ancho in (("tipo", "Tipo", 145), ("lexema", "Lexema", 230), ("linea", "Línea", 65), ("columna", "Columna", 75)):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="center" if columna in {"linea", "columna"} else "w")
        scroll_tokens = ttk.Scrollbar(tokens_frame, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_tokens.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll_tokens.pack(side="right", fill="y")
        ttk.Label(errores_frame, text="DIAGNÓSTICOS", foreground=self.COLORES["acento"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        self.errores = tk.Listbox(errores_frame, bg="#181818", fg="#f2b8b5", selectbackground=self.COLORES["seleccion"], relief="flat", font=("Segoe UI", 9))
        self.errores.pack(fill="both", expand=True)
        self.errores.bind("<<ListboxSelect>>", self._localizar_error)
        self.estado = tk.StringVar(value="Listo para analizar.")
        ttk.Label(self, textvariable=self.estado, padding=(12, 7)).pack(fill="x")

    def _configurar_tags(self) -> None:
        colores = {
            "VERBO": "#ff6b6b", "SUSTANTIVO": "#82b1ff", "ADJETIVO": "#b388ff",
            "PREPOSICION": "#ffd180", "DETERMINANTE": "#80cbc4", "IDENTIFICADOR": "#eeeeee",
            "NUMERO_ENTERO": "#c5e1a5", "NUMERO_DECIMAL": "#c5e1a5", "CADENA": "#ffe082",
            "OPERADOR": "#ff8a80", "DELIMITADOR": "#b0bec5",
        }
        for etiqueta, color in colores.items():
            self.editor.tag_configure(etiqueta, foreground=color)
        self.editor.tag_configure("ERROR", background="#5a1717", underline=True)

    def abrir(self) -> None:
        ruta = filedialog.askopenfilename(title="Abrir entrada", filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if ruta:
            try:
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", Path(ruta).read_text(encoding="utf-8"))
                self._actualizar_lineas()
                self.estado.set(f"Archivo abierto: {ruta}")
            except (OSError, UnicodeError) as error:
                messagebox.showerror("No se pudo abrir", str(error), parent=self)

    def abrir_ejemplo(self) -> None:
        base = Path(__file__).resolve().parents[2] / "ejemplos"
        ruta = filedialog.askopenfilename(initialdir=base, title="Abrir ejemplo", filetypes=[("Texto", "*.txt")])
        if ruta:
            try:
                self.editor.delete("1.0", "end")
                self.editor.insert("1.0", Path(ruta).read_text(encoding="utf-8"))
                self._actualizar_lineas()
            except OSError as error:
                messagebox.showerror("Error", str(error), parent=self)

    def analizar(self) -> None:
        texto = self.editor.get("1.0", "end-1c")
        self.resultado = self.analizador.analizar(texto)
        self.tabla.delete(*self.tabla.get_children())
        self.errores.delete(0, "end")
        for etiqueta in self.editor.tag_names():
            if etiqueta not in {"sel"}:
                self.editor.tag_remove(etiqueta, "1.0", "end")
        for token in self.resultado.tokens:
            self.tabla.insert("", "end", values=(token.tipo.name, token.lexema, token.linea, token.columna))
            if token.tipo is not TipoToken.FIN:
                inicio = f"{token.linea}.{token.columna - 1}"
                self.editor.tag_add(token.tipo.name, inicio, f"{inicio}+{len(token.lexema)}c")
        for error in self.resultado.errores:
            self.errores.insert("end", f"{error.codigo} · L{error.linea}:C{error.columna} · {error.descripcion}")
            inicio = f"{error.linea}.{error.columna - 1}"
            self.editor.tag_add("ERROR", inicio, f"{inicio}+{max(1, len(error.fragmento))}c")
        resumen = self.resultado.resumen()
        self.estado.set(f"{resumen['total_tokens']} tokens · {resumen['numero_errores']} errores · {resumen['estado_final']}")

    def limpiar(self) -> None:
        self.editor.delete("1.0", "end")
        self.tabla.delete(*self.tabla.get_children())
        self.errores.delete(0, "end")
        self.resultado = None
        self._actualizar_lineas()
        self.estado.set("Editor limpio.")

    def guardar(self) -> None:
        if self.resultado is None:
            self.analizar()
        ruta = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("CSV", "*.csv"), ("Texto", "*.txt")])
        if ruta and self.resultado:
            try:
                ExportadorResultados.exportar(self.resultado, ruta)
                self.estado.set(f"Resultados guardados: {ruta}")
            except (OSError, ValueError) as error:
                messagebox.showerror("Error de exportación", str(error), parent=self)

    def ver_automata(self) -> None:
        VisualizadorAutomatas(self, self.analizador.automatas)

    def ayuda(self) -> None:
        messagebox.showinfo(
            "Ayuda",
            "Escriba o abra un archivo .txt y pulse Analizar texto.\n\n"
            "Los colores identifican categorías léxicas. Seleccione un diagnóstico "
            "para ir a su posición. Ver autómata permite simular los mismos AFD paso a paso.",
            parent=self,
        )

    def _localizar_error(self, _evento: object) -> None:
        if not self.resultado or not self.errores.curselection():
            return
        error = self.resultado.errores[self.errores.curselection()[0]]
        indice = f"{error.linea}.{error.columna - 1}"
        self.editor.mark_set("insert", indice)
        self.editor.see(indice)
        self.editor.focus_set()

    def _actualizar_lineas(self) -> None:
        total = int(self.editor.index("end-1c").split(".")[0])
        self.numeros.configure(state="normal")
        self.numeros.delete("1.0", "end")
        self.numeros.insert("1.0", "\n".join(str(i) for i in range(1, total + 1)))
        self.numeros.configure(state="disabled")

    def _sincronizar_scroll(self, primero: str, ultimo: str) -> None:
        self.scroll_editor.set(primero, ultimo)
        self.numeros.yview_moveto(primero)

    def _scroll_editor(self, *args: str) -> None:
        self.editor.yview(*args)
        self.numeros.yview(*args)


def iniciar_gui() -> None:
    AplicacionLexer().mainloop()
