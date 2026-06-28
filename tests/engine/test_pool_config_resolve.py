from core.engine.opponent_pool import PoolConfig, resolve_pool_config


def test_defaults_when_empty():
    cfg = resolve_pool_config(section=None, getenv=lambda k: None)
    assert cfg == PoolConfig()  # все дефолты, enabled=False


def test_section_overrides_default():
    section = {"enabled": True, "p_heuristic": 0.4, "pool_size": 5, "strategy": "uniform"}
    cfg = resolve_pool_config(section=section, getenv=lambda k: None)
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.4
    assert cfg.pool_size == 5
    assert cfg.strategy == "uniform"
    assert cfg.pfsp_power == 2.0  # из дефолта


def test_env_overrides_section():
    section = {"enabled": False, "p_heuristic": 0.4, "pool_size": 5}
    env = {"OPPONENT_POOL_ENABLED": "1", "OPPONENT_POOL_P_HEURISTIC": "0.1", "OPPONENT_POOL_SIZE": "12"}
    cfg = resolve_pool_config(section=section, getenv=lambda k: env.get(k))
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.1
    assert cfg.pool_size == 12


def test_clamps_invalid_values():
    env = {"OPPONENT_POOL_SIZE": "0", "OPPONENT_POOL_P_HEURISTIC": "1.5", "OPPONENT_POOL_UNIFORM_FLOOR": "-0.2"}
    cfg = resolve_pool_config(section=None, getenv=lambda k: env.get(k))
    assert cfg.pool_size == 1          # >=1
    assert cfg.p_heuristic == 1.0      # [0,1]
    assert cfg.uniform_floor == 0.0    # [0,1]
