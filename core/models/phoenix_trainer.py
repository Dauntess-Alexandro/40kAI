"""PHOENIX trainer: IQN-TD + value-expansion + SPR, periodic resets, аннелинг n-step/γ."""
from __future__ import annotations

import numpy as np
import torch

from core.models.phoenix_loss import spr_consistency_loss
from core.models.utils import quantile_huber_loss


def anneal_value(start: float, end: float, step: int, anneal_steps: int) -> float:
    # Линейная интерполяция start→end за anneal_steps шагов (Волна 1).
    # Полноценный экспоненциальный профиль — задача Волны 2; концы заякорены на DQN.
    if anneal_steps <= 0 or step >= anneal_steps:
        return float(end)
    if step <= 0:
        return float(start)
    frac = step / anneal_steps
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

    def _target_quantiles_for_horizon(self, obs, rewards, dones, h: int, gamma: float, zhat=None):
        B, span = obs.shape[0], obs.shape[1]
        h = min(max(1, int(h)), span - 1)
        gammas = torch.full((B, span), float(gamma), device=self.device)
        use_latent = bool(getattr(self.cfg, "ve_latent_bootstrap", False)) and zhat is not None and h <= zhat.shape[1]
        if use_latent:
            target_q = self.net.target_quantiles_from_latent(
                zhat[:, h - 1].detach(),
                num_quantiles=int(self.cfg.iqn_num_target_quantiles),
            )
        else:
            target_q = self.net.target_quantiles(
                obs[:, h],
                num_quantiles=int(self.cfg.iqn_num_target_quantiles),
            )
        out = []
        boot_mask = (1.0 - dones[:, h]).to(torch.float32).view(B, 1)
        for qh in target_q:
            greedy = qh.mean(dim=2).argmax(dim=1)
            idx = greedy.view(B, 1, 1).expand(-1, 1, qh.shape[2])
            boot = qh.gather(1, idx).squeeze(1) * boot_mask
            acc = torch.zeros_like(boot)
            discount = torch.ones((B, 1), dtype=torch.float32, device=self.device)
            for j in range(h):
                valid = (1.0 - dones[:, j]).to(torch.float32).view(B, 1)
                acc = acc + discount * rewards[:, j].view(B, 1) * valid
                discount = discount * gammas[:, j].view(B, 1) * valid
            out.append(acc + discount * boot)
        return out

    def _steve_targets(self, obs, rewards, dones, max_h: int, gamma: float, zhat=None):
        horizons = list(range(1, max(1, int(max_h)) + 1))
        per_h = [self._target_quantiles_for_horizon(obs, rewards, dones, h, gamma, zhat=zhat) for h in horizons]
        num_heads = len(per_h[0])
        out = []
        for head_idx in range(num_heads):
            stacked = torch.stack([targets[head_idx] for targets in per_h], dim=0)  # [H,B,Nt]
            inv_var = 1.0 / (stacked.var(dim=2, unbiased=False).clamp(min=1e-4))  # [H,B]
            weights = inv_var / inv_var.sum(dim=0, keepdim=True).clamp(min=1e-6)
            out.append((stacked * weights.unsqueeze(2)).sum(dim=0))
        return out

    def learn_step(self, windows, is_weights=None) -> dict:
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

        # --- IQN TD с value-expansion ---
        h = min(self.cfg.ve_horizon, span - 1)
        q_online, taus = self.net.online_quantiles(
            obs[:, 0],
            num_quantiles=int(self.cfg.iqn_num_quantiles),
            return_taus=True,
        )  # list per-head [B,A,Nq], taus [B,Nq,1]
        with torch.no_grad():
            if bool(getattr(self.cfg, "ve_steve", False)):
                target_by_head = self._steve_targets(obs, rewards, dones, h, gamma, zhat=zhat)
            else:
                target_by_head = self._target_quantiles_for_horizon(obs, rewards, dones, h, gamma, zhat=zhat)

        sample_losses = []
        sample_td = []
        max_heads = min(len(q_online), actions.shape[2], active.shape[2], len(target_by_head))
        for head_idx in range(max_heads):
            qh = q_online[head_idx]
            act = actions[:, 0, head_idx].clamp(min=0, max=qh.shape[1] - 1)
            idx = act.view(B, 1, 1).expand(-1, 1, qh.shape[2])
            pred = qh.gather(1, idx).squeeze(1)
            per_sample, td = quantile_huber_loss(
                pred.float(),
                target_by_head[head_idx].detach().float(),
                taus.float(),
                kappa=float(getattr(self.cfg, "iqn_kappa", 1.0)),
            )
            mask = active[:, 0, head_idx].to(per_sample.dtype)
            sample_losses.append(per_sample * mask)
            sample_td.append(td.detach().abs().mean(dim=(1, 2)) * mask)
        if not sample_losses:
            iqn_loss = torch.zeros((), dtype=torch.float32, device=self.device)
            td_errors = torch.zeros((B,), dtype=torch.float32, device=self.device)
        else:
            per_sample_loss = torch.stack(sample_losses, dim=0).sum(dim=0)
            denom = torch.stack([active[:, 0, h].to(torch.float32) for h in range(max_heads)], dim=0).sum(dim=0).clamp(min=1.0)
            per_sample_loss = per_sample_loss / denom
            if is_weights is not None:
                weights_t = torch.tensor(is_weights, dtype=torch.float32, device=self.device).view(-1)
                if weights_t.shape[0] == per_sample_loss.shape[0]:
                    per_sample_loss = per_sample_loss * weights_t
            iqn_loss = per_sample_loss.mean()
            td_errors = torch.stack(sample_td, dim=0).sum(dim=0) / denom

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
