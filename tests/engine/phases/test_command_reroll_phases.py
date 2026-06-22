import numpy as np

import core.envs.warhamEnv as warham_mod
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases import stratagem_engine
from core.engine.phases.stratagems import by_id
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env, flat_default_action


def _shooting_setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.modelCP = 2
    env.enemyCP = 2
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_phases_test")


def _shoot_action(env):
    return flat_default_action(len(env.unit_health), shoot_num_0=0)


def _movement_setup(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [2, 2]
    env.unit_health[1] = 0.0
    env.enemy_health[1] = 0.0
    env.modelCP = 2
    env.enemyCP = 0
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env._invalidate_target_cache("command_reroll_movement_test")


def _advance_option_with_non_max_roll(env):
    opts = movement_options_for_unit(env, "model", 0)
    base_m = int(env.unit_data[0]["Movement"])
    row, col = [int(v) for v in env.unit_coords[0]]
    fallback = None
    for opt in opts:
        if opt.kind is not ActionKind.ADVANCE:
            continue
        dest_x, dest_y = opt.param["dest"]
        distance = env._grid_distance_chebyshev((row, col), (int(dest_y), int(dest_x)))
        advance_roll = max(1, min(6, int(distance) - base_m))
        fallback = fallback or opt
        if advance_roll != 6:
            return opt
    if fallback is None:
        raise AssertionError("no advance option for movement command reroll test")
    return fallback


def test_command_reroll_registry_includes_shooting_phase():
    assert Phase.SHOOTING in by_id("command_reroll").phases


def test_command_reroll_registry_includes_movement_phase_for_advance():
    assert Phase.MOVEMENT in by_id("command_reroll").phases


def test_movement_command_reroll_advance_updates_final_roll(monkeypatch):
    calls = []

    def fake_dice(*, min=1, max=6, num=1):
        calls.append((min, max, num))
        return 6

    monkeypatch.setattr(warham_mod, "dice", fake_dice)
    env = build_env()
    _movement_setup(env)
    chosen = _advance_option_with_non_max_roll(env)
    action = flat_default_action(len(env.unit_health), **chosen.legacy_patch)
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="movement", reroll_roll="advance")

    with env.simulation_mode():
        env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))

    assert calls == [(1, 6, 1)]
    assert env.model_advance_roll[0] == 6


def test_shooting_command_reroll_wound_reaches_attack_effect(monkeypatch):
    calls = []

    def fake_attack(attacker_health, weapon, attacker_data, defender_health, defender_data, *args, **kwargs):
        effects = kwargs.get("effects")
        calls.append(effects)
        damage = 2.0 if isinstance(effects, dict) and effects.get("reroll_wounds") == "one" else 0.0
        return [damage], defender_health - damage

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _shooting_setup(env)
    start_hp = float(env.enemy_health[0])
    stratagem_engine.apply(env, "model", "command_reroll", 0, phase="shooting", reroll_roll="wound")

    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=_shoot_action(env))

    assert calls and calls[0] == {"reroll_wounds": "one"}
    assert float(env.enemy_health[0]) == start_hp - 2.0


def test_shooting_command_reroll_save_belongs_to_defender(monkeypatch):
    calls = []

    def fake_attack(attacker_health, weapon, attacker_data, defender_health, defender_data, *args, **kwargs):
        decider = kwargs.get("reroll_decider")
        calls.append(
            {
                "hit": bool(decider("hit", np.array([2]), 4)),
                "save": bool(decider("save", np.array([2]), 4)),
            }
        )
        return [0.0], defender_health

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    _shooting_setup(env)
    stratagem_engine.apply(env, "enemy", "command_reroll", 0, phase="shooting", reroll_roll="save")

    with env.simulation_mode():
        env.shooting_phase("model", advanced_flags=[False] * len(env.unit_health), action=_shoot_action(env))

    assert calls == [{"hit": False, "save": True}]
