# План: Inference Server для Gumbel AlphaZero (GAZ) — local + LAN

**Статус:** черновик (код не написан).
**Подход:** тонкий слой на общей AZ-инфраструктуре (см. `docs/superpowers/specs/2026-06-16-gaz-inference-and-distributed-design.md`).
**Scope:** `TRAIN_ALGO=gumbel_az`. Дефолт — ВЫКЛ; прежний CPU-путь без регрессий.
**Родственные:** `plans/az-tree-inference-server.md` (переиспользуем движок/протокол/транспорт/SMB-sync), `plans/gaz-distributed-selfplay.md`.

> Все имена сверены с кодом на `main`. GAZ уже едет на `_main_actor_learner_alphazero`/`_az_env_worker_entry`/`_build_az_search` и на той же сети `AlphaZeroPolicyValueNet` → IS-сервер (`net.infer`) не дублируем.

---

## 1. Суть

Net-only offload (как у AZ): SH-поиск `GumbelAlphaZeroSearch` + env-rollout остаются на CPU-воркере; на GPU-сервер уходит только `net.infer`:
- `evaluate_one(obs, masks)` → priors+value (root + per-head base) — B=1;
- `evaluate_batch(leaves)` → values (батч листьев) — B=N, `want_priors=False`.

Это уже реализовано через `evaluator`-шов в `GumbelAlphaZeroSearch._evaluate_net`/`_evaluate_value_batch` (`gumbel_alphazero_search.py:77-118`) и `RemoteEvaluator` в `_az_env_worker_entry` (`train.py:8943`). Сервер — общий `az_inference_server.py`/`tools/az_remote_inference_server.py` (stateless, алго-агностичен).

**Специфика GAZ (учесть, не сломать):** leaf-eval БАТЧИНГ (`batch_eval_size`, дефолт 16); batch-ceiling: серверный `inference_batch_size`≥пачки; RNG (`np.random.gumbel`/`choice`) — на воркере, offload не трогает.

## 2. Что чиним (разрывы из спеки §2)

1. Порты: `gumbel_az.inference_remote_port=5565`.
2. env-флаги `GAZ_*` (приоритет `GAZ_* → AZ_* → gumbel_az`).
3. Веса remote: GAZ-spec/builder с `latest_az_gumbel_az_policy.pth` + `gaz_remote_search_cfg.json`.
4. Лог-теги `[GAZ][...]`.
5. GUI-панель + `remote_is_gaz.json`.
6. ПК2-лаунчер `pc2_remote_gaz_is.bat` + роль `gaz_inference`.

## 3. Фазы (каждая: тест → код → прогон, дефолт ВЫКЛ)

### Phase 1 — env-резолв + порты (config-only код)
- `train.py`: при `is_gumbel_az_algo` резолвить `AZ_INFERENCE_SERVER_*`/`AZ_INFERENCE_REMOTE_*` с приоритетом `GAZ_* env → AZ_* env → AZ_CFG`. Хелпер `_gaz_or_az_env(gaz_key, az_key, cfg_key, default)`.
- `hyperparams.json` → `gumbel_az`: `inference_remote_port: 5565`.
- **Тест** `tests/engine/test_gaz_inference_config.py`: монкейпатч env — `GAZ_INFERENCE_SERVER=1` включает; порт по умолчанию 5565; `GAZ_*` бьёт `AZ_*`; при `gumbel_az`-секции без env берётся 5565. (Импортировать резолвер-хелпер, не весь train.)
- **Готово:** тест зелёный; запуск GAZ с `GAZ_INFERENCE_SERVER=1 GAZ_INFERENCE_SERVER_MODE=local` поднимает local IS (лог `[GAZ][INF_SERVER]`).

### Phase 2 — GAZ search_cfg/веса для remote (см. §4 спеки, разрыв #3)
- `core/models/gaz_remote_search_cfg_builder.py`: тонкий по образцу `az_remote_search_cfg_builder.py`, но `WEIGHTS_NAME="latest_az_gumbel_az_policy.pth"`, `SEARCH_CFG_NAME="gaz_remote_search_cfg.json"`, читает секцию `gumbel_az`; net-арх — те же поля (`hidden_size`/`num_layers`/`value_ensemble`). Переиспользует `remote_is_search_cfg_common` + `write_az_remote_search_cfg` (форма сети одна).
- `core/models/remote_is_search_cfg_registry.py`: `_spec_gaz()` (`algo_id="gaz"`, label `GAZ`, role `gaz_inference`, env `GAZ_REMOTE_SEARCH_CONFIG`/`GAZ_REMOTE_WEIGHTS_PATH`) в `REMOTE_IS_SEARCH_CFG_SPECS`.
- **Тест** `tests/engine/test_gaz_remote_search_cfg.py`: spec резолвится по роли; `ensure/publish` пишет cfg с правильными именами; `prepare_inference_launch("gaz_inference", share)` отдаёт env-пары с GAZ-весами.
- **Готово:** тесты зелёные; `publish_all_remote_search_cfgs_from_repo` включает `gaz`.

### Phase 3 — auto-write search_cfg на ПК1 + standalone-сервер `--algo-label`
- `train.py` (`_main_actor_learner_alphazero`, ветка dist/IS): при `is_gumbel_az_algo` авто-писать GAZ search_cfg (через builder Phase 2), а не AZ (сейчас `write_az_remote_search_cfg`, `:9463` — для GAZ те же дим., но имя файла должно быть GAZ; иначе ПК2 не найдёт по `GAZ_REMOTE_SEARCH_CONFIG`).
- `tools/az_remote_inference_server.py`: arg `--algo-label` (default `AZ`) → лог `[<LABEL>][REMOTE_IS]`. weights/cfg уже из аргументов/env.
- **Тест:** smoke — сервер логирует `[GAZ][REMOTE_IS] listening` при `--algo-label GAZ`.

### Phase 4 — лог-теги в общем коде
- Провести `_AZ_LOG_TAG` в лог-строки `_az_env_worker_entry` (`[AZ][ENV_WORKER]`→`[<TAG>][ENV_WORKER]`), local IS spawn (`[AZ][INF_SERVER]`), remote client (`[AZ][REMOTE_CLIENT]`). Для AZ тег=`AZ` (ноль изменений).
- **Готово:** при GAZ-train в `LOGS_FOR_AGENTS_TRAIN.md` маркеры `[GAZ][ENV_WORKER]`/`[GAZ][INF_SERVER]`.

### Phase 5 — GUI (вкладка GAZ)
- `app/gui_qt/qml/components/GazInferenceServerPanel.qml` (копия `AzInferenceServerPanel.qml`, тексты GAZ, порт 5565).
- `app/gui_qt/remote_is_store.py`: добавить параметр `qsettings_prefix="remote_is"` в `apply_*`/`load_*_from_qsettings` → для GAZ `remote_is_gaz`. Файл `remote_is_gaz.json` (через `filename`).
- `app/gui_qt/main.py` + `qml/Main.qml`: загрузка/сохранение `remote_is_gaz.json`, прокидка `GAZ_INFERENCE_*` env в `_start_training` (ветка `gumbel_az`), кнопка «Проверить соединение» (`az_remote_health_check` на GAZ host/port).
- `.gitignore`: `runtime/state/remote_is_gaz.json`.
- **Тест** `tests/gui_qt/test_remote_is_gaz_store.py`: `remote_is_gaz.json` round-trip; QSettings-префикс не пересекается с AZ.

### Phase 6 — ПК2-лаунчер
- `tools/pc2_remote_gaz_is.bat` + `runtime/state/pc2_remote_gaz_is_config.example.bat`: порт 5565, GAZ-веса; зовёт `az_remote_inference_server.py --algo-label GAZ`.
- `app/gui_qt/pc2_launcher_backend.py`: роль `gaz_inference` (script `tools/pc2_remote_gaz_is.bat`, port 5565, requires_gpu).
- **Тест** `tests/gui_qt/test_pc2_launcher_roles.py` (или расширить): роль `gaz_inference` резолвится, порт 5565.

## 4. Тестовая стратегия
Unit (резолвер env, реестр, builder), GUI-store, роли лаунчера. Регрессия: AZ не задет; `GAZ_INFERENCE_SERVER=0` → CPU-путь. Smoke (ручной, GUI): local IS на 1 ПК; LAN — health_check + train.

## 5. Риски
| Риск | Митигация |
|---|---|
| Алго-гейт `is_az_algo`-онли режет GAZ | grep-проверка; общий код пускает оба |
| Порт-конфликт AZ/GAZ на ПК2 | GAZ=5565 дефолтом |
| guard_paths блокирует pc2-конфиг | вносим `*.example.bat`, рабочий — через GUI/вручную |
| Имя весов remote (AZ vs GAZ) | GAZ-spec `latest_az_gumbel_az_policy.pth` + auto-write GAZ cfg на ПК1 |
| Rollback | `GAZ_INFERENCE_SERVER=0` → прежний путь |
