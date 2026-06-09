@echo off
REM === Конфиг ПК2 для DQN distributed actors ===
REM
REM ОБЯЗАТЕЛЬНО задать только одно — общую SMB-папку ПК1 (где лежит artifacts/models):
REM «if not defined» — чтобы значение из окна-лаунчера (pc2_launcher.bat) НЕ затиралось.
if not defined 40KAI_SHARE_ROOT set "40KAI_SHARE_ROOT=\\192.168.0.100\actor_sync"
REM (Можно указать и прямо на ...\actor_sync — корень models определится сам.)
REM
REM Совместимость: старая MODELS_DIR тоже понимается (если 40KAI_SHARE_ROOT пуст):
REM set MODELS_DIR=\\192.168.1.10\40kai_models
REM
REM Остальное выводится автоматически:
REM   - IP ПК1    из UNC-пути шары (\\192.168.1.10\... -^> 192.168.1.10)
REM   - порт+auth из dqn_dist_train_context.json (ПК1 пишет при старте)
REM   - воркеры   из числа ядер CPU
REM
REM --- Переопределения (раскомментируй, если автодеривация не подходит) ---
REM set DQN_DIST_PC1_HOST=192.168.1.10
REM set DQN_DIST_ROLLOUT_PORT=5558
REM set DQN_DIST_AUTH_TOKEN=
REM set DQN_DIST_PC2_NUM_WORKERS=6
REM
REM Сколько ждать train-context от ПК1 при старте (сек):
set DQN_DIST_WAIT_CONTEXT_SEC=120
REM Self-play (1 — если ПК1 учит с оппонентом-снапшотом):
set SELF_PLAY_ENABLED=0
