import numpy as np

import core.envs.warhamEnv as warham_mod
from core.engine.phases import stratagem_engine
from core.engine.phases.stratagems import by_id
from core.engine.phases.types import Phase
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


def test_command_reroll_registry_includes_shooting_phase():
    assert Phase.SHOOTING in by_id("command_reroll").phases


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
