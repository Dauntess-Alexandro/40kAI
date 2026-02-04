@echo off
setlocal
cd /d %~dp0
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
set PYTHONPATH=%cd%\gym_mod;%PYTHONPATH%
REM Дефолты для ускорения обучения/чекпойнтов (не переопределяем, если заданы в окружении)
if not defined NUM_ENVS set NUM_ENVS=16
if not defined BATCH_ACT set BATCH_ACT=1
if not defined USE_AMP set USE_AMP=1
if not defined USE_COMPILE set USE_COMPILE=1
if not defined PREFETCH set PREFETCH=1
if not defined PIN_MEMORY set PIN_MEMORY=1
if not defined SAVE_EVERY set SAVE_EVERY=200
python -u train.py
endlocal
