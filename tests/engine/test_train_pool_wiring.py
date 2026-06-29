import os
from pathlib import Path


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


def test_pool_stats_have_single_learner_writer_wiring():
    source = Path("train.py").read_text(encoding="utf-8")
    assert "_pool.stats.save()" not in source
    assert source.count('("pool_result", build_pool_result_payload(') >= 4
    assert source.count('_consume_opponent_pool_message(pool_stats_writer, kind, payload)') == 5
