@echo off
REM Пример конфига Remote IS для ПК2.
REM Скопируется в pc2_remote_is_config.bat при первом запуске tools\pc2_remote_is.bat
REM Отредактируйте пути под свой ПК и сохраните.

REM --- SMB: файл весов с ПК1 (learner пишет, сервер читает) ---
set "GMZ_REMOTE_WEIGHTS_PATH=Z:\latest_gmz_policy.pth"

REM --- Стартовый checkpoint, если на SMB ещё нет latest_gmz_policy.pth ---
REM Оставьте пустым, если weights-path уже существует:
set "GMZ_REMOTE_INIT_WEIGHTS=C:\40kAI\artifacts\models\gumbel_muzero\checkpoint_ep1.pth"

REM --- JSON: obs_dim, action_sizes, num_simulations (как на ПК1) ---
set "GMZ_REMOTE_SEARCH_CONFIG=C:\40kAI\runtime\state\gmz_remote_search_cfg.json"

REM --- Сеть / GPU ---
set "GMZ_REMOTE_HOST=0.0.0.0"
set "GMZ_REMOTE_PORT=5555"
set "GMZ_REMOTE_DEVICE=cuda:0"

REM --- Производительность ---
set "GMZ_REMOTE_BATCH_SIZE=10"
set "GMZ_REMOTE_BATCH_INTERVAL_MS=20"
set "GMZ_REMOTE_SYNC_INTERVAL=0.5"
set "GMZ_REMOTE_COMPILE=1"

REM --- Опционально: общий секрет (должен совпадать с GUI на ПК1) ---
set "GMZ_REMOTE_AUTH_TOKEN="

REM --- При первом setup: добавить правило firewall для порта (1=да, 0=нет) ---
set "GMZ_REMOTE_SETUP_FIREWALL=1"
