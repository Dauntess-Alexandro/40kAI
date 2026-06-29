from __future__ import annotations

import json
import os
import random
import re
from collections import OrderedDict
from collections.abc import Callable
from datetime import datetime
from typing import Any

from core.engine.opponent_pool import OpponentChoice, OpponentPool, OpponentStatsStore, PoolConfig

__all__ = [
    "OpponentRuntimeCache",
    "OpponentPoolStatsWriter",
    "algo_short_label",
    "build_pool_result_payload",
    "default_candidate_provider",
    "build_pool_for_actor",
    "build_pool_ui_state",
    "choose_opponent_policy_fn",
    "parse_last_pool_pick",
    "parse_pool_log_tail",
    "short_agent_label",
]

POOL_RUN_HEURISTIC_KEY = "__heuristic__"

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
    created_raw = str(rec.get("created_at", "") or "")
    created = created_raw
    if created:
        created = created[:16].replace("T", " ")
    return {
        "algo": algo,
        "algo_short": algo_short_label(algo),
        "ep": ep,
        "created_at": created,
        "age": _age_label(created_raw),
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


def _atomic_write_json(path: str, payload: dict[str, Any]) -> None:
    target = str(path or "").strip()
    if not target or target == ":memory:":
        return
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    os.replace(tmp, target)


def _load_json_object(path: str) -> dict[str, Any]:
    target = str(path or "").strip()
    if not target or target == ":memory:" or not os.path.isfile(target):
        return {}
    try:
        with open(target, encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def build_pool_result_payload(
    *,
    pool: OpponentPool,
    choice: OpponentChoice,
    result: str,
    vp_diff: float,
    actor_idx: int,
    actor_ep: int,
    source: str = "local",
) -> dict[str, Any]:
    """Обновить только локальный sampler актора и собрать событие для единого writer learner-а."""
    result_norm = str(result or "").strip().lower()
    if result_norm not in {"win", "draw", "loss"}:
        result_norm = "draw"
    if choice.kind == "snapshot" and choice.agent_id:
        # Это локальный кэш PFSP конкретного актора. На диск он не пишет: авторитетный
        # aggregate обновляет только OpponentPoolStatsWriter в learner-процессе.
        pool.record_result(
            agent_id=choice.agent_id,
            win=(result_norm == "win"),
            draw=(result_norm == "draw"),
            vp_diff=float(vp_diff),
        )
    if choice.kind == "snapshot":
        prob_snapshot = max(0.0, float(choice.weight))
        prob_episode = (1.0 - float(pool.config.p_heuristic)) * prob_snapshot
    else:
        prob_snapshot = 0.0
        # При пустом пуле sample() возвращает weight=1.0; при fallback — 0.0.
        prob_episode = max(0.0, float(choice.weight))
    return {
        "actor_idx": int(actor_idx),
        "actor_ep": int(actor_ep),
        "source": str(source or "local"),
        "kind": str(choice.kind or "heuristic"),
        "agent_id": str(choice.agent_id or ""),
        "reason": str(choice.reason or ""),
        "prob_snapshot": float(prob_snapshot),
        "prob_episode": float(prob_episode),
        "result": result_norm,
        "vp_diff": float(vp_diff),
    }


def _age_label(raw: str) -> str:
    text = str(raw or "").strip()
    if not text:
        return "—"
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo) if dt.tzinfo is not None else datetime.now()
        seconds = max(0, int((now - dt).total_seconds()))
    except (TypeError, ValueError):
        return "—"
    if seconds < 60:
        return "<1 мин"
    if seconds < 3600:
        return f"{seconds // 60} мин"
    if seconds < 86400:
        return f"{seconds // 3600} ч"
    return f"{seconds // 86400} д"


def _short_timestamp(raw: Any) -> str:
    text = str(raw or "").strip().replace("T", " ")
    return text[:16] if text else ""


class OpponentPoolStatsWriter:
    """Единственный learner-side writer aggregate stats и live-state текущего запуска."""

    def __init__(
        self,
        *,
        stats_path: str,
        run_state_path: str,
        config: PoolConfig,
        learner_side: str,
        learner_algo: str,
        mission_name: str = "",
        run_id: str = "",
    ) -> None:
        self.stats_path = str(stats_path)
        self.run_state_path = str(run_state_path)
        self.config = config
        self.stats = OpponentStatsStore.load(self.stats_path, ema_alpha=config.ema_alpha)
        now = datetime.now().isoformat(timespec="seconds")
        self.run_state: dict[str, Any] = {
            "schema_version": 1,
            "run_id": str(run_id or f"pool-{os.getpid()}-{now}"),
            "started_at": now,
            "updated_at": now,
            "learner_side": str(learner_side or "").upper(),
            "learner_algo": str(learner_algo or ""),
            "mission": str(mission_name or ""),
            "p_heuristic": float(config.p_heuristic),
            "strategy": str(config.strategy),
            "total_games": 0,
            "snapshot_games": 0,
            "heuristic_games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "opponents": {},
            "last_opponent": {},
        }
        self._save_run_state()

    def _save_run_state(self) -> None:
        _atomic_write_json(self.run_state_path, self.run_state)

    def handle(self, payload: dict[str, Any], *, log_fn=None) -> dict[str, Any]:
        if not isinstance(payload, dict):
            return {}
        kind = str(payload.get("kind", "heuristic") or "heuristic").strip().lower()
        if kind not in {"snapshot", "heuristic"}:
            kind = "heuristic"
        agent_id = str(payload.get("agent_id", "") or "").strip()
        if kind == "snapshot" and not agent_id:
            kind = "heuristic"
        result = str(payload.get("result", "draw") or "draw").strip().lower()
        if result not in {"win", "draw", "loss"}:
            result = "draw"
        vp_diff = float(payload.get("vp_diff", 0.0) or 0.0)
        actor_raw = payload.get("actor_idx", -1)
        actor_idx = int(actor_raw) if actor_raw is not None else -1
        actor_ep_raw = payload.get("actor_ep", 0)
        actor_ep = int(actor_ep_raw) if actor_ep_raw is not None else 0

        if kind == "snapshot":
            self.stats.update(
                agent_id=agent_id,
                win=(result == "win"),
                draw=(result == "draw"),
                vp_diff=vp_diff,
            )
            self.stats.save()

        now = datetime.now().isoformat(timespec="seconds")
        state = self.run_state
        state["updated_at"] = now
        state["total_games"] = int(state.get("total_games", 0) or 0) + 1
        branch_key = "snapshot_games" if kind == "snapshot" else "heuristic_games"
        state[branch_key] = int(state.get(branch_key, 0) or 0) + 1
        result_key = {"win": "wins", "draw": "draws", "loss": "losses"}[result]
        state[result_key] = int(state.get(result_key, 0) or 0) + 1

        key = agent_id if kind == "snapshot" else POOL_RUN_HEURISTIC_KEY
        opponents = state.setdefault("opponents", {})
        rec = opponents.setdefault(key, {
            "kind": kind,
            "agent_id": agent_id,
            "games": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "vp_sum": 0.0,
            "last_selected_at": "",
            "last_reason": "",
            "expected_prob": 0.0,
        })
        rec["games"] = int(rec.get("games", 0) or 0) + 1
        rec[result_key] = int(rec.get(result_key, 0) or 0) + 1
        rec["vp_sum"] = float(rec.get("vp_sum", 0.0) or 0.0) + vp_diff
        rec["last_selected_at"] = now
        rec["last_reason"] = str(payload.get("reason", "") or "")
        rec["expected_prob"] = float(payload.get("prob_episode", 0.0) or 0.0)
        state["last_opponent"] = {
            "kind": kind,
            "agent_id": agent_id,
            "label": short_agent_label(agent_id) if agent_id else "эвристика",
            "reason": rec["last_reason"],
            "result": result,
            "actor_idx": actor_idx,
            "actor_ep": actor_ep,
            "selected_at": now,
        }
        self._save_run_state()

        persistent = self.stats.record(agent_id) if kind == "snapshot" else {}
        if log_fn is not None:
            suffix = (
                f" ema_wr={float(persistent.get('ema_winrate', 0.5)):.3f} "
                f"games={int(persistent.get('games', 0) or 0)}"
                if kind == "snapshot" else ""
            )
            log_fn(
                f"[POOL][RESULT] writer=learner actor={actor_idx} "
                f"kind={kind} agent={agent_id or '-'} result={result} vp={vp_diff:g} "
                f"run_games={int(rec['games'])} p_episode={float(rec['expected_prob']):.3f}{suffix}"
            )
        return dict(rec)


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
    run_state_path: str = "",
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
    run_state = _load_json_object(run_state_path)
    run_side = str(run_state.get("learner_side", "") or "").strip().upper()
    if run_side and run_side != learner_side:
        run_state = {}
    run_total = max(0, int(run_state.get("total_games", 0) or 0))
    run_opponents = run_state.get("opponents", {}) if isinstance(run_state.get("opponents"), dict) else {}
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
        run_rec = run_opponents.get(aid, {}) if isinstance(run_opponents.get(aid), dict) else {}
        run_games = max(0, int(run_rec.get("games", 0) or 0))
        prob_snapshot = float(row.get("prob", 0.0) or 0.0)
        prob_episode = (1.0 - preview_cfg.p_heuristic) * prob_snapshot
        meta = _enrich_agent_meta(aid, meta_index, in_pool=True)
        candidates.append({
            "agent_id": aid,
            "label": short_agent_label(aid),
            "games": games,
            "winrate": float(row.get("winrate", 0.5)) if row.get("winrate") is not None else 0.5,
            "draw_pct": (draws / games) if games > 0 else -1.0,
            "vp_per_game": (vp_sum / games) if games > 0 else 0.0,
            "wins": int(rec.get("wins", 0) or 0),
            "losses": int(rec.get("losses", 0) or 0),
            "tracked_draws": int(rec.get("tracked_draws", 0) or 0),
            "unclassified_games": int(rec.get("unclassified_games", 0) or 0),
            "updated_at": _short_timestamp(rec.get("updated_at", "")),
            "prob": prob_snapshot,
            "prob_snapshot": prob_snapshot,
            "prob_episode": prob_episode,
            "reason": str(row.get("reason", "") or ""),
            "run_games": run_games,
            "run_actual_prob": (run_games / run_total) if run_total > 0 else -1.0,
            "run_wins": int(run_rec.get("wins", 0) or 0),
            "run_draws": int(run_rec.get("draws", 0) or 0),
            "run_losses": int(run_rec.get("losses", 0) or 0),
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
            "winrate": float(rec.get("ema_winrate", 0.5)) if rec.get("ema_winrate") is not None else 0.5,
            "draw_pct": (draws / games) if games > 0 else -1.0,
            "vp_per_game": (vp_sum / games) if games > 0 else 0.0,
            "wins": int(rec.get("wins", 0) or 0),
            "losses": int(rec.get("losses", 0) or 0),
            "tracked_draws": int(rec.get("tracked_draws", 0) or 0),
            "unclassified_games": int(rec.get("unclassified_games", 0) or 0),
            "updated_at": _short_timestamp(rec.get("updated_at", "")),
            **meta,
        })
    history.sort(key=lambda item: int(item.get("games", 0) or 0), reverse=True)

    candidate_count = len(ids)
    formation = ui.get("refresh", {}) if isinstance(ui.get("refresh"), dict) else {}
    last_pick = parse_last_pool_pick(train_log_path) if train_log_path else {}
    run_last = run_state.get("last_opponent", {}) if isinstance(run_state.get("last_opponent"), dict) else {}
    if run_last:
        last_pick = {
            "label": str(run_last.get("label", "") or ""),
            "kind": str(run_last.get("kind", "") or ""),
            "reason": str(run_last.get("reason", "") or ""),
            "result": str(run_last.get("result", "") or ""),
            "selected_at": str(run_last.get("selected_at", "") or ""),
            "weight": 0.0,
        }
    max_snapshot_prob = max((float(row.get("prob_snapshot", 0.0) or 0.0) for row in candidates), default=0.0)
    latest_stats_at = max((str(row.get("updated_at", "") or "") for row in history), default="")
    draw_value = float(draw_rate) if draw_rate is not None else -1.0
    run_snapshot_games = max(0, int(run_state.get("snapshot_games", 0) or 0))
    run_heuristic_games = max(0, int(run_state.get("heuristic_games", 0) or 0))
    context: dict[str, Any] = {
        "learner_side": learner_side,
        "learner_faction": learner_faction,
        "learner_algo": str(learner_algo or ""),
        "opponent_side": opp_side,
        "pool_fill": f"{candidate_count}/{preview_cfg.pool_size}",
        "candidate_count": candidate_count,
        "pool_size": int(preview_cfg.pool_size),
        "registry_opponent_count": _count_registry_side(opp_side),
        "formation": formation,
        "pool_algo_mix": _pool_algo_mix(candidates),
        "mission": str(mission_name or ""),
        "draw_rate": draw_value,
        "draw_pit_alert": bool(draw_value >= 0.70),
        "max_snapshot_prob": max_snapshot_prob,
        "concentration_alert": bool(max_snapshot_prob >= 0.40),
        "stats_updated_at": latest_stats_at,
        "pool_enabled": bool(pool_enabled),
        "train_running": bool(train_running),
        "strategy": str(preview_cfg.strategy),
        "p_heuristic": float(preview_cfg.p_heuristic),
        "has_contract": bool(contract),
        "last_pick_label": str(last_pick.get("label", "") or ""),
        "last_pick_kind": str(last_pick.get("kind", "") or ""),
        "last_pick_reason": str(last_pick.get("reason", "") or ""),
        "last_pick_weight": float(last_pick.get("weight", 0.0) or 0.0),
        "last_pick_result": str(last_pick.get("result", "") or ""),
        "last_pick_at": _short_timestamp(last_pick.get("selected_at", "")),
        "run_id": str(run_state.get("run_id", "") or ""),
        "run_total_games": run_total,
        "run_snapshot_games": run_snapshot_games,
        "run_heuristic_games": run_heuristic_games,
        "run_snapshot_actual": (run_snapshot_games / run_total) if run_total > 0 else -1.0,
        "run_heuristic_actual": (run_heuristic_games / run_total) if run_total > 0 else -1.0,
        "run_wins": int(run_state.get("wins", 0) or 0),
        "run_draws": int(run_state.get("draws", 0) or 0),
        "run_losses": int(run_state.get("losses", 0) or 0),
        "run_updated_at": _short_timestamp(run_state.get("updated_at", "")),
    }

    heur_run = run_opponents.get(POOL_RUN_HEURISTIC_KEY, {})
    if not isinstance(heur_run, dict):
        heur_run = {}
    heur_games = max(0, int(heur_run.get("games", 0) or 0))

    return {
        "context": context,
        "candidates": candidates,
        "history": history,
        "heuristic": {
            "prob": float(preview_cfg.p_heuristic),
            "prob_episode": float(preview_cfg.p_heuristic),
            "label": "эвристика",
            "run_games": heur_games,
            "run_actual_prob": (heur_games / run_total) if run_total > 0 else -1.0,
            "run_wins": int(heur_run.get("wins", 0) or 0),
            "run_draws": int(heur_run.get("draws", 0) or 0),
            "run_losses": int(heur_run.get("losses", 0) or 0),
        },
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
                f"reason={choice.reason} weight={choice.weight:.3f} "
                f"p_episode={choice.weight:.3f}"
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
        p_episode = (1.0 - float(pool.config.p_heuristic)) * float(choice.weight)
        log_fn(
            f"[POOL] {actor_label} kind=snapshot agent={choice.agent_id} "
            f"reason={choice.reason} weight={choice.weight:.3f} "
            f"p_snapshot={choice.weight:.3f} p_episode={p_episode:.3f}"
        )
    return choice, policy_fn
