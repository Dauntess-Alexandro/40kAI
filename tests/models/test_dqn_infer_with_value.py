"""DQN.infer_with_value: masked max-Q V-proxy."""

import numpy as np
import torch

from core.models.action_contract import action_sizes_from_env, ordered_action_keys
from core.models.DQN import make_dqn
from tests.engine.phases._helpers import build_env


def _tiny_net(env, *, dueling=False, distributional="none"):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    return make_dqn(
        obs_dim,
        sizes,
        dueling=dueling,
        noisy=False,
        distributional=distributional,
    )


def test_infer_with_value_shape_and_finite():
    env = build_env()
    net = _tiny_net(env)
    net.eval()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(2, obs_dim)
    probs, v = net.infer_with_value(obs)
    assert len(probs) > 0
    assert v.shape == (2,)
    assert torch.isfinite(v).all()


def test_masked_max_uses_legal_only():
    env = build_env()
    net = _tiny_net(env, dueling=False)
    net.eval()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(1, obs_dim)
    q_lists = net.q_values(obs)
    keys = ordered_action_keys(len(env.unit_health))
    masks = []
    for idx, q in enumerate(q_lists):
        m = torch.ones(1, q.shape[1], dtype=torch.bool)
        if idx == 0:
            m[0, 0] = True
            m[0, 1:] = False
        masks.append(m)
    _, v = net.infer_with_value(obs, masks_by_head=masks)
    expected_heads = []
    for idx, q in enumerate(q_lists):
        if idx == 0:
            expected_heads.append(q[0, 0])
        else:
            expected_heads.append(q.max(dim=1).values[0])
    expected = torch.stack(expected_heads).mean()
    assert abs(float(v[0].item()) - float(expected.item())) < 1e-5


def test_dueling_and_distributional_smoke():
    env = build_env()
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    obs = torch.randn(1, obs_dim)
    for dueling in (False, True):
        net = _tiny_net(env, dueling=dueling)
        net.eval()
        _, v = net.infer_with_value(obs)
        assert v.shape == (1,) and torch.isfinite(v).all()
    for dist in ("iqn", "c51"):
        net = _tiny_net(env, distributional=dist)
        net.eval()
        _, v = net.infer_with_value(obs)
        assert v.shape == (1,) and torch.isfinite(v).all()
