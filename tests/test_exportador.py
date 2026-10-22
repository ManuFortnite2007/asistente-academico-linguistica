import csv
import json
import tempfile
import unittest
from pathlib import Path

from src.analizadores.analizador_lexico import AnalizadorLexico
from src.core.exportador import ExportadorResultados
from src.core.lector_texto import LectorTexto


class TestExportador(unittest.TestCase):
    def setUp(self):
        self.resultado = AnalizadorLexico().analizar("mostrar tareas")

    def test_exporta_json_con_resumen(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = ExportadorResultados.exportar(self.resultado, Path(temporal) / "salida.json")
            datos = json.loads(ruta.read_text(encoding="utf-8"))
            self.assertEqual(datos["resumen"]["total_tokens"], 2)
            self.assertEqual(datos["tokens"][0]["tipo"], "VERBO")

    def test_exporta_csv_estructurado(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = ExportadorResultados.exportar(self.resultado, Path(temporal) / "salida.csv")
            with ruta.open(encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
            self.assertEqual(filas[1]["lexema"], "tareas")

    def test_exporta_txt_con_errores_y_resumen(self):
        resultado = AnalizadorLexico().analizar("mostrar @")
        with tempfile.TemporaryDirectory() as temporal:
            ruta = ExportadorResultados.exportar(resultado, Path(temporal) / "salida.txt")
            contenido = ruta.read_text(encoding="utf-8")
            self.assertIn("LEX001", contenido)
            self.assertIn("total_tokens: 1", contenido)

    def test_rechaza_formato_desconocido(self):
        with self.assertRaises(ValueError):
            ExportadorResultados.exportar(self.resultado, "salida.xml")


class TestLectorArchivos(unittest.TestCase):
    def test_lectura_utf8(self):
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "entrada.txt"
            ruta.write_text("lingüística", encoding="utf-8")
            self.assertEqual(LectorTexto.desde_archivo(ruta).contenido, "lingüística")

    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            LectorTexto.desde_archivo("archivo_que_no_existe.txt")


if __name__ == "__main__":
    unittest.main()
