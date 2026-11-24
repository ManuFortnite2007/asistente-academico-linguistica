"""Presentación de resultados sintácticos en consola y archivo."""
from pathlib import Path
import sys
from src.analizadores.analizador_sintactico import AnalizadorSintactico

def ejecutar_sintaxis(args):
    try:
        texto = Path(args.archivo).read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as e:
        print(f"Error de lectura: {e}", file=sys.stderr)
        return 2
    lexico, sintaxis = AnalizadorSintactico().analizar_texto(texto)
    lineas = ["ANÁLISIS SINTÁCTICO — ASISTENTE ACADÉMICO", "=" * 55]
    for comando in sintaxis.comandos:
        lineas.append(f"[VÁLIDO] Línea {comando.linea}: {comando.texto}")
        if not args.sin_arbol:
            lineas.append(comando.arbol.arbol_texto())
        lineas.append("")
    for e in lexico.errores:
        lineas.append("[ERROR LÉXICO] " + str(e))
    for e in sintaxis.errores:
        lineas.append("[ERROR SINTÁCTICO] " + str(e))
    for numero in sintaxis.lineas_omitidas:
        lineas.append(f"[OMITIDA] Línea {numero}: contiene errores léxicos.")
    correcto = sintaxis.exitoso and not lexico.errores
    lineas.extend(["", "RESULTADO FINAL: " + ("SINTAXIS VÁLIDA" if correcto else "SINTAXIS INVÁLIDA"),
                   f"Comandos válidos: {len(sintaxis.comandos)} | Errores sintácticos: "
                   f"{len(sintaxis.errores)} | Errores léxicos: {len(lexico.errores)}"])
    salida = "\n".join(lineas)
    print(salida)
    if args.salida:
        try:
            Path(args.salida).write_text(salida + "\n", encoding="utf-8")
            print(f"Reporte escrito en: {args.salida}")
        except (OSError, ValueError) as e:
            print(f"Error de salida: {e}", file=sys.stderr)
            return 2
    return 0 if correcto else 1
