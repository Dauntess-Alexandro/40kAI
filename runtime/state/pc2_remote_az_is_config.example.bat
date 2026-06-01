@echo off
REM Пример конфига AZ Remote IS для ПК2 (AlphaZero tree inference server).
REM Скопируйте в pc2_remote_az_is_config.bat и заполните пути.

REM --- SMB: файл весов с ПК1 (learner пишет latest_az_tree_policy.pth, сервер читает) ---
set "AZ_REMOTE_WEIGHTS_PATH=Z:\latest_az_tree_policy.pth"

REM --- Стартовый checkpoint, если на Z: ещё нет latest_az_tree_policy.pth (иначе пусто) ---
set "AZ_REMOTE_INIT_WEIGHTS="

REM --- JSON: obs_dim, action_sizes, hidden_size (как на ПК1) ---
REM С ПК1: tools\write_az_remote_search_cfg.bat кладёт копию в actor_sync (SMB Z:)
set "AZ_REMOTE_SEARCH_CONFIG=Z:\az_remote_search_cfg.json"

REM --- Сеть / GPU ---
set "AZ_REMOTE_HOST=0.0.0.0"
set "AZ_REMOTE_PORT=5555"
set "AZ_REMOTE_DEVICE=cuda:0"

REM --- Производительность ---
REM BATCH_SIZE = max batch на ПК2 (>= num_env_workers * parallel_sims на ПК1).
REM INTERVAL_MS = окно сбора батча (мс). Меньше = меньше задержка, хуже батчинг.
set "AZ_REMOTE_BATCH_SIZE=32"
set "AZ_REMOTE_BATCH_INTERVAL_MS=10"
set "AZ_REMOTE_SYNC_INTERVAL=0.5"

REM --- Опционально: общий секрет (должен совпадать с GUI на ПК1) ---
set "AZ_REMOTE_AUTH_TOKEN="

REM --- При первом setup: добавить правило firewall для порта (1=да, 0=нет) ---
set "AZ_REMOTE_SETUP_FIREWALL=1"
