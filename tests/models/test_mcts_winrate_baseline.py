"""Smoke-тест winrate-baseline harness (Stage 4)."""

from tools.mcts_winrate_baseline import run_baseline


def test_baseline_harness_smoke():
    report = run_baseline(episodes=2, seed=42, modes=["joint", "filter"])
    assert report["episodes"] == 2
    assert "joint" in report["modes"]
    assert "filter" in report["modes"]
    for mode in ("joint", "filter"):
        m = report["modes"][mode]
        assert m["wins"] + m["losses"] + m["draws"] == 2.0
