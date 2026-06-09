@echo off
chcp 65001 >nul 2>&1
setlocal
REM ПК2: окно-лаунчер распределённого обучения (выбор роли + общая папка + лог).
REM Корень репо = родитель папки tools (где лежит этот .bat) — проект может быть в любом месте.
cd /d "%~dp0.."

REM Python из локального .venv (если есть), иначе системный.
if exist ".\.venv\Scripts\python.exe" (
  set "PY=.\.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

REM Окну нужен PySide6. На ПК2 (раньше только headless-акторы) его может не быть —
REM ставим точечно в тот же python, без переустановки torch/zmq.
"%PY%" -c "import PySide6" 1>nul 2>nul
if errorlevel 1 (
  echo [ПК2] PySide6 не найден в этом python — ставлю для окна-лаунчера...
  "%PY%" -m pip install PySide6
  if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось поставить PySide6. Поставь вручную:
    echo          "%PY%" -m pip install PySide6
    echo          или прогони полный installer\install_deps.bat
    pause
    exit /b 1
  )
)

echo [ПК2] Запуск окна-лаунчера...
"%PY%" tools\pc2_launcher.py

REM Окно закрылось/ошибка — не прячем сразу, чтобы было видно сообщение.
if errorlevel 1 (
  echo.
  echo [ОШИБКА] Лаунчер завершился с ошибкой. Проверь зависимости
  echo          (installer\install_deps.bat) и что Python доступен.
)
pause
