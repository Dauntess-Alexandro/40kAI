import itertools

import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig


def _exact_marginal_targets(net, obs, legal, tau, tau_s):
    """Точный оператор улучшения: перебор всех joint-действий."""
    device = torch.device("cpu")
    obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
    masks_t = [torch.as_tensor(m, dtype=torch.bool, device=device).unsqueeze(0) for m in legal]
    root_logits, _v, _r, latent = net.initial_inference(obs_t, masks_by_head=masks_t)
    H = len(legal)
    beta = []
    legal_idx = []
    for h in range(H):
        lg = np.asarray(legal[h], dtype=bool)
        idx = np.where(lg)[0]
        legal_idx.append(idx)
        lo = root_logits[h].squeeze(0).detach().cpu().numpy().astype(np.float64)[idx] / tau_s
        lo = lo - lo.max()
        e = np.exp(lo)
        b = np.zeros(lg.shape[0], dtype=np.float64)
        b[idx] = e / e.sum()
        beta.append(b)
    joints = list(itertools.product(*[list(ix) for ix in legal_idx]))
    acts = torch.tensor(joints, dtype=torch.long, device=device)
    lat = latent.expand(len(joints), -1)
    _p, val, rew, _nl = net.recurrent_inference(lat, acts, masks_by_head=None)
    q = (rew.detach().cpu().numpy().reshape(-1).astype(np.float64)
         + 0.997 * val.detach().cpu().numpy().reshape(-1).astype(np.float64))
    bj = np.array([np.prod([beta[h][j[h]] for h in range(H)]) for j in joints], dtype=np.float64)
    w = bj * np.exp((q - q.max()) / tau)
    w = w / w.sum()
    targets = [np.zeros(legal[h].shape[0], dtype=np.float64) for h in range(H)]
    for wi, j in zip(w, joints):
        for h in range(H):
            targets[h][j[h]] += wi
    return [t / t.sum() for t in targets]


def test_sampled_target_matches_exact_enumeration():
    torch.manual_seed(0)
    n_obs, n_actions = 10, [2, 3]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions,
                          latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16)
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.ones(2, dtype=bool), np.ones(3, dtype=bool)]
    tau, tau_s = 0.15, 1.0

    exact = _exact_marginal_targets(net, obs, legal, tau, tau_s)

    s = SampledMuZeroSearch(
        net=net,
        config=SampledMuZeroSearchConfig(num_samples=40000, temperature=tau,
                                         sample_temperature=tau_s, prior_weight=0.0),
        device=torch.device("cpu"),
    )
    np.random.seed(123)
    pi, _, _, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)

    for h in range(len(n_actions)):
        np.testing.assert_allclose(pi[h], exact[h], atol=0.02,
                                   err_msg=f"head {h}: sampled target != exact")
