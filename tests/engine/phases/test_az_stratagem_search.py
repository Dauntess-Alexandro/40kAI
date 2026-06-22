
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


# ---------------------------------------------------------------------------
# Task 3: anti-double (голова strat_fight + pending fight plan)
# ---------------------------------------------------------------------------


def test_head_and_fight_plan_no_double_apply():
    """Голова strat_fight и старый fight-план оба просят command_reroll на юните 0.

    fight_phase применяет голову ПЕРЕД pending plan → plan видит запись в
    stratagem_used/active_stratagem_effects и пропускает (MC-гейт
    _value_pick_command_reroll → _command_reroll_record_exists → None).
    Итого: ровно одно списание CP, не два.
    """
    env = build_env()
    _setup(env)
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    # и голова, и старый fight-план просят command_reroll на юните 0
    action = {
        "strat_fight": stratagem_choice_index(Phase.FIGHT, "command_reroll:hit"),
        "strat_fight_unit": 0,
    }
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    cp_before = env.modelCP
    with env.simulation_mode():
        env.fight_phase("model", action=action)
    # ровно одно списание CP (нет двойного применения)
    assert cp_before - env.modelCP <= 1


# ---------------------------------------------------------------------------
# Task 3: policy-таргет strat_fight головы не вырожден
# ---------------------------------------------------------------------------


def test_final_policy_from_visits_nondegenerate_for_strat_head():
    """Проверяем, что _final_policy_from_visits раскладывает визиты по strat_fight-голове.

    Строим минимальное дерево: корень с двумя детьми, у которых action_tuple
    различается в позиции strat_fight (индекс 0 vs != 0). При наличии визитов
    на обоих — policy target для strat_fight головы НЕ должен быть вырожден
    (вся масса на индексе 0 = «none»).
    """
    import numpy as np

    from core.models.action_contract import ordered_action_keys
    from core.models.alphazero_mcts import AlphaZeroFactorizedMCTS, MCTSConfig, MCTSNode

    n_units = 2
    keys = ordered_action_keys(n_units)
    num_heads = len(keys)
    strat_fight_idx = keys.index("strat_fight")

    # Размеры голов: для простоты — 4 для всех (реальные значения неважны,
    # главное strat_fight_size >= 2 чтобы было куда класть «не none»).
    head_sizes = [4] * num_heads

    # Uniform priors — все действия равновероятны.
    priors = [np.ones(s, dtype=np.float32) / s for s in head_sizes]
    # Все действия легальны.
    legal_masks = [np.ones(s, dtype=bool) for s in head_sizes]

    # Корень: два ребёнка с разным strat_fight.
    root = MCTSNode()
    root.visit_count = 20

    # Child A: strat_fight=0 (none), 10 визитов.
    tuple_a = tuple(0 for _ in range(num_heads))
    child_a = MCTSNode(parent=root, action_tuple=tuple_a, visit_count=10, value_sum=5.0)
    root.children[tuple_a] = child_a

    # Child B: strat_fight=1 (command_reroll:hit), 10 визитов.
    tuple_b_list = [0] * num_heads
    tuple_b_list[strat_fight_idx] = 1
    tuple_b = tuple(tuple_b_list)
    child_b = MCTSNode(parent=root, action_tuple=tuple_b, visit_count=10, value_sum=5.0)
    root.children[tuple_b] = child_b

    # Минимальная конфигурация MCTS (mock net — не вызывается).
    cfg = MCTSConfig(temperature_opening_moves=0, prior_weight_early=0.0)
    mcts = AlphaZeroFactorizedMCTS(policy_value_net=None, config=cfg)

    policy_targets, _ = mcts._final_policy_from_visits(
        root, priors, legal_masks, temperature=1.0, move_count=100,
    )

    pi_strat_fight = policy_targets[strat_fight_idx]
    # Масса на index 0 (none) < 1.0 → не вырожден.
    assert pi_strat_fight[0] < 1.0, (
        f"policy target для strat_fight вырожден: вся масса на none (idx=0). "
        f"pi={pi_strat_fight}"
    )
    # Масса на index 1 > 0 — визиты от child_b учтены.
    assert pi_strat_fight[1] > 0.0, (
        f"policy target для strat_fight[1] == 0, визиты child_b не учтены. "
        f"pi={pi_strat_fight}"
    )
