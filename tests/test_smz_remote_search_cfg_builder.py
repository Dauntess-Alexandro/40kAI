"""SMZ remote search_cfg: resolve/ensure для ПК2-лаунчера."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.gui_qt.pc2_launcher_backend import prepare_smz_inference_launch
from core.models.smz_remote_search_cfg_builder import (
    ACTOR_SYNC_SEARCH_CFG_NAME,
    ensure_smz_remote_search_cfg,
    resolve_smz_smb_paths,
)


def _valid_cfg() -> dict:
    return {
        "obs_dim": 17,
        "action_sizes": [5, 2, 2, 2, 5, 2, 24, 24],
        "latent_dim": 256,
        "hidden_dim": 256,
        "num_layers": 2,
        "action_embed_dim": 64,
        "num_samples": 24,
        "discount": 0.997,
        "temperature": 0.15,
        "sample_temperature": 1.0,
        "prior_weight": 0.0,
        "dedup": 1,
    }


def test_resolve_smz_smb_paths_models_layout(tmp_path):
    actor_sync = tmp_path / "actor_sync"
    actor_sync.mkdir()
    (actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME).write_text(
        json.dumps(_valid_cfg()), encoding="utf-8"
    )
    paths = resolve_smz_smb_paths(str(tmp_path))
    assert paths.search_cfg_path.endswith(ACTOR_SYNC_SEARCH_CFG_NAME)
    assert (actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME).as_posix() in paths.search_cfg_path.replace("\\", "/")


def test_ensure_smz_copies_local_to_share(tmp_path, monkeypatch):
    share = tmp_path / "share"
    share.mkdir()
    actor_sync = share / "actor_sync"
    actor_sync.mkdir()
    local = tmp_path / "local_state"
    local.mkdir()
    local_cfg = local / ACTOR_SYNC_SEARCH_CFG_NAME
    local_cfg.write_text(json.dumps(_valid_cfg()), encoding="utf-8")

    monkeypatch.setenv("40KAI_SHARE_ROOT", str(share))
    import project_paths as pp

    monkeypatch.setattr(pp, "RUNTIME_STATE_DIR", local)

    result = ensure_smz_remote_search_cfg(str(share))
    assert result.ok is True
    assert result.action == "copied"
    assert (actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME).is_file()


def test_ensure_smz_generates_from_share_snapshot(tmp_path, monkeypatch):
    from project_paths import TRAIN_DATA_PATH

    share = tmp_path / "share"
    actor_sync = share / "actor_sync"
    actor_sync.mkdir(parents=True)
    source = Path(TRAIN_DATA_PATH)
    if not source.is_file():
        pytest.skip("нет runtime/state/data.json для интеграционного теста")

    import core.models.smz_remote_search_cfg_builder as builder

    def _share_only_targets(**kwargs):
        extra = kwargs.get("extra_actor_sync")
        if extra:
            return [Path(extra) / ACTOR_SYNC_SEARCH_CFG_NAME]
        return []

    monkeypatch.setattr(builder, "_search_cfg_targets", _share_only_targets)
    builder.publish_smz_remote_search_cfg_from_repo(
        roster_path=source,
        sources=["test:snapshot"],
        extra_actor_sync=str(actor_sync),
        snapshot_actor_sync=str(actor_sync),
    )
    (actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME).unlink(missing_ok=True)

    result = ensure_smz_remote_search_cfg(str(share))
    assert result.ok is True
    assert result.action == "generated"
    assert (actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME).is_file()


def test_prepare_smz_inference_launch_sets_env(tmp_path):
    share = tmp_path / "share"
    actor_sync = share / "actor_sync"
    actor_sync.mkdir(parents=True)
    cfg_path = actor_sync / ACTOR_SYNC_SEARCH_CFG_NAME
    cfg_path.write_text(json.dumps(_valid_cfg()), encoding="utf-8")

    prep = prepare_smz_inference_launch(str(share))
    assert prep.ok is True
    env = dict(prep.env_extra)
    assert env["SMZ_REMOTE_SEARCH_CONFIG"] == str(cfg_path)
