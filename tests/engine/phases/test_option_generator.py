import numpy as np

from core.engine.phases.option_generator import (
    charge_options_for_unit,
    movement_options_for_unit,
    shooting_options_for_unit,
)
from core.engine.phases.types import ActionKind
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
    # local_rank — индекс в списке целей; legacy_patch кодирует shoot=rank
    for rank, o in enumerate(shoot_opts):
        assert o.param["local_rank"] == rank
        assert o.legacy_patch == {"shoot": rank}
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
        assert o.legacy_patch == {"charge": int(o.target_idx), "attack": 1}
    assert any(o.kind is ActionKind.PASS for o in opts)


def test_shoot_targets_union_matches_shoot_mask():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.unit_coords[1] = [10, 11]
    env.enemy_coords[0] = [11, 10]
    env.enemy_coords[1] = [12, 10]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["shoot"]
    mask_ids = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}

    gen_ids: set[int] = set()
    for u in range(len(env.unit_health)):
        for o in shooting_options_for_unit(env, "model", u):
            if o.target_idx is not None:
                gen_ids.add(int(o.target_idx))

    # Маска shoot строится в глобальном id-пространстве как объединение целей всех юнитов;
    # при отсутствии целей маска вырождается в {0} (no-op), что генератор не порождает.
    if gen_ids:
        assert gen_ids == mask_ids


def test_charge_targets_union_matches_charge_mask():
    env = build_env()
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["charge"]
    mask_ids = {int(i) for i, v in enumerate(np.asarray(mask, dtype=bool)) if v}

    gen_ids: set[int] = set()
    for u in range(len(env.unit_health)):
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
        assert o.legacy_patch == {"move_num_0": k}
    # Генератор покрывает ровно весь исполнительный диапазон reachable.
    assert len(opts) == total


def test_movement_generator_exceeds_buggy_move_num_mask():
    """Документирует баг маски move_num (len(overlay)=2 → только индексы 0,1,2).

    Генератор движется по исполнительной истине и обязан давать НЕ меньше
    опций, чем разрешает сломанная маска.
    """
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    mask = env.get_legal_action_masks_by_head("model")["move_num_0"]
    mask_true = int(np.sum(np.asarray(mask, dtype=bool)))
    opts = movement_options_for_unit(env, "model", 0)
    assert len(opts) >= mask_true
