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
    # RL-путь (online/target) реально загружен → его ключей нет в missing
    assert not any(m.startswith("online.") for m in missing)
    assert not any(m.startswith("target.") for m in missing)
    # отсутствуют только SPR/dynamics-ключи (обвязка обучения)
    assert all(
        m.startswith(("projector.", "predictor.", "dynamics.", "action_embed.", "target_projector."))
        for m in missing
    )
    # лишних ключей при strict=False быть не должно
    assert unexpected == []
    # форвард работает
    out = fresh.iqn_q(torch.randn(2, 6))
    assert len(out) == 2
