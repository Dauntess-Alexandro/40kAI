import types

from core.envs.warhamEnv import Warhammer40kEnv


def _stub(turn_order):
    s = types.SimpleNamespace()
    s.turn_order = list(turn_order)
    s.active_side = turn_order[0]
    s.battle_round = 1
    s.phase = "command"
    s._ends = 0

    def _end_battle_round(_self=s):
        _self._ends += 1
        _self.battle_round += 1
    s._end_battle_round = _end_battle_round
    return s


def _play_full_round(stub, order):
    # имитируем драйвер: каждая половина выставляет active_side своей стороны, затем advance
    for side in order:
        stub.active_side = side
        Warhammer40kEnv._advance_turn_order(stub)


def test_enemy_first_one_round_one_end():
    s = _stub(["enemy", "model"])
    _play_full_round(s, ["enemy", "model"])
    assert s._ends == 1
    assert s.battle_round == 2
    assert s.active_side == "enemy"  # начало следующего раунда = turn_order[0]


def test_model_first_one_round_one_end():
    s = _stub(["model", "enemy"])
    _play_full_round(s, ["model", "enemy"])
    assert s._ends == 1
    assert s.battle_round == 2
    assert s.active_side == "model"
