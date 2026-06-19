from core.models.action_contract import BASE_ACTION_HEADS, ordered_action_keys


def test_base_heads_drop_single_shoot_charge():
    assert "shoot" not in BASE_ACTION_HEADS
    assert "charge" not in BASE_ACTION_HEADS


def test_ordered_keys_have_per_unit_shoot_charge():
    keys = ordered_action_keys(2)
    assert keys == [
        "move", "attack", "use_cp", "cp_on",
        "move_num_0", "move_num_1",
        "shoot_num_0", "shoot_num_1",
        "charge_num_0", "charge_num_1",
    ]
