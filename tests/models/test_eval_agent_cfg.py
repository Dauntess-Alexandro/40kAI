import pytest
from core.models.eval_agent import EvalSearchCfg, resolve_eval_search_cfg


def test_cfg_defaults_deterministic(monkeypatch):
    for k in ("EVAL_DETERMINISTIC", "EVAL_EPSILON", "AZ_EVAL_MCTS_SIMS"):
        monkeypatch.delenv(k, raising=False)
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert isinstance(cfg, EvalSearchCfg)
    assert cfg.deterministic is True
    assert cfg.epsilon == 0.0
    assert cfg.search["simulations"] == 32


def test_cfg_reads_unified_az_temperature(monkeypatch):
    monkeypatch.setenv("AZ_EVAL_MCTS_TEMPERATURE", "0.20")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert abs(cfg.search["temperature"] - 0.20) < 1e-9


def test_cfg_opponent_override_warns(monkeypatch):
    monkeypatch.setenv("AZ_EVAL_OPPONENT_MCTS_SIMS", "8")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert cfg.opponent_override_active is True


def test_cfg_gmz_smz_search_params(monkeypatch):
    monkeypatch.setenv("GMZ_EVAL_SIMS", "16")
    cfg = resolve_eval_search_cfg("gumbel_muzero")
    assert cfg.search["num_simulations"] == 16
