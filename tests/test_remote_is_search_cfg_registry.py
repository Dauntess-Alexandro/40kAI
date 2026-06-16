"""Тесты реестра remote IS search_cfg."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.models.remote_is_search_cfg_registry import (
    REMOTE_IS_SEARCH_CFG_SPECS,
    prepare_inference_launch,
    publish_all_remote_search_cfgs_from_repo,
    spec_for_pc2_role,
)


def test_registry_has_gmz_az_smz():
    ids = {s.algo_id for s in REMOTE_IS_SEARCH_CFG_SPECS}
    assert ids == {"gmz", "az", "smz"}


def test_spec_for_pc2_roles():
    assert spec_for_pc2_role("gmz_inference") is not None
    assert spec_for_pc2_role("az_inference") is not None
    assert spec_for_pc2_role("smz_inference") is not None
    assert spec_for_pc2_role("dqn_actors") is None


def test_prepare_inference_launch_noop_for_actors():
    prep = prepare_inference_launch("dqn_actors", r"C:\share")
    assert prep.ok is True
    assert prep.message == ""


def test_publish_all_returns_all_algos(tmp_path, monkeypatch):
    import project_paths as pp

    monkeypatch.setenv("40KAI_SHARE_ROOT", str(tmp_path))
    monkeypatch.setattr(pp, "TRAIN_DATA_PATH", tmp_path / "no_data.json")
    results = publish_all_remote_search_cfgs_from_repo(sources=["test"])
    assert set(results.keys()) == {"gmz", "az", "smz"}
    for info in results.values():
        assert "ok" in info


def test_prepare_gmz_with_existing_cfg(tmp_path):
    actor_sync = tmp_path / "actor_sync"
    actor_sync.mkdir()
    cfg = {
        "obs_dim": 17,
        "action_sizes": [5, 2, 2, 2, 5, 2, 24, 24],
        "latent_dim": 256,
        "hidden_dim": 256,
        "num_layers": 2,
        "action_embed_dim": 64,
        "num_simulations": 24,
        "root_top_k": 8,
        "discount": 0.997,
        "temperature": 0.15,
        "gumbel_scale": 1.0,
        "prior_weight": 0.0,
        "batch_recurrent": 1,
        "tree_reuse": 1,
    }
    (actor_sync / "gmz_remote_search_cfg.json").write_text(json.dumps(cfg), encoding="utf-8")
    prep = prepare_inference_launch("gmz_inference", str(tmp_path))
    assert prep.ok is True
    assert "GMZ_REMOTE_SEARCH_CONFIG" in dict(prep.env_extra)
