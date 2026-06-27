import importlib
import pytest
import reward_config as rc


@pytest.fixture(autouse=True)
def _reset_profile():
    yield
    rc.configure_for_mission("only_war")   # анти-поллюшн


def test_default_profile_is_only_war():
    importlib.reload(rc)
    assert rc.active_profile_name() == "only_war"
    assert rc.VP_OBJECTIVE_HOLD_REWARD != 0   # objective-shaping включён


def test_switch_to_annihilation_zeroes_objective_shaping():
    assert rc.configure_for_mission("annihilation") == "annihilation"
    assert rc.active_profile_name() == "annihilation"
    assert rc.VP_OBJECTIVE_HOLD_REWARD == 0
    assert rc.VP_OBJECTIVE_PROXIMITY_REWARD == 0
    assert rc.KILL_ON_OBJECTIVE_BONUS == 0
    assert rc.MISSION_NO_CONTEST_PENALTY == 0
    assert rc.VP_DIFF_REWARD_SCALE == 0
    assert rc.TURN_LIMIT_DRAW_PENALTY == 0
    assert rc.ANNIHILATION_TIEBREAK_MODE == "destroyed_hp"


def test_combat_shaping_present_in_annihilation():
    rc.configure_for_mission("annihilation")
    assert rc.SHOOT_REWARD_DAMAGE_SCALE != 0   # combat-shaping есть (reward v1)
    assert rc.MELEE_REWARD_DAMAGE_SCALE != 0


def test_training_grounds_uses_only_war_profile():
    assert rc.configure_for_mission("training_grounds") == "only_war"
    assert rc.VP_OBJECTIVE_HOLD_REWARD != 0
