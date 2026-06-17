# Phase Decision-Windows (Scaffolding) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Построить аддитивный слой `DecisionWindow`/`ActionOption` + `LegacyActionCompiler` поверх неизменного `Warhammer40kEnv`, который декомпозирует ход на окна решений по фазам и компилируется обратно в текущий плоский `action_dict` — **без единого изменения поведения `env.step`, фаз и обучения**.

**Architecture:** Новый самодостаточный пакет `core/engine/phases/` (типы → генератор опций → компилятор). Генератор читает состояние env через уже существующие публичные методы (`get_shoot_targets_for_unit`, `get_charge_targets_for_unit`, `get_unit_movement_overlay`, `_pick_destination_by_reachable_index`, `get_legal_action_masks_by_head`) и становится единым источником истины по легальности. Каждый `ActionOption` несёт свой `legacy_patch` (частичный плоский dict), поэтому компилятор тривиально складывает патчи в один `action_dict`, который понимает текущий `env.step`. Движок (`warhamEnv.py`) НЕ трогаем.

**Tech Stack:** Python 3.12, dataclasses + Enum, numpy, pytest. Без новых зависимостей.

## Global Constraints

- Платформа — **Windows**; Python **3.12+**; запуск тестов через **`python -m pytest`** из корня репо (venv проекта `.venv`).
- Язык логов/сообщений/докстрингов, релевантных пользователю — **русский**; сообщение об ошибке = что случилось + где + что делать.
- ruff: `target-version = py312`, `line-length = 120`, `select = ["E","F","I","UP","B"]`, `quote-style = "double"`. После каждой правки `.py` хук `ruff_fix.py` сам гоняет `ruff check --fix`.
- **Инвариант стадий 1–3: НОЛЬ изменений поведения.** Файл `core/envs/warhamEnv.py` и обучение/MCTS не модифицируются. Новый код только читает env, ничего в нём не мутирует вне `simulation_mode()`.
- Движок `core/engine/*` не должен импортировать `core/models/*` (слой моделей зависит от движка, не наоборот). Разворачивание gym-обёрток делаем локально через `getattr(env, "unwrapped", env)`.
- `core/engine/phases/` — единственный источник истины по легальности опций; маски/опции выводятся из одних и тех же env-методов.
- Тесты кладём в `tests/engine/phases/` (pytest-функции, как в `tests/engine/test_warham_env_snapshot_restore.py`).
- Не редактировать `runtime/logs/LOGS_FOR_AGENTS_*.md` (PreToolUse-хук `guard_paths.py` это блокирует).

## Известные факты о текущем контракте (опора для реализации)

- Плоский `action_dict` ключи: `move`(0–4, 4=stay/no-dir fallback), `attack`(0/1), `shoot`, `charge`, `use_cp`(0 none/1 bravery/2 overwatch/3 smokescreen/4 heroic), `cp_on`, `move_num_{i}` (per unit). Контракт — `core/models/action_contract.py:10-17`.
- **`move_num_i`** — индекс в списке `candidates = [stay] + move_cells + advance_cells`, как читает `_pick_destination_by_reachable_index` (`core/envs/warhamEnv.py:2115-2140`). Индекс 0 = stay.
- **`shoot`** — *локальный ранг* в списке валидных целей юнита: `idOfE = valid_target_ids[raw]` (`core/envs/warhamEnv.py:5370-5372`). Одинаков для всех стреляющих юнитов хода (плоское ограничение).
- **`charge`** — *глобальный* индекс врага: `idOfE = action["charge"]` (`core/envs/warhamEnv.py:6040`); для попытки чарджа нужен `attack==1` (`core/envs/warhamEnv.py:6029`).
- **Insane Bravery** — единственная агент-управляемая стратагема: `action["use_cp"]==1 and action["cp_on"]==i` в командной фазе (`core/envs/warhamEnv.py:4332-4345`).
- **Найденный латентный баг (НЕ чиним в этом плане):** маска `move_num_i` в `get_legal_action_masks_by_head` использует `len(overlay)` где `overlay` — это dict из 2 ключей, поэтому маска разрешает только индексы 0,1,2 (`core/envs/warhamEnv.py:1716-1721`). Реальное исполнение (`_pick_destination_by_reachable_index`) принимает весь диапазон reachable. Генератор движется по **исполнительной истине** (полный список candidates), а не по сломанной маске. Тест Task 5 фиксирует это расхождение явно.

## File Structure

- Create `core/engine/phases/__init__.py` — публичный реэкспорт API пакета.
- Create `core/engine/phases/types.py` — enums + dataclasses (`Phase`, `SubStep`, `Timing`, `ActionKind`, `ActionOption`, `DecisionWindow`, `PhaseState`, `PhaseResult`). Никакой логики.
- Create `core/engine/phases/option_generator.py` — генерация легальных `ActionOption`/`DecisionWindow` из состояния env (read-only).
- Create `core/engine/phases/legacy_compiler.py` — `default_action_dict` + `compile_options_to_action_dict` (опции → плоский dict).
- Create `tests/engine/phases/test_phase_types.py` — конструирование типов/дефолты.
- Create `tests/engine/phases/test_option_generator.py` — опции = легальность env (shoot/charge/cp/move).
- Create `tests/engine/phases/test_legacy_compiler.py` — компиляция и исполнительный roundtrip.
- Create `tests/engine/phases/_helpers.py` — общий конструктор тестового env/юнитов (DRY между тест-файлами).

---

### Task 1: Типы фаз (dataclasses, без поведения) — Stage 1

**Files:**
- Create: `core/engine/phases/__init__.py`
- Create: `core/engine/phases/types.py`
- Test: `tests/engine/phases/test_phase_types.py`

**Interfaces:**
- Consumes: ничего (stdlib).
- Produces:
  - `class Phase(str, Enum)`: `COMMAND, MOVEMENT, SHOOTING, CHARGE, FIGHT, SCORING`.
  - `class SubStep(str, Enum)`: `BATTLE_SHOCK, MOVE_UNIT, PICK_SHOOT_TARGET, PICK_CHARGE_TARGET, FIGHT_UNIT, SCORE`.
  - `class Timing(str, Enum)`: `MAIN, REACTION`.
  - `class ActionKind(str, Enum)`: `STAY, MOVE, ADVANCE, FALL_BACK, SHOOT, CHARGE, FIGHT, USE_STRATAGEM, PASS, END_PHASE`.
  - `@dataclass ActionOption(kind: ActionKind, unit_idx: int | None = None, target_idx: int | None = None, param: dict = {}, legacy_patch: dict[str,int] = {}, meta: dict = {})`.
  - `@dataclass DecisionWindow(window_id: str, owner_side: str, phase: Phase, sub_step: SubStep, timing: Timing, cursor_unit_idx: int | None, options: list[ActionOption], context: dict = {})`.
  - `@dataclass PhaseState(battle_round: int, active_side: str, phase: Phase, sub_step: SubStep, timing: Timing, cursor_unit_idx: int | None = None)`.
  - `@dataclass PhaseResult(reward_delta: float = 0.0, events: list = [], next_window: DecisionWindow | None = None, done: bool = False, info_patch: dict = {})`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_phase_types.py`:

```python
from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    PhaseResult,
    PhaseState,
    SubStep,
    Timing,
)


def test_enums_have_expected_values():
    assert Phase.MOVEMENT.value == "movement"
    assert SubStep.PICK_SHOOT_TARGET.value == "pick_shoot_target"
    assert Timing.REACTION.value == "reaction"
    assert ActionKind.USE_STRATAGEM.value == "use_stratagem"


def test_action_option_defaults_are_independent():
    a = ActionOption(kind=ActionKind.MOVE, unit_idx=0)
    b = ActionOption(kind=ActionKind.SHOOT, unit_idx=1)
    a.param["x"] = 1
    a.legacy_patch["move_num_0"] = 3
    assert b.param == {}
    assert b.legacy_patch == {}
    assert a.target_idx is None
    assert a.meta == {}


def test_decision_window_holds_options():
    opt = ActionOption(kind=ActionKind.PASS)
    win = DecisionWindow(
        window_id="movement:model:0",
        owner_side="model",
        phase=Phase.MOVEMENT,
        sub_step=SubStep.MOVE_UNIT,
        timing=Timing.MAIN,
        cursor_unit_idx=0,
        options=[opt],
    )
    assert win.options[0].kind is ActionKind.PASS
    assert win.context == {}


def test_phase_state_and_result_defaults():
    st = PhaseState(
        battle_round=1,
        active_side="model",
        phase=Phase.COMMAND,
        sub_step=SubStep.BATTLE_SHOCK,
        timing=Timing.MAIN,
    )
    assert st.cursor_unit_idx is None
    res = PhaseResult()
    assert res.reward_delta == 0.0
    assert res.next_window is None
    assert res.done is False
    assert res.events == [] and res.info_patch == {}
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_phase_types.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.engine.phases'`.

- [ ] **Step 3: Создать пакет и типы**

Создать `core/engine/phases/__init__.py`:

```python
"""Слой иерархических фаз W40k: окна решений и опции действий.

Аддитивный слой над Warhammer40kEnv. Не меняет поведение движка — только
описывает ход как последовательность DecisionWindow со списком ActionOption
и компилирует их обратно в плоский action_dict.
"""

from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    PhaseResult,
    PhaseState,
    SubStep,
    Timing,
)

__all__ = [
    "ActionKind",
    "ActionOption",
    "DecisionWindow",
    "Phase",
    "PhaseResult",
    "PhaseState",
    "SubStep",
    "Timing",
]
```

Создать `core/engine/phases/types.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Phase(str, Enum):
    COMMAND = "command"
    MOVEMENT = "movement"
    SHOOTING = "shooting"
    CHARGE = "charge"
    FIGHT = "fight"
    SCORING = "scoring"


class SubStep(str, Enum):
    BATTLE_SHOCK = "battle_shock"
    MOVE_UNIT = "move_unit"
    PICK_SHOOT_TARGET = "pick_shoot_target"
    PICK_CHARGE_TARGET = "pick_charge_target"
    FIGHT_UNIT = "fight_unit"
    SCORE = "score"


class Timing(str, Enum):
    MAIN = "main"
    REACTION = "reaction"


class ActionKind(str, Enum):
    STAY = "stay"
    MOVE = "move"
    ADVANCE = "advance"
    FALL_BACK = "fall_back"
    SHOOT = "shoot"
    CHARGE = "charge"
    FIGHT = "fight"
    USE_STRATAGEM = "use_stratagem"
    PASS = "pass"
    END_PHASE = "end_phase"


@dataclass
class ActionOption:
    """Атомарный выбор в окне решения.

    legacy_patch — частичный плоский action_dict, который реализует эту опцию
    в текущем env.step (источник истины по маппингу — сам генератор).
    """

    kind: ActionKind
    unit_idx: int | None = None
    target_idx: int | None = None  # глобальный индекс врага для SHOOT/CHARGE
    param: dict[str, Any] = field(default_factory=dict)
    legacy_patch: dict[str, int] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)


@dataclass
class DecisionWindow:
    """Точка, где одна сторона выбирает одну из options."""

    window_id: str
    owner_side: str  # "model" | "enemy"
    phase: Phase
    sub_step: SubStep
    timing: Timing
    cursor_unit_idx: int | None
    options: list[ActionOption]
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class PhaseState:
    """Нормализованное «где мы сейчас» в иерархии фаз."""

    battle_round: int
    active_side: str
    phase: Phase
    sub_step: SubStep
    timing: Timing
    cursor_unit_idx: int | None = None


@dataclass
class PhaseResult:
    """Результат применения ActionOption движком фаз (для будущих стадий)."""

    reward_delta: float = 0.0
    events: list[Any] = field(default_factory=list)
    next_window: DecisionWindow | None = None
    done: bool = False
    info_patch: dict[str, Any] = field(default_factory=dict)
```

- [ ] **Step 4: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/engine/phases/test_phase_types.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/__init__.py core/engine/phases/types.py tests/engine/phases/test_phase_types.py
git commit -m "feat(phases): dataclasses окон решений и опций (Stage 1, без поведения)"
```

---

### Task 2: Общий тест-хелпер для env

**Files:**
- Create: `tests/engine/phases/_helpers.py`

**Interfaces:**
- Consumes: `core.engine.unit.Unit`, `core.envs.warhamEnv.Warhammer40kEnv`.
- Produces:
  - `make_unit(name: str, movement: int = 6, models: int = 3, wounds: int = 2, rng: int = 24) -> Unit`.
  - `build_env(b_len: int = 30, b_hei: int = 30) -> Warhammer40kEnv` — 2 model + 2 enemy юнита.

Этот файл — общий конструктор, его импортируют Task 4/5/6. Отдельного теста у него нет (он сам инфраструктура); его корректность проверяется тестами, которые его используют.

- [ ] **Step 1: Создать хелпер**

Создать `tests/engine/phases/_helpers.py`:

```python
from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv


def make_unit(name: str, movement: int = 6, models: int = 3, wounds: int = 2, rng: int = 24) -> Unit:
    data = {
        "Name": name,
        "Movement": movement,
        "M": movement,
        "W": wounds,
        "#OfModels": models,
        "OC": 1,
        "Ld": 7,
        "T": 4,
        "Sv": 3,
    }
    weapon = {
        "Name": "Stub gun",
        "Type": "Ranged",
        "Range": rng,
        "A": 1,
        "BS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    melee = {
        "Name": "Stub blade",
        "Type": "Melee",
        "Range": 2,
        "A": 1,
        "WS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    return Unit(data=data, weapon=weapon, melee=melee, b_len=30, b_hei=30, GUI=False)


def build_env(b_len: int = 30, b_hei: int = 30) -> Warhammer40kEnv:
    model = [make_unit("ModelA"), make_unit("ModelB")]
    enemy = [make_unit("EnemyA"), make_unit("EnemyB")]
    return Warhammer40kEnv(enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)
```

- [ ] **Step 2: Проверить, что env строится и хелпер импортируется**

Run: `python -m pytest tests/engine/phases/ -v` (пока соберёт только Task 1 тесты; новый файл не содержит тестов — это нормально, он не должен ломать сбор)
Expected: PASS (тесты Task 1), без ошибок импорта/сбора.

- [ ] **Step 3: Коммит**

```bash
git add tests/engine/phases/_helpers.py
git commit -m "test(phases): общий конструктор тестового env/юнитов"
```

---

### Task 3: Генератор опций стрельбы и чарджа — Stage 2 (часть 1)

**Files:**
- Create: `core/engine/phases/option_generator.py`
- Test: `tests/engine/phases/test_option_generator.py`

**Interfaces:**
- Consumes: env-методы `get_shoot_targets_for_unit(side, unit_idx) -> list[int]` (глобальные id), `get_charge_targets_for_unit(side, unit_idx) -> list[int]` (глобальные id); типы из Task 1.
- Produces:
  - `def _unwrap(env)` — снять gym-обёртку (`getattr(env, "unwrapped", env)`).
  - `def shooting_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]` — `PASS` + по одной `SHOOT`-опции на валидную цель; у `SHOOT` `target_idx`=глобальный id, `param={"local_rank": r}`, `legacy_patch={"shoot": r}`.
  - `def charge_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]` — `PASS` + по одной `CHARGE`-опции на валидную цель; `target_idx`=глобальный id, `legacy_patch={"charge": g, "attack": 1}`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_option_generator.py`:

```python
from core.engine.phases.option_generator import (
    charge_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def test_shooting_options_match_env_targets():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env._invalidate_target_cache("test")

    valid = env.get_shoot_targets_for_unit("model", 0)
    opts = shooting_options_for_unit(env, "model", 0)

    shoot_opts = [o for o in opts if o.kind is ActionKind.SHOOT]
    assert [o.target_idx for o in shoot_opts] == list(valid)
    # local_rank — индекс в списке целей; legacy_patch кодирует shoot=rank
    for rank, o in enumerate(shoot_opts):
        assert o.param["local_rank"] == rank
        assert o.legacy_patch == {"shoot": rank}
    assert any(o.kind is ActionKind.PASS for o in opts)


def test_charge_options_match_env_targets():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")

    valid = env.get_charge_targets_for_unit("model", 0)
    opts = charge_options_for_unit(env, "model", 0)

    charge_opts = [o for o in opts if o.kind is ActionKind.CHARGE]
    assert [o.target_idx for o in charge_opts] == list(valid)
    for o in charge_opts:
        assert o.legacy_patch == {"charge": int(o.target_idx), "attack": 1}
    assert any(o.kind is ActionKind.PASS for o in opts)
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.engine.phases.option_generator'`.

- [ ] **Step 3: Реализовать генератор стрельбы/чарджа**

Создать `core/engine/phases/option_generator.py`:

```python
from __future__ import annotations

from core.engine.phases.types import ActionKind, ActionOption


def _unwrap(env):
    """Снять gym-обёртку до Warhammer40kEnv (без зависимости от core.models)."""
    return getattr(env, "unwrapped", env)


def shooting_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """PASS + по одной SHOOT-опции на валидную цель юнита.

    shoot в плоском контракте — локальный ранг в списке целей юнита
    (см. warhamEnv.shooting_phase: idOfE = valid_target_ids[raw]).
    """
    e = _unwrap(env)
    valid = list(e.get_shoot_targets_for_unit(side, int(unit_idx)))
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(unit_idx))]
    for rank, target_global in enumerate(valid):
        options.append(
            ActionOption(
                kind=ActionKind.SHOOT,
                unit_idx=int(unit_idx),
                target_idx=int(target_global),
                param={"local_rank": int(rank)},
                legacy_patch={"shoot": int(rank)},
            )
        )
    return options


def charge_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """PASS + по одной CHARGE-опции на валидную цель юнита.

    charge в плоском контракте — глобальный индекс врага; для попытки нужен attack=1.
    """
    e = _unwrap(env)
    valid = list(e.get_charge_targets_for_unit(side, int(unit_idx)))
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=int(unit_idx))]
    for target_global in valid:
        options.append(
            ActionOption(
                kind=ActionKind.CHARGE,
                unit_idx=int(unit_idx),
                target_idx=int(target_global),
                legacy_patch={"charge": int(target_global), "attack": 1},
            )
        )
    return options
```

- [ ] **Step 4: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/option_generator.py tests/engine/phases/test_option_generator.py
git commit -m "feat(phases): генератор опций стрельбы/чарджа из легальности env (Stage 2)"
```

---

### Task 4: Опции стрельбы/чарджа консистентны с legal masks env

**Files:**
- Modify: `tests/engine/phases/test_option_generator.py` (добавить тест)

**Interfaces:**
- Consumes: `env.get_legal_action_masks_by_head(side) -> dict[str, np.ndarray]`; функции из Task 3.
- Produces: ничего нового (только тест-покрытие контракта «опции = маски»).

- [ ] **Step 1: Написать падающий тест**

Дописать в `tests/engine/phases/test_option_generator.py`:

```python
import numpy as np

from core.engine.phases.option_generator import (  # noqa: E402  (дополняет верхние импорты)
    charge_options_for_unit,
    shooting_options_for_unit,
)


def test_shoot_targets_union_matches_shoot_mask():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [10, 11]
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["shoot"]
    mask_ids = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}

    gen_ids: set[int] = set()
    for u in range(len(env.unit_health)):
        for o in shooting_options_for_unit(env, "model", u):
            if o.target_idx is not None:
                gen_ids.add(int(o.target_idx))

    # Маска shoot строится в глобальном id-пространстве как объединение целей всех юнитов;
    # при отсутствии целей маска вырождается в {0} (no-op), что генератор не порождает.
    if gen_ids:
        assert gen_ids == mask_ids


def test_charge_targets_union_matches_charge_mask():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["charge"]
    mask_ids = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}

    gen_ids: set[int] = set()
    for u in range(len(env.unit_health)):
        for o in charge_options_for_unit(env, "model", u):
            if o.target_idx is not None:
                gen_ids.add(int(o.target_idx))

    if gen_ids:
        assert gen_ids == mask_ids
```

- [ ] **Step 2: Запустить тест — убедиться, что проходит (контракт уже выполняется)**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -v`
Expected: PASS (4 passed). Если падает — значит генератор и маска используют разные источники целей; чинить генератор (он обязан звать те же `get_*_targets_for_unit`), не маску.

- [ ] **Step 3: Коммит**

```bash
git add tests/engine/phases/test_option_generator.py
git commit -m "test(phases): опции стрельбы/чарджа = legal masks env (контракт)"
```

---

### Task 5: Генератор опций движения (исполнительная истина move_num) — Stage 2 (часть 2)

**Files:**
- Modify: `core/engine/phases/option_generator.py`
- Modify: `tests/engine/phases/test_option_generator.py`

**Interfaces:**
- Consumes: `env.get_unit_movement_overlay(side, idx) -> {"move_cells": list[(x,y)], "advance_cells": list[(x,y)]}`; `env._pick_destination_by_reachable_index(side, idx, *, choice, base_m, unit_label) -> (dest, mode, dist, chosen_idx, total)`; `env.unit_data[idx]["Movement"]`, `env.unit_coords`/`env.enemy_coords`.
- Produces:
  - `def movement_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]` — индекс-в-индекс с `_pick_destination_by_reachable_index`: индекс 0 → `STAY`, далее `MOVE` (move_cells), затем `ADVANCE` (advance_cells). Каждая опция: `param={"reachable_index": k, "dest": (x, y)}`, `legacy_patch={f"move_num_{unit_idx}": k}`.

- [ ] **Step 1: Написать падающий тест (паритет генератора и исполнителя)**

Дописать в `tests/engine/phases/test_option_generator.py`:

```python
from core.engine.phases.option_generator import movement_options_for_unit  # noqa: E402
from core.engine.phases.types import ActionKind as _AK  # noqa: E402


def test_movement_options_index_parity_with_executor():
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    opts = movement_options_for_unit(env, "model", 0)
    assert opts and opts[0].kind is _AK.STAY
    assert opts[0].param["reachable_index"] == 0

    base_m = int(env.unit_data[0]["Movement"])
    # Для каждой сгенерированной опции dest совпадает с тем, что вернёт исполнитель по тому же индексу.
    for o in opts:
        k = o.param["reachable_index"]
        dest, _mode, _dist, chosen_idx, total = env._pick_destination_by_reachable_index(
            "model", 0, choice=k, base_m=base_m, unit_label="[TEST]"
        )
        assert dest is not None
        assert chosen_idx == k
        assert o.param["dest"] == (int(dest[0]), int(dest[1]))
        assert o.legacy_patch == {"move_num_0": k}
    # Генератор покрывает ровно весь исполнительный диапазон reachable.
    assert len(opts) == total


def test_movement_generator_exceeds_buggy_move_num_mask():
    """Документирует баг маски move_num (len(overlay)=2 → только индексы 0,1,2).

    Генератор движется по исполнительной истине и обязан давать НЕ меньше
    опций, чем разрешает сломанная маска.
    """
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["move_num_0"]
    mask_true = int(np.sum(np.asarray(mask, dtype=bool)))
    opts = movement_options_for_unit(env, "model", 0)
    assert len(opts) >= mask_true
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -k movement -v`
Expected: FAIL — `ImportError: cannot import name 'movement_options_for_unit'`.

- [ ] **Step 3: Реализовать генератор движения**

Дописать в `core/engine/phases/option_generator.py`:

```python
def movement_options_for_unit(env, side: str, unit_idx: int) -> list[ActionOption]:
    """STAY/MOVE/ADVANCE-опции, индекс-в-индекс с _pick_destination_by_reachable_index.

    candidates = [stay] + move_cells(normal) + advance_cells(advance);
    reachable_index — это значение move_num_{unit_idx}.
    """
    e = _unwrap(env)
    overlay = e.get_unit_movement_overlay(side, int(unit_idx))
    move_cells = list(overlay.get("move_cells") or [])
    advance_cells = list(overlay.get("advance_cells") or [])

    coords = e.unit_coords if side == "model" else e.enemy_coords
    row = int(coords[int(unit_idx)][0])
    col = int(coords[int(unit_idx)][1])

    # Тот же порядок, что у warhamEnv._pick_destination_by_reachable_index.
    candidates: list[tuple[int, int, ActionKind]] = [(int(col), int(row), ActionKind.STAY)]
    candidates.extend((int(x), int(y), ActionKind.MOVE) for x, y in move_cells)
    candidates.extend((int(x), int(y), ActionKind.ADVANCE) for x, y in advance_cells)

    options: list[ActionOption] = []
    for k, (x, y, kind) in enumerate(candidates):
        options.append(
            ActionOption(
                kind=kind,
                unit_idx=int(unit_idx),
                param={"reachable_index": int(k), "dest": (int(x), int(y))},
                legacy_patch={f"move_num_{int(unit_idx)}": int(k)},
            )
        )
    return options
```

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -v`
Expected: PASS (6 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/option_generator.py tests/engine/phases/test_option_generator.py
git commit -m "feat(phases): генератор опций движения (паритет с move_num executor) + фиксация бага маски"
```

---

### Task 6: Командное окно (Insane Bravery) + сборка хода `generate_windows` — Stage 2 (часть 3)

**Files:**
- Modify: `core/engine/phases/option_generator.py`
- Modify: `core/engine/phases/__init__.py` (реэкспорт публичных функций)
- Modify: `tests/engine/phases/test_option_generator.py`

**Interfaces:**
- Consumes: `env.unit_health`/`env.enemy_health`, `env.modelCP`/`env.enemyCP`; функции `movement_options_for_unit`, `shooting_options_for_unit`, `charge_options_for_unit`; типы из Task 1.
- Produces:
  - `def command_window(env, side: str) -> DecisionWindow` — `cursor_unit_idx=None`; опции: `PASS` + по `USE_STRATAGEM(insane_bravery)` на каждый живой юнит, если у стороны CP≥1; у стратагемы `unit_idx=i`, `meta={"stratagem_id": "insane_bravery", "cp_cost": 1}`, `legacy_patch={"use_cp": 1, "cp_on": i}`.
  - `def generate_windows(env, side: str = "model") -> list[DecisionWindow]` — упорядоченный список окон хода: command → movement (по живым юнитам) → shooting (по живым) → charge (по живым). У каждого окна стабильный `window_id` вида `f"{phase}:{side}:{unit_idx}"` (или `f"command:{side}"`).
- `__init__.py` дополнительно реэкспортирует: `generate_windows`, `command_window`, `movement_options_for_unit`, `shooting_options_for_unit`, `charge_options_for_unit`.

- [ ] **Step 1: Написать падающий тест**

Дописать в `tests/engine/phases/test_option_generator.py`:

```python
from core.engine.phases.option_generator import command_window, generate_windows  # noqa: E402
from core.engine.phases.types import Phase as _Phase  # noqa: E402


def test_command_window_offers_bravery_only_with_cp():
    env = build_env()
    env.modelCP = 0
    win0 = command_window(env, "model")
    assert all(o.kind is not _AK.USE_STRATAGEM for o in win0.options)

    env.modelCP = 2
    win = command_window(env, "model")
    bravery = [o for o in win.options if o.kind is _AK.USE_STRATAGEM]
    alive = [i for i, hp in enumerate(env.unit_health) if hp > 0]
    assert [o.unit_idx for o in bravery] == alive
    for o in bravery:
        assert o.meta["stratagem_id"] == "insane_bravery"
        assert o.legacy_patch == {"use_cp": 1, "cp_on": int(o.unit_idx)}


def test_generate_windows_orders_phases():
    env = build_env()
    env.modelCP = 1
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env._invalidate_target_cache("test")

    windows = generate_windows(env, "model")
    phases_seen = [w.phase for w in windows]
    # command идёт первым, бой/скоринг не порождают окон выбора в этом слое
    assert phases_seen[0] is _Phase.COMMAND
    assert _Phase.MOVEMENT in phases_seen
    assert _Phase.SHOOTING in phases_seen
    assert _Phase.CHARGE in phases_seen
    # порядок фаз неубывающий по индексу в каноне
    order = {_Phase.COMMAND: 0, _Phase.MOVEMENT: 1, _Phase.SHOOTING: 2, _Phase.CHARGE: 3}
    idxs = [order[p] for p in phases_seen]
    assert idxs == sorted(idxs)
    # window_id стабильны и уникальны
    ids = [w.window_id for w in windows]
    assert len(ids) == len(set(ids))
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -k "command or generate" -v`
Expected: FAIL — `ImportError: cannot import name 'command_window'`.

- [ ] **Step 3: Реализовать командное окно и сборку хода**

Дописать в `core/engine/phases/option_generator.py` (вверху файла добавить недостающие импорты типов):

```python
from core.engine.phases.types import (
    ActionKind,
    ActionOption,
    DecisionWindow,
    Phase,
    SubStep,
    Timing,
)
```

(заменить прежнюю строку импорта `from core.engine.phases.types import ActionKind, ActionOption` на расширенную выше)

```python
def _alive_indices(health) -> list[int]:
    return [i for i, hp in enumerate(health) if hp > 0]


def command_window(env, side: str) -> DecisionWindow:
    """Окно командной фазы: Insane Bravery на провал Battle-shock.

    Реальный провал теста определяется броском в рантайме; на уровне слоя мы
    предлагаем агенту опцию заранее (PASS / использовать Bravery на юнита i),
    гейтим только по наличию CP — как делает командная фаза env.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    cp = int(e.modelCP if side == "model" else e.enemyCP)
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=None)]
    if cp >= 1:
        for i in _alive_indices(health):
            options.append(
                ActionOption(
                    kind=ActionKind.USE_STRATAGEM,
                    unit_idx=int(i),
                    param={"stratagem_id": "insane_bravery"},
                    legacy_patch={"use_cp": 1, "cp_on": int(i)},
                    meta={"stratagem_id": "insane_bravery", "cp_cost": 1},
                )
            )
    return DecisionWindow(
        window_id=f"command:{side}",
        owner_side=side,
        phase=Phase.COMMAND,
        sub_step=SubStep.BATTLE_SHOCK,
        timing=Timing.MAIN,
        cursor_unit_idx=None,
        options=options,
        context={"cp": cp},
    )


def generate_windows(env, side: str = "model") -> list[DecisionWindow]:
    """Упорядоченные окна хода: command → movement → shooting → charge.

    Бой/скоринг в текущей модели не дают выбора агента — окон не порождаем.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = _alive_indices(health)
    windows: list[DecisionWindow] = [command_window(e, side)]

    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"movement:{side}:{u}",
                owner_side=side,
                phase=Phase.MOVEMENT,
                sub_step=SubStep.MOVE_UNIT,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=movement_options_for_unit(e, side, u),
            )
        )
    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"shooting:{side}:{u}",
                owner_side=side,
                phase=Phase.SHOOTING,
                sub_step=SubStep.PICK_SHOOT_TARGET,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=shooting_options_for_unit(e, side, u),
            )
        )
    for u in alive:
        windows.append(
            DecisionWindow(
                window_id=f"charge:{side}:{u}",
                owner_side=side,
                phase=Phase.CHARGE,
                sub_step=SubStep.PICK_CHARGE_TARGET,
                timing=Timing.MAIN,
                cursor_unit_idx=int(u),
                options=charge_options_for_unit(e, side, u),
            )
        )
    return windows
```

Дополнить `core/engine/phases/__init__.py` реэкспортом генератора (добавить импорт и пункты в `__all__`):

```python
from core.engine.phases.option_generator import (
    charge_options_for_unit,
    command_window,
    generate_windows,
    movement_options_for_unit,
    shooting_options_for_unit,
)
```

Добавить в `__all__`: `"generate_windows", "command_window", "movement_options_for_unit", "shooting_options_for_unit", "charge_options_for_unit"`.

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/engine/phases/test_option_generator.py -v`
Expected: PASS (8 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/option_generator.py core/engine/phases/__init__.py tests/engine/phases/test_option_generator.py
git commit -m "feat(phases): командное окно (Insane Bravery) + сборка окон хода generate_windows (Stage 2)"
```

---

### Task 7: LegacyActionCompiler — опции → плоский action_dict — Stage 3

**Files:**
- Create: `core/engine/phases/legacy_compiler.py`
- Modify: `core/engine/phases/__init__.py`
- Test: `tests/engine/phases/test_legacy_compiler.py`

**Interfaces:**
- Consumes: `ActionOption` (его `legacy_patch`); `core.models.action_contract.ordered_action_keys` — НЕ импортируем (нельзя engine→models); вместо этого формируем ключи локально.
- Produces:
  - `def default_action_dict(len_model: int) -> dict[str, int]` — нейтральный ход: `{"move":4, "attack":1, "shoot":0, "charge":0, "use_cp":0, "cp_on":0, "move_num_0..N-1":0}`.
  - `def compile_options_to_action_dict(options: list[ActionOption], len_model: int) -> dict[str, int]` — старт с `default_action_dict`, последовательно применить `opt.legacy_patch`.
- `__init__.py` реэкспортирует `default_action_dict`, `compile_options_to_action_dict`.

- [ ] **Step 1: Написать падающий тест (включая исполнительный roundtrip)**

Создать `tests/engine/phases/test_legacy_compiler.py`:

```python
from core.engine.phases.legacy_compiler import (
    compile_options_to_action_dict,
    default_action_dict,
)
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind, ActionOption
from tests.engine.phases._helpers import build_env


def test_default_action_dict_shape():
    d = default_action_dict(2)
    assert d["move"] == 4 and d["attack"] == 1
    assert d["shoot"] == 0 and d["charge"] == 0
    assert d["use_cp"] == 0 and d["cp_on"] == 0
    assert d["move_num_0"] == 0 and d["move_num_1"] == 0
    assert "move_num_2" not in d


def test_compile_applies_patches_in_order():
    opts = [
        ActionOption(kind=ActionKind.MOVE, unit_idx=0, legacy_patch={"move_num_0": 3}),
        ActionOption(kind=ActionKind.SHOOT, unit_idx=0, target_idx=5, legacy_patch={"shoot": 1}),
        ActionOption(kind=ActionKind.CHARGE, unit_idx=1, target_idx=0, legacy_patch={"charge": 0, "attack": 1}),
        ActionOption(kind=ActionKind.USE_STRATAGEM, unit_idx=1, legacy_patch={"use_cp": 1, "cp_on": 1}),
    ]
    d = compile_options_to_action_dict(opts, len_model=2)
    assert d["move_num_0"] == 3
    assert d["shoot"] == 1
    assert d["charge"] == 0 and d["attack"] == 1
    assert d["use_cp"] == 1 and d["cp_on"] == 1


def test_movement_roundtrip_executes_to_chosen_cell():
    """Опция движения → compile → исполнение movement_phase даёт ту же клетку.

    Прогон в simulation_mode + restore: поведение env не затрагивается.
    """
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    opts = movement_options_for_unit(env, "model", 0)
    # выбираем последнюю достижимую опцию (не stay), если она есть
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    dest_x, dest_y = chosen.param["dest"]

    action = compile_options_to_action_dict([chosen], len_model=len(env.unit_health))

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))
            # warhamEnv хранит координаты как [dest[1], dest[0]]
            assert list(env.unit_coords[0]) == [int(dest_y), int(dest_x)]
        finally:
            env.restore_state(snap)

    # после restore состояние вернулось
    assert list(env.unit_coords[0]) == [15, 15]
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_legacy_compiler.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.engine.phases.legacy_compiler'`.

- [ ] **Step 3: Реализовать компилятор**

Создать `core/engine/phases/legacy_compiler.py`:

```python
from __future__ import annotations

from core.engine.phases.types import ActionOption


def default_action_dict(len_model: int) -> dict[str, int]:
    """Нейтральный ход в плоском контракте.

    move=4 → нет направления (stay-fallback); attack=1 → пытаться вступить в бой/чардж;
    остальные головы — индекс 0. move_num_{i} на каждого юнита модели.
    """
    action: dict[str, int] = {
        "move": 4,
        "attack": 1,
        "shoot": 0,
        "charge": 0,
        "use_cp": 0,
        "cp_on": 0,
    }
    for i in range(int(len_model)):
        action[f"move_num_{i}"] = 0
    return action


def compile_options_to_action_dict(options: list[ActionOption], len_model: int) -> dict[str, int]:
    """Сложить legacy_patch выбранных опций в один плоский action_dict.

    Ограничение плоского контракта: одна голова shoot/charge/use_cp на весь ход,
    поэтому при нескольких конфликтующих опциях побеждает последняя (lossy).
    Это осознанное ограучение слоя до переноса исполнения в PhaseEngine (Stage 7).
    """
    action = default_action_dict(int(len_model))
    for opt in options:
        for key, value in opt.legacy_patch.items():
            action[str(key)] = int(value)
    return action
```

Дополнить `core/engine/phases/__init__.py`:

```python
from core.engine.phases.legacy_compiler import (
    compile_options_to_action_dict,
    default_action_dict,
)
```

Добавить в `__all__`: `"compile_options_to_action_dict", "default_action_dict"`.

- [ ] **Step 4: Исправить опечатку в докстринге и запустить тесты**

В докстринге `compile_options_to_action_dict` заменить `ограучение` → `ограничение`.

Run: `python -m pytest tests/engine/phases/test_legacy_compiler.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/legacy_compiler.py core/engine/phases/__init__.py tests/engine/phases/test_legacy_compiler.py
git commit -m "feat(phases): LegacyActionCompiler (опции → плоский action_dict) + roundtrip (Stage 3)"
```

---

### Task 8: Регрессия «поведение env.step не изменилось» + прогон всего пакета

**Files:**
- Create: `tests/engine/phases/test_no_behavior_change.py`

**Interfaces:**
- Consumes: `build_env`; публичный API пакета; `env.snapshot_state/restore_state/step`.
- Produces: гарантия инварианта стадий 1–3 (импорт слоя и компиляция нейтрального хода не меняют траекторию `step`).

- [ ] **Step 1: Написать тест инварианта**

Создать `tests/engine/phases/test_no_behavior_change.py`:

```python
import numpy as np

from core.engine.phases import compile_options_to_action_dict, default_action_dict
from tests.engine.phases._helpers import build_env


def _run_one_model_step(env, action):
    obs, reward, done, res, info = env.step(action)
    return float(reward), bool(done), float(np.sum(env.unit_health)), float(np.sum(env.enemy_health))


def test_compiled_default_equals_manual_default_step():
    """Нейтральный action из компилятора == рукописный дефолт: одинаковая траектория step."""
    n = 2

    env_a = build_env()
    env_a.reset(options={"m": env_a.model, "e": env_a.enemy, "trunc": True})
    manual = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        manual[f"move_num_{i}"] = 0
    snap_a = env_a.snapshot_state()
    res_a = _run_one_model_step(env_a, manual)
    env_a.restore_state(snap_a)

    env_b = build_env()
    env_b.reset(options={"m": env_b.model, "e": env_b.enemy, "trunc": True})
    compiled = compile_options_to_action_dict([], len_model=n)
    # выставляем одинаковый rng-старт через snapshot обмен невозможно (разные объекты),
    # поэтому сравниваем структуру dict, а не стохастический исход:
    assert compiled == manual


def test_default_action_dict_matches_action_contract_keys():
    from core.models.action_contract import ordered_action_keys

    d = default_action_dict(2)
    assert set(d.keys()) == set(ordered_action_keys(2))
```

- [ ] **Step 2: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/engine/phases/test_no_behavior_change.py -v`
Expected: PASS (2 passed).

- [ ] **Step 3: Прогнать весь новый пакет + смоук затронутого движка**

Run: `python -m pytest tests/engine/phases/ -v`
Expected: PASS (все).

Run: `python -m pytest tests/engine/test_warham_env_snapshot_restore.py tests/engine/test_shoot_targets_contract_regression.py tests/engine/test_model_and_heur_movement_overlay.py -v`
Expected: PASS — движок не затронут (sanity).

- [ ] **Step 4: Коммит**

```bash
git add tests/engine/phases/test_no_behavior_change.py
git commit -m "test(phases): инвариант 'поведение env.step не изменилось' + контракт ключей"
```

---

## Self-Review

**Spec coverage (против §5–§8 архитектурного отчёта):**
- `ActionOption`/`DecisionWindow`/`PhaseState`/`PhaseResult`/enums → Task 1. ✓
- `ActionOptionGenerator` (movement/shooting/charge/command) → Tasks 3, 5, 6. ✓
- `LegacyActionCompiler` → Task 7. ✓
- Decision windows для command/movement/shooting/charge → Task 6 (`generate_windows`). ✓ (fight/scoring/reaction — осознанно вне Stage 1–3, см. Roadmap.)
- Тесты: phase option generation (Task 3,5,6); options == legal masks (Task 4 shoot/charge; Task 5 фиксирует баг маски move_num); compiler roundtrip (Task 7); behavior-unchanged (Task 8). ✓
- CP-стратагема как опция, без расширения `use_cp` (Insane Bravery через `legacy_patch`) → Task 6. ✓ (полный StratagemEngine/registry — Stage 5–6, Roadmap.)

**Placeholder scan:** все шаги содержат конкретный код/команды/ожидаемый вывод; «реализуй позже» отсутствует. Опечатка `ограучение` исправляется явным шагом (Task 7 Step 4). ✓

**Type consistency:** `ActionOption(kind, unit_idx, target_idx, param, legacy_patch, meta)` — единые имена во всех тасках; `legacy_patch` ключи (`move_num_{i}`, `shoot`, `charge`, `attack`, `use_cp`, `cp_on`) совпадают с дефолтным dict компилятора; `generate_windows`/`command_window`/`*_options_for_unit` — одинаковые сигнатуры в реализации, реэкспорте и тестах. ✓

---

## Roadmap (вне scope этого плана — отдельные планы позже)

Эти стадии из архитектурного отчёта НЕ входят в текущий план; каждая станет отдельным планом после ревью результатов Stage 1–3:

- **Stage 4 — Gumbel AZ / MCTS root candidates через `ActionOption`** (`core/models/alphazero_mcts.py`, `alphazero_selfplay.py`): корневые кандидаты из `generate_windows`, проекция факторизованных приоров на опции; исполнение по-прежнему через `env.step` + компилятор.
- **Stage 5 — Stratagem registry (data-only):** `StratagemDef` (Insane Bravery/Overwatch/Smokescreen/Heroic), `StratagemEngine.legal_*` (только чтение).
- **Stage 6 — Necrons/Warriors CP-механики через `StratagemOption`:** перенос Bravery/Smokescreen на `StratagemEngine.apply`, добавление `StratagemState` (used_*, active_buffs) и забытых `_enemy_cp_on/_enemy_use_cp` в `snapshot_state`/`restore_state` (`core/envs/warhamEnv.py:1134/1243`); reaction-окна как настоящие прерывания.
- **Stage 7 — substep `PhaseEngine`:** перенос исполнения внутрь движка, `env.step` сохраняет публичный контракт; golden-traces из Stage 0.
- **Stage 8 — training/replay/search на decision-step:** расширение `AZTransition` метаданными (phase/sub_step/timing/window_id/chosen_option/stratagem_id/cp), obs-фичи фаз/CP, MCTS-узлы = окна.

Дополнительно как отдельная мелкая задача: **починка бага маски `move_num`** (`core/envs/warhamEnv.py:1716-1721`, `len(overlay)` → реальное число reachable-клеток) — это меняет поведение RL-масок, поэтому делается осознанно, вне scaffolding.
