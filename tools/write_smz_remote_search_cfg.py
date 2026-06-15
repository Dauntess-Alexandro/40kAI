#!/usr/bin/env python3
"""Создать runtime/state/smz_remote_search_cfg.json с ПК1 (ростер GUI + hyperparams SMZ)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Сгенерировать smz_remote_search_cfg.json для remote inference server (ПК2)."
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Путь к JSON (по умолчанию: runtime/state/smz_remote_search_cfg.json)",
    )
    args = parser.parse_args(argv)

    root = _repo_root()
    sys.path.insert(0, str(root))

    from core.models.smz_remote_search_cfg_builder import write_smz_remote_search_cfg

    out, smb_out = write_smz_remote_search_cfg(args.output, repo_root=root)
    print(f"[OK] Written: {out}")
    if smb_out is not None:
        print(f"[OK] SMB copy:  {smb_out}")
        print("  PC2: set SMZ_REMOTE_SEARCH_CONFIG=Z:\\smz_remote_search_cfg.json")
    print("  Optional: git push on PC1 / git pull on PC2 for runtime/state copy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
