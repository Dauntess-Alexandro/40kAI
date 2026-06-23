"""install_dqn_stratagem_policy: value-gate для стратагем (side-generic)."""

import torch

from core.models.dqn_stratagem_bridge import install_dqn_stratagem_policy
from tests.engine.phases._helpers import build_env


def test_install_dqn_side_generic_both_sides():
    class _Q:
        def infer_with_value(self, obs, masks_by_head=None):
            return None, torch.tensor([0.0])

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    p1, p2 = _Q(), _Q()
    install_dqn_stratagem_policy(env, {"model": p1, "enemy": p2}, torch.device("cpu"))
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side == {"model": p1, "enemy": p2}
