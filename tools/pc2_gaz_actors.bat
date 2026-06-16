@echo off
chcp 65001 >nul 2>&1
REM 40kAI — только distributed actors на ПК2 для GAZ (IS уже должен слушать :5565).
REM Обычно достаточно: tools\pc2_remote_gaz_is.bat  (IS + actors одной кнопкой).
cd /d "%~dp0"
call "%~dp0pc2_remote_gaz_is.bat" actors-only %*
