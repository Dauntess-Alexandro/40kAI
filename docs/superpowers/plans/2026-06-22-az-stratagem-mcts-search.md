# Стратагемы как действия — Под-проект 4 (AZ MCTS) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Завести strat-выбор в joint_tuple AZ MCTS (через `legacy_patch` на опциях стратагем) и добавить окна стратагем в shooting/charge, чтобы дерево искало strat-измерения и давало ненулевой policy-таргет (AZ/GAZ учатся стратагемам).

**Architecture:** Опции стратагем (fight/shooting/charge) задают `legacy_patch={strat_<phase>: idx, strat_<phase>_unit: u}` → `compile_options_to_action_dict` → action_dict → joint_tuple различает кандидатов. `generate_windows` добавляет стратагем-окна shooting/charge. Применение и policy-таргет — готовы (п.3 `_apply_action_stratagem` + `_final_policy_from_visits`). Только AZ/GAZ.

**Tech Stack:** Python 3.12+, NumPy, pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-az-stratagem-mcts-search-design.md`. **Под-проект 4 из 5**, **только AZ/GAZ** (DQN/PPO головы бесплатны → п.5; GMZ/SMZ — вне).
- **legacy_patch** опции стратагемы: `{f"strat_{phase.value}": stratagem_choice_index(phase, choice), f"strat_{phase.value}_unit": unit}`. `choice` = id или `command_reroll:<sub>`. insane_bravery — СОХРАНЯЕТ `use_cp`/`cp_on` + добавляет strat_command.
- **Окна стратагем shooting/charge** в `generate_windows` по образцу fight (отдельные per-unit окна: PASS + `command_reroll_options_for_unit`).
- **Применение/таргет — готовы (п.3).** Старый fight-план/MC-хук сосуществуют (anti-double, sequenced — снос в п.5).
- `stratagem_choice_index` определён в `core/engine/phases/stratagems.py` (тот же модуль — без импорта; в option_generator — импортировать).
- Язык RU; `ruff check --fix`; baseline `tests/engine/` 23; коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. DRY/YAGNI/TDD. **engine-regression-reviewer обязателен** (AZ-внутренности).

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/engine/phases/stratagems.py` | `legal_stratagem_options` — strat legacy_patch (command_reroll + general) | 1 |
| `core/engine/phases/option_generator.py` | `command_reroll_options_for_unit` — strat legacy_patch; `generate_windows` — окна shooting/charge | 1, 2 |
| `tests/engine/phases/test_az_stratagem_search.py` (новый) | legacy_patch/joint; окна; policy-таргет; anti-double | 1, 2, 3 |

---

## Task 1: strat `legacy_patch` на опциях стратагем

**Files:** Modify `core/engine/phases/stratagems.py` (`legal_stratagem_options`, ~319-351), `core/engine/phases/option_generator.py` (`command_reroll_options_for_unit` ~147-162 + импорт). Test `tests/engine/phases/test_az_stratagem_search.py` (новый).

**Interfaces:**
- Consumes: `stratagem_choice_index` (п.1 helper).
- Produces: опции стратагем несут `legacy_patch` с strat-головами → `compile_options_to_action_dict` ставит их → `joint_tuple` различает кандидатов.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_az_stratagem_search.py`:
```python
from core.engine.phases.legacy_compiler import compile_options_to_action_dict, default_action_dict
from core.engine.phases.option_generator import (
    command_reroll_options_for_unit,
    fight_stratagem_options_for_unit,
)
from core.engine.phases.stratagems import stratagem_choice_index
from core.engine.phases.types import ActionKind, Phase
from core.models.option_candidates import joint_tuple_from_action_dict
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []


def test_fight_command_reroll_option_carries_strat_patch():
    env = build_env()
    _setup(env)
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    cr = [o for o in opts if o.meta.get("stratagem_id") == "command_reroll" and o.meta.get("reroll_roll") == "hit"][0]
    assert cr.legacy_patch["strat_fight"] == stratagem_choice_index(Phase.FIGHT, "command_reroll:hit")
    assert cr.legacy_patch["strat_fight_unit"] == 0


def test_fight_hungry_void_option_carries_strat_patch():
    env = build_env()
    _setup(env)
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    hv = [o for o in opts if o.meta.get("stratagem_id") == "hungry_void"][0]
    assert hv.legacy_patch["strat_fight"] == stratagem_choice_index(Phase.FIGHT, "hungry_void")
    assert hv.legacy_patch["strat_fight_unit"] == 0


def test_command_reroll_options_for_unit_carries_strat_patch():
    env = build_env()
    _setup(env)
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound"))
    o = [x for x in opts if x.meta.get("reroll_roll") == "wound"][0]
    assert o.legacy_patch["strat_shooting"] == stratagem_choice_index(Phase.SHOOTING, "command_reroll:wound")
    assert o.legacy_patch["strat_shooting_unit"] == 0


def test_compile_and_joint_differs_with_strat():
    env = build_env()
    _setup(env)
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    cr = [o for o in opts if o.param.get("reroll_roll") == "hit"][0]
    n = len(env.unit_health)
    ad = compile_options_to_action_dict([cr], n)
    assert ad["strat_fight"] != 0
    jt_with = joint_tuple_from_action_dict(ad, n)
    jt_none = joint_tuple_from_action_dict(default_action_dict(n), n)
    assert jt_with != jt_none  # кандидаты с/без реролла НЕ схлопываются
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_az_stratagem_search.py -k "carries_strat or joint_differs" -v`
Expected: FAIL (legacy_patch пустой → `KeyError`/`strat_fight==0`).

- [ ] **Step 3: Реализация**

`core/engine/phases/stratagems.py::legal_stratagem_options` — command_reroll-ветка (~319-336): заменить `legacy_patch={}` на strat-патч:
```python
            if d.id == "command_reroll":
                for roll in ("hit", "wound"):
                    _choice = f"command_reroll:{roll}"
                    options.append(
                        ActionOption(
                            kind=ActionKind.USE_STRATAGEM,
                            unit_idx=i,
                            param={"stratagem_id": d.id, "reroll_roll": roll},
                            legacy_patch={
                                f"strat_{phase.value}": stratagem_choice_index(phase, _choice),
                                f"strat_{phase.value}_unit": i,
                            },
                            meta={
                                "stratagem_id": d.id,
                                "cp_cost": d.cp_cost,
                                "timing": d.timing,
                                "scope": d.scope,
                                "reroll_roll": roll,
                            },
                        )
                    )
                continue
```
Общая ветка (~337-351): заменить вычисление `legacy_patch`:
```python
            if d.id == "insane_bravery":
                legacy_patch = {
                    "use_cp": 1,
                    "cp_on": i,
                    f"strat_{phase.value}": stratagem_choice_index(phase, d.id),
                    f"strat_{phase.value}_unit": i,
                }
            else:
                legacy_patch = {
                    f"strat_{phase.value}": stratagem_choice_index(phase, d.id),
                    f"strat_{phase.value}_unit": i,
                }
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
```
(`stratagem_choice_index` — в этом же модуле, импорт не нужен.)

`core/engine/phases/option_generator.py`: импорт расширить:
```python
from core.engine.phases.stratagems import Trigger, by_id, legal_stratagem_options, stratagem_choice_index
```
В `command_reroll_options_for_unit` (~148-161) заменить `legacy_patch={}`:
```python
            legacy_patch={
                f"strat_{phase.value}": stratagem_choice_index(phase, f"command_reroll:{roll}"),
                f"strat_{phase.value}_unit": i,
            },
```

- [ ] **Step 4: Запустить — PASS + регрессия**

Run: `python -m pytest tests/engine/phases/test_az_stratagem_search.py -v` → PASS.
Регрессия (опции шарятся с windowed/обс): `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS (windowed run_fight читает `meta`, не legacy_patch; obs читает meta — не затронуто; но проверить `test_command_reroll.py`/`test_windowed_*`/`test_option_candidates.py`). Если падает контракт-тест на пустой legacy_patch — обновить ожидание. `ruff check --fix` по двум `.py` + тест.

- [ ] **Step 5: Коммит**
```
git add core/engine/phases/stratagems.py core/engine/phases/option_generator.py tests/engine/phases/test_az_stratagem_search.py
git commit -m "feat(strat): strat-головы в legacy_patch опций стратагем (joint_tuple различает выбор)"
```

---

## Task 2: окна стратагем shooting/charge в `generate_windows`

**Files:** Modify `core/engine/phases/option_generator.py` (`generate_windows`, ~207-261). Test `tests/engine/phases/test_az_stratagem_search.py`.

**Interfaces:**
- Consumes: `command_reroll_options_for_unit` (Task 1, с legacy_patch).
- Produces: `generate_windows` содержит per-unit стратагем-окна для shooting/charge (USE_STRATAGEM-опции).

- [ ] **Step 1: Написать падающий тест**
```python
from core.engine.phases.option_generator import generate_windows
from core.engine.phases.types import Phase as _Ph


def _strat_opts_for_phase(windows, phase):
    out = []
    for w in windows:
        if w.phase is phase:
            out += [o for o in w.options if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "command_reroll"]
    return out


def test_generate_windows_has_shooting_charge_stratagem_options():
    env = build_env()
    _setup(env)
    windows = generate_windows(env, "model")
    assert _strat_opts_for_phase(windows, _Ph.SHOOTING), "нет command_reroll-опций в shooting-окнах"
    assert _strat_opts_for_phase(windows, _Ph.CHARGE), "нет command_reroll-опций в charge-окнах"
    # и они несут strat legacy_patch
    sh = _strat_opts_for_phase(windows, _Ph.SHOOTING)[0]
    assert "strat_shooting" in sh.legacy_patch
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_az_stratagem_search.py -k generate_windows -v`
Expected: FAIL (shooting/charge-окна сейчас только action-опции).

- [ ] **Step 3: Реализация** — в `generate_windows` (option_generator.py), в циклах построения shooting- и charge-окон ДОБАВИТЬ отдельные per-unit стратагем-окна (после соответствующих action-окон). Найти блоки `for u in alive:` для SHOOTING (~225) и CHARGE (~237) и после каждого добавить:
```python
    for u in alive:
        _sopts = command_reroll_options_for_unit(e, side, u, phase=Phase.SHOOTING, rolls=("hit", "wound"))
        if _sopts:
            windows.append(
                DecisionWindow(
                    window_id=f"shooting_stratagem:{side}:{u}",
                    owner_side=side,
                    phase=Phase.SHOOTING,
                    sub_step=SubStep.PICK_SHOOT_TARGET,
                    timing=Timing.MAIN,
                    cursor_unit_idx=int(u),
                    options=[ActionOption(kind=ActionKind.PASS, unit_idx=int(u)), *_sopts],
                )
            )
```
и аналогично для CHARGE (`window_id=f"charge_stratagem:{side}:{u}"`, `phase=Phase.CHARGE`, `sub_step=SubStep.PICK_CHARGE_TARGET`, `rolls=("charge",)`). (`ActionOption`/`DecisionWindow`/`SubStep`/`Timing` уже импортированы в модуле.)

- [ ] **Step 4: Запустить — PASS + регрессия**

Run: `python -m pytest tests/engine/phases/test_az_stratagem_search.py -v` → PASS.
Регрессия: `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS (новые окна аддитивны; `build_turn_plan_candidates` итерирует все окна; проверить `test_option_candidates.py`/`test_windowed_*`). `python -m pytest tests/engine/ -q` → baseline 23 (если AZ n_actions/candidate-тесты сменили размер — обновить ожидания). `ruff check --fix core/engine/phases/option_generator.py`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add core/engine/phases/option_generator.py tests/engine/phases/test_az_stratagem_search.py
git commit -m "feat(strat): окна стратагем shooting/charge в generate_windows (AZ MCTS видит strat-выбор)"
```

---

## Task 3: policy-таргет не вырожден + anti-double + AZ/GAZ смоук

**Files:** Test `tests/engine/phases/test_az_stratagem_search.py`. Смоук — наблюдательный (контроллер).

**Interfaces:** Consumes Task 1–2.

- [ ] **Step 1: Написать тест policy-таргета (не вырожден)**
```python
def test_final_policy_from_visits_nondegenerate_for_strat_head():
    import numpy as np
    from core.models.alphazero_mcts import AlphaZeroMCTS  # см. фактическое имя класса в файле
    # Если прямой вызов _final_policy_from_visits сложен — построить корень с детьми,
    # у которых action_tuple[strat_fight_idx] != 0 у части, и проверить, что pi для strat_fight
    # имеет массу вне индекса 0. Реализатор: найти сигнатуру _final_policy_from_visits и
    # сконструировать минимальный root (Node с children по action_tuple, visit_count).
    # Цель ассерта: pi_targets[strat_fight_head_index][0] < 1.0 (не вся масса на none).
    ...
```
(ПРИМЕЧАНИЕ исполнителю: `_final_policy_from_visits` — приватный метод MCTS со специфичной сигнатурой. Если юнит-тест на него хрупок — заменить на интеграционную проверку: после короткого `play_episode_with_mcts`-смоука в записях `policy_targets` голова strat_fight имеет ненулевую массу вне index 0 хотя бы в одном шаге, ЛИБО зафиксировать через смоук Step 4. Не писать вырожденный тест ради галочки — согласовать с контроллером, если метод неудобен.)

- [ ] **Step 2: Написать тест anti-double (голова + старый fight-план)**
```python
def test_head_and_fight_plan_no_double_apply():
    env = build_env()
    _setup(env)
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    # и голова, и старый fight-план просят command_reroll на юните 0
    from core.engine.phases.stratagems import stratagem_choice_index
    action = {f"strat_fight": stratagem_choice_index(Phase.FIGHT, "command_reroll:hit"), f"strat_fight_unit": 0}
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    cp_before = env.modelCP
    with env.simulation_mode():
        env.fight_phase("model", action=action)
    # ровно одно списание CP (нет двойного применения)
    assert cp_before - env.modelCP <= 1
```

- [ ] **Step 3: Реализация** — кода не требуется (поведение из Task 1–2 + п.3). Прогнать тесты; если anti-double падает — диагностировать (`_apply_action_stratagem` ставит запись ПЕРЕД `_apply_pending_fight_stratagem_plan` в fight_phase → план видит `_command_reroll_record_exists` и не дублирует). Если policy-тест хрупок — перевести на смоук (Step 4), как помечено.

- [ ] **Step 4: Полный прогон + AZ/GAZ self-play смоук (контроллер)**

`python -m pytest tests/engine/phases/test_az_stratagem_search.py tests/engine/phases/ tests/models/ -q` → PASS.
`python -m pytest tests/engine/ -q` → baseline 23.
**Смоук (наблюдательный, контроллер):** короткий AZ self-play локально:
```
AZ_INFERENCE_SERVER=0 AZ_DISTRIBUTED_ACTORS=0 TRAIN_EPISODES_OVERRIDE=4 NUM_ACTORS=1 \
  PYTHONIOENCODING=utf-8 python train.py --algo alphazero_tree   # точную команду свериться с run-40kai/AGENTS.md
```
Ожидаемо: exit=0, без traceback; в agent-логах применяется стратагема через head-путь (`[STRATAGEM] applied=...`). Повторить для GAZ (`gumbel_az`). Если смоук недоступен в среде исполнителя — пометить DEFERRED-TO-CONTROLLER.

- [ ] **Step 5: Коммит**
```
git add tests/engine/phases/test_az_stratagem_search.py
git commit -m "test(strat): policy-таргет strat-головы не вырожден + anti-double голова/fight-план"
```

---

## Self-Review

**Spec coverage:**
- legacy_patch на опциях (command_reroll + general + command_reroll_options_for_unit) → strat в joint_tuple — Task 1. ✅
- Окна стратагем shooting/charge в generate_windows — Task 2. ✅
- Кандидаты не схлопываются (разный joint_tuple) — Task 1 (`test_compile_and_joint_differs`). ✅
- Применение/policy-таргет готовы (п.3 + `_final_policy_from_visits`) — Task 3 (тест/смоук). ✅
- Anti-double (голова vs fight-план) — Task 3. ✅
- insane_bravery + strat_command (сохраняя use_cp) — Task 1. ✅
- AZ/GAZ смоук, регрессия baseline 23, DQN/PPO/GMZ/SMZ не затронуты — Task 3 + engine-regression-reviewer. ✅
- Снос дублей/переобучение — п.5 (вне области). ✅

**Placeholder scan:** Task 1–2 — полный код. Task 3 Step 1 (policy-тест) честно помечен как потенциально хрупкий (приватный метод) с альтернативой-смоуком — это реальная инструкция/развилка исполнителю, не placeholder; контроллер адъюдицирует. Anti-double тест — полный.

**Type consistency:** `legacy_patch` ключи `strat_{phase.value}`/`_unit` едины с п.1/2/3; `stratagem_choice_index(phase, choice)` из п.1; окна — формат `DecisionWindow`/`ActionOption` как fight.

**Примечание:** взрыв кандидатов (кап 64) — open/тюнинг (спека), замер на смоуке; снос дубля fight-план↔голова — п.5.

---

## Execution Handoff

См. ниже выбор способа исполнения.
