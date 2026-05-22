#!/usr/bin/env python3
"""Grid search over DQN architecture hyperparameters (short smoke runs)."""

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
    "DQN_HIDDEN_SIZE": [128, 256],
    "DQN_NUM_LAYERS": [2, 3],
    "DQN_ENSEMBLE_SIZE": [1, 3],
    "lr": ["1e-4", "3e-4"],
}


def _append_result(line: str) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(line.rstrip() + "\n")


def main(max_runs: int = 4) -> int:
    keys = list(GRID.keys())
    combos = list(itertools.product(*[GRID[k] for k in keys]))[: max(1, int(max_runs))]
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _append_result(f"[DQN_GRID] start {stamp} combos={len(combos)}")
    for combo in combos:
        env = os.environ.copy()
        cfg = dict(zip(keys, combo))
        env["DQN_HIDDEN_SIZE"] = str(cfg["DQN_HIDDEN_SIZE"])
        env["DQN_NUM_LAYERS"] = str(cfg["DQN_NUM_LAYERS"])
        env["DQN_ENSEMBLE_SIZE"] = str(cfg["DQN_ENSEMBLE_SIZE"])
        env["TOT_LIFE_T"] = env.get("TOT_LIFE_T", "1")
        cmd = [sys.executable, "-m", "pytest", "tests/engine/test_dqn_trunk_arch.py", "-q"]
        proc = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
        status = "ok" if proc.returncode == 0 else "fail"
        _append_result(f"[DQN_GRID] {status} cfg={cfg} rc={proc.returncode}")
    _append_result(f"[DQN_GRID] done {stamp}")
    return 0


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    raise SystemExit(main(max_runs=n))
