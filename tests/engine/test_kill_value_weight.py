import reward_config as rc
from core.envs.warhamEnv import Warhammer40kEnv


def teardown_function():
    rc.configure_for_mission("only_war")


def _factor(enabled, max_hp):
    rc.configure_for_mission("annihilation" if enabled else "only_war")
    env = object.__new__(Warhammer40kEnv)   # без полного reset
    env.enemy_health = [max_hp]
    env.enemy_data = [{"W": max_hp, "#OfModels": 1}]
    return Warhammer40kEnv._kill_value_factor(env, "enemy", 0)


def test_factor_disabled_is_one():
    # only_war: KILL_VALUE_WEIGHT_ENABLED=0 -> множитель нейтрален
    assert _factor(enabled=False, max_hp=20) == 1.0


def test_factor_scales_with_value():
    assert abs(_factor(enabled=True, max_hp=8) - 1.0) < 1e-6   # max_hp == NORM
    assert _factor(enabled=True, max_hp=40) == 2.5             # клампится сверху
    assert _factor(enabled=True, max_hp=1) == 0.3             # клампится снизу
