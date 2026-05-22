import pytest

from core.models.alphazero_ids import (
    az_mcts_mode_for,
    az_mcts_mode_from_payload,
    az_section_for,
    is_az_algo,
)


def test_is_az_algo_accepts_tree_and_proxy_only():
    assert is_az_algo("alphazero_tree")
    assert is_az_algo("alphazero_proxy")
    assert not is_az_algo("alphazero")
    assert not is_az_algo("ppo")


def test_az_mcts_mode_for_maps_algo_id():
    assert az_mcts_mode_for("alphazero_tree") == "tree"
    assert az_mcts_mode_for("alphazero_proxy") == "proxy"
    with pytest.raises(ValueError):
        az_mcts_mode_for("alphazero")


def test_az_section_for():
    assert az_section_for("alphazero_tree") == "alphazero_tree"
    assert az_section_for("alphazero_proxy") == "alphazero_proxy"


def test_az_mcts_mode_from_payload_prefers_meta():
    assert az_mcts_mode_from_payload("alphazero_tree", {"mcts_mode": "tree"}) == "tree"
    assert az_mcts_mode_from_payload("alphazero_proxy", {}) == "proxy"
