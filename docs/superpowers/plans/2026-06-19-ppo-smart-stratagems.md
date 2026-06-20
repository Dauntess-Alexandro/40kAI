# PPO Smart Stratagems Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Дать PPO «умный» выбор всех 7 стратагем через тот же `reaction_policy` value-gate, что у DQN/AZ, с честным critic-V как источником V(s).

**Architecture:** Не трогаем движок и action-space. Добавляем PPO `infer_with_value` (critic V), модуль `ppo_stratagem_bridge.py` (side-generic install + critic-V + greedy fight-plan) и хуки в train.py/eval.py. Seam `_simulate_reaction_branch` подхватывает PPO автоматически (duck-typing уже на месте).

**Tech Stack:** Python 3.12+, PyTorch, pytest, Windows. Спека: `docs/superpowers/specs/2026-06-19-ppo-smart-stratagems-design.md`.

## Global Constraints

- Платформа Windows; язык логов/сообщений — русский (что случилось + где + что делать).
- Движок (`core/engine/*`, `core/envs/warhamEnv.py` фазовые методы, `_simulate_reaction_branch`) и action-space (`action_contract.py`) **не менять**.
- DQN/AZ-код **не трогать** (`infer_with_value` у PPO независим; seam-duck-typing общий).
- `ruff_fix.py` PostToolUse срезает временно-неиспользуемые импорты — импорт добавлять вместе с использованием.
- `guard_paths.py` блокирует правку `runtime/logs/LOGS_FOR_AGENTS_*.md` — не редактировать вручную.
- V(s) для PPO = честный critic (`ActorCriticMultiHead._value_from_features`), **mask-независим**.
- Флаг `PPO_REACTION_VALUE_POLICY` дефолт `1`; install-API side-generic (`net_by_side` dict).
- Fight-plan `eps=1e-3`; реакции `eps=0` (дефолт `make_stratagem_value_policy`).
- Частые коммиты: один коммит на задачу после зелёных тестов.

---

### Task 1: `ActorCriticMultiHead.infer_with_value`

**Files:**
- Modify: `core/models/PPO.py` (добавить метод в класс `ActorCriticMultiHead`, после `act`, ~строка 187)
- Test: `tests/models/test_ppo_infer_with_value.py` (создать)

**Interfaces:**
- Consumes: `ActorCriticMultiHead.forward(obs) -> (logits_list, value)`, `_apply_action_mask(logits, mask)` (оба уже в `PPO.py`).
- Produces: `ActorCriticMultiHead.infer_with_value(obs, masks_by_head=None) -> (probs: list[Tensor], V: Tensor[(B,)])`. V — критик, mask-независим. Метод нужен seam'у `_simulate_reaction_branch` (duck-typing `hasattr(net, "infer_with_value")`).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_ppo_infer_with_value.py
"""ActorCriticMultiHead.infer_with_value: честный critic V, mask-независим."""

import numpy as np
import torch

from core.models.action_contract import action_sizes_from_env
from core.models.PPO import ActorCriticMultiHead
from tests.engine.phases._helpers import build_env


def _tiny_ac(env, *, n_value_ensemble=1):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    return ActorCriticMultiHead(obs_dim, sizes, hidden_size=32, num_layers=1, n_value_ensemble=n_value_ensemble)


def test_infer_with_value_shape_and_finite():
    env = build_env()
    net = _tiny_ac(env)
    net.eval()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(2, obs_dim)
    probs, v = net.infer_with_value(obs)
    assert len(probs) > 0
    assert v.shape == (2,)
    assert torch.isfinite(v).all()


def test_value_is_mask_independent():
    env = build_env()
    net = _tiny_ac(env)
    net.eval()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(1, obs_dim)
    logits_list, _ = net.forward(obs)
    masks = []
    for idx, lg in enumerate(logits_list):
        m = torch.ones(1, lg.shape[1], dtype=torch.bool)
        if idx == 0:
            m[0, 1:] = False  # сильно ограничиваем head 0
        masks.append(m)
    _, v_masked = net.infer_with_value(obs, masks_by_head=masks)
    _, v_plain = net.infer_with_value(obs, masks_by_head=None)
    assert abs(float(v_masked[0]) - float(v_plain[0])) < 1e-6  # V не зависит от масок


def test_mask_affects_probs():
    env = build_env()
    net = _tiny_ac(env)
    net.eval()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(1, obs_dim)
    logits_list, _ = net.forward(obs)
    masks = []
    for idx, lg in enumerate(logits_list):
        m = torch.ones(1, lg.shape[1], dtype=torch.bool)
        if idx == 0 and lg.shape[1] > 1:
            m[0, 1:] = False
        masks.append(m)
    probs, _ = net.infer_with_value(obs, masks_by_head=masks)
    if probs[0].shape[1] > 1:
        assert float(probs[0][0, 0]) > 0.999  # вся масса на единственный legal


def test_ensemble_value_smoke():
    env = build_env()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(1, obs_dim)
    for n_ens in (1, 3):
        net = _tiny_ac(env, n_value_ensemble=n_ens)
        net.eval()
        _, v = net.infer_with_value(obs)
        assert v.shape == (1,) and torch.isfinite(v).all()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_ppo_infer_with_value.py -v`
Expected: FAIL — `AttributeError: 'ActorCriticMultiHead' object has no attribute 'infer_with_value'`.

- [ ] **Step 3: Write minimal implementation**

В `core/models/PPO.py`, в классе `ActorCriticMultiHead`, после метода `act` (после строки 187) добавить:

```python
    @torch.no_grad()
    def infer_with_value(self, obs, masks_by_head=None):
        """Как act, но возвращает (probs, V). V — честный critic, mask-независим.

        Нужно seam'у env._simulate_reaction_branch (duck-typing hasattr infer_with_value):
        он зовёт net.infer_with_value(obs, masks_by_head=...) и ждёт (probs, value).
        Маски влияют только на probs; critic V их игнорирует.
        """
        logits_list, value = self.forward(obs)
        probs = []
        for idx, logits in enumerate(logits_list):
            mask = masks_by_head[idx] if (masks_by_head is not None and idx < len(masks_by_head)) else None
            masked = _apply_action_mask(logits, mask)
            probs.append(torch.softmax(masked, dim=1))
        return probs, value
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_ppo_infer_with_value.py -v`
Expected: PASS (4 теста).

- [ ] **Step 5: Commit**

```bash
git add core/models/PPO.py tests/models/test_ppo_infer_with_value.py
git commit -m "feat(ppo): infer_with_value — честный critic V для value-gate"
```

---

### Task 2: `ppo_stratagem_bridge.py` — флаг, install (side-generic), ppo_value

**Files:**
- Create: `core/models/ppo_stratagem_bridge.py`
- Test: `tests/models/test_ppo_stratagem_bridge.py` (создать; fight-plan тесты добавит Task 3)

**Interfaces:**
- Consumes: `ActorCriticMultiHead.infer_with_value` (Task 1); `make_stratagem_value_policy(net_by_side, *, device)` из `core/models/reaction_value_policy.py`; `unwrap_env` из `core/models/utils.py`.
- Produces:
  - `ppo_reaction_value_policy_enabled(default="1") -> bool`
  - `install_ppo_stratagem_policy(env, device, net_by_side: dict) -> None` — ставит `env.reaction_policy` + `env._reaction_net_by_side = dict(net_by_side)`.
  - `ppo_value(env, ac_net, device, side: str) -> float` — critic V (без масок).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_ppo_stratagem_bridge.py
"""ppo_stratagem_bridge: install (side-generic) + critic-V."""

import torch

from core.models.ppo_stratagem_bridge import (
    install_ppo_stratagem_policy,
    ppo_reaction_value_policy_enabled,
    ppo_value,
)
from tests.engine.phases._helpers import build_env


class _ConstNet:
    """Возвращает фиксированный V на каждый infer_with_value."""

    def __init__(self, value):
        self._value = float(value)

    def infer_with_value(self, obs, masks_by_head=None):
        return None, torch.tensor([self._value])


def test_flag_enabled_default(monkeypatch):
    monkeypatch.delenv("PPO_REACTION_VALUE_POLICY", raising=False)
    assert ppo_reaction_value_policy_enabled() is True


def test_flag_off(monkeypatch):
    monkeypatch.setenv("PPO_REACTION_VALUE_POLICY", "0")
    assert ppo_reaction_value_policy_enabled() is False


def test_install_side_generic_sets_policy():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    net = _ConstNet(0.5)
    install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": net})
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side == {"model": net}


def test_install_accepts_both_sides():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    p1, p2 = _ConstNet(0.1), _ConstNet(0.2)
    install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": p1, "enemy": p2})
    assert env._reaction_net_by_side == {"model": p1, "enemy": p2}


def test_ppo_value_returns_critic():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    v = ppo_value(env, _ConstNet(0.73), torch.device("cpu"), "model")
    assert abs(v - 0.73) < 1e-6
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_ppo_stratagem_bridge.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'core.models.ppo_stratagem_bridge'`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/ppo_stratagem_bridge.py
"""PPO ↔ стратагемы: critic-V, fight-plan builder, side-generic policy install.

Переиспользует AZ-инфру (reaction_value_policy, attach_fight_stratagem_plan)
поверх ActorCriticMultiHead.infer_with_value (честный critic V).
"""

from __future__ import annotations

import os

import numpy as np
import torch

from core.engine.phases.stratagem_engine import apply as _apply_stratagem
from core.engine.phases.stratagems import for_phase, usage_limit_reached
from core.engine.phases.types import Phase
from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def ppo_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("PPO_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_ppo_stratagem_policy(env, device, net_by_side: dict) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": ac_net}. Both-sides (честный p1/p2) — тот же вызов с
    {"model": p1, "enemy": p2}, без правок движка/bridge. Сторона без сети → legacy.
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def ppo_value(env, ac_net, device, side: str) -> float:
    """critic V(s) для стороны side. Маски не нужны — critic mask-независим."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    with torch.no_grad():
        _, v = ac_net.infer_with_value(obs, masks_by_head=None)
    return float(v.reshape(-1)[0].item())
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_ppo_stratagem_bridge.py -v`
Expected: PASS (5 тестов).

- [ ] **Step 5: Commit**

```bash
git add core/models/ppo_stratagem_bridge.py tests/models/test_ppo_stratagem_bridge.py
git commit -m "feat(ppo): ppo_stratagem_bridge — флаг, side-generic install, critic-V"
```

---

### Task 3: `ppo_build_fight_plan` — greedy critic-V lookahead

**Files:**
- Modify: `core/models/ppo_stratagem_bridge.py` (добавить `ppo_build_fight_plan`)
- Test: `tests/models/test_ppo_stratagem_bridge.py` (дописать кейсы)

**Interfaces:**
- Consumes: `ppo_value` (Task 2); `for_phase(Phase.FIGHT)`, `usage_limit_reached`, `_apply_stratagem` (импорты уже в модуле); env API: `snapshot_state`/`restore_state`/`simulation_mode`, `unit_health`/`enemy_health`, `unitInAttack`/`enemyInAttack`, `modelCP`/`enemyCP`, `_reaction_sim_active`.
- Produces: `ppo_build_fight_plan(env, ac_net, device, side="model") -> dict[int, str]` (`{unit_idx: stratagem_id}`).

- [ ] **Step 1: Write the failing test**

Дописать в `tests/models/test_ppo_stratagem_bridge.py`:

```python
from unittest.mock import MagicMock

from core.models.ppo_stratagem_bridge import ppo_build_fight_plan


class _ValueSeqNet:
    """Возвращает заданную последовательность V при каждом infer_with_value."""

    def __init__(self, values):
        self._values = list(values)

    def infer_with_value(self, obs, masks_by_head=None):
        v = self._values.pop(0) if self._values else 0.0
        return None, torch.tensor([float(v)])


def test_fight_plan_snapshot_invariant():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    cp_before = int(env.modelCP)
    su_before = dict(getattr(env, "stratagem_used", {}) or {})
    plan = ppo_build_fight_plan(env, _ValueSeqNet([0.9, 0.1]), torch.device("cpu"), side="model")
    assert isinstance(plan, dict)
    assert env.modelCP == cp_before  # snapshot/restore не испортил состояние
    assert dict(getattr(env, "stratagem_used", {}) or {}) == su_before


def test_fight_plan_empty_when_pass_wins():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.unitInAttack[0] = [1, 0]
    plan = ppo_build_fight_plan(env, _ValueSeqNet([0.1, 0.9]), torch.device("cpu"), side="model")
    assert plan == {}


def test_fight_plan_skips_when_no_cp():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 0
    env.unitInAttack[0] = [1, 0]
    plan = ppo_build_fight_plan(env, _ValueSeqNet([0.9, 0.1]), torch.device("cpu"), side="model")
    assert plan == {}


def test_fight_plan_recursion_guard():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env._reaction_sim_active = True
    net = MagicMock()
    assert ppo_build_fight_plan(env, net, torch.device("cpu")) == {}
    net.infer_with_value.assert_not_called()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_ppo_stratagem_bridge.py -k fight_plan -v`
Expected: FAIL — `ImportError: cannot import name 'ppo_build_fight_plan'`.

- [ ] **Step 3: Write minimal implementation**

Добавить в конец `core/models/ppo_stratagem_bridge.py`:

```python
def ppo_build_fight_plan(env, ac_net, device, side: str = "model") -> dict[int, str]:
    """Hungry Void / Command Re-roll план через critic-V lookahead (2 ветки на юнит).

    Структура 1:1 с dqn_build_fight_plan: snapshot → apply/pass → critic V → выбор.
    eps=1e-3: greedy per-unit planner без MCTS-joint → лёгкий уклон в PASS.
    """
    e = unwrap_env(env)
    if getattr(e, "_reaction_sim_active", False):
        return {}  # recursion guard
    health = e.unit_health if side == "model" else e.enemy_health
    in_attack = e.unitInAttack if side == "model" else e.enemyInAttack
    plan: dict[int, str] = {}
    eps = 1e-3
    for d in for_phase(Phase.FIGHT):
        cp = int(e.modelCP if side == "model" else e.enemyCP)
        if cp < d.cp_cost:
            continue
        if usage_limit_reached(e, side, d, phase="fight"):
            continue
        for u in range(len(health)):
            if health[u] <= 0 or in_attack[u][0] != 1:
                continue
            if u in plan:
                continue
            snap = e.snapshot_state()
            try:
                with e.simulation_mode():
                    e.restore_state(snap)
                    _apply_stratagem(e, side, d.id, u, phase="fight")
                    v_apply = ppo_value(e, ac_net, device, side)
                    e.restore_state(snap)
                    v_pass = ppo_value(e, ac_net, device, side)
            finally:
                e.restore_state(snap)
            if v_apply > v_pass + eps:
                plan[u] = d.id
    return plan
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_ppo_stratagem_bridge.py -v`
Expected: PASS (все, включая fight_plan).

- [ ] **Step 5: Commit**

```bash
git add core/models/ppo_stratagem_bridge.py tests/models/test_ppo_stratagem_bridge.py
git commit -m "feat(ppo): ppo_build_fight_plan — greedy critic-V lookahead (eps=1e-3)"
```

---

### Task 4: Регрессия seam — PPO-сеть через `_simulate_reaction_branch`

**Files:**
- Test: `tests/engine/phases/test_simulate_reaction_branch_ppo.py` (создать)

**Interfaces:**
- Consumes: `env._simulate_reaction_branch(ctx, *, apply)` (без изменений движка), `ActorCriticMultiHead.infer_with_value` (Task 1).
- Produces: ничего (регрессия-гард, что real PPO-net проходит seam'ом, а AZ-mock — прежним путём).

- [ ] **Step 1: Write the failing test**

```python
# tests/engine/phases/test_simulate_reaction_branch_ppo.py
"""_simulate_reaction_branch: real ActorCriticMultiHead идёт через infer_with_value."""

import numpy as np

from core.models.action_contract import action_sizes_from_env
from core.models.PPO import ActorCriticMultiHead
from tests.engine.phases._helpers import build_env


def _ctx(env, net):
    return {
        "side": "model",
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": 1,
        "env": env,
        "resolve_trigger": lambda apply: None,
        "net": net,
    }


def test_ppo_net_runs_through_seam():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    net = ActorCriticMultiHead(obs_dim, sizes, hidden_size=32, num_layers=1)
    net.eval()
    v = env._simulate_reaction_branch(_ctx(env, net), apply=False)
    assert isinstance(v, float)
    assert np.isfinite(v)


def test_az_mock_without_infer_with_value_unbroken():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}

    class _AzNet:
        def infer(self, obs):
            import torch

            calls["method"] = "infer"
            return None, torch.tensor([0.42])

    v = env._simulate_reaction_branch(_ctx(env, _AzNet()), apply=True)
    assert calls["method"] == "infer"
    assert abs(v - 0.42) < 1e-6
```

- [ ] **Step 2: Run test to verify it fails or passes**

Run: `python -m pytest tests/engine/phases/test_simulate_reaction_branch_ppo.py -v`
Expected: PASS сразу (движок уже умеет duck-typing; это регрессия-гард). Если FAIL — значит seam сломан/изменён; **остановиться и разобраться** (движок менять нельзя).

- [ ] **Step 3: Commit**

```bash
git add tests/engine/phases/test_simulate_reaction_branch_ppo.py
git commit -m "test(ppo): seam-регрессия — ActorCriticMultiHead через _simulate_reaction_branch"
```

---

### Task 5: train.py — флаг + install + fight-plan (inline и actor пути)

**Files:**
- Modify: `train.py` — резолв флага (рядом со строкой 300); install после создания `actor_critic` (~3627 и ~3919); fight-plan вокруг `env.step` (~3685).

**Interfaces:**
- Consumes: `ppo_reaction_value_policy_enabled`, `install_ppo_stratagem_policy`, `ppo_build_fight_plan` (Tasks 2-3); `attach_fight_stratagem_plan` из `core.models.option_candidates`; `actor_critic`, `device`, `env`/`env_contexts`, `USE_SUBPROC_ENVS`, `data` (загруженный hyperparams dict), `append_agent_log`.
- Produces: установленный `env.reaction_policy` + per-step fight-plan для PPO-inline/actor путей.

- [ ] **Step 1: Добавить резолв флага**

В `train.py` рядом с `DQN_REACTION_VALUE_POLICY` (после строки 302) вставить:

```python
_PPO_CFG = data.get("ppo", {}) if isinstance(data, dict) else {}
_ppo_rvp_raw = os.getenv("PPO_REACTION_VALUE_POLICY", str(_PPO_CFG.get("reaction_value_policy", 1)))
PPO_REACTION_VALUE_POLICY = str(_ppo_rvp_raw).strip().lower() in ("1", "true", "yes", "on")
if "PPO_REACTION_VALUE_POLICY" not in os.environ:
    os.environ["PPO_REACTION_VALUE_POLICY"] = "1" if PPO_REACTION_VALUE_POLICY else "0"
```

> Проверка: `data` — имя загруженного hyperparams-словаря в `train.py` (используется в `_cfg_raw`).
> Если в этой области имя другое — взять то, что реально содержит top-level hyperparams.

- [ ] **Step 2: Установить policy после создания actor_critic (оба пути)**

После `actor_critic = make_actor_critic(...)` на строке ~3627 и ~3919 — определить `env_contexts`-эквивалент для этого пути (одиночный `env` или список). Для одиночного `env` вставить:

```python
if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
    from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

    install_ppo_stratagem_policy(env, device, {"model": actor_critic})
    append_agent_log("[PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)")
```

> Если путь использует список окружений (`env_contexts`), цикл: `for ctx in env_contexts: install_ppo_stratagem_policy(ctx["env"], device, {"model": actor_critic})`. Сверься с тем, как рядом сделан DQN (`train.py:4694-4701`).

- [ ] **Step 3: Fight-plan вокруг env.step**

В PPO-цикле перед `env.step`/`strat_tracer.run_model_step` (~3685) обернуть step:

```python
from core.models.option_candidates import attach_fight_stratagem_plan
from core.models.ppo_stratagem_bridge import ppo_build_fight_plan

if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
    attach_fight_stratagem_plan(env, ppo_build_fight_plan(env, actor_critic, device, side="model"))
try:
    # существующий вызов: strat_tracer.run_model_step(...) ИЛИ env.step(action_dict)
    ...
finally:
    if PPO_REACTION_VALUE_POLICY and not USE_SUBPROC_ENVS:
        attach_fight_stratagem_plan(env, None)
```

> Зеркало DQN-блока `train.py:5374-5395`. `attach_fight_stratagem_plan(env, None)` в `finally` — обязательно (cleanup).

- [ ] **Step 4: Smoke-проверка резолва импортов**

Run: `python -c "import train"`
Expected: без ImportError/SyntaxError (ruff_fix мог тронуть импорты — проверить, что всё на месте).

- [ ] **Step 5: Commit**

```bash
git add train.py
git commit -m "feat(ppo,train): reaction_value_policy install + fight-plan (inline/actor)"
```

---

### Task 6: train.py — actor-learner spawn (`_main_actor_learner`)

**Files:**
- Modify: `train.py` — PPO-ветка в `_main_actor_learner` (cpu_net ~8604; зеркало DQN install `8213` и fight-plan `8383`).

**Interfaces:**
- Consumes: те же символы, что Task 5; `cpu_net` (PPO actor-net в spawn-процессе); `os.environ["PPO_REACTION_VALUE_POLICY"]` (проброшен в spawn).
- Produces: install + fight-plan для PPO в spawn-процессах (learner и actors не разъезжаются по семантике стратагем).

- [ ] **Step 1: Найти PPO-ветку в `_main_actor_learner`**

Прочитать `train.py` около строк 8590-8760 (там `cpu_net = make_actor_critic(...)` на ~8604 и `cpu_net.act(...)` на ~8748). Определить: одиночный `env` в этом процессе и где идёт `env.step`.

- [ ] **Step 2: Установить policy после cpu_net**

После `cpu_net = make_actor_critic(...)` (~8604) — по аналогии с DQN-блоком `train.py:8213-8218`:

```python
if str(os.getenv("PPO_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on"):
    from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

    install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": cpu_net})
```

- [ ] **Step 3: Fight-plan вокруг env.step в spawn-цикле**

Перед `env.step` в этом цикле (зеркало DQN `train.py:8383-8395`):

```python
from core.models.option_candidates import attach_fight_stratagem_plan

_ppo_rvp = str(os.getenv("PPO_REACTION_VALUE_POLICY", "1")).strip().lower() in ("1", "true", "yes", "on")
if _ppo_rvp:
    from core.models.ppo_stratagem_bridge import ppo_build_fight_plan

    attach_fight_stratagem_plan(env, ppo_build_fight_plan(env, cpu_net, torch.device("cpu"), side="model"))
try:
    # существующий env.step(...)
    ...
finally:
    if _ppo_rvp:
        attach_fight_stratagem_plan(env, None)
```

- [ ] **Step 4: Smoke-проверка**

Run: `python -c "import train"`
Expected: без ошибок импорта/синтаксиса.

- [ ] **Step 5: Commit**

```bash
git add train.py
git commit -m "feat(ppo,train): reaction_value_policy в _main_actor_learner (spawn)"
```

---

### Task 7: eval.py — install + fight-plan для PPO

**Files:**
- Modify: `eval.py` — install после загрузки PPO-чекпойнта (~1273); fight-plan в `run_episode` PPO-ветке (после ~795, до `env.step` ~890).

**Interfaces:**
- Consumes: `ppo_reaction_value_policy_enabled` (уже импортирован в eval.py? — нет, импортирован `dqn_reaction_value_policy_enabled` на строке 43; добавить `ppo_reaction_value_policy_enabled`), `install_ppo_stratagem_policy`, `ppo_build_fight_plan`; `attach_fight_stratagem_plan` (уже используется в eval.py:792/893); `policy_net` (PPO-net), `device`, `env`, `algo`.
- Produces: PPO-eval с умными стратагемами; CONFIG-лог.

- [ ] **Step 1: Install после загрузки PPO-чекпойнта**

В `eval.py` после `policy_net.eval()` в ветке `if algo == "ppo":` (после строки 1273) вставить:

```python
        if ppo_reaction_value_policy_enabled():
            from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

            install_ppo_stratagem_policy(env, device, {"model": policy_net})
            log("[EVAL][PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)")
```

И добавить импорт рядом со строкой 43:

```python
from core.models.ppo_stratagem_bridge import ppo_reaction_value_policy_enabled
```

> ruff_fix может срезать импорт, если он не используется в момент сохранения — добавляй импорт **вместе** с использованием в Step 1 (один Edit), либо сразу за ним.

- [ ] **Step 2: Fight-plan в run_episode PPO-ветке**

В `run_episode`, в ветке `if algo == "ppo":` (после `action = select_action_with_epsilon_ppo(...)`, строка ~801, по аналогии с DQN-веткой `eval.py:836-841`) вставить:

```python
        if algo == "ppo" and ppo_reaction_value_policy_enabled():
            from core.models.ppo_stratagem_bridge import ppo_build_fight_plan

            attach_fight_stratagem_plan(
                env, ppo_build_fight_plan(env, policy_net, device, side="model")
            )
```

> Cleanup уже есть: `attach_fight_stratagem_plan(env, None)` на `eval.py:792` (перед след. шагом) и в `finally` на `eval.py:893`. Дополнительно ничего не нужно.

- [ ] **Step 3: Smoke-проверка**

Run: `python -c "import eval"`
Expected: без ошибок импорта/синтаксиса.

- [ ] **Step 4: Commit**

```bash
git add eval.py
git commit -m "feat(ppo,eval): reaction_value_policy install + fight-plan в run_episode"
```

---

### Task 8: hyperparams.json + smoke (eval --games 50)

**Files:**
- Modify: `hyperparams.json` (добавить/обновить секцию `ppo` ключом `reaction_value_policy: 1`)
- Verify: запуск train (короткий) + eval `--games 50`.

**Interfaces:**
- Consumes: всё из Tasks 1-7.
- Produces: дефолт-флаг в конфиге; подтверждённое поведение в логах.

- [ ] **Step 1: Добавить ключ в hyperparams.json**

Прочитать `hyperparams.json`, найти секцию `"ppo"` (если есть). Добавить ключ:

```json
  "ppo": {
    "reaction_value_policy": 1
  }
```

> Если секция `ppo` уже есть — добавить только ключ `reaction_value_policy`, не ломая существующие.
> Если её нет — создать с этим ключом. Сохранить валидный JSON (запятые!).

- [ ] **Step 2: Прогнать весь новый тест-набор**

Run:
```bash
python -m pytest tests/models/test_ppo_infer_with_value.py tests/models/test_ppo_stratagem_bridge.py tests/engine/phases/test_simulate_reaction_branch_ppo.py -v
```
Expected: всё PASS.

- [ ] **Step 3: Регрессия DQN/AZ reaction-тестов**

Run:
```bash
python -m pytest tests/engine/phases/test_simulate_reaction_branch_dqn.py tests/models/test_dqn_stratagem_bridge.py tests/models/test_dqn_infer_with_value.py -v
```
Expected: всё PASS (PPO не задел DQN/AZ).

- [ ] **Step 4: Smoke — короткий train PPO**

Run (PowerShell):
```powershell
$env:TRAIN_ALGO="ppo"; $env:PPO_REACTION_VALUE_POLICY="1"; python train.py --episodes 1
```
Expected: в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` есть строка `[PPO][CONFIG] reaction_value_policy установлена (critic V, learner_only)`; появляются `[STRATAGEM]` со списанным CP; нет трейсбеков.

> Точные аргументы train.py сверь с `python train.py --help` / GUI-дефолтами; цель — минимальный прогон.

- [ ] **Step 5: Smoke — eval 50 игр**

Run (PowerShell):
```powershell
$env:PPO_REACTION_VALUE_POLICY="1"; python eval.py --algo ppo --games 50
```
Expected: лог `[EVAL][PPO][CONFIG] reaction_value_policy установлена ...`; 50 игр без падений; в `LOGS_FOR_AGENTS_EVAL.md` видны умные стратагемы (CP списывается выборочно, не всегда).

> Сверь точные флаги eval.py с `python eval.py --help` (модель/агент-id). Если нужен `--agent-id` — подставь актуальный PPO-чекпойнт.

- [ ] **Step 6: Smoke — legacy выключение**

Run (PowerShell):
```powershell
$env:PPO_REACTION_VALUE_POLICY="0"; python eval.py --algo ppo --games 5
```
Expected: CONFIG-лог отсутствует; CP списывается всегда при достатке (legacy). Подтверждает, что флаг реально гейтит.

- [ ] **Step 7: Commit**

```bash
git add hyperparams.json
git commit -m "feat(ppo): hyperparams ppo.reaction_value_policy=1 + smoke verified"
```

---

## Self-Review

**Spec coverage:**
- §3.4.1 `infer_with_value` → Task 1. ✅
- §3.4.2 bridge (флаг, install side-generic, ppo_value, fight-plan) → Tasks 2-3. ✅
- §3.3 «движок 0 изменений» / seam → Task 4 (регрессия-гард). ✅
- §3.4.3 train.py (inline/actor + spawn) → Tasks 5-6. ✅
- §3.4.4 eval.py → Task 7. ✅
- §5 hyperparams + §7.4 smoke (eval --games 50) → Task 8. ✅
- §4 side-generic install → Task 2 (`net_by_side` dict) + тест `test_install_accepts_both_sides`. ✅
- §7.1-7.3 тесты → Tasks 1-4, 8 (регрессия). ✅

**Placeholder scan:** Код во всех code-шагах конкретный. Места с «сверься» (имя `data`, точные CLI-флаги train/eval, расположение `cpu_net`) — это явные verify-инструкции, не placeholder'ы реализации; они есть потому, что 3 PPO-пути в train.py имеют разную локальную структуру и точные имена нужно подтвердить в коде, а не угадывать.

**Type consistency:** `infer_with_value(obs, masks_by_head=None) -> (probs, V)` — одинаково в Tasks 1, 2, 4. `install_ppo_stratagem_policy(env, device, net_by_side)` — одинаково в Tasks 2, 5, 6, 7. `ppo_build_fight_plan(env, ac_net, device, side="model")` — одинаково в Tasks 3, 5, 6, 7. `ppo_value(env, ac_net, device, side)` — Tasks 2, 3. ✅
