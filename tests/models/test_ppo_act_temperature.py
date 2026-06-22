"""PPO eval: act() поддерживает temperature (вариант 1: PPO→temperature).

- deterministic=True: temperature не влияет на argmax (детерминированный выбор стабилен).
- deterministic=False + низкая temperature: сэмпл концентрируется на argmax-действии.
- высокая temperature: сэмпл становится разнообразнее.
"""
import torch

from core.models.PPO import make_actor_critic


def _build_net(n_obs=12, n_actions=(5, 2, 3)):
    net = make_actor_critic(n_obs, list(n_actions), hidden_size=32, num_layers=2, n_value_ensemble=1)
    net.eval()
    return net


def test_act_temperature_does_not_change_greedy():
    net = _build_net()
    obs = torch.randn(1, 12)
    a_lo, _, _ = net.act(obs, deterministic=True, temperature=0.05)
    a_hi, _, _ = net.act(obs, deterministic=True, temperature=2.0)
    assert torch.equal(a_lo, a_hi)


def test_act_low_temperature_matches_greedy():
    net = _build_net()
    obs = torch.randn(1, 12)
    greedy, _, _ = net.act(obs, deterministic=True)
    torch.manual_seed(0)
    # Очень низкая температура ⇒ сэмпл практически всегда = argmax.
    matches = 0
    for _ in range(20):
        sampled, _, _ = net.act(obs, deterministic=False, temperature=0.01)
        if torch.equal(sampled, greedy):
            matches += 1
    assert matches >= 19


def test_act_high_temperature_is_more_diverse():
    net = _build_net()
    obs = torch.randn(1, 12)
    torch.manual_seed(0)
    seen = set()
    for _ in range(40):
        sampled, _, _ = net.act(obs, deterministic=False, temperature=2.0)
        seen.add(tuple(sampled.squeeze(0).tolist()))
    # При высокой температуре ожидаем более одного уникального действия.
    assert len(seen) > 1
