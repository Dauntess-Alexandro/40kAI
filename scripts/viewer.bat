@echo off
setlocal
cd /d %~dp0\..
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
set PYTHONPATH=%cd%\core;%PYTHONPATH%
python -m app.viewer %*
endlocal
