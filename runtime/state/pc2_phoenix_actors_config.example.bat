@echo off
REM === Конфиг ПК2 для PHOENIX distributed actors ===
REM
REM Обычно достаточно задать общую SMB-папку ПК1 (где лежит artifacts/models или actor_sync):
if not defined 40KAI_SHARE_ROOT set "40KAI_SHARE_ROOT=\\192.168.0.100\actor_sync"
REM
REM Остальное берётся автоматически из phoenix_dist_train_context.json, который пишет ПК1:
REM   - IP ПК1    из UNC-пути шары
REM   - порт+auth из контекста ПК1
REM   - воркеры   из контекста ПК1
REM
REM --- Переопределения (раскомментируй, если автодеривация не подходит) ---
REM set PHOENIX_DIST_PC1_HOST=192.168.1.10
REM set PHOENIX_DIST_ROLLOUT_PORT=5562
REM set PHOENIX_DIST_AUTH_TOKEN=
REM set PHOENIX_DIST_PC2_NUM_WORKERS=8
REM
REM Сколько ждать train-context от ПК1 при старте (сек):
set PHOENIX_DIST_WAIT_CONTEXT_SEC=120
REM Self-play (1 — если ПК1 учит с оппонентом-снапшотом/пулом):
set SELF_PLAY_ENABLED=0
