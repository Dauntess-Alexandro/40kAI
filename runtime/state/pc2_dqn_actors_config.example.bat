@echo off
REM === Конфиг ПК2 для DQN distributed actors ===
REM IP ПК1 (learner) — куда слать переходы:
set DQN_DIST_PC1_HOST=192.168.1.10
REM Порт rollout (должен совпадать с ПК1, по умолчанию 5558):
set DQN_DIST_ROLLOUT_PORT=5558
REM Общий секрет (должен совпадать с ПК1; пусто = без auth):
set DQN_DIST_AUTH_TOKEN=
REM Число актор-процессов на ПК2 (по числу ядер CPU, напр. 6 для Ryzen 1600):
set DQN_DIST_PC2_NUM_WORKERS=6
REM SMB-шара ПК1 с моделью (actor_sync лежит здесь): \\PC1\40kai_models
set MODELS_DIR=\\PC1\40kai_models
REM Сколько ждать train-context от ПК1 (сек):
set DQN_DIST_WAIT_CONTEXT_SEC=120
REM Self-play (1 — если ПК1 учит с оппонентом-снапшотом):
set SELF_PLAY_ENABLED=0
