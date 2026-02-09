#!/usr/bin/env python3
import json
import random
import time
from itertools import cycle
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATE_PATH = BASE_DIR / "viewer_state.json"
ASSETS_DIR = BASE_DIR / "assets"


def list_pngs(subdir: str) -> list[str]:
    path = ASSETS_DIR / subdir
    if not path.exists():
        return []
    return sorted(p.name for p in path.iterdir() if p.suffix.lower() == ".png")


def pick_first(items: list[str]) -> str | None:
    return items[0] if items else None


def build_state(tick: int, assets: dict) -> dict:
    ground_tile = pick_first(assets["ground"]) or "ground_01.png"
    unit_sprites = assets["units"] or ["necron_01.png", "necron_02.png"]
    prop_sprites = assets["props"] or ["tree_01.png", "crate_01.png"]
    shadow_sprites = assets["shadows"] or ["shadow_small.png", "shadow_medium.png"]
    fx_sprites = assets["fx"] or ["smoke_01.png"]
    decal_sprites = assets["decals"] or ["blood_01.png", "scorch_01.png"]

    unit_cycle = cycle(unit_sprites)
    shadow_cycle = cycle(shadow_sprites)

    return {
        "camera": {"x": 640, "y": 360, "zoom": 1.0},
        "ground": {"tile": ground_tile},
        "units": [
            {
                "id": 1,
                "x": 520 + tick * 4,
                "y": 310,
                "sprite": next(unit_cycle),
                "shadow": next(shadow_cycle),
                "dir": (tick * 8) % 360,
            },
            {
                "id": 2,
                "x": 740,
                "y": 420 + (tick % 60),
                "sprite": next(unit_cycle),
                "shadow": next(shadow_cycle),
                "dir": (180 + tick * 4) % 360,
            },
        ],
        "props": [
            {
                "x": 400,
                "y": 520,
                "sprite": random.choice(prop_sprites),
                "shadow": random.choice(shadow_sprites),
            },
            {
                "x": 860,
                "y": 280,
                "sprite": random.choice(prop_sprites),
                "shadow": random.choice(shadow_sprites),
            },
        ],
        "fx": [
            {
                "type": random.choice(fx_sprites),
                "x": 540,
                "y": 300,
                "scale": 1.2,
            }
        ],
        "decals": [
            {
                "type": random.choice(decal_sprites),
                "x": 480 + random.randint(-80, 80),
                "y": 290 + random.randint(-80, 80),
                "rotation": random.random() * 2,
                "scale": 1.0,
            }
        ],
    }


def main() -> None:
    assets = {
        "ground": list_pngs("ground"),
        "props": list_pngs("props"),
        "shadows": list_pngs("shadows"),
        "fx": list_pngs("fx"),
        "decals": list_pngs("decals"),
        "units": list_pngs("units"),
    }

    tick = 0
    while True:
        state = build_state(tick, assets)
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tick += 1
        time.sleep(0.15)


if __name__ == "__main__":
    main()
