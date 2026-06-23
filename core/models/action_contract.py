from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch

from core.engine.phases.stratagems import STRATAGEM_PHASES

BASE_ACTION_HEADS = ["move", "attack"]


def ordered_action_keys(len_model: int) -> list[str]:
    n = int(len_model)
    keys = list(BASE_ACTION_HEADS)
    keys += [f"move_num_{i}" for i in range(n)]
    keys += [f"shoot_num_{i}" for i in range(n)]
    keys += [f"charge_num_{i}" for i in range(n)]
    for ph in STRATAGEM_PHASES:
        keys.append(f"strat_{ph.value}")
        keys.append(f"strat_{ph.value}_unit")
    return keys


def action_sizes_from_env(env, len_model: int) -> list[int]:
    out: list[int] = []
    for k in ordered_action_keys(len_model):
        sp = env.action_space.spaces[k]
        if hasattr(sp, "n"):
            out.append(int(sp.n))
        elif hasattr(sp, "nvec"):
            out.extend([int(x) for x in sp.nvec])
        else:
            raise TypeError(f"Unsupported action space for {k}: {type(sp)}")
    return out


def action_tensor_to_dict(action, len_model: int) -> dict:
    if torch.is_tensor(action):
        naction = action.detach().cpu().numpy()[0]
    else:
        naction = np.asarray(action)[0]
    keys = ordered_action_keys(int(len_model))
    action_dict: dict[str, int] = {}
    for idx, key in enumerate(keys):
        action_dict[key] = int(naction[idx])
    return action_dict


@dataclass
class FactorizedLegalMasks:
    masks: dict[str, np.ndarray]

    def as_ordered_list(self, len_model: int) -> list[torch.Tensor]:
        out: list[torch.Tensor] = []
        for key in ordered_action_keys(int(len_model)):
            arr = self.masks.get(key)
            if arr is None:
                raise KeyError(f"Missing legal mask for key={key}")
            out.append(torch.as_tensor(arr, dtype=torch.bool))
        return out
