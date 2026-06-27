from core.engine import mission as M


def test_annihilation_registered_and_aliased():
    assert M.normalize_mission_name("annihilation") == "annihilation"
    assert M.normalize_mission_name("purge_the_enemy") == "annihilation"
    assert M.normalize_mission_name("kill_points") == "annihilation"


def test_annihilation_board_is_like_only_war():
    assert M.board_dims_for_mission("annihilation") == (
        M.ONLY_WAR_BOARD_HEIGHT_INCH, M.ONLY_WAR_BOARD_WIDTH_INCH)


def test_annihilation_has_phantom_single_objective():
    coords = M.objective_coords_for_mission("annihilation", 40, 60)
    assert len(coords) == 1  # фантом: obs остаётся как у Only War


def test_mission_flag_helpers():
    assert M.mission_scoring_mode("annihilation") == "kill_points"
    assert M.mission_scoring_mode("only_war") == "objective_control"
    assert M.mission_uses_objectives("annihilation") is False
    assert M.mission_uses_objectives("only_war") is True
    assert M.is_annihilation_mission("purge_the_enemy") is True
    assert M.is_annihilation_mission("only_war") is False
