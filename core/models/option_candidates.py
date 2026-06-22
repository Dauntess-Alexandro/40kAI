"""Мост PhaseEngine/ActionOption ↔ факторизованный MCTS (joint tuple).

Stage 4: кандидаты корня tree-MCTS из generate_windows с проекцией prior
на плоский action_dict. Дефолтный режим joint — прежнее поведение.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from core.engine.phases.legacy_compiler import compile_options_to_action_dict
from core.engine.phases.option_generator import generate_windows
from core.engine.phases.types import ActionKind, ActionOption, DecisionWindow, Phase
from core.models.action_contract import ordered_action_keys
from core.models.utils import unwrap_env

CandidateMode = Literal["joint", "filter", "option", "option_plus"]
_VALID_MODES = frozenset({"joint", "filter", "option", "option_plus"})


def resolve_candidate_mode(mode: str | None = None) -> CandidateMode:
    raw = mode if mode is not None else os.getenv("MCTS_CANDIDATE_MODE", "option")
    m = str(raw or "option").strip().lower()
    if m not in _VALID_MODES:
        return "option"
    return m  # type: ignore[return-value]


@dataclass(frozen=True)
class TurnPlanCandidate:
    """Один кандидат корня MCTS: выборы по окнам → action_dict → joint tuple."""

    window_choices: tuple[tuple[str, int], ...]
    options: tuple[ActionOption, ...]
    action_dict: dict[str, int]
    joint_tuple: tuple[int, ...]
    projected_prior: float = 0.0
    fight_stratagem_plan: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True)
class RootJointCandidates:
    """Joint-кандидаты корня MCTS + fight-стратагемы (не входят в joint tuple)."""

    tuples: tuple[tuple[int, ...], ...]
    fight_plans: dict[tuple[int, ...], tuple[tuple[int, str], ...]] = field(default_factory=dict)

    def __iter__(self):
        return iter(self.tuples)

    def __len__(self) -> int:
        return len(self.tuples)

    def __getitem__(self, key):
        return self.tuples[key]

    def fight_plan_for(self, joint_tuple: tuple[int, ...]) -> dict[int, str]:
        raw = self.fight_plans.get(joint_tuple, ())
        return {int(u): str(s) for u, s in raw}


def attach_fight_stratagem_plan(env, fight_plan: dict[int, str] | None) -> None:
    """Задать план fight-стратагем перед env.step (option/MCTS rollout)."""
    e = unwrap_env(env)
    if fight_plan:
        e._pending_fight_stratagem_plan = dict(fight_plan)
    else:
        e._pending_fight_stratagem_plan = None


def joint_tuple_from_action_dict(action_dict: dict[str, int], len_model: int) -> tuple[int, ...]:
    keys = ordered_action_keys(int(len_model))
    return tuple(int(action_dict[k]) for k in keys)


def action_dict_from_joint_tuple(joint_tuple: tuple[int, ...], len_model: int) -> dict[str, int]:
    keys = ordered_action_keys(int(len_model))
    if len(joint_tuple) != len(keys):
        raise ValueError(
            f"joint_tuple длины {len(joint_tuple)} не совпадает с числом голов {len(keys)}; "
            f"где: option_candidates.action_dict_from_joint_tuple; задайте len_model корректно."
        )
    return {k: int(joint_tuple[i]) for i, k in enumerate(keys)}


def score_joint_prior(
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    joint_tuple: tuple[int, ...],
) -> float:
    """Произведение prior по головам для joint tuple (0 если нелегален)."""
    p = 1.0
    for head_i, a in enumerate(joint_tuple):
        if head_i >= len(priors):
            return 0.0
        ai = int(a)
        legal = np.asarray(legal_masks[head_i], dtype=bool)
        if ai < 0 or ai >= legal.size or not bool(legal[ai]):
            return 0.0
        p *= float(priors[head_i][ai])
    return max(float(p), 1e-8)


def joint_action_candidates(
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    top_k_per_head: int,
    max_candidates: int = 64,
) -> list[tuple[int, ...]]:
    """Greedy Cartesian joint-кандидаты (прежняя логика alphazero_mcts)."""
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


def _score_option_isolated(
    option: ActionOption,
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    len_model: int,
) -> float:
    ad = compile_options_to_action_dict([option], int(len_model))
    jt = joint_tuple_from_action_dict(ad, int(len_model))
    return score_joint_prior(priors, legal_masks, jt)


def _choices_from_windows(
    windows: list[DecisionWindow],
    choice_by_window: dict[str, int],
) -> tuple[tuple[tuple[str, int], ...], tuple[ActionOption, ...]]:
    choices: list[tuple[str, int]] = []
    options: list[ActionOption] = []
    for w in windows:
        if not w.options:
            continue
        oi = int(choice_by_window.get(w.window_id, 0))
        oi = max(0, min(oi, len(w.options) - 1))
        choices.append((w.window_id, oi))
        options.append(w.options[oi])
    return tuple(choices), tuple(options)


def _fight_stratagem_plan_from_choices(
    windows: list[DecisionWindow],
    choice_by_window: dict[str, int],
) -> tuple[tuple[int, str], ...]:
    plan: list[tuple[int, str]] = []
    for w in windows:
        if w.phase is not Phase.FIGHT or not w.options:
            continue
        oi = int(choice_by_window.get(w.window_id, 0))
        oi = max(0, min(oi, len(w.options) - 1))
        opt = w.options[oi]
        if opt.kind is ActionKind.USE_STRATAGEM and opt.unit_idx is not None:
            sid = str(opt.meta.get("stratagem_id", "") or "")
            if sid == "command_reroll":
                # Сохраняем выбранный деревом под-тип (hit/wound) в colon-форме,
                # чтобы apply-путь применил реролл напрямую (AZ/MCTS не ставит reaction_policy).
                roll = str(opt.meta.get("reroll_roll", "") or opt.param.get("reroll_roll", "") or "")
                if roll:
                    sid = f"command_reroll:{roll}"
            if sid:
                plan.append((int(opt.unit_idx), sid))
    return tuple(plan)


def _turn_plan_from_choices(
    windows: list[DecisionWindow],
    choice_by_window: dict[str, int],
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    len_model: int,
) -> TurnPlanCandidate:
    window_choices, options = _choices_from_windows(windows, choice_by_window)
    ad = compile_options_to_action_dict(list(options), int(len_model))
    jt = joint_tuple_from_action_dict(ad, int(len_model))
    pp = score_joint_prior(priors, legal_masks, jt)
    fight_plan = _fight_stratagem_plan_from_choices(windows, choice_by_window)
    return TurnPlanCandidate(
        window_choices=window_choices,
        options=options,
        action_dict=ad,
        joint_tuple=jt,
        projected_prior=pp,
        fight_stratagem_plan=fight_plan,
    )


def build_turn_plan_candidates(
    env,
    len_model: int,
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    *,
    side: str = "model",
    max_candidates: int = 64,
    perturb_top_m: int = 4,
) -> list[TurnPlanCandidate]:
    """Bounded turn-планы: greedy + single-window perturbations."""
    e = unwrap_env(env)
    windows = generate_windows(e, str(side))
    if not windows:
        ad = compile_options_to_action_dict([], int(len_model))
        jt = joint_tuple_from_action_dict(ad, int(len_model))
        return [
            TurnPlanCandidate(
                window_choices=(),
                options=(),
                action_dict=ad,
                joint_tuple=jt,
                projected_prior=score_joint_prior(priors, legal_masks, jt),
            )
        ]

    greedy_map: dict[str, int] = {}
    for w in windows:
        if not w.options:
            continue
        best_i = 0
        best_score = -1.0
        for i, opt in enumerate(w.options):
            sc = _score_option_isolated(opt, priors, legal_masks, int(len_model))
            if sc > best_score:
                best_score = sc
                best_i = i
        greedy_map[w.window_id] = best_i

    by_tuple: dict[tuple[int, ...], TurnPlanCandidate] = {}
    greedy_cand = _turn_plan_from_choices(windows, greedy_map, priors, legal_masks, int(len_model))
    by_tuple[greedy_cand.joint_tuple] = greedy_cand

    top_m = max(1, int(perturb_top_m))
    for w in windows:
        if not w.options:
            continue
        ranked = sorted(
            enumerate(w.options),
            key=lambda item: _score_option_isolated(item[1], priors, legal_masks, int(len_model)),
            reverse=True,
        )
        for oi, _opt in ranked[:top_m]:
            variant = dict(greedy_map)
            variant[w.window_id] = int(oi)
            cand = _turn_plan_from_choices(windows, variant, priors, legal_masks, int(len_model))
            by_tuple[cand.joint_tuple] = cand
            if len(by_tuple) >= int(max_candidates):
                break
        if len(by_tuple) >= int(max_candidates):
            break

    out = sorted(by_tuple.values(), key=lambda c: c.projected_prior, reverse=True)
    return out[: max(1, int(max_candidates))]


def filter_joint_candidates(
    joint_tuples: list[tuple[int, ...]],
    env,
    len_model: int,
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    *,
    max_legal_lookup: int = 512,
) -> list[tuple[int, ...]]:
    """Оставить только joint-кандидаты, достижимые из turn-планов (подмножество)."""
    if not joint_tuples:
        return []
    legal_set = {
        c.joint_tuple
        for c in build_turn_plan_candidates(
            env,
            int(len_model),
            priors,
            legal_masks,
            max_candidates=int(max_legal_lookup),
        )
    }
    filtered = [t for t in joint_tuples if t in legal_set]
    return filtered if filtered else [joint_tuples[0]]


def build_window_layer_plan_candidates(
    env,
    len_model: int,
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    *,
    side: str = "model",
    window_index: int = 0,
    max_candidates: int = 64,
    perturb_top_m: int = 8,
) -> list[TurnPlanCandidate]:
    """Turn-планы с perturb только одного окна (Stage 8.4f)."""
    e = unwrap_env(env)
    windows = generate_windows(e, str(side))
    if not windows:
        return build_turn_plan_candidates(
            env,
            int(len_model),
            priors,
            legal_masks,
            side=str(side),
            max_candidates=int(max_candidates),
        )

    wi = max(0, min(int(window_index), len(windows) - 1))
    greedy_map: dict[str, int] = {}
    for w in windows:
        if not w.options:
            continue
        best_i = 0
        best_score = -1.0
        for i, opt in enumerate(w.options):
            sc = _score_option_isolated(opt, priors, legal_masks, int(len_model))
            if sc > best_score:
                best_score = sc
                best_i = i
        greedy_map[w.window_id] = best_i

    by_tuple: dict[tuple[int, ...], TurnPlanCandidate] = {}
    target = windows[wi]
    if not target.options:
        return build_turn_plan_candidates(
            env,
            int(len_model),
            priors,
            legal_masks,
            side=str(side),
            max_candidates=int(max_candidates),
        )

    top_m = max(1, int(perturb_top_m))
    ranked = sorted(
        enumerate(target.options),
        key=lambda item: _score_option_isolated(item[1], priors, legal_masks, int(len_model)),
        reverse=True,
    )
    for oi, _opt in ranked[:top_m]:
        variant = dict(greedy_map)
        variant[target.window_id] = int(oi)
        cand = _turn_plan_from_choices(windows, variant, priors, legal_masks, int(len_model))
        by_tuple[cand.joint_tuple] = cand
        if len(by_tuple) >= int(max_candidates):
            break

    if not by_tuple:
        cand = _turn_plan_from_choices(windows, greedy_map, priors, legal_masks, int(len_model))
        by_tuple[cand.joint_tuple] = cand

    out = sorted(by_tuple.values(), key=lambda c: c.projected_prior, reverse=True)
    return out[: max(1, int(max_candidates))]


def root_joint_candidates(
    *,
    mode: str,
    priors: list[np.ndarray],
    legal_masks: list[np.ndarray],
    env,
    len_model: int,
    top_k_per_head: int = 8,
    max_candidates: int = 64,
    perturb_top_m: int = 4,
    move_count: int = 0,
    window_nodes: bool = False,
) -> RootJointCandidates:
    """Единая точка выбора кандидатов корня MCTS."""
    resolved = resolve_candidate_mode(mode)
    joint = joint_action_candidates(priors, legal_masks, int(top_k_per_head), int(max_candidates))

    use_window_nodes = bool(window_nodes) and resolved in {"option", "option_plus"}
    if use_window_nodes:
        from core.models.windowed_mcts import root_joint_candidates_window_nodes

        return root_joint_candidates_window_nodes(
            env=env,
            len_model=int(len_model),
            priors=priors,
            legal_masks=legal_masks,
            move_count=int(move_count),
            max_candidates=int(max_candidates),
            perturb_top_m=max(int(perturb_top_m), 4),
        )

    if resolved == "joint":
        return RootJointCandidates(tuples=tuple(joint))

    if resolved == "filter":
        filtered = filter_joint_candidates(
            joint,
            env,
            int(len_model),
            priors,
            legal_masks,
        )
        return RootJointCandidates(tuples=tuple(filtered))

    plans = build_turn_plan_candidates(
        env,
        int(len_model),
        priors,
        legal_masks,
        max_candidates=int(max_candidates),
        perturb_top_m=int(perturb_top_m),
    )
    tuples: list[tuple[int, ...]] = [p.joint_tuple for p in plans]
    fight_plans: dict[tuple[int, ...], tuple[tuple[int, str], ...]] = {
        p.joint_tuple: p.fight_stratagem_plan for p in plans
    }

    if resolved == "option_plus":
        legacy_greedy = joint[0] if joint else tuples[0]
        if legacy_greedy not in tuples:
            tuples.insert(0, legacy_greedy)
            fight_plans.setdefault(legacy_greedy, ())

    if not tuples:
        fallback = joint[:1] if joint else [tuple(0 for _ in priors)]
        return RootJointCandidates(tuples=tuple(fallback))
    capped = tuples[: max(1, int(max_candidates))]
    return RootJointCandidates(
        tuples=tuple(capped),
        fight_plans={t: fight_plans.get(t, ()) for t in capped},
    )
