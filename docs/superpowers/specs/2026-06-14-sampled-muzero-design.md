# Sampled MuZero — Design Spec

**Дата:** 2026-06-14
**Статус:** утверждён пользователем (брейншторм), готов к написанию плана реализации.
**Автор:** AI-агент + ревью пользователя.

## Цель

Добавить в проект **отдельную модель `sampled_muzero` («Sampled MuZero»)** — сиблинг существующих
`dqn` / `ppo` / `alphazero_tree` / `alphazero_proxy` / `gumbel_muzero`. Полная рабочая интеграция:
обучение, чекпойнты, resume, реестр агентов, eval/play/Viewer/оппонент, GUI-вкладка. Распределёнка/ПК2
и remote inference server — **не в v1**.

Мотивация: наш ход факторизован по головам (6 базовых + `move_num_{i}` на юнита, см.
`core/models/action_contract.py`), а joint-пространство действий комбинаторно большое. Текущий
`gumbel_muzero_search.py` ищет **по головам независимо** (depth-1, `base_action` greedy у остальных голов,
строки 193–312) — координация между головами/юнитами теряется (фокус огня, совместный чардж). Sampled MuZero
сэмплирует K **цельных** ходов из приора, честно их взвешивает (importance sampling) и так учит политику
координировать юнитов.

## Контекст и решения брейншторма

1. **Форма модели — отдельная модель** (новый `TRAIN_ALGO='sampled_muzero'`, своя GUI-вкладка, свои
   чекпойнты). НО «отдельная» относится к точкам входа/интеграции; идентичный код переиспользуем (см. ниже).
2. **Политика — факторизованная** (как сейчас: произведение маргиналов по головам). Авторегрессионная
   политика (голова `i` видит выбор голов `0..i-1`) — **фаза 2**, не в v1.
3. **Поиск работает везде** — train self-play + eval + play/Viewer + оппонент (как у gmz).
4. **Инфраструктура v1 — одна машина** (локальные акторы CPU/GPU, actor-learner как у gmz). Remote IS и
   distributed self-play (ПК1+ПК2) — отдельной фазой позже.
5. **DRY-решение (утверждено):** переиспользуем сеть и тренер gmz **импортом**, без физических копий
   идентичного кода. Модель остаётся отдельной по точкам входа, чекпойнтам и GUI.

## Что уникально, что переиспользуем

Уникальное в Sampled MuZero — **только поиск** (сэмпл K joint вместо перебора по головам) и **построение
policy-таргета** (IS-коррекция + маргинализация в головы). Сеть, обучение value/reward/consistency, V-trace,
reanalyze, EMA — та же MuZero-машина, что в gmz.

**Новые файлы (уникальная логика):**
- `core/models/sampled_muzero_search.py` — ★ ядро: сэмпл K joint, оценка, выбор хода, IS-улучшенная политика,
  маргинализация в головы. Sequential `run` + `run_batched` (по средам), как у gmz.
- `core/models/sampled_muzero_selfplay.py` — прогон эпизода с sampled-поиском (аналог
  `gumbel_muzero_selfplay.py`).
- `core/models/sampled_muzero_model.py` — тонкая обёртка: фабрики/загрузка/arch, переиспользует сеть
  `GumbelMuZeroNet` (архитектура идентична). Ради чистых чекпойнтов модели — свой namespace.
- `core/models/sampled_muzero_trainer.py` — тонкая обёртка над `train_gumbel_muzero_step` (named-модуль для
  модели, без дублирования логики).

**Переиспользуем у gmz (импортом):**
- `action_contract.py` — уже общий (`ordered_action_keys`, `action_sizes_from_env`, `FactorizedLegalMasks`).
- Сеть `GumbelMuZeroNet` (representation/dynamics/predict, deterministic dynamics, reward/value heads,
  consistency-projector) — идентична, менять не нужно.
- `train_gumbel_muzero_step` + `GumbelMuZeroTrainConfig` + `GumbelMuZeroEMATarget` + V-trace + LR-scheduler.
- Replay-буфер (`GumbelMuZeroReplayBuffer` / `GMZTransition`) — структура совместима 1:1 (см. Секцию 3).
- Reanalyze (`GumbelMuZeroReanalyzer`) — работает через инъекцию sampled-search (та же сигнатура `run`).

---

## Секция 2 — Сердце алгоритма

На каждом ходу в корне:

1. **Прайор β** = произведение голов: `β = Π_h softmax(logits_h)` (факторизованный, из `initial_inference`).
2. **Сэмплируем K цельных ходов** `a₁..a_K ~ β` (каждая голова независимо → один joint-сэмпл). **Дедуп с
   весами**: повторы складываются, эффективный бюджет учитывается.
3. **Оцениваем каждый уникальный ход** одним батчевым `recurrent_inference`: `Q(a) = r(a) + γ·v(s'(a))`
   (depth-1, как gmz).
4. **Улучшенная политика по сэмплам** через Gumbel-MuZero σ-преобразование Q над **носителем сэмплов**.
5. **IS-коррекция сэмплинга**: так как тянули из β, веса корректируем для **несмещённости** (в матожидании
   таргет совпадает с полным перебором). Точная формула фиксируется тестом против полного перебора на
   крошечном пространстве (Секция 5, тест 1).
6. **Выбор хода для игры**: argmax/сэмпл по улучшенной **joint**-политике → **координация сохраняется в
   выбранном ходе**.
7. **Таргет для обучения**: маргинализуем joint-улучшенную политику в головы
   `π̂_h(a_h) = Σ_{a: фикс a_h} π̂(a)` и сохраняем как `policy_targets` (поле как у gmz).

**Ключевой приём (упрощение):** IS-коррекцию и маргинализацию делаем **на self-play** и «запекаем» результат
в `policy_targets`. Тогда тренер не меняется (обычный CE к сохранённому таргету), вся новизна локализована в
`sampled_muzero_search.py`, а уроки perf-фикса 0064b8ebc сохраняются автоматически: предсказания идут с
градиентом, таргет — detached; learner остаётся векторизованным (один батчевый форвард на шаг unroll).

---

## Секция 3 — Компоненты и поток данных

- **`SampledMuZeroSearch.run(obs, legal_masks_by_head, deterministic)`** → возвращает
  `(policy_targets [маргинализованные, по головам], behavior_logits [сырые root-логиты, для V-trace],
  selected_actions [joint], value_out)` — **та же сигнатура и тип**, что `GumbelMuZeroSearch.run`
  (`gumbel_muzero_search.py:153-159`). За счёт этого selfplay/reanalyze/eval подключаются без переделок.
- **`run_batched` + `BatchedSampledMuZeroSearch`** — батч по средам (вариант B throughput), как у gmz; с тем
  же явным контрактом RNG-порядка (env-major, head-minor) ради эквивалентности sequential↔batched.
- **selfplay** кладёт транзишены в replay. Структура `GMZTransition` достаточна **как есть** (state, action,
  reward, done, `policy_targets` [уже запечённый sampled-таргет], `value_target`, `behavior_logits`,
  `legal_masks_by_head`, `policy_version`). **Новых полей не требуется**, т.к. IS «запечён» на self-play.
- **trainer**: `sampled_muzero_trainer.train_sampled_muzero_step` = тонкая обёртка над
  `train_gumbel_muzero_step`.
- **train.py**: новый `TRAIN_ALGO='sampled_muzero'`; секция конфига `SMZ_*` (зеркало `GMZ_*`,
  `train.py:2980-3069`) + новые ключи (Секция 6); диспетч learner-шага; чекпойнт-роутинг (`sampled_muzero_net`,
  ср. `train.py:7338-7342`); добавление в множества допустимых algo (`train.py:4824`, `:6274`, `:7384`);
  ветки `_main_actor_learner_sampled_muzero` / `_actor_learner_actor_entry_sampled_muzero` по образцу gmz.
- **eval.py / play / Viewer / opponent**: подключить sampled-поиск там же, где сейчас gmz.
- **GUI** (`app/gui_qt/`): новая вкладка «Sampled MuZero» (клон вкладки GMZ; пресеты fast/balanced/heavy).
- **Логи**: маркер `[SMZ]`, пишем в существующие `runtime/logs/LOGS_FOR_AGENTS_TRAIN/PLAY/EVAL.md` через код
  логирования (новый файл логов не нужен; правка формата логов запрещена хуком guard_paths).

---

## Секция 4 — Два РАЗНЫХ механизма importance sampling (не путать)

1. **IS политики** — корректирует сэмплинг K ходов из β (ядро Sampled MuZero). Живёт в `search`, «запекается»
   в `policy_targets`.
2. **V-trace IS для value** — корректирует off-policy replay при обучении value (уже в gmz,
   `gumbel_muzero_trainer.py:169-208`). Переиспользуем как есть, на тех же `behavior_logits`.

Эти механизмы независимы и не должны смешиваться в коде.

---

## Секция 5 — Тесты (TDD, RED-first)

1. **Несмещённость policy-таргета.** Крошечное joint-пространство (2 головы × 2–3 действия): sampled-таргет
   сходится к таргету полного перебора при росте K (с допуском). Это пин точной IS-формулы.
2. **Инвариант эквивалентности при стохастике (RNG-порядок).** При фиксированном `np.random.seed`
   `run` == `run_batched` (точное совпадение `selected_actions` / `policy_targets` / `behavior_logits`).
   Аналог существующего контракта gmz (`gumbel_muzero_search.py:395-415`).
3. **Маски легальности.** Нелегальные действия имеют 0 в таргете и не выбираются; кросс-голова легальность
   (если есть в env) не порождает нелегальных joint-комбинаций.
4. **Маргинализация.** Сумма таргета по каждой голове = 1; нет NaN при вырожденном/остром β (один уникальный
   сэмпл).
5. **Дедуп/веса.** Повторные сэмплы складываются корректно; эффективный бюджет учтён.
6. **Градиенты (защита perf-фикса).** Через `train_sampled_muzero_step`: value-голова и все policy-головы
   получают градиент; таргет detached; путь остаётся векторизованным (нет per-sample цикла).
7. **Координация (поведенческий тест).** Сценарий «фокус огня», где joint-выбор строго лучше независимого
   факторизованного argmax.
8. **Регресс gmz.** Вся gumbel-сюита остаётся зелёной (Sampled MuZero — отдельная модель, gmz не трогаем).

---

## Секция 6 — Конфиг и дефолты

Секция `sampled_muzero` в `hyperparams.json`, маппинг `SMZ_*` в `train.py` (зеркало `GMZ_*`):
- **Новое:** `num_samples` (K) — дефолт 24; `dedup` — вкл; `sample_temperature` — температура β при сэмплинге
  (дефолт 1.0); опционально `sample_uniform_mix` — подмешивание равномерного шума в β (дефолт 0.0) против
  схлопывания при остром β.
- **Зеркало gmz:** lr, batch_size, unroll_steps, discount, value/reward/consistency weights, l2, max_grad_norm,
  atom_range, vtrace_full + клипы, reanalyze_fraction, ema_tau, tree_reuse, температурный график, outcome_only +
  значения исходов, replay_capacity, актор-параметры (num_actors, sync_every_updates, updates_per_rollout,
  replay_min_size, max_policy_staleness_updates), пресеты сети (latent/hidden/num_layers/action_embed).
- Пресеты поиска fast/balanced/heavy (по образцу `SEARCH_PRESETS` в gmz), отличие — `num_samples` вместо
  `root_top_k`.

---

## Секция 7 — Риски и фазирование

**Риски v1 и митигации:**
- *Маргинализация теряет корреляцию в таргете* (в выбранном ходе — сохраняется). Осознанный компромисс v1;
  лечится авторегрессией (фаза 2). Тест 7 фиксирует, что выгода координации реально есть в выбранном ходе.
- *Острый β → мало уникальных сэмплов* → дедуп + `sample_uniform_mix`/`sample_temperature`.
- *Двойной учёт приора* (в сэмплинге и в prior-mix) → тест 1 на несмещённость ловит смещение.
- *RNG-расхождение sequential vs batched* → тест 2 (обязательный инвариант).
- *Коррекция и связанность с движком* минимальны: модель/тренер переиспользуются, движок не трогаем.

**Фаза 2 (после рабочей v1, отдельные спеки):**
- Авторегрессионная политика (координация в самом прайоре, меньше нужно K).
- Remote inference server + distributed self-play (ПК1+ПК2).
- Опционально: mixed/search-based value-таргеты (заимствование из EfficientZero-V2).

---

## Критерий готовности v1

- `TRAIN_ALGO='sampled_muzero'` обучается на одной машине (actor-learner), пишет чекпойнты `sampled_muzero_net`,
  resume работает.
- eval/play/Viewer/оппонент играют sampled-моделью через единый sampled-поиск.
- GUI-вкладка «Sampled MuZero» запускает train/eval.
- Все тесты Секции 5 зелёные; gumbel-сюита не сломана.
- Логи `[SMZ]` присутствуют в TRAIN/PLAY/EVAL.
