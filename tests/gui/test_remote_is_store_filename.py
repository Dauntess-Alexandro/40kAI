from app.gui_qt.remote_is_store import (
    load_remote_is,
    remote_is_config_path,
    save_remote_is,
)


def test_filename_param_roundtrip_smz(tmp_path):
    data = {"user_enabled_lan": True, "host": "192.168.1.50", "port": 5560, "auth_token": "tok"}
    save_remote_is(tmp_path, data, filename="remote_is_smz.json")
    assert (tmp_path / "runtime" / "state" / "remote_is_smz.json").is_file()
    loaded = load_remote_is(tmp_path, filename="remote_is_smz.json")
    assert loaded["host"] == "192.168.1.50"
    assert loaded["port"] == 5560
    assert loaded["user_enabled_lan"] is True
    assert loaded["enabled"] is True


def test_gmz_default_filename_unchanged(tmp_path):
    save_remote_is(tmp_path, {"user_enabled_lan": True, "host": "10.0.0.1"})
    assert (tmp_path / "runtime" / "state" / "remote_is.json").is_file()
    assert not (tmp_path / "runtime" / "state" / "remote_is_smz.json").is_file()
    assert load_remote_is(tmp_path)["host"] == "10.0.0.1"
    assert remote_is_config_path(tmp_path).name == "remote_is.json"


def test_config_path_filename(tmp_path):
    assert remote_is_config_path(tmp_path, filename="remote_is_smz.json").name == "remote_is_smz.json"
