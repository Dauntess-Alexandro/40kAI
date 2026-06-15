@echo off
REM Конфиг ПК2 для Sampled MuZero Remote Inference Server.
REM Копируется в pc2_remote_smz_is_config.bat при первом запуске. Правьте пути под вашу SMB-шару.
set "SMZ_REMOTE_HOST=0.0.0.0"
set "SMZ_REMOTE_PORT=5560"
set "SMZ_REMOTE_DEVICE=cuda:0"
set "SMZ_REMOTE_BATCH_SIZE=10"
set "SMZ_REMOTE_BATCH_INTERVAL_MS=20"
set "SMZ_REMOTE_SYNC_INTERVAL=0.5"
set "SMZ_REMOTE_COMPILE=1"
set "SMZ_REMOTE_AUTH_TOKEN="
set "SMZ_REMOTE_SETUP_FIREWALL=1"
REM Веса и search-cfg (если не выводятся из 40KAI_SHARE_ROOT автоматически):
set "SMZ_REMOTE_WEIGHTS_PATH="
set "SMZ_REMOTE_SEARCH_CONFIG="
set "SMZ_REMOTE_INIT_WEIGHTS="
exit /b 0
