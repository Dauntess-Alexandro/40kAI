import numpy as np
import torch
from contextlib import contextmanager

from core.models.action_contract import ordered_action_keys
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_model import AlphaZeroPolicyValueNet


class _FakeTreeEnv:
    def __init__(self, n_obs: int, n_actions: list[int], len_model: int, terminal_on_step: bool = True):
        self.n_obs = int(n_obs)
        self.n_actions = list(n_actions)
        self.len_model = int(len_model)
        self.unwrapped = self
        self.game_over = False
        self._last_info = {"winner": "", "end reason": ""}
        self._terminal_on_step = bool(terminal_on_step)
        self._step_counter = 0

    def get_legal_action_masks_by_head(self, side: str = "model"):
        keys = ordered_action_keys(self.len_model)
        masks = {}
        for i, k in enumerate(keys):
            m = np.ones(self.n_actions[i], dtype=bool)
            # Force illegal actions on move head for mask regression checks.
            if k == "move" and m.size >= 4:
                m[2:] = False
            masks[k] = m
        return masks

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
        attack_action = int(action_dict.get("attack", 0))
        if self._terminal_on_step:
            self._last_info = {
                "end reason": "wipeout_enemy" if attack_action == 1 else "wipeout_model",
                "winner": "model" if attack_action == 1 else "enemy",
            }
            self.game_over = True
            done = True
        else:
            self._last_info = {"end reason": "", "winner": ""}
            self.game_over = False
            done = False
        obs = np.zeros(self.n_obs, dtype=np.float32)
        return obs, 0.0, done, False, dict(self._last_info)

    def enemyTurn(self, trunc=False, policy_fn=None):
        return None

    def get_info(self):
        return dict(self._last_info)


def test_alphazero_tree_mcts_policy_targets_and_masks():
    len_model = 1
    n_obs = 16
    n_actions = [5, 2, 6, 6, 5, 3, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]

    mcts = AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(simulations=24, c_puct=1.3, top_k_per_head=4, mode="tree"),
        device=torch.device("cpu"),
    )
    pi, act, value = mcts.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=1.0,
        env=env,
        len_model=len_model,
    )

    assert len(pi) == len(n_actions)
    assert len(act) == len(n_actions)
    for head_idx, p in enumerate(pi):
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
        assert np.all(p[~legal[head_idx]] <= 1e-12)
    assert -1.0 <= float(value) <= 1.0
    assert float(mcts.last_run_stats.get("simulations", 0.0)) == 24.0


def test_alphazero_tree_mcts_backup_prefers_winning_attack():
    len_model = 1
    n_obs = 12
    n_actions = [5, 2, 4, 4, 5, 2, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]

    mcts = AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(simulations=64, c_puct=2.0, top_k_per_head=4, mode="tree"),
        device=torch.device("cpu"),
    )
    pi, _act, _value = mcts.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=0.3,
        env=env,
        len_model=len_model,
    )
    # attack head index = 1, action 1 means terminal win in fake env.
    assert float(pi[1][1]) >= float(pi[1][0])
    assert float(pi[1][1]) > 0.2


def test_alphazero_tree_mcts_respects_max_depth():
    len_model = 1
    n_obs = 12
    n_actions = [5, 2, 4, 4, 5, 2, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    env = _FakeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model, terminal_on_step=False)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]

    mcts = AlphaZeroFactorizedMCTS(
        net,
        config=MCTSConfig(simulations=8, c_puct=1.5, top_k_per_head=4, mode="tree", max_depth=2),
        device=torch.device("cpu"),
    )
    _pi, _act, _value = mcts.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=1.0,
        env=env,
        len_model=len_model,
    )
    assert float(mcts.last_run_stats.get("depth_max", 0.0)) >= 2.0
