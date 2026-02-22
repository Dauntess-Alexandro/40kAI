@echo off
setlocal
cd /d %~dp0
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
set PYTHONPATH=%cd%\gym_mod;%PYTHONPATH%
python -u train_alphazero.py
endlocal
