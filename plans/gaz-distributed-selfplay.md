# План: Distributed self-play для Gumbel AlphaZero (GAZ) — PC1 learner + PC2 actors

**Статус:** черновик (код не написан).
**Подход:** тонкий слой на общей AZ-distributed-инфре (см. `docs/superpowers/specs/2026-06-16-gaz-inference-and-distributed-design.md`).
**Scope:** `TRAIN_ALGO=gumbel_az`. Learner на PC1, env-воркеры на PC1+PC2. Дефолт — ВЫКЛ.
**Родственные:** `plans/az-distributed-selfplay.md` (переиспускаем транспорт/sink/receiver/SMB-sync), `plans/gaz-inference-server.md`.

> Транспорт `az_rollout_{protocol,receiver,sink}.py` и `RolloutReceiver` — общие и работают для GAZ. Единственный реальный код-разрыв: на ПК2 не доезжают **GAZ-настройки поиска** (dist-контекст и `pc2_az_actors` пакуют AZ MCTS-параметры независимо от алго).

---

## 1. Суть и целевой профиль
Как у AZ: learner на PC1 поднимает `RolloutReceiver` (PULL, для GAZ :5567); PC2-воркеры `_az_env_worker_entry` + `RemoteSink` шлют rollout'ы; веса политики и `gaz_dist_stop.flag` — по SMB. Каналы независимы: IS (:5565) и rollout (:5567). Целевой деплой: IS LAN на PC2 (:5565) + dist-воркеры PC2 (infer → localhost :5565, rollout → PC1 :5567).

## 2. Реальный разрыв (что чиним)
**GAZ search-config не доезжает на ПК2.** Сейчас:
- PC1: `_dist_az_hp = pack_az_dist_hyperparams({**AZ_CFG, "mcts_simulations":..., ...})` (`train.py:9417`) пакует AZ MCTS-поля независимо от алго; контекст уже несёт `train_algo` (`:9456`).
- PC2: `pc2_az_actors._train_dist_defaults` (`tools/pc2_az_actors.py:89`) читает `AZ_MCTS_*`; `build_az_dist_worker_payloads` строит AZ MCTS-payload; `_build_az_search` для GAZ ждёт `num_simulations`/`num_considered_actions`/`joint_action` → их нет → откат на PC2-локальные дефолты (рассинхрон параметров поиска PC1↔PC2).

## 3. Фазы

### Phase 1 — algo-aware dist-контекст на ПК1
- `train.py` (`_main_actor_learner_alphazero`, блок `AZ_DISTRIBUTED_ACTORS`, `:9416-9459`): при `is_gumbel_az_algo` паковать GAZ-поля (`_gaz_cfg_payload()`-форма: `num_simulations`, `num_considered_actions`, `max_depth`, `value_scale`, `c_visit`, `simulate_enemy`, `joint_action`, `eval_cache_size`, `batch_eval_size`) вместо AZ MCTS. `train_algo=gumbel_az` уже пишется.
- auto-write GAZ search_cfg (см. `plans/gaz-inference-server.md` Phase 3).
- stop-flag: `gaz_dist_stop.flag` (по `_az_sync_tag`/algo), чтобы AZ и GAZ dist не глушили друг друга. Проверить `_touch/_clear/_az_dist_stop_flag` — параметризовать по алго или отдельное имя.
- **Тест** `tests/engine/test_gaz_dist_context.py`: при `gumbel_az` `pack/normalize` несут GAZ-поля; `train_algo=gumbel_az`.

### Phase 2 — GAZ-payload на ПК2
- `tools/pc2_az_actors.py`: если `train_algo` из контекста == `gumbel_az` → строить GAZ-payload (форма `_gaz_cfg_payload`) и прокидывать в `_az_env_worker_entry` (он через `_build_az_search` сделает `GumbelAlphaZeroSearch`). IS-порт по умолчанию 5565 (`GAZ_DIST_PC2_IS_PORT`), rollout 5567.
- Хелпер `build_gaz_dist_worker_payloads` (или ветка в существующем) в `az_rollout_sink.py`.
- **Тест** `tests/engine/test_gaz_dist_worker_payload.py`: из GAZ-контекста собирается payload с `num_simulations`/`joint_action`, не AZ MCTS.

### Phase 3 — ПК2-лаунчер + роль
- `tools/pc2_gaz_actors.bat` (+ конфиг `runtime/state/pc2_gaz_actors_config.example.bat`): `GAZ_*` env, IS 5565 / rollout 5567, `GAZ_REMOTE_DIST_ACTORS_ENABLED=1`; зовёт `pc2_az_actors.py` (общий).
- `tools/pc2_remote_gaz_is.bat`: опционально поднимать и dist-актора при `GAZ_REMOTE_DIST_ACTORS_ENABLED=1` (как `AZ_REMOTE_DIST_ACTORS_ENABLED` в `pc2_remote_az_is.bat`).
- `app/gui_qt/pc2_launcher_backend.py`: роль `gaz_actors` (script `tools/pc2_gaz_actors.bat`, port 5567).
- **Тест:** роль `gaz_actors` резолвится, порт 5567.

### Phase 4 — лог-теги dist + GUI-тоггл
- `[GAZ][DIST]`/`[GAZ][DIST][RECEIVER]`/`[GAZ][DIST][SINK]` через `_AZ_LOG_TAG`.
- GUI: тоггл «Distributed actors (PC2)» на вкладке GAZ (как у AZ), прокидка `GAZ_DISTRIBUTED_ACTORS`/порт.

## 4. Тесты
Unit: GAZ dist-контекст пакует GAZ-поля; PC2 payload-сборка. Регрессия: AZ dist не задет; `GAZ_DISTRIBUTED_ACTORS=0` → одиночный путь. Integration (localhost): PUSH→PULL→data_q (общий, уже покрыт для AZ — проверить, что GAZ-контракт проходит). Perf/LAN (ручной): ep/h PC1 vs PC1+PC2, `[GAZ][DIST] stale_drop remote=%`.

## 5. Риски
| Риск | Митигация |
|---|---|
| GAZ search-параметры не доезжают на PC2 | Phase 1+2 (algo-aware pack + PC2 payload) |
| stop-flag коллизия AZ/GAZ | отдельный `gaz_dist_stop.flag` |
| Staleness PC2 (SMB-лаг) | как у AZ: тюнинг `max_policy_staleness_updates`, мерить `stale_drop %` |
| Контракт/ростер PC2 | `env_contract_hash` в rollout (общий механизм) |
| Rollback | `GAZ_DISTRIBUTED_ACTORS=0` → одиночный путь |

## 6. Решено
- Транспорт/receiver/sink — общие AZ (не дублируем).
- PC2 dist: `_az_env_worker_entry` + infer localhost :5565 + RemoteSink → PC1 :5567.
- Порты GAZ: IS 5565 / rollout 5567.
