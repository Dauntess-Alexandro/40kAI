# Stage 5 — Stratagem Registry (data-only) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дать типизированный справочник стратагем (data-only) и read-only движок легальности, чтобы окна решений могли предлагать стратагемы как обычные `ActionOption(kind=USE_STRATAGEM)` — без изменения поведения `env.step`/обучения.

**Architecture:** Новый модуль `core/engine/phases/stratagems.py` (enums + `StratagemDef` + `REGISTRY` 4 стратагем + лукапы + чистая функция `legal_stratagem_options`, читающая `env`). `command_window` переключается на реестр (Insane Bravery перестаёт быть инлайн-хардкодом), выход прежний. Реакционные стратагемы — только данные/легальность (`legacy_patch={}`, в плоский ход не выражаются).

**Tech Stack:** Python 3.12, dataclasses + StrEnum, pytest. Без новых зависимостей.

**Спека:** `docs/superpowers/specs/2026-06-17-stage5-stratagem-registry-design.md`.

## Global Constraints

- Платформа Windows; Python 3.12+; тесты — `python -m pytest` из корня (venv `.venv`).
- ruff `py312`, line-length 120, `select=["E","F","I","UP","B"]`, `StrEnum` вместо `(str, Enum)`. Хук `ruff_fix.py` авто-фиксит и **удаляет временно-неиспользуемые импорты** — добавляй импорт вместе с его использованием в одной правке (или восстанавливай после).
- Язык докстрингов/сообщений — русский; ошибка = что + где + что делать.
- `core/engine/*` НЕ импортирует `core/models/*`.
- **Инвариант:** `core/envs/warhamEnv.py` не модифицируется. `legal_stratagem_options` только читает env (`modelCP`/`enemyCP`, `unit_health`/`enemy_health`, `unit_data`/`enemy_data`, `_unit_has_keyword`).
- Источник истины по легальности — слой `core/engine/phases/`.

## Известные факты (опора)

- Типы слоя: `ActionOption(kind, unit_idx, target_idx, param, legacy_patch, meta)`, `DecisionWindow`, `Phase`, `Timing`, `ActionKind` — `core/engine/phases/types.py`.
- `command_window`/`_alive_indices`/`_unwrap` — `core/engine/phases/option_generator.py`.
- `_unit_has_keyword(unit_data, kw)` — регистронезависимый: явный скан полей (`Keywords`,`Abilities`,`Type`,`Faction`,…) + fallback по всем значениям. `core/envs/warhamEnv.py:3895-3917`. `_unit_has_smoke` = `_unit_has_keyword(...,"smoke")` (`:3919`).
- Соответствие стратагем коду: Insane Bravery `warhamEnv.py:4332-4345` (единственная с рабочим `legacy_patch`); Overwatch `:3972/:4000`; Smokescreen `:3922` (keyword SMOKE); Heroic `:4134`.

## File Structure

- Create `core/engine/phases/stratagems.py` — `Trigger`, `UsageLimit`, `StratagemDef`, `REGISTRY`, `by_id`/`for_phase`/`for_trigger`, `legal_stratagem_options`.
- Modify `core/engine/phases/option_generator.py` — `command_window` строит Bravery через `legal_stratagem_options`.
- Modify `core/engine/phases/__init__.py` — реэкспорт публичных имён реестра.
- Create `tests/engine/phases/test_stratagems.py` — реестр + легальность.
- (Регрессия) существующий `tests/engine/phases/test_option_generator.py::test_command_window_offers_bravery_only_with_cp` фиксирует неизменность `command_window`.

---

### Task 1: Реестр стратагем (enums + StratagemDef + REGISTRY + лукапы)

**Files:**
- Create: `core/engine/phases/stratagems.py`
- Test: `tests/engine/phases/test_stratagems.py`

**Interfaces:**
- Consumes: `core.engine.phases.types` (`Phase`, `Timing`).
- Produces:
  - `class Trigger(StrEnum)`: `BATTLE_SHOCK_FAILED, TARGETED_BY_SHOOTING, ENEMY_ENDED_MOVE, ENEMY_CHARGED_IN`.
  - `class UsageLimit(StrEnum)`: `PER_PHASE, PER_TURN, PER_BATTLE, UNLIMITED`.
  - `@dataclass(frozen=True) StratagemDef(id, name_ru, cp_cost, phases: tuple[Phase,...], timing: Timing, trigger: Trigger, scope: str, keyword_req: tuple[str,...], usage_limit: UsageLimit, effect_id: str)`.
  - `REGISTRY: tuple[StratagemDef, ...]` (4 шт.).
  - `by_id(stratagem_id: str) -> StratagemDef` (KeyError с RU-сообщением).
  - `for_phase(phase: Phase) -> list[StratagemDef]`.
  - `for_trigger(trigger: Trigger) -> list[StratagemDef]`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_stratagems.py`:

```python
import pytest

from core.engine.phases.stratagems import (
    REGISTRY,
    StratagemDef,
    Trigger,
    by_id,
    for_phase,
    for_trigger,
)
from core.engine.phases.types import Phase


def test_registry_integrity():
    assert len(REGISTRY) == 4
    ids = [d.id for d in REGISTRY]
    assert ids == ["insane_bravery", "overwatch", "smokescreen", "heroic_intervention"]
    assert len(ids) == len(set(ids))
    for d in REGISTRY:
        assert isinstance(d, StratagemDef)
        assert d.cp_cost >= 1
        assert by_id(d.id) is d


def test_lookups_by_phase_and_trigger():
    assert any(d.id == "insane_bravery" for d in for_phase(Phase.COMMAND))
    assert any(d.id == "smokescreen" for d in for_phase(Phase.SHOOTING))
    assert [d.id for d in for_trigger(Trigger.TARGETED_BY_SHOOTING)] == ["smokescreen"]
    assert [d.id for d in for_trigger(Trigger.BATTLE_SHOCK_FAILED)] == ["insane_bravery"]


def test_smokescreen_requires_smoke_keyword():
    smoke = by_id("smokescreen")
    assert smoke.keyword_req == ("smoke",)
    assert by_id("insane_bravery").keyword_req == ()


def test_by_id_unknown_raises():
    with pytest.raises(KeyError):
        by_id("does_not_exist")
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_stratagems.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.engine.phases.stratagems'`.

- [ ] **Step 3: Реализовать реестр**

Создать `core/engine/phases/stratagems.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from core.engine.phases.types import Phase, Timing


class Trigger(StrEnum):
    BATTLE_SHOCK_FAILED = "battle_shock_failed"
    TARGETED_BY_SHOOTING = "targeted_by_shooting"
    ENEMY_ENDED_MOVE = "enemy_ended_move"
    ENEMY_CHARGED_IN = "enemy_charged_in"


class UsageLimit(StrEnum):
    PER_PHASE = "per_phase"
    PER_TURN = "per_turn"
    PER_BATTLE = "per_battle"
    UNLIMITED = "unlimited"


@dataclass(frozen=True)
class StratagemDef:
    """Описание стратагемы (data-only). usage_limit пока НЕ enforced (Stage 6)."""

    id: str
    name_ru: str
    cp_cost: int
    phases: tuple[Phase, ...]
    timing: Timing
    trigger: Trigger
    scope: str  # "self_unit" | "reacting_unit" | "enemy_unit" (описательное)
    keyword_req: tuple[str, ...]
    usage_limit: UsageLimit
    effect_id: str


REGISTRY: tuple[StratagemDef, ...] = (
    StratagemDef(
        id="insane_bravery",
        name_ru="Insane Bravery",
        cp_cost=1,
        phases=(Phase.COMMAND,),
        timing=Timing.MAIN,
        trigger=Trigger.BATTLE_SHOCK_FAILED,
        scope="self_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_BATTLE,
        effect_id="auto_pass_battle_shock",
    ),
    StratagemDef(
        id="overwatch",
        name_ru="Fire Overwatch",
        cp_cost=1,
        phases=(Phase.MOVEMENT, Phase.CHARGE),
        timing=Timing.REACTION,
        trigger=Trigger.ENEMY_ENDED_MOVE,
        scope="reacting_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="shoot_hits_on_6",
    ),
    StratagemDef(
        id="smokescreen",
        name_ru="Smokescreen",
        cp_cost=1,
        phases=(Phase.SHOOTING,),
        timing=Timing.REACTION,
        trigger=Trigger.TARGETED_BY_SHOOTING,
        scope="reacting_unit",
        keyword_req=("smoke",),
        usage_limit=UsageLimit.UNLIMITED,
        effect_id="benefit_of_cover",
    ),
    StratagemDef(
        id="heroic_intervention",
        name_ru="Heroic Intervention",
        cp_cost=1,
        phases=(Phase.CHARGE,),
        timing=Timing.REACTION,
        trigger=Trigger.ENEMY_CHARGED_IN,
        scope="reacting_unit",
        keyword_req=(),
        usage_limit=UsageLimit.PER_PHASE,
        effect_id="counter_charge",
    ),
)


_BY_ID: dict[str, StratagemDef] = {d.id: d for d in REGISTRY}


def by_id(stratagem_id: str) -> StratagemDef:
    try:
        return _BY_ID[stratagem_id]
    except KeyError:
        raise KeyError(
            f"нет стратагемы id={stratagem_id!r}; где: stratagems.by_id; "
            "что делать: проверить REGISTRY/опечатку id."
        ) from None


def for_phase(phase: Phase) -> list[StratagemDef]:
    return [d for d in REGISTRY if phase in d.phases]


def for_trigger(trigger: Trigger) -> list[StratagemDef]:
    return [d for d in REGISTRY if d.trigger == trigger]
```

- [ ] **Step 4: Запустить тест — убедиться, что проходит**

Run: `python -m pytest tests/engine/phases/test_stratagems.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/stratagems.py tests/engine/phases/test_stratagems.py
git commit -m "feat(phases): реестр стратагем StratagemDef + REGISTRY + лукапы (Stage 5)"
```

---

### Task 2: Read-only движок легальности `legal_stratagem_options`

**Files:**
- Modify: `core/engine/phases/stratagems.py`
- Modify: `tests/engine/phases/test_stratagems.py`

**Interfaces:**
- Consumes: env (чтение `modelCP`/`enemyCP`, `unit_health`/`enemy_health`, `unit_data`/`enemy_data`, `_unit_has_keyword`); `ActionKind`, `ActionOption` из types; `Phase`, `Trigger`, `for_trigger`.
- Produces:
  - `def legal_stratagem_options(env, side: str, *, phase: Phase, trigger: Trigger, candidate_unit_idxs: list[int] | None = None) -> list[ActionOption]`.
    - Фильтры: `phase in d.phases`, `cp >= d.cp_cost`, юнит жив, `keyword_req` через `env._unit_has_keyword`.
    - `legacy_patch`: `{"use_cp":1,"cp_on":i}` только для `insane_bravery`; иначе `{}`.
    - `meta = {"stratagem_id", "cp_cost", "timing", "scope"}`, `param = {"stratagem_id": d.id}`.

- [ ] **Step 1: Написать падающий тест**

Дописать в `tests/engine/phases/test_stratagems.py` (импорты добавить вместе с использованием):

```python
from core.engine.phases.stratagems import legal_stratagem_options  # noqa: E402
from core.engine.phases.types import ActionKind  # noqa: E402
from tests.engine.phases._helpers import build_env  # noqa: E402


def _alive(env):
    return [i for i, hp in enumerate(env.unit_health) if hp > 0]


def test_command_bravery_cp_gate_and_patch():
    env = build_env()
    alive = _alive(env)

    env.modelCP = 0
    assert (
        legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=alive
        )
        == []
    )

    env.modelCP = 2
    opts = legal_stratagem_options(
        env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=alive
    )
    assert [o.unit_idx for o in opts] == alive
    for o in opts:
        assert o.kind is ActionKind.USE_STRATAGEM
        assert o.meta["stratagem_id"] == "insane_bravery"
        assert o.legacy_patch == {"use_cp": 1, "cp_on": int(o.unit_idx)}


def test_smokescreen_legality_follows_env_keyword():
    env = build_env()
    env.modelCP = 1
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.unit_data[1]["Keywords"] = ["INFANTRY"]
    for i in (0, 1):
        opts = legal_stratagem_options(
            env, "model", phase=Phase.SHOOTING, trigger=Trigger.TARGETED_BY_SHOOTING, candidate_unit_idxs=[i]
        )
        has_smoke_opt = any(o.meta["stratagem_id"] == "smokescreen" for o in opts)
        assert has_smoke_opt == bool(env._unit_has_smoke(env.unit_data[i]))
    assert env._unit_has_smoke(env.unit_data[0]) is True
    assert env._unit_has_smoke(env.unit_data[1]) is False


def test_reaction_options_have_empty_legacy_patch():
    env = build_env()
    env.modelCP = 2
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    cases = [
        (Phase.MOVEMENT, Trigger.ENEMY_ENDED_MOVE),
        (Phase.SHOOTING, Trigger.TARGETED_BY_SHOOTING),
        (Phase.CHARGE, Trigger.ENEMY_CHARGED_IN),
    ]
    for phase, trig in cases:
        opts = legal_stratagem_options(env, "model", phase=phase, trigger=trig, candidate_unit_idxs=[0])
        assert opts, f"ожидались опции для {trig}"
        for o in opts:
            assert o.legacy_patch == {}


def test_reaction_cp_gate_blocks_all():
    env = build_env()
    env.modelCP = 0
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    for phase, trig in [
        (Phase.MOVEMENT, Trigger.ENEMY_ENDED_MOVE),
        (Phase.SHOOTING, Trigger.TARGETED_BY_SHOOTING),
        (Phase.CHARGE, Trigger.ENEMY_CHARGED_IN),
    ]:
        assert legal_stratagem_options(env, "model", phase=phase, trigger=trig, candidate_unit_idxs=[0]) == []


def test_no_candidates_returns_empty():
    env = build_env()
    env.modelCP = 3
    assert (
        legal_stratagem_options(
            env, "model", phase=Phase.COMMAND, trigger=Trigger.BATTLE_SHOCK_FAILED, candidate_unit_idxs=None
        )
        == []
    )
```

- [ ] **Step 2: Запустить тест — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_stratagems.py -k "legality or cp_gate or reaction or candidates or patch" -v`
Expected: FAIL — `ImportError: cannot import name 'legal_stratagem_options'`.

- [ ] **Step 3: Реализовать движок легальности**

Дописать в `core/engine/phases/stratagems.py` (импорты типов — вместе с использованием):

```python
from core.engine.phases.types import ActionKind, ActionOption
```

(объединить с существующей строкой импорта types: `from core.engine.phases.types import ActionKind, ActionOption, Phase, Timing`)

```python
def _unwrap(env):
    """Снять gym-обёртку до Warhammer40kEnv (локально, без цикла на option_generator)."""
    return getattr(env, "unwrapped", env)


def legal_stratagem_options(
    env,
    side: str,
    *,
    phase: Phase,
    trigger: Trigger,
    candidate_unit_idxs: list[int] | None = None,
) -> list[ActionOption]:
    """Какие стратагемы доступны сейчас (read-only).

    Фильтры: фаза, триггер, хватает ли CP, юнит жив, есть ли нужный keyword.
    legacy_patch есть только у insane_bravery (выразима в плоском action_dict);
    реакции пока несут пустой patch (исполняются движком авто до Stage 6/7).
    """
    e = _unwrap(env)
    is_model = side == "model"
    cp = int(e.modelCP if is_model else e.enemyCP)
    health = e.unit_health if is_model else e.enemy_health
    unit_data_list = e.unit_data if is_model else e.enemy_data

    defs = [d for d in for_trigger(trigger) if phase in d.phases]
    options: list[ActionOption] = []
    for d in defs:
        if cp < d.cp_cost:
            continue
        if candidate_unit_idxs is None:
            continue
        for raw in candidate_unit_idxs:
            i = int(raw)
            if not (0 <= i < len(health)) or health[i] <= 0:
                continue
            if d.keyword_req and not all(
                e._unit_has_keyword(unit_data_list[i], kw) for kw in d.keyword_req
            ):
                continue
            legacy_patch = {"use_cp": 1, "cp_on": i} if d.id == "insane_bravery" else {}
            options.append(
                ActionOption(
                    kind=ActionKind.USE_STRATAGEM,
                    unit_idx=i,
                    param={"stratagem_id": d.id},
                    legacy_patch=dict(legacy_patch),
                    meta={
                        "stratagem_id": d.id,
                        "cp_cost": d.cp_cost,
                        "timing": d.timing,
                        "scope": d.scope,
                    },
                )
            )
    return options
```

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `python -m pytest tests/engine/phases/test_stratagems.py -v`
Expected: PASS (9 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/stratagems.py tests/engine/phases/test_stratagems.py
git commit -m "feat(phases): legal_stratagem_options (read-only легальность по фазе/CP/keyword) (Stage 5)"
```

---

### Task 3: `command_window` на реестр + реэкспорт + регрессия неизменности

**Files:**
- Modify: `core/engine/phases/option_generator.py`
- Modify: `core/engine/phases/__init__.py`

**Interfaces:**
- Consumes: `legal_stratagem_options`, `Trigger` из `stratagems`; существующие `Phase`, `ActionOption`, `ActionKind`, `DecisionWindow`, `_alive_indices`, `_unwrap`.
- Produces: `command_window` строит Bravery-опции через реестр (выход прежний); `__init__` реэкспортирует `StratagemDef`, `Trigger`, `UsageLimit`, `REGISTRY`, `by_id`, `for_phase`, `for_trigger`, `legal_stratagem_options`.

- [ ] **Step 1: Переключить `command_window` на реестр**

В `core/engine/phases/option_generator.py` добавить импорт (вместе с использованием ниже):

```python
from core.engine.phases.stratagems import Trigger, legal_stratagem_options
```

Заменить тело `command_window` (блок построения опций) на:

```python
def command_window(env, side: str) -> DecisionWindow:
    """Окно командной фазы: Insane Bravery на провал Battle-shock.

    Опции Bravery берутся из реестра стратагем (legal_stratagem_options),
    а не инлайнятся: единый источник истины по легальности CP.
    """
    e = _unwrap(env)
    health = e.unit_health if side == "model" else e.enemy_health
    cp = int(e.modelCP if side == "model" else e.enemyCP)
    options: list[ActionOption] = [ActionOption(kind=ActionKind.PASS, unit_idx=None)]
    options.extend(
        legal_stratagem_options(
            e,
            side,
            phase=Phase.COMMAND,
            trigger=Trigger.BATTLE_SHOCK_FAILED,
            candidate_unit_idxs=_alive_indices(health),
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
```

- [ ] **Step 2: Прогнать существующую регрессию `command_window` (должна остаться зелёной)**

Run: `python -m pytest tests/engine/phases/test_option_generator.py::test_command_window_offers_bravery_only_with_cp tests/engine/phases/test_option_generator.py::test_generate_windows_orders_phases -v`
Expected: PASS (2 passed) — состав опций (`unit_idx`, `legacy_patch`, `meta["stratagem_id"]`) не изменился после рефактора.

- [ ] **Step 3: Реэкспорт публичных имён реестра**

В `core/engine/phases/__init__.py` добавить импорт и пункты `__all__`:

```python
from core.engine.phases.stratagems import (
    REGISTRY,
    StratagemDef,
    Trigger,
    UsageLimit,
    by_id,
    for_phase,
    for_trigger,
    legal_stratagem_options,
)
```

Добавить в `__all__`: `"StratagemDef", "Trigger", "UsageLimit", "REGISTRY", "by_id", "for_phase", "for_trigger", "legal_stratagem_options"`.

- [ ] **Step 4: Прогнать весь пакет + смоук движка + ruff**

Run: `python -m pytest tests/engine/phases/ -q`
Expected: PASS (все: 17 прежних + 9 stratagems = 26).

Run: `python -m pytest tests/engine/test_warham_env_snapshot_restore.py tests/engine/test_shoot_targets_contract_regression.py -q`
Expected: PASS (env не тронут).

Run: `python -m ruff check core/engine/phases/ tests/engine/phases/`
Expected: `All checks passed!`.

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/option_generator.py core/engine/phases/__init__.py
git commit -m "feat(phases): command_window через реестр стратагем + реэкспорт публичного API (Stage 5)"
```

---

## Self-Review

**Spec coverage:**
- Реестр `StratagemDef`/`REGISTRY`/лукапы → Task 1. ✓
- `legal_stratagem_options` (read-only, фильтры фаза/CP/keyword, legacy_patch только Bravery, реакции `{}`) → Task 2. ✓
- Интеграция `command_window` через реестр, выход прежний → Task 3 (+регрессия). ✓
- Реэкспорт публичного API → Task 3. ✓
- Тесты: registry integrity (T1); command bravery cp-gate+patch, smokescreen==env keyword, reaction empty patch, reaction cp-gate, no-candidates (T2); command_window unchanged (T3 регрессия существующего теста); env-смоук (T3). ✓
- Инвариант «поведение env.step не изменилось» — обеспечен тем, что env не трогаем и `command_window` даёт прежний выход; покрыт существующим `test_no_behavior_change.py`, прогоняется в составе пакета (T3 Step 4). ✓

**Placeholder scan:** код полный в каждом шаге; плейсхолдеров нет.

**Type consistency:** `StratagemDef` поля и `legal_stratagem_options(env, side, *, phase, trigger, candidate_unit_idxs)` едины во всех тасках; `ActionOption(kind, unit_idx, param, legacy_patch, meta)` совпадает с типами Stage 1; `command_window` сохраняет сигнатуру и `DecisionWindow`-поля; `Trigger`/`Phase`/`Timing`/`ActionKind` импортируются согласованно.

## Заметки по исполнению

- Хук `ruff_fix.py` удаляет временно-неиспользуемые импорты в не-тестовых файлах (F401). В Task 2/3 добавляй импорт **в одной правке** с его использованием, либо восстанавливай импорт после добавления кода (как в Stage 1–3).
- `effect_id`/`usage_limit` в Stage 5 — инертные метаданные (enforced в Stage 6). Тесты их значения не фиксируют (кроме наличия поля).
