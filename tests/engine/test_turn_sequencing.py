import types

from core.engine.turn_sequencing import run_battle_round


def _env(turn_order, game_over_after=None):
    e = types.SimpleNamespace()
    e.turn_order = list(turn_order)
    e.game_over = False
    e._after = game_over_after  # сторона, после которой выставить game_over
    return e


def test_calls_in_turn_order_model_first():
    calls = []
    e = _env(["model", "enemy"])
    run_battle_round(
        e,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["model", "enemy"]


def test_calls_in_turn_order_enemy_first():
    calls = []
    e = _env(["enemy", "model"])
    run_battle_round(
        e,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["enemy", "model"]


def test_short_circuit_on_game_over():
    calls = []
    e = _env(["enemy", "model"])

    def enemy():
        calls.append("enemy")
        e.game_over = True

    run_battle_round(e, run_model_half=lambda: calls.append("model"), run_enemy_half=enemy)
    assert calls == ["enemy"]  # model-половина не вызвана


def test_reads_unwrapped_turn_order():
    calls = []
    inner = types.SimpleNamespace(turn_order=["model", "enemy"], game_over=False)
    wrapper = types.SimpleNamespace(unwrapped=inner)
    run_battle_round(
        wrapper,
        run_model_half=lambda: calls.append("model"),
        run_enemy_half=lambda: calls.append("enemy"),
    )
    assert calls == ["model", "enemy"]
