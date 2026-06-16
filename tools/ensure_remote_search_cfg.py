#!/usr/bin/env python3
"""ПК2: убедиться, что search_cfg есть на SMB-шаре (gmz/az/smz)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Найти или создать remote IS search_cfg на SMB-шаре.")
    parser.add_argument(
        "--algo",
        required=True,
        choices=("gmz", "az", "smz"),
        help="Алгоритм remote IS",
    )
    parser.add_argument(
        "--share-root",
        required=True,
        help="Корень общей папки (40KAI_SHARE_ROOT)",
    )
    args = parser.parse_args(argv)

    root = _repo_root()
    sys.path.insert(0, str(root))

    from core.models.remote_is_search_cfg_registry import ensure_for_algo

    result = ensure_for_algo(str(args.algo), str(args.share_root))
    label = str(args.algo).upper()
    if result.ok:
        print(f"[OK][{label}] {result.message}")
        if result.search_cfg_path:
            print(f"  search_cfg={result.search_cfg_path}")
        if result.weights_path:
            print(f"  weights={result.weights_path}")
        return 0
    print(f"[ERROR][{label}] {result.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
