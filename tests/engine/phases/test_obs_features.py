import os

import numpy as np
import pytest

from core.engine.phases.obs_features import (
    PHASE_OBS_EXTENSION_SIZE,
    append_phase_obs_features,
    base_observation_length,
    build_phase_obs_signature_suffix,
    phase_obs_features_enabled,
    phase_obs_vector,
)
from core.engine.phases.stratagems import REGISTRY
from tests.engine.phases._helpers import build_env


def test_phase_obs_features_disabled_by_default(monkeypatch):
    monkeypatch.delenv("PHASE_OBS_FEATURES", raising=False)
    assert phase_obs_features_enabled() is False


def test_phase_obs_features_enabled_from_env(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    assert phase_obs_features_enabled() is True


def test_base_observation_length_matches_legacy_vector(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    obs = env.get_observation_for_side("model")
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    n_om = len(env.coordsOfOM)
    assert len(obs) == base_observation_length(n_model, n_enemy, n_om)


def test_phase_obs_disabled_does_not_change_vector(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    obs0 = env.get_observation_for_side("model").copy()
    env.modelCP = 3
    env.phase = "fight"
    obs1 = env.get_observation_for_side("model")
    assert len(obs1) == len(obs0)
    assert obs1.shape == obs0.shape


def test_phase_obs_enabled_extends_vector(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    obs = env.get_observation_for_side("model")
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    n_om = len(env.coordsOfOM)
    assert len(obs) == base_observation_length(n_model, n_enemy, n_om) + PHASE_OBS_EXTENSION_SIZE
    assert env.observation_space.shape[0] == len(obs)


def test_phase_obs_one_hot_command_phase(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "command"
    tail = phase_obs_vector(env, "model")
    phase_block = tail[:6]
    assert phase_block == pytest.approx([1, 0, 0, 0, 0, 0])


def test_phase_obs_cp_normalized(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 6
    env.enemyCP = 3
    tail = phase_obs_vector(env, "model")
    cp_self, cp_opp = tail[8], tail[9]
    assert cp_self == pytest.approx(0.5)
    assert cp_opp == pytest.approx(0.25)


def test_phase_obs_fight_stratagem_available_with_cp(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "fight"
    env.modelCP = 2
    tail = phase_obs_vector(env, "model")
    avail_start = 10
    avail = tail[avail_start : avail_start + len(REGISTRY)]
    ids = [d.id for d in REGISTRY]
    assert avail[ids.index("hungry_void")] == 1.0
    assert avail[ids.index("command_reroll")] == 1.0


def test_phase_obs_deterministic(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "movement"
    env.modelCP = 2
    a = phase_obs_vector(env, "model")
    b = phase_obs_vector(env, "model")
    assert a == pytest.approx(b)


def test_build_phase_obs_signature_suffix():
    assert build_phase_obs_signature_suffix(False) == ""
    assert build_phase_obs_signature_suffix(True) == f"+phase{PHASE_OBS_EXTENSION_SIZE}"
