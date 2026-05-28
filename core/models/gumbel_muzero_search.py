from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch


# ---------------------------------------------------------------------------
# Search preset configs
# ---------------------------------------------------------------------------

@dataclass
class GumbelMuZeroSearchConfig:
    num_simulations: int = 32
    root_top_k: int = 8
    discount: float = 0.997
    temperature: float = 0.15
    gumbel_scale: float = 1.0
    prior_weight: float = 0.25
    # Sprint 3: batch recurrent_inference calls (True = batch all sims at once)
    batch_recurrent: bool = True
    # B3: tree reuse — warm-start visits/Q from previous search
    tree_reuse: bool = True


SEARCH_PRESETS: dict[str, dict] = {
    "fast": {
        "num_simulations": 16,
        "root_top_k": 4,
        "temperature": 0.2,
        "gumbel_scale": 1.0,
        "prior_weight": 0.3,
    },
    "balanced": {
        "num_simulations": 32,
        "root_top_k": 8,
        "temperature": 0.15,
        "gumbel_scale": 1.0,
        "prior_weight": 0.25,
    },
    "heavy": {
        "num_simulations": 64,
        "root_top_k": 12,
        "temperature": 0.1,
        "gumbel_scale": 0.8,
        "prior_weight": 0.2,
    },
}


def make_search_config(preset: str = "balanced", **overrides) -> GumbelMuZeroSearchConfig:
    kwargs = SEARCH_PRESETS.get(preset, SEARCH_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return GumbelMuZeroSearchConfig(**kwargs)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _masked_softmax(logits: np.ndarray, legal_mask: np.ndarray, temperature: float) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float32).copy()
    m = np.asarray(legal_mask, dtype=bool)
    if x.shape != m.shape:
        return np.ones_like(x, dtype=np.float32) / float(max(1, x.size))
    x[~m] = -1e9
    x = x / max(1e-6, float(temperature))
    x = x - np.max(x[m])
    p = np.exp(x)
    p[~m] = 0.0
    s = float(p.sum())
    if s <= 1e-12:
        p = m.astype(np.float32)
        s = float(p.sum())
    return p / max(1e-12, s)


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

class GumbelMuZeroSearch:
    """
    Factorized root-search with proper Gumbel-UCB and prior mixing.

    Each head independently:
    1. Samples top-k candidates via Gumbel trick on policy prior
    2. Evaluates each candidate via recurrent_inference (reward + value)
    3. Builds Q-values with UCB exploration bonus
    4. Mixes Q-values with prior: π = (1-α)*softmax(Q/T) + α*prior
    5. Selects action deterministically or stochastically
    """

    def __init__(
        self,
        net,
        config: Optional[GumbelMuZeroSearchConfig] = None,
        device: Optional[torch.device] = None,
    ):
        self.net = net
        self.cfg = config or GumbelMuZeroSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}

        # B3: Real tree reuse — warm-start visits/Q from previous search
        self._tree_reuse_enabled = bool(getattr(self.cfg, "tree_reuse", True))
        self._prev_visits: dict[int, np.ndarray] | None = None
        self._prev_q_sums: dict[int, np.ndarray] | None = None
        self._prev_latent: torch.Tensor | None = None
        self._prev_legal_masks: list[np.ndarray] | None = None
        self._last_selected_actions: list[int] | None = None

    def _can_warm_start(self, legal_masks_by_head: list[np.ndarray]) -> bool:
        """Check if we can warm-start from previous tree state."""
        if not self._tree_reuse_enabled:
            return False
        if self._prev_latent is None or self._prev_visits is None:
            return False
        if self._prev_legal_masks is None:
            return False
        # Shapes must match
        if len(legal_masks_by_head) != len(self._prev_legal_masks):
            return False
        for a, b in zip(legal_masks_by_head, self._prev_legal_masks):
            if a.shape != b.shape:
                return False
        return True

    def _save_tree_state(
        self,
        visits_by_head: dict[int, np.ndarray],
        q_sums_by_head: dict[int, np.ndarray],
        latent: torch.Tensor,
        legal_masks_by_head: list[np.ndarray],
    ) -> None:
        """Save tree state after successful search for reuse in next move."""
        self._prev_visits = {k: v.copy() for k, v in visits_by_head.items()}
        self._prev_q_sums = {k: v.copy() for k, v in q_sums_by_head.items()}
        self._prev_latent = latent.detach().clone()
        self._prev_legal_masks = [m.copy() for m in legal_masks_by_head]

    def clear_tree_state(self) -> None:
        """Clear saved tree state (e.g., when game state changes significantly)."""
        self._prev_visits = None
        self._prev_q_sums = None
        self._prev_latent = None
        self._prev_legal_masks = None
        self._last_selected_actions = None

    @torch.no_grad()
    def run(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        deterministic: bool = True,
    ) -> tuple[list[np.ndarray], list[np.ndarray], list[int], float]:
        """Returns (policy_targets, behavior_logits, selected_actions, value_out).

        behavior_logits are the pre-softmax raw network outputs from the root —
        used as the behavior policy for V-trace importance-sampling correction.
        """
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [
            torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0)
            for m in legal_masks_by_head
        ]
        root_logits, root_value, _root_reward, latent = self.net.initial_inference(
            obs_t, masks_by_head=masks_t
        )

        sims = max(1, int(self.cfg.num_simulations))
        root_top_k = max(1, int(self.cfg.root_top_k))
        discount = float(self.cfg.discount)
        temp = float(self.cfg.temperature)
        gumbel_scale = float(self.cfg.gumbel_scale)
        prior_weight = float(self.cfg.prior_weight)

        # Greedy base action (fallback when no legal actions)
        base_action = [int(torch.argmax(head.squeeze(0), dim=0).item()) for head in root_logits]

        policy_targets: list[np.ndarray] = []
        behavior_logits: list[np.ndarray] = []  # ← A3: pre-softmax root logits
        selected_actions: list[int] = []
        value_samples: list[float] = []

        # B3: Tree reuse — initialize visits/q_sums with warm-start from previous search
        visits_by_head: dict[int, np.ndarray] = {}
        q_sums_by_head: dict[int, np.ndarray] = {}

        for head_idx, head_logits in enumerate(root_logits):
            logits_np = head_logits.squeeze(0).detach().cpu().numpy().astype(np.float32)
            legal = np.asarray(legal_masks_by_head[head_idx], dtype=bool)
            legal_idx = np.where(legal)[0]

            # A3: store raw logits BEFORE any masking / mixing
            behavior_logits.append(logits_np.copy())

            if legal_idx.size == 0:
                policy_targets.append(
                    np.ones_like(logits_np, dtype=np.float32) / float(max(1, logits_np.size))
                )
                selected_actions.append(0)
                continue

            # Prior probabilities from root policy
            prior_np = np.full_like(logits_np, -1e9)
            prior_np[legal_idx] = logits_np[legal_idx]
            prior_np -= prior_np[legal_idx].max()
            prior_exp = np.exp(prior_np)
            prior_exp[~legal] = 0.0
            prior_sum = prior_exp.sum()
            prior_probs = prior_exp / max(prior_sum, 1e-12)

            # Top-k selection via Gumbel trick on legal actions
            local_logits = logits_np[legal_idx]
            gumbel = np.random.gumbel(
                loc=0.0, scale=max(1e-6, gumbel_scale), size=legal_idx.size
            ).astype(np.float32)
            ranking = np.argsort(local_logits + gumbel)[::-1]
            top_local = ranking[: min(root_top_k, ranking.size)]
            candidate_actions = legal_idx[top_local]

            # B3: Per-action statistics — try warm-start from previous tree
            visits = np.zeros(logits_np.size, dtype=np.float32)
            q_sums = np.zeros(logits_np.size, dtype=np.float32)

            # Warm-start: use previous search tree for heads that match
            if self._can_warm_start(legal_masks_by_head):
                prev_v = self._prev_visits.get(head_idx)
                prev_q = self._prev_q_sums.get(head_idx)
                if prev_v is not None and prev_q is not None:
                    # Copy previous visits/q_sums that are still valid (shape match)
                    copy_len = min(len(visits), len(prev_v))
                    if copy_len > 0:
                        visits[:copy_len] = prev_v[:copy_len]
                        q_sums[:copy_len] = prev_q[:copy_len]

            if bool(getattr(self.cfg, "batch_recurrent", True)) and sims > 1:
                # Batch all sims into a single recurrent_inference call.
                # latent is the same root latent for all sims — expand it.
                sim_candidates = [
                    int(candidate_actions[s % candidate_actions.size]) for s in range(sims)
                ]
                action_vecs = [list(base_action) for _ in range(sims)]
                for s_idx, cand in enumerate(sim_candidates):
                    action_vecs[s_idx][head_idx] = cand
                action_t_batch = torch.tensor(action_vecs, dtype=torch.long, device=self.device)
                latent_batch = latent.expand(sims, -1)
                masks_t_batch = [m.expand(sims, -1) for m in masks_t]

                with torch.no_grad():
                    _p_batch, val_batch, rew_batch, _nl = self.net.recurrent_inference(
                        latent_batch, action_t_batch, masks_by_head=masks_t_batch
                    )

                for s_idx, cand in enumerate(sim_candidates):
                    q = float(rew_batch[s_idx].item()) + discount * float(val_batch[s_idx].item())
                    visits[cand] += 1.0
                    q_sums[cand] += q
                    value_samples.append(q)
            else:
                for sim in range(sims):
                    # Cycle through candidates; each gets ~equal budget
                    candidate = int(candidate_actions[sim % candidate_actions.size])
                    action_vec = list(base_action)
                    action_vec[head_idx] = candidate
                    action_t = torch.tensor([action_vec], dtype=torch.long, device=self.device)

                    _p, val_next, rew_next, _nl = self.net.recurrent_inference(
                        latent, action_t, masks_by_head=masks_t
                    )
                    q = float(rew_next.item()) + discount * float(val_next.item())

                    visits[candidate] += 1.0
                    q_sums[candidate] += q
                    value_samples.append(q)

            # Store visits/q_sums for tree reuse
            visits_by_head[head_idx] = visits.copy()
            q_sums_by_head[head_idx] = q_sums.copy()

            # Mean Q-values for visited actions; fallback to logit for unvisited
            q_values = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), logits_np)
            q_values[~legal] = -1e9

            # UCB bonus on Q-values (sqrt exploration)
            total_visits = visits.sum() + 1.0
            ucb_bonus = np.sqrt(np.log(total_visits + 1.0) / (visits + 1.0))
            ucb_q = np.where(legal, q_values + 0.3 * ucb_bonus, -1e9)

            # Softmax over Q-values
            q_soft = _masked_softmax(ucb_q, legal_mask=legal, temperature=temp)

            # Prior mixing: π = (1-α)*softmax(Q/T) + α*prior
            mixed = (1.0 - prior_weight) * q_soft + prior_weight * prior_probs
            mixed[~legal] = 0.0
            mixed_sum = mixed.sum()
            if mixed_sum > 1e-12:
                mixed /= mixed_sum
            else:
                mixed = legal.astype(np.float32) / float(legal.sum())

            if deterministic:
                action = int(np.argmax(mixed))
            else:
                action = int(np.random.choice(np.arange(mixed.size), p=mixed))

            policy_targets.append(mixed.astype(np.float32))
            selected_actions.append(action)

        self.last_run_stats = {
            "mode": 1.0,
            "simulations": float(sims),
            "root_value": float(root_value.item()),
            "q_mean": float(np.mean(value_samples) if value_samples else float(root_value.item())),
        }
        value_out = float(
            np.mean(value_samples) if value_samples else float(root_value.item())
        )

        # B3: Save tree state for warm-start in next search
        self._save_tree_state(visits_by_head, q_sums_by_head, latent, legal_masks_by_head)
        self._last_selected_actions = selected_actions.copy()

        return policy_targets, behavior_logits, selected_actions, value_out


# ---------------------------------------------------------------------------
# Batched search (variant B throughput): one forward over N environments
# ---------------------------------------------------------------------------

@torch.no_grad()
def run_batched(
    *,
    net,
    cfg: GumbelMuZeroSearchConfig,
    device: torch.device,
    requests: list[dict],
    deterministic: bool = False,
    warm_start: dict[int, dict] | None = None,
) -> list[dict]:
    """Батч-вариант GumbelMuZeroSearch.run по средам.

    requests: список dict с ключами env_id, obs (np.ndarray), legal_masks_by_head (list[np.ndarray]).
    Возвращает список dict (в порядке requests): env_id, selected_actions, policy_targets,
    behavior_logits, value_est, _visits_by_head, _q_sums_by_head, _legal_masks
    (последние три — для tree-reuse в BatchedGumbelMuZeroSearch).

    warm_start: optional {env_id: {"visits": {h: arr}, "q_sums": {h: arr},
    "legal_masks": [arr]}} — пред-заполнение visits/q_sums.

    Числовая логика повторяет GumbelMuZeroSearch.run, но recurrent_inference батчится
    по средам внутри каждого head'а: один forward на N*sims строк вместо N форвардов.
    Для эквивалентности sequential-пути розыгрыш Gumbel идёт env-major, head-minor,
    и head'ы без легальных действий не тянут RNG.
    """
    N = len(requests)
    if N == 0:
        return []

    sims = max(1, int(cfg.num_simulations))
    root_top_k = max(1, int(cfg.root_top_k))
    discount = float(cfg.discount)
    temp = float(cfg.temperature)
    gumbel_scale = float(cfg.gumbel_scale)
    prior_weight = float(cfg.prior_weight)

    num_heads = len(requests[0]["legal_masks_by_head"])

    # --- Батч-инференс корня ---
    obs_batch = torch.tensor(
        np.stack([np.asarray(r["obs"], dtype=np.float32) for r in requests], axis=0),
        device=device,
    )
    masks_batch = []
    for h in range(num_heads):
        mh = np.stack(
            [np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool) for n in range(N)],
            axis=0,
        )
        masks_batch.append(torch.as_tensor(mh, dtype=torch.bool, device=device))

    root_logits, root_value, _root_reward, latent = net.initial_inference(
        obs_batch, masks_by_head=masks_batch
    )
    root_logits_np = [
        root_logits[h].detach().cpu().numpy().astype(np.float32) for h in range(num_heads)
    ]
    root_value_np = root_value.detach().cpu().numpy().reshape(-1).astype(np.float32)
    base_action = np.stack([rl.argmax(axis=1) for rl in root_logits_np], axis=1)  # [N, num_heads]

    # --- Candidate-выборка (RNG-порядок: env-major, head-minor — как sequential) ---
    candidates: list[list] = [[None] * num_heads for _ in range(N)]
    legal_np: list[list] = [[None] * num_heads for _ in range(N)]
    behavior_logits: list[list] = [[None] * num_heads for _ in range(N)]
    for n in range(N):
        for h in range(num_heads):
            logits_np = root_logits_np[h][n]
            legal = np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool)
            legal_np[n][h] = legal
            behavior_logits[n][h] = logits_np.copy()
            legal_idx = np.where(legal)[0]
            if legal_idx.size == 0:
                candidates[n][h] = np.empty(0, dtype=np.int64)
                continue
            local_logits = logits_np[legal_idx]
            gumbel = np.random.gumbel(
                loc=0.0, scale=max(1e-6, gumbel_scale), size=legal_idx.size
            ).astype(np.float32)
            ranking = np.argsort(local_logits + gumbel)[::-1]
            top_local = ranking[: min(root_top_k, ranking.size)]
            candidates[n][h] = legal_idx[top_local].astype(np.int64)

    # --- Аккумуляторы visits/q_sums (+ warm-start) ---
    visits = [
        [np.zeros(root_logits_np[h].shape[1], dtype=np.float32) for h in range(num_heads)]
        for _ in range(N)
    ]
    q_sums = [
        [np.zeros(root_logits_np[h].shape[1], dtype=np.float32) for h in range(num_heads)]
        for _ in range(N)
    ]
    value_samples: list[list[float]] = [[] for _ in range(N)]

    if warm_start:
        for n in range(N):
            env_id = int(requests[n].get("env_id", n))
            ws = warm_start.get(env_id)
            if not ws:
                continue
            prev_masks = ws.get("legal_masks")
            if prev_masks is None or len(prev_masks) != num_heads:
                continue
            if any(prev_masks[h].shape != legal_np[n][h].shape for h in range(num_heads)):
                continue
            for h in range(num_heads):
                pv = ws["visits"].get(h)
                pq = ws["q_sums"].get(h)
                if pv is None or pq is None:
                    continue
                clen = min(len(visits[n][h]), len(pv))
                if clen > 0:
                    visits[n][h][:clen] = pv[:clen]
                    q_sums[n][h][:clen] = pq[:clen]

    # --- Батч-recurrent по head'ам: один forward на N*sims строк ---
    for h in range(num_heads):
        active = [n for n in range(N) if candidates[n][h].size > 0]
        if not active:
            continue
        rows_action: list[np.ndarray] = []
        env_of_row: list[int] = []
        cand_of_row: list[int] = []
        for n in active:
            cand = candidates[n][h]
            for s in range(sims):
                c = int(cand[s % cand.size])
                av = base_action[n].copy()
                av[h] = c
                rows_action.append(av)
                env_of_row.append(n)
                cand_of_row.append(c)
        idx_t = torch.tensor(env_of_row, dtype=torch.long, device=device)
        latent_rep = latent.index_select(0, idx_t)
        action_t = torch.tensor(np.asarray(rows_action), dtype=torch.long, device=device)
        masks_rep = [masks_batch[h2].index_select(0, idx_t) for h2 in range(num_heads)]
        _p, val_b, rew_b, _nl = net.recurrent_inference(
            latent_rep, action_t, masks_by_head=masks_rep
        )
        val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float32)
        rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float32)
        for row in range(len(env_of_row)):
            n = env_of_row[row]
            c = cand_of_row[row]
            q = float(rew_b[row]) + discount * float(val_b[row])
            visits[n][h][c] += 1.0
            q_sums[n][h][c] += q
            value_samples[n].append(q)

    # --- Пост-обработка (numpy, как sequential): UCB → softmax → prior-mix → select ---
    results: list[dict] = []
    for n in range(N):
        policy_targets: list[np.ndarray] = []
        selected: list[int] = []
        v_by_head: dict[int, np.ndarray] = {}
        q_by_head: dict[int, np.ndarray] = {}
        for h in range(num_heads):
            logits_np = root_logits_np[h][n]
            legal = legal_np[n][h]
            legal_idx = np.where(legal)[0]
            v_by_head[h] = visits[n][h].copy()
            q_by_head[h] = q_sums[n][h].copy()
            if legal_idx.size == 0:
                policy_targets.append(
                    np.ones_like(logits_np, dtype=np.float32) / float(max(1, logits_np.size))
                )
                selected.append(0)
                continue
            prior_np = np.full_like(logits_np, -1e9)
            prior_np[legal_idx] = logits_np[legal_idx]
            prior_np -= prior_np[legal_idx].max()
            prior_exp = np.exp(prior_np)
            prior_exp[~legal] = 0.0
            prior_probs = prior_exp / max(prior_exp.sum(), 1e-12)

            vv = visits[n][h]
            qq = q_sums[n][h]
            q_values = np.where(vv > 0, qq / np.maximum(vv, 1.0), logits_np)
            q_values[~legal] = -1e9
            total_visits = vv.sum() + 1.0
            ucb_bonus = np.sqrt(np.log(total_visits + 1.0) / (vv + 1.0))
            ucb_q = np.where(legal, q_values + 0.3 * ucb_bonus, -1e9)
            q_soft = _masked_softmax(ucb_q, legal_mask=legal, temperature=temp)
            mixed = (1.0 - prior_weight) * q_soft + prior_weight * prior_probs
            mixed[~legal] = 0.0
            ms = mixed.sum()
            mixed = mixed / ms if ms > 1e-12 else legal.astype(np.float32) / float(legal.sum())
            action = (
                int(np.argmax(mixed))
                if deterministic
                else int(np.random.choice(np.arange(mixed.size), p=mixed))
            )
            policy_targets.append(mixed.astype(np.float32))
            selected.append(action)
        value_out = float(np.mean(value_samples[n]) if value_samples[n] else root_value_np[n])
        results.append(
            {
                "env_id": int(requests[n].get("env_id", n)),
                "selected_actions": selected,
                "policy_targets": policy_targets,
                "behavior_logits": behavior_logits[n],
                "value_est": value_out,
                "_visits_by_head": v_by_head,
                "_q_sums_by_head": q_by_head,
                "_legal_masks": [m.copy() for m in legal_np[n]],
            }
        )
    return results
