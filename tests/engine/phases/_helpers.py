from core.engine.mission import apply_end_of_battle
from core.engine.phases import default_action_dict, phase_engine
from core.engine.phases.types import ActionKind, Phase
from core.engine.unit import Unit
from core.envs.warhamEnv import Warhammer40kEnv


def flat_default_action(n: int, **overrides: int) -> dict[str, int]:
    """Нейтральный flat action_dict для тестов (B2 per-unit shoot/charge)."""
    action = default_action_dict(int(n))
    action.update(overrides)
    return action


def make_unit(name: str, movement: int = 6, models: int = 3, wounds: int = 2, rng: int = 24, keywords: list[str] | None = None) -> Unit:
    data = {
        "Name": name,
        "Movement": movement,
        "M": movement,
        "W": wounds,
        "#OfModels": models,
        "OC": 1,
        "Ld": 7,
        "T": 4,
        "Sv": 3,
    }
    if keywords is not None:
        data["Keywords"] = list(keywords)
    weapon = {
        "Name": "Stub gun",
        "Type": "Ranged",
        "Range": rng,
        "A": 1,
        "BS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    melee = {
        "Name": "Stub blade",
        "Type": "Melee",
        "Range": 2,
        "A": 1,
        "WS": 4,
        "S": 4,
        "AP": 0,
        "Damage": 1,
    }
    return Unit(data=data, weapon=weapon, melee=melee, b_len=30, b_hei=30, GUI=False)


def build_env(b_len: int = 30, b_hei: int = 30) -> Warhammer40kEnv:
    model = [make_unit("ModelA"), make_unit("ModelB")]
    enemy = [make_unit("EnemyA"), make_unit("EnemyB")]
    return Warhammer40kEnv(enemy=enemy, model=model, b_len=b_len, b_hei=b_hei)


def _default_window_decide(window):
    if window.phase is Phase.MOVEMENT:
        for opt in window.options:
            if opt.param.get("reachable_index") == 0:
                return opt
    if window.phase is Phase.SHOOTING:
        for opt in window.options:
            if opt.kind is ActionKind.SHOOT and opt.param.get("local_rank") == 0:
                return opt
    if window.phase is Phase.CHARGE:
        for opt in window.options:
            if opt.kind is ActionKind.CHARGE and opt.target_idx == 0:
                return opt
    return window.options[0]


def run_windowed_default_turn(env: Warhammer40kEnv, side: str = "model"):
    """Test-only helper: run one windowed turn using legacy default choices."""
    env._invalidate_target_cache(f"windowed_default_start:{side}")
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env.active_side = side

    state = phase_engine.run_command(env, side, _default_window_decide)
    state = phase_engine.run_movement(env, side, _default_window_decide, state)
    state = phase_engine.run_shooting(env, side, _default_window_decide, state)
    state = phase_engine.run_charge(env, side, _default_window_decide, state)
    state = phase_engine.run_fight(env, side, _default_window_decide, state)
    env._invalidate_target_cache(f"windowed_default_after_fight:{side}")
    apply_end_of_battle(env, log_fn=env._log)
    if side == "model":
        env.enemyStrat["overwatch"] = -1
        env.enemyStrat["smokescreen"] = -1
    else:
        env.modelStrat["overwatch"] = -1
        env.modelStrat["smokescreen"] = -1
    return state
