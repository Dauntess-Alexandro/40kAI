from dataclasses import dataclass
import numpy as np
import torch


@dataclass
class PPOBatch:
    obs: torch.Tensor
    actions: torch.Tensor
    logprobs: torch.Tensor
    returns: torch.Tensor
    advantages: torch.Tensor
    values: torch.Tensor
    masks_by_head: list[torch.Tensor]


class PPORolloutBuffer:
    def __init__(self):
        self.clear()

    def clear(self):
        self.obs = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.dones = []
        self.values = []
        self.masks_by_head = []
        self.env_ids = []

    def add(self, obs, action, logprob, reward, done, value, masks_by_head, env_id: int = 0):
        self.obs.append(np.asarray(obs, dtype=np.float32))
        self.actions.append(np.asarray(action, dtype=np.int64))
        self.logprobs.append(float(logprob))
        self.rewards.append(float(reward))
        self.dones.append(bool(done))
        self.values.append(float(value))
        self.masks_by_head.append(masks_by_head)
        self.env_ids.append(int(env_id))

    def add_batch(
        self,
        obs_list,
        actions_list,
        logprobs_list,
        rewards_list,
        dones_list,
        values_list,
        masks_by_head_list,
        env_ids_list,
    ):
        for obs, act, lp, rew, dn, val, masks, env_id in zip(
            obs_list,
            actions_list,
            logprobs_list,
            rewards_list,
            dones_list,
            values_list,
            masks_by_head_list,
            env_ids_list,
        ):
            self.add(obs, act, lp, rew, dn, val, masks, env_id=int(env_id))

    def __len__(self):
        return len(self.rewards)

    def compute_returns_and_advantages(self, gamma: float, gae_lambda: float):
        rewards = np.asarray(self.rewards, dtype=np.float32)
        dones = np.asarray(self.dones, dtype=np.float32)
        values = np.asarray(self.values, dtype=np.float32)
        env_ids = np.asarray(self.env_ids, dtype=np.int64) if self.env_ids else np.zeros_like(rewards, dtype=np.int64)

        advantages = np.zeros_like(rewards, dtype=np.float32)
        last_gae_by_env: dict[int, float] = {}
        next_value_by_env: dict[int, float] = {}
        for t in reversed(range(len(rewards))):
            env_id = int(env_ids[t])
            if dones[t] >= 1.0:
                next_value = 0.0
                last_gae = 0.0
            else:
                next_value = float(next_value_by_env.get(env_id, 0.0))
                last_gae = float(last_gae_by_env.get(env_id, 0.0))
            non_terminal = 1.0 - dones[t]
            delta = rewards[t] + gamma * next_value * non_terminal - values[t]
            last_gae = delta + gamma * gae_lambda * non_terminal * last_gae
            advantages[t] = float(last_gae)
            last_gae_by_env[env_id] = float(last_gae)
            next_value_by_env[env_id] = float(values[t])

        returns = advantages + values
        return returns, advantages

    def to_tensors(self, device: torch.device, gamma: float, gae_lambda: float, normalize_adv: bool = True):
        returns, advantages = self.compute_returns_and_advantages(gamma=gamma, gae_lambda=gae_lambda)
        if normalize_adv and len(advantages) > 1:
            adv_mean = advantages.mean()
            adv_std = advantages.std() + 1e-8
            advantages = (advantages - adv_mean) / adv_std

        obs_t = torch.tensor(np.asarray(self.obs, dtype=np.float32), device=device)
        actions_t = torch.tensor(np.asarray(self.actions, dtype=np.int64), device=device)
        logprobs_t = torch.tensor(np.asarray(self.logprobs, dtype=np.float32), device=device)
        returns_t = torch.tensor(returns, dtype=torch.float32, device=device)
        adv_t = torch.tensor(advantages, dtype=torch.float32, device=device)
        values_t = torch.tensor(np.asarray(self.values, dtype=np.float32), device=device)

        if self.masks_by_head:
            num_heads = len(self.masks_by_head[0])
            mask_heads = []
            for head_idx in range(num_heads):
                stacked = []
                for item in self.masks_by_head:
                    head_mask = item[head_idx]
                    stacked.append(np.asarray(head_mask, dtype=np.bool_))
                mask_heads.append(torch.tensor(np.stack(stacked, axis=0), dtype=torch.bool, device=device))
        else:
            mask_heads = []

        return PPOBatch(
            obs=obs_t,
            actions=actions_t,
            logprobs=logprobs_t,
            returns=returns_t,
            advantages=adv_t,
            values=values_t,
            masks_by_head=mask_heads,
        )

