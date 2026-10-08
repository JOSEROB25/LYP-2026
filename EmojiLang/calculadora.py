from emojilang import Interpreter


Interpreter().run("""📦 🅱️ = 1
🔁 🅱️ ➡️ 0 👉 {
    🖨️ "🧮 CALCULADORA"
    🖨️ "1️⃣ Calcular"
    🖨️ "2️⃣ Salir"
    ⌨️ 🎯

    🤔 🎯 🟰 1 👉 {
        🖨️ "Escribe la operación (por ejemplo: 12 + 4):"
        ⌨️ ⭐
        📦 🍎 = 🧮 ⭐
        🖨️ "Resultado:"
        🖨️ 🍎
    }
    🙅 🎯 🟰 2 👉 {
        📦 🅱️ = 0
        🖨️ "🚪 Hasta luego."
    }
    🙅 {
        🖨️ "⚠️ Opción no válida. Elige 1 o 2."
    }
}""")