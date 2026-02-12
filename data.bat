@echo off
setlocal
cd /d %~dp0
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python -u gym_mod\gym_mod\engine\initFile.py %1 %2 %3 %4 %5 %6
endlocal
