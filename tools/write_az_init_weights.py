"""Bootstrap initial weights для AZ remote IS (AlphaZero tree) БЕЗ предобучения на ПК1.

Строит AZ-сеть из az_remote_search_cfg.json и сохраняет СЛУЧАЙНО инициализированные веса
latest_az_tree_policy.pth рядом с cfg. После этого лаунчер ПК2 найдёт веса и сервер стартует;
ПК1-learner потом синканёт настоящие веса (формы совпадают — обе строятся из cfg).

Примеры:
  python tools/write_az_init_weights.py --share \\\\USER-PC\\models
  python tools/write_az_init_weights.py --search-cfg PATH\\az_remote_search_cfg.json --out PATH\\latest_az_tree_policy.pth
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models.alphazero_model import write_az_init_weights_from_cfg  # noqa: E402

# AZ-семья едет на общей сети (AlphaZeroPolicyValueNet) — один инструмент, имена файлов по algo.
_NAMES = {
    "az": ("az_remote_search_cfg.json", "latest_az_tree_policy.pth"),
    "gaz": ("gaz_remote_search_cfg.json", "latest_az_gumbel_az_policy.pth"),
}


def _derive_paths(share: str, algo: str) -> tuple[str, str]:
    """Из корня шары вывести пути cfg и весов в actor_sync/ (с фолбэком на корень шары)."""
    cfg_name, w_name = _NAMES[str(algo).lower()]
    sub = os.path.join(share, "actor_sync")
    base = sub if os.path.isfile(os.path.join(sub, cfg_name)) else share
    return os.path.join(base, cfg_name), os.path.join(base, w_name)


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap random init weights для AZ/GAZ remote IS.")
    ap.add_argument("--algo", default="az", choices=["az", "gaz"], help="алгоритм AZ-семьи (по умолчанию az)")
    ap.add_argument("--share", default="", help="корень общей папки (SMB), напр. \\\\USER-PC\\models")
    ap.add_argument("--search-cfg", default="", help="путь к *_remote_search_cfg.json (вместо --share)")
    ap.add_argument("--out", default="", help="путь к latest_*_policy.pth (вместо --share)")
    args = ap.parse_args()

    cfg_path, out_path = str(args.search_cfg), str(args.out)
    if not cfg_path or not out_path:
        if not args.share:
            print("[ОШИБКА] укажи либо --share, либо оба --search-cfg и --out.", flush=True)
            return 2
        cfg_path, out_path = _derive_paths(str(args.share), str(args.algo))

    if not os.path.isfile(cfg_path):
        print(
            f"[ОШИБКА] search_cfg не найден: {cfg_path}\n"
            "Что делать: сначала опубликуй cfg (GUI ПК1 / ensure_remote_search_cfg) или проверь путь шары.",
            flush=True,
        )
        return 1
    if os.path.isfile(out_path):
        print(f"[ПРОПУСК] веса уже есть: {out_path} (удали вручную, если нужен пере-bootstrap).", flush=True)
        return 0

    write_az_init_weights_from_cfg(cfg_path, out_path)
    print(
        f"[OK] bootstrap-веса записаны: {out_path}\n"
        f"     (случайная инициализация из {os.path.basename(cfg_path)}; "
        "теперь сервер ПК2 стартует без предобучения, learner синканёт настоящие веса).",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
