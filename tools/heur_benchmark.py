# tools/heur_benchmark.py
"""Benchmark enemy heuristic strength and first-class style metrics."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.engine.heuristic_targeting import load_heur_records
from project_paths import ARTIFACTS_METRICS_DIR
from tools.heur_metrics_report import build_heur_metrics_summary

_DETAIL_RE = re.compile(r"P1/P2/Draw:\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)")
_SUMMARY_RE = re.compile(r"\[SUMMARY_V2\].*?\bp1_wins=(\d+)\s+p2_wins=(\d+)\s+draws=(\d+)")
_MODE_RE = re.compile(r"\[ENEMY\]\[HEUR\]\[MOVE\].*?\bmode=(\w+)")
_ERROR_RE = re.compile(r"\[(?:EVAL\]\s*)?ERROR\]")


class BenchmarkError(RuntimeError):
    pass


def parse_eval_output(text: str) -> dict:
    """Extract P1/P2/draw counts and optional debug movement modes from eval output."""
    p1 = p2 = draws = 0
    for m in _SUMMARY_RE.finditer(text or ""):
        p1, p2, draws = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if p1 + p2 + draws <= 0:
        for m in _DETAIL_RE.finditer(text or ""):
            p1, p2, draws = int(m.group(1)), int(m.group(2)), int(m.group(3))

    mode_counts: dict[str, int] = {}
    for mm in _MODE_RE.finditer(text or ""):
        mode = mm.group(1)
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    return {"p1_wins": p1, "p2_wins": p2, "draws": draws, "mode_counts": mode_counts}


def validate_benchmark_output(text: str, *, requested_games: int, returncode: int = 0) -> dict:
    if int(returncode) != 0:
        raise BenchmarkError(f"eval.py завершился с кодом {returncode}. Проверьте stdout/stderr benchmark-лога.")
    if _ERROR_RE.search(text or ""):
        raise BenchmarkError("eval.py напечатал [ERROR]. Проверьте модель/agent-id и benchmark-лог.")
    parsed = parse_eval_output(text or "")
    actual_games = int(parsed.get("p1_wins", 0)) + int(parsed.get("p2_wins", 0)) + int(parsed.get("draws", 0))
    if actual_games <= 0:
        raise BenchmarkError("eval.py не вернул ни одной партии: games=0 или итог серии не найден.")
    if actual_games != int(requested_games):
        raise BenchmarkError(f"eval.py вернул {actual_games} игр вместо requested={int(requested_games)}.")
    return parsed


def summarize(parsed: dict, *, heuristic_side: str = "p2", metrics: dict | None = None) -> dict:
    """Compute heuristic win-rate and normalized style entropy.

    Existing tests use this with stdout mode_counts. Real Phase 8 runs pass JSONL metrics.
    """
    p1 = int(parsed.get("p1_wins", 0))
    p2 = int(parsed.get("p2_wins", 0))
    draws = int(parsed.get("draws", 0))
    games = p1 + p2 + draws
    decisive = p1 + p2
    heur_wins = p2 if heuristic_side == "p2" else p1
    winrate_all = heur_wins / games if games else 0.0
    winrate_dec = heur_wins / decisive if decisive else 0.0

    counts = dict(parsed.get("mode_counts", {}) or {})
    entropy_norm = 0.0
    if metrics:
        counts = dict(metrics.get("mode_totals", counts) or {})
        entropy_norm = float(metrics.get("style_entropy_norm", 0.0))
    else:
        total = sum(counts.values())
        entropy = 0.0
        if total > 0:
            for c in counts.values():
                if c <= 0:
                    continue
                p = c / total
                entropy -= p * math.log2(p)
        n_modes = max(1, len(counts))
        max_entropy = math.log2(n_modes) if n_modes > 1 else 1.0
        entropy_norm = (entropy / max_entropy) if max_entropy > 0 else 0.0

    result = {
        "games": games,
        "p1_wins": p1,
        "p2_wins": p2,
        "draws": draws,
        "heur_winrate_all": winrate_all,
        "heur_winrate_decisive": winrate_dec,
        "heur_winrate": winrate_all,
        "draw_rate": (draws / games) if games else 0.0,
        "style_entropy_norm": entropy_norm,
        "mode_counts": counts,
    }
    if metrics:
        result.update(metrics)
        result["heur_winrate_all"] = winrate_all
        result["heur_winrate_decisive"] = winrate_dec
    return result


def heuristic_side_for_learner(learner_side: str) -> str:
    """Сторона эвристики противоположна стороне learner.

    learner P1 → эвристика p2 (по умолчанию), learner P2 → эвристика p1.
    """
    side = str(learner_side or "").strip().upper()
    return "p1" if side == "P2" else "p2"


def _default_run_id() -> str:
    return time.strftime("%Y%m%d_%H%M%S") + f"_{os.getpid()}"


def run_benchmark(
    games: int,
    *,
    model: str | None = None,
    learner_agent_id: str = "",
    learner_side: str = "P1",
    opponent_agent_id: str = "",
    opponent_policy: str = "heuristic_auto",
    run_id: str | None = None,
    metrics_dir: str | os.PathLike[str] | None = None,
    overrides_json: str | None = None,
    extra_env: dict[str, str] | None = None,
) -> dict:
    """Run eval.py and return a strict benchmark summary.

    learner играет на learner_side (P1 или P2); вражеская эвристика — на
    противоположной стороне (heuristic_side_for_learner). winrate считается
    для стороны эвристики.
    """
    requested_games = int(games)
    norm_learner_side = str(learner_side or "P1").strip().upper()
    if norm_learner_side not in {"P1", "P2"}:
        norm_learner_side = "P1"
    heuristic_side = heuristic_side_for_learner(norm_learner_side)
    rid = str(run_id or _default_run_id())
    root = Path(metrics_dir) if metrics_dir is not None else ARTIFACTS_METRICS_DIR / "heur_calibration" / rid
    decisions_dir = root / "heur_decisions"
    decisions_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["HEUR_METRICS_DECISIONS_DIR"] = str(decisions_dir)
    env["ENEMY_HEUR_METRICS_ENABLED"] = "1"
    env["LEARNER_SIDE"] = norm_learner_side
    if overrides_json:
        env["HEUR_CALIBRATION_OVERRIDES_JSON"] = str(overrides_json)
    if extra_env:
        env.update({str(k): str(v) for k, v in extra_env.items()})

    cmd = [sys.executable, "-u", "eval.py", "--games", str(requested_games)]
    if model:
        cmd.extend(["--model", str(model)])
    if learner_agent_id:
        cmd.extend(["--learner-agent-id", str(learner_agent_id)])
    if opponent_agent_id:
        cmd.extend(["--opponent-agent-id", str(opponent_agent_id)])
    if opponent_policy:
        cmd.extend(["--opponent-policy", str(opponent_policy)])

    t0 = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    elapsed = time.perf_counter() - t0
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    parsed = validate_benchmark_output(text, requested_games=requested_games, returncode=int(proc.returncode))

    records = load_heur_records(decisions_dir)
    metrics = build_heur_metrics_summary(records, outcome=parsed) if records else {}
    summary = summarize(parsed, heuristic_side=heuristic_side, metrics=metrics)
    summary.update(
        {
            "requested_games": requested_games,
            "actual_games": int(summary.get("games", 0)),
            "learner_side": norm_learner_side,
            "heuristic_side": heuristic_side,
            "run_id": rid,
            "run_dir": str(root),
            "decisions_dir": str(decisions_dir),
            "metrics_source": "jsonl" if records else "stdout",
            "cmd": cmd,
            "returncode": int(proc.returncode),
            "elapsed_sec": float(elapsed),
            "sec_per_game": float(elapsed / max(1, requested_games)),
            "stdout": proc.stdout or "",
            "stderr": proc.stderr or "",
        }
    )
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Benchmark enemy heuristic strength and style diversity.")
    ap.add_argument("--games", type=int, default=30)
    ap.add_argument("--model", type=str, default="")
    ap.add_argument("--learner-agent-id", type=str, default="")
    ap.add_argument("--learner-side", type=str, default="P1", choices=["P1", "P2", "p1", "p2"])
    ap.add_argument("--opponent-agent-id", type=str, default="")
    ap.add_argument("--opponent-policy", type=str, default="heuristic_auto")
    ap.add_argument("--run-id", type=str, default="")
    ap.add_argument("--metrics-dir", type=str, default="")
    ap.add_argument("--overrides-json", type=str, default="")
    args = ap.parse_args()

    try:
        summary = run_benchmark(
            args.games,
            model=args.model or None,
            learner_agent_id=args.learner_agent_id,
            learner_side=args.learner_side,
            opponent_agent_id=args.opponent_agent_id,
            opponent_policy=args.opponent_policy,
            run_id=args.run_id or None,
            metrics_dir=args.metrics_dir or None,
            overrides_json=args.overrides_json or None,
        )
    except BenchmarkError as exc:
        print(f"[HEUR-BENCH][ERROR] {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    printable = {k: v for k, v in summary.items() if k not in {"stdout", "stderr"}}
    print(
        "[HEUR-BENCH] "
        f"games={summary['games']} "
        f"winrate_all={summary['heur_winrate_all']:.3f} "
        f"winrate_decisive={summary['heur_winrate_decisive']:.3f} "
        f"draw_rate={summary.get('draw_rate', 0.0):.3f} "
        f"style_entropy_norm={summary['style_entropy_norm']:.3f} "
        f"hold_ratio={summary.get('hold_ratio', 0.0):.3f} "
        f"modes={summary.get('mode_totals', summary.get('mode_counts', {}))} "
        f"source={summary.get('metrics_source', 'stdout')}"
    )
    print(json.dumps(printable, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
