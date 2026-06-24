# Движковый гейт command_reroll — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** Не предлагать command_reroll юниту без предстоящего броска (нет цели стрельбы/чарджа) → реролл нелегален в масках для всех алго → нет no-target waste.

**Architecture:** Один гейт в `command_reroll_options_for_unit` (`core/engine/phases/option_generator.py`), предикат — существующие `get_shoot_targets_for_unit`/`get_charge_targets_for_unit`.

**Tech Stack:** Python 3.12, pytest, движок 40kAI.

## Global Constraints

- Платформа Windows; язык RU. TDD (движок!). ruff чист. Коммит — только релевантный код.
- Не трогать reward/штрафы, FIGHT-реролл, прочие фазы.
- Сверить engine-baseline (частично красный) — не добавить падений.

---

### Task 1: Гейт + тесты

**Files:**
- Modify: `core/engine/phases/option_generator.py` (`command_reroll_options_for_unit`, после alive-check ~`:150`)
- Test: `tests/engine/phases/test_command_reroll_gate.py`

- [ ] **Step 1: Снять baseline релевантных тестов (ДО правки)**

Run:
```bash
python -m pytest tests/engine/phases/test_option_generator.py tests/engine/phases/test_stratagems.py tests/engine/phases/test_phase_engine_command.py tests/engine/test_command_reroll_wasted_penalty.py -q
```
Запомнить счётчик passed/failed (baseline).

- [ ] **Step 2: Написать падающий тест**

```python
# tests/engine/phases/test_command_reroll_gate.py
from core.engine.phases.option_generator import _unwrap, command_reroll_options_for_unit
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _eu_with_cp(monkeypatch, cp=5):
    env = build_env()
    eu = _unwrap(env)
    eu.modelCP = cp
    eu.enemyCP = cp
    return env, eu


def test_reroll_gated_when_no_shoot_target(monkeypatch):
    env, eu = _eu_with_cp(monkeypatch)
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound")) == []


def test_reroll_offered_when_has_shoot_target(monkeypatch):
    env, eu = _eu_with_cp(monkeypatch)
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [1])
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound"))
    assert len(opts) == 2  # hit + wound


def test_reroll_gated_when_no_charge_target(monkeypatch):
    env, eu = _eu_with_cp(monkeypatch)
    monkeypatch.setattr(eu, "get_charge_targets_for_unit", lambda side, idx: [])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.CHARGE, rolls=("charge",)) == []


def test_reroll_offered_when_has_charge_target(monkeypatch):
    env, eu = _eu_with_cp(monkeypatch)
    monkeypatch.setattr(eu, "get_charge_targets_for_unit", lambda side, idx: [2])
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.CHARGE, rolls=("charge",))
    assert len(opts) == 1


def test_cp_gate_still_blocks_even_with_target(monkeypatch):
    env, eu = _eu_with_cp(monkeypatch, cp=0)
    monkeypatch.setattr(eu, "get_shoot_targets_for_unit", lambda side, idx: [1])
    assert command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound")) == []
```

- [ ] **Step 3: Запустить — упадёт** (`test_reroll_gated_when_no_shoot_target` / charge провалятся: сейчас реролл предлагается без цели).

Run: `python -m pytest tests/engine/phases/test_command_reroll_gate.py -q` → FAIL.

- [ ] **Step 4: Реализовать гейт** — в `command_reroll_options_for_unit`, ПОСЛЕ alive-check (после строки `if not (0 <= i < len(health)) or health[i] <= 0: return []`), ДО `options: list[ActionOption] = []`:

```python
    # Гейт «нет цели — нет реролла»: не предлагаем command_reroll, если у юнита нет предстоящего
    # броска в этой фазе (нет валидной цели стрельбы/чарджа) — иначе CP тратится впустую (wasted).
    if phase is Phase.SHOOTING and not e.get_shoot_targets_for_unit(side, i):
        return []
    if phase is Phase.CHARGE and not e.get_charge_targets_for_unit(side, i):
        return []
```

- [ ] **Step 5: Запустить тест гейта — зелёный**

Run: `python -m pytest tests/engine/phases/test_command_reroll_gate.py -q` → 5 passed.

- [ ] **Step 6: Регресс — сверить с baseline (Step 1)**

Run (те же файлы, что в Step 1) → счётчик passed/failed **не хуже** baseline. Новых падений нет.

- [ ] **Step 7: ruff + коммит**

```bash
python -m ruff check core/engine/phases/option_generator.py
git add core/engine/phases/option_generator.py tests/engine/phases/test_command_reroll_gate.py
git commit -m "feat(engine): гейт command_reroll — нелегален без цели стрельбы/чарджа (no-target waste)"
```

## Definition of Done

- 5 гейт-тестов зелёные; релевантные engine-тесты не хуже baseline; ruff чист; коммит только кода.
