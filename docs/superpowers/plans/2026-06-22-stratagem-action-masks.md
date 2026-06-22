# Стратагемы как действия — Под-проект 2 (маски) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заменить дефолтные all-True маски новых голов `strat_<phase>`/`strat_<phase>_unit` на реальные факторизованные маски легальности (CP / usage_limit / keyword / alive), зеркало `use_cp`/`cp_on`.

**Architecture:** Хелпер `_stratagem_choice_legal(side, phase, choice)` (CP≥cost, не usage-exhausted, есть живой keyword-юнит) + заполнение масок strat-голов в `get_legal_action_masks_by_head` (единый источник; `build_action_masks_by_head` в utils делегирует туда). Лояльно: index 0 (none) всегда легален, unit-маска = живые юниты, fallback на [0].

**Tech Stack:** Python 3.12+, NumPy, Gymnasium, pytest. Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-stratagem-action-masks-design.md`. **Под-проект 2 из 5** («стратагемы как действия»). Под-проект 1 (кодирование) уже в коде.
- **Факторизовано + лояльно** (как `use_cp`/`cp_on`): `strat_<phase>`[0]=none всегда True; [k] по легальности; `strat_<phase>_unit` = живые юниты; fallback [0].
- **`strat_<phase>` НЕ гейтить по `env.phase`** (action_dict — на весь ход): легальность только по CP/usage_limit/keyword/alive.
- **Подтипы** (`command_reroll:hit/wound/...`) маскируются по `base_id` (часть до `:`); легальность от подтипа не зависит.
- **`use_cp`/`cp_on` маски не трогать.** Применение голов не требуется (под-проект 3). Взаимодействие с `reaction_policy` — под-проект 3, не здесь.
- **Единый источник масок:** `Warhammer40kEnv.get_legal_action_masks_by_head` (utils `build_action_masks_by_head` делегирует в него + fallback all-True). Правим только env-метод.
- **Факт:** новые strat-ключи уже получают all-True по дефолтному циклу (warhamEnv:1764-1768) → KeyError нет; задача — сузить до легальности.
- Язык RU; `ruff check --fix`; baseline `tests/engine/` 23; коммит RU + `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. DRY/YAGNI/TDD.

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/envs/warhamEnv.py` | `_stratagem_choice_legal` (хелпер) + заполнение strat-масок в `get_legal_action_masks_by_head` | 1, 2 |
| `tests/engine/phases/test_stratagem_action_masks.py` (новый) | хелпер легальности + маски голов | 1, 2 |

---

## Task 1: хелпер `_stratagem_choice_legal`

**Files:** Modify `core/envs/warhamEnv.py`; Test `tests/engine/phases/test_stratagem_action_masks.py` (новый).

**Interfaces:**
- Produces: `Warhammer40kEnv._stratagem_choice_legal(side: str, phase, choice: str) -> bool` — `"none"`→True; иначе True ⟺ CP≥cost базовой стратагемы, не `usage_limit_reached`, есть ≥1 живой юнит стороны с `keyword_req` (или ≥1 живой, если keyword пуст).

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_stratagem_action_masks.py`:
```python
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []


def test_choice_none_always_legal():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "none") is True


def test_command_reroll_needs_cp():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is False
    env.modelCP = 1
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is True
    # подтип не влияет на легальность
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:wound") is True


def test_hungry_void_requires_necrons_keyword():
    env = build_env()
    _setup(env, cp=2)
    # по умолчанию у юнитов нет necrons-keyword (build_env) → hungry_void нелегален
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is True


def test_usage_limit_blocks_choice():
    env = build_env()
    _setup(env, cp=3)
    env.battle_round = 1
    env.unit_data[0]["Keywords"] = ["Necrons"]
    # hungry_void PER_PHASE: запись в journal → нелегален в той же (round, phase)
    env.stratagem_used = [("model", "hungry_void", 1, "fight", 0)]
    env.phase = "fight"
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_masks.py -v`
Expected: FAIL — `AttributeError: ... '_stratagem_choice_legal'`.

- [ ] **Step 3: Реализация** — в `core/envs/warhamEnv.py` (рядом с `get_legal_action_masks_by_head`):
```python
    def _stratagem_choice_legal(self, side: str, phase, choice: str) -> bool:
        """Легальна ли категория головы strat_<phase> сейчас (CP/usage_limit/keyword/alive).

        choice "none" → всегда True. Иначе base_id = часть до ':' (подтип не влияет на легальность).
        Лоялен (как use_cp): keyword-связку с конкретным юнитом не проверяем (это unit-голова +
        валидация применения), здесь — есть ли ХОТЯ БЫ один живой юнит с нужным keyword.
        """
        from core.engine.phases.stratagems import by_id, usage_limit_reached

        if str(choice) == "none":
            return True
        base_id = str(choice).split(":", 1)[0]
        try:
            d = by_id(base_id)
        except KeyError:
            return False
        is_model = side == "model"
        cp = int(self.modelCP if is_model else self.enemyCP)
        if cp < int(d.cp_cost):
            return False
        phase_str = phase.value if hasattr(phase, "value") else str(phase)
        if usage_limit_reached(self, side, d, phase=phase_str):
            return False
        health = self.unit_health if is_model else self.enemy_health
        unit_data = self.unit_data if is_model else self.enemy_data
        alive = [i for i in range(len(health)) if health[i] > 0]
        if not alive:
            return False
        if d.keyword_req:
            return any(
                all(self._unit_has_keyword(unit_data[i], kw) for kw in d.keyword_req) for i in alive
            )
        return True
```

- [ ] **Step 4: Запустить — PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_masks.py -v`
Expected: PASS. Затем `ruff check --fix core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_masks.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_masks.py
git commit -m "feat(env): хелпер _stratagem_choice_legal (CP/usage/keyword/alive) для strat-масок"
```

---

## Task 2: заполнение strat-масок в `get_legal_action_masks_by_head`

**Files:** Modify `core/envs/warhamEnv.py` (`get_legal_action_masks_by_head`, после блока `use_cp`/`cp_on` ~строка 1841). Test `tests/engine/phases/test_stratagem_action_masks.py`.

**Interfaces:**
- Consumes: `_stratagem_choice_legal` (Task 1); `STRATAGEM_PHASES`, `stratagem_action_choices` (под-проект 1).
- Produces: `get_legal_action_masks_by_head(side)` возвращает корректные маски `strat_<phase>` (по легальности) и `strat_<phase>_unit` (живые юниты) вместо all-True.

- [ ] **Step 1: Написать падающий тест**
```python
def test_strat_phase_mask_cp_gating():
    env = build_env()
    _setup(env, cp=0)
    masks = env.get_legal_action_masks_by_head("model")
    fm = masks["strat_fight"]
    assert bool(fm[0]) is True  # none всегда
    assert not bool(fm[1:].any())  # CP=0 → только none
    env2 = build_env()
    _setup(env2, cp=2)
    fm2 = env2.get_legal_action_masks_by_head("model")["strat_fight"]
    # command_reroll:hit/wound легальны при CP (hungry_void без necrons — нет)
    from core.engine.phases.stratagems import stratagem_action_choices
    choices = stratagem_action_choices(__import__("core.engine.phases.types", fromlist=["Phase"]).Phase.FIGHT)
    assert bool(fm2[choices.index("command_reroll:hit")]) is True
    assert bool(fm2[choices.index("command_reroll:wound")]) is True


def test_strat_unit_mask_alive_only():
    env = build_env()
    _setup(env, cp=2)
    env.unit_health[1] = 0.0
    masks = env.get_legal_action_masks_by_head("model")
    um = masks["strat_fight_unit"]
    assert bool(um[0]) is True
    assert bool(um[1]) is False  # мёртв


def test_strat_mask_sizes_match_space():
    env = build_env()
    _setup(env, cp=2)
    from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices
    masks = env.get_legal_action_masks_by_head("model")
    spaces = env.action_space.spaces
    for ph in STRATAGEM_PHASES:
        assert len(masks[f"strat_{ph.value}"]) == len(stratagem_action_choices(ph))
        assert len(masks[f"strat_{ph.value}_unit"]) == int(spaces[f"strat_{ph.value}_unit"].n)


def test_build_action_masks_delegates_strat():
    from core.models.utils import build_action_masks_by_head
    env = build_env()
    _setup(env, cp=0)
    ordered = build_action_masks_by_head(env, 2, side="model")
    # порядок ordered_action_keys: strat_fight маска присутствует и [0] разрешён
    from core.models.action_contract import ordered_action_keys
    keys = ordered_action_keys(2)
    idx = keys.index("strat_fight")
    assert bool(ordered[idx][0]) is True
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_masks.py -k "strat_phase_mask or strat_unit_mask or strat_mask_sizes or delegates_strat" -v`
Expected: FAIL — сейчас маски all-True (`fm[1:].any()` True при CP=0; мёртвый юнит True).

- [ ] **Step 3: Реализация** — в `get_legal_action_masks_by_head`, ПОСЛЕ блока `masks["use_cp"] = use_cp_mask` (~строка 1841), вставить:
```python
        # Под-проект 2: маски пофазных голов стратагем (заменяют дефолтный all-True).
        from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices

        for _ph in STRATAGEM_PHASES:
            _skey = f"strat_{_ph.value}"
            if _skey in spaces:
                _choices = stratagem_action_choices(_ph)
                _sm = np.zeros(len(_choices), dtype=bool)
                _sm[0] = True  # none всегда легален
                for _k in range(1, len(_choices)):
                    if self._stratagem_choice_legal(side, _ph, _choices[_k]):
                        _sm[_k] = True
                masks[_skey] = _sm
            _ukey = f"strat_{_ph.value}_unit"
            if _ukey in spaces:
                _un = int(spaces[_ukey].n)
                _um = np.zeros(_un, dtype=bool)
                for _i in range(min(_un, len(unit_health))):
                    if unit_health[_i] > 0:
                        _um[_i] = True
                if not _um.any():
                    _um[0] = True
                masks[_ukey] = _um
```
(`np`, `spaces`, `unit_health`, `side` уже в области видимости метода.)

- [ ] **Step 4: Запустить — PASS + регрессия**

Run: `python -m pytest tests/engine/phases/test_stratagem_action_masks.py -v`
Expected: PASS. Затем регрессия потребителей масок:
`python -m pytest tests/models/ tests/engine/phases/ -q`
Expected: проход; `python -m pytest tests/engine/ -q` → сверить **23 failed (baseline)**, тот же набор файлов (0 новых). `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: engine-regression-reviewer + Коммит**

Запустить `engine-regression-reviewer` (маски — общий путь DQN/PPO/AZ). Затем:
```
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_action_masks.py
git commit -m "feat(env): маски strat_<phase>/strat_<phase>_unit в get_legal_action_masks_by_head"
```

---

## Self-Review

**Spec coverage:**
- `strat_<phase>` маска (none всегда; legality по CP/usage/keyword; без env.phase-гейтинга) — Task 2 + хелпер Task 1. ✅
- `strat_<phase>_unit` маска (живые юниты, fallback [0]) — Task 2. ✅
- Подтипы по base_id — Task 1 (`split(":",1)[0]`). ✅
- usage_limit / keyword / CP — Task 1 (`usage_limit_reached`, `_unit_has_keyword`, CP). ✅
- Единый источник (`get_legal_action_masks_by_head`); utils делегирует — Task 2 (тест `delegates_strat`). ✅
- `use_cp`/`cp_on` не тронуты — вставка ПОСЛЕ их блока, их код не меняется. ✅
- Потребители не падают / baseline 23 — Task 2 Step 4. ✅
- Применение не требуется (под-проект 3) — головы остаются no-op. ✅

**Placeholder scan:** код во всех шагах полный. Тест `test_strat_phase_mask_cp_gating` использует `stratagem_action_choices(Phase.FIGHT)` для индексов (не хардкод) — корректно.

**Type consistency:** `_stratagem_choice_legal(side, phase, choice)->bool` (Task 1) ровно как зовётся в Task 2; ключи `strat_{ph.value}`/`strat_{ph.value}_unit` едины с под-проектом 1.

**Примечание:** риск «латентный KeyError» из спеки снят (дефолтный all-True цикл уже покрывает ключи) — здесь только сужаем маски; крэша нет ни до, ни после.

---

## Execution Handoff

См. ниже выбор способа исполнения.
