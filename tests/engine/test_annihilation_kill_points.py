import types
from core.engine import mission as M


def _fake_env(model_health, enemy_health):
    env = types.SimpleNamespace()
    env.unit_health = list(model_health)
    env.enemy_health = list(enemy_health)
    env._start_model_unit_wounds = list(model_health)
    env._start_enemy_unit_wounds = list(enemy_health)
    env.modelKP = 0
    env.enemyKP = 0
    env.modelVP = 0
    env.enemyVP = 0
    env._mission_destroyed_enemy_units = set()
    env._mission_destroyed_model_units = set()
    return env


def test_kp_counts_destroyed_units():
    env = _fake_env([10, 10], [6, 6, 6])
    env.enemy_health = [0, 6, 0]   # 2 вражеских юнита уничтожены
    M.recompute_kill_points(env)
    assert env.modelKP == 2
    assert env.enemyKP == 0


def test_kp_granted_once_idempotent():
    env = _fake_env([10, 10], [6, 6])
    env.enemy_health = [0, 6]
    M.recompute_kill_points(env)
    M.recompute_kill_points(env)   # повторный вызов не должен «дозасчитать»
    assert env.modelKP == 1


def test_vp_mirrors_kp_for_display():
    env = _fake_env([10], [6, 6])
    env.enemy_health = [0, 0]
    M.recompute_kill_points(env)
    assert env.modelVP == env.modelKP == 2


def test_destroyed_hp_tiebreak_value():
    env = _fake_env([10, 4], [6, 9])
    env.enemy_health = [0, 9]      # убит вражеский юнит со стартовым HP=6
    env.unit_health = [10, 0]      # убит наш юнит со стартовым HP=4
    M.recompute_kill_points(env)
    assert M._destroyed_hp(env, "model") == 6
    assert M._destroyed_hp(env, "enemy") == 4
