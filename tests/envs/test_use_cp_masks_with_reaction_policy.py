"""Маски use_cp/cp_on при reaction_policy vs legacy."""

import numpy as np

from core.models.reaction_value_policy import make_stratagem_value_policy
from tests.engine.phases._helpers import build_env


def _use_cp_mask(env, side="model"):
    return env.get_legal_action_masks_by_head(side=side)["use_cp"]


def _cp_on_mask(env, side="model"):
    return env.get_legal_action_masks_by_head(side=side)["cp_on"]


def test_legacy_bravery_mask_in_command():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.reaction_policy = None
    env.phase = "command"
    env.modelCP = 2
    m = _use_cp_mask(env)
    assert m[0] and m[1]
    assert not m[2:].any()
    cp = _cp_on_mask(env)
    assert cp.any() and cp.sum() >= 1


def test_reaction_policy_dead_heads():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 2
    env.phase = "command"

    class _StubNet:
        def infer_with_value(self, obs, masks_by_head=None):
            import torch

            return None, torch.tensor([0.0])

    env.reaction_policy = make_stratagem_value_policy({"model": _StubNet()}, device="cpu")
    use_cp = _use_cp_mask(env)
    assert use_cp[0] and not use_cp[1:].any()
    cp_on = _cp_on_mask(env)
    assert cp_on[0] and cp_on.sum() == 1


def test_use_cp_only_none_outside_command():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 2
    env.phase = "movement"
    for rvp in (None, make_stratagem_value_policy({"model": object()}, device="cpu")):
        env.reaction_policy = rvp
        m = _use_cp_mask(env)
        assert m[0] and not m[1:].any()
