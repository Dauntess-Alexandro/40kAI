@echo off
REM Пример конфига Remote IS для ПК2.
REM При git pull: tools\pc2_remote_is.bat сам обновит pc2_remote_is_config.bat,
REM если pc2_remote_is_config.example.rev новее (старый → .bat.bak).
REM Свои пути (Z:, auth) после обновления проверь в .bat или .bat.bak.

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

REM --- Производительность (дефолт = Very Heavy, 20 workers на ПК1) ---
REM BATCH_SIZE = max batch на ПК2 (>= num_env_workers на ПК1).
REM INTERVAL_MS = окно сбора батча: батч-поиск собирает запросы и гонит одним forward'ом.
REM   Heavy (10 workers):      BATCH_SIZE=10,  INTERVAL_MS=8
REM   Very Heavy (20 workers): BATCH_SIZE=24,  INTERVAL_MS=20  ← дефолт ниже
REM   Смотри средний batch= в runtime\logs\gmz_remote_is_*.log: должен быть близок к BATCH_SIZE, не к 1.
set "GMZ_REMOTE_BATCH_SIZE=24"
set "GMZ_REMOTE_BATCH_INTERVAL_MS=20"
set "GMZ_REMOTE_SYNC_INTERVAL=0.5"
REM Windows: triton often missing; 0 = no torch.compile warning, still uses GPU
set "GMZ_REMOTE_COMPILE=0"

REM --- Опционально: общий секрет (должен совпадать с GUI на ПК1) ---
set "GMZ_REMOTE_AUTH_TOKEN="

REM --- При первом setup: добавить правило firewall для порта (1=да, 0=нет) ---
set "GMZ_REMOTE_SETUP_FIREWALL=1"
