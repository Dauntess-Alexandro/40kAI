from __future__ import annotations

import json
import os
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

__all__ = ["OpponentStatsStore", "PoolConfig", "resolve_pool_config"]


@dataclass(frozen=True)
class PoolConfig:
    enabled: bool = False
    p_heuristic: float = 0.30
    pool_size: int = 8
    strategy: str = "pfsp"          # "pfsp" | "uniform"
    pfsp_power: float = 2.0
    uniform_floor: float = 0.10
    novelty_bonus: float = 0.25
    min_games_for_pfsp: int = 3
    ema_alpha: float = 0.15
    seed: int | None = None


def _as_bool(v: Any, default: bool) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def _as_float(v: Any, default: float) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _as_int(v: Any, default: int) -> int:
    try:
        return int(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def resolve_pool_config(*, section: dict | None, getenv: Callable[[str], str | None] = os.getenv) -> PoolConfig:
    """Резолв конфига пула: env OPPONENT_POOL_* → секция hyperparams.opponent_pool → default."""
    s = section if isinstance(section, dict) else {}
    d = PoolConfig()

    def pick(env_key: str, sect_key: str):
        ev = getenv(env_key)
        if ev is not None:
            return ev
        return s.get(sect_key)

    strategy = str(pick("OPPONENT_POOL_STRATEGY", "strategy") or d.strategy).strip().lower()
    if strategy not in {"pfsp", "uniform"}:
        strategy = d.strategy

    pool_size = max(1, _as_int(pick("OPPONENT_POOL_SIZE", "pool_size"), d.pool_size))
    seed_raw = pick("OPPONENT_POOL_SEED", "seed")
    return PoolConfig(
        enabled=_as_bool(pick("OPPONENT_POOL_ENABLED", "enabled"), d.enabled),
        p_heuristic=_clamp01(_as_float(pick("OPPONENT_POOL_P_HEURISTIC", "p_heuristic"), d.p_heuristic)),
        pool_size=pool_size,
        strategy=strategy,
        pfsp_power=max(0.0, _as_float(pick("OPPONENT_POOL_PFSP_POWER", "pfsp_power"), d.pfsp_power)),
        uniform_floor=_clamp01(_as_float(pick("OPPONENT_POOL_UNIFORM_FLOOR", "uniform_floor"), d.uniform_floor)),
        novelty_bonus=max(0.0, _as_float(pick("OPPONENT_POOL_NOVELTY_BONUS", "novelty_bonus"), d.novelty_bonus)),
        min_games_for_pfsp=max(0, _as_int(pick("OPPONENT_POOL_MIN_GAMES", "min_games_for_pfsp"), d.min_games_for_pfsp)),
        ema_alpha=_clamp01(_as_float(pick("OPPONENT_POOL_EMA_ALPHA", "ema_alpha"), d.ema_alpha)) or d.ema_alpha,
        seed=_as_int(seed_raw, 0) if seed_raw is not None else None,
    )


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
