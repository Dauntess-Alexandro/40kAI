import numpy as np

from core.engine.phases import compile_options_to_action_dict, default_action_dict
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind
from core.models.action_contract import ordered_action_keys
from core.models.option_candidates import (
    action_dict_from_joint_tuple,
    attach_fight_stratagem_plan,
    build_turn_plan_candidates,
    filter_joint_candidates,
    joint_action_candidates,
    joint_tuple_from_action_dict,
    resolve_candidate_mode,
    root_joint_candidates,
    score_joint_prior,
)
from tests.engine.phases._helpers import build_env


def test_resolve_candidate_mode_defaults_option(monkeypatch):
    monkeypatch.delenv("MCTS_CANDIDATE_MODE", raising=False)
    assert resolve_candidate_mode(None) == "option"
    assert resolve_candidate_mode("filter") == "filter"
    assert resolve_candidate_mode("bogus") == "option"


def test_joint_tuple_roundtrip():
    n = 2
    d = default_action_dict(n)
    d["shoot_num_0"] = 1
    d["move_num_1"] = 3
    jt = joint_tuple_from_action_dict(d, n)
    d2 = action_dict_from_joint_tuple(jt, n)
    assert d2 == d


def test_joint_action_candidates_nonempty():
    priors = [np.array([0.1, 0.2, 0.7], dtype=np.float32), np.array([0.4, 0.6], dtype=np.float32)]
    legal = [np.array([True, True, True]), np.array([True, True])]
    out = joint_action_candidates(priors, legal, top_k_per_head=2, max_candidates=8)
    assert out
    assert out[0] == (2, 1)


def test_build_turn_plan_candidates_bounded_and_has_greedy():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env._invalidate_target_cache("test")
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal = [np.ones(p.size, dtype=bool) for p in priors]

    plans = build_turn_plan_candidates(env, n, priors, legal, max_candidates=32)
    assert 1 <= len(plans) <= 32
    assert all(p.projected_prior > 0 for p in plans)
    assert plans[0].joint_tuple  # не пустой


def test_filter_joint_subset_of_joint():
    env = build_env()
    env.modelCP = 1
    env._invalidate_target_cache("test")
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal = [np.ones(p.size, dtype=bool) for p in priors]
    joint = joint_action_candidates(priors, legal, top_k_per_head=6, max_candidates=24)
    filtered = filter_joint_candidates(joint, env, n, priors, legal)
    assert filtered
    assert set(filtered).issubset(set(joint))


def test_greedy_joint_matches_compiled_plan_when_legal():
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal_masks = [np.ones(p.size, dtype=bool) for p in priors]

    plans = build_turn_plan_candidates(env, n, priors, legal_masks, max_candidates=64)
    best_plan = plans[0]
    score_plan = score_joint_prior(priors, legal_masks, best_plan.joint_tuple)

    joint = joint_action_candidates(priors, legal_masks, top_k_per_head=8, max_candidates=64)
    greedy_joint = joint[0]
    score_joint = score_joint_prior(priors, legal_masks, greedy_joint)

    # При uniform prior скоры положительны и согласованы с размерностью.
    assert score_plan > 0
    assert score_joint > 0


def test_movement_plan_simulates_without_error():
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")
    opts = movement_options_for_unit(env, "model", 0)
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    action = compile_options_to_action_dict([chosen], len(env.unit_health))
    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))
        finally:
            env.restore_state(snap)


def test_root_joint_mode_joint_unchanged():
    env = build_env()
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal = [np.ones(p.size, dtype=bool) for p in priors]
    a = joint_action_candidates(priors, legal, 8, 64)
    b = root_joint_candidates(
        mode="joint",
        priors=priors,
        legal_masks=legal,
        env=env,
        len_model=n,
        top_k_per_head=8,
        max_candidates=64,
    )
    assert a == list(b)


def test_turn_plan_can_carry_fight_stratagem_plan():
    env = build_env()
    env.modelCP = 2
    env._invalidate_target_cache("test")
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal = [np.ones(p.size, dtype=bool) for p in priors]

    plans = build_turn_plan_candidates(env, n, priors, legal, max_candidates=64, perturb_top_m=8)
    with_fight = [p for p in plans if p.fight_stratagem_plan]
    assert with_fight, "должен быть план с fight-стратагемой при CP>=1"

    root = root_joint_candidates(
        mode="option",
        priors=priors,
        legal_masks=legal,
        env=env,
        len_model=n,
        max_candidates=32,
    )
    sample = with_fight[0].joint_tuple
    assert root.fight_plan_for(sample) == dict(with_fight[0].fight_stratagem_plan)


def test_attach_fight_stratagem_plan_sets_pending():
    env = build_env()
    attach_fight_stratagem_plan(env, {0: "hungry_void"})
    assert env._pending_fight_stratagem_plan == {0: "hungry_void"}
    attach_fight_stratagem_plan(env, None)
    assert env._pending_fight_stratagem_plan is None


def test_root_option_plus_contains_legacy_greedy():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")
    n = len(env.unit_health)
    keys = ordered_action_keys(n)
    priors = [np.ones(env.action_space.spaces[k].n, dtype=np.float32) for k in keys]
    legal = [np.ones(p.size, dtype=bool) for p in priors]
    joint = joint_action_candidates(priors, legal, 6, 32)
    tuples = root_joint_candidates(
        mode="option_plus",
        priors=priors,
        legal_masks=legal,
        env=env,
        len_model=n,
        top_k_per_head=6,
        max_candidates=32,
    )
    assert joint[0] in list(tuples)


def test_fight_stratagem_plan_command_reroll_colon_form():
    """command_reroll должен кодироваться в colon-форме (command_reroll:hit),
    чтобы AZ/MCTS-путь без reaction_policy мог применить реролл напрямую."""
    from core.engine.phases.types import (
        ActionKind,
        ActionOption,
        DecisionWindow,
        Phase,
        SubStep,
        Timing,
    )
    from core.models.option_candidates import _fight_stratagem_plan_from_choices

    # Окно с command_reroll:hit (выбор дерева)
    opt_cr = ActionOption(
        kind=ActionKind.USE_STRATAGEM,
        unit_idx=0,
        meta={"stratagem_id": "command_reroll", "reroll_roll": "hit"},
        param={"stratagem_id": "command_reroll", "reroll_roll": "hit"},
    )
    win_cr = DecisionWindow(
        window_id="fight:model:cr",
        owner_side="model",
        phase=Phase.FIGHT,
        sub_step=SubStep.FIGHT_UNIT,
        timing=Timing.MAIN,
        cursor_unit_idx=0,
        options=[opt_cr],
    )

    # Окно с обычной стратагемой (не command_reroll) — должна оставаться без двоеточия
    opt_hv = ActionOption(
        kind=ActionKind.USE_STRATAGEM,
        unit_idx=1,
        meta={"stratagem_id": "hungry_void"},
        param={"stratagem_id": "hungry_void"},
    )
    win_hv = DecisionWindow(
        window_id="fight:model:hv",
        owner_side="model",
        phase=Phase.FIGHT,
        sub_step=SubStep.FIGHT_UNIT,
        timing=Timing.MAIN,
        cursor_unit_idx=1,
        options=[opt_hv],
    )

    plan = _fight_stratagem_plan_from_choices(
        [win_cr, win_hv],
        {win_cr.window_id: 0, win_hv.window_id: 0},
    )

    # command_reroll должен быть в colon-форме с подтипом
    assert (0, "command_reroll:hit") in plan, f"ожидали command_reroll:hit, получили: {plan}"
    # hungry_void — без двоеточия
    assert (1, "hungry_void") in plan, f"ожидали hungry_void, получили: {plan}"
