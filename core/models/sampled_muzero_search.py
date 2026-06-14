from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SampledMuZeroSearchConfig:
    num_samples: int = 24            # K joint-сэмплов из приора
    discount: float = 0.997
    temperature: float = 0.15        # τ улучшения политики
    sample_temperature: float = 1.0  # τ_s сэмплинга из приора (β)
    prior_weight: float = 0.0        # подмешивание приора в таргет (0 = несмещённо)
    dedup: bool = True
    tree_reuse: bool = False         # v1: без warm-start (depth-1, свежие сэмплы)


SAMPLED_PRESETS: dict[str, dict] = {
    "fast":     {"num_samples": 12, "temperature": 0.20, "sample_temperature": 1.0, "prior_weight": 0.0},
    "balanced": {"num_samples": 24, "temperature": 0.15, "sample_temperature": 1.0, "prior_weight": 0.0},
    "heavy":    {"num_samples": 48, "temperature": 0.10, "sample_temperature": 1.0, "prior_weight": 0.0},
}


def make_sampled_search_config(preset: str = "balanced", **overrides) -> SampledMuZeroSearchConfig:
    kwargs = SAMPLED_PRESETS.get(preset, SAMPLED_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return SampledMuZeroSearchConfig(**kwargs)
