@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions
REM PC1: write runtime/state/az_remote_search_cfg.json from hyperparams + checkpoint env_contract
REM Run: tools\write_az_remote_search_cfg.bat

cd /d "%~dp0\.."
set "ROOT=%cd%"

where python >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Python not found in PATH.
  pause
  exit /b 1
)

echo.
echo 40kAI - write az_remote_search_cfg.json
echo Root: %ROOT%
echo.

python "%ROOT%\tools\write_az_remote_search_cfg.py" %*
set "EC=%ERRORLEVEL%"
if not "%EC%"=="0" (
  echo.
  echo [ERROR] Exit code: %EC%
  pause
  exit /b %EC%
)

echo.
pause
exit /b 0
