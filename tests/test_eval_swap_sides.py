from eval import _aggregate_swap


def test_aggregate_swap_averages_per_color():
    # Назначение A: agentA как model выиграл 6/10; назначение B (swap): agentA как enemy выиграл 4/10.
    res_a = {"model_wins": 6, "enemy_wins": 4, "draws": 0, "games": 10}
    res_b = {"model_wins": 5, "enemy_wins": 5, "draws": 0, "games": 10}
    agg = _aggregate_swap(res_a, res_b)
    # agentA winrate = (model в A + enemy в B) / 2N = (6 + 5) / 20
    assert abs(agg["agentA_winrate"] - 11 / 20) < 1e-9
    assert abs(agg["agentB_winrate"] - 9 / 20) < 1e-9
    assert agg["total_games"] == 20
