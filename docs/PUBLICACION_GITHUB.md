# Guía de publicación en GitHub

Esta guía es para cuando el equipo decida publicar. **Los comandos de `push` aquí documentados no forman parte de la preparación local y no se ejecutan automáticamente.**

## 1. Verificación previa

Desde la raíz del proyecto:

```bash
git status
git branch --show-current
python -m unittest discover -s tests -v
python main.py analizar ejemplos/entrada_valida.txt
```

El estado esperado es una rama `feat/lexer-fase2-avanzado`, sin cambios pendientes y con todas las pruebas correctas.

## 2. Confirmar el destino

```bash
git remote -v
```

Actualmente `origin` señala al repositorio original. Si se desea publicar en otro repositorio o fork, no se debe sobrescribir el destino por accidente. Puede conservarse el original y agregar otro remoto:

```bash
git remote add entrega URL_DEL_NUEVO_REPOSITORIO
git remote -v
```

## 3. Publicar únicamente la rama

En el remoto original:

```bash
git push -u origin feat/lexer-fase2-avanzado
```

En un remoto nuevo llamado `entrega`:

```bash
git push -u entrega feat/lexer-fase2-avanzado
```

Esto publica la rama; no fusiona `main` ni `master`.

## 4. Pull request recomendado

En GitHub, cree un pull request desde `feat/lexer-fase2-avanzado` hacia la rama principal. Compruebe que la acción **Pruebas del lexer** termine correctamente en Python 3.10/3.12 para Windows y Linux. Revise el diff antes de fusionar.

## 5. Decisiones antes de hacerlo público

- Elegir una licencia con autorización de todos los integrantes. No se añadió una automáticamente porque implica una decisión legal del equipo.
- Verificar nombres, datos académicos y visibilidad deseada del repositorio.
- Decidir si se conserva el historial de la fase base.
- No versionar entornos virtuales, salidas exportadas ni credenciales.

## 6. Comprobación posterior

Tras publicar, pruebe una clonación limpia en otra carpeta:

```bash
git clone URL_DEL_REPOSITORIO copia-verificacion
cd copia-verificacion
git switch feat/lexer-fase2-avanzado
python -m unittest discover -s tests -v
python main.py --help
```
