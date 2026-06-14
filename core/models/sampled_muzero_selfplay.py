from __future__ import annotations

from core.models.gumbel_muzero_selfplay import (
    GumbelSelfPlayConfig as SampledSelfPlayConfig,
)
from core.models.gumbel_muzero_selfplay import (
    play_episode_with_gumbel_muzero,
)

__all__ = ["SampledSelfPlayConfig", "play_episode_with_sampled_muzero"]


def play_episode_with_sampled_muzero(**kwargs):
    """Прогон эпизода с sampled-поиском. selfplay-петля идентична gmz: search.run имеет
    ту же сигнатуру, поэтому переиспользуем play_episode_with_gumbel_muzero как есть."""
    return play_episode_with_gumbel_muzero(**kwargs)
