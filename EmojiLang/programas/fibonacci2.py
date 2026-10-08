import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emojilang import Interpreter


Interpreter().run("""📦 🍎 = 1
🔁 🍎 ➡️ 0 👉 {
    🖨️ "1️⃣ Generar Fibonacci"
    🖨️ "2️⃣ Salir"
    ⌨️ 🍌

    🤔 🍌 🟰 1 👉 {
        🖨️ "Indica cuántos términos quieres generar:"
        ⌨️ ⭐
        🤔 ⭐ ➡️ 0 👉 {
            📦 🅰️ = 0
            📦 🅱️ = 1
            🔄 ⭐ {
                🖨️ 🅰️
                📦 🎯 = 🅰️ ➕ 🅱️
                📦 🅰️ = 🅱️
                📦 🅱️ = 🎯
            }
        }
        🙅 {
            🖨️ "⚠️ Escribe un número mayor que cero."
        }
    }
    🙅 🍌 🟰 2 👉 {
        📦 🍎 = 0
        🖨️ "🚪 Hasta luego."
    }
    🙅 {
        🖨️ "⚠️ Elige la opción 1 o 2."
    }
}""")