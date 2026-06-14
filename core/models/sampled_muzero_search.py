from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch


@dataclass
class SampledMuZeroSearchConfig:
    num_samples: int = 24            # K joint-сэмплов из приора
    discount: float = 0.997
    temperature: float = 0.15        # τ улучшения политики
    sample_temperature: float = 1.0  # τ_s сэмплинга из приора (β)
    prior_weight: float = 0.0        # подмешивание приора в таргет (0 = несмещённо)
    dedup: bool = True
    tree_reuse: bool = False         # v1: без warm-start (depth-1, свежие сэмплы)


SAMPLED_PRESETS: dict[str, dict] = {
    "fast":     {"num_samples": 12, "temperature": 0.20, "sample_temperature": 1.0, "prior_weight": 0.0},
    "balanced": {"num_samples": 24, "temperature": 0.15, "sample_temperature": 1.0, "prior_weight": 0.0},
    "heavy":    {"num_samples": 48, "temperature": 0.10, "sample_temperature": 1.0, "prior_weight": 0.0},
}


def make_sampled_search_config(preset: str = "balanced", **overrides) -> SampledMuZeroSearchConfig:
    kwargs = SAMPLED_PRESETS.get(preset, SAMPLED_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return SampledMuZeroSearchConfig(**kwargs)


def _beta_heads_from_logits(root_logits, legal_masks_by_head, tau_s):
    """Возвращает (behavior_logits, beta_heads, legal_list). beta_heads — полноразмерные
    вероятности сэмплинга (0 на нелегальных), beh — сырые root-логиты (для V-trace)."""
    behavior_logits, beta_heads, legal_list = [], [], []
    for h, head_logits in enumerate(root_logits):
        logits_np = head_logits.squeeze(0).detach().cpu().numpy().astype(np.float32)
        behavior_logits.append(logits_np.copy())
        legal = np.asarray(legal_masks_by_head[h], dtype=bool)
        legal_list.append(legal)
        beta = np.zeros_like(logits_np, dtype=np.float64)
        idx = np.where(legal)[0]
        if idx.size > 0:
            x = logits_np[idx].astype(np.float64) / max(1e-6, float(tau_s))
            x = x - x.max()
            e = np.exp(x)
            beta[idx] = e / e.sum()
        beta_heads.append(beta)
    return behavior_logits, beta_heads, legal_list


def _sample_joint(beta_heads, legal_list, K):
    """Сэмплинг K joint-действий. RNG-порядок: sample-major, head-minor.
    Головы без легальных действий не тянут RNG (action=0)."""
    H = len(beta_heads)
    samples = np.zeros((K, H), dtype=np.int64)
    for k in range(K):
        for h in range(H):
            idx = np.where(legal_list[h])[0]
            if idx.size == 0:
                samples[k, h] = 0
            else:
                samples[k, h] = int(np.random.choice(idx, p=beta_heads[h][idx]))
    return samples


def _improved_joint_policy(q, counts, tau):
    """π̂(a) ∝ count(a)·exp((Q−maxQ)/τ)."""
    adv = (q - q.max()) / max(1e-6, float(tau))
    w = counts.astype(np.float64) * np.exp(adv)
    s = w.sum()
    if s > 1e-12:
        return w / s
    return counts.astype(np.float64) / counts.sum()


def _marginalize(uniq, pi_joint, beta_heads, legal_list, behavior_logits, prior_weight):
    """Маргинализация joint-политики в головы (+опц. prior-mix), с занулением нелегальных."""
    H = len(behavior_logits)
    out = []
    for h in range(H):
        size = int(behavior_logits[h].shape[0])
        tgt = np.zeros(size, dtype=np.float64)
        for u in range(uniq.shape[0]):
            tgt[uniq[u, h]] += pi_joint[u]
        if prior_weight > 0.0:
            tgt = (1.0 - prior_weight) * tgt + prior_weight * beta_heads[h]
        tgt[~legal_list[h]] = 0.0
        s = tgt.sum()
        if s > 1e-12:
            tgt = tgt / s
        else:
            lg = legal_list[h]
            tgt = lg.astype(np.float64) / max(1.0, float(lg.sum()))
        out.append(tgt.astype(np.float32))
    return out


class SampledMuZeroSearch:
    """Depth-1 sampled search: K joint-сэмплов из факторизованного приора, IS-улучшенная
    joint-политика, маргинализация в головы. Сигнатура run совпадает с GumbelMuZeroSearch."""

    def __init__(self, net, config: SampledMuZeroSearchConfig | None = None,
                 device: torch.device | None = None):
        self.net = net
        self.cfg = config or SampledMuZeroSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}

    def clear_tree_state(self) -> None:
        # v1: без tree-reuse; метод для API-паритета с gmz.
        return None

    @torch.no_grad()
    def run(self, *, obs: np.ndarray, legal_masks_by_head: list[np.ndarray],
            deterministic: bool = True):
        cfg, device = self.cfg, self.device
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=device).unsqueeze(0)
                   for m in legal_masks_by_head]
        root_logits, root_value, _r, latent = self.net.initial_inference(obs_t, masks_by_head=masks_t)

        K = max(1, int(cfg.num_samples))
        tau_s = float(cfg.sample_temperature)
        behavior_logits, beta_heads, legal_list = _beta_heads_from_logits(
            root_logits, legal_masks_by_head, tau_s
        )

        samples = _sample_joint(beta_heads, legal_list, K)
        if bool(cfg.dedup):
            uniq, counts = np.unique(samples, axis=0, return_counts=True)
        else:
            uniq, counts = samples, np.ones(samples.shape[0], dtype=np.int64)
        U = uniq.shape[0]

        latent_batch = latent.expand(U, -1)
        action_t = torch.as_tensor(uniq, dtype=torch.long, device=device)
        _p, val_b, rew_b, _nl = self.net.recurrent_inference(latent_batch, action_t, masks_by_head=None)
        val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
        rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
        q = rew_b + float(cfg.discount) * val_b

        pi_joint = _improved_joint_policy(q, counts, float(cfg.temperature))

        if deterministic:
            sel = int(np.argmax(pi_joint))
        else:
            sel = int(np.random.choice(np.arange(U), p=pi_joint))
        selected_actions = [int(x) for x in uniq[sel]]

        policy_targets = _marginalize(
            uniq, pi_joint, beta_heads, legal_list, behavior_logits, float(cfg.prior_weight)
        )

        value_out = float(np.average(q, weights=counts))
        self.last_run_stats = {
            "num_samples": float(K), "unique_samples": float(U),
            "root_value": float(root_value.item()), "q_mean": value_out,
        }
        return policy_targets, behavior_logits, selected_actions, value_out
