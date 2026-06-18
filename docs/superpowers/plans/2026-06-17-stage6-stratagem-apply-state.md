# Stage 6 — StratagemEngine.apply + журнал (behavior-neutral) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Единая точка списания CP (`stratagem_engine.apply`) + журнал использования на env, который снапшотится; Insane Bravery (model) проводится через неё — поведение игры идентично.

**Architecture:** Новый `core/engine/phases/stratagem_engine.py` с чистой `apply(env, side, id, unit_idx)` (списывает CP + пишет `env.stratagem_used`). `command_phase` (model, Bravery) вызывает `apply` вместо инлайнового `modelCP -= 1` (ветки reward/log 1:1). `snapshot_state`/`restore_state` сохраняют `stratagem_used` + `_enemy_cp_on`/`_enemy_use_cp`.

**Tech Stack:** Python 3.12, dataclasses/StrEnum (Stage 5), pytest.

**Спека:** `docs/superpowers/specs/2026-06-17-stage6-stratagem-apply-state-design.md`.

## Global Constraints

- Платформа Windows; Python 3.12+; тесты — `python -m pytest`; ruff `py312`, line-length 120, `StrEnum`.
- Хук `ruff_fix.py` удаляет временно-неиспользуемые импорты (даже в тестах) — добавляй импорт вместе с использованием.
- `core/engine/phases/*` НЕ импортирует `core/envs/*` (apply принимает env параметром). `warhamEnv.py` импортирует `core.engine.phases.stratagem_engine` — цикла нет.
- Язык докстрингов/сообщений — русский.
- **Инвариант:** изменение CP-логики Insane Bravery — строго 1:1 (apply при ok делает `modelCP -= 1`, ветки reward/battle-shock/log сохраняются). Журнал инертен (ничего не гейтит).

## Известные факты (точные места)

- Insane Bravery (model) инлайн: `core/envs/warhamEnv.py:4332-4345` (`if self.modelCP - 1 >= 0: ... self.modelCP -= 1`). `unit_label` определён выше (`:4311`). Командная фаза в начале делает `self.modelCP += 1` (`:4306`) и `self.enemyCP += 1` (`:4307`).
- `__init__` инициализация strat: `self.enemyStrat = {...}` `:1029` — рядом ставим `self.stratagem_used`.
- `reset()` сбрасывает скаляры: `self.enemyVP = 0` `:6733` — рядом сбрасываем журнал.
- `snapshot_state` literal scalars блок `:1152-1189`; strat-dicts секция `:1228-1230`. `restore_state` `_SCALAR_KEYS` `:1251-1261`; strat-dicts `:1304-1306`.
- `_enemy_cp_on`/`_enemy_use_cp` ставятся `:4466-4467`, читаются `:5113-5114`.
- `test_snapshot_slim_regression.py` использует автономный `_SlimTestEnv` (не импортит warhamEnv) → добавление ключей в реальный snapshot его НЕ ломает.
- `Stratagem` реестр: `by_id`, `StratagemDef.cp_cost` — `core/engine/phases/stratagems.py`.

## File Structure

- Create `core/engine/phases/stratagem_engine.py` — `apply(env, side, stratagem_id, unit_idx=None) -> dict`.
- Modify `core/envs/warhamEnv.py` — журнал init (`__init__`, `reset`), snapshot/restore (+`stratagem_used`, `_enemy_cp_on`, `_enemy_use_cp`), command_phase Bravery через apply.
- Modify `core/engine/phases/__init__.py` — реэкспорт `stratagem_engine` (модуль) и `apply`.
- Create `tests/engine/phases/test_stratagem_engine.py` — apply unit-тесты.
- Create `tests/engine/phases/test_snapshot_stratagem_state.py` — snapshot round-trip журнала/enemy-cp.
- Create `tests/engine/phases/test_command_bravery_via_engine.py` — командная фаза проводит Bravery через apply (детерминированно).

---

### Task 1: `stratagem_engine.apply` + журнал на env + реэкспорт

**Files:**
- Create: `core/engine/phases/stratagem_engine.py`
- Modify: `core/envs/warhamEnv.py` (init журнала в `__init__` и `reset`)
- Modify: `core/engine/phases/__init__.py`
- Test: `tests/engine/phases/test_stratagem_engine.py`

**Interfaces:**
- Consumes: `core.engine.phases.stratagems.by_id`; env (чтение/запись `modelCP`/`enemyCP`, чтение `battle_round`, запись `stratagem_used`).
- Produces: `def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None) -> dict` → `{"ok": bool, "cp_spent": int, "reason": str | None}`.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_stratagem_engine.py`:

```python
import pytest

from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def test_apply_spends_cp_and_records_model():
    env = build_env()
    env.modelCP = 3
    env.battle_round = 2
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0)
    assert res == {"ok": True, "cp_spent": 1, "reason": None}
    assert env.modelCP == 2
    assert env.stratagem_used == [("model", "insane_bravery", 2)]


def test_apply_spends_cp_enemy_side():
    env = build_env()
    env.enemyCP = 1
    env.battle_round = 1
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "enemy", "insane_bravery", 1)
    assert res["ok"] is True
    assert env.enemyCP == 0
    assert env.stratagem_used == [("enemy", "insane_bravery", 1)]


def test_apply_no_cp_is_noop():
    env = build_env()
    env.modelCP = 0
    env.stratagem_used = []
    res = stratagem_engine.apply(env, "model", "insane_bravery", 0)
    assert res == {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    assert env.modelCP == 0
    assert env.stratagem_used == []


def test_apply_unknown_id_raises():
    env = build_env()
    env.modelCP = 3
    with pytest.raises(KeyError):
        stratagem_engine.apply(env, "model", "does_not_exist", 0)
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_stratagem_engine.py -v`
Expected: FAIL — `ImportError: cannot import name 'stratagem_engine'` (или ModuleNotFound).

- [ ] **Step 3a: Реализовать `apply`**

Создать `core/engine/phases/stratagem_engine.py`:

```python
from __future__ import annotations

from core.engine.phases.stratagems import by_id


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def apply(env, side: str, stratagem_id: str, unit_idx: int | None = None) -> dict:
    """Списать CP за стратагему и записать использование в журнал env.

    Единая точка CP-расхода. Решение «можно ли» — по наличию CP (cp >= cost).
    unit_idx пока резервируется для Stage 7 (эффект на юнита applies вызывающим).
    Возвращает {"ok": bool, "cp_spent": int, "reason": str | None}.
    """
    e = _unwrap(env)
    d = by_id(stratagem_id)
    is_model = side == "model"
    cp = int(e.modelCP if is_model else e.enemyCP)
    if cp < d.cp_cost:
        return {"ok": False, "cp_spent": 0, "reason": "not_enough_cp"}
    if is_model:
        e.modelCP = cp - d.cp_cost
    else:
        e.enemyCP = cp - d.cp_cost
    used = getattr(e, "stratagem_used", None)
    if used is None:
        used = []
        e.stratagem_used = used
    used.append((side, d.id, int(getattr(e, "battle_round", 1))))
    return {"ok": True, "cp_spent": d.cp_cost, "reason": None}
```

- [ ] **Step 3b: Инициализировать журнал на env**

В `core/envs/warhamEnv.py` после строки `self.enemyStrat = {"overwatch": -1, "smokescreen": -1}` (около `:1029`) добавить:

```python
        self.stratagem_used = []
```

В `core/envs/warhamEnv.py` в `reset()` после `self.enemyVP = 0` (около `:6733`) добавить:

```python
        self.stratagem_used = []
```

- [ ] **Step 3c: Реэкспорт в пакете**

В `core/engine/phases/__init__.py` добавить импорт модуля и `apply`:

```python
from core.engine.phases import stratagem_engine
from core.engine.phases.stratagem_engine import apply as apply_stratagem
```

Добавить в `__all__`: `"stratagem_engine", "apply_stratagem"`.

- [ ] **Step 4: Запустить тесты — PASS**

Run: `python -m pytest tests/engine/phases/test_stratagem_engine.py -v`
Expected: PASS (4 passed).

- [ ] **Step 5: Коммит**

```bash
git add core/engine/phases/stratagem_engine.py core/engine/phases/__init__.py core/envs/warhamEnv.py tests/engine/phases/test_stratagem_engine.py
git commit -m "feat(phases): stratagem_engine.apply (единое списание CP + журнал) + журнал на env (Stage 6)"
```

---

### Task 2: snapshot/restore журнала и enemy-cp-полей

**Files:**
- Modify: `core/envs/warhamEnv.py` (`snapshot_state`, `restore_state`)
- Test: `tests/engine/phases/test_snapshot_stratagem_state.py`

**Interfaces:**
- Consumes: `env.snapshot_state()`/`restore_state()`; `stratagem_engine.apply`.
- Produces: snapshot содержит `stratagem_used` (list of 3-tuples), `_enemy_cp_on`, `_enemy_use_cp`; restore их восстанавливает.

- [ ] **Step 1: Написать падающий тест**

Создать `tests/engine/phases/test_snapshot_stratagem_state.py`:

```python
from core.engine.phases import stratagem_engine
from tests.engine.phases._helpers import build_env


def test_snapshot_restore_preserves_stratagem_journal_and_enemy_cp():
    env = build_env()
    env.modelCP = 3
    env.stratagem_used = []
    env._enemy_cp_on = 1
    env._enemy_use_cp = 2

    snap = env.snapshot_state()

    # мутации после снимка
    stratagem_engine.apply(env, "model", "insane_bravery", 0)
    env._enemy_cp_on = 9
    env._enemy_use_cp = 0
    assert env.stratagem_used == [("model", "insane_bravery", env.battle_round)]

    env.restore_state(snap)

    assert env.stratagem_used == []
    assert env.modelCP == 3
    assert env._enemy_cp_on == 1
    assert env._enemy_use_cp == 2
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_snapshot_stratagem_state.py -v`
Expected: FAIL — `stratagem_used` не восстановлен (`assert [...] == []`), либо `_enemy_cp_on` mismatch.

- [ ] **Step 3a: snapshot_state — добавить ключи**

В `core/envs/warhamEnv.py`, в literal-словаре `snap` (блок скаляров `:1152-1189`), после строки `"modelUpdates": _ga(_self, "modelUpdates", ""),` добавить:

```python
            "_enemy_cp_on": _ga(_self, "_enemy_cp_on", None),
            "_enemy_use_cp": _ga(_self, "_enemy_use_cp", None),
```

В `snapshot_state`, после секции strat-dicts (после блока, кладущего `modelStrat`/`enemyStrat`, около `:1230`), добавить:

```python
        # --- журнал стратагем (list of (side, id, round)) ---
        _su = _ga(_self, "stratagem_used", None)
        snap["stratagem_used"] = [tuple(x) for x in _su] if _su is not None else []
```

- [ ] **Step 3b: restore_state — восстановить ключи**

В `core/envs/warhamEnv.py`, в `_SCALAR_KEYS` (`:1251-1261`), добавить в кортеж два имени:

```python
            "_enemy_cp_on", "_enemy_use_cp",
```

В `restore_state`, после секции strat-dicts (после блока `for _k in ("modelStrat", "enemyStrat"): ...`, около `:1306`), добавить:

```python
        if "stratagem_used" in snapshot:
            _self.stratagem_used = [tuple(x) for x in snapshot["stratagem_used"]]
```

- [ ] **Step 4: Запустить тест — PASS**

Run: `python -m pytest tests/engine/phases/test_snapshot_stratagem_state.py -v`
Expected: PASS (1 passed).

- [ ] **Step 5: Прогнать smoke snapshot-регрессии движка**

Run: `python -m pytest tests/engine/test_warham_env_snapshot_restore.py tests/engine/test_snapshot_slim_regression.py -q`
Expected: PASS (автономный `_SlimTestEnv` не зависит от новых ключей).

- [ ] **Step 6: Коммит**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_snapshot_stratagem_state.py
git commit -m "feat(phases): snapshot/restore журнала стратагем + _enemy_cp_on/_enemy_use_cp (Stage 6)"
```

---

### Task 3: command_phase (model Bravery) через `apply` + golden-trace

**Files:**
- Modify: `core/envs/warhamEnv.py` (`command_phase` model branch)
- Test: `tests/engine/phases/test_command_bravery_via_engine.py`

**Interfaces:**
- Consumes: `stratagem_engine.apply`; `env.command_phase`, `snapshot_state`/`restore_state`, `simulation_mode`.
- Produces: Insane Bravery проводится через `apply`; поведение идентично; на применённую Bravery в `stratagem_used` появляется запись.

- [ ] **Step 1: Написать тест (детерминированная Bravery)**

Создать `tests/engine/phases/test_command_bravery_via_engine.py`:

```python
from tests.engine.phases._helpers import build_env


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": use_cp, "cp_on": cp_on}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def test_command_bravery_routed_through_engine_records_journal():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)

    # Юнит 0 ниже половины состава + невозможный Ld(13): 2D6<=12 → battle-shock всегда провален.
    env.unit_data[0]["Ld"] = 13
    env.unit_health[0] = 1.0
    env.modelCP = 2
    start_cp = env.modelCP

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            battle_shock, _reward = env.command_phase("model", action=_action(1, 0, n))
            # Bravery спасла юнит 0
            assert battle_shock[0] is False
            # запись в журнале появилась
            assert ("model", "insane_bravery", env.battle_round) in env.stratagem_used
            # нетто CP: +1 (командование) -1 (bravery) = без изменений
            assert env.modelCP == start_cp
        finally:
            env.restore_state(snap)

    # restore вернул журнал и CP
    assert env.stratagem_used == []
    assert env.modelCP == start_cp


def test_command_no_bravery_when_not_requested():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    n = len(env.unit_health)
    env.unit_data[0]["Ld"] = 13
    env.unit_health[0] = 1.0
    env.modelCP = 2

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            battle_shock, _reward = env.command_phase("model", action=_action(0, 0, n))
            # Bravery не запрошена → юнит 0 в battle-shock, журнал пуст
            assert battle_shock[0] is True
            assert env.stratagem_used == []
        finally:
            env.restore_state(snap)
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_command_bravery_via_engine.py -v`
Expected: FAIL — `stratagem_used` пуст (Bravery ещё не проведена через `apply`, журнал не пишется).

- [ ] **Step 3: Подключить apply в command_phase**

В `core/envs/warhamEnv.py` добавить импорт рядом с прочими top-level импортами движка (вместе с использованием ниже):

```python
from core.engine.phases.stratagem_engine import apply as _apply_stratagem
```

Заменить блок `:4332-4345`:

```python
                        if action and action.get("use_cp") == 1 and action.get("cp_on") == i:
                            if self.modelCP - 1 >= 0:
                                battle_shock[i] = False
                                reward_delta += reward_cfg.COMMAND_INSANE_BRAVERY_REWARD
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery bonus=+{reward_cfg.COMMAND_INSANE_BRAVERY_REWARD:.3f}",
                                )
                                self.modelCP -= 1
                                if self.trunc is False:
                                    self._log(f"{unit_label}: применена Insane Bravery (-1 CP), тест пройден.")
                            else:
                                reward_delta -= reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery penalty=-{reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY:.3f} "
                                    "(нет CP)",
                                )
```

на:

```python
                        if action and action.get("use_cp") == 1 and action.get("cp_on") == i:
                            _bravery = _apply_stratagem(self, "model", "insane_bravery", i)
                            if _bravery["ok"]:
                                battle_shock[i] = False
                                reward_delta += reward_cfg.COMMAND_INSANE_BRAVERY_REWARD
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery bonus=+{reward_cfg.COMMAND_INSANE_BRAVERY_REWARD:.3f}",
                                )
                                if self.trunc is False:
                                    self._log(f"{unit_label}: применена Insane Bravery (-1 CP), тест пройден.")
                            else:
                                reward_delta -= reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY
                                self._log_reward_unit(
                                    "model",
                                    i + 21,
                                    i,
                                    "Reward (командование): "
                                    f"Insane Bravery penalty=-{reward_cfg.COMMAND_INSANE_BRAVERY_PENALTY:.3f} "
                                    "(нет CP)",
                                )
```

(Условие `self.modelCP - 1 >= 0` ⟺ `_bravery["ok"]` при cp_cost=1; `apply` делает `modelCP -= 1` при ok. Ветки reward/log/battle_shock — без изменений.)

- [ ] **Step 4: Запустить тест Task 3 — PASS**

Run: `python -m pytest tests/engine/phases/test_command_bravery_via_engine.py -v`
Expected: PASS (2 passed).

- [ ] **Step 5: Полная регрессия + ruff**

Run: `python -m pytest tests/engine/phases/ -q`
Expected: PASS (все: 26 Stage 1–5 + 4 + 1 + 2 = 33).

Run: `python -m pytest tests/engine/test_warham_env_snapshot_restore.py tests/engine/test_command_phase_reanimation_sync_regression.py tests/engine/test_snapshot_slim_regression.py tests/engine/test_phase_logging_regression.py -q`
Expected: PASS (движок/командная фаза не регрессировали).

Run: `python -m ruff check core/engine/phases/ core/envs/warhamEnv.py tests/engine/phases/`
Expected: `All checks passed!`.

- [ ] **Step 6: Коммит**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_command_bravery_via_engine.py
git commit -m "feat(phases): command_phase проводит Insane Bravery через stratagem_engine.apply (Stage 6, поведение 1:1)"
```

---

## Self-Review

**Spec coverage:**
- `apply` (списание CP + журнал, ok/no-cp/unknown-id) → Task 1. ✓
- журнал на env (`__init__`/`reset`) → Task 1. ✓
- snapshot/restore `stratagem_used` + `_enemy_cp_on`/`_enemy_use_cp` → Task 2. ✓
- command_phase Bravery через apply, поведение 1:1 → Task 3. ✓
- реэкспорт → Task 1. ✓
- Тесты: apply (T1), snapshot round-trip (T2), детерминированная Bravery + журнал + «без запроса нет Bravery» (T3), регрессии движка/пакета/ruff (T3 Step 5). ✓

**Placeholder scan:** код полный во всех шагах; плейсхолдеров нет.

**Type consistency:** `apply(env, side, stratagem_id, unit_idx=None) -> dict` с ключами `ok/cp_spent/reason` един во всех тасках и тестах; журнал — список 3-кортежей `(side, id, battle_round)` везде; `_apply_stratagem` = реэкспорт `apply`.

## Заметки по исполнению

- Импорт `_apply_stratagem` в `warhamEnv.py` добавлять вместе с использованием (хук срежет неиспользуемый). Проверить отсутствие циклического импорта при старте (`python -c "import core.envs.warhamEnv"`).
- `command_phase` в начале даёт `+1 CP` модели — поэтому в тесте Task 3 нетто CP после одной Bravery = без изменений (start_cp).
- Если ruff предложит StrEnum/прочее в новых файлах — применить безопасные фиксы (`ruff check --fix`).
