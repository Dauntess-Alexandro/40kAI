from contextlib import contextmanager

import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
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


class _RecordingEvaluator:
    def __init__(self, action_sizes, value=0.0):
        self.action_sizes = list(action_sizes)
        self._value = float(value)
        self.one_calls = 0
        self.batch_sizes: list[int] = []

    def _priors(self, legal_masks_by_head):
        priors = []
        for mask in legal_masks_by_head:
            legal = np.asarray(mask, dtype=bool)
            if legal.any():
                p = legal.astype(np.float32) / float(legal.sum())
            else:
                p = np.full(legal.shape, 1.0 / max(1, legal.size), dtype=np.float32)
            priors.append(p.astype(np.float32))
        return priors

    def evaluate_one(self, obs, legal_masks_by_head):
        self.one_calls += 1
        return self._priors(legal_masks_by_head), self._value

    def evaluate_batch(self, leaves):
        self.batch_sizes.append(len(leaves))
        out = []
        for leaf in leaves:
            obs = np.asarray(leaf["obs"], dtype=np.float32)
            out.append(float(np.tanh(float(obs[:8].sum()) * 0.25)))
        return out


class _BatchEvalEnv:
    def __init__(self, n_obs: int, n_actions: list[int], len_model: int, terminal_on_step: bool = False):
        self.n_obs = int(n_obs)
        self.n_actions = list(n_actions)
        self.len_model = int(len_model)
        self.unwrapped = self
        self.game_over = False
        self._last_info = {"winner": "", "end reason": ""}
        self._terminal_on_step = bool(terminal_on_step)
        self._step_counter = 0

    def get_legal_action_masks_by_head(self, side: str = "model"):
        return {
            key: np.ones(self.n_actions[i], dtype=bool)
            for i, key in enumerate(ordered_action_keys(self.len_model))
        }

    @contextmanager
    def simulation_mode(self):
        yield self

    def snapshot_state(self):
        return {
            "game_over": bool(self.game_over),
            "_last_info": dict(self._last_info),
            "_step_counter": int(self._step_counter),
        }

    def restore_state(self, snap):
        self.game_over = bool(snap.get("game_over", False))
        self._last_info = dict(snap.get("_last_info", {"winner": "", "end reason": ""}))
        self._step_counter = int(snap.get("_step_counter", 0))

    def step(self, action_dict):
        self._step_counter += 1
        obs = np.zeros(self.n_obs, dtype=np.float32)
        for idx, key in enumerate(ordered_action_keys(self.len_model)):
            if idx >= obs.size:
                break
            obs[idx] = float(action_dict.get(key, 0)) + float(idx) * 0.01
        if self._terminal_on_step:
            attack_action = int(action_dict.get("attack", 0))
            self._last_info = {
                "end reason": "wipeout_enemy" if attack_action == 1 else "wipeout_model",
                "winner": "model" if attack_action == 1 else "enemy",
            }
            self.game_over = True
            return obs, 0.0, True, False, dict(self._last_info)
        self._last_info = {"winner": "", "end reason": ""}
        self.game_over = False
        return obs, 0.0, False, False, dict(self._last_info)

    def enemyTurn(self, trunc=False, policy_fn=None):
        return None

    def get_info(self):
        return dict(self._last_info)


def _run_batch_env(*, batch_eval_size: int, seed: int = 17, terminal_on_step: bool = False):
    len_model = 1
    n_obs = 16
    n_actions = [5, 2, 4, 4, 5, 2, 24]
    env = _BatchEvalEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model, terminal_on_step=terminal_on_step)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
    evaluator = _RecordingEvaluator(n_actions)
    cfg = GumbelAZSearchConfig(
        num_simulations=16,
        num_considered_actions=4,
        simulate_enemy=False,
        batch_eval_size=batch_eval_size,
    )
    np.random.seed(seed)
    search = GumbelAlphaZeroSearch(_StubNet(n_actions), config=cfg, device=torch.device("cpu"), evaluator=evaluator)
    pi, actions, value = search.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=0.0,
        env=env,
        len_model=len_model,
    )
    return search, evaluator, env, legal, pi, actions, value


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


def test_joint_action_default_off():
    assert GumbelAZSearchConfig().joint_action is False


def _run_capturing_base_action(joint: bool):
    """Прогоняет поиск, перехватывая base_action, который видит каждая голова."""
    net = _StubNet([3, 3, 3], value=0.0)
    legal = [np.ones(3, dtype=bool) for _ in range(3)]
    obs = np.zeros(5, dtype=np.float32)
    cfg = GumbelAZSearchConfig(
        num_simulations=8, num_considered_actions=3, simulate_enemy=False, joint_action=joint
    )
    np.random.seed(7)
    s = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    seen: list[tuple[int, list[int]]] = []
    orig = s._search_head

    def _wrapped(*, head_idx, base_action, **kw):
        seen.append((int(head_idx), list(base_action)))
        return orig(head_idx=head_idx, base_action=base_action, **kw)

    s._search_head = _wrapped
    _pi, actions, _v = s.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)
    return actions, seen


def test_joint_action_off_keeps_greedy_context():
    # per-head: каждая голова видит исходный greedy base_action (argmax uniform = 0)
    _actions, seen = _run_capturing_base_action(joint=False)
    for _head_idx, base in seen:
        assert base == [0, 0, 0]


def test_joint_action_on_propagates_winners_to_later_heads():
    # joint: голова h+1 видит уже ВЫБРАННОЕ действие головы h в base_action
    actions, seen = _run_capturing_base_action(joint=True)
    # seen[k] = (head_idx=k, base_action на момент поиска головы k)
    assert seen[1][1][0] == actions[0]  # голова 1 увидела победителя головы 0
    assert seen[2][1][0] == actions[0]
    assert seen[2][1][1] == actions[1]  # голова 2 увидела победителя головы 1


def test_inference_temperature_deterministic_vs_stochastic():
    net = _StubNet([6], value=0.0)
    legal = [np.ones(6, dtype=bool)]
    obs = np.zeros(7, dtype=np.float32)
    cfg = GumbelAZSearchConfig(num_simulations=8, num_considered_actions=6, simulate_enemy=False)
    # инференс (move_count=None), T≈0 → детерминированный argmax улучшённой политики
    s = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    a0 = {s.run(obs=obs, legal_masks_by_head=legal, temperature=0.0)[1][0] for _ in range(6)}
    assert len(a0) == 1
    # высокая T → появляется разнообразие выбора
    np.random.seed(0)
    s2 = GumbelAlphaZeroSearch(net, config=cfg, device=torch.device("cpu"))
    a1 = {s2.run(obs=obs, legal_masks_by_head=legal, temperature=1.0)[1][0] for _ in range(40)}
    assert len(a1) > 1


def test_build_inference_search_config_and_run():
    from core.models.gumbel_alphazero_search import build_gumbel_inference_search

    net = _StubNet([4, 3], value=0.0)
    s = build_gumbel_inference_search(
        net, num_simulations=16, num_considered_actions=4, joint_action=True,
        device=torch.device("cpu"),
    )
    # инференс: без симуляции врага, joint прокинут, depth-1
    assert s.cfg.simulate_enemy is False
    assert s.cfg.joint_action is True
    assert s.cfg.max_depth == 1
    legal = [np.ones(4, dtype=bool), np.ones(3, dtype=bool)]
    pi, actions, value = s.run(
        obs=np.zeros(5, dtype=np.float32), legal_masks_by_head=legal, temperature=0.0
    )
    assert len(actions) == 2
    for p in pi:
        assert abs(float(p.sum()) - 1.0) < 1e-5
    for a, lg in zip(actions, legal):
        assert bool(lg[a])
    assert -1.0 <= float(value) <= 1.0


def test_nonterminal_leaf_eval_uses_configured_batches():
    search, evaluator, _env, _legal, pi, actions, value = _run_batch_env(batch_eval_size=4)

    assert evaluator.batch_sizes
    assert max(evaluator.batch_sizes) <= 4
    assert any(size > 1 for size in evaluator.batch_sizes)
    assert float(search.last_run_stats["leaf_eval_requests"]) > 0.0
    assert float(search.last_run_stats["leaf_eval_batch_max"]) <= 4.0
    assert float(search.last_run_stats["leaf_eval_dedup_hits"]) > 0.0
    assert len(pi) == len(actions)
    for p in pi:
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
    assert -1.0 <= float(value) <= 1.0


def test_batch_eval_size_matches_scalar_gumbel_az_search():
    seq = _run_batch_env(batch_eval_size=1, seed=23)
    batched = _run_batch_env(batch_eval_size=4, seed=23)
    _s1, _e1, _env1, _legal1, pi_seq, act_seq, val_seq = seq
    _s2, _e2, _env2, _legal2, pi_batch, act_batch, val_batch = batched

    assert act_seq == act_batch
    assert abs(float(val_seq) - float(val_batch)) < 1e-6
    assert len(pi_seq) == len(pi_batch)
    for p_seq, p_batch in zip(pi_seq, pi_batch):
        assert np.allclose(p_seq, p_batch, atol=1e-6)


def test_terminal_leaf_eval_skips_value_batch():
    search, evaluator, env, legal, pi, actions, value = _run_batch_env(
        batch_eval_size=4, terminal_on_step=True
    )

    assert evaluator.batch_sizes == []
    assert float(search.last_run_stats["leaf_eval_requests"]) == 0.0
    assert env.game_over is False
    for head_idx, p in enumerate(pi):
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
        assert np.all(p[~legal[head_idx]] <= 1e-12)
        assert bool(legal[head_idx][actions[head_idx]])
    assert -1.0 <= float(value) <= 1.0
