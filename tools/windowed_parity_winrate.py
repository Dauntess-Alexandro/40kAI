"""Сравнение агрессии windowed=0 vs windowed=1 на одинаковых сидах (after-fix gate).

Запуск: python tools/windowed_parity_winrate.py --episodes 100 --seed 1000
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys


def _configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")


def _run(windowed: str, episodes: int, seed: int) -> str:
    env = dict(os.environ)
    env["WINDOWED_SELFPLAY"] = windowed
    env["TRAIN_ALGO"] = "az"
    cmd = [
        sys.executable,
        "tools/mcts_winrate_baseline.py",
        "--episodes",
        str(episodes),
        "--seed",
        str(seed),
        "--modes",
        "option",
    ]
    out = subprocess.run(cmd, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.stdout + out.stderr


def main() -> int:
    _configure_console_encoding()
    p = argparse.ArgumentParser(description="windowed 0 vs 1 winrate parity")
    p.add_argument("--episodes", type=int, default=100)
    p.add_argument("--seed", type=int, default=1000)
    args = p.parse_args()
    for w in ("0", "1"):
        print(f"=== WINDOWED_SELFPLAY={w} ===", flush=True)
        print(_run(w, args.episodes, args.seed), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
