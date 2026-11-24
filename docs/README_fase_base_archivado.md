# Proyecto Integrador - Asistente Académico por Comandos Textuales

## Fase 2: Estructura inicial del código y arquitectura base

**Carrera:** Ingeniería en Sistemas Computacionales  
**Materia:** Lingüística Computacional  
**Integrantes:** Manuel Pool , Jorge Medina , Isaac Cardos  
**Profesor:** Alejandro Isidoro Madariaga  

---

## 1. Descripción

Este repositorio contiene la estructura base del proyecto integrador
**Asistente Académico por Comandos Textuales**.

El sistema se construirá durante el cuatrimestre para reconocer,
analizar y validar comandos escritos relacionados con actividades
académicas, por ejemplo:

```text
mostrar tareas pendientes
agregar tarea matematicas
consultar horario de redes
```

En esta fase todavía no se implementa el procesamiento completo del
lenguaje. El objetivo es establecer una arquitectura modular que sirva
de base para los analizadores:

- Léxico
- Sintáctico
- Semántico

También se incluye un módulo capaz de leer texto carácter por carácter,
ya sea desde una cadena escrita en consola o desde un archivo plano.

---

## 2. Restricción principal

El proyecto **NO utiliza librerías externas de Procesamiento de Lenguaje
Natural**.

No se utilizan herramientas como:

- NLTK
- spaCy
- Transformers
- TextBlob
- Stanza

Todo el procesamiento se construirá desde cero utilizando únicamente
Python y su biblioteca estándar.

---

## 3. Requisitos

- Python 3.10 o superior
- Windows, Linux o macOS
- Terminal o consola

No se requiere instalar paquetes adicionales.

---

## 4. Estructura del proyecto

```text
Asistente_Academico_Fase_2/
│
├── main.py
├── README.md
├── .gitignore
│
├── ejemplos/
│   └── entrada.txt
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── lector_texto.py
│   │
│   ├── modelos/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   ├── estado.py
│   │   └── automata.py
│   │
│   └── analizadores/
│       ├── __init__.py
│       ├── analizador_lexico.py
│       ├── analizador_sintactico.py
│       └── analizador_semantico.py
│
└── tests/
    └── test_base.py
```

---

## 5. Clases principales

### `Caracter`

Representa cada carácter leído e incluye:

- valor
- índice
- línea
- columna

Esto permitirá que en etapas posteriores los errores léxicos o
sintácticos puedan indicar exactamente dónde ocurrió el problema.

### `LectorTexto`

Puede recibir:

1. Una cadena escrita directamente.
2. Un archivo `.txt`.

Después permite recorrer la entrada **carácter por carácter**.

### `Token`

Representa una unidad léxica del lenguaje.

Atributos iniciales:

- tipo
- lexema
- línea
- columna

### `TipoToken`

Enumeración con categorías iniciales como:

- DETERMINANTE
- SUSTANTIVO
- VERBO
- PREPOSICION
- ADJETIVO
- NUMERO
- OPERADOR
- IDENTIFICADOR
- DESCONOCIDO
- FIN

### `Estado`

Representa un estado perteneciente a un autómata.

Permite indicar si es:

- Estado inicial
- Estado final

### `Automata`

Estructura base de un Autómata Finito Determinista.

Actualmente permite:

- Agregar estados.
- Definir un único estado inicial.
- Marcar estados finales.
- Crear transiciones.
- Procesar una cadena.
- Determinar si una cadena es aceptada o rechazada.

---

## 6. Cómo ejecutar el proyecto

### Opción A - Descargar el ZIP

1. Descomprimir el archivo.
2. Abrir una terminal dentro de la carpeta del proyecto.
3. Ejecutar:

```bash
python main.py
```

En algunos sistemas puede ser necesario utilizar:

```bash
python3 main.py
```

El programa mostrará dos opciones:

```text
1. Leer una cadena escrita en consola
2. Leer el archivo de ejemplo
```

Si se selecciona la primera opción, el usuario puede escribir cualquier
cadena.

Si se selecciona la segunda opción, se cargará:

```text
ejemplos/entrada.txt
```

Después se mostrará cada carácter con su índice, línea y columna.

---

## 7. Ejemplo de ejecución

Entrada:

```text
mostrar tarea
```

Salida aproximada:

```text
Índice=000 | Línea=01 | Columna=01 | Carácter='m'
Índice=001 | Línea=01 | Columna=02 | Carácter='o'
Índice=002 | Línea=01 | Columna=03 | Carácter='s'
...
```

Al final también se ejecuta una demostración de las estructuras
`Token`, `Estado` y `Automata`.

---

## 8. Ejecutar las pruebas

Desde la carpeta principal:

```bash
python -m unittest discover -s tests
```

o:

```bash
python3 -m unittest discover -s tests
```

Si todo funciona correctamente debe aparecer un resultado similar a:

```text
....
----------------------------------------------------------------------
Ran 4 tests

OK
```

---

## 9. Trabajo planeado para las siguientes fases

### Fase siguiente - Analizador léxico

Se desarrollará un reconocedor capaz de transformar el texto en una
secuencia de tokens mediante autómatas construidos manualmente.

Ejemplo:

```text
mostrar tareas pendientes
```

podrá convertirse posteriormente en:

```text
VERBO("mostrar")
SUSTANTIVO("tareas")
ADJETIVO("pendientes")
```

### Analizador sintáctico

Validará que los tokens cumplan la gramática definida para el proyecto.

### Analizador semántico

Comprobará que un comando sintácticamente válido también tenga sentido
dentro del dominio académico.

---

## 10. Estado actual

Esta entrega cumple con la estructura base solicitada:

- Lectura de cadenas de texto.
- Lectura de archivos planos.
- Recorrido carácter por carácter.
- Clase `Token`.
- Clase `Estado`.
- Clase `Automata`.
- Estructura preparada para análisis léxico.
- Estructura preparada para análisis sintáctico.
- Estructura preparada para análisis semántico.
- Código sin librerías externas.
- Archivo README con instrucciones de ejecución y prueba.
