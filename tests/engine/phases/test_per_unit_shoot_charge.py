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
