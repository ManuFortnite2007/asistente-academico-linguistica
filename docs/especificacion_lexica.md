# Especificación del lenguaje léxico

## Alcance

El lexer reconoce unidades léxicas; no valida todavía gramática, intención ni existencia real de materias o tareas. La entrada es texto Unicode leído secuencialmente y las posiciones son 1-based.

## Categorías

| Categoría | Forma aceptada | Ejemplo |
|---|---|---|
| `VERBO` | Palabra del vocabulario de acciones | `mostrar` |
| `SUSTANTIVO` | Palabra nominal académica reservada | `tareas` |
| `ADJETIVO` | Modificador reservado | `pendientes` |
| `PREPOSICION` | Preposición española reservada | `de` |
| `DETERMINANTE` | Artículo/determinante reservado | `las` |
| `IDENTIFICADOR` | Letra o `_`, seguida por letras Unicode, dígitos o `_` | `curso_2026` |
| `NUMERO_ENTERO` | Uno o más dígitos decimales Unicode | `42` |
| `NUMERO_DECIMAL` | Dígitos, punto y uno o más dígitos | `95.5` |
| `CADENA` | Contenido entre comillas dobles | `"Proyecto"` |
| `OPERADOR` | `+ - * / = == != < <= > >= :` | `>=` |
| `DELIMITADOR` | `( ) [ ] { } , ; .` | `[` |
| `FIN` | Marcador con lexema vacío al acabar | — |

Las palabras se buscan con minúsculas y sin diacríticos, pero el token conserva la forma original. Por ello `MATEMÁTICAS` coincide con `matematicas` y mantiene su lexema.

## Espacios, comentarios y cadenas

- Espacio, tabulador vertical/horizontal y salto de página separan tokens.
- `LF`, `CR` y `CRLF` actualizan línea y columna; `CRLF` cuenta como un salto.
- `#` y `//` inician comentarios hasta fin de línea y no generan token.
- Las cadenas no atraviesan líneas.
- Escapes admitidos: `\\n`, `\\t`, `\\r`, `\\"` y `\\\\`. El lexer conserva el lexema escrito; no ejecuta el escape.

## Errores y recuperación

| Código | Causa | Recuperación |
|---|---|---|
| `LEX001` | Símbolo fuera del alfabeto | Consume exactamente el símbolo y continúa. |
| `LEX002` | Cadena sin cierre antes del salto/EOF | Conserva el fragmento, no emite `CADENA` y continúa en el salto. |
| `LEX003` | Punto decimal sin dígito posterior | Consume el fragmento numérico incompleto y continúa. |
| `LEX004` | Escape de cadena no admitido | Registra el escape, consume sus dos caracteres y continúa buscando el cierre. |

Toda rama de error consume al menos un carácter o termina al llegar a EOF; esto evita ciclos infinitos.

En las estadísticas, `total_tokens` cuenta las unidades reconocidas y excluye el centinela `FIN`. Las exportaciones conservan `FIN` para que futuros analizadores puedan consumir la secuencia completa.
