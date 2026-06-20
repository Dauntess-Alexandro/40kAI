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
