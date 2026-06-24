from collections import Counter

from eval import _extract_model_stratagem_aggregates, _write_stratagem_report


def _sm():
    sm = Counter()
    # model-only per-sid (префикс m_), заполняется парсером eval
    sm["m_strat_attempt_command_reroll"] = 100
    sm["m_strat_applied_command_reroll"] = 30
    sm["m_strat_miss_command_reroll"] = 70
    sm["m_strat_games_used_command_reroll"] = 50
    sm["m_strat_wins_used_command_reroll"] = 20
    sm["m_games_total"] = 100
    sm["m_model_wins_total"] = 33
    return sm


def test_extract_aggregates():
    agg = _extract_model_stratagem_aggregates(_sm())
    assert agg["attempts"]["command_reroll"] == 100
    assert agg["applied"]["command_reroll"] == 30
    assert agg["miss"]["command_reroll"] == 70
    assert agg["games_used"]["command_reroll"] == 50
    assert agg["wins_used"]["command_reroll"] == 20
    assert agg["games_total"] == 100
    assert agg["model_wins_total"] == 33


def test_write_report_creates_files(tmp_path):
    md_path, csv_path = _write_stratagem_report(_sm(), agent_id="ag", out_dir=str(tmp_path))
    md = open(md_path, encoding="utf-8").read()
    csv = open(csv_path, encoding="utf-8").read()
    assert "command_reroll" in md
    assert csv.splitlines()[0].startswith("stratagem,")
    assert "command_reroll" in csv
