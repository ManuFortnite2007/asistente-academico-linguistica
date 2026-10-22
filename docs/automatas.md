# Autómatas y tablas de transición

Los tres AFD son creados en `src/analizadores/reconocedores.py` y los consumen tanto el lexer como el visualizador. Una transición inexistente representa rechazo.

## Identificador

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1: LETRA o _
    q1 --> q1: LETRA, DIGITO o _
    q1 --> [*]
```

| Estado | LETRA | DÍGITO | `_` | Acepta |
|---|---|---|---|---|
| `q0` | `q1` | — | `q1` | No |
| `q1` | `q1` | `q1` | `q1` | Sí |

## Número

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1: DIGITO
    q1 --> q1: DIGITO
    q1 --> q2: punto
    q2 --> q3: DIGITO
    q3 --> q3: DIGITO
    q1 --> [*]
    q3 --> [*]
```

| Estado | DÍGITO | `.` | Acepta |
|---|---|---|---|
| `q0` | `q1` | — | No |
| `q1` | `q1` | `q2` | Sí: entero |
| `q2` | `q3` | — | No |
| `q3` | `q3` | — | Sí: decimal |

## Cadena

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> q1: comilla
    q1 --> q1: carácter ordinario
    q1 --> q2: barra inversa
    q2 --> q1: escape admitido
    q1 --> q3: comilla
    q3 --> [*]
```

| Estado | Comilla | Barra | Ordinario | Escape válido | Acepta |
|---|---|---|---|---|---|
| `q0` | `q1` | — | — | — | No |
| `q1` | `q3` | `q2` | `q1` | — | No |
| `q2` | — | — | — | `q1` | No |
| `q3` | — | — | — | — | Sí |

El escáner añade diagnósticos y recuperación alrededor de este modelo formal: un escape inválido produce `LEX004`, y salto/EOF antes de `q3` produce `LEX002`.
