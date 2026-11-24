# Estrategia de pruebas y trazabilidad

## Estrategia

Las pruebas usan `unittest` y entradas pequeñas con un propósito observable. Cubren el camino feliz, límites de AFD, Unicode, posiciones, recuperación múltiple, lectura y los tres exportadores. Los archivos temporales aíslan las pruebas de escritura.

Ejecutar desde la raíz:

```bash
python -m unittest discover -s tests -v
```

## Requisitos del profesor

| Requisito | Implementación | Verificación |
|---|---|---|
| Tokenizador desde cero | `AnalizadorLexico` + AFD manuales | `tests/test_lexer.py` |
| Tipo, lexema, línea y columna | `Token` y tablas CLI/GUI | Pruebas de categorías y posición |
| Entrada válida | `ejemplos/entrada_valida.txt` | CLI sin diagnósticos |
| Entrada con error | `ejemplos/entrada_invalida.txt` | Códigos `LEX001`/`LEX002` |
| README ejecutable | Instrucciones CLI, GUI y pruebas | Ejecución manual documentada |
| Recuperación | Consumo seguro tras cada error | `test_recuperacion_varios_errores` |
| Exportación | `ExportadorResultados` | `tests/test_exportador.py` |
| Visualizador real | Usa `AnalizadorLexico.automatas` | Simulación comparte `trazar()` |

## Límites de esta fase

No se valida el orden gramatical de tokens, la intención del comando ni la existencia de entidades académicas. El resaltado GUI es deliberadamente básico y se actualiza al pulsar Analizar. Esas decisiones mantienen separadas las futuras fases sintáctica, semántica y de ejecución.
