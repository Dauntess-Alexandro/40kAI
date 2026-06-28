from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

__all__ = ["OpponentStatsStore"]


def _result_value(*, win: bool, draw: bool) -> float:
    if win:
        return 1.0
    if draw:
        return 0.5
    return 0.0


class OpponentStatsStore:
    """Персист per-opponent EMA-winrate ЛЕРНЕРА против каждого оппонента.

    Хранилище: JSON {opponents: {agent_id: {games, ema_winrate, draws, vp_sum, updated_at}}}.
    path == ":memory:" => без диска (для тестов/in-process).
    """

    def __init__(self, path: str, *, ema_alpha: float = 0.15) -> None:
        self._path = str(path)
        self._alpha = float(ema_alpha)
        self._data: dict[str, dict[str, Any]] = {}

    def update(self, *, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None:
        aid = str(agent_id or "").strip()
        if not aid:
            return
        rec = self._data.get(aid)
        result = _result_value(win=win, draw=draw)
        if rec is None:
            rec = {"games": 0, "ema_winrate": 0.5, "draws": 0, "vp_sum": 0.0, "updated_at": ""}
            self._data[aid] = rec
        rec["ema_winrate"] = (1.0 - self._alpha) * float(rec["ema_winrate"]) + self._alpha * result
        rec["games"] = int(rec["games"]) + 1
        rec["draws"] = int(rec["draws"]) + (1 if draw else 0)
        rec["vp_sum"] = float(rec["vp_sum"]) + float(vp_diff)
        rec["updated_at"] = datetime.now().isoformat(timespec="seconds")

    def winrate(self, agent_id: str) -> float:
        rec = self._data.get(str(agent_id or "").strip())
        return 0.5 if rec is None else float(rec["ema_winrate"])

    def games(self, agent_id: str) -> int:
        rec = self._data.get(str(agent_id or "").strip())
        return 0 if rec is None else int(rec["games"])

    def record(self, agent_id: str) -> dict[str, Any]:
        rec = self._data.get(str(agent_id or "").strip())
        return dict(rec) if rec else {"games": 0, "ema_winrate": 0.5, "draws": 0, "vp_sum": 0.0, "updated_at": ""}

    def all_records(self) -> dict[str, dict[str, Any]]:
        return {k: dict(v) for k, v in self._data.items()}

    def save(self) -> None:
        if self._path == ":memory:":
            return
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"opponents": self._data}, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, self._path)  # атомарная запись (SMB-safe, ср. state_export.py)

    @classmethod
    def load(cls, path: str, *, ema_alpha: float = 0.15) -> "OpponentStatsStore":
        store = cls(path, ema_alpha=ema_alpha)
        if path != ":memory:" and os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as handle:
                    payload = json.load(handle)
                opp = payload.get("opponents", {}) if isinstance(payload, dict) else {}
                if isinstance(opp, dict):
                    store._data = {str(k): dict(v) for k, v in opp.items() if isinstance(v, dict)}
            except (OSError, json.JSONDecodeError):
                store._data = {}
        return store
