from __future__ import annotations

from contextlib import contextmanager
import json
import os
import threading
import time
from typing import Iterator


class IOProfiler:
    """Лёгкий агрегатор таймингов I/O по категориям."""

    def __init__(self) -> None:
        self._enabled = os.getenv("IO_PROFILE_ENABLED", "1") == "1"
        self._lock = threading.Lock()
        self._stats: dict[str, dict[str, float]] = {}

    @property
    def enabled(self) -> bool:
        return self._enabled

    def record(self, category: str, elapsed_s: float) -> None:
        if not self._enabled:
            return
        if elapsed_s < 0:
            elapsed_s = 0.0
        with self._lock:
            slot = self._stats.setdefault(category, {"count": 0.0, "total_s": 0.0, "max_s": 0.0})
            slot["count"] += 1
            slot["total_s"] += float(elapsed_s)
            slot["max_s"] = max(slot["max_s"], float(elapsed_s))

    @contextmanager
    def timed(self, category: str) -> Iterator[None]:
        started = time.perf_counter()
        try:
            yield
        finally:
            self.record(category, time.perf_counter() - started)

    def snapshot(self) -> dict[str, dict[str, float]]:
        with self._lock:
            result = {}
            for key, value in self._stats.items():
                count = int(value.get("count", 0.0))
                total_s = float(value.get("total_s", 0.0))
                max_s = float(value.get("max_s", 0.0))
                avg_s = (total_s / count) if count > 0 else 0.0
                result[key] = {
                    "count": count,
                    "total_ms": round(total_s * 1000.0, 3),
                    "avg_ms": round(avg_s * 1000.0, 3),
                    "max_ms": round(max_s * 1000.0, 3),
                }
            return result

    def write_snapshot(self, path: str | None = None) -> None:
        if not self._enabled:
            return
        profile_path = path or os.getenv("IO_PROFILE_PATH", os.path.join(os.getcwd(), "metrics", "io_profile.json"))
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        payload = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "categories": self.snapshot(),
        }
        with open(profile_path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)


_IO_PROFILER = IOProfiler()


def get_io_profiler() -> IOProfiler:
    return _IO_PROFILER
