import pytest
from core.models.sampled_muzero_search import (
    SAMPLED_PRESETS,
    SampledMuZeroSearchConfig,
    make_sampled_search_config,
)


@pytest.mark.parametrize("preset", ["fast", "balanced", "heavy"])
def test_presets_make(preset):
    cfg = make_sampled_search_config(preset=preset)
    exp = SAMPLED_PRESETS[preset]
    assert cfg.num_samples == exp["num_samples"]
    assert cfg.temperature == exp["temperature"]
    assert cfg.prior_weight == exp["prior_weight"]


def test_config_defaults():
    cfg = SampledMuZeroSearchConfig()
    assert cfg.num_samples == 24
    assert cfg.sample_temperature == 1.0
    assert cfg.prior_weight == 0.0
    assert cfg.dedup is True
