"""
Одноразовая чистка gauss_reaper_icon.png: снять коричневато-серый ореол JPEG у границы с прозрачностью.
Запуск: python tools/fix_gauss_reaper_icon.py
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def dilate_transparent(opaque: np.ndarray, iterations: int) -> np.ndarray:
    """True = в пределах iterations шагов от любой прозрачной клетки (8-соседство)."""
    h, w = opaque.shape
    trans = ~opaque
    region = trans.copy()
    for _ in range(iterations):
        nxt = region.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                ys, ye = max(0, -dy), min(h, h - dy)
                xs, xe = max(0, -dx), min(w, w - dx)
                nxt[ys:ye, xs:xe] |= region[ys + dy : ye + dy, xs + dx : xe + dx]
        region = nxt
    return region


def saturation(rgb: np.ndarray) -> np.ndarray:
    r = rgb[:, :, 0].astype(np.float32)
    g = rgb[:, :, 1].astype(np.float32)
    b = rgb[:, :, 2].astype(np.float32)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    return np.where(mx > 1e-3, (mx - mn) / np.maximum(mx, 1.0), 0.0)


def clean_icon(path: Path) -> None:
    img = Image.open(path).convert("RGBA")
    a = np.array(img)
    h, w = a.shape[:2]
    opaque = a[:, :, 3] > 128
    rgb = a[:, :, :3]
    sat = saturation(rgb)

    near_trans = dilate_transparent(opaque, iterations=2)
    # ореол: рядом с «настоящим» фоном и низкая насыщенность (не зелёные трубки)
    greenish = (rgb[:, :, 1].astype(np.float32) > rgb[:, :, 0] + 15) & (
        rgb[:, :, 1].astype(np.float32) > rgb[:, :, 2] + 15
    )
    remove = opaque & near_trans & (sat < 0.16) & ~greenish

    # одиночные очень яркие артефакты на тёмном фоне
    lum = rgb.astype(np.float32).mean(axis=2)
    stray = opaque & (lum > 245) & (sat < 0.05)
    remove |= stray

    a2 = a.copy()
    a2[remove, 3] = 0
    Image.fromarray(a2).save(path, optimize=True)
    print(f"OK {path}: removed {int(remove.sum())} px")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    for rel in (
        "app/gui_qt/assets/gauss_reaper_icon.png",
        "app/viewer/assets/icons/gauss_reaper_icon.png",
    ):
        clean_icon(root / rel)


if __name__ == "__main__":
    main()
