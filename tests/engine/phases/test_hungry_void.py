import core.envs.warhamEnv as warham_mod
from core.engine.phases import stratagem_engine
from core.engine.phases.option_generator import fight_stratagem_options_for_unit
from core.engine.phases.types import ActionKind
from tests.engine.phases._helpers import build_env


def _setup_engagement(env):
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)


def test_hungry_void_fight_option_apply_effect_and_snapshot_restore():
    env = build_env()
    env.modelCP = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []

    opts = fight_stratagem_options_for_unit(env, "model", 0)
    hungry = [o for o in opts if o.kind is ActionKind.USE_STRATAGEM and o.meta["stratagem_id"] == "hungry_void"]
    assert len(hungry) == 1
    assert hungry[0].legacy_patch == {}
    assert hungry[0].unit_idx == 0

    res = stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")

    expected_used = ("model", "hungry_void", env.battle_round, "fight", 0)
    expected_effect = {
        "side": "model",
        "unit_idx": 0,
        "round": env.battle_round,
        "phase": "fight",
        "effect_id": "hungry_void_strength_mod",
        "strength_mod": 1,
    }
    assert res == {"ok": True, "cp_spent": 1, "reason": None}
    assert env.modelCP == 0
    assert env.stratagem_used == [expected_used]
    assert env.active_stratagem_effects == [expected_effect]

    snap = env.snapshot_state()
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.modelCP = 99

    env.restore_state(snap)

    assert env.stratagem_used == [expected_used]
    assert env.active_stratagem_effects == [expected_effect]
    assert env.modelCP == 0


def test_hungry_void_changes_fight_damage_only_when_selected(monkeypatch):
    calls = []

    def fake_attack(attacker_health, weapon, attacker_data, defender_health, defender_data, *args, **kwargs):
        effects = kwargs.get("effects")
        damage = 1.0 if isinstance(effects, dict) and effects.get("strength_mod") == 1 else 0.0
        calls.append({"attacker": attacker_data.get("Name"), "effects": effects, "damage": damage})
        return [damage], defender_health - damage

    monkeypatch.setattr(warham_mod, "attack", fake_attack)

    env = build_env()
    _setup_engagement(env)
    start_enemy_hp = env.enemy_health[0]

    with env.simulation_mode():
        env.resolve_fight_phase("model", trunc=True)

    model_call = next(c for c in calls if c["attacker"] == "ModelA")
    assert model_call["effects"] is None
    assert env.enemy_health[0] == start_enemy_hp
    assert env.active_stratagem_effects == []

    calls.clear()
    _setup_engagement(env)
    env.modelCP = 1
    stratagem_engine.apply(env, "model", "hungry_void", 0, phase="fight")
    start_enemy_hp = env.enemy_health[0]

    with env.simulation_mode():
        env.resolve_fight_phase("model", trunc=True)

    model_call = next(c for c in calls if c["attacker"] == "ModelA")
    enemy_call = next(c for c in calls if c["attacker"] == "EnemyA")
    assert model_call["effects"] == {"strength_mod": 1}
    assert enemy_call["effects"] is None
    assert env.enemy_health[0] == start_enemy_hp - 1.0
    assert env.active_stratagem_effects == []
