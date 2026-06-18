# Track 1 · Batch #1 — opt-in эффекты `attack()` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Обобщить `effects` в `attack()` до набора композируемых эффектов (cover/ре-ролл хитов/+S/улучшение AP), применяемых только если переданы; поведение по умолчанию идентично текущему.

**Architecture:** Приватный `_normalize_effects(effects) -> dict` + точечные правки в `attack()` (`utils.py`). `expected_damage()` не трогаем.

**Tech Stack:** Python 3.12, numpy, pytest. Без новых зависимостей.

**Спека:** `docs/superpowers/specs/2026-06-17-track1-attack-effects-design.md`.

## Global Constraints

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`, line-length 120.
- **Инвариант:** `attack(effects=None)` и `attack(effects="benefit of cover")` дают тот же результат, что сейчас (при том же `roller`/RNG). Новые ветки активны только при dict-effects, который ни один текущий вызов не передаёт.
- Только `core/engine/utils.py::attack()` + `_normalize_effects`. `expected_damage` (`utils.py:129`) — вне scope.

## Известные факты (точные места в `core/engine/utils.py`)

- `attack()` `:318-497`. `_roll`/`_roll_with_stage` определены `:342-357`; блок профиля начинается `:359`.
- `s = _to_int(attackerWeapon.get("S"), default=0)` `:368`.
- `ap = _to_int(attackerWeapon.get("AP"), default=0)` `:372`.
- `cover_bonus = 1 if (effects == "benefit of cover" and rangeOfComb == "Ranged") else 0` `:375`.
- hit-роллы: `rolls = _roll_with_stage(num=attacks, stage="hit")` `:423`, нормализация в np.array `:424-427`, далее `lethal = ...` `:429` и цикл подсчёта `:433-443`.
- `roller(num, max, stage)` инъектируется; стадии `"hit"/"wound"/"save"`, damage/attacks — без стадии (stage=None).
- Текущие вызовы передают `effects` только `None` или `"benefit of cover"` (`shooting_phase`, `_resolve_overwatch`, `resolve_fight_phase`, `_resolve_cover_effect_for_shot`).

## File Structure

- Modify `core/engine/utils.py` — `_normalize_effects` + правки `attack()`.
- Create `tests/engine/test_attack_effects.py` — детерминированные тесты (StubRoller).

---

### Task 1: `_normalize_effects` + cover через нормализатор (back-compat)

**Files:**
- Modify: `core/engine/utils.py`
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Produces: `_normalize_effects(effects) -> dict` с ключами `cover:bool, reroll_hits:None|"ones"|"all", strength_mod:int, ap_improve:int`. `attack()` использует `eff["cover"]` для cover_bonus.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/test_attack_effects.py`:

```python
from core.engine.utils import _normalize_effects, attack


class StubRoller:
    """Детерминированный roller: очереди по стадиям hit/wound/save (+damage=None)."""

    def __init__(self, hit=None, wound=None, save=None, damage=None, default=6):
        self.q = {
            "hit": list(hit or []),
            "wound": list(wound or []),
            "save": list(save or []),
            None: list(damage or []),
        }
        self.default = default

    def __call__(self, num=1, max=6, stage=None):
        q = self.q.get(stage, [])
        out = [int(q.pop(0)) if q else int(self.default) for _ in range(num)]
        return out if num != 1 else out[0]


_ATT_DATA = {"#OfModels": 1, "W": 1}


def _ranged_weapon(**over):
    w = {"BS": 4, "S": 4, "AP": 0, "Damage": 1, "Attacks": 1, "Range": 24}
    w.update(over)
    return w


def test_normalize_effects_variants():
    assert _normalize_effects(None) == {"cover": False, "reroll_hits": None, "strength_mod": 0, "ap_improve": 0}
    assert _normalize_effects("benefit of cover")["cover"] is True
    d = _normalize_effects({"cover": True, "reroll_hits": "ones", "strength_mod": 1, "ap_improve": 2})
    assert d == {"cover": True, "reroll_hits": "ones", "strength_mod": 1, "ap_improve": 2}
    # неизвестный reroll → None
    assert _normalize_effects({"reroll_hits": "weird"})["reroll_hits"] is None


def test_cover_back_compat_reduces_damage():
    # Sv6, AP0 → save 6+. cover → 5+. save-бросок [5]: без cover не сейвит (урон 1), с cover сейвит (урон 0).
    weapon = _ranged_weapon()
    defender = {"Sv": 6, "T": 4, "IVSave": 0}
    no_cover, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                         roller=StubRoller(hit=[5], wound=[6], save=[5]))
    with_cover, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects="benefit of cover",
                          roller=StubRoller(hit=[5], wound=[6], save=[5]))
    assert float(sum(no_cover)) == 1.0
    assert float(sum(with_cover)) == 0.0


def test_cover_dict_equivalent_to_string():
    weapon = _ranged_weapon()
    defender = {"Sv": 6, "T": 4, "IVSave": 0}
    via_dict, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"cover": True},
                        roller=StubRoller(hit=[5], wound=[6], save=[5]))
    assert float(sum(via_dict)) == 0.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: FAIL — `ImportError: cannot import name '_normalize_effects'`.

- [ ] **Step 3a: Добавить `_normalize_effects`**

В `core/engine/utils.py` перед `def attack(` (около `:318`) добавить:

```python
def _normalize_effects(effects):
    """Привести effects к dict со стабильными ключами (назад-совместимо).

    None -> дефолты (cover=False); "benefit of cover" -> cover=True; dict -> читаем ключи.
    """
    out = {"cover": False, "reroll_hits": None, "strength_mod": 0, "ap_improve": 0}
    if effects is None:
        return out
    if isinstance(effects, str):
        if effects.strip().lower() == "benefit of cover":
            out["cover"] = True
        return out
    if isinstance(effects, dict):
        out["cover"] = bool(effects.get("cover") or effects.get("benefit_of_cover"))
        rh = effects.get("reroll_hits")
        out["reroll_hits"] = rh if rh in ("ones", "all") else None
        try:
            out["strength_mod"] = int(effects.get("strength_mod", 0) or 0)
        except (TypeError, ValueError):
            out["strength_mod"] = 0
        try:
            out["ap_improve"] = int(effects.get("ap_improve", 0) or 0)
        except (TypeError, ValueError):
            out["ap_improve"] = 0
    return out
```

- [ ] **Step 3b: Использовать нормализатор для cover**

В `attack()`, перед строкой `# --- Targets / profile parsing ---` (`:359`), добавить:

```python
    eff = _normalize_effects(effects)
```

Заменить (`:375`):

```python
    cover_bonus = 1 if (effects == "benefit of cover" and rangeOfComb == "Ranged") else 0
```

на:

```python
    cover_bonus = 1 if (eff["cover"] and rangeOfComb == "Ranged") else 0
```

- [ ] **Step 4: Запустить тесты — PASS**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS (3 passed).

- [ ] **Step 5: Регрессия cover-зависимых + коммит**

Run: `python -m pytest tests/engine/test_expected_damage.py tests/engine/test_charge_ev.py tests/engine/phases/ -q`
Expected: PASS.

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): _normalize_effects + cover через нормализатор (Track 1, back-compat)"
```

---

### Task 2: strength_mod + ap_improve

**Files:**
- Modify: `core/engine/utils.py` (`attack()`)
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Consumes: `eff["strength_mod"]`, `eff["ap_improve"]` (из Task 1).

- [ ] **Step 1: Дописать тесты**

Дописать в `tests/engine/test_attack_effects.py`:

```python
def test_strength_mod_changes_wound_threshold():
    # S4 vs T4 → 4+; S5 vs T4 → 3+. wound-бросок [3]: без +S не ранит, с +1 S ранит.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}  # Sv7 → засейвить нельзя
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[3]))
    boosted, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"strength_mod": 1},
                        roller=StubRoller(hit=[5], wound=[3]))
    assert float(sum(base)) == 0.0
    assert float(sum(boosted)) == 1.0


def test_ap_improve_worsens_save():
    # Sv4 AP0 → 4+; ap_improve=1 → AP-1 → 5+. save-бросок [4]: без эффекта сейвит, с эффектом нет.
    weapon = _ranged_weapon(S=4, AP=0)
    defender = {"Sv": 4, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[5], wound=[6], save=[4]))
    improved, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"ap_improve": 1},
                         roller=StubRoller(hit=[5], wound=[6], save=[4]))
    assert float(sum(base)) == 0.0
    assert float(sum(improved)) == 1.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_attack_effects.py -k "strength or ap_improve" -v`
Expected: FAIL — эффект не применяется (boosted/improved == 0).

- [ ] **Step 3: Применить strength_mod и ap_improve**

В `attack()` заменить (`:368`):

```python
    s = _to_int(attackerWeapon.get("S"), default=0)
```

на:

```python
    s = _to_int(attackerWeapon.get("S"), default=0) + int(eff["strength_mod"])
```

Заменить (`:372`):

```python
    ap = _to_int(attackerWeapon.get("AP"), default=0)
```

на:

```python
    ap = _to_int(attackerWeapon.get("AP"), default=0) - int(eff["ap_improve"])
```

- [ ] **Step 4: Запустить тесты — PASS**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS (5 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): strength_mod + ap_improve в attack() (Track 1)"
```

---

### Task 3: reroll_hits + полная регрессия

**Files:**
- Modify: `core/engine/utils.py` (`attack()`)
- Test: `tests/engine/test_attack_effects.py`

**Interfaces:**
- Consumes: `eff["reroll_hits"]`.

- [ ] **Step 1: Дописать тесты**

Дописать в `tests/engine/test_attack_effects.py`:

```python
def test_reroll_hits_ones():
    # bs4. hit-броски [1, 5]: без ре-ролла [1] промах → урон 0; с reroll_hits="ones" [1]→ре-ролл [5] хит → урон 1.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}  # засейвить нельзя
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[1], wound=[6]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "ones"},
                    roller=StubRoller(hit=[1, 5], wound=[6]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0


def test_reroll_hits_all_rerolls_misses():
    # bs4. hit [2] промах (не 1, но < bs) → reroll_hits="all" ре-роллит [5] → хит.
    weapon = _ranged_weapon(S=4)
    defender = {"Sv": 7, "T": 4, "IVSave": 0}
    base, _ = attack(1, weapon, _ATT_DATA, 10, defender,
                     roller=StubRoller(hit=[2], wound=[6]))
    rer, _ = attack(1, weapon, _ATT_DATA, 10, defender, effects={"reroll_hits": "all"},
                    roller=StubRoller(hit=[2, 5], wound=[6]))
    assert float(sum(base)) == 0.0
    assert float(sum(rer)) == 1.0
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_attack_effects.py -k reroll -v`
Expected: FAIL — ре-ролл не применяется (rer == 0).

- [ ] **Step 3: Добавить ре-ролл хитов**

В `attack()` после блока нормализации `rolls` в np.array (после `:427`, перед `lethal = _weapon_has_lethal_hits(attackerWeapon)` `:429`) вставить:

```python
        if eff["reroll_hits"]:
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

(Существующий цикл подсчёта хитов/критов работает на обновлённом `rolls` без изменений.)

- [ ] **Step 4: Запустить тесты — PASS**

Run: `python -m pytest tests/engine/test_attack_effects.py -v`
Expected: PASS (7 passed).

- [ ] **Step 5: Полная регрессия + ruff**

Run: `python -m pytest tests/engine/test_attack_effects.py tests/engine/test_expected_damage.py tests/engine/test_charge_ev.py tests/engine/test_shoot_targets_contract_regression.py tests/engine/phases/ -q`
Expected: PASS (всё).

Run: `python -m ruff check core/engine/utils.py tests/engine/test_attack_effects.py 2>&1 | tail -2`
Expected: чисто на новых строках (если есть преэкзистинг в utils.py — не увеличить).

- [ ] **Step 6: Коммит**

```bash
git add core/engine/utils.py tests/engine/test_attack_effects.py
git commit -m "feat(engine): reroll_hits (ones/all) в attack() (Track 1 batch #1 done)"
```

---

## Self-Review

**Spec coverage:**
- `_normalize_effects` + cover back-compat → Task 1. ✓
- strength_mod, ap_improve → Task 2. ✓
- reroll_hits ones/all → Task 3. ✓
- Тесты: normalizer (T1), cover back-compat + dict (T1), strength/ap (T2), reroll ones/all (T3), регрессия EV/charge/phases/ruff (T1 Step5, T3 Step5). ✓
- Инвариант behavior-neutral при None/строке → тесты cover + регрессия (реакции зовут attack с "benefit of cover"/None). ✓

**Placeholder scan:** код полный; плейсхолдеров нет.

**Type consistency:** `_normalize_effects(effects) -> dict` ключи (`cover/reroll_hits/strength_mod/ap_improve`) едины в нормализаторе, attack() и тестах; StubRoller `(num,max,stage)` совпадает с контрактом `roller`.

## Заметки по исполнению

- `eff = _normalize_effects(effects)` поставить ДО первого использования (`cover_bonus`/`s`/`ap`/reroll). В Task 1 ставим его перед профилем; Task 2/3 уже опираются.
- StubRoller для `num==1` возвращает int (как реальный dice в проекте), для `num>1` — список; attack() обрабатывает оба.
- Damage/Attacks у тестовых оружий фиксированы (1) → не роллятся; управляем только hit/wound/save.
- `expected_damage` остаётся без эффектов (вне scope) — это ожидаемо.
