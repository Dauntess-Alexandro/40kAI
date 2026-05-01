import numpy as np
import torch
from contextlib import contextmanager

from core.models.alphazero_model import AlphaZeroPolicyValueNet
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.alphazero_replay import AlphaZeroReplayBuffer, AZTransition
from core.models.alphazero_trainer import AlphaZeroTrainConfig, train_alphazero_step
from core.models.action_contract import ordered_action_keys


def test_alphazero_model_forward_shapes():
    n_obs = 32
    n_actions = [5, 2, 8, 8, 5, 4, 24, 24]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    x = torch.randn(3, n_obs)
    logits, value = net(x)
    assert len(logits) == len(n_actions)
    assert value.shape == (3,)
    for idx, head in enumerate(logits):
        assert head.shape == (3, n_actions[idx])


def test_alphazero_trainer_step_runs():
    n_obs = 16
    n_actions = [3, 2, 5]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    replay = AlphaZeroReplayBuffer(capacity=64)
    for _ in range(20):
        replay.push(
            AZTransition(
                state=np.random.randn(n_obs).astype(np.float32),
                policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
                value_target=float(np.random.uniform(-1.0, 1.0)),
            )
        )
    opt = torch.optim.Adam(net.parameters(), lr=1e-3)
    out = train_alphazero_step(
        net=net,
        optimizer=opt,
        replay=replay,
        config=AlphaZeroTrainConfig(batch_size=8),
        device=torch.device("cpu"),
    )
    assert out is not None
    assert out["loss"] >= 0.0


def test_alphazero_mcts_policy_targets_sum_to_one():
    n_obs = 10
    n_actions = [4, 3]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    mcts = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(simulations=8), device=torch.device("cpu"))
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.array([1, 1, 0, 1], dtype=bool), np.array([1, 0, 1], dtype=bool)]
    pi, act, value = mcts.run(obs=obs, legal_masks_by_head=legal, temperature=1.0)
    assert len(pi) == 2
    assert len(act) == 2
    for p in pi:
        assert abs(float(np.sum(p)) - 1.0) < 1e-5
    assert -1.0 <= float(value) <= 1.0


def test_alphazero_tree_mode_smoke_runs():
    class _SmokeTreeEnv:
        def __init__(self, n_obs: int, n_actions: list[int], len_model: int):
            self.n_obs = int(n_obs)
            self.n_actions = list(n_actions)
            self.len_model = int(len_model)
            self.unwrapped = self
            self.game_over = False
            self._last_info = {"winner": "", "end reason": ""}

        def get_legal_action_masks_by_head(self, side="model"):
            keys = ordered_action_keys(self.len_model)
            return {k: np.ones(self.n_actions[i], dtype=bool) for i, k in enumerate(keys)}

        @contextmanager
        def simulation_mode(self):
            yield self

        def snapshot_state(self):
            return {"game_over": bool(self.game_over), "info": dict(self._last_info)}

        def restore_state(self, snap):
            self.game_over = bool(snap.get("game_over", False))
            self._last_info = dict(snap.get("info", {"winner": "", "end reason": ""}))

        def step(self, action_dict):
            self._last_info = {"winner": "model", "end reason": "wipeout_enemy"}
            self.game_over = True
            obs = np.zeros(self.n_obs, dtype=np.float32)
            return obs, 0.0, True, False, dict(self._last_info)

        def enemyTurn(self, trunc=False, policy_fn=None):
            return None

        def get_info(self):
            return dict(self._last_info)

    len_model = 1
    n_obs = 10
    n_actions = [4, 2, 6, 6, 4, 3, 24]
    env = _SmokeTreeEnv(n_obs=n_obs, n_actions=n_actions, len_model=len_model)
    legal_dict = env.get_legal_action_masks_by_head("model")
    legal = [legal_dict[k] for k in ordered_action_keys(len_model)]
    net = AlphaZeroPolicyValueNet(n_obs, n_actions)
    mcts = AlphaZeroFactorizedMCTS(net, config=MCTSConfig(simulations=12, mode="tree"), device=torch.device("cpu"))
    pi, act, value = mcts.run(
        obs=np.zeros(n_obs, dtype=np.float32),
        legal_masks_by_head=legal,
        temperature=1.0,
        env=env,
        len_model=len_model,
    )
    assert len(pi) == len(n_actions)
    assert len(act) == len(n_actions)
    assert -1.0 <= float(value) <= 1.0
