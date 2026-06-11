# tools/heur_benchmark.py
"""Бенчмарк enemy-эвристики: гоняет eval.py и измеряет силу + разнообразие стилей.

Запуск (пример):
    python tools/heur_benchmark.py --games 30 --seed 0

Зачем style_entropy: цель эвристики — curriculum-оппонент. Чистый win-rate без
контроля энтропии режимов схлопнет разнообразие в один стиль. Мерим оба числа.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import subprocess
import sys

_DETAIL_RE = re.compile(r"Итог серии P1/P2/Draw:\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)")
_MODE_RE = re.compile(r"\[ENEMY\]\[HEUR\]\[MOVE\].*?\bmode=(\w+)")


def parse_eval_output(text: str) -> dict:
    """Достаёт из stdout+логов eval.py: счёт партий и распределение режимов движения."""
    p1 = p2 = draws = 0
    m = _DETAIL_RE.search(text)
    if m:
        p1, p2, draws = int(m.group(1)), int(m.group(2)), int(m.group(3))
    mode_counts: dict[str, int] = {}
    for mm in _MODE_RE.finditer(text):
        mode = mm.group(1)
        mode_counts[mode] = mode_counts.get(mode, 0) + 1
    return {"p1_wins": p1, "p2_wins": p2, "draws": draws, "mode_counts": mode_counts}


def summarize(parsed: dict, *, heuristic_side: str = "p2") -> dict:
    """Считает win-rate эвристики и нормированную энтропию распределения стилей."""
    p1 = int(parsed.get("p1_wins", 0))
    p2 = int(parsed.get("p2_wins", 0))
    draws = int(parsed.get("draws", 0))
    games = p1 + p2 + draws
    decisive = p1 + p2
    heur_wins = p2 if heuristic_side == "p2" else p1
    winrate_all = heur_wins / games if games else 0.0
    winrate_dec = heur_wins / decisive if decisive else 0.0

    counts = parsed.get("mode_counts", {}) or {}
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
    return {
        "games": games,
        "heur_winrate_all": winrate_all,
        "heur_winrate_decisive": winrate_dec,
        "style_entropy_norm": entropy_norm,
        "mode_counts": dict(counts),
    }


def run_benchmark(games: int) -> dict:
    """Гоняет eval.py как subprocess с HEURISTIC_DEBUG=1 и агрегирует результат.

    Без явного opponent-agent eval.py ведёт врага как heuristic_auto (см. eval.py:605)
    — это ровно наша enemy-эвристика. eval.py НЕ поддерживает --seed, поэтому он не
    передаётся; вариативность даёт встроенный RNG движка.
    """
    env = dict(os.environ)
    env["HEURISTIC_DEBUG"] = "1"
    cmd = [
        sys.executable,
        "eval.py",
        "--games",
        str(games),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env)
    text = (proc.stdout or "") + "\n" + (proc.stderr or "")
    parsed = parse_eval_output(text)
    return summarize(parsed, heuristic_side="p2")


def main() -> None:
    ap = argparse.ArgumentParser(description="Бенчмарк силы и разнообразия enemy-эвристики")
    ap.add_argument("--games", type=int, default=30)
    args = ap.parse_args()
    summary = run_benchmark(args.games)
    print(
        "[HEUR-BENCH] "
        f"games={summary['games']} "
        f"winrate_all={summary['heur_winrate_all']:.3f} "
        f"winrate_decisive={summary['heur_winrate_decisive']:.3f} "
        f"style_entropy_norm={summary['style_entropy_norm']:.3f} "
        f"modes={summary['mode_counts']}"
    )


if __name__ == "__main__":
    main()
