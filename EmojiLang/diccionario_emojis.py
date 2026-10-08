# ============================================================
# EmojiLang - Diccionario oficial
# ============================================================
#
# Lenguaje de programación basado en emojis.
#
# PRINCIPIO:
# - Los emojis definidos aquí son palabras clave del lenguaje.
# - Los emojis NO definidos pueden utilizarse como nombres
#   de variables.
#
# ============================================================


# ============================================================
# 🧠 COMANDOS
# ============================================================

COMANDOS = {

    # Entrada / salida
    "🖨️": "IMPRIMIR",
    "⌨️": "PEDIR_DATO",

    # Variables
    "📦": "GUARDAR_VARIABLE",

    # Condiciones
    "🤔": "SI",
    "👉": "ENTONCES",
    "🙅": "SI_NO",

    # Bucles
    "🔄": "REPETIR",
    "🔁": "REPETIR_MIENTRAS",
    "🛑": "ROMPER",

    # Funciones
    "🛠️": "CREAR_FUNCION",
    "📞": "LLAMAR_FUNCION",
    "🎁": "PARAMETRO",

    # Código externo
    "📚": "IMPORTAR",

    # Comentarios
    "💬": "COMENTARIO",

    # Programa
    "🚪": "SALIR",

    # Errores
    "⚠️": "ERROR",
}


# ============================================================
# ➕ OPERADORES ARITMÉTICOS
# ============================================================

OPERADORES = {

    "➕": "+",       # sumar
    "➖": "-",       # restar
    "✖️": "*",       # multiplicar
    "➗": "/",       # dividir
    "🧩": "%",       # resto
    "⬆️": "**",      # potencia
}


# ============================================================
# 👀 COMPARADORES
# ============================================================

COMPARADORES = {

    "🟰": "==",      # igual
    "❌": "!=",      # diferente

    "⬅️": "<",       # menor
    "➡️": ">",       # mayor

    "⬅️🟰": "<=",    # menor o igual
    "➡️🟰": ">=",    # mayor o igual
}


# ============================================================
# 🧠 OPERADORES LÓGICOS
# ============================================================

LOGICA = {

    "👍": "and",     # y
    "👎": "not",     # no
    "🤝": "or",      # o
}


# ============================================================
# 🔢 TIPOS DE DATOS
# ============================================================

TIPOS = {

    # Tipos básicos
    "🔢": "NUMERO",
    "🔤": "TEXTO",

    # Booleanos
    "👍": "VERDADERO",
    "👎": "FALSO",

    # Colecciones
    "📋": "LISTA",
    "📕": "DICCIONARIO",

    # Valor vacío
    "🚫": "NULO",
}


# ============================================================
# 🔧 FUNCIONES BÁSICAS
# ============================================================

FUNCIONES = {

    "📏": "LONGITUD",
    "🔍": "BUSCAR",
    "🔼": "MAXIMO",
    "🔽": "MINIMO",
    "🎲": "ALEATORIO",
}


# ============================================================
# 🔤 FUNCIONES DE TEXTO
# ============================================================

FUNCIONES_TEXTO = {

    # Reemplazar texto
    "🔧": "REEMPLAZAR",
}


# ============================================================
# 🌡️ FUNCIONES DE TEMPERATURA
# ============================================================

FUNCIONES_TEMPERATURA = {

    # Conversor
    "🌡️": "CONVERTIR_TEMPERATURA",

    # Unidades
    "❄️": "CELSIUS",
    "🔥": "FAHRENHEIT",
    "💧": "KELVIN",
}


# ============================================================
# 📋 ESTRUCTURAS DE DATOS
# ============================================================

ESTRUCTURAS = {

    "📋": "LISTA",
    "📕": "DICCIONARIO",
}


# ============================================================
# ✏️ ALIAS DE EMOJIS
# ============================================================

ALIAS_EMOJIS = {

    # Matemáticas
    ":suma:": "➕",
    ":resta:": "➖",
    ":multiplicar:": "✖️",
    ":dividir:": "➗",
    ":resto:": "🧩",
    ":potencia:": "⬆️",

    # Entrada / salida
    ":imprimir:": "🖨️",
    ":entrada:": "⌨️",

    # Variables
    ":variable:": "📦",

    # Condiciones
    ":si:": "🤔",
    ":entonces:": "👉",
    ":sino:": "🙅",

    # Bucles
    ":repetir:": "🔄",
    ":mientras:": "🔁",
    ":romper:": "🛑",

    # Funciones
    ":funcion:": "🛠️",
    ":llamar:": "📞",
    ":parametro:": "🎁",

    # Datos
    ":lista:": "📋",
    ":diccionario:": "📕",
    ":texto:": "🔤",
    ":numero:": "🔢",

    # Booleanos
    ":verdadero:": "👍",
    ":falso:": "👎",

    # Programa
    ":salir:": "🚪",

    # Funciones básicas
    ":buscar:": "🔍",
    ":longitud:": "📏",
    ":aleatorio:": "🎲",

    # Texto
    ":reemplazar:": "🔧",

    # Temperatura
    ":temperatura:": "🌡️",
    ":celsius:": "❄️",
    ":fahrenheit:": "🔥",
    ":kelvin:": "💧",

    # Otros
    ":error:": "⚠️",
    ":nulo:": "🚫",
}


# ============================================================
# ➗ ALIAS DE OPERADORES
# ============================================================

ALIAS_OPERADORES = {

    ":suma:": "+",
    ":resta:": "-",
    ":multiplicar:": "*",
    ":dividir:": "/",
    ":resto:": "%",
    ":potencia:": "**",

    ":igual:": "==",
    ":diferente:": "!=",
    ":menor:": "<",
    ":mayor:": ">",

    ":y:": "and",
    ":o:": "or",
    ":no:": "not",
}


# ============================================================
# 🌎 DICCIONARIO GENERAL
# ============================================================

DICCIONARIO_EMOJIS = {

    **COMANDOS,
    **OPERADORES,
    **COMPARADORES,
    **LOGICA,
    **TIPOS,
    **FUNCIONES,
    **FUNCIONES_TEXTO,
    **FUNCIONES_TEMPERATURA,
    **ESTRUCTURAS,
    **ALIAS_EMOJIS,
}


# ============================================================
# 🔎 EMOJIS RESERVADOS
# ============================================================

EMOJIS_RESERVADOS = set(DICCIONARIO_EMOJIS.keys())


# ============================================================
# 🧩 ¿ES UN EMOJI RESERVADO?
# ============================================================

def es_emoji_reservado(valor):

    """Devuelve True si el emoji pertenece al lenguaje."""

    return valor in EMOJIS_RESERVADOS


# ============================================================
# 📦 ¿PUEDE SER UNA VARIABLE?
# ============================================================

def puede_ser_variable(valor):

    """
    Un emoji puede utilizarse como nombre de variable
    siempre que no sea un emoji reservado.
    """

    if not valor:
        return False

    if valor in EMOJIS_RESERVADOS:
        return False

    return True


# ============================================================
# 🔧 REEMPLAZAR TEXTO
# ============================================================

def reemplazar_texto(texto, buscar, reemplazo):

    """
    Reemplaza todas las apariciones de un texto por otro.
    """

    return texto.replace(buscar, reemplazo)


# ============================================================
# ❄️ CELSIUS → 🔥 FAHRENHEIT
# ============================================================

def celsius_a_fahrenheit(celsius):

    return (celsius * 9 / 5) + 32


# ============================================================
# 🔥 FAHRENHEIT → ❄️ CELSIUS
# ============================================================

def fahrenheit_a_celsius(fahrenheit):

    return (fahrenheit - 32) * 5 / 9


# ============================================================
# ❄️ CELSIUS → 💧 KELVIN
# ============================================================

def celsius_a_kelvin(celsius):

    return celsius + 273.15


# ============================================================
# 💧 KELVIN → ❄️ CELSIUS
# ============================================================

def kelvin_a_celsius(kelvin):

    return kelvin - 273.15


# ============================================================
# 🔥 FAHRENHEIT → 💧 KELVIN
# ============================================================

def fahrenheit_a_kelvin(fahrenheit):

    return (fahrenheit - 32) * 5 / 9 + 273.15


# ============================================================
# 💧 KELVIN → 🔥 FAHRENHEIT
# ============================================================

def kelvin_a_fahrenheit(kelvin):

    return (kelvin - 273.15) * 9 / 5 + 32


# ============================================================
# 🌡️ CONVERTIR TEMPERATURA
# ============================================================

def convertir_temperatura(valor, origen, destino):

    # Misma unidad
    if origen == destino:
        return valor

    # ❄️ → 🔥
    if origen == "❄️" and destino == "🔥":
        return celsius_a_fahrenheit(valor)

    # 🔥 → ❄️
    if origen == "🔥" and destino == "❄️":
        return fahrenheit_a_celsius(valor)

    # ❄️ → 💧
    if origen == "❄️" and destino == "💧":
        return celsius_a_kelvin(valor)

    # 💧 → ❄️
    if origen == "💧" and destino == "❄️":
        return kelvin_a_celsius(valor)

    # 🔥 → 💧
    if origen == "🔥" and destino == "💧":
        return fahrenheit_a_kelvin(valor)

    # 💧 → 🔥
    if origen == "💧" and destino == "🔥":
        return kelvin_a_fahrenheit(valor)

    raise ValueError("⚠️ Conversión de temperatura no válida")