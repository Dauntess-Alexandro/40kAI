import json
import types

import torch

from core.models.muzero_stratagem_bridge import install_worker_reaction_value_net
from core.models.muzero_value_net_builder import build_gmz_net_from_search_cfg

_CFG = {"obs_dim": 8, "action_sizes": [3, 2], "latent_dim": 16,
        "hidden_dim": 16, "num_layers": 1, "action_embed_dim": 4}


def _assets(tmp_path):
    (tmp_path / "gmz_remote_search_cfg.json").write_text(json.dumps(_CFG), encoding="utf-8")
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    torch.save(net.state_dict(), str(tmp_path / "latest_gmz_policy.pth"))


def _env():
    e = types.SimpleNamespace()
    e.unwrapped = e
    return e


def _install(tmp_path):
    return install_worker_reaction_value_net(
        _env(),
        assets_dir=str(tmp_path),
        cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY",
        log_tag="GMZ",
    )


def test_install_worker_reaction_net_ok(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    _assets(tmp_path)
    env = _env()
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is not None
    assert callable(env.reaction_policy)


def test_install_worker_reaction_net_missing_assets(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _env()  # каталог пуст
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is None
    assert getattr(env, "reaction_policy", None) is None


def test_install_worker_reaction_net_flag_off(tmp_path, monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    _assets(tmp_path)
    env = _env()
    net = install_worker_reaction_value_net(
        env, assets_dir=str(tmp_path), cfg_name="gmz_remote_search_cfg.json",
        weights_name="latest_gmz_policy.pth",
        build_net_fn=build_gmz_net_from_search_cfg,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert net is None
    assert getattr(env, "reaction_policy", None) is None
