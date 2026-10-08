"""Interprete pequeno de EmojiLang, una sintaxis amigable sobre Python."""
from __future__ import annotations

import ast
import operator
import sys
import unicodedata
from pathlib import Path
from typing import Any

if __package__:
    from . import diccionario_emojis
else:
    import diccionario_emojis


class EmojiLangError(Exception):
    """Error producido por un programa EmojiLang."""


class EmojiLangExit(Exception):
    """Salida solicitada por el usuario."""


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


class Interpreter:
    def __init__(self) -> None:
        self.variables: dict[str, Any] = {}
        self.output: list[Any] = []

    def _valid_variable_name(self, name: str) -> bool:
        if name in diccionario_emojis.EMOJIS_RESERVADOS:
            return False
        if name.isidentifier():
            return True
        categories = [unicodedata.category(character) for character in name]
        emoji_categories = {"So", "Sk", "Mn", "Mc", "Me", "Cf", "Nd"}
        return (
            any(category in {"So", "Sk"} for category in categories)
            and all(category in emoji_categories for category in categories)
        )

    def run(self, source: str) -> list[Any]:
        lines = source.lstrip("\ufeff").splitlines()
        self._execute_block(lines, 0, len(lines))
        return self.output

    def _execute_block(self, lines: list[str], start: int, end: int) -> int:
        index = start
        while index < end:
            line = lines[index].strip()
            index += 1

            if not line or line.startswith("📝") or line.startswith("#"):
                continue

            if line.endswith("{"):
                command = line[:-1].strip()
                block_start = index
                block_end, next_index = self._read_block(
                    lines, block_start, end
                )

                if command.startswith(("🤔", "✅", "❌")):
                    index = self._execute_conditional_chain(
                        lines,
                        command,
                        block_start,
                        block_end,
                        next_index,
                        end,
                    )

                elif command.startswith(("🙅", "🔀", "↪️", "↪")):
                    raise EmojiLangError(
                        "🙅, 🔀 y ↪️ solo pueden seguir a 🤔, ✅ o ❌"
                    )

                else:
                    self._execute_command(
                        command,
                        lines,
                        block_start,
                        block_end,
                    )
                    index = next_index

                continue

            if line == "}":
                raise EmojiLangError("Hay un '}' sin bloque abierto")

            self._execute_command(line, lines, index, index)

        return index

    def _read_block(
        self,
        lines: list[str],
        start: int,
        end: int,
    ) -> tuple[int, int]:

        depth = 1
        index = start

        while index < end and depth:
            token = lines[index].strip()

            if token.endswith("{"):
                depth += 1

            if token == "}":
                depth -= 1

            index += 1

        if depth:
            raise EmojiLangError("Falta cerrar un bloque con '}'")

        return index - 1, index

    def _execute_conditional_chain(
        self,
        lines: list[str],
        command: str,
        block_start: int,
        block_end: int,
        next_index: int,
        end: int,
    ) -> int:

        matched = self._condition_matches(command)

        if matched:
            self._execute_block(lines, block_start, block_end)

        index = next_index

        while index < end:
            candidate = lines[index].strip()

            if not candidate.endswith("{"):
                break

            candidate_command = candidate[:-1].strip()

            if not candidate_command.startswith(
                ("🙅", "🔀", "↪️", "↪")
            ):
                break

            candidate_start = index + 1

            candidate_end, candidate_next = self._read_block(
                lines,
                candidate_start,
                end,
            )

            should_run = candidate_command.startswith(("↪️", "↪"))

            if candidate_command.startswith(("🙅", "🔀")):
                condition = candidate_command[1:].strip()

                if condition.endswith("👉"):
                    condition = condition[:-1].strip()

                should_run = (
                    bool(self._evaluate(condition))
                    if condition
                    else True
                )

            if not matched and should_run:
                self._execute_block(
                    lines,
                    candidate_start,
                    candidate_end,
                )
                matched = True

            index = candidate_next

        return index

    def _condition_matches(self, command: str) -> bool:
        condition = command[1:].strip()

        if condition.endswith("👉"):
            condition = condition[:-1].strip()

        if command.startswith("❌"):
            return not bool(self._evaluate(condition))

        return bool(self._evaluate(condition))

    def _execute_command(
        self,
        line: str,
        lines: list[str],
        block_start: int,
        block_end: int,
    ) -> None:

        if line == "🚪":
            raise EmojiLangExit

        if line.startswith("🖨️") or line.startswith("🖨"):
            value = self._evaluate(
                line.lstrip("🖨️🖨 ")
            )
            self.output.append(value)
            print(value)
            return

        if line.startswith("⌨️") or line.startswith("⌨"):
            assignment = (
                line.removeprefix("⌨️")
                .removeprefix("⌨")
                .strip()
            )

            if not self._valid_variable_name(assignment):
                raise EmojiLangError(
                    "La entrada necesita un nombre: ⌨️ numero"
                )

            value = input(f"⌨️ {assignment}: ")

            if value.strip() == "🚪":
                raise EmojiLangExit

            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass

            self.variables[assignment] = value
            return

        if line.startswith("📦"):
            assignment = line[1:].strip()

            if "=" not in assignment:
                raise EmojiLangError(
                    "La asignacion necesita '=': 📦 nombre = valor"
                )

            name, expression = assignment.split("=", 1)

            name = name.strip()

            if not self._valid_variable_name(name):
                raise EmojiLangError(
                    f"Nombre de variable invalido: {name}"
                )

            self.variables[name] = self._evaluate(expression)
            return

        if line.startswith(("🔄", "🔁", "🔂")):
            repetition = line[1:].strip()

            if repetition.endswith("👉"):
                repetition = repetition[:-1].strip()

            if line.startswith("🔄"):
                count = int(self._evaluate(repetition))

                if count < 0:
                    raise EmojiLangError(
                        "🔄 necesita un numero positivo"
                    )

                for _ in range(count):
                    self._execute_block(
                        lines,
                        block_start,
                        block_end,
                    )

                return

            while self._evaluate(repetition):
                self._execute_block(
                    lines,
                    block_start,
                    block_end,
                )

            return

        if line.startswith("✅"):
            if self._evaluate(line[1:].strip()):
                self._execute_block(
                    lines,
                    block_start,
                    block_end,
                )
            return

        raise EmojiLangError(
            f"Comando desconocido: {line}"
        )

    def _evaluate(
        self,
        expression: str,
        *,
        allow_commands: bool = True,
    ) -> Any:
        expression = expression.strip()

        if allow_commands and expression.startswith("🧮"):
            operation = self._evaluate(expression[1:].strip())

            if not isinstance(operation, str):
                raise EmojiLangError(
                    "🧮 necesita una operación escrita como texto"
                )

            try:
                return self._evaluate(
                    operation,
                    allow_commands=False,
                )
            except EmojiLangError:
                return "⚠️ Operación no válida."

        # ====================================================
        # 🔧 REEMPLAZAR TEXTO
        # ====================================================

        if allow_commands and expression.startswith("🔧"):
            arguments = expression.split()

            if len(arguments) != 4:
                raise EmojiLangError(
                    "Uso: 🔧 texto buscar reemplazo"
                )

            texto = self._evaluate(arguments[1])
            buscar = self._evaluate(arguments[2])
            reemplazo = self._evaluate(arguments[3])

            if not isinstance(texto, str):
                raise EmojiLangError(
                    "🔧 necesita un texto"
                )

            if not isinstance(buscar, str):
                raise EmojiLangError(
                    "🔧 necesita un texto para buscar"
                )

            if not isinstance(reemplazo, str):
                raise EmojiLangError(
                    "🔧 necesita un texto de reemplazo"
                )

            return diccionario_emojis.reemplazar_texto(
                texto,
                buscar,
                reemplazo,
            )

        # ====================================================
        # 🌡️ CONVERTIR TEMPERATURA
        # ====================================================

        if allow_commands and expression.startswith("🌡️"):
            arguments = expression.split()

            if len(arguments) != 4:
                raise EmojiLangError(
                    "Uso: 🌡️ temperatura unidad_origen unidad_destino"
                )

            value = self._evaluate(arguments[1])

            origin = self.variables.get(
                arguments[2],
                arguments[2],
            )

            destination = self.variables.get(
                arguments[3],
                arguments[3],
            )

            units = {
                meaning: emoji
                for emoji, meaning
                in diccionario_emojis.FUNCIONES_TEMPERATURA.items()
                if meaning in {
                    "CELSIUS",
                    "FAHRENHEIT",
                    "KELVIN",
                }
            }

            letters = {
                "C": "CELSIUS",
                "F": "FAHRENHEIT",
                "K": "KELVIN",
            }

            def normalize_unit(unit: Any) -> Any:
                if not isinstance(unit, str):
                    return unit

                value = unit.strip()

                meaning = letters.get(value.upper())

                return units[meaning] if meaning else value

            origin = normalize_unit(origin)
            destination = normalize_unit(destination)

            valid_units = set(units.values())

            if (
                origin not in valid_units
                or destination not in valid_units
            ):
                raise EmojiLangError(
                    "Usa C o ❄️, F o 🔥, K o 💧 como unidad"
                )

            try:
                return diccionario_emojis.convertir_temperatura(
                    value,
                    origin,
                    destination,
                )

            except (TypeError, ValueError) as error:
                raise EmojiLangError(
                    str(error)
                ) from error

        if allow_commands and expression.startswith("❌"):
            return not bool(
                self._evaluate(
                    expression[1:].strip()
                )
            )

        if allow_commands and expression.startswith("🔠"):
            value = self._evaluate(
                expression[1:].strip()
            )

            return (
                isinstance(value, str)
                and bool(value)
                and value[0].isupper()
            )

        expression, emoji_variables = self._translate_expression(
            expression
        )

        original_variables = self.variables

        self.variables = {
            **original_variables,
            **emoji_variables,
        }

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            return self._evaluate_node(tree.body)

        except (
            SyntaxError,
            ValueError,
            TypeError,
            ZeroDivisionError,
        ) as error:

            raise EmojiLangError(
                f"No puedo entender la expresion: {expression}"
            ) from error

        finally:
            self.variables = original_variables

    def _translate_expression(
        self,
        expression: str,
    ) -> tuple[str, dict[str, Any]]:

        replacements = {
            **diccionario_emojis.OPERADORES,
            **diccionario_emojis.COMPARADORES,
            **diccionario_emojis.ALIAS_OPERADORES,
            "⬆": "**",
            "💡": "**",
        }

        emoji_variables: dict[str, Any] = {}
        variable_replacements: dict[str, str] = {}

        for index, (name, value) in enumerate(
            (
                item
                for item in self.variables.items()
                if not item[0].isidentifier()
            )
        ):
            internal_name = (
                f"__emojilang_emoji_variable_{index}"
            )

            while internal_name in self.variables:
                internal_name += "_"

            variable_replacements[name] = internal_name
            emoji_variables[internal_name] = value

        replacements.update(variable_replacements)

        tokens = sorted(
            replacements,
            key=len,
            reverse=True,
        )

        translated: list[str] = []

        quote: str | None = None
        index = 0

        while index < len(expression):
            character = expression[index]

            if quote:
                translated.append(character)

                if (
                    character == quote
                    and (
                        index == 0
                        or expression[index - 1] != "\\"
                    )
                ):
                    quote = None

                index += 1
                continue

            if character in {"\"", "'"}:
                quote = character
                translated.append(character)
                index += 1
                continue

            token = next(
                (
                    token
                    for token in tokens
                    if expression.startswith(
                        token,
                        index,
                    )
                ),
                None,
            )

            if token is not None:
                translated.append(
                    replacements[token]
                )
                index += len(token)

            else:
                translated.append(character)
                index += 1

        return "".join(translated), emoji_variables

    def _evaluate_node(self, node: ast.AST) -> Any:

        if isinstance(
            node,
            ast.Constant,
        ) and isinstance(
            node.value,
            (int, float, str, bool),
        ):
            return node.value

        if (
            isinstance(node, ast.Name)
            and node.id in {"verdadero", "falso"}
        ):
            return node.id == "verdadero"

        if (
            isinstance(node, ast.Name)
            and node.id in self.variables
        ):
            return self.variables[node.id]

        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in BINARY_OPERATORS
        ):
            return BINARY_OPERATORS[
                type(node.op)
            ](
                self._evaluate_node(node.left),
                self._evaluate_node(node.right),
            )

        if isinstance(
            node,
            ast.UnaryOp,
        ) and isinstance(
            node.op,
            (
                ast.UAdd,
                ast.USub,
                ast.Not,
            ),
        ):
            value = self._evaluate_node(node.operand)

            return (
                +value
                if isinstance(node.op, ast.UAdd)
                else -value
                if isinstance(node.op, ast.USub)
                else not value
            )

        if isinstance(
            node,
            ast.Compare,
        ) and len(node.ops) == 1:

            left = self._evaluate_node(node.left)
            right = self._evaluate_node(
                node.comparators[0]
            )

            comparisons = {
                ast.Eq: operator.eq,
                ast.NotEq: operator.ne,
                ast.Lt: operator.lt,
                ast.LtE: operator.le,
                ast.Gt: operator.gt,
                ast.GtE: operator.ge,
            }

            comparison = comparisons.get(
                type(node.ops[0])
            )

            if comparison:
                return comparison(left, right)

        raise EmojiLangError(
            "Expresion no permitida"
        )


def main() -> int:

    if len(sys.argv) == 1:
        program_path = (
            Path(__file__).parent
            / "programas"
            / "nombre_apellido.emoji"
        )

    elif len(sys.argv) == 2:
        program_path = Path(sys.argv[1])

    else:
        print(
            "Uso: python emojilang.py [programa.emoji]",
            file=sys.stderr,
        )
        return 2

    try:

        source = program_path.read_text(
            encoding="utf-8"
        )

        Interpreter().run(source)

    except (
        EmojiLangExit,
        EOFError,
        KeyboardInterrupt,
    ):
        print("Hasta luego")
        return 0

    except (
        OSError,
        EmojiLangError,
    ) as error:

        print(
            f"Error: {error}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

