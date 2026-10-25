# Asistente Académico — Lexer Pro

Aplicación desarrollada para la Fase 2 del Proyecto Integrador de **Lingüística Computacional**.

**Carrera:** Ingeniería en Sistemas Computacionales  
**Profesor:** Alejandro Isidoro Madariaga  
**Integrantes:** Manuel Pool, Jorge Medina e Isaac Cardos

## Descripción y objetivo

La aplicación analiza comandos académicos escritos en un lenguaje natural controlado y los convierte en tokens. Cada token conserva su tipo, lexema y posición dentro del texto. El reconocimiento se realiza con autómatas finitos deterministas implementados con la biblioteca estándar de Python.

Ejemplo:

```text
mostrar tareas pendientes
buscar tarea "Proyecto de redes"
```

Esta versión se concentra en el análisis léxico. El análisis sintáctico, el análisis semántico y la ejecución de acciones académicas quedan reservados para fases posteriores.

## Funcionalidades implementadas

- Lexer secuencial para archivos completos y texto escrito.
- AFD reutilizables para identificadores, números y cadenas.
- Vocabulario académico con verbos, sustantivos, adjetivos, preposiciones y determinantes.
- Identificadores Unicode, enteros, decimales, cadenas, operadores y delimitadores.
- Comentarios `#` y `//`, espacios, tabulaciones, CR/LF/CRLF y múltiples líneas.
- Escapes de cadena `\\n`, `\\t`, `\\r`, `\\"` y `\\\\`.
- Diagnósticos `LEX001` a `LEX004` con posición, fragmento, descripción y sugerencia.
- Recuperación tras errores independientes sin ciclos infinitos.
- CLI con tabla, trazas, códigos de salida y exportación.
- GUI oscura Tkinter/ttk con editor, números de línea, resaltado y navegación de errores.
- Visualizador Canvas con estados, aceptación, transiciones y simulación paso a paso.
- Exportación a TXT, CSV y JSON con estadísticas.
- Pruebas automatizadas `unittest` sin dependencias externas.

## Cómo funciona

El programa recibe un texto y lo recorre carácter por carácter. Según el símbolo encontrado, selecciona el autómata adecuado para reconocer identificadores, números o cadenas; los operadores y delimitadores se comparan con los símbolos admitidos por el lenguaje.

Cuando una palabra coincide con el vocabulario académico, se clasifica como verbo, sustantivo, adjetivo, preposición o determinante. Las demás palabras válidas se conservan como identificadores. Al finalizar, el lexer entrega la lista de tokens, los diagnósticos encontrados y un resumen del análisis.

La interfaz gráfica, la consola y los exportadores utilizan el mismo resultado, por lo que muestran la misma información. Si aparece un error, el lexer registra su ubicación e intenta continuar con el resto de la entrada.

## Requisitos

- Python 3.10 o superior.
- Tkinter solo para la GUI. En Windows suele venir con Python; en Arch/CachyOS puede instalarse mediante el paquete del sistema `tk`.
- No es necesario ejecutar `pip install`; `requirements.txt` confirma que no hay dependencias externas.

## Instalación

Clone el repositorio y entre en la carpeta del proyecto:

```bash
git clone --branch feat/lexer-fase2-avanzado --single-branch https://github.com/ManuFortnite2007/asistente-academico-linguistica.git
cd asistente-academico-linguistica
```

No hay paquetes de Python que instalar. Compruebe la versión y ejecute las pruebas:

```bash
python --version
python -m unittest discover -s tests -v
```

En Linux puede ser necesario usar `python3` en lugar de `python`. Para habilitar la GUI:

```bash
# Arch Linux / CachyOS
sudo pacman -S tk

# Debian / Ubuntu
sudo apt install python3-tk
```

En Windows, Tkinter se incluye normalmente al instalar Python desde python.org. Si el comando `python` no está disponible, utilice `py`:

```powershell
py main.py --gui
```

## Estructura

```text
.
├── main.py
├── README.md
├── requirements.txt
├── .github/workflows/tests.yml
├── ejemplos/
│   ├── entrada.txt
│   ├── entrada_valida.txt
│   ├── entrada_invalida.txt
│   ├── entrada_multilinea.txt
│   └── entrada_avanzada.txt
├── docs/
│   ├── arquitectura.md
│   ├── automatas.md
│   ├── especificacion_lexica.md
│   ├── pruebas_y_trazabilidad.md
│   └── README_fase_base_archivado.md
├── src/
│   ├── analizadores/
│   │   ├── analizador_lexico.py
│   │   ├── reconocedores.py
│   │   ├── analizador_sintactico.py
│   │   └── analizador_semantico.py
│   ├── core/
│   │   ├── lector_texto.py
│   │   └── exportador.py
│   ├── gui/
│   │   ├── aplicacion.py
│   │   └── visualizador_automatas.py
│   └── modelos/
│       ├── automata.py
│       ├── diagnostico.py
│       ├── estado.py
│       ├── resultado.py
│       └── token.py
└── tests/
    ├── test_base.py
    ├── test_exportador.py
    └── test_lexer.py
```

## Uso por consola

Mostrar ayuda:

```bash
python main.py --help
```

Analizar una entrada válida:

```bash
python main.py analizar ejemplos/entrada_valida.txt
```

Analizar una entrada con errores:

```bash
python main.py analizar ejemplos/entrada_invalida.txt
```

Exportar el mismo resultado a JSON, CSV o TXT:

```bash
python main.py analizar ejemplos/entrada_avanzada.txt --exportar salida.json
python main.py analizar ejemplos/entrada_valida.txt --exportar salida.csv
python main.py analizar ejemplos/entrada_invalida.txt --exportar salida.txt
```

Mostrar una traza real del AFD:

```bash
python main.py analizar ejemplos/entrada_valida.txt --traza identificador --entrada-traza curso_2026
```

Los códigos de salida son: `0` análisis correcto, `1` errores léxicos encontrados, `2` error de argumentos/archivo/exportación y `3` Tkinter no disponible.

## Interfaz gráfica

```bash
python main.py --gui
```

También puede abrirse haciendo doble clic en `main.py`: cuando no recibe argumentos, el programa inicia la interfaz gráfica automáticamente.

La barra permite abrir texto, analizar, limpiar, guardar resultados, elegir ejemplos, consultar ayuda y abrir el visualizador. Al seleccionar un diagnóstico, el cursor salta a su posición. El visualizador permite elegir `identificador`, `numero` o `cadena`, preparar una entrada y avanzar transición por transición sobre los mismos AFD del lexer.

Si Tkinter no está instalado, la CLI continúa completamente operativa.

## Categorías de tokens

`VERBO`, `SUSTANTIVO`, `ADJETIVO`, `PREPOSICION`, `DETERMINANTE`, `IDENTIFICADOR`, `NUMERO_ENTERO`, `NUMERO_DECIMAL`, `CADENA`, `OPERADOR`, `DELIMITADOR` y `FIN`.

Una palabra desconocida con forma válida se clasifica como `IDENTIFICADOR`, no como error. Las palabras reservadas se comparan normalizadas a minúsculas y sin diacríticos; el lexema original siempre se conserva.

Consulte la [especificación léxica](docs/especificacion_lexica.md) para el alfabeto, escapes y recuperación, y [autómatas](docs/automatas.md) para diagramas y tablas de transición.

## Ejemplo de salida

Para `mostrar tareas pendientes`:

```text
+-----------+------------+-------+---------+
| TIPO      | LEXEMA     | LÍNEA | COLUMNA |
+-----------+------------+-------+---------+
| VERBO     | mostrar    | 1     | 1       |
| SUSTANTIVO| tareas     | 1     | 9       |
| ADJETIVO  | pendientes | 1     | 16      |
| FIN       |            | 1     | 26      |
+-----------+------------+-------+---------+
```

La anchura real se ajusta automáticamente al contenido.

## Errores léxicos

- `LEX001`: símbolo no reconocido.
- `LEX002`: cadena sin comilla de cierre.
- `LEX003`: decimal incompleto.
- `LEX004`: secuencia de escape no admitida.

Cada diagnóstico contiene tipo, descripción, fragmento, línea, columna y sugerencia. La estrategia exacta se documenta en [especificacion_lexica.md](docs/especificacion_lexica.md).

## Pruebas

```bash
python -m unittest discover -s tests -v
```

La suite cubre palabras, números, identificadores, vocabulario reservado, cadenas, escapes, símbolos inválidos, entrada vacía, Unicode, posiciones, CRLF, estados y transiciones, recuperación, exportación y lectura de archivos. La matriz requisito-prueba está en [pruebas_y_trazabilidad.md](docs/pruebas_y_trazabilidad.md).

GitHub Actions ejecuta esta misma suite con Python 3.10 y 3.12 en Windows y Linux después de cada `push` y al abrir un pull request.

## Solución de problemas

- **`python` no se reconoce en Windows:** pruebe `py` o reinstale Python activando “Add Python to PATH”.
- **`No module named tkinter`:** instale el paquete `tk`/`python3-tk` de su distribución; la modalidad de consola seguirá funcionando.
- **Archivo no encontrado:** ejecute los comandos desde la carpeta que contiene `main.py`.
- **La entrada inválida termina con código 1:** es el comportamiento esperado; indica que el análisis finalizó y encontró errores léxicos.
- **Caracteres acentuados incorrectos:** guarde las entradas `.txt` con codificación UTF-8.

## Arquitectura y modelo de AFD

`Automata` admite transiciones exactas y predicados de clase (`LETRA`, `DIGITO`). El método `trazar()` registra las transiciones que después utiliza el simulador visual. `ResultadoAnalisis` reúne los tokens, diagnósticos y estadísticas que consumen la consola, la interfaz y los exportadores. Consulte [arquitectura.md](docs/arquitectura.md) para conocer los componentes y sus responsabilidades.

## Limitaciones actuales

- No existe todavía validación sintáctica ni semántica.
- El vocabulario reservado es inicial y ampliable; términos no registrados son identificadores.
- Las cadenas no pueden abarcar varias líneas.
- No se ejecutan operaciones académicas ni se persisten tareas.
- El resaltado GUI se actualiza al solicitar un análisis, no mientras se escribe.

## Trabajo futuro

Las siguientes fases pueden incorporar una gramática de comandos, un árbol de sintaxis, validación semántica, un catálogo académico y ejecución controlada de acciones.
