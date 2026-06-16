# Inference Server для Gumbel AlphaZero (GAZ) — дизайн (реализация)

**Статус:** реализовано (тонкий слой на общей AZ-инфраструктуре).
**Полный дизайн/обоснование:** [`docs/superpowers/specs/2026-06-16-gaz-inference-and-distributed-design.md`](superpowers/specs/2026-06-16-gaz-inference-and-distributed-design.md).
**Планы:** [`plans/gaz-inference-server.md`](../plans/gaz-inference-server.md), [`plans/gaz-distributed-selfplay.md`](../plans/gaz-distributed-selfplay.md).

## Суть

GAZ (`TRAIN_ALGO=gumbel_az`) использует **ту же сеть** `AlphaZeroPolicyValueNet` и **тот же**
actor-learner (`_main_actor_learner_alphazero`, `_az_env_worker_entry`, `_build_az_search`), что и
AlphaZero tree. Поэтому Inference Server **не дублируется** — переиспользуется AZ:
`az_inference_{server,client,transport,protocol}.py`, `tools/az_remote_inference_server.py`.

Net-only offload: SH-поиск `GumbelAlphaZeroSearch` + env-rollout остаются на CPU-воркере; на GPU-сервер
уходит только `net.infer`:
- `evaluate_one(obs, masks)` → priors+value (root + per-head base), B=1;
- `evaluate_batch(leaves)` → values (**батч листовых оценок**, специфика GAZ), B=N.

Шов уже встроен в `GumbelAlphaZeroSearch._evaluate_net`/`_evaluate_value_batch`
(`core/models/gumbel_alphazero_search.py`) и `RemoteEvaluator` в `_az_env_worker_entry`.

> **Специфика GAZ:** leaf-eval БАТЧИНГ (`batch_eval_size`, дефолт 16). batch-ceiling: серверный
> `inference_batch_size` (дефолт 32) ≥ пачки воркера. RNG (`np.random.gumbel`/`choice`) живёт на
> воркере — offload его не трогает, детерминизм при сиде сохраняется.

## Отличия от AZ (что своё у GAZ)

| | AZ tree | GAZ |
|---|---|---|
| Порт IS / distributed | 5555 / 5557 | **5565 / 5567** |
| Веса (SMB) | `latest_az_tree_policy.pth` | `latest_az_gumbel_az_policy.pth` |
| search_cfg | `az_remote_search_cfg.json` | `gaz_remote_search_cfg.json` |
| env-флаги | `AZ_INFERENCE_*` | **`GAZ_INFERENCE_*`** (приоритет `GAZ_* → AZ_* → секция gumbel_az`) |
| Лог-тег | `[AZ]` | **`[GAZ]`** (`--algo-label GAZ` на сервере) |
| GUI-панель | AlphaZero Tree | **Gumbel AlphaZero** (`GazInferenceServerPanel.qml`) |
| ПК2-лаунчер | `pc2_remote_az_is.bat` | `pc2_remote_gaz_is.bat` (роль `gaz_inference`) |

## Конфигурация (env / hyperparams `gumbel_az`)

| Ключ (`gumbel_az`) | Env (GAZ) | Default | Описание |
|---|---|---|---|
| `inference_server_enabled` | `GAZ_INFERENCE_SERVER` | 0 | 1 = вариант B |
| `inference_server_mode` | `GAZ_INFERENCE_SERVER_MODE` | `local` | `local` / `remote` |
| `inference_remote_host` | `GAZ_INFERENCE_REMOTE_HOST` | `127.0.0.1` | ПК2 |
| `inference_remote_port` | `GAZ_INFERENCE_REMOTE_PORT` | **5565** | ПК2 |
| `inference_remote_auth_token` | `GAZ_INFERENCE_REMOTE_AUTH_TOKEN` | `""` | LAN-секрет |
| `distributed_actors_enabled` | `GAZ_DISTRIBUTED_ACTORS` | 0 | distributed self-play |
| `distributed_actors_port` | `GAZ_DIST_ROLLOUT_PORT` | **5567** | rollout PULL на ПК1 |

> `GAZ_*` env имеет приоритет над `AZ_*`; при отсутствии обоих — берётся секция `gumbel_az`.
> Для не-GAZ алго `GAZ_*` игнорируется (AZ без изменений). Резолвер — `core/models/az_family_env.py`.

**Fallback:** `inference_server_enabled=1` + нет CUDA (local) → лог `[GAZ][CONFIG][FALLBACK]`, откат на CPU-акторов.

## Локальный запуск (один ПК)

```bat
set TRAIN_ALGO=gumbel_az
set GAZ_INFERENCE_SERVER=1
set GAZ_INFERENCE_SERVER_MODE=local
set AZ_NUM_ENV_WORKERS=8
python train.py ...
```

Или в GUI: вкладка **Gumbel AlphaZero → Inference Server → Local**. Или `hyperparams.json → gumbel_az`: `"inference_server_enabled": 1`.

## Маркеры логов

`[GAZ][INF_SERVER]` (local server), `[GAZ][ENV_WORKER]`, `[GAZ][REMOTE_IS]` (ПК2),
`[GAZ][REMOTE_CLIENT]`, `[GAZ][DIST]`, `[GAZ][DIST][RECEIVER]`, `[GAZ][DIST][SINK]`, `[GAZ][CONFIG][FALLBACK]`.

## Тесты

- `tests/engine/test_gaz_inference_config.py` — резолвер `GAZ_* → AZ_* → default`.
- `tests/test_gaz_remote_search_cfg_builder.py` — GAZ search_cfg builder + GAZ-spec в реестре.
- `tests/engine/test_gaz_dist_payload.py` — паковка GAZ-полей + worker-payload + stop-flag.
- `tests/gui_qt/test_remote_is_gaz_store.py` — `remote_is_gaz.json` / QSettings-префикс.
- `tests/gui/test_pc2_roles_gaz.py` — роли ПК2-лаунчера (порты 5565/5567).
