import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


def _apply_action_mask(logits: torch.Tensor, mask: torch.Tensor | None) -> torch.Tensor:
    if mask is None:
        return logits
    if mask.dtype != torch.bool:
        mask = mask.to(dtype=torch.bool)
    if mask.shape != logits.shape:
        return logits
    valid_any = mask.any(dim=1, keepdim=True)
    safe_mask = torch.where(valid_any, mask, torch.ones_like(mask, dtype=torch.bool))
    masked_logits = logits.masked_fill(~safe_mask, -1e9)
    return masked_logits


class ActorCriticMultiHead(nn.Module):
    def __init__(self, n_observations: int, n_actions: list[int], hidden_size: int = 256):
        super().__init__()
        self.action_sizes = [int(x) for x in n_actions]
        self.layer1 = nn.Linear(n_observations, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.policy_heads = nn.ModuleList([nn.Linear(hidden_size, size) for size in self.action_sizes])
        self.value_head = nn.Linear(hidden_size, 1)

    def _encode(self, obs: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.layer1(obs))
        x = F.relu(self.layer2(x))
        return x

    def forward(self, obs: torch.Tensor):
        x = self._encode(obs)
        logits = [head(x) for head in self.policy_heads]
        value = self.value_head(x).squeeze(-1)
        return logits, value

    def evaluate_actions(
        self,
        obs: torch.Tensor,
        actions: torch.Tensor,
        masks_by_head: list[torch.Tensor | None] | None = None,
    ):
        logits_list, values = self.forward(obs)
        total_logprob = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        total_entropy = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        for idx, logits in enumerate(logits_list):
            mask = None
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
            logits = _apply_action_mask(logits, mask)
            dist = Categorical(logits=logits)
            head_actions = actions[:, idx]
            total_logprob = total_logprob + dist.log_prob(head_actions)
            total_entropy = total_entropy + dist.entropy()
        return total_logprob, total_entropy, values

    @torch.no_grad()
    def act(
        self,
        obs: torch.Tensor,
        masks_by_head: list[torch.Tensor | None] | None = None,
        deterministic: bool = False,
    ):
        logits_list, values = self.forward(obs)
        actions = []
        total_logprob = torch.zeros(obs.shape[0], device=obs.device, dtype=torch.float32)
        for idx, logits in enumerate(logits_list):
            mask = None
            if masks_by_head is not None and idx < len(masks_by_head):
                mask = masks_by_head[idx]
            logits = _apply_action_mask(logits, mask)
            dist = Categorical(logits=logits)
            if deterministic:
                head_actions = logits.argmax(dim=1)
            else:
                head_actions = dist.sample()
            total_logprob = total_logprob + dist.log_prob(head_actions)
            actions.append(head_actions)
        stacked_actions = torch.stack(actions, dim=1)
        return stacked_actions, total_logprob, values

