from core.engine.phases.legacy_compiler import (
    compile_options_to_action_dict,
    default_action_dict,
)
from core.engine.phases.option_generator import movement_options_for_unit
from core.engine.phases.types import ActionKind, ActionOption
from tests.engine.phases._helpers import build_env


def test_default_action_dict_shape():
    d = default_action_dict(2)
    assert d["move"] == 4 and d["attack"] == 1
    assert d["shoot_num_0"] == 0 and d["charge_num_0"] == 0
    assert d["use_cp"] == 0 and d["cp_on"] == 0
    assert d["move_num_0"] == 0 and d["move_num_1"] == 0
    assert "move_num_2" not in d


def test_compile_applies_patches_in_order():
    opts = [
        ActionOption(kind=ActionKind.MOVE, unit_idx=0, legacy_patch={"move_num_0": 3}),
        ActionOption(kind=ActionKind.SHOOT, unit_idx=0, target_idx=5, legacy_patch={"shoot_num_0": 1}),
        ActionOption(kind=ActionKind.CHARGE, unit_idx=1, target_idx=0, legacy_patch={"charge_num_1": 0, "attack": 1}),
        ActionOption(kind=ActionKind.USE_STRATAGEM, unit_idx=1, legacy_patch={"use_cp": 1, "cp_on": 1}),
    ]
    d = compile_options_to_action_dict(opts, len_model=2)
    assert d["move_num_0"] == 3
    assert d["shoot_num_0"] == 1
    assert d["charge_num_1"] == 0 and d["attack"] == 1
    assert d["use_cp"] == 1 and d["cp_on"] == 1


def test_movement_roundtrip_executes_to_chosen_cell():
    """Опция движения → compile → исполнение movement_phase даёт ту же клетку.

    Прогон в simulation_mode + restore: поведение env не затрагивается.
    """
    env = build_env()
    env.unit_coords[0] = [15, 15]
    env._invalidate_target_cache("test")

    opts = movement_options_for_unit(env, "model", 0)
    # выбираем последнюю достижимую опцию (не stay), если она есть
    move_opts = [o for o in opts if o.kind in (ActionKind.MOVE, ActionKind.ADVANCE)]
    chosen = move_opts[-1] if move_opts else opts[0]
    dest_x, dest_y = chosen.param["dest"]

    action = compile_options_to_action_dict([chosen], len_model=len(env.unit_health))

    snap = env.snapshot_state()
    with env.simulation_mode():
        try:
            env.movement_phase("model", action=action, battle_shock=[False] * len(env.unit_health))
            # warhamEnv хранит координаты как [dest[1], dest[0]]
            assert list(env.unit_coords[0]) == [int(dest_y), int(dest_x)]
        finally:
            env.restore_state(snap)

    # после restore состояние вернулось
    assert list(env.unit_coords[0]) == [15, 15]
