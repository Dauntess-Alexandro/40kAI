from core.engine.phases.types import Phase
from tests.engine.phases._helpers import build_env


def _setup(env, cp=2):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = cp
    env.enemyCP = cp
    env.stratagem_used = []
    env.active_stratagem_effects = []


def test_choice_none_always_legal():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "none") is True


def test_command_reroll_needs_cp():
    env = build_env()
    _setup(env, cp=0)
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is False
    env.modelCP = 1
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:hit") is True
    # подтип не влияет на легальность
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "command_reroll:wound") is True


def test_hungry_void_requires_necrons_keyword():
    env = build_env()
    _setup(env, cp=2)
    # по умолчанию у юнитов нет necrons-keyword (build_env) → hungry_void нелегален
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._invalidate_target_cache("kw")
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is True


def test_usage_limit_blocks_choice():
    env = build_env()
    _setup(env, cp=3)
    env.battle_round = 1
    env.unit_data[0]["Keywords"] = ["Necrons"]
    # hungry_void PER_PHASE: запись в journal → нелегален в той же (round, phase)
    env.stratagem_used = [("model", "hungry_void", 1, "fight", 0)]
    env.phase = "fight"
    assert env._stratagem_choice_legal("model", Phase.FIGHT, "hungry_void") is False


def test_strat_phase_mask_cp_gating():
    env = build_env()
    _setup(env, cp=0)
    masks = env.get_legal_action_masks_by_head("model")
    fm = masks["strat_fight"]
    assert bool(fm[0]) is True  # none всегда
    assert not bool(fm[1:].any())  # CP=0 → только none
    env2 = build_env()
    _setup(env2, cp=2)
    fm2 = env2.get_legal_action_masks_by_head("model")["strat_fight"]
    # command_reroll:hit/wound легальны при CP (hungry_void без necrons — нет)
    from core.engine.phases.stratagems import stratagem_action_choices
    choices = stratagem_action_choices(__import__("core.engine.phases.types", fromlist=["Phase"]).Phase.FIGHT)
    assert bool(fm2[choices.index("command_reroll:hit")]) is True
    assert bool(fm2[choices.index("command_reroll:wound")]) is True


def test_strat_movement_mask_advance_reroll_illegal():
    """Подзадача 3.3A: command_reroll:advance — нелегальная опция в movement-маске при CP.

    action-контракт не меняется (подтип остаётся в choices), но mask должна быть False,
    чтобы policy/MCTS не выбирали advance reroll как legal option.
    """
    env = build_env()
    _setup(env, cp=2)
    masks = env.get_legal_action_masks_by_head("model")
    fm = masks["strat_movement"]
    from core.engine.phases.stratagems import stratagem_action_choices
    choices = stratagem_action_choices(Phase.MOVEMENT)
    assert bool(fm[0]) is True  # none всегда
    assert bool(fm[choices.index("command_reroll:advance")]) is False  # advance нелегален


def test_strat_unit_mask_alive_only():
    env = build_env()
    _setup(env, cp=2)
    env.unit_health[1] = 0.0
    masks = env.get_legal_action_masks_by_head("model")
    um = masks["strat_fight_unit"]
    assert bool(um[0]) is True
    assert bool(um[1]) is False  # мёртв


def test_strat_mask_sizes_match_space():
    env = build_env()
    _setup(env, cp=2)
    from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices
    masks = env.get_legal_action_masks_by_head("model")
    spaces = env.action_space.spaces
    for ph in STRATAGEM_PHASES:
        assert len(masks[f"strat_{ph.value}"]) == len(stratagem_action_choices(ph))
        assert len(masks[f"strat_{ph.value}_unit"]) == int(spaces[f"strat_{ph.value}_unit"].n)


def test_build_action_masks_delegates_strat():
    from core.models.utils import build_action_masks_by_head
    env = build_env()
    _setup(env, cp=0)
    ordered = build_action_masks_by_head(env, 2, side="model")
    # порядок ordered_action_keys: strat_fight маска присутствует и [0] разрешён
    from core.models.action_contract import ordered_action_keys
    keys = ordered_action_keys(2)
    idx = keys.index("strat_fight")
    assert bool(ordered[idx][0]) is True
