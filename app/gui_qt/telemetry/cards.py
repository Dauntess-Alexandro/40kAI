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


def _cpu_card(card_id: str, label: str, value, active: bool, variant: str) -> dict[str, Any]:
    cpu_pct = int(round(value)) if (active and value is not None) else 0
    return {
        "id": card_id, "icon": "cpu", "label": label,
        "valueText": (f"{cpu_pct}%" if (active and value is not None) else "—"),
        "sub": "система", "pct": cpu_pct,
        "color": COLOR_WARN if (active and cpu_pct >= WARN_PCT) else COLOR_CPU,
        "warn": bool(active and cpu_pct >= WARN_PCT), "variant": variant,
    }


def build_cards(
    *, local: dict[str, Any], remote: Optional[dict[str, Any]],
    batch_avg: Optional[float], batch_size_hint: Optional[int],
    algo: str, active: bool, labels: Optional[dict[str, Any]] = None,
) -> list[dict[str, Any]]:
    cards: list[dict[str, Any]] = []
    labels = labels or {}

    # В режиме двух ПК (есть remote) подписываем локальные карточки префиксом «ПК1»,
    # чтобы не путать с «ПК2 · …». На одном ПК префикс не добавляем.
    pc1_prefix = "ПК1 · " if remote is not None else ""

    # P3: имена железа можно переопределить через telemetry_labels.json
    # (pc1_gpu / pc1_cpu / pc2_gpu / pc2_cpu), иначе берём то, что отдаёт NVML/health.
    def _label(key: str, fallback: str) -> str:
        override = str(labels.get(key, "") or "").strip()
        return override or fallback

    for g in local.get("gpus", []):
        gpu_name = _label("pc1_gpu", g.get("name", "GPU"))
        cards.append(_gpu_card(
            f"gpu{g['index']}", f"{pc1_prefix}{gpu_name}", g.get("util"),
            g.get("mem_used_mb"), g.get("mem_total_mb"), g.get("temp_c"),
            variant="local", active=active,
        ))

    if remote is not None:
        gpu_name = _label("pc2_gpu", remote.get("name", "GPU"))
        cards.append(_gpu_card(
            "pc2", f"ПК2 · {gpu_name}", remote.get("util"),
            remote.get("mem_used_mb"), remote.get("mem_total_mb"), remote.get("temp_c"),
            variant="remote", active=active,
        ))

    # CPU ПК1: загрузка всей машины («система»), а не только дерева train.
    # Fallback на process-метрику, если системная недоступна (старый psutil/нет данных).
    cpu_sys = local.get("cpu_pct_system")
    cpu_value = cpu_sys if cpu_sys is not None else local.get("cpu_pct", 0.0)
    pc1_cpu_name = str(local.get("cpu_name") or "CPU")
    cards.append(_cpu_card(
        "cpu", f"{pc1_prefix}{_label('pc1_cpu', pc1_cpu_name)}", cpu_value, active, "local",
    ))

    # P1: CPU ПК2 — только если сервер прислал системную метрику (новый ПК2).
    if remote is not None and remote.get("cpu_pct_system") is not None:
        pc2_cpu_name = _label("pc2_cpu", str(remote.get("cpu_name") or "CPU"))
        cards.append(_cpu_card(
            "pc2_cpu", f"ПК2 · {pc2_cpu_name}", remote.get("cpu_pct_system"), active, "remote",
        ))

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
