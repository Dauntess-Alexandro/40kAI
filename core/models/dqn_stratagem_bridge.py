"""DQN ↔ стратагемы: V-proxy (masked max-Q), policy install.

Реакции (reaction_value_policy) поверх DQN.infer_with_value.
Fight-стратагемы применяются через голову strat_fight (_apply_action_stratagem).
"""

from __future__ import annotations

import os

import numpy as np
import torch

from core.models.action_contract import ordered_action_keys
from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def dqn_reaction_value_policy_enabled(default: str = "1") -> bool:
    raw = str(os.getenv("DQN_REACTION_VALUE_POLICY", default)).strip().lower()
    return raw in _TRUTHY


def install_dqn_stratagem_policy(env, net_by_side: dict, device) -> None:
    """Value-gate для стратагем. Side-generic: net_by_side = {side: net}.

    v1 кладёт {"model": net} (learner-only). Both-sides (честный p1/p2) — тот же
    вызов с {"model": p1, "enemy": p2}, без правок движка/bridge. Сторона без сети → legacy.
    """
    from core.models.reaction_value_policy import make_stratagem_value_policy

    e = unwrap_env(env)
    e._reaction_net_by_side = dict(net_by_side)
    e.reaction_policy = make_stratagem_value_policy(e._reaction_net_by_side, device=device)


def _masks_for_side(env, side: str, device) -> list:
    """Legal action masks в порядке ordered_action_keys — для masked max-Q."""
    e = unwrap_env(env)
    legal = e.get_legal_action_masks_by_head(side=side)
    # action_space и сеть размерены по len(model)=len(unit_data); маски enemy идут по тем же
    # model-space ключам. len(enemy_data) → KeyError move_num_{i} при асимметрии армий.
    # Тот же инвариант, что в warhamEnv._reaction_net_value.
    n_units = len(e.unit_data)
    keys = ordered_action_keys(int(n_units))
    return [
        torch.tensor(legal[k], dtype=torch.bool, device=device).unsqueeze(0)
        for k in keys
    ]


def dqn_value(env, policy_net, device, side: str) -> float:
    """max-Q V(s) для стороны side (masked infer_with_value)."""
    e = unwrap_env(env)
    obs = torch.tensor(
        np.asarray([e.get_observation_for_side(side)], dtype=np.float32),
        device=device,
    )
    masks = _masks_for_side(e, side, device)
    with torch.no_grad():
        _, v = policy_net.infer_with_value(obs, masks_by_head=masks)
    return float(v.reshape(-1)[0].item())
