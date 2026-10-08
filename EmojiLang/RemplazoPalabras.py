try:
    from EmojiLang.emojilang import Interpreter
except ModuleNotFoundError as error:
    if error.name != "EmojiLang":
        raise
    from emojilang import Interpreter

Interpreter().run("""🖨️ "🔧 📝"

🖨️ "📝"
⌨️ 🧾

🖨️ "🔎"
⌨️ 🔎

🖨️ "✨"
⌨️ ✨

📦 📄 = 🔧 🧾 🔎 ✨

🖨️ "✅"
🖨️ 📄""")