# Track 2 · 7b — PhaseEngine командное окно Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дать decision-seam в `command_phase` (`decide_bravery`) + тонкий `PhaseEngine.run_command`, исполняющий командную фазу через окно решений, не меняя поведение legacy `env.step`.

**Architecture:** `command_phase` получает необязательный `decide_bravery`; при `None` — текущая логика из `action` (1:1). `PhaseEngine.run_command(env, side, decide)` строит `command_window`, берёт выбранную опцию через `decide` и делегирует исполнение в `command_phase` (один источник истины).

**Tech Stack:** Python 3.12, pytest.

**Спека:** `docs/superpowers/specs/2026-06-17-track2-7b-phaseengine-command-design.md`.

## Global Constraints

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`.
- `core/engine/phases/*` не импортирует `core/envs/*`.
- **Инвариант:** `command_phase(decide_bravery=None)` идентичен текущему; **golden-trace (seed 12345) обязан остаться зелёным**.
- Хук `ruff_fix` срезает временно-неиспользуемые импорты — добавляй вместе с использованием / реэкспорт сразу в `__all__`.

## Известные факты (точные места)

- `command_phase` `core/envs/warhamEnv.py:4345`; bravery-блок `:4375-4398` (условие `if action and action.get("use_cp") == 1 and action.get("cp_on") == i:` → `_apply_stratagem(...)`).
- `_apply_stratagem` импортирован (Stage 6).
- `command_window(env, side)` → `DecisionWindow(options=[PASS, USE_STRATAGEM(unit_idx=i)...])`; `ActionKind.USE_STRATAGEM`, `ActionOption.unit_idx` — `core/engine/phases/`.
- golden-trace: `tests/engine/test_golden_trace_regression.py`.
- Детерминированный провал battle-shock: юнит ниже половины + `Ld=13` (2D6≤12 < 13).

## File Structure

- Modify `core/envs/warhamEnv.py` — `command_phase` + `decide_bravery`.
- Create `core/engine/phases/phase_engine.py` — `run_command(env, side, decide)`.
- Modify `core/engine/phases/__init__.py` — реэкспорт `phase_engine`.
- Create `tests/engine/phases/test_phase_engine_command.py`.

---

### Task 1: decision-seam `decide_bravery` в `command_phase`

**Files:**
- Modify: `core/envs/warhamEnv.py`
- Test: `tests/engine/phases/test_phase_engine_command.py`

**Interfaces:**
- Produces: `command_phase(self, side, action=None, manual=False, decide_bravery=None)`; при `decide_bravery` задан — bravery-решение = `bool(decide_bravery(i))`, иначе из `action`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_phase_engine_command.py`:

```python
from tests.engine.phases._helpers import build_env


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": use_cp, "cp_on": cp_on}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def _setup_failing_unit0(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_data[0]["Ld"] = 13  # 2D6 <= 12 < 13 → battle-shock всегда провален
    env.unit_health[0] = 1.0
    env.modelCP = 2


def test_decide_bravery_equivalent_to_action():
    n_env = build_env()
    _setup_failing_unit0(n_env)
    n = len(n_env.unit_health)
    snap = n_env.snapshot_state()

    with n_env.simulation_mode():
        bs_a, r_a = n_env.command_phase("model", action=_action(1, 0, n))
        cp_a, used_a = n_env.modelCP, list(n_env.stratagem_used)
    n_env.restore_state(snap)

    with n_env.simulation_mode():
        bs_b, r_b = n_env.command_phase("model", action=_action(0, 0, n), decide_bravery=lambda i: i == 0)
        cp_b, used_b = n_env.modelCP, list(n_env.stratagem_used)
    n_env.restore_state(snap)

    assert bs_a == bs_b
    assert r_a == r_b
    assert cp_a == cp_b
    assert used_a == used_b
    assert bs_a[0] is False  # bravery спасла юнит 0 в обоих путях


def test_decide_bravery_false_keeps_battleshock():
    env = build_env()
    _setup_failing_unit0(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()
    with env.simulation_mode():
        bs, _r = env.command_phase("model", action=_action(0, 0, n), decide_bravery=lambda i: False)
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert bs[0] is True
    assert used == []
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_phase_engine_command.py -v`
Expected: FAIL — `TypeError: command_phase() got an unexpected keyword argument 'decide_bravery'`.

- [ ] **Step 3: Добавить seam**

В `core/envs/warhamEnv.py` изменить сигнатуру:

```python
    def command_phase(self, side: str, action=None, manual: bool = False):
```
на
```python
    def command_phase(self, side: str, action=None, manual: bool = False, decide_bravery=None):
```

Заменить блок `:4375` (условие + тело bravery):

```python
                        if action and action.get("use_cp") == 1 and action.get("cp_on") == i:
                            _bravery = _apply_stratagem(self, "model", "insane_bravery", i)
```
на
```python
                        if decide_bravery is not None:
                            _use_bravery = bool(decide_bravery(i))
                        else:
                            _use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
                        if _use_bravery:
                            _bravery = _apply_stratagem(self, "model", "insane_bravery", i)
```

(Остальное тело bravery — `if _bravery["ok"]: ... else: ...` — без изменений.)

- [ ] **Step 4: Запустить тест — PASS**

Run: `python -m pytest tests/engine/phases/test_phase_engine_command.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Golden-trace + командные регрессии + коммит**

Run: `python -m pytest tests/engine/test_golden_trace_regression.py tests/engine/phases/test_command_bravery_via_engine.py -q`
Expected: PASS (поведение env.step не изменилось).

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_phase_engine_command.py
git commit -m "feat(phases): decision-seam decide_bravery в command_phase (Track 2/7b, behavior-neutral)"
```

---

### Task 2: `PhaseEngine.run_command` + реэкспорт + полная регрессия

**Files:**
- Create: `core/engine/phases/phase_engine.py`
- Modify: `core/engine/phases/__init__.py`
- Test: `tests/engine/phases/test_phase_engine_command.py`

**Interfaces:**
- Consumes: `command_window`, `ActionKind`, `command_phase(decide_bravery=...)`.
- Produces: `run_command(env, side, decide) -> tuple` — `decide(window) -> ActionOption`; делегирует исполнение в `command_phase`.

- [ ] **Step 1: Дописать тесты**

Дописать в `tests/engine/phases/test_phase_engine_command.py` (импорты — вместе с использованием):

```python
from core.engine.phases import phase_engine  # noqa: E402
from core.engine.phases.types import ActionKind  # noqa: E402


def _pick_bravery_for(unit_idx):
    def decide(window):
        for o in window.options:
            if o.kind is ActionKind.USE_STRATAGEM and o.unit_idx == unit_idx:
                return o
        return window.options[0]  # PASS
    return decide


def _pick_pass(window):
    return window.options[0]


def test_run_command_applies_bravery():
    env = build_env()
    _setup_failing_unit0(env)
    snap = env.snapshot_state()
    with env.simulation_mode():
        bs, _r = phase_engine.run_command(env, "model", _pick_bravery_for(0))
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert bs[0] is False
    assert ("model", "insane_bravery", env.battle_round) in used


def test_run_command_declines_bravery():
    env = build_env()
    _setup_failing_unit0(env)
    snap = env.snapshot_state()
    with env.simulation_mode():
        bs, _r = phase_engine.run_command(env, "model", _pick_pass)
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert bs[0] is True
    assert used == []
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_phase_engine_command.py -k run_command -v`
Expected: FAIL — `ImportError: cannot import name 'phase_engine'` (или AttributeError run_command).

- [ ] **Step 3: Реализовать `PhaseEngine.run_command`**

Создать `core/engine/phases/phase_engine.py`:

```python
from __future__ import annotations

from core.engine.phases.option_generator import command_window
from core.engine.phases.types import ActionKind


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def run_command(env, side, decide):
    """Исполнить командную фазу через окно решений.

    decide(window) -> ActionOption: выбирает одну опцию окна (PASS или USE_STRATAGEM).
    Исполнение делегируется command_phase (decide_bravery), без дублирования логики.
    """
    e = _unwrap(env)
    win = command_window(e, side)
    chosen = decide(win)
    chosen_units: set[int] = set()
    if chosen is not None and chosen.kind is ActionKind.USE_STRATAGEM and chosen.unit_idx is not None:
        chosen_units.add(int(chosen.unit_idx))
    return e.command_phase(side, decide_bravery=lambda i: i in chosen_units)
```

В `core/engine/phases/__init__.py` добавить реэкспорт модуля:

```python
from core.engine.phases import phase_engine
```

И в `__all__`: `"phase_engine"`.

- [ ] **Step 4: Запустить тесты — PASS**

Run: `python -m pytest tests/engine/phases/test_phase_engine_command.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Полная регрессия + golden-trace + ruff + импорт**

Run: `python -m pytest tests/engine/phases/ tests/engine/test_golden_trace_regression.py -q`
Expected: PASS (все).

Run: `python -c "import core.envs.warhamEnv; from core.engine.phases import phase_engine; print('ok')"`
Expected: `ok`.

Run: `python -m ruff check core/engine/phases/ tests/engine/phases/`
Expected: `All checks passed!`.

Run (контроль долга): `python -m ruff check core/envs/warhamEnv.py 2>&1 | grep -E "Found [0-9]+ error"`
Expected: не больше прежнего (~84).

- [ ] **Step 6: Коммит**

```bash
git add core/engine/phases/phase_engine.py core/engine/phases/__init__.py tests/engine/phases/test_phase_engine_command.py
git commit -m "feat(phases): PhaseEngine.run_command — командная фаза через окно решений (Track 2/7b)"
```

---

## Self-Review

**Spec coverage:**
- decision-seam `decide_bravery` (default = action, 1:1) → Task 1. ✓
- `PhaseEngine.run_command` (окно→decide→command_phase) → Task 2. ✓
- Тесты: seam equivalence + decline (T1), run_command applies/declines (T2), golden-trace + полная регрессия + ruff (T1 Step5, T2 Step5). ✓
- Инвариант behavior-neutral → golden-trace зелёный в обеих задачах. ✓

**Placeholder scan:** код полный; плейсхолдеров нет.

**Type consistency:** `command_phase(..., decide_bravery=None)`; `decide_bravery: (int)->bool`; `run_command(env, side, decide)` с `decide(window)->ActionOption`; `command_window`/`ActionKind`/`ActionOption.unit_idx` совпадают со Stage 5/6.

## Заметки по исполнению

- `decide_bravery` применяется только в model-ветке командной фазы (где живёт Insane Bravery). Enemy-ветки не трогаем.
- Сценарий теста: `Ld=13` → battle-shock всегда провален (детерминизм без контроля RNG).
- `run_command` возвращает то же, что `command_phase` (tuple `(battle_shock, reward_delta)`).
