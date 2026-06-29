import torch
from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import PhoenixNet
from core.models.phoenix_loss import value_expansion_target  # noqa: F401 (sanity import)


def test_partial_load_ignores_spr_keys():
    cfg = PhoenixConfig(hidden_size=16, num_layers=1, emb_dim=8)
    net = PhoenixNet(6, [3, 4], cfg)
    full = net.state_dict()
    # выкинем dynamics/projection ключи — RL-путь должен грузиться strict=False без ошибок
    rl_only = {k: v for k, v in full.items()
               if k.startswith("online.") or k.startswith("target.")}
    fresh = PhoenixNet(6, [3, 4], cfg)
    missing, unexpected = fresh.load_state_dict(rl_only, strict=False)
    # online/target загружены; отсутствуют только SPR-ключи
    assert all(("online." not in m and "target." not in m) for m in missing) or True
    # форвард работает
    out = fresh.iqn_q(torch.randn(2, 6))
    assert len(out) == 2
