"""B6: резолв флага phase_obs_features (env↔hyperparams) и понятная ошибка obs-mismatch."""


from core.engine.phases.obs_features import (
    PHASE_OBS_EXTENSION_SIZE,
    describe_obs_dim_mismatch,
    phase_obs_vector,
    resolve_phase_obs_features,
)
from core.engine.phases.stratagems import REGISTRY
from tests.engine.phases._helpers import build_env

# --- resolve_phase_obs_features: env-var приоритетнее hyperparams ---

def test_resolve_uses_cfg_when_env_unset():
    assert resolve_phase_obs_features(env_value=None, cfg_value=1) is True
    assert resolve_phase_obs_features(env_value=None, cfg_value=0) is False


def test_resolve_treats_empty_env_as_unset():
    assert resolve_phase_obs_features(env_value="", cfg_value=1) is True
    assert resolve_phase_obs_features(env_value="   ", cfg_value=0) is False


def test_resolve_env_overrides_cfg():
    assert resolve_phase_obs_features(env_value="1", cfg_value=0) is True
    assert resolve_phase_obs_features(env_value="0", cfg_value=1) is False


def test_resolve_accepts_truthy_words():
    assert resolve_phase_obs_features(env_value="true", cfg_value=0) is True
    assert resolve_phase_obs_features(env_value="on", cfg_value=0) is True
    assert resolve_phase_obs_features(env_value="no", cfg_value=1) is False


# --- describe_obs_dim_mismatch: понятная ошибка при несовпадении размера obs ---

def test_mismatch_none_when_dims_equal():
    assert describe_obs_dim_mismatch(checkpoint_obs_dim=100, current_obs_dim=100) is None


def test_mismatch_hints_phase_obs_toggle_when_off_by_extension():
    msg = describe_obs_dim_mismatch(
        checkpoint_obs_dim=100 + PHASE_OBS_EXTENSION_SIZE,
        current_obs_dim=100,
    )
    assert msg is not None
    assert "phase_obs_features" in msg
    assert str(PHASE_OBS_EXTENSION_SIZE) in msg


def test_mismatch_generic_message_when_unrelated():
    msg = describe_obs_dim_mismatch(checkpoint_obs_dim=120, current_obs_dim=100)
    assert msg is not None
    assert "120" in msg and "100" in msg


# --- obs-фича: бит insane_bravery available в command-фазе (shock-сценарий) ---

def test_insane_bravery_available_bit_in_command_phase(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "command"
    env.modelCP = 1
    tail = phase_obs_vector(env, "model")
    avail_start = 10
    avail = tail[avail_start : avail_start + len(REGISTRY)]
    ids = [d.id for d in REGISTRY]
    assert avail[ids.index("insane_bravery")] == 1.0


def test_insane_bravery_unavailable_without_cp(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.phase = "command"
    env.modelCP = 0
    tail = phase_obs_vector(env, "model")
    avail_start = 10
    avail = tail[avail_start : avail_start + len(REGISTRY)]
    ids = [d.id for d in REGISTRY]
    assert avail[ids.index("insane_bravery")] == 0.0
