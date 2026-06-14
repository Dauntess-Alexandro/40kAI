import numpy as np
import pytest
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import (
    SAMPLED_PRESETS,
    SampledMuZeroSearch,
    SampledMuZeroSearchConfig,
    make_sampled_search_config,
)


@pytest.mark.parametrize("preset", ["fast", "balanced", "heavy"])
def test_presets_make(preset):
    cfg = make_sampled_search_config(preset=preset)
    exp = SAMPLED_PRESETS[preset]
    assert cfg.num_samples == exp["num_samples"]
    assert cfg.temperature == exp["temperature"]
    assert cfg.prior_weight == exp["prior_weight"]


def test_config_defaults():
    cfg = SampledMuZeroSearchConfig()
    assert cfg.num_samples == 24
    assert cfg.sample_temperature == 1.0
    assert cfg.prior_weight == 0.0
    assert cfg.dedup is True


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16,
    )


def test_run_targets_sum_to_one_and_shapes():
    n_obs, n_actions = 12, [4, 3, 5]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=32), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [
        np.array([1, 1, 0, 1], dtype=bool),
        np.array([1, 0, 1], dtype=bool),
        np.array([1, 1, 1, 0, 0], dtype=bool),
    ]
    np.random.seed(0)
    pi, beh, actions, value = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert len(pi) == len(n_actions) == len(beh) == len(actions)
    for h, p in enumerate(pi):
        assert p.shape[0] == n_actions[h]
        assert abs(float(p.sum()) - 1.0) < 1e-5
        assert beh[h].shape[0] == n_actions[h]
    assert isinstance(value, float)


def test_run_illegal_zero_prob_and_legal_selection():
    n_obs, n_actions = 8, [5]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=64), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.array([True, False, False, True, False], dtype=bool)]
    np.random.seed(1)
    pi, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert pi[0][1] == 0.0 and pi[0][2] == 0.0 and pi[0][4] == 0.0
    assert legal[0][actions[0]]


def test_run_handles_empty_legal_head():
    n_obs, n_actions = 8, [3, 4]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=16), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.zeros(3, dtype=bool), np.ones(4, dtype=bool)]
    np.random.seed(2)
    pi, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert abs(float(pi[1].sum()) - 1.0) < 1e-5
    assert 0 <= actions[1] < 4


def test_joint_selection_matches_global_argmax_over_q():
    """С низкой температурой и достаточным K sampled-поиск выбирает joint-ход,
    совпадающий с argmax Q по ВСЕМ комбинациям (эталон полного перебора).
    Это и есть координация: выбор цельного хода, а не покомпонентный argmax."""
    import itertools

    import numpy as np
    import torch

    from core.models.gumbel_muzero_model import GumbelMuZeroNet
    from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig

    torch.manual_seed(0)
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[2, 2],
                          latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8)
    s = SampledMuZeroSearch(
        net=net,
        config=SampledMuZeroSearchConfig(num_samples=2000, temperature=0.02, prior_weight=0.0),
        device=torch.device("cpu"),
    )
    obs = np.zeros(8, dtype=np.float32)
    legal = [np.ones(2, dtype=bool), np.ones(2, dtype=bool)]
    np.random.seed(0)
    _, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)

    # Эталон: argmax Q по всем 4 joint-комбинациям
    lat = net.initial_inference(torch.zeros(1, 8))[3]
    joints = list(itertools.product([0, 1], [0, 1]))
    acts = torch.tensor(joints, dtype=torch.long)
    _p, val, rew, _nl = net.recurrent_inference(lat.expand(len(joints), -1), acts)
    q = (rew + 0.997 * val).detach().numpy().reshape(-1)
    best = joints[int(np.argmax(q))]
    assert tuple(actions) == best, f"selected {tuple(actions)} != global argmax {best}"
