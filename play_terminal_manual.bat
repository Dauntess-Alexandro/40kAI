@echo off
setlocal
cd /d %~dp0
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
set PYTHONPATH=%cd%\gym_mod;%PYTHONPATH%
set MANUAL_DICE=1
set MODEL=%~1
if "%MODEL%"=="" set MODEL=None
if not exist logs mkdir logs
for /f "tokens=1-3 delims=/: " %%a in ("%date%") do set _d=%%c-%%a-%%b
for /f "tokens=1-3 delims=:. " %%a in ("%time%") do set _t=%%a-%%b-%%c
set LOGFILE=%cd%\logs\run_%_d%_%_t%.log
if "%VERBOSE_LOGS%"=="1" (
  powershell -NoProfile -Command "python -u play.py \"%MODEL%\" False 2>&1 | Tee-Object -FilePath \"%LOGFILE%\""
) else (
  python -u play.py "%MODEL%" False
)
endlocal
