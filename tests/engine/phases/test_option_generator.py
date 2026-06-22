import numpy as np

from core.engine.phases.option_generator import (
    charge_options_for_unit,
    command_window,
    generate_windows,
    movement_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.stratagems import stratagem_choice_index
from core.engine.phases.types import ActionKind, Phase
from tests.engine.phases._helpers import build_env


def test_shooting_options_match_env_targets():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env._invalidate_target_cache("test")

    valid = env.get_shoot_targets_for_unit("model", 0)
    opts = shooting_options_for_unit(env, "model", 0)

    shoot_opts = [o for o in opts if o.kind is ActionKind.SHOOT]
    assert [o.target_idx for o in shoot_opts] == list(valid)
    # local_rank — индекс в списке целей; legacy_patch кодирует shoot_num_{unit}=rank
    for rank, o in enumerate(shoot_opts):
        assert o.param["local_rank"] == rank
        assert o.legacy_patch == {"shoot_num_0": rank}
    assert any(o.kind is ActionKind.PASS for o in opts)


def test_charge_options_match_env_targets():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")

    valid = env.get_charge_targets_for_unit("model", 0)
    opts = charge_options_for_unit(env, "model", 0)

    charge_opts = [o for o in opts if o.kind is ActionKind.CHARGE]
    assert [o.target_idx for o in charge_opts] == list(valid)
    for o in charge_opts:
        assert o.legacy_patch == {"charge_num_0": int(o.target_idx), "attack": 1}
    assert any(o.kind is ActionKind.PASS for o in opts)


def test_shoot_targets_union_matches_per_unit_shoot_masks():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [10, 11]
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env._invalidate_target_cache("test")

    masks = env.get_legal_action_masks_by_head("model")

    for u in range(len(env.unit_health)):
        mask = masks[f"shoot_num_{u}"]
        mask_ranks = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}
        gen_ranks: set[int] = set()
        for o in shooting_options_for_unit(env, "model", u):
            if o.kind is ActionKind.SHOOT:
                gen_ranks.add(int(o.legacy_patch[f"shoot_num_{u}"]))
        if gen_ranks:
            assert gen_ranks == mask_ranks


def test_charge_targets_union_matches_per_unit_charge_masks():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")

    masks = env.get_legal_action_masks_by_head("model")

    for u in range(len(env.unit_health)):
        mask = masks[f"charge_num_{u}"]
        mask_ids = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}
        gen_ids: set[int] = set()
        for o in charge_options_for_unit(env, "model", u):
            if o.target_idx is not None:
                gen_ids.add(int(o.target_idx))
        if gen_ids:
            assert gen_ids == mask_ids


def test_movement_options_index_parity_with_executor():
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    opts = movement_options_for_unit(env, "model", 0)
    assert opts and opts[0].kind is ActionKind.STAY
    assert opts[0].param["reachable_index"] == 0

    base_m = int(env.unit_data[0]["Movement"])
    # Для каждой сгенерированной опции dest совпадает с тем, что вернёт исполнитель по тому же индексу.
    total = None
    for o in opts:
        k = o.param["reachable_index"]
        dest, _mode, _dist, chosen_idx, total = env._pick_destination_by_reachable_index(
            "model", 0, choice=k, base_m=base_m, unit_label="[TEST]"
        )
        assert dest is not None
        assert chosen_idx == k
        assert o.param["dest"] == (int(dest[0]), int(dest[1]))
        expected_patch = {"move_num_0": k}
        if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE):
            assert o.legacy_patch.get("move") in {0, 1, 2, 3}
            expected_patch["move"] = o.legacy_patch["move"]
        else:
            assert "move" not in o.legacy_patch
        assert o.legacy_patch == expected_patch
    # Генератор покрывает ровно весь исполнительный диапазон reachable.
    assert len(opts) == total


def test_move_num_mask_covers_representable_reachable_indices():
    """The legal mask must cover every executor-reachable movement option it can represent."""
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["move_num_0"]
    mask_true = int(np.sum(np.asarray(mask, dtype=bool)))
    opts = movement_options_for_unit(env, "model", 0)
    assert mask_true == min(len(mask), len(opts))


def test_model_charge_targets_respect_model_used_advance():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env.unit_health[1] = 0.0
    env.model_used_advance = [True, False]
    env._invalidate_target_cache("test")

    assert env.get_charge_targets_for_unit("model", 0) == []


def test_command_window_offers_bravery_only_with_cp():
    env = build_env()
    env.modelCP = 0
    win0 = command_window(env, "model")
    assert all(o.kind is not ActionKind.USE_STRATAGEM for o in win0.options)

    env.modelCP = 2
    win = command_window(env, "model")
    bravery = [o for o in win.options if o.kind is ActionKind.USE_STRATAGEM]
    alive = [i for i, hp in enumerate(env.unit_health) if hp > 0]
    assert [o.unit_idx for o in bravery] == alive
    for o in bravery:
        assert o.meta["stratagem_id"] == "insane_bravery"
        assert o.legacy_patch == {
            "use_cp": 1,
            "cp_on": int(o.unit_idx),
            "strat_command": stratagem_choice_index(Phase.COMMAND, "insane_bravery"),
            "strat_command_unit": int(o.unit_idx),
        }


def test_generate_windows_orders_phases():
    env = build_env()
    env.modelCP = 1
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env._invalidate_target_cache("test")

    windows = generate_windows(env, "model")
    phases_seen = [w.phase for w in windows]
    assert phases_seen[0] is Phase.COMMAND
    assert Phase.MOVEMENT in phases_seen
    assert Phase.SHOOTING in phases_seen
    assert Phase.CHARGE in phases_seen
    assert Phase.FIGHT in phases_seen
    order = {Phase.COMMAND: 0, Phase.MOVEMENT: 1, Phase.SHOOTING: 2, Phase.CHARGE: 3, Phase.FIGHT: 4}
    idxs = [order[p] for p in phases_seen]
    assert idxs == sorted(idxs)
    ids = [w.window_id for w in windows]
    assert len(ids) == len(set(ids))
    fight_ids = [w.window_id for w in windows if w.phase is Phase.FIGHT]
    assert fight_ids == [f"fight:model:{u}" for u in range(len(env.unit_health)) if env.unit_health[u] > 0]
