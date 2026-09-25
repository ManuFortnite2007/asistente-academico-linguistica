from pathlib import Path

from src.core.lector_texto import LectorTexto
from src.modelos.automata import Automata
from src.modelos.estado import Estado
from src.modelos.token import Token, TipoToken


def mostrar_lectura(lector: LectorTexto) -> None:
    print("\nLECTURA CARÁCTER POR CARÁCTER")
    print("-" * 50)
    for caracter in lector.recorrer():
        representacion = repr(caracter.valor)
        print(
            f"Índice={caracter.indice:03d} | "
            f"Línea={caracter.linea:02d} | "
            f"Columna={caracter.columna:02d} | "
            f"Carácter={representacion}"
        )


def demo_estructuras_base() -> None:
    print("\nDEMOSTRACIÓN DE ESTRUCTURAS BASE")
    print("-" * 50)

    token = Token(
        tipo=TipoToken.VERBO,
        lexema="mostrar",
        linea=1,
        columna=1,
    )
    print("Token de ejemplo:", token)

    q0 = Estado("q0", es_inicial=True)
    q1 = Estado("q1", es_final=True)

    automata = Automata(nombre="AutomataDemo")
    automata.agregar_estado(q0)
    automata.agregar_estado(q1)
    automata.agregar_transicion("q0", "a", "q1")

    print("Estados:", [estado.nombre for estado in automata.estados.values()])
    print("Acepta 'a':", automata.procesar("a"))
    print("Acepta 'b':", automata.procesar("b"))


def main() -> None:
    print("=" * 60)
    print("ASISTENTE ACADÉMICO - ESTRUCTURA BASE DEL PROYECTO")
    print("=" * 60)

    print("\nSelecciona una opción:")
    print("1. Leer una cadena escrita en consola")
    print("2. Leer el archivo de ejemplo")
    opcion = input("> ").strip()

    if opcion == "2":
        ruta = Path("ejemplos/entrada.txt")
        lector = LectorTexto.desde_archivo(ruta)
        print(f"\nArchivo cargado: {ruta}")
    else:
        texto = input("\nEscribe una cadena: ")
        lector = LectorTexto.desde_cadena(texto)

    mostrar_lectura(lector)
    demo_estructuras_base()


if __name__ == "__main__":
    main()
