#!/usr/bin/env python3
import json
import random
import time
from pathlib import Path

STATE_PATH = Path(__file__).with_name("viewer_state.json")

SPRITES = ["necron_01.png", "necron_02.png"]
PROP_SPRITES = ["tree_01.png", "crate_01.png"]
SHADOWS = ["shadow_small.png", "shadow_medium.png"]
FX_SPRITES = ["smoke_01.png"]
DECALS = ["blood_01.png", "scorch_01.png"]
GROUND_TILE = "ground_01.png"


def build_state(tick: int) -> dict:
    return {
        "camera": {"x": 640, "y": 360, "zoom": 1.0},
        "ground": {"tile": GROUND_TILE},
        "units": [
            {
                "id": 1,
                "x": 520 + tick * 4,
                "y": 310,
                "sprite": SPRITES[0],
                "shadow": SHADOWS[0],
                "dir": (tick * 8) % 360,
            },
            {
                "id": 2,
                "x": 740,
                "y": 420 + (tick % 60),
                "sprite": SPRITES[1],
                "shadow": SHADOWS[0],
                "dir": (180 + tick * 4) % 360,
            },
        ],
        "props": [
            {"x": 400, "y": 520, "sprite": PROP_SPRITES[0], "shadow": SHADOWS[1]},
            {"x": 860, "y": 280, "sprite": PROP_SPRITES[1], "shadow": SHADOWS[0]},
        ],
        "fx": [
            {"type": FX_SPRITES[0], "x": 540, "y": 300, "scale": 1.2}
        ],
        "decals": [
            {
                "type": random.choice(DECALS),
                "x": 480 + random.randint(-80, 80),
                "y": 290 + random.randint(-80, 80),
                "rotation": random.random() * 2,
                "scale": 1.0,
            }
        ],
    }


def main() -> None:
    tick = 0
    while True:
        state = build_state(tick)
        STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tick += 1
        time.sleep(0.15)


if __name__ == "__main__":
    main()
