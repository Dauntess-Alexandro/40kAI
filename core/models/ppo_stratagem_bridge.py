"""PPO ↔ стратагемы: critic-V, side-generic policy install.

Fight-стратагемы применяются через head strat_fight (_apply_action_stratagem).
"""

from __future__ import annotations

import os

import numpy as np
import torch

from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def ppo_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("PPO_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_ppo_stratagem_policy(env, device, net_by_side: dict) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": ac_net}. Both-sides (честный p1/p2) — тот же вызов с
    {"model": p1, "enemy": p2}, без правок движка/bridge. Сторона без сети → legacy.
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def ppo_value(env, ac_net, device, side: str) -> float:
    """critic V(s) для стороны side. Маски не нужны — critic mask-независим."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    with torch.no_grad():
        _, v = ac_net.infer_with_value(obs, masks_by_head=None)
    return float(v.reshape(-1)[0].item())
