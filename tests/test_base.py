import unittest

from src.core.lector_texto import LectorTexto
from src.modelos.automata import Automata
from src.modelos.estado import Estado
from src.modelos.token import Token, TipoToken


class TestLectorTexto(unittest.TestCase):
    def test_lectura_caracter_por_caracter(self):
        lector = LectorTexto.desde_cadena("abc")
        caracteres = list(lector.recorrer())

        self.assertEqual(len(caracteres), 3)
        self.assertEqual(caracteres[0].valor, "a")
        self.assertEqual(caracteres[1].valor, "b")
        self.assertEqual(caracteres[2].valor, "c")

    def test_linea_y_columna(self):
        lector = LectorTexto.desde_cadena("a\nb")
        caracteres = list(lector.recorrer())

        self.assertEqual((caracteres[0].linea, caracteres[0].columna), (1, 1))
        self.assertEqual((caracteres[1].linea, caracteres[1].columna), (1, 2))
        self.assertEqual((caracteres[2].linea, caracteres[2].columna), (2, 1))


class TestToken(unittest.TestCase):
    def test_creacion_token(self):
        token = Token(TipoToken.VERBO, "mostrar", 1, 1)
        self.assertEqual(token.lexema, "mostrar")
        self.assertEqual(token.tipo, TipoToken.VERBO)


class TestAutomata(unittest.TestCase):
    def test_automata_simple(self):
        automata = Automata("AFD prueba")
        automata.agregar_estado(Estado("q0", es_inicial=True))
        automata.agregar_estado(Estado("q1", es_final=True))
        automata.agregar_transicion("q0", "a", "q1")

        self.assertTrue(automata.procesar("a"))
        self.assertFalse(automata.procesar("b"))


if __name__ == "__main__":
    unittest.main()
