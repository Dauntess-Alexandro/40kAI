from app.gui_qt.phoenix_hyperparams_defaults import DEFAULT_PHOENIX_HYPERPARAMS, PHOENIX_HYPERPARAM_KEYS


def test_phoenix_actor_dist_defaults_present():
    assert int(DEFAULT_PHOENIX_HYPERPARAMS["num_actors"]) == 1
    assert int(DEFAULT_PHOENIX_HYPERPARAMS["distributed_rollout_port"]) == 5562
    for key in (
        "num_actors",
        "actor_batch_send",
        "actor_queue_max",
        "distributed_actors_enabled",
        "distributed_pc2_num_workers",
        "dist_max_windows_per_msg",
    ):
        assert key in PHOENIX_HYPERPARAM_KEYS


def test_load_phoenix_section_preserves_auth_and_host():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    payload = {
        "phoenix": {
            "distributed_bind_host": "0.0.0.0",
            "distributed_auth_token": "SecretCase",
            "num_actors": "8",
        }
    }
    loaded = ctrl._load_algo_hyperparams_section(
        payload, "phoenix", dict(DEFAULT_PHOENIX_HYPERPARAMS), PHOENIX_HYPERPARAM_KEYS
    )
    assert loaded["distributed_bind_host"] == "0.0.0.0"
    assert loaded["distributed_auth_token"] == "SecretCase"
    assert int(loaded["num_actors"]) == 8


def test_validate_phoenix_actor_fields():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    hp = dict(DEFAULT_PHOENIX_HYPERPARAMS)
    assert ctrl._validate_phoenix_hyperparams(hp) is None
    hp["num_actors"] = 0
    assert "num_actors" in ctrl._validate_phoenix_hyperparams(hp)
