from __future__ import annotations

import os

from core.models.gumbel_muzero_model import (
    GMZ_PRESETS as SAMPLED_NET_PRESETS,
)
from core.models.gumbel_muzero_model import (
    GumbelMuZeroNet as SampledMuZeroNet,
)
from core.models.gumbel_muzero_model import (
    load_gumbel_muzero_state_dict as load_sampled_muzero_state_dict,
)

__all__ = [
    "SampledMuZeroNet", "SAMPLED_NET_PRESETS", "load_sampled_muzero_state_dict",
    "make_sampled_muzero_net", "sampled_muzero_kwargs_from_env", "sampled_muzero_arch_from_payload",
]


def sampled_muzero_kwargs_from_env() -> dict:
    preset = SAMPLED_NET_PRESETS.get(os.getenv("SMZ_PRESET", "balanced").lower(),
                                     SAMPLED_NET_PRESETS["balanced"]).copy()
    return {
        "latent_dim": int(os.getenv("SMZ_LATENT_DIM", str(preset["latent_dim"]))),
        "hidden_dim": int(os.getenv("SMZ_HIDDEN_DIM", str(preset["hidden_dim"]))),
        "num_layers": int(os.getenv("SMZ_NUM_LAYERS", str(preset["num_layers"]))),
        "action_embed_dim": int(os.getenv("SMZ_ACTION_EMBED_DIM", str(preset["action_embed_dim"]))),
    }


def sampled_muzero_arch_from_payload(payload: dict | None) -> dict:
    out = sampled_muzero_kwargs_from_env()
    if isinstance(payload, dict) and isinstance(payload.get("arch"), dict):
        for k in ("latent_dim", "hidden_dim", "num_layers", "action_embed_dim"):
            if k in payload["arch"]:
                out[k] = int(payload["arch"][k])
    return out


def make_sampled_muzero_net(obs_dim, action_sizes, **overrides) -> SampledMuZeroNet:
    kwargs = sampled_muzero_kwargs_from_env()
    kwargs.update(overrides)
    return SampledMuZeroNet(obs_dim, action_sizes, **kwargs)
