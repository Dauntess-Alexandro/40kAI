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
