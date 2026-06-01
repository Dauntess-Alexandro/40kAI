@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM ============================================================
REM  40kAI — AZ Remote Inference Server (ПК2), одна кнопка.
REM  Режимы:  tools\pc2_remote_az_is.bat [setup|check]
REM ============================================================

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "MODE=%~1"

set "CFG=%ROOT%\runtime\state\pc2_remote_az_is_config.bat"
set "CFG_EXAMPLE=%ROOT%\runtime\state\pc2_remote_az_is_config.example.bat"

REM --- Первый запуск: создать конфиг из примера и открыть блокнот ---
if not exist "%CFG%" (
  echo [SETUP] Конфиг не найден, создаю из примера: %CFG%
  copy /y "%CFG_EXAMPLE%" "%CFG%" >nul
  echo [SETUP] Заполните пути (Z:\, порт, auth) и запустите bat снова.
  notepad "%CFG%"
  pause
  exit /b 0
)

call "%CFG%"

REM --- Дефолты, если в конфиге пусто ---
if "%AZ_REMOTE_HOST%"=="" set "AZ_REMOTE_HOST=0.0.0.0"
if "%AZ_REMOTE_PORT%"=="" set "AZ_REMOTE_PORT=5555"
if "%AZ_REMOTE_DEVICE%"=="" set "AZ_REMOTE_DEVICE=cuda:0"
if "%AZ_REMOTE_BATCH_SIZE%"=="" set "AZ_REMOTE_BATCH_SIZE=32"
if "%AZ_REMOTE_BATCH_INTERVAL_MS%"=="" set "AZ_REMOTE_BATCH_INTERVAL_MS=10"
if "%AZ_REMOTE_SYNC_INTERVAL%"=="" set "AZ_REMOTE_SYNC_INTERVAL=0.5"

REM --- venv ---
set "VENV=%ROOT%\.venv\Scripts\activate.bat"
if not exist "%VENV%" (
  echo [SETUP] .venv не найден, ставлю зависимости...
  call "%ROOT%\installer\install_deps.bat" -y
)
call "%VENV%"

REM --- check режим ---
if /i "%MODE%"=="check" (
  python -c "import torch, zmq, msgpack; print('CUDA:', torch.cuda.is_available()); print('zmq/msgpack OK')"
  pause
  exit /b 0
)

REM --- firewall (только setup) ---
if /i "%MODE%"=="setup" (
  if "%AZ_REMOTE_SETUP_FIREWALL%"=="1" (
    echo [SETUP] Добавляю firewall-правило на порт %AZ_REMOTE_PORT%...
    netsh advfirewall firewall add rule name="40kAI AZ Remote IS" dir=in action=allow protocol=TCP localport=%AZ_REMOTE_PORT% >nul 2>&1
  )
  echo [SETUP] Готово.
  pause
  exit /b 0
)

REM --- запуск сервера ---
set "INIT_ARG="
if not "%AZ_REMOTE_INIT_WEIGHTS%"=="" set "INIT_ARG=--init-weights "%AZ_REMOTE_INIT_WEIGHTS%""

python "%ROOT%\tools\az_remote_inference_server.py" ^
  --host %AZ_REMOTE_HOST% ^
  --port %AZ_REMOTE_PORT% ^
  --device %AZ_REMOTE_DEVICE% ^
  --weights-path "%AZ_REMOTE_WEIGHTS_PATH%" ^
  --search-config "%AZ_REMOTE_SEARCH_CONFIG%" ^
  --sync-method smb ^
  --sync-interval %AZ_REMOTE_SYNC_INTERVAL% ^
  --batch-size %AZ_REMOTE_BATCH_SIZE% ^
  --batch-interval-ms %AZ_REMOTE_BATCH_INTERVAL_MS% ^
  --auth-token "%AZ_REMOTE_AUTH_TOKEN%" ^
  %INIT_ARG%

set "EC=%ERRORLEVEL%"
if not "%EC%"=="0" (
  echo.
  echo [ERROR] Сервер завершился с кодом %EC%
  pause
)
exit /b %EC%
