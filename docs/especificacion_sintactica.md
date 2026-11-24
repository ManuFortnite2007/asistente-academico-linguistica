# Fase 3 — Diseño e implementación del parser

Implementación propia de un analizador **descendente recursivo LL(1)** integrado
con `AnalizadorLexico`; no se usan generadores de parsers ni dependencias externas.

## Gramática libre de contexto

En los terminales específicos se verifica `TipoToken` más lexema
normalizado; `CADENA`, `IDENTIFICADOR`, `SUSTANTIVO` y los números
pueden representar una categoría completa según la producción.

```text
S             → Comando FIN
Comando       → Mostrar | Agregar | Consultar | Buscar
Mostrar       → MOSTRAR ObjVisual Filtro
ObjVisual     → TAREAS | HORARIOS | MATERIAS | EXAMENES | PROYECTOS
              | RECORDATORIOS | CALIFICACIONES
Filtro        → PENDIENTES | COMPLETADAS | PROXIMOS | Lista | ε
Lista         → CORCH_I Num ColaNums CORCH_D
ColaNums      → COMA Num ColaNums | ε
Num           → NUM_ENTERO | NUM_DECIMAL
Agregar       → AGREGAR Carga
Carga         → TipoAlta Nombre | CALIFICACION Num
TipoAlta      → TAREA | MATERIA | EXAMEN | PROYECTO | RECORDATORIO
Consultar     → CONSULTAR DetOpt ObjConsulta RefOpt
DetOpt        → EL | LA | LOS | LAS | ε
ObjConsulta   → HORARIO | HORARIOS | MATERIA | MATERIAS | TAREA | TAREAS
              | EXAMEN | EXAMENES | CALIFICACION | CALIFICACIONES
RefOpt        → DE Nombre | ε
Buscar        → BUSCAR TipoBusqueda Nombre
TipoBusqueda  → TAREA | MATERIA | EXAMEN | PROYECTO | RECORDATORIO
Nombre        → CADENA | IDENTIFICADOR | SUSTANTIVO
```

## Arquitectura y árbol

El lector de archivos alimenta al lexer de la fase anterior, que genera
objetos Token (tipo, lexema, línea, columna, normalizado). El parser agrupa
los tokens por línea y les añade un FIN lógico; acepta un solo comando por
línea. Cada no terminal corresponde a una función recursiva que crea un
`NodoSintactico` con sus hijos. Las llamadas anidadas cumplen el papel
de la pila en un autómata a pila equivalente a la gramática.

El árbol incluye símbolos no terminales, terminales, lexema y posición,
y puede imprimirse en consola o convertirse en un diccionario de Python.

## Manejo de errores

- **SYN001**: token inesperado frente a la regla actual.
- **SYN002**: fin de comando, faltaba un símbolo obligatorio.
- **SYN003**: tokens sobrantes después de un comando completo.
- **SYN004**: verbo/acción no admitido.

Cada diagnóstico incluye línea, columna, tipo y lexema inesperados y el
conjunto de terminales esperados. La recuperación *panic mode* descarta
la sentencia defectuosa y continúa en la próxima línea. Si una línea
presenta errores léxicos, no se acepta como sentencia sintácticamente
correcta; se informa su omisión.

## Ejecución

Desde la carpeta principal con Python 3.10+:

```bash
python main.py sintaxis ejemplos/sintaxis_valida.txt
python main.py sintaxis ejemplos/sintaxis_invalida.txt
python main.py sintaxis ejemplos/sintaxis_valida.txt --salida resultado_parser.txt
python main.py sintaxis ejemplos/sintaxis_valida.txt --sin-arbol
python -m unittest discover -s tests -v
```

Código de salida: 0 si todo es válido, 1 si hay fallos léxicos o
sintácticos, 2 si falla la lectura/escritura de archivo.

Limitación: el parser reconoce estructura, pero todavía no comprueba si
la materia o tarea realmente existe, ni ejecuta las acciones. Eso se
reserva para el análisis semántico.
