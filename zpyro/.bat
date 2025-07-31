@echo off
REM Executa o interpretador passando um arquivo como argumento

if "%~1"=="" (
    echo Nenhum arquivo de programa foi especificado.
    echo Uso: zpyro.bat ^<nome_do_arquivo^>
) else (
    python zpyro\Interpretador\Interpreter.py "%~1"
)

pause
