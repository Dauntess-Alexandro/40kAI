@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion
REM ============================================================
REM  40kAI — AZ Distributed Actors (ПК2), одна кнопка.
REM  Требуется: pc2_remote_az_is.bat уже запущен (IS :5555).
REM ============================================================

cd /d "%~dp0\.."
set "ROOT=%cd%"
set "MODE=%~1"

set "CFG=%ROOT%\runtime\state\pc2_az_actors_config.bat"
set "CFG_EXAMPLE=%ROOT%\runtime\state\pc2_az_actors_config.example.bat"

if not exist "%CFG%" (
  echo [SETUP] Конфиг не найден, создаю из примера: %CFG%
  copy /y "%CFG_EXAMPLE%" "%CFG%" >nul
  echo [SETUP] Заполните AZ_DIST_PC1_HOST и OPPONENT_AGENT_ID, затем запустите bat снова.
  notepad "%CFG%"
  pause
  exit /b 0
)

call "%CFG%"

set "VENV=%ROOT%\.venv\Scripts\activate.bat"
if not exist "%VENV%" (
  echo [SETUP] .venv не найден, ставлю зависимости...
  call "%ROOT%\installer\install_deps.bat" -y
)
call "%VENV%"

if /i "%MODE%"=="check" (
  python -c "import zmq, msgpack; print('zmq+msgpack OK')"
  pause
  exit /b 0
)

if /i "%MODE%"=="setup" (
  if "%AZ_DIST_SETUP_FIREWALL_PC2%"=="1" (
    echo [SETUP] Firewall на PC2 для dist actors обычно не нужен (PUSH к PC1).
  )
  pause
  exit /b 0
)

echo [AZ][DIST] Запуск PC2 actors. IS должен слушать %AZ_DIST_PC2_IS_HOST%:%AZ_DIST_PC2_IS_PORT%
python "%ROOT%\tools\pc2_az_actors.py"
set "EC=%ERRORLEVEL%"
if not "%EC%"=="0" echo [ОШИБКА] pc2_az_actors exit=%EC%
pause
exit /b %EC%
