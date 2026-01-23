from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import ast
import re


PHASE_TRANSLATIONS = {
    "command": "КОМАНДА",
    "movement": "ДВИЖЕНИЕ",
    "psychic": "ПСИХИКА",
    "shooting": "СТРЕЛЬБА",
    "charge": "АТАКА",
    "fight": "БОЙ",
    "morale": "МОРАЛЬ",
}

SIDE_TRANSLATIONS = {
    "enemy": "ИГРОК",
    "model": "МОДЕЛЬ",
}


@dataclass(frozen=True)
class UnitStatus:
    unit_id: int
    side: str
    hp: Optional[int]
    name: Optional[str]


@dataclass(frozen=True)
class GameState:
    turn: Optional[str]
    battle_round: Optional[str]
    phase: Optional[str]
    active_side: Optional[str]
    player_vp: Optional[str]
    model_vp: Optional[str]
    player_cp: Optional[str]
    model_cp: Optional[str]
    player_units: List[UnitStatus]
    model_units: List[UnitStatus]


def _parse_value(value: str):
    try:
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value.strip()


def _load_status(path: Path) -> Dict[str, object]:
    data: Dict[str, object] = {}
    if not path.exists():
        return data
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            data[key.strip()] = _parse_value(value.strip())
    except OSError:
        return {}
    return data


def _parse_units_file(path: Path) -> Tuple[List[str], List[str]]:
    if not path.exists():
        return [], []
    player: List[str] = []
    model: List[str] = []
    current: Optional[List[str]] = None
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.lower().startswith("player units"):
                current = player
                continue
            if line.lower().startswith("model units"):
                current = model
                continue
            if current is not None:
                name, _, _ = _parse_unit_entry(line)
                if name:
                    current.append(name)
    except OSError:
        return [], []
    return player, model


def _parse_unit_entry(value: str) -> Tuple[str, int, str]:
    if not value:
        return "", 0, ""
    if "|" not in value:
        return value.strip(), 0, ""
    parts = [part.strip() for part in value.split("|")]
    if not parts:
        return "", 0, ""
    name = parts[0]
    count = 0
    instance_id = ""
    if len(parts) >= 2:
        try:
            count = int(parts[1])
        except ValueError:
            count = 0
    if len(parts) >= 3:
        instance_id = parts[2]
    return name, count, instance_id


def _parse_roster_from_journal(lines: Iterable[str]) -> Tuple[List[str], List[str]]:
    player_names: Dict[int, str] = {}
    model_names: Dict[int, str] = {}
    pattern = re.compile(
        r"\[roster\]\s+(model|enemy)\[(\d+)\]\s+name=(.+?)\s+instance_id=[^\s]+\s+models=\d+",
        re.IGNORECASE,
    )
    for line in lines:
        match = pattern.search(line)
        if not match:
            continue
        side, index_str, name = match.groups()
        try:
            index = int(index_str)
        except ValueError:
            continue
        if side.lower() == "enemy":
            player_names[index] = name.strip()
        else:
            model_names[index] = name.strip()

    def _as_list(names: Dict[int, str]) -> List[str]:
        if not names:
            return []
        max_index = max(names)
        return [names.get(i, "") for i in range(max_index + 1)]

    return _as_list(player_names), _as_list(model_names)


def parse_state(
    status_path: str | Path = "status.txt",
    units_path: str | Path = "units.txt",
    journal_lines: Optional[Iterable[str]] = None,
) -> GameState:
    status = _load_status(Path(status_path))
    player_names, model_names = _parse_units_file(Path(units_path))
    if journal_lines is not None:
        journal_player, journal_model = _parse_roster_from_journal(journal_lines)
        if journal_player:
            player_names = journal_player
        if journal_model:
            model_names = journal_model

    def _list(value) -> List:
        if isinstance(value, list):
            return value
        return []

    player_health = _list(status.get("player_health"))
    model_health = _list(status.get("model_health"))

    player_units: List[UnitStatus] = []
    for idx, hp in enumerate(player_health):
        unit_id = 11 + idx
        name = player_names[idx] if idx < len(player_names) else None
        player_units.append(UnitStatus(unit_id=unit_id, side="enemy", hp=_safe_int(hp), name=name))

    model_units: List[UnitStatus] = []
    for idx, hp in enumerate(model_health):
        unit_id = 21 + idx
        name = model_names[idx] if idx < len(model_names) else None
        model_units.append(UnitStatus(unit_id=unit_id, side="model", hp=_safe_int(hp), name=name))

    return GameState(
        turn=_stringify(status.get("turn")),
        battle_round=_stringify(status.get("battle_round")),
        phase=_translate_phase(status.get("phase")),
        active_side=_translate_side(status.get("active_side")),
        player_vp=_stringify(status.get("player_vp")),
        model_vp=_stringify(status.get("model_vp")),
        player_cp=_stringify(status.get("player_cp")),
        model_cp=_stringify(status.get("model_cp")),
        player_units=player_units,
        model_units=model_units,
    )


def _translate_phase(value: object) -> Optional[str]:
    if value is None:
        return None
    key = str(value).strip().lower()
    if not key:
        return None
    return PHASE_TRANSLATIONS.get(key, str(value).upper())


def _translate_side(value: object) -> Optional[str]:
    if value is None:
        return None
    key = str(value).strip().lower()
    if not key:
        return None
    return SIDE_TRANSLATIONS.get(key, str(value).upper())


def _stringify(value: object) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None


def _safe_int(value: object) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
