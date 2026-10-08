# EmojiLang

Una pequena biblioteca/interprete escrita en Python para programas sencillos con emojis intuitivos.

## Ejecutar

Desde esta carpeta:

```powershell
python emojilang.py programas\ejemplo_base.emoji
```

Si ejecutas `python emojilang.py` sin argumentos, se ejecuta ese ejemplo base.

Para ejecutar directamente el menu de Fibonacci con Python, ejecuta `python fibonacci.py`.
El ejemplo equivalente en EmojiLang se ejecuta con `python emojilang.py programas\fibonacci.emoji`.

En VS Code, abre un archivo `.emoji`, pulsa `F5` y selecciona **Ejecutar programa EmojiLang**.

## Diccionario oficial

El diccionario que define el significado del lenguaje está en [diccionario_emojis.py](diccionario_emojis.py). Está separado para que una persona o una IA pueda identificar cada símbolo al leer una fotografía del código.

## Sintaxis

| Emoji | Significado | Ejemplo |
| --- | --- | --- |
| 🖨️ | imprimir | `🖨️ "Hola"` |
| ⌨️ | pedir un dato | `⌨️ numero` |
| 🚪 | cerrar el programa | `🚪` |
| 📦 | guardar una variable | `📦 edad = 18` |
| 🔄 | repetir un numero de veces | `🔄 3 { ... }` |
| 🔁 | repetir mientras | `🔁 valido > 0 👉 { ... }` |
| 🔠 | comprobar mayuscula inicial | `🔠 nombre` |
| 🤔 | ejecutar si es verdadero | `🤔 edad > 17 👉 { ... }` |
| 🙅 | else if o else | `🙅 edad 🟰 18 👉 { ... }` |
| ➕ ➖ ✖️ ➗ ⬆️ | operaciones | `📦 total = 2 ➕ 3` |
| 📝 | comentario | `📝 Esto no se ejecuta` |

Los condicionales se pueden encadenar:

```text
📦 nota = 7
🤔 nota > 7 👉 {
    🖨️ "notable"
}
🙅 nota 🟰 7 👉 {
    🖨️ "aprobado"
}
🙅 {
    🖨️ "suspenso"
}
```

Los nombres de variables y los valores usan una forma sencilla de Python. Los programas `.emoji` no necesitan instalar paquetes.

Los valores `verdadero` y `falso` representan booleanos. Consulta [nombre_apellido.emoji](programas/nombre_apellido.emoji) para ver un ejemplo de validacion y repeticion.

## Alias opcionales

Para escribir operaciones sin buscar el emoji, el intérprete acepta `:suma:`, `:resta:`, `:multiplica:`, `:divide:` y `:potencia:`. La tabla completa está en `ALIAS_EMOJIS` y `ALIAS_OPERADORES`.
