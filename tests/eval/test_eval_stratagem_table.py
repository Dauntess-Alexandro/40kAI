from collections import Counter

from eval import _extract_model_stratagem_aggregates, _write_stratagem_report


def _sm():
    sm = Counter()
    # learner (model)
    sm["m_strat_applied_command_reroll"] = 30
    sm["m_strat_games_used_command_reroll"] = 50
    sm["m_strat_wins_used_command_reroll"] = 20
    sm["m_games_total"] = 100
    sm["m_model_wins_total"] = 33
    # opponent (enemy)
    sm["o_strat_applied_go_to_ground"] = 80
    sm["o_strat_games_used_go_to_ground"] = 90
    sm["o_strat_wins_used_go_to_ground"] = 60
    sm["o_opp_wins_total"] = 67
    return sm


def test_extract_model_aggregates_backcompat():
    agg = _extract_model_stratagem_aggregates(_sm())
    assert agg["applied"]["command_reroll"] == 30
    assert agg["games_total"] == 100
    assert agg["model_wins_total"] == 33  # обратная совместимость


def test_write_two_sided_report(tmp_path):
    md_path, csv_path = _write_stratagem_report(
        _sm(), agent_id="dqn_ag", out_dir=str(tmp_path), opponent_agent_id="ppo_ag"
    )
    md = open(md_path, encoding="utf-8").read()
    csv = open(csv_path, encoding="utf-8").read()
    assert "Learner (model)" in md and "command_reroll" in md
    assert "Opponent (enemy)" in md and "go_to_ground" in md
    assert csv.splitlines()[0].startswith("side,stratagem,")
    assert any(l.startswith("Opponent (enemy),go_to_ground,") for l in csv.splitlines())
