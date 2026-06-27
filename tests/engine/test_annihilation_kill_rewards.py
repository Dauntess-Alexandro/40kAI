import reward_config as rc


def teardown_function():
    rc.configure_for_mission("only_war")


def test_v2_weights_in_annihilation_profile():
    rc.configure_for_mission("annihilation")
    assert rc.SHOOT_REWARD_KILL_BONUS == 0.9
    assert rc.MELEE_REWARD_KILL_BONUS == 0.9
    assert rc.SHOOT_REWARD_TARGET_LOW_HP == 0.20
    assert rc.SHOOT_REWARD_DAMAGE_SCALE == 0.45
    assert rc.MELEE_REWARD_DAMAGE_SCALE == 0.45
    assert rc.SHOOT_REWARD_OVERKILL_PENALTY == 0.35
    assert rc.DAMAGE_TAKEN_SCALE == 0.45
    assert rc.MELEE_REWARD_TAKEN_SCALE == 0.6
    assert rc.SHOOT_REWARD_SKIP_PENALTY == 0.20


def test_only_war_combat_weights_unchanged():
    rc.configure_for_mission("only_war")
    assert rc.SHOOT_REWARD_KILL_BONUS == 0.4   # v2 не затронул Only War
    assert rc.SHOOT_REWARD_DAMAGE_SCALE == 0.6


def test_opponent_objective_weights_zeroed_in_annihilation():
    rc.configure_for_mission("annihilation")
    assert rc.ENEMY_HEUR_OBJECTIVE_CONTROL_W == 0.0
    assert rc.ENEMY_HEUR_OBJECTIVE_DIST_W == 0.0
    assert rc.ENEMY_HEUR_OBJECTIVE_PRESSURE_W == 0.0
    assert rc.ENEMY_HEUR_SHOOT_OBJECTIVE_W == 0.0
    assert rc.ENEMY_HEUR_CHARGE_OBJECTIVE_W == 0.0
    assert int(rc.ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED) == 0


def test_only_war_opponent_objective_weights_intact():
    rc.configure_for_mission("only_war")
    assert rc.ENEMY_HEUR_OBJECTIVE_CONTROL_W == 0.42


def test_kill_value_flags_present_both_profiles():
    rc.configure_for_mission("only_war")
    assert int(rc.KILL_VALUE_WEIGHT_ENABLED) == 0
    assert rc.KILL_VALUE_NORM == 8.0
    rc.configure_for_mission("annihilation")
    assert int(rc.KILL_VALUE_WEIGHT_ENABLED) == 1
    assert rc.KILL_VALUE_NORM == 8.0
