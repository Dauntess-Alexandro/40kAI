@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0\.."
set CFG=runtime\state\pc2_phoenix_actors_config.bat
if not exist "%CFG%" (
    echo [PHOENIX][DIST][PC2] %CFG% не найден — копирую из .example. Отредактируйте SMB/IP при необходимости и запустите снова!
    copy "runtime\state\pc2_phoenix_actors_config.example.bat" "%CFG%" >nul
)
call "%CFG%"
echo [PHOENIX][DIST][PC2] PC1=%PHOENIX_DIST_PC1_HOST%:%PHOENIX_DIST_ROLLOUT_PORT% workers=%PHOENIX_DIST_PC2_NUM_WORKERS% MODELS_DIR=%MODELS_DIR%
if exist ".\.venv\Scripts\python.exe" (set "PY=.\.venv\Scripts\python.exe") else (set "PY=python")
echo [PHOENIX][DIST][PC2] python=%PY%
"%PY%" tools\pc2_phoenix_actors.py
endlocal
