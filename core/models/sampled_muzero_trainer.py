from __future__ import annotations

from core.models.gumbel_muzero_trainer import (
    GumbelMuZeroEMATarget as SampledMuZeroEMATarget,
)
from core.models.gumbel_muzero_trainer import (
    GumbelMuZeroTrainConfig as SampledMuZeroTrainConfig,
)
from core.models.gumbel_muzero_trainer import (
    make_gmz_lr_scheduler as make_smz_lr_scheduler,
)
from core.models.gumbel_muzero_trainer import (
    train_gumbel_muzero_step,
)

__all__ = [
    "SampledMuZeroTrainConfig", "SampledMuZeroEMATarget",
    "make_smz_lr_scheduler", "train_sampled_muzero_step",
]


def train_sampled_muzero_step(**kwargs):
    """policy-таргет уже запечён sampled-поиском на self-play → learner идентичен gmz."""
    return train_gumbel_muzero_step(**kwargs)
