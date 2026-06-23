"""Stage 8.4f: MCTS-корень по одному DecisionWindow (opt-in, дефолт выкл)."""

from __future__ import annotations

import os

from core.models.option_candidates import RootJointCandidates, build_window_layer_plan_candidates


def mcts_window_nodes_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    raw = str(os.getenv("MCTS_WINDOW_NODES", "0")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def resolve_active_window_index(*, move_count: int, num_windows: int) -> int:
    """Индекс окна для расширения корня: command на move 0, далее по кругу."""
    if num_windows <= 0:
        return 0
    mc = max(0, int(move_count))
    return min(mc, num_windows - 1)


def root_joint_candidates_window_nodes(
    *,
    env,
    len_model: int,
    priors,
    legal_masks,
    move_count: int = 0,
    max_candidates: int = 64,
    perturb_top_m: int = 8,
    side: str = "model",
) -> RootJointCandidates:
    """Кандидаты корня: perturb только одного окна (остальные — greedy)."""
    from core.engine.phases.option_generator import generate_windows
    from core.models.utils import unwrap_env

    e = unwrap_env(env)
    windows = generate_windows(e, str(side))
    wi = resolve_active_window_index(move_count=int(move_count), num_windows=len(windows))
    plans = build_window_layer_plan_candidates(
        e,
        int(len_model),
        priors,
        legal_masks,
        side=str(side),
        window_index=int(wi),
        max_candidates=int(max_candidates),
        perturb_top_m=int(perturb_top_m),
    )
    tuples = [p.joint_tuple for p in plans]
    if not tuples:
        return RootJointCandidates(tuples=((0,) * len(priors),))
    capped = tuples[: max(1, int(max_candidates))]
    return RootJointCandidates(tuples=tuple(capped))
