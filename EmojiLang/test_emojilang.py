import ast
import unittest
from pathlib import Path
import runpy
import sys
from unittest.mock import patch

from emojilang import Interpreter

ARBOL_CALCULADORA = ast.parse(
    (Path(__file__).parent / "calculadora.py").read_text(encoding="utf-8")
)
PROGRAMA_CALCULADORA = next(
    node.args[0].value
    for node in ast.walk(ARBOL_CALCULADORA)
    if isinstance(node, ast.Call)
    and isinstance(node.func, ast.Attribute)
    and node.func.attr == "run"
    and node.args
    and isinstance(node.args[0], ast.Constant)
    and isinstance(node.args[0].value, str)
)


class EmojiLangTests(unittest.TestCase):
    def run_program(self, source: str) -> list[object]:
        return Interpreter().run(source)

    def test_suma(self) -> None:
        programa = "📦 resultado = 12 ➕ 8\n🖨️ resultado"
        resultado = self.run_program(programa)
        print(f"Resultado de la suma: {resultado[-1]}")
        self.assertEqual(resultado, [20])

    def test_aliases_de_operaciones(self) -> None:
        programa = "🖨️ 12 :suma: 8\n🖨️ 12 :resta: 8"
        self.assertEqual(self.run_program(programa), [20, 4])

    def test_variables_emoji_y_comparadores_del_diccionario(self) -> None:
        programa = """📦 🎯 = 2
🤔 🎯 ➡️ 1 👉 {
    🖨️ 🎯 ➕ 1
}"""
        self.assertEqual(self.run_program(programa), [3])

    def test_calculadora_todas_las_operaciones(self) -> None:
        casos = [
            ("8 + 5", 13),
            ("8 - 5", 3),
            ("8 * 5", 40),
            ("8 / 2", 4),
            ("8 % 3", 2),
            ("2 ** 8", 256),
        ]
        for operacion, esperado in casos:
            with self.subTest(operacion=operacion):
                with patch(
                    "builtins.input",
                    side_effect=["1", operacion, "2"],
                ):
                    resultado = self.run_program(PROGRAMA_CALCULADORA)
                self.assertIn(esperado, resultado)

    @patch("builtins.input", side_effect=["1", "8 / 0", "2"])
    def test_calculadora_evitar_division_por_cero(self, input_mock) -> None:
        resultado = self.run_program(PROGRAMA_CALCULADORA)

        self.assertIn("⚠️ Operación no válida.", resultado)
        self.assertEqual(input_mock.call_count, 3)

    def test_conversiones_temperatura_del_diccionario(self) -> None:
        casos = [
            ("25", "C", "F", 77.0),
            ("77", " f ", "c", 25.0),
            ("0", "❄️", "K", 273.15),
            ("32", "F", "💧", 273.15),
        ]
        for valor, origen, destino, esperado in casos:
            with self.subTest(origen=origen, destino=destino):
                ruta = Path(__file__).parent / "programas" / "Temperatura.py"
                salida = []
                with patch(
                    "sys.path", [str(ruta.parent.parent.parent), *sys.path]
                ), patch(
                    "builtins.input", side_effect=[valor, origen, destino]
                ), patch(
                    "builtins.print", side_effect=salida.append
                ):
                    runpy.run_path(str(ruta), run_name="__main__")
                self.assertAlmostEqual(salida[-1], esperado)

    def test_lanzador_reemplazo_emoji(self) -> None:
        ruta = Path(__file__).parent.parent / "RemplazoPalabras.py"
        salida = []
        entradas = ["Hola mundo, mundo", "mundo", "EmojiLang"]
        with patch("sys.path", [str(ruta.parent), *sys.path]), patch(
            "builtins.input", side_effect=entradas
        ), patch(
            "builtins.print", side_effect=salida.append
        ):
            runpy.run_path(str(ruta), run_name="__main__")

        self.assertIn("Hola EmojiLang, EmojiLang", salida)

    def test_if_not_else_if_else(self) -> None:
        programa = """📦 numero = 7
❌ numero 🟰 7 {
    🖨️ "distinto de siete"
}
🔀 numero 🟰 7 {
    🖨️ "siete"
}
↪️ {
    🖨️ "otro"
}"""
        self.assertEqual(self.run_program(programa), ["siete"])

    @patch("builtins.input", side_effect=["12", "4"])
    def test_entrada_de_numeros(self, input_mock) -> None:
        programa = "⌨️ numero1\n⌨️ numero2\n🖨️ numero1 ➕ numero2"
        self.assertEqual(self.run_program(programa), [16])
        self.assertEqual(input_mock.call_count, 2)

    @patch("builtins.input", side_effect=["juan", "Juan", "Perez"])
    def test_nombre_con_mayuscula(self, input_mock) -> None:
        programa = """📦 valido = falso
🔂 ❌ valido {
⌨️ nombre
✅ 🔠 nombre {
📦 valido = verdadero
}
}
⌨️ apellido
🖨️ nombre ➕ " " ➕ apellido"""
        self.assertEqual(self.run_program(programa), ["Juan Perez"])
        self.assertEqual(input_mock.call_count, 3)

    @patch("builtins.input", side_effect=["1", "7", "2"])
    def test_menu_genera_fibonacci_y_permite_salir(self, input_mock) -> None:
        ruta = Path(__file__).parent / "programas" / "fibonacci.emoji"
        programa = ruta.read_text(encoding="utf-8")

        resultado = self.run_program(programa)

        serie = [0, 1, 1, 2, 3, 5, 8]
        inicio_serie = resultado.index(0)
        self.assertEqual(resultado[inicio_serie:inicio_serie + len(serie)], serie)
        self.assertIn("Hasta luego", resultado)
        self.assertEqual(input_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
