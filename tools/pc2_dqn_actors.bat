@echo off
chcp 65001 >nul 2>&1
setlocal
cd /d "%~dp0\.."
set CFG=runtime\state\pc2_dqn_actors_config.bat
if not exist "%CFG%" (
    echo [DQN][DIST][PC2] %CFG% не найден — копирую из .example. Отредактируйте IP/порт/MODELS_DIR и запустите снова!
    copy "runtime\state\pc2_dqn_actors_config.example.bat" "%CFG%" >nul
)
call "%CFG%"
echo [DQN][DIST][PC2] PC1=%DQN_DIST_PC1_HOST%:%DQN_DIST_ROLLOUT_PORT% workers=%DQN_DIST_PC2_NUM_WORKERS% MODELS_DIR=%MODELS_DIR%
python tools\pc2_dqn_actors.py
endlocal
