from __future__ import annotations

import pytest


def test_parse_clip_reward_off_disables():
    import train

    enabled, lo, hi = train.parse_clip_reward_config("off")
    assert enabled is False
    assert lo is None
    assert hi is None
    assert train.format_clip_reward_effective("off", enabled, lo, hi) == (
        "[TRAIN][CONFIG] CLIP_REWARD=off effective=disabled"
    )


def test_parse_clip_reward_one_keeps_legacy_unit_clip():
    import train

    enabled, lo, hi = train.parse_clip_reward_config("1")
    assert enabled is True
    assert lo == pytest.approx(-1.0)
    assert hi == pytest.approx(1.0)
    assert train.format_clip_reward_effective("1", enabled, lo, hi) == (
        "[TRAIN][CONFIG] CLIP_REWARD=1 effective=[-1.000,1.000]"
    )


def test_parse_clip_reward_range():
    import train

    enabled, lo, hi = train.parse_clip_reward_config("-5,5")
    assert enabled is True
    assert lo == pytest.approx(-5.0)
    assert hi == pytest.approx(5.0)
    assert train.format_clip_reward_effective("-5,5", enabled, lo, hi) == (
        "[TRAIN][CONFIG] CLIP_REWARD=-5,5 effective=[-5.000,5.000]"
    )
