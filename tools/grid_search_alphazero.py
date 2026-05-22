#!/usr/bin/env python3
"""Grid search over AlphaZero architecture / MCTS hyperparameters (short smoke runs)."""

from __future__ import annotations

import itertools
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "artifacts" / "results" / "results.txt"

GRID = {
    "AZ_HIDDEN_SIZE": ["128", "256"],
    "AZ_NUM_LAYERS": ["2", "3"],
    "AZ_VALUE_ENSEMBLE": ["1", "2"],
    "AZ_C_PUCT": ["1.1", "1.5"],
    "AZ_MCTS_MAX_DEPTH": ["2", "4"],
}


def _append_result(line: str) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def main(max_runs: int = 4) -> int:
    keys = list(GRID.keys())
    combos = list(itertools.product(*[GRID[k] for k in keys]))[: max(1, int(max_runs))]
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _append_result(f"[AZ_GRID] start {stamp} combos={len(combos)}")
    tests = [
        "tests/engine/test_alphazero_arch.py",
        "tests/engine/test_alphazero_smoke.py",
        "tests/engine/test_alphazero_mcts_tree_basic.py",
    ]
    for combo in combos:
        env = os.environ.copy()
        cfg = dict(zip(keys, combo))
        for k, v in cfg.items():
            env[k] = str(v)
        cmd = [sys.executable, "-m", "pytest", *tests, "-q", "--tb=no"]
        proc = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
        status = "ok" if proc.returncode == 0 else "fail"
        _append_result(f"[AZ_GRID] {status} cfg={cfg} rc={proc.returncode}")
    _append_result(f"[AZ_GRID] done {stamp}")
    return 0


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    raise SystemExit(main(max_runs=n))
