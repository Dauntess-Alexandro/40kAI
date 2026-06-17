# Stage 7a — Reaction policy seam Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Провести решение трёх реакций (Overwatch/Smokescreen/Heroic) через подключаемый `env.reaction_policy` (default `None` → поведение 1:1) и единое CP-списание через `stratagem_engine.apply`; фикс `heroic.cp_cost=2`.

**Architecture:** Поле `env.reaction_policy` + метод `env._should_use_reaction(...)`; в non-manual ветке каждого резолвера решение «да/нет» берётся из него, CP — через `_apply_stratagem`. Manual (человек) не трогаем. `reaction_policy` не снапшотится.

**Tech Stack:** Python 3.12, pytest. Без новых зависимостей.

**Спека:** `docs/superpowers/specs/2026-06-17-stage7a-reaction-policy-seam-design.md`.

## Global Constraints

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`, line-length 120.
- Язык логов — русский; пропуск реакции логируется (без тишины).
- **Инвариант:** `reaction_policy=None` → реакции срабатывают как раньше, CP списывается столько же, эффект тот же. `reaction_policy` НЕ добавлять в snapshot.
- Хук `ruff_fix.py` срезает временно-неиспользуемые импорты — но `_apply_stratagem` уже импортирован в `warhamEnv.py` (Stage 6).
- `warhamEnv.py` имеет 86 преэкзистинг ruff-ошибок (легаси) — не увеличивать; новые строки чисты.

## Известные факты (точные места)

- `_maybe_use_smokescreen` `:3922-3970`: `use_it=True`(`:3947`), читается `if not use_it`(`:3955`), spend `:3959/3961`. `side_label`(`:3927`), `cp`(`:3929/3932`).
- `_resolve_overwatch` `:4000-4132`: `use_it=True`(`:4023`, мёртвая), `chosen=candidates[0]`(`:4024`), manual `:4025-4047`, spend `self.modelCP-=1`(`:4050`)/`self.enemyCP-=1`(`:4057`). `side_label`(`:4005`), `cp`(`:4011`).
- `_resolve_heroic_intervention` `:4134-4227`: гейт `defender_cp<2`(`:4178`), `use_it=True`(`:4185`, мёртвая), `chosen=eligible[0]`(`:4186`), manual `:4187-4206`, spend `-=2`(`:4209/4211`). `side_label`(`:4152`), `defender_cp`(`:4157/4162`).
- `self.stratagem_used = []` в `__init__` рядом (`:1030`, после enemyStrat) — туда же `reaction_policy`.
- `_apply_stratagem` импортирован: `from core.engine.phases.stratagem_engine import apply as _apply_stratagem` (Stage 6).
- Реестр heroic: `cp_cost=1` → `2` в `core/engine/phases/stratagems.py`.
- `_collect_overwatch_candidates(defender_side, moving_unit_side, moving_idx)` `:3972` — для сетапа теста overwatch.

## File Structure

- Modify `core/engine/phases/stratagems.py` — heroic `cp_cost=2`.
- Modify `core/envs/warhamEnv.py` — `reaction_policy` init, `_should_use_reaction`, шов в 3 резолверах + CP через apply.
- Create `tests/engine/phases/test_reaction_policy_seam.py` — тесты шва.

---

### Task 1: реестр heroic=2 + `reaction_policy` + `_should_use_reaction`

**Files:**
- Modify: `core/engine/phases/stratagems.py`
- Modify: `core/envs/warhamEnv.py`
- Test: `tests/engine/phases/test_reaction_policy_seam.py`

**Interfaces:**
- Produces: `env.reaction_policy` (default None); `env._should_use_reaction(stratagem_id, side, chosen, candidates, phase, cp) -> bool`; `by_id("heroic_intervention").cp_cost == 2`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_reaction_policy_seam.py`:

```python
from core.engine.phases.stratagems import by_id
from tests.engine.phases._helpers import build_env


def test_heroic_registry_cost_is_two():
    assert by_id("heroic_intervention").cp_cost == 2


def test_should_use_reaction_default_true_when_no_policy():
    env = build_env()
    env.reaction_policy = None
    assert env._should_use_reaction("overwatch", "model", 0, [0], "movement", 2) is True


def test_should_use_reaction_delegates_to_policy_and_passes_ctx():
    env = build_env()
    captured = {}

    def policy(ctx):
        captured.update(ctx)
        return False

    env.reaction_policy = policy
    assert env._should_use_reaction("overwatch", "model", 0, [0, 1], "movement", 2) is False
    assert captured["stratagem_id"] == "overwatch"
    assert captured["side"] == "model"
    assert captured["chosen"] == 0
    assert captured["candidates"] == [0, 1]
    assert captured["cp"] == 2


def test_should_use_reaction_policy_exception_falls_back_to_true():
    env = build_env()

    def boom(ctx):
        raise ValueError("policy boom")

    env.reaction_policy = boom
    assert env._should_use_reaction("smokescreen", "model", 0, [0], "shooting", 1) is True
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -v`
Expected: FAIL — `test_heroic_registry_cost_is_two` (cost==1) и `AttributeError: _should_use_reaction`.

- [ ] **Step 3a: Реестр heroic=2**

В `core/engine/phases/stratagems.py`, в записи `heroic_intervention`, заменить `cp_cost=1,` на `cp_cost=2,`.

- [ ] **Step 3b: Поле + хелпер на env**

В `core/envs/warhamEnv.py` после `self.stratagem_used = []` (в `__init__`, около `:1030`) добавить:

```python
        self.reaction_policy = None
```

Добавить метод (перед `def _maybe_use_smokescreen`, около `:3922`):

```python
    def _should_use_reaction(self, stratagem_id, side, chosen, candidates, phase, cp) -> bool:
        """Решение «использовать реакцию»: без политики — текущее поведение (всегда да)."""
        policy = getattr(self, "reaction_policy", None)
        if policy is None:
            return True
        ctx = {
            "side": side,
            "stratagem_id": stratagem_id,
            "phase": phase,
            "chosen": chosen,
            "candidates": list(candidates),
            "cp": int(cp),
        }
        try:
            return bool(policy(ctx))
        except Exception:
            return True
```

- [ ] **Step 4: Запустить тест — PASS**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/stratagems.py core/envs/warhamEnv.py tests/engine/phases/test_reaction_policy_seam.py
git commit -m "feat(phases): reaction_policy + _should_use_reaction + фикс heroic cp_cost=2 (Stage 7a)"
```

---

### Task 2: шов в Smokescreen + CP через apply

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_maybe_use_smokescreen`)
- Test: `tests/engine/phases/test_reaction_policy_seam.py`

**Interfaces:**
- Consumes: `env._should_use_reaction`, `_apply_stratagem`.

- [ ] **Step 1: Дописать тест (smokescreen)**

Дописать в `tests/engine/phases/test_reaction_policy_seam.py`:

```python
def test_smokescreen_fires_with_default_policy():
    env = build_env()
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect == "benefit of cover"
    assert env.modelCP == 1
    assert ("model", "smokescreen", 1) in env.stratagem_used


def test_smokescreen_skipped_by_policy():
    env = build_env()
    env.unit_data[0]["Keywords"] = ["INFANTRY", "SMOKE"]
    env.modelCP = 2
    env.stratagem_used = []
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        effect = env._maybe_use_smokescreen("model", 0, "shooting")
    assert effect is None
    assert env.modelCP == 2
    assert env.stratagem_used == []
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -k smokescreen -v`
Expected: FAIL — `test_smokescreen_skipped_by_policy` (сейчас smokescreen всегда срабатывает: effect != None, CP списан) и/или нет записи в журнале (CP-расход ещё не через apply).

- [ ] **Step 3: Шов в `_maybe_use_smokescreen`**

В `core/envs/warhamEnv.py` заменить блок (`:3947-3970`):

```python
        use_it = True
        if manual:
            strat = self._prompt_yes_no("Использовать Smokescreen (1 CP)? (y/n): ")
            if strat is None:
                self.game_over = True
                return None
            use_it = strat

        if not use_it:
            return None

        if defender_side == "model":
            self.modelCP -= 1
        else:
            self.enemyCP -= 1

        self._log_rule(
            defender_side,
            defender_idx,
            "Smokescreen",
            "Триггер: выбран в качестве цели. Стоимость: -1 CP. Эффект: benefit of cover до конца атаки.",
            phase=phase,
        )
        return "benefit of cover"
```

на:

```python
        if manual:
            strat = self._prompt_yes_no("Использовать Smokescreen (1 CP)? (y/n): ")
            if strat is None:
                self.game_over = True
                return None
            use_it = strat
        else:
            use_it = self._should_use_reaction("smokescreen", defender_side, defender_idx, [defender_idx], phase, cp)

        if not use_it:
            if not manual:
                self._log_rule(
                    defender_side,
                    defender_idx,
                    "Smokescreen",
                    "Реакция пропущена политикой реакций.",
                    phase=phase,
                )
            return None

        _apply_stratagem(self, defender_side, "smokescreen", defender_idx)

        self._log_rule(
            defender_side,
            defender_idx,
            "Smokescreen",
            "Триггер: выбран в качестве цели. Стоимость: -1 CP. Эффект: benefit of cover до конца атаки.",
            phase=phase,
        )
        return "benefit of cover"
```

- [ ] **Step 4: Запустить тест — PASS**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -k smokescreen -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_policy_seam.py
git commit -m "feat(phases): Smokescreen через reaction_policy + apply (Stage 7a)"
```

---

### Task 3: шов в Overwatch + Heroic + регрессия

**Files:**
- Modify: `core/envs/warhamEnv.py` (`_resolve_overwatch`, `_resolve_heroic_intervention`)
- Test: `tests/engine/phases/test_reaction_policy_seam.py`

**Interfaces:**
- Consumes: `env._should_use_reaction`, `_apply_stratagem`.

- [ ] **Step 1: Дописать тесты (overwatch + heroic)**

Дописать в `tests/engine/phases/test_reaction_policy_seam.py`:

```python
def _setup_overwatch(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env._invalidate_target_cache("test")
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1
    assert env._collect_overwatch_candidates("model", "enemy", 0), "overwatch сетап: нет кандидатов"


def test_overwatch_fires_with_default_policy():
    env = build_env()
    _setup_overwatch(env)
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert env.modelCP == 1
    assert ("model", "overwatch", 1) in env.stratagem_used


def test_overwatch_skipped_by_policy_false():
    env = build_env()
    _setup_overwatch(env)
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert env.modelCP == 2
    assert env.stratagem_used == []


def test_overwatch_policy_receives_ctx():
    env = build_env()
    _setup_overwatch(env)
    seen = {}

    def policy(ctx):
        seen.update(ctx)
        return True

    env.reaction_policy = policy
    with env.simulation_mode():
        env._resolve_overwatch("model", "enemy", 0, "movement")
    assert seen["stratagem_id"] == "overwatch"
    assert seen["side"] == "model"
    assert seen["cp"] >= 1


def _setup_heroic(env):
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env.modelCP = 2
    env.stratagem_used = []
    env.battle_round = 1


def test_heroic_fires_with_default_policy_spends_two():
    env = build_env()
    _setup_heroic(env)
    with env.simulation_mode():
        env._resolve_heroic_intervention("model", "enemy", 0, "charge")
    assert env.modelCP == 0
    assert ("model", "heroic_intervention", 1) in env.stratagem_used


def test_heroic_skipped_by_policy_false():
    env = build_env()
    _setup_heroic(env)
    env.reaction_policy = lambda ctx: False
    with env.simulation_mode():
        env._resolve_heroic_intervention("model", "enemy", 0, "charge")
    assert env.modelCP == 2
    assert env.stratagem_used == []
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -k "overwatch or heroic" -v`
Expected: FAIL — `*_skipped_by_policy_false` (реакция всё ещё срабатывает) и/или нет записи в журнале.

- [ ] **Step 3a: Overwatch — убрать мёртвую use_it**

В `core/envs/warhamEnv.py` заменить (`:4023-4024`):

```python
        use_it = True
        chosen = candidates[0]
        if manual:
```

на:

```python
        chosen = candidates[0]
        if manual:
```

- [ ] **Step 3b: Overwatch — else-политика + model apply**

Заменить (`:4047-4053`, конец manual-блока + начало model-ветки):

```python
            chosen = int(choice) - (21 if defender_side == "model" else 11)

        if defender_side == "model":
            self.modelCP -= 1
            attacker_health = self.unit_health
```

на:

```python
            chosen = int(choice) - (21 if defender_side == "model" else 11)
        else:
            if not self._should_use_reaction("overwatch", defender_side, chosen, candidates, phase, cp):
                self._log_phase_msg(side_label, phase, "Overwatch пропущен политикой реакций.")
                return

        if defender_side == "model":
            _apply_stratagem(self, "model", "overwatch", chosen)
            attacker_health = self.unit_health
```

- [ ] **Step 3c: Overwatch — enemy apply**

Заменить (`:4056-4058`):

```python
        else:
            self.enemyCP -= 1
            attacker_health = self.enemy_health
```

на:

```python
        else:
            _apply_stratagem(self, "enemy", "overwatch", chosen)
            attacker_health = self.enemy_health
```

- [ ] **Step 3d: Heroic — убрать мёртвую use_it**

Заменить (`:4185-4187`):

```python
        use_it = True
        chosen = eligible[0]
        if manual:
```

на:

```python
        chosen = eligible[0]
        if manual:
```

- [ ] **Step 3e: Heroic — else-политика + apply (2 CP)**

Заменить (`:4206-4211`):

```python
            chosen = int(choice) - (21 if defender_side == "model" else 11)

        if defender_side == "model":
            self.modelCP -= 2
        else:
            self.enemyCP -= 2
```

на:

```python
            chosen = int(choice) - (21 if defender_side == "model" else 11)
        else:
            if not self._should_use_reaction("heroic_intervention", defender_side, chosen, eligible, phase, defender_cp):
                self._log_phase_msg(side_label, phase, "Heroic Intervention пропущен политикой реакций.")
                return

        if defender_side == "model":
            _apply_stratagem(self, "model", "heroic_intervention", chosen)
        else:
            _apply_stratagem(self, "enemy", "heroic_intervention", chosen)
```

- [ ] **Step 4: Запустить тесты Task 3 — PASS**

Run: `python -m pytest tests/engine/phases/test_reaction_policy_seam.py -v`
Expected: PASS (12 passed: 4 T1 + 2 T2 + 6 T3).

- [ ] **Step 5: Полная регрессия + ruff + импорт**

Run: `python -m pytest tests/engine/phases/ -q`
Expected: PASS (все: 33 Stage 1–6 + 12 = 45).

Run: `python -c "import core.envs.warhamEnv; print('import ok')"`
Expected: `import ok`.

Run: `python -m pytest tests/engine/test_warham_env_snapshot_restore.py tests/engine/test_snapshot_slim_regression.py tests/engine/test_phase_logging_regression.py -q`
Expected: PASS.

Run: `python -m ruff check core/engine/phases/ tests/engine/phases/`
Expected: `All checks passed!`.

Run (контроль: не добавил ruff-ошибок в движок): `python -m ruff check core/envs/warhamEnv.py 2>&1 | tail -1`
Expected: `Found 86 errors.` (как было; убедиться, что не выросло — мёртвые `use_it` удалены, новые строки чисты).

- [ ] **Step 6: Коммит**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_reaction_policy_seam.py
git commit -m "feat(phases): Overwatch+Heroic через reaction_policy + apply (Stage 7a, поведение 1:1 по умолчанию)"
```

---

## Self-Review

**Spec coverage:**
- `reaction_policy` + `_should_use_reaction` → Task 1. ✓
- heroic cp_cost=2 → Task 1. ✓
- Smokescreen шов + apply → Task 2. ✓
- Overwatch + Heroic шов + apply → Task 3. ✓
- Тесты: helper/registry (T1), smokescreen None/False (T2), overwatch None/False/ctx + heroic None/False (T3), регрессия+ruff+import (T3 Step 5). ✓
- Инвариант 1:1 при None: тесты `*_fires_with_default_policy` + регрессия пакета/движка. ✓

**Placeholder scan:** код полный; плейсхолдеров нет.

**Type consistency:** `_should_use_reaction(stratagem_id, side, chosen, candidates, phase, cp)` един везде; `_apply_stratagem(self, side, id, chosen)` совпадает со Stage 6; ctx-ключи (`side/stratagem_id/phase/chosen/candidates/cp`) совпадают в хелпере и тестах.

## Заметки по исполнению

- Удаляя мёртвую `use_it = True` в overwatch/heroic, проверь что decline в manual-ветке остаётся через ранний `return` (он есть). Smokescreen — `use_it` остаётся (читается).
- `reaction_policy` НЕ добавлять в snapshot_state.
- `heroic` гейт `defender_cp < 2` остаётся до политики; `apply` спишет 2 (после фикса реестра).
- Преэкзистинг-fail `test_command_phase_reanimation_sync_regression::test_viewer_pace_summary_handles_command_resolve` — не наш (падает и на main), в регрессию Step 5 не включён.
