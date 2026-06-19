from core.engine.phases.windowed_selfplay import run_model_fight_from_action
from tests.engine.phases._helpers import build_env, flat_default_action


def _action(n: int) -> dict:
    return flat_default_action(n)


def _setup_engaged(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [11, 10]
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env.enemyCP = 0
    env.unitCharged = [0] * len(env.unit_health)
    env.enemyCharged = [0] * len(env.enemy_health)
    env._invalidate_target_cache("test")


def test_fight_phase_skips_pending_plan_when_windowed(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _setup_engaged(env)
    env._pending_fight_stratagem_plan = {0: "hungry_void"}
    env.modelCP = 2
    snap = env.snapshot_state()

    with env.simulation_mode():
        env.fight_phase("model")
        used = list(env.stratagem_used)
        assert env._pending_fight_stratagem_plan is None
    env.restore_state(snap)

    assert not any("hungry_void" in str(x) for x in used)


def test_run_model_fight_applies_pending_plan(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "1")
    env = build_env()
    _setup_engaged(env)
    env.unit_data[0]["Keywords"] = ["Necrons"]
    env._pending_fight_stratagem_plan = {0: "hungry_void"}
    env.modelCP = 2
    snap = env.snapshot_state()

    with env.simulation_mode():
        from core.engine.phases.types import PhaseTurnState

        run_model_fight_from_action(env, _action(len(env.unit_health)), PhaseTurnState(side="model"))
        used = list(env.stratagem_used)
    env.restore_state(snap)

    assert any("hungry_void" in str(x) for x in used)


def test_pending_fight_plan_applied_when_legacy(monkeypatch):
    monkeypatch.setenv("WINDOWED_SELFPLAY", "0")
    env = build_env()
    _setup_engaged(env)
    env._pending_fight_stratagem_plan = {0: "hungry_void"}
    env.modelCP = 2
    snap = env.snapshot_state()

    with env.simulation_mode():
        env.fight_phase("model")
        used = list(env.stratagem_used)
    env.restore_state(snap)

    assert any("hungry_void" in str(x) for x in used)
