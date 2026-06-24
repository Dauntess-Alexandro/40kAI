import torch

from core.models.muzero_value_net_builder import (
    build_gmz_net_from_search_cfg,
    build_smz_net_from_search_cfg,
    load_value_net_weights,
)

_CFG = {
    "obs_dim": 8,
    "action_sizes": [3, 2],
    "latent_dim": 16,
    "hidden_dim": 16,
    "num_layers": 1,
    "action_embed_dim": 4,
}


def test_build_gmz_net_infers_value():
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    policy, value = net.infer(torch.zeros(1, 8), masks_by_head=None)
    assert float(value.reshape(-1)[0]) == float(value.reshape(-1)[0])  # структура: не падает, число


def test_build_smz_net_infers_value():
    net = build_smz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    policy, value = net.infer(torch.zeros(1, 8), masks_by_head=None)
    assert value.reshape(-1).shape[0] >= 1


def test_build_raises_on_empty_cfg():
    import pytest

    with pytest.raises(ValueError):
        build_gmz_net_from_search_cfg({}, device=torch.device("cpu"))


def test_load_value_net_weights_roundtrip(tmp_path):
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    p = tmp_path / "w.pth"
    torch.save(net.state_dict(), str(p))
    net2 = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    assert load_value_net_weights(net2, str(p)) is True


def test_load_value_net_weights_missing_returns_false():
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    assert load_value_net_weights(net, "no_such_file.pth") is False


def test_write_init_weights_from_cfg_roundtrip(tmp_path):
    import json

    from core.models.muzero_value_net_builder import write_init_weights_from_cfg

    cfg_path = tmp_path / "gmz_remote_search_cfg.json"
    cfg_path.write_text(json.dumps(_CFG), encoding="utf-8")
    out = tmp_path / "latest_gmz_policy.pth"
    p = write_init_weights_from_cfg(str(cfg_path), str(out), algo="gmz")
    net = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    assert load_value_net_weights(net, p) is True
    # формат должен совпадать с тем, что ждёт сервер/learner: обёртка {"state_dict": ...}
    payload = torch.load(p, map_location="cpu")
    assert isinstance(payload, dict) and "state_dict" in payload
    net2 = build_gmz_net_from_search_cfg(_CFG, device=torch.device("cpu"))
    net2.load_state_dict(payload["state_dict"], strict=False)  # сервер-стиль (payload.get("state_dict"))
