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


@torch.no_grad()
def run_batched(*, net, cfg: SampledMuZeroSearchConfig, device: torch.device,
                requests: list[dict], deterministic: bool = False) -> list[dict]:
    """Батч по средам. RNG-порядок строго env-major → sample-major → head-minor,
    чтобы при общем seed совпадать с последовательным run() по средам."""
    N = len(requests)
    if N == 0:
        return []
    K = max(1, int(cfg.num_samples))
    tau_s = float(cfg.sample_temperature)
    num_heads = len(requests[0]["legal_masks_by_head"])

    obs_batch = torch.tensor(
        np.stack([np.asarray(r["obs"], dtype=np.float32) for r in requests], axis=0), device=device)
    masks_batch = []
    for h in range(num_heads):
        mh = np.stack([np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool) for n in range(N)], axis=0)
        masks_batch.append(torch.as_tensor(mh, dtype=torch.bool, device=device))
    root_logits, root_value, _r, latent = net.initial_inference(obs_batch, masks_by_head=masks_batch)
    root_value_np = root_value.detach().cpu().numpy().reshape(-1).astype(np.float64)

    per_env = []
    rows_action, env_of_row = [], []
    for n in range(N):
        rl_n = [root_logits[h][n:n + 1] for h in range(num_heads)]
        beh, beta_heads, legal_list = _beta_heads_from_logits(
            rl_n, requests[n]["legal_masks_by_head"], tau_s)
        samples = _sample_joint(beta_heads, legal_list, K)
        if bool(cfg.dedup):
            uniq, counts = np.unique(samples, axis=0, return_counts=True)
        else:
            uniq, counts = samples, np.ones(samples.shape[0], dtype=np.int64)
        per_env.append((uniq, counts, beh, beta_heads, legal_list))
        for u in range(uniq.shape[0]):
            rows_action.append(uniq[u])
            env_of_row.append(n)

    idx_t = torch.tensor(env_of_row, dtype=torch.long, device=device)
    latent_rep = latent.index_select(0, idx_t)
    action_t = torch.as_tensor(np.asarray(rows_action), dtype=torch.long, device=device)
    _p, val_b, rew_b, _nl = net.recurrent_inference(latent_rep, action_t, masks_by_head=None)
    val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
    rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
    q_all = rew_b + float(cfg.discount) * val_b

    results, cursor = [], 0
    for n in range(N):
        uniq, counts, beh, beta_heads, legal_list = per_env[n]
        U = uniq.shape[0]
        q = q_all[cursor:cursor + U]
        cursor += U
        pi_joint = _improved_joint_policy(q, counts, float(cfg.temperature))
        if deterministic:
            sel = int(np.argmax(pi_joint))
        else:
            sel = int(np.random.choice(np.arange(U), p=pi_joint))
        selected = [int(x) for x in uniq[sel]]
        policy_targets = _marginalize(uniq, pi_joint, beta_heads, legal_list, beh, float(cfg.prior_weight))
        value_out = float(np.average(q, weights=counts)) if U > 0 else float(root_value_np[n])
        results.append({
            "env_id": int(requests[n].get("env_id", n)),
            "selected_actions": selected,
            "policy_targets": policy_targets,
            "behavior_logits": beh,
            "value_est": value_out,
        })
    return results


class BatchedSampledMuZeroSearch:
    """Обёртка над run_batched (для паритета с gmz). v1: без tree-reuse."""

    def __init__(self, *, net, config: SampledMuZeroSearchConfig, device: torch.device):
        self.net, self.cfg, self.device = net, config, device

    def clear_tree_state(self, env_id: int | None = None) -> None:
        return None

    def run_batched_stateful(self, requests: list[dict], deterministic: bool = False) -> list[dict]:
        return run_batched(net=self.net, cfg=self.cfg, device=self.device,
                           requests=requests, deterministic=deterministic)
