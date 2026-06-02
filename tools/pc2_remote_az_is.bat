@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM 40kAI — AZ Remote Inference Server на ПК2 (одна кнопка).
REM Запуск: tools\pc2_remote_az_is.bat  (или двойной клик = start)
REM   tools\pc2_remote_az_is.bat setup   — venv + firewall + конфиг
REM   tools\pc2_remote_az_is.bat start   — запуск сервера
REM   tools\pc2_remote_az_is.bat check   — проверка без сервера
REM   tools\pc2_remote_az_is.bat config  — открыть конфиг в блокноте

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "TOOLS=%~dp0"
if "%TOOLS:~-1%"=="\" set "TOOLS=%TOOLS:~0,-1%"
set "MODE=%~1"
if "%MODE%"=="" set "MODE=start"

echo.
echo ========================================
echo  40kAI  AZ Remote Inference Server (PC2)
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

set "CONFIG_BAT=%ROOT%\runtime\state\pc2_remote_az_is_config.bat"
set "CONFIG_EXAMPLE=%ROOT%\runtime\state\pc2_remote_az_is_config.example.bat"
set "CONFIG_EXAMPLE_REV=%ROOT%\runtime\state\pc2_remote_az_is_config.example.rev"
set "CONFIG_LOCAL_REV=%ROOT%\runtime\state\pc2_remote_az_is_config.rev"
set "SERVER_PY=%TOOLS%\az_remote_inference_server.py"

if not exist "%ROOT%\runtime\state" mkdir "%ROOT%\runtime\state" 2>nul

if /i "%MODE%"=="config" (
  call :sync_config_from_example
  if not exist "%CONFIG_BAT%" (
    echo [ERROR] Config not found: %CONFIG_BAT%
    pause
    exit /b 1
  )
  notepad "%CONFIG_BAT%"
  pause
  exit /b 0
)

call :sync_config_from_example
if not exist "%CONFIG_BAT%" (
  echo [ОШИБКА] Нет шаблона %CONFIG_EXAMPLE%
  pause
  exit /b 1
)

goto :after_config_sync

:sync_config_from_example
if not exist "%CONFIG_EXAMPLE%" exit /b 0
set "EX_REV=0"
set "CFG_REV=0"
if exist "%CONFIG_EXAMPLE_REV%" set /p EX_REV=<"%CONFIG_EXAMPLE_REV%"
if exist "%CONFIG_LOCAL_REV%" set /p CFG_REV=<"%CONFIG_LOCAL_REV%"
if not defined EX_REV set "EX_REV=0"
if not defined CFG_REV set "CFG_REV=0"
if not exist "%CONFIG_BAT%" goto :do_copy_example_config
if %CFG_REV% LSS %EX_REV% goto :do_copy_example_config
exit /b 0

:do_copy_example_config
if exist "%CONFIG_BAT%" (
  copy /Y "%CONFIG_BAT%" "%CONFIG_BAT%.bak" >nul
  echo [CONFIG] Backup: %CONFIG_BAT%.bak
)
copy /Y "%CONFIG_EXAMPLE%" "%CONFIG_BAT%" >nul
echo %EX_REV%>"%CONFIG_LOCAL_REV%"
echo [CONFIG] Synced %CONFIG_BAT% from example rev %EX_REV%
if not exist "%CONFIG_BAT%.bak" echo         Edit paths if needed: tools\pc2_remote_az_is.bat config
exit /b 0

:after_config_sync

call "%CONFIG_BAT%"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось загрузить конфиг: %CONFIG_BAT%
  pause
  exit /b 1
)

if "%AZ_REMOTE_WEIGHTS_PATH%"=="" set "AZ_REMOTE_WEIGHTS_PATH=Z:\latest_az_tree_policy.pth"
if "%AZ_REMOTE_SEARCH_CONFIG%"=="" set "AZ_REMOTE_SEARCH_CONFIG=Z:\az_remote_search_cfg.json"
if "%AZ_REMOTE_WEIGHTS_PATH%"=="" (
  echo [ОШИБКА] В конфиге не задан AZ_REMOTE_WEIGHTS_PATH
  echo Что делать: tools\pc2_remote_az_is.bat config
  pause
  exit /b 1
)
if "%AZ_REMOTE_SEARCH_CONFIG%"=="" (
  echo [ОШИБКА] В конфиге не задан AZ_REMOTE_SEARCH_CONFIG
  echo Что делать: tools\pc2_remote_az_is.bat config
  pause
  exit /b 1
)
if not exist "%AZ_REMOTE_SEARCH_CONFIG%" (
  echo [ОШИБКА] search_cfg не найден: %AZ_REMOTE_SEARCH_CONFIG%
  echo С ПК1: tools\write_az_remote_search_cfg.bat ^(копия на Z:\^)
  pause
  exit /b 1
)

if "%AZ_REMOTE_HOST%"=="" set "AZ_REMOTE_HOST=0.0.0.0"
if "%AZ_REMOTE_PORT%"=="" set "AZ_REMOTE_PORT=5555"
if "%AZ_REMOTE_DEVICE%"=="" set "AZ_REMOTE_DEVICE=cuda:0"
if "%AZ_REMOTE_BATCH_SIZE%"=="" set "AZ_REMOTE_BATCH_SIZE=32"
if "%AZ_REMOTE_BATCH_INTERVAL_MS%"=="" set "AZ_REMOTE_BATCH_INTERVAL_MS=10"
if "%AZ_REMOTE_SYNC_INTERVAL%"=="" set "AZ_REMOTE_SYNC_INTERVAL=0.5"
if "%AZ_REMOTE_SETUP_FIREWALL%"=="" set "AZ_REMOTE_SETUP_FIREWALL=1"

if /i "%MODE%"=="check" goto :do_check
if /i "%MODE%"=="setup" goto :do_setup
if /i "%MODE%"=="start" goto :do_setup
goto :unknown_mode

:unknown_mode
echo [ОШИБКА] Неизвестный режим: %MODE%
echo Использование: tools\pc2_remote_az_is.bat [setup^|start^|check^|config]
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

if "%AZ_REMOTE_SETUP_FIREWALL%"=="1" (
  echo [SETUP] Правило firewall TCP %AZ_REMOTE_PORT% ...
  netsh advfirewall firewall add rule name="40kAI AZ Remote IS %AZ_REMOTE_PORT%" dir=in action=allow protocol=TCP localport=%AZ_REMOTE_PORT% >nul 2>&1
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
  echo [ОШИБКА] pyzmq или msgpack не установлены. Запустите: tools\pc2_remote_az_is.bat setup
  pause
  exit /b 1
)

if /i "%MODE%"=="check" (
  echo.
  echo [OK] Проверка пройдена. Для запуска: tools\pc2_remote_az_is.bat
  pause
  exit /b 0
)

if not exist "%AZ_REMOTE_WEIGHTS_PATH%" (
  if "%AZ_REMOTE_INIT_WEIGHTS%"=="" (
    echo [ОШИБКА] Нет файла весов: %AZ_REMOTE_WEIGHTS_PATH%
    echo Укажите AZ_REMOTE_INIT_WEIGHTS в конфиге или подключите SMB Z:\
    pause
    exit /b 1
  )
  if not exist "%AZ_REMOTE_INIT_WEIGHTS%" (
    echo [ОШИБКА] init-weights не найден: %AZ_REMOTE_INIT_WEIGHTS%
    pause
    exit /b 1
  )
  echo [WARN] SMB-файл пока отсутствует — старт с --init-weights
) else (
  echo [OK] Веса SMB: %AZ_REMOTE_WEIGHTS_PATH%
)

set "USE_INIT=0"
if not exist "%AZ_REMOTE_WEIGHTS_PATH%" if not "%AZ_REMOTE_INIT_WEIGHTS%"=="" set "USE_INIT=1"

echo.
echo [START] AZ Remote IS  host=%AZ_REMOTE_HOST%  port=%AZ_REMOTE_PORT%  device=%AZ_REMOTE_DEVICE%
echo         weights=%AZ_REMOTE_WEIGHTS_PATH%
echo         search=%AZ_REMOTE_SEARCH_CONFIG%
echo         Остановка: Ctrl+C
echo         Лог: runtime\logs\az_remote_is_*.log
echo.

if "%USE_INIT%"=="1" (
  if not "%AZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %AZ_REMOTE_HOST% --port %AZ_REMOTE_PORT% --device %AZ_REMOTE_DEVICE% --weights-path "%AZ_REMOTE_WEIGHTS_PATH%" --search-config "%AZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %AZ_REMOTE_SYNC_INTERVAL% --batch-size %AZ_REMOTE_BATCH_SIZE% --batch-interval-ms %AZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%AZ_REMOTE_INIT_WEIGHTS%" --auth-token "%AZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %AZ_REMOTE_HOST% --port %AZ_REMOTE_PORT% --device %AZ_REMOTE_DEVICE% --weights-path "%AZ_REMOTE_WEIGHTS_PATH%" --search-config "%AZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %AZ_REMOTE_SYNC_INTERVAL% --batch-size %AZ_REMOTE_BATCH_SIZE% --batch-interval-ms %AZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%AZ_REMOTE_INIT_WEIGHTS%"
  goto :server_done
)

if not "%AZ_REMOTE_AUTH_TOKEN%"=="" (
  python "%SERVER_PY%" --host %AZ_REMOTE_HOST% --port %AZ_REMOTE_PORT% --device %AZ_REMOTE_DEVICE% --weights-path "%AZ_REMOTE_WEIGHTS_PATH%" --search-config "%AZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %AZ_REMOTE_SYNC_INTERVAL% --batch-size %AZ_REMOTE_BATCH_SIZE% --batch-interval-ms %AZ_REMOTE_BATCH_INTERVAL_MS% --auth-token "%AZ_REMOTE_AUTH_TOKEN%"
  goto :server_done
)
python "%SERVER_PY%" --host %AZ_REMOTE_HOST% --port %AZ_REMOTE_PORT% --device %AZ_REMOTE_DEVICE% --weights-path "%AZ_REMOTE_WEIGHTS_PATH%" --search-config "%AZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %AZ_REMOTE_SYNC_INTERVAL% --batch-size %AZ_REMOTE_BATCH_SIZE% --batch-interval-ms %AZ_REMOTE_BATCH_INTERVAL_MS%

:server_done

set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [ОШИБКА] Сервер завершился с кодом %EC%. См. runtime\logs\az_remote_is_*.log
) else (
  echo [EXIT] Сервер остановлен.
)
pause
exit /b %EC%
