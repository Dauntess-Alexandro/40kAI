from __future__ import annotations

import os
import random
import re
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from core.engine.opponent_pool import OpponentChoice, OpponentPool, OpponentStatsStore, PoolConfig

__all__ = [
    "OpponentRuntimeCache",
    "algo_short_label",
    "default_candidate_provider",
    "build_pool_for_actor",
    "build_pool_ui_state",
    "choose_opponent_policy_fn",
    "parse_last_pool_pick",
    "parse_pool_log_tail",
    "short_agent_label",
]

_EP_LABEL_RE = re.compile(r"_ep(\d+)(?:_|$)", re.IGNORECASE)
_POOL_PICK_RE = re.compile(
    r"kind=(?P<kind>\w+)\s+agent=(?P<agent>\S+)\s+reason=(?P<reason>\S+)\s+weight=(?P<weight>[\d.]+)"
)
_ALGO_SHORT = {
    "ppo": "PPO",
    "dqn": "DQN",
    "alphazero_tree": "AZ",
    "alphazero_proxy": "AZp",
    "gumbel_az": "GAZ",
    "gumbel_muzero": "GMZ",
    "sampled_muzero": "SMZ",
}


def algo_short_label(algo: str) -> str:
    key = str(algo or "").strip().lower()
    if key == "alphazero":
        key = "alphazero_tree"
    if key in _ALGO_SHORT:
        return _ALGO_SHORT[key]
    if not key or key == "unknown":
        return "?"
    return key.upper()[:4]


def parse_last_pool_pick(log_path: str) -> dict[str, Any]:
    """Последний сэмпл [POOL] kind=snapshot/heuristic из train-лога."""
    path = str(log_path or "").strip()
    if not path or not os.path.exists(path):
        return {}
    last_line = ""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if "[POOL]" in line and "kind=" in line and "[POOL][RESULT]" not in line:
                    last_line = line.strip()
    except OSError:
        return {}
    if not last_line:
        return {}
    match = _POOL_PICK_RE.search(last_line)
    if not match:
        return {}
    kind = str(match.group("kind") or "")
    agent = str(match.group("agent") or "")
    if agent in {"", "-"}:
        agent = ""
    return {
        "kind": kind,
        "agent_id": agent,
        "label": short_agent_label(agent) if agent else "эвристика",
        "reason": str(match.group("reason") or ""),
        "weight": float(match.group("weight") or 0.0),
    }


def _registry_meta_index() -> dict[str, dict[str, str]]:
    from core.engine.agent_registry import collect_registered_agents_meta

    out: dict[str, dict[str, str]] = {}
    for rec in collect_registered_agents_meta():
        aid = str(rec.get("agent_id", "") or "")
        if aid:
            out[aid] = rec
    return out


def _enrich_agent_meta(agent_id: str, meta_index: dict[str, dict[str, str]], *, in_pool: bool = False) -> dict[str, Any]:
    aid = str(agent_id or "").strip()
    rec = meta_index.get(aid, {})
    algo = str(rec.get("algo", "") or "")
    ep_match = _EP_LABEL_RE.search(aid)
    ep = int(ep_match.group(1)) if ep_match else -1
    created = str(rec.get("created_at", "") or "")
    if created:
        created = created[:16].replace("T", " ")
    return {
        "algo": algo,
        "algo_short": algo_short_label(algo),
        "ep": ep,
        "created_at": created,
        "faction": str(rec.get("faction", "") or ""),
        "in_pool": bool(in_pool),
    }


def _pool_algo_mix(candidates: list[dict[str, Any]]) -> str:
    counts: dict[str, int] = {}
    for row in candidates:
        label = str(row.get("algo_short", "") or "?")
        counts[label] = counts.get(label, 0) + 1
    if not counts:
        return ""
    parts = [f"{name}×{count}" for name, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))]
    return ", ".join(parts)


def short_agent_label(agent_id: str) -> str:
    """Краткая подпись снапшота для UI: «P1 Necrons ep950»."""
    aid = str(agent_id or "").strip()
    if not aid:
        return "—"
    parts = aid.split("_")
    side = parts[0] if parts else "?"
    faction = parts[1] if len(parts) > 1 else ""
    ep_match = _EP_LABEL_RE.search(aid)
    if ep_match:
        ep = ep_match.group(1)
        return f"{side} {faction} ep{ep}".strip()
    if re.search(r"(^|_)final($|_)", aid, re.IGNORECASE):
        return f"{side} {faction} final".strip()
    return aid if len(aid) <= 40 else aid[:37] + "..."


def parse_pool_log_tail(log_path: str, *, max_lines: int = 20) -> list[dict[str, str]]:
    """Последние строки [POOL] из train-лога для вкладки «Train live»."""
    path = str(log_path or "").strip()
    if not path or not os.path.exists(path):
        return []
    matched: list[str] = []
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if "[POOL]" in line:
                    matched.append(line.rstrip("\n\r"))
    except OSError:
        return []
    tail = matched[-max(1, int(max_lines)) :]
    rows: list[dict[str, str]] = []
    for line in tail:
        kind = "warn" if "[POOL][WARN]" in line else ("result" if "[POOL][RESULT]" in line else "info")
        rows.append({"text": line.strip(), "kind": kind})
    return rows


def _resolve_learner_contract_for_ui(*, learner_side: str) -> dict:
    from core.engine.agent_registry import _load_json, _resolve_agent_artifact_path, list_agents

    side = str(learner_side or "P1").strip().upper() or "P1"
    for probe_side in (side, "P2" if side == "P1" else "P1"):
        for entry in list_agents(side=probe_side):
            artifact_dir = str(entry.get("artifact_dir", "") or "")
            contract_path = _resolve_agent_artifact_path(
                entry.get("contract_path"), artifact_dir, "env_contract.json"
            )
            contract = _load_json(str(contract_path), {})
            if isinstance(contract, dict) and contract:
                return contract
    return {}


def _count_registry_side(side: str) -> int:
    from core.engine.agent_registry import list_agents

    return len(list_agents(side=str(side or "").strip().upper()))


def build_pool_ui_state(
    *,
    learner_side: str,
    learner_faction: str,
    config: PoolConfig,
    stats_path: str,
    mission_name: str = "",
    draw_rate: float | None = None,
    pool_enabled: bool = True,
    train_running: bool = False,
    learner_algo: str = "",
    train_log_path: str = "",
) -> dict[str, Any]:
    """Снимок пула для GUI: кандидаты (PFSP), история stats, контекст learner."""
    from core.engine.agent_registry import AgentIdentity

    learner_side = str(learner_side or "P1").strip().upper() or "P1"
    opp_side = "P2" if learner_side == "P1" else "P1"
    learner_faction = str(learner_faction or "Necrons").strip() or "Necrons"
    contract = _resolve_learner_contract_for_ui(learner_side=learner_side)

    preview_cfg = PoolConfig(
        enabled=True,
        p_heuristic=float(config.p_heuristic),
        pool_size=max(1, int(config.pool_size)),
        strategy=str(config.strategy or "pfsp"),
        pfsp_power=float(config.pfsp_power),
        uniform_floor=float(config.uniform_floor),
        novelty_bonus=float(config.novelty_bonus),
        min_games_for_pfsp=max(0, int(config.min_games_for_pfsp)),
        ema_alpha=float(config.ema_alpha),
        seed=config.seed,
    )

    stats = OpponentStatsStore.load(str(stats_path), ema_alpha=preview_cfg.ema_alpha)
    identity = AgentIdentity(side=learner_side, faction=learner_faction).normalized()
    pool = OpponentPool(
        learner_identity=identity,
        learner_contract=contract,
        config=preview_cfg,
        stats=stats,
        rng=random.Random(0),
        candidate_provider=default_candidate_provider,
    )
    ids = pool.refresh_candidates()
    ui = pool.state_for_ui()
    active_ids = set(ids)
    meta_index = _registry_meta_index()

    candidates: list[dict[str, Any]] = []
    for row in ui.get("candidates", []):
        if not isinstance(row, dict):
            continue
        aid = str(row.get("agent_id", "") or "")
        rec = stats.record(aid)
        games = int(rec.get("games", 0) or 0)
        draws = int(rec.get("draws", 0) or 0)
        vp_sum = float(rec.get("vp_sum", 0.0) or 0.0)
        meta = _enrich_agent_meta(aid, meta_index, in_pool=True)
        candidates.append({
            "agent_id": aid,
            "label": short_agent_label(aid),
            "games": games,
            "winrate": float(row.get("winrate", 0.5) or 0.5),
            "draw_pct": (draws / games) if games > 0 else -1.0,
            "vp_per_game": (vp_sum / games) if games > 0 else 0.0,
            "prob": float(row.get("prob", 0.0) or 0.0),
            "reason": str(row.get("reason", "") or ""),
            **meta,
        })

    history: list[dict[str, Any]] = []
    for aid, rec in stats.all_records().items():
        games = int(rec.get("games", 0) or 0)
        draws = int(rec.get("draws", 0) or 0)
        vp_sum = float(rec.get("vp_sum", 0.0) or 0.0)
        meta = _enrich_agent_meta(str(aid), meta_index, in_pool=str(aid) in active_ids)
        history.append({
            "agent_id": str(aid),
            "label": short_agent_label(str(aid)),
            "games": games,
            "winrate": float(rec.get("ema_winrate", 0.5) or 0.5),
            "draw_pct": (draws / games) if games > 0 else -1.0,
            "vp_per_game": (vp_sum / games) if games > 0 else 0.0,
            **meta,
        })
    history.sort(key=lambda item: int(item.get("games", 0) or 0), reverse=True)

    candidate_count = len(ids)
    last_pick = parse_last_pool_pick(train_log_path) if train_log_path else {}
    context: dict[str, Any] = {
        "learner_side": learner_side,
        "learner_faction": learner_faction,
        "learner_algo": str(learner_algo or ""),
        "opponent_side": opp_side,
        "pool_fill": f"{candidate_count}/{preview_cfg.pool_size}",
        "candidate_count": candidate_count,
        "pool_size": int(preview_cfg.pool_size),
        "registry_opponent_count": _count_registry_side(opp_side),
        "pool_algo_mix": _pool_algo_mix(candidates),
        "mission": str(mission_name or ""),
        "draw_rate": float(draw_rate) if draw_rate is not None else -1.0,
        "pool_enabled": bool(pool_enabled),
        "train_running": bool(train_running),
        "strategy": str(preview_cfg.strategy),
        "p_heuristic": float(preview_cfg.p_heuristic),
        "has_contract": bool(contract),
        "last_pick_label": str(last_pick.get("label", "") or ""),
        "last_pick_kind": str(last_pick.get("kind", "") or ""),
        "last_pick_reason": str(last_pick.get("reason", "") or ""),
        "last_pick_weight": float(last_pick.get("weight", 0.0) or 0.0),
    }

    return {
        "context": context,
        "candidates": candidates,
        "history": history,
        "heuristic": {"prob": float(preview_cfg.p_heuristic), "label": "эвристика"},
        "train_live": [],
    }


class OpponentRuntimeCache:
    """LRU-кэш agent_id -> потребляемый объект (policy_fn/net). build_fn зовётся один раз на id."""

    def __init__(self, build_fn: Callable[[str], Any], maxsize: int) -> None:
        self._build = build_fn
        self._max = max(1, int(maxsize))
        self._store: OrderedDict[str, Any] = OrderedDict()

    def get(self, agent_id: str) -> Any:
        aid = str(agent_id)
        if aid in self._store:
            self._store.move_to_end(aid)
            return self._store[aid]
        obj = self._build(aid)
        self._store[aid] = obj
        self._store.move_to_end(aid)
        while len(self._store) > self._max:
            self._store.popitem(last=False)
        return obj


def default_candidate_provider() -> list[dict]:
    """Кандидаты из реестра: agent_id/side/contract/created_at (для OpponentPool.refresh_candidates)."""
    from core.engine.agent_registry import collect_registered_agents_meta, list_agents

    contracts: dict[str, dict] = {}
    for entry in list_agents():
        aid = str(entry.get("agent_id", "") or "")
        cpath = entry.get("contract_path")
        if aid and cpath:
            from core.engine.agent_registry import _load_json  # type: ignore[attr-defined]

            c = _load_json(str(cpath), {})
            contracts[aid] = c if isinstance(c, dict) else {}
    rows: list[dict] = []
    for rec in collect_registered_agents_meta():
        aid = str(rec.get("agent_id", "") or "")
        rows.append({
            "agent_id": aid,
            "side": str(rec.get("side", "")).upper(),
            "created_at": str(rec.get("created_at", "")),
            "contract": contracts.get(aid, {}),
        })
    return rows


def build_pool_for_actor(*, learner_identity, learner_contract, config: PoolConfig,
                         stats_path: str, seed: int | None, log_fn=None) -> OpponentPool | None:
    if not config.enabled:
        return None
    stats = OpponentStatsStore.load(stats_path, ema_alpha=config.ema_alpha)
    pool = OpponentPool(
        learner_identity=learner_identity, learner_contract=learner_contract or {},
        config=config, stats=stats, rng=random.Random(seed),
        candidate_provider=default_candidate_provider, log_fn=log_fn,
    )
    pool.refresh_candidates()
    return pool


def choose_opponent_policy_fn(pool, cache, *, log_fn=None, actor_label=""):
    """Сэмплит оппонента из пула и строит policy_fn через кэш.

    При сбое построения (битый/несовместимый снапшот) — fallback на эвристику
    (policy_fn=None) + [POOL][WARN], и кандидат выкидывается из пула, чтобы сбой
    не повторялся каждый эпизод. Возвращает (choice, policy_fn); policy_fn=None => эвристика.
    """
    choice = pool.sample()
    if choice.kind == "heuristic":
        if log_fn:
            log_fn(
                f"[POOL] {actor_label} kind=heuristic agent=- "
                f"reason={choice.reason} weight={choice.weight:.3f}"
            )
        return choice, None
    try:
        policy_fn = cache.get(choice.agent_id)
    except Exception as exc:
        if log_fn:
            log_fn(
                f"[POOL][WARN] {actor_label} build opponent agent={choice.agent_id} "
                f"failed: {exc}; fallback heuristic"
            )
        pool.drop_candidate(choice.agent_id)
        return OpponentChoice("heuristic", "", "heuristic_fallback", 0.0), None
    if log_fn:
        log_fn(
            f"[POOL] {actor_label} kind=snapshot agent={choice.agent_id} "
            f"reason={choice.reason} weight={choice.weight:.3f}"
        )
    return choice, policy_fn
