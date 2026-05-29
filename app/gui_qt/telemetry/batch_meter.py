from __future__ import annotations

import re
from collections import deque
from typing import Optional

_BATCH_RE = re.compile(r"batch=(\d+)")


class BatchMeter:
    """Скользящее среднее размера батча inference-сервера из строк stdout."""

    def __init__(self, window: int = 30) -> None:
        self._vals: deque[int] = deque(maxlen=max(1, int(window)))

    def feed_line(self, line: str) -> None:
        m = _BATCH_RE.search(line or "")
        if m:
            self._vals.append(int(m.group(1)))

    def average(self) -> Optional[float]:
        if not self._vals:
            return None
        return sum(self._vals) / len(self._vals)

    def reset(self) -> None:
        self._vals.clear()
