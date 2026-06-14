from __future__ import annotations

from contextlib import nullcontext
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch

from core.models.action_contract import action_tensor_to_dict, ordered_action_keys
from core.models.alphazero_mcts import EvalCache, _masked_normalize
from core.models.utils import unwrap_env


@dataclass
class GumbelAZSearchConfig:
    num_simulations: int = 32          # бюджет SH на голову
    num_considered_actions: int = 8    # m: размер Gumbel top-k
    max_depth: int = 1                 # v1 = 1 (задел под дерево)
    value_scale: float = 0.1           # c_scale в sigma(q)
    c_visit: float = 50.0              # c_visit в sigma(q)
    temperature_opening_moves: int = 12
    eval_cache_size: int = 10000
    batch_eval_size: int = 16
    simulate_enemy: bool = True
    joint_action: bool = False     # координатный режим: следующие головы видят выбор предыдущих
    mode: str = "gumbel"


def sequential_halving_keep_schedule(m: int) -> list[int]:
    """Сколько кандидатов остаётся после каждой фазы SH (включая старт m и финал 1)."""
    m = max(1, int(m))
    sched = [m]
    k = m
    while k > 1:
        k = max(1, k // 2)
        sched.append(k)
    return sched


def _sigma(q: np.ndarray, *, c_visit: float, value_scale: float, max_visit: float) -> np.ndarray:
    return (float(c_visit) + float(max_visit)) * float(value_scale) * np.asarray(q, dtype=np.float32)


def _terminal_value_from_info(info: dict[str, Any]) -> float | None:
    winner = str((info or {}).get("winner", "") or "").strip().lower()
    end_reason = str((info or {}).get("end reason", "") or "").strip().lower()
    if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
        return 1.0
    if winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
        return -1.0
    if str(end_reason).startswith("turn_limit"):
        return 0.0
    return None


class GumbelAlphaZeroSearch:
    """Gumbel AlphaZero, вариант A: per-head Gumbel top-k + Sequential Halving, depth-1.

    Кандидаты оцениваются через реальный env-шаг (+ ход врага) и value-сеть.
    Контракт run() совпадает с AlphaZeroFactorizedMCTS.run() — drop-in для актёра.

    evaluator: опционально (LocalNetEvaluator/RemoteEvaluator) — тот же шов, что у AZ
      MCTS; None → self.net.infer + внутренний EvalCache.
    """

    def __init__(self, policy_value_net, config: GumbelAZSearchConfig | None = None,
                 device: torch.device | None = None, *, evaluator=None):
        self.net = policy_value_net
        self.cfg = config or GumbelAZSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}
        self._eval_cache = EvalCache(max_size=int(getattr(self.cfg, "eval_cache_size", 10000) or 10000))
        self._evaluator = evaluator

    # --- net eval (reuse evaluator seam) ---
    def _evaluate_net(self, obs: np.ndarray, legal_masks_by_head: list[np.ndarray]):
        if self._evaluator is not None:
            return self._evaluator.evaluate_one(obs, legal_masks_by_head)
        cached = self._eval_cache.get(obs, legal_masks_by_head)
        if cached is not None:
            return cached
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0) for m in legal_masks_by_head]
        priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        priors = [p.squeeze(0).detach().cpu().numpy().astype(np.float32) for p in priors_t]
        value = float(value_t.reshape(-1)[0].item())
        self._eval_cache.set(obs, legal_masks_by_head, priors, value)
        return priors, value

    def _evaluate_value_batch(self, leaves: list[dict]) -> list[float]:
        n = len(leaves)
        if n == 0:
            return []

        self._leaf_eval_requests = int(getattr(self, "_leaf_eval_requests", 0)) + n
        self._leaf_eval_batches = int(getattr(self, "_leaf_eval_batches", 0)) + 1
        self._leaf_eval_batch_max = max(int(getattr(self, "_leaf_eval_batch_max", 0)), n)

        unique_leaves: list[dict] = []
        remap: list[int] = []
        seen: dict[bytes, int] = {}
        for leaf in leaves:
            key = EvalCache._key(leaf["obs"], leaf["legal_masks"])
            unique_idx = seen.get(key)
            if unique_idx is None:
                unique_idx = len(unique_leaves)
                seen[key] = unique_idx
                unique_leaves.append(leaf)
            remap.append(unique_idx)

        dedup_hits = n - len(unique_leaves)
        if dedup_hits > 0:
            self._leaf_eval_dedup_hits = int(getattr(self, "_leaf_eval_dedup_hits", 0)) + dedup_hits

        if self._evaluator is not None:
            unique_values = [float(v) for v in self._evaluator.evaluate_batch(unique_leaves)]
            return [float(unique_values[i]) for i in remap]

        values: list[float | None] = [None] * len(unique_leaves)
        uncached: list[int] = []
        for i, leaf in enumerate(unique_leaves):
            c = self._eval_cache.get(leaf["obs"], leaf["legal_masks"])
            if c is not None:
                values[i] = float(c[1])
            else:
                uncached.append(i)
        if uncached:
            obs_batch = np.stack([unique_leaves[i]["obs"] for i in uncached])
            obs_t = torch.tensor(obs_batch, dtype=torch.float32, device=self.device)
            num_heads = len(unique_leaves[uncached[0]]["legal_masks"])
            masks_t = []
            for h in range(num_heads):
                hm = np.stack([np.asarray(unique_leaves[i]["legal_masks"][h], dtype=bool) for i in uncached])
                masks_t.append(torch.as_tensor(hm, dtype=torch.bool, device=self.device))
            with torch.no_grad():
                priors_t, values_t = self.net.infer(obs_t, masks_by_head=masks_t)
            for j, i in enumerate(uncached):
                priors_np = [priors_t[h][j].detach().cpu().numpy().astype(np.float32) for h in range(num_heads)]
                val = float(values_t.reshape(-1)[j].item())
                self._eval_cache.set(unique_leaves[i]["obs"], unique_leaves[i]["legal_masks"], priors_np, val)
                values[i] = val
        unique_values = [float(v if v is not None else 0.0) for v in values]
        return [float(unique_values[i]) for i in remap]

    def _restore_env_safe(self, env_u, snapshot, reset_options) -> None:
        if snapshot is None:
            return
        try:
            if hasattr(env_u, "restore_state"):
                env_u.restore_state(snapshot)
                return
        except Exception:
            pass
        try:
            if hasattr(env_u, "reset") and reset_options is not None:
                env_u.reset(options=reset_options)
        except Exception:
            pass

    def _rollout_leaf(self, *, env, env_u, snapshot, action_list, len_model, ordered_keys,
                      enemy_policy_fn, reset_options) -> dict:
        """Один depth-1 env-шаг action_list (+ход врага). Возвращает leaf dict.

        leaf: {obs, legal_masks, terminal_value(None|float), needs_net_eval(bool)}.
        Гарантированно восстанавливает env в исходное состояние (snapshot).
        """
        leaf = {"obs": np.asarray([], dtype=np.float32), "legal_masks": [],
                "terminal_value": None, "needs_net_eval": False}
        sim_ctx = env_u.simulation_mode() if hasattr(env_u, "simulation_mode") else nullcontext(env_u)
        with sim_ctx:
            try:
                action_dict = action_tensor_to_dict(
                    torch.tensor([list(action_list)], dtype=torch.long), len_model=int(len_model)
                )
                next_obs, _r, done, trunc, info = env.step(action_dict)
                if not bool(done or trunc) and bool(self.cfg.simulate_enemy):
                    env_u.enemyTurn(trunc=False, policy_fn=enemy_policy_fn)
                    done = bool(getattr(env_u, "game_over", False))
                    info = env_u.get_info()
                term = _terminal_value_from_info(info or {})
                leaf["obs"] = np.asarray(next_obs, dtype=np.float32)
                if term is not None or bool(done or trunc):
                    leaf["terminal_value"] = float(term if term is not None else 0.0)
                else:
                    legal_dict = env_u.get_legal_action_masks_by_head(side="model")
                    leaf["legal_masks"] = [legal_dict[k] for k in ordered_keys]
                    leaf["needs_net_eval"] = True
            finally:
                self._restore_env_safe(env_u, snapshot, reset_options)
        return leaf

    def _search_head(
        self, *, head_idx, base_action, legal, prior, root_value,
        leaf_eval_fn=None, leaf_eval_batch_fn=None,
    ):
        """SH по одной голове. leaf_eval_fn(action_list)->q (через env) или None (нет env).

        Возвращает (pi: np.ndarray, selected_action: int).
        """
        legal = np.asarray(legal, dtype=bool)
        legal_idx = np.where(legal)[0]
        prior = _masked_normalize(prior, legal)
        logits = np.log(np.clip(prior, 1e-12, 1.0)).astype(np.float32)

        if legal_idx.size <= 1:
            a = int(legal_idx[0]) if legal_idx.size == 1 else 0
            return prior.astype(np.float32), a

        # Gumbel top-m
        g = np.random.gumbel(size=legal.size).astype(np.float32)
        g_legal = np.where(legal, g, np.float32(-1e30))
        base_score = logits + g_legal
        m = int(min(int(self.cfg.num_considered_actions), legal_idx.size))
        order = legal_idx[np.argsort(base_score[legal_idx])[::-1]]
        candidates = list(order[:m])

        visits = np.zeros(legal.size, dtype=np.float32)
        q_sums = np.zeros(legal.size, dtype=np.float32)
        n = max(1, int(self.cfg.num_simulations))
        schedule = sequential_halving_keep_schedule(m)
        phases = max(1, len(schedule) - 1)

        remaining = list(candidates)
        for phase in range(phases):
            per = max(1, n // (phases * max(1, len(remaining))))
            work: list[tuple[int, list[int]]] = []
            for a in remaining:
                for _ in range(per):
                    action_vec = list(base_action)
                    action_vec[head_idx] = int(a)
                    work.append((int(a), action_vec))
            if leaf_eval_batch_fn is not None and work:
                qs = list(leaf_eval_batch_fn([action_vec for _a, action_vec in work]))
            else:
                qs = [
                    leaf_eval_fn(action_vec) if leaf_eval_fn is not None else float(root_value)
                    for _a, action_vec in work
                ]
            if len(qs) != len(work):
                raise RuntimeError(
                    "GumbelAlphaZeroSearch._search_head: leaf_eval returned wrong number of values. "
                    "Что делать: проверьте batched leaf evaluator для Gumbel AlphaZero."
                )
            for (a, _action_vec), q in zip(work, qs):
                if q is None:
                    q = float(root_value)
                visits[int(a)] += 1.0
                q_sums[int(a)] += float(q)
            # ранжируем выживших по g+logit+sigma(qhat)
            keep = schedule[phase + 1]
            qmean = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), float(root_value))
            qn = _normalize01(qmean, remaining)
            max_visit = float(visits.max()) if visits.size else 0.0
            score = base_score + _sigma(qn, c_visit=self.cfg.c_visit,
                                        value_scale=self.cfg.value_scale, max_visit=max_visit)
            remaining = sorted(remaining, key=lambda a: float(score[int(a)]), reverse=True)[:keep]

        winner = int(remaining[0])

        # completed-Q policy target по всем легальным
        qmean_all = np.where(visits > 0, q_sums / np.maximum(visits, 1.0), float(root_value))
        completed = _normalize01(qmean_all, list(legal_idx))
        max_visit = float(visits.max()) if visits.size else 0.0
        target_logits = logits + _sigma(completed, c_visit=self.cfg.c_visit,
                                        value_scale=self.cfg.value_scale, max_visit=max_visit)
        target_logits = np.where(legal, target_logits, np.float32(-1e30))
        target_logits = target_logits - np.max(target_logits[legal])
        pi = np.exp(target_logits).astype(np.float32)
        pi[~legal] = 0.0
        pi = _masked_normalize(pi, legal)
        return pi, winner

    @torch.no_grad()
    def run(self, *, obs, legal_masks_by_head, temperature: float = 1.0, env=None,
            len_model: int | None = None, enemy_policy_fn=None, reset_options=None,
            move_count: int | None = None, progress: float | None = None):
        self._leaf_eval_requests = 0
        self._leaf_eval_batches = 0
        self._leaf_eval_batch_max = 0
        self._leaf_eval_dedup_hits = 0

        legal_masks = [np.asarray(m, dtype=bool) for m in legal_masks_by_head]
        priors, root_value = self._evaluate_net(obs=np.asarray(obs, dtype=np.float32),
                                                legal_masks_by_head=legal_masks)
        num_heads = len(priors)
        base_action = [int(np.argmax(np.where(legal_masks[i], priors[i], -1e30)))
                       for i in range(num_heads)]

        env_u = unwrap_env(env) if env is not None else None
        ordered_keys = ordered_action_keys(int(len_model)) if (env is not None and len_model is not None) else []
        use_env = env is not None and len_model is not None and env_u is not None and hasattr(env_u, "snapshot_state")

        def _make_leaf_eval_batch():
            if not use_env:
                return lambda action_vecs: [float(root_value) for _ in action_vecs]

            chunk_size = max(1, int(getattr(self.cfg, "batch_eval_size", 1) or 1))

            def _flush_pending(out: list[float], pending: list[dict], indices: list[int]) -> None:
                if not pending:
                    return
                vals = self._evaluate_value_batch(pending)
                for idx, val in zip(indices, vals):
                    out[int(idx)] = float(val)
                pending.clear()
                indices.clear()

            def _eval_batch(action_vecs):
                out = [float(root_value) for _ in action_vecs]
                pending: list[dict] = []
                pending_indices: list[int] = []
                for idx, action_vec in enumerate(action_vecs):
                    snap = env_u.snapshot_state()
                    leaf = self._rollout_leaf(
                        env=env, env_u=env_u, snapshot=snap, action_list=action_vec,
                        len_model=int(len_model), ordered_keys=ordered_keys,
                        enemy_policy_fn=enemy_policy_fn, reset_options=reset_options,
                    )
                    terminal_value = leaf.get("terminal_value")
                    if terminal_value is not None:
                        out[idx] = float(terminal_value)
                    elif bool(leaf.get("needs_net_eval", False)):
                        pending.append(leaf)
                        pending_indices.append(idx)
                        if len(pending) >= chunk_size:
                            _flush_pending(out, pending, pending_indices)
                    else:
                        out[idx] = float(root_value)
                _flush_pending(out, pending, pending_indices)
                return out

            return _eval_batch

        leaf_eval_batch_fn = _make_leaf_eval_batch()

        def leaf_eval_fn(action_vec):
            vals = leaf_eval_batch_fn([action_vec])
            return float(vals[0]) if vals else float(root_value)

        policy_targets: list[np.ndarray] = []
        selected_actions: list[int] = []
        for h in range(num_heads):
            pi, a = self._search_head(
                head_idx=h, base_action=base_action, legal=legal_masks[h],
                prior=priors[h], root_value=root_value,
                leaf_eval_fn=leaf_eval_fn, leaf_eval_batch_fn=leaf_eval_batch_fn,
            )
            opening = int(getattr(self.cfg, "temperature_opening_moves", 12) or 12)
            if move_count is not None:
                # обучение: дебютная стохастика из улучшённой политики (как было)
                if int(move_count) < opening and float(temperature) > 1e-3:
                    a = int(np.random.choice(np.arange(pi.size), p=pi))
            elif float(temperature) <= 1e-3:
                # инференс, T≈0: детерминированно — argmax улучшённой политики (сильно, воспроизводимо)
                a = int(np.argmax(pi))
            else:
                # инференс, T>0: сэмпл из pi^(1/T). Низкая T → почти argmax, высокая → разнообразнее
                p = np.power(pi.astype(np.float64), 1.0 / max(1e-3, float(temperature)))
                s = float(p.sum())
                a = int(np.random.choice(np.arange(pi.size), p=(p / s))) if s > 0 else int(np.argmax(pi))
            policy_targets.append(pi.astype(np.float32))
            selected_actions.append(int(a))
            # joint-action (координатный): следующие головы ищут уже с учётом выбора текущей
            if bool(getattr(self.cfg, "joint_action", False)):
                base_action[h] = int(a)

        self.last_run_stats = {
            "mode": 1.0,
            "simulations": float(self.cfg.num_simulations),
            "root_value": float(root_value),
            "eval_cache_hits": float(self._eval_cache.hits),
            "eval_cache_misses": float(self._eval_cache.misses),
            "leaf_eval_requests": float(getattr(self, "_leaf_eval_requests", 0)),
            "leaf_eval_batches": float(getattr(self, "_leaf_eval_batches", 0)),
            "leaf_eval_batch_max": float(getattr(self, "_leaf_eval_batch_max", 0)),
            "leaf_eval_dedup_hits": float(getattr(self, "_leaf_eval_dedup_hits", 0)),
        }
        return policy_targets, selected_actions, float(root_value)


def build_gumbel_inference_search(net, *, num_simulations: int, num_considered_actions: int,
                                  joint_action: bool = False, value_scale: float = 0.1,
                                  c_visit: float = 50.0, device=None, evaluator=None):
    """Фабрика Gumbel-поиска для инференса (eval/play/Viewer).

    depth-1, simulate_enemy=False (лист = оценка сети после хода модели, без тяжёлой
    эвристики врага), без дебютной стохастики. joint_action прокидывается как при обучении.
    Контракт run() тот же → вызывающий берёт selected_actions (победители SH).
    """
    cfg = GumbelAZSearchConfig(
        num_simulations=max(1, int(num_simulations)),
        num_considered_actions=max(2, int(num_considered_actions)),
        max_depth=1,
        value_scale=float(value_scale),
        c_visit=float(c_visit),
        temperature_opening_moves=0,
        simulate_enemy=False,
        joint_action=bool(joint_action),
    )
    return GumbelAlphaZeroSearch(net, config=cfg, device=device, evaluator=evaluator)


def _normalize01(values: np.ndarray, idx_subset: list[int]) -> np.ndarray:
    """Min-max нормировка значений по подмножеству индексов в [0,1] (для sigma)."""
    out = np.zeros_like(values, dtype=np.float32)
    if not idx_subset:
        return out
    sub = np.asarray([values[int(i)] for i in idx_subset], dtype=np.float32)
    lo = float(np.min(sub))
    hi = float(np.max(sub))
    rng = hi - lo
    if rng <= 1e-9:
        for i in idx_subset:
            out[int(i)] = 0.5
        return out
    for i in idx_subset:
        out[int(i)] = (float(values[int(i)]) - lo) / rng
    return out
