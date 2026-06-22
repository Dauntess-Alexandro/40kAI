# Command Re-roll Fidelity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Привести core-стратагему **Command Re-roll** в 40kAI от fight-only/wound-only приближения к правилу Wahapedia 10ed (реакция в любой фазе на любой применимый бросок), поэтапно от низкорискового расширения к архитектурному roll-context и AI-интеграции.

**Architecture:** Этап 1 расширяет существующий `effects`-механизм в `attack()` на hit+wound (attacker-side) без новой архитектуры. Этап 2 вводит реактивный `reroll_decider`-hook в `attack()` (точка «после броска») + инвариант «кость нельзя перебросить дважды», что позволяет корректно атрибутировать save-ре-ролл защитнику. Этап 3 распространяет hook на все фазы/броски (advance, charge 2D6, стрельба, кол-во атак), пересматривает лимит на «per-roll». Этап 4 подключает value-reaction-policy к hook.

**Tech Stack:** Python 3.12+, NumPy, Gymnasium-env (`Warhammer40kEnv`), pytest. Платформа Windows.

## Global Constraints

- **Язык:** все логи/комментарии/сообщения об ошибках — русский; формат ошибки «что + где + что делать».
- **Платформа:** Windows; запуск тестов через `pytest` (терминал допустим для тестов, см. AGENTS.md «тесты при надобности»).
- **Источник правды по правилу:** [Command Re-roll](https://wahapedia.ru/wh40k10ed/the-rules/core-stratagems/) — 1 CP, любая фаза, реакция после броска; [Re-rolls commentary](https://wahapedia.ru/wh40k10ed/the-rules/rules-commentary/) — «кость нельзя перебросить более одного раза», multi-dice перебрасывается целиком.
- **Решения заказчика (зафиксированы):** (1) выбор кости — всегда **худшая проваленная** (без выбора игроком, без fast dice); (2) лимит Command Re-roll — `UNLIMITED` в реестре + per-roll-гейт в roll-context (естественный лимит = CP); (3) Desperate Escape / Hazardous механик в движке **нет** → под-этап 3b, в MVP «не поддержано»; (4) charge бросается как `dice(num=2)` и схлопывается в `sum` локально ([warhamEnv.py:6494-6495](../../../core/envs/warhamEnv.py#L6494-L6495), [:6658](../../../core/envs/warhamEnv.py#L6658), [:6854](../../../core/envs/warhamEnv.py#L6854)) — пара костей доступна только в момент броска, не персистится.
- **Не трогать механику `usage_limit` для других стратагем** (Insane Bravery=PER_BATTLE, Overwatch=PER_TURN и т.д.) — меняется только запись Command Re-roll.
- **Ревью перед коммитом крупного:** субагент `engine-regression-reviewer` обязателен для задач, меняющих `core/engine/utils.py::attack` и `core/envs/warhamEnv.py` боевые/charge-пути.
- **DRY/YAGNI/TDD, частые коммиты.** Каждый шаг — одно действие (2–5 мин).

---

## File Structure

| Файл | Ответственность | Этапы |
|------|-----------------|-------|
| `core/engine/utils.py` | `attack()` + `_normalize_effects` + новый хелпер выбора худшей кости + `reroll_decider`-hook | 1, 2, 3 |
| `core/engine/phases/stratagems.py` | реестр Command Re-roll, `legal_stratagem_options`, лимит | 1, 3 |
| `core/engine/phases/stratagem_engine.py` | payload эффекта (под-тип ре-ролла), потребление | 1 |
| `core/engine/phases/option_generator.py` | генерация вариантов ре-ролла (hit/wound) и reaction-окон | 1, 3 |
| `core/envs/warhamEnv.py` | `_fight_effects_for_attacker`, маппинг payload, charge/advance roll-context, очистка | 1, 2, 3 |
| `core/models/reaction_value_policy.py` + bridges | подключение value-политики к hook | 4 |
| `tests/engine/test_attack_effects.py` | low-level ре-ролл/`_normalize_effects` | 1, 2, 3 |
| `tests/engine/phases/test_command_reroll.py` | стратагема e2e (обновить «approximation») | 1, 3 |
| `tests/engine/phases/test_stratagem_engine.py` | payload | 1 |
| `tests/engine/phases/test_roll_context.py` (new) | hook, «нельзя дважды», save-attribution | 2 |
| `tests/engine/phases/test_command_reroll_phases.py` (new) | advance/charge/shooting ре-ролл | 3 |

---

# ЭТАП 1 — hit+wound ре-ролл в Fight (attacker-side), worst-failed, потребление

**Независимо мёржится. Save отложен на этап 2/3 (save-бросок делает защитник — его и атрибутируем через roll-context).**

### Task 1: Хелпер выбора худшей проваленной кости + worst-failed для wound "one"

**Files:**
- Modify: `core/engine/utils.py` (добавить `_worst_failed_index`, использовать в wound-проходе [:534-548](../../../core/engine/utils.py#L534-L548))
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Produces: `_worst_failed_index(dice: np.ndarray, threshold: int) -> int | None` — индекс наименьшей кости среди `< threshold`, иначе `None`.

- [ ] **Step 1: Написать падающий тест**

В `tests/engine/test_attack_effects.py` добавить:
```python
def test_worst_failed_index_picks_lowest_failure():
    import numpy as np
    from core.engine.utils import _worst_failed_index
    # threshold=4: провалы — индексы 0(=3) и 2(=2); худший = 2 (значение 2)
    assert _worst_failed_index(np.array([3, 5, 2, 6]), 4) == 2
    # нет провалов
    assert _worst_failed_index(np.array([4, 5, 6]), 4) is None


def test_reroll_wounds_one_rerolls_worst_failure():
    # Два хита, провалы [2,3]; "one" должен реролить ХУДШИЙ (2, idx0), не первый по списку.
    # wound-очередь: [2,3] исходные, затем [6] на реролл худшего → одна рана.
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]))
    assert float(sum(one)) == 1.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/test_attack_effects.py::test_worst_failed_index_picks_lowest_failure -v`
Expected: FAIL — `cannot import name '_worst_failed_index'`.

- [ ] **Step 3: Реализовать хелпер и применить в wound-проходе**

В `core/engine/utils.py` рядом с `_normalize_effects` добавить:
```python
def _worst_failed_index(dice, threshold):
    """Индекс наименьшей кости среди проваленных (< threshold); None если провалов нет.

    Используется для Command Re-roll: реролим всегда ХУДШУЮ проваленную кость.
    """
    worst_idx = None
    worst_val = None
    for idx, d in enumerate(dice):
        d = int(d)
        if d < int(threshold) and (worst_val is None or d < worst_val):
            worst_val = d
            worst_idx = idx
    return worst_idx
```
В wound-проходе ([:534-548](../../../core/engine/utils.py#L534-L548)) заменить блок выбора для `"one"`: вместо `need = need[:1]` (первый) выбирать худший:
```python
            if eff["reroll_wounds"]:
                if eff["reroll_wounds"] == "one":
                    wi = _worst_failed_index(wound_rolls, wt)
                    need = [wi] if wi is not None else []
                else:
                    need = []
                    for idx, w in enumerate(wound_rolls):
                        w = int(w)
                        if eff["reroll_wounds"] == "ones" and w == 1:
                            need.append(idx)
                        elif eff["reroll_wounds"] == "all" and w < wt:
                            need.append(idx)
                if need:
                    new = _roll_with_stage(num=len(need), stage="wound")
                    new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
                    for j, idx in enumerate(need):
                        wound_rolls[idx] = int(new[j])
```

- [ ] **Step 4: Запустить тесты — убедиться, что проходят**

Run: `pytest tests/engine/test_attack_effects.py -v`
Expected: PASS (включая существующий `test_reroll_wounds_one_rerolls_single_failure` — там обе кости =3, худший==первый).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): worst-failed выбор кости для reroll_wounds=one"
```

---

### Task 2: `reroll_hits="one"` (worst-failed) в attack()

**Files:**
- Modify: `core/engine/utils.py` — `_normalize_effects` ([:341-342](../../../core/engine/utils.py#L341-L342)) и hit-проход ([:483-495](../../../core/engine/utils.py#L483-L495))
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Consumes: `_worst_failed_index` (Task 1).
- Produces: `effects={"reroll_hits": "one"}` реролит худший проваленный hit-бросок один раз.

- [ ] **Step 1: Написать падающий тест**
```python
def test_reroll_hits_one_rerolls_worst_failure():
    # BS4 → hit 4+. Два броска [2,3] провал; "one" реролит худший (2) → [6,_] = 1 хит → 1 рана (wound 6) → урон.
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "one"},
                    roller=StubRoller(hit=[2, 3, 6], wound=[6]))
    assert float(sum(one)) == 1.0


def test_normalize_effects_reroll_hits_one_allowed():
    assert _normalize_effects({"reroll_hits": "one"})["reroll_hits"] == "one"
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/test_attack_effects.py::test_normalize_effects_reroll_hits_one_allowed -v`
Expected: FAIL — `assert None == 'one'` (сейчас `"one"` не пропускается для hits, [:342](../../../core/engine/utils.py#L342)).

- [ ] **Step 3: Реализация**

В `_normalize_effects` ([:341-342](../../../core/engine/utils.py#L341-L342)):
```python
        rh = effects.get("reroll_hits")
        out["reroll_hits"] = rh if rh in ("ones", "all", "one") else None
```
В hit-проходе ([:483-495](../../../core/engine/utils.py#L483-L495)) — добавить ветку `"one"` (worst-failed; для hit порог = `bs`, крит-6 не провал):
```python
    if eff["reroll_hits"]:
        if eff["reroll_hits"] == "one":
            wi = _worst_failed_index(rolls, bs)
            need = [wi] if wi is not None else []
        else:
            need = []
            for idx, r in enumerate(rolls):
                r = int(r)
                if eff["reroll_hits"] == "ones" and r == 1:
                    need.append(idx)
                elif eff["reroll_hits"] == "all" and r != 6 and r < bs:
                    need.append(idx)
        if need:
            new = _roll_with_stage(num=len(need), stage="hit")
            new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
            for j, idx in enumerate(need):
                rolls[idx] = int(new[j])
```

- [ ] **Step 4: Запустить — убедиться, что проходят**

Run: `pytest tests/engine/test_attack_effects.py -v`
Expected: PASS.

- [ ] **Step 5: Коммит**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): reroll_hits=one (worst-failed) в attack()"
```

---

### Task 3: Под-тип ре-ролла в стратагеме (hit|wound) + потребление эффекта

**Files:**
- Modify: `core/engine/phases/stratagems.py` (Command Re-roll → `legal_stratagem_options` отдаёт варианты hit/wound), `core/engine/phases/stratagem_engine.py` (payload по под-типу + флаг `consumed`), `core/envs/warhamEnv.py::_fight_effects_for_attacker` ([:2341-2342](../../../core/envs/warhamEnv.py#L2341-L2342))
- Test: `tests/engine/phases/test_command_reroll.py`, `tests/engine/phases/test_stratagem_engine.py`

**Interfaces:**
- Consumes: Tasks 1–2 (`reroll_hits/reroll_wounds="one"`).
- Produces: `apply(env, side, "command_reroll", unit_idx, phase="fight", reroll_roll="wound"|"hit")` пишет в `active_stratagem_effects` запись `{"effect_id":"command_reroll", "reroll_roll": <roll>, "consumed": False}`. `_fight_effects_for_attacker` возвращает `{f"reroll_{roll}": "one"}` и помечает запись `consumed=True` после первого чтения.

- [ ] **Step 1: Написать падающие тесты**

В `tests/engine/phases/test_stratagem_engine.py` заменить `test_command_reroll_payload_is_single` (которое жёстко ждёт `reroll_wounds=="one"`):
```python
def test_command_reroll_payload_records_roll_subtype():
    env = build_env()
    env.modelCP = 2
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight", reroll_roll="hit")
    rec = [r for r in env.active_stratagem_effects if r["effect_id"] == "command_reroll"][0]
    assert rec["reroll_roll"] == "hit"
    assert rec["consumed"] is False
```
В `tests/engine/phases/test_command_reroll.py` добавить:
```python
def test_fight_effect_consumed_after_first_read():
    env = build_env()
    env.battle_round = 1
    env.active_stratagem_effects = [{
        "side": "model", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "command_reroll", "reroll_roll": "wound", "consumed": False,
    }]
    first = env._fight_effects_for_attacker("model", 0)
    assert first == {"reroll_wounds": "one"}
    second = env._fight_effects_for_attacker("model", 0)
    assert second is None  # эффект потреблён, повторно не срабатывает
```

- [ ] **Step 2: Запустить — убедиться, что падают**

Run: `pytest tests/engine/phases/test_stratagem_engine.py::test_command_reroll_payload_records_roll_subtype tests/engine/phases/test_command_reroll.py::test_fight_effect_consumed_after_first_read -v`
Expected: FAIL (`apply` не принимает `reroll_roll`; нет `consumed`).

- [ ] **Step 3: Реализация**

`stratagem_engine.py::apply` — добавить параметр и payload:
```python
def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None,
          phase: str | None = None, *, reroll_roll: str = "wound") -> dict:
```
Заменить `_FIGHT_EFFECT_PAYLOAD` / запись эффекта ([:43-60](../../../core/engine/phases/stratagem_engine.py#L43-L60)):
```python
    if d.effect_id == "hungry_void_strength_mod" and unit_idx is not None:
        ... (как было)
    if d.effect_id == "command_reroll" and unit_idx is not None:
        active = getattr(e, "active_stratagem_effects", None)
        if active is None:
            active = []; e.active_stratagem_effects = active
        roll = reroll_roll if reroll_roll in ("hit", "wound") else "wound"
        active.append({
            "side": str(side), "unit_idx": int(unit_idx),
            "round": int(getattr(e, "battle_round", 1)),
            "phase": str(phase or getattr(e, "phase", "fight") or "fight"),
            "effect_id": "command_reroll", "reroll_roll": roll, "consumed": False,
        })
```
В реестре ([stratagems.py:142-153](../../../core/engine/phases/stratagems.py#L142-L153)) сменить `effect_id="command_reroll_wounds"` → `effect_id="command_reroll"` (и обновить `test_registry_has_command_reroll`).
`warhamEnv.py::_fight_effects_for_attacker` ([:2341-2342](../../../core/envs/warhamEnv.py#L2341-L2342)) — потребление:
```python
            elif rec.get("effect_id") == "command_reroll" and not rec.get("consumed", False):
                roll = str(rec.get("reroll_roll", "wound"))
                effects[f"reroll_{roll}"] = "one"
                rec["consumed"] = True
```

- [ ] **Step 4: Запустить — убедиться, что проходят**

Run: `pytest tests/engine/phases/test_command_reroll.py tests/engine/phases/test_stratagem_engine.py -v`
Expected: PASS (обновить `test_registry_has_command_reroll` на `effect_id == "command_reroll"`; `test_apply_command_reroll_writes_reroll_effect` — на новую форму записи).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/stratagems.py core/engine/phases/stratagem_engine.py core/envs/warhamEnv.py tests/engine/phases/test_command_reroll.py tests/engine/phases/test_stratagem_engine.py
git commit -m "feat(strat): Command Re-roll выбор hit|wound + потребление эффекта"
```

---

### Task 4: Опции hit/wound в fight-окне + прокидывание под-типа в pending-plan

**Files:**
- Modify: `core/engine/phases/stratagems.py::legal_stratagem_options` ([:271-285](../../../core/engine/phases/stratagems.py#L271-L285)) — для `command_reroll` отдавать 2 опции (hit/wound) с `param={"stratagem_id","reroll_roll"}`; `core/envs/warhamEnv.py::_apply_pending_fight_stratagem_plan` ([:2353-2382](../../../core/envs/warhamEnv.py#L2353-L2382)) — план хранит под-тип.
- Test: `tests/engine/phases/test_command_reroll.py`

**Interfaces:**
- Consumes: Task 3 (`apply(..., reroll_roll=)`).
- Produces: fight-окно содержит опции с `meta["stratagem_id"]=="command_reroll"` и `param["reroll_roll"] in {"hit","wound"}`; pending-plan значение для command_reroll = `"command_reroll:hit"` либо `"command_reroll:wound"` (string-кодирование под-типа поверх существующего `dict[int,str]`).

- [ ] **Step 1: Написать падающий тест**
```python
def test_fight_window_offers_command_reroll_hit_and_wound():
    env = build_env()
    env.modelCP = 1
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    rolls = {o.param.get("reroll_roll") for o in opts
             if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "command_reroll"}
    assert rolls == {"hit", "wound"}
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/phases/test_command_reroll.py::test_fight_window_offers_command_reroll_hit_and_wound -v`
Expected: FAIL (`rolls` пуст/без под-типа).

- [ ] **Step 3: Реализация**

В `legal_stratagem_options` ([:271-285](../../../core/engine/phases/stratagems.py#L271-L285)) — спец-ветка для command_reroll (генерим по одной опции на под-тип):
```python
            if d.id == "command_reroll":
                for roll in ("hit", "wound"):
                    options.append(ActionOption(
                        kind=ActionKind.USE_STRATAGEM, unit_idx=i,
                        param={"stratagem_id": d.id, "reroll_roll": roll},
                        legacy_patch={},
                        meta={"stratagem_id": d.id, "cp_cost": d.cp_cost,
                              "timing": d.timing, "scope": d.scope, "reroll_roll": roll},
                    ))
                continue
            legacy_patch = {"use_cp": 1, "cp_on": i} if d.id == "insane_bravery" else {}
            options.append(ActionOption(...))  # как было для прочих
```
В `_apply_pending_fight_stratagem_plan` ([:2379-2382](../../../core/envs/warhamEnv.py#L2379-L2382)) — распарсить под-тип из значения плана:
```python
                sid_raw = str(sid)
                if sid_raw.startswith("command_reroll:"):
                    base_id, roll = "command_reroll", sid_raw.split(":", 1)[1]
                    _apply_stratagem(self, side, base_id, ui, phase="fight", reroll_roll=roll)
                else:
                    _apply_stratagem(self, side, sid_raw, ui, phase="fight")
```

- [ ] **Step 4: Запустить — убедиться, что проходят**

Run: `pytest tests/engine/phases/test_command_reroll.py tests/engine/phases/test_obs_features.py -v`
Expected: PASS (в `test_obs_features.py:97` проверка наличия id остаётся валидной).

- [ ] **Step 5: engine-regression-reviewer + Коммит**

Запустить субагента `engine-regression-reviewer` на диффе. Затем:
```bash
git add core/engine/phases/stratagems.py core/envs/warhamEnv.py tests/engine/phases/test_command_reroll.py
git commit -m "feat(strat): fight-окно отдаёт Command Re-roll отдельно для hit/wound"
```

---

# ЭТАП 2 — roll-context hook в attack() (фундамент реакций) + save-attribution

### Task 5: `reroll_decider`-hook в attack() (worst-failed, один раз на стадию)

**Files:**
- Modify: `core/engine/utils.py::attack` (сигнатура [:366-367](../../../core/engine/utils.py#L366-L367); hit/wound/save проходы)
- Test: `tests/engine/phases/test_roll_context.py` (new)

**Interfaces:**
- Produces: `attack(..., reroll_decider=None)` где `reroll_decider: Callable[[str, np.ndarray, int], bool] | None`. Контракт: вызывается **после** бросков стадии `stage in {"hit","wound","save"}` с `(stage, dice_array, threshold)`; возвращает `True` → движок реролит ЕДИНСТВЕННУЮ худшую проваленную кость этой стадии один раз; повторный вызов для той же стадии в одной атаке не делается (один decider-вызов на стадию). Decider не получает side/unit_idx — их связывает замыкание вызывающего.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_roll_context.py`:
```python
from core.engine.utils import attack
from tests.engine.test_attack_effects import StubRoller, _ranged_weapon, _ATT_DATA


def test_reroll_decider_rerolls_worst_failed_wound():
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    calls = []

    def decider(stage, dice, threshold):
        calls.append(stage)
        return stage == "wound"  # реролим только wound-стадию

    dmg, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 6]),
                    reroll_decider=decider)
    assert "wound" in calls
    assert float(sum(dmg)) == 1.0  # худший (2) перереролен в 6 → 1 рана
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/phases/test_roll_context.py::test_reroll_decider_rerolls_worst_failed_wound -v`
Expected: FAIL — `attack() got an unexpected keyword argument 'reroll_decider'`.

- [ ] **Step 3: Реализация**

В сигнатуру `attack()` ([:366-367](../../../core/engine/utils.py#L366-L367)) добавить `reroll_decider=None`. Добавить локальный хелпер после `eff = _normalize_effects(effects)`:
```python
    def _maybe_decider_reroll(stage, dice, threshold):
        # Реактивный Command Re-roll-style hook: после броска стадии спросить decider,
        # реролить ли худшую проваленную кость (один раз). Возвращает обновлённый dice.
        if reroll_decider is None:
            return dice
        try:
            want = bool(reroll_decider(stage, dice, int(threshold)))
        except Exception:
            want = False
        if not want:
            return dice
        wi = _worst_failed_index(dice, int(threshold))
        if wi is None:
            return dice
        new = _roll_with_stage(num=1, stage=stage)
        dice[wi] = int(new if isinstance(new, int) else list(new)[0])
        return dice
```
Вызвать после каждого effect-прохода: hit (после [:495](../../../core/engine/utils.py#L495), порог `bs`), wound (после wound-реролла, порог `wt`), save (после [:577](../../../core/engine/utils.py#L577), порог `save_target`). Для save «провал» = `< save_target` (кость защитника, которую защитник захочет перебросить).

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/test_attack_effects.py -v`
Expected: PASS (без decider поведение неизменно — golden существующих тестов).

- [ ] **Step 5: Коммит**
```bash
git add core/engine/utils.py tests/engine/phases/test_roll_context.py
git commit -m "feat(engine): reroll_decider hook в attack() (worst-failed, per-stage)"
```

---

### Task 6: Инвариант «кость нельзя перебросить дважды»

**Files:**
- Modify: `core/engine/utils.py::attack` — для каждой стадии не давать decider реролить кость, уже переброшенную effect-проходом или предыдущим decider-вызовом.
- Test: `tests/engine/phases/test_roll_context.py`

**Interfaces:**
- Consumes: Task 5.
- Produces: гарантия — на одной стадии одна кость перебрасывается максимум один раз суммарно (effect-reroll + decider).

- [ ] **Step 1: Написать падающий тест**
```python
def test_die_not_rerolled_twice_effect_then_decider():
    # reroll_wounds="one" уже реролит худшую failed-кость; decider не должен реролить её повторно.
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    rerolled_stages = []

    def decider(stage, dice, threshold):
        rerolled_stages.append(stage)
        return True

    # wound: [2,3] → effect реролит худший(2)→[5]; остаётся [5,3]. decider НЕ трогает уже-переброшенную.
    dmg, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                    effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[2, 3, 5, 6]),
                    reroll_decider=decider)
    # Если бы decider реролил уже-переброшенную кость, потратили бы [6]. Проверяем, что [6] НЕ израсходован
    # на ту же кость: ожидаем, что decider реролит ВТОРУЮ failed (idx1=3) → [6] = wound. Итог: 2 раны.
    assert float(sum(dmg)) == 2.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/phases/test_roll_context.py::test_die_not_rerolled_twice_effect_then_decider -v`
Expected: FAIL — без защиты decider реролит уже-переброшенную кость (idx0), даёт неверный итог.

- [ ] **Step 3: Реализация**

В `attack()` вести по стадии `set` индексов уже-переброшенных костей; effect-проход добавляет свои индексы; `_maybe_decider_reroll` принимает `rerolled: set` и выбирает худшую failed-кость, **исключая** уже-переброшенные:
```python
    def _worst_failed_index_excl(dice, threshold, exclude):
        worst_idx = worst_val = None
        for idx, d in enumerate(dice):
            if idx in exclude:
                continue
            d = int(d)
            if d < int(threshold) and (worst_val is None or d < worst_val):
                worst_val, worst_idx = d, idx
        return worst_idx
```
`_maybe_decider_reroll(stage, dice, threshold, rerolled)` использует `_worst_failed_index_excl` и добавляет выбранный idx в `rerolled`. Effect-проходы регистрируют свои переброшенные индексы в тот же `rerolled`.

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/test_attack_effects.py -v`
Expected: PASS.

- [ ] **Step 5: Коммит**
```bash
git add core/engine/utils.py tests/engine/phases/test_roll_context.py
git commit -m "feat(engine): инвариант одна кость = один реролл (effect+decider)"
```

---

### Task 7: Проброс decider из resolve_fight + side-attribution (attacker=hit/wound, defender=save)

**Files:**
- Modify: `core/envs/warhamEnv.py` — `resolve_fight_phase` вызовы `attack()` ([:7377-7396](../../../core/envs/warhamEnv.py#L7377-L7396), [:7464-7485](../../../core/envs/warhamEnv.py#L7464-L7485)); новый билдер decider из `active_stratagem_effects`.
- Test: `tests/engine/phases/test_roll_context.py`

**Interfaces:**
- Consumes: Tasks 5–6; `active_stratagem_effects` записи Command Re-roll (Task 3).
- Produces: метод `Warhammer40kEnv._build_reroll_decider(attacker_side, attacker_idx, defender_side, defender_idx) -> Callable[[str,np.ndarray,int],bool]`: для `stage in {"hit","wound"}` смотрит запись command_reroll атакующего юнита; для `stage == "save"` — запись защищающегося юнита; помечает `consumed=True` при срабатывании.

- [ ] **Step 1: Написать падающий тест**
```python
def test_defender_command_reroll_applies_to_save(monkeypatch):
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.battle_round = 1
    env.active_stratagem_effects = [{
        "side": "enemy", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "command_reroll", "reroll_roll": "save", "consumed": False,
    }]
    decider = env._build_reroll_decider("model", 0, "enemy", 0)
    import numpy as np
    assert decider("save", np.array([2]), 4) is True   # защитник реролит свой провальный сейв
    assert decider("hit", np.array([2]), 4) is False   # hit — не его стадия
```
(Примечание: для save под-тип `reroll_roll="save"` появляется на этапе 3; на этапе 2 достаточно научить `apply` принимать `reroll_roll="save"` — расширить whitelist в Task 3 с `("hit","wound")` до `("hit","wound","save")`.)

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/engine/phases/test_roll_context.py::test_defender_command_reroll_applies_to_save -v`
Expected: FAIL — нет `_build_reroll_decider`.

- [ ] **Step 3: Реализация**

Расширить whitelist в `stratagem_engine.apply` (Task 3) до `("hit","wound","save")`. Добавить в `warhamEnv.py`:
```python
    def _build_reroll_decider(self, attacker_side, attacker_idx, defender_side, defender_idx):
        def _find(side, unit_idx, roll):
            for rec in list(getattr(self, "active_stratagem_effects", []) or []):
                if (rec.get("effect_id") == "command_reroll" and not rec.get("consumed", False)
                        and str(rec.get("phase", "")) == "fight"
                        and str(rec.get("side", "")) == str(side)
                        and int(rec.get("unit_idx", -1)) == int(unit_idx)
                        and str(rec.get("reroll_roll", "")) == roll
                        and int(rec.get("round", getattr(self, "battle_round", 1))) == int(getattr(self, "battle_round", 1))):
                    return rec
            return None

        def decider(stage, dice, threshold):
            if stage in ("hit", "wound"):
                rec = _find(attacker_side, attacker_idx, stage)
            elif stage == "save":
                rec = _find(defender_side, defender_idx, "save")
            else:
                rec = None
            if rec is None:
                return False
            rec["consumed"] = True
            return True

        return decider
```
В `resolve_fight_phase` строить decider и передавать в `attack(..., reroll_decider=...)` для обеих веток (model-attacker [:7377](../../../core/envs/warhamEnv.py#L7377), enemy-attacker [:7464](../../../core/envs/warhamEnv.py#L7464)). На этом этапе `_fight_effects_for_attacker` для hit/wound можно оставить (effect-путь), либо постепенно перевести на decider — но без двойного реролла (инвариант Task 6 защищает).

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `pytest tests/engine/phases/test_roll_context.py tests/engine/phases/test_command_reroll.py -v`
Expected: PASS.

- [ ] **Step 5: engine-regression-reviewer + Коммит**
```bash
git add core/engine/phases/stratagem_engine.py core/envs/warhamEnv.py tests/engine/phases/test_roll_context.py
git commit -m "feat(strat): save-реролл защитника через reroll_decider в fight"
```

---

# ЭТАП 3 — все фазы и броски (advance, charge 2D6, стрельба, attacks)

### Task 8: Command Re-roll в стрельбе (hit/wound/save) через decider

**Files:**
- Modify: `core/envs/warhamEnv.py` — путь стрельбы, где вызывается `attack()` для shooting (найти по `rangeOfComb="Ranged"`); строить decider аналогично fight; `_clear_phase_stratagem_effects` вызвать в конце shooting.
- Modify: `core/engine/phases/stratagems.py` — `phases` Command Re-roll += `SHOOTING`; reaction-окна в `option_generator`.
- Test: `tests/engine/phases/test_command_reroll_phases.py` (new)

**Interfaces:**
- Consumes: Task 7 (`_build_reroll_decider`, save-attribution).
- Produces: в shooting-фазе Command Re-roll доступен (hit/wound для стрелка, save для цели); эффект очищается в конце shooting.

- [ ] **Step 1: Написать падающий тест** — e2e: стрелок с активным `command_reroll/wound` реролит худший провальный wound в стрельбе (детерминированный roller через `simulation_mode`/manual-dice; зеркалит `test_run_fight_command_reroll_spends_cp_and_applies` для shooting).

- [ ] **Step 2: Запустить — убедиться, что падает.** Run: `pytest tests/engine/phases/test_command_reroll_phases.py -k shooting -v`

- [ ] **Step 3: Реализация** — добавить `Phase.SHOOTING` в реестр Command Re-roll; добавить shooting reaction-опции в `option_generator` (по аналогии с `fight_stratagem_options_for_unit`, но trigger для стрельбы); строить decider в shooting-резолве и передавать в `attack()`; `_clear_phase_stratagem_effects("shooting")` в конце фазы.

- [ ] **Step 4: Запустить — PASS.** Run: `pytest tests/engine/phases/ -v`

- [ ] **Step 5: Коммит** — `feat(strat): Command Re-roll в Shooting phase (hit/wound/save)`

---

### Task 9: Command Re-roll на Advance (D6)

**Files:**
- Modify: `core/envs/warhamEnv.py` — advance-броски ([:4986-5100](../../../core/envs/warhamEnv.py#L4986-L5100) model, [:5249-5306](../../../core/envs/warhamEnv.py#L5249-L5306) enemy); `model/enemy_advance_roll` ([:1074-1075](../../../core/envs/warhamEnv.py#L1074-L1075)) уже хранит результат — реролл перезаписывает его.
- Test: `tests/engine/phases/test_command_reroll_phases.py`

**Interfaces:**
- Consumes: reaction-инфраструктура этапа 2.
- Produces: после advance-броска, если у юнита активен `command_reroll/advance`, бросок D6 перебрасывается один раз (берём новый результат безусловно — «худшая» для одиночной кости = сам бросок).

- [ ] **Step 1: Падающий тест** — advance-бросок юнита с активным `command_reroll/advance` перебрасывается (seeded RNG: первый бросок низкий, реролл выше; проверяем итоговый `model_advance_roll[i]`).
- [ ] **Step 2: Запустить — FAIL.**
- [ ] **Step 3: Реализация** — в момент записи `model_advance_roll[i]`/`enemy_advance_roll[i]` проверить активный `command_reroll/advance` для юнита; если есть и не consumed — перебросить `dice()` один раз, перезаписать, пометить consumed, списать уже списанный CP (CP списывается при `apply`). Добавить `Phase.MOVEMENT` в реестр + advance-reaction-окно.
- [ ] **Step 4: Запустить — PASS.**
- [ ] **Step 5: Коммит** — `feat(strat): Command Re-roll на Advance-бросок`

---

### Task 10: Command Re-roll на Charge (2D6, обе кости) + унификация charge-путей

**Files:**
- Modify: `core/envs/warhamEnv.py::charge_phase` — три пути ([:6494-6495](../../../core/envs/warhamEnv.py#L6494-L6495) model, [:6658](../../../core/envs/warhamEnv.py#L6658) enemy-action, [:6854](../../../core/envs/warhamEnv.py#L6854) enemy-heur): сохранять пару `dice_vals` до точки реакции; enemy-heur перестать схлопывать сразу.
- Test: `tests/engine/phases/test_command_reroll_phases.py`

**Interfaces:**
- Consumes: reaction-инфраструктура.
- Produces: при активном `command_reroll/charge` charge-бросок перебрасывает **обе** кости 2D6 (multi-dice rule), пересчитывает `diceRoll = sum`.

- [ ] **Step 1: Падающий тест** — юнит с `command_reroll/charge`: первый `dice(num=2)` низкий (провал), реролл обеих → успех; проверяем, что charge удался и что переброшены ОБЕ кости (seeded).
- [ ] **Step 2: Запустить — FAIL.**
- [ ] **Step 3: Реализация** — выделить общий хелпер `_charge_roll_with_reroll(side, unit_idx) -> (dice_vals, total)`; во всех трёх путях заменить `dice(num=2)`/`sum(...)` на него; внутри — после первого броска при активном `command_reroll/charge` перебросить `dice(num=2)` целиком один раз. Добавить `Phase.CHARGE` в реестр + charge-reaction-окно.
- [ ] **Step 4: Запустить — PASS** (вкл. существующие charge-тесты).
- [ ] **Step 5: engine-regression-reviewer + Коммит** — `feat(strat): Command Re-roll на Charge 2D6 (обе кости), унификация charge-путей`

---

### Task 11: Лимит Command Re-roll → UNLIMITED + per-roll-гейт

**Files:**
- Modify: `core/engine/phases/stratagems.py` — `usage_limit=UsageLimit.UNLIMITED` для command_reroll ([:151](../../../core/engine/phases/stratagems.py#L151)).
- Test: `tests/engine/phases/test_usage_limit.py`, `tests/engine/phases/test_command_reroll_phases.py`

**Interfaces:**
- Consumes: per-roll consume-флаг (Tasks 3,7) — фактический лимит «один бросок = один реролл» обеспечивается `consumed` + инвариантом Task 6.
- Produces: Command Re-roll можно применить несколько раз в фазе на РАЗНЫЕ броски (по 1 CP), но один бросок/кость — не дважды.

- [ ] **Step 1: Падающий тест** — два разных юнита/два разных броска в одной фазе: оба Command Re-roll применяются (CP=2 → 0), `usage_limit_reached` не блокирует второй.
- [ ] **Step 2: Запустить — FAIL** (сейчас PER_PHASE блокирует второй).
- [ ] **Step 3: Реализация** — сменить `usage_limit` на `UNLIMITED`; убедиться, что `legal_stratagem_options`/`apply` больше не зовут `usage_limit_reached` как блокер для command_reroll (UNLIMITED → `usage_limit_reached` возвращает False [:212-213](../../../core/engine/phases/stratagems.py#L212-L213), менять её не нужно).
- [ ] **Step 4: Запустить — PASS** (проверить, что лимиты Insane Bravery/Overwatch не затронуты — `test_usage_limit.py`).
- [ ] **Step 5: Коммит** — `feat(strat): Command Re-roll лимит = UNLIMITED (per-roll вместо per-phase)`

---

### Task 12 (3b, опционально): Desperate Escape / Hazardous — заглушка «не поддержано»

**Files:** docstring/комментарий в реестре + (если реализуются механики) отдельный план.

- [ ] **Step 1:** Зафиксировать в комментарии реестра ([stratagems.py:136-141](../../../core/engine/phases/stratagems.py#L136-L141)), что Desperate Escape/Hazardous-тесты в движке не моделируются и Command Re-roll к ним не применяется (механики отсутствуют). Если потребуется — отдельный план на реализацию самих механик.
- [ ] **Step 2: Коммит** — `docs(strat): Command Re-roll — Desperate Escape/Hazardous вне области (нет механики)`

---

# ЭТАП 4 — AI / MCTS reaction-policy на hook

### Task 13: Подключить value-reaction-policy к reroll_decider

**Files:**
- Modify: `core/models/reaction_value_policy.py` ([:16-36](../../../core/models/reaction_value_policy.py#L16-L36)), `core/envs/warhamEnv.py::_build_reroll_decider` (Task 7) — вместо «есть запись → True» спрашивать `env.reaction_policy` (apply vs pass value-lookahead) когда нет предустановленной стратагемы.
- Modify: `core/models/dqn_stratagem_bridge.py` ([:66-98](../../../core/models/dqn_stratagem_bridge.py#L66-L98)), `core/models/ppo_stratagem_bridge.py` — fight-plan теперь учитывает под-типы hit/wound и не нужен для реактивных save/charge/advance (их решает decider в момент броска).
- Test: `tests/models/test_eval_agent.py` ([:52-56](../../../tests/models/test_eval_agent.py#L52-L56)), новый reaction-policy тест.

**Interfaces:**
- Consumes: `reroll_decider` (Task 7), `make_stratagem_value_policy` ([reaction_value_policy.py:16](../../../core/models/reaction_value_policy.py#L16)).
- Produces: AI применяет Command Re-roll реактивно через value-сравнение «реролл vs нет» в точке броска.

- [ ] **Step 1: Падающий тест** — reaction-policy на ctx «бросок с провалами» → apply; «без провалов» → pass (мок value-сети). Обновить `test_eval_agent.py` под новую модель (план хранит под-тип `command_reroll:hit`).
- [ ] **Step 2: Запустить — FAIL.**
- [ ] **Step 3: Реализация** — расширить ctx reaction-policy полями броска (`stage`, кол-во провалов, ожидаемый выигрыш); в `_build_reroll_decider` при отсутствии предустановленной записи и наличии CP+сети вызвать `env.reaction_policy(ctx)`; ограничить вызовы heuristics-гейтом «есть провалы и CP>0», чтобы не плодить reaction-вызовы.
- [ ] **Step 4: Запустить — PASS** + смоук eval (число reaction-вызовов в норме).
- [ ] **Step 5: engine-regression-reviewer + Коммит** — `feat(ai): reaction value-policy для Command Re-roll в точке броска`

---

## Self-Review

**Spec coverage:**
- CP cost (1) — без изменений (Task не нужен, уже корректно).
- Phase: fight (Этап 1) → shooting/movement/charge (Tasks 8–10). ✅
- Target unit/model — attacker hit/wound, defender save (Task 7). ✅
- Список бросков: hit/wound (Tasks 1–4), save (Task 7), shooting (8), advance (9), charge 2D6 (10), attacks/damage — **частично**: attacks/damage стадии покрываются hook-механизмом Task 5 при добавлении соответствующих `stage` вызовов; явная задача на attacks/damage не выделена → **добавить под-задачу в Task 8/10 или отдельным шагом** (gap зафиксирован).
- Fast dice rolling — намеренно НЕ реализуется (решение (1) worst-failed). ✅ задокументировано в Global Constraints.
- Multi-dice (charge) — Task 10. ✅
- «Один roll/один реролл» — Tasks 3,6,7,11. ✅
- «Кость не дважды» — Task 6. ✅
- Reuse-лимит — Task 11 (UNLIMITED + per-roll). ✅
- Desperate Escape/Hazardous — Task 12 (вне области, нет механики). ✅

**Gap явный:** ре-ролл **Damage-броска** и **кол-ва Attacks** не имеет выделенной задачи. Добавить шаг в Этап 3: дать `stage="damage"` и `stage="attacks"` вызовы decider в `attack()` (стадии есть в `_roll_damage_expr`/attacks-парсинге) — аналогично Task 5, под-типы `command_reroll/damage|attacks`. Зафиксировано как **Task 8b** при исполнении.

**Placeholder scan:** код-шаги Этапа 1–2 содержат полный код; Этап 3–4 — задачи с интерфейсами и точными местами правок, код-скелеты приведены для нетривиальных мест (decider, charge-хелпер). Шаги «Падающий тест» Этапа 3–4 описаны без полного листинга намеренно (зависят от seeded-RNG конкретного env-пути) — при исполнении тест пишется по образцу `test_run_fight_command_reroll_spends_cp_and_applies` ([test_command_reroll.py:81-91](../../../tests/engine/phases/test_command_reroll.py#L81-L91)).

**Type consistency:** `reroll_roll` ∈ {"hit","wound","save","charge","advance","damage","attacks"}; `effect_id="command_reroll"` единообразно (Tasks 3–11); `_build_reroll_decider` сигнатура едина (Tasks 7–13); `reroll_decider: Callable[[str,np.ndarray,int],bool]` едина (Tasks 5–7).

---

## Execution Handoff

См. ниже — выбор способа исполнения.
