# Remote Inference Server (Gumbel AlphaZero, GAZ) — ПК1 + ПК2 (LAN)

Руководство по запуску GAZ inference-сервера на ПК2 и обучения на ПК1 через LAN.
GAZ переиспользует AZ-инфраструктуру (та же сеть), отличаются порт/веса/имена — см.
[`docs/inference-server-gaz-design.md`](inference-server-gaz-design.md). Пошагово на ПК2:
[`docs/pc2-remote-gaz-is-setup-guide.md`](pc2-remote-gaz-is-setup-guide.md).

## Кратко

- **Что выносится на ПК2:** только `net.infer` (GPU). Дерево SH + env-rollout остаются на ПК1.
- **Порт:** `5565` (AZ=5555, GMZ=5555, SMZ=5560 — не конфликтуют, можно вместе на одном ПК2).
- **Веса (SMB):** ПК1 пишет `artifacts/models/actor_sync/latest_az_gumbel_az_policy.pth`; ПК2 читает по SMB.
- **search_cfg (форма сети):** `gaz_remote_search_cfg.json` — пишется автоматически при старте train на ПК1
  (или через ensure на ПК2). Сеть та же, что у AZ tree.

## ПК1 (learner)

1. GUI: вкладка **Gumbel AlphaZero → Inference Server → LAN**, задать host (IP ПК2), порт 5565, при
   необходимости auth-token. Кнопка «Проверить соединение» зовёт `az_remote_health_check`.
   Конфиг GUI: `runtime/state/remote_is_gaz.json` (в `.gitignore`).
2. Либо вручную:
   ```bat
   set TRAIN_ALGO=gumbel_az
   set GAZ_INFERENCE_SERVER=1
   set GAZ_INFERENCE_SERVER_MODE=remote
   set GAZ_INFERENCE_REMOTE_HOST=192.168.0.101
   set GAZ_INFERENCE_REMOTE_PORT=5565
   python train.py ...
   ```
3. Перед стартом train делает health_check ПК2 (`[GAZ][REMOTE_CLIENT] health_check ok ...`). Если ПК2
   недоступен — train падает с RU-ошибкой (проверьте сервер/IP/порт/firewall TCP 5565).

## ПК2 (inference server)

Одной кнопкой: `tools\pc2_remote_gaz_is.bat` (конфиг: `runtime/state/pc2_remote_gaz_is_config.bat`,
шаблон — `*.example.bat`). Делает venv, firewall TCP 5565, ensure search_cfg, запуск сервера
`tools/az_remote_inference_server.py --algo-label GAZ` (лог `[GAZ][REMOTE_IS]`,
`runtime/logs/gaz_remote_is_*.log`).

## Distributed self-play (опционально, +CPU ПК2)

См. план [`plans/gaz-distributed-selfplay.md`](../plans/gaz-distributed-selfplay.md). Кратко:
- ПК1: `GAZ_DISTRIBUTED_ACTORS=1` (или GUI-тоггл) → learner поднимает `RolloutReceiver` (PULL **5567**),
  пишет контекст `az_dist_train_context.json` (с `train_algo=gumbel_az` и GAZ-параметрами поиска) и
  `gaz_remote_search_cfg.json` на SMB; по завершении — `gaz_dist_stop.flag`.
- ПК2: `pc2_remote_gaz_is.bat` при `GAZ_REMOTE_DIST_ACTORS_ENABLED=1` поднимает IS (:5565) **и**
  dist-акторов (`_az_env_worker_entry` → infer `127.0.0.1:5565`, rollout → IP ПК1:5567). Только акторы:
  `tools\pc2_gaz_actors.bat`.
- ПК2-воркеры строят `GumbelAlphaZeroSearch` по `train_algo` из контекста (GAZ-payload, не AZ MCTS).

## Маркеры логов

`[GAZ][REMOTE_IS]` (ПК2), `[GAZ][REMOTE_CLIENT]`/`[GAZ][REMOTE_CLIENT][CONN]` (воркеры ПК1),
`[GAZ][DIST]`, `[GAZ][DIST][RECEIVER]`, `[GAZ][DIST][SINK]`, `stale_drop remote=…%`.

## Частые проблемы

- **«Remote GAZ inference server недоступен»** — сервер на ПК2 не запущен / неверный IP-порт /
  firewall TCP 5565. host должен быть LAN-IP ПК2, не 127.0.0.1.
- **Веса не найдены на ПК2** — SMB не смонтирован (Z:) или ПК1 ещё не записал
  `latest_az_gumbel_az_policy.pth`. Для первого старта — `GAZ_REMOTE_INIT_WEIGHTS` в конфиге ПК2.
- **search_cfg не найден** — запустите train на ПК1 (пишет `gaz_remote_search_cfg.json` на SMB) или
  ensure на ПК2 (`pc2_remote_gaz_is.bat` делает это автоматически).
- **Порт-конфликт с AZ/GMZ** — у GAZ свой порт 5565; не запускайте два сервера на одном порту.
