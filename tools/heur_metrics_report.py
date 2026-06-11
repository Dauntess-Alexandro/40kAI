"""Отчёт по first-class метрикам enemy-эвристики.

Читает JSONL, который пишет env (artifacts/metrics/heur_decisions/heur_dec_<pid>.jsonl),
и печатает сводку: распределение режимов, энтропию стилей, средний риск, success-rate
чарджа, разбивку исходов (в т.ч. draws) по профилям.

Запуск:
    python tools/heur_metrics_report.py
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.engine.heuristic_targeting import aggregate_heur_records

try:
    from project_paths import ARTIFACTS_METRICS_DIR

    _DEFAULT_DIR = str(ARTIFACTS_METRICS_DIR / "heur_decisions")
except Exception:
    _DEFAULT_DIR = os.path.join("artifacts", "metrics", "heur_decisions")


def load_records(metrics_dir: str = _DEFAULT_DIR) -> list[dict]:
    """Считать все записи (по партиям) из per-pid JSONL-файлов."""
    records: list[dict] = []
    for path in glob.glob(os.path.join(metrics_dir, "heur_dec_*.jsonl")):
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        except OSError:
            continue
    return records


def outcomes_by_profile(records: list[dict]) -> dict:
    """Разбивка исходов по профилям: games / draws / heur_wins / model_wins.

    draw = winner не 'model' и не 'enemy' (turn_limit/ничья). heur_win = winner=='enemy'.
    """
    out: dict[str, dict] = {}
    for rec in records or []:
        if not isinstance(rec, dict):
            continue
        prof = str(rec.get("profile", "balanced"))
        d = out.setdefault(prof, {"games": 0, "draws": 0, "heur_wins": 0, "model_wins": 0})
        d["games"] += 1
        winner = str(rec.get("winner", "") or "").strip().lower()
        if winner == "enemy":
            d["heur_wins"] += 1
        elif winner == "model":
            d["model_wins"] += 1
        else:
            d["draws"] += 1
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Отчёт по first-class метрикам enemy-эвристики")
    ap.add_argument("--dir", type=str, default=_DEFAULT_DIR)
    args = ap.parse_args()

    records = load_records(args.dir)
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
