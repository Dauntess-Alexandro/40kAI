from __future__ import annotations

import math
from collections import OrderedDict
from contextlib import nullcontext
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.utils import unwrap_env


@dataclass
class MCTSConfig:
    simulations: int = 64
    c_puct: float = 1.5
    c_puct_min: float = 1.0
    c_puct_max: float = 2.0
    c_puct_schedule: str = "none"  # none | linear | cosine
    dirichlet_alpha: float = 0.3
    dirichlet_eps: float = 0.25
    top_k_per_head: int = 8
    max_depth: int = 1
    mode: str = "proxy"  # "proxy" | "tree"
    root_dirichlet_only: bool = True
    eval_cache_size: int = 10000
    pw_alpha: float = 1.0
    pw_beta: float = 0.5
    prior_weight_early: float = 0.25
    progress: float = 0.0
    move_count: int = 0
    temperature_opening_moves: int = 12


@dataclass
class MCTSNode:
    prior: float = 0.0
    parent: MCTSNode | None = None
    children: dict[tuple[int, ...], MCTSNode] = field(default_factory=dict)
    visit_count: int = 0
    value_sum: float = 0.0
    action_tuple: tuple[int, ...] | None = None

    def mean_value(self) -> float:
        if self.visit_count <= 0:
            return 0.0
        return float(self.value_sum) / float(self.visit_count)

    def puct_score(self, c_puct: float) -> float:
        if self.visit_count == 0:
            return float("inf")
        parent_visits = 1 if self.parent is None else max(1, int(self.parent.visit_count))
        exploration = float(c_puct) * float(self.prior) * math.sqrt(float(parent_visits)) / (1.0 + float(self.visit_count))
        return self.mean_value() + exploration


class EvalCache:
    """LRU cache for network evaluations keyed by obs + legal masks."""

    def __init__(self, max_size: int = 10000):
        self.max_size = max(1, int(max_size))
        self._cache: OrderedDict[bytes, tuple[list[np.ndarray], float]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _key(obs: np.ndarray, legal_masks_by_head: list[np.ndarray]) -> bytes:
        parts = [np.asarray(obs, dtype=np.float32).tobytes()]
        for m in legal_masks_by_head:
            parts.append(np.asarray(m, dtype=bool).tobytes())
        return b"".join(parts)

    def get(self, obs: np.ndarray, legal_masks_by_head: list[np.ndarray]) -> tuple[list[np.ndarray], float] | None:
        key = self._key(obs, legal_masks_by_head)
        if key not in self._cache:
            self.misses += 1
            return None
        self.hits += 1
        val = self._cache.pop(key)
        self._cache[key] = val
        return val

    def set(self, obs: np.ndarray, legal_masks_by_head: list[np.ndarray], priors: list[np.ndarray], value: float) -> None:
        key = self._key(obs, legal_masks_by_head)
        if key in self._cache:
            self._cache.pop(key)
        elif len(self._cache) >= self.max_size:
            self._cache.popitem(last=False)
        self._cache[key] = (priors, float(value))


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


def adaptive_c_puct(cfg: MCTSConfig) -> float:
    schedule = str(getattr(cfg, "c_puct_schedule", "none") or "none").strip().lower()
    base = float(getattr(cfg, "c_puct", 1.5) or 1.5)
    if schedule == "none":
        return base
    progress = max(0.0, min(1.0, float(getattr(cfg, "progress", 0.0) or 0.0)))
    c_min = float(getattr(cfg, "c_puct_min", 1.0) or 1.0)
    c_max = float(getattr(cfg, "c_puct_max", 2.0) or 2.0)
    if schedule == "cosine":
        import math as _m

        t = 0.5 * (1.0 + _m.cos(_m.pi * progress))
        return c_min + (c_max - c_min) * t
    # linear: early high exploration, late low
    return c_max + (c_min - c_max) * progress


def progressive_widening_allowed(parent_visits: int, num_children: int, pw_alpha: float, pw_beta: float) -> bool:
    if num_children <= 0:
        return True
    if int(parent_visits) <= 0:
        return True
    threshold = float(pw_alpha) * (float(max(1, num_children)) ** float(pw_beta))
    return float(parent_visits) >= threshold


def _joint_action_candidates(
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    top_k_per_head: int,
    max_candidates: int = 64,
) -> list[tuple[int, ...]]:
    per_head_idx: list[list[int]] = []
    for prior, legal in zip(priors, legal_masks):
        legal = np.asarray(legal, dtype=bool)
        legal_idx = np.where(legal)[0]
        if legal_idx.size == 0:
            per_head_idx.append([0])
            continue
        k = max(1, int(top_k_per_head))
        if legal_idx.size <= k:
            per_head_idx.append([int(i) for i in legal_idx])
        else:
            scores = np.asarray(prior[legal_idx], dtype=np.float32)
            top_local = np.argsort(scores)[-k:]
            per_head_idx.append([int(legal_idx[i]) for i in top_local])

    out: list[tuple[int, ...]] = []
    # Greedy Cartesian: start from argmax per head, then add top-scoring variants.
    greedy = tuple(int(np.argmax(np.where(legal_masks[i], priors[i], -1e9))) for i in range(len(priors)))
    out.append(greedy)
    seen = {greedy}
    for head_i, indices in enumerate(per_head_idx):
        for a in indices:
            base = list(greedy)
            base[head_i] = int(a)
            tup = tuple(base)
            if tup not in seen:
                seen.add(tup)
                out.append(tup)
            if len(out) >= max_candidates:
                return out
    return out


class AlphaZeroFactorizedMCTS:
    """
    Factorized AlphaZero-style search:
    - proxy: network priors + Dirichlet + temperature (fast),
    - tree: PUCT MCTS with MCTSNode, eval cache, env rollout.
    """

    def __init__(self, policy_value_net, config: MCTSConfig | None = None, device: torch.device | None = None):
        self.net = policy_value_net
        self.cfg = config or MCTSConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}
        cache_size = int(getattr(self.cfg, "eval_cache_size", 10000) or 10000)
        self._eval_cache = EvalCache(max_size=cache_size)

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
        cached = self._eval_cache.get(obs, legal_masks_by_head)
        if cached is not None:
            return cached
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        priors = [p.squeeze(0).detach().cpu().numpy().astype(np.float32) for p in priors_t]
        value = float(value_t.item())
        self._eval_cache.set(obs, legal_masks_by_head, priors, value)
        return priors, value

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

    def _apply_root_dirichlet(
        self,
        pi: np.ndarray,
        legal: np.ndarray,
        *,
        apply_noise: bool,
    ) -> np.ndarray:
        legal = np.asarray(legal, dtype=bool)
        pi = _masked_normalize(pi, legal)
        legal_count = int(np.sum(legal))
        if apply_noise and legal_count > 1 and float(self.cfg.dirichlet_eps) > 0.0:
            alpha = float(self.cfg.dirichlet_alpha)
            noise = np.random.dirichlet([alpha] * legal_count).astype(np.float32)
            noisy = np.zeros_like(pi, dtype=np.float32)
            noisy[np.where(legal)[0]] = noise
            pi = _masked_normalize(
                (1.0 - float(self.cfg.dirichlet_eps)) * pi + float(self.cfg.dirichlet_eps) * noisy,
                legal,
            )
        return pi

    def _run_proxy(self, *, obs: np.ndarray, legal_masks_by_head: list[np.ndarray], temperature: float) -> tuple[list[np.ndarray], list[int], float]:
        priors, value = self._evaluate_net(obs=obs, legal_masks_by_head=legal_masks_by_head)
        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        temp = max(1e-6, float(temperature))
        for head_idx, prior in enumerate(priors):
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            pi = self._apply_root_dirichlet(prior, legal, apply_noise=True)
            logits = np.log(np.clip(pi, 1e-12, 1.0)) / temp
            ptemp = np.exp(logits - np.max(logits))
            ptemp = _masked_normalize(ptemp, legal)
            if temp <= 1e-3:
                action = int(np.argmax(ptemp))
            else:
                action = int(np.random.choice(np.arange(ptemp.size), p=ptemp))
            policy_targets.append(ptemp.astype(np.float32))
            selected_actions.append(action)
        self.last_run_stats = {
            "mode": "proxy",
            "simulations": 1.0,
            "eval_cache_hits": float(self._eval_cache.hits),
            "eval_cache_misses": float(self._eval_cache.misses),
        }
        return policy_targets, selected_actions, value

    def _restore_env_safe(self, env, snapshot, reset_options: dict | None = None) -> bool:
        if snapshot is None:
            return True
        try:
            if hasattr(env, "restore_state"):
                env.restore_state(snapshot)
                return True
        except Exception:
            pass
        try:
            if hasattr(env, "reset") and reset_options is not None:
                env.reset(options=reset_options)
                return False
        except Exception:
            pass
        return False

    def _expand_root_child(
        self,
        root: MCTSNode,
        action_tuple: tuple[int, ...],
        priors: list[np.ndarray],
        legal_masks: list[np.ndarray],
    ) -> MCTSNode:
        if action_tuple in root.children:
            return root.children[action_tuple]
        joint_prior = 1.0
        for head_i, a in enumerate(action_tuple):
            p = _masked_normalize(priors[head_i], legal_masks[head_i])
            joint_prior *= float(p[int(a)]) if int(a) < p.size else 0.0
        child = MCTSNode(prior=max(1e-8, joint_prior), parent=root, action_tuple=action_tuple)
        root.children[action_tuple] = child
        return child

    def _select_child_puct(self, node: MCTSNode, c_puct: float, legal_action_tuples: set[tuple[int, ...]] | None = None) -> MCTSNode | None:
        best_score = float("-inf")
        best_child: MCTSNode | None = None
        for action_tuple, child in node.children.items():
            if legal_action_tuples is not None and action_tuple not in legal_action_tuples:
                continue
            score = child.puct_score(c_puct)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def _backpropagate(self, path: list[MCTSNode], value: float) -> None:
        v = float(np.clip(float(value), -1.0, 1.0))
        for node in reversed(path):
            node.visit_count += 1
            node.value_sum += v

    def _final_policy_from_visits(
        self,
        root: MCTSNode,
        priors: list[np.ndarray],
        legal_masks: list[np.ndarray],
        temperature: float,
        move_count: int,
    ) -> tuple[list[np.ndarray], list[int]]:
        temp = max(1e-6, float(temperature))
        opening_moves = int(getattr(self.cfg, "temperature_opening_moves", 12) or 12)
        prior_weight = float(getattr(self.cfg, "prior_weight_early", 0.25) or 0.25)
        early = int(move_count) < opening_moves

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        num_heads = len(priors)

        for head_i in range(num_heads):
            legal = np.asarray(legal_masks[head_i], dtype=bool)
            n = priors[head_i].size
            visits = np.zeros(n, dtype=np.float32)
            for action_tuple, child in root.children.items():
                if head_i < len(action_tuple):
                    visits[int(action_tuple[head_i])] += float(child.visit_count)

            visits[~legal] = 0.0
            if float(visits.sum()) <= 1e-12:
                pi = _masked_normalize(priors[head_i], legal)
            else:
                if early and prior_weight > 0.0:
                    prior_vec = _masked_normalize(priors[head_i], legal)
                    blended = (1.0 - prior_weight) * visits + prior_weight * prior_vec * float(max(1, visits.sum()))
                    logits = np.log(np.clip(blended, 1e-12, None)) / temp
                else:
                    logits = np.log(np.clip(visits, 1e-12, None)) / temp
                ptemp = np.exp(logits - np.max(logits))
                pi = _masked_normalize(ptemp, legal)

            if temp <= 1e-3:
                action = int(np.argmax(pi))
            else:
                action = int(np.random.choice(np.arange(pi.size), p=pi))
            policy_targets.append(pi.astype(np.float32))
            selected_actions.append(action)

        return policy_targets, selected_actions

    def _run_tree(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        temperature: float,
        env,
        len_model: int,
        enemy_policy_fn=None,
        reset_options: dict | None = None,
    ) -> tuple[list[np.ndarray], list[int], float]:
        root_priors, root_value = self._evaluate_net(obs=obs, legal_masks_by_head=legal_masks_by_head)
        legal_masks = [np.asarray(m, dtype=bool) for m in legal_masks_by_head]
        priors = []
        for i, prior in enumerate(root_priors):
            legal_topk = self._masked_topk(prior, legal_masks[i])
            p = _masked_normalize(prior, legal_topk)
            if bool(getattr(self.cfg, "root_dirichlet_only", True)):
                p = self._apply_root_dirichlet(p, legal_topk, apply_noise=True)
            priors.append(p)
            legal_masks[i] = legal_topk

        root = MCTSNode(prior=1.0)
        c_puct = adaptive_c_puct(self.cfg)
        sims = max(1, int(getattr(self.cfg, "simulations", 1) or 1))
        max_depth = max(1, int(getattr(self.cfg, "max_depth", 1) or 1))
        pw_alpha = float(getattr(self.cfg, "pw_alpha", 1.0) or 1.0)
        pw_beta = float(getattr(self.cfg, "pw_beta", 0.5) or 0.5)

        candidates = _joint_action_candidates(priors, legal_masks, int(self.cfg.top_k_per_head))
        sim_values: list[float] = []
        sim_depths: list[float] = []

        env_u = unwrap_env(env)
        ordered_keys = ordered_action_keys(int(len_model))

        for _ in range(sims):
            # Progressive widening: add a new child if allowed
            if progressive_widening_allowed(root.visit_count, len(root.children), pw_alpha, pw_beta):
                for action_tuple in candidates:
                    if action_tuple not in root.children:
                        self._expand_root_child(root, action_tuple, priors, legal_masks)
                        break

            # Ensure at least one child
            if not root.children:
                for action_tuple in candidates[: max(1, int(self.cfg.top_k_per_head))]:
                    self._expand_root_child(root, action_tuple, priors, legal_masks)

            child = self._select_child_puct(root, c_puct)
            if child is None or child.action_tuple is None:
                action_list = [int(np.argmax(priors[i])) for i in range(len(priors))]
            else:
                action_list = list(child.action_tuple)

            snapshot = env_u.snapshot_state() if hasattr(env_u, "snapshot_state") else None
            current_obs = np.asarray(obs, dtype=np.float32)
            leaf_value: Optional[float] = None
            depth_reached = 0
            path = [root]
            if child is not None:
                path.append(child)

            sim_ctx = env_u.simulation_mode() if hasattr(env_u, "simulation_mode") else nullcontext(env_u)
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
                            env_u.enemyTurn(trunc=False, policy_fn=enemy_policy_fn)
                            done = bool(getattr(env_u, "game_over", False))
                            info = env_u.get_info()

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
                    restored = self._restore_env_safe(env_u, snapshot, reset_options=reset_options)

            if leaf_value is None:
                leaf_value = float(root_value)
            leaf_value = float(np.clip(float(leaf_value), -1.0, 1.0))
            sim_values.append(leaf_value)
            sim_depths.append(float(depth_reached))
            self._backpropagate(path, leaf_value)
            if snapshot is not None and not restored:
                self.last_run_stats["snapshot_fallback"] = 1.0

        move_count = int(getattr(self.cfg, "move_count", 0) or 0)
        policy_targets, selected_actions = self._final_policy_from_visits(
            root, priors, legal_masks, temperature, move_count
        )

        self.last_run_stats = {
            "mode": "tree",
            "simulations": float(sims),
            "value_mean": float(np.mean(sim_values) if sim_values else root_value),
            "value_root": float(root_value),
            "depth_mean": float(np.mean(sim_depths) if sim_depths else 1.0),
            "depth_max": float(np.max(sim_depths) if sim_depths else 1.0),
            "c_puct": float(c_puct),
            "eval_cache_hits": float(self._eval_cache.hits),
            "eval_cache_misses": float(self._eval_cache.misses),
            "root_children": float(len(root.children)),
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
        reset_options: dict | None = None,
        move_count: int | None = None,
        progress: float | None = None,
    ) -> tuple[list[np.ndarray], list[int], float]:
        if move_count is not None:
            self.cfg.move_count = int(move_count)
        if progress is not None:
            self.cfg.progress = float(progress)
        mode = str(getattr(self.cfg, "mode", "proxy") or "proxy").strip().lower()
        if mode == "tree" and env is not None and len_model is not None:
            return self._run_tree(
                obs=obs,
                legal_masks_by_head=legal_masks_by_head,
                temperature=temperature,
                env=env,
                len_model=int(len_model),
                enemy_policy_fn=enemy_policy_fn,
                reset_options=reset_options,
            )
        return self._run_proxy(obs=obs, legal_masks_by_head=legal_masks_by_head, temperature=temperature)
