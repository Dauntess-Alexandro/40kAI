from __future__ import annotations

import json
import os

from core.engine.agent_registry import (
    _remap_models_path,
    agents_meta_root,
    collect_registered_agents_meta,
    models_dir,
    resolve_latest_opponent_agent_id,
)
from core.models.az_rollout_sink import (
    az_dist_context_path,
    build_az_dist_worker_payloads,
    normalize_az_dist_hyperparams,
    pack_az_dist_hyperparams,
    read_az_dist_train_context,
    write_az_dist_train_context,
)


def test_write_and_read_dist_context(tmp_path, monkeypatch):
    sync = tmp_path / "actor_sync"
    sync.mkdir()
    monkeypatch.setenv("AZ_DIST_STOP_FLAG_PATH", str(sync / "az_dist_stop.flag"))
    write_az_dist_train_context({"opponent_agent_id": "agent_test", "learner_side": "P1"})
    assert read_az_dist_train_context()["opponent_agent_id"] == "agent_test"
    assert az_dist_context_path().endswith("az_dist_train_context.json")


def test_pack_and_pc2_mcts_payload_prefers_smb_hyperparams():
    defaults = {
        "simulations": 32,
        "parallel_simulations": 1,
        "max_depth": 1,
        "batch_eval_size": 16,
        "c_puct": 1.5,
        "c_puct_min": 1.0,
        "c_puct_max": 2.0,
        "c_puct_schedule": "none",
        "dirichlet_alpha": 0.3,
        "dirichlet_eps": 0.25,
        "top_k_per_head": 10,
        "mode": "tree",
        "root_dirichlet_only": True,
        "eval_cache_size": 10000,
        "pw_alpha": 1.0,
        "pw_beta": 0.5,
        "prior_weight_early": 0.25,
        "simulate_enemy_in_tree": True,
        "temperature_opening_moves": 12,
        "temperature_opening_value": 0.9,
        "temperature_late_value": 0.15,
        "outcome_only": True,
        "outcome_value_win": 1.0,
        "outcome_value_loss": -1.0,
        "outcome_value_draw": -0.25,
        "batch_send": 32,
        "inference_timeout": 5.0,
        "self_play_enabled": 0,
    }
    smb = pack_az_dist_hyperparams(
        {"mcts_parallel_sims": 8, "mcts_simulations": 64, "mcts_max_depth": 2, "noise": 999}
    )
    assert "noise" not in smb
    assert smb["mcts_parallel_sims"] == 8
    payloads = build_az_dist_worker_payloads(smb, defaults=defaults)
    assert payloads["mcts"]["parallel_simulations"] == 8
    assert payloads["mcts"]["simulations"] == 64
    assert payloads["mcts"]["max_depth"] == 2
    assert payloads["mcts"]["parallel_simulations"] != defaults["parallel_simulations"]
    empty = normalize_az_dist_hyperparams(None)
    assert empty == {}


def test_resolve_latest_opponent(tmp_path, monkeypatch):
    agents = tmp_path / "agents" / "a1"
    agents.mkdir(parents=True)
    meta = {
        "agent_id": "snap_old",
        "side": "P2",
        "created_at": "2020-01-01T00:00:00",
        "algo": "ppo",
    }
    (agents / "meta.json").write_text(json.dumps(meta), encoding="utf-8")
    agents2 = tmp_path / "agents" / "a2"
    agents2.mkdir(parents=True)
    meta2 = {
        "agent_id": "snap_new",
        "side": "P2",
        "created_at": "2026-01-01T00:00:00",
        "algo": "alphazero_tree",
    }
    (agents2 / "meta.json").write_text(json.dumps(meta2), encoding="utf-8")
    monkeypatch.setenv("MODELS_DIR", str(tmp_path))
    records = collect_registered_agents_meta()
    assert records[0]["agent_id"] == "snap_new"
    assert resolve_latest_opponent_agent_id(learner_side="P1") == "snap_new"
    assert resolve_latest_opponent_agent_id(learner_side="P2") == ""


def test_remap_models_path_pc1_to_smb(tmp_path, monkeypatch):
    smb = tmp_path / "models"
    agents = smb / "agents" / "P2" / "Necrons" / "agent1"
    agents.mkdir(parents=True)
    policy = agents / "policy.pth"
    policy.write_text("x", encoding="utf-8")
    monkeypatch.setenv("MODELS_DIR", str(smb))
    pc1_path = r"C:\40kAI\artifacts\models\agents\P2\Necrons\agent1\policy.pth"
    assert _remap_models_path(pc1_path) == str(policy)
    assert agents_meta_root() == str(smb / "agents")
    assert models_dir() == str(smb)
