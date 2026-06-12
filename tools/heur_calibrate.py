# tools/heur_calibrate.py
"""Random-search calibration for enemy heuristic weights."""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import reward_config as reward_cfg
from core.engine.agent_registry import collect_registered_agents_meta
from project_paths import ARTIFACTS_METRICS_DIR
from tools.heur_benchmark import BenchmarkError, run_benchmark

WEIGHT_NAMES = [
    "ENEMY_HEUR_MATCHUP_DIST_W",
    "ENEMY_HEUR_TARGET_DIST_W",
    "ENEMY_HEUR_MODE_W",
    "ENEMY_HEUR_PROGRESS_W",
    "ENEMY_HEUR_OBJECTIVE_DIST_W",
    "ENEMY_HEUR_OBJECTIVE_CONTROL_W",
    "ENEMY_HEUR_RISK_W",
    "ENEMY_HEUR_OBJECTIVE_PRESSURE_W",
    "ENEMY_HEUR_LOOKAHEAD_W",
    "ENEMY_HEUR_LOOK2_FUTURE_W",
    "ENEMY_HEUR_LOOK2_RISK_W",
    "ENEMY_HEUR_SHOOT_KILL_W",
    "ENEMY_HEUR_SHOOT_DAMAGE_W",
    "ENEMY_HEUR_SHOOT_OBJECTIVE_W",
    "ENEMY_HEUR_SHOOT_OVERKILL_W",
    "ENEMY_HEUR_SHOOT_EV_RETURN_RISK_W",
    "ENEMY_HEUR_CHARGE_EV_SUCCESS_W",
    "ENEMY_HEUR_CHARGE_EV_COUNTER_W",
]

BASELINE = {
    "baseline_run": "1390520",
    "heur_winrate": 0.500,
    "draw_rate": 0.008,
    "style_entropy_norm": 0.889,
    "invalid_rate": 0.0,
    "hold_ratio": 0.575,
    "fallback_rate": 0.0,
    "actual_games": 1000,
    "requested_games": 1000,
}


def current_weight_vector() -> dict[str, float]:
    return {name: float(getattr(reward_cfg, name)) for name in WEIGHT_NAMES}


def weight_bounds(name: str, current: float) -> tuple[float, float]:
    if name == "ENEMY_HEUR_OBJECTIVE_CONTROL_W":
        return 0.25, 0.75
    if name == "ENEMY_HEUR_SHOOT_OVERKILL_W":
        return 0.10, 0.35
    if name in {"ENEMY_HEUR_RISK_W", "ENEMY_HEUR_SHOOT_EV_RETURN_RISK_W"}:
        return max(0.0, current * 0.75), max(0.0, current * 1.55)
    return max(0.0, current * 0.65), max(0.0, current * 1.45)


def generate_candidates(count: int, *, seed: int, baseline: dict[str, float] | None = None) -> list[dict[str, float]]:
    base = dict(baseline or current_weight_vector())
    total = max(1, int(count))
    rng = random.Random(int(seed))
    candidates = [dict(base)]
    for _ in range(total - 1):
        cand: dict[str, float] = {}
        for name, value in base.items():
            lo, hi = weight_bounds(name, float(value))
            cand[name] = float(rng.uniform(lo, hi))
        candidates.append(cand)
    return candidates


def overrides_json(candidate: dict[str, float]) -> str:
    return json.dumps({k: float(v) for k, v in candidate.items()}, sort_keys=True, separators=(",", ":"))


def validate_overrides(candidate: dict[str, float]) -> None:
    validator = getattr(reward_cfg, "_validate_heur_calibration_override")
    for key, value in candidate.items():
        validator(str(key), value)


def score_candidate(metrics: dict[str, Any]) -> float:
    heur_winrate = float(metrics.get("heur_winrate", metrics.get("heur_winrate_all", 0.0)))
    draw_rate = float(metrics.get("draw_rate", 0.0))
    invalid_rate = float(metrics.get("invalid_rate", 0.0))
    entropy = float(metrics.get("style_entropy_norm", 0.0))
    hold_ratio = float(metrics.get("hold_ratio", 0.0))
    fallback_rate = float(metrics.get("fallback_rate", 0.0))
    return (
        1.00 * min(heur_winrate, 0.54)
        - 0.50 * abs(heur_winrate - 0.50)
        - 0.70 * max(0.0, draw_rate - 0.015)
        - 1.50 * invalid_rate
        - 0.60 * max(0.0, 0.86 - entropy)
        - 0.25 * max(0.0, hold_ratio - 0.62)
        - 0.15 * fallback_rate
    )


def reject_reasons(metrics: dict[str, Any], *, requested_games: int) -> list[str]:
    reasons: list[str] = []
    actual_games = int(metrics.get("actual_games", metrics.get("games", 0)))
    if actual_games != int(requested_games):
        reasons.append(f"actual_games={actual_games} != requested_games={int(requested_games)}")
    if float(metrics.get("invalid_rate", 0.0)) > 0.001:
        reasons.append("invalid_rate > 0.001")
    if float(metrics.get("style_entropy_norm", 0.0)) < 0.84:
        reasons.append("style_entropy_norm < 0.84")
    if float(metrics.get("draw_rate", 0.0)) > 0.03:
        reasons.append("draw_rate > 0.03")
    if float(metrics.get("heur_winrate", metrics.get("heur_winrate_all", 0.0))) > 0.56:
        reasons.append("heur_winrate > 0.56")
    if float(metrics.get("fallback_rate", 0.0)) > 0.02:
        reasons.append("fallback_rate > 0.02")
    return reasons


def acceptance_reasons(metrics: dict[str, Any], *, baseline_score: float) -> list[str]:
    reasons: list[str] = []
    score = float(metrics.get("score", score_candidate(metrics)))
    heur_winrate = float(metrics.get("heur_winrate", metrics.get("heur_winrate_all", 0.0)))
    if score <= baseline_score:
        reasons.append("score <= baseline_score")
    if float(metrics.get("style_entropy_norm", 0.0)) < 0.86:
        reasons.append("style_entropy_norm < 0.86")
    if float(metrics.get("draw_rate", 0.0)) > 0.02:
        reasons.append("draw_rate > 0.02")
    if not (0.46 <= heur_winrate <= 0.54):
        reasons.append("heur_winrate outside 0.46..0.54")
    return reasons


def resolve_learner_agent_id(agent_id: str) -> str:
    raw = str(agent_id or "").strip()
    if raw.lower() != "latest":
        return raw
    records = collect_registered_agents_meta()
    p1_records = [rec for rec in records if str(rec.get("side", "")).upper() == "P1"]
    selected = p1_records[0] if p1_records else (records[0] if records else None)
    if not selected:
        raise RuntimeError(
            "learner-agent-id=latest не найден. Укажите явный --learner-agent-id или --model."
        )
    return str(selected.get("agent_id", "") or "").strip()


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def make_reward_config_patch(best: dict[str, Any] | None, baseline: dict[str, float], baseline_score: float) -> str:
    lines = ["# Phase 8 best reward_config patch", ""]
    lines.append(f"baseline_score={baseline_score:.6f}")
    if not best:
        lines.append("accepted_candidate=none")
        return "\n".join(lines) + "\n"
    lines.append(f"candidate={best.get('candidate_idx')}")
    lines.append(f"status={best.get('status')}")
    lines.append(f"score={float(best.get('score', 0.0)):.6f}")
    lines.append(f"score_delta={float(best.get('score', 0.0)) - baseline_score:.6f}")
    lines.append(f"reject_reasons={best.get('reject_reasons', [])}")
    lines.append("")
    lines.append("```python")
    weights = best.get("weights", {}) if isinstance(best.get("weights"), dict) else {}
    for name in WEIGHT_NAMES:
        if name not in weights:
            continue
        old = float(baseline[name])
        new = float(weights[name])
        lines.append(f"{name} = {new:.6f}  # baseline {old:.6f}, delta {new - old:+.6f}")
    lines.append("```")
    return "\n".join(lines) + "\n"


def run_calibration(args: argparse.Namespace) -> dict[str, Any]:
    run_id = str(args.run_id or time.strftime("phase8_%Y%m%d_%H%M%S"))
    run_dir = ARTIFACTS_METRICS_DIR / "heur_calibration" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    candidates_path = run_dir / "candidates.jsonl"
    if candidates_path.exists():
        candidates_path.unlink()

    learner_agent_id = resolve_learner_agent_id(args.learner_agent_id)
    baseline_weights = current_weight_vector()
    baseline_score = score_candidate(BASELINE)
    candidates = generate_candidates(args.candidates, seed=args.seed, baseline=baseline_weights)

    rows: list[dict[str, Any]] = []
    best: dict[str, Any] | None = None
    t_all = time.perf_counter()
    for idx, weights in enumerate(candidates):
        validate_overrides(weights)
        candidate_dir = run_dir / f"candidate_{idx:03d}"
        row: dict[str, Any] = {
            "candidate_idx": idx,
            "weights": weights,
            "overrides_json": overrides_json(weights),
            "run_dir": str(candidate_dir),
        }
        t0 = time.perf_counter()
        if args.dry_run:
            row.update({"status": "dry_run", "elapsed_sec": 0.0, "score": None, "reject_reasons": []})
        else:
            try:
                summary = run_benchmark(
                    args.games,
                    model=args.model or None,
                    learner_agent_id=learner_agent_id,
                    opponent_agent_id=args.opponent_agent_id,
                    opponent_policy=args.opponent_policy,
                    run_id=f"{run_id}_candidate_{idx:03d}",
                    metrics_dir=candidate_dir,
                    overrides_json=row["overrides_json"],
                )
                stdout = str(summary.pop("stdout", "") or "")
                stderr = str(summary.pop("stderr", "") or "")
                logs_dir = candidate_dir / "benchmark_logs"
                logs_dir.mkdir(parents=True, exist_ok=True)
                (logs_dir / "stdout.txt").write_text(stdout, encoding="utf-8")
                (logs_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
                score = score_candidate(summary)
                summary["score"] = score
                rejects = reject_reasons(summary, requested_games=args.games)
                accepts = acceptance_reasons(summary, baseline_score=baseline_score)
                status = "ok" if not rejects else "rejected"
                row.update(summary)
                row.update({"status": status, "reject_reasons": rejects, "acceptance_reasons": accepts})
                if status == "ok" and not accepts and (best is None or score > float(best.get("score", -1e9))):
                    best = row
            except (BenchmarkError, RuntimeError, OSError) as exc:
                if idx == 0:
                    raise
                row.update({"status": "failed", "error": str(exc), "reject_reasons": [str(exc)]})
        row["elapsed_sec"] = float(time.perf_counter() - t0)
        row["sec_per_game"] = float(row["elapsed_sec"] / max(1, int(args.games))) if not args.dry_run else 0.0
        rows.append(row)
        _append_jsonl(candidates_path, row)

    elapsed_all = time.perf_counter() - t_all
    ranked = sorted(
        [r for r in rows if isinstance(r.get("score"), (int, float))],
        key=lambda r: float(r.get("score", -1e9)),
        reverse=True,
    )
    summary_payload = {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "dry_run": bool(args.dry_run),
        "games_per_candidate": int(args.games),
        "candidates": int(args.candidates),
        "seed": int(args.seed),
        "learner_agent_id": learner_agent_id,
        "model": str(args.model or ""),
        "opponent_policy": str(args.opponent_policy),
        "baseline": BASELINE,
        "baseline_score": baseline_score,
        "best_candidate_idx": best.get("candidate_idx") if best else None,
        "elapsed_sec": float(elapsed_all),
        "sec_per_candidate": float(elapsed_all / max(1, len(rows))),
        "top_candidates": ranked[: max(1, int(args.top_k))],
        "status_counts": {status: sum(1 for r in rows if r.get("status") == status) for status in sorted({str(r.get("status")) for r in rows})},
    }
    _write_json(run_dir / "summary.json", summary_payload)
    (run_dir / "best_reward_config_patch.md").write_text(
        make_reward_config_patch(best, baseline_weights, baseline_score),
        encoding="utf-8",
    )
    return summary_payload


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase 8 random-search calibration for enemy heuristic weights.")
    ap.add_argument("--candidates", type=int, default=40)
    ap.add_argument("--games", type=int, default=50)
    ap.add_argument("--seed", type=int, default=1390520)
    ap.add_argument("--model", type=str, default="")
    ap.add_argument("--learner-agent-id", type=str, default="")
    ap.add_argument("--opponent-agent-id", type=str, default="")
    ap.add_argument("--opponent-policy", type=str, default="heuristic_auto")
    ap.add_argument("--run-id", type=str, default="")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    try:
        summary = run_calibration(args)
    except Exception as exc:
        print(f"[HEUR-CAL][ERROR] {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    print(
        "[HEUR-CAL] "
        f"run_id={summary['run_id']} "
        f"candidates={summary['candidates']} "
        f"games={summary['games_per_candidate']} "
        f"dry_run={int(bool(summary['dry_run']))} "
        f"best={summary['best_candidate_idx']} "
        f"run_dir={summary['run_dir']}"
    )


if __name__ == "__main__":
    main()
