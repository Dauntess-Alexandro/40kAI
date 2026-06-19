"""_simulate_reaction_branch: duck-typing DQN infer_with_value vs AZ infer."""

from tests.engine.phases._helpers import build_env


def test_dqn_path_calls_infer_with_value_with_masks():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}

    class _DqnNet:
        def infer_with_value(self, obs, masks_by_head=None):
            calls["method"] = "infer_with_value"
            calls["masks"] = masks_by_head
            import torch

            return None, torch.tensor([0.77])

        def infer(self, obs):
            calls["method"] = "infer"
            import torch

            return None, torch.tensor([0.0])

    ctx = {
        "side": "model",
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": 1,
        "env": env,
        "resolve_trigger": lambda apply: None,
        "net": _DqnNet(),
    }
    v = env._simulate_reaction_branch(ctx, apply=False)
    assert calls["method"] == "infer_with_value"
    assert calls["masks"] is not None
    assert len(calls["masks"]) > 0
    assert abs(v - 0.77) < 1e-6


def test_az_path_uses_infer():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    calls = {}

    class _AzNet:
        def infer(self, obs):
            calls["method"] = "infer"
            import torch

            return None, torch.tensor([0.33])

    ctx = {
        "side": "model",
        "stratagem_id": "go_to_ground",
        "phase": "shooting",
        "chosen": 0,
        "candidates": [0],
        "cp": 1,
        "env": env,
        "resolve_trigger": lambda apply: None,
        "net": _AzNet(),
    }
    v = env._simulate_reaction_branch(ctx, apply=True)
    assert calls["method"] == "infer"
    assert abs(v - 0.33) < 1e-6
