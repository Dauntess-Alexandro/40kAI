@echo off
setlocal EnableExtensions
cd /d %~dp0\..

echo [build_installer] === 40kAI Install.exe ===

call "%~dp0build_gui_exe.bat"
if errorlevel 1 exit /b 1

set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if "%ISCC%"=="" (
  echo [build_installer] Inno Setup 6 не найден.
  echo Установите: https://jrsoftware.org/isdl.php
  echo Затем повторите этот скрипт.
  exit /b 1
)

if not exist "installer\output" mkdir "installer\output"

echo [build_installer] Компиляция installer\40kAI.iss ...
"%ISCC%" "installer\40kAI.iss"
if errorlevel 1 exit /b 1

if exist "installer\output\Install.exe" (
  echo [build_installer] Готово: installer\output\Install.exe
) else (
  echo [build_installer] Install.exe не найден в installer\output\
  exit /b 1
)

endlocal
exit /b 0
