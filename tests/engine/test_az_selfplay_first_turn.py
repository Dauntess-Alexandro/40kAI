import types

from core.engine.turn_sequencing import apply_first_turn_prepend


def _env(first):
    return types.SimpleNamespace(
        turn_order=[first, "model" if first == "enemy" else "enemy"],
        game_over=False,
    )


def test_prepend_when_enemy_first():
    calls = []
    apply_first_turn_prepend(_env("enemy"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == ["enemy"]


def test_no_prepend_when_model_first():
    calls = []
    apply_first_turn_prepend(_env("model"), run_enemy_half=lambda: calls.append("enemy"))
    assert calls == []


def test_no_prepend_when_already_game_over():
    calls = []
    e = _env("enemy")
    e.game_over = True
    apply_first_turn_prepend(e, run_enemy_half=lambda: calls.append("enemy"))
    assert calls == []
