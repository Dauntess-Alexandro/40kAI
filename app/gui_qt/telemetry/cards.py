from __future__ import annotations

from typing import Any, Optional

COLOR_GPU = "#3fae6e"
COLOR_CPU = "#4a90d9"
COLOR_RAM = "#d9a441"
COLOR_TEMP = "#e06a4a"
COLOR_WARN = "#e0524a"
WARN_PCT = 90


def _gb(mb: Optional[int]) -> str:
    if not mb:
        return "0.0G"
    return f"{mb / 1024.0:.1f}G"


def _gpu_card(card_id: str, name: str, util, used_mb, total_mb, temp, variant: str, active: bool) -> dict[str, Any]:
    has = active and util is not None
    pct = int(util) if has else 0
    return {
        "id": card_id,
        "icon": "server" if variant == "remote" else "gpu",
        "label": name,
        "valueText": (f"{pct}%" if has else "—"),
        "sub": (f"{_gb(used_mb)}/{_gb(total_mb)}" + (f" · {temp}°" if temp is not None else "")) if active else "—",
        "pct": pct,
        "color": COLOR_WARN if (has and pct >= WARN_PCT) else COLOR_GPU,
        "warn": bool(has and pct >= WARN_PCT),
        "variant": variant,
    }


def build_cards(
    *, local: dict[str, Any], remote: Optional[dict[str, Any]],
    batch_avg: Optional[float], batch_size_hint: Optional[int],
    algo: str, active: bool,
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []

    for g in local.get("gpus", []):
        cards.append(_gpu_card(
            f"gpu{g['index']}", g.get("name", "GPU"), g.get("util"),
            g.get("mem_used_mb"), g.get("mem_total_mb"), g.get("temp_c"),
            variant="local", active=active,
        ))

    if remote is not None:
        cards.append(_gpu_card(
            "pc2", f"ПК2 · {remote.get('name', 'GPU')}", remote.get("util"),
            remote.get("mem_used_mb"), remote.get("mem_total_mb"), remote.get("temp_c"),
            variant="remote", active=active,
        ))

    cpu_pct = int(round(local.get("cpu_pct", 0.0))) if active else 0
    cards.append({
        "id": "cpu", "icon": "cpu", "label": "CPU",
        "valueText": (f"{cpu_pct}%" if active else "—"),
        "sub": "процесс", "pct": cpu_pct,
        "color": COLOR_WARN if (active and cpu_pct >= WARN_PCT) else COLOR_CPU,
        "warn": bool(active and cpu_pct >= WARN_PCT), "variant": "local",
    })

    ram_pct = int(round(local.get("ram_pct", 0.0))) if active else 0
    cards.append({
        "id": "ram", "icon": "ram", "label": "RAM",
        "valueText": (f"{ram_pct}%" if active else "—"),
        "sub": (f"{local.get('ram_gb', 0.0):.1f}G" if active else "—"), "pct": ram_pct,
        "color": COLOR_WARN if (active and ram_pct >= WARN_PCT) else COLOR_RAM,
        "warn": bool(active and ram_pct >= WARN_PCT), "variant": "local",
    })

    if str(algo).lower() == "gumbel_muzero":
        avg = remote.get("avg_batch") if (remote and remote.get("avg_batch") is not None) else batch_avg
        hint = int(batch_size_hint) if batch_size_hint else None
        if active and avg is not None:
            pct = int(min(100.0, (avg / hint) * 100.0)) if hint else 0
            vtext = f"{avg:.1f}" + (f"/{hint}" if hint else "")
        else:
            pct, vtext = 0, "—"
        cards.append({
            "id": "batch", "icon": "batch", "label": "Батч поиска",
            "valueText": vtext, "sub": "ср. размер", "pct": pct,
            "color": COLOR_GPU, "warn": False, "variant": "local",
        })

    return cards
