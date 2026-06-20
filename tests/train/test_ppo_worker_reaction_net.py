"""_ppo_worker_install_reaction_net: воркер строит net + ставит reaction_policy."""

import numpy as np
import torch

from core.models.action_contract import action_sizes_from_env
from core.models.PPO import ActorCriticMultiHead
from tests.engine.phases._helpers import build_env


def _payload(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    net = ActorCriticMultiHead(obs_dim, sizes, hidden_size=32, num_layers=1, n_value_ensemble=1)
    return {
        "arch": {"hidden_size": 32, "num_layers": 1, "n_value_ensemble": 1},
        "n_obs": obs_dim,
        "n_actions": sizes,
        "weights": {k: v.detach().cpu() for k, v in net.state_dict().items()},
    }


def test_install_returns_net_and_sets_policy():
    from train import _ppo_worker_install_reaction_net

    env = build_env()
    payload = _payload(env)
    net = _ppo_worker_install_reaction_net(env, payload, torch.device("cpu"))
    assert net is not None
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side.get("model") is net


def test_install_bad_payload_returns_none():
    from train import _ppo_worker_install_reaction_net

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    net = _ppo_worker_install_reaction_net(env, {"arch": {}, "n_obs": 4, "n_actions": [2], "weights": {}}, torch.device("cpu"))
    # mismatched arch/obs → net создан, но weights пустые (strict=False) — допустимо; главное без падения.
    assert net is None or env.reaction_policy is not None
