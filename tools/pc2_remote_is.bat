@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM 40kAI — Remote Inference Server на ПК2 (одна кнопка).
REM Запуск: tools\pc2_remote_is.bat  (или двойной клик)
REM   tools\pc2_remote_is.bat setup   — только установка + firewall + конфиг
REM   tools\pc2_remote_is.bat start   — запуск (по умолчанию)
REM   tools\pc2_remote_is.bat check   — проверка без сервера

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "TOOLS=%~dp0"
if "%TOOLS:~-1%"=="\" set "TOOLS=%TOOLS:~0,-1%"
set "MODE=%~1"
if "%MODE%"=="" set "MODE=start"

echo.
echo ========================================
echo  40kAI  Remote Inference Server  (PC2)
echo ========================================
echo  Корень: %ROOT%
echo.

where python >nul 2>&1
if errorlevel 1 (
  echo [ОШИБКА] Python не найден в PATH.
  echo Установите Python 3.12+ с python.org и включите "Add to PATH".
  pause
  exit /b 1
)

set "CONFIG_BAT=%ROOT%\runtime\state\pc2_remote_is_config.bat"
set "CONFIG_EXAMPLE=%ROOT%\runtime\state\pc2_remote_is_config.example.bat"
set "SERVER_PY=%TOOLS%\gmz_remote_inference_server.py"

if not exist "%ROOT%\runtime\state" mkdir "%ROOT%\runtime\state" 2>nul

if not exist "%CONFIG_BAT%" (
  if exist "%CONFIG_EXAMPLE%" (
    copy /Y "%CONFIG_EXAMPLE%" "%CONFIG_BAT%" >nul
    echo [КОНФИГ] Создан %CONFIG_BAT%
    echo Откройте файл, укажите пути к весам SMB и search_cfg.json, сохраните.
    echo.
    notepad "%CONFIG_BAT%"
    echo.
    echo После сохранения конфига запустите tools\pc2_remote_is.bat снова.
    pause
    exit /b 0
  ) else (
    echo [ОШИБКА] Нет шаблона %CONFIG_EXAMPLE%
    pause
    exit /b 1
  )
)

call "%CONFIG_BAT%"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось загрузить конфиг: %CONFIG_BAT%
  pause
  exit /b 1
)

if "%GMZ_REMOTE_WEIGHTS_PATH%"=="" (
  echo [ОШИБКА] В конфиге не задан GMZ_REMOTE_WEIGHTS_PATH
  notepad "%CONFIG_BAT%"
  pause
  exit /b 1
)
if "%GMZ_REMOTE_SEARCH_CONFIG%"=="" (
  echo [ОШИБКА] В конфиге не задан GMZ_REMOTE_SEARCH_CONFIG
  notepad "%CONFIG_BAT%"
  pause
  exit /b 1
)
if not exist "%GMZ_REMOTE_SEARCH_CONFIG%" (
  echo [ОШИБКА] search_cfg не найден: %GMZ_REMOTE_SEARCH_CONFIG%
  echo Создайте JSON по образцу в docs\remote-inference-server-gmz.md
  pause
  exit /b 1
)

if "%GMZ_REMOTE_HOST%"=="" set "GMZ_REMOTE_HOST=0.0.0.0"
if "%GMZ_REMOTE_PORT%"=="" set "GMZ_REMOTE_PORT=5555"
if "%GMZ_REMOTE_DEVICE%"=="" set "GMZ_REMOTE_DEVICE=cuda:0"
if "%GMZ_REMOTE_BATCH_SIZE%"=="" set "GMZ_REMOTE_BATCH_SIZE=10"
if "%GMZ_REMOTE_BATCH_INTERVAL_MS%"=="" set "GMZ_REMOTE_BATCH_INTERVAL_MS=20"
if "%GMZ_REMOTE_SYNC_INTERVAL%"=="" set "GMZ_REMOTE_SYNC_INTERVAL=0.5"
if "%GMZ_REMOTE_COMPILE%"=="" set "GMZ_REMOTE_COMPILE=1"

if /i "%MODE%"=="check" goto :do_check
if /i "%MODE%"=="setup" goto :do_setup
if /i "%MODE%"=="start" goto :do_setup
goto :unknown_mode

:unknown_mode
echo [ОШИБКА] Неизвестный режим: %MODE%
echo Использование: tools\pc2_remote_is.bat [setup^|start^|check]
pause
exit /b 1

:do_setup
if not exist "%ROOT%\.venv\Scripts\python.exe" (
  echo [SETUP] Виртуальное окружение не найдено — запуск installer\install_deps.bat -y
  echo         Это может занять несколько минут...
  call "%ROOT%\installer\install_deps.bat" -y
  if errorlevel 1 (
    echo [ОШИБКА] install_deps.bat завершился с ошибкой.
    pause
    exit /b 1
  )
) else (
  echo [SETUP] .venv уже есть — пропуск install_deps
)

if "%GMZ_REMOTE_SETUP_FIREWALL%"=="1" (
  echo [SETUP] Правило firewall TCP %GMZ_REMOTE_PORT% ...
  netsh advfirewall firewall add rule name="40kAI Remote IS %GMZ_REMOTE_PORT%" dir=in action=allow protocol=TCP localport=%GMZ_REMOTE_PORT% >nul 2>&1
)

if /i "%MODE%"=="setup" goto :do_check

:do_check
call "%ROOT%\.venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось активировать .venv
  pause
  exit /b 1
)

echo [CHECK] Python + PyTorch + zmq/msgpack ...
python -c "import torch; c=torch.cuda.is_available(); n=torch.cuda.get_device_name(0) if c else 'CPU'; print('  torch', torch.__version__, '| CUDA:', c, '|', n)"
if errorlevel 1 (
  echo [ОШИБКА] PyTorch не импортируется.
  pause
  exit /b 1
)
python -c "import zmq, msgpack; print('  zmq+msgpack OK')"
if errorlevel 1 (
  echo [ОШИБКА] pyzmq или msgpack не установлены. Запустите: tools\pc2_remote_is.bat setup
  pause
  exit /b 1
)

if /i "%MODE%"=="check" (
  echo.
  echo [OK] Проверка пройдена. Для запуска: tools\pc2_remote_is.bat
  pause
  exit /b 0
)

if not exist "%GMZ_REMOTE_WEIGHTS_PATH%" (
  if "%GMZ_REMOTE_INIT_WEIGHTS%"=="" (
    echo [ОШИБКА] Нет файла весов: %GMZ_REMOTE_WEIGHTS_PATH%
    echo Укажите GMZ_REMOTE_INIT_WEIGHTS в конфиге или подключите SMB.
    pause
    exit /b 1
  )
  if not exist "%GMZ_REMOTE_INIT_WEIGHTS%" (
    echo [ОШИБКА] init-weights не найден: %GMZ_REMOTE_INIT_WEIGHTS%
    pause
    exit /b 1
  )
  echo [WARN] SMB-файл пока отсутствует — старт с --init-weights
) else (
  echo [OK] Веса SMB: %GMZ_REMOTE_WEIGHTS_PATH%
)

set "USE_INIT=0"
if not exist "%GMZ_REMOTE_WEIGHTS_PATH%" if not "%GMZ_REMOTE_INIT_WEIGHTS%"=="" set "USE_INIT=1"

echo.
echo [START] Remote IS  host=%GMZ_REMOTE_HOST%  port=%GMZ_REMOTE_PORT%  device=%GMZ_REMOTE_DEVICE%
echo         weights=%GMZ_REMOTE_WEIGHTS_PATH%
echo         search=%GMZ_REMOTE_SEARCH_CONFIG%
echo         Остановка: Ctrl+C
echo.

if "%USE_INIT%"=="1" (
  if "%GMZ_REMOTE_COMPILE%"=="1" (
    if not "%GMZ_REMOTE_AUTH_TOKEN%"=="" (
      python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GMZ_REMOTE_INIT_WEIGHTS%" --compile --auth-token "%GMZ_REMOTE_AUTH_TOKEN%"
      goto :server_done
    )
    python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GMZ_REMOTE_INIT_WEIGHTS%" --compile
    goto :server_done
  )
  if not "%GMZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GMZ_REMOTE_INIT_WEIGHTS%" --auth-token "%GMZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GMZ_REMOTE_INIT_WEIGHTS%"
  goto :server_done
)

if "%GMZ_REMOTE_COMPILE%"=="1" (
  if not "%GMZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --compile --auth-token "%GMZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --compile
  goto :server_done
)
if not "%GMZ_REMOTE_AUTH_TOKEN%"=="" (
  python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS% --auth-token "%GMZ_REMOTE_AUTH_TOKEN%"
  goto :server_done
)
python "%SERVER_PY%" --host %GMZ_REMOTE_HOST% --port %GMZ_REMOTE_PORT% --device %GMZ_REMOTE_DEVICE% --weights-path "%GMZ_REMOTE_WEIGHTS_PATH%" --search-config "%GMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %GMZ_REMOTE_SYNC_INTERVAL% --batch-size %GMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GMZ_REMOTE_BATCH_INTERVAL_MS%

:server_done

set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [ОШИБКА] Сервер завершился с кодом %EC%. См. runtime\logs\gmz_remote_is_*.log
) else (
  echo [EXIT] Сервер остановлен.
)
pause
exit /b %EC%
