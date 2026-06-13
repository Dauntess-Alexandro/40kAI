# Gumbel AlphaZero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить отдельный режим обучения `gumbel_az` («Gumbel AlphaZero») — per-head Gumbel top-k + Sequential Halving (depth-1, оценка через реальный env-шаг) — с полной интеграцией (train/checkpoint/resume/registry/eval/play/GUI, 3 пресета), переиспользуя AZ learner-конвейер.

**Architecture:** `GumbelAlphaZeroSearch.run()` повторяет контракт `AlphaZeroFactorizedMCTS.run()` `(policy_targets, selected_actions, value)`, поэтому весь AZ learner/replay/checkpoint/resume переиспользуется без изменений; различается только бэкенд поиска у актёра. Сеть — `AlphaZeroPolicyValueNet` (policy+value, без dynamics). eval/play грузят модель как обычную AZ-сеть (greedy).

**Tech Stack:** Python 3.12, PyTorch, NumPy, Gymnasium, PySide6/QML. Спек: `docs/superpowers/specs/2026-06-13-gumbel-alphazero-design.md`.

> ⚠️ **Номера строк — до-правочные ориентиры, а не истина.** Внутри одного файла любая вставка/удаление сдвигает
> последующие номера (особенно в `train.py`: Task 3 Step 4 вставляет блок перед ~2885 → все номера ниже уезжают).
> **Перед каждой правкой ищи по якорной строке** (текст рядом с правкой), а не по номеру. Номера держим как
> грубый указатель «где примерно».

---

## File Structure

**Создаём:**
- `core/models/gumbel_alphazero_search.py` — ядро поиска `GumbelAlphaZeroSearch` + `GumbelAZSearchConfig`.
- `app/gui_qt/gaz_hyperparams_defaults.py` — дефолты/пресеты/группы/тултипы для GUI.
- `tests/models/test_gumbel_alphazero_search.py` — юнит-тесты ядра.
- `tests/engine/test_gumbel_az_integration.py` — интеграция (эпизод селфплея).
- `tests/engine/test_gumbel_az_ids.py` — id-хелперы + registry resolve.
- `tests/gui_qt/test_gaz_hyperparams_load.py` — загрузка/coercion GUI-гиперпараметров.

**Изменяем:**
- `core/models/alphazero_ids.py` — id `gumbel_az`, хелперы `is_gumbel_az_algo`, `is_alphazero_net_algo`, `gaz_section_for`.
- `core/engine/agent_registry.py` — `_VALID_AGENT_ALGOS`, `resolve_agent_algo` (meta-авторитет для gumbel_az).
- `hyperparams.json` — секция `"gumbel_az"`.
- `train.py` — env-блок `GAZ_*`, `_gaz_search_config`, фабрика бэкенда поиска, dispatch, checkpoint/sync naming.
- `eval.py`, `play.py`, `core/engine/game_controller.py`, `core/models/opponent_adapter.py` — гейты `is_az_algo` → `is_alphazero_net_algo` там, где это «семейство сети».
- `app/gui_qt/main.py` — состояние/слоты/проперти/env для `gumbel_az`.
- `app/gui_qt/qml/Main.qml` — dropdown + вкладка настроек.
- `app/gui_qt/qml/components/SectionHyperparamsEditor.qml` — ветка `algoSection === "gaz"`.
- `app/gui_qt/qml/components/TrainingAlgoHelpDialog.qml` — карточка-справка.

---

## Task 1: id-хелперы `gumbel_az`

**Files:**
- Modify: `core/models/alphazero_ids.py`
- Test: `tests/engine/test_gumbel_az_ids.py`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_gumbel_az_ids.py
from core.models.alphazero_ids import (
    VALID_TRAIN_ALGOS,
    is_gumbel_az_algo,
    is_alphazero_net_algo,
    is_az_algo,
    gaz_section_for,
)


def test_gumbel_az_in_valid_train_algos():
    assert "gumbel_az" in VALID_TRAIN_ALGOS


def test_is_gumbel_az_algo():
    assert is_gumbel_az_algo("gumbel_az")
    assert not is_gumbel_az_algo("alphazero_tree")
    assert not is_gumbel_az_algo("")


def test_is_alphazero_net_family():
    # gumbel_az шарит AZ-сеть и формат чекпойнта
    assert is_alphazero_net_algo("alphazero_tree")
    assert is_alphazero_net_algo("alphazero_proxy")
    assert is_alphazero_net_algo("gumbel_az")
    assert not is_alphazero_net_algo("dqn")
    assert not is_alphazero_net_algo("gumbel_muzero")


def test_gumbel_az_is_not_az_puct_algo():
    # is_az_algo остаётся строго для PUCT tree/proxy
    assert not is_az_algo("gumbel_az")


def test_gaz_section_for():
    assert gaz_section_for("gumbel_az") == "gumbel_az"
```

- [ ] **Step 2: Запустить — упадёт (ImportError)**

Run: `python -m pytest tests/engine/test_gumbel_az_ids.py -v`
Expected: FAIL — `ImportError: cannot import name 'is_gumbel_az_algo'`.

- [ ] **Step 3: Реализация в `core/models/alphazero_ids.py`**

Заменить строку 5 (`VALID_TRAIN_ALGOS = ...`):

```python
VALID_TRAIN_ALGOS = frozenset(
    {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az", "distill"}
)
VALID_AZ_ALGOS = frozenset({"alphazero_tree", "alphazero_proxy"})
GUMBEL_AZ_ALGO = "gumbel_az"
LEGACY_AZ_ALGO = "alphazero"
```

Добавить в конец файла:

```python
def is_gumbel_az_algo(algo: str) -> bool:
    return str(algo or "").strip().lower() == GUMBEL_AZ_ALGO


def is_alphazero_net_algo(algo: str) -> bool:
    """True для алгоритмов, использующих AlphaZeroPolicyValueNet и AZ-формат чекпойнта
    (ключ policy_value_net): alphazero_tree, alphazero_proxy, gumbel_az."""
    key = str(algo or "").strip().lower()
    return key in VALID_AZ_ALGOS or key == GUMBEL_AZ_ALGO


def gaz_section_for(algo: str) -> str:
    key = str(algo or "").strip().lower()
    if key != GUMBEL_AZ_ALGO:
        raise ValueError(f"expected gumbel_az, got {algo!r}")
    return key
```

- [ ] **Step 4: Запустить — должно пройти**

Run: `python -m pytest tests/engine/test_gumbel_az_ids.py -v`
Expected: PASS (5 тестов).

- [ ] **Step 5: Коммит**

```bash
git add core/models/alphazero_ids.py tests/engine/test_gumbel_az_ids.py
git commit -m "feat(gumbel_az): id-хелперы и семейный is_alphazero_net_algo"
```

---

## Task 2: Поисковое ядро `GumbelAlphaZeroSearch`

**Files:**
- Create: `core/models/gumbel_alphazero_search.py`
- Test: `tests/models/test_gumbel_alphazero_search.py`

Контракт `run()` (как у AZ): `run(*, obs, legal_masks_by_head, temperature=1.0, env=None, len_model=None, enemy_policy_fn=None, reset_options=None, move_count=None, progress=None) -> (policy_targets: list[np.ndarray], selected_actions: list[int], value: float)`.

- [ ] **Step 1: Написать падающие юнит-тесты**

```python
# tests/models/test_gumbel_alphazero_search.py
import numpy as np
import torch

from core.models.gumbel_alphazero_search import (
    GumbelAlphaZeroSearch,
    GumbelAZSearchConfig,
    sequential_halving_keep_schedule,
)


class _StubNet:
    """policy = uniform логиты, value = const. Совместим с net.infer()."""

    def __init__(self, action_sizes, value=0.0):
        self.action_sizes = action_sizes
        self._value = float(value)

    @torch.no_grad()
    def infer(self, obs, masks_by_head=None):
        b = obs.shape[0]
        probs = []
        for i, n in enumerate(self.action_sizes):
            p = torch.full((b, n), 1.0 / n)
            probs.append(p)
        value = torch.full((b,), self._value)
        return probs, value


def test_keep_schedule_halves_to_one():
    sched = sequential_halving_keep_schedule(m=8)
    assert sched[0] == 8
    assert sched[-1] == 1
    # монотонно невозрастающая, делит пополам
    for a, b in zip(sched, sched[1:]):
        assert b <= a


def test_run_returns_az_contract_no_env():
    # depth-1 без env: оценка кандидатов через net-value на корне (terminal None → root value)
    net = _StubNet([5, 3], value=0.2)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([1, 1, 1, 0, 0], dtype=bool), np.array([1, 1, 0], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=0.0,
        env=None,
        len_model=None,
    )
    assert len(pi) == 2 and len(actions) == 2
    for head_pi, head_legal in zip(pi, legal):
        assert head_pi.shape == head_legal.shape
        assert np.all(head_pi[~head_legal] == 0.0)
        assert abs(float(head_pi.sum()) - 1.0) < 1e-5
        assert np.all(head_pi >= 0.0)
    assert -1.0 <= value <= 1.0
    # выбранные действия — только легальные
    for a, head_legal in zip(actions, legal):
        assert bool(head_legal[a])


def test_head_without_legal_actions_uniform_fallback():
    net = _StubNet([4], value=0.0)
    cfg = GumbelAZSearchConfig(num_simulations=4, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([0, 0, 0, 0], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert abs(float(pi[0].sum()) - 1.0) < 1e-5
    assert not np.any(np.isnan(pi[0]))


def test_nan_priors_fallback_uniform():
    class _NanNet(_StubNet):
        @torch.no_grad()
        def infer(self, obs, masks_by_head=None):
            probs, value = super().infer(obs, masks_by_head)
            probs[0] = probs[0] * float("nan")
            return probs, value

    net = _NanNet([4], value=0.0)
    cfg = GumbelAZSearchConfig(num_simulations=4, num_considered_actions=4, simulate_enemy=False)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    legal = [np.array([1, 1, 1, 1], dtype=bool)]
    pi, actions, value = search.run(
        obs=np.zeros(7, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert not np.any(np.isnan(pi[0]))
    assert abs(float(pi[0].sum()) - 1.0) < 1e-5


def test_deterministic_with_seed():
    net = _StubNet([6], value=0.1)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=False)
    legal = [np.array([1, 1, 1, 1, 1, 0], dtype=bool)]
    obs = np.zeros(7, dtype=np.float32)

    np.random.seed(123)
    s1 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    pi1, a1, _ = s1.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    np.random.seed(123)
    s2 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    pi2, a2, _ = s2.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    assert a1 == a2
    assert np.allclose(pi1[0], pi2[0])
```

- [ ] **Step 2: Запустить — упадёт (ModuleNotFoundError)**

Run: `python -m pytest tests/models/test_gumbel_alphazero_search.py -v`
Expected: FAIL — модуль `core.models.gumbel_alphazero_search` не существует.

- [ ] **Step 3: Реализация `core/models/gumbel_alphazero_search.py`**

```python
from __future__ import annotations

import math
from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.alphazero_mcts import EvalCache, _masked_normalize
from core.models.utils import unwrap_env


@dataclass
class GumbelAZSearchConfig:
    num_simulations: int = 32          # бюджет SH на голову
    num_considered_actions: int = 8    # m: размер Gumbel top-k
    max_depth: int = 1                 # v1 = 1 (задел под дерево)
    value_scale: float = 0.1           # c_scale в sigma(q)
    c_visit: float = 50.0              # c_visit в sigma(q)
    temperature_opening_moves: int = 12
    eval_cache_size: int = 10000
    batch_eval_size: int = 16
    simulate_enemy: bool = True
    mode: str = "gumbel"


def sequential_halving_keep_schedule(m: int) -> list[int]:
    """Сколько кандидатов остаётся после каждой фазы SH (включая старт m и финал 1)."""
    m = max(1, int(m))
    sched = [m]
    k = m
    while k > 1:
        k = max(1, k // 2)
        sched.append(k)
    return sched


def _sigma(q: np.ndarray, *, c_visit: float, value_scale: float, max_visit: float) -> np.ndarray:
    return (float(c_visit) + float(max_visit)) * float(value_scale) * np.asarray(q, dtype=np.float32)


def _terminal_value_from_info(info: dict[str, Any]) -> Optional[float]:
    winner = str((info or {}).get("winner", "") or "").strip().lower()
    end_reason = str((info or {}).get("end reason", "") or "").strip().lower()
    if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
        return 1.0
    if winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
        return -1.0
    if str(end_reason).startswith("turn_limit"):
        return 0.0
    return None


class GumbelAlphaZeroSearch:
    """Gumbel AlphaZero, вариант A: per-head Gumbel top-k + Sequential Halving, depth-1.

    Кандидаты оцениваются через реальный env-шаг (+ ход врага) и value-сеть.
    Контракт run() совпадает с AlphaZeroFactorizedMCTS.run() — drop-in для актёра.

    evaluator: опционально (LocalNetEvaluator/RemoteEvaluator) — тот же шов, что у AZ
      MCTS; None → self.net.infer + внутренний EvalCache.
    """

    def __init__(self, policy_value_net, config: GumbelAZSearchConfig | None = None,
                 device: torch.device | None = None, *, evaluator=None):
        self.net = policy_value_net
        self.cfg = config or GumbelAZSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}
        self._eval_cache = EvalCache(max_size=int(getattr(self.cfg, "eval_cache_size", 10000) or 10000))
        self._evaluator = evaluator

    # --- net eval (reuse evaluator seam) ---
    def _evaluate_net(self, obs: np.ndarray, legal_masks_by_head: list[np.ndarray]):
        if self._evaluator is not None:
            return self._evaluator.evaluate_one(obs, legal_masks_by_head)
        cached = self._eval_cache.get(obs, legal_masks_by_head)
        if cached is not None:
            return cached
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        priors = [p.squeeze(0).detach().cpu().numpy().astype(np.float32) for p in priors_t]
        value = float(value_t.reshape(-1)[0].item())
        self._eval_cache.set(obs, legal_masks_by_head, priors, value)
        return priors, value

    def _evaluate_value_batch(self, leaves: list[dict]) -> list[float]:
        if self._evaluator is not None:
            return self._evaluator.evaluate_batch(leaves)
        n = len(leaves)
        if n == 0:
            return []
        values: list[Optional[float]] = [None] * n
        uncached: list[int] = []
        for i, leaf in enumerate(leaves):
            c = self._eval_cache.get(leaf["obs"], leaf["legal_masks"])
            if c is not None:
                values[i] = float(c[1])
            else:
                uncached.append(i)
        if uncached:
            obs_batch = np.stack([leaves[i]["obs"] for i in uncached])
            obs_t = torch.tensor(obs_batch, dtype=torch.float32, device=self.device)
            num_heads = len(leaves[uncached[0]]["legal_masks"])
            masks_t = []
            for h in range(num_heads):
                hm = np.stack([np.asarray(leaves[i]["legal_masks"][h], dtype=bool) for i in uncached])
                masks_t.append(torch.as_tensor(hm, dtype=torch.bool, device=self.device))
            with torch.no_grad():
                priors_t, values_t = self.net.infer(obs_t, masks_by_head=masks_t)
            for j, i in enumerate(uncached):
                priors_np = [priors_t[h][j].detach().cpu().numpy().astype(np.float32) for h in range(num_heads)]
                val = float(values_t.reshape(-1)[j].item())
                self._eval_cache.set(leaves[i]["obs"], leaves[i]["legal_masks"], priors_np, val)
                values[i] = val
        return [float(v if v is not None else 0.0) for v in values]

    def _restore_env_safe(self, env_u, snapshot, reset_options) -> None:
        if snapshot is None:
            return
        try:
            if hasattr(env_u, "restore_state"):
                env_u.restore_state(snapshot)
                return
        except Exception:
            pass
        try:
            if hasattr(env_u, "reset") and reset_options is not None:
                env_u.reset(options=reset_options)
        except Exception:
            pass

    def _rollout_leaf(self, *, env, env_u, snapshot, action_list, len_model, ordered_keys,
                      enemy_policy_fn, reset_options) -> dict:
        """Один depth-1 env-шаг action_list (+ход врага). Возвращает leaf dict.

        leaf: {obs, legal_masks, terminal_value(None|float), needs_net_eval(bool)}.
        Гарантированно восстанавливает env в исходное состояние (snapshot).
        """
        leaf = {"obs": np.asarray([], dtype=np.float32), "legal_masks": [],
                "terminal_value": None, "needs_net_eval": False}
        sim_ctx = env_u.simulation_mode() if hasattr(env_u, "simulation_mode") else nullcontext(env_u)
        with sim_ctx:
            try:
                action_dict = action_tensor_to_dict(
                    torch.tensor([list(action_list)], dtype=torch.long), len_model=int(len_model)
                )
                next_obs, _r, done, trunc, info = env.step(action_dict)
                if not bool(done or trunc) and bool(self.cfg.simulate_enemy):
                    env_u.enemyTurn(trunc=False, policy_fn=enemy_policy_fn)
                    done = bool(getattr(env_u, "game_over", False))
                    info = env_u.get_info()
                term = _terminal_value_from_info(info or {})
                leaf["obs"] = np.asarray(next_obs, dtype=np.float32)
                if term is not None or bool(done or trunc):
                    leaf["terminal_value"] = float(term if term is not None else 0.0)
                else:
                    legal_dict = env_u.get_legal_action_masks_by_head(side="model")
                    leaf["legal_masks"] = [legal_dict[k] for k in ordered_keys]
                    leaf["needs_net_eval"] = True
            finally:
                self._restore_env_safe(env_u, snapshot, reset_options)
        return leaf

    def _search_head(self, *, head_idx, base_action, legal, prior, root_value, leaf_eval_fn):
        """SH по одной голове. leaf_eval_fn(action_list)->q (через env) или None (нет env).

        Возвращает (pi: np.ndarray, selected_action: int).
        """
        legal = np.asarray(legal, dtype=bool)
        legal_idx = np.where(legal)[0]
        prior = _masked_normalize(prior, legal)
        logits = np.log(np.clip(prior, 1e-12, 1.0)).astype(np.float32)

        if legal_idx.size <= 1:
            a = int(legal_idx[0]) if legal_idx.size == 1 else 0
            return prior.astype(np.float32), a

        # Gumbel top-m
        g = np.random.gumbel(size=legal.size).astype(np.float32)
        g_legal = np.where(legal, g, np.float32(-1e30))
        base_score = logits + g_legal
        m = int(min(int(self.cfg.num_considered_actions), legal_idx.size))
        order = legal_idx[np.argsort(base_score[legal_idx])[::-1]]
        candidates = list(order[:m])

        visits = np.zeros(legal.size, dtype=np.float32)
        q_sums = np.zeros(legal.size, dtype=np.float32)
        n = max(1, int(self.cfg.num_simulations))
        schedule = sequential_halving_keep_schedule(m)
        phases = max(1, len(schedule) - 1)

        remaining = list(candidates)
        for phase in range(phases):
            per = max(1, n // (phases * max(1, len(remaining))))
            for a in remaining:
                for _ in range(per):
                    action_vec = list(base_action)
                    action_vec[head_idx] = int(a)
                    q = leaf_eval_fn(action_vec)
                    if q is None:
                        q = float(root_value)
                    visits[int(a)] += 1.0
                    q_sums[int(a)] += float(q)
            # ранжируем выживших по g+logit+sigma(qhat)
            keep = schedule[phase + 1]
            qmean = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), float(root_value))
            qn = _normalize01(qmean, remaining)
            max_visit = float(visits.max()) if visits.size else 0.0
            score = base_score + _sigma(qn, c_visit=self.cfg.c_visit,
                                        value_scale=self.cfg.value_scale, max_visit=max_visit)
            remaining = sorted(remaining, key=lambda a: float(score[int(a)]), reverse=True)[:keep]

        winner = int(remaining[0])

        # completed-Q policy target по всем легальным
        qmean_all = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), float(root_value))
        completed = _normalize01(qmean_all, list(legal_idx))
        max_visit = float(visits.max()) if visits.size else 0.0
        target_logits = logits + _sigma(completed, c_visit=self.cfg.c_visit,
                                        value_scale=self.cfg.value_scale, max_visit=max_visit)
        target_logits = np.where(legal, target_logits, np.float32(-1e30))
        target_logits = target_logits - np.max(target_logits[legal])
        pi = np.exp(target_logits).astype(np.float32)
        pi[~legal] = 0.0
        pi = _masked_normalize(pi, legal)
        return pi, winner

    @torch.no_grad()
    def run(self, *, obs, legal_masks_by_head, temperature: float = 1.0, env=None,
            len_model: Optional[int] = None, enemy_policy_fn=None, reset_options=None,
            move_count: int | None = None, progress: float | None = None):
        legal_masks = [np.asarray(m, dtype=bool) for m in legal_masks_by_head]
        priors, root_value = self._evaluate_net(obs=np.asarray(obs, dtype=np.float32),
                                                legal_masks_by_head=legal_masks)
        num_heads = len(priors)
        base_action = [int(np.argmax(np.where(legal_masks[i], priors[i], -1e30)))
                       for i in range(num_heads)]

        env_u = unwrap_env(env) if env is not None else None
        ordered_keys = ordered_action_keys(int(len_model)) if (env is not None and len_model is not None) else []
        use_env = env is not None and len_model is not None and env_u is not None and hasattr(env_u, "snapshot_state")

        def _make_leaf_eval():
            if not use_env:
                return lambda action_vec: float(root_value)

            def _eval(action_vec):
                snap = env_u.snapshot_state()
                leaf = self._rollout_leaf(
                    env=env, env_u=env_u, snapshot=snap, action_list=action_vec,
                    len_model=int(len_model), ordered_keys=ordered_keys,
                    enemy_policy_fn=enemy_policy_fn, reset_options=reset_options,
                )
                if leaf["terminal_value"] is not None:
                    return float(leaf["terminal_value"])
                vals = self._evaluate_value_batch([leaf])
                return float(vals[0]) if vals else float(root_value)

            return _eval

        leaf_eval_fn = _make_leaf_eval()

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        for h in range(num_heads):
            pi, a = self._search_head(
                head_idx=h, base_action=base_action, legal=legal_masks[h],
                prior=priors[h], root_value=root_value, leaf_eval_fn=leaf_eval_fn,
            )
            # дебютная стохастика: сэмпл из улучшенной политики
            opening = int(getattr(self.cfg, "temperature_opening_moves", 12) or 12)
            if move_count is not None and int(move_count) < opening and float(temperature) > 1e-3:
                a = int(np.random.choice(np.arange(pi.size), p=pi))
            policy_targets.append(pi.astype(np.float32))
            selected_actions.append(int(a))

        self.last_run_stats = {
            "mode": 1.0,
            "simulations": float(self.cfg.num_simulations),
            "root_value": float(root_value),
            "eval_cache_hits": float(self._eval_cache.hits),
            "eval_cache_misses": float(self._eval_cache.misses),
        }
        return policy_targets, selected_actions, float(root_value)


def _normalize01(values: np.ndarray, idx_subset: list[int]) -> np.ndarray:
    """Min-max нормировка значений по подмножеству индексов в [0,1] (для sigma)."""
    out = np.zeros_like(values, dtype=np.float32)
    if not idx_subset:
        return out
    sub = np.asarray([values[int(i)] for i in idx_subset], dtype=np.float32)
    lo = float(np.min(sub))
    hi = float(np.max(sub))
    rng = hi - lo
    if rng <= 1e-9:
        for i in idx_subset:
            out[int(i)] = 0.5
        return out
    for i in idx_subset:
        out[int(i)] = (float(values[int(i)]) - lo) / rng
    return out
```

- [ ] **Step 4: Запустить — должно пройти**

Run: `python -m pytest tests/models/test_gumbel_alphazero_search.py -v`
Expected: PASS (5 тестов).

- [ ] **Step 5: Линт + коммит**

```bash
ruff check --fix core/models/gumbel_alphazero_search.py
git add core/models/gumbel_alphazero_search.py tests/models/test_gumbel_alphazero_search.py
git commit -m "feat(gumbel_az): поисковое ядро GumbelAlphaZeroSearch (per-head Gumbel + SH, depth-1)"
```

---

## Task 3: Интеграция в `train.py` (config, backend factory, dispatch, checkpoint/sync)

**Files:**
- Modify: `train.py`

> Контракт `run()` у Gumbel-поиска совпадает с AZ → learner/replay/`train_alphazero_step`/checkpoint/resume переиспользуются. Меняем: импорт, выбор секции hyperparams, режим, env-блок `GAZ_*`, фабрику бэкенда, dispatch, sync-тег. Spawn-сигнатуры **не меняем** — gaz-параметры едут в существующем dict `mcts_cfg_payload`.

- [ ] **Step 1: Импорт id-хелперов**

Найти строку импорта из `core.models.alphazero_ids` (рядом с использованием `is_az_algo`, `az_section_for`, `az_mcts_mode_for`) и добавить новые имена:

```python
from core.models.alphazero_ids import (
    is_az_algo,
    is_gumbel_az_algo,
    is_alphazero_net_algo,
    az_section_for,
    az_mcts_mode_for,
    az_mcts_mode_from_payload,
    VALID_TRAIN_ALGOS,
)
```
(сохранить те имена, что уже импортируются; добавить `is_gumbel_az_algo`, `is_alphazero_net_algo`.)

- [ ] **Step 2: Выбор секции hyperparams для gumbel_az**

`train.py:2544` — заменить:

```python
_AZ_HP_SECTION = az_section_for(TRAIN_ALGO) if is_az_algo(TRAIN_ALGO) else "alphazero_tree"
```
на:
```python
if is_az_algo(TRAIN_ALGO):
    _AZ_HP_SECTION = az_section_for(TRAIN_ALGO)
elif is_gumbel_az_algo(TRAIN_ALGO):
    _AZ_HP_SECTION = "gumbel_az"
else:
    _AZ_HP_SECTION = "alphazero_tree"
```

- [ ] **Step 3: Режим для gumbel_az**

`train.py:2558-2563` — заменить блок:

```python
if is_az_algo(TRAIN_ALGO):
    AZ_MCTS_MODE = az_mcts_mode_for(TRAIN_ALGO)
else:
    AZ_MCTS_MODE = str(AZ_CFG.get("mcts_mode", "tree")).strip().lower() or "tree"
if AZ_MCTS_MODE not in {"proxy", "tree"}:
    AZ_MCTS_MODE = "tree"
```
на:
```python
if is_az_algo(TRAIN_ALGO):
    AZ_MCTS_MODE = az_mcts_mode_for(TRAIN_ALGO)
elif is_gumbel_az_algo(TRAIN_ALGO):
    AZ_MCTS_MODE = "gumbel"
else:
    AZ_MCTS_MODE = str(AZ_CFG.get("mcts_mode", "tree")).strip().lower() or "tree"
if AZ_MCTS_MODE not in {"proxy", "tree", "gumbel"}:
    AZ_MCTS_MODE = "tree"
```

- [ ] **Step 4: Env-блок `GAZ_*` + `_gaz_search_config` + фабрика бэкенда**

Вставить ПОСЛЕ `def _az_honest_eval_mcts_config(...)` (заканчивается на `train.py:2882`), ПЕРЕД `GMZ_CFG = data.get("gumbel_muzero", {})` (`train.py:2885`):

```python
# --- Gumbel AlphaZero (gumbel_az) search config ---
GAZ_CFG = data.get("gumbel_az", {}) if isinstance(data, dict) else {}
GAZ_NUM_SIMS = max(1, int(os.getenv("GAZ_NUM_SIMULATIONS", str(GAZ_CFG.get("num_simulations", 32)))))
GAZ_NUM_CONSIDERED = max(2, int(os.getenv("GAZ_NUM_CONSIDERED_ACTIONS", str(GAZ_CFG.get("num_considered_actions", 8)))))
GAZ_MAX_DEPTH = max(1, int(os.getenv("GAZ_MAX_DEPTH", str(GAZ_CFG.get("max_depth", 1)))))
GAZ_VALUE_SCALE = float(os.getenv("GAZ_VALUE_SCALE", str(GAZ_CFG.get("value_scale", 0.1))))
GAZ_C_VISIT = float(os.getenv("GAZ_C_VISIT", str(GAZ_CFG.get("c_visit", 50.0))))
GAZ_SIMULATE_ENEMY = str(os.getenv("GAZ_SIMULATE_ENEMY", str(GAZ_CFG.get("simulate_enemy", 1)))).strip() == "1"
GAZ_EVAL_CACHE_SIZE = int(os.getenv("GAZ_EVAL_CACHE_SIZE", str(GAZ_CFG.get("eval_cache_size", 10000))))
GAZ_BATCH_EVAL_SIZE = max(1, int(os.getenv("GAZ_BATCH_EVAL_SIZE", str(GAZ_CFG.get("batch_eval_size", 16)))))


def _gaz_cfg_payload() -> dict:
    return {
        "num_simulations": GAZ_NUM_SIMS,
        "num_considered_actions": GAZ_NUM_CONSIDERED,
        "max_depth": GAZ_MAX_DEPTH,
        "value_scale": GAZ_VALUE_SCALE,
        "c_visit": GAZ_C_VISIT,
        "simulate_enemy": GAZ_SIMULATE_ENEMY,
        "eval_cache_size": GAZ_EVAL_CACHE_SIZE,
        "batch_eval_size": GAZ_BATCH_EVAL_SIZE,
    }


def _build_az_search(net, payload: dict, device, *, evaluator=None):
    """Фабрика бэкенда поиска для AZ-семейства актёров.

    gumbel_az → GumbelAlphaZeroSearch; alphazero_tree/proxy → AlphaZeroFactorizedMCTS.
    payload — это dict, что уже едет в актёр (mcts_cfg_payload). Для gumbel_az он
    содержит gaz-поля (см. _gaz_cfg_payload), для AZ — mcts-поля.
    """
    if is_gumbel_az_algo(TRAIN_ALGO):
        from core.models.gumbel_alphazero_search import GumbelAlphaZeroSearch, GumbelAZSearchConfig
        return GumbelAlphaZeroSearch(
            net,
            config=GumbelAZSearchConfig(
                num_simulations=int(payload.get("num_simulations", GAZ_NUM_SIMS)),
                num_considered_actions=int(payload.get("num_considered_actions", GAZ_NUM_CONSIDERED)),
                max_depth=int(payload.get("max_depth", GAZ_MAX_DEPTH)),
                value_scale=float(payload.get("value_scale", GAZ_VALUE_SCALE)),
                c_visit=float(payload.get("c_visit", GAZ_C_VISIT)),
                temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
                eval_cache_size=int(payload.get("eval_cache_size", GAZ_EVAL_CACHE_SIZE)),
                batch_eval_size=int(payload.get("batch_eval_size", GAZ_BATCH_EVAL_SIZE)),
                simulate_enemy=bool(payload.get("simulate_enemy", GAZ_SIMULATE_ENEMY)),
            ),
            device=device,
            evaluator=evaluator,
        )
    return AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(
            simulations=int(payload.get("simulations", AZ_MCTS_SIMS)),
            c_puct=float(payload.get("c_puct", AZ_C_PUCT)),
            c_puct_min=float(payload.get("c_puct_min", AZ_C_PUCT_MIN)),
            c_puct_max=float(payload.get("c_puct_max", AZ_C_PUCT_MAX)),
            c_puct_schedule=str(payload.get("c_puct_schedule", AZ_C_PUCT_SCHEDULE)),
            dirichlet_alpha=float(payload.get("dirichlet_alpha", AZ_DIR_ALPHA)),
            dirichlet_eps=float(payload.get("dirichlet_eps", AZ_DIR_EPS)),
            top_k_per_head=int(payload.get("top_k_per_head", AZ_MCTS_TOP_K_PER_HEAD)),
            max_depth=int(payload.get("max_depth", AZ_MCTS_MAX_DEPTH)),
            mode=str(payload.get("mode", AZ_MCTS_MODE)),
            root_dirichlet_only=bool(payload.get("root_dirichlet_only", AZ_MCTS_ROOT_DIRICHLET_ONLY)),
            eval_cache_size=int(payload.get("eval_cache_size", AZ_MCTS_EVAL_CACHE_SIZE)),
            pw_alpha=float(payload.get("pw_alpha", AZ_PW_ALPHA)),
            pw_beta=float(payload.get("pw_beta", AZ_PW_BETA)),
            prior_weight_early=float(payload.get("prior_weight_early", AZ_PRIOR_WEIGHT_EARLY)),
            temperature_opening_moves=int(AZ_TEMP_OPENING_MOVES),
            batch_eval_size=int(payload.get("batch_eval_size", AZ_MCTS_BATCH_EVAL_SIZE)),
            parallel_simulations=int(payload.get("parallel_simulations", AZ_MCTS_PARALLEL_SIMS)),
            simulate_enemy_in_tree=bool(payload.get("simulate_enemy_in_tree", AZ_MCTS_SIMULATE_ENEMY)),
        ),
        device=device,
        evaluator=evaluator,
    )
```

- [ ] **Step 5: Использовать фабрику в actor-entry (variant A)**

`train.py:8423-8447` — заменить блок `mcts = AlphaZeroFactorizedMCTS(...)` на:

```python
        mcts = _build_az_search(az_net, mcts_cfg_payload, cpu_device)
```
(весь явный `MCTSConfig(...)` теперь внутри `_build_az_search`.)

- [ ] **Step 6: Использовать фабрику в env-worker (variant B, inference server)**

В `_az_env_worker_entry` (около `train.py:8701-8726`) аналогично заменить инлайновое создание `AlphaZeroFactorizedMCTS(... evaluator=...)` на:

```python
        mcts = _build_az_search(net, mcts_cfg_payload, worker_device, evaluator=evaluator)
```
(имя переменной net/evaluator/device — как в текущем env-worker; сохранить их.)

- [ ] **Step 7: Наполнить payload gaz-полями для gumbel_az**

`train.py:9123-9142` — где строится `_mcts_cfg_payload`, обернуть в выбор:

```python
    if is_gumbel_az_algo(TRAIN_ALGO):
        _mcts_cfg_payload = _gaz_cfg_payload()
    else:
        _mcts_cfg_payload = {
            "simulations": AZ_MCTS_SIMS,
            "c_puct": AZ_C_PUCT,
            "dirichlet_alpha": AZ_DIR_ALPHA,
            "dirichlet_eps": AZ_DIR_EPS,
            "top_k_per_head": AZ_MCTS_TOP_K_PER_HEAD,
            "max_depth": AZ_MCTS_MAX_DEPTH,
            "mode": AZ_MCTS_MODE,
            "root_dirichlet_only": AZ_MCTS_ROOT_DIRICHLET_ONLY,
            "eval_cache_size": AZ_MCTS_EVAL_CACHE_SIZE,
            "c_puct_min": AZ_C_PUCT_MIN,
            "c_puct_max": AZ_C_PUCT_MAX,
            "c_puct_schedule": AZ_C_PUCT_SCHEDULE,
            "pw_alpha": AZ_PW_ALPHA,
            "pw_beta": AZ_PW_BETA,
            "prior_weight_early": AZ_PRIOR_WEIGHT_EARLY,
            "batch_eval_size": AZ_MCTS_BATCH_EVAL_SIZE,
            "parallel_simulations": AZ_MCTS_PARALLEL_SIMS,
            "simulate_enemy_in_tree": AZ_MCTS_SIMULATE_ENEMY,
        }
```

- [ ] **Step 8: Sync-тег для gumbel_az (2 места)**

`train.py:8463` и `train.py:9078` — заменить:

```python
        _az_sync_tag = "tree" if TRAIN_ALGO == "alphazero_tree" else "proxy"
```
на:
```python
        if TRAIN_ALGO == "alphazero_tree":
            _az_sync_tag = "tree"
        elif is_gumbel_az_algo(TRAIN_ALGO):
            _az_sync_tag = "gumbel_az"
        else:
            _az_sync_tag = "proxy"
```
(sync-файл станет `latest_az_gumbel_az_policy.pth` — учесть тот же тег в обоих местах, чтобы learner и актор совпали.)

- [ ] **Step 9: Dispatch в `main()` (2 точки)**

`train.py:3897` и `train.py:4231` — заменить условие `if is_az_algo(TRAIN_ALGO):` на:

```python
    if is_az_algo(TRAIN_ALGO) or is_gumbel_az_algo(TRAIN_ALGO):
```
(оба входа ведут в `_main_actor_learner_alphazero`, что и нужно.)

- [ ] **Step 10: Проверить чекпойнт-папку**

`checkpoint_dir` строится как `os.path.join(MODELS_DIR, TRAIN_ALGO)` → для `gumbel_az` папка `artifacts/models/gumbel_az/` создастся сама. Подтвердить чтением определения `checkpoint_dir` в `_main_actor_learner_alphazero` (искать `checkpoint_dir =`). Если оно завязано на `AZ_MCTS_MODE` — оставить `TRAIN_ALGO`.

- [ ] **Step 11: Smoke import-тест**

Run: `python -c "import train"`
Expected: импорт без ошибок (env `TRAIN_ALGO` не задан → dqn-ветка, gaz-код не падает на import).

- [ ] **Step 12: Smoke `_gaz_search_config`/payload (без env)**

Run:
```bash
python -c "import os; os.environ['TRAIN_ALGO']='gumbel_az'; import importlib, train; importlib.reload(train); p=train._gaz_cfg_payload(); print(p['num_simulations'], p['num_considered_actions'])"
```
Expected: печатает значения из секции `gumbel_az` (после Task 5) или дефолты `32 8`.

- [ ] **Step 13: Коммит**

```bash
git add train.py
git commit -m "feat(gumbel_az): интеграция в train.py (GAZ_* config, backend factory, dispatch, sync-тег)"
```

---

## Task 4: Реестр агентов + eval/play/Viewer/opponent (`reuse`)

**Files:**
- Modify: `core/engine/agent_registry.py`, `eval.py`, `play.py`, `core/engine/game_controller.py`, `core/models/opponent_adapter.py`
- Test: дополнить `tests/engine/test_gumbel_az_ids.py`

- [ ] **Step 1: Падающий тест на resolve_agent_algo**

Добавить в `tests/engine/test_gumbel_az_ids.py`:

```python
def test_resolve_gumbel_az_meta_authoritative():
    # веса как у AlphaZero (policy_heads.*), но meta.algo=gumbel_az → gumbel_az
    from core.engine.agent_registry import resolve_agent_algo
    policy_state = {"policy_heads.0.weight": [[0.0]], "input_fc.weight": [[0.0]]}
    algo = resolve_agent_algo(
        meta={"algo": "gumbel_az"}, policy_state=policy_state, agent_id="t"
    )
    assert algo == "gumbel_az"


def test_resolve_az_meta_still_tree():
    from core.engine.agent_registry import resolve_agent_algo
    policy_state = {"policy_heads.0.weight": [[0.0]]}
    algo = resolve_agent_algo(
        meta={"algo": "alphazero_tree", "mcts_mode": "tree"}, policy_state=policy_state, agent_id="t"
    )
    assert algo == "alphazero_tree"
```

- [ ] **Step 2: Запустить — упадёт**

Run: `python -m pytest tests/engine/test_gumbel_az_ids.py::test_resolve_gumbel_az_meta_authoritative -v`
Expected: FAIL — возвращается `alphazero_tree` (meta не учтена для gumbel_az).

- [ ] **Step 3: `agent_registry.py` — id + meta-авторитет**

`core/engine/agent_registry.py:199-201` — заменить:

```python
_VALID_AGENT_ALGOS = frozenset(
    {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}
)
```
на:
```python
_VALID_AGENT_ALGOS = frozenset(
    {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az"}
)
```

В `resolve_agent_algo`, после блока PPO (`core/engine/agent_registry.py:254-255`), добавить зеркальное правило для gumbel_az:

```python
        if resolved in {"alphazero_tree", "alphazero_proxy"} and meta_algo == "ppo":
            return "ppo"
        # gumbel_az шарит AZ-архитектуру (policy_heads/value_heads) — веса неотличимы
        # от AZ-tree; meta.algo авторитетна (её пишет тренер).
        if resolved in {"alphazero_tree", "alphazero_proxy"} and meta_algo == "gumbel_az":
            return "gumbel_az"
```

> Размещение важно: эта проверка должна идти **до** generic-блока `if meta_algo in _VALID_AGENT_ALGOS and
> meta_algo != resolved:` (он печатает WARN и возвращает веса = `alphazero_tree`). Ставим сразу после PPO-кейса,
> как и он.

- [ ] **Step 3b: `collect_registered_agents_meta` + текст ошибки**

В `core/engine/agent_registry.py` у `collect_registered_agents_meta` свой **отдельный** хардкод-вайтлист (~строка 379):
```python
        if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
```
→ добавить `"gumbel_az"`:
```python
        if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az"}:
```
Без этого `gumbel_az`-агенты будут отфильтрованы из списка зарегистрированных агентов (не появятся как
оппонент — Step 8 повиснет вхолостую). Заодно (косметика) обновить enumeration в тексте ошибки
`resolve_agent_algo` (~строка 271), добавив `gumbel_az`.

- [ ] **Step 4: Запустить — должно пройти**

Run: `python -m pytest tests/engine/test_gumbel_az_ids.py -v`
Expected: PASS (все тесты, включая 2 новых).

- [ ] **Step 5: eval.py — гейты загрузки сети**

В `eval.py` найти `is_az_algo(algo)` в ветках построения/загрузки AZ-сети (около строк 1039 и 1084 — выбор алгоритма и net). Заменить там, где это «семейство сети/чекпойнта» (грузит `make_alphazero_net` + `policy_value_net`), на `is_alphazero_net_algo(algo)`. Импорт: `from core.models.alphazero_ids import is_az_algo, is_alphazero_net_algo`.

Конкретно `eval.py:1039`:
```python
    elif is_az_algo(algo):
```
→
```python
    elif is_alphazero_net_algo(algo):
```
И аналогично в `eval.py:648` (диспатч выбора действия) — там, где AZ идёт в `select_action_with_epsilon_alphazero`: заменить `is_az_algo(algo)` → `is_alphazero_net_algo(algo)`, чтобы gumbel_az шёл по AZ greedy-пути.

- [ ] **Step 6: game_controller.py — гейты (Viewer)**

В `core/engine/game_controller.py` заменить `is_az_algo(agent_algo)` / `is_az_algo(algo)` → `is_alphazero_net_algo(...)` в точках: построение checkpoint для registry-агента (~431), загрузка net (~582), выбор действия (~674), а также путь распознавания (~302). Импорт обновить. Mcts-fallback (`az_mcts_mode_from_payload`) для gumbel_az вернёт "tree" — это безопасный PUCT-fallback при `AZ_PLAY_MODE=mcts` (greedy — дефолт).

- [ ] **Step 7: play.py — гейты**

В `play.py` (около строк 203, 220, 336) заменить `is_az_algo(algo)` → `is_alphazero_net_algo(algo)`. Импорт обновить.

- [ ] **Step 8: opponent_adapter.py — гейт противника**

В `core/models/opponent_adapter.py:160` заменить `is_az_algo(opponent.algo)` → `is_alphazero_net_algo(opponent.algo)`, чтобы gumbel_az можно было выбрать оппонентом (greedy). Импорт обновить.

- [ ] **Step 9: Аудит остальных call-sites `is_az_algo`**

Run: `rg -n "is_az_algo" eval.py play.py core/engine/game_controller.py core/models/opponent_adapter.py`
Для каждой оставшейся точки решить: «семейство сети» (→ `is_alphazero_net_algo`) или «именно PUCT tree/proxy режим» (→ оставить `is_az_algo`). Точки, которые задают PUCT-Dirichlet-специфичную логику (например, eval mcts с `AZ_EVAL_MCTS_DIR_EPS`) — оставить `is_az_algo`. Зафиксировать решение комментарием рядом.

- [ ] **Step 10: Smoke — импорт модулей**

Run: `python -c "import eval, play; import core.engine.game_controller; import core.models.opponent_adapter; print('ok')"`
Expected: `ok` без ошибок импорта.

- [ ] **Step 11: Коммит**

```bash
git add core/engine/agent_registry.py eval.py play.py core/engine/game_controller.py core/models/opponent_adapter.py tests/engine/test_gumbel_az_ids.py
git commit -m "feat(gumbel_az): registry meta-авторитет + eval/play/viewer/opponent через is_alphazero_net_algo"
```

---

## Task 5: Секция `"gumbel_az"` в `hyperparams.json`

**Files:**
- Modify: `hyperparams.json`

- [ ] **Step 1: Добавить секцию**

`hyperparams.json` — закрытие блока `"gumbel_muzero"` (строки 249-251):

```json
        "outcome_value_draw": -0.25
    }
}
```
заменить на (добавить запятую и новую секцию):
```json
        "outcome_value_draw": -0.25
    },
    "gumbel_az": {
        "learning_rate": 0.0003,
        "batch_size": 128,
        "value_loss_weight": 1.0,
        "l2_weight": 1e-06,
        "num_simulations": 32,
        "num_considered_actions": 8,
        "max_depth": 1,
        "value_scale": 0.1,
        "c_visit": 50.0,
        "simulate_enemy": 1,
        "eval_cache_size": 10000,
        "batch_eval_size": 16,
        "replay_capacity": 100000,
        "num_actors": 8,
        "actor_batch_send": 32,
        "actor_queue_max": 2048,
        "sync_every_updates": 2,
        "updates_per_rollout": 2,
        "replay_min_size": 512,
        "balanced_outcome_sampling": 1,
        "max_policy_staleness_updates": 600,
        "outcome_only": 1,
        "outcome_value_win": 1.0,
        "outcome_value_loss": -1.0,
        "outcome_value_draw": -0.25,
        "hidden_size": 256,
        "num_layers": 2,
        "value_ensemble": 1,
        "temperature_opening_moves": 12,
        "temperature_opening_value": 0.9,
        "temperature_late_value": 0.15,
        "lr_scheduler": "none",
        "lr_warmup_steps": 0,
        "lr_total_steps": 0,
        "det_eval_gate_win_min": 0.45,
        "det_eval_gate_turn_limit_max": 0.65,
        "inference_server_enabled": 0,
        "inference_server_mode": "local",
        "inference_remote_host": "127.0.0.1",
        "inference_remote_port": 5555,
        "inference_remote_auth_token": "",
        "distributed_actors_enabled": 0,
        "distributed_actors_port": 5557,
        "distributed_actors_bind_host": "0.0.0.0",
        "distributed_actors_auth_token": ""
    }
}
```

> Значения = **balanced**. Поля `inference_*`/`distributed_*` присутствуют, но выключены (задел под ПК2). Общие ключи (`learning_rate`, `batch_size`, `replay_capacity`, `num_actors`, …) нужны, т.к. learner читает их через `AZ_CFG` (= секция `gumbel_az`).

- [ ] **Step 2: Проверить валидность JSON**

Run: `python -c "import json; json.load(open('hyperparams.json', encoding='utf-8')); print('json ok')"`
Expected: `json ok`.

- [ ] **Step 3: Коммит**

```bash
git add hyperparams.json
git commit -m "feat(gumbel_az): секция gumbel_az в hyperparams.json (пресет balanced + швы ПК2)"
```

---

## Task 6: GUI-дефолты `gaz_hyperparams_defaults.py`

**Files:**
- Create: `app/gui_qt/gaz_hyperparams_defaults.py`

- [ ] **Step 1: Создать файл** (зеркало `gmz_hyperparams_defaults.py`)

```python
"""Default Gumbel AlphaZero (gumbel_az) hyperparams for GUI editor."""

from __future__ import annotations

# Поля, не затираемые при смене пресета (LAN/inference — задел под ПК2).
GAZ_INFERENCE_PRESERVE_KEYS: tuple[str, ...] = (
    "inference_server_enabled",
    "inference_server_mode",
    "inference_remote_host",
    "inference_remote_port",
    "inference_remote_auth_token",
    "distributed_actors_enabled",
    "distributed_actors_port",
    "distributed_actors_bind_host",
    "distributed_actors_auth_token",
)

GAZ_HYPERPARAM_KEYS: tuple[str, ...] = (
    "learning_rate",
    "batch_size",
    "value_loss_weight",
    "l2_weight",
    "num_simulations",
    "num_considered_actions",
    "max_depth",
    "value_scale",
    "c_visit",
    "simulate_enemy",
    "eval_cache_size",
    "batch_eval_size",
    "replay_capacity",
    "num_actors",
    "actor_batch_send",
    "actor_queue_max",
    "sync_every_updates",
    "updates_per_rollout",
    "replay_min_size",
    "balanced_outcome_sampling",
    "max_policy_staleness_updates",
    "outcome_only",
    "outcome_value_win",
    "outcome_value_loss",
    "outcome_value_draw",
    "hidden_size",
    "num_layers",
    "value_ensemble",
    "temperature_opening_moves",
    "temperature_opening_value",
    "temperature_late_value",
    "lr_scheduler",
    "lr_warmup_steps",
    "lr_total_steps",
    "det_eval_gate_win_min",
    "det_eval_gate_turn_limit_max",
    *GAZ_INFERENCE_PRESERVE_KEYS,
)

_GAZ_BASE: dict[str, int | float | str] = {
    "learning_rate": 0.0003,
    "batch_size": 128,
    "value_loss_weight": 1.0,
    "l2_weight": 1e-6,
    "max_depth": 1,
    "value_scale": 0.1,
    "c_visit": 50.0,
    "simulate_enemy": 1,
    "eval_cache_size": 10000,
    "replay_capacity": 100000,
    "num_actors": 8,
    "actor_batch_send": 32,
    "actor_queue_max": 2048,
    "sync_every_updates": 2,
    "updates_per_rollout": 2,
    "replay_min_size": 512,
    "balanced_outcome_sampling": 1,
    "max_policy_staleness_updates": 600,
    "outcome_only": 1,
    "outcome_value_win": 1.0,
    "outcome_value_loss": -1.0,
    "outcome_value_draw": -0.25,
    "hidden_size": 256,
    "num_layers": 2,
    "value_ensemble": 1,
    "temperature_opening_moves": 12,
    "temperature_opening_value": 0.9,
    "temperature_late_value": 0.15,
    "lr_scheduler": "none",
    "lr_warmup_steps": 0,
    "lr_total_steps": 0,
    "det_eval_gate_win_min": 0.45,
    "det_eval_gate_turn_limit_max": 0.65,
    # Швы под ПК2 — выключены
    "inference_server_enabled": 0,
    "inference_server_mode": "local",
    "inference_remote_host": "127.0.0.1",
    "inference_remote_port": 5555,
    "inference_remote_auth_token": "",
    "distributed_actors_enabled": 0,
    "distributed_actors_port": 5557,
    "distributed_actors_bind_host": "0.0.0.0",
    "distributed_actors_auth_token": "",
}

GAZ_PROFILE_DETECT_ORDER: tuple[str, ...] = ("fast", "balanced", "heavy")

GAZ_PROFILE_PRESETS: dict[str, dict[str, int | float | str]] = {
    "fast": {
        "num_simulations": 16,
        "num_considered_actions": 4,
        "batch_eval_size": 8,
    },
    "balanced": {
        "num_simulations": 32,
        "num_considered_actions": 8,
        "batch_eval_size": 16,
    },
    "heavy": {
        "num_simulations": 64,
        "num_considered_actions": 16,
        "batch_eval_size": 32,
    },
}

# No-preset дефолт = balanced.
DEFAULT_GAZ_HYPERPARAMS: dict[str, int | float | str] = {
    **_GAZ_BASE,
    **GAZ_PROFILE_PRESETS["balanced"],
}

GAZ_BASIC_KEYS: tuple[str, ...] = (
    "learning_rate",
    "batch_size",
    "num_simulations",
    "num_considered_actions",
    "num_actors",
)

GAZ_GROUPS: tuple[dict[str, object], ...] = (
    {
        "id": "search",
        "title": "Поиск (Gumbel + Sequential Halving)",
        "keys": (
            "num_simulations",
            "num_considered_actions",
            "max_depth",
            "value_scale",
            "c_visit",
            "simulate_enemy",
            "eval_cache_size",
            "batch_eval_size",
        ),
        "default_collapsed": False,
    },
    {
        "id": "training",
        "title": "Обучение",
        "keys": (
            "learning_rate",
            "batch_size",
            "value_loss_weight",
            "l2_weight",
            "lr_scheduler",
            "lr_warmup_steps",
            "lr_total_steps",
        ),
        "default_collapsed": False,
    },
    {
        "id": "temperature",
        "title": "Температура",
        "keys": (
            "temperature_opening_moves",
            "temperature_opening_value",
            "temperature_late_value",
        ),
        "default_collapsed": True,
    },
    {
        "id": "actors_replay",
        "title": "Акторы и replay",
        "keys": (
            "num_actors",
            "actor_batch_send",
            "actor_queue_max",
            "sync_every_updates",
            "updates_per_rollout",
            "replay_capacity",
            "replay_min_size",
            "balanced_outcome_sampling",
            "max_policy_staleness_updates",
        ),
        "default_collapsed": False,
    },
    {
        "id": "arch_outcome",
        "title": "Архитектура и outcome",
        "keys": (
            "hidden_size",
            "num_layers",
            "value_ensemble",
            "outcome_only",
            "outcome_value_win",
            "outcome_value_loss",
            "outcome_value_draw",
            "det_eval_gate_win_min",
            "det_eval_gate_turn_limit_max",
        ),
        "default_collapsed": True,
    },
)

GAZ_FIELD_TOOLTIPS: dict[str, str] = {
    "learning_rate": "Скорость обучения learner.",
    "batch_size": "Размер батча при обновлении весов.",
    "value_loss_weight": "Вес value loss.",
    "l2_weight": "L2-регуляризация.",
    "num_simulations": "Бюджет Sequential Halving на голову (на ход).",
    "num_considered_actions": "m: размер Gumbel top-k кандидатов на голову.",
    "max_depth": "Глубина поиска (v1 = 1, root-only).",
    "value_scale": "Масштаб c_scale в sigma(Q) для completed-Q.",
    "c_visit": "Константа c_visit в sigma(Q).",
    "simulate_enemy": "1 = симулировать ход врага в depth-1 rollout (точнее, дороже).",
    "eval_cache_size": "Размер LRU-кэша оценок сети.",
    "batch_eval_size": "Сколько листьев батчить в один forward value-сети.",
    "replay_capacity": "Ёмкость replay buffer.",
    "num_actors": "Число параллельных CPU-акторов self-play.",
    "actor_batch_send": "Сколько переходов актор шлёт за раз.",
    "actor_queue_max": "Макс. размер очереди переходов.",
    "sync_every_updates": "Каждые N обновлений learner пишет latest_az_gumbel_az_policy.pth для акторов.",
    "updates_per_rollout": "Градиентных обновлений на один rollout.",
    "replay_min_size": "Мин. размер replay до старта обучения.",
    "balanced_outcome_sampling": "1 = балансировка сэмплинга по исходу.",
    "max_policy_staleness_updates": "Макс. устаревание политики у акторов.",
    "outcome_only": "1 = только outcome reward.",
    "outcome_value_win": "Награда за победу.",
    "outcome_value_loss": "Награда за поражение.",
    "outcome_value_draw": "Награда за ничью.",
    "hidden_size": "Размер скрытого слоя сети.",
    "num_layers": "Число residual-блоков.",
    "value_ensemble": "Число value-голов (ансамбль).",
    "temperature_opening_moves": "Ходов с повышенной температурой (сэмпл из улучшенной π).",
    "temperature_opening_value": "Температура в дебюте.",
    "temperature_late_value": "Температура в эндшпиле.",
    "lr_scheduler": "Тип LR-расписания (none/cosine/...).",
    "lr_warmup_steps": "Шаги warmup для LR.",
    "lr_total_steps": "Всего шагов для LR-расписания.",
    "det_eval_gate_win_min": "Порог win_rate для аннотации gate_pass в DET-eval.",
    "det_eval_gate_turn_limit_max": "Макс. доля turn_limit для gate_pass.",
}
```

- [ ] **Step 2: Smoke — импорт и пресеты**

Run:
```bash
python -c "from app.gui_qt.gaz_hyperparams_defaults import DEFAULT_GAZ_HYPERPARAMS as D, GAZ_PROFILE_PRESETS as P; assert D['num_simulations']==32; assert P['fast']['num_simulations']==16; assert P['heavy']['num_considered_actions']==16; print('gaz defaults ok')"
```
Expected: `gaz defaults ok`.

- [ ] **Step 3: Коммит**

```bash
git add app/gui_qt/gaz_hyperparams_defaults.py
git commit -m "feat(gumbel_az): GUI-дефолты gaz_hyperparams_defaults (пресеты fast/balanced/heavy)"
```

---

## Task 7: GUI-контроллер `app/gui_qt/main.py`

**Files:**
- Modify: `app/gui_qt/main.py`

> Зеркалим обвязку GMZ. Generic-машинерия (`_load_algo_hyperparams_section`, `_az_hyperparams_map_for_qml`, `_detect_profile`, `_hyperparam_values_equal`) переиспользуется — добавляем секцию "gaz" в её реестры.

- [ ] **Step 1: Импорт дефолтов**

Рядом с импортом `gmz_hyperparams_defaults` (около `main.py:60-66`) добавить:

```python
from app.gui_qt.gaz_hyperparams_defaults import (
    DEFAULT_GAZ_HYPERPARAMS,
    GAZ_PROFILE_DETECT_ORDER,
    GAZ_PROFILE_PRESETS,
    GAZ_GROUPS,
    GAZ_FIELD_TOOLTIPS,
    GAZ_BASIC_KEYS,
    GAZ_INFERENCE_PRESERVE_KEYS,
)
```

- [ ] **Step 2: Состояние в `__init__` + dropdown**

`main.py:406` — заменить:
```python
        self._training_algo_options = ["dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"]
```
на:
```python
        self._training_algo_options = ["dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az"]
```

Рядом с инициализацией `self._gmz_hyperparams` (около `main.py:416-424`) добавить:
```python
        self._default_gaz_hyperparams: dict[str, int | float | str] = dict(DEFAULT_GAZ_HYPERPARAMS)
        self._gaz_profile_presets = dict(GAZ_PROFILE_PRESETS)
        self._gaz_hyperparams = dict(self._default_gaz_hyperparams)
        self._gaz_selected_profile = "balanced"
```

- [ ] **Step 3: Слот `set_gaz_hyperparam` + `apply_gaz_profile`**

Рядом с `set_gmz_hyperparam` (`main.py:3369`) добавить аналог:
```python
    @Slot(str, str)
    def set_gaz_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key).strip()
        if normalized_key not in self._default_gaz_hyperparams:
            return
        default = self._default_gaz_hyperparams[normalized_key]
        current = self._gaz_hyperparams.get(normalized_key, default)
        parsed = self._coerce_hyperparam_value(default, current, value)
        if parsed is None:
            return
        self._gaz_hyperparams[normalized_key] = parsed
        self._refresh_selected_profiles()
        self.hyperparamsChanged.emit()
```

Рядом с `apply_gmz_profile` (`main.py:3454`) добавить:
```python
    @Slot(str)
    def apply_gaz_profile(self, profile: str) -> None:
        mode = str(profile).strip().lower()
        if mode not in set(GAZ_PROFILE_DETECT_ORDER):
            return
        preset_patch = self._gaz_profile_presets.get(mode, {})
        # сохраняем LAN/inference поля (задел под ПК2)
        preserved = {
            k: self._gaz_hyperparams[k]
            for k in GAZ_INFERENCE_PRESERVE_KEYS
            if k in self._gaz_hyperparams
        }
        base = dict(self._default_gaz_hyperparams)
        base.update(preset_patch)
        base.update(preserved)
        self._gaz_hyperparams.update(base)
        self._refresh_selected_profiles()
        self.hyperparamsChanged.emit()
```

> Если `_coerce_hyperparam_value`/`hyperparamsChanged` названы иначе — использовать те же имена, что в `set_gmz_hyperparam` (скопировать сигнатуру 1:1).

- [ ] **Step 4: Детект активного пресета**

В `_refresh_selected_profiles` (около `main.py:3428-3439`, где идут `_dqn_selected_profile`/`_az_tree_selected_profile`) добавить строку:
```python
        self._gaz_selected_profile = self._detect_profile(self._gaz_hyperparams, self._gaz_profile_presets)
```

- [ ] **Step 5: QML-проперти**

Рядом с `hpGmzHyperparamsMap`/`hpGmzGroups`/… (`main.py:3907-3983`) добавить зеркальные `hpGaz*` (используют общий `_az_hyperparams_map_for_qml`):
```python
    @Property("QVariant", notify=hyperparamsChanged)
    def hpGazHyperparamsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._gaz_hyperparams)

    @Property("QVariant", notify=hyperparamsChanged)
    def hpGazDefaultsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._default_gaz_hyperparams)

    @Property("QVariant", constant=True)
    def hpGazGroups(self) -> list:
        return [dict(g) for g in GAZ_GROUPS]

    @Property("QVariant", constant=True)
    def hpGazFieldTooltips(self) -> dict:
        return dict(GAZ_FIELD_TOOLTIPS)

    @Property("QVariant", constant=True)
    def hpGazBasicKeys(self) -> list:
        return list(GAZ_BASIC_KEYS)
```

Рядом с `hpGmzPresetLabel` (`main.py:2240`) добавить:
```python
    @Property(str, notify=hyperparamsChanged)
    def hpGazPresetLabel(self) -> str:
        return str(self._gaz_selected_profile or "")
```
(если `hpGmzPresetLabel` использует другой notify-сигнал — взять тот же.)

- [ ] **Step 6: Регистрация секции "gaz" в generic-реестрах**

В словарях-реестрах рядом с ключом `"gmz"` (около `main.py:3727`, `3759`, `3848`) добавить `"gaz"`:
- `main.py:3727` (defaults map):
```python
            "gaz": self._default_gaz_hyperparams,
```
- `main.py:3759` (defaults/current/presets tuple):
```python
            "gaz": (self._default_gaz_hyperparams, self._gaz_hyperparams, self._gaz_profile_presets),
```
- `main.py:3785` (allowed_profiles) — добавить ветку для "gaz":
```python
            allowed_profiles = set(GAZ_PROFILE_DETECT_ORDER) if section == "gaz" else allowed_profiles
```
(или внести `"gaz"` в существующую логику выбора `allowed_profiles` так же, как `"gmz"`.)
- `main.py:3848-3849` (defaults/current для записи) — добавить ветку `section == "gaz"`:
```python
            elif section == "gaz":
                defaults = self._default_gaz_hyperparams
                current = self._gaz_hyperparams
```

- [ ] **Step 7: Загрузка/сохранение секции `gumbel_az`**

Рядом с загрузкой gmz (`main.py:4375`) добавить:
```python
        self._gaz_hyperparams = self._load_algo_hyperparams_section(
            payload,
            "gumbel_az",
            self._default_gaz_hyperparams,
        )
```
В ветке reset/default (около `main.py:4126`/`4347`) добавить:
```python
        self._gaz_hyperparams = dict(self._default_gaz_hyperparams)
```
В сборку `merged_payload` для сохранения (`main.py:4187`) добавить:
```python
            merged_payload["gumbel_az"] = dict(self._gaz_hyperparams)
```

- [ ] **Step 8: Env при запуске train (gumbel_az)**

В `_start_training`, рядом с веткой `if is_az_algo(self._training_algo):` (около `main.py:5545`) добавить ветку:
```python
        if self._training_algo == "gumbel_az":
            gaz = self._gaz_hyperparams
            d = self._default_gaz_hyperparams
            env.insert("GAZ_NUM_SIMULATIONS", str(int(gaz.get("num_simulations", d["num_simulations"]))))
            env.insert("GAZ_NUM_CONSIDERED_ACTIONS", str(int(gaz.get("num_considered_actions", d["num_considered_actions"]))))
            env.insert("GAZ_MAX_DEPTH", str(int(gaz.get("max_depth", d["max_depth"]))))
            env.insert("GAZ_VALUE_SCALE", str(float(gaz.get("value_scale", d["value_scale"]))))
            env.insert("GAZ_C_VISIT", str(float(gaz.get("c_visit", d["c_visit"]))))
            env.insert("GAZ_SIMULATE_ENEMY", "1" if int(gaz.get("simulate_enemy", 1)) == 1 else "0")
            env.insert("GAZ_BATCH_EVAL_SIZE", str(int(gaz.get("batch_eval_size", d["batch_eval_size"]))))
            env.insert("GAZ_EVAL_CACHE_SIZE", str(int(gaz.get("eval_cache_size", d["eval_cache_size"]))))
            env.insert("AZ_NUM_ACTORS", str(int(gaz.get("num_actors", d["num_actors"]))))
            env.insert("AZ_HIDDEN_SIZE", str(int(gaz.get("hidden_size", d["hidden_size"]))))
            env.insert("AZ_NUM_LAYERS", str(int(gaz.get("num_layers", d["num_layers"]))))
            env.insert("AZ_VALUE_ENSEMBLE", str(int(gaz.get("value_ensemble", d["value_ensemble"]))))
```
(`TRAIN_ALGO` уже выставляется из `self._training_algo` выше — проверить, что `gumbel_az` проходит. Остальное train читает из секции `gumbel_az` в hyperparams.json после «Сохранить».)

- [ ] **Step 9: Синхронизировать прочие whitelists/labels**

Run: `rg -n "gumbel_muzero" app/gui_qt/main.py`
Для каждой точки, где `gumbel_muzero` участвует в списках допустимых алго / `_format_algo_label` / фильтрах eval-play — добавить `gumbel_az` (label: `"GUMBEL ALPHAZERO"`).

- [ ] **Step 10: Smoke — импорт GUI-контроллера**

Run: `python -c "import app.gui_qt.main as m; print('gui main import ok')"`
Expected: `gui main import ok` (без QML-рендера).

- [ ] **Step 11: Коммит**

```bash
git add app/gui_qt/main.py
git commit -m "feat(gumbel_az): обвязка GUI-контроллера (состояние, слоты, проперти, env, save/load)"
```

---

## Task 8: QML — dropdown + вкладка настроек

**Files:**
- Modify: `app/gui_qt/qml/Main.qml`, `app/gui_qt/qml/components/SectionHyperparamsEditor.qml`

- [ ] **Step 1: Пункт dropdown выбора алгоритма**

`Main.qml:1810-1816` — в `model:` комбобокса `trainingAlgoComboMain` добавить пункт после `gumbel_muzero`:
```qml
                                                        { value: "gumbel_muzero", label: "GUMBEL MUZERO" },
                                                        { value: "gumbel_az", label: "GUMBEL ALPHAZERO" }
```
(не забыть запятую после строки `gumbel_muzero`.)

- [ ] **Step 2: Вкладка настроек**

`Main.qml:4558-4562` (TabBar) — добавить `TabButton` после «Gumbel MuZero»:
```qml
                                    TabButton { text: "Gumbel MuZero" }
                                    TabButton { text: "Gumbel AlphaZero" }
```
`Main.qml` StackLayout рядом — добавить child после редактора gmz:
```qml
                                    SectionHyperparamsEditor {
                                        algoSection: "gaz"
                                        rootUi: root
                                    }
```
(порядок child'ов StackLayout должен совпадать с порядком TabButton.)

- [ ] **Step 3: Ветка `gaz` в `SectionHyperparamsEditor.qml`**

В местах, где компонент выбирает источники по `algoSection` (карты/группы/пресеты), добавить ветку `"gaz"` рядом с `"gmz"`. Например, presets-Repeater (`SectionHyperparamsEditor.qml:280-283`):
```qml
                Repeater {
                    model: hpEditor.algoSection === "gmz"
                           ? ["fast", "balanced", "heavy", "very_heavy"]
                           : ["fast", "balanced", "heavy"]
```
(`gaz` уже попадёт в else → `["fast","balanced","heavy"]` — корректно.)

`applyProfile` (`SectionHyperparamsEditor.qml:101-108`) — добавить ветку:
```qml
        else if (algoSection === "gaz") controller.apply_gaz_profile(name)
```
И там, где компонент берёт карты значений/групп/тултипов/basic/preset-label по секции, добавить маппинг `"gaz"`:
```qml
    readonly property var hpMap: algoSection === "gmz" ? controller.hpGmzHyperparamsMap
                                 : algoSection === "gaz" ? controller.hpGazHyperparamsMap
                                 : ... // существующие ветки tree/proxy/dqn/ppo
    readonly property var hpDefaults: algoSection === "gaz" ? controller.hpGazDefaultsMap : ...
    readonly property var hpGroups: algoSection === "gaz" ? controller.hpGazGroups : ...
    readonly property var hpTooltips: algoSection === "gaz" ? controller.hpGazFieldTooltips : ...
    readonly property var hpBasic: algoSection === "gaz" ? controller.hpGazBasicKeys : ...
    readonly property string presetLabel: algoSection === "gaz" ? controller.hpGazPresetLabel : ...
    function setKey(k, v) { if (algoSection === "gaz") controller.set_gaz_hyperparam(k, String(v)); else ... }
```
(точные имена property/функций — как уже используются для `gmz` в этом файле; добавить ветку `gaz` в каждую.)

- [ ] **Step 2 verify: запустить GUI smoke (ручная проверка)**

Run (через `/run-40kai` или GUI): открыть Настройки → должна появиться вкладка «Gumbel AlphaZero» с полями и кнопками Fast/Balanced/Heavy; dropdown Train содержит «GUMBEL ALPHAZERO».

- [ ] **Step 4: Коммит**

```bash
git add app/gui_qt/qml/Main.qml app/gui_qt/qml/components/SectionHyperparamsEditor.qml
git commit -m "feat(gumbel_az): QML dropdown + вкладка настроек Gumbel AlphaZero"
```

---

## Task 9: Справка в `TrainingAlgoHelpDialog.qml`

**Files:**
- Modify: `app/gui_qt/qml/components/TrainingAlgoHelpDialog.qml`

- [ ] **Step 1: Добавить карточку**

Добавить карточку-описание (рядом с карточкой Gumbel MuZero, индексы 134-136):
```qml
        AlgoHelpCard {
            title: "Gumbel AlphaZero"
            body: "AlphaZero с Gumbel-планированием: Gumbel top-k в корне + Sequential Halving + "
                + "completed-Q как цель политики. Гарантирует улучшение даже при малом числе симуляций "
                + "(16–64), depth-1. Реальная модель среды (как AlphaZero), без выученной динамики. "
                + "Сеть и чекпойнты совместимы с AlphaZero (eval/play грузят greedy)."
        }
```
(структуру карточки взять идентичной существующим в этом файле.)

- [ ] **Step 2: Коммит**

```bash
git add app/gui_qt/qml/components/TrainingAlgoHelpDialog.qml
git commit -m "docs(gumbel_az): карточка-справка Gumbel AlphaZero в GUI"
```

---

## Task 10: Интеграционные тесты, GUI-тест, финальная верификация

**Files:**
- Create: `tests/engine/test_gumbel_az_integration.py`, `tests/gui_qt/test_gaz_hyperparams_load.py`

- [ ] **Step 1: Интеграционный тест эпизода селфплея**

Скопировать env-постройку из `tests/engine/test_alphazero_mcts_tree_basic.py` (тот же mini-env / roster), заменив объект поиска на `GumbelAlphaZeroSearch`. Каркас:

```python
# tests/engine/test_gumbel_az_integration.py
import numpy as np
import torch

from core.models.gumbel_alphazero_search import GumbelAlphaZeroSearch, GumbelAZSearchConfig
from core.models.alphazero_model import make_alphazero_net
from core.models.alphazero_selfplay import play_episode_with_mcts, SelfPlayConfig
# --- env/roster helpers: импортировать ровно те же, что использует
# tests/engine/test_alphazero_mcts_tree_basic.py (build env + len_model) ---


def _make_env_and_net():
    # СКОПИРОВАТЬ из tests/engine/test_alphazero_mcts_tree_basic.py:
    # построение env (gym.make 40kAI-v0 с минимальным roster), n_observations,
    # n_actions, len_model. Вернуть (env, net, len_model).
    ...


def test_gumbel_az_selfplay_episode_produces_transitions():
    env, net, len_model = _make_env_and_net()
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=4, simulate_enemy=True)
    search = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    transitions, info = play_episode_with_mcts(
        env=env, mcts=search, len_model=len_model, config=SelfPlayConfig(),
        outcome_only=True,
    )
    assert len(transitions) > 0
    for t in transitions:
        assert -1.0 <= float(t.value_target) <= 1.0
        assert len(t.policy_targets) >= 1
        for pi in t.policy_targets:
            assert abs(float(np.sum(pi)) - 1.0) < 1e-4
```

> Если в `test_alphazero_mcts_tree_basic.py` есть фикстура/функция для env — переиспользовать её импортом, а не копипастой.

- [ ] **Step 2: Запустить интеграционный тест**

Run: `python -m pytest tests/engine/test_gumbel_az_integration.py -v`
Expected: PASS (эпизод отыгрывается, транзишены валидны, env восстановлен).

- [ ] **Step 3: GUI-тест загрузки гиперпараметров**

```python
# tests/gui_qt/test_gaz_hyperparams_load.py
from app.gui_qt.gaz_hyperparams_defaults import DEFAULT_GAZ_HYPERPARAMS


def test_load_gaz_section_preserves_remote_host_ip():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    payload = {
        "gumbel_az": {
            "inference_remote_host": "192.168.0.105",
            "inference_server_mode": "remote",
            "num_simulations": 64,
        }
    }
    loaded = ctrl._load_algo_hyperparams_section(payload, "gumbel_az", dict(DEFAULT_GAZ_HYPERPARAMS))
    assert loaded["inference_remote_host"] == "192.168.0.105"
    assert loaded["inference_server_mode"] == "remote"
    assert int(loaded["num_simulations"]) == 64


def test_gaz_in_training_algo_options():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    ctrl._training_algo_options = ["dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az"]
    assert "gumbel_az" in ctrl._training_algo_options
```

> Если загрузчик называется `_load_az_hyperparams_section` (а не `_load_algo_hyperparams_section`) — использовать фактическое имя из `main.py`.

- [ ] **Step 4: Запустить GUI-тест**

Run: `python -m pytest tests/gui_qt/test_gaz_hyperparams_load.py -v`
Expected: PASS.

- [ ] **Step 5: Регрессия AZ + полный прогон новых тестов**

Run:
```bash
python -m pytest tests/engine/test_alphazero_smoke.py tests/engine/test_alphazero_mcts_tree_basic.py tests/engine/test_alphazero_mcts_advanced.py tests/engine/test_resolve_agent_algo.py tests/gui_qt/test_az_hyperparams_load.py -v
python -m pytest tests/models/test_gumbel_alphazero_search.py tests/engine/test_gumbel_az_ids.py tests/engine/test_gumbel_az_integration.py tests/gui_qt/test_gaz_hyperparams_load.py -v
```
Expected: все PASS (AZ-регрессий нет; новые зелёные).

- [ ] **Step 6: Smoke train-запуск gumbel_az (короткий)**

Через GUI (`/run-40kai`) или env: запустить train с `TRAIN_ALGO=gumbel_az`, `TRAIN_EPISODES_OVERRIDE=2`, balanced. Проверить:
- появляется папка `artifacts/models/gumbel_az/` и пишется `checkpoint_ep*.pth`;
- в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` нет ошибок, есть маркеры `[AZ]`/`[ACTOR]`;
- sync-файл `artifacts/models/actor_sync/latest_az_gumbel_az_policy.pth` создан.

- [ ] **Step 7: Smoke resume gumbel_az**

Повторить запуск с галочкой resume (или env `RESUME_CHECKPOINT=<artifacts/models/gumbel_az/checkpoint_epN.pth>`). Проверить в логах строку `[RESUME] ... gumbel_az` и продолжение нумерации эпизодов.

- [ ] **Step 8: Финальный коммит**

```bash
git add tests/engine/test_gumbel_az_integration.py tests/gui_qt/test_gaz_hyperparams_load.py
git commit -m "test(gumbel_az): интеграция селфплея + GUI hyperparams load"
```

---

## Self-Review (выполнить после реализации)

1. **Покрытие спека:** все 6 секций спека имеют задачи (1: ядро; 2: train; 3: registry/eval/play; 4: GUI; 5: hyperparams; 6: тесты). ✓
2. **Контракт run():** `GumbelAlphaZeroSearch.run()` отдаёт `(policy_targets, selected_actions, value)` — совпадает с AZ, поэтому `play_episode_with_mcts` и learner работают без правок.
3. **Типы/имена:** `is_gumbel_az_algo`, `is_alphazero_net_algo`, `gaz_section_for`, `_build_az_search`, `_gaz_cfg_payload`, `GumbelAZSearchConfig`, `sequential_halving_keep_schedule` — используются одинаково во всех задачах.
4. **Sync-тег:** `latest_az_gumbel_az_policy.pth` совпадает в actor (Step 8 Task 3, 8463) и learner (9078).
5. **Реестр:** meta-авторитет для gumbel_az добавлен (Task 4 Step 3), тест есть (Task 4 Step 1).
6. **Регрессии:** Task 10 Step 5 явно гоняет AZ-тесты.
7. **Перед коммитом крупного:** вызвать субагентов `engine-regression-reviewer` (ядро/движок) и `code-reviewer` (дублирование AZ↔gumbel_az) — по правилу проекта.

## Вне scope (подтверждено в спеке)
ПК2/distributed, варианты B/C поиска, Gumbel-поиск на инференсе (eval/play пока greedy-reuse).

