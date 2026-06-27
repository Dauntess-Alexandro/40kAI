from app.gui_qt.main import GUIController


def _controller_stub() -> GUIController:
    ctrl = GUIController.__new__(GUIController)
    ctrl._mission_options = ["only_war", "annihilation"]
    ctrl._eval_games = 50
    ctrl._eval_p1_policy = "agent"
    ctrl._eval_p2_policy = "agent"
    ctrl._eval_selected_p1_agent_id = "p1_ann"
    ctrl._eval_selected_p2_agent_id = "p2_ann"
    ctrl._learner_faction = "Necrons"
    ctrl._player_roster = []
    ctrl._model_roster = []
    ctrl._unit_faction_by_name = {}
    ctrl._eval_agent_meta_by_id = {
        "p1_ann": {
            "agent_id": "p1_ann",
            "side": "P1",
            "faction": "Necrons",
            "algo": "ppo",
            "mission_name": "annihilation",
            "ruleset_version": "annihilation_v2",
        },
        "p2_ann": {
            "agent_id": "p2_ann",
            "side": "P2",
            "faction": "Necrons",
            "algo": "dqn",
            "mission_name": "annihilation",
            "ruleset_version": "annihilation_v2",
        },
        "p2_only": {
            "agent_id": "p2_only",
            "side": "P2",
            "faction": "Necrons",
            "algo": "dqn",
            "mission_name": "only_war",
            "ruleset_version": "only_war_v2",
        },
    }
    return ctrl


def test_eval_launch_uses_agent_mission_and_ruleset():
    ctrl = _controller_stub()

    ok, cfg, err = ctrl._build_eval_launch_config()

    assert ok, err
    assert cfg["mission_name"] == "annihilation"
    assert cfg["ruleset_version"] == "annihilation_v2"
    assert cfg["learner_side"] == "P1"
    assert cfg["learner_agent_id"] == "p1_ann"
    assert cfg["opponent_agent_id"] == "p2_ann"


def test_eval_launch_blocks_agent_mission_mismatch():
    ctrl = _controller_stub()
    ctrl._eval_selected_p2_agent_id = "p2_only"

    ok, cfg, err = ctrl._build_eval_launch_config()

    assert not ok
    assert cfg == {}
    assert "Несовместимые миссии eval" in err
    assert "P1=ANNIHILATION" in err
    assert "P2=ONLY WAR" in err


def test_eval_launch_uses_p2_mission_when_p1_is_heuristic():
    ctrl = _controller_stub()
    ctrl._eval_p1_policy = "heuristic"
    ctrl._eval_p2_policy = "agent"
    ctrl._eval_selected_p2_agent_id = "p2_ann"

    ok, cfg, err = ctrl._build_eval_launch_config()

    assert ok, err
    assert cfg["mission_name"] == "annihilation"
    assert cfg["ruleset_version"] == "annihilation_v2"
    assert cfg["learner_side"] == "P2"
    assert cfg["learner_agent_id"] == "p2_ann"
    assert cfg["opponent_agent_id"] == ""


def test_eval_heuristic_p2_card_gets_series_mission_badge():
    ctrl = _controller_stub()
    ctrl._eval_p1_policy = "agent"
    ctrl._eval_p2_policy = "heuristic"

    ctrl._update_eval_matchup_text()

    assert "MISSION: ANNIHILATION" in ctrl._eval_p2_badges
