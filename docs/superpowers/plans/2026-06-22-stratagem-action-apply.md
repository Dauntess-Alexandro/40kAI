# Стратагемы как действия — Под-проект 3 (применение) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Читать и применять головы `strat_<phase>` в env (movement/shooting/charge/fight) детерминированно с валидацией и anti-double-guard, + завести Insane Bravery на `strat_command` (наряду с `use_cp`). Старые пути не трогаем (снос — п.5).

**Architecture:** Метод `_apply_action_stratagem(side, phase, action)` в начале фазы читает голову, валидирует (легально+юнит+keyword+не-active) и применяет `_apply_stratagem`. Ставится ПЕРЕД существующими MC-хуком/fight-планом → те видят запись и не дублируют. Insane Bravery — через `_use_bravery` (триггер = провал battle-shock). Инертно в проде до п.4/5 (сети ещё не выдают головы); тестируется рукотворными action_dict.

**Tech Stack:** Python 3.12+, NumPy, pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-stratagem-action-apply-design.md`. **Под-проект 3 из 5** («стратагемы как действия»). П.1 (кодирование), п.2 (маски) — в коде.
- **(A)-sequenced:** головы применяются; **старые пути (`use_cp`/`cp_on`, MC-хук `_apply_phase_command_reroll`, fight-план `_apply_pending_fight_stratagem_plan`, reaction_policy) ОСТАЮТСЯ.** Снос — п.5.
- **Anti-double-guard:** `_stratagem_already_active(side, base_id, unit, phase)` (существует) — пропуск уже-применённых. `_apply_action_stratagem` вызывается ПЕРЕД старыми хуками в каждой фазе.
- **Подтип:** `command_reroll:hit` → base_id=`command_reroll`, reroll_roll=`hit`. Прочие стратагемы — без reroll_roll.
- **Insane Bravery** — особый триггер (провал battle-shock), интеграция через `_use_bravery`, НЕ через `_apply_action_stratagem`.
- **Инертность:** головы=0 пока сети их не выдают (до п.4/5) → no-op; не пугаться отсутствия эффекта вживую.
- Язык RU; `ruff check --fix`; baseline `tests/engine/` 23; коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. DRY/YAGNI/TDD.

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/envs/warhamEnv.py` | `_apply_action_stratagem` + вызовы в фазах + `action` в fight_phase + bravery через strat_command | 1, 2, 3 |
| `tests/engine/phases/test_stratagem_action_apply.py` (новый) | helper + фазы + anti-double + bravery + parity | 1, 2, 3 |

---

## Task 1: `_apply_action_stratagem`

**Files:** Modify `core/envs/warhamEnv.py`; Test `tests/engine/phases/test_stratagem_action_apply.py` (новый).

**Interfaces:**
- Consumes: `stratagem_choice_str`, `by_id` (stratagems); `_stratagem_choice_legal` (п.2), `_stratagem_already_active`, `_unit_has_keyword`, `_apply_stratagem`.
- Produces: `Warhammer40kEnv._apply_action_stratagem(side: str, phase, action: dict) -> None` — читает `strat_<phase>`/`strat_<phase>_unit`, валидирует, применяет (anti-double).

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_stratagem_action_apply.py`:
```python
from core.engine.phases.stratagems import stratagem_action_choices
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.battle_round = 1
    env.phase = "fight"


def _idx(phase, choice):
    return stratagem_action_choices(phase).index(choice)


def test_apply_action_stratagem_command_reroll_fight():
    env = build_env()
    _setup(env)
    action = {f"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), f"strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert any(
        r.get("effect_id") == "command_reroll" and r.get("reroll_roll") == "hit" and int(r.get("unit_idx", -1)) == 0
        for r in env.active_stratagem_effects
    )
    assert ("model", "command_reroll", 1, "fight", 0) in env.stratagem_used


def test_apply_action_stratagem_none_idx0_noop():
    env = build_env()
    _setup(env)
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": 0, "strat_fight_unit": 0})
    assert env.active_stratagem_effects == []
    assert env.modelCP == 2


def test_apply_action_stratagem_illegal_no_cp():
    env = build_env()
    _setup(env, cp=0)
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.active_stratagem_effects == []


def test_apply_action_stratagem_dead_unit_noop():
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0.0
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 1}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.active_stratagem_effects == []


def test_apply_action_stratagem_hungry_void_needs_necrons():
    env = build_env()
    _setup(env)
    hv = _idx(Phase.FIGHT, "hungry_void")
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": hv, "strat_fight_unit": 0})
    assert not any(r[1] == "hungry_void" for r in env.stratagem_used)  # нет necrons keyword
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": hv, "strat_fight_unit": 0})
    assert any(r[1] == "hungry_void" for r in env.stratagem_used)


def test_apply_action_stratagem_anti_double():
    env = build_env()
    _setup(env)
    # имитируем, что MC-хук уже применил command_reroll на юните 0 в fight
    env.stratagem_used = [("model", "command_reroll", 1, "fight", 0)]
    cp_before = env.modelCP
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.modelCP == cp_before  # не списан повторно
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -v`
Expected: FAIL — `AttributeError: ... '_apply_action_stratagem'`.

- [ ] **Step 3: Реализация** — в `core/envs/warhamEnv.py` (рядом с `_apply_action_stratagem`-семейством, напр. после `_apply_phase_command_reroll`):
```python
    def _apply_action_stratagem(self, side: str, phase, action) -> None:
        """Применить стратагему из головы strat_<phase> (action-driven, детерминированно).

        Валидация: легальна (_stratagem_choice_legal) + конкретный юнит жив + имеет keyword +
        не применена уже (_stratagem_already_active, anti-double с MC-хуком/fight-планом).
        Вызывается в начале фазы ДО старых хуков. Голова idx=0 (none) → no-op.
        """
        if not isinstance(action, dict):
            return
        from core.engine.phases.stratagems import by_id, stratagem_choice_str

        phase_str = phase.value if hasattr(phase, "value") else str(phase)
        idx = int(action.get(f"strat_{phase_str}", 0) or 0)
        if idx <= 0:
            return
        choice = stratagem_choice_str(phase, idx)
        if choice == "none":
            return
        base_id = choice.split(":", 1)[0]
        sub = choice.split(":", 1)[1] if ":" in choice else None
        unit = int(action.get(f"strat_{phase_str}_unit", 0) or 0)
        is_model = side == "model"
        health = self.unit_health if is_model else self.enemy_health
        unit_data = self.unit_data if is_model else self.enemy_data
        if not (0 <= unit < len(health)) or health[unit] <= 0:
            return
        if not self._stratagem_choice_legal(side, phase, choice):
            return
        try:
            d = by_id(base_id)
        except KeyError:
            return
        if d.keyword_req and not all(self._unit_has_keyword(unit_data[unit], kw) for kw in d.keyword_req):
            return
        if self._stratagem_already_active(side, base_id, unit, phase_str):
            return
        try:
            if sub is not None:
                _apply_stratagem(self, side, base_id, unit, phase=phase_str, reroll_roll=sub)
            else:
                _apply_stratagem(self, side, base_id, unit, phase=phase_str)
        except Exception as exc:
            self._log(
                f"[STRATAGEM] action-head не применил {choice!r} side={side} unit={unit} "
                f"phase={phase_str}: {exc}"
            )
```

- [ ] **Step 4: Запустить — PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -v`
Expected: PASS. Затем `ruff check --fix core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_apply.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_apply.py
git commit -m "feat(env): _apply_action_stratagem — применение strat_<phase> голов (валидация+anti-double)"
```

---

## Task 2: вызовы `_apply_action_stratagem` в фазах (+ action в fight_phase)

**Files:** Modify `core/envs/warhamEnv.py` (movement/shooting/charge/fight_phase + 2 fight call sites). Test `tests/engine/phases/test_stratagem_action_apply.py`.

**Interfaces:**
- Consumes: `_apply_action_stratagem` (Task 1).
- Produces: фазы применяют strat-головы в начале (ДО старых хуков); `fight_phase(self, side, action=None)`.

- [ ] **Step 1: Написать падающий тест**
```python
from tests.engine.phases._helpers import flat_default_action


def test_movement_phase_applies_strat_head_advance():
    env = build_env()
    _setup(env)
    env.phase = "movement"
    action = flat_default_action(len(env.unit_health))
    action["strat_movement"] = _idx(Phase.MOVEMENT, "command_reroll:advance")
    action["strat_movement_unit"] = 0
    with env.simulation_mode():
        env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))
    assert any(r[1] == "command_reroll" and r[3] == "movement" for r in env.stratagem_used)


def test_fight_phase_action_param_applies_strat_head():
    env = build_env()
    _setup(env)
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    action = flat_default_action(len(env.unit_health))
    action["strat_fight"] = _idx(Phase.FIGHT, "command_reroll:wound")
    action["strat_fight_unit"] = 0
    with env.simulation_mode():
        env.fight_phase("model", action=action)
    assert any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)


def test_fight_phase_no_action_is_parity():
    env = build_env()
    _setup(env)
    with env.simulation_mode():
        env.fight_phase("model")  # без action — старый путь, не падает
    assert not any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -k "movement_phase_applies or fight_phase_action or fight_phase_no_action" -v`
Expected: FAIL (movement не применяет; `fight_phase()` не принимает `action`).

- [ ] **Step 3: Реализация**

В `fight_phase` (warhamEnv.py:7544-7546) изменить сигнатуру и добавить вызов ПЕРЕД pending-планом:
```python
    def fight_phase(self, side: str, action=None):
        self.begin_phase(side, "fight")
        if action is not None:
            self._apply_action_stratagem(side, Phase.FIGHT, action)
        self._apply_pending_fight_stratagem_plan(side)
```
(Импортировать `Phase` из `core.engine.phases.types` локально в методе, если не импортирован на уровне модуля.)
Обновить вызовы fight_phase, где есть `action` в scope: warhamEnv.py:7909 `self.fight_phase("enemy")` → `self.fight_phase("enemy", action=action)`; :8402 `self.fight_phase("model")` → `self.fight_phase("model", action=action)`. Вызов :8865 (manual, нет action) — оставить `self.fight_phase("enemy")`.

В `movement_phase` (после `begin_phase`, ПЕРЕД остальной логикой), `shooting_phase` и `charge_phase` (после `begin_phase`, ПЕРЕД существующим `_apply_phase_command_reroll`-хуком) добавить:
```python
        if action is not None:
            self._apply_action_stratagem(side, Phase.<PHASE>, action)
```
где `<PHASE>` = MOVEMENT/SHOOTING/CHARGE соответственно. (В shooting/charge — строго ПЕРЕД `self._apply_phase_command_reroll(...)`, чтобы голова поставила запись первой и MC-хук не дублировал через `_command_reroll_record_exists`.)

- [ ] **Step 4: Запустить — PASS + регрессия**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -v` → PASS.
Регрессия: `python -m pytest tests/engine/phases/ tests/models/ -q` → PASS (фазовые/windowed/MC тесты не сломаны — добавление `action=None`-ветки и проброса не меняет поведение при нулевых головах). `python -m pytest tests/engine/ -q` → baseline 23 (тот же набор). `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_apply.py
git commit -m "feat(env): применять strat-головы в начале movement/shooting/charge/fight (action в fight_phase)"
```

---

## Task 3: Insane Bravery через `strat_command`

**Files:** Modify `core/envs/warhamEnv.py` (`command_phase`, ветки `_use_bravery` ~5320 model и ~5398 enemy). Test `tests/engine/phases/test_stratagem_action_apply.py`.

**Interfaces:**
- Consumes: `stratagem_choice_str` (stratagems), `Phase`.
- Produces: `command_phase` применяет Insane Bravery, если `strat_command`-голова = insane_bravery и `strat_command_unit==i` (наряду с `use_cp`/`cp_on`); только при провале battle-shock (существующий триггер).

- [ ] **Step 1: Написать падающий тест**
```python
def test_command_strat_head_triggers_bravery(monkeypatch):
    env = build_env()
    _setup(env)
    env.phase = "command"
    # форсим провал battle-shock у юнита 0
    monkeypatch.setattr(env, "_unit_passes_battle_shock", lambda side, i: False, raising=False)
    action = flat_default_action(len(env.unit_health))
    action["strat_command"] = _idx(Phase.COMMAND, "insane_bravery")
    action["strat_command_unit"] = 0
    with env.simulation_mode():
        env.command_phase("model", action=action)
    assert any(r[1] == "insane_bravery" for r in env.stratagem_used)
```
(ПРИМЕЧАНИЕ исполнителю: имя метода проверки battle-shock уточнить по факту — в command_phase найди, как определяется провал теста для юнита, и замокай ИМЕННО его, чтобы юнит 0 провалил. Если battle-shock определяется иначе (бросок), сетапь seed/CP так, чтобы провал был детерминирован. Тест должен реально проверять: strat_command→bravery применён.)

- [ ] **Step 2: Запустить — упадёт.** Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -k command_strat_head -v` → FAIL.

- [ ] **Step 3: Реализация** — в `command_phase`, в обеих ветках `_use_bravery` (model ~5320, enemy ~5398), РАСШИРИТЬ action-fallback. Модель (~5320), где сейчас:
```python
                            _use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
```
заменить на:
```python
                            _use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
                            if not _use_bravery and isinstance(action, dict):
                                from core.engine.phases.stratagems import stratagem_choice_str
                                from core.engine.phases.types import Phase as _Ph
                                _cmd_choice = stratagem_choice_str(_Ph.COMMAND, int(action.get("strat_command", 0) or 0))
                                if _cmd_choice == "insane_bravery" and int(action.get("strat_command_unit", 0) or 0) == i:
                                    _use_bravery = True
```
Enemy-ветку (~5398), где `_use_bravery = (use_cp == 1 and cp_on == i)` (use_cp/cp_on — локальные из action) — добавить аналогичную проверку strat_command после неё:
```python
                            if not _use_bravery and isinstance(action, dict):
                                from core.engine.phases.stratagems import stratagem_choice_str
                                from core.engine.phases.types import Phase as _Ph
                                if stratagem_choice_str(_Ph.COMMAND, int(action.get("strat_command", 0) or 0)) == "insane_bravery" and int(action.get("strat_command_unit", 0) or 0) == i:
                                    _use_bravery = True
```

- [ ] **Step 4: Запустить — PASS + регрессия.** Run: `python -m pytest tests/engine/phases/test_stratagem_action_apply.py -v` → PASS; `python -m pytest tests/engine/phases/ -q` → PASS (bravery через use_cp по-прежнему работает). `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_apply.py
git commit -m "feat(env): Insane Bravery через strat_command (наряду с use_cp, sequenced)"
```

---

## Self-Review

**Spec coverage:**
- `_apply_action_stratagem` (read+validate+apply, anti-double) — Task 1. ✅
- Вызовы в movement/shooting/charge/fight (голова ДО старых хуков) + action в fight_phase — Task 2. ✅
- Insane Bravery через strat_command (триггер battle-shock, сосуществует с use_cp) — Task 3. ✅
- Подтип command_reroll → reroll_roll — Task 1. ✅
- Anti-double (_stratagem_already_active) — Task 1 + тест; порядок «голова раньше хуков» — Task 2. ✅
- Старые пути не трогаем (sequenced) — ни одна задача их не меняет. ✅
- Parity при нулевых головах — Task 2 (`fight_phase()` без action), общая регрессия. ✅
- Инертность до п.4/5 — головы=0 в проде; тесты рукотворные. ✅

**Placeholder scan:** код полный. Task 3 Step 1 помечает: исполнитель уточняет имя метода battle-shock-провала по факту (это реальная сверка с кодом, не placeholder — альтернатива: детерминировать провал через seed). Допустимо как явная инструкция исполнителю.

**Type consistency:** `_apply_action_stratagem(side, phase, action)->None` (Task 1) ровно как зовётся в Task 2; ключи `strat_{phase.value}`/`_unit` едины с п.1; `stratagem_choice_str`/`stratagem_action_choices` из п.1.

**Примечание:** инертно в проде до п.4/5 (сети не выдают головы); под-проект самодостаточен (env-применение готово к обученным головам).

---

## Execution Handoff

См. ниже выбор способа исполнения.
