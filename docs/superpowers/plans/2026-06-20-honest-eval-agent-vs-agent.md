# Честный eval agent-vs-agent (P1 ≡ P2 1:1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Убрать сегрегацию learner/enemy в `eval.py` — обе стороны (P1/P2) проходят через один код и один search-конфиг, симметричный reaction value-gate, fight-plan активной стороны и опциональный double-header (свап сторон).

**Architecture:** Вводим `EvalAgent` (новый `core/models/eval_agent.py`) — единая абстракция действия+реакции для всех 6 algo; ею ходят обе стороны. `eval.py` строит `p1_agent`/`p2_agent`, ставит `_reaction_net_by_side = {"model": p1.reaction_net, "enemy": p2.reaction_net}`, и в `run_episode` model ходит через `select_action`+`env.step`, enemy — через `as_policy_fn`+`env.enemyTurn`. Движок не трогаем сверх одной точечной правки `insane_bravery` для enemy.

**Tech Stack:** Python 3.12+, PyTorch (CPU eval), pytest. Reuse: `make_dqn`/`make_actor_critic`/`make_alphazero_net`/`GumbelMuZeroNet`/`make_sampled_muzero_net`, search-обёртки (`AlphaZeroFactorizedMCTS`, `build_gumbel_inference_search`, `GumbelMuZeroSearch`, `SampledMuZeroSearch`).

## Global Constraints

- Платформа — **Windows**; запуск train/eval приоритетно через Qt GUI (для тестов — pytest).
- Язык логов/ошибок/комментариев пользователю — **русский**; ошибка = что случилось + где + что делать.
- Движок (`core/engine`, `core/envs`) **не трогать** сверх Task 2 (одна правка `insane_bravery` enemy за гардом).
- **TDD**: тест до кода, частые коммиты (по задаче минимум один коммит).
- Зависимости — только из `requirements_windows.txt` (новых не вводим).
- Старые чекпойнты обязаны грузиться без изменений (загрузчики не меняем).
- `ruff` PostToolUse-хук срежет неиспользуемые импорты — добавляй импорт вместе с использованием.
- Спека: [docs/superpowers/specs/2026-06-20-honest-eval-agent-vs-agent-design.md](../specs/2026-06-20-honest-eval-agent-vs-agent-design.md).

---

### Task 1: `install_dqn_stratagem_policy` → side-generic

Зеркалим PPO-bridge: DQN-install принимает `net_by_side` (словарь side→net), а не один net. Поведение train/eval не меняется (вызыватели передают `{"model": net}`).

**Files:**
- Modify: `core/models/dqn_stratagem_bridge.py:28-34` (`install_dqn_stratagem_policy`)
- Modify: `train.py:4803`, `train.py:8322` (вызыватели)
- Modify: `eval.py:1355` (вызыватель — временно, удалится в Task 5)
- Test: `tests/models/test_dqn_stratagem_bridge.py` (добавить кейсы)

**Interfaces:**
- Produces: `install_dqn_stratagem_policy(env, net_by_side: dict, device) -> None` — ставит `env._reaction_net_by_side = dict(net_by_side)` и `env.reaction_policy = make_stratagem_value_policy(...)`.

- [ ] **Step 1: Написать падающий тест**

В `tests/models/test_dqn_stratagem_bridge.py` добавить:

```python
def test_install_dqn_side_generic_both_sides():
    from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy
    from tests.engine.phases._helpers import build_env
    import torch

    class _Q:
        def infer_with_value(self, obs, masks_by_head=None):
            return None, torch.tensor([0.0])

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    p1, p2 = _Q(), _Q()
    install_dqn_stratagem_policy(env, {"model": p1, "enemy": p2}, torch.device("cpu"))
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side == {"model": p1, "enemy": p2}
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/models/test_dqn_stratagem_bridge.py::test_install_dqn_side_generic_both_sides -v`
Expected: FAIL (старая сигнатура `(env, policy_net, device)` → `net_by_side` интерпретируется как `policy_net`, `_reaction_net_by_side == {"model": {"model": p1, "enemy": p2}}`).

- [ ] **Step 3: Сделать side-generic**

В `core/models/dqn_stratagem_bridge.py` заменить тело `install_dqn_stratagem_policy`:

```python
def install_dqn_stratagem_policy(env, net_by_side: dict, device) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": net} (learner-only). Both-sides (честный p1/p2) — тот же
    вызов с {"model": p1, "enemy": p2}, без правок движка/bridge. Сторона без сети → legacy.
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)
```

- [ ] **Step 4: Обновить вызывателей**

`train.py:4803`: `install_dqn_stratagem_policy(ctx["env"], policy_net, device)` → `install_dqn_stratagem_policy(ctx["env"], {"model": policy_net}, device)`.
`train.py:8322`: `install_dqn_stratagem_policy(env, cpu_net, torch.device("cpu"))` → `install_dqn_stratagem_policy(env, {"model": cpu_net}, torch.device("cpu"))`.
`eval.py:1355`: `install_dqn_stratagem_policy(env, policy_net, device)` → `install_dqn_stratagem_policy(env, {"model": policy_net}, device)`.

- [ ] **Step 5: Прогнать тесты bridge**

Run: `python -m pytest tests/models/test_dqn_stratagem_bridge.py -v`
Expected: PASS (новый + существующие; старый `test_install_*` если ждал старую сигнатуру — обновить на `{"model": net}`).

- [ ] **Step 6: Коммит**

```bash
git add core/models/dqn_stratagem_bridge.py train.py eval.py tests/models/test_dqn_stratagem_bridge.py
git commit -m "refactor(dqn): install_dqn_stratagem_policy side-generic (net_by_side)"
```

---

### Task 2: Движковая симметрия `insane_bravery` для enemy

Авто-путь enemy командной фазы (`warhamEnv.py:4803`) проводим через тот же value-gate, что и model (`4723-4727`). Гард `reaction_policy is not None` → при выключенных реакциях поведение неизменно.

**Files:**
- Modify: `core/envs/warhamEnv.py:4803` (enemy auto insane_bravery)
- Test: `tests/engine/phases/test_stratagem_insane_bravery.py` (добавить enemy-кейс)

**Interfaces:**
- Consumes: `_should_use_stratagem(sid, side, chosen, candidates, phase, cp, *, net=...)`, `_reaction_net_by_side`.

- [ ] **Step 1: Написать падающий тест (зеркало модельного)**

В `tests/engine/phases/test_stratagem_insane_bravery.py` добавить:

```python
def test_insane_bravery_value_gate_used_when_policy_enemy(monkeypatch):
    from tests.engine.phases._helpers import build_env
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}
    def fake_gate(sid, side, chosen, cand, phase, cp, **k):
        calls["sid"] = sid
        calls["side"] = side
        return True
    env.reaction_policy = object()  # не None
    env._reaction_net_by_side = {"enemy": object()}
    monkeypatch.setattr(env, "_should_use_stratagem", fake_gate)
    monkeypatch.setattr("core.envs.warhamEnv.dice", lambda num=1: [1, 1])
    env.enemy_health[0] = 1
    env.enemy_data[0]["W"] = 4  # ниже половины
    env.enemyCP = 3
    env.command_phase("enemy", action={"use_cp": 0, "cp_on": -1})
    assert calls.get("sid") == "insane_bravery"
    assert calls.get("side") == "enemy"
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/engine/phases/test_stratagem_insane_bravery.py::test_insane_bravery_value_gate_used_when_policy_enemy -v`
Expected: FAIL (enemy-путь сейчас решает только по `use_cp == 1 and cp_on == i`, gate не вызывается → `calls` пуст).

- [ ] **Step 3: Зеркалить модельный gate в enemy-блоке**

В `core/envs/warhamEnv.py` заменить строку 4803 (`if use_cp == 1 and cp_on == i:`) на:

```python
                        if getattr(self, "reaction_policy", None) is not None:
                            _use_bravery = self._should_use_stratagem(
                                "insane_bravery", "enemy", i, [i], "command", int(self.enemyCP),
                                net=getattr(self, "_reaction_net_by_side", {}).get("enemy"),
                            )
                        else:
                            _use_bravery = (use_cp == 1 and cp_on == i)
                        if _use_bravery:
```

(Тело под `if` — существующие строки 4804-4809 `_bravery = _apply_stratagem(...)` и далее — оставить без изменений, под новым `if _use_bravery:`.)

- [ ] **Step 4: Прогнать тесты insane_bravery + реакций**

Run: `python -m pytest tests/engine/phases/test_stratagem_insane_bravery.py tests/engine/phases/test_stratagem_value_gate_parity.py -v`
Expected: PASS (новый enemy-кейс + существующие model-кейсы; при `reaction_policy is None` поведение не изменилось).

- [ ] **Step 5: Коммит**

```bash
git add core/envs/warhamEnv.py tests/engine/phases/test_stratagem_insane_bravery.py
git commit -m "fix(env): insane_bravery enemy через value-gate (симметрия с model, за гардом)"
```

---

### Task 3: `EvalSearchCfg` + `resolve_eval_search_cfg` (единый конфиг обеих сторон)

Новый модуль `core/models/eval_agent.py` начинаем с конфиг-резолвера: один источник search-настроек для P1 и P2 (форк `*_OPPONENT_*` уходит из честного пути; при их наличии — WARN-флаг).

**Files:**
- Create: `core/models/eval_agent.py`
- Test: `tests/models/test_eval_agent_cfg.py`

**Interfaces:**
- Produces:
  - `@dataclass EvalSearchCfg(algo: str, deterministic: bool, epsilon: float, search: dict, opponent_override_active: bool)`
  - `resolve_eval_search_cfg(algo: str) -> EvalSearchCfg`

- [ ] **Step 1: Написать падающий тест**

`tests/models/test_eval_agent_cfg.py`:

```python
import pytest
from core.models.eval_agent import resolve_eval_search_cfg, EvalSearchCfg


def test_cfg_defaults_deterministic(monkeypatch):
    for k in ("EVAL_DETERMINISTIC", "EVAL_EPSILON", "AZ_EVAL_MCTS_SIMS"):
        monkeypatch.delenv(k, raising=False)
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert isinstance(cfg, EvalSearchCfg)
    assert cfg.deterministic is True
    assert cfg.epsilon == 0.0
    assert cfg.search["simulations"] == 32


def test_cfg_reads_unified_az_temperature(monkeypatch):
    monkeypatch.setenv("AZ_EVAL_MCTS_TEMPERATURE", "0.20")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert abs(cfg.search["temperature"] - 0.20) < 1e-9


def test_cfg_opponent_override_warns(monkeypatch):
    monkeypatch.setenv("AZ_EVAL_OPPONENT_MCTS_SIMS", "8")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert cfg.opponent_override_active is True


def test_cfg_gmz_smz_search_params(monkeypatch):
    monkeypatch.setenv("GMZ_EVAL_SIMS", "16")
    cfg = resolve_eval_search_cfg("gumbel_muzero")
    assert cfg.search["num_simulations"] == 16
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/models/test_eval_agent_cfg.py -v`
Expected: FAIL (модуль `core.models.eval_agent` не существует).

- [ ] **Step 3: Реализовать резолвер**

`core/models/eval_agent.py`:

```python
"""EvalAgent: единый путь действия+реакции для обеих сторон eval (P1 ≡ P2).

Резолвер конфига читает общие EVAL-флаги (без *_OPPONENT_*); при наличии
*_OPPONENT_* поднимает opponent_override_active (честный 1:1 нарушен).
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

from core.models.alphazero_ids import is_alphazero_net_algo, is_gumbel_az_algo

_TRUTHY = frozenset({"1", "true", "yes", "on"})
_OPPONENT_KEYS = (
    "AZ_EVAL_OPPONENT_MODE", "AZ_EVAL_OPPONENT_MCTS_SIMS", "AZ_EVAL_OPPONENT_MCTS_TEMPERATURE",
    "GAZ_EVAL_OPPONENT_MODE", "GMZ_OPPONENT_MODE", "GMZ_EVAL_OPPONENT_SIMS",
    "GMZ_EVAL_OPPONENT_TEMPERATURE", "SMZ_OPPONENT_MODE", "SMZ_EVAL_OPPONENT_NUM_SAMPLES",
    "SMZ_EVAL_OPPONENT_TEMPERATURE",
)


def _bool_env(name: str, default: str) -> bool:
    return str(os.getenv(name, default)).strip().lower() in _TRUTHY


@dataclass
class EvalSearchCfg:
    algo: str
    deterministic: bool
    epsilon: float
    search: dict[str, Any] = field(default_factory=dict)
    opponent_override_active: bool = False


def resolve_eval_search_cfg(algo: str) -> EvalSearchCfg:
    algo = str(algo or "").strip().lower()
    deterministic = _bool_env("EVAL_DETERMINISTIC", "1")
    epsilon = float(os.getenv("EVAL_EPSILON", "0"))
    override = any(os.getenv(k) is not None for k in _OPPONENT_KEYS)
    search: dict[str, Any] = {}

    if is_alphazero_net_algo(algo):
        if is_gumbel_az_algo(algo):
            search.update(
                mode=str(os.getenv("GAZ_EVAL_MODE", "gumbel")).strip().lower(),
                num_simulations=max(1, int(os.getenv("GAZ_EVAL_SIMS", "32"))),
                num_considered_actions=max(2, int(os.getenv("GAZ_EVAL_NUM_CONSIDERED", "8"))),
                joint_action=str(os.getenv("GAZ_JOINT_ACTION", "1")).strip() == "1",
                temperature=float(os.getenv("GAZ_EVAL_TEMPERATURE", "0.05")),
            )
        else:
            search.update(
                mode=str(os.getenv("AZ_EVAL_MODE", "mcts")).strip().lower(),
                simulations=max(1, int(os.getenv("AZ_EVAL_MCTS_SIMS", "32"))),
                c_puct=float(os.getenv("AZ_EVAL_MCTS_C_PUCT", "1.5")),
                dirichlet_alpha=float(os.getenv("AZ_EVAL_MCTS_DIR_ALPHA", "0.3")),
                dirichlet_eps=float(os.getenv("AZ_EVAL_MCTS_DIR_EPS", "0.0")),
                top_k_per_head=max(1, int(os.getenv("AZ_EVAL_MCTS_TOP_K_PER_HEAD", "8"))),
                max_depth=max(1, int(os.getenv("AZ_EVAL_MCTS_MAX_DEPTH", "1"))),
                mcts_mode=str(os.getenv("AZ_EVAL_MCTS_MODE", "tree")).strip().lower(),
                candidate_mode=str(os.getenv("AZ_EVAL_MCTS_CANDIDATE_MODE", os.getenv("MCTS_CANDIDATE_MODE", "option"))).strip().lower(),
                window_nodes=_bool_env("AZ_EVAL_MCTS_WINDOW_NODES", os.getenv("MCTS_WINDOW_NODES", "0")),
                joint_best_child=_bool_env("AZ_EVAL_MCTS_JOINT_BEST_CHILD", os.getenv("AZ_MCTS_JOINT_BEST_CHILD", "0")),
                temperature=float(os.getenv("AZ_EVAL_MCTS_TEMPERATURE", "0.06")),
            )
    elif algo == "gumbel_muzero":
        search.update(
            mode=str(os.getenv("GMZ_EVAL_MODE", "search")).strip().lower(),
            num_simulations=max(1, int(os.getenv("GMZ_EVAL_SIMS", "32"))),
            root_top_k=max(1, int(os.getenv("GMZ_EVAL_ROOT_TOP_K", "8"))),
            temperature=float(os.getenv("GMZ_EVAL_TEMPERATURE", "0.10")),
        )
    elif algo == "sampled_muzero":
        search.update(
            mode=str(os.getenv("SMZ_EVAL_MODE", "search")).strip().lower(),
            num_samples=int(os.getenv("SMZ_EVAL_NUM_SAMPLES", "24")),
            temperature=float(os.getenv("SMZ_EVAL_TEMPERATURE", "0.10")),
            sample_temperature=float(os.getenv("SMZ_EVAL_SAMPLE_TEMPERATURE", "1.0")),
            discount=float(os.getenv("SMZ_DISCOUNT", "0.997")),
        )
    return EvalSearchCfg(algo=algo, deterministic=deterministic, epsilon=epsilon, search=search, opponent_override_active=override)
```

- [ ] **Step 4: Прогнать — убедиться, что проходит**

Run: `python -m pytest tests/models/test_eval_agent_cfg.py -v`
Expected: PASS (4 кейса).

- [ ] **Step 5: Коммит**

```bash
git add core/models/eval_agent.py tests/models/test_eval_agent_cfg.py
git commit -m "feat(eval): EvalSearchCfg + resolve_eval_search_cfg (единый конфиг обеих сторон)"
```

---

### Task 4: `EvalAgent` + `build_eval_agent` (все 6 algo)

Ядро. `EvalAgent` строит net + search-обёртку из `EvalSearchCfg`, экспонирует `reaction_net`, даёт `select_action(env, side) -> (action_dict, fight_plan|None)` и `as_policy_fn(env, side)`. Конструкцию net+search **переиспользуем** из существующих веток (`opponent_adapter.build_policy_fn` и `eval.py` select_*), вынося в фабрику.

**Files:**
- Modify: `core/models/eval_agent.py` (добавить `EvalAgent` + `build_eval_agent`)
- Test: `tests/models/test_eval_agent.py`

**Interfaces:**
- Consumes: `EvalSearchCfg`, `resolve_eval_search_cfg` (Task 3); `attach_fight_stratagem_plan` (`option_candidates`); `ppo_build_fight_plan`/`dqn_build_fight_plan`; конструкторы сетей/поиска.
- Produces:
  - `class EvalAgent` с атрибутами `algo: str`, `net`, `reaction_net | None`, `search | None`, `cfg: EvalSearchCfg`, `len_model: int`.
  - `EvalAgent.select_action(env, side: str) -> tuple[dict, dict | None]`
  - `EvalAgent.as_policy_fn(env, side: str) -> Callable[[Any], dict]`
  - `build_eval_agent(*, algo: str, policy_state: dict, contract: dict, len_model: int, cfg: EvalSearchCfg | None = None, device=torch.device("cpu")) -> EvalAgent`

- [ ] **Step 1: Написать падающие тесты (стаб-нет/поиск, как `_ConstNet`)**

`tests/models/test_eval_agent.py`:

```python
import torch
from core.models.eval_agent import EvalAgent, resolve_eval_search_cfg
from core.models.option_candidates import attach_fight_stratagem_plan
from tests.engine.phases._helpers import build_env


class _DQNStub:
    """3 головы argmax + value-head (как DQN.infer_with_value)."""
    def __call__(self, obs_t):
        # heads: move(9), attack(2), shoot(K) — упрощённо фикс-размеры из контракта теста
        return [torch.zeros(1, 9), torch.zeros(1, 2), torch.zeros(1, 5)]
    def infer_with_value(self, obs, masks_by_head=None):
        return None, torch.tensor([0.0])


def _agent(env, algo, net, reaction_net):
    cfg = resolve_eval_search_cfg(algo)
    a = EvalAgent.__new__(EvalAgent)
    a.algo = algo; a.net = net; a.reaction_net = reaction_net
    a.search = None; a.cfg = cfg; a.len_model = len(env.model)
    return a


def test_reaction_net_none_for_gmz():
    # build_eval_agent для gmz/smz должен ставить reaction_net=None (legacy реакции)
    from core.models.eval_agent import build_eval_agent
    env = build_env(); env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    # Используем реальный путь сборки только до проверки reaction_net (см. Step 3 фабрику).
    # Здесь проверяем инвариант через приватный хелпер _reaction_net_for_algo.
    from core.models.eval_agent import _reaction_net_for_algo
    assert _reaction_net_for_algo("gumbel_muzero", object()) is None
    assert _reaction_net_for_algo("sampled_muzero", object()) is None
    sentinel = object()
    assert _reaction_net_for_algo("ppo", sentinel) is sentinel
    assert _reaction_net_for_algo("dqn", sentinel) is sentinel
    assert _reaction_net_for_algo("alphazero_tree", sentinel) is sentinel


def test_as_policy_fn_attaches_fight_plan(monkeypatch):
    env = build_env(); env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    a = _agent(env, "ppo", net=object(), reaction_net=object())
    monkeypatch.setattr(a, "select_action", lambda e, side: ({"move_num_0": 0}, {0: "command_reroll"}))
    fn = a.as_policy_fn(env, "enemy")
    out = fn(env.get_observation_for_side("enemy"))
    assert out == {"move_num_0": 0}
    assert dict(getattr(env, "_pending_fight_stratagem_plan", None) or {}) == {0: "command_reroll"}
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/models/test_eval_agent.py -v`
Expected: FAIL (`EvalAgent`, `_reaction_net_for_algo`, `build_eval_agent` не определены).

- [ ] **Step 3: Реализовать `EvalAgent` + фабрику**

Добавить в `core/models/eval_agent.py`. Ключевые элементы (переиспользуют существующие конструкторы из `opponent_adapter.py` 1:1 — те же `make_*`, `MCTSConfig`, search-обёртки):

```python
from collections.abc import Callable
from typing import Any as _Any

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict
from core.models.option_candidates import attach_fight_stratagem_plan
from core.models.utils import build_action_masks_by_head, build_shoot_action_mask, convertToDict


def _reaction_net_for_algo(algo: str, net):
    """GMZ/SMZ → None (legacy-симметрия); остальные → net (value-gate)."""
    a = str(algo or "").strip().lower()
    if a in ("gumbel_muzero", "sampled_muzero"):
        return None
    return net


class EvalAgent:
    def __init__(self, *, algo, net, reaction_net, search, cfg, len_model):
        self.algo = str(algo).strip().lower()
        self.net = net
        self.reaction_net = reaction_net
        self.search = search
        self.cfg = cfg
        self.len_model = int(len_model)

    def select_action(self, env, side: str) -> tuple[dict, dict | None]:
        obs_np = np.asarray(env.get_observation_for_side(side), dtype=np.float32)
        obs_t = torch.tensor(obs_np, dtype=torch.float32, device=torch.device("cpu")).unsqueeze(0)
        masks_cpu = build_action_masks_by_head(env, self.len_model, log_fn=None, debug=False)
        if self.algo == "dqn":
            return self._select_dqn(env, obs_t, masks_cpu, side)
        if self.algo == "ppo":
            return self._select_ppo(env, obs_t, masks_cpu, side)
        if is_alphazero_net_algo(self.algo):
            return self._select_az(env, obs_np, masks_cpu, side)
        if self.algo in ("gumbel_muzero", "sampled_muzero"):
            return self._select_muzero(env, obs_np, masks_cpu, side)
        raise ValueError(f"EvalAgent: неподдержанный algo={self.algo}")

    def as_policy_fn(self, env, side: str) -> Callable[[_Any], dict]:
        def _fn(_obs_any):
            act, plan = self.select_action(env, side)
            attach_fight_stratagem_plan(env, plan)
            return act
        return _fn

    # --- per-algo (тела переносим из opponent_adapter.build_policy_fn / eval.select_*) ---
    def _fight_plan(self, env, side):
        if self.reaction_net is None:
            return None
        if self.algo == "ppo":
            from core.models.ppo_stratagem_bridge import ppo_build_fight_plan
            return ppo_build_fight_plan(env, self.reaction_net, torch.device("cpu"), side=side)
        if self.algo == "dqn":
            from core.models.dqn_stratagem_bridge import dqn_build_fight_plan
            return dqn_build_fight_plan(env, self.reaction_net, torch.device("cpu"), side=side)
        return None

    def _select_dqn(self, env, obs_t, masks_cpu, side):
        with torch.no_grad():
            decision = self.net(obs_t)
        shoot_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
        action = []
        for head_idx, head in enumerate(decision):
            head_row = head.squeeze(0)
            if head_idx == 2 and shoot_mask is not None:
                mask = torch.as_tensor(shoot_mask, dtype=torch.bool, device=head_row.device)
                if mask.numel() == head_row.numel() and bool(mask.any()):
                    masked = head_row.clone(); masked[~mask] = -1e9
                    action.append(int(masked.argmax().item())); continue
            action.append(int(head_row.argmax().item()))
        action_dict = convertToDict(torch.tensor([action], device="cpu"))
        for i_u in range(self.len_model):
            action_dict[f"move_num_{i_u}"] = int(action[6 + i_u])
        return action_dict, self._fight_plan(env, side)

    def _select_ppo(self, env, obs_t, masks_cpu, side):
        masks = [m.to(torch.device("cpu")).unsqueeze(0) for m in masks_cpu]
        with torch.no_grad():
            action_t, _lp, _v = self.net.act(obs_t, masks_by_head=masks, deterministic=self.cfg.deterministic)
        action_np = action_t.squeeze(0).detach().cpu().numpy().tolist()
        action_dict = convertToDict(torch.tensor([action_np], device="cpu"))
        for i_u in range(self.len_model):
            action_dict[f"move_num_{i_u}"] = int(action_np[6 + i_u])
        return action_dict, self._fight_plan(env, side)

    def _select_az(self, env, obs_np, masks_cpu, side):
        legal = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
        s = self.search
        pi, selected, _v = s.run(
            obs=obs_np, legal_masks_by_head=legal,
            temperature=float(self.cfg.search.get("temperature", 0.06)),
            env=env, len_model=self.len_model, enemy_policy_fn=None,
        )
        if self.cfg.search.get("joint_best_child") or self.cfg.deterministic is False:
            action = [int(x) for x in selected]
        else:
            action = [int(np.argmax(p)) for p in pi] or [int(x) for x in selected]
        plan = getattr(s, "last_selected_fight_plan", None)
        return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), plan

    def _select_muzero(self, env, obs_np, masks_cpu, side):
        legal = [m.detach().cpu().numpy().astype(bool) for m in masks_cpu]
        pi, _bl, selected, _v = self.search.run(
            obs=obs_np, legal_masks_by_head=legal, deterministic=self.cfg.deterministic,
        )
        if self.cfg.deterministic:
            action = [int(np.argmax(p)) for p in pi] or [int(x) for x in selected]
        else:
            action = [int(x) for x in selected]
        return action_tensor_to_dict(torch.tensor([action], device="cpu"), len_model=self.len_model), None
```

`build_eval_agent(...)`: строит `net` и `search` per-algo **теми же вызовами**, что `opponent_adapter.build_policy_fn` (`opponent_adapter.py:106-382` — `make_dqn`/`make_actor_critic`/`make_alphazero_net`/`GumbelMuZeroNet`/`make_sampled_muzero_net` + `MCTSConfig`/`build_gumbel_inference_search`/`GumbelMuZeroSearch`/`SampledMuZeroSearch`), но числа симуляций/temp берёт из `cfg.search` (а не из `*_OPPONENT_*`). `reaction_net = _reaction_net_for_algo(algo, net)`. `search = None` для dqn/ppo. Параметры сети (`n_obs`, `n_actions`) — через `_parse_contract_sizes(contract)` (вынести/импортировать из `opponent_adapter`).

> **DRY-примечание для исполнителя:** вынеси конструкцию net+search из `opponent_adapter.build_policy_fn` в `build_eval_agent`, а `build_policy_fn` оставь тонкой обёрткой `build_eval_agent(...).as_policy_fn(env, "enemy")` (это закрывает Task 5/7). Пока (на этом шаге) допустимо продублировать и убрать дубль в Task 7.

- [ ] **Step 4: Прогнать — убедиться, что проходит**

Run: `python -m pytest tests/models/test_eval_agent.py -v`
Expected: PASS (reaction_net-инвариант + as_policy_fn attach).

- [ ] **Step 5: Коммит**

```bash
git add core/models/eval_agent.py tests/models/test_eval_agent.py
git commit -m "feat(eval): EvalAgent + build_eval_agent (единый путь действия+реакции, 6 algo)"
```

---

### Task 5: Интеграция в `eval.py` (обе стороны через EvalAgent)

`main` строит `p1_agent`/`p2_agent` и ставит симметричный reaction-словарь; `run_episode` использует агентов для обеих сторон. Логирование/трассировка/метрики не трогаем (меняется только источник действия).

**Files:**
- Modify: `eval.py` — `run_episode` (сигнатура + блоки enemy `734-768` и model `792-849`); `main` (загрузка `policy_net`/reaction `1270-1356`, opponent `1244-1254`, вызов `run_episode` `1480-1490`)
- Modify: `core/models/opponent_adapter.py` — `build_policy_fn` → обёртка над `build_eval_agent(...).as_policy_fn`
- Test: `tests/test_eval_honest_symmetry.py`

**Interfaces:**
- Consumes: `build_eval_agent`, `resolve_eval_search_cfg`, `EvalAgent.select_action`/`as_policy_fn`.
- Produces: `run_episode(env, model_units, enemy_units, learner_agent, opponent_agent, device, *, learner_side="P1")` — без `policy_net`/`epsilon`/`algo`/`opponent_policy_fn` (они внутри агентов).

- [ ] **Step 1: Написать падающий тест симметрии**

`tests/test_eval_honest_symmetry.py`:

```python
import torch
from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg
from tests.engine.phases._helpers import build_env


def _contract_from_env(env):
    obs = env.get_observation_for_side("model")
    from core.models.utils import build_action_masks_by_head
    masks = build_action_masks_by_head(env, len(env.model), log_fn=None, debug=False)
    heads = ",".join(str(int(m.numel())) for m in masks)
    return {"obs_space_signature": f"vec:{len(obs)}", "action_space_signature": f"heads:{heads}"}


def test_both_sides_get_reaction_net_for_same_algo():
    env = build_env(); env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    contract = _contract_from_env(env)
    from core.models.PPO import make_actor_critic, ppo_kwargs_from_env
    from core.models.opponent_adapter import _parse_contract_sizes
    n_obs, n_actions = _parse_contract_sizes(contract)
    net = make_actor_critic(n_obs, n_actions, **ppo_kwargs_from_env())
    cfg = resolve_eval_search_cfg("ppo")
    p1 = build_eval_agent(algo="ppo", policy_state=net.state_dict(), contract=contract, len_model=len(env.model), cfg=cfg)
    p2 = build_eval_agent(algo="ppo", policy_state=net.state_dict(), contract=contract, len_model=len(env.enemy), cfg=cfg)
    assert p1.reaction_net is not None and p2.reaction_net is not None
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/test_eval_honest_symmetry.py -v`
Expected: FAIL до реализации `build_eval_agent` net-construction (Task 4 Step 3 фабрика) — если фабрика готова, тест проходит уже здесь; иначе доделать фабрику.

- [ ] **Step 3: Переписать `run_episode` на агентов**

Сигнатура (`eval.py:448-458`):
```python
def run_episode(env, model_units, enemy_units, learner_agent, opponent_agent, device, *, learner_side: str = "P1"):
```
Блок enemy-хода (`eval.py:766`): заменить
```python
            env_unwrapped.enemyTurn(trunc=True, policy_fn=_logged_opponent_policy)
```
на (оборачиваем agent.as_policy_fn в существующий логирующий `_logged_opponent_policy`):
```python
            base_enemy_fn = opponent_agent.as_policy_fn(env_unwrapped, "enemy") if opponent_agent is not None else None
            if base_enemy_fn is not None:
                env_unwrapped.enemyTurn(trunc=True, policy_fn=_logged_wrap(base_enemy_fn))
            else:
                env_unwrapped.enemyTurn(trunc=True)
```
где `_logged_wrap` — существующая логика `_logged_opponent_policy`, но принимающая базовый fn (рефактор: `_logged_opponent_policy(obs)` → `_logged_wrap(base)(obs)`; внутренняя трассировка `[TRACE][ENEMY_ACTION]` сохраняется).
Блок model-хода (`eval.py:792-849`): заменить весь if/elif по algo + fight-plan на:
```python
        attach_fight_stratagem_plan(env, None)
        action_dict, _plan = learner_agent.select_action(env_unwrapped, "model")
        attach_fight_stratagem_plan(env, _plan)
```
(удаляются вызовы `select_action_with_epsilon*`, локальные `ppo_build_fight_plan`/`dqn_build_fight_plan` и строка `action_dict = convertToDict(action)` на `849` — `action_dict` уже готов.)

- [ ] **Step 4: Перевести `main` на агентов**

Заменить per-algo загрузку `policy_net` и reaction-install (`eval.py:1270-1356`) на:
```python
        cfg = resolve_eval_search_cfg(algo)
        if cfg.opponent_override_active:
            log("[EVAL][CONFIG][WARN] *_OPPONENT_* override активен → честный 1:1 нарушен.")
        learner_agent = build_eval_agent(
            algo=algo, policy_state=normalize_state_dict(policy_state),
            contract=eval_contract, len_model=len(model_units), cfg=cfg, device=device,
        )
```
Opponent (`eval.py:1244-1254`): вместо `build_policy_fn` →
```python
            opponent_agent = build_eval_agent(
                algo=opp.algo, policy_state=opp.policy_state, contract=opp.contract,
                len_model=len(enemy_units), cfg=resolve_eval_search_cfg(opp.algo), device=device,
            )
```
(`opponent_agent = None` при отсутствии opponent — heuristic).
Симметричный reaction-словарь (после построения обоих агентов):
```python
        _eu = unwrap_env(env)
        react = {"model": learner_agent.reaction_net, "enemy": getattr(opponent_agent, "reaction_net", None)}
        if any(v is not None for v in react.values()):
            from core.models.reaction_value_policy import make_reaction_value_policy
            _eu._reaction_net_by_side = react
            _eu.reaction_policy = make_reaction_value_policy(react, device=device)
            log("[EVAL][CONFIG] reaction_value_policy установлена both-sides (model/enemy).")
```
Вызов `run_episode` (`eval.py:1480-1490`):
```python
        ) = run_episode(env, model_units, enemy_units, learner_agent, opponent_agent, device, learner_side=learner_side)
```

- [ ] **Step 5: `build_policy_fn` → тонкая обёртка**

В `core/models/opponent_adapter.py` заменить тело `build_policy_fn` на:
```python
def build_policy_fn(*, env, len_model, opponent, deterministic=True):
    from core.models.eval_agent import build_eval_agent, resolve_eval_search_cfg
    cfg = resolve_eval_search_cfg(opponent.algo)
    cfg.deterministic = bool(deterministic)
    agent = build_eval_agent(algo=opponent.algo, policy_state=opponent.policy_state,
                             contract=opponent.contract, len_model=len_model, cfg=cfg)
    return agent.as_policy_fn(env, "enemy")
```

- [ ] **Step 6: Прогнать симметрию + smoke eval**

Run: `python -m pytest tests/test_eval_honest_symmetry.py tests/test_eval_stratagem_metric.py -v`
Expected: PASS. Затем smoke: `python -m pytest tests/ -k eval -q` — без регрессий.

- [ ] **Step 7: Коммит**

```bash
git add eval.py core/models/opponent_adapter.py tests/test_eval_honest_symmetry.py
git commit -m "refactor(eval): обе стороны через EvalAgent + симметричный reaction-словарь"
```

---

### Task 6: Double-header (`--swap-sides`) + per-color агрегация

Новый CLI-флаг: каждую пару агентов играем двумя назначениями (A=model/B=enemy и swap), теги по «цвету», репорт per-color + усреднённо. Каждое назначение — полный набор из N игр (итого 2N).

**Files:**
- Modify: `eval.py` — argparse (флаг `--swap-sides`), игровой цикл (`1465-...`), агрегация/репорт
- Test: `tests/test_eval_swap_sides.py`

**Interfaces:**
- Consumes: `build_eval_agent`, `run_episode`.
- Produces: функция `_run_assignment(env, p1_agent, p2_agent, games, ...) -> dict` (winrate/vp по «цвету»); агрегатор `_aggregate_swap(res_a, res_b) -> dict`.

- [ ] **Step 1: Написать падающий тест агрегатора**

`tests/test_eval_swap_sides.py`:

```python
from eval import _aggregate_swap


def test_aggregate_swap_averages_per_color():
    # Назначение A: agentA как model выиграл 6/10; назначение B (swap): agentA как enemy выиграл 4/10.
    res_a = {"model_wins": 6, "enemy_wins": 4, "draws": 0, "games": 10}
    res_b = {"model_wins": 5, "enemy_wins": 5, "draws": 0, "games": 10}
    agg = _aggregate_swap(res_a, res_b)
    # agentA winrate = (model в A + enemy в B) / 2N = (6 + 5) / 20
    assert abs(agg["agentA_winrate"] - 11 / 20) < 1e-9
    assert abs(agg["agentB_winrate"] - 9 / 20) < 1e-9
    assert agg["total_games"] == 20
```

- [ ] **Step 2: Прогнать — убедиться, что падает**

Run: `python -m pytest tests/test_eval_swap_sides.py -v`
Expected: FAIL (`_aggregate_swap` не определён).

- [ ] **Step 3: Реализовать агрегатор + флаг + второй прогон**

В `eval.py` добавить:
```python
def _aggregate_swap(res_a: dict, res_b: dict) -> dict:
    """res_a: A=model/B=enemy; res_b: B=model/A=enemy. Winrate агента = его победы в обоих назначениях / 2N."""
    n = int(res_a["games"]) + int(res_b["games"])
    a_wins = int(res_a["model_wins"]) + int(res_b["enemy_wins"])
    b_wins = int(res_a["enemy_wins"]) + int(res_b["model_wins"])
    return {"agentA_winrate": a_wins / n if n else 0.0,
            "agentB_winrate": b_wins / n if n else 0.0,
            "total_games": n, "draws": int(res_a["draws"]) + int(res_b["draws"])}
```
Argparse: добавить `parser.add_argument("--swap-sides", action="store_true", help="Сыграть оба назначения сторон и усреднить (честный P1≡P2).")`.
Игровой цикл вынести в `_run_assignment(env, learner_agent, opponent_agent, games, learner_side, ...)` (возвращает `{"model_wins","enemy_wins","draws","games", ...}`). Если `args.swap_sides` и есть opponent — прогнать дважды (второй раз поменяв местами `learner_agent`/`opponent_agent` и заново выставив симметричный reaction-словарь), затем `_aggregate_swap` и лог per-color.

- [ ] **Step 4: Прогнать — убедиться, что проходит**

Run: `python -m pytest tests/test_eval_swap_sides.py -v`
Expected: PASS.

- [ ] **Step 5: Коммит**

```bash
git add eval.py tests/test_eval_swap_sides.py
git commit -m "feat(eval): double-header --swap-sides + per-color агрегация (симметрия назначения)"
```

---

### Task 7: Чистка дублей + регрессионный прогон

Удаляем мёртвый код (старые `select_action_with_epsilon_*` learner-пути и продублированную в Task 4 конструкцию net), убеждаемся в зелёном полном прогоне.

**Files:**
- Modify: `eval.py` — удалить неиспользуемые `select_action_with_epsilon_ppo/_alphazero/_gumbel_muzero/_sampled_muzero` (`285-445`), если на них больше нет ссылок
- Modify: `core/models/opponent_adapter.py` — убрать дубль конструкции, оставив делегирование в `build_eval_agent`
- Test: полный прогон `tests/`

- [ ] **Step 1: Найти оставшиеся ссылки**

Run: `python -m pytest tests/ -q` (зафиксировать baseline до чистки).
Grep по `select_action_with_epsilon_ppo|_alphazero|_gumbel_muzero|_sampled_muzero` — если ссылок вне определения нет, удалять безопасно (DQN `select_action_with_epsilon` мог остаться для других путей — проверить отдельно).

- [ ] **Step 2: Удалить мёртвые функции**

Удалить тела перечисленных `select_action_with_epsilon_*` в `eval.py`, на которые не осталось ссылок. Конструкцию net в `opponent_adapter` свести к `build_eval_agent`.

- [ ] **Step 3: Полный регресс**

Run: `python -m pytest tests/ -q`
Expected: PASS (как baseline Step 1, без новых падений; ~198+ тестов).

- [ ] **Step 4: Коммит**

```bash
git add eval.py core/models/opponent_adapter.py
git commit -m "refactor(eval): чистка дублей action-path после унификации на EvalAgent"
```

---

## Self-Review

**Spec coverage:**
- §2 EvalAgent → Task 4. §2.1/2.2 интерфейс+per-algo → Task 4. §3 поток хода → Task 5. §4 единый конфиг → Task 3 (+ WARN в Task 5 Step 4). §5 insane_bravery → Task 2. §6 double-header → Task 6. §7 GMZ/SMZ legacy → Task 4 (`_reaction_net_for_algo` → None). §8 совместимость: DQN bridge side-generic → Task 1; загрузчики не тронуты (Task 4 reuse). §9 тесты: parity/symmetry → Task 5/4; insane_bravery → Task 2; конфиг → Task 3; swap → Task 6. §10 файлы/риски покрыты задачами 1-7. §11 out-of-scope не реализуем (GMZ/SMZ умный gate, opponent-modeling, train both-sides).
- **Пробел и его закрытие:** AZ-fight-plan у enemy раньше не строился — теперь `select_action` возвращает `getattr(search, "last_selected_fight_plan", None)` для активной стороны (Task 4 `_select_az`), а `as_policy_fn` прикрепляет его до фазы боя enemy (Task 4 + Task 5 Step 3).

**Placeholder scan:** Кодовые шаги содержат конкретный код; формулировки «теми же вызовами, что opponent_adapter.py:NNN» сопровождены точными ссылками строк и списком конструкторов — не плейсхолдер, а DRY-перенос.

**Type consistency:** `build_eval_agent(*, algo, policy_state, contract, len_model, cfg, device)` — единая сигнатура в Task 4/5/6. `select_action(env, side) -> (dict, dict|None)`, `as_policy_fn(env, side) -> Callable` — согласованы. `_aggregate_swap(res_a, res_b)` ключи `model_wins/enemy_wins/draws/games` — согласованы между Task 6 Step 1/3. `install_dqn_stratagem_policy(env, net_by_side, device)` — Task 1 и вызыватели.
