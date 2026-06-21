import core.envs.warhamEnv as we


def test_first_turn_winner_goes_first(monkeypatch):
    # enemy=5 > model=2 → победитель enemy ходит первым
    monkeypatch.setattr(we, "auto_dice", lambda: 2)   # model
    seq = iter([5])                                    # enemy
    monkeypatch.setattr(we, "player_dice", lambda *a, **k: next(seq))
    monkeypatch.setenv("MANUAL_DICE", "1")
    assert we.roll_off_first_turn(manual_roll_allowed=True) == "enemy"


def test_first_turn_model_wins(monkeypatch):
    rolls = iter([6, 3])  # auto_dice: model=6, затем enemy(auto)=3
    monkeypatch.setattr(we, "auto_dice", lambda: next(rolls))
    monkeypatch.delenv("MANUAL_DICE", raising=False)
    assert we.roll_off_first_turn(manual_roll_allowed=False) == "model"


def test_first_turn_reroll_on_tie(monkeypatch):
    # сначала ничья (3,3), потом model=4 enemy(auto)=1 → model
    rolls = iter([3, 3, 4, 1])
    monkeypatch.setattr(we, "auto_dice", lambda: next(rolls))
    monkeypatch.delenv("MANUAL_DICE", raising=False)
    assert we.roll_off_first_turn(manual_roll_allowed=False) == "model"
