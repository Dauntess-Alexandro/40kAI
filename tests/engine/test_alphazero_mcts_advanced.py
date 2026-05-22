import numpy as np
import torch
from contextlib import contextmanager

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import (
    AlphaZeroFactorizedMCTS,
    EvalCache,
    MCTSConfig,
    MCTSNode,
    adaptive_c_puct,
    progressive_widening_allowed,
)
from core.models.alphazero_model import make_alphazero_net


def test_mcts_node_puct_score_formula():
    parent = MCTSNode(prior=1.0)
    parent.visit_count = 10
    child = MCTSNode(prior=0.5, parent=parent, action_tuple=(1, 0))
    child.visit_count = 2
    child.value_sum = 0.4
    c_puct = 1.5
    expected_q = 0.4 / 2.0
    expected_u = 1.5 * 0.5 * (10 ** 0.5) / (1.0 + 2.0)
    assert abs(child.puct_score(c_puct) - (expected_q + expected_u)) < 1e-5


def test_mcts_eval_cache_hits():
    cache = EvalCache(max_size=8)
    obs = np.zeros(8, dtype=np.float32)
    legal = [np.array([1, 1, 0], dtype=bool)]
    priors = [np.array([0.7, 0.2, 0.1], dtype=np.float32)]
    cache.set(obs, legal, priors, 0.5)
    assert cache.get(obs, legal) is not None
    assert cache.hits == 1
    assert cache.get(obs, legal) is not None
    assert cache.hits == 2


def test_mcts_backprop_increments_parent_visits():
    root = MCTSNode(prior=1.0)
    child = MCTSNode(prior=0.3, parent=root, action_tuple=(0,))
    root.children[(0,)] = child
    path = [root, child]
    mcts = AlphaZeroFactorizedMCTS(make_alphazero_net(8, [3]), config=MCTSConfig())
    mcts._backpropagate(path, 1.0)
    assert root.visit_count == 1
    assert child.visit_count == 1
    assert abs(child.value_sum - 1.0) < 1e-6


class _RestoreFailEnv:
    def __init__(self, n_obs: int, n_actions: list[int], len_model: int):
        self.n_obs = n_obs
        self.n_actions = n_actions
        self.len_model = len_model
        self.unwrapped = self
        self.game_over = False
        self._info = {"winner": "model", "end reason": "wipeout_enemy"}
        self.reset_calls = 0

    def get_legal_action_masks_by_head(self, side="model"):
        keys = ordered_action_keys(self.len_model)
        return {k: np.ones(self.n_actions[i], dtype=bool) for i, k in enumerate(keys)}

    @contextmanager
    def simulation_mode(self):
        yield self

    def snapshot_state(self):
        return {"ok": True}

    def restore_state(self, _snap):
        raise RuntimeError("restore failed")

    def reset(self, options=None):
        self.reset_calls += 1
        return np.zeros(self.n_obs, dtype=np.float32), {}

    def step(self, action_dict):
        self.game_over = True
        return np.zeros(self.n_obs, dtype=np.float32), 0.0, True, False, dict(self._info)

    def enemyTurn(self, trunc=False, policy_fn=None):
        return None

    def get_info(self):
        return dict(self._info)


def test_mcts_snapshot_restore_fallback():
    len_model = 1
    n_obs = 8
    n_actions = [4, 2, 4, 4, 4, 2, 12]
    env = _RestoreFailEnv(n_obs, n_actions, len_model)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
    net = make_alphazero_net(n_obs, n_actions)
    mcts = AlphaZeroFactorizedMCTS(
        net, config=MCTSConfig(simulations=4, mode="tree", max_depth=1), device=torch.device("cpu")
    )
    mcts.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=1.0,
        env=env,
        len_model=len_model,
        reset_options={"m": None, "e": None, "trunc": True},
    )
    assert env.reset_calls >= 1 or float(mcts.last_run_stats.get("snapshot_fallback", 0.0)) >= 1.0


def test_az_adaptive_c_puct_schedule():
    cfg = MCTSConfig(c_puct=1.2, c_puct_min=1.0, c_puct_max=2.0, c_puct_schedule="linear", progress=0.0)
    early = adaptive_c_puct(cfg)
    cfg.progress = 1.0
    late = adaptive_c_puct(cfg)
    assert early > late


def test_az_progressive_widening_limits_expansion():
    assert progressive_widening_allowed(parent_visits=0, num_children=5, pw_alpha=1.0, pw_beta=0.5) is True
    assert progressive_widening_allowed(parent_visits=1, num_children=10, pw_alpha=10.0, pw_beta=0.5) is False


def test_az_move_averaging_early_vs_late():
    root = MCTSNode(prior=1.0)
    priors = [np.array([0.1, 0.8, 0.1], dtype=np.float32)]
    legal = [np.array([1, 1, 1], dtype=bool)]
    child0 = MCTSNode(prior=0.1, parent=root, action_tuple=(0,))
    child1 = MCTSNode(prior=0.8, parent=root, action_tuple=(1,))
    child0.visit_count = 1
    child1.visit_count = 9
    root.children[(0,)] = child0
    root.children[(1,)] = child1
    mcts = AlphaZeroFactorizedMCTS(
        make_alphazero_net(8, [3]),
        config=MCTSConfig(temperature_opening_moves=20, prior_weight_early=0.5),
    )
    early_pi, _ = mcts._final_policy_from_visits(root, priors, legal, temperature=1.0, move_count=0)
    late_pi, _ = mcts._final_policy_from_visits(root, priors, legal, temperature=0.01, move_count=50)
    assert float(early_pi[0][1]) > 0.0
    assert float(late_pi[0][1]) >= float(early_pi[0][1]) - 0.05
