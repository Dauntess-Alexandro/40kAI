from __future__ import annotations

import re
from collections import OrderedDict, defaultdict
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple


PHASE_ORDER = ["command", "movement", "shooting", "charge", "fight"]
PHASE_LABELS = {
    "command": "ФАЗА КОМАНДОВАНИЯ",
    "movement": "ФАЗА ДВИЖЕНИЯ",
    "shooting": "ФАЗА СТРЕЛЬБЫ",
    "charge": "ФАЗА ЧАРДЖА",
    "fight": "ФАЗА БОЯ",
}

MOVE_BEFORE_RE = re.compile(
    r"Позиция до: \((?P<x>-?\d+),\s*(?P<y>-?\d+)\)\. "
    r"Выбор: (?P<dir>[^,]+), advance=(?P<adv>да|нет)"
    r"(?:, бросок=(?P<roll>\d+), макс=(?P<max>\d+))?, distance=(?P<dist>\d+)"
)
MOVE_AFTER_RE = re.compile(r"Позиция после: \((?P<x>-?\d+),\s*(?P<y>-?\d+)\)")


@dataclass
class UnitPhaseData:
    unit_id: int
    unit_name: Optional[str]
    events: List[dict] = field(default_factory=list)
    move_from: Optional[Tuple[int, int]] = None
    move_to: Optional[Tuple[int, int]] = None
    move_dir: Optional[str] = None
    move_dist: Optional[int] = None
    move_advance: Optional[bool] = None
    move_roll: Optional[int] = None
    move_max: Optional[int] = None
    action_msg: Optional[str] = None
    skip_reason: Optional[str] = None


@dataclass
class PhaseData:
    phase: str
    units: Dict[int, UnitPhaseData] = field(default_factory=dict)
    unit_order: List[int] = field(default_factory=list)
    phase_events: List[dict] = field(default_factory=list)
    round_end_messages: List[str] = field(default_factory=list)


def render_model_log_flat(
    events: Iterable[dict],
    include_verbose: bool = False,
    only_round: Optional[int] = None,
) -> str:
    rounds = _build_rounds(events, include_verbose=include_verbose, only_round=only_round)
    lines: List[str] = []
    for round_id, phases in rounds.items():
        lines.append(f"=== БОЕВОЙ РАУНД {round_id} ===")
        lines.append("")
        for phase in PHASE_ORDER:
            if phase not in phases:
                continue
            phase_data = phases[phase]
            if not phase_data.units and not phase_data.phase_events:
                continue
            phase_label = PHASE_LABELS.get(phase, f"ФАЗА {phase.upper()}")
            lines.append(f"--- {phase_label} ---")
            lines.append(f"📌 Итог: {_render_phase_summary(phase, phase_data)}")
            lines.append("")
            for unit_id in phase_data.unit_order:
                unit_data = phase_data.units[unit_id]
                lines.append(_format_unit_title(unit_data))
                main_line = _format_unit_main_line(phase, unit_data)
                if main_line:
                    lines.append(main_line)
                lines.append("")
        for phase_data in phases.values():
            for msg in phase_data.round_end_messages:
                lines.append(msg)
        if lines and lines[-1] == "":
            lines.pop()
        lines.append("")
    if lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _build_rounds(
    events: Iterable[dict],
    include_verbose: bool,
    only_round: Optional[int],
) -> Dict[int, Dict[str, PhaseData]]:
    rounds: Dict[int, Dict[str, PhaseData]] = OrderedDict()
    for event in events:
        if not isinstance(event, dict):
            continue
        if not include_verbose and event.get("verbosity") == "verbose":
            continue
        round_id = event.get("battle_round")
        if round_id is None:
            continue
        if only_round is not None and int(round_id) != int(only_round):
            continue
        phase = event.get("phase") or "unknown"
        rounds.setdefault(int(round_id), OrderedDict())
        phases = rounds[int(round_id)]
        if phase not in phases:
            phases[phase] = PhaseData(phase=phase)
        phase_data = phases[phase]
        if _is_round_end_event(event):
            phase_data.round_end_messages.append(_format_round_end(event, round_id))
        unit_id = event.get("unit_id")
        if unit_id is None:
            phase_data.phase_events.append(event)
            continue
        unit_id = int(unit_id)
        if unit_id not in phase_data.units:
            phase_data.units[unit_id] = UnitPhaseData(unit_id=unit_id, unit_name=event.get("unit_name"))
            phase_data.unit_order.append(unit_id)
        unit_data = phase_data.units[unit_id]
        unit_data.events.append(event)
        _parse_unit_event(phase, unit_data, event)
    return rounds


def _is_round_end_event(event: dict) -> bool:
    msg = str(event.get("msg") or "").lower()
    return "конец боевого раунда" in msg


def _format_round_end(event: dict, round_id: int) -> str:
    msg = event.get("msg") or f"Конец раунда {round_id}"
    return f"🏁 {msg}"


def _parse_unit_event(phase: str, unit_data: UnitPhaseData, event: dict) -> None:
    msg = str(event.get("msg") or "")
    if event.get("type") == "unit_start":
        return
    if phase == "movement":
        before = MOVE_BEFORE_RE.search(msg)
        if before:
            unit_data.move_from = (int(before.group("x")), int(before.group("y")))
            unit_data.move_dir = before.group("dir")
            unit_data.move_advance = before.group("adv") == "да"
            unit_data.move_roll = _safe_int(before.group("roll"))
            unit_data.move_max = _safe_int(before.group("max"))
            unit_data.move_dist = _safe_int(before.group("dist"))
            return
        after = MOVE_AFTER_RE.search(msg)
        if after:
            unit_data.move_to = (int(after.group("x")), int(after.group("y")))
            return
        if "Движение пропущено" in msg or "no move" in msg:
            unit_data.move_dist = 0
            return
    if _is_action_msg(phase, msg) and unit_data.action_msg is None:
        unit_data.action_msg = _short_action_msg(msg)
    if _is_skip_msg(msg):
        unit_data.skip_reason = unit_data.skip_reason or _derive_reason_code(msg)


def _format_unit_title(unit_data: UnitPhaseData) -> str:
    if unit_data.unit_name:
        return f"Unit {unit_data.unit_id} — {unit_data.unit_name}"
    return f"Unit {unit_data.unit_id}"


def _format_unit_main_line(phase: str, unit_data: UnitPhaseData) -> str:
    if phase == "movement":
        return _format_move_line(unit_data)
    if phase == "shooting":
        return _format_action_line("SHOOT", "🎯", "shoot", unit_data)
    if phase == "charge":
        return _format_action_line("CHARGE", "⚡", "charge", unit_data)
    if phase == "fight":
        return _format_action_line("FIGHT", "⚔️", "fight", unit_data, no_action_label="No fight")
    return ""


def _format_move_line(unit_data: UnitPhaseData) -> str:
    dist = unit_data.move_dist if unit_data.move_dist is not None else 0
    if unit_data.move_from and unit_data.move_to and unit_data.move_from == unit_data.move_to:
        dist = 0
    if dist == 0:
        return "⏭️ No move: dist=0"
    if unit_data.move_from and unit_data.move_to:
        adv_text = "да" if unit_data.move_advance else "нет"
        adv_extra = ""
        if unit_data.move_roll is not None or unit_data.move_max is not None:
            adv_extra = f" (roll={unit_data.move_roll}, max={unit_data.move_max})"
        return (
            f"👣 Move: {unit_data.move_from} → {unit_data.move_to} | "
            f"dir={unit_data.move_dir or '—'} | adv={adv_text}{adv_extra} | "
            f"dist={dist}"
        )
    return "⏭️ No move: dist=0"


def _format_action_line(
    label: str,
    icon: str,
    action_name: str,
    unit_data: UnitPhaseData,
    no_action_label: str = "Skip",
) -> str:
    if unit_data.action_msg:
        return f"{icon} {label.title()}: {unit_data.action_msg}"
    reason = unit_data.skip_reason or "unknown"
    if action_name == "fight" and reason == "no_attacks":
        return f"⏭️ {no_action_label} (no_attacks)"
    return f"⏭️ Skip {action_name} ({reason})"


def _render_phase_summary(phase: str, phase_data: PhaseData) -> str:
    if phase == "command":
        return _summary_command(phase_data)
    if phase == "movement":
        return _summary_move(phase_data)
    if phase == "shooting":
        return _summary_action(phase_data, label="shots")
    if phase == "charge":
        return _summary_action(phase_data, label="charges")
    if phase == "fight":
        return _summary_action(phase_data, label="fights")
    return "нет данных"


def _summary_command(phase_data: PhaseData) -> str:
    vp = None
    cp = None
    for event in phase_data.phase_events:
        if event.get("type") == "phase_end":
            data = event.get("data", {})
            vp = data.get("vp", vp)
            cp = data.get("cp", cp)
    if vp is None and cp is None:
        return "нет данных"
    return f"VP={vp}, CP={cp}"


def _summary_move(phase_data: PhaseData) -> str:
    total_units = len(phase_data.units)
    if total_units == 0:
        return "нет данных"
    moved = 0
    advanced = 0
    dist_total = 0
    has_data = False
    for unit in phase_data.units.values():
        if unit.move_dist is None and unit.move_from is None:
            continue
        has_data = True
        dist = unit.move_dist or 0
        dist_total += dist
        if unit.move_advance:
            advanced += 1
        if dist > 0:
            moved += 1
    if not has_data:
        return "нет данных"
    return f"moved={moved}/{total_units}, advanced={advanced}, dist_total={dist_total}"


def _summary_action(phase_data: PhaseData, label: str) -> str:
    total_units = len(phase_data.units)
    if total_units == 0:
        return "нет данных"
    actions = 0
    skipped = 0
    reasons = defaultdict(int)
    for unit in phase_data.units.values():
        if unit.action_msg:
            actions += 1
            continue
        skipped += 1
        reason = unit.skip_reason or "unknown"
        reasons[reason] += 1
    reason_text = ""
    if reasons:
        joined = ", ".join(f"{key}={value}" for key, value in sorted(reasons.items()))
        reason_text = f" (reasons: {joined})"
    return f"{label}={actions}, skipped={skipped}{reason_text}"


def _is_skip_msg(msg: str) -> bool:
    lowered = msg.lower()
    return any(
        token in lowered
        for token in (
            "пропущ",
            "нет целей",
            "нет доступных целей",
            "невозможен",
            "недоступна",
            "нет доступных атак",
        )
    )


def _is_action_msg(phase: str, msg: str) -> bool:
    lowered = msg.lower()
    if phase == "shooting":
        return "итог урона" in lowered or "стреляет по" in lowered
    if phase == "charge":
        return "чардж цели" in lowered or "charge объявлен" in lowered or "результат: успех" in lowered
    if phase == "fight":
        return "итог атаки" in lowered or "в бою с" in lowered
    return False


def _short_action_msg(msg: str) -> str:
    return msg.replace("\n", " ").strip()


def _derive_reason_code(msg: str) -> str:
    lowered = msg.lower()
    if "advance без assault" in lowered:
        return "advance_no_assault"
    if "advance — чардж невозможен" in lowered:
        return "advance"
    if "нет дальнобойного оружия" in lowered:
        return "no_weapon"
    if "юнит мертв" in lowered:
        return "dead"
    if "нет целей" in lowered or "нет доступных целей" in lowered:
        return "no_targets"
    if "fall back" in lowered:
        return "fell_back"
    if "юнит в ближнем бою" in lowered:
        return "in_melee"
    if "недоступная цель" in lowered or "недоступен" in lowered:
        return "invalid_target"
    if "нет доступных атак" in lowered:
        return "no_attacks"
    return "unknown"


def _safe_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

