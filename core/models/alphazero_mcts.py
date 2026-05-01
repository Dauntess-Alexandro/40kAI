from __future__ import annotations

from dataclasses import dataclass
from contextlib import nullcontext
from typing import Any, Optional

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys


@dataclass
class MCTSConfig:
    simulations: int = 64
    c_puct: float = 1.5
    dirichlet_alpha: float = 0.3
    dirichlet_eps: float = 0.25
    top_k_per_head: int = 8
    max_depth: int = 1
    mode: str = "proxy"  # "proxy" | "tree"
    root_dirichlet_only: bool = True


def _masked_normalize(prior: np.ndarray, legal_mask: np.ndarray) -> np.ndarray:
    p = np.asarray(prior, dtype=np.float32).copy()
    m = np.asarray(legal_mask, dtype=bool)
    if p.shape != m.shape:
        return np.ones_like(p, dtype=np.float32) / float(max(1, p.size))
    p[~m] = 0.0
    s = float(p.sum())
    if s <= 1e-12:
        p = m.astype(np.float32)
        s = float(p.sum())
    return p / max(1e-12, s)


class AlphaZeroFactorizedMCTS:
    """
    Практичный factorized-search proxy для текущего env:
    - Использует priors сети по головам + legal masks.
    - Возвращает factorized policy targets (по головам) и sampled action.
    NOTE: это production-ready интерфейс, но без полного env-copy tree search;
    эволюционно сюда добавляется настоящий deep-tree rollout.
    """

    def __init__(self, policy_value_net, config: MCTSConfig | None = None, device: torch.device | None = None):
        self.net = policy_value_net
        self.cfg = config or MCTSConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}

    def _masked_topk(self, prior: np.ndarray, legal: np.ndarray) -> np.ndarray:
        legal = np.asarray(legal, dtype=bool)
        k = max(1, int(getattr(self.cfg, "top_k_per_head", 8) or 8))
        if int(np.sum(legal)) <= k:
            return legal
        out = np.zeros_like(legal, dtype=bool)
        legal_idx = np.where(legal)[0]
        scores = np.asarray(prior[legal_idx], dtype=np.float32)
        top_local = np.argsort(scores)[-k:]
        out[legal_idx[top_local]] = True
        return out

    def _evaluate_net(self, obs: np.ndarray, legal_masks_by_head: list[np.ndarray]) -> tuple[list[np.ndarray], float]:
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        priors = [p.squeeze(0).detach().cpu().numpy().astype(np.float32) for p in priors_t]
        return priors, float(value_t.item())

    def _terminal_value_from_info(self, info: dict[str, Any]) -> Optional[float]:
        winner = str((info or {}).get("winner", "") or "").strip().lower()
        end_reason = str((info or {}).get("end reason", "") or "").strip().lower()
        if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
            return 1.0
        if winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
            return -1.0
        if str(end_reason).startswith("turn_limit"):
            return 0.0
        return None

    def _run_proxy(self, *, obs: np.ndarray, legal_masks_by_head: list[np.ndarray], temperature: float) -> tuple[list[np.ndarray], list[int], float]:
        priors, value = self._evaluate_net(obs=obs, legal_masks_by_head=legal_masks_by_head)
        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        temp = max(1e-6, float(temperature))
        for head_idx, prior in enumerate(priors):
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            pi = _masked_normalize(prior, legal)
            legal_count = int(np.sum(legal))
            if legal_count > 1 and self.cfg.dirichlet_eps > 0:
                alpha = float(self.cfg.dirichlet_alpha)
                noise = np.random.dirichlet([alpha] * legal_count).astype(np.float32)
                noisy = np.zeros_like(pi, dtype=np.float32)
                noisy[np.where(legal)[0]] = noise
                pi = (1.0 - float(self.cfg.dirichlet_eps)) * pi + float(self.cfg.dirichlet_eps) * noisy
                pi = _masked_normalize(pi, legal)
            logits = np.log(np.clip(pi, 1e-12, 1.0)) / temp
            ptemp = np.exp(logits - np.max(logits))
            ptemp = _masked_normalize(ptemp, legal)
            action = int(np.random.choice(np.arange(ptemp.size), p=ptemp))
            policy_targets.append(ptemp.astype(np.float32))
            selected_actions.append(action)
        self.last_run_stats = {"mode": "proxy", "simulations": 1.0}
        return policy_targets, selected_actions, value

    def _run_tree(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        temperature: float,
        env,
        len_model: int,
        enemy_policy_fn=None,
    ) -> tuple[list[np.ndarray], list[int], float]:
        root_priors, root_value = self._evaluate_net(obs=obs, legal_masks_by_head=legal_masks_by_head)
        priors = []
        legal_masks = []
        visits = []
        values_sum = []
        q_values = []
        for i, prior in enumerate(root_priors):
            legal = np.asarray(legal_masks_by_head[i], dtype=bool)
            legal_topk = self._masked_topk(prior, legal)
            p = _masked_normalize(prior, legal_topk)
            # Root noise only.
            legal_count = int(np.sum(legal_topk))
            if legal_count > 1 and float(self.cfg.dirichlet_eps) > 0.0:
                alpha = float(self.cfg.dirichlet_alpha)
                noise = np.random.dirichlet([alpha] * legal_count).astype(np.float32)
                noisy = np.zeros_like(p, dtype=np.float32)
                noisy[np.where(legal_topk)[0]] = noise
                p = _masked_normalize((1.0 - float(self.cfg.dirichlet_eps)) * p + float(self.cfg.dirichlet_eps) * noisy, legal_topk)
            priors.append(p)
            legal_masks.append(legal_topk)
            visits.append(np.zeros_like(p, dtype=np.float32))
            values_sum.append(np.zeros_like(p, dtype=np.float32))
            q_values.append(np.zeros_like(p, dtype=np.float32))

        sims = max(1, int(getattr(self.cfg, "simulations", 1) or 1))
        max_depth = max(1, int(getattr(self.cfg, "max_depth", 1) or 1))
        c_puct = float(getattr(self.cfg, "c_puct", 1.5) or 1.5)
        sim_values: list[float] = []
        sim_depths: list[float] = []
        for _ in range(sims):
            action_list: list[int] = []
            total_n = float(sum(float(v.sum()) for v in visits) + 1.0)
            sqrt_n = float(np.sqrt(total_n))
            for i in range(len(priors)):
                legal = legal_masks[i]
                u = q_values[i] + c_puct * priors[i] * sqrt_n / (1.0 + visits[i])
                u[~legal] = -1e9
                action_idx = int(np.argmax(u))
                if not legal[action_idx]:
                    legal_idx = np.where(legal)[0]
                    action_idx = int(legal_idx[0]) if legal_idx.size else 0
                action_list.append(action_idx)

            snapshot = env.snapshot_state() if hasattr(env, "snapshot_state") else None
            env_u = getattr(env, "unwrapped", env)
            ordered_keys = ordered_action_keys(int(len_model))
            current_obs = np.asarray(obs, dtype=np.float32)
            leaf_value: Optional[float] = None
            depth_reached = 0
            sim_ctx = env.simulation_mode() if hasattr(env, "simulation_mode") else nullcontext(env)
            with sim_ctx:
                try:
                    current_action = list(action_list)
                    for depth in range(max_depth):
                        depth_reached = depth + 1
                        action_dict = action_tensor_to_dict(
                            torch.tensor([current_action], dtype=torch.long),
                            len_model=int(len_model),
                        )
                        next_obs, _reward, done, trunc, info = env.step(action_dict)
                        if not bool(done or trunc):
                            env.enemyTurn(trunc=False, policy_fn=enemy_policy_fn)
                            done = bool(getattr(env, "game_over", False))
                            info = env.get_info()

                        term = self._terminal_value_from_info(info or {})
                        current_obs = np.asarray(next_obs, dtype=np.float32)
                        if term is not None or bool(done or trunc):
                            leaf_value = float(term if term is not None else 0.0)
                            break

                        if depth < (max_depth - 1):
                            legal_dict_next = env_u.get_legal_action_masks_by_head(side="model")
                            next_legal = [legal_dict_next[k] for k in ordered_keys]
                            next_priors, _value_tmp = self._evaluate_net(
                                obs=current_obs,
                                legal_masks_by_head=next_legal,
                            )
                            next_action: list[int] = []
                            for head_idx, prior_next in enumerate(next_priors):
                                legal_next = np.asarray(next_legal[head_idx], dtype=bool)
                                legal_topk_next = self._masked_topk(prior_next, legal_next)
                                pi_next = _masked_normalize(prior_next, legal_topk_next)
                                next_action.append(int(np.random.choice(np.arange(pi_next.size), p=pi_next)))
                            current_action = next_action

                    if leaf_value is None:
                        legal_dict_leaf = env_u.get_legal_action_masks_by_head(side="model")
                        legal_leaf = [legal_dict_leaf[k] for k in ordered_keys]
                        _leaf_priors, leaf_value = self._evaluate_net(
                            obs=current_obs,
                            legal_masks_by_head=legal_leaf,
                        )
                finally:
                    if snapshot is not None and hasattr(env, "restore_state"):
                        env.restore_state(snapshot)

            if leaf_value is None:
                leaf_value = 0.0
            leaf_value = float(np.clip(float(leaf_value), -1.0, 1.0))
            sim_values.append(leaf_value)
            sim_depths.append(float(depth_reached))
            for i, a in enumerate(action_list):
                visits[i][a] += 1.0
                values_sum[i][a] += leaf_value
                q_values[i][a] = values_sum[i][a] / max(1.0, visits[i][a])

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        temp = max(1e-6, float(temperature))
        for i in range(len(priors)):
            legal = legal_masks[i]
            n = visits[i].copy()
            n[~legal] = 0.0
            if float(n.sum()) <= 1e-12:
                pi = _masked_normalize(priors[i], legal)
            else:
                logits = np.log(np.clip(n, 1e-12, None)) / temp
                ptemp = np.exp(logits - np.max(logits))
                pi = _masked_normalize(ptemp, legal)
            action = int(np.random.choice(np.arange(pi.size), p=pi))
            policy_targets.append(pi.astype(np.float32))
            selected_actions.append(action)

        self.last_run_stats = {
            "mode": "tree",
            "simulations": float(sims),
            "value_mean": float(np.mean(sim_values) if sim_values else root_value),
            "value_root": float(root_value),
            "depth_mean": float(np.mean(sim_depths) if sim_depths else 1.0),
            "depth_max": float(np.max(sim_depths) if sim_depths else 1.0),
        }
        value_out = float(np.mean(sim_values) if sim_values else root_value)
        return policy_targets, selected_actions, value_out

    @torch.no_grad()
    def run(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        temperature: float = 1.0,
        env=None,
        len_model: Optional[int] = None,
        enemy_policy_fn=None,
    ) -> tuple[list[np.ndarray], list[int], float]:
        mode = str(getattr(self.cfg, "mode", "proxy") or "proxy").strip().lower()
        if mode == "tree" and env is not None and len_model is not None and hasattr(env, "simulate_step"):
            return self._run_tree(
                obs=obs,
                legal_masks_by_head=legal_masks_by_head,
                temperature=temperature,
                env=env,
                len_model=int(len_model),
                enemy_policy_fn=enemy_policy_fn,
            )
        return self._run_proxy(obs=obs, legal_masks_by_head=legal_masks_by_head, temperature=temperature)
