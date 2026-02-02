@echo off
setlocal

cd /d C:\40kAI

REM запускаем python ИЗ .venv напрямую (без activate)
.\.venv\Scripts\python.exe gui_qt\main.py

pause
