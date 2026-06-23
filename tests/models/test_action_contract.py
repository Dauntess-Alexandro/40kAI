from core.engine.phases.stratagems import STRATAGEM_PHASES
from core.models.action_contract import BASE_ACTION_HEADS, ordered_action_keys


def test_base_heads_drop_single_shoot_charge():
    assert "shoot" not in BASE_ACTION_HEADS
    assert "charge" not in BASE_ACTION_HEADS


def test_ordered_keys_have_per_unit_shoot_charge():
    keys = ordered_action_keys(2)
    # Пофазные головы strat_<phase> добавлены аддитивно (Task 2) после per-unit голов.
    strat_keys = []
    for ph in STRATAGEM_PHASES:
        strat_keys.append(f"strat_{ph.value}")
        strat_keys.append(f"strat_{ph.value}_unit")
    assert keys == [
        "move", "attack",
        "move_num_0", "move_num_1",
        "shoot_num_0", "shoot_num_1",
        "charge_num_0", "charge_num_1",
        *strat_keys,
    ]
