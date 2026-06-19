from core.engine.phases.legacy_compiler import compile_options_to_action_dict, default_action_dict
from core.engine.phases.types import ActionKind, ActionOption
from tests.engine.phases._helpers import build_env


def test_action_space_has_per_unit_heads():
    env = build_env()
    sp = env.action_space.spaces
    assert "shoot" not in sp and "charge" not in sp
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    for i in range(n_model):
        assert sp[f"shoot_num_{i}"].n == n_enemy
        assert sp[f"charge_num_{i}"].n == n_enemy


def test_masks_have_per_unit_shoot_charge():
    env = build_env()
    masks = env.get_legal_action_masks_by_head("model")
    n_model = len(env.unit_health)
    n_enemy = len(env.enemy_health)
    for i in range(n_model):
        assert masks[f"shoot_num_{i}"].shape[0] == n_enemy
        assert masks[f"charge_num_{i}"].shape[0] == n_enemy


def test_flat_shoot_uses_per_unit_head(monkeypatch):
    import core.envs.warhamEnv as warham_mod

    hits = []

    def fake_attack(ah, w, ad, dh, dd, *a, **k):
        hits.append(1)
        return [0.0], dh

    monkeypatch.setattr(warham_mod, "attack", fake_attack)
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [0.0, 0.0]
    env.unit_coords[1] = [0.0, 0.0]
    env.enemy_coords[0] = [1.0, 1.0]
    env.enemy_coords[1] = [1.0, 1.0]
    action = {"shoot_num_0": 0, "shoot_num_1": 0}
    env.shooting_phase("model", action=action)
    assert len(hits) >= 1  # выстрелы по per-unit головам, без KeyError 'shoot'


def test_flat_charge_uses_per_unit_head():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    action = {"attack": 1, "charge_num_0": 0, "charge_num_1": 0}
    # не должно падать с KeyError 'charge'
    env.charge_phase("model", action=action, advanced_flags=[False] * len(env.unit_health))
    assert True


def test_compile_keeps_per_unit_shoot():
    opts = [
        ActionOption(kind=ActionKind.SHOOT, unit_idx=0, legacy_patch={"shoot_num_0": 2}),
        ActionOption(kind=ActionKind.SHOOT, unit_idx=1, legacy_patch={"shoot_num_1": 1}),
    ]
    a = compile_options_to_action_dict(opts, len_model=2)
    assert a["shoot_num_0"] == 2 and a["shoot_num_1"] == 1


def test_default_action_dict_per_unit():
    a = default_action_dict(2)
    assert "shoot" not in a and "charge" not in a
    assert a["shoot_num_0"] == 0 and a["charge_num_1"] == 0
