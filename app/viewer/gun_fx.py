from __future__ import annotations

from typing import Dict, Optional, Tuple


# *_px tuned for cell_size ~24; opengl_view applies modest sprite multipliers on top.
_GAUSS_BEAM_SPRITE = {
    "beam_glow_sprite_scale": 1.48,
    "beam_glow_step_px": 6.5,
    "beam_tube_alpha_scale": 0.72,
    "beam_noise_alpha_scale": 0.5,
    "beam_noise_scroll_px_s": 110.0,
    "impact_flash_sprite_scale": 1.55,
    "impact_ring_sprite_scale": 1.62,
    "scorch_ttl_s": 1.8,
    "scorch_base": 0.42,
    "scorch_scale": 1.2,
    "scorch_alpha": 0.95,
    "scorch_offset_px_min": 2.0,
    "scorch_offset_px_max": 4.0,
    "glyph_sprite_scale": 1.6,
    "glyph_pulse_speed": 1.0,
    "glyph_count_scale": 1.0,
    "muzzle_life_s": 0.20,
    "muzzle_scale": 1.28,
    "muzzle_stretch_x": 1.06,
}

GAUSS_FLAYER_FX = {
    **_GAUSS_BEAM_SPRITE,
    "weapon_name": "Gauss flayer",
    "duration": 3.0,
    "core_life": 0.22,
    "glow_life": 0.34,
    "flash_life": 0.14,
    "ring_life": 0.38,
    "glow_width_px": 9.0,
    "glow_jitter_px": 1.6,
    "glow_jitter_speed": 18.0,
    "core_width_px": 2.2,
    "core_gap_px": 2.4,
    "pulse_len_px": 8.0,
    "pulse_gap_px": 12.0,
    "pulse_speed": 2.2,
    "pulse_width_px": 2.4,
    "pulse_alpha": 0.72,
    "impact_flash_base": 0.06,
    "impact_flash_extra": 0.11,
    "impact_ring_base": 0.045,
    "impact_ring_extra": 0.24,
    "impact_ring_width_px": 2.2,
    "particle_color": (140, 255, 180),
    "glow_color": (90, 255, 140),
    "core_color": (140, 255, 190),
    "impact_color": (160, 255, 200),
    "pulse_color": (120, 255, 170),
    "branches": {
        "count_min": 8,
        "count_max": 14,
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
        "alpha_min": 0.12,
        "alpha_max": 0.26,
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
        "count_min": 40,
        "count_max": 80,
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

GAUSS_REAPER_FX = {
    **GAUSS_FLAYER_FX,
    "weapon_name": "Gauss reaper",
    "duration": 3.8,
    "core_life": 0.26,
    "glow_life": 0.38,
    "flash_life": 0.17,
    "ring_life": 0.42,
    "beam_glow_sprite_scale": 1.58,
    "beam_glow_step_px": 5.5,
    "beam_tube_alpha_scale": 0.78,
    "beam_noise_alpha_scale": 0.55,
    "beam_noise_scroll_px_s": 135.0,
    "impact_flash_sprite_scale": 1.62,
    "impact_ring_sprite_scale": 1.72,
    "scorch_ttl_s": 1.95,
    "scorch_base": 0.52,
    "scorch_scale": 1.55,
    "scorch_offset_px_min": 2.5,
    "scorch_offset_px_max": 4.5,
    "glyph_sprite_scale": 1.6,
    "glyph_pulse_speed": 1.35,
    "glyph_count_scale": 1.28,
    "muzzle_life_s": 0.26,
    "muzzle_scale": 1.58,
    "muzzle_stretch_x": 1.28,
    "glow_width_px": 12.0,
    "glow_jitter_px": 2.0,
    "core_width_px": 2.8,
    "core_gap_px": 3.0,
    "pulse_len_px": 10.0,
    "pulse_gap_px": 14.0,
    "pulse_speed": 1.5,
    "pulse_width_px": 3.0,
    "pulse_alpha": 0.78,
    "impact_flash_base": 0.07,
    "impact_flash_extra": 0.13,
    "impact_ring_base": 0.05,
    "impact_ring_extra": 0.3,
    "impact_ring_width_px": 2.6,
    "particle_color": (180, 255, 140),
    "glow_color": (110, 255, 90),
    "core_color": (170, 255, 150),
    "impact_color": (200, 255, 170),
    "pulse_color": (140, 255, 110),
    "branches": {
        **GAUSS_FLAYER_FX["branches"],
        "count_min": 10,
        "count_max": 16,
        "wide_chance": 0.16,
        "len_max_px": 14.0,
        "alpha_max": 0.24,
    },
    "edge_specks": {
        **GAUSS_FLAYER_FX["edge_specks"],
        "count_min": 50,
        "count_max": 95,
        "size_max_px": 3.2,
        "alpha_max": 0.2,
    },
}

GUN_FX_CONFIGS: Dict[str, Dict] = {
    "gauss flayer": GAUSS_FLAYER_FX,
    "gauss reaper": GAUSS_REAPER_FX,
}


# Подстрока в lower-cased weapon_name -> ключ в GUN_FX_CONFIGS.
# Порядок проверки — как в dict (Python 3.7+ сохраняет порядок вставки),
# поэтому более специфичные паттерны должны идти раньше общих.
WEAPON_ALIASES: Dict[str, str] = {
    "gauss reaper": "gauss reaper",
    "gauss flayer": "gauss flayer",
}


def get_gun_fx_config(weapon_name: str) -> Dict:
    if not weapon_name:
        return {}
    return GUN_FX_CONFIGS.get(weapon_name.strip().lower(), {})


def resolve_fx_profile(weapon_name: str) -> Optional[Tuple[str, Dict]]:
    """Find FX config for a weapon name.

    Returns (config_key, config_dict) or None if no profile matches.
    Lookup order: exact lower-cased key in GUN_FX_CONFIGS, then substring
    match against WEAPON_ALIASES patterns.
    """
    key = (weapon_name or "").strip().lower()
    if not key:
        return None
    if key in GUN_FX_CONFIGS:
        return key, GUN_FX_CONFIGS[key]
    for pattern, target in WEAPON_ALIASES.items():
        if pattern in key:
            cfg = GUN_FX_CONFIGS.get(target)
            if cfg is not None:
                return target, cfg
    return None
