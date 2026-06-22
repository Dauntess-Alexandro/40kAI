# Стратагемы как действия — Под-проект 1 (кодирование) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить в action-contract пофазные головы выбора стратагемы (`strat_<phase>` + `strat_<phase>_unit`) с единым хелпером индексации — **аддитивно**, не ломая `use_cp`/`cp_on` (Insane Bravery) и без применения значений (применение — под-проект 3).

**Architecture:** Один источник истины `stratagem_action_choices(phase)` (из `REGISTRY`, MAIN-timing, с развёрткой подтипов command_reroll) определяет категории на фазу. `ordered_action_keys`, `default_action_dict` и `env.action_space` получают новые головы консистентно. Значения пока no-op (десериализуются, не применяются).

**Tech Stack:** Python 3.12+, NumPy, Gymnasium (`spaces.Dict`), PyTorch (контракт), pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-stratagem-action-encoding-design.md`. Это **под-проект 1 из 5** большого проекта «стратагемы как действия»; здесь только ФОРМА контракта (не маски/применение/головы/переобучение).
- **Аддитивно:** `use_cp`/`cp_on` СОХРАНЯЕМ (Insane Bravery работает). Новые `strat_<phase>` головы — добавляются, **не применяются** (no-op до под-проекта 3).
- **Одна стратагема на фазу на сторону** (YAGNI; контракт расширяемый).
- **Только MAIN-timing стратагемы** в головах активной стороны (реакции overwatch/smokescreen/go_to_ground/heroic — REACTION-timing, гонятся в ход оппонента отдельной системой → НЕ в эти головы). Уточнение к спеке (она писала «легальные в фазе»; реакции исключаем как не-действия активного хода).
- **Фазы:** `STRATAGEM_PHASES = (COMMAND, MOVEMENT, SHOOTING, CHARGE, FIGHT)`.
- **Подтипы command_reroll по фазе:** fight/shooting → `hit,wound`; charge → `charge`; movement → `advance`; command → (command_reroll нет в command).
- **Язык:** комментарии/логи русские. Линт: `ruff check --fix <файл>`. Контракт меняет obs/action-dim → чекпойнты ломаются (обрабатывается в под-проекте 5; здесь не чиним).
- Baseline `tests/engine/` ~23 предсуществующих падения.
- DRY/YAGNI/TDD; коммит-сообщение русское + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/engine/phases/stratagems.py` | `STRATAGEM_PHASES`, `stratagem_action_choices/index/str` — единый источник истины | 1 |
| `core/models/action_contract.py` | `ordered_action_keys` += пофазные strat-головы | 2 |
| `core/engine/phases/legacy_compiler.py` | `default_action_dict` += strat-ключи = 0 | 2 |
| `core/envs/warhamEnv.py` | `action_space` += strat-головы (Discrete) | 2 |
| `tests/engine/phases/test_stratagem_action_choices.py` (новый) | хелпер индексации | 1 |
| `tests/models/test_action_contract_stratagems.py` (новый) | контракт+env round-trip | 2 |

---

## Task 1: хелпер индексации `stratagem_action_choices`

**Files:** Modify `core/engine/phases/stratagems.py`; Test `tests/engine/phases/test_stratagem_action_choices.py` (новый).

**Interfaces:**
- Produces:
  - `STRATAGEM_PHASES: tuple[Phase, ...] = (COMMAND, MOVEMENT, SHOOTING, CHARGE, FIGHT)`
  - `stratagem_action_choices(phase: Phase) -> list[str]` — `["none", ...]`, MAIN-timing стратагемы фазы, command_reroll развёрнут в подтипы.
  - `stratagem_choice_index(phase: Phase, choice: str) -> int`
  - `stratagem_choice_str(phase: Phase, idx: int) -> str`

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_stratagem_action_choices.py`:
```python
from core.engine.phases.stratagems import (
    STRATAGEM_PHASES,
    stratagem_action_choices,
    stratagem_choice_index,
    stratagem_choice_str,
)
from core.engine.phases.types import Phase


def test_phases_set():
    assert STRATAGEM_PHASES == (Phase.COMMAND, Phase.MOVEMENT, Phase.SHOOTING, Phase.CHARGE, Phase.FIGHT)


def test_choices_index0_is_none_all_phases():
    for ph in STRATAGEM_PHASES:
        assert stratagem_action_choices(ph)[0] == "none"


def test_fight_choices_have_command_reroll_subtypes_and_hungry_void():
    ch = stratagem_action_choices(Phase.FIGHT)
    assert "command_reroll:hit" in ch
    assert "command_reroll:wound" in ch
    assert "hungry_void" in ch
    assert "command_reroll" not in ch  # только подтипы, не голый id


def test_shooting_choices_command_reroll_subtypes_no_reactions():
    ch = stratagem_action_choices(Phase.SHOOTING)
    assert "command_reroll:hit" in ch and "command_reroll:wound" in ch
    # реакции (REACTION-timing) исключены
    assert "go_to_ground" not in ch
    assert "smokescreen" not in ch


def test_charge_and_movement_subtypes():
    assert "command_reroll:charge" in stratagem_action_choices(Phase.CHARGE)
    assert "command_reroll:advance" in stratagem_action_choices(Phase.MOVEMENT)
    # heroic_intervention/overwatch (REACTION) исключены
    assert "heroic_intervention" not in stratagem_action_choices(Phase.CHARGE)
    assert "overwatch" not in stratagem_action_choices(Phase.MOVEMENT)


def test_command_has_insane_bravery():
    ch = stratagem_action_choices(Phase.COMMAND)
    assert "insane_bravery" in ch


def test_index_str_roundtrip():
    for ph in STRATAGEM_PHASES:
        for i, s in enumerate(stratagem_action_choices(ph)):
            assert stratagem_choice_index(ph, s) == i
            assert stratagem_choice_str(ph, i) == s
    assert stratagem_choice_str(Phase.FIGHT, 999) == "none"
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_choices.py -v`
Expected: FAIL — `ImportError: cannot import name 'STRATAGEM_PHASES'`.

- [ ] **Step 3: Реализация** — в `core/engine/phases/stratagems.py` (после `REGISTRY`/`_BY_ID`, `Timing`/`Phase` уже импортированы из `types`):
```python
STRATAGEM_PHASES: tuple[Phase, ...] = (
    Phase.COMMAND, Phase.MOVEMENT, Phase.SHOOTING, Phase.CHARGE, Phase.FIGHT,
)

# Подтипы Command Re-roll по фазе (как принимает движок в reroll_roll; реакции-сейвы не в активной голове).
_COMMAND_REROLL_SUBTYPES_BY_PHASE: dict[Phase, tuple[str, ...]] = {
    Phase.FIGHT: ("hit", "wound"),
    Phase.SHOOTING: ("hit", "wound"),
    Phase.CHARGE: ("charge",),
    Phase.MOVEMENT: ("advance",),
}


def stratagem_action_choices(phase: Phase) -> list[str]:
    """Категории головы strat_<phase> (индекс 0 = none). Только MAIN-timing стратагемы фазы;
    command_reroll развёрнут в подтипы. Реакции (REACTION-timing) исключены (гонятся в ход оппонента).
    Детерминированный порядок (по REGISTRY + фикс. порядок подтипов) — стабильный индекс.
    """
    choices: list[str] = ["none"]
    for d in REGISTRY:
        if phase not in d.phases or d.timing is not Timing.MAIN:
            continue
        if d.id == "command_reroll":
            for sub in _COMMAND_REROLL_SUBTYPES_BY_PHASE.get(phase, ()):
                choices.append(f"command_reroll:{sub}")
        else:
            choices.append(d.id)
    return choices


def stratagem_choice_index(phase: Phase, choice: str) -> int:
    """Индекс категории; неизвестная строка → 0 (none)."""
    ch = stratagem_action_choices(phase)
    try:
        return ch.index(str(choice))
    except ValueError:
        return 0


def stratagem_choice_str(phase: Phase, idx: int) -> str:
    """Строка категории по индексу; вне диапазона → 'none'."""
    ch = stratagem_action_choices(phase)
    i = int(idx)
    return ch[i] if 0 <= i < len(ch) else "none"
```

- [ ] **Step 4: Запустить — PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_choices.py -v`
Expected: PASS. Затем `ruff check --fix core/engine/phases/stratagems.py tests/engine/phases/test_stratagem_action_choices.py`.

- [ ] **Step 5: Коммит**
```
git add core/engine/phases/stratagems.py tests/engine/phases/test_stratagem_action_choices.py
git commit -m "feat(strat): хелпер stratagem_action_choices/index/str (action-encoding п.1)"
```

---

## Task 2: проводка пофазных голов в контракт + env.action_space (аддитивно)

**Files:** Modify `core/models/action_contract.py` (`ordered_action_keys`), `core/engine/phases/legacy_compiler.py` (`default_action_dict`), `core/envs/warhamEnv.py` (`action_space` ~1045-1064). Test `tests/models/test_action_contract_stratagems.py` (новый).

**Interfaces:**
- Consumes: `STRATAGEM_PHASES`, `stratagem_action_choices` (Task 1).
- Produces: `ordered_action_keys(n)` содержит `strat_<phase>`/`strat_<phase>_unit` для всех `STRATAGEM_PHASES` (после per-unit голов); `use_cp`/`cp_on` сохранены; `default_action_dict` задаёт новые ключи=0; `env.action_space` объявляет новые головы (`strat_<phase>`=Discrete(len choices), `strat_<phase>_unit`=Discrete(len model)).

- [ ] **Step 1: Написать падающий тест**

Создать `tests/models/test_action_contract_stratagems.py`:
```python
from core.engine.phases.legacy_compiler import default_action_dict
from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices
from core.models.action_contract import (
    action_sizes_from_env,
    action_tensor_to_dict,
    ordered_action_keys,
)
from tests.engine.phases._helpers import build_env

import torch


def test_ordered_keys_have_strat_heads_and_keep_use_cp():
    keys = ordered_action_keys(2)
    for ph in STRATAGEM_PHASES:
        assert f"strat_{ph.value}" in keys
        assert f"strat_{ph.value}_unit" in keys
    assert "use_cp" in keys and "cp_on" in keys  # аддитивно: не убрали


def test_default_action_dict_sets_strat_zero():
    ad = default_action_dict(2)
    for ph in STRATAGEM_PHASES:
        assert ad[f"strat_{ph.value}"] == 0
        assert ad[f"strat_{ph.value}_unit"] == 0
    assert ad["use_cp"] == 0


def test_env_action_space_declares_strat_heads_with_sizes():
    env = build_env()  # 2 model units
    spaces = env.action_space.spaces
    for ph in STRATAGEM_PHASES:
        assert int(spaces[f"strat_{ph.value}"].n) == len(stratagem_action_choices(ph))
        assert int(spaces[f"strat_{ph.value}_unit"].n) == 2


def test_action_sizes_and_tensor_roundtrip():
    env = build_env()
    sizes = action_sizes_from_env(env, 2)  # не падает: все ordered-ключи есть в action_space
    keys = ordered_action_keys(2)
    assert len(sizes) == len(keys)
    vec = torch.zeros((1, len(keys)), dtype=torch.long)
    ad = action_tensor_to_dict(vec, 2)
    assert set(ad.keys()) == set(keys)
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/models/test_action_contract_stratagems.py -v`
Expected: FAIL (нет strat-ключей в ordered_action_keys / action_space).

- [ ] **Step 3: Реализация**

`core/models/action_contract.py` — добавить импорт и расширить `ordered_action_keys`:
```python
from core.engine.phases.stratagems import STRATAGEM_PHASES
```
```python
def ordered_action_keys(len_model: int) -> list[str]:
    n = int(len_model)
    keys = list(BASE_ACTION_HEADS)
    keys += [f"move_num_{i}" for i in range(n)]
    keys += [f"shoot_num_{i}" for i in range(n)]
    keys += [f"charge_num_{i}" for i in range(n)]
    for ph in STRATAGEM_PHASES:
        keys.append(f"strat_{ph.value}")
        keys.append(f"strat_{ph.value}_unit")
    return keys
```
`core/engine/phases/legacy_compiler.py` — расширить `default_action_dict`:
```python
from core.engine.phases.stratagems import STRATAGEM_PHASES
```
```python
def default_action_dict(len_model: int) -> dict[str, int]:
    n = int(len_model)
    action: dict[str, int] = {"move": 4, "attack": 1, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        action[f"move_num_{i}"] = 0
        action[f"shoot_num_{i}"] = 0
        action[f"charge_num_{i}"] = 0
    for ph in STRATAGEM_PHASES:
        action[f"strat_{ph.value}"] = 0
        action[f"strat_{ph.value}_unit"] = 0
    return action
```
`core/envs/warhamEnv.py` — после per-unit голов (после строки `action_spaces[f"charge_num_{i}"] = ...`, перед `self.action_space = spaces.Dict(...)`):
```python
        # Под-проект 1: пофазные головы выбора стратагемы (аддитивно; применение — под-проект 3).
        from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices
        for _ph in STRATAGEM_PHASES:
            action_spaces[f"strat_{_ph.value}"] = spaces.Discrete(len(stratagem_action_choices(_ph)))
            action_spaces[f"strat_{_ph.value}_unit"] = spaces.Discrete(len(model))
```
(Импорт `spaces` уже есть в модуле; локальный импорт STRATAGEM_PHASES во избежание цикла на уровне модуля.)

- [ ] **Step 4: Запустить — PASS + регрессия контракта**

Run: `python -m pytest tests/models/test_action_contract_stratagems.py -v`
Expected: PASS. Затем регрессия путей, читающих контракт:
`python -m pytest tests/models/ tests/engine/phases/ -q`
Expected: проверить, что добавление голов не уронило существующее (масочные/контракт-тесты используют ordered_action_keys). Если падают тесты, ожидающие фиксированный набор ключей/размер obs — это ожидаемое следствие смены контракта: **обновить их под новый контракт** (не подгонять логику; добавить strat-ключи в ожидания), и зафиксировать в отчёте. `ruff check --fix` по трём `.py` + тесту.

- [ ] **Step 5: engine-regression-reviewer + Коммит**

Запустить субагента `engine-regression-reviewer` на диффе (контракт — общий для всех алго). Затем:
```
git add core/models/action_contract.py core/engine/phases/legacy_compiler.py core/envs/warhamEnv.py tests/models/test_action_contract_stratagems.py
git commit -m "feat(contract): пофазные головы strat_<phase> в action-space (аддитивно, action-encoding п.1)"
```

---

## Self-Review

**Spec coverage:**
- `stratagem_action_choices/index/str` + STRATAGEM_PHASES — Task 1. ✅
- Подтипы command_reroll как отдельные индексы — Task 1 (`_COMMAND_REROLL_SUBTYPES_BY_PHASE`). ✅
- Пофазные головы `strat_<phase>`/`strat_<phase>_unit` в ordered_action_keys + env.action_space + default_action_dict — Task 2. ✅
- Аддитивно (use_cp/cp_on сохранены, no-op применение) — Task 2 (тест `..._keep_use_cp`). ✅
- Сериализация round-trip (action_sizes_from_env, action_tensor_to_dict) — Task 2. ✅
- MAIN-timing фильтр (реакции исключены) — Task 1 (уточнение к спеке, явно в Global Constraints). ✅
- Применение НЕ требуется (под-проект 3); движок не падает (use_cp/cp_on живы, новые головы no-op) — обеспечено аддитивностью. ✅
- obs-dim mismatch — вне области (под-проект 5); здесь контракт растёт, чекпойнты несовместимы (ожидаемо).

**Placeholder scan:** весь код приведён; Step 4 Task 2 честно предупреждает о возможном обновлении контракт-зависимых тестов (реальная последовательность, не placeholder).

**Type consistency:** `stratagem_action_choices(phase)->list[str]`, `stratagem_choice_index(phase,str)->int`, `stratagem_choice_str(phase,int)->str`, `STRATAGEM_PHASES: tuple[Phase,...]`; ключи `strat_{ph.value}`/`strat_{ph.value}_unit` — единообразны в Task 1/2.

**Примечание:** под-проекты 2-5 (маски/применение/головы-алго/переобучение) — отдельные спеки/планы; этот план самодостаточен (контракт растёт, движок работает через сохранённые use_cp/cp_on).

---

## Execution Handoff

См. ниже выбор способа исполнения.
