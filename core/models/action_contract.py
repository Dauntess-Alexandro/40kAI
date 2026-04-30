from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
import torch


BASE_ACTION_HEADS = ["move", "attack", "shoot", "charge", "use_cp", "cp_on"]


def ordered_action_keys(len_model: int) -> list[str]:
    keys = list(BASE_ACTION_HEADS)
    for i_u in range(int(len_model)):
        keys.append(f"move_num_{i_u}")
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
    action_dict: Dict[str, int] = {}
    for idx, key in enumerate(keys):
        action_dict[key] = int(naction[idx])
    return action_dict


@dataclass
class FactorizedLegalMasks:
    masks: dict[str, np.ndarray]

    def as_ordered_list(self, len_model: int) -> List[torch.Tensor]:
        out: List[torch.Tensor] = []
        for key in ordered_action_keys(int(len_model)):
            arr = self.masks.get(key)
            if arr is None:
                raise KeyError(f"Missing legal mask for key={key}")
            out.append(torch.as_tensor(arr, dtype=torch.bool))
        return out
