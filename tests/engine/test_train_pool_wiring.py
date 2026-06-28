import os


def test_pool_config_disabled_by_default(monkeypatch):
    for k in list(os.environ):
        if k.startswith("OPPONENT_POOL_"):
            monkeypatch.delenv(k, raising=False)
    from core.engine.opponent_pool import resolve_pool_config

    cfg = resolve_pool_config(section=None)
    assert cfg.enabled is False  # дефолт — пул выключен (нулевая регрессия)


def test_pool_config_env_enable(monkeypatch):
    monkeypatch.setenv("OPPONENT_POOL_ENABLED", "1")
    monkeypatch.setenv("OPPONENT_POOL_P_HEURISTIC", "0.25")
    from core.engine.opponent_pool import resolve_pool_config

    cfg = resolve_pool_config(section=None)
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.25
