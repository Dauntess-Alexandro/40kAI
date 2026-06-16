import types

from app.gui_qt.main import GUIController


def _stub(algo, remote_is_smz):
    # Call method as unbound function with a stub — no QApplication needed.
    return types.SimpleNamespace(_training_algo=algo, _remote_is_smz=remote_is_smz)


def test_smz_cfg_returned_when_lan_active():
    stub = _stub("sampled_muzero", {
        "user_enabled_lan": True, "host": "192.168.0.101",
        "port": 5560, "auth_token": "",
    })
    cfg = GUIController._smz_remote_cfg_for_telemetry(stub)
    assert cfg == {
        "host": "192.168.0.101", "port": 5560,
        "auth_token": "", "transport": "gmz",
    }


def test_smz_cfg_none_when_lan_off():
    stub = _stub("sampled_muzero", {"user_enabled_lan": False, "host": "192.168.0.101", "port": 5560})
    assert GUIController._smz_remote_cfg_for_telemetry(stub) is None


def test_smz_cfg_none_for_other_algo():
    stub = _stub("gumbel_muzero", {"user_enabled_lan": True, "host": "192.168.0.101", "port": 5560})
    assert GUIController._smz_remote_cfg_for_telemetry(stub) is None
