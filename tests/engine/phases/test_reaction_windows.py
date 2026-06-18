import numpy as np

from core.engine.phases.option_generator import generate_windows
from core.engine.phases.reaction_windows import (
    build_reaction_windows,
    windowed_reaction_windows_enabled,
)
from core.engine.phases.stratagems import Trigger
from core.engine.phases.types import Phase, Timing
from tests.engine.phases._helpers import build_env


def test_reaction_windows_disabled_by_default(monkeypatch):
    monkeypatch.delenv("WINDOWED_REACTION_WINDOWS", raising=False)
    assert windowed_reaction_windows_enabled() is False


def test_generate_windows_has_no_reaction_timing():
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    for w in generate_windows(env, "model"):
        assert w.timing is not Timing.REACTION


def test_build_reaction_windows_empty_when_disabled(monkeypatch):
    monkeypatch.setenv("WINDOWED_REACTION_WINDOWS", "0")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    assert build_reaction_windows(env, "enemy", phase=Phase.MOVEMENT, trigger=Trigger.ENEMY_ENDED_MOVE) == []


def test_build_reaction_windows_overwatch_when_enabled(monkeypatch):
    monkeypatch.setenv("WINDOWED_REACTION_WINDOWS", "1")
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.enemyCP = 2
    env.unit_coords[0] = [10, 10]
    env.enemy_coords[0] = [12, 10]
    env._invalidate_target_cache("test")
    wins = build_reaction_windows(env, "enemy", phase=Phase.MOVEMENT, trigger=Trigger.ENEMY_ENDED_MOVE)
    assert wins
    assert all(w.timing is Timing.REACTION for w in wins)
    assert any("overwatch" in str(o.meta.get("stratagem_id", "")) for w in wins for o in w.options)
