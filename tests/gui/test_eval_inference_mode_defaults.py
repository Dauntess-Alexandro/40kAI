"""Режим инференса eval: дефолты search/mcts/gumbel не сбрасываются на greedy при эвристике."""

from __future__ import annotations

import pytest

from app.gui_qt.main import (
    _coerce_eval_inference_mode,
    _default_inference_mode_for_algo,
    _valid_inference_modes_for_algo,
)


@pytest.mark.parametrize(
    ("algo", "expected"),
    [
        ("alphazero_tree", "mcts"),
        ("alphazero_proxy", "mcts"),
        ("gumbel_muzero", "search"),
        ("sampled_muzero", "search"),
        ("gumbel_az", "gumbel"),
        # DQN/PPO: дефолт greedy (поведение как раньше).
        ("dqn", "greedy"),
        ("ppo", "greedy"),
    ],
)
def test_default_inference_mode_for_algo(algo: str, expected: str) -> None:
    assert _default_inference_mode_for_algo(algo) == expected


def test_valid_modes_dqn_ppo() -> None:
    assert _valid_inference_modes_for_algo("dqn") == {"greedy", "epsilon"}
    assert _valid_inference_modes_for_algo("ppo") == {"greedy", "stochastic"}


def test_coerce_dqn_ppo_modes() -> None:
    assert _coerce_eval_inference_mode("epsilon", "dqn") == "epsilon"
    assert _coerce_eval_inference_mode("stochastic", "ppo") == "stochastic"
    # Чужой режим коэрсится в дефолт (greedy).
    assert _coerce_eval_inference_mode("mcts", "dqn") == "greedy"
    assert _coerce_eval_inference_mode("epsilon", "ppo") == "greedy"


def test_coerce_preserves_search_when_side_is_heuristic() -> None:
    """Эвристика (algo пустой): search/mcts не затираются в greedy."""
    assert _coerce_eval_inference_mode("search", "") == "search"
    assert _coerce_eval_inference_mode("mcts", "") == "mcts"
    assert _coerce_eval_inference_mode("gumbel", "") == "gumbel"


def test_coerce_restores_algo_default_after_heuristic_roundtrip() -> None:
    """Агент снова выбран: сохранённый search/mcts остаётся валидным."""
    assert _coerce_eval_inference_mode("search", "sampled_muzero") == "search"
    assert _coerce_eval_inference_mode("search", "gumbel_muzero") == "search"
    assert _coerce_eval_inference_mode("mcts", "alphazero_tree") == "mcts"


def test_coerce_fixes_invalid_mode_for_algo() -> None:
    assert _coerce_eval_inference_mode("mcts", "sampled_muzero") == "search"
    assert _coerce_eval_inference_mode("search", "alphazero_tree") == "mcts"
    assert _coerce_eval_inference_mode("greedy", "sampled_muzero") == "greedy"


def test_coerce_heuristic_then_agent_no_greedy_corruption() -> None:
    """Сценарий: SMZ search → эвристика → тот же SMZ — не greedy."""
    mode = "search"
    mode = _coerce_eval_inference_mode(mode, "sampled_muzero")
    assert mode == "search"
    mode = _coerce_eval_inference_mode(mode, "")
    assert mode == "search"
    mode = _coerce_eval_inference_mode(mode, "sampled_muzero")
    assert mode == "search"
