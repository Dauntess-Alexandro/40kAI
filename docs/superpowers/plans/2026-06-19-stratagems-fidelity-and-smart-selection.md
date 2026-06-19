# Стратагемы: точность правил 10e + единый умный выбор — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Привести все стратагемы к правилам W40k 10e (эффекты/лимиты/условия) и свести выбор всех стратагем к единому value-ориентированному механизму, чтобы AZ-агент решал «применять/нет» по ценности.

**Architecture:** Фаза A — расширяем боёвку `attack()` новыми механиками (single-reroll, hit_penalty/Stealth, invuln_grant) и правим реестр стратагем. Фаза B — обобщаем `reaction_value_policy`/`_should_use_reaction` в общий «stratagem value gate» и переводим на него fight + command-bravery, закрывая дыру под `windowed_selfplay`. Фаза C — честные метрики и smoke/parity.

**Tech Stack:** Python 3.12, pytest, numpy, PyTorch (value-сеть в lookahead). Спек: `docs/superpowers/specs/2026-06-19-stratagems-fidelity-and-smart-selection-design.md`.

## Global Constraints

- Платформа Windows; язык логов/UI/ошибок — русский (что случилось + где + что делать).
- Источник правды по правилам — Wahapedia; упрощения помечать явно в комментах реестра.
- Parity: при `reaction_policy/stratagem_policy is None` поведение байт-в-байт прежнее (эвристики/replay/старые тесты не ломаются).
- Только релевантный код в коммитах; не трогать `runtime/logs/*`, `hyperparams.json` без надобности.
- TDD: тест → провал → минимальная реализация → зелёный → коммит. Перед коммитом фазы — `engine-regression-reviewer`.
- Запуск тестов: `python -m pytest <path> -v` из `c:\40kAI`.

---

## ФАЗА A — Точность правил

### Task A1: `attack()` — single-roll реролл ран (`reroll_wounds: "one"`)

**Files:**
- Modify: `core/engine/utils.py` (`_normalize_effects` ~341-342; реролл-блок ран ~519-531)
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Produces: `_normalize_effects` принимает `reroll_wounds in ("ones","all","one")`; `"one"` рероллит ровно один первый проваленный wound-бросок.

- [ ] **Step 1: Failing test**

```python
def test_reroll_wounds_one_rerolls_single_failure():
    # S4 vs T4 → wound 4+. Два хита, оба провал [3,3]; "one" рероллит только первый → [5,_].
    weapon = _ranged_weapon(S=4, Attacks=2)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    one, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_wounds": "one"},
                    roller=StubRoller(hit=[5, 5], wound=[3, 3, 5]))
    assert float(sum(one)) == 1.0  # только один реролл стал успешным


def test_normalize_effects_reroll_one_allowed():
    assert _normalize_effects({"reroll_wounds": "one"})["reroll_wounds"] == "one"
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/test_attack_effects.py::test_reroll_wounds_one_rerolls_single_failure tests/engine/test_attack_effects.py::test_normalize_effects_reroll_one_allowed -v`
Expected: FAIL (`"one"` нормализуется в None / не рероллит).

- [ ] **Step 3: Implement**

В `_normalize_effects` расширить допуск:
```python
        rw = effects.get("reroll_wounds")
        out["reroll_wounds"] = rw if rw in ("ones", "all", "one") else None
```
В реролл-блоке ран заменить сбор `need` так, чтобы `"one"` брал только первый провал:
```python
            if eff["reroll_wounds"]:
                need = []
                for idx, w in enumerate(wound_rolls):
                    w = int(w)
                    if eff["reroll_wounds"] == "ones" and w == 1:
                        need.append(idx)
                    elif eff["reroll_wounds"] in ("all", "one") and w < wt:
                        need.append(idx)
                if eff["reroll_wounds"] == "one":
                    need = need[:1]
                if need:
                    new = _roll_with_stage(num=len(need), stage="wound")
                    new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
                    for j, idx in enumerate(need):
                        wound_rolls[idx] = int(new[j])
```

- [ ] **Step 4: Run, expect PASS** (и весь файл не сломан)

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(strat): attack() — single-roll реролл ран (reroll_wounds=one)"
```

---

### Task A2: `attack()` — `hit_penalty` (механика Stealth)

**Files:**
- Modify: `core/engine/utils.py` (`_normalize_effects`; hit-петля ~485-498)
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Produces: `effects["hit_penalty"]: int` — штраф к hit; попадание при `roll==6` всегда, иначе `roll != 1 and roll >= bs + hit_penalty`. Не строже натуральной 6.

- [ ] **Step 1: Failing test**

```python
def test_hit_penalty_stealth_reduces_hits():
    # bs4. hit [4]: без штрафа хит (4>=4) → урон; hit_penalty=1 → нужно 5+ → [4] промах.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[4], wound=[6]))
    stealth, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"hit_penalty": 1},
                        roller=StubRoller(hit=[4], wound=[6]))
    assert float(sum(base)) == 1.0
    assert float(sum(stealth)) == 0.0


def test_hit_penalty_natural_six_still_hits():
    # hit [6] всегда попадает даже со штрафом.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    stealth, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"hit_penalty": 3},
                        roller=StubRoller(hit=[6], wound=[6]))
    assert float(sum(stealth)) == 1.0
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/test_attack_effects.py::test_hit_penalty_stealth_reduces_hits tests/engine/test_attack_effects.py::test_hit_penalty_natural_six_still_hits -v`
Expected: FAIL (ключ `hit_penalty` игнорируется).

- [ ] **Step 3: Implement**

В `_normalize_effects` добавить дефолт и парсинг:
```python
    out = {
        "cover": False,
        "reroll_hits": None,
        "reroll_wounds": None,
        "reroll_save": None,
        "strength_mod": 0,
        "ap_improve": 0,
        "hit_penalty": 0,
        "invuln_grant": 0,
    }
```
(в ветке `isinstance(effects, dict)`)
```python
        try:
            out["hit_penalty"] = max(0, int(effects.get("hit_penalty", 0) or 0))
        except (TypeError, ValueError):
            out["hit_penalty"] = 0
        try:
            out["invuln_grant"] = max(0, int(effects.get("invuln_grant", 0) or 0))
        except (TypeError, ValueError):
            out["invuln_grant"] = 0
```
В hit-петле учесть порог `bs + hit_penalty` (натуральная 6 всегда хит):
```python
    hit_threshold = bs + int(eff["hit_penalty"])
    hits = 0
    crit_hits = 0
    for r in rolls:
        r = int(r)
        if r == 1:
            continue
        if r == 6:
            hits += 1
            crit_hits += 1
            continue
        if r >= hit_threshold:
            hits += 1
```
(Reroll-hits «all» сравнение оставить с `bs`; натуральная 6 всё равно не рероллится.)

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(strat): attack() — hit_penalty (механика Stealth)"
```

---

### Task A3: `attack()` — `invuln_grant` (Go to Ground 6+)

**Files:**
- Modify: `core/engine/utils.py` (save-расчёт ~418-426)
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Produces: `effects["invuln_grant"]: int` — даровать инвул N+, если он лучше текущего сейва/инвула. `save_target = min(save_target, invuln_grant)` при `invuln_grant>0`.

- [ ] **Step 1: Failing test**

```python
def test_invuln_grant_saves_against_ap():
    # Sv4 против AP-3 → 7+ (нельзя). invuln_grant=6 → 6+. save [6]: без грант урон 1, с грантом 0.
    weapon = _ranged_weapon(S=4, AP=-3)
    defender = {"Sv": 4, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[6], save=[6]))
    grant, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"invuln_grant": 6},
                      roller=StubRoller(hit=[5], wound=[6], save=[6]))
    assert float(sum(base)) == 1.0
    assert float(sum(grant)) == 0.0
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/test_attack_effects.py::test_invuln_grant_saves_against_ap -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

После блока `if inv and inv > 0: save_target = min(save_target, inv)` добавить:
```python
    granted = int(eff["invuln_grant"])
    if granted > 0:
        save_target = min(save_target, granted)
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(strat): attack() — invuln_grant (Go to Ground 6+)"
```

---

### Task A4: Реестр — Command Re-roll = один бросок

**Files:**
- Modify: `core/engine/phases/stratagem_engine.py` (`_FIGHT_EFFECT_PAYLOAD` ~43-46); `core/engine/phases/stratagems.py` (коммент `command_reroll` ~134-151)
- Test: `tests/engine/phases/test_stratagem_engine.py`

**Interfaces:**
- Consumes: `attack()` `reroll_wounds="one"` (Task A1).
- Produces: применение `command_reroll` пишет в `active_stratagem_effects` `reroll_wounds="one"`.

- [ ] **Step 1: Failing test**

```python
def test_command_reroll_payload_is_single():
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.modelCP = 3
    env.battle_round = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="fight")
    rec = [r for r in env.active_stratagem_effects if r["effect_id"] == "command_reroll_wounds"][0]
    assert rec["reroll_wounds"] == "one"
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_stratagem_engine.py::test_command_reroll_payload_is_single -v`
Expected: FAIL (сейчас `"all"`).

- [ ] **Step 3: Implement**

В `stratagem_engine.py`:
```python
    _FIGHT_EFFECT_PAYLOAD = {
        "hungry_void_strength_mod": {"strength_mod": 1},
        "command_reroll_wounds": {"reroll_wounds": "one"},
    }
```
В `stratagems.py` поправить коммент `command_reroll`: «реролл ОДНОГО проваленного wound-броска (fight-only упрощение реального per-roll правила)».

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_engine.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/phases/stratagem_engine.py core/engine/phases/stratagems.py tests/engine/phases/test_stratagem_engine.py
git commit -m "feat(strat): Command Re-roll — реролл одного броска ран"
```

---

### Task A5: Go to Ground — эффект cover + 6+ invuln

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_maybe_use_go_to_ground` ~4123-4169; `_resolve_cover_effect_for_shot` ~2215-2252); `core/engine/phases/stratagems.py` (коммент GtG ~152-169)
- Test: `tests/engine/phases/test_go_to_ground.py`

**Interfaces:**
- Consumes: `attack()` `invuln_grant` (Task A3).
- Produces: `_maybe_use_go_to_ground` возвращает dict `{"cover": True, "invuln_grant": 6}`; `_resolve_cover_effect_for_shot` мёржит cover в dict-эффекты.

- [ ] **Step 1: Failing test** (добавить в существующий файл)

```python
def test_go_to_ground_returns_cover_and_invuln():
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["Infantry"]
    eff = env._maybe_use_go_to_ground("model", 0, "shooting")
    assert isinstance(eff, dict)
    assert eff.get("cover") is True
    assert int(eff.get("invuln_grant", 0)) == 6
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_go_to_ground.py::test_go_to_ground_returns_cover_and_invuln -v`
Expected: FAIL (возвращается строка `"benefit of cover"`).

- [ ] **Step 3: Implement**

В `_maybe_use_go_to_ground` заменить `return "benefit of cover"` на:
```python
        return {"cover": True, "invuln_grant": 6}
```
В `_resolve_cover_effect_for_shot` добавить поддержку dict (cover-мёрж), в начало после `effect_norm`:
```python
        if isinstance(base_effect, dict):
            report = self._visibility_report_between_units(attacker_side, int(attacker_idx), defender_side, int(defender_idx))
            if bool(report.get("los", False)) and bool(report.get("obscured", False)):
                base_effect = dict(base_effect)
                base_effect["cover"] = True
            return base_effect
```
В `stratagems.py` поправить коммент GtG: «реальный эффект — Benefit of Cover + **6+ invulnerable save**; моделируем оба».

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_go_to_ground.py tests/engine/phases/test_reaction_go_to_ground.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py core/engine/phases/stratagems.py tests/engine/phases/test_go_to_ground.py
git commit -m "feat(strat): Go to Ground — Benefit of Cover + 6+ invuln"
```

---

### Task A6: Smokescreen — эффект cover + Stealth

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_maybe_use_smokescreen` ~4225-4234); `core/engine/phases/stratagems.py` (коммент Smokescreen ~79-96)
- Test: `tests/engine/phases/test_reaction_smokescreen.py`

**Interfaces:**
- Consumes: `attack()` `hit_penalty` (Task A2); dict-мёрж из Task A5.
- Produces: `_maybe_use_smokescreen` возвращает `{"cover": True, "hit_penalty": 1}`.

- [ ] **Step 1: Failing test**

```python
def test_smokescreen_returns_cover_and_stealth():
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.unit_data[0]["Keywords"] = ["Smoke"]
    eff = env._maybe_use_smokescreen("model", 0, "shooting")
    assert isinstance(eff, dict)
    assert eff.get("cover") is True
    assert int(eff.get("hit_penalty", 0)) == 1
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_reaction_smokescreen.py::test_smokescreen_returns_cover_and_stealth -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

В `_maybe_use_smokescreen` заменить финальный `return "benefit of cover"` на:
```python
        return {"cover": True, "hit_penalty": 1}
```
В `stratagems.py` поправить коммент Smokescreen: «моделируем Benefit of Cover + Stealth (hit_penalty=1)».

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_reaction_smokescreen.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py core/engine/phases/stratagems.py tests/engine/phases/test_reaction_smokescreen.py
git commit -m "feat(strat): Smokescreen — Benefit of Cover + Stealth (hit_penalty)"
```

---

### Task A7: Hungry Void — keyword NECRONS + AP+1 при Character-лидере

**Files:**
- Modify: `core/engine/phases/stratagems.py` (`hungry_void` `keyword_req` ~122-133); `core/envs/warhamEnv.py` (`_fight_effects_for_attacker` ~2254-2269)
- Test: `tests/engine/phases/test_stratagems.py`, новый `tests/engine/phases/test_hungry_void.py`

**Interfaces:**
- Consumes: `attack()` `ap_improve` (существует); `_unit_has_keyword`.
- Produces: `hungry_void.keyword_req=("necrons",)`; `_fight_effects_for_attacker` добавляет `ap_improve=1`, если атакующий юнит имеет keyword `character`.

**Решение по «Character-лидеру» (спек §9):** в песочнице нет явного прикрепления лидера → AP-бонус гейтим по наличию у юнита keyword `character` (через `_unit_has_keyword`). «Ещё не дрался» обеспечивается таймингом применения (fight-стратагемы применяются в начале фазы до боёв).

- [ ] **Step 1: Failing test** (`test_hungry_void.py`)

```python
from tests.engine.phases._helpers import build_env


def test_hungry_void_keyword_gate():
    from core.engine.phases.stratagems import by_id
    assert by_id("hungry_void").keyword_req == ("necrons",)


def test_hungry_void_ap_only_for_character():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.battle_round = 1
    env.phase = "fight"
    env.active_stratagem_effects = [{
        "side": "model", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "hungry_void_strength_mod", "strength_mod": 1,
    }]
    # без character — только +S
    env.unit_data[0]["Keywords"] = ["Necrons", "Infantry"]
    eff_plain = env._fight_effects_for_attacker("model", 0)
    assert eff_plain.get("strength_mod") == 1
    assert int(eff_plain.get("ap_improve", 0)) == 0
    # с character — +S и +1 AP
    env.unit_data[0]["Keywords"] = ["Necrons", "Character"]
    eff_char = env._fight_effects_for_attacker("model", 0)
    assert int(eff_char.get("ap_improve", 0)) == 1
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_hungry_void.py -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

В `stratagems.py` у `hungry_void`: `keyword_req=("necrons",)`.
В `_fight_effects_for_attacker`, в ветке `hungry_void_strength_mod` после установки `strength_mod`:
```python
            if rec.get("effect_id") == "hungry_void_strength_mod":
                effects["strength_mod"] = int(effects.get("strength_mod", 0)) + int(rec.get("strength_mod", 1))
                unit_data_list = self.unit_data if str(side) == "model" else self.enemy_data
                if 0 <= int(unit_idx) < len(unit_data_list) and self._unit_has_keyword(unit_data_list[int(unit_idx)], "character"):
                    effects["ap_improve"] = int(effects.get("ap_improve", 0)) + 1
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_hungry_void.py tests/engine/phases/test_stratagems.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/phases/stratagems.py core/envs/warhamEnv.py tests/engine/phases/test_hungry_void.py
git commit -m "feat(strat): Hungry Void — keyword NECRONS + AP+1 при Character-лидере"
```

---

### Task A8: Fire Overwatch — 24" + LOS + once-per-turn

**Files:**
- Modify: `core/engine/phases/stratagems.py` (`overwatch.usage_limit` → `PER_TURN`, коммент); `core/envs/warhamEnv.py` (`_collect_overwatch_candidates` ~4236-4262; LOS-гейт в `_resolve_overwatch` перед выстрелом ~4346)
- Test: `tests/engine/phases/test_reaction_overwatch.py`

**Interfaces:**
- Consumes: `_visibility_report_between_units`.
- Produces: кандидаты overwatch только при `distance <= 24` И LOS; `usage_limit=PER_TURN`.

- [ ] **Step 1: Failing test**

```python
def test_overwatch_blocked_beyond_24(monkeypatch):
    import core.envs.warhamEnv as warham_mod
    def fake_attack(ah, w, ad, dh, dd, *a, **k):
        return [3.0], max(0.0, dh - 3.0)
    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _setup(env)
    # увести цель за 24" (грид-координаты), дальность оружия 24
    env.unit_coords[0] = [0.0, 0.0]
    env.enemy_coords[0] = [25.0, 0.0]
    env._resolve_overwatch("model", "enemy", 0, "movement")
    assert "overwatch" not in [r[1] for r in env.stratagem_used]


def test_overwatch_usage_limit_per_turn():
    from core.engine.phases.stratagems import by_id, UsageLimit
    assert by_id("overwatch").usage_limit is UsageLimit.PER_TURN
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_reaction_overwatch.py::test_overwatch_blocked_beyond_24 tests/engine/phases/test_reaction_overwatch.py::test_overwatch_usage_limit_per_turn -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

В `stratagems.py`: `overwatch.usage_limit=UsageLimit.PER_TURN`; коммент: «range 24", требуется LOS, once per turn (PER_TURN)».
В `_collect_overwatch_candidates` заменить условие дальности на min(24, дальность оружия) + LOS:
```python
            within = self._distance_between_units(defender_side, i, target_side, moving_idx)
            weapon_range = float(defender_weapon[i]["Range"])
            if within > min(24.0, weapon_range):
                continue
            rep = self._visibility_report_between_units(defender_side, i, target_side, moving_idx)
            if not bool(rep.get("los", False)):
                continue
            candidates.append(i)
```
(заменив прежнюю строку `if self._distance_between_units(...) <= defender_weapon[i]["Range"]: candidates.append(i)`).

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_reaction_overwatch.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/phases/stratagems.py core/envs/warhamEnv.py tests/engine/phases/test_reaction_overwatch.py
git commit -m "feat(strat): Fire Overwatch — 24\" + LOS + once-per-turn"
```

---

### Task A9: Честные метрики eval + мёртвые heads

**Files:**
- Modify: `eval.py` (`cp_used` ~1055,1071; комменты `_USE_CP_STRATAGEM_HEAD` ~64-70)
- Modify: `core/envs/warhamEnv.py` (коммент action_space ~984)
- Test: `tests/test_eval_stratagem_metric.py` (новый, лёгкий unit на хелперах eval)

**Interfaces:**
- Produces: в `round_stats` ключ `use_cp_head_set` (бывш. `cp_used`); основной показатель применения — `strat_applied`.

- [ ] **Step 1: Failing test**

```python
from eval import stratagem_attempt_from_action


def test_use_cp_head_maps_only_known_ids():
    assert stratagem_attempt_from_action({"use_cp": 1, "cp_on": 0})[0] == "insane_bravery"
    # head 2/3/4 помечены как не исполняемые в плоском пути — но маппинг сохраняем для трейс-логов
    assert stratagem_attempt_from_action({"use_cp": 0})[0] is None
```

- [ ] **Step 2: Run, expect PASS-как-есть или адаптировать** (маппинг уже существует)

Run: `python -m pytest tests/test_eval_stratagem_metric.py -v`
Expected: PASS (фиксируем текущее поведение перед переименованием).

- [ ] **Step 3: Implement**

В `eval.py` переименовать ключ `cp_used`→`use_cp_head_set` в инициализации `round_stats` и инкременте; в итоговых строках вывода рядом печатать `strat_applied`. Добавить коммент к `_USE_CP_STRATAGEM_HEAD`: «heads 2/3/4 — для трейса; в плоском action_dict не исполняются (реакции идут через value-gate)».
В `warhamEnv.py` к строке `'use_cp': spaces.Discrete(5)` добавить коммент: «реально исполняется только 1 (Insane Bravery); 2/3/4 — реакции через value-gate, не плоский head».

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/test_eval_stratagem_metric.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add eval.py core/envs/warhamEnv.py tests/test_eval_stratagem_metric.py
git commit -m "feat(strat): честная метрика strat_applied; пометка мёртвых use_cp heads"
```

- [ ] **Чекпойнт фазы A:** запустить `engine-regression-reviewer` по диффу; `python -m pytest tests/engine -q`.

---

## ФАЗА B — Единый value-гейт

### Task B1: Обобщить value-policy (reaction → stratagem)

**Files:**
- Modify: `core/models/reaction_value_policy.py`
- Test: `tests/models/test_reaction_value_policy.py`

**Interfaces:**
- Produces: `make_stratagem_value_policy(net_by_side, *, device, eps=0.0)` — идентичная логика; `make_reaction_value_policy = make_stratagem_value_policy` (обратная совместимость как алиас).

- [ ] **Step 1: Failing test**

```python
def test_stratagem_value_policy_alias_exists():
    from core.models.reaction_value_policy import make_stratagem_value_policy, make_reaction_value_policy
    assert make_reaction_value_policy is make_stratagem_value_policy
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/models/test_reaction_value_policy.py::test_stratagem_value_policy_alias_exists -v`
Expected: FAIL (нет имени).

- [ ] **Step 3: Implement**

Переименовать функцию в `make_stratagem_value_policy` и добавить в конце модуля:
```python
make_reaction_value_policy = make_stratagem_value_policy
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/models/test_reaction_value_policy.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/models/reaction_value_policy.py tests/models/test_reaction_value_policy.py
git commit -m "refactor(strat): make_stratagem_value_policy (+ alias reaction)"
```

---

### Task B2: Обобщить `_should_use_reaction` → `_should_use_stratagem`

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_should_use_reaction` ~4032-4057)
- Test: `tests/engine/phases/test_reaction_policy_seam.py`

**Interfaces:**
- Produces: метод `_should_use_stratagem(self, stratagem_id, side, chosen, candidates, phase, cp, *, resolve_trigger=None, net=None)`; `_should_use_reaction` остаётся тонкой обёрткой над ним (parity вызовов).

- [ ] **Step 1: Failing test**

```python
def test_should_use_stratagem_no_policy_returns_true():
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reaction_policy = None
    assert env._should_use_stratagem("insane_bravery", "model", 0, [0], "command", 1) is True
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py::test_should_use_stratagem_no_policy_returns_true -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

Переименовать тело `_should_use_reaction` в `_should_use_stratagem` (та же логика; `getattr(self, "reaction_policy", None)`). Оставить:
```python
    def _should_use_reaction(self, *args, **kwargs) -> bool:
        return self._should_use_stratagem(*args, **kwargs)
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_policy_seam.py
git commit -m "refactor(strat): _should_use_stratagem (общий гейт, обёртка reaction)"
```

---

### Task B3: Fight-стратагемы через value-гейт под windowed_selfplay

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_apply_pending_fight_stratagem_plan` ~2279-2304)
- Test: `tests/engine/phases/test_windowed_fight_stratagem.py` (новый)

**Interfaces:**
- Consumes: `_should_use_stratagem` (Task B2), `_apply_stratagem`.
- Produces: под windowed_selfplay план НЕ обнуляется; каждый юнит из плана проходит value-гейт перед применением.

- [ ] **Step 1: Failing test**

```python
from tests.engine.phases._helpers import build_env


def test_fight_stratagem_applied_under_windowed(monkeypatch):
    import core.engine.phases.windowed_selfplay as ws
    monkeypatch.setattr(ws, "windowed_selfplay_enabled", lambda: True)
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.battle_round = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.reaction_policy = None  # без политики гейт = legacy «да»
    env.unitInAttack[0] = [1, 0]
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    env._apply_pending_fight_stratagem_plan("model")
    assert "command_reroll" in [r[1] for r in env.stratagem_used]
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_windowed_fight_stratagem.py -v`
Expected: FAIL (план обнуляется под windowed).

- [ ] **Step 3: Implement**

Убрать ранний `return` для windowed; пропускать каждый юнит через гейт:
```python
    def _apply_pending_fight_stratagem_plan(self, side: str) -> None:
        plan = getattr(self, "_pending_fight_stratagem_plan", None)
        self._pending_fight_stratagem_plan = None
        if not plan:
            return
        health = self.unit_health if side == "model" else self.enemy_health
        in_attack = self.unitInAttack if side == "model" else self.enemyInAttack
        cp = self.modelCP if side == "model" else self.enemyCP
        for u, sid in dict(plan).items():
            ui = int(u)
            if not (0 <= ui < len(health)) or health[ui] <= 0:
                continue
            if in_attack[ui][0] != 1:
                continue
            if not self._should_use_stratagem(
                str(sid), side, ui, [ui], "fight", cp,
                net=getattr(self, "_reaction_net_by_side", {}).get(side),
            ):
                continue
            try:
                _apply_stratagem(self, side, str(sid), ui, phase="fight")
            except Exception as exc:
                self._log(f"[STRATAGEM] pending fight plan: не применили {sid!r} на юните {ui}: {exc}")
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_windowed_fight_stratagem.py tests/engine/phases -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_windowed_fight_stratagem.py
git commit -m "fix(strat): fight-стратагемы под windowed_selfplay через value-гейт"
```

---

### Task B4: Insane Bravery через value-гейт

**Files:**
- Modify: `core/envs/warhamEnv.py` (`command_phase`, model-ветка ~4636-4643)
- Test: `tests/engine/phases/test_stratagem_insane_bravery.py`

**Interfaces:**
- Consumes: `_should_use_stratagem`.
- Produces: при `reaction_policy is None` решение = прежнее (`decide_bravery`/`use_cp==1`); при наличии политики — value-гейт.

- [ ] **Step 1: Failing test**

```python
def test_insane_bravery_value_gate_used_when_policy(monkeypatch):
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}
    def fake_gate(sid, side, chosen, cand, phase, cp, **k):
        calls["sid"] = sid
        return True
    env.reaction_policy = object()  # не None
    monkeypatch.setattr(env, "_should_use_stratagem", fake_gate)
    # форсим провал battle-shock на юните 0
    monkeypatch.setattr("core.envs.warhamEnv.dice", lambda num=1: [1, 1])
    env.unit_health[0] = 1
    env.unit_data[0]["W"] = 4  # ниже половины
    env.modelCP = 3
    env.command_phase("model", action={"use_cp": 0, "cp_on": -1})
    assert calls.get("sid") == "insane_bravery"
```

- [ ] **Step 2: Run, expect FAIL**

Run: `python -m pytest tests/engine/phases/test_stratagem_insane_bravery.py::test_insane_bravery_value_gate_used_when_policy -v`
Expected: FAIL.

- [ ] **Step 3: Implement**

В model-ветке `command_phase`, заменить выбор `_use_bravery`:
```python
                        if getattr(self, "reaction_policy", None) is not None and decide_bravery is None:
                            _use_bravery = self._should_use_stratagem(
                                "insane_bravery", "model", i, [i], "command", int(self.modelCP),
                                net=getattr(self, "_reaction_net_by_side", {}).get("model"),
                            )
                        elif decide_bravery is not None:
                            _use_bravery = bool(decide_bravery(i))
                        else:
                            _use_bravery = bool(action and action.get("use_cp") == 1 and action.get("cp_on") == i)
```

- [ ] **Step 4: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_insane_bravery.py -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_insane_bravery.py
git commit -m "feat(strat): Insane Bravery через единый value-гейт (при наличии политики)"
```

- [ ] **Чекпойнт фазы B:** `engine-regression-reviewer`; `python -m pytest tests/engine tests/models -q`.

---

## ФАЗА C — Интеграция, parity, smoke

### Task C1: Parity-тест (без политики = legacy)

**Files:**
- Test: `tests/engine/phases/test_stratagem_value_gate_parity.py` (новый)

**Interfaces:**
- Consumes: `run_windowed_default_turn` (`_helpers`).

- [ ] **Step 1: Write test**

```python
from tests.engine.phases._helpers import build_env, run_windowed_default_turn


def test_no_policy_runs_turn_without_error_and_no_strat_applied():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.reaction_policy = None
    env.stratagem_used = []
    run_windowed_default_turn(env, side="model")
    # без политики/плана авто-fight-стратагемы не применяются молча
    assert isinstance(env.stratagem_used, list)
```

- [ ] **Step 2: Run, expect PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_value_gate_parity.py -v`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add tests/engine/phases/test_stratagem_value_gate_parity.py
git commit -m "test(strat): parity — без политики поведение legacy"
```

---

### Task C2: Smoke train/eval + полный прогон тестов

**Files:** —

- [ ] **Step 1: Полный прогон тестов**

Run: `python -m pytest tests -q`
Expected: всё зелёное (или только заранее известные skips).

- [ ] **Step 2: Smoke eval (короткий)**

Запуск через Qt GUI (приоритет, AGENTS.md) или CLI: короткий `eval.py` на 5-10 эпизодов; проверить, что в логах появляются `strat_applied`/`strat_attempt` с разбивкой и нет ошибок применения стратагем.

- [ ] **Step 3: Проверка логов**

Прочитать свежие строки `runtime/logs/LOGS_FOR_AGENTS_EVAL.md`: маркеры применения стратагем, причины отказов (вне 24"/нет LOS/нет CP/usage_limit) присутствуют и читаемы.

- [ ] **Step 4: Финальный чекпойнт**

`engine-regression-reviewer` по полному диффу фаз A–C; затем `/code-review` или `superpowers:requesting-code-review` перед мержем.

---

## Self-Review (выполнено при написании)

- **Покрытие спека:** §4 (правила) → A1–A8; §5 (метрики/heads) → A9; §3 (value-гейт) → B1–B4; §6 (тесты) → распределены по задачам; §7 (фазы) → A/B/C; §9 (Character-лидер) → решение в A7, (Stealth↔hit_on_6) → A2 (натуральная 6 всегда хит).
- **Плейсхолдеры:** нет; весь код приведён.
- **Согласованность типов:** `reroll_wounds="one"`, `hit_penalty`/`invuln_grant` (int), `_should_use_stratagem` сигнатура едина в B2/B3/B4; `make_stratagem_value_policy` алиас в B1.
