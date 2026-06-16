#!/usr/bin/env python3
"""Обратная совместимость: делегирует в ensure_remote_search_cfg --algo smz."""
from __future__ import annotations

import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--share-root", required=True)
    args, _ = parser.parse_known_args(argv)

    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))

    from core.models.remote_is_search_cfg_registry import ensure_for_algo

    result = ensure_for_algo("smz", str(args.share_root))
    if result.ok:
        print(f"[OK] {result.message}")
        return 0
    print(f"[ERROR] {result.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
