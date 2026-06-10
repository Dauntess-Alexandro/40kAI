import math
import os

import torch


def dqn_kwargs_from_env():
    """Shared DQN constructor kwargs from environment variables."""
    return {
        "hidden_size": int(os.getenv("DQN_HIDDEN_SIZE", "256")),
        "num_layers": int(os.getenv("DQN_NUM_LAYERS", "2")),
        "n_ensemble": int(os.getenv("DQN_ENSEMBLE_SIZE", "1")),
        "noisy_sigma0": float(os.getenv("NOISY_SIGMA0", "0.5")),
        "iqn_num_quantiles": int(os.getenv("IQN_N_QUANTILES", "32")),
        "iqn_num_target_quantiles": int(os.getenv("IQN_N_TARGET_QUANTILES", "32")),
        "iqn_num_tau_samples": int(os.getenv("IQN_N_TAU_SAMPLES", "32")),
        "iqn_embed_dim": int(os.getenv("IQN_EMBED_DIM", "64")),
    }


def make_dqn(n_observations, n_actions, dueling=False, noisy=True, distributional="iqn", **overrides):
    kwargs = dqn_kwargs_from_env()
    kwargs.update(
        {
            "dueling": bool(dueling),
            "noisy": bool(noisy),
            "distributional": str(distributional or os.getenv("DIST_TYPE", "iqn")).strip().lower() or "iqn",
        }
    )
    kwargs.update(overrides)
    return DQN(n_observations, n_actions, **kwargs)


def infer_dqn_arch_from_state_dict(state_dict) -> dict:
    """Восстановить арх-параметры сети из её state_dict.

    Нужно, чтобы загрузить чужой чекпойнт (например DQN-оппонента для AZ) без
    знания исходного конфига: иначе ensemble/dueling/слои не совпадут и
    load_state_dict упадёт. Меты с арх-параметрами у агента может не быть.
    """
    import re

    keys = list(state_dict.keys())

    def _count_prefix(pattern: str) -> int:
        idx = set()
        for k in keys:
            m = re.match(pattern, k)
            if m:
                idx.add(int(m.group(1)))
        return len(idx)

    n_ensemble = max(1, _count_prefix(r"head_bundles\.(\d+)\."))
    num_layers = max(1, _count_prefix(r"blocks\.(\d+)\."))
    dueling = any(k.startswith("value_heads.") or ".value_heads." in k for k in keys)
    noisy = any(k.endswith("weight_mu") or ".weight_mu" in k for k in keys)
    if any("iqn_tau_fc" in k for k in keys):
        distributional = "iqn"
    elif any(k.endswith("support") or ".support" in k for k in keys):
        distributional = "c51"
    else:
        distributional = None

    hidden_size = None
    for k in keys:
        if k.startswith("input_fc.") and (k.endswith("weight_mu") or k.endswith("weight")):
            hidden_size = int(state_dict[k].shape[0])
            break

    arch = {
        "dueling": dueling,
        "noisy": noisy,
        "distributional": distributional,
        "n_ensemble": n_ensemble,
        "num_layers": num_layers,
    }
    if hidden_size:
        arch["hidden_size"] = hidden_size
    return arch
import torch.nn as nn
import torch.nn.functional as F


class NoisyLinear(nn.Module):
    def __init__(self, in_features, out_features, sigma0=0.5, sigma_min=0.01):
        super().__init__()
        self.in_features = int(in_features)
        self.out_features = int(out_features)
        self.sigma_min = float(sigma_min)

        self.weight_mu = nn.Parameter(torch.empty(self.out_features, self.in_features))
        self.weight_sigma = nn.Parameter(torch.empty(self.out_features, self.in_features))
        self.register_buffer("weight_epsilon", torch.zeros(self.out_features, self.in_features))

        self.bias_mu = nn.Parameter(torch.empty(self.out_features))
        self.bias_sigma = nn.Parameter(torch.empty(self.out_features))
        self.register_buffer("bias_epsilon", torch.zeros(self.out_features))

        self.sigma0 = float(sigma0)
        self.reset_parameters()
        self.reset_noise()

    def reset_parameters(self):
        mu_range = 1.0 / math.sqrt(self.in_features)
        self.weight_mu.data.uniform_(-mu_range, mu_range)
        self.bias_mu.data.uniform_(-mu_range, mu_range)
        sigma_init = self.sigma0 / math.sqrt(self.in_features)
        self.weight_sigma.data.fill_(sigma_init)
        self.bias_sigma.data.fill_(sigma_init)

    def _scale_noise(self, size):
        x = torch.randn(size, device=self.weight_mu.device)
        return x.sign().mul_(x.abs().sqrt_())

    def reset_noise(self):
        eps_in = self._scale_noise(self.in_features)
        eps_out = self._scale_noise(self.out_features)
        self.weight_epsilon.copy_(eps_out.outer(eps_in))
        self.bias_epsilon.copy_(eps_out)

    def mean_abs_sigma(self) -> float:
        return float((self.weight_sigma.abs() + self.bias_sigma.abs()).mean().item())

    def anneal_sigma(self, progress: float) -> None:
        """progress in [0, 1]: linearly interpolate sigma toward sigma_min."""
        progress = max(0.0, min(1.0, float(progress)))
        with torch.no_grad():
            for param, init_val in (
                (self.weight_sigma, self.sigma0 / math.sqrt(self.in_features)),
                (self.bias_sigma, self.sigma0 / math.sqrt(self.in_features)),
            ):
                target = self.sigma_min
                param.data.mul_(1.0 - progress).add_(target * progress)

    def forward(self, x):
        if self.training:
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias = self.bias_mu + self.bias_sigma * self.bias_epsilon
        else:
            weight = self.weight_mu
            bias = self.bias_mu
        return F.linear(x, weight, bias)


def _make_linear(hidden_size, out_features, noisy, noisy_sigma0, layer_cls, layer_kwargs):
    if noisy:
        return layer_cls(hidden_size, out_features, **layer_kwargs)
    return layer_cls(hidden_size, out_features)


class ResidualBlock(nn.Module):
    """Pre-norm residual MLP block (NoisyLinear-aware)."""

    def __init__(self, hidden_size, noisy=False, noisy_sigma0=0.5):
        super().__init__()
        layer_cls = NoisyLinear if noisy else nn.Linear
        layer_kwargs = {"sigma0": noisy_sigma0} if noisy else {}
        self.norm1 = nn.LayerNorm(hidden_size)
        self.fc1 = layer_cls(hidden_size, hidden_size, **layer_kwargs)
        self.norm2 = nn.LayerNorm(hidden_size)
        self.fc2 = layer_cls(hidden_size, hidden_size, **layer_kwargs)

    def forward(self, x):
        residual = x
        x = F.relu(self.norm1(self.fc1(x)))
        x = self.norm2(self.fc2(x))
        return F.relu(x + residual)


class _DQNHeadBundle(nn.Module):
    """One ensemble member's output heads."""

    def __init__(
        self,
        hidden_size,
        action_sizes,
        dueling,
        noisy,
        noisy_sigma0,
        distributional,
        num_atoms,
        layer_cls,
        layer_kwargs,
    ):
        super().__init__()
        self.dueling = bool(dueling)
        self.distributional = distributional
        self.num_atoms = int(num_atoms)
        self.action_sizes = list(action_sizes)

        if distributional == "c51":
            if self.dueling:
                self.value_heads = nn.ModuleList(
                    [_make_linear(hidden_size, self.num_atoms, noisy, noisy_sigma0, layer_cls, layer_kwargs) for _ in action_sizes]
                )
                self.advantage_heads = nn.ModuleList(
                    [_make_linear(hidden_size, size * self.num_atoms, noisy, noisy_sigma0, layer_cls, layer_kwargs) for size in action_sizes]
                )
            else:
                self.q_heads = nn.ModuleList(
                    [_make_linear(hidden_size, size * self.num_atoms, noisy, noisy_sigma0, layer_cls, layer_kwargs) for size in action_sizes]
                )
        else:
            if self.dueling:
                self.value_heads = nn.ModuleList(
                    [_make_linear(hidden_size, 1, noisy, noisy_sigma0, layer_cls, layer_kwargs) for _ in action_sizes]
                )
                self.advantage_heads = nn.ModuleList(
                    [_make_linear(hidden_size, size, noisy, noisy_sigma0, layer_cls, layer_kwargs) for size in action_sizes]
                )
            else:
                self.q_heads = nn.ModuleList(
                    [_make_linear(hidden_size, size, noisy, noisy_sigma0, layer_cls, layer_kwargs) for size in action_sizes]
                )

    def q_from_features(self, x):
        outputs = []
        if self.dueling:
            for value_head, advantage_head in zip(self.value_heads, self.advantage_heads):
                value = value_head(x)
                advantage = advantage_head(x)
                outputs.append(value + (advantage - advantage.mean(dim=1, keepdim=True)))
        else:
            for head in self.q_heads:
                outputs.append(head(x))
        return outputs

    def c51_dist_from_features(self, x):
        outputs = []
        if self.dueling:
            for action_size, value_head, advantage_head in zip(self.action_sizes, self.value_heads, self.advantage_heads):
                value_logits = value_head(x).view(-1, 1, self.num_atoms)
                adv_logits = advantage_head(x).view(-1, action_size, self.num_atoms)
                logits = value_logits + (adv_logits - adv_logits.mean(dim=1, keepdim=True))
                outputs.append(logits)
        else:
            for action_size, head in zip(self.action_sizes, self.q_heads):
                logits = head(x).view(-1, action_size, self.num_atoms)
                outputs.append(logits)
        return outputs

    def iqn_from_features(self, iqn_feat, batch_size, n_q, action_sizes):
        outputs = []
        if self.dueling:
            for action_size, value_head, advantage_head in zip(action_sizes, self.value_heads, self.advantage_heads):
                value = value_head(iqn_feat).view(batch_size, n_q, 1)
                advantage = advantage_head(iqn_feat).view(batch_size, n_q, action_size)
                q_vals = value + (advantage - advantage.mean(dim=2, keepdim=True))
                outputs.append(q_vals.permute(0, 2, 1).contiguous())
        else:
            for action_size, head in zip(action_sizes, self.q_heads):
                q_vals = head(iqn_feat).view(batch_size, n_q, action_size)
                outputs.append(q_vals.permute(0, 2, 1).contiguous())
        return outputs


class DQN(nn.Module):
    def __init__(
        self,
        n_observations,
        n_actions,
        dueling=False,
        noisy=True,
        noisy_sigma0=0.5,
        distributional="iqn",
        num_atoms=51,
        v_min=-10.0,
        v_max=10.0,
        iqn_num_quantiles=32,
        iqn_num_target_quantiles=32,
        iqn_num_tau_samples=32,
        iqn_embed_dim=64,
        hidden_size=256,
        num_layers=2,
        n_ensemble=1,
    ):
        super().__init__()
        self.dueling = bool(dueling)
        self.noisy = bool(noisy)
        self.noisy_sigma0 = float(noisy_sigma0)
        self.distributional = str(distributional or "").strip().lower() or None
        self.num_atoms = int(num_atoms)
        self.v_min = float(v_min)
        self.v_max = float(v_max)
        self.iqn_num_quantiles = int(iqn_num_quantiles)
        self.iqn_num_target_quantiles = int(iqn_num_target_quantiles)
        self.iqn_num_tau_samples = int(iqn_num_tau_samples)
        self.iqn_embed_dim = int(iqn_embed_dim)
        self.action_sizes = list(n_actions)
        self.hidden_size = int(hidden_size)
        self.num_layers = max(1, int(num_layers))
        self.n_ensemble = max(1, int(n_ensemble))

        if self.num_atoms < 2 and self.distributional == "c51":
            raise ValueError("num_atoms должен быть >=2 для C51.")
        if self.distributional == "c51" and self.v_min >= self.v_max:
            raise ValueError("C51: v_min должен быть строго меньше v_max.")
        if self.distributional == "iqn":
            if self.iqn_num_quantiles < 1 or self.iqn_num_target_quantiles < 1 or self.iqn_num_tau_samples < 1:
                raise ValueError("IQN: количество квантилей/семплов должно быть >=1.")
            if self.iqn_embed_dim < 1:
                raise ValueError("IQN: iqn_embed_dim должен быть >=1.")

        layer_cls = NoisyLinear if self.noisy else nn.Linear
        layer_kwargs = {"sigma0": self.noisy_sigma0} if self.noisy else {}

        self.input_fc = layer_cls(n_observations, self.hidden_size, **layer_kwargs)
        self.input_norm = nn.LayerNorm(self.hidden_size)
        self.blocks = nn.ModuleList(
            [
                ResidualBlock(self.hidden_size, noisy=self.noisy, noisy_sigma0=self.noisy_sigma0)
                for _ in range(self.num_layers)
            ]
        )

        if self.distributional == "c51":
            self.register_buffer("support", torch.linspace(self.v_min, self.v_max, self.num_atoms))

        if self.distributional == "iqn":
            self.iqn_tau_fc = nn.Linear(self.iqn_embed_dim, self.hidden_size)
            self.iqn_tau_norm = nn.LayerNorm(self.hidden_size)
            self.register_buffer("iqn_pi_multipliers", torch.arange(1, self.iqn_embed_dim + 1, dtype=torch.float32))

        self.head_bundles = nn.ModuleList(
            [
                _DQNHeadBundle(
                    self.hidden_size,
                    self.action_sizes,
                    self.dueling,
                    self.noisy,
                    self.noisy_sigma0,
                    self.distributional,
                    self.num_atoms,
                    layer_cls,
                    layer_kwargs,
                )
                for _ in range(self.n_ensemble)
            ]
        )

        # Backward-compat aliases for code that references value_heads on single-ensemble nets
        if self.n_ensemble == 1:
            bundle = self.head_bundles[0]
            if hasattr(bundle, "value_heads"):
                self.value_heads = bundle.value_heads
            if hasattr(bundle, "advantage_heads"):
                self.advantage_heads = bundle.advantage_heads
            if hasattr(bundle, "q_heads"):
                self.q_heads = bundle.q_heads

    def reset_noise(self):
        if not self.noisy:
            return
        for module in self.modules():
            if isinstance(module, NoisyLinear):
                module.reset_noise()

    def mean_noisy_sigma(self) -> float:
        sigmas = [m.mean_abs_sigma() for m in self.modules() if isinstance(m, NoisyLinear)]
        return float(sum(sigmas) / len(sigmas)) if sigmas else 0.0

    def anneal_noisy_sigma(self, progress: float) -> None:
        for module in self.modules():
            if isinstance(module, NoisyLinear):
                module.anneal_sigma(progress)

    def _feature(self, x):
        x = F.relu(self.input_norm(self.input_fc(x)))
        for block in self.blocks:
            x = block(x)
        return x

    def _ensemble_q_lists(self, feat_fn):
        """feat_fn(bundle) -> list of Q tensors per head."""
        all_lists = [feat_fn(bundle) for bundle in self.head_bundles]
        if self.n_ensemble == 1:
            return all_lists[0]
        num_heads = len(all_lists[0])
        merged = []
        for h in range(num_heads):
            stacked = torch.stack([lst[h] for lst in all_lists], dim=0)
            merged.append(stacked.mean(dim=0))
        return merged

    def _per_member_q_values(self, x):
        """List[n_ensemble] of list[num_heads] Q tensors."""
        if self.distributional == "c51":
            feat = self._feature(x)
            support = self.support.view(1, 1, -1).to(x.device)
            return [
                [
                    torch.softmax(logits, dim=-1).mul(support).sum(dim=-1)
                    for logits in bundle.c51_dist_from_features(feat)
                ]
                for bundle in self.head_bundles
            ]
        if self.distributional == "iqn":
            feat = self._feature(x)
            batch_size = feat.shape[0]
            n_q = self.iqn_num_tau_samples
            taus = self._sample_taus(batch_size, n_q, feat.device)
            iqn_feat = self._iqn_features(feat, taus).reshape(batch_size * n_q, self.hidden_size)
            return [
                [q.mean(dim=2) for q in bundle.iqn_from_features(iqn_feat, batch_size, n_q, self.action_sizes)]
                for bundle in self.head_bundles
            ]
        feat = self._feature(x)
        return [bundle.q_from_features(feat) for bundle in self.head_bundles]

    def q_ensemble_stats(self, x):
        """Returns (mean_q_per_head, std_q_per_head)."""
        per_member = self._per_member_q_values(x)
        if self.n_ensemble == 1:
            return per_member[0], [torch.zeros_like(t) for t in per_member[0]]
        num_heads = len(per_member[0])
        means, stds = [], []
        for h in range(num_heads):
            stacked = torch.stack([member[h] for member in per_member], dim=0)
            means.append(stacked.mean(dim=0))
            stds.append(stacked.std(dim=0, unbiased=False))
        return means, stds

    def iqn_ensemble_members(self, x, num_quantiles=None, taus=None, return_taus=False):
        """Returns list[n_ensemble] of per-head quantile tensors [B, A, Nq]."""
        if self.distributional != "iqn":
            raise RuntimeError("iqn_ensemble_members() только для distributional='iqn'.")
        feat = self._feature(x)
        batch_size = feat.shape[0]
        n_q = int(num_quantiles or self.iqn_num_quantiles)
        if taus is None:
            taus = self._sample_taus(batch_size, n_q, feat.device)
        iqn_feat = self._iqn_features(feat, taus).reshape(batch_size * n_q, self.hidden_size)
        outputs = [
            bundle.iqn_from_features(iqn_feat, batch_size, n_q, self.action_sizes)
            for bundle in self.head_bundles
        ]
        if return_taus:
            return outputs, taus
        return outputs

    def dist(self, x):
        if self.distributional != "c51":
            raise RuntimeError("dist() доступен только при distributional='c51'.")
        feat = self._feature(x)

        def _one(bundle):
            return bundle.c51_dist_from_features(feat)

        if self.n_ensemble == 1:
            return _one(self.head_bundles[0])
        all_d = [_one(b) for b in self.head_bundles]
        num_heads = len(all_d[0])
        return [
            torch.stack([all_d[e][h] for e in range(self.n_ensemble)], dim=0).mean(dim=0)
            for h in range(num_heads)
        ]

    def _sample_taus(self, batch_size, num_quantiles, device):
        return torch.rand(batch_size, num_quantiles, 1, device=device)

    def _iqn_features(self, base_features, taus):
        # taus: [B, Nq, 1] — standard IQN cosine embedding
        cos_in = torch.cos(taus * math.pi * self.iqn_pi_multipliers.view(1, 1, -1).to(taus.device))
        tau_embed = F.relu(self.iqn_tau_norm(self.iqn_tau_fc(cos_in)))
        return base_features.unsqueeze(1) * tau_embed

    def iqn(self, x, num_quantiles=None, taus=None, return_taus=False):
        if self.distributional != "iqn":
            raise RuntimeError("iqn() доступен только при distributional='iqn'.")
        feat = self._feature(x)
        batch_size = feat.shape[0]
        n_q = int(num_quantiles or self.iqn_num_quantiles)
        if taus is None:
            taus = self._sample_taus(batch_size, n_q, feat.device)
        iqn_feat = self._iqn_features(feat, taus).reshape(batch_size * n_q, self.hidden_size)

        all_outputs = []
        for bundle in self.head_bundles:
            all_outputs.append(bundle.iqn_from_features(iqn_feat, batch_size, n_q, self.action_sizes))

        if self.n_ensemble == 1:
            outputs = all_outputs[0]
        else:
            num_heads = len(all_outputs[0])
            outputs = []
            for h in range(num_heads):
                stacked = torch.stack([all_outputs[e][h] for e in range(self.n_ensemble)], dim=0)
                outputs.append(stacked.mean(dim=0))

        if return_taus:
            return outputs, taus
        return outputs

    def q_values(self, x):
        if self.distributional == "c51":
            dists = self.dist(x)
            support = self.support.view(1, 1, -1).to(x.device)
            return [torch.softmax(logits, dim=-1).mul(support).sum(dim=-1) for logits in dists]
        if self.distributional == "iqn":
            quantiles = self.iqn(x, num_quantiles=self.iqn_num_tau_samples, return_taus=False)
            return [q.mean(dim=2) for q in quantiles]

        feat = self._feature(x)
        return self._ensemble_q_lists(lambda bundle: bundle.q_from_features(feat))

    def forward(self, x):
        return self.q_values(x)

    def infer(self, obs, masks_by_head=None):
        logits = self.q_values(obs)
        probs = []
        for idx, head_logits in enumerate(logits):
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
                if mask is not None and mask.shape == head_logits.shape:
                    safe_mask = torch.where(mask.any(dim=1, keepdim=True), mask, torch.ones_like(mask))
                    masked = head_logits.masked_fill(~safe_mask, -1e9)
                    probs.append(torch.softmax(masked, dim=1))
                    continue
            probs.append(torch.softmax(head_logits, dim=1))
        return probs, None
