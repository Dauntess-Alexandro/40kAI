@echo off
chcp 65001 >nul 2>&1
setlocal
REM ПК2: окно-лаунчер распределённого обучения (выбор роли + общая папка + лог).
REM Корень репо = родитель папки tools — проект может лежать где угодно.
cd /d "%~dp0.."

REM Тот же python, что у акторов: .venv (где install_deps ставит стек), иначе системный.
if exist ".\.venv\Scripts\python.exe" (set "PY=.\.venv\Scripts\python.exe") else (set "PY=python")
echo [ПК2] python=%PY%

"%PY%" tools\pc2_launcher.py

REM pause — чтобы при ошибке окно не закрылось мгновенно и был виден текст.
if errorlevel 1 (
  echo.
  echo [ОШИБКА] Лаунчер упал. Если жалуется на PySide6 — поставь в venv:
  echo          .\.venv\Scripts\python.exe -m pip install PySide6
)
pause
