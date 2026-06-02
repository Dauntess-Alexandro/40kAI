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
