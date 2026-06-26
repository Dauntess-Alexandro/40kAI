"""Bootstrap init-weights для AZ remote IS: формы из search_cfg, формат как у learner/сервера."""
import json

import pytest
import torch

from core.models.alphazero_model import (
    load_alphazero_state_dict,
    make_alphazero_net,
    write_az_init_weights_from_cfg,
)

_CFG = {
    "obs_dim": 8,
    "action_sizes": [3, 2],
    "hidden_size": 16,
    "num_layers": 1,
    "n_value_ensemble": 1,
}


def _build_net():
    return make_alphazero_net(
        n_observations=_CFG["obs_dim"],
        n_actions=_CFG["action_sizes"],
        hidden_size=_CFG["hidden_size"],
        num_layers=_CFG["num_layers"],
        n_value_ensemble=_CFG["n_value_ensemble"],
    )


def test_write_az_init_weights_roundtrip(tmp_path):
    cfg_path = tmp_path / "az_remote_search_cfg.json"
    cfg_path.write_text(json.dumps(_CFG), encoding="utf-8")
    out = tmp_path / "latest_az_tree_policy.pth"

    p = write_az_init_weights_from_cfg(str(cfg_path), str(out))

    # Формат как у learner/сервера: обёртка {"state_dict": ...} + policy_version (читает _poll_weights).
    payload = torch.load(p, map_location="cpu", weights_only=False)
    assert isinstance(payload, dict)
    assert "state_dict" in payload
    assert int(payload.get("policy_version", -1)) == 0

    # Сервер строит net из cfg и грузит state_dict — формы должны совпасть (нет missing/unexpected).
    net = _build_net()
    missing, unexpected = load_alphazero_state_dict(net, payload["state_dict"], log_fn=None)
    assert list(missing) == []
    assert list(unexpected) == []


def test_write_az_init_weights_raises_on_bad_cfg(tmp_path):
    cfg_path = tmp_path / "bad.json"
    cfg_path.write_text(json.dumps({"obs_dim": 0, "action_sizes": []}), encoding="utf-8")
    out = tmp_path / "w.pth"
    with pytest.raises(ValueError):
        write_az_init_weights_from_cfg(str(cfg_path), str(out))


def _load_cli_tool():
    import importlib.util
    from pathlib import Path

    p = Path(__file__).resolve().parents[2] / "tools" / "write_az_init_weights.py"
    spec = importlib.util.spec_from_file_location("write_az_init_weights", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_derive_paths_az_and_gaz():
    """AZ-семья на общей сети: один инструмент, имена файлов различаются по --algo."""
    import os

    mod = _load_cli_tool()
    share = os.path.join("X:", os.sep)  # без actor_sync на диске → фолбэк на корень шары

    cfg_az, w_az = mod._derive_paths(share, "az")
    assert cfg_az.endswith("az_remote_search_cfg.json")
    assert w_az.endswith("latest_az_tree_policy.pth")

    cfg_gaz, w_gaz = mod._derive_paths(share, "gaz")
    assert cfg_gaz.endswith("gaz_remote_search_cfg.json")
    assert w_gaz.endswith("latest_az_gumbel_az_policy.pth")
