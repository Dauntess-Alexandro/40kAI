@echo off
setlocal EnableExtensions
cd /d %~dp0\..

echo [build_gui_exe] Корень: %cd%

where python >nul 2>&1
if errorlevel 1 (
  echo [build_gui_exe] Python не найден в PATH.
  exit /b 1
)

if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)

echo [build_gui_exe] Используется: %PY%
"%PY%" -m pip install -q pyinstaller
if errorlevel 1 exit /b 1

echo [build_gui_exe] Сборка 40kAI_GUI (onedir) ...
"%PY%" -m PyInstaller --noconfirm --clean installer\40kAI_gui.spec
if errorlevel 1 (
  echo [build_gui_exe] Ошибка PyInstaller.
  exit /b 1
)

if not exist "dist\40kAI_GUI\40kAI_GUI.exe" (
  echo [build_gui_exe] Не найден dist\40kAI_GUI\40kAI_GUI.exe
  exit /b 1
)

echo [build_gui_exe] Готово: dist\40kAI_GUI\40kAI_GUI.exe
endlocal
exit /b 0
