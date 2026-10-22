import unittest

from src.analizadores.analizador_lexico import AnalizadorLexico, normalizar_palabra
from src.modelos.token import TipoToken


class TestAnalizadorLexico(unittest.TestCase):
    def setUp(self):
        self.lexer = AnalizadorLexico()

    def tipos(self, texto):
        return [t.tipo for t in self.lexer.analizar(texto).tokens]

    def test_reconocimiento_palabras_reservadas(self):
        resultado = self.lexer.analizar("mostrar las tareas pendientes de matemáticas")
        self.assertEqual(
            [t.tipo for t in resultado.tokens],
            [TipoToken.VERBO, TipoToken.DETERMINANTE, TipoToken.SUSTANTIVO,
             TipoToken.ADJETIVO, TipoToken.PREPOSICION, TipoToken.SUSTANTIVO,
             TipoToken.FIN],
        )
        self.assertEqual(resultado.tokens[-2].lexema, "matemáticas")
        self.assertEqual(resultado.tokens[-2].normalizado, "matematicas")

    def test_identificador_alfanumerico(self):
        resultado = self.lexer.analizar("curso_2026")
        self.assertEqual(resultado.tokens[0].tipo, TipoToken.IDENTIFICADOR)
        self.assertEqual(resultado.tokens[0].lexema, "curso_2026")

    def test_identificador_unicode(self):
        resultado = self.lexer.analizar("lingüística_日本")
        self.assertEqual(resultado.tokens[0].tipo, TipoToken.IDENTIFICADOR)
        self.assertFalse(resultado.errores)

    def test_enteros_y_decimales(self):
        resultado = self.lexer.analizar("42 3.1416")
        self.assertEqual(resultado.tokens[0].tipo, TipoToken.NUMERO_ENTERO)
        self.assertEqual(resultado.tokens[1].tipo, TipoToken.NUMERO_DECIMAL)

    def test_decimal_incompleto(self):
        resultado = self.lexer.analizar("valor 12.")
        self.assertEqual(resultado.errores[0].codigo, "LEX003")
        self.assertEqual(resultado.errores[0].fragmento, "12.")

    def test_cadena_valida_y_escapes(self):
        resultado = self.lexer.analizar(r'buscar "Proyecto \"Redes\"\nFase 2"')
        cadena = next(t for t in resultado.tokens if t.tipo is TipoToken.CADENA)
        self.assertEqual(cadena.linea, 1)
        self.assertFalse(resultado.errores)

    def test_escape_invalido_se_reporta_y_recupera(self):
        resultado = self.lexer.analizar(r'"hola\q" mostrar')
        self.assertEqual(resultado.errores[0].codigo, "LEX004")
        self.assertEqual(resultado.tokens[-2].tipo, TipoToken.VERBO)

    def test_cadena_sin_cerrar(self):
        resultado = self.lexer.analizar('buscar "proyecto\nmostrar tareas')
        self.assertEqual(resultado.errores[0].codigo, "LEX002")
        self.assertEqual(resultado.tokens[-3].tipo, TipoToken.VERBO)
        self.assertEqual(resultado.tokens[-2].tipo, TipoToken.SUSTANTIVO)

    def test_simbolo_invalido(self):
        resultado = self.lexer.analizar("mostrar @tareas")
        self.assertEqual(len(resultado.errores), 1)
        self.assertEqual(resultado.errores[0].codigo, "LEX001")
        self.assertEqual((resultado.errores[0].linea, resultado.errores[0].columna), (1, 9))

    def test_recuperacion_varios_errores(self):
        resultado = self.lexer.analizar("@ mostrar $ tareas")
        self.assertEqual(len(resultado.errores), 2)
        self.assertEqual([t.tipo for t in resultado.tokens[:-1]], [TipoToken.VERBO, TipoToken.SUSTANTIVO])

    def test_entrada_vacia_solo_fin(self):
        resultado = self.lexer.analizar("")
        self.assertEqual(len(resultado.tokens), 1)
        self.assertEqual(resultado.tokens[0].tipo, TipoToken.FIN)
        self.assertEqual((resultado.tokens[0].linea, resultado.tokens[0].columna), (1, 1))

    def test_multiples_lineas_y_columnas(self):
        resultado = self.lexer.analizar("mostrar tareas\n  agregar tarea")
        self.assertEqual((resultado.tokens[2].linea, resultado.tokens[2].columna), (2, 3))
        self.assertEqual((resultado.tokens[3].linea, resultado.tokens[3].columna), (2, 11))

    def test_crlf_cuenta_un_salto(self):
        resultado = self.lexer.analizar("mostrar\r\ntareas")
        self.assertEqual((resultado.tokens[1].linea, resultado.tokens[1].columna), (2, 1))

    def test_comentarios_de_linea(self):
        resultado = self.lexer.analizar("mostrar tareas # comentario\n// otro\nagregar tarea")
        self.assertEqual([t.lexema for t in resultado.tokens[:-1]], ["mostrar", "tareas", "agregar", "tarea"])

    def test_operadores_y_delimitadores(self):
        resultado = self.lexer.analizar("(x >= 10); y != 2")
        self.assertIn(TipoToken.OPERADOR, [t.tipo for t in resultado.tokens])
        self.assertIn(TipoToken.DELIMITADOR, [t.tipo for t in resultado.tokens])

    def test_normalizacion_no_modifica_lexema(self):
        resultado = self.lexer.analizar("MOSTRAR")
        self.assertEqual(resultado.tokens[0].tipo, TipoToken.VERBO)
        self.assertEqual(resultado.tokens[0].lexema, "MOSTRAR")
        self.assertEqual(normalizar_palabra("Lingüística"), "linguistica")

    def test_resumen_real(self):
        resultado = self.lexer.analizar("mostrar @ tareas")
        resumen = resultado.resumen()
        self.assertEqual(resumen["total_caracteres"], 16)
        self.assertEqual(resumen["total_tokens"], 2)
        self.assertEqual(resumen["numero_errores"], 1)
        self.assertEqual(resumen["estado_final"], "CON_ERRORES")


class TestAutomatasLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = AnalizadorLexico()

    def test_afd_identificador_acepta_y_rechaza(self):
        afd = self.lexer.automata("identificador")
        self.assertTrue(afd.procesar("área_2"))
        self.assertFalse(afd.procesar("2area"))

    def test_afd_numero_estados_aceptacion(self):
        afd = self.lexer.automata("numero")
        self.assertTrue(afd.procesar("25"))
        self.assertTrue(afd.procesar("25.5"))
        self.assertFalse(afd.procesar("25."))

    def test_traza_transicion_invalida(self):
        traza = self.lexer.automata("numero").trazar("1x")
        self.assertFalse(traza.aceptada)
        self.assertIsNone(traza.pasos[-1].destino)

    def test_afd_cadena_escapes(self):
        afd = self.lexer.automata("cadena")
        self.assertTrue(afd.procesar(r'"hola\n"'))
        self.assertFalse(afd.procesar(r'"hola\q"'))
        self.assertFalse(afd.procesar('"hola'))


if __name__ == "__main__":
    unittest.main()
