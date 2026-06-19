"""Task A7: Hungry Void — keyword NECRONS + AP+1 при Character-лидере."""

from tests.engine.phases._helpers import build_env


def test_hungry_void_keyword_gate():
    from core.engine.phases.stratagems import by_id
    assert by_id("hungry_void").keyword_req == ("necrons",)


def test_hungry_void_ap_only_for_character():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.battle_round = 1
    env.phase = "fight"
    env.active_stratagem_effects = [{
        "side": "model", "unit_idx": 0, "round": 1, "phase": "fight",
        "effect_id": "hungry_void_strength_mod", "strength_mod": 1,
    }]
    # без character — только +S
    env.unit_data[0]["Keywords"] = ["Necrons", "Infantry"]
    eff_plain = env._fight_effects_for_attacker("model", 0)
    assert eff_plain.get("strength_mod") == 1
    assert int(eff_plain.get("ap_improve", 0)) == 0
    # с character — +S и +1 AP
    env.unit_data[0]["Keywords"] = ["Necrons", "Character"]
    eff_char = env._fight_effects_for_attacker("model", 0)
    assert int(eff_char.get("ap_improve", 0)) == 1
