import pytest

from core.models.eval_agent import EvalSearchCfg, _apply_az_terminal_metadata, resolve_eval_search_cfg


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


def test_cfg_az_terminal_draw_from_metadata(monkeypatch):
    monkeypatch.delenv("AZ_OUTCOME_VALUE_DRAW", raising=False)
    cfg = resolve_eval_search_cfg("alphazero_tree")
    merged = _apply_az_terminal_metadata(cfg.search, {"outcome_value_draw": -0.7})
    assert merged["terminal_value_draw"] == -0.7


def test_cfg_az_terminal_draw_env_overrides_metadata(monkeypatch):
    monkeypatch.setenv("AZ_OUTCOME_VALUE_DRAW", "-0.4")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    merged = _apply_az_terminal_metadata(cfg.search, {"outcome_value_draw": -0.7})
    assert merged["terminal_value_draw"] == -0.4


def test_cfg_opponent_override_warns(monkeypatch):
    monkeypatch.setenv("AZ_EVAL_OPPONENT_MCTS_SIMS", "8")
    cfg = resolve_eval_search_cfg("alphazero_tree")
    assert cfg.opponent_override_active is True


def test_cfg_gmz_smz_search_params(monkeypatch):
    monkeypatch.setenv("GMZ_EVAL_SIMS", "16")
    cfg = resolve_eval_search_cfg("gumbel_muzero")
    assert cfg.search["num_simulations"] == 16


# --- DQN: управляемый epsilon-режим (вариант 1: DQN→epsilon) ---

def test_cfg_dqn_greedy_default(monkeypatch):
    for k in ("DQN_EVAL_MODE", "DQN_EVAL_EPSILON", "EVAL_EPSILON", "EVAL_DETERMINISTIC"):
        monkeypatch.delenv(k, raising=False)
    cfg = resolve_eval_search_cfg("dqn")
    assert cfg.search["mode"] == "greedy"
    assert cfg.epsilon == 0.0
    assert cfg.search["epsilon"] == 0.0
    assert cfg.deterministic is True


def test_cfg_dqn_epsilon_mode(monkeypatch):
    monkeypatch.setenv("DQN_EVAL_MODE", "epsilon")
    monkeypatch.setenv("DQN_EVAL_EPSILON", "0.25")
    cfg = resolve_eval_search_cfg("dqn")
    assert cfg.search["mode"] == "epsilon"
    assert abs(cfg.epsilon - 0.25) < 1e-9
    assert abs(cfg.search["epsilon"] - 0.25) < 1e-9
    assert cfg.deterministic is False


def test_cfg_dqn_epsilon_clamped(monkeypatch):
    monkeypatch.setenv("DQN_EVAL_MODE", "epsilon")
    monkeypatch.setenv("DQN_EVAL_EPSILON", "5.0")
    cfg = resolve_eval_search_cfg("dqn")
    assert cfg.epsilon == 1.0


def test_cfg_dqn_greedy_forces_zero_epsilon(monkeypatch):
    # В greedy-режиме DQN_EVAL_EPSILON игнорируется (epsilon=0, детерминированно).
    monkeypatch.setenv("DQN_EVAL_MODE", "greedy")
    monkeypatch.setenv("DQN_EVAL_EPSILON", "0.5")
    cfg = resolve_eval_search_cfg("dqn")
    assert cfg.epsilon == 0.0
    assert cfg.deterministic is True


def test_cfg_dqn_epsilon_falls_back_to_eval_epsilon(monkeypatch):
    # CLI-совместимость: при epsilon-режиме без DQN_EVAL_EPSILON берём EVAL_EPSILON.
    monkeypatch.delenv("DQN_EVAL_EPSILON", raising=False)
    monkeypatch.setenv("DQN_EVAL_MODE", "epsilon")
    monkeypatch.setenv("EVAL_EPSILON", "0.1")
    cfg = resolve_eval_search_cfg("dqn")
    assert abs(cfg.epsilon - 0.1) < 1e-9


# --- PPO: управляемая температура (вариант 1: PPO→temperature) ---

def test_cfg_ppo_greedy_default(monkeypatch):
    for k in ("PPO_EVAL_MODE", "PPO_EVAL_TEMPERATURE", "EVAL_DETERMINISTIC"):
        monkeypatch.delenv(k, raising=False)
    cfg = resolve_eval_search_cfg("ppo")
    assert cfg.search["mode"] == "greedy"
    assert cfg.deterministic is True


def test_cfg_ppo_stochastic_mode(monkeypatch):
    monkeypatch.setenv("PPO_EVAL_MODE", "stochastic")
    monkeypatch.setenv("PPO_EVAL_TEMPERATURE", "0.5")
    cfg = resolve_eval_search_cfg("ppo")
    assert cfg.search["mode"] == "stochastic"
    assert abs(cfg.search["temperature"] - 0.5) < 1e-9
    assert cfg.deterministic is False


def test_cfg_ppo_temperature_clamped(monkeypatch):
    monkeypatch.setenv("PPO_EVAL_MODE", "stochastic")
    monkeypatch.setenv("PPO_EVAL_TEMPERATURE", "9.0")
    cfg = resolve_eval_search_cfg("ppo")
    assert cfg.search["temperature"] == 2.0
