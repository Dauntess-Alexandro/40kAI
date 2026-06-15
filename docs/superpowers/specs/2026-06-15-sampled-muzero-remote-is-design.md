# Sampled MuZero — Remote Inference Server (Design Spec)

**Дата:** 2026-06-15
**Статус:** утверждён пользователем (брейншторм), готов к написанию плана реализации.
**Автор:** AI-агент + ревью пользователя.

## Цель

Дать модели `sampled_muzero` (реализована, влита в main) **inference-server** как у `gumbel_muzero`:
вариант B (env-воркеры + централизованный GPU-сервер поиска), режимы **local** (одна машина) и
**remote** (сервер на ПК2). Полный паритет с gmz: движок + GUI-панель «Inference Server» во вкладке
Sampled MuZero + ПК2-обвязка (bat/launcher/конфиг) + дока. **По умолчанию ВЫКЛ** (вариант A —
прямые акторы — остаётся дефолтом).

Distributed self-play (rollout-акторы ПК2 → learner ПК1, как у AZ/DQN) — **НЕ в этом цикле** (отдельный
подпроект позже).

## Контекст и решения брейншторма

1. **Объём:** только Remote IS (distributed отложен). Полный паритет с gmz (движок + GUI + ПК2 + дока).
2. **Дефолт — выкл:** `inference_server_enabled=0`; вариант A (акторы крутят sampled-поиск сами) — текущий путь.
3. **Переиспользование (ключевое):** gmz remote-IS оффлоадит **весь поиск целиком** (клиент шлёт obs+masks →
   сервер возвращает selected_actions/policy_targets/behavior_logits/value). Протокол/транспорт/клиент и
   env-воркер **search-agnostic** → переиспользуются импортом. Уникален только **сервер** (класс поиска).

## Что уникально, что переиспользуем

**Новое:**
- `core/models/smz_inference_server.py` — `SMZInferenceServer` + `smz_inference_server_entry`. Зеркало
  `gmz_inference_server.py`: грузит `SampledMuZeroNet`, гоняет `BatchedSampledMuZeroSearch.run_batched_stateful`
  на GPU, синкает веса из `sync_path`. Конфиг поиска — `SampledMuZeroSearchConfig` (num_samples,
  sample_temperature, temperature, prior_weight, dedup, discount) — НЕ gmz-поля (num_simulations/root_top_k/
  gumbel_scale отсутствуют в этом конфиге).
- `tools/smz_remote_inference_server.py` — ПК2 standalone (зеркало `tools/gmz_remote_inference_server.py`).
- `tools/pc2_remote_smz_is.bat` + `runtime/state/pc2_remote_smz_is_config.bat` (зеркало gmz; `.bat`-конфиг
  с секретами — править вручную/через GUI, не агентом; в `.gitignore` если так у gmz).
- `docs/remote-inference-server-smz.md` + `docs/pc2-remote-smz-is-setup-guide.md` (зеркало gmz-доки).

**Переиспользуем (импорт, без копий):**
- `core/models/gmz_inference_protocol.py` (msgpack/numpy wire, build_infer_request, health_check) — search-agnostic.
- `core/models/gmz_inference_transport.py` (Local/TCP transport) — search-agnostic.
- `core/models/gmz_inference_client.py::GMZInferenceClient` — search-agnostic (obs→actions).
- `train.py::_gmz_env_worker_entry` — search-agnostic (зовёт `client.infer`, строит `GMZTransition` через
  `play_episode_with_gumbel_muzero(inference_fn=...)`; sampled selfplay — тонкая обёртка над ним).
- `GMZTransition`, sync-файл механизм, `normalize_state_dict`.

> Решение: НЕ плодить `smz_inference_{protocol,transport,client}.py` — они были бы побайтовой копией.
> Если позже понадобится sampled-специфика на проводе — выделим тогда (YAGNI).

## Секция 1 — Сервер `SMZInferenceServer`

`core/models/smz_inference_server.py` — структурная копия gmz-сервера с заменами:
- `GumbelMuZeroNet` → `SampledMuZeroNet` (та же арх; грузим через sampled-фабрику ради паритета модели).
- `BatchedGumbelMuZeroSearch` → `BatchedSampledMuZeroSearch`.
- `GumbelMuZeroSearchConfig(...)` → `SampledMuZeroSearchConfig(num_samples, sample_temperature, temperature,
  prior_weight, dedup, discount)`.
- `search_cfg_payload` поля: `num_samples` (вместо num_simulations/root_top_k/gumbel_scale), `sample_temperature`,
  `temperature`, `prior_weight`, `dedup`, `discount`, + сетевые (latent/hidden/num_layers/action_embed/obs_dim/action_sizes).
- Логи `[GMZ][INF_SERVER]` → `[SMZ][INF_SERVER]`.
- torch.compile / triton-guard / weight-poll / батч-цикл / форма ответа (`infer_response`: env_id,
  selected_actions, policy_targets, behavior_logits, value_est, policy_version) — идентичны (это и есть
  контракт, который ждёт `GMZInferenceClient`/env-воркер).
- `deterministic=False` на self-play (как gmz).

## Секция 2 — Конфиг `SMZ_INFERENCE_*` в train.py

Зеркало блока `GMZ_INFERENCE_*` (train.py:3060–3119):
- `SMZ_ACTOR_DEVICE` — добавить допустимое значение `"inference_server"` (сейчас только cpu/cuda).
- `SMZ_INFERENCE_SERVER_MODE` (local|remote), `SMZ_INFERENCE_REMOTE` = mode==remote.
- `SMZ_INFERENCE_REMOTE_HOST/PORT/AUTH_TOKEN` (порт по умолчанию — НЕ 5555, чтобы не конфликтовать с gmz/az
  на одном ПК2; выбрать свободный, напр. **5560**; зафиксировать в плане).
- `SMZ_INFERENCE_SERVER_REQUESTED/ENABLED/LOCAL/USING_FALLBACK` (fallback: запрошен, но нет CUDA и не remote
  → вариант A, с WARN `[SMZ][CONFIG][FALLBACK]`).
- `SMZ_INFERENCE_SERVER_COMPILE`, `SMZ_INFERENCE_BATCH_SIZE`, `SMZ_INFERENCE_BATCH_INTERVAL_MS`,
  `SMZ_INFERENCE_REQUEST_QUEUE_MAX`, `SMZ_NUM_ENV_WORKERS`, `SMZ_INFERENCE_TIMEOUT`.
- При `ENABLED`: `SMZ_ACTOR_DEVICE="inference_server"`, `SMZ_ACTOR_EFFECTIVE_NUM_ACTORS = SMZ_NUM_ENV_WORKERS`.

## Секция 3 — Провод в `_main_actor_learner_sampled_muzero`

В sampled actor-learner уже скопирован inference-server каркас, но с gmz-«хвостом» (ссылки
`GMZ_INFERENCE_SERVER_ENABLED`, `gmz_inference_server_entry`, `[GMZ][CONFIG]`). Перенаправить:
- `GMZ_INFERENCE_*` → `SMZ_INFERENCE_*`.
- `gmz_inference_server_entry` → `smz_inference_server_entry`, `search_cfg_payload` → sampled-поля.
- env-воркеры: реюз `_gmz_env_worker_entry` (search-agnostic) + `GMZInferenceClient` — менять не нужно;
  они дергают сервер, а sampled selfplay-петля внутри идентична gmz.
- Логи `[GMZ][CONFIG]`/режимные строки → `[SMZ][CONFIG]`.
- Remote: при `SMZ_INFERENCE_REMOTE` сервер НЕ спавнится локально; воркеры коннектятся к
  `SMZ_INFERENCE_REMOTE_HOST:PORT` через TCP-транспорт (как gmz).

## Секция 4 — ПК2-обвязка

- `tools/smz_remote_inference_server.py` — поднимает `smz_inference_server_entry` на ПК2 (зеркало gmz):
  слушает TCP-порт, грузит начальные веса, пишет лог `LOGS_FOR_AGENTS_REMOTE_IS.md` (тот же файл; маркер `[SMZ]`).
- `tools/pc2_remote_smz_is.bat` + `runtime/state/pc2_remote_smz_is_config.bat` — кнопка/конфиг ПК2 (зеркало
  `pc2_remote_is.bat`). Порт по умолчанию = `SMZ_INFERENCE_REMOTE_PORT`.
- Конфиг ПК1 (GUI): `runtime/state/remote_is_smz.json` (host/port/auth/mode) — отдельно от gmz `remote_is.json`,
  чтобы можно было держать оба. В `.gitignore`.

## Секция 5 — GUI (вкладка Sampled MuZero)

Зеркало gmz-панели «Inference Server»:
- `hyperparams.json → sampled_muzero`: `inference_server_enabled:0`, `inference_server_mode:"local"`,
  `inference_server_compile:1`, `inference_batch_size`, `inference_batch_interval_ms`,
  `inference_request_queue_max`, `inference_timeout`, `num_env_workers`, `actor_device:"cuda"`.
- `app/gui_qt/sampled_muzero_hyperparams_defaults.py` — добавить эти ключи (+ тултипы RU) в подходящую группу.
- `app/gui_qt/main.py`: при train-launch экспортировать `SMZ_INFERENCE_*` env из hpSmz-полей (зеркало того,
  как gmz экспортит `GMZ_INFERENCE_*`); панель/поля remote (host/port/auth) — через `remote_is_smz.json`,
  как gmz читает `remote_is.json`.
- QML (`SectionHyperparamsEditor.qml` / панель IS): поля inference-server в группе; целочисленные
  (batch_size/queue_max/num_env_workers/compile/enabled) — через `isIntKey`.

## Секция 6 — Тесты

1. `tests/engine/test_smz_inference_server.py`:
   - `build_batch_responses` на батче из N obs/masks → N ответов; для каждого: `selected_actions` легальны,
     `policy_targets` суммы=1 и формы по головам, `behavior_logits` присутствуют, `value_est` float, `kind=="infer_response"`.
   - **Эквивалентность поиску:** ответ сервера численно совпадает с прямым `BatchedSampledMuZeroSearch.run_batched`
     при том же seed/весах (сервер не искажает поиск).
   - Сервер использует именно `BatchedSampledMuZeroSearch` (анти-регрессия «забытого зеркала» — не gmz-поиск).
2. Реюз: gmz protocol/transport тесты уже покрывают провод — не дублируем.
3. Регресс: gmz inference-тесты и вся sampled-сюита зелёные (мы их не трогаем; только импортируем).

## Секция 7 — Риски

- **«Забытое зеркало»** (тот же класс багов, что в фазе 1): variant-B sampled не должен дергать gmz-сервер/конфиг.
  Покрыто тестом сервера (проверяем класс поиска) + перенаправлением всех `GMZ_INFERENCE_*`→`SMZ_*` в sampled-ветке.
- **Порт-конфликт на ПК2**: gmz/az используют 5555. Sampled IS — свой порт (5560), задокументировать «не
  запускать конфликтующие серверы на одном ПК2 на одном порту».
- **Веса**: sampled-сеть = gmz-арх; сервер грузит через sampled-фабрику — совместимо, но грузить именно
  `sampled_muzero_net` из чекпойнта / sync-файла.
- **torch.compile/triton** на Windows обычно недоступен — graceful skip (как gmz).
- **Секреты** (`.bat`-конфиг, remote_is_smz.json): не коммитить, править вручную/GUI (guard_paths hook).

## Критерий готовности

- `SMZ_ACTOR_DEVICE=inference_server` / `inference_server_enabled=1` (hyperparams или GUI) поднимает
  variant-B-local: GPU-сервер sampled-поиска + env-воркеры, train идёт, чекпойнты пишутся.
- Remote: `tools/pc2_remote_smz_is.bat` на ПК2 + GUI ПК1 (remote_is_smz.json) → train с оффлоадом поиска на ПК2.
- GUI-вкладка Sampled MuZero показывает панель Inference Server, тумблер работает, дефолт выкл.
- `tests/engine/test_smz_inference_server.py` зелёный; gmz/sampled регресс не сломан.
- Логи `[SMZ][INF_SERVER]`/`[SMZ][CONFIG]` присутствуют.
