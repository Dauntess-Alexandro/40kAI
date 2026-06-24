# tests/core/telemetry/test_stratagem_report.py
from core.telemetry.stratagem_report import (
    SideReport,
    StratagemRow,
    build_stratagem_rows,
    render_csv,
    render_markdown,
    rows_to_csv,
    rows_to_markdown,
)


def _rows():
    return build_stratagem_rows(
        attempts={"command_reroll": 100, "overwatch": 40, "rare": 0},
        applied={"command_reroll": 30, "overwatch": 20, "rare": 5},
        miss={"command_reroll": 70, "overwatch": 20},
        games_used={"command_reroll": 50, "overwatch": 50, "rare": 10},
        wins_used={"command_reroll": 20, "overwatch": 15, "rare": 1},
        games_total=100,
        side_wins_total=33,
    )


def test_basic_metrics():
    rows = {r.stratagem: r for r in _rows()}
    cr = rows["command_reroll"]
    assert cr.attempts == 100 and cr.applied == 30 and cr.miss == 70
    assert cr.apply_rate_pct == 30.0          # 30/100*100
    assert cr.applied_per_game == 0.30        # 30/100
    assert cr.games_used == 50
    assert cr.pct_games == 50.0               # 50/100*100
    assert cr.wr_used == 0.40                 # 20/50
    # notused: games_not=50, wins_not=33-20=13 -> 0.26
    assert cr.wr_notused == 0.26
    assert round(cr.dwr, 4) == round(0.40 - 0.26, 4)


def test_apply_rate_none_when_zero_attempts():
    rows = {r.stratagem: r for r in _rows()}
    assert rows["rare"].attempts == 0
    assert rows["rare"].apply_rate_pct is None  # деления на ноль нет


def test_sorted_by_applied_desc():
    rows = _rows()
    applied = [r.applied for r in rows]
    assert applied == sorted(applied, reverse=True)


def test_wr_notused_none_when_all_games_used():
    rows = {
        r.stratagem: r
        for r in build_stratagem_rows(
            attempts={"x": 10}, applied={"x": 5}, miss={"x": 5},
            games_used={"x": 100}, wins_used={"x": 33},
            games_total=100, side_wins_total=33,
        )
    }
    assert rows["x"].wr_notused is None  # games_not == 0
    assert rows["x"].dwr is None


def test_empty_input_no_crash():
    rows = build_stratagem_rows(
        attempts={}, applied={}, miss={},
        games_used={}, wins_used={}, games_total=0, side_wins_total=0,
    )
    assert rows == []
    md = rows_to_markdown(rows, header_meta={"agent_id": "x", "games": 0, "winrate": 0.0, "date": "2026-06-24"})
    assert "стратагем" in md.lower()  # шапка есть, без падения
    assert "нет данных" in md.lower()
    csv = rows_to_csv(rows)
    assert csv.splitlines()[0].startswith("stratagem,")


def test_markdown_renders_dash_for_none():
    rows = _rows()
    md = rows_to_markdown(rows, header_meta={"agent_id": "ag", "games": 100, "winrate": 0.33, "date": "2026-06-24"})
    assert "| rare |" in md
    assert "—" in md  # apply_rate None отрисован как «—»


def _two_sides():
    learner = build_stratagem_rows(
        attempts={}, applied={"command_reroll": 30, "overwatch": 20},
        miss={}, games_used={"command_reroll": 50, "overwatch": 60},
        wins_used={"command_reroll": 20, "overwatch": 25},
        games_total=100, side_wins_total=33,
    )
    opp = build_stratagem_rows(
        attempts={}, applied={"go_to_ground": 80},
        miss={}, games_used={"go_to_ground": 90},
        wins_used={"go_to_ground": 60},
        games_total=100, side_wins_total=67,
    )
    return [
        SideReport(label="Learner (model)", agent_id="dqn_ag", winrate=0.33, rows=learner),
        SideReport(label="Opponent (enemy)", agent_id="ppo_ag", winrate=0.67, rows=opp),
    ]


def test_render_markdown_two_sections():
    md = render_markdown(_two_sides(), run_meta={"games": 100, "date": "2026-06-24"})
    assert "Learner (model)" in md and "dqn_ag" in md
    assert "Opponent (enemy)" in md and "ppo_ag" in md
    assert "command_reroll" in md and "go_to_ground" in md


def test_render_csv_has_side_column():
    csv = render_csv(_two_sides())
    header = csv.splitlines()[0]
    assert header.startswith("side,stratagem,")
    body = csv.splitlines()[1:]
    assert any(line.startswith("Learner (model),command_reroll,") for line in body)
    assert any(line.startswith("Opponent (enemy),go_to_ground,") for line in body)


def test_render_markdown_empty_side_no_crash():
    sides = [SideReport(label="Opponent (enemy)", agent_id="heuristic", winrate=0.0, rows=[])]
    md = render_markdown(sides, run_meta={"games": 0, "date": "2026-06-24"})
    assert "нет данных" in md.lower()
