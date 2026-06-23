import torch

from core.engine.phases.legacy_compiler import default_action_dict
from core.engine.phases.stratagems import STRATAGEM_PHASES, stratagem_action_choices
from core.models.action_contract import (
    action_sizes_from_env,
    action_tensor_to_dict,
    ordered_action_keys,
)
from tests.engine.phases._helpers import build_env


def test_ordered_keys_have_strat_heads_no_use_cp():
    """Task 4: use_cp/cp_on убраны; strat-головы на месте."""
    keys = ordered_action_keys(2)
    for ph in STRATAGEM_PHASES:
        assert f"strat_{ph.value}" in keys
        assert f"strat_{ph.value}_unit" in keys
    assert "use_cp" not in keys and "cp_on" not in keys


def test_default_action_dict_sets_strat_zero():
    ad = default_action_dict(2)
    for ph in STRATAGEM_PHASES:
        assert ad[f"strat_{ph.value}"] == 0
        assert ad[f"strat_{ph.value}_unit"] == 0
    # Task 4: use_cp убран из контракта
    assert "use_cp" not in ad


def test_env_action_space_declares_strat_heads_with_sizes():
    env = build_env()  # 2 model units
    spaces = env.action_space.spaces
    for ph in STRATAGEM_PHASES:
        assert int(spaces[f"strat_{ph.value}"].n) == len(stratagem_action_choices(ph))
        assert int(spaces[f"strat_{ph.value}_unit"].n) == 2


def test_action_sizes_and_tensor_roundtrip():
    env = build_env()
    sizes = action_sizes_from_env(env, 2)  # не падает: все ordered-ключи есть в action_space
    keys = ordered_action_keys(2)
    assert len(sizes) == len(keys)
    vec = torch.zeros((1, len(keys)), dtype=torch.long)
    ad = action_tensor_to_dict(vec, 2)
    assert set(ad.keys()) == set(keys)


def test_contract_has_no_use_cp_cp_on():
    """Task 4: use_cp/cp_on убраны из контракта (bravery — только strat_command head)."""
    keys = ordered_action_keys(2)
    assert "use_cp" not in keys and "cp_on" not in keys
    assert "move" in keys and "attack" in keys
    # strat-головы на месте
    assert "strat_command" in keys
