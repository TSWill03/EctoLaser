@echo off
setlocal
cd /d "%~dp0.."
set "PYTHON=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
if not exist "%PYTHON%" set "PYTHON=python"
echo ====================================================
echo EctoLaser - Webcam e QR de demonstracao
echo SEM identificacao facial; SEM laser
echo ====================================================
"%PYTHON%" demo\webcam_demo.py --make-badge demo\badge_wicolly_demo.png
echo.
echo Exiba o QR gerado demo\badge_wicolly_demo.png
echo Webcam 0. Tecla Q / ESC para fechar.
"%PYTHON%" demo\webcam_demo.py --camera 0
if errorlevel 1 (
 echo.
 echo Falha ao abrir Camera 0. Tente executar no terminal:
 echo python demo\webcam_demo.py --camera 1
)
pause
