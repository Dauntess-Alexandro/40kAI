"""Отчёт по first-class метрикам enemy-эвристики.

Читает JSONL, который пишет env (artifacts/metrics/heur_decisions/heur_dec_<pid>.jsonl),
и печатает сводку: распределение режимов, энтропию стилей, средний риск, success-rate
чарджа, разбивку исходов (в т.ч. draws) по профилям.

Запуск:
    python tools/heur_metrics_report.py
"""
from __future__ import annotations

import argparse
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


def main() -> None:
    ap = argparse.ArgumentParser(description="Отчёт по first-class метрикам enemy-эвристики")
    ap.add_argument("--dir", type=str, default=_DEFAULT_DIR)
    args = ap.parse_args()

    records = load_heur_records(args.dir)
    agg = aggregate_heur_records(records)
    by_prof = outcomes_by_profile(records)

    print(
        "[HEUR-METRICS] "
        f"games={agg['games']} "
        f"style_entropy_norm={agg['style_entropy_norm']:.3f} "
        f"mode_totals={agg['mode_totals']} "
        f"role_totals={agg['role_totals']} "
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
