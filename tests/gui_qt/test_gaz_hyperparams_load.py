from app.gui_qt.gaz_hyperparams_defaults import DEFAULT_GAZ_HYPERPARAMS, GAZ_HYPERPARAM_KEYS


def test_load_gaz_section_preserves_remote_host_ip():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    payload = {
        "gumbel_az": {
            "inference_remote_host": "192.168.0.105",
            "inference_server_mode": "remote",
            "num_simulations": 64,
        }
    }
    loaded = ctrl._load_algo_hyperparams_section(
        payload, "gumbel_az", dict(DEFAULT_GAZ_HYPERPARAMS), GAZ_HYPERPARAM_KEYS
    )
    assert loaded["inference_remote_host"] == "192.168.0.105"
    assert loaded["inference_server_mode"] == "remote"
    assert int(loaded["num_simulations"]) == 64


def test_load_gaz_section_coerces_and_falls_back():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    payload = {"gumbel_az": {"num_considered_actions": "16", "value_scale": "not-a-number"}}
    loaded = ctrl._load_algo_hyperparams_section(
        payload, "gumbel_az", dict(DEFAULT_GAZ_HYPERPARAMS), GAZ_HYPERPARAM_KEYS
    )
    # строковый int приводится
    assert int(loaded["num_considered_actions"]) == 16
    # битое значение откатывается к дефолту
    assert float(loaded["value_scale"]) == float(DEFAULT_GAZ_HYPERPARAMS["value_scale"])


def test_gaz_in_training_algo_options():
    from app.gui_qt.main import GUIController

    ctrl = GUIController.__new__(GUIController)
    ctrl._training_algo_options = [
        "dqn",
        "ppo",
        "alphazero_tree",
        "alphazero_proxy",
        "gumbel_muzero",
        "gumbel_az",
    ]
    assert "gumbel_az" in ctrl._training_algo_options
    assert ctrl._format_algo_label("gumbel_az") == "GUMBEL ALPHAZERO"
