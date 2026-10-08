import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from emojilang import Interpreter

Interpreter().run("""📝 🌡️ convierte entre ❄️ Celsius, 🔥 Fahrenheit y 💧 Kelvin.

🖨️ "🌡️ CONVERSOR DE TEMPERATURA"

🖨️ "Introduce la temperatura:"
⌨️ 🧪

🖨️ "Introduce la unidad de origen:"
🖨️ "Escribe C o ❄️ para Celsius, F o 🔥 para Fahrenheit, K o 💧 para Kelvin."
🖨️ "❄️ Celsius"
🖨️ "🔥 Fahrenheit"
🖨️ "💧 Kelvin"
⌨️ 🅾️

🖨️ "Introduce la unidad de destino:"
🖨️ "Escribe C o ❄️ para Celsius, F o 🔥 para Fahrenheit, K o 💧 para Kelvin."
🖨️ "❄️ Celsius"
🖨️ "🔥 Fahrenheit"
🖨️ "💧 Kelvin"
⌨️ 🅳

📦 🆁 = 🌡️ 🧪 🅾️ 🅳

🖨️ "Resultado:"
🖨️ 🆁""")