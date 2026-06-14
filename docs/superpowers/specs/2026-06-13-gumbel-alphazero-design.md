# Gumbel AlphaZero — Design Spec

**Дата:** 2026-06-13
**Статус:** утверждён пользователем (брейншторм), готов к написанию плана реализации.
**Автор:** AI-агент + ревью пользователя.

## Цель

Добавить в проект **отдельный режим обучения `gumbel_az` («Gumbel AlphaZero»)** — сиблинг существующих
`alphazero_tree` / `alphazero_proxy` / `gumbel_muzero`. Полная рабочая интеграция: обучение, чекпойнты,
resume, реестр агентов, eval/play/Viewer, GUI с тремя пресетами (light/fast, balanced, heavy; дефолт —
balanced). Распределёнка/ПК2 — **не в v1**, но швы (hyperparams-поля + env-маппинг) заложены под будущее.

## Контекст и решения брейншторма

- **Алгоритм.** Gumbel AlphaZero = AlphaZero (реальная модель среды, не выученная как в MuZero) +
  политика-улучшение через планирование с Gumbel: Gumbel top-k сэмплинг в корне, Sequential Halving для
  распределения бюджета симуляций, **completed Q-values** как policy-target. Главное свойство — гарантия
  улучшения политики даже при крошечном бюджете симуляций (16–64), что ровно соответствует нашему профилю
  (`max_depth=1`, низкие sims, LAN).
- **Выбранная архитектура поиска — Вариант A:** per-head Gumbel top-k + Sequential Halving, depth-1
  (root-only), оценка кандидатов через **реальный env-шаг + value-сеть**. Причины: максимальный реюз
  отлаженного кода (env-роллаут AZ + Gumbel-математика из `gumbel_muzero_search.py`), минимальный риск
  регрессий в движке, и это «сладкая зона» Gumbel. Варианты B (joint-action SH) и C (полное дерево с PUCT
  внутри, depth>1) отложены — апгрейд возможен позже за тем же id без изменения обвязки.
- **eval/play — режим `reuse`:** обученная `gumbel_az`-модель — обычная AlphaZero-сеть, поэтому eval/play/Viewer
  грузят и играют её greedy (как AZ). Отдельный Gumbel-поиск на инференсе — будущий режим за тем же id.

## Принцип интеграции (ключевой)

`GumbelAlphaZeroSearch.run()` повторяет **сигнатуру и возвращаемый тип** `AlphaZeroFactorizedMCTS.run()`
— `(policy_targets, selected_actions, value)`. За счёт этого:
- весь AZ learner-конвейер (`play_episode_with_mcts`, `AZTransition`, `AlphaZeroReplayBuffer`,
  `train_alphazero_step`, чекпойнт, resume, sync-файл, det_eval gate) **переиспользуется без изменений**;
- единственное новое алгоритмическое — сам объект поиска;
- сеть, формат чекпойнта и eval/play наследуются от AZ-семейства.

---

## Секция 1 — Поисковое ядро `GumbelAlphaZeroSearch`

**Новый файл:** `core/models/gumbel_alphazero_search.py`. Класс `GumbelAlphaZeroSearch` + конфиг
`GumbelAZSearchConfig`.

### Переиспользуем
- Сеть `AlphaZeroPolicyValueNet` (policy-логиты + value, без dynamics-модели).
- Машинерию env-роллаута на 1 шаг: `snapshot_state`/`restore_state`, `step`, `enemyTurn`, терминальная
  развязка, `eval_cache`, батч-оценку value — общая с AZ tree (выносится в общий хелпер во избежание
  дублирования; вынос делать аккуратно, т.к. код движко-критичный).
- Интерфейс инъектируемого `evaluator` (`evaluate_one`/`evaluate_batch`) — тот же шов, что AZ использует
  для inference-сервера → будущий ПК2 заведётся без правок ядра.

### Новая логика (только это)
Для каждой головы `h` независимо (depth-1):
1. **Логиты из приоров:** `logit(a) = log(prior(a))` по легальным `a` (приоры из `net.infer`/evaluator —
   совместимо с inference-сервером).
2. **Gumbel top-m:** сэмплим `g(a) ~ Gumbel(0,1)`, берём top-`m` кандидатов по `g(a)+logit(a)`
   (`m = num_considered_actions`). Dirichlet не используется — шум встроен в Gumbel.
3. **Sequential Halving:** бюджет `num_simulations` режется по раундам `⌈log2(m)⌉`; каждому выжившему
   кандидату даётся порция симуляций, считается `q(a)` = value позиции после реального env-шага этим
   действием + ход врага; отбрасывается худшая половина по `g(a)+logit(a)+σ(q̂(a))`; повтор до 1
   победителя. Оценки позиций внутри раунда **батчатся** через общий `evaluate_value_batch`.
4. **Выбранное действие** головы = победитель SH (= argmax `g+logit+σ(q̂)` на рассмотренном наборе).
5. **Completed-Q policy target:** `π'(a) = softmax(logit(a) + σ(completedQ(a)))` по **всем** легальным `a`,
   где `completedQ(a)=q̂(a)` для оценённых действий, неоценённые «достраиваются» нормированным root-value.
   `q̂` — min-max нормировка q в [0,1] по голове; `σ` — монотонная шкала (форма из статьи Gumbel,
   параметры `value_scale`, `c_visit`).

### Температура / эксплорейшн
На дебюте (`move_count < temperature_opening_moves`) ход сэмплим из `π'`, дальше — argmax
(детерминированный SH-победитель). Совпадает с AZ-логикой температуры.

### Конфиг `GumbelAZSearchConfig`
`num_simulations`, `num_considered_actions` (m), `max_depth` (=1 в v1, задел под C),
`value_scale`/`c_visit` (для σ), `temperature_opening_moves`, `eval_cache_size`, `batch_eval_size`,
`simulate_enemy`, `mode` (задел под будущее дерево).

### Робастность
- Голова без легальных действий → uniform-фолбэк, без падения.
- NaN/inf в приорах → uniform по легальным (зеркало `_masked_normalize`).

### Замечания по v1 (важно для реализации)

- **SH при детерминированном depth-1 почти вырождается.** q-оценка кандидата детерминирована (env-шаг + ход
  врага + value), повторные симуляции бьют в `eval_cache` → тот же q. Значит `num_simulations` сверх `m` не
  меняет ни победителя, ни policy-target; реальный рычаг — `num_considered_actions` (m) + completed-Q.
  «Халвинг» даёт прирост только при **стохастичном** `enemyTurn`. Это норм для v1 (корректность сохраняется),
  но в логах/доке не подавать sims=64 как «сильнее». Тест «бюджет соблюдён» (§6.1) должен либо реально это
  проверять, либо быть убран из критериев.
- **`simulate_enemy=0` — дефолт.** Встроенная эвристика врага тяжёлая (6 фаз), и при `simulate_enemy=1` она
  вызывается на каждого кандидата каждой головы (per-head, depth-1) → ~60–116 серийных роллаутов на ход,
  ~10–16 с/ход на CPU → первый эпизод не завершается минутами, replay пуст, learner не стартует. Поэтому по
  умолчанию лист оценивается сетью сразу после хода модели (как `simulate_enemy_in_tree=False` у AZ).
  `simulate_enemy=1` оставлен опцией для тех, кто готов платить за более точную (с ответом врага) оценку,
  но тогда нужно резко снижать `num_simulations`/`num_considered_actions`/`num_actors`.
- **Дублирование движко-кода — избегаем.** Машинерия rollout (`_terminal_value_from_info`, `_restore_env_safe`,
  `_evaluate_net`, `_evaluate_value_batch`, тело depth-1 шага) уже есть и оттестирована в
  `alphazero_mcts.py`. Предпочтительно вынести её в общий хелпер и звать из обоих поисков (AZ MCTS + Gumbel),
  а не копировать verbatim — иначе будущие фиксы движка придётся вносить в двух местах (правило проекта против
  дублей AZ↔gmz). Если копия неизбежна — синхронизировать при изменениях и пометить якорь-комментарием.
- **Per-head аппроксимация.** Победитель головы оценивается при остальных головах = greedy-prior (`base_action`),
  а исполняется совместное действие из всех победителей — сознательная аппроксимация Варианта A.

---

## Секция 2 — Интеграция в `train.py`

**Принцип:** контракт `run()` тот же → learner AZ переиспользуется; различается только бэкенд поиска у актёра.

- **2.1 Новый id** в `core/models/alphazero_ids.py`: `gumbel_az` → в `VALID_TRAIN_ALGOS`; новый
  `is_gumbel_az_algo(algo)`; семейный `is_alphazero_net_algo(algo)` = `{alphazero_tree, alphazero_proxy,
  gumbel_az}` (там, где код завязан на AZ-сеть и формат чекпойнта). `is_az_algo()` оставляем строго для
  PUCT-MCTS-режима. `az_section_for(gumbel_az)` → `"gumbel_az"`.
- **2.2 Диспатч в `main()`:** ветка AZ принимает `gumbel_az` и заходит в общий
  `_main_actor_learner_alphazero`. Не копируем гигантскую функцию — параметризуем точку выбора бэкенда
  (actor-entry + сборка cfg-payload).
- **2.3 Сборка конфига:** новая `_gaz_search_config()` (зеркало `_az_mcts_config()`) собирает
  `GumbelAZSearchConfig` из секции `gumbel_az` + env-оверрайдов.
- **2.4 Выбор бэкенда в актёре:** в `_actor_learner_actor_entry_alphazero` и `_az_env_worker_entry` —
  если `TRAIN_ALGO == gumbel_az` строим `GumbelAlphaZeroSearch`, иначе `AlphaZeroFactorizedMCTS`. Оба
  получают одинаковые `net`/`evaluator`/`device`.
- **2.5 Чекпойнт:** формат идентичен AZ (`policy_value_net`, `optimizer`, `arch`, `episode`,
  `policy_version`, `replay_memory`), плюс `algo="gumbel_az"`, метка режима `mcts_mode="gumbel"`. Папка
  `artifacts/models/gumbel_az/checkpoint_ep*.pth`; sync-файл
  `artifacts/models/actor_sync/latest_az_gumbel_az_policy.pth` (паттерн `latest_az_{tag}_policy.pth`, tag=`gumbel_az`
  — совпадает с реальным кодом `train.py`, см. строки сборки `_az_sync_tag`).
- **2.6 Resume:** без нового кода — тот же `RESUME_CHECKPOINT`, тот же inline-загрузчик AZ (ключ
  `policy_value_net` + `arch`), та же жёсткая остановка на битых весах. Проверить, что resume-ветка
  срабатывает для `is_alphazero_net_algo`.
- **2.7 Env-переменные:** новое семейство `GAZ_*` (зеркало `AZ_*`): ядро
  (`GAZ_NUM_SIMULATIONS`, `GAZ_NUM_CONSIDERED_ACTIONS`, `GAZ_MAX_DEPTH`, `GAZ_VALUE_SCALE`, `GAZ_C_VISIT`,
  `GAZ_SIMULATE_ENEMY`, `GAZ_EVAL_CACHE_SIZE`, `GAZ_BATCH_EVAL_SIZE`); инфраструктура
  (`GAZ_NUM_ACTORS`, `GAZ_REPLAY_*`, `GAZ_SYNC_EVERY_UPDATES`, `GAZ_UPDATES_PER_ROLLOUT`, lr/арх);
  шаблонные под ПК2 (`GAZ_INFERENCE_SERVER*`, `GAZ_DISTRIBUTED_ACTORS*`), по умолчанию off.
- **2.8 det_eval gate:** переиспользуем AZ train-window gate без изменений.

---

## Секция 3 — Реестр агентов + eval / play / Viewer (`reuse`)

**Принцип:** `gumbel_az`-модель = обычная AZ-сеть; eval/play/Viewer по умолчанию играют через
GAZ Search (`GAZ_*`), а Greedy остаётся быстрым fallback/baseline.

- **3.1 `core/engine/agent_registry.py`:** `gumbel_az` → `_VALID_AGENT_ALGOS`. Веса не отличить от AZ
  (`infer_algo_from_policy_state` → `alphazero_tree`), поэтому **`meta.algo` авторитетен** (как у PPO):
  в `resolve_agent_algo` если веса = AZ-семейство, но `meta.algo == "gumbel_az"` → вернуть `gumbel_az`.
  Включить `gumbel_az` в `collect_registered_agents_meta`.
- **3.2 `eval.py`:** ветки загрузки сети с `is_az_algo` → `is_alphazero_net_algo` (грузить через
  `make_alphazero_net` + `load_alphazero_state_dict`, ключ `policy_value_net`, `arch` из payload). Выбор
  действия для `gumbel_az` — дефолт Gumbel Search; Greedy (`net.infer` + argmax) остаётся отдельным режимом.
- **3.3 `core/engine/game_controller.py` и `play.py`:** те же гейты → `is_alphazero_net_algo`; чекпойнт
  пересобирается с ключом `policy_value_net`; `GAZ_PLAY_MODE` дефолт `gumbel`, `GAZ_JOINT_ACTION` дефолт 1.
- **3.4 `core/models/opponent_adapter.py`:** гейт → `is_alphazero_net_algo`, чтобы `gumbel_az` можно было
  выбрать противником (Gumbel Search по умолчанию, Greedy по явному выбору).
- **3.5 Аудит call-sites `is_az_algo`:** пройти все точки (eval.py, game_controller.py, play.py,
  opponent_adapter.py) и для каждой решить — «семейство сети/чекпойнта» (→ `is_alphazero_net_algo`) или
  «именно PUCT-MCTS-режим» (→ оставить `is_az_algo`), чтобы не сломать AZ tree/proxy.

---

## Секция 4 — GUI (Qt/QML)

Зеркалим паттерн Gumbel MuZero (отдельный файл дефолтов + своя вкладка), т.к. `gumbel_az` — самостоятельное
семейство со своими ключами `GAZ_*`.

- **4.1 Новый `app/gui_qt/gaz_hyperparams_defaults.py`:** `GAZ_HYPERPARAM_KEYS`, `_GAZ_BASE`,
  `DEFAULT_GAZ_HYPERPARAMS` (= base + balanced), `GAZ_PROFILE_PRESETS = {fast, balanced, heavy}` (дефолт
  balanced), `GAZ_GROUPS`, `GAZ_FIELD_TOOLTIPS`, `GAZ_BASIC_KEYS`, `GAZ_INFERENCE_PRESERVE_KEYS`.
- **4.2 `app/gui_qt/main.py`:** `_training_algo_options += "gumbel_az"` + синхронизация прочих whitelists
  и `_format_algo_label` → `"GUMBEL ALPHAZERO"`; состояние `self._gaz_hyperparams` + load/save секции
  `"gumbel_az"` с type-coercion (как `_load_az_hyperparams_section`); QML-проперти `hpGaz*`; слоты
  `set_gaz_hyperparam`, `apply_gaz_profile`, ветка `_detect_profile`; в `_start_training` при
  `algo==gumbel_az` — `TRAIN_ALGO=gumbel_az` + проброс ключевых `GAZ_*` env.
- **4.3 `app/gui_qt/qml/Main.qml`:** пункт dropdown `{ value: "gumbel_az", label: "GUMBEL ALPHAZERO" }`;
  в Settings TabBar — `TabButton "Gumbel AlphaZero"` + `StackLayout`-ребёнок
  `SectionHyperparamsEditor { algoSection: "gaz" }`.
- **4.4 `SectionHyperparamsEditor.qml`:** ветка `algoSection === "gaz"` → `hpGaz*`-карты; пресеты
  `["fast","balanced","heavy"]` → `controller.apply_gaz_profile(name)`.
- **4.5 `TrainingAlgoHelpDialog.qml`:** карточка-справка про Gumbel AlphaZero.
- **4.6 Resume-чекбокс** — общий (`RESUME_CHECKPOINT` через `_find_latest_resume_file`); проверить, что
  скан `artifacts/models/**/checkpoint_ep*.pth` захватывает папку `gumbel_az/`.

---

## Секция 5 — Три пресета в `hyperparams.json`

Новая секция `"gumbel_az"` (значения = balanced). Пресеты живут патчами в
`gaz_hyperparams_defaults.py`; дефолт — balanced (как у AZ).

Ядро поиска:

| Параметр | fast | balanced | heavy |
|---|---|---|---|
| `num_simulations` | 16 | 32 | 64 |
| `num_considered_actions` (m) | 4 | 8 | 16 |
| `max_depth` | 1 | 1 | 1 |
| `value_scale` (σ) | 0.1 | 0.1 | 0.1 |
| `c_visit` | 50 | 50 | 50 |
| `simulate_enemy` | 0 | 0 | 0 |
| `batch_eval_size` | 8 | 16 | 32 |

Общие поля (во всех трёх): `learning_rate 3e-4`, `batch_size 128`, `value_loss_weight 1.0`,
`l2_weight 1e-6`, `replay_capacity 100000`, `num_actors 8`, `sync_every_updates 2`,
`updates_per_rollout 2`, `replay_min_size 512`, `balanced_outcome_sampling 1`,
`max_policy_staleness_updates 600`, outcome win/loss/draw `1.0/-1.0/-0.25`, `hidden_size 256`,
`num_layers 2`, `value_ensemble 1`, `temperature_opening_moves 12`, `temperature_opening_value 0.9`,
`temperature_late_value 0.15`, `eval_cache_size 10000`, `lr_scheduler "none"`.

Поля под будущий ПК2 (присутствуют, выключены): `inference_server_enabled 0`,
`inference_server_mode "local"`, `inference_remote_host/port/auth`, `distributed_actors_enabled 0` и т.д.

---

## Секция 6 — Тесты + критерии готовности

### Тесты
- **6.1 Юнит — ядро** (`tests/models/test_gumbel_alphazero_search.py`): Gumbel top-m ≤ m среди легальных;
  Sequential Halving → 1 победитель, бюджет соблюдён; completed-Q target — валидное распределение по
  головам (масса на легальных); голова без легальных → uniform-фолбэк; NaN/inf → uniform;
  `temperature→0` → argmax, воспроизводимость при сид; контракт возврата = AZ (3-tuple).
- **6.2 Интеграция** (`tests/engine/test_gumbel_az_integration.py`): `play_episode_with_mcts` с
  `GumbelAlphaZeroSearch` на мини-env → корректные `AZTransition`, value ∈ [-1,1], без исключений;
  snapshot/restore консистентен.
- **6.3 ids/registry** (дополнения в `tests/engine/test_resolve_agent_algo.py`): AZ-веса +
  `meta.algo=gumbel_az` → `gumbel_az`; корректность `is_gumbel_az_algo` / `is_alphazero_net_algo`.
- **6.4 Связка train** (зеркало `test_alphazero_smoke`): `_gaz_search_config()` собирает конфиг;
  чекпойнт-payload имеет `algo=gumbel_az`, `policy_value_net`, `arch`; resume round-trip.
- **6.5 GUI** (`tests/gui_qt/test_gaz_hyperparams_load.py`): `_load_gaz_hyperparams_section` сохраняет
  строковый host, приводит int, фолбэчит битые значения; `apply_gaz_profile` ставит fast/balanced/heavy и
  сохраняет inference-ключи; `gumbel_az` в `_training_algo_options`.
- **6.6 eval/play smoke:** чекпойнт `gumbel_az` грузится по пути `is_alphazero_net_algo`, GAZ Search и
  Greedy работают.

### Логи
В train-цикле для `gumbel_az` префикс `[GAZ]` (вместо `[AZ]`) на ключевых строках: `[GAZ][CONFIG]`,
`[GAZ][WAIT]`, `[GAZ][ACTOR]` — переключается по `TRAIN_ALGO` (learner) / `cfg.mode=="gumbel"` (актёр).
Числа `sims`/`depth` в этих строках берутся из gaz-конфига (`GAZ_NUM_SIMS`/`GAZ_MAX_DEPTH`), а не из
generic `AZ_MCTS_*` (которые для gumbel_az остаются дефолтами секции AZ и путали бы в логах). heartbeat
актёра дополнительно печатает `mcts_mode=gumbel`.

### Критерии готовности v1
1. **Функционал:** dropdown содержит «Gumbel AlphaZero»; выбор + любой из 3 пресетов + resume запускает
   train без ошибок; чекпойнты в `artifacts/models/gumbel_az/`; resume продолжает; eval/play грузит и
   играет модель (в т.ч. как противник).
2. **Логи:** маркеры фаз `[GAZ]`/`[AZ]` без ошибок в `LOGS_FOR_AGENTS_TRAIN.md`; det_eval gate выдаёт
   `win_rate`.
3. **Тесты:** новые проходят; существующие AZ-тесты зелёные (нет регрессии).
4. **Качество (A/B):** через `eval.py` `gumbel_az` при равном бюджете симуляций ≥ AZ tree — замеряется
   позже, не блокер v1. Критерий v1 = корректность + интеграция-parity + отсутствие регрессий.

## Вне scope v1 (явно)
- ПК2 / распределённые акторы / remote inference server для `gumbel_az` (швы заложены, включение позже).
- Варианты B (joint-action SH) и C (полное дерево depth>1).
- Глубокое дерево GAZ depth>1 и параллельные env-clone rollout'ы для инференса.
