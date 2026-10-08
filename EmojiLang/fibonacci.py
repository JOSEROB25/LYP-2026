"""Ejecuta el menu de Fibonacci escrito con los emojis del diccionario."""

import sys
from pathlib import Path

from emojilang import EmojiLangError, EmojiLangExit, Interpreter


def main() -> None:
    ruta_programa = Path(__file__).parent / "programas" / "fibonacci.emoji"
    try:
        Interpreter().run(ruta_programa.read_text(encoding="utf-8"))
    except (EmojiLangExit, EOFError, KeyboardInterrupt):
        print("Hasta luego")
    except (OSError, EmojiLangError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()