from core.engine.phases.stratagems import REGISTRY
from tests.engine.phases._helpers import build_env


def test_obs_length_stable_when_flag_off(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    env = build_env()
    a = len(env.get_observation_for_side("model"))
    b = len(env.get_observation_for_side("model"))
    assert a == b


def test_phase_obs_features_flag_on_appends_block(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "0")
    off = len(build_env().get_observation_for_side("model"))

    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    obs_on = env.get_observation_for_side("model")
    on = len(obs_on)

    # блок = 6 (phase one-hot) + 1 (timing main) + 2 (cp self/enemy norm) + K + K
    k = len(REGISTRY)
    assert on == off + 6 + 1 + 2 + 2 * k


def test_phase_obs_block_phase_onehot_sums_to_one(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.phase = "command"
    obs = env.get_observation_for_side("model")
    k = len(REGISTRY)
    block_len = 6 + 1 + 2 + 2 * k
    block = obs[-block_len:]
    phase_onehot = block[:6]
    assert abs(float(sum(phase_onehot)) - 1.0) < 1e-6


def test_phase_obs_cp_normalized_in_range(monkeypatch):
    monkeypatch.setenv("PHASE_OBS_FEATURES", "1")
    env = build_env()
    env.modelCP = 6
    env.enemyCP = 12
    obs = env.get_observation_for_side("model")
    k = len(REGISTRY)
    block_len = 6 + 1 + 2 + 2 * k
    block = obs[-block_len:]
    cp_self, cp_enemy = float(block[7]), float(block[8])
    assert 0.0 <= cp_self <= 1.5
    assert 0.0 <= cp_enemy <= 1.5
    assert cp_enemy > cp_self  # 12 > 6
