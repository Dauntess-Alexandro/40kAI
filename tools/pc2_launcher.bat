@echo off
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

echo [ПК2] Запуск окна-лаунчера...
"%PY%" tools\pc2_launcher.py

REM Окно закрылось/ошибка — не прячем сразу, чтобы было видно сообщение.
if errorlevel 1 (
  echo.
  echo [ОШИБКА] Лаунчер завершился с ошибкой. Проверь, что установлены зависимости
  echo          (installer\install_deps.bat) и что Python доступен.
)
pause
