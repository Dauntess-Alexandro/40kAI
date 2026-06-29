# tests/engine/test_opponent_pool.py
import json
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


def test_refresh_filters_side_and_contract():
    learner_contract = {"ruleset_version": "r1", "obs_space_signature": "vec:10",
                        "action_space_signature": "heads:3,3"}
    same = dict(learner_contract)
    bad = dict(learner_contract, obs_space_signature="vec:999")
    provided = [
        {"agent_id": "p2_new", "side": "P2", "contract": same, "created_at": "2026-06-28T10:00:00"},
        {"agent_id": "p2_old", "side": "P2", "contract": same, "created_at": "2026-06-01T10:00:00"},
        {"agent_id": "p1_self", "side": "P1", "contract": same, "created_at": "2026-06-28T11:00:00"},
        {"agent_id": "p2_incompat", "side": "P2", "contract": bad, "created_at": "2026-06-28T12:00:00"},
    ]
    from core.engine.agent_registry import AgentIdentity
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="Necrons"),
        learner_contract=learner_contract,
        config=PoolConfig(enabled=True, pool_size=8),
        stats=OpponentStatsStore(":memory:"), rng=random.Random(0),
        candidate_provider=lambda: provided,
    )
    ids = pool.refresh_candidates()
    assert ids == ["p2_new", "p2_old"]  # P1 (своя сторона) и несовместимый отфильтрованы; новые первыми
    diag = pool.refresh_diagnostics()
    assert diag["registry_total"] == 4
    assert diag["filtered_side"] == 1
    assert diag["filtered_contract"] == 1
    assert diag["contract_compatible"] == 2
    assert diag["selected"] == 2


def test_refresh_trims_to_pool_size():
    from core.engine.agent_registry import AgentIdentity
    c = {"ruleset_version": "r", "obs_space_signature": "vec:1", "action_space_signature": "heads:1"}
    provided = [{"agent_id": f"p2_{i}", "side": "P2", "contract": c,
                 "created_at": f"2026-06-{i+1:02d}T00:00:00"} for i in range(10)]
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="X"), learner_contract=c,
        config=PoolConfig(enabled=True, pool_size=3),
        stats=OpponentStatsStore(":memory:"), rng=random.Random(0),
        candidate_provider=lambda: provided,
    )
    ids = pool.refresh_candidates()
    assert len(ids) == 3
    assert ids == ["p2_9", "p2_8", "p2_7"]  # три самых новых


def test_record_result_updates_stats():
    from core.engine.agent_registry import AgentIdentity
    stats = OpponentStatsStore(":memory:")
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="X"), learner_contract={},
        config=PoolConfig(enabled=True), stats=stats, rng=random.Random(0),
        candidate_provider=lambda: [],
    )
    pool.record_result(agent_id="A", win=True, draw=False, vp_diff=2.0)
    assert stats.games("A") == 1
    assert stats.record("A")["wins"] == 1
    assert stats.record("A")["losses"] == 0


def test_legacy_stats_migration_keeps_unknown_results_honest(tmp_path):
    path = tmp_path / "stats.json"
    path.write_text(json.dumps({
        "opponents": {
            "OLD": {"games": 10, "ema_winrate": 0.6, "draws": 4, "vp_sum": 2.0, "updated_at": "x"}
        }
    }), encoding="utf-8")

    stats = OpponentStatsStore.load(str(path))
    rec = stats.record("OLD")
    assert rec["wins"] == 0
    assert rec["losses"] == 0
    assert rec["tracked_draws"] == 0
    assert rec["unclassified_games"] == 10

    stats.update(agent_id="OLD", win=False, draw=False, vp_diff=-1.0)
    rec = stats.record("OLD")
    assert rec["games"] == 11
    assert rec["losses"] == 1
    assert rec["unclassified_games"] == 10
