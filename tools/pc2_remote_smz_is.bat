@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM 40kAI — Sampled MuZero Remote Inference Server на ПК2 (одна кнопка).
REM Запуск: tools\pc2_remote_smz_is.bat  (или двойной клик)
REM   tools\pc2_remote_smz_is.bat setup   — только установка + firewall + конфиг
REM   tools\pc2_remote_smz_is.bat start   — запуск (по умолчанию)
REM   tools\pc2_remote_smz_is.bat check   — проверка без сервера
REM Batch на ПК2 (дефолт из example = Very Heavy): SMZ_REMOTE_BATCH_SIZE=24, SMZ_REMOTE_BATCH_INTERVAL_MS=20

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "TOOLS=%~dp0"
if "%TOOLS:~-1%"=="\" set "TOOLS=%TOOLS:~0,-1%"
set "MODE=%~1"
if "%MODE%"=="" set "MODE=start"

echo.
echo ========================================
echo  40kAI  Sampled MuZero Remote IS  (PC2)
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

set "CONFIG_BAT=%ROOT%\runtime\state\pc2_remote_smz_is_config.bat"
set "CONFIG_EXAMPLE=%ROOT%\runtime\state\pc2_remote_smz_is_config.example.bat"
set "CONFIG_EXAMPLE_REV=%ROOT%\runtime\state\pc2_remote_smz_is_config.example.rev"
set "CONFIG_LOCAL_REV=%ROOT%\runtime\state\pc2_remote_smz_is_config.rev"
set "SERVER_PY=%TOOLS%\smz_remote_inference_server.py"

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
if not exist "%CONFIG_BAT%.bak" echo         Edit paths if needed: tools\pc2_remote_smz_is.bat config
exit /b 0

:after_config_sync

call "%CONFIG_BAT%"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось загрузить конфиг: %CONFIG_BAT%
  pause
  exit /b 1
)

REM Единый корень общей папки (как у акторов): если задан 40KAI_SHARE_ROOT и пути
REM не заданы явно — выводим их из него. Обе раскладки: SHARE\actor_sync\ или SHARE\.
REM Имя 40KAI_* начинается с цифры — в batch %40KAI_..% ломается на %4, читаем через for/f.
set "_SHARE="
for /f "tokens=1* delims==" %%A in ('set 40KAI_SHARE_ROOT 2^>nul') do set "_SHARE=%%B"
if not "%_SHARE%"=="" (
  if "%SMZ_REMOTE_WEIGHTS_PATH%"=="" (
    if exist "%_SHARE%\actor_sync\latest_smz_policy.pth" set "SMZ_REMOTE_WEIGHTS_PATH=%_SHARE%\actor_sync\latest_smz_policy.pth"
    if exist "%_SHARE%\latest_smz_policy.pth" set "SMZ_REMOTE_WEIGHTS_PATH=%_SHARE%\latest_smz_policy.pth"
  )
  if "%SMZ_REMOTE_SEARCH_CONFIG%"=="" (
    if exist "%_SHARE%\actor_sync\smz_remote_search_cfg.json" set "SMZ_REMOTE_SEARCH_CONFIG=%_SHARE%\actor_sync\smz_remote_search_cfg.json"
    if exist "%_SHARE%\smz_remote_search_cfg.json" set "SMZ_REMOTE_SEARCH_CONFIG=%_SHARE%\smz_remote_search_cfg.json"
  )
)

REM Фолбэк (обратная совместимость): прежний дефолт на Z:\.
if "%SMZ_REMOTE_WEIGHTS_PATH%"=="" set "SMZ_REMOTE_WEIGHTS_PATH=Z:\latest_smz_policy.pth"
if "%SMZ_REMOTE_SEARCH_CONFIG%"=="" set "SMZ_REMOTE_SEARCH_CONFIG=Z:\smz_remote_search_cfg.json"
if "%SMZ_REMOTE_WEIGHTS_PATH%"=="" (
  echo [ОШИБКА] В конфиге не задан SMZ_REMOTE_WEIGHTS_PATH
  notepad "%CONFIG_BAT%"
  pause
  exit /b 1
)
if "%SMZ_REMOTE_SEARCH_CONFIG%"=="" (
  echo [ОШИБКА] В конфиге не задан SMZ_REMOTE_SEARCH_CONFIG
  notepad "%CONFIG_BAT%"
  pause
  exit /b 1
)
if not exist "%SMZ_REMOTE_SEARCH_CONFIG%" (
  echo [ОШИБКА] search_cfg не найден: %SMZ_REMOTE_SEARCH_CONFIG%
  echo Создайте JSON по образцу в docs\remote-inference-server-smz.md
  pause
  exit /b 1
)

if "%SMZ_REMOTE_HOST%"=="" set "SMZ_REMOTE_HOST=0.0.0.0"
if "%SMZ_REMOTE_PORT%"=="" set "SMZ_REMOTE_PORT=5560"
if "%SMZ_REMOTE_DEVICE%"=="" set "SMZ_REMOTE_DEVICE=cuda:0"
if "%SMZ_REMOTE_BATCH_SIZE%"=="" set "SMZ_REMOTE_BATCH_SIZE=10"
if "%SMZ_REMOTE_BATCH_INTERVAL_MS%"=="" set "SMZ_REMOTE_BATCH_INTERVAL_MS=20"
if "%SMZ_REMOTE_SYNC_INTERVAL%"=="" set "SMZ_REMOTE_SYNC_INTERVAL=0.5"
if "%SMZ_REMOTE_COMPILE%"=="" set "SMZ_REMOTE_COMPILE=1"

if /i "%MODE%"=="check" goto :do_check
if /i "%MODE%"=="setup" goto :do_setup
if /i "%MODE%"=="start" goto :do_setup
goto :unknown_mode

:unknown_mode
echo [ОШИБКА] Неизвестный режим: %MODE%
echo Использование: tools\pc2_remote_smz_is.bat [setup^|start^|check^|config]
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

if "%SMZ_REMOTE_SETUP_FIREWALL%"=="1" (
  echo [SETUP] Правило firewall TCP %SMZ_REMOTE_PORT% ...
  netsh advfirewall firewall add rule name="40kAI SMZ Remote IS %SMZ_REMOTE_PORT%" dir=in action=allow protocol=TCP localport=%SMZ_REMOTE_PORT% >nul 2>&1
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
  echo [ОШИБКА] pyzmq или msgpack не установлены. Запустите: tools\pc2_remote_smz_is.bat setup
  pause
  exit /b 1
)

if /i "%MODE%"=="check" (
  echo.
  echo [OK] Проверка пройдена. Для запуска: tools\pc2_remote_smz_is.bat
  pause
  exit /b 0
)

if not exist "%SMZ_REMOTE_WEIGHTS_PATH%" (
  if "%SMZ_REMOTE_INIT_WEIGHTS%"=="" (
    echo [ОШИБКА] Нет файла весов: %SMZ_REMOTE_WEIGHTS_PATH%
    echo Укажите SMZ_REMOTE_INIT_WEIGHTS в конфиге или подключите SMB.
    pause
    exit /b 1
  )
  if not exist "%SMZ_REMOTE_INIT_WEIGHTS%" (
    echo [ОШИБКА] init-weights не найден: %SMZ_REMOTE_INIT_WEIGHTS%
    pause
    exit /b 1
  )
  echo [WARN] SMB-файл пока отсутствует — старт с --init-weights
) else (
  echo [OK] Веса SMB: %SMZ_REMOTE_WEIGHTS_PATH%
)

set "USE_INIT=0"
if not exist "%SMZ_REMOTE_WEIGHTS_PATH%" if not "%SMZ_REMOTE_INIT_WEIGHTS%"=="" set "USE_INIT=1"

echo.
echo [START] Remote IS  host=%SMZ_REMOTE_HOST%  port=%SMZ_REMOTE_PORT%  device=%SMZ_REMOTE_DEVICE%
echo         weights=%SMZ_REMOTE_WEIGHTS_PATH%
echo         search=%SMZ_REMOTE_SEARCH_CONFIG%
echo         Остановка: Ctrl+C
echo.

if "%USE_INIT%"=="1" (
  if "%SMZ_REMOTE_COMPILE%"=="1" (
    if not "%SMZ_REMOTE_AUTH_TOKEN%"=="" (
      python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%SMZ_REMOTE_INIT_WEIGHTS%" --compile --auth-token "%SMZ_REMOTE_AUTH_TOKEN%"
      goto :server_done
    )
    python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%SMZ_REMOTE_INIT_WEIGHTS%" --compile
    goto :server_done
  )
  if not "%SMZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%SMZ_REMOTE_INIT_WEIGHTS%" --auth-token "%SMZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%SMZ_REMOTE_INIT_WEIGHTS%"
  goto :server_done
)

if "%SMZ_REMOTE_COMPILE%"=="1" (
  if not "%SMZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --compile --auth-token "%SMZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --compile
  goto :server_done
)
if not "%SMZ_REMOTE_AUTH_TOKEN%"=="" (
  python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS% --auth-token "%SMZ_REMOTE_AUTH_TOKEN%"
  goto :server_done
)
python "%SERVER_PY%" --host %SMZ_REMOTE_HOST% --port %SMZ_REMOTE_PORT% --device %SMZ_REMOTE_DEVICE% --weights-path "%SMZ_REMOTE_WEIGHTS_PATH%" --search-config "%SMZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --sync-interval %SMZ_REMOTE_SYNC_INTERVAL% --batch-size %SMZ_REMOTE_BATCH_SIZE% --batch-interval-ms %SMZ_REMOTE_BATCH_INTERVAL_MS%

:server_done

set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [ОШИБКА] Сервер завершился с кодом %EC%. См. runtime\logs\smz_remote_is_*.log
) else (
  echo [EXIT] Сервер остановлен.
)
pause
exit /b %EC%
