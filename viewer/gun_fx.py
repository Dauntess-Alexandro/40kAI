from __future__ import annotations

from typing import Dict


GAUSS_FLAYER_FX = {
    "weapon_name": "Gauss flayer",
    "duration": 3.5,
    "core_life": 0.22,
    "glow_life": 0.34,
    "flash_life": 0.14,
    "ring_life": 0.38,
    "glow_width_px": 10.0,
    "glow_jitter_px": 2.0,
    "glow_jitter_speed": 18.0,
    "core_width_px": 2.0,
    "core_gap_px": 3.0,
    "pulse_len_px": 8.0,
    "pulse_gap_px": 14.0,
    "pulse_speed": 2.2,
    "pulse_width_px": 3.0,
    "pulse_alpha": 0.65,
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
    "branches": {
        "count_min": 10,
        "count_max": 18,
        "life_min": 0.10,
        "life_max": 0.18,
        "width_px": 1.0,
        "wide_width_px": 2.0,
        "wide_chance": 0.12,
        "len_min_px": 6.0,
        "len_max_px": 18.0,
        "alpha_min": 0.10,
        "alpha_max": 0.22,
        "spawn_rate_min": 2.0,
        "spawn_rate_max": 4.0,
        "fork_chance": 0.25,
    },
    "glyphs": {
        "count_min": 8,
        "count_max": 14,
        "alpha_min": 0.06,
        "alpha_max": 0.14,
        "scale_min_px": 1.6,
        "scale_max_px": 3.0,
        "offset_n_min_px": -4.0,
        "offset_n_max_px": 4.0,
        "drift_speed_min": 0.10,
        "drift_speed_max": 0.25,
        "life_min": 0.25,
        "life_max": 0.45,
        "period_min": 0.7,
        "period_max": 1.4,
    },
    "edge_specks": {
        "count_min": 60,
        "count_max": 120,
        "life_min": 0.16,
        "life_max": 0.26,
        "size_min_px": 1.0,
        "size_max_px": 3.0,
        "alpha_min": 0.08,
        "alpha_max": 0.18,
        "offset_min_px": 2.0,
        "offset_max_px": 6.0,
        "speed_min": 0.6,
        "speed_max": 1.8,
        "wobble_min_px": 0.5,
        "wobble_max_px": 1.5,
        "period_min": 0.35,
        "period_max": 0.6,
    },
}

GUN_FX_CONFIGS: Dict[str, Dict] = {
    "gauss flayer": GAUSS_FLAYER_FX,
}


def get_gun_fx_config(weapon_name: str) -> Dict:
    if not weapon_name:
        return {}
    return GUN_FX_CONFIGS.get(weapon_name.strip().lower(), {})
