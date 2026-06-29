# tests/models/test_phoenix_config.py
from core.models.phoenix_config import resolve_phoenix_config


def test_defaults_when_no_hp_no_env():
    cfg = resolve_phoenix_config(None, {})
    assert cfg.replay_ratio == 2
    assert cfg.reset_interval == 40000
    assert cfg.gamma_start == 0.97 and cfg.gamma_end == 0.99
    assert cfg.nstep_start == 10 and cfg.nstep_end == 3
    assert cfg.noisy is False
    assert cfg.ve_steve is False
    assert cfg.spr_horizon_K == 5 and cfg.ve_horizon == 3


def test_section_overrides_default():
    cfg = resolve_phoenix_config({"phoenix": {"replay_ratio": 8, "shrink_alpha": 0.4}}, {})
    assert cfg.replay_ratio == 8
    assert abs(cfg.shrink_alpha - 0.4) < 1e-9


def test_env_overrides_section():
    hp = {"phoenix": {"replay_ratio": 8}}
    env = {"PHOENIX_REPLAY_RATIO": "16", "PHOENIX_VE_STEVE": "1"}
    cfg = resolve_phoenix_config(hp, env)
    assert cfg.replay_ratio == 16
    assert cfg.ve_steve is True
