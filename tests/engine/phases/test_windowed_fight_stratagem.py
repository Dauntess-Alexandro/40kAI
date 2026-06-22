from tests.engine.phases._helpers import build_env


def test_fight_stratagem_applied_under_windowed(monkeypatch):
    import core.engine.phases.windowed_selfplay as ws
    monkeypatch.setattr(ws, "windowed_selfplay_enabled", lambda: True)
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.battle_round = 1
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.reaction_policy = None
    env.unitInAttack[0] = [1, 0]
    # Подтип «wound» закодирован через двоеточие — прямой apply без MC-гейта.
    env._pending_fight_stratagem_plan = {0: "command_reroll:wound"}
    env._apply_pending_fight_stratagem_plan("model")
    assert "command_reroll" in [r[1] for r in env.stratagem_used]
