from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from gym_mod.engine.agent_registry import compatible_contracts, list_agents


MATCHUPS_PATH = os.path.join("models", "matchups.json")


@dataclass
class OpponentPick:
    mode: str
    source: str
    agent_id: str
    reason: str


def _load_json(path: str, fallback: Any) -> Any:
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return fallback


def _write_json(path: str, payload: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _entry_contract(entry: dict[str, Any]) -> dict[str, Any]:
    path = entry.get("contract_path")
    contract = _load_json(path, {})
    return contract if isinstance(contract, dict) else {}


def choose_opponent(
    *,
    learner_side: str,
    learner_faction: str,
    learner_contract: dict[str, Any],
    mode: str = "mirror",
    rng: Optional[random.Random] = None,
) -> Optional[OpponentPick]:
    pool = list_agents()
    if not pool:
        return None
    rng = rng or random.Random()
    mode_norm = str(mode or "mirror").strip().lower()
    side_norm = str(learner_side or "P1").upper()
    wanted_side = "P2" if side_norm == "P1" else "P1"
    faction_norm = str(learner_faction or "").strip().lower()

    candidates = []
    for entry in pool:
        entry_side = str(entry.get("side", "")).upper()
        entry_faction = str(entry.get("faction", "")).strip().lower()
        if entry_side != wanted_side:
            continue
        contract = _entry_contract(entry)
        ok, reason = compatible_contracts(learner_contract, contract)
        if not ok:
            continue
        candidates.append((entry, contract, reason))
    if not candidates:
        return None

    if mode_norm == "mirror":
        subset = [it for it in candidates if str(it[0].get("faction", "")).strip().lower() == faction_norm]
        chosen = rng.choice(subset or candidates)
        return OpponentPick(mode=mode_norm, source="registry", agent_id=str(chosen[0]["agent_id"]), reason="mirror")

    if mode_norm == "cross_faction":
        subset = [it for it in candidates if str(it[0].get("faction", "")).strip().lower() != faction_norm]
        chosen = rng.choice(subset or candidates)
        return OpponentPick(mode=mode_norm, source="registry", agent_id=str(chosen[0]["agent_id"]), reason="cross_faction")

    # league: blend latest + random_old + best from matchup scores
    scored = _score_candidates(candidates, learner_side=side_norm, learner_faction=faction_norm)
    scored.sort(key=lambda x: x[1], reverse=True)
    if not scored:
        return None

    latest_prob = float(os.getenv("LEAGUE_PICK_LATEST_PROB", "0.40") or "0.40")
    random_old_prob = float(os.getenv("LEAGUE_PICK_RANDOM_OLD_PROB", "0.30") or "0.30")
    roll = rng.random()
    if roll < latest_prob:
        chosen = scored[0][0]
        return OpponentPick(mode=mode_norm, source="league_latest", agent_id=str(chosen["agent_id"]), reason="latest")
    if roll < latest_prob + random_old_prob and len(scored) > 1:
        chosen = rng.choice([item[0] for item in scored[1:]])
        return OpponentPick(mode=mode_norm, source="league_random_old", agent_id=str(chosen["agent_id"]), reason="random_old")
    chosen = scored[0][0]
    return OpponentPick(mode=mode_norm, source="league_best", agent_id=str(chosen["agent_id"]), reason="best_score")


def _score_candidates(candidates: list[tuple[dict[str, Any], dict[str, Any], str]], *, learner_side: str, learner_faction: str) -> list[tuple[dict[str, Any], float]]:
    data = _load_json(MATCHUPS_PATH, {"records": []})
    records = data.get("records", []) if isinstance(data, dict) else []
    by_agent: dict[str, float] = {}
    for rec in records:
        if not isinstance(rec, dict):
            continue
        opp = str(rec.get("opponent_agent_id", ""))
        if not opp:
            continue
        vp = float(rec.get("vp_diff", 0.0))
        wins = float(rec.get("win", 0.0))
        draws = float(rec.get("draw", 0.0))
        by_agent.setdefault(opp, 0.0)
        by_agent[opp] += (wins * 1.0) + (draws * 0.2) + (vp * 0.05)

    scored = []
    for entry, _contract, _reason in candidates:
        aid = str(entry.get("agent_id", ""))
        score = float(by_agent.get(aid, 0.0))
        scored.append((entry, score))
    return scored


def record_matchup(
    *,
    learner_agent_id: str,
    opponent_agent_id: str,
    win: bool,
    draw: bool,
    vp_diff: float,
    reason: str,
) -> None:
    payload = _load_json(MATCHUPS_PATH, {"records": []})
    if not isinstance(payload, dict):
        payload = {"records": []}
    records = payload.get("records")
    if not isinstance(records, list):
        records = []
    records.append(
        {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "learner_agent_id": learner_agent_id,
            "opponent_agent_id": opponent_agent_id,
            "win": 1 if win else 0,
            "draw": 1 if draw else 0,
            "vp_diff": float(vp_diff),
            "reason": str(reason or "unknown"),
        }
    )
    # Keep file bounded.
    records = records[-20000:]
    payload["records"] = records
    _write_json(MATCHUPS_PATH, payload)

