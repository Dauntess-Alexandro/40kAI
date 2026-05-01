import os
from pathlib import Path

from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv


def _mk_unit(name: str) -> Unit:
    data = {
        "Name": name,
        "W": 2,
        "#OfModels": 3,
        "OC": 1,
        "M": 5,
        "T": 4,
        "Sv": 3,
    }
    weapon = {
        "Name": "Stub gun",
        "Range": 12,
        "A": 1,
        "BS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    melee = {
        "Name": "Stub blade",
        "A": 1,
        "WS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    return Unit(data=data, weapon=weapon, melee=melee, b_len=20, b_hei=20, GUI=False)


def _build_env() -> Warhammer40kEnv:
    enemy = [_mk_unit("EnemyA"), _mk_unit("EnemyB")]
    model = [_mk_unit("ModelA"), _mk_unit("ModelB")]
    return Warhammer40kEnv(enemy=enemy, model=model, b_len=20, b_hei=20)


def test_snapshot_restore_returns_runtime_state():
    env = _build_env()
    env.unit_coords[0] = [3, 4]
    env.enemy_coords[1] = [8, 9]
    env.modelVP = 2
    env.enemyVP = 1
    env.modelCP = 3
    snap = env.snapshot_state()

    env.unit_coords[0] = [0, 0]
    env.enemy_coords[1] = [0, 0]
    env.modelVP = 0
    env.enemyVP = 0
    env.modelCP = 0

    env.restore_state(snap)
    assert env.unit_coords[0] == [3, 4]
    assert env.enemy_coords[1] == [8, 9]
    assert int(env.modelVP) == 2
    assert int(env.enemyVP) == 1
    assert int(env.modelCP) == 3


def test_simulation_mode_blocks_render_and_agent_log_side_effects():
    env = _build_env()
    display_dir = Path("display")
    display_dir.mkdir(parents=True, exist_ok=True)
    before_png = {p.name for p in display_dir.glob("*.png")}
    log_path = Path(getattr(env, "_agent_log_path", ""))
    before_log_size = log_path.stat().st_size if log_path.exists() else 0

    with env.simulation_mode():
        env._append_agent_log("[TEST] sandbox log")
        env.updateBoard()

    after_png = {p.name for p in display_dir.glob("*.png")}
    after_log_size = log_path.stat().st_size if log_path.exists() else 0
    assert before_png == after_png
    assert before_log_size == after_log_size
