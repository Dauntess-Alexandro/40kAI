# Inference Server для AlphaZero Tree — дизайн (реализация)

**Статус:** реализовано (Phase 0–3). GUI-панель — отложена (env-var путь работает).
**Полный план/обоснование:** [`plans/az-tree-inference-server.md`](../plans/az-tree-inference-server.md).

## Суть

Net-only offload: дерево PUCT + env-rollout'ы остаются на CPU-воркере; на GPU
inference server уходят только `net.infer` (root/intermediate) и батч leaf-eval.
Сервер **stateless** (нет per-env tree, в отличие от GMZ) — проще и батчит запросы
между воркерами/потоками.

> Важно: при AZ tree GPU не bottleneck (узкое место — CPU env-rollout'ы), поэтому
> выигрыш скромнее, чем у GMZ. Для LAN критичен `mcts_max_depth=1` (иначе round-trip
> шторм на intermediate-evals — см. план §5.4).

## Компоненты

| Файл | Роль |
|------|------|
| `core/models/az_inference_protocol.py` | msgpack+numpy, `AZ_PROTOCOL_VERSION=1`, унифицированный `infer` (obs `[B, obs_dim]`) |
| `core/models/az_inference_transport.py` | `LocalAZInferenceTransport` (mp.Queue) / `RemoteAZInferenceTransport` (ZMQ DEALER :5555) + `az_remote_health_check` |
| `core/models/az_inference_server.py` | `AZInferenceEngine` (batched `net.infer` + server-side EvalCache + weight polling), `AZInferenceServer` (батч-коллектор), `az_inference_server_entry` (spawn) |
| `core/models/az_inference_client.py` | `Evaluator` protocol, `LocalNetEvaluator`, `RemoteEvaluator` (thread-safe Lock + request_id) |
| `core/models/alphazero_mcts.py` | `AlphaZeroFactorizedMCTS(evaluator=...)` — инъекция; `evaluator=None` = текущее поведение |
| `tools/az_remote_inference_server.py` | standalone ZMQ ROUTER для ПК2 (LAN) |
| `train.py` | константы `AZ_INFERENCE_*`, `_az_env_worker_entry`, dispatch в `_main_actor_learner_alphazero` |

## Конфигурация (env / hyperparams `alphazero_tree`)

| Ключ | Env | Default | Описание |
|------|-----|---------|----------|
| `inference_server_enabled` | `AZ_INFERENCE_SERVER` | 0 | 1 = вариант B |
| `inference_server_mode` | `AZ_INFERENCE_SERVER_MODE` | `local` | `local` / `remote` |
| `num_env_workers` | `AZ_NUM_ENV_WORKERS` | =num_actors | CPU воркеры |
| `inference_batch_size` | `AZ_INFERENCE_BATCH_SIZE` | 32 | max батч |
| `inference_batch_interval_ms` | `AZ_INFERENCE_BATCH_INTERVAL_MS` | 10 | окно сбора |
| `inference_timeout` | `AZ_INFERENCE_TIMEOUT` | 5.0 | таймаут ответа |
| — | `AZ_INFERENCE_REMOTE_HOST/PORT` | `127.0.0.1`/`5555` | ПК2 |

**Fallback:** `inference_server_enabled=1` + нет CUDA → лог `[AZ][CONFIG][FALLBACK]`, откат на вариант A (CPU акторы).

## Локальный запуск (один ПК)

```bat
set TRAIN_ALGO=alphazero_tree
set AZ_INFERENCE_SERVER=1
set AZ_INFERENCE_SERVER_MODE=local
set AZ_NUM_ENV_WORKERS=8
REM рекомендуется для меньших round-trip:
set AZ_MCTS_MAX_DEPTH=1
python train.py ...
```

Или в `hyperparams.json` → `alphazero_tree`: `"inference_server_enabled": 1`.

## Маркеры логов

`[AZ][INF_SERVER]` (local server), `[AZ][ENV_WORKER]` (воркеры),
`[AZ][REMOTE_IS]` (ПК2), `[AZ][REMOTE_CLIENT]` (воркеры в remote-режиме),
`[AZ][CONFIG][FALLBACK]`.

## Тесты

- `tests/engine/test_az_inference_protocol.py` — encode/decode (16).
- `tests/engine/test_az_evaluator_parity.py` — Local evaluator vs net.infer + evaluator=None invariant (6).
- `tests/engine/test_az_inference_server.py` — engine batch + cache (7).
- `tests/engine/test_az_remote_server.py` — localhost ZMQ integration (4).
- `tests/engine/test_alphazero_mcts_tree_basic.py` — без регрессии (5).
