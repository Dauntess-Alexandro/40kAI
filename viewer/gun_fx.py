from __future__ import annotations

from typing import Dict


GAUSS_FLAYER_FX = {
    "weapon_name": "Gauss flayer",
    "duration": 0.5,
    "core_life": 0.22,
    "glow_life": 0.34,
    "flash_life": 0.14,
    "ring_life": 0.38,
    "glow_width_px": 10.0,
    "glow_jitter_px": 2.0,
    "glow_jitter_speed": 18.0,
    "core_width_px": 2.0,
    "core_gap_px": 2.2,
    "pulse_len_px": 12.0,
    "pulse_gap_px": 18.0,
    "pulse_speed": 0.9,
    "pulse_width_px": 3.0,
    "pulse_alpha": 0.5,
    "impact_flash_base": 0.08,
    "impact_flash_extra": 0.12,
    "impact_ring_base": 0.05,
    "impact_ring_extra": 0.3,
    "impact_ring_width_px": 2.5,
    "particle_color": (140, 255, 180),
    "glow_color": (90, 255, 140),
    "core_color": (140, 255, 190),
    "impact_color": (160, 255, 200),
    "pulse_color": (120, 255, 170),
}

GUN_FX_CONFIGS: Dict[str, Dict] = {
    "gauss flayer": GAUSS_FLAYER_FX,
}


def get_gun_fx_config(weapon_name: str) -> Dict:
    if not weapon_name:
        return {}
    return GUN_FX_CONFIGS.get(weapon_name.strip().lower(), {})
