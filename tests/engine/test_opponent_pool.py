# tests/engine/test_opponent_pool.py
import random
from core.engine.opponent_pool import OpponentPool, OpponentStatsStore, PoolConfig


def _pool(cfg, *, candidates, stats=None, seed=0):
    stats = stats or OpponentStatsStore(":memory:", ema_alpha=cfg.ema_alpha)
    pool = OpponentPool(
        learner_identity=None, learner_contract={}, config=cfg,
        stats=stats, rng=random.Random(seed),
        candidate_provider=lambda: [{"agent_id": a, "side": "P2", "contract": {}} for a in candidates],
    )
    pool.set_candidates(candidates)
    return pool


def test_empty_pool_always_heuristic():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0)
    pool = _pool(cfg, candidates=[])
    assert all(pool.sample().kind == "heuristic" for _ in range(20))


def test_p_heuristic_one_always_heuristic():
    cfg = PoolConfig(enabled=True, p_heuristic=1.0)
    pool = _pool(cfg, candidates=["A", "B"])
    assert all(pool.sample().kind == "heuristic" for _ in range(20))


def test_pfsp_prefers_low_winrate():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", pfsp_power=2.0,
                     uniform_floor=0.0, min_games_for_pfsp=1)
    stats = OpponentStatsStore(":memory:")
    # A: проигрываем (wr низкий) -> должен выбираться чаще; B: уверенно бьём
    for _ in range(20):
        stats.update(agent_id="A", win=False, draw=False, vp_diff=-1.0)
        stats.update(agent_id="B", win=True, draw=False, vp_diff=1.0)
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", pfsp_power=2.0,
                     uniform_floor=0.0, min_games_for_pfsp=1, ema_alpha=0.3)
    pool = _pool(cfg, candidates=["A", "B"], stats=stats, seed=42)
    picks = [pool.sample().agent_id for _ in range(400)]
    assert picks.count("A") > picks.count("B") * 2


def test_uniform_strategy_balanced():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="uniform", seed=1)
    pool = _pool(cfg, candidates=["A", "B"], seed=1)
    picks = [pool.sample().agent_id for _ in range(400)]
    assert 0.35 < picks.count("A") / 400 < 0.65


def test_novelty_reason_for_unseen():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", min_games_for_pfsp=3)
    pool = _pool(cfg, candidates=["NEW"])
    choice = pool.sample()
    assert choice.kind == "snapshot"
    assert choice.reason == "novelty"
