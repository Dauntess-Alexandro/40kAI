@echo off
setlocal
cd /d %~dp0\..
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
set "PYTHONW=pythonw"
where /q pythonw.exe
if errorlevel 1 set "PYTHONW=pythonw.exe"
if exist ".venv\Scripts\pythonw.exe" set "PYTHONW=.venv\Scripts\pythonw.exe"
if exist ".venv\Scripts\pythonw" set "PYTHONW=.venv\Scripts\pythonw"
start "" "%PYTHONW%" -m viewer %*
endlocal
