import math
import torch
import torch.nn as nn
import torch.nn.functional as F


class NoisyLinear(nn.Module):
    def __init__(self, in_features, out_features, sigma0=0.5):
        super().__init__()
        self.in_features = int(in_features)
        self.out_features = int(out_features)

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

    def forward(self, x):
        if self.training:
            weight = self.weight_mu + self.weight_sigma * self.weight_epsilon
            bias = self.bias_mu + self.bias_sigma * self.bias_epsilon
        else:
            weight = self.weight_mu
            bias = self.bias_mu
        return F.linear(x, weight, bias)


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
        self.hidden_size = 256

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
        self.layer1 = layer_cls(n_observations, self.hidden_size, **layer_kwargs)
        self.layer2 = layer_cls(self.hidden_size, self.hidden_size, **layer_kwargs)

        if self.distributional == "c51":
            self.register_buffer("support", torch.linspace(self.v_min, self.v_max, self.num_atoms))
            if self.dueling:
                self.value_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, self.num_atoms, **layer_kwargs) for _ in self.action_sizes]
                )
                self.advantage_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size * self.num_atoms, **layer_kwargs) for size in self.action_sizes]
                )
            else:
                self.q_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size * self.num_atoms, **layer_kwargs) for size in self.action_sizes]
                )
        elif self.distributional == "iqn":
            self.iqn_tau_fc = nn.Linear(self.iqn_embed_dim, self.hidden_size)
            self.register_buffer("iqn_pi_multipliers", torch.arange(1, self.iqn_embed_dim + 1, dtype=torch.float32))
            if self.dueling:
                self.value_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, 1, **layer_kwargs) for _ in self.action_sizes]
                )
                self.advantage_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size, **layer_kwargs) for size in self.action_sizes]
                )
            else:
                self.q_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size, **layer_kwargs) for size in self.action_sizes]
                )
        else:
            if self.dueling:
                self.value_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, 1, **layer_kwargs) for _ in self.action_sizes]
                )
                self.advantage_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size, **layer_kwargs) for size in self.action_sizes]
                )
            else:
                self.q_heads = nn.ModuleList(
                    [layer_cls(self.hidden_size, size, **layer_kwargs) for size in self.action_sizes]
                )

    def reset_noise(self):
        if not self.noisy:
            return
        for module in self.modules():
            if isinstance(module, NoisyLinear):
                module.reset_noise()

    def _feature(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return x

    def dist(self, x):
        if self.distributional != "c51":
            raise RuntimeError("dist() доступен только при distributional='c51'.")
        x = self._feature(x)
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

    def _sample_taus(self, batch_size, num_quantiles, device):
        return torch.rand(batch_size, num_quantiles, 1, device=device)

    def _iqn_features(self, base_features, taus):
        # taus: [B, Nq, 1]
        cos_in = taus * self.iqn_pi_multipliers.view(1, 1, -1).to(taus.device) * math.pi
        tau_embed = F.relu(self.iqn_tau_fc(torch.cos(cos_in)))
        return base_features.unsqueeze(1) * tau_embed

    def iqn(self, x, num_quantiles=None, taus=None, return_taus=False):
        if self.distributional != "iqn":
            raise RuntimeError("iqn() доступен только при distributional='iqn'.")
        x = self._feature(x)
        batch_size = x.shape[0]
        n_q = int(num_quantiles or self.iqn_num_quantiles)
        if taus is None:
            taus = self._sample_taus(batch_size, n_q, x.device)
        iqn_feat = self._iqn_features(x, taus).reshape(batch_size * n_q, self.hidden_size)
        outputs = []
        if self.dueling:
            for action_size, value_head, advantage_head in zip(self.action_sizes, self.value_heads, self.advantage_heads):
                value = value_head(iqn_feat).view(batch_size, n_q, 1)
                advantage = advantage_head(iqn_feat).view(batch_size, n_q, action_size)
                q_vals = value + (advantage - advantage.mean(dim=2, keepdim=True))
                outputs.append(q_vals.permute(0, 2, 1).contiguous())  # [B, A, Nq]
        else:
            for action_size, head in zip(self.action_sizes, self.q_heads):
                q_vals = head(iqn_feat).view(batch_size, n_q, action_size)
                outputs.append(q_vals.permute(0, 2, 1).contiguous())  # [B, A, Nq]
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
        x = self._feature(x)
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

    def forward(self, x):
        return self.q_values(x)
