# PHOENIX Distributed Actors на ПК2

PHOENIX Wave 2 использует Ape-X style сбор опыта: learner/GPU остаётся на ПК1, а ПК2 запускает CPU-акторов и шлёт `phoenix_batch` sequence windows в общий replay.

## ПК1

1. Открой Qt GUI.
2. В настройках тренировки выбери `PHOENIX`.
3. Во вкладке PHOENIX выставь:
   - `num_actors` — локальные акторы ПК1,
   - `Distributed actors (ПК2)` — включить,
   - порт по умолчанию `5562`,
   - `Воркеров на ПК2` — обычно 6-12 по CPU.
4. Запусти train. GUI/лог должны показать `[PHOENIX][DIST] receiver bind=:5562` и запись `phoenix_dist_train_context.json`.

## ПК2

1. Убедись, что репозиторий и зависимости установлены.
2. Проверь `runtime/state/pc2_phoenix_actors_config.bat`.
   Если файла нет, `tools\pc2_phoenix_actors.bat` создаст его из `.example`.
3. Укажи `40KAI_SHARE_ROOT` на SMB-папку ПК1 (`artifacts\models` или `actor_sync`).
4. Запусти:

```bat
tools\pc2_phoenix_actors.bat
```

ПК2 прочитает `phoenix_dist_train_context.json`, `latest_phoenix_policy.pth`, подключится к ПК1 и начнёт отправлять `phoenix_batch`.

## Логи

- ПК1: `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`
  - `[PHOENIX][DIST][RECEIVER] hello worker=...`
  - `[PHOENIX][DIST] stop_requested`
  - `[PHOENIX][DIST] drain_done`
- ПК2: консоль `pc2_phoenix_actors.bat`
  - `[PHOENIX][DIST][PC2] автоконфиг`
  - `[PHOENIX][DIST][SINK] closed ... sent_batch=...`

## Частые проблемы

- `env_contract_hash mismatch`: ростер/миссия/архитектура сети на ПК2 не совпали с контекстом ПК1. Перезапусти train на ПК1 и затем ПК2-actors.
- `ПК2 не подключился`: проверь порт `5562`, firewall и `PHOENIX_DIST_PC1_HOST`.
- `ep без batch` или `sent_batch=0`: проверь, что ПК2 читает свежий `latest_phoenix_policy.pth` и не использует старый код.

Rollback: выключи `distributed_actors_enabled` и поставь `num_actors=1`; PHOENIX вернётся к Wave 1 single-process пути.
