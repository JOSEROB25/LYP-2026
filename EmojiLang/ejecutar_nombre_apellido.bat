@echo off
setlocal
cd /d "%~dp0"
python emojilang.py programas\nombre_apellido.emoji
if errorlevel 1 (
    echo.
    echo No se pudo ejecutar EmojiLang.
    echo Comprueba que Python esta instalado y disponible como "python".
)
pause
