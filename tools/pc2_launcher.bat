@echo off
chcp 65001 >nul 2>&1
setlocal
REM ПК2: окно-лаунчер распределённого обучения (выбор роли + общая папка + лог).
REM Корень репо = родитель папки tools (где лежит этот .bat) — проект может быть в любом месте.
cd /d "%~dp0.."

REM Тот же python, что у акторов (pc2_dqn_actors.bat зовёт голый python) — системный.
REM Так зависимости окна и акторов в одном месте, без рассинхрона venv/system.
set "PY=python"

REM Окну нужен PySide6, акторам — gymnasium/torch и пр. Если чего-то нет в этом
REM python — ставим весь requirements_windows.txt один раз (туда же, где крутятся актора).
"%PY%" -c "import PySide6, gymnasium, torch" 1>nul 2>nul
if errorlevel 1 (
  echo [ПК2] Не хватает зависимостей в системном python — ставлю requirements_windows.txt
  echo       (один раз, ~5-10 мин: torch, gymnasium, PySide6, zmq...).
  "%PY%" -m pip install -r requirements_windows.txt
  if errorlevel 1 (
    echo.
    echo [ОШИБКА] Не удалось поставить зависимости. Поставь вручную:
    echo          python -m pip install -r requirements_windows.txt
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
