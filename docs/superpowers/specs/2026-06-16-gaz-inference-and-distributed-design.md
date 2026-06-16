# GAZ (Gumbel AlphaZero) — Inference Server + Distributed self-play — Design Spec

**Дата:** 2026-06-16
**Статус:** утверждён пользователем (брейншторм). Подход: **тонкий слой на общей AZ-инфраструктуре** (не дублируем рабочий AZ-код).
**Scope:** `TRAIN_ALGO=gumbel_az` (GAZ). Цель — чтобы у GAZ работали: Inference Server (local + LAN) и Distributed self-play (ПК1+ПК2), как у AlphaZero tree.

> Имена функций/файлов сверены с кодом на `main`. Где утверждается поведение — указан файл/строка.

---

## 1. Ключевой вывод (важно прочитать до плана)

GAZ **уже на ~90% едет на общей AZ-инфраструктуре** — это не пустой задел:

- Точка входа обучения **общая**: `_main_actor_learner_alphazero` вызывается и для `is_az_algo`, и для `is_gumbel_az_algo` (`train.py:4129, 4476, 9099`).
- Фабрика поиска `_build_az_search` диспетчит `gumbel_az → GumbelAlphaZeroSearch`, прочее → `AlphaZeroFactorizedMCTS` (`train.py:2950`). В неё уже прокидывается `evaluator` (`train.py:2967`).
- Воркер `_az_env_worker_entry` (общий) строит поиск через `_build_az_search(None, payload, cpu, evaluator=RemoteEvaluator)` (`train.py:8943`). У `GumbelAlphaZeroSearch` уже есть **evaluator-шов** в `_evaluate_net`/`_evaluate_value_batch` (`gumbel_alphazero_search.py:77-118`).
- Сеть для offload — **та же** `AlphaZeroPolicyValueNet`. Значит `net.infer` (единственное, что выносит IS-сервер) для GAZ и AZ **идентичен** → IS-сервер не дублируем.
- Гиперпараметры `gumbel_az.inference_*`/`distributed_*` — **живые**: `AZ_CFG = data.get(_AZ_HP_SECTION)` где для GAZ `_AZ_HP_SECTION="gumbel_az"` (`train.py:2564-2568`). Все `AZ_INFERENCE_*`/`AZ_DISTRIBUTED_*` константы читаются из секции `gumbel_az` (`train.py:2693-2745`).
- env-флаги `AZ_INFERENCE_SERVER`/`AZ_DISTRIBUTED_ACTORS` уже гейтят и GAZ-путь.

**Следствие:** «полный аналог AZ» = доделать несколько «проводов» + GAZ-фасад, а НЕ копировать `az_inference_*`/`az_rollout_*` (это была бы копия рабочего кода, та же сеть → ровно тот рассинхрон `az_*↔gmz_*`, против которого борется проект: CLAUDE.md, `code-reviewer`, `code-simplifier`).

---

## 2. Реальные разрывы (что чиним)

| # | Разрыв | Сейчас | Нужно |
|---|--------|--------|-------|
| 1 | **Порты** | `gumbel_az.inference_remote_port=5555`, `distributed_actors_port=5557` (как у AZ) | GAZ-дефолты **5565 / 5567** (config-only), чтобы AZ+GAZ IS жили на одном ПК2 |
| 2 | **env-флаги** | GAZ управляется только `AZ_*` env | добавить `GAZ_*` env с приоритетом `GAZ_* → AZ_* → секция gumbel_az` |
| 3 | **Веса remote IS** | реестр `az`-spec поллит `latest_az_tree_policy.pth` | GAZ пишет `latest_az_gumbel_az_policy.pth` (`train.py:9321`) → нужен GAZ-spec/builder с этим именем |
| 4 | **Distributed → ПК2** | dist-контекст (`_dist_az_hp`, `train.py:9417`) и `pc2_az_actors.py` (`_train_dist_defaults`) пакуют **AZ MCTS-параметры** независимо от алго | при `gumbel_az` паковать **GAZ-поля** (`num_simulations`, `num_considered_actions`, `joint_action`, ...) и строить GAZ-payload на ПК2 |
| 5 | **GUI** | есть `AzInferenceServerPanel.qml`; у GAZ панели нет | `GazInferenceServerPanel.qml` + `remote_is_gaz.json` |
| 6 | **ПК2-лаунчеры** | `pc2_remote_az_is.bat`/`pc2_az_actors.bat`; роли `az_inference`/`az_actors` | тонкие GAZ-bat + роли `gaz_inference`(:5565)/`gaz_actors`(:5567) |
| 7 | **Лог-теги** | общие логи — `[AZ][...]` | провести `_AZ_LOG_TAG` (`GAZ`/`AZ`) → `[GAZ][...]` для триажа |
| 8 | **Доки/тесты** | нет GAZ-доков; тесты только AZ/SMZ | docs + тесты; grep алго-гейтов |

---

## 3. Архитектура (что общее, что новое)

**Общее (НЕ трогаем семантику, переиспользуем):**
`core/models/az_inference_{server,client,transport,protocol}.py`, `az_rollout_{protocol,receiver,sink}.py`,
`_main_actor_learner_alphazero`, `_az_env_worker_entry`, `_build_az_search`, `tools/az_remote_inference_server.py`
(алгоритмо-агностичен: грузит `make_alphazero_net` по net_cfg, поллит `weights_path` из аргументов/env),
`tools/pc2_az_actors.py` (параметризуем по алго).

**Новое (GAZ-специфика и фасад):**
- `core/models/gaz_remote_search_cfg_builder.py` — тонкий: общие хелперы из `remote_is_search_cfg_common`, но `WEIGHTS_NAME="latest_az_gumbel_az_policy.pth"`, `SEARCH_CFG_NAME="gaz_remote_search_cfg.json"`, читает секцию `gumbel_az`. search_cfg = арх. сети (та же, что AZ).
- GAZ-spec в `core/models/remote_is_search_cfg_registry.py` (`algo_id="gaz"`, label `GAZ`, role `gaz_inference`, env `GAZ_REMOTE_SEARCH_CONFIG`/`GAZ_REMOTE_WEIGHTS_PATH`).
- `tools/pc2_remote_gaz_is.bat` + `runtime/state/pc2_remote_gaz_is_config.bat` (шаблон) — порт 5565, GAZ-веса; зовут общий `az_remote_inference_server.py --algo-label GAZ`.
- `tools/pc2_gaz_actors.bat` (+ `.py` или переиспользование `pc2_az_actors.py` с `GAZ_*` env) — порт 5567/IS 5565.
- `app/gui_qt/qml/components/GazInferenceServerPanel.qml` + wiring в `main.py`/`Main.qml`; `runtime/state/remote_is_gaz.json`.
- Роли `gaz_inference`/`gaz_actors` в `app/gui_qt/pc2_launcher_backend.py`.

### 3.1. Inference Server (local + LAN) — поток
Идентичен AZ (см. `docs/inference-server-az-design.md`): дерево/SH + env-rollout на CPU-воркере; на GPU-сервер уходит только `net.infer` (root + per-head base + **батч листовых оценок** `_evaluate_value_batch`). Сервер stateless.

**Специфика GAZ — leaf-eval БАТЧИНГ:** `GumbelAlphaZeroSearch` собирает листья пачками по `batch_eval_size` (`gumbel_alphazero_search.py:298-333`) и зовёт `evaluator.evaluate_batch(unique_leaves)` → `values` (без priors — экономия трафика; priors GAZ из evaluator-пути не использует, `:116-118`). `evaluate_one` (root/base) возвращает priors+value. Это **точно ложится** на унифицированный AZ-протокол `infer` с осью `B` и флагом `want_priors`. **Batch-ceiling:** серверный `inference_batch_size` (дефолт 32) ≥ того, что шлёт воркер (≤ `batch_eval_size`); воркер сам ограничивает пачку `batch_eval_size`. **RNG-порядок:** все `np.random.gumbel`/`np.random.choice` живут на воркере (`:211, :353`) — offload их не трогает (чистый net.infer), детерминизм при сиде сохраняется.

### 3.2. Distributed self-play — поток
Как AZ (`plans/az-distributed-selfplay.md`): learner на ПК1 поднимает `RolloutReceiver` (PULL :5567 для GAZ), ПК2-воркеры (`_az_env_worker_entry` + `RemoteSink`) шлют rollout'ы; веса и `stop.flag` — по SMB. Канал IS (:5565) и канал rollout (:5567) — независимы. **Разрыв чиним только в передаче GAZ-настроек поиска на ПК2** (раздел 2 #4): контекст `az_dist_train_context.json` уже несёт `train_algo`; при `gumbel_az` пакуем GAZ-поля, и `pc2_az_actors._worker_main` строит GAZ-payload.

---

## 4. Конфиг / флаги (дефолт — ВЫКЛ)

В `train.py` при `is_gumbel_az_algo` резолвить IS/dist-константы с приоритетом **`GAZ_*` env → `AZ_*` env → секция `gumbel_az`** (AZ_* остаётся fallback — ноль регрессий для существующих запусков):

| Константа | GAZ env | AZ env (fallback) | hyperparams (`gumbel_az`) | Default |
|---|---|---|---|---|
| IS вкл | `GAZ_INFERENCE_SERVER` | `AZ_INFERENCE_SERVER` | `inference_server_enabled` | 0 |
| IS mode | `GAZ_INFERENCE_SERVER_MODE` | `AZ_INFERENCE_SERVER_MODE` | `inference_server_mode` | `local` |
| IS host | `GAZ_INFERENCE_REMOTE_HOST` | `AZ_INFERENCE_REMOTE_HOST` | `inference_remote_host` | `127.0.0.1` |
| IS port | `GAZ_INFERENCE_REMOTE_PORT` | `AZ_INFERENCE_REMOTE_PORT` | `inference_remote_port` | **5565** |
| IS auth | `GAZ_INFERENCE_REMOTE_AUTH_TOKEN` | `AZ_INFERENCE_REMOTE_AUTH_TOKEN` | `inference_remote_auth_token` | `""` |
| dist вкл | `GAZ_DISTRIBUTED_ACTORS` | `AZ_DISTRIBUTED_ACTORS` | `distributed_actors_enabled` | 0 |
| dist port | `GAZ_DIST_ROLLOUT_PORT` | `AZ_DIST_ROLLOUT_PORT` | `distributed_actors_port` | **5567** |
| dist bind | `GAZ_DIST_ROLLOUT_BIND` | `AZ_DIST_ROLLOUT_BIND` | `distributed_actors_bind_host` | `0.0.0.0` |
| dist auth | `GAZ_DIST_AUTH_TOKEN` | `AZ_DIST_AUTH_TOKEN` | `distributed_actors_auth_token` | `""` |

На ПК2 — `GAZ_REMOTE_DIST_ACTORS_ENABLED=1` (по образцу `AZ_REMOTE_DIST_ACTORS_ENABLED`).
**Fallback:** `inference_server_enabled=1` + нет CUDA (local) → лог `[GAZ][CONFIG][FALLBACK]`, откат на CPU-акторов (как AZ).

---

## 5. Лог-маркеры (RU, «что+где+что делать»)

`[GAZ][INF_SERVER]` (local server), `[GAZ][ENV_WORKER]`, `[GAZ][REMOTE_IS]` (ПК2), `[GAZ][REMOTE_CLIENT]`,
`[GAZ][DIST]`, `[GAZ][DIST][RECEIVER]`, `[GAZ][DIST][SINK]`, `[GAZ][CONFIG][FALLBACK]`.
Достигается прокидкой `_AZ_LOG_TAG` (уже = `GAZ` для gumbel_az, `train.py:2924`) в общие лог-строки воркера/IS/dist; standalone-сервер получает `--algo-label GAZ`. Для AZ тег остаётся `AZ` — без изменений.

---

## 6. Порты (на одном ПК2 не конфликтуют)

| Алго | IS | Distributed |
|---|---|---|
| AZ / GMZ | 5555 | 5557 (AZ) |
| SMZ | 5560 | — |
| **GAZ (новое)** | **5565** | **5567** |

---

## 7. Грабли проекта (учесть)

- **Algo-allowlist gates** (память `algo-allowlist-gates`): любой `is_az_algo`-онли путь, через который проходит IS/dist, должен пускать и `is_gumbel_az_algo`, иначе GAZ молча подменится. Grep-проверка в верификации.
- **guard_paths.py** блокирует прямой Edit/Write по `runtime/state/*remote_is*` и pc2-конфигам → шаблоны конфигов вносим как `*.example.bat`/через код, не правим защищённые файлы напрямую.
- **Windows spawn**: top-level entry-функции, dict в очередях (как в существующем коде).
- **batch-ceiling / RNG-порядок GAZ**: см. §3.1 — offload net-only, RNG на воркере, пачка ≤ `batch_eval_size`.

---

## 8. Тесты (TDD)

- `tests/`: GAZ-spec в реестре резолвится (веса `latest_az_gumbel_az_policy.pth`, cfg `gaz_remote_search_cfg.json`, role `gaz_inference`); `gaz_remote_search_cfg_builder` пишет корректную арх. сети из секции `gumbel_az`.
- algo-aware dist-контекст: при `gumbel_az` пакует GAZ-поля; `pc2_az_actors` строит GAZ-payload (`num_simulations`/`joint_action` доезжают).
- env-резолв: `GAZ_INFERENCE_SERVER`/порт 5565 имеют приоритет; при отсутствии — секция `gumbel_az`; AZ-запуск не задет.
- GUI: `remote_is_gaz.json` грузится/сохраняется с префиксом ключей `remote_is_gaz/`; панель присутствует.
- ПК2-лаунчер: роли `gaz_inference`/`gaz_actors` резолвятся, порты 5565/5567.
- **Регрессия**: AZ tree/proxy IS+dist не задеты; `GAZ_INFERENCE_SERVER=0` → прежний CPU-путь GAZ без изменений.

---

## 9. Что НЕ делаем (явно, YAGNI)

- НЕ создаём `gaz_inference_server/client/protocol/transport.py`, `gaz_rollout_{protocol,receiver,sink}.py` — это копия рабочего AZ-кода (сеть одна, offload идентичен). Вместо — переиспользование + GAZ-spec/builder/launchers/panel.
- НЕ меняем семантику поиска `GumbelAlphaZeroSearch` и контракт обучения.
- НЕ выносим env/дерево на сервер (net-only offload, как у AZ).

---

## 10. Файлы (сводка)

**Изменяем:** `hyperparams.json` (`gumbel_az`: порты 5565/5567), `train.py` (GAZ env-резолв; algo-aware dist-контекст; лог-тег), `core/models/remote_is_search_cfg_registry.py` (GAZ-spec), `tools/pc2_az_actors.py` (GAZ-payload по `train_algo`), `tools/az_remote_inference_server.py` (`--algo-label`), `app/gui_qt/remote_is_store.py` (префикс QSettings-ключа), `app/gui_qt/main.py` + `qml/Main.qml` (wiring панели), `app/gui_qt/gaz_hyperparams_defaults.py` (inference-дефолты, если нужны), `app/gui_qt/pc2_launcher_backend.py` (роли), `AGENTS.md`.

**Создаём:** `core/models/gaz_remote_search_cfg_builder.py`, `app/gui_qt/qml/components/GazInferenceServerPanel.qml`, `tools/pc2_remote_gaz_is.bat` (+ `runtime/state/pc2_remote_gaz_is_config.example.bat`), `tools/pc2_gaz_actors.bat`, `docs/inference-server-gaz-design.md`, `docs/remote-inference-server-gaz.md`, `docs/pc2-remote-gaz-is-setup-guide.md`, тесты в `tests/`.

**Планы:** `plans/gaz-inference-server.md`, `plans/gaz-distributed-selfplay.md`.
