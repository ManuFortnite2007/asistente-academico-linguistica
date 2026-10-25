"""Interfaz de línea de comandos no interactiva."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.analizadores.analizador_lexico import AnalizadorLexico
from src.core.exportador import ExportadorResultados
from src.core.lector_texto import LectorTexto
from src.modelos.resultado import ResultadoAnalisis


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Analizador léxico AFD para comandos académicos.",
    )
    parser.add_argument("--gui", action="store_true", help="Abre la interfaz gráfica Tkinter.")
    subparsers = parser.add_subparsers(dest="comando")
    analizar = subparsers.add_parser("analizar", help="Analiza un archivo de texto completo.")
    analizar.add_argument("archivo", type=Path, help="Ruta del archivo UTF-8 de entrada.")
    analizar.add_argument("--exportar", type=Path, help="Archivo de salida .txt, .csv o .json.")
    analizar.add_argument("--formato", choices=("txt", "csv", "json"), help="Formato explícito de exportación.")
    analizar.add_argument("--traza", choices=("identificador", "numero", "cadena"), help="AFD que se trazará.")
    analizar.add_argument("--entrada-traza", help="Cadena independiente para la simulación del AFD.")
    return parser


def tabla_resultado(resultado: ResultadoAnalisis) -> str:
    filas = [("TIPO", "LEXEMA", "LÍNEA", "COLUMNA")]
    filas.extend(
        (t.tipo.name, t.lexema.replace("\n", "\\n"), str(t.linea), str(t.columna))
        for t in resultado.tokens
    )
    anchos = [max(len(fila[i]) for fila in filas) for i in range(4)]
    separador = "+" + "+".join("-" * (ancho + 2) for ancho in anchos) + "+"
    salida = [separador]
    for numero, fila in enumerate(filas):
        salida.append("| " + " | ".join(valor.ljust(anchos[i]) for i, valor in enumerate(fila)) + " |")
        if numero == 0:
            salida.append(separador)
    salida.append(separador)
    return "\n".join(salida)


def ejecutar_analisis(args: argparse.Namespace) -> int:
    try:
        texto = LectorTexto.desde_archivo(args.archivo).contenido
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error al leer {args.archivo}: {error}", file=sys.stderr)
        return 2
    analizador = AnalizadorLexico()
    resultado = analizador.analizar(texto)
    print(tabla_resultado(resultado))
    if resultado.errores:
        print("\nDIAGNÓSTICOS")
        for error in resultado.errores:
            print(f"- {error}")
    else:
        print("\nAnálisis completado sin errores léxicos.")
    print("Resumen:", resultado.resumen())

    if args.traza:
        entrada = args.entrada_traza
        if entrada is None:
            print("--traza requiere --entrada-traza.", file=sys.stderr)
            return 2
        traza = analizador.automata(args.traza).trazar(entrada)
        print(f"\nTRAZA AFD: {analizador.automata(args.traza).nombre}")
        for paso in traza.pasos:
            print(f"Paso {paso.numero}: {paso.origen} --{paso.simbolo!r}--> {paso.destino or 'RECHAZO'}")
        print("Resultado:", "ACEPTADA" if traza.aceptada else "RECHAZADA")

    if args.exportar:
        try:
            ruta = ExportadorResultados.exportar(resultado, args.exportar, args.formato)
            print(f"Resultados exportados: {ruta.resolve()}")
        except (OSError, ValueError) as error:
            print(f"Error de exportación: {error}", file=sys.stderr)
            return 2
    return 0 if resultado.exitoso else 1


def ejecutar(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    argumentos = sys.argv[1:] if argv is None else argv
    # Al abrir main.py con doble clic, Windows no envía argumentos. En ese
    # caso iniciamos la interfaz gráfica; la CLI conserva su comportamiento
    # cuando se proporciona un subcomando u opción explícita.
    if not argumentos:
        argumentos = ["--gui"]
    args = parser.parse_args(argumentos)
    if args.gui:
        try:
            from src.gui.aplicacion import iniciar_gui
            iniciar_gui()
            return 0
        except ImportError as error:
            print(f"Tkinter no está disponible: {error}", file=sys.stderr)
            return 3
    if args.comando == "analizar":
        return ejecutar_analisis(args)
    parser.print_help()
    return 0
