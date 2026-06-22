from core.engine.phases.legacy_compiler import compile_options_to_action_dict, default_action_dict
from core.engine.phases.option_generator import (
    command_reroll_options_for_unit,
    fight_stratagem_options_for_unit,
    generate_windows,
)
from core.engine.phases.stratagems import stratagem_choice_index
from core.engine.phases.types import ActionKind, Phase
from core.models.option_candidates import joint_tuple_from_action_dict
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []


def test_fight_command_reroll_option_carries_strat_patch():
    env = build_env()
    _setup(env)
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    cr = [o for o in opts if o.meta.get("stratagem_id") == "command_reroll" and o.meta.get("reroll_roll") == "hit"][0]
    assert cr.legacy_patch["strat_fight"] == stratagem_choice_index(Phase.FIGHT, "command_reroll:hit")
    assert cr.legacy_patch["strat_fight_unit"] == 0


def test_fight_hungry_void_option_carries_strat_patch():
    env = build_env()
    _setup(env)
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    hv = [o for o in opts if o.meta.get("stratagem_id") == "hungry_void"][0]
    assert hv.legacy_patch["strat_fight"] == stratagem_choice_index(Phase.FIGHT, "hungry_void")
    assert hv.legacy_patch["strat_fight_unit"] == 0


def test_command_reroll_options_for_unit_carries_strat_patch():
    env = build_env()
    _setup(env)
    opts = command_reroll_options_for_unit(env, "model", 0, phase=Phase.SHOOTING, rolls=("hit", "wound"))
    o = [x for x in opts if x.meta.get("reroll_roll") == "wound"][0]
    assert o.legacy_patch["strat_shooting"] == stratagem_choice_index(Phase.SHOOTING, "command_reroll:wound")
    assert o.legacy_patch["strat_shooting_unit"] == 0


def test_compile_and_joint_differs_with_strat():
    env = build_env()
    _setup(env)
    opts = fight_stratagem_options_for_unit(env, "model", 0)
    cr = [o for o in opts if o.param.get("reroll_roll") == "hit"][0]
    n = len(env.unit_health)
    ad = compile_options_to_action_dict([cr], n)
    assert ad["strat_fight"] != 0
    jt_with = joint_tuple_from_action_dict(ad, n)
    jt_none = joint_tuple_from_action_dict(default_action_dict(n), n)
    assert jt_with != jt_none  # кандидаты с/без реролла НЕ схлопываются


def _strat_opts_for_phase(windows, phase):
    out = []
    for w in windows:
        if w.phase is phase:
            out += [o for o in w.options if o.kind is ActionKind.USE_STRATAGEM and o.meta.get("stratagem_id") == "command_reroll"]
    return out


def test_generate_windows_has_shooting_charge_stratagem_options():
    env = build_env()
    _setup(env)
    windows = generate_windows(env, "model")
    assert _strat_opts_for_phase(windows, Phase.SHOOTING), "нет command_reroll-опций в shooting-окнах"
    assert _strat_opts_for_phase(windows, Phase.CHARGE), "нет command_reroll-опций в charge-окнах"
    # и они несут strat legacy_patch
    sh = _strat_opts_for_phase(windows, Phase.SHOOTING)[0]
    assert "strat_shooting" in sh.legacy_patch
