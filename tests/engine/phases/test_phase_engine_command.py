from core.engine.phases import phase_engine
from core.engine.phases.stratagems import stratagem_action_choices
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env, flat_default_action


def _bravery_idx():
    return stratagem_action_choices(Phase.COMMAND).index("insane_bravery")


def _action(use_cp: int, cp_on: int, n: int) -> dict:
    return flat_default_action(n, use_cp=int(use_cp), cp_on=int(cp_on))


def _action_bravery(n: int, unit: int = 0) -> dict:
    """Action с strat_command=insane_bravery, нацеленный на юнит `unit`."""
    a = flat_default_action(n)
    a["strat_command"] = _bravery_idx()
    a["strat_command_unit"] = unit
    return a


def _action_no_bravery(n: int) -> dict:
    """Action без bravery (strat_command=0 → none)."""
    return flat_default_action(n)


def _setup_failing_unit0(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_data[0]["Ld"] = 13  # 2D6 <= 12 < 13 → battle-shock всегда провален
    env.unit_health[0] = 1.0
    env.modelCP = 2


def test_decide_bravery_equivalent_to_action():
    """strat_command=insane_bravery и decide_bravery(i==0) дают одинаковый результат."""
    n_env = build_env()
    _setup_failing_unit0(n_env)
    n = len(n_env.unit_health)
    snap = n_env.snapshot_state()

    with n_env.simulation_mode():
        bs_a, r_a = n_env.command_phase("model", action=_action_bravery(n, unit=0))
        cp_a, used_a = n_env.modelCP, list(n_env.stratagem_used)
    n_env.restore_state(snap)

    with n_env.simulation_mode():
        bs_b, r_b = n_env.command_phase("model", action=_action_no_bravery(n), decide_bravery=lambda i: i == 0)
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


def _pick_bravery_for(unit_idx):
    def decide(window):
        for o in window.options:
            if o.kind is ActionKind.USE_STRATAGEM and o.unit_idx == unit_idx:
                return o
        return window.options[0]  # PASS

    return decide


def _pick_pass(window):
    return window.options[0]


def test_run_command_applies_bravery():
    env = build_env()
    _setup_failing_unit0(env)
    snap = env.snapshot_state()
    with env.simulation_mode():
        state = phase_engine.run_command(env, "model", _pick_bravery_for(0))
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert state.battle_shock[0] is False
    assert ("model", "insane_bravery", env.battle_round, "command", 0) in used


def test_run_command_declines_bravery():
    env = build_env()
    _setup_failing_unit0(env)
    snap = env.snapshot_state()
    with env.simulation_mode():
        state = phase_engine.run_command(env, "model", _pick_pass)
        used = list(env.stratagem_used)
    env.restore_state(snap)
    assert state.battle_shock[0] is True
    assert used == []
