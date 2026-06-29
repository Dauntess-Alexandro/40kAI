import json
import random

from core.engine.opponent_pool import OpponentPool, OpponentStatsStore, PoolConfig
from core.models.opponent_pool_runtime import (
    LeagueLearnerSnapshotWriter,
    LeagueSnapshotSaveArgs,
    OpponentPoolStatsWriter,
    OpponentRuntimeCache,
    algo_short_label,
    build_pool_result_payload,
    build_pool_for_actor,
    build_pool_ui_state,
    choose_opponent_policy_fn,
    describe_episode_opponent,
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


def test_algo_short_label_mapping():
    assert algo_short_label("ppo") == "PPO"
    assert algo_short_label("gumbel_az") == "GAZ"
    assert algo_short_label("unknown_algo") == "UNKN"


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


def test_learner_writer_aggregates_multiple_actor_results(tmp_path):
    stats_path = tmp_path / "stats.json"
    run_path = tmp_path / "run.json"
    cfg = PoolConfig(enabled=True, p_heuristic=0.30, ema_alpha=0.15)
    writer = OpponentPoolStatsWriter(
        stats_path=str(stats_path),
        run_state_path=str(run_path),
        config=cfg,
        learner_side="P1",
        learner_algo="ppo",
        run_id="test-run",
    )
    writer.handle({
        "actor_idx": 0, "actor_ep": 1, "kind": "snapshot", "agent_id": "A",
        "reason": "pfsp", "prob_episode": 0.35, "result": "win", "vp_diff": 1,
    })
    writer.handle({
        "actor_idx": 7, "actor_ep": 1, "kind": "snapshot", "agent_id": "A",
        "reason": "pfsp", "prob_episode": 0.35, "result": "loss", "vp_diff": -1,
    })
    writer.handle({
        "actor_idx": 3, "actor_ep": 1, "kind": "heuristic", "agent_id": "",
        "reason": "heuristic_anchor", "prob_episode": 0.30, "result": "draw", "vp_diff": 0,
    })

    persisted = json.loads(stats_path.read_text(encoding="utf-8"))
    assert persisted["schema_version"] == 2
    assert persisted["opponents"]["A"]["games"] == 2
    assert persisted["opponents"]["A"]["wins"] == 1
    assert persisted["opponents"]["A"]["losses"] == 1
    run = json.loads(run_path.read_text(encoding="utf-8"))
    assert run["total_games"] == 3
    assert run["snapshot_games"] == 2
    assert run["heuristic_games"] == 1
    assert run["wins"] == 1 and run["draws"] == 1 and run["losses"] == 1


def test_learner_writer_preserves_actor_zero_in_log_and_live_state(tmp_path):
    logs: list[str] = []
    writer = OpponentPoolStatsWriter(
        stats_path=str(tmp_path / "stats.json"),
        run_state_path=str(tmp_path / "run.json"),
        config=PoolConfig(enabled=True),
        learner_side="P1",
        learner_algo="ppo",
    )
    writer.handle({
        "actor_idx": 0,
        "actor_ep": 1,
        "kind": "heuristic",
        "result": "draw",
        "vp_diff": 0,
        "prob_episode": 0.3,
    }, log_fn=logs.append)
    assert "actor=0" in logs[-1]
    assert writer.run_state["last_opponent"]["actor_idx"] == 0
    ep = {"actor_idx": 0, "actor_ep": 1}
    writer.attach_episode_opponent(ep)
    assert ep["source"] == "local"
    assert ep["opponent_label"] == "heuristic"


def test_episode_opponent_descriptor_contains_algo_and_epoch():
    fields = describe_episode_opponent(
        kind="snapshot",
        agent_id="P2_Necrons_annihilation_v2_final_ep100_20260629_104052",
        algo_hint="ppo",
        reason="pfsp",
    )
    assert fields["opponent_label"] == "PPO:ep100"
    assert fields["opponent_algo"] == "ppo"
    assert fields["opponent_ep"] == 100
    assert fields["opponent_reason"] == "pfsp"


def test_actor_result_payload_updates_only_local_sampler():
    pool = _pool_with(["A"])
    choice = pool.sample()
    payload = build_pool_result_payload(
        pool=pool,
        choice=choice,
        result="win",
        vp_diff=1,
        actor_idx=2,
        actor_ep=5,
    )
    assert pool.stats.games("A") == 1
    assert payload["kind"] == "snapshot"
    assert payload["prob_snapshot"] == 1.0
    assert payload["prob_episode"] == 1.0


def test_ui_state_exposes_episode_probability_and_run_stats(tmp_path, monkeypatch):
    import core.models.opponent_pool_runtime as runtime

    stats_path = tmp_path / "stats.json"
    run_path = tmp_path / "run.json"
    stats = OpponentStatsStore(str(stats_path))
    stats.update(agent_id="A", win=False, draw=True, vp_diff=0)
    stats.save()
    run_path.write_text(json.dumps({
        "learner_side": "P1",
        "total_games": 4,
        "snapshot_games": 3,
        "heuristic_games": 1,
        "wins": 1,
        "draws": 2,
        "losses": 1,
        "opponents": {
            "A": {"games": 3, "wins": 1, "draws": 1, "losses": 1},
            "__heuristic__": {"games": 1, "wins": 0, "draws": 1, "losses": 0},
        },
    }), encoding="utf-8")
    monkeypatch.setattr(runtime, "default_candidate_provider", lambda: [
        {"agent_id": "A", "side": "P2", "contract": {}, "created_at": "2026-06-29T10:00:00"}
    ])
    monkeypatch.setattr(runtime, "_resolve_learner_contract_for_ui", lambda learner_side: {})
    monkeypatch.setattr(runtime, "_registry_meta_index", lambda: {
        "A": {"agent_id": "A", "algo": "ppo", "created_at": "2026-06-29T10:00:00"}
    })
    monkeypatch.setattr(runtime, "_count_registry_side", lambda side: 1)

    state = build_pool_ui_state(
        learner_side="P1",
        learner_faction="Necrons",
        config=PoolConfig(enabled=True, p_heuristic=0.30, pool_size=1),
        stats_path=str(stats_path),
        run_state_path=str(run_path),
    )
    row = state["candidates"][0]
    assert row["prob_snapshot"] == 1.0
    assert row["prob_episode"] == 0.7
    assert row["run_games"] == 3
    assert row["run_actual_prob"] == 0.75
    assert row["run_wins"] == 1 and row["run_draws"] == 1 and row["run_losses"] == 1
    assert state["heuristic"]["run_actual_prob"] == 0.25


def test_league_snapshot_writer_periodic_and_final(monkeypatch, tmp_path):
    from core.engine.agent_registry import AgentIdentity

    saved: list[tuple[str, int, str]] = []

    def _fake_save(**kwargs):
        saved.append((str(kwargs["agent_id"]), int(kwargs["extra_meta"]["episode"]), str(kwargs["extra_meta"]["league_snapshot"])))
        return str(tmp_path / "artifact")

    monkeypatch.setattr(
        "core.engine.agent_registry.save_agent_artifact",
        lambda **kwargs: _fake_save(**kwargs),
    )
    monkeypatch.setattr(
        "core.engine.agent_registry.build_agent_id",
        lambda identity, tag: f"{identity.side}_test_{tag}",
    )

    identity = AgentIdentity(side="P1", faction="Necrons", ruleset_version="w40k_v1")
    writer = LeagueLearnerSnapshotWriter(
        every_episodes=100,
        identity=identity,
        env_contract={"contract_hash": "x"},
        log_fn=None,
    )
    args = LeagueSnapshotSaveArgs(policy_state_dict={"w": 1})

    assert writer.maybe_periodic(50, args) is None
    assert writer.maybe_periodic(100, args) is not None
    assert writer.maybe_periodic(100, args) is None
    assert writer.maybe_periodic(190, args) is None
    assert writer.maybe_final(190, args) is not None
    assert writer.maybe_final(190, args) is None

    writer2 = LeagueLearnerSnapshotWriter(
        every_episodes=100,
        identity=identity,
        env_contract={"contract_hash": "x"},
        log_fn=None,
    )
    writer2.maybe_periodic(200, args)
    assert writer2.maybe_final(200, args) is None

    assert [row[1:] for row in saved] == [(100, "periodic"), (190, "final"), (200, "periodic")]
