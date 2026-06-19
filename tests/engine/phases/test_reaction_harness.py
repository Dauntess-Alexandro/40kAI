from tests.engine.phases._helpers import build_env


def _net_value_stub(value):
    class _Net:
        def infer(self, obs, masks_by_head=None):
            import torch

            return None, torch.tensor([float(value)])

    return _Net()


def test_simulate_branch_restores_state_and_returns_value():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    cp_before = env.modelCP
    called = {"apply": None}

    def resolve_trigger(apply):
        called["apply"] = apply  # триггер-резолв в симуляции (заглушка)

    ctx = {
        "side": "model",
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": cp_before,
        "env": env,
        "resolve_trigger": resolve_trigger,
        "net": _net_value_stub(0.42),
    }
    v = env._simulate_reaction_branch(ctx, apply=True)
    assert abs(v - 0.42) < 1e-6
    assert called["apply"] is True
    assert env.modelCP == cp_before  # внутренний снапшот восстановлен (no side-effects)
    assert env._reaction_sim_active is False  # флаг сброшен в finally


def test_recursion_guard_set_during_branch():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    seen = {}

    def resolve_trigger(apply):
        seen["guard"] = env._reaction_sim_active

    ctx = {
        "side": "model",
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": 1,
        "env": env,
        "resolve_trigger": resolve_trigger,
        "net": _net_value_stub(0.0),
    }
    env._simulate_reaction_branch(ctx, apply=False)
    assert seen["guard"] is True
