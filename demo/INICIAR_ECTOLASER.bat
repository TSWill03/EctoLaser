@echo off
setlocal
cd /d "%~dp0.."
set "SYSTEM_PY=%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
if not exist "%SYSTEM_PY%" set "SYSTEM_PY=python"
set "VENV_PY=.venv\Scripts\python.exe"

echo ====================================================
echo EctoLaser - Webcam e credencial QR de demonstracao
echo NAO identifica pessoas; SEM laser
echo ====================================================
if not exist "%VENV_PY%" (
  echo Criando ambiente Python isolado...
  "%SYSTEM_PY%" -m venv .venv
  if errorlevel 1 goto ERROR
  echo Instalando OpenCV 4.13 e NumPy no ambiente isolado...
  "%VENV_PY%" -m pip install -r demo\requirements-demo.txt
  if errorlevel 1 goto ERROR
)

"%VENV_PY%" -c "import cv2; assert hasattr(cv2, 'CascadeClassifier')"
if errorlevel 1 (
  echo Instalando versoes compatíveis na venv...
  "%VENV_PY%" -m pip install -r demo\requirements-demo.txt
  if errorlevel 1 goto ERROR
)

"%VENV_PY%" demo\webcam_demo.py --make-badge demo\badge_wicolly_demo.png
if errorlevel 1 goto ERROR

echo.
echo Credencial QR: demo\badge_wicolly_demo.png
echo Mostre o QR impresso ou em outra tela diante da camera.
echo Webcam 0. Tecla Q / ESC encerra.
"%VENV_PY%" demo\webcam_demo.py --camera 0
if errorlevel 1 (
  echo.
  echo Se Camera 0 falhar, execute manualmente com --camera 1 ou 2.
)
goto END

:ERROR
echo.
echo Falha na configuracao automatica. Leia docs\WEBCAM_DEMO.md.
:END
pause
