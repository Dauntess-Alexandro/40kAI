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
