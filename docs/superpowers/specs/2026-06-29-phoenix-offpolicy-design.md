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
- **IQN RL-голова** — существующий `_DQNHeadBundle` (IQN-путь) на `z`. Dueling/Noisy — опции (по
  умолчанию как у DQN). Per-head квантили `Q(z, ·)`.
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

### 3.2 SPR consistency
- Для `k=1..K`: нормированная косинус-дистанция между `q(p(ẑ_{t+k}))` и `sg(p_m(f_m(o_{t+k})))`.
- Маска по `done`: за терминалом эпизода k-члены не считаются.
- Градиент **не течёт** в target-ветку (EMA + stop-grad).

### 3.3 Итог
`L = L_IQN + λ_spr · L_spr`. Оптимизатор **AdamW** (weight decay — BBF-регуляризация).
Дефолты: `spr_coef(λ_spr)=2.0`, `spr_horizon_K=5`, `ve_horizon=3`.

---

## 4. Рецепт обучения (BBF)

Модуль: `core/models/phoenix_trainer.py` (learn-step, resets, аннелинги) + sequence-replay.

- **Sequence-replay:** буфер хранит связные траектории, сэмплит окно длиной `H+1` подряд, где
  `H = max(spr_horizon_K, ve_horizon)` (по умолчанию `H=5`). Приоритет (PER, reuse существующего) —
  по TD-ошибке первого перехода. На границе эпизода окно маскируется по `done`.
- **Высокий replay ratio** — `replay_ratio` градиентных апдейтов на каждый env-шаг (дефолт 2; в A/B
  поднимаем).
- **Periodic resets** — каждые `reset_interval` градиентных шагов:
  - полный reset голов (IQN-голова, projection/prediction, dynamics, action-embed) к свежей
    инициализации;
  - **shrink-and-perturb** энкодера: `w ← α·w + (1−α)·φ`, `φ` — случайная инициализация, `α=shrink_alpha` (0.5);
  - ре-синк target-сетей (RL-target и SPR `f_m`/`p_m`);
  - сброс моментов AdamW для сброшенных параметров;
  - reset запрещён внутри накопления градиента (между полными шагами).
- **Аннелинг** после каждого reset: n-step `nstep_start→nstep_end` (10→3), γ `gamma_start→gamma_end`
  (0.97→0.997), экспоненциально за фиксированное число шагов.
- **Target EMA** — отдельные коэффициенты для RL-target и SPR-энкодера (`target_ema`).

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
- **Битый снапшот лиги/оппонента** → fallback на эвристику с `[PHOENIX][WARN]` (как в pool).
- **Reset-safety**: reset не внутри накопления градиента; целостность optimizer-state.
- **Distributed**: контракт-хэш и арх-параметры сети синхронизируются ПК1→ПК2 (как у DQN), иначе
  load_state_dict mismatch.

---

## 8. Критерии успеха (A/B vs текущий DQN, равный бюджет эпизодов)

- **Главное:** достичь того же WR-vs-эвристика за **≥1.5–2× меньше эпизодов** (sample-efficiency).
- **Не хуже:** `draw_rate` не растёт; стабильность на длинном прогоне (resets держат пластичность).
- **Стретч:** выше асимптотический WR.
- A/B-прогон — отдельная исследовательская активность после внедрения (как с opponent pool).

---

## 9. Декомпозиция на под-проекты (для writing-plans)

1. **Ядро сети** (`phoenix_model.py`): encoder-reuse, IQN-голова, action-embed, dynamics, BYOL-головы,
   EMA-target, arch-restore. Тесты 1, 2, 10.
2. **Лоссы** (`phoenix_loss.py`): IQN-TD + value-expansion, SPR-consistency. Тесты 3, 4.
3. **Trainer + sequence-replay** (`phoenix_trainer.py`): learn-step, resets+shrink-perturb, аннелинги,
   replay-окна. Тесты 5, 6, 7.
4. **Конфиг** (`resolve_phoenix_config`): секция + env + дефолты. Тест 8.
5. **Интеграция train.py + allowlist-гейты + opponent pool + логи.** Тест 9.
6. **Distributed (Ape-X) расширение протокола до последовательностей.**
7. **GUI-вкладка + help-карточка.**
8. **eval/play/viewer поддержка.**

Под-проекты 1–4 не зависят от движка и тестируются изолированно; 5–8 — интеграция.
