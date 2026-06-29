# Дизайн: PHOENIX — sample-efficient off-policy агент для W40k

- **Дата:** 2026-06-29
- **Статус:** утверждён (brainstorming), готов к writing-plans
- **Ветка:** worktree2
- **Кодовое имя / id:** `PHOENIX` / `phoenix` (Self-Predictive Reset Q-learning с латентным value-expansion)
- **Связанные памяти:** algo-allowlist-gates, eval-loader-shape-mismatch-failfast, muzero-test-subset-ram-heavy, opponent-pool-league, annihilation-training-findings

---

## 0. Контекст и текущее состояние кода (проверено)

RL-песочница W40k. Алгоритмы (`core/models/`): DQN, PPO, AlphaZero tree/proxy, Gumbel AZ,
Gumbel/Sampled MuZero. Точка входа — `train.py`, окружение — `core/envs/warhamEnv.py`.

**Что уже есть и переиспользуется:**
- `core/models/DQN.py` — Rainbow-plus сеть: **IQN** (distributional), NoisyNets, dueling,
  ensemble, ствол `input_fc`+LayerNorm+`ResidualBlock`×N. Действие — **факторизованное
  многоголовое** (`spaces.Dict`): per-unit `move_num_i`/`shoot_num_i`/`charge_num_i` + per-phase
  `strat_*`/`strat_*_unit`. Текущий DQN берёт argmax **по каждой голове независимо** (branching).
- `core/models/dqn_dist.py` — Ape-X distributed актор↔learner (stop-flag, train-context,
  RemoteDataQ, транспорт из `az_rollout_*`). Off-policy value-based — та же схема подходит PHOENIX.
- Opponent pool / League (PFSP) — `core/engine/opponent_pool.py`, `core/models/opponent_pool_runtime.py`;
  врезка в `train.py` при `SELF_PLAY_ENABLED=1` + `POOL_CONFIG.enabled` (см. память
  [[opponent-pool-league]]). PHOENIX подключается к пулу как остальные algo.
- Резолв конфига env→секция→default — образец в `resolve_pool_config` / `opponent_pool`.

**Проблема, которую решает PHOENIX.** Текущий DQN тренируется долго и затратно по железу/времени.
Нужен off-policy агент, который достигает того же качества за заметно меньший бюджет эпизодов
(**sample-efficiency**), оставаясь «классическим» off-policy на инференсе (replay buffer, без дерева
поиска / без планирования при выборе действия).

**Принятые на brainstorming решения:**
- Главная цель — **sample-efficiency** (BBF-семейство), а не координация/exploration.
- Ядро — **полный SPR-аух** (латентная динамика + BYOL-consistency).
- Вариант **B**: SPR + латентный **value-expansion** (model-based таргеты в обучении, model-free на инференсе).
- Охват — **полноценный новый `TRAIN_ALGO=phoenix`** (реестр, allowlist-гейты, train-луп, eval/play,
  вкладка GUI, opponent pool, distributed).
- Дефолты открытых вопросов: value-expansion — STEVE-усреднение по горизонтам за флагом (`H=0` →
  обычный 1-step IQN); dynamics — детерминированный **MLP** (GRU опцией); replay ratio — старт **RR=2**.

**Не-цели (YAGNI на первом этапе):**
- Никакого дерева поиска / планирования на инференсе (это не MuZero).
- Coordination-by-prediction (вариант C) — только опциональный флаг на будущее, не в scope.
- Никаких новых reward-профилей — reuse `reward_config.py` как есть.

---

## 1. Идентичность алгоритма

PHOENIX — off-policy value-based агент для факторизованного многоголового действия W40k. К IQN-сети
DQN добавляет три вещи:

1. **Self-predictive репрезентации (SPR):** латентная transition-модель учится предсказывать будущие
   скрытые состояния (BYOL-style consistency на горизонте K) — улучшает репрезентации без наград.
2. **Латентный value-expansion (наша изюминка):** ту же выученную динамику используем для расчёта
   **таргетов** (реальные награды из последовательности + bootstrap target-IQN на предсказанном
   латенте, усреднение по горизонтам). Часть выигрыша EfficientZero **без дерева поиска**.
3. **BBF-рецепт обучения:** периодические resets + shrink-and-perturb, высокий replay ratio,
   аннелинг n-step и γ.

На инференсе — чистый off-policy: модель и SPR работают **только в обучении**; при выборе действия —
per-head argmax по IQN-Q, как в текущем DQN.

---

## 2. Архитектура сети

Модуль: `core/models/phoenix_model.py` (новый). Переиспользует слои из `DQN.py`.

```
obs ─► [Encoder f_o] ─► z_t ─► [IQN-голова (per branch)] ─► Q-квантили на голову
        (input_fc+LayerNorm           │
         +ResidualBlock×N из DQN)      ├─► [Projection p] ─► [Prediction q] ─► ŷ_online (SPR)
                                       │
action a_t (Dict голов) ─►[Action-embed g]─►[Latent dynamics h(z, g(a))]─► ẑ_{t+1..t+K}

target (для SPR): o_{t+k} ─► [Encoder f_m = EMA(f_o)] ─► [Proj p_m = EMA(p)] ─► stop-grad
```

**Компоненты:**
- **Encoder `f_o`** — ствол DQN (`input_fc`+`input_norm`+`ResidualBlock`×`num_layers`), выход `z`
  размера `hidden_size`.
- **IQN RL-голова** — существующий `_DQNHeadBundle` (IQN-путь) на `z`. Per-head квантили `Q(z, ·)`.
  Dueling — опция (дефолт как у DQN). **NoisyNets по умолчанию ВЫКЛ (`noisy=False`)** — это
  осознанное отличие от DQN: шумовые сети делают greedy `a*` в value-expansion таргете стохастичным
  и плохо сочетаются с resets/EMA; BBF/SPR шумовые сети не используют. Exploration в PHOENIX даёт
  ε-greedy + ротация оппонента (лига).
- **Action-embed `g(a)`** — на каждую голову своя `nn.Embedding(action_size_i, emb_dim)`; берём
  эмбеддинг выбранного индекса, **умножаем на маску активности головы** (неактивные в фазе головы
  → вклад 0), суммируем по головам → вектор действия `emb_dim`.
- **Latent dynamics `h`** — `dynamics_type="mlp"` (по умолчанию): MLP `[z; g(a)] → z'`. Раскрутка
  рекуррентна: `ẑ_{k+1} = h(ẑ_k, g(a_{t+k}))`, `ẑ_0 = z_t`. Опция `"gru"` — GRUCell.
- **Projection `p` / Prediction `q`** — BYOL-головы (MLP). `f_m`, `p_m` — EMA-копии (stop-grad),
  обновляются `target_ema`.

**Восстановление арх-параметров** из state_dict — аналог `infer_dqn_arch_from_state_dict` (для
загрузки чужого/распределённого чекпойнта без знания конфига).

---

## 3. Лоссы

Модуль: `core/models/phoenix_loss.py` (новый, torch-зависимый, но тонкий).

### 3.1 IQN TD-loss с латентным value-expansion
- Базовый таргет на горизонте `h`: `y_h = Σ_{j=0..h-1} γ^j r_{t+j} + γ^h · Q_target(ẑ_{t+h}, a*_{t+h})`,
  где `r` — реальные награды из sequence-replay, `ẑ_{t+h}` — латент из dynamics (detach), `a*` —
  greedy по target-сети, маска голов учитывается.
- **value-expansion агрегация:** при `ve_steve=True` — усреднение `y_h` по `h∈{1..ve_horizon}` с
  инверсно-дисперсионным весом (STEVE) по ансамблю/квантильному разбросу; при `ve_steve=False` —
  фиксированный `y_{ve_horizon}`. **`ve_horizon=0` ⇒ обычный 1-step IQN-таргет** (sanity/ablation).
- Лосс — квантильный Huber (как в текущем IQN), суммирование по головам с маской.
- **Off-policy честно:** награды `r_{t+j}` — реальные из реплея (собраны под старой/поведенческой
  политикой), bootstrap — на предсказанном латенте. Это **некорректированный off-policy n-step**
  (без importance sampling / tree-backup), ровно как в текущем DQN. Смещение принимается осознанно
  (как в BBF/SPR) и гасится коротким n-step + частыми resets; это не баг, а компромисс рецепта.

### 3.2 SPR consistency
- Для `k=1..K`: нормированная косинус-дистанция между `q(p(ẑ_{t+k}))` и `sg(p_m(f_m(o_{t+k})))`.
- Маска по `done`: за терминалом эпизода k-члены не считаются.
- Градиент **не течёт** в target-ветку (EMA + stop-grad).

### 3.3 Итог
`L = L_IQN + λ_spr · L_spr`. Оптимизатор **AdamW** (weight decay — BBF-регуляризация).
Дефолты: `spr_coef(λ_spr)=2.0`, `spr_horizon_K=5`, `ve_horizon=3`, **`ve_steve=False`** (по умолчанию
фиксированный `y_{ve_horizon}` — ядро проще, тест 4 без инверсно-дисперсионной математики;
STEVE-усреднение — отдельная A/B-кнопка).

---

## 4. Рецепт обучения (BBF)

Модуль: `core/models/phoenix_trainer.py` (learn-step, resets, аннелинги) + sequence-replay.

- **Sequence-replay:** буфер хранит связные траектории, сэмплит окно длиной `H+1` подряд, где
  `H = max(spr_horizon_K, ve_horizon)` (по умолчанию `H=5`).
  - **Реюз — механизм sum-tree/segment-tree из `PrioritizedReplayMemory`, а НЕ класс целиком**:
    существующая `PrioritizedReplayMemory` хранит одиночные `Transition`. Нужен новый
    sequence-буфер, индексирующий sum-tree **по началу окна**; приоритет — по TD-ошибке первого
    перехода окна. На границе эпизода окно маскируется по `done`.
  - **Data-contract окна (важно для VE):** буфер хранит на **каждый** из `H+1` шагов: `obs`,
    реальное `action` (Dict голов) для dynamics/SPR, награду, флаг `done`, и **per-step маски
    активности голов** + аналог `next_shoot_mask`. VE-таргету нужен `a*_{t+h}` с маской активных
    голов именно на шаге `t+h` (зависит от фазы в этот момент), поэтому маски нужны на все шаги
    окна, а не только на первый переход.
- **Replay ratio** — `replay_ratio` градиентных апдейтов на env-шаг. **Дефолт 2 — только для
  smoke/валидации ядра** (проверить, что пайплайн учится и не падает). **RR — A/B-кнопка №1**: весь
  смысл BBF в высоком RR (SR-SPR/BBF гоняют 8–16); выигрыш sample-efficiency показывается именно её
  подъёмом. `reset_interval`/аннелинги считаются в **градиентных шагах** → инвариантны к RR, но
  env-степовый след resets меняется ×RR (это учитываем при A/B).
- **Periodic resets** — каждые `reset_interval` градиентных шагов:
  - полный reset голов (IQN-голова, projection/prediction, dynamics, action-embed) к свежей
    инициализации;
  - **shrink-and-perturb** энкодера: `w ← α·w + (1−α)·φ`, `φ` — случайная инициализация,
    `α=shrink_alpha=0.5`. **Агрессивный дефолт** (сильно перетряхивает энкодер) — ключевая A/B-кнопка.
  - ре-синк target-сетей (RL-target и SPR `f_m`/`p_m`);
  - сброс моментов AdamW для сброшенных параметров;
  - reset запрещён внутри накопления градиента (между полными шагами).
- **Аннелинг** после каждого reset, экспоненциально за `anneal_steps` градиентных шагов:
  n-step `nstep_start→nstep_end` = **10→3**, γ `gamma_start→gamma_end` = **0.97→0.99**.
  **End-значения заякорены на рабочие DQN-гиперы** (`N_STEP=3` в [train.py:347](../../../train.py),
  `gamma=0.99` в hyperparams.json), а не на атаревский профиль (0.997/слепой 10); start —
  исследовательские.
- **Target EMA** — отдельные коэффициенты для RL-target и SPR-энкодера.

**Закреплённые дефолты расписаний (нужны для тестов 5/6):**

| Поле | Дефолт | Примечание |
|------|--------|------------|
| `replay_ratio` | 2 | только smoke; A/B-кнопка №1 (поднимать до 8–16) |
| `reset_interval` | 40000 град. шагов | BBF-профиль |
| `anneal_steps` | 10000 град. шагов | длина n-step/γ аннелинга после reset |
| `shrink_alpha` | 0.5 | агрессивно; A/B-кнопка |
| `nstep_start→end` | 10 → 3 | end = рабочий DQN `N_STEP` |
| `gamma_start→end` | 0.97 → 0.99 | end = рабочий DQN `gamma` |
| `target_ema_rl` | 0.005 | RL-target |
| `target_ema_spr` | 0.01 | SPR-энкодер (BYOL-профиль) |
| `replay_capacity` | 200000 окон | sequence-буфер |
| `ve_steve` | False | фикс. `y_{ve_horizon}`; STEVE — A/B |
| `noisy` | False | см. §2 (footgun с VE/resets) |

---

## 5. Интеграция в проект (новый `TRAIN_ALGO=phoenix`)

**Allowlist-гейты** (критично — иначе модель молча подменится на dqn, см. [[algo-allowlist-gates]]):
добавить `phoenix` в `VALID_TRAIN_ALGOS`, реестр агентов (`make_env_contract` / билд сети),
**все** списки источников оппонента (включая `pool`), списки algo в `eval.py`/`play.py`/Viewer,
GUI-селекторы. Защитный тест проверяет присутствие во всех гейтах.

**train.py:** новая ветка learner'а рядом с DQN (переиспользует encoder-ствол, IQN-голову, PER →
sequence-replay, self-play + opponent pool как у остальных algo). Финальный/периодический league-snapshot
через уже существующий `LeagueLearnerSnapshotWriter`.

**Distributed (Ape-X):** переиспользуем `dqn_dist.py` / `az_rollout_*`. Расширение протокола:
актор шлёт **последовательности** переходов (K+1) вместо одиночных. Stop-flag `phoenix_dist_stop.flag`.

**Конфиг:** секция `phoenix` в `hyperparams.json`. Поля: `replay_ratio`, `reset_interval`,
`shrink_alpha`, `spr_horizon_K`, `spr_coef`, `ve_horizon`, `ve_steve`, `nstep_start`, `nstep_end`,
`gamma_start`, `gamma_end`, `dynamics_type`, `emb_dim`, `target_ema`, + наследуемые DQN-арх
(`hidden_size`, `num_layers`, `ensemble_size`, IQN-параметры). Env-флаги `PHOENIX_*`, приоритет резолва
`env → секция → default` (как у opponent_pool). Функция `resolve_phoenix_config`.

**GUI:** вкладка «PHOENIX» по образцу DQN/AZ (старт train, гиперы, help-карточка алгоритма). Запуск —
через Qt GUI (правило проекта).

**Логи** (`LOGS_FOR_AGENTS_TRAIN.md`):
- `[PHOENIX][CONFIG]` — резолв конфига (источник каждого поля).
- `[PHOENIX][TRAIN]` — шаг, лоссы (IQN/SPR), replay_ratio.
- `[PHOENIX][SPR]` — consistency-loss, horizon K.
- `[PHOENIX][VE]` — горизонты/веса value-expansion.
- `[PHOENIX][RESET]` — что сброшено, α, ре-синк target.
- `[PHOENIX][DIST]` — распределёнка.
- `[PHOENIX][WARN]` — fallback/ошибка: что случилось + где + что делать.

---

## 6. Тесты (TDD, до кода)

Юнит-тесты в `tests/models/` (точечно по затронутым файлам — НЕ гонять весь muzero-сабсет,
см. [[muzero-test-subset-ram-heavy]]):

1. **action-embed**: неактивные головы дают вклад 0; маска активности работает; форма `emb_dim`.
2. **latent rollout**: формы `ẑ_{1..K}` корректны; раскрутка рекуррентна; `ẑ_0 == z_t`.
3. **SPR-loss**: =0 при prediction==target, >0 иначе; градиент НЕ течёт в target-энкодер; маска `done`.
4. **value-expansion**: при `ve_horizon=0` таргет == 1-step IQN; при identity-dynamics == n-step (sanity).
5. **reset**: параметры голов = свежая инициализация; энкодер сдвинут к init на α; PER/буфер сохранены;
   моменты AdamW сброшены для сброшенных параметров.
6. **аннелинг**: расписание n-step/γ выдаёт ожидаемые значения по шагам.
7. **sequence-replay**: возвращает связные `K+1`; на границе эпизода маскирует за `done`.
8. **config resolve**: приоритет env→секция→default (`resolve_phoenix_config`).
9. **allowlist-гейт**: `phoenix` присутствует во всех hardcoded-списках algo (защита от тихой подмены).
10. **state_dict arch-restore**: восстановление арх-параметров из чекпойнта.

---

## 7. Обработка ошибок / fallback

- **Граница эпизода** в последовательности: SPR/VE-члены за `done` маскируются (не предсказываем и не
  бутстрапим сквозь терминал).
- **Shape mismatch** при загрузке чекпойнта → понятная RU-ошибка fail-fast (что/где/что делать),
  без тихого мусора (см. [[eval-loader-shape-mismatch-failfast]]).
- **Deploy/eval-чекпойнт грузим частично:** на инференсе нужны только `encoder` + IQN-голова;
  `dynamics`/`projection`/`prediction`/`action-embed` — обучающая обвязка и в eval не требуются.
  RL-путь (encoder+IQN-голова) грузим **строго** (mismatch → fail-fast выше); SPR/dynamics-ключи —
  опционально (`strict=False`, отсутствие/лишние ключи допускаются). Стыкуется с планом eval-arch-parity.
- **Битый снапшот лиги/оппонента** → fallback на эвристику с `[PHOENIX][WARN]` (как в pool).
- **Reset-safety**: reset не внутри накопления градиента; целостность optimizer-state.
- **Distributed**: контракт-хэш и арх-параметры сети синхронизируются ПК1→ПК2 (как у DQN), иначе
  load_state_dict mismatch.

---

## 8. Критерии успеха (A/B vs текущий DQN, равный бюджет эпизодов)

- **Главное:** достичь того же WR-vs-эвристика за **≥1.5–2× меньше эпизодов** (sample-efficiency).
- **Не хуже:** `draw_rate` не растёт; стабильность на длинном прогоне (resets держат пластичность).
- **Стретч:** выше асимптотический WR.
- **Главная A/B-кнопка — `replay_ratio`:** дефолт 2 даёт лишь smoke-валидацию ядра; выигрыш
  sample-efficiency измеряется подъёмом RR до 8–16 (BBF-режим). Без подъёма RR §8 не закрывается.
- A/B-прогон — отдельная исследовательская активность после внедрения (как с opponent pool).

---

## 9. Декомпозиция на под-проекты и волны (для writing-plans)

Под-проекты:

1. **Ядро сети** (`phoenix_model.py`): encoder-reuse, IQN-голова, action-embed, dynamics, BYOL-головы,
   EMA-target, arch-restore. Тесты 1, 2, 10.
2. **Лоссы** (`phoenix_loss.py`): IQN-TD + value-expansion, SPR-consistency. Тесты 3, 4.
3. **Trainer + sequence-replay** (`phoenix_trainer.py`): learn-step, resets+shrink-perturb, аннелинги,
   sequence-буфер (sum-tree по началу окна, per-step маски). Тесты 5, 6, 7.
4. **Конфиг** (`resolve_phoenix_config`): секция + env + дефолты. Тест 8.
5. **Интеграция train.py + allowlist-гейты + opponent pool + логи.** Тест 9.
6. **Distributed (Ape-X)**: расширение протокола до последовательностей.
7. **Полноценная GUI-вкладка PHOENIX + help-карточка.**
8. **eval/play/viewer поддержка.**

Под-проекты 1–4 не зависят от движка и тестируются изолированно; 5–8 — интеграция.

**Разбиение на волны** (главное: отделить «учится ли алгоритм» от ортогональных классов багов):

- **Волна 1 — валидация гипотезы Варианта B (single-process):** под-проекты **1–5** + **минимальный
  eval/play-лоадер** (часть 8, нужен чтобы измерить WR-vs-эвристика и закрыть §8). Без него гипотезу
  не проверить.
  - **КРИТИЧНО ([[algo-allowlist-gates]]): «отложить GUI-вкладку» ≠ «отложить регистрацию `phoenix`».**
    ВСЕ hardcoded-allowlist-ы — `VALID_TRAIN_ALGOS`, реестр, списки источников оппонента (включая
    `pool`), algo-списки в `eval.py`/`play.py`/Viewer **и селекторы GUI** — должны получить `phoenix`
    **в волне 1**, иначе тихий fallback на dqn. **Тест 9 (защитный гейт) — обязателен в волне 1.**
    Откладывается только UI самой вкладки (под-проект 7), но НЕ запись `phoenix` в списки.
- **Волна 2 — масштаб и UX:** **distributed** (под-проект 6 — отдельный класс sync-багов, ортогонален
  вопросу «учится ли алгоритм») + полноценная **GUI-вкладка** (7) + остаток **Viewer/eval** (8).
