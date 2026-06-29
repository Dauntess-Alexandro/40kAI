# tests/models/test_phoenix_config.py
from core.models.phoenix_config import resolve_phoenix_config


def test_defaults_when_no_hp_no_env():
    cfg = resolve_phoenix_config(None, {})
    assert cfg.replay_ratio == 2
    assert cfg.reset_interval == 40000
    assert cfg.gamma_start == 0.97 and cfg.gamma_end == 0.99
    assert cfg.nstep_start == 10 and cfg.nstep_end == 3
    assert cfg.noisy is False
    assert cfg.ve_steve is False
    assert cfg.spr_horizon_K == 5 and cfg.ve_horizon == 3
    assert cfg.num_actors == 1
    assert cfg.batch_size == 32 and cfg.replay_min_size == 256
    assert cfg.actor_batch_send == 32 and cfg.actor_queue_max == 256
    assert cfg.distributed_actors_enabled is False
    assert cfg.distributed_rollout_port == 5562
    assert cfg.dist_max_windows_per_msg == 64
    assert cfg.ve_latent_bootstrap is False
    assert cfg.iqn_kappa == 1.0


def test_section_overrides_default():
    cfg = resolve_phoenix_config({"phoenix": {"replay_ratio": 8, "shrink_alpha": 0.4}}, {})
    assert cfg.replay_ratio == 8
    assert abs(cfg.shrink_alpha - 0.4) < 1e-9


def test_env_overrides_section():
    hp = {"phoenix": {"replay_ratio": 8}}
    env = {"PHOENIX_REPLAY_RATIO": "16", "PHOENIX_VE_STEVE": "1"}
    cfg = resolve_phoenix_config(hp, env)
    assert cfg.replay_ratio == 16
    assert cfg.ve_steve is True


def test_actor_and_dist_fields_resolve_from_section_and_env():
    hp = {
        "phoenix": {
            "num_actors": 4,
            "actor_batch_send": 12,
            "actor_queue_max": 300,
            "distributed_actors_enabled": 1,
            "distributed_rollout_port": 5570,
            "distributed_auth_token": "secret",
            "distributed_local_episode_fraction": 0.6,
            "distributed_pc2_num_workers": 6,
            "ve_latent_bootstrap": 1,
        }
    }
    env = {
        "PHOENIX_NUM_ACTORS": "8",
        "PHOENIX_DIST_ROLLOUT_PORT": "5562",
        "PHOENIX_IQN_KAPPA": "0.5",
    }
    cfg = resolve_phoenix_config(hp, env)
    assert cfg.num_actors == 8
    assert cfg.actor_batch_send == 12
    assert cfg.actor_queue_max == 300
    assert cfg.distributed_actors_enabled is True
    assert cfg.distributed_rollout_port == 5562
    assert cfg.distributed_auth_token == "secret"
    assert abs(cfg.distributed_local_episode_fraction - 0.6) < 1e-9
    assert cfg.distributed_pc2_num_workers == 6
    assert cfg.ve_latent_bootstrap is True
    assert cfg.iqn_kappa == 0.5


def test_num_actors_falls_back_to_legacy_num_actors_env():
    cfg = resolve_phoenix_config({"phoenix": {"num_actors": 2}}, {"NUM_ACTORS": "5"})
    assert cfg.num_actors == 5


def test_gui_defaults_expose_runtime_keys():
    from app.gui_qt.phoenix_hyperparams_defaults import DEFAULT_PHOENIX_HYPERPARAMS, PHOENIX_HYPERPARAM_KEYS

    for key in (
        "num_actors",
        "batch_size",
        "replay_min_size",
        "actor_batch_send",
        "actor_queue_max",
        "distributed_actors_enabled",
        "distributed_rollout_port",
        "dist_max_windows_per_msg",
        "ve_latent_bootstrap",
        "iqn_kappa",
    ):
        assert key in PHOENIX_HYPERPARAM_KEYS
        assert key in DEFAULT_PHOENIX_HYPERPARAMS
