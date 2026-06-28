import os
from core.engine.opponent_pool import OpponentStatsStore


def test_unknown_agent_neutral():
    store = OpponentStatsStore(":memory:", ema_alpha=0.15)
    assert store.games("X") == 0
    assert store.winrate("X") == 0.5


def test_ema_update_win():
    store = OpponentStatsStore(":memory:", ema_alpha=0.15)
    store.update(agent_id="A", win=True, draw=False, vp_diff=3.0)
    assert store.games("A") == 1
    # ema = 0.85*0.5 + 0.15*1.0 = 0.575
    assert abs(store.winrate("A") - 0.575) < 1e-9


def test_ema_update_draw_then_loss():
    store = OpponentStatsStore(":memory:", ema_alpha=0.5)
    store.update(agent_id="A", win=False, draw=True, vp_diff=0.0)   # result 0.5 -> ema 0.5
    store.update(agent_id="A", win=False, draw=False, vp_diff=-2.0) # result 0.0 -> ema 0.25
    assert store.games("A") == 2
    assert abs(store.winrate("A") - 0.25) < 1e-9


def test_round_trip(tmp_path):
    path = os.path.join(str(tmp_path), "stats.json")
    store = OpponentStatsStore(path, ema_alpha=0.2)
    store.update(agent_id="A", win=True, draw=False, vp_diff=1.0)
    store.save()
    loaded = OpponentStatsStore.load(path, ema_alpha=0.2)
    assert loaded.games("A") == 1
    assert abs(loaded.winrate("A") - store.winrate("A")) < 1e-9
