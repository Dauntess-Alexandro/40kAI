@echo off
REM Пример конфига AZ Remote IS для ПК2 (AlphaZero tree inference server).
REM При git pull: tools\pc2_remote_az_is.bat сам обновит pc2_remote_az_is_config.bat,
REM если pc2_remote_az_is_config.example.rev новее (старый → .bat.bak).
REM Свои пути (Z:, auth) после обновления проверь в .bat или .bat.bak.

REM --- SMB: Z: = весь artifacts\models (рекомендуется; внутри actor_sync + agents) ---
REM Если Z: = только actor_sync (legacy), пути без actor_sync\ — bat подставит сам при старте.
set "AZ_REMOTE_WEIGHTS_PATH=Z:\actor_sync\latest_az_tree_policy.pth"

REM --- Стартовый checkpoint, если на Z: ещё нет latest_az_tree_policy.pth (иначе пусто) ---
set "AZ_REMOTE_INIT_WEIGHTS="

REM --- JSON: obs_dim, action_sizes (ПК1: tools\write_az_remote_search_cfg.bat) ---
set "AZ_REMOTE_SEARCH_CONFIG=Z:\actor_sync\az_remote_search_cfg.json"

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

REM --- Distributed self-play (CPU env на ПК2 → rollout на ПК1) ---
REM 1 = pc2_remote_az_is.bat поднимает IS + actors одной кнопкой (IS в отдельном окне).
REM Train на ПК1 должен быть уже запущен (receiver :5557). На ПК1 открыть inbound TCP 5557.
set "AZ_REMOTE_DIST_ACTORS_ENABLED=1"
set "AZ_REMOTE_DIST_ACTORS_DELAY_SEC=12"
REM Сек: ждать az_dist_train_context.json с ПК1 (если ПК2 стартуют до train)
set "AZ_DIST_WAIT_CONTEXT_SEC=90"
REM IP ПК1 (learner), не ПК2:
set "AZ_DIST_PC1_HOST=192.168.0.100"
set "AZ_DIST_ROLLOUT_PORT=5557"
set "AZ_DIST_PC2_IS_HOST=127.0.0.1"
set "AZ_DIST_PC2_IS_PORT=5555"
set "AZ_DIST_STOP_FLAG_PATH=Z:\actor_sync\az_dist_stop.flag"
set "MODELS_DIR=Z:\"
set "AZ_DIST_PC2_NUM_WORKERS=4"
set "AZ_DIST_PC2_WORKER_ID_BASE=100"
REM Пусто = авто из train (SMB az_dist_train_context.json) или latest_snapshot на Z:\agents
set "OPPONENT_AGENT_ID="
set "AZ_DIST_ENV_CONTRACT_HASH="
set "AZ_DIST_AUTH_TOKEN="
set "AZ_INFERENCE_REMOTE_AUTH_TOKEN="
