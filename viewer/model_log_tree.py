from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


PHASE_ORDER = ["command", "movement", "shooting", "charge", "fight"]
PHASE_LABELS = {
    "command": "ФАЗА КОМАНДОВАНИЯ",
    "movement": "ФАЗА ДВИЖЕНИЯ",
    "shooting": "ФАЗА СТРЕЛЬБЫ",
    "charge": "ФАЗА ЧАРДЖА",
    "fight": "ФАЗА БОЯ",
}


TYPE_ICONS = {
    "phase_start": "🟢",
    "phase_end": "🔴",
    "unit_start": "🧩",
    "move": "👣",
    "shoot": "🎯",
    "charge": "⚡",
    "fight": "⚔️",
    "dice": "🎲",
    "skip": "⏭️",
    "scan": "🔎",
    "vp": "🏁",
    "reward": "💠",
    "summary": "📝",
}


@dataclass
class UnitNode:
    unit_id: Optional[int]
    unit_name: Optional[str]
    events: List[dict] = field(default_factory=list)


@dataclass
class PhaseNode:
    phase: str
    unit_order: List[Optional[int]] = field(default_factory=list)
    units: Dict[Optional[int], UnitNode] = field(default_factory=dict)


@dataclass
class RoundNode:
    round_id: int
    phase_order: List[str] = field(default_factory=list)
    phases: Dict[str, PhaseNode] = field(default_factory=dict)


class ModelLogTreeBuilder:
    def __init__(self) -> None:
        self.rounds: Dict[int, RoundNode] = {}

    def reset(self) -> None:
        self.rounds = {}

    def add_event(self, event: dict) -> None:
        if not isinstance(event, dict):
            return
        round_id = event.get("battle_round")
        if round_id is None:
            return
        phase = event.get("phase") or "unknown"
        unit_id = event.get("unit_id")
        unit_name = event.get("unit_name")
        round_node = self.rounds.setdefault(int(round_id), RoundNode(round_id=int(round_id)))
        if phase not in round_node.phases:
            round_node.phases[phase] = PhaseNode(phase=phase)
            if phase in PHASE_ORDER:
                if phase not in round_node.phase_order:
                    round_node.phase_order.append(phase)
            else:
                round_node.phase_order.append(phase)
        phase_node = round_node.phases[phase]
        unit_key = unit_id
        if unit_key not in phase_node.units:
            phase_node.units[unit_key] = UnitNode(unit_id=unit_id, unit_name=unit_name)
            phase_node.unit_order.append(unit_key)
        phase_node.units[unit_key].events.append(event)
        if os.getenv("EVT_DEBUG", "0") == "1":
            sys.stderr.write(
                f"[EVT_DEBUG] accept: round={round_id} phase={phase} unit={unit_id}\n"
            )

    def ingest(self, events: List[dict]) -> None:
        self.reset()
        for event in events:
            self.add_event(event)

    def render_text(self, include_verbose: bool = False, only_round: Optional[int] = None) -> str:
        lines: List[str] = []
        for round_id in sorted(self.rounds.keys()):
            if only_round is not None and int(round_id) != int(only_round):
                continue
            round_node = self.rounds[round_id]
            lines.append(f"=== БОЕВОЙ РАУНД {round_id} ===")
            for phase in self._phase_iter(round_node):
                phase_label = PHASE_LABELS.get(phase, f"ФАЗА {phase.upper()}")
                lines.append(f"  --- {phase_label} ---")
                phase_node = round_node.phases[phase]
                for unit_key in phase_node.unit_order:
                    unit_node = phase_node.units[unit_key]
                    unit_title = self._format_unit_title(unit_node)
                    lines.append(f"    {unit_title}")
                    for event in unit_node.events:
                        if not include_verbose and event.get("verbosity") == "verbose":
                            continue
                        lines.append(self._format_event_line(event))
        return "\n".join(lines)

    def _phase_iter(self, round_node: RoundNode) -> List[str]:
        ordered = []
        for phase in PHASE_ORDER:
            if phase in round_node.phase_order:
                ordered.append(phase)
        for phase in round_node.phase_order:
            if phase not in ordered:
                ordered.append(phase)
        return ordered

    def _format_unit_title(self, unit_node: UnitNode) -> str:
        if unit_node.unit_id is None:
            return "Общие события фазы"
        if unit_node.unit_name:
            return f"Unit {unit_node.unit_id} — {unit_node.unit_name}"
        return f"Unit {unit_node.unit_id}"

    def _format_event_line(self, event: dict) -> str:
        event_type = event.get("type", "summary")
        icon = TYPE_ICONS.get(event_type, "•")
        msg = event.get("msg") or ""
        return f"      {icon} {msg}"
