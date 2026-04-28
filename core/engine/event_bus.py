from __future__ import annotations

import json
import os
import sys
import threading
import time
from typing import Callable, Dict, List, Optional


Event = Dict[str, object]


class EventBus:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._subscribers: List[Callable[[Event], None]] = []

    def subscribe(self, callback: Callable[[Event], None]) -> None:
        with self._lock:
            self._subscribers.append(callback)

    def emit(self, event: Event) -> None:
        if "ts" not in event:
            event["ts"] = time.time()
        subscribers = []
        with self._lock:
            subscribers = list(self._subscribers)
        if os.getenv("EVT_DEBUG", "0") == "1":
            sys.stderr.write(f"[EVT_DEBUG] emit: {event}\n")
        for callback in subscribers:
            try:
                callback(event)
            except Exception:
                continue
        if os.getenv("EVT_STDOUT", "0") == "1":
            try:
                sys.stdout.write("__EVT__ " + json.dumps(event, ensure_ascii=False) + "\n")
                sys.stdout.flush()
            except Exception:
                pass


class EventRecorder:
    def __init__(self, max_events: int = 5000) -> None:
        self._lock = threading.Lock()
        self._events: List[Event] = []
        self._max_events = max(100, max_events)

    def record(self, event: Event) -> None:
        with self._lock:
            self._events.append(dict(event))
            if len(self._events) > self._max_events:
                self._events = self._events[-self._max_events :]

    def clear(self) -> None:
        with self._lock:
            self._events = []

    def snapshot(self, limit: Optional[int] = None) -> List[Event]:
        with self._lock:
            if limit is None:
                return list(self._events)
            return list(self._events[-limit:])


_EVENT_BUS = EventBus()
_EVENT_RECORDER = EventRecorder()
_EVENT_BUS.subscribe(_EVENT_RECORDER.record)


def get_event_bus() -> EventBus:
    return _EVENT_BUS


def get_event_recorder() -> EventRecorder:
    return _EVENT_RECORDER
