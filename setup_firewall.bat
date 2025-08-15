@echo off
echo ====================================
echo  CONFIGURACION DE FIREWALL
echo  Servidor Flask de Phishing
echo ====================================
echo.

echo Configurando reglas de firewall para permitir acceso externo...
echo.

REM Verificar si se ejecuta como administrador
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Este script debe ejecutarse como Administrador
    echo Haz clic derecho en el archivo y selecciona "Ejecutar como administrador"
    pause
    exit /b 1
)

echo Agregando regla para puerto principal (5000)...
netsh advfirewall firewall add rule name="Flask Phishing - Panel Principal" dir=in action=allow protocol=TCP localport=5000

echo Agregando regla para puertos de sitios (5001-5999)...
netsh advfirewall firewall add rule name="Flask Phishing - Sitios Desplegados" dir=in action=allow protocol=TCP localport=5001-5999

echo.
echo ✅ Configuracion completada!
echo.
echo Ahora puedes acceder al servidor desde:
echo   • Esta maquina: http://localhost:5000
echo   • Red local: http://TU_IP_LOCAL:5000
echo.
echo Para encontrar tu IP local ejecuta: ipconfig
echo.
pause
