from __future__ import annotations

from typing import Any, Optional


def _format_faction(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if not text:
        return ""
    if text.isupper():
        return text.title()
    return text


def format_unit(
    unit_id: Optional[int],
    unit_data: Optional[dict] = None,
    *,
    instance_id: Optional[str] = None,
    include_instance_id: bool = False,
) -> str:
    base = f"Unit {unit_id}" if unit_id is not None else "Unit <unknown>"

    if not unit_data:
        return f"{base} — <unknown>"

    name = unit_data.get("Name") or unit_data.get("name")
    faction = _format_faction(
        unit_data.get("Faction")
        or unit_data.get("Army Faction")
        or unit_data.get("Army")
    )
    models = unit_data.get("#OfModels") or unit_data.get("Models") or unit_data.get("models")

    if name and faction:
        main = f"{faction} {name}"
    elif name:
        main = str(name)
    elif faction:
        main = faction
    else:
        main = "<unknown>"

    extras = []
    if models is not None:
        try:
            extras.append(f"x{int(models)} моделей")
        except (TypeError, ValueError):
            extras.append(f"x{models} моделей")
    if include_instance_id and instance_id:
        extras.append(f"id={instance_id}")

    if extras:
        return f"{base} — {main} ({', '.join(extras)})"
    return f"{base} — {main}"
