"""Pruebas de la fase 3 con el lexer real (unittest estándar)."""
import unittest
from src.analizadores.analizador_sintactico import AnalizadorSintactico

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = AnalizadorSintactico()

    def test_comandos_validos_con_arbol(self):
        casos = (
            "mostrar tareas pendientes",
            "mostrar tareas",
            "mostrar recordatorios [1, 2, 3]",
            "agregar tarea matemáticas",
            "agregar calificacion 95.5",
            "consultar horario de redes",
            "consultar el horario de redes",
            'buscar tarea "Proyecto de redes"',
        )
        for entrada in casos:
            with self.subTest(entrada=entrada):
                lexer, resultado = self.parser.analizar_texto(entrada)
                self.assertFalse(lexer.errores)
                self.assertTrue(resultado.exitoso, resultado.errores)
                self.assertEqual(len(resultado.comandos), 1)
                arbol = resultado.comandos[0].arbol
                self.assertEqual(arbol.simbolo, "S")
                self.assertIn("Comando", arbol.arbol_texto())
                self.assertEqual(arbol.hijos[-1].simbolo, "FIN")

    def test_comandos_invalidos_reportan_posicion_y_esperados(self):
        for entrada, codigo, col in (
            ("mostrar pendientes", "SYN001", 9),
            ("buscar tarea", "SYN002", 13),
            ("mostrar tareas de redes", "SYN001", 16),
            ("listar tareas", "SYN004", 1),
            ("mostrar tareas pendientes extra", "SYN003", 27),
            ("mostrar recordatorios [1, ]", "SYN001", 27),
        ):
            with self.subTest(entrada=entrada):
                lexer, r = self.parser.analizar_texto(entrada)
                self.assertFalse(lexer.errores)
                self.assertEqual(len(r.errores), 1)
                e = r.errores[0]
                self.assertEqual((e.codigo, e.linea, e.columna), (codigo, 1, col))
                self.assertTrue(e.esperados)

    def test_recuperacion_por_linea(self):
        _, r = self.parser.analizar_texto(
            "mostrar pendientes\nconsultar el horario de redes\nbuscar tarea\nagregar tarea matematicas")
        self.assertEqual([c.linea for c in r.comandos], [2, 4])
        self.assertEqual([e.linea for e in r.errores], [1, 3])

    def test_error_lexico_no_se_confunde_con_sintactico(self):
        lex, r = self.parser.analizar_texto("mostrar @ tareas\nmostrar tareas")
        self.assertEqual(len(lex.errores), 1)
        self.assertEqual(r.lineas_omitidas, (1,))
        self.assertEqual([c.linea for c in r.comandos], [2])

    def test_lexer_acepta_pero_parser_rechaza(self):
        lex, r = self.parser.analizar_texto("curso_2026 >= 10")
        self.assertFalse(lex.errores)
        self.assertEqual(r.errores[0].codigo, "SYN004")

    def test_arbol_exportable(self):
        _, r = self.parser.analizar_texto('buscar tarea "Proyecto de redes"')
        estructura = r.comandos[0].arbol.como_dict()
        self.assertEqual(estructura["simbolo"], "S")
        self.assertTrue(estructura["hijos"])

if __name__ == "__main__":
    unittest.main()
