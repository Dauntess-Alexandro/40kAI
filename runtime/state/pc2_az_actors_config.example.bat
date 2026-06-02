@echo off
REM Пример конфига distributed AZ actors на ПК2 (IS LAN + rollout → ПК1).
REM Скопируйте в pc2_az_actors_config.bat и заполните.

REM --- ПК1: IP learner (RolloutReceiver PULL :5557) ---
set "AZ_DIST_PC1_HOST=192.168.1.10"
set "AZ_DIST_ROLLOUT_PORT=5557"

REM --- ПК2: localhost IS (pc2_remote_az_is.bat должен быть запущен) ---
set "AZ_DIST_PC2_IS_HOST=127.0.0.1"
set "AZ_DIST_PC2_IS_PORT=5555"

REM --- SMB: stop.flag и веса (тот же share, что для IS) ---
set "AZ_DIST_STOP_FLAG_PATH=Z:\az_dist_stop.flag"
set "MODELS_DIR=Z:"

REM --- Воркеры ---
set "AZ_DIST_PC2_NUM_WORKERS=4"
set "AZ_DIST_PC2_WORKER_ID_BASE=100"

REM --- Должен совпадать с train на ПК1 (GUI / hyperparams) ---
set "OPPONENT_AGENT_ID="
set "AZ_DIST_ENV_CONTRACT_HASH="
set "AZ_DIST_AUTH_TOKEN="
set "AZ_INFERENCE_REMOTE_AUTH_TOKEN="

REM --- При setup: firewall для исходящих не нужен; на ПК1 открыть 5557 inbound ---
set "AZ_DIST_SETUP_FIREWALL_PC2=0"
