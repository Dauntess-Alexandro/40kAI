from __future__ import annotations

import json
import os
import random
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from core.engine.agent_registry import compatible_contracts

__all__ = ["OpponentChoice", "OpponentPool", "OpponentStatsStore", "PoolConfig", "resolve_pool_config"]


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
            rec = {
                "games": 0,
                "ema_winrate": 0.5,
                "draws": 0,
                "vp_sum": 0.0,
                "updated_at": "",
                "wins": 0,
                "losses": 0,
                "tracked_draws": 0,
                "unclassified_games": 0,
            }
            self._data[aid] = rec
        rec["ema_winrate"] = (1.0 - self._alpha) * float(rec["ema_winrate"]) + self._alpha * result
        rec["games"] = int(rec["games"]) + 1
        rec["draws"] = int(rec["draws"]) + (1 if draw else 0)
        rec["wins"] = int(rec.get("wins", 0) or 0) + (1 if win else 0)
        rec["losses"] = int(rec.get("losses", 0) or 0) + (1 if not win and not draw else 0)
        rec["tracked_draws"] = int(rec.get("tracked_draws", 0) or 0) + (1 if draw else 0)
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
        return dict(rec) if rec else {
            "games": 0,
            "ema_winrate": 0.5,
            "draws": 0,
            "vp_sum": 0.0,
            "updated_at": "",
            "wins": 0,
            "losses": 0,
            "tracked_draws": 0,
            "unclassified_games": 0,
        }

    def all_records(self) -> dict[str, dict[str, Any]]:
        return {k: dict(v) for k, v in self._data.items()}

    def save(self) -> None:
        if self._path == ":memory:":
            return
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"schema_version": 2, "opponents": self._data}, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, self._path)  # атомарная запись (SMB-safe, ср. state_export.py)

    @classmethod
    def load(cls, path: str, *, ema_alpha: float = 0.15) -> OpponentStatsStore:
        store = cls(path, ema_alpha=ema_alpha)
        if path != ":memory:" and os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as handle:
                    payload = json.load(handle)
                opp = payload.get("opponents", {}) if isinstance(payload, dict) else {}
                if isinstance(opp, dict):
                    for key, value in opp.items():
                        if not isinstance(value, dict):
                            continue
                        rec = dict(value)
                        games = max(0, int(rec.get("games", 0) or 0))
                        rec["games"] = games
                        rec["draws"] = max(0, int(rec.get("draws", 0) or 0))
                        rec["vp_sum"] = float(rec.get("vp_sum", 0.0) or 0.0)
                        ema_raw = rec.get("ema_winrate", 0.5)
                        rec["ema_winrate"] = float(ema_raw) if ema_raw is not None else 0.5
                        rec["updated_at"] = str(rec.get("updated_at", "") or "")
                        if not any(k in rec for k in ("wins", "losses", "tracked_draws", "unclassified_games")):
                            # Старый schema v1 не позволял восстановить W/L: были только games/draws/vp_sum.
                            # Не выдумываем результаты — помечаем старые игры как неклассифицированные.
                            rec["wins"] = 0
                            rec["losses"] = 0
                            rec["tracked_draws"] = 0
                            rec["unclassified_games"] = games
                        else:
                            rec["wins"] = max(0, int(rec.get("wins", 0) or 0))
                            rec["losses"] = max(0, int(rec.get("losses", 0) or 0))
                            rec["tracked_draws"] = max(0, int(rec.get("tracked_draws", 0) or 0))
                            rec["unclassified_games"] = max(0, int(rec.get("unclassified_games", 0) or 0))
                        store._data[str(key)] = rec
            except (OSError, json.JSONDecodeError):
                store._data = {}
        return store


@dataclass(frozen=True)
class OpponentChoice:
    kind: str          # "heuristic" | "snapshot"
    agent_id: str
    reason: str        # "heuristic_anchor" | "pfsp" | "uniform_floor" | "novelty"
    weight: float


class OpponentPool:
    def __init__(self, *, learner_identity, learner_contract, config: PoolConfig,
                 stats: OpponentStatsStore, rng: random.Random,
                 candidate_provider: Callable[[], list[dict]] | None = None, log_fn=None) -> None:
        self.learner_identity = learner_identity
        self.learner_contract = dict(learner_contract or {})
        self.config = config
        self.stats = stats
        self._rng = rng
        self._provider = candidate_provider
        self._log = log_fn
        self._candidates: list[str] = []
        self._refresh_diagnostics: dict[str, int | str] = {
            "registry_total": 0,
            "opponent_side": self._opponent_side(),
            "side_compatible": 0,
            "contract_compatible": 0,
            "selected": 0,
            "filtered_side": 0,
            "filtered_contract": 0,
            "filtered_duplicate": 0,
            "limited_out": 0,
        }

    def set_candidates(self, ids: list[str]) -> None:
        self._candidates = [str(a) for a in ids if str(a or "").strip()]

    def drop_candidate(self, agent_id: str) -> None:
        """Убрать кандидата из пула (напр. битый/несовместимый снапшот не смог построиться)."""
        aid = str(agent_id or "").strip()
        if aid:
            self._candidates = [c for c in self._candidates if c != aid]

    def _weights(self, ids: list[str]) -> tuple[list[float], list[str]]:
        cfg = self.config
        base: list[float] = []
        reasons: list[str] = []
        if cfg.strategy == "uniform":
            for _ in ids:
                base.append(1.0)
                reasons.append("uniform_floor")
        else:  # pfsp
            for aid in ids:
                if self.stats.games(aid) < cfg.min_games_for_pfsp:
                    base.append((1.0 - 0.5) ** cfg.pfsp_power + cfg.novelty_bonus)
                    reasons.append("novelty")
                else:
                    wr = self.stats.winrate(aid)
                    base.append((1.0 - wr) ** cfg.pfsp_power)
                    reasons.append("pfsp")
        n = len(ids)
        total = sum(base) or 1.0
        floor = cfg.uniform_floor
        probs = [(1.0 - floor) * (b / total) + floor * (1.0 / n) for b in base]
        return probs, reasons

    def sample(self) -> OpponentChoice:
        ids = list(self._candidates)
        if not ids:
            return OpponentChoice("heuristic", "", "heuristic_anchor", 1.0)
        if self._rng.random() < self.config.p_heuristic:
            return OpponentChoice("heuristic", "", "heuristic_anchor", self.config.p_heuristic)
        probs, reasons = self._weights(ids)
        r = self._rng.random()
        acc = 0.0
        idx = len(ids) - 1
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                idx = i
                break
        return OpponentChoice("snapshot", ids[idx], reasons[idx], probs[idx])

    def _opponent_side(self) -> str:
        side = ""
        if self.learner_identity is not None:
            side = str(getattr(self.learner_identity, "side", "") or "").upper()
        return "P1" if side == "P2" else "P2"

    def refresh_candidates(self) -> list[str]:
        if self._provider is None:
            return list(self._candidates)
        opp_side = self._opponent_side()
        rows = self._provider() or []
        # сортировка: новые первыми (по created_at, затем agent_id)
        rows = sorted(rows, key=lambda r: (str(r.get("created_at", "")), str(r.get("agent_id", ""))), reverse=True)
        out: list[str] = []
        seen: set[str] = set()
        filtered_side = 0
        filtered_contract = 0
        filtered_duplicate = 0
        side_compatible = 0
        contract_compatible = 0
        limited_out = 0
        for r in rows:
            aid = str(r.get("agent_id", "") or "").strip()
            if not aid:
                continue
            if aid in seen:
                filtered_duplicate += 1
                continue
            seen.add(aid)
            if str(r.get("side", "")).upper() != opp_side:
                filtered_side += 1
                continue
            side_compatible += 1
            ok, _reason = compatible_contracts(self.learner_contract, r.get("contract", {}) or {})
            if not ok:
                filtered_contract += 1
                continue
            contract_compatible += 1
            if len(out) < self.config.pool_size:
                out.append(aid)
            else:
                limited_out += 1
        self._refresh_diagnostics = {
            "registry_total": len(rows),
            "opponent_side": opp_side,
            "side_compatible": side_compatible,
            "contract_compatible": contract_compatible,
            "selected": len(out),
            "filtered_side": filtered_side,
            "filtered_contract": filtered_contract,
            "filtered_duplicate": filtered_duplicate,
            "limited_out": limited_out,
        }
        if self._log:
            self._log(
                f"[POOL][REFRESH] registry={len(rows)} side={opp_side} side_ok={side_compatible} "
                f"contract_ok={contract_compatible} selected={len(out)} filtered_side={filtered_side} "
                f"filtered_contract={filtered_contract} duplicate={filtered_duplicate} limited={limited_out}"
            )
        self._candidates = out
        return list(out)

    def refresh_diagnostics(self) -> dict[str, int | str]:
        return dict(self._refresh_diagnostics)

    def record_result(self, *, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None:
        if not str(agent_id or "").strip():
            return
        self.stats.update(agent_id=agent_id, win=win, draw=draw, vp_diff=vp_diff)

    def state_for_ui(self) -> dict:
        ids = list(self._candidates)
        probs, reasons = self._weights(ids) if ids else ([], [])
        rows = []
        for i, aid in enumerate(ids):
            rows.append({
                "agent_id": aid,
                "games": self.stats.games(aid),
                "winrate": round(self.stats.winrate(aid), 4),
                "prob": round(probs[i], 4) if probs else 0.0,
                "reason": reasons[i] if reasons else "",
            })
        return {
            "pool_size": len(ids),
            "strategy": self.config.strategy,
            "p_heuristic": self.config.p_heuristic,
            "candidates": rows,
            "refresh": self.refresh_diagnostics(),
        }
