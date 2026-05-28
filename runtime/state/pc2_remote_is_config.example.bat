@echo off
REM Пример конфига Remote IS для ПК2.
REM Скопируется в pc2_remote_is_config.bat при первом запуске tools\pc2_remote_is.bat
REM Отредактируйте пути под свой ПК и сохраните.

REM --- SMB: файл весов с ПК1 (learner пишет, сервер читает) ---
set "GMZ_REMOTE_WEIGHTS_PATH=Z:\latest_gmz_policy.pth"

REM --- Стартовый checkpoint, если на Z: ещё нет latest_gmz_policy.pth (иначе пусто) ---
set "GMZ_REMOTE_INIT_WEIGHTS="

REM --- JSON: obs_dim, action_sizes, num_simulations (как на ПК1) ---
REM С ПК1: tools\write_gmz_remote_search_cfg.bat кладёт копию в actor_sync (SMB Z:)
set "GMZ_REMOTE_SEARCH_CONFIG=Z:\gmz_remote_search_cfg.json"

REM --- Сеть / GPU ---
set "GMZ_REMOTE_HOST=0.0.0.0"
set "GMZ_REMOTE_PORT=5555"
set "GMZ_REMOTE_DEVICE=cuda:0"

REM --- Производительность ---
REM BATCH_SIZE = число env-воркеров на ПК1 (больше не доедет по сети, воркеры блокируются по ходу).
REM INTERVAL_MS = окно сбора батча: батч-поиск собирает запросы и гонит одним forward'ом.
REM   По LAN запросы прилетают вразнобой — окно ~8-10мс даёт им «слететься» (5мс часто мало).
REM   Смотри средний batch= в runtime\logs\gmz_remote_is_*.log: должен быть близок к BATCH_SIZE, не к 1.
set "GMZ_REMOTE_BATCH_SIZE=10"
set "GMZ_REMOTE_BATCH_INTERVAL_MS=8"
set "GMZ_REMOTE_SYNC_INTERVAL=0.5"
REM Windows: triton often missing; 0 = no torch.compile warning, still uses GPU
set "GMZ_REMOTE_COMPILE=0"

REM --- Опционально: общий секрет (должен совпадать с GUI на ПК1) ---
set "GMZ_REMOTE_AUTH_TOKEN="

REM --- При первом setup: добавить правило firewall для порта (1=да, 0=нет) ---
set "GMZ_REMOTE_SETUP_FIREWALL=1"
