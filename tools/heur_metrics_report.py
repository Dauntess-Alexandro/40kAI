"""Отчёт по first-class метрикам enemy-эвристики.

Читает JSONL, который пишет env (artifacts/metrics/heur_decisions/heur_dec_<pid>.jsonl),
и печатает сводку: распределение режимов, энтропию стилей, средний риск, success-rate
чарджа, разбивку исходов (в т.ч. draws) по профилям.

Запуск:
    python tools/heur_metrics_report.py
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# load_heur_records/outcomes_by_profile живут в core (DRY: их же использует GUI).
from core.engine.heuristic_targeting import (
    aggregate_heur_records,
    load_heur_records,
    outcomes_by_profile,
)

try:
    from project_paths import ARTIFACTS_METRICS_DIR

    _DEFAULT_DIR = str(ARTIFACTS_METRICS_DIR / "heur_decisions")
except Exception:
    _DEFAULT_DIR = os.path.join("artifacts", "metrics", "heur_decisions")


def build_heur_metrics_summary(records: list[dict], outcome: dict | None = None) -> dict:
    agg = aggregate_heur_records(records)
    by_prof = outcomes_by_profile(records)
    mode_totals = dict(agg.get("mode_totals", {}) or {})
    total_modes = sum(int(v) for v in mode_totals.values())
    p1_wins = int((outcome or {}).get("p1_wins", 0))
    p2_wins = int((outcome or {}).get("p2_wins", 0))
    draws = int((outcome or {}).get("draws", 0))
    games = p1_wins + p2_wins + draws
    return {
        "games": games,
        "p1_wins": p1_wins,
        "p2_wins": p2_wins,
        "draws": draws,
        "heur_winrate": (p2_wins / games) if games else 0.0,
        "draw_rate": (draws / games) if games else 0.0,
        "style_entropy_norm": float(agg.get("style_entropy_norm", 0.0)),
        "mode_totals": mode_totals,
        "hold_ratio": (float(mode_totals.get("hold", 0)) / float(total_modes)) if total_modes else 0.0,
        "role_totals": dict(agg.get("role_totals", {}) or {}),
        "obj_kind_totals": dict(agg.get("obj_kind_totals", {}) or {}),
        "invalid_rate": float((outcome or {}).get("invalid_rate", 0.0)),
        "avg_risk": float(agg.get("avg_risk", 0.0)),
        "charge_success_rate": float(agg.get("charge_success_rate", 0.0)),
        "shoot_overkill_rate": float((outcome or {}).get("shoot_overkill_rate", 0.0)),
        "fallback_rate": float((outcome or {}).get("fallback_rate", 0.0)),
        "metrics_games": int(agg.get("games", 0)),
        "outcomes_by_profile": by_prof,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Отчёт по first-class метрикам enemy-эвристики")
    ap.add_argument("--dir", type=str, default=_DEFAULT_DIR)
    ap.add_argument("--decisions-dir", type=str, default="")
    ap.add_argument("--summary-out", type=str, default="")
    args = ap.parse_args()

    metrics_dir = args.decisions_dir or args.dir
    records = load_heur_records(metrics_dir)
    agg = aggregate_heur_records(records)
    by_prof = outcomes_by_profile(records)
    summary = build_heur_metrics_summary(records)
    if args.summary_out:
        out_path = Path(args.summary_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "[HEUR-METRICS] "
        f"games={agg['games']} "
        f"style_entropy_norm={agg['style_entropy_norm']:.3f} "
        f"mode_totals={agg['mode_totals']} "
        f"role_totals={agg['role_totals']} "
        f"obj_kind_totals={agg.get('obj_kind_totals', {})} "
        f"hold_ratio={agg.get('hold_ratio', 0.0):.3f} "
        f"avg_risk={agg['avg_risk']:.3f} "
        f"charge_success_rate={agg['charge_success_rate']:.3f}"
    )
    for prof, d in sorted(by_prof.items()):
        games = max(1, d["games"])
        print(
            f"  profile={prof:<10} games={d['games']:<5} "
            f"heur_win={d['heur_wins'] / games:.3f} draw={d['draws'] / games:.3f} "
            f"model_win={d['model_wins'] / games:.3f}"
        )


if __name__ == "__main__":
    main()
