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
def _ann_profile(request):
    # Тай-брейк читает reward_config.ANNIHILATION_TIEBREAK_MODE — ключ есть только в
    # annihilation-профиле. Активируем его на время scoring/win-тестов, сбрасываем после.
    # Layout/info-тесты (Task 5) управляют профилем сами через apply_mission_layout —
    # autouse их не трогает, иначе only_war-проверки маскировались бы annihilation-сетапом.
    _layout_or_info = (
        request.node.name.startswith("test_apply_layout")
        or request.node.name.startswith("test_get_info")
    )
    if _layout_or_info:
        yield
        _rc.configure_for_mission("only_war")
        return
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


# ---------------------------------------------------------------------------
# Task 5: Env wiring — reward-профиль в apply_mission_layout + info-поля
# ---------------------------------------------------------------------------

def test_apply_layout_sets_reward_profile():
    env = types.SimpleNamespace()   # apply_mission_layout только выставляет атрибуты
    try:
        M.apply_mission_layout(env, "annihilation")
        assert env.mission_key == "annihilation"
        assert env.mission_scoring_mode == "kill_points"
        assert env.mission_uses_objectives is False
        assert len(env.coordsOfOM) == 1            # фантом-точка
        assert _rc.active_profile_name() == "annihilation"
        assert _rc.VP_OBJECTIVE_HOLD_REWARD == 0    # objective-shaping нейтрализован профилем
    finally:
        _rc.configure_for_mission("only_war")


def test_apply_layout_only_war_keeps_objective_profile():
    env = types.SimpleNamespace()
    try:
        M.apply_mission_layout(env, "only_war")
        assert _rc.active_profile_name() == "only_war"
        assert _rc.VP_OBJECTIVE_HOLD_REWARD != 0
    finally:
        _rc.configure_for_mission("only_war")


def test_apply_layout_training_grounds_uses_only_war_profile():
    env = types.SimpleNamespace()
    try:
        M.apply_mission_layout(env, "training_grounds")
        assert env.mission_key == "training_grounds"
        assert _rc.active_profile_name() == "only_war"
        assert _rc.VP_OBJECTIVE_HOLD_REWARD != 0
    finally:
        _rc.configure_for_mission("only_war")


def test_get_info_exposes_kp_and_mission_fields():
    """get_info() возвращает KP/mission-поля без полного init env."""
    from core.envs.warhamEnv import Warhammer40kEnv

    env = object.__new__(Warhammer40kEnv)
    env.unit_health = [10, 0]
    env.enemy_health = [6, 0]
    env.modelKP = 1
    env.enemyKP = 1
    env.modelCP = 0
    env.enemyCP = 0
    env.unitInAttack = [[0, 0], [0, 0]]
    env.modelVP = 1
    env.enemyVP = 1
    env.mission_name = "Annihilation / Kill Points"
    env.mission_key = "annihilation"
    env.mission_scoring_mode = "kill_points"
    env.numTurns = 5
    env.battle_round = 3
    env.active_side = "model"
    env.phase = "command"
    env.game_over = False
    env._last_movement_meta = {}
    env.model_obj_oc = []
    env.enemy_obj_oc = []
    env._mission_destroyed_enemy_units = {1}
    env._mission_destroyed_model_units = {1}
    env._mission_draw_reason = ""
    # monkeypatch: не нужен реальный pool моделей
    env._alive_models_from_pool = lambda side, i: 1

    info = env.get_info()

    assert info["mission_key"] == "annihilation"
    assert info["mission_scoring_mode"] == "kill_points"
    assert info["model_kill_points"] == 1
    assert info["player_kill_points"] == 1
    assert info["model_destroyed_units"] == 1
    assert info["player_destroyed_units"] == 1
    assert info["mission_draw_reason"] == ""


# ---------------------------------------------------------------------------
# Task 6: Логирование исходов annihilation (winner/draw + tiebreak)
# ---------------------------------------------------------------------------

def test_apply_end_of_battle_logs_kp_outcome():
    env = _ann_env([10, 10], [0, 0, 6])   # model 2 KP -> winner
    logs = []
    M.apply_end_of_battle(env, log_fn=logs.append)
    joined = "\n".join(logs)
    assert "[MISSION][Annihilation]" in joined
    assert "winner=model" in joined
    assert "KP model=2" in joined


def test_apply_end_of_battle_logs_draw_reason():
    env = _ann_env([0, 10], [0, 10])      # по 1 KP, стартовые hp равны -> draw
    env._start_enemy_unit_wounds = [10, 10]
    env._start_model_unit_wounds = [10, 10]
    env.enemy_health = [0, 10]
    env.unit_health = [0, 10]
    logs = []
    M.apply_end_of_battle(env, log_fn=logs.append)
    joined = "\n".join(logs)
    assert "draw" in joined and "reason=equal_kp_and_hp" in joined


def test_max_battle_rounds_per_mission():
    assert M.mission_max_battle_rounds("annihilation") == 8
    assert M.mission_max_battle_rounds("only_war") == 20


def test_annihilation_turn_limit_at_round_9():
    env = _ann_env([10, 10], [0, 0, 6], battle_round=9)   # 9 > 8 -> turn_limit
    over, reason, winner = M.check_end_of_battle(env)
    assert over and reason == "turn_limit"


def test_annihilation_not_over_at_round_8():
    env = _ann_env([10, 10], [6, 6], battle_round=8)      # 8 не > 8, обе стороны живы
    over, reason, winner = M.check_end_of_battle(env)
    assert not over


def test_only_war_continues_at_round_9():
    env = types.SimpleNamespace(unit_health=[10], enemy_health=[10],
                                modelVP=0, enemyVP=0, battle_round=9,
                                mission_key="only_war", mission_scoring_mode="objective_control",
                                game_over=False)
    over, reason, winner = M.check_end_of_battle(env)
    assert not over   # 9 <= 20, Only War продолжается


def test_only_war_turn_limit_log():
    """Regression: Only War лог-формат не должен измениться (без [MISSION][Annihilation])."""
    env = types.SimpleNamespace(
        unit_health=[10], enemy_health=[10],
        modelVP=5, enemyVP=2, battle_round=21,
        mission_key="only_war", mission_scoring_mode="objective_control",
        game_over=False,
    )
    logs = []
    M.apply_end_of_battle(env, log_fn=logs.append)
    joined = "\n".join(logs)
    assert "Game over: turn_limit (after BR" in joined
    assert "(VP 5-2)" in joined
    assert "[MISSION][Annihilation]" not in joined
