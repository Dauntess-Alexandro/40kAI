@echo off
setlocal
cd /d %~dp0
set MODEL=%~1
if "%MODEL%"=="" set MODEL=None
set MANUAL_DICE=1
set VERBOSE_LOGS=1
start "40kAI" cmd /k ""%cd%\play_terminal_manual.bat" "%MODEL%""
endlocal
