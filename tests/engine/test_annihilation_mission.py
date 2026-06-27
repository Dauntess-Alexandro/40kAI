import types

import pytest

import reward_config as _rc
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


# ---------------------------------------------------------------------------
# Task 4: Scoring & win-condition dispatch (kill_points + tiebreak)
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _ann_profile():
    # Тай-брейк читает reward_config.ANNIHILATION_TIEBREAK_MODE — ключ есть только в
    # annihilation-профиле. Активируем его на время тестов файла, сбрасываем после.
    _rc.configure_for_mission("annihilation")
    yield
    _rc.configure_for_mission("only_war")


def _ann_env(model_health, enemy_health, *, battle_round=21):
    env = types.SimpleNamespace()
    env.unit_health = list(model_health)
    env.enemy_health = list(enemy_health)
    env._start_model_unit_wounds = list(model_health)
    env._start_enemy_unit_wounds = list(enemy_health)
    env.modelKP = env.enemyKP = env.modelVP = env.enemyVP = 0
    env._mission_destroyed_enemy_units = set()
    env._mission_destroyed_model_units = set()
    env.mission_key = "annihilation"
    env.mission_scoring_mode = "kill_points"
    env.battle_round = battle_round
    env.game_over = False
    return env


def test_command_phase_no_objective_vp_in_annihilation():
    env = _ann_env([10], [6, 0])
    gained = M.score_end_of_command_phase(env, "model")
    assert gained == 0                 # objective VP не начисляется
    assert env.modelKP == 1            # но KP пересчитан


def test_turn_limit_winner_by_kp():
    env = _ann_env([10, 10], [0, 0, 6])   # model убила 2 вражеских юнита
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "turn_limit" and winner == "model"


def test_turn_limit_equal_kp_tiebreak_destroyed_hp():
    # равные KP (по 1), но model снёс юнит с большим стартовым HP -> побеждает по destroyed_hp
    env = _ann_env([10, 4], [7, 9])       # стартовые раны: model=[10,4], enemy=[7,9]
    env.enemy_health = [0, 9]             # model убил enemy#0 (start HP 7)
    env.unit_health = [10, 0]             # enemy убил model#1 (start HP 4)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and winner == "model"     # 7 > 4


def test_wipeout_enemy_winner_model():
    env = _ann_env([10], [0, 0], battle_round=3)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "wipeout_enemy" and winner == "model"


def test_only_war_turn_limit_unchanged():
    env = types.SimpleNamespace(unit_health=[10], enemy_health=[10],
                                modelVP=5, enemyVP=2, battle_round=21,
                                mission_key="only_war", mission_scoring_mode="objective_control",
                                game_over=False)
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "turn_limit" and winner == "model"
