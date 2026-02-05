from __future__ import annotations

import json
import os
import threading
import time
from typing import Dict, Optional


class EventStream:
    def __init__(self, run_dir: str, enabled: bool) -> None:
        self.run_dir = os.path.abspath(run_dir)
        self.enabled = bool(enabled)
        self.event_id = 0
        self.last_event_id: Optional[int] = None
        self.last_context: Dict[str, object] = {
            "battle_round": None,
            "turn": None,
            "phase": None,
            "active_side": None,
        }
        self._handle = None
        self._lock = threading.Lock()

    def reset(self) -> None:
        self.event_id = 0
        self.last_event_id = None
        self.last_context = {
            "battle_round": None,
            "turn": None,
            "phase": None,
            "active_side": None,
        }

    def update_context(
        self,
        battle_round: Optional[int] = None,
        turn: Optional[int] = None,
        phase: Optional[str] = None,
        active_side: Optional[str] = None,
    ) -> None:
        if battle_round is not None:
            self.last_context["battle_round"] = battle_round
        if turn is not None:
            self.last_context["turn"] = turn
        if phase is not None:
            self.last_context["phase"] = phase
        if active_side is not None:
            self.last_context["active_side"] = self.normalize_active_side(active_side)

    def emit(self, event_type: str, **payload) -> None:
        if not self.enabled:
            return
        with self._lock:
            try:
                if self._handle is None:
                    os.makedirs(self.run_dir, exist_ok=True)
                    path = os.path.join(self.run_dir, "events.jsonl")
                    self._handle = open(path, "a", encoding="utf-8", buffering=1)
                self.event_id += 1
                record = dict(payload)
                record["type"] = event_type
                record["event_id"] = self.event_id
                record["ts"] = time.time()
                if "battle_round" not in record:
                    record["battle_round"] = self.last_context.get("battle_round")
                if "turn" not in record:
                    record["turn"] = self.last_context.get("turn")
                if "phase" not in record:
                    record["phase"] = self.last_context.get("phase")
                if "active_side" not in record:
                    record["active_side"] = self.last_context.get("active_side")
                if record.get("active_side") is not None:
                    record["active_side"] = self.normalize_active_side(record["active_side"])

                self.last_event_id = self.event_id
                self.update_context(
                    battle_round=record.get("battle_round"),
                    turn=record.get("turn"),
                    phase=record.get("phase"),
                    active_side=record.get("active_side"),
                )

                line = json.dumps(record, ensure_ascii=False)
                self._handle.write(line + "\n")
                self._handle.flush()
            except Exception:
                return

    @staticmethod
    def normalize_active_side(value: str) -> str:
        if value == "enemy":
            return "model"
        return value
