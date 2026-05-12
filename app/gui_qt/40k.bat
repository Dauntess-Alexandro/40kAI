@echo off
setlocal

cd /d C:\40kAI

REM запускаем python ИЗ .venv напрямую (без activate)
REM модульный запуск: корень репо в sys.path, импорт project_paths стабилен
.\.venv\Scripts\python.exe -m app.gui_qt.main

pause
