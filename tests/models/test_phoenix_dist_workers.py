from core.engine.agent_registry import make_env_contract
from core.models.phoenix_dist import (
    PHOENIX_DIST_TOPUP_ACTOR_IDX,
    atomic_save_phoenix_sync,
    compute_phoenix_dist_topup_episodes,
    phoenix_actor_epsilon_floor,
    phoenix_dist_env_contract_extras,
    read_phoenix_dist_train_context,
    resolve_phoenix_dist_contract_hash,
    resolve_phoenix_dist_episode_split,
    split_count_among_workers,
    write_phoenix_dist_train_context,
)


def test_phoenix_dist_extras_match_pc1_pc2_style():
    extras = phoenix_dist_env_contract_extras(num_local_actors=8)
    assert extras == {"actor_learner": 1, "train_algo": "phoenix", "num_actors": 8}


def test_pc1_pc2_recomputed_hash_matches():
    n_act = [5, 2, 2]
    extras = phoenix_dist_env_contract_extras(num_local_actors=8)
    ec1 = make_env_contract(
        n_observations=17,
        n_actions=n_act,
        mission_name="only_war",
        ruleset_version="only_war_v1",
        extras=extras,
    )
    got = resolve_phoenix_dist_contract_hash(
        ctx={},
        n_observations=17,
        n_actions=n_act,
        mission_name="only_war",
        ruleset_version="only_war_v1",
        num_local_actors=8,
    )
    assert got == ec1["contract_hash"]


def test_resolve_phoenix_contract_hash_prefers_context():
    got = resolve_phoenix_dist_contract_hash(
        ctx={"env_contract_hash": "from_ctx"},
        n_observations=1,
        n_actions=[2],
        mission_name="only_war",
        ruleset_version="only_war_v1",
        num_local_actors=1,
    )
    assert got == "from_ctx"


def test_episode_split_and_worker_plan():
    local, remote = resolve_phoenix_dist_episode_split(total_episodes=400, local_fraction=0.7)
    assert (local, remote) == (280, 120)
    assert split_count_among_workers(total=120, num_workers=8) == [15] * 8


def test_topup_after_remote_dead_and_local_done():
    assert PHOENIX_DIST_TOPUP_ACTOR_IDX >= 9000
    assert (
        compute_phoenix_dist_topup_episodes(
            episodes_finished=90,
            total_episodes=100,
            local_actors_done=8,
            num_local_actors=8,
            remote_alive=0,
            topup_process_alive=False,
        )
        == 10
    )


def test_actor_epsilon_floor_is_ranked_and_single_actor_zero():
    assert phoenix_actor_epsilon_floor(actor_idx=0, total_actors=1) == 0.0
    lo = phoenix_actor_epsilon_floor(actor_idx=0, total_actors=4, floor_min=0.02, floor_max=0.2)
    hi = phoenix_actor_epsilon_floor(actor_idx=3, total_actors=4, floor_min=0.02, floor_max=0.2)
    remote = phoenix_actor_epsilon_floor(actor_idx=103, total_actors=4, floor_min=0.02, floor_max=0.2)
    assert lo == 0.02
    assert abs(hi - 0.2) < 1e-9
    assert abs(remote - hi) < 1e-9


def test_atomic_phoenix_sync_replaces_tmp(tmp_path):
    path = tmp_path / "latest_phoenix_policy.pth"

    def save_fn(payload, target):
        import json

        with open(target, "w", encoding="utf-8") as handle:
            json.dump(payload, handle)

    atomic_save_phoenix_sync({"policy_version": 7, "reset_id": 2}, str(path), save_fn=save_fn)
    assert path.is_file()
    assert not path.with_suffix(path.suffix + ".tmp").exists()
    assert '"policy_version": 7' in path.read_text(encoding="utf-8")


def test_phoenix_context_roundtrip_uses_override_path(tmp_path, monkeypatch):
    ctx_path = tmp_path / "phoenix_dist_train_context.json"
    monkeypatch.setenv("PHOENIX_DIST_CONTEXT_PATH", str(ctx_path))
    write_phoenix_dist_train_context({"env_contract_hash": "H", "sync_weights_name": "latest_phoenix_policy.pth"})
    got = read_phoenix_dist_train_context()
    assert got["env_contract_hash"] == "H"
    assert got["sync_weights_name"] == "latest_phoenix_policy.pth"
    assert "written_at" in got
