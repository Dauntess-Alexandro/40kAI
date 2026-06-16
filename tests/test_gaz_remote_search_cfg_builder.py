"""Тесты GAZ remote search_cfg builder + GAZ-spec в реестре.

GAZ использует ту же сеть AlphaZeroPolicyValueNet, что и AZ → форма search_cfg
идентична AZ; отличаются только имена файлов (веса latest_az_gumbel_az_policy.pth,
cfg gaz_remote_search_cfg.json) и секция гиперпараметров (gumbel_az).
"""

from __future__ import annotations

import json

from core.models.gaz_remote_search_cfg_builder import (
    SEARCH_CFG_NAME,
    WEIGHTS_NAME,
    resolve_gaz_smb_paths,
)
from core.models.remote_is_search_cfg_registry import (
    prepare_inference_launch,
    spec_for_pc2_role,
)


def test_gaz_filenames():
    assert SEARCH_CFG_NAME == "gaz_remote_search_cfg.json"
    assert WEIGHTS_NAME == "latest_az_gumbel_az_policy.pth"


def test_resolve_gaz_smb_paths(tmp_path):
    paths = resolve_gaz_smb_paths(str(tmp_path))
    assert paths.search_cfg_path.endswith("gaz_remote_search_cfg.json")
    assert paths.weights_path.endswith("latest_az_gumbel_az_policy.pth")


def test_registry_has_gaz_spec():
    spec = spec_for_pc2_role("gaz_inference")
    assert spec is not None
    assert spec.algo_id == "gaz"
    assert spec.env_search_key == "GAZ_REMOTE_SEARCH_CONFIG"
    assert spec.env_weights_key == "GAZ_REMOTE_WEIGHTS_PATH"
    assert spec.weights_filename == "latest_az_gumbel_az_policy.pth"


def test_prepare_gaz_with_existing_cfg(tmp_path):
    actor_sync = tmp_path / "actor_sync"
    actor_sync.mkdir()
    cfg = {
        "obs_dim": 17,
        "action_sizes": [5, 2, 2, 2, 5, 2, 24, 24],
        "hidden_size": 256,
        "num_layers": 2,
        "n_value_ensemble": 1,
        "num_simulations": 32,
    }
    (actor_sync / "gaz_remote_search_cfg.json").write_text(json.dumps(cfg), encoding="utf-8")
    prep = prepare_inference_launch("gaz_inference", str(tmp_path))
    assert prep.ok is True
    env = dict(prep.env_extra)
    assert "GAZ_REMOTE_SEARCH_CONFIG" in env
    assert "GAZ_REMOTE_WEIGHTS_PATH" in env
