from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F


class AlphaZeroPolicyValueNet(nn.Module):
    """
    Factorized policy-value net:
    - несколько policy heads (по контракту action heads),
    - один value head в диапазоне [-1, 1].
    """

    def __init__(self, n_observations: int, n_actions: list[int], hidden_size: int = 256):
        super().__init__()
        self.n_observations = int(n_observations)
        self.action_sizes = [int(x) for x in n_actions]
        self.hidden_size = int(hidden_size)

        self.layer1 = nn.Linear(self.n_observations, self.hidden_size)
        self.layer2 = nn.Linear(self.hidden_size, self.hidden_size)
        self.policy_heads = nn.ModuleList([nn.Linear(self.hidden_size, n) for n in self.action_sizes])
        self.value_head = nn.Linear(self.hidden_size, 1)

    def _encode(self, obs: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.layer1(obs))
        x = F.relu(self.layer2(x))
        return x

    def forward(self, obs: torch.Tensor):
        x = self._encode(obs)
        policy_logits = [head(x) for head in self.policy_heads]
        value = torch.tanh(self.value_head(x)).squeeze(-1)
        return policy_logits, value

    @torch.no_grad()
    def infer(self, obs: torch.Tensor, masks_by_head: list[torch.Tensor] | None = None):
        logits, value = self.forward(obs)
        probs = []
        for idx, head_logits in enumerate(logits):
            masked = head_logits
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
                if mask is not None and mask.shape == head_logits.shape:
                    safe_mask = torch.where(mask.any(dim=1, keepdim=True), mask, torch.ones_like(mask, dtype=torch.bool))
                    masked = head_logits.masked_fill(~safe_mask, -1e9)
            probs.append(torch.softmax(masked, dim=1))
        return probs, value
