"""GUI: загрузка alphazero_tree hyperparams с LAN host (строки, не float)."""

from __future__ import annotations

from app.gui_qt.az_hyperparams_defaults import DEFAULT_AZ_TREE_HYPERPARAMS


def test_load_az_section_preserves_remote_host_ip():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    payload = {
        "alphazero_tree": {
            "inference_remote_host": "192.168.0.105",
            "inference_server_mode": "remote",
            "inference_server_enabled": 1,
        }
    }
    loaded = ctrl._load_az_hyperparams_section(payload, "alphazero_tree", dict(DEFAULT_AZ_TREE_HYPERPARAMS))
    assert loaded["inference_remote_host"] == "192.168.0.105"
    assert loaded["inference_server_mode"] == "remote"
    assert int(loaded["inference_server_enabled"]) == 1
