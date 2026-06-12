import importlib
import json

import pytest

import reward_config


def _reload_reward_config(monkeypatch, payload):
    if payload is None:
        monkeypatch.delenv("HEUR_CALIBRATION_OVERRIDES_JSON", raising=False)
    else:
        monkeypatch.setenv("HEUR_CALIBRATION_OVERRIDES_JSON", json.dumps(payload))
    return importlib.reload(reward_config)


def test_applies_valid_enemy_heur_weight(monkeypatch):
    rc = _reload_reward_config(monkeypatch, {"ENEMY_HEUR_OBJECTIVE_CONTROL_W": 0.48})
    try:
        assert rc.ENEMY_HEUR_OBJECTIVE_CONTROL_W == pytest.approx(0.48)
        assert rc._HEUR_CALIBRATION_APPLIED_OVERRIDES == {"ENEMY_HEUR_OBJECTIVE_CONTROL_W": 0.48}
    finally:
        _reload_reward_config(monkeypatch, None)


def test_rejects_unknown_key(monkeypatch):
    with pytest.raises(ValueError, match="unknown"):
        _reload_reward_config(monkeypatch, {"ENEMY_HEUR_DOES_NOT_EXIST": 1.0})
    _reload_reward_config(monkeypatch, None)


def test_rejects_feature_flag(monkeypatch):
    with pytest.raises(ValueError, match="feature flag"):
        _reload_reward_config(monkeypatch, {"ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED": 0})
    _reload_reward_config(monkeypatch, None)


def test_rejects_non_numeric_and_negative(monkeypatch):
    with pytest.raises(ValueError, match="numeric"):
        _reload_reward_config(monkeypatch, {"ENEMY_HEUR_RISK_W": "bad"})
    _reload_reward_config(monkeypatch, None)
    with pytest.raises(ValueError, match=">= 0"):
        _reload_reward_config(monkeypatch, {"ENEMY_HEUR_RISK_W": -0.1})
    _reload_reward_config(monkeypatch, None)
