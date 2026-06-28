from __future__ import annotations

import random
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from core.engine.opponent_pool import OpponentChoice, OpponentPool, OpponentStatsStore, PoolConfig

__all__ = [
    "OpponentRuntimeCache",
    "default_candidate_provider",
    "build_pool_for_actor",
    "choose_opponent_policy_fn",
]


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
