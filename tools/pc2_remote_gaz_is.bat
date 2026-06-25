@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM 40kAI — GAZ Remote Inference Server на ПК2 (одна кнопка).
REM Запуск: tools\pc2_remote_gaz_is.bat  (или двойной клик = start)
REM   tools\pc2_remote_gaz_is.bat setup   — venv + firewall + конфиг
REM   tools\pc2_remote_gaz_is.bat start   — запуск сервера
REM   tools\pc2_remote_gaz_is.bat check   — проверка без сервера
REM   tools\pc2_remote_gaz_is.bat config  — открыть конфиг в блокноте
REM   tools\pc2_remote_gaz_is.bat actors-only — только dist-акторы (IS уже запущен)
REM   tools\pc2_remote_gaz_is.bat serve — только IS (внутренний режим, отдельное окно)
REM При GAZ_REMOTE_DIST_ACTORS_ENABLED=1 (по умолчанию в example): IS + actors одной кнопкой.

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "TOOLS=%~dp0"
if "%TOOLS:~-1%"=="\" set "TOOLS=%TOOLS:~0,-1%"
set "MODE=%~1"
if "%MODE%"=="" set "MODE=start"

echo.
echo ========================================
echo  40kAI  GAZ Remote Inference Server (PC2)
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

set "CONFIG_BAT=%ROOT%\runtime\state\pc2_remote_gaz_is_config.bat"
set "CONFIG_EXAMPLE=%ROOT%\runtime\state\pc2_remote_gaz_is_config.example.bat"
set "CONFIG_EXAMPLE_REV=%ROOT%\runtime\state\pc2_remote_gaz_is_config.example.rev"
set "CONFIG_LOCAL_REV=%ROOT%\runtime\state\pc2_remote_gaz_is_config.rev"
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

:resolve_smb_paths
REM Единый корень общей папки (как у акторов): сперва пробуем 40KAI_SHARE_ROOT, потом Z:.
REM Обе раскладки: SHARE\actor_sync\ (SHARE=models) или SHARE\ (SHARE=actor_sync).
REM Имя 40KAI_* начинается с цифры — в batch %40KAI_..% ломается на %4, читаем через for/f.
set "_SHARE="
for /f "tokens=1* delims==" %%A in ('set 40KAI_SHARE_ROOT 2^>nul') do set "_SHARE=%%B"
if not "%_SHARE%"=="" (
  if not exist "%GAZ_REMOTE_SEARCH_CONFIG%" (
    if exist "%_SHARE%\actor_sync\gaz_remote_search_cfg.json" set "GAZ_REMOTE_SEARCH_CONFIG=%_SHARE%\actor_sync\gaz_remote_search_cfg.json"
    if exist "%_SHARE%\gaz_remote_search_cfg.json" set "GAZ_REMOTE_SEARCH_CONFIG=%_SHARE%\gaz_remote_search_cfg.json"
  )
  if not exist "%GAZ_REMOTE_WEIGHTS_PATH%" (
    if exist "%_SHARE%\actor_sync\latest_az_gumbel_az_policy.pth" set "GAZ_REMOTE_WEIGHTS_PATH=%_SHARE%\actor_sync\latest_az_gumbel_az_policy.pth"
    if exist "%_SHARE%\latest_az_gumbel_az_policy.pth" set "GAZ_REMOTE_WEIGHTS_PATH=%_SHARE%\latest_az_gumbel_az_policy.pth"
  )
  if "%MODELS_DIR%"=="" set "MODELS_DIR=%_SHARE%"
)

REM Z: = artifacts\models (файлы в actor_sync\) или Z: = только actor_sync (файлы в корне Z:\).
if not exist "%GAZ_REMOTE_SEARCH_CONFIG%" (
  if exist "Z:\actor_sync\gaz_remote_search_cfg.json" set "GAZ_REMOTE_SEARCH_CONFIG=Z:\actor_sync\gaz_remote_search_cfg.json"
  if exist "Z:\gaz_remote_search_cfg.json" set "GAZ_REMOTE_SEARCH_CONFIG=Z:\gaz_remote_search_cfg.json"
)
if not exist "%GAZ_REMOTE_WEIGHTS_PATH%" (
  if exist "Z:\actor_sync\latest_az_gumbel_az_policy.pth" set "GAZ_REMOTE_WEIGHTS_PATH=Z:\actor_sync\latest_az_gumbel_az_policy.pth"
  if exist "Z:\latest_az_gumbel_az_policy.pth" set "GAZ_REMOTE_WEIGHTS_PATH=Z:\latest_az_gumbel_az_policy.pth"
)
if "%MODELS_DIR%"=="" set "MODELS_DIR=Z:\"
if /i "%MODELS_DIR%"=="Z:\actor_sync" if exist "Z:\agents\" set "MODELS_DIR=Z:\"
if not "%MODELS_DIR%"=="" set "40KAI_MODELS_DIR=%MODELS_DIR%"
exit /b 0

:sync_config_from_example
if not exist "%CONFIG_EXAMPLE%" exit /b 0
set "EX_REV=0"
set "CFG_REV=0"
if exist "%CONFIG_EXAMPLE_REV%" set /p EX_REV=<"%CONFIG_EXAMPLE_REV%"
if exist "%CONFIG_LOCAL_REV%" set /p CFG_REV=<"%CONFIG_LOCAL_REV%"
if not defined EX_REV set "EX_REV=0"
if not defined CFG_REV set "CFG_REV=0"
echo %CFG_REV%| findstr /r "^[0-9][0-9]*$" >nul || set "CFG_REV=0"
echo %EX_REV%| findstr /r "^[0-9][0-9]*$" >nul || set "EX_REV=0"
if not exist "%CONFIG_BAT%" goto :do_copy_example_config
if %CFG_REV% LSS %EX_REV% goto :do_copy_example_config
exit /b 0

:do_copy_example_config
if exist "%CONFIG_BAT%" (
  copy /Y "%CONFIG_BAT%" "%CONFIG_BAT%.bak" >nul
  echo [CONFIG] Backup: %CONFIG_BAT%.bak
)
copy /Y "%CONFIG_EXAMPLE%" "%CONFIG_BAT%" >nul
> "%CONFIG_LOCAL_REV%" echo %EX_REV%
echo [CONFIG] Synced %CONFIG_BAT% from example rev %EX_REV%
if not exist "%CONFIG_BAT%.bak" echo         Edit paths if needed: tools\pc2_remote_gaz_is.bat config
exit /b 0

:after_config_sync

call "%CONFIG_BAT%"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось загрузить конфиг: %CONFIG_BAT%
  pause
  exit /b 1
)

if "%GAZ_REMOTE_WEIGHTS_PATH%"=="" set "GAZ_REMOTE_WEIGHTS_PATH=Z:\actor_sync\latest_az_gumbel_az_policy.pth"
if "%GAZ_REMOTE_SEARCH_CONFIG%"=="" set "GAZ_REMOTE_SEARCH_CONFIG=Z:\actor_sync\gaz_remote_search_cfg.json"
call :resolve_smb_paths
if "%GAZ_REMOTE_WEIGHTS_PATH%"=="" (
  echo [ОШИБКА] В конфиге не задан GAZ_REMOTE_WEIGHTS_PATH
  echo Что делать: tools\pc2_remote_gaz_is.bat config
  pause
  exit /b 1
)
if "%GAZ_REMOTE_SEARCH_CONFIG%"=="" (
  echo [ОШИБКА] В конфиге не задан GAZ_REMOTE_SEARCH_CONFIG
  echo Что делать: tools\pc2_remote_gaz_is.bat config
  pause
  exit /b 1
)
if not exist "%GAZ_REMOTE_SEARCH_CONFIG%" (
  set "AZ_ENSURE_PENDING=1"
) else (
  set "AZ_ENSURE_PENDING=0"
)

if "%GAZ_REMOTE_HOST%"=="" set "GAZ_REMOTE_HOST=0.0.0.0"
if "%GAZ_REMOTE_PORT%"=="" set "GAZ_REMOTE_PORT=5565"
if "%GAZ_REMOTE_DEVICE%"=="" set "GAZ_REMOTE_DEVICE=cuda:0"
if "%GAZ_REMOTE_BATCH_SIZE%"=="" set "GAZ_REMOTE_BATCH_SIZE=32"
if "%GAZ_REMOTE_BATCH_INTERVAL_MS%"=="" set "GAZ_REMOTE_BATCH_INTERVAL_MS=10"
if "%GAZ_REMOTE_SYNC_INTERVAL%"=="" set "GAZ_REMOTE_SYNC_INTERVAL=0.5"
if "%GAZ_REMOTE_SETUP_FIREWALL%"=="" set "GAZ_REMOTE_SETUP_FIREWALL=1"

if /i "%MODE%"=="check" goto :do_check
if /i "%MODE%"=="setup" goto :do_setup
if /i "%MODE%"=="start" goto :do_setup
if /i "%MODE%"=="serve" goto :do_serve
if /i "%MODE%"=="actors-only" goto :do_actors_only
goto :unknown_mode

:unknown_mode
echo [ОШИБКА] Неизвестный режим: %MODE%
echo Использование: tools\pc2_remote_gaz_is.bat [setup^|start^|check^|config^|actors-only]
pause
exit /b 1

:apply_dist_env
if "%AZ_DIST_TRAIN_ALGO%"=="" set "AZ_DIST_TRAIN_ALGO=gumbel_az"
if "%AZ_DIST_PC2_IS_HOST%"=="" set "AZ_DIST_PC2_IS_HOST=127.0.0.1"
if "%AZ_DIST_PC2_IS_PORT%"=="" set "AZ_DIST_PC2_IS_PORT=%GAZ_REMOTE_PORT%"
if "%AZ_DIST_ROLLOUT_PORT%"=="" set "AZ_DIST_ROLLOUT_PORT=5567"
if "%AZ_DIST_PC2_NUM_WORKERS%"=="" set "AZ_DIST_PC2_NUM_WORKERS=8"
if "%AZ_DIST_PC2_WORKER_ID_BASE%"=="" set "AZ_DIST_PC2_WORKER_ID_BASE=100"
if "%GAZ_REMOTE_DIST_ACTORS_DELAY_SEC%"=="" set "GAZ_REMOTE_DIST_ACTORS_DELAY_SEC=12"
if "%AZ_DIST_WAIT_CONTEXT_SEC%"=="" set "AZ_DIST_WAIT_CONTEXT_SEC=90"
if "%AZ_DIST_STOP_FLAG_PATH%"=="" set "AZ_DIST_STOP_FLAG_PATH=Z:\actor_sync\gaz_dist_stop.flag"
if "%MODELS_DIR%"=="" set "MODELS_DIR=Z:\actor_sync"
if "%AZ_INFERENCE_REMOTE_AUTH_TOKEN%"=="" if not "%GAZ_REMOTE_AUTH_TOKEN%"=="" set "AZ_INFERENCE_REMOTE_AUTH_TOKEN=%GAZ_REMOTE_AUTH_TOKEN%"
if "%AZ_DIST_AUTH_TOKEN%"=="" if not "%GAZ_REMOTE_AUTH_TOKEN%"=="" set "AZ_DIST_AUTH_TOKEN=%GAZ_REMOTE_AUTH_TOKEN%"
exit /b 0

:run_actors_foreground
call "%ROOT%\.venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось активировать .venv для dist actors
  pause
  exit /b 1
)
echo.
echo [START] Distributed actors  target=%AZ_DIST_PC1_HOST%:%AZ_DIST_ROLLOUT_PORT%  is=%AZ_DIST_PC2_IS_HOST%:%AZ_DIST_PC2_IS_PORT%  workers=%AZ_DIST_PC2_NUM_WORKERS%
echo         Train на ПК1 должен быть запущен (distributed_actors_enabled=1).
echo         Остановка: Ctrl+C
echo.
python "%TOOLS%\pc2_az_actors.py"
set "EC=%ERRORLEVEL%"
if not "%EC%"=="0" echo [ОШИБКА] pc2_az_actors exit=%EC%
exit /b %EC%

:do_actors_only
call :apply_dist_env
if "%AZ_DIST_PC1_HOST%"=="" (
  echo [ОШИБКА] Не задан AZ_DIST_PC1_HOST ^(IP ПК1^) в %CONFIG_BAT%
  echo Что делать: tools\pc2_remote_gaz_is.bat config
  pause
  exit /b 1
)
if not exist "%ROOT%\.venv\Scripts\python.exe" (
  echo [SETUP] .venv не найден — setup...
  call "%ROOT%\installer\install_deps.bat" -y
)
call :run_actors_foreground
pause
exit /b %EC%

:do_serve
call "%ROOT%\.venv\Scripts\activate.bat"
if errorlevel 1 (
  echo [ОШИБКА] Не удалось активировать .venv
  exit /b 1
)
set "USE_INIT=0"
if not exist "%GAZ_REMOTE_WEIGHTS_PATH%" if not "%GAZ_REMOTE_INIT_WEIGHTS%"=="" set "USE_INIT=1"
goto :start_is_foreground

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

if "%GAZ_REMOTE_SETUP_FIREWALL%"=="1" (
  echo [SETUP] Правило firewall TCP %GAZ_REMOTE_PORT% ...
  netsh advfirewall firewall add rule name="40kAI GAZ Remote IS %GAZ_REMOTE_PORT%" dir=in action=allow protocol=TCP localport=%GAZ_REMOTE_PORT% >nul 2>&1
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
  echo [ОШИБКА] pyzmq или msgpack не установлены. Запустите: tools\pc2_remote_gaz_is.bat setup
  pause
  exit /b 1
)

if "%AZ_ENSURE_PENDING%"=="1" (
  call :ensure_search_cfg
  call :resolve_smb_paths
)
if not exist "%GAZ_REMOTE_SEARCH_CONFIG%" (
  echo [ОШИБКА] search_cfg не найден: %GAZ_REMOTE_SEARCH_CONFIG%
  echo Лаунчер ПК2 или Qt GUI на ПК1 создают search_cfg на шаре автоматически.
  pause
  exit /b 1
)

if /i "%MODE%"=="check" (
  echo.
  echo [OK] Проверка пройдена. Для запуска: tools\pc2_remote_gaz_is.bat
  pause
  exit /b 0
)

if not exist "%GAZ_REMOTE_WEIGHTS_PATH%" (
  if "%GAZ_REMOTE_INIT_WEIGHTS%"=="" (
    echo [ОШИБКА] Нет файла весов: %GAZ_REMOTE_WEIGHTS_PATH%
    echo Укажите GAZ_REMOTE_INIT_WEIGHTS в конфиге или подключите SMB Z:\
    pause
    exit /b 1
  )
  if not exist "%GAZ_REMOTE_INIT_WEIGHTS%" (
    echo [ОШИБКА] init-weights не найден: %GAZ_REMOTE_INIT_WEIGHTS%
    pause
    exit /b 1
  )
  echo [WARN] SMB-файл пока отсутствует — старт с --init-weights
) else (
  echo [OK] Веса SMB: %GAZ_REMOTE_WEIGHTS_PATH%
)

set "USE_INIT=0"
if not exist "%GAZ_REMOTE_WEIGHTS_PATH%" if not "%GAZ_REMOTE_INIT_WEIGHTS%"=="" set "USE_INIT=1"

if "%GAZ_REMOTE_DIST_ACTORS_ENABLED%"=="" set "GAZ_REMOTE_DIST_ACTORS_ENABLED=0"
if /i not "%MODE%"=="serve" if "%GAZ_REMOTE_DIST_ACTORS_ENABLED%"=="1" goto :start_dist_bundle

:start_is_foreground
echo.
echo [START] GAZ Remote IS  host=%GAZ_REMOTE_HOST%  port=%GAZ_REMOTE_PORT%  device=%GAZ_REMOTE_DEVICE%
echo         weights=%GAZ_REMOTE_WEIGHTS_PATH%
echo         search=%GAZ_REMOTE_SEARCH_CONFIG%
echo         Остановка: Ctrl+C
echo         Лог: runtime\logs\gaz_remote_is_*.log
echo.

if "%USE_INIT%"=="1" (
  if not "%GAZ_REMOTE_AUTH_TOKEN%"=="" (
    python "%SERVER_PY%" --host %GAZ_REMOTE_HOST% --port %GAZ_REMOTE_PORT% --device %GAZ_REMOTE_DEVICE% --weights-path "%GAZ_REMOTE_WEIGHTS_PATH%" --search-config "%GAZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --algo-label GAZ --sync-interval %GAZ_REMOTE_SYNC_INTERVAL% --batch-size %GAZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GAZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GAZ_REMOTE_INIT_WEIGHTS%" --auth-token "%GAZ_REMOTE_AUTH_TOKEN%"
    goto :server_done
  )
  python "%SERVER_PY%" --host %GAZ_REMOTE_HOST% --port %GAZ_REMOTE_PORT% --device %GAZ_REMOTE_DEVICE% --weights-path "%GAZ_REMOTE_WEIGHTS_PATH%" --search-config "%GAZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --algo-label GAZ --sync-interval %GAZ_REMOTE_SYNC_INTERVAL% --batch-size %GAZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GAZ_REMOTE_BATCH_INTERVAL_MS% --init-weights "%GAZ_REMOTE_INIT_WEIGHTS%"
  goto :server_done
)

if not "%GAZ_REMOTE_AUTH_TOKEN%"=="" (
  python "%SERVER_PY%" --host %GAZ_REMOTE_HOST% --port %GAZ_REMOTE_PORT% --device %GAZ_REMOTE_DEVICE% --weights-path "%GAZ_REMOTE_WEIGHTS_PATH%" --search-config "%GAZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --algo-label GAZ --sync-interval %GAZ_REMOTE_SYNC_INTERVAL% --batch-size %GAZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GAZ_REMOTE_BATCH_INTERVAL_MS% --auth-token "%GAZ_REMOTE_AUTH_TOKEN%"
  goto :server_done
)
python "%SERVER_PY%" --host %GAZ_REMOTE_HOST% --port %GAZ_REMOTE_PORT% --device %GAZ_REMOTE_DEVICE% --weights-path "%GAZ_REMOTE_WEIGHTS_PATH%" --search-config "%GAZ_REMOTE_SEARCH_CONFIG%" --sync-method smb --algo-label GAZ --sync-interval %GAZ_REMOTE_SYNC_INTERVAL% --batch-size %GAZ_REMOTE_BATCH_SIZE% --batch-interval-ms %GAZ_REMOTE_BATCH_INTERVAL_MS%

:server_done

set "EC=%ERRORLEVEL%"
echo.
if not "%EC%"=="0" (
  echo [ОШИБКА] Сервер завершился с кодом %EC%. См. runtime\logs\gaz_remote_is_*.log
) else (
  echo [EXIT] Сервер остановлен.
)
if /i "%MODE%"=="serve" exit /b %EC%
pause
exit /b %EC%

:start_dist_bundle
call :apply_dist_env
if "%AZ_DIST_PC1_HOST%"=="" (
  echo [ОШИБКА] GAZ_REMOTE_DIST_ACTORS_ENABLED=1, но не задан AZ_DIST_PC1_HOST ^(IP ПК1^).
  echo Что делать: tools\pc2_remote_gaz_is.bat config
  pause
  exit /b 1
)
echo.
echo [START] IS + distributed actors ^(два процесса^)
echo         1^) IS в отдельном окне  :%GAZ_REMOTE_PORT%
echo         2^) Actors здесь  -^> %AZ_DIST_PC1_HOST%:%AZ_DIST_ROLLOUT_PORT%
echo         Сначала запустите train на ПК1, затем этот bat ^(или наоборот в течение ~1 мин^).
echo.
start "40kAI GAZ IS" cmd /k ""%~f0" serve"
echo [WAIT] Ждём готовности IS ^(%GAZ_REMOTE_DIST_ACTORS_DELAY_SEC% с^)...
REM timeout падает при запуске из GUI (stdin перенаправлён): "Input redirection is not supported".
REM ping -n N даёт ~N-1 c паузы и не требует консольного stdin.
set /a "_IS_WAIT_PINGS=%GAZ_REMOTE_DIST_ACTORS_DELAY_SEC%+1"
ping -n %_IS_WAIT_PINGS% 127.0.0.1 >nul 2>&1
call :run_actors_foreground
set "EC=%ERRORLEVEL%"
echo.
echo [INFO] Окно "40kAI GAZ IS" может оставаться открытым — закройте его вручную после train.
pause
exit /b %EC%

:ensure_search_cfg
set "_SHARE="
for /f "tokens=1* delims==" %%A in ('set 40KAI_SHARE_ROOT 2^>nul') do set "_SHARE=%%B"
if "%_SHARE%"=="" (
  echo [WARN] 40KAI_SHARE_ROOT не задан — ensure search_cfg пропущен
  exit /b 0
)
echo [SETUP] search_cfg не найден — ensure_remote_search_cfg.py --algo gaz ...
python "%TOOLS%\ensure_remote_search_cfg.py" --algo gaz --share-root "%_SHARE%"
if errorlevel 1 (
  echo [WARN] ensure_remote_search_cfg завершился с ошибкой
) else (
  set "AZ_ENSURE_PENDING=0"
)
exit /b 0
