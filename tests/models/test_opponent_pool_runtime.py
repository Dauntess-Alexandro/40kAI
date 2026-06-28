import random

from core.engine.opponent_pool import OpponentPool, OpponentStatsStore, PoolConfig
from core.models.opponent_pool_runtime import (
    OpponentRuntimeCache,
    build_pool_for_actor,
    choose_opponent_policy_fn,
)


def _pool_with(candidates, *, p_heuristic=0.0, seed=0):
    pool = OpponentPool(
        learner_identity=None, learner_contract={},
        config=PoolConfig(enabled=True, p_heuristic=p_heuristic),
        stats=OpponentStatsStore(":memory:"), rng=random.Random(seed),
        candidate_provider=lambda: [],
    )
    pool.set_candidates(candidates)
    return pool


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


def test_choose_opponent_returns_policy_fn_on_success():
    pool = _pool_with(["GOOD"])
    cache = OpponentRuntimeCache(build_fn=lambda aid: f"fn::{aid}", maxsize=4)
    choice, fn = choose_opponent_policy_fn(pool, cache, log_fn=None, actor_label="actor=0 ep=1")
    assert choice.kind == "snapshot"
    assert choice.agent_id == "GOOD"
    assert fn == "fn::GOOD"


def test_choose_opponent_fallback_on_build_error():
    pool = _pool_with(["BAD"])

    def boom(aid):
        raise RuntimeError("corrupt snapshot")

    cache = OpponentRuntimeCache(build_fn=boom, maxsize=4)
    logs: list[str] = []
    choice, fn = choose_opponent_policy_fn(pool, cache, log_fn=logs.append, actor_label="actor=0 ep=1")
    assert fn is None                                  # fallback на эвристику, актор не падает
    assert choice.kind == "heuristic"
    assert choice.reason == "heuristic_fallback"
    assert any("[POOL][WARN]" in m for m in logs)
    assert "BAD" not in pool._candidates               # битый снапшот выкинут из пула


def test_choose_opponent_heuristic_anchor_no_build():
    built = {"n": 0}

    def build(aid):
        built["n"] += 1
        return aid

    pool = _pool_with(["A"], p_heuristic=1.0)          # всегда эвристика
    cache = OpponentRuntimeCache(build_fn=build, maxsize=4)
    choice, fn = choose_opponent_policy_fn(pool, cache, log_fn=None, actor_label="actor=0 ep=1")
    assert choice.kind == "heuristic"
    assert fn is None
    assert built["n"] == 0                             # эвристика не строит оппонента
