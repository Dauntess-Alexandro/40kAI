@echo off
chcp 65001 >nul 2>&1
REM 40kAI — только distributed actors на ПК2 (IS уже должен слушать :5555).
REM Обычно достаточно: tools\pc2_remote_az_is.bat  (IS + actors одной кнопкой).
cd /d "%~dp0"
call "%~dp0pc2_remote_az_is.bat" actors-only %*
