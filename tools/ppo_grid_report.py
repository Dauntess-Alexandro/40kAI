#!/usr/bin/env python3
"""Summarize PPO grid search lines from artifacts/results/results.txt."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = ROOT / "artifacts" / "results" / "results.txt"


def main(top_k: int = 5) -> int:
    if not RESULTS_PATH.is_file():
        print(f"Нет файла результатов: {RESULTS_PATH}")
        return 1
    lines = RESULTS_PATH.read_text(encoding="utf-8").splitlines()
    ok_lines = [ln for ln in lines if "[PPO_GRID] ok" in ln]
    print(f"PPO grid OK runs: {len(ok_lines)}")
    for ln in ok_lines[-top_k:]:
        m = re.search(r"cfg=(\{.*\})", ln)
        print(f"  {m.group(1) if m else ln}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
