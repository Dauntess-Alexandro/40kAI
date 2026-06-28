from core.models.opponent_pool_runtime import OpponentRuntimeCache, build_pool_for_actor
from core.engine.opponent_pool import PoolConfig


def test_cache_builds_once_per_id():
    calls = {"n": 0}
    def build(aid):
        calls["n"] += 1
        return f"net::{aid}"
    cache = OpponentRuntimeCache(build_fn=build, maxsize=2)
    assert cache.get("A") == "net::A"
    assert cache.get("A") == "net::A"
    assert calls["n"] == 1  # повтор не пересобирает


def test_cache_lru_eviction():
    calls = {"n": 0}
    def build(aid):
        calls["n"] += 1
        return aid
    cache = OpponentRuntimeCache(build_fn=build, maxsize=2)
    cache.get("A"); cache.get("B"); cache.get("C")  # A вытеснен
    cache.get("A")  # пересборка A
    assert calls["n"] == 4


def test_build_pool_disabled_returns_none():
    cfg = PoolConfig(enabled=False)
    pool = build_pool_for_actor(learner_identity=None, learner_contract={}, config=cfg,
                                stats_path=":memory:", seed=0)
    assert pool is None
