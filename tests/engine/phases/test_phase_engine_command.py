from tests.engine.phases._helpers import build_env


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    a = {"move": 4, "attack": 1, "shoot": 0, "charge": 0, "use_cp": use_cp, "cp_on": cp_on}
    for i in range(n):
        a[f"move_num_{i}"] = 0
    return a


def _setup_failing_unit0(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_data[0]["Ld"] = 13  # 2D6 <= 12 < 13 → battle-shock всегда провален
    env.unit_health[0] = 1.0
    env.modelCP = 2


def test_decide_bravery_equivalent_to_action():
    n_env = build_env()
    _setup_failing_unit0(n_env)
    n = len(n_env.unit_health)
    snap = n_env.snapshot_state()

    with n_env.simulation_mode():
        bs_a, r_a = n_env.command_phase("model", action=_action(1, 0, n))
        cp_a, used_a = n_env.modelCP, list(n_env.stratagem_used)
    n_env.restore_state(snap)

    with n_env.simulation_mode():
        bs_b, r_b = n_env.command_phase("model", action=_action(0, 0, n), decide_bravery=lambda i: i == 0)
        cp_b, used_b = n_env.modelCP, list(n_env.stratagem_used)
    n_env.restore_state(snap)

    assert bs_a == bs_b
    assert r_a == r_b
    assert cp_a == cp_b
    assert used_a == used_b
    assert bs_a[0] is False  # bravery спасла юнит 0 в обоих путях


def test_decide_bravery_false_keeps_battleshock():
    env = build_env()
    _setup_failing_unit0(env)
    n = len(env.unit_health)
    snap = env.snapshot_state()
    with env.simulation_mode():
        bs, _r = env.command_phase("model", action=_action(0, 0, n), decide_bravery=lambda i: False)
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert bs[0] is True
    assert used == []
