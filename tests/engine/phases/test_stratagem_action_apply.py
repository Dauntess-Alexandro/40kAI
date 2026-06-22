from core.engine.phases.stratagems import stratagem_action_choices
from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env, flat_default_action


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.battle_round = 1
    env.phase = "fight"
    # unitCharged/enemyCharged сайзятся в step()/enemyTurn(); при прямом вызове фаз — инициализируем сами
    # (как во всех fight/charge-тестах), иначе resolve_fight_phase падает на IndexError.
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)


def _idx(phase, choice):
    return stratagem_action_choices(phase).index(choice)


# ---------------------------------------------------------------------------
# Task 1: _apply_action_stratagem
# ---------------------------------------------------------------------------


def test_apply_action_stratagem_command_reroll_fight():
    env = build_env()
    _setup(env)
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert any(
        r.get("effect_id") == "command_reroll" and r.get("reroll_roll") == "hit" and int(r.get("unit_idx", -1)) == 0
        for r in env.active_stratagem_effects
    )
    assert ("model", "command_reroll", 1, "fight", 0) in env.stratagem_used


def test_apply_action_stratagem_none_idx0_noop():
    env = build_env()
    _setup(env)
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": 0, "strat_fight_unit": 0})
    assert env.active_stratagem_effects == []
    assert env.modelCP == 2


def test_apply_action_stratagem_illegal_no_cp():
    env = build_env()
    _setup(env, cp=0)
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.active_stratagem_effects == []


def test_apply_action_stratagem_dead_unit_noop():
    env = build_env()
    _setup(env)
    env.unit_health[1] = 0.0
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 1}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.active_stratagem_effects == []


def test_apply_action_stratagem_hungry_void_needs_necrons():
    env = build_env()
    _setup(env)
    hv = _idx(Phase.FIGHT, "hungry_void")
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": hv, "strat_fight_unit": 0})
    assert not any(r[1] == "hungry_void" for r in env.stratagem_used)  # нет necrons keyword
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    env._apply_action_stratagem("model", Phase.FIGHT, {"strat_fight": hv, "strat_fight_unit": 0})
    assert any(r[1] == "hungry_void" for r in env.stratagem_used)


def test_apply_action_stratagem_anti_double():
    env = build_env()
    _setup(env)
    # имитируем, что MC-хук уже применил command_reroll на юните 0 в fight
    env.stratagem_used = [("model", "command_reroll", 1, "fight", 0)]
    cp_before = env.modelCP
    action = {"strat_fight": _idx(Phase.FIGHT, "command_reroll:hit"), "strat_fight_unit": 0}
    env._apply_action_stratagem("model", Phase.FIGHT, action)
    assert env.modelCP == cp_before  # не списан повторно


# ---------------------------------------------------------------------------
# Task 2: вызовы _apply_action_stratagem в фазах (+ action в fight_phase)
# ---------------------------------------------------------------------------


def test_movement_phase_applies_strat_head_advance():
    env = build_env()
    _setup(env)
    env.phase = "movement"
    action = flat_default_action(len(env.unit_health))
    action["strat_movement"] = _idx(Phase.MOVEMENT, "command_reroll:advance")
    action["strat_movement_unit"] = 0
    with env.simulation_mode():
        env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))
    assert any(r[1] == "command_reroll" and r[3] == "movement" for r in env.stratagem_used)


def test_fight_phase_action_param_applies_strat_head():
    env = build_env()
    _setup(env)
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    action = flat_default_action(len(env.unit_health))
    action["strat_fight"] = _idx(Phase.FIGHT, "command_reroll:wound")
    action["strat_fight_unit"] = 0
    with env.simulation_mode():
        env.fight_phase("model", action=action)
    assert any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)


def test_fight_phase_no_action_is_parity():
    env = build_env()
    _setup(env)
    with env.simulation_mode():
        env.fight_phase("model")  # без action — старый путь, не падает
    assert not any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)


# ---------------------------------------------------------------------------
# Task 3: Insane Bravery через strat_command
# ---------------------------------------------------------------------------


def test_command_strat_head_triggers_bravery():
    env = build_env()
    _setup(env)
    env.phase = "command"
    # Детерминируем провал battle-shock у юнита 0: health ниже половины состава +
    # Ld=13 (2D6<=12 < 13 → всегда провал). Отдельного метода-проверки нет —
    # провал определяется инлайн-броском в command_phase (как в test_command_bravery_via_engine).
    env.unit_health[0] = 1.0
    env.unit_data[0]["Ld"] = 13
    # use_cp=0/cp_on=-1 → старый путь точно не сработает; проверяем только strat_command.
    action = flat_default_action(len(env.unit_health), use_cp=0, cp_on=-1)
    action["strat_command"] = _idx(Phase.COMMAND, "insane_bravery")
    action["strat_command_unit"] = 0
    with env.simulation_mode():
        env.command_phase("model", action=action)
    assert any(r[1] == "insane_bravery" for r in env.stratagem_used)
