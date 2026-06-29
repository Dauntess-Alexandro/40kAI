"""PHOENIX trainer: IQN-TD + value-expansion + SPR, periodic resets, аннелинг n-step/γ."""
from __future__ import annotations

import numpy as np
import torch
import torch.nn.functional as F

from core.models.phoenix_loss import spr_consistency_loss, value_expansion_target


def anneal_value(start: float, end: float, step: int, anneal_steps: int) -> float:
    if anneal_steps <= 0 or step >= anneal_steps:
        return float(end)
    if step <= 0:
        return float(start)
    frac = step / anneal_steps
    # экспоненциальная интерполяция в лог-пространстве сдвига
    return float(start + (end - start) * frac)


class PhoenixTrainer:
    def __init__(self, net, cfg, device: str = "cpu"):
        self.net = net.to(device)
        self.cfg = cfg
        self.device = device
        self.optimizer = torch.optim.AdamW(self.net.parameters(), lr=1e-4, weight_decay=0.1)
        self.grad_step = 0
        self._steps_since_reset = 0

    def current_gamma(self, grad_step: int) -> float:
        return anneal_value(
            self.cfg.gamma_start,
            self.cfg.gamma_end,
            self._steps_since_reset,
            self.cfg.anneal_steps,
        )

    def current_nstep(self, grad_step: int) -> int:
        return int(
            round(
                anneal_value(
                    float(self.cfg.nstep_start),
                    float(self.cfg.nstep_end),
                    grad_step,
                    self.cfg.anneal_steps,
                )
            )
        )

    def _stack_windows(self, windows):
        obs = torch.tensor(np.stack([w.obs for w in windows]), dtype=torch.float32, device=self.device)
        actions = torch.tensor(np.stack([w.actions for w in windows]), dtype=torch.long, device=self.device)
        active = torch.tensor(np.stack([w.active_masks for w in windows]), dtype=torch.bool, device=self.device)
        rewards = torch.tensor(np.stack([w.rewards for w in windows]), dtype=torch.float32, device=self.device)
        dones = torch.tensor(np.stack([w.dones for w in windows]), dtype=torch.float32, device=self.device)
        return obs, actions, active, rewards, dones  # [B,H+1,...]

    def learn_step(self, windows) -> dict:
        obs, actions, active, rewards, dones = self._stack_windows(windows)
        B, span = obs.shape[0], obs.shape[1]
        K = min(self.cfg.spr_horizon_K, span - 1)
        gamma = self.current_gamma(self.grad_step)

        z0 = self.net.encode(obs[:, 0])  # [B, hid]

        # --- SPR ---
        a_emb_seq = torch.stack(
            [self.net.action_embed(actions[:, k], active[:, k]) for k in range(K)], dim=1
        )  # [B,K,emb]
        zhat = self.net.dynamics.rollout(z0, a_emb_seq)  # [B,K,hid]
        pred = self.net.predict(self.net.project(zhat.reshape(B * K, -1))).reshape(B, K, -1)
        with torch.no_grad():
            tgt_z = torch.stack([self.net.target_encode(obs[:, k + 1]) for k in range(K)], dim=1)
            tgt_proj = self.net.target_project(tgt_z.reshape(B * K, -1)).reshape(B, K, -1)
        spr = spr_consistency_loss(pred, tgt_proj, dones[:, 1 : K + 1])

        # --- IQN TD с value-expansion (фикс. h = ve_horizon, ve_steve=False по умолчанию) ---
        h = min(self.cfg.ve_horizon, span - 1)
        # online quantiles на obs[:,0] для выбранных действий первой головы (упрощённо: голова 0)
        q_online = self.net.online_quantiles(obs[:, 0])  # list per-head [B,A,Nq]
        # bootstrap: greedy по target-IQN на реальном obs[:,h] (Волна 1: honest n-step; латентный
        # bootstrap — флаг в Task 8.x), берём среднее по головам от max-Q
        with torch.no_grad():
            tq = self.net.target.q_values(obs[:, h])  # list per-head [B,A]
            boot = torch.stack([qh.max(dim=1).values for qh in tq], dim=1).mean(dim=1)  # [B]
        gammas = torch.full((B, span), gamma, device=self.device)
        y = value_expansion_target(rewards[:, :h], gammas[:, :h], boot, h=h)  # [B]
        # текущая оценка V(s0) ≈ mean по головам от mean-quantile max
        v0 = torch.stack([qh.mean(dim=2).max(dim=1).values for qh in q_online], dim=1).mean(dim=1)
        td_errors = y.detach() - v0
        iqn_loss = F.smooth_l1_loss(v0, y.detach())

        loss = iqn_loss + self.cfg.spr_coef * spr
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.net.update_targets(self.cfg.target_ema_rl, self.cfg.target_ema_spr)
        self.grad_step += 1
        self._steps_since_reset += 1
        return {
            "loss": float(loss.detach()),
            "loss_iqn": float(iqn_loss.detach()),
            "loss_spr": float(spr.detach()),
            "td_errors": td_errors.detach().abs().cpu().numpy(),
        }

    def maybe_reset(self, grad_step: int) -> bool:
        if self.cfg.reset_interval > 0 and grad_step > 0 and grad_step % self.cfg.reset_interval == 0:
            self.net.reset_heads_and_shrink_encoder(self.cfg.shrink_alpha)
            self.optimizer = torch.optim.AdamW(self.net.parameters(), lr=1e-4, weight_decay=0.1)
            self._steps_since_reset = 0
            return True
        return False
