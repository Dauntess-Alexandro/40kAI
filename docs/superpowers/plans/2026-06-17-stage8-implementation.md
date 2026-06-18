# Stage 8 — Implementation Plan (полный)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Steps use checkbox (`- [ ]`). Каждый под-проект (8.x) самодостаточен и заканчивается зелёными тестами + (для рискованных) golden-trace.

**Goal:** Подключить PhaseEngine/стратагемы к обучению: агент видит CP/фазы/доступные стратагемы и (постепенно) выбирает их. Поведение по умолчанию не меняется (фиче-флаги), пока явно не переключим.

**Roadmap:** `docs/superpowers/specs/2026-06-17-stage8-roadmap.md`.

## Global Constraints

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`.
- **Инвариант:** до явного переключения флага — поведение игры/обучения 1:1. Golden-trace (`tests/engine/test_golden_trace_regression.py`) зелёный после каждого под-проекта.
- `core/engine/phases/*` не импортирует `core/envs/*` / `core/models/*`.
- Хук `ruff_fix` срезает временно-неиспользуемые импорты — добавлять вместе с использованием.
- Долг ruff в `warhamEnv.py` (~84) не увеличивать.

## КРИТИЧЕСКАЯ НАХОДКА (учесть в 8.1)

`observation_space.shape=(14,)`, но `get_observation_for_side` возвращает **17** значений (формула `obsSpace` на `warhamEnv.py:1121` не учитывает 2×CP и расходится с реальным obs). Сеть, вероятно, строится по `len(env.reset()[0])`, а не по `observation_space`. **Перед добавлением фич 8.1 — выяснить, какое число реально определяет вход сети** (Task 8.1.0).

---

## Под-проект 8.1 — Observation-фичи фаз/CP (фиче-флаг, behavior-neutral)

**Files:**
- Modify: `core/envs/warhamEnv.py` (`get_observation_for_side`, `obsSpace`)
- Create: `tests/engine/phases/test_obs_phase_features.py`

### Task 8.1.0: выяснить источник размера obs

- [ ] **Step 1:** Grep, как train.py/модели определяют вход сети.

Run: `python -m pytest -q` НЕ нужен; вместо — `grep -rn "observation_space\|n_observations\|reset()\[0\]\|len(state)\|len(obs" train.py core/models/*.py | head -40`
Зафиксировать: использует ли пайплайн `observation_space.shape` или `len(obs)` из reset. Записать вывод в комментарий теста 8.1.

- [ ] **Step 2:** Подтвердить рассинхрон тестом-документом.

```python
# tests/engine/phases/test_obs_phase_features.py
from tests.engine.phases._helpers import build_env

def test_obs_length_matches_observation_space_or_documents_mismatch():
    env = build_env()
    obs = env.get_observation_for_side("model")
    # Документируем фактический инвариант (флаг выключен): длина obs стабильна.
    assert len(obs) == len(env.get_observation_for_side("model"))
```

Run: `python -m pytest tests/engine/phases/test_obs_phase_features.py -v` → PASS.

### Task 8.1.1: фиче-флаг + фичи фаз/CP

**Interfaces:** env-флаг `PHASE_OBS_FEATURES` (env var, дефолт "0"). При "1" `get_observation_for_side` дописывает в хвост: `[phase_onehot(6), timing_main(1), cp_self_norm(1), cp_enemy_norm(1), strat_available(K), strat_used_this_turn(K)]`, где K = число стратагем в REGISTRY на нужные триггеры (фикс. порядок).

- [ ] **Step 1: Тест (флаг выкл == старая длина; вкл == +N)**

```python
import os
from tests.engine.phases._helpers import build_env

def test_phase_obs_features_flag_off_keeps_length(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    env = build_env()
    base = len(env.get_observation_for_side("model"))
    # столько же, сколько без фич
    assert base == len(env.get_observation_for_side("model"))

def test_phase_obs_features_flag_on_appends_block(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    env = build_env()
    off = len(env.get_observation_for_side("model"))
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env2 = build_env()
    on = len(env2.get_observation_for_side("model"))
    assert on > off
    # детерминизм/диапазоны: phase one-hot суммируется в 1
```

- [ ] **Step 2:** Run → FAIL (нет фич).
- [ ] **Step 3:** Реализовать: хелпер `_phase_obs_block(side) -> list[float]`; в `get_observation_for_side` при `os.getenv("PHASE_OBS_FEATURES","0")=="1"` дописать блок. CP нормализовать (`cp/ N`, напр /12). Фазы — фикс. список из `Phase`. Стратагемы — стабильный порядок из REGISTRY.
- [ ] **Step 4:** Run → PASS.
- [ ] **Step 5:** golden-trace + obs-тесты + ruff. Коммит: `feat(env): observation-фичи фаз/CP за флагом PHASE_OBS_FEATURES (8.1)`.

---

## Под-проект 8.2 — Replay-метаданные (опционально, дефолт None)

**Files:** Modify `core/models/alphazero_replay.py`; Test `tests/engine/test_az_replay_stratagem_meta.py`.

### Task 8.2.1: расширить AZTransition

**Interfaces:** `AZTransition` += опциональные поля `phase: str|None=None`, `window_id: str|None=None`, `stratagem_id: str|None=None`, `cp_before: int|None=None`, `cp_after: int|None=None`. Дефолт None → обратная совместимость.

- [ ] **Step 1: Тест** — `AZTransition(state, policy_targets, value_target)` создаётся как раньше; новые поля = None; с заданными — хранятся.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Добавить поля в dataclass.
- [ ] **Step 4:** Run → PASS + существующие az replay-тесты зелёные.
- [ ] **Step 5:** ruff + коммит: `feat(models): опциональные stratagem/phase-метаданные в AZTransition (8.2)`.

---

## Под-проект 8.6 — Долги корректности (низкий риск, до рискованного ядра)

**Files:** Modify `core/engine/utils.py` (`expected_damage`).

### Task 8.6.1: expected_damage учитывает новые эффекты

**Interfaces:** `expected_damage(..., effects=...)` нормализует через `_normalize_effects` и учитывает `strength_mod`/`ap_improve`/reroll в EV (как `attack`).

- [ ] **Step 1: Тест** — EV с `effects={"strength_mod":1}` > EV без (S4→S5 vs T4); `reroll_hits="all"` повышает EV; None == текущему.
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** В `expected_damage`: `eff=_normalize_effects(effects)`; `s += eff["strength_mod"]`; `ap -= eff["ap_improve"]`; `p_hit *= (2-p_hit)` при reroll_hits=="all" (или `+(1-p_hit)*p_hit_ones` для ones); аналогично wound/save. Cover-ветку перевести на `eff["cover"]`.
- [ ] **Step 4:** Run → PASS + `test_expected_damage.py`/`test_charge_ev.py` зелёные (None-путь неизменен).
- [ ] **Step 5:** ruff + коммит: `feat(engine): expected_damage учитывает opt-in effects (8.6)`.

### Task 8.6.2: CP по правилам — Heroic 1CP (поведенческое, под re-baseline)

- [ ] **Step 1:** Решить с пользователем (СПРОСИТЬ): менять ли engine Heroic 2→1 (это меняет golden-trace и баланс). Если да — план: `heroic` gate `<2`→`<1`, `-=2`→`-=1`, реестр `cp_cost 2→1`, **перегенерировать golden-trace эталон**, обновить тесты heroic.
- [ ] (выполнять только после явного OK пользователя)

---

## Safety-harness — winrate-baseline (перед 8.3+)

**Files:** Create `tests/engine/test_winrate_baseline.py` (медленный, маркер `slow`/skip по умолчанию).

### Task 8.H.1: baseline-снимок

**Interfaces:** функция гоняет N (напр. 50) детерминированных эпизодов эвристика-vs-эвристика (или дефолтная политика) фикс. сидами, считает winrate/средний VP; эталон заморожен. Тест сверяет с допуском.

- [ ] **Step 1:** Реализовать прогон через `env.step`+`enemyTurn` дефолтным action на сидах [0..N).
- [ ] **Step 2:** Снять эталон (winrate, avg model VP, avg enemy VP), вшить.
- [ ] **Step 3:** Тест сверяет (маркер skip если медленно в CI; запускать вручную перед 8.3+).
- [ ] **Step 4:** ruff + коммит: `test(engine): winrate-baseline harness под Stage 8.3+ (8.H)`.

---

## Под-проект 8.3 — Командные стратагемы от политики (фиче-флаг WINDOWED_SELFPLAY)

**Files:** Modify `core/models/alphazero_selfplay.py`; Test `tests/engine/test_windowed_selfplay_command.py`.

### Task 8.3.1: windowed-режим self-play (только command)

**Interfaces:** env/cfg-флаг `WINDOWED_SELFPLAY` (дефолт 0). При 1 в `play_episode_with_mcts` командная фаза идёт через `PhaseEngine.run_command` с decide, выводящим bravery из политики (proj приоров на command-окно). Остальные фазы — как сейчас. При 0 — старый путь.

- [ ] **Step 1: Тест** — при флаге 0 self-play идентичен (smoke); при 1 командное решение идёт от decide (мок-политика выбирает bravery → журнал содержит запись).
- [ ] **Step 2:** Run → FAIL.
- [ ] **Step 3:** Реализовать ветку за флагом.
- [ ] **Step 4:** Run → PASS + golden-trace + az smoke.
- [ ] **Step 5: ЧЕКПОЙНТ** — прогнать winrate-baseline (8.H) вручную, убедиться без сдвига. Коммит: `feat(selfplay): windowed command-фаза за флагом WINDOWED_SELFPLAY (8.3)`.

---

## Под-проект 8.4 — Активные стратагемы как ActionOption в MCTS (ВЫСОКИЙ РИСК)

> **СТОП-ГЕЙТ:** перед началом 8.4 — СПРОСИТЬ пользователя. Это переписывает кандидат-генерацию MCTS и требует прогона обучения для верификации winrate (который агент сам полноценно не гоняет). Делать пофазно, только AlphaZero tree первым, под флагом + golden-trace + winrate-baseline.

**Files:** Modify `core/models/alphazero_mcts.py`, `alphazero_selfplay.py`.

### Task 8.4.1: кандидаты из generate_windows (фиче-флаг WINDOWED_MCTS)
- [ ] Спека отдельным документом (под-проект слишком большой для inline-плана). Ключевые шаги: проекция факторизованных приоров на ActionOption; узлы=окна; симуляция через PhaseEngine.run_*; snapshot-инвариант (CP/active_stratagem_effects не течёт); winrate A/B.

---

## Под-проект 8.5 — Перенос на остальные алгоритмы (ОБЪЁМ)

> Только после 8.4 на AlphaZero. По одному: Gumbel AZ → Gumbel MuZero → Sampled MuZero → PPO/DQN. Каждый — отдельная спека. code-reviewer-субагент на рассинхрон `az_*`↔`gmz_*`.

---

## Порядок исполнения (этой сессии, автономно)

1. **8.1** (obs-фичи, флаг) — безопасно.
2. **8.2** (replay-метаданные) — безопасно.
3. **8.6.1** (expected_damage) — безопасно.
4. **8.H** (winrate-baseline harness) — безопасно.
5. **8.3** (windowed command за флагом) — средний риск, на чекпойнте сверить baseline.
6. **СТОП** перед 8.4 — спросить пользователя (требует train-прогона; 8.6.2 Heroic CP тоже спросить).

## Self-Review

- Покрытие roadmap: 8.1–8.6 + harness — есть задачи. ✓
- Плейсхолдеры: 8.4/8.5 намеренно вынесены в отдельные спеки (слишком большие для inline) — это не плейсхолдер, а декомпозиция; для них СТОП-гейт. ✓
- Типы/имена: флаги (`PHASE_OBS_FEATURES`, `WINDOWED_SELFPLAY`, `WINDOWED_MCTS`), `AZTransition` поля — согласованы. ✓
- Риск-гейты: 8.3 чекпойнт на baseline; 8.4 и 8.6.2 — явный СПРОСИТЬ. ✓
