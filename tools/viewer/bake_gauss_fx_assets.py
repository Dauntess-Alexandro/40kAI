#!/usr/bin/env python3
"""Bake oversized Gauss FX PNG sources to viewer target sizes.

Sources are expected at app/viewer/assets/fx/<name>.png (often huge AI exports).
Backups go to app/viewer/assets/fx/_source/<name>.png once per file.
Run from repo root: python tools/viewer/bake_gauss_fx_assets.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FX_DIR = ROOT / "app" / "viewer" / "assets" / "fx"
SOURCE_DIR = FX_DIR / "_source"

TARGETS: dict[str, tuple[int, int]] = {
    "gauss_muzzle_atlas": (256, 64),
    "gauss_glow_radial": (128, 128),
    "gauss_noise_stripe": (512, 16),
    "gauss_scorch_decal": (96, 96),
    "necron_glyphs_atlas": (256, 256),
    "gauss_impact_ring": (128, 128),
}

RESAMPLE = Image.Resampling.LANCZOS


def premultiply_rgba(img: Image.Image) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a <= 0:
                px[x, y] = (0, 0, 0, 0)
                continue
            af = a / 255.0
            px[x, y] = (
                int(r * af + 0.5),
                int(g * af + 0.5),
                int(b * af + 0.5),
                a,
            )
    return img


def save_baked(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    premultiply_rgba(img).save(path, format="PNG", optimize=True)


def backup_if_needed(src: Path) -> None:
    backup = SOURCE_DIR / src.name
    if backup.exists():
        return
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, backup)
    print(f"  backup -> {backup.relative_to(ROOT)}")


def resize_cover(img: Image.Image, tw: int, th: int) -> Image.Image:
    """Scale to cover tw×th, center-crop."""
    w, h = img.size
    scale = max(tw / w, th / h)
    nw, nh = max(1, int(w * scale + 0.5)), max(1, int(h * scale + 0.5))
    img = img.resize((nw, nh), RESAMPLE)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return img.crop((left, top, left + tw, top + th))


def bake_muzzle_atlas(src: Image.Image) -> Image.Image:
    """4 frames in a row -> 256×64 (4× 64×64)."""
    w, h = src.size
    frames = 4
    slice_w = w // frames
    out = Image.new("RGBA", (256, 64), (0, 0, 0, 0))
    for i in range(frames):
        box = (i * slice_w, 0, (i + 1) * slice_w if i < frames - 1 else w, h)
        frame = src.crop(box)
        frame = resize_cover(frame, 64, 64)
        out.paste(frame, (i * 64, 0))
    return out


def bake_noise_stripe(src: Image.Image) -> Image.Image:
    """Wide tile: center horizontal band, squash to 512×16."""
    w, h = src.size
    band_h = max(8, h // 12)
    top = (h - band_h) // 2
    band = src.crop((0, top, w, top + band_h))
    return band.resize((512, 16), RESAMPLE)


def bake_glyphs_atlas(src: Image.Image) -> Image.Image:
    """2048² 4×4 grid -> 256² (64² cells)."""
    return src.resize((256, 256), RESAMPLE)


def bake_default(src: Image.Image, tw: int, th: int) -> Image.Image:
    return resize_cover(src, tw, th)


def bake_one(name: str, tw: int, th: int) -> bool:
    path = FX_DIR / f"{name}.png"
    if not path.exists():
        print(f"SKIP missing {path.relative_to(ROOT)}")
        return False

    src = Image.open(path).convert("RGBA")
    sw, sh = src.size
    if sw == tw and sh == th:
        print(f"OK   {name}: already {tw}x{th}")
        return True

    print(f"BAKE {name}: {sw}x{sh} -> {tw}x{th}")
    backup_if_needed(path)

    if name == "gauss_muzzle_atlas":
        baked = bake_muzzle_atlas(src)
    elif name == "gauss_noise_stripe":
        baked = bake_noise_stripe(src)
    elif name == "necron_glyphs_atlas":
        baked = bake_glyphs_atlas(src)
    else:
        baked = bake_default(src, tw, th)

    save_baked(baked, path)
    kb = path.stat().st_size / 1024
    print(f"  wrote {path.relative_to(ROOT)} ({kb:.0f} KB)")
    return True


def main() -> int:
    ok = 0
    for name, (tw, th) in TARGETS.items():
        if bake_one(name, tw, th):
            ok += 1
    print(f"\nDone: {ok}/{len(TARGETS)} assets.")
    print(f"Full-res backups: {SOURCE_DIR.relative_to(ROOT)}/")
    return 0 if ok == len(TARGETS) else 1


if __name__ == "__main__":
    sys.exit(main())
