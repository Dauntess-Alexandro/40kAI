from core.engine.phases.option_generator import (
    charge_options_for_unit,
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
