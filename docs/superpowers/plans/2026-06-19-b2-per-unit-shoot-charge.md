# B2 Per-unit shoot/charge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заменить одиночные action-головы `shoot`/`charge` на per-unit `shoot_num_i`/`charge_num_i`, чтобы политика выбирала цели по юниту (убрать lossy-override flat-контракта). Жёсткий разрыв контракта.

**Architecture:** Контракт (`action_contract.ordered_action_keys`) добавляет `shoot_num_i`/`charge_num_i` и убирает `shoot`/`charge`. Env строит per-unit головы и маски; потребление в shooting/charge-фазах читает per-unit ключи. DQN-маски обобщаются по ключам. AZ/GMZ/PPO generic. Бамп `ENV_RULESET_VERSION` отклоняет старые чекпойнты.

**Tech Stack:** Python 3.12, gymnasium spaces, PyTorch, pytest.

**Spec:** `docs/superpowers/specs/2026-06-19-b2-per-unit-shoot-charge-design.md`

**Семантика голов (сохраняем):** `shoot_num_i` = **локальный ранг** в `get_shoot_targets_for_unit(side,i)` (`idOfE = valid[raw]`); `charge_num_i` = **глобальный индекс врага** (`idOfE = action[charge_num_i]`). Маски: shoot — по рангам `[0,len(targets_i))`; charge — по enemy-id из `get_charge_targets_for_unit(i)`.

---

## File Structure
- `core/models/action_contract.py` — ключи контракта.
- `core/envs/warhamEnv.py` — action_space, маски, потребление, `_action_signature`.
- `core/models/utils.py` — DQN select_action/маски.
- `core/engine/phases/legacy_compiler.py` — default/compile action_dict.
- `core/engine/phases/option_generator.py` — legacy_patch per-unit (shoot уже rank; charge добавить `_num`).
- `play.py`, `eval.py` — потребители action_dict.
- Tests: `tests/models/test_action_contract.py`, `tests/engine/phases/test_per_unit_shoot_charge.py`.

---

## Task 1: Контракт — per-unit ключи

**Files:**
- Modify: `core/models/action_contract.py:10-17`
- Test: `tests/models/test_action_contract.py`

- [ ] **Step 1: Failing test** — `tests/models/test_action_contract.py`:

```python
from core.models.action_contract import BASE_ACTION_HEADS, ordered_action_keys


def test_base_heads_drop_single_shoot_charge():
    assert "shoot" not in BASE_ACTION_HEADS
    assert "charge" not in BASE_ACTION_HEADS


def test_ordered_keys_have_per_unit_shoot_charge():
    keys = ordered_action_keys(2)
    assert keys == [
        "move", "attack", "use_cp", "cp_on",
        "move_num_0", "move_num_1",
        "shoot_num_0", "shoot_num_1",
        "charge_num_0", "charge_num_1",
    ]
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/models/test_action_contract.py -q`. Expected: FAIL.

- [ ] **Step 3: Implement** — `core/models/action_contract.py`:

```python
BASE_ACTION_HEADS = ["move", "attack", "use_cp", "cp_on"]


def ordered_action_keys(len_model: int) -> list[str]:
    n = int(len_model)
    keys = list(BASE_ACTION_HEADS)
    keys += [f"move_num_{i}" for i in range(n)]
    keys += [f"shoot_num_{i}" for i in range(n)]
    keys += [f"charge_num_{i}" for i in range(n)]
    return keys
```

- [ ] **Step 4: Run, verify passes** — `pytest tests/models/test_action_contract.py -q`. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/models/action_contract.py tests/models/test_action_contract.py
git commit -m "feat(b2): контракт per-unit shoot_num_i/charge_num_i"
```

---

## Task 2: Env action_space + per-unit маски

**Files:**
- Modify: `core/envs/warhamEnv.py:982-984` (action_space), `:1716-1738` (маски)
- Test: `tests/engine/phases/test_per_unit_shoot_charge.py`

- [ ] **Step 1: Failing test** — `tests/engine/phases/test_per_unit_shoot_charge.py`:

```python
from tests.engine.phases._helpers import build_env


def test_action_space_has_per_unit_heads():
    env = build_env()
    sp = env.action_space.spaces
    assert "shoot" not in sp and "charge" not in sp
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    for i in range(n_model):
        assert sp[f"shoot_num_{i}"].n == n_enemy
        assert sp[f"charge_num_{i}"].n == n_enemy


def test_masks_have_per_unit_shoot_charge():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    masks = env.build_action_masks("model")  # см. фактическое имя метода масок
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    for i in range(n_model):
        assert masks[f"shoot_num_{i}"].shape[0] == n_enemy
        assert masks[f"charge_num_{i}"].shape[0] == n_enemy
```

> NB: подставить реальное имя метода построения масок (искать `masks["attack"] =` в warhamEnv; метод, возвращающий dict масок).

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_per_unit_shoot_charge.py -q`. Expected: FAIL (KeyError shoot_num_0).

- [ ] **Step 3a: action_space** — в конструкторе (`core/envs/warhamEnv.py` ~982) убрать строки `'shoot': spaces.Discrete(len(enemy))` и `'charge': spaces.Discrete(len(enemy))` из `action_spaces`. В цикле `for i in range(len(model)):` (где добавляется `move_num_i`) дополнительно:

```python
            action_spaces[f"shoot_num_{i}"] = spaces.Discrete(len(enemy))
            action_spaces[f"charge_num_{i}"] = spaces.Discrete(len(enemy))
```

- [ ] **Step 3b: маски** — заменить блок `masks["shoot"]`/`masks["charge"]` (warhamEnv ~1716-1738) на per-unit:

```python
        # shoot_num_i: ранг в легальных целях юнита i (idOfE = valid[raw]).
        for u_idx in range(len(unit_health)):
            key = f"shoot_num_{u_idx}"
            if key not in spaces:
                continue
            n = int(spaces[key].n)
            m = np.zeros(n, dtype=bool)
            if u_idx in can_shoot_units:
                k = len(self.get_shoot_targets_for_unit(side, u_idx))
                if k > 0:
                    m[: min(n, k)] = True
            if not m.any():
                m[0] = True
            masks[key] = m

        # charge_num_i: глобальный enemy-index целей чарджа юнита i.
        for u_idx in range(len(unit_health)):
            key = f"charge_num_{u_idx}"
            if key not in spaces:
                continue
            n = int(spaces[key].n)
            m = np.zeros(n, dtype=bool)
            if u_idx in can_charge_units:
                for t_idx in self.get_charge_targets_for_unit(side, u_idx):
                    if 0 <= int(t_idx) < n:
                        m[int(t_idx)] = True
            if not m.any():
                m[0] = True
            masks[key] = m
```

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_per_unit_shoot_charge.py -q`. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_per_unit_shoot_charge.py
git commit -m "feat(b2): env per-unit shoot/charge action_space + маски"
```

---

## Task 3: Потребление shoot (flat) per-unit

**Files:**
- Modify: `core/envs/warhamEnv.py:5675` (model), `:5968` (enemy)
- Test: `tests/engine/phases/test_per_unit_shoot_charge.py`

- [ ] **Step 1: Failing test** — добавить в `test_per_unit_shoot_charge.py`:

```python
def test_flat_shoot_uses_per_unit_head(monkeypatch):
    import core.envs.warhamEnv as warham_mod

    hits = []

    def fake_attack(ah, w, ad, dh, dd, *a, **k):
        hits.append(dd.get("Name"))
        return [0.0], dh

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    # оба model-юнита могут стрелять; разные shoot_num → разные цели (ранг 0 и 1)
    env.unit_coords[0] = [0.0, 0.0]
    env.unit_coords[1] = [0.0, 0.0]
    env.enemy_coords[0] = [1.0, 1.0]
    env.enemy_coords[1] = [1.0, 1.0]
    action = {"shoot_num_0": 0, "shoot_num_1": 1}
    env.shooting_phase("model", action=action)
    # цель юнита 0 (ранг0) и юнита 1 (ранг1) различаются, если у юнитов ≥2 легальных цели
    assert len(hits) >= 1  # выстрелы произошли по per-unit головам (без KeyError на 'shoot')
```

- [ ] **Step 2: Run, verify fails** — `pytest tests/engine/phases/test_per_unit_shoot_charge.py::test_flat_shoot_uses_per_unit_head -q`. Expected: FAIL (KeyError 'shoot').

- [ ] **Step 3: Implement** — `core/envs/warhamEnv.py`:

Строка 5675 (model shoot):

```python
                    raw = int(decide_shoot(i)) if decide_shoot is not None else int(action.get(f"shoot_num_{i}", 0))
```

Строка 5968 (enemy shoot):

```python
                    raw = int(action.get(f"shoot_num_{i}", 0)) if isinstance(action, dict) else 0
```

- [ ] **Step 4: Run, verify passes** — `pytest tests/engine/phases/test_per_unit_shoot_charge.py -q`. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_per_unit_shoot_charge.py
git commit -m "feat(b2): потребление shoot per-unit (flat)"
```

---

## Task 4: Потребление charge (flat) per-unit

**Files:**
- Modify: `core/envs/warhamEnv.py:6362` (model), `:6519`, `:6591` (enemy)
- Test: `tests/engine/phases/test_per_unit_shoot_charge.py`

- [ ] **Step 1: Failing test**:

```python
def test_flat_charge_uses_per_unit_head():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    action = {"attack": 1, "charge_num_0": 0, "charge_num_1": 0}
    # не должно падать с KeyError 'charge'; charge_phase читает per-unit
    env.charge_phase("model", action=action)
    assert True
```

- [ ] **Step 2: Run, verify fails** — Expected: FAIL (KeyError 'charge').

- [ ] **Step 3: Implement** — заменить чтения:

`:6362` (model): `idOfE = int(_charge_target) if decide_charge is not None else int(action.get(f"charge_num_{i}", 0))`

`:6519` (enemy): `idOfM = int(action.get(f"charge_num_{i}", 0))`

`:6591` (enemy heur log): `action.get('charge', 0)` → `action.get(f'charge_num_{i}', 0)`

> NB: подтвердить, что переменная юнита в каждой ветке называется `i` (искать enclosing loop); если иначе — использовать корректный индекс.

- [ ] **Step 4: Run, verify passes** — Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_per_unit_shoot_charge.py
git commit -m "feat(b2): потребление charge per-unit (flat)"
```

---

## Task 5: `_action_signature` + прочие одиночные чтения

**Files:**
- Modify: `core/envs/warhamEnv.py:1780-1790`

- [ ] **Step 1: Найти callers** — `grep -n "_action_signature" core/envs/warhamEnv.py`. Это сигнатура для дедупа/логов.

- [ ] **Step 2: Implement** — убрать `shoot`/`charge` из сигнатуры (они больше не одиночные):

```python
    def _action_signature(self, action) -> tuple[int, int, int, int]:
        if not isinstance(action, dict):
            return (-1, -1, -1, -1)
        return (
            self._coerce_int(action.get("move", -1), default=-1),
            self._coerce_int(action.get("attack", -1), default=-1),
            self._coerce_int(action.get("use_cp", -1), default=-1),
            self._coerce_int(action.get("cp_on", -1), default=-1),
        )
```

- [ ] **Step 3: Verify** — `grep -nE "action\[.shoot.\]|action\.get\(.shoot|action\[.charge.\]|action\.get\(.charge" core/envs/warhamEnv.py`. Expected: только per-unit `shoot_num`/`charge_num` чтения (нет одиночных).

- [ ] **Step 4: Commit**

```bash
git add core/envs/warhamEnv.py
git commit -m "feat(b2): _action_signature без одиночных shoot/charge"
```

---

## Task 6: DQN select_action / маски по ключам

**Files:**
- Modify: `core/models/utils.py:135-205`
- Test: `tests/models/test_action_contract.py`

- [ ] **Step 1: Прочитать** `select_action` и `build_shoot_action_mask` целиком (utils.py:135-205); понять, как `head_idx==2` и `sampled_action["shoot"]`/`["charge"]` используются.

- [ ] **Step 2: Failing test** — характеризующий, что DQN использует per-unit ключи (точная форма зависит от текущего API; написать после чтения Step 1, проверяя что нет `sampled_action["shoot"]` и маски применяются к `shoot_num_*` головам).

- [ ] **Step 3: Implement** — обобщить:
  - убрать `if head_idx == 2`; применять маску к голове по её ключу `ordered_action_keys(len_model)[head_idx]`, если ключ начинается с `shoot_num_`/`charge_num_` — брать соответствующую per-unit маску из `env`/переданного dict масок;
  - `sampled_action["shoot"]`/`["charge"]` — заменить на per-unit чтение из `sampled_action[f"shoot_num_{i}"]` по всем юнитам (или убрать, если использовалось лишь для маск-фильтра).

> NB: точный код — после Step 1 (зависит от текущей реализации select_action; сохранить поведение DQN, обобщив на per-unit маски по ключам).

- [ ] **Step 4: Run** — `pytest tests/models/ -q`. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/models/utils.py tests/models/test_action_contract.py
git commit -m "feat(b2): DQN маски per-unit shoot/charge по ключам"
```

---

## Task 7: legacy_compiler + option_generator per-unit

**Files:**
- Modify: `core/engine/phases/legacy_compiler.py:6-36`, `core/engine/phases/option_generator.py:34-35,102`
- Test: `tests/engine/phases/test_per_unit_shoot_charge.py`

- [ ] **Step 1: Failing test** — два shooting-окна разных юнитов компилируются без потери:

```python
from core.engine.phases.legacy_compiler import default_action_dict, compile_options_to_action_dict
from core.engine.phases.types import ActionOption, ActionKind


def test_compile_keeps_per_unit_shoot():
    opts = [
        ActionOption(kind=ActionKind.SHOOT, unit_idx=0, legacy_patch={"shoot_num_0": 2}),
        ActionOption(kind=ActionKind.SHOOT, unit_idx=1, legacy_patch={"shoot_num_1": 1}),
    ]
    a = compile_options_to_action_dict(opts, len_model=2)
    assert a["shoot_num_0"] == 2 and a["shoot_num_1"] == 1  # нет lossy-override


def test_default_action_dict_per_unit():
    a = default_action_dict(2)
    assert "shoot" not in a and "charge" not in a
    assert a["shoot_num_0"] == 0 and a["charge_num_1"] == 0
```

- [ ] **Step 2: Run, verify fails** — Expected: FAIL.

- [ ] **Step 3a: legacy_compiler** — `default_action_dict`:

```python
def default_action_dict(len_model: int) -> dict[str, int]:
    n = int(len_model)
    action: dict[str, int] = {"move": 4, "attack": 1, "use_cp": 0, "cp_on": 0}
    for i in range(n):
        action[f"move_num_{i}"] = 0
        action[f"shoot_num_{i}"] = 0
        action[f"charge_num_{i}"] = 0
    return action
```

`compile_options_to_action_dict` — без изменения логики (legacy_patch теперь per-unit ключи); обновить docstring (убрать «одна голова shoot/charge на ход → lossy»).

- [ ] **Step 3b: option_generator** — `shooting_options_for_unit` (line 35): `legacy_patch={"shoot": int(rank)}` → `legacy_patch={f"shoot_num_{int(unit_idx)}": int(rank)}`. `charge_options_for_unit` (line 102): `legacy_patch={"charge": int(target_global), "attack": 1}` → `legacy_patch={f"charge_num_{int(unit_idx)}": int(target_global), "attack": 1}`.

- [ ] **Step 4: Run** — `pytest tests/engine/phases/ -q`. Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/engine/phases/legacy_compiler.py core/engine/phases/option_generator.py tests/engine/phases/test_per_unit_shoot_charge.py
git commit -m "feat(b2): legacy_compiler/option_generator per-unit (нет lossy)"
```

---

## Task 8: Потребители action_dict + бамп версии + smoke/parity

**Files:**
- Modify: `play.py`, `eval.py` (где строится/читается `action["shoot"]`/`["charge"]`), `core/envs/warhamEnv.py` (`ENV_RULESET_VERSION`)

- [ ] **Step 1: Найти потребителей** — `grep -rnE "action\[.shoot.\]|action\.get\(.shoot|\"shoot\":|action\[.charge.\]|\"charge\":" play.py eval.py core/ | grep -v _num`. Для каждого, строящего action_dict, перейти на per-unit ключи или `default_action_dict`; читающие одиночный shoot/charge — на per-unit по нужному юниту. Viewer-строки (имена фаз) — НЕ трогать.

- [ ] **Step 2: Бамп версии** — `core/envs/warhamEnv.py`: `ENV_RULESET_VERSION = os.getenv("ENV_RULESET_VERSION", "only_war_v2")`.

- [ ] **Step 3: Тест mismatch** — `tests/engine/test_agent_registry_contract.py` или новый: контракт с per-unit головами даёт другой `action_space_signature`, `compatible_contracts(old, new)` → `(False, "action_space_signature mismatch")`.

```python
from core.engine.agent_registry import make_env_contract, compatible_contracts


def test_contract_action_signature_changed():
    old = make_env_contract(n_observations=10, n_actions=[5, 2, 5, 2], mission_name="only_war")
    new = make_env_contract(n_observations=10, n_actions=[5, 2, 5, 2, 4, 4, 6, 6, 6, 6], mission_name="only_war")
    ok, reason = compatible_contracts(old, new)
    assert ok is False
```

- [ ] **Step 4: Регресс** — `pytest tests/engine/phases/ tests/models/ -q`. Expected: всё зелёное.

- [ ] **Step 5: Smoke** — AZ: `TRAIN_ALGO=alphazero_tree TRAIN_EPISODES_OVERRIDE=6 AZ_NUM_ACTORS=2 AZ_MCTS_SIMULATIONS=8 python train.py` — без краша. DQN: `TRAIN_ALGO=dqn TRAIN_EPISODES_OVERRIDE=6 python train.py` — без краша. Parity: `python tools/windowed_parity_winrate.py --episodes 50 --seed 1000` (новый контракт; windowed↔legacy).

- [ ] **Step 6: Commit**

```bash
git add play.py eval.py core/envs/warhamEnv.py tests/engine/
git commit -m "feat(b2): потребители action_dict per-unit + бамп ENV_RULESET_VERSION + smoke"
```

---

## Self-Review

**Spec coverage:** §2 контракт→T1; §3 env/маски/потребление→T2-4; §4 DQN→T6 (AZ/GMZ/PPO generic — без задач, проверяется smoke T8); §5 windowed/legacy→T7; §6 потребители→T8; §7 миграция→T8; §8 тесты→распределены; §9 инкремент→T1-8.

**Открытые места для исполнителя (требуют чтения перед кодом):**
- Имя метода построения масок (T2 Step 1 NB) — искать `masks["attack"] =`.
- Переменная индекса юнита в charge-ветках (T4 NB) — подтвердить `i`.
- DQN `select_action` точный код (T6) — зависит от текущей реализации; обобщить, не сломав поведение.
- Перечень потребителей action_dict (T8 Step 1) — грепом, не по памяти.

**Риск-напоминание:** не полагаться на позицию головы (DQN `head_idx==2`); все индексы — через `ordered_action_keys`. shoot=ранг, charge=enemy-id (не перепутать в масках/потреблении).
