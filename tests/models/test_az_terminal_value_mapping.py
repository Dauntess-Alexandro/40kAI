from __future__ import annotations

import json
from pathlib import Path

from core.models.az_rollout_sink import build_az_dist_worker_payloads, build_gaz_dist_worker_payloads
from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig
from core.models.gumbel_alphazero_search import _terminal_value_from_info as gaz_terminal_value


def test_az_mcts_turn_limit_draw_uses_configured_value():
    mcts = AlphaZeroFactorizedMCTS(
        policy_value_net=None,
        config=MCTSConfig(terminal_value_draw=-0.7),
    )

    assert mcts._terminal_value_from_info({"end reason": "turn_limit"}) == -0.7


def test_az_mcts_turn_limit_vp_win_stays_win():
    mcts = AlphaZeroFactorizedMCTS(
        policy_value_net=None,
        config=MCTSConfig(terminal_value_draw=-0.7),
    )

    assert mcts._terminal_value_from_info({"winner": "model", "end reason": "turn_limit"}) == 1.0


def test_gaz_turn_limit_draw_uses_configured_value():
    assert gaz_terminal_value({"end reason": "turn_limit"}, value_draw=-0.7) == -0.7


def test_gaz_turn_limit_vp_win_stays_win():
    assert gaz_terminal_value({"winner": "model", "end reason": "turn_limit"}, value_draw=-0.7) == 1.0


def test_dist_payload_carries_outcome_values_into_search_config():
    hp = {
        "outcome_value_win": 0.8,
        "outcome_value_loss": -0.9,
        "outcome_value_draw": -0.7,
    }

    az_payloads = build_az_dist_worker_payloads(hp, defaults={})
    assert az_payloads["mcts"]["terminal_value_win"] == 0.8
    assert az_payloads["mcts"]["terminal_value_loss"] == -0.9
    assert az_payloads["mcts"]["terminal_value_draw"] == -0.7

    gaz_payloads = build_gaz_dist_worker_payloads(hp, defaults={})
    assert gaz_payloads["mcts"]["terminal_value_win"] == 0.8
    assert gaz_payloads["mcts"]["terminal_value_loss"] == -0.9
    assert gaz_payloads["mcts"]["terminal_value_draw"] == -0.7


def test_search_algorithms_have_negative_draw_outcome_in_hyperparams():
    hp_path = Path(__file__).resolve().parents[2] / "hyperparams.json"
    hp = json.loads(hp_path.read_text(encoding="utf-8"))

    for section in ("alphazero_tree", "gumbel_az", "gumbel_muzero", "sampled_muzero"):
        cfg = hp[section]
        assert int(cfg["outcome_only"]) == 1
        assert float(cfg["outcome_value_draw"]) < 0.0
