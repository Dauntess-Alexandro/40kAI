"""Stage 8.2: опциональные метаданные фаз/стратагем в replay-транзишенах."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, fields
from typing import Any


@dataclass
class ReplayPhaseMeta:
    phase: str | None = None
    sub_step: str | None = None
    window_id: str | None = None
    chosen_option: str | None = None
    stratagem_id: str | None = None
    cp_before: int | None = None
    cp_after: int | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if val is not None:
                out[f.name] = val
        return out

    @classmethod
    def from_dict(cls, raw: dict[str, Any] | None) -> ReplayPhaseMeta | None:
        if not isinstance(raw, dict) or not raw:
            return None
        kwargs: dict[str, Any] = {}
        for f in fields(cls):
            if f.name not in raw:
                continue
            val = raw.get(f.name)
            if val is None:
                continue
            if f.name in {"cp_before", "cp_after"}:
                kwargs[f.name] = int(val)
            else:
                kwargs[f.name] = str(val)
        if not kwargs:
            return None
        return cls(**kwargs)


def replay_phase_meta_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    raw = str(os.getenv("REPLAY_PHASE_META", "1")).strip().lower()
    return raw in {"1", "true", "yes", "on"}


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def _infer_stratagem_id(action_dict: dict | None) -> str | None:
    if not isinstance(action_dict, dict):
        return None
    use_cp = int(action_dict.get("use_cp", 0) or 0)
    if use_cp == 1:
        return "insane_bravery"
    plan = action_dict.get("_fight_stratagem_plan")
    if isinstance(plan, dict) and plan:
        # первый выбранный fight-стратагем (плоский step не кодирует их в головах)
        return str(next(iter(plan.values())))
    return None


def _action_dict_summary(action_dict: dict | None) -> str | None:
    if not isinstance(action_dict, dict) or not action_dict:
        return None
    compact = {str(k): int(v) for k, v in action_dict.items() if v is not None}
    if not compact:
        return None
    return json.dumps(compact, sort_keys=True, ensure_ascii=False)


def capture_replay_phase_meta(
    env,
    *,
    side: str = "model",
    action_dict: dict | None = None,
    cp_before: int | None = None,
    phase: str | None = None,
    sub_step: str | None = None,
    window_id: str | None = None,
    chosen_option: str | None = None,
    stratagem_id: str | None = None,
) -> ReplayPhaseMeta | None:
    """Снять метаданные с env после шага (или перед+после для CP)."""
    if not replay_phase_meta_enabled():
        return None
    e = _unwrap(env)
    if side == "model":
        cp_after = int(getattr(e, "modelCP", 0) or 0)
    else:
        cp_after = int(getattr(e, "enemyCP", 0) or 0)
    if cp_before is None:
        cp_before = cp_after
    sid = stratagem_id if stratagem_id is not None else _infer_stratagem_id(action_dict)
    chosen = chosen_option if chosen_option is not None else _action_dict_summary(action_dict)
    phase_name = str(phase if phase is not None else getattr(e, "phase", "") or "") or None
    return ReplayPhaseMeta(
        phase=phase_name,
        sub_step=str(sub_step) if sub_step else None,
        window_id=str(window_id) if window_id else None,
        chosen_option=chosen,
        stratagem_id=sid,
        cp_before=int(cp_before),
        cp_after=int(cp_after),
    )


def snapshot_cp_before(env, *, side: str = "model") -> int:
    e = _unwrap(env)
    if side == "model":
        return int(getattr(e, "modelCP", 0) or 0)
    return int(getattr(e, "enemyCP", 0) or 0)


def wire_dict_for_phase_meta(meta: ReplayPhaseMeta | None) -> dict[str, Any]:
    if meta is None:
        return {}
    d = meta.to_dict()
    return {"phase_meta": d} if d else {}


def az_transition_to_rollout_dict(transition, *, policy_version: int | None = None) -> dict[str, Any]:
    """Сериализация AZTransition для dist rollout / replay wire."""
    import numpy as np

    pv = int(
        policy_version
        if policy_version is not None
        else getattr(transition, "policy_version", 0)
    )
    row: dict[str, Any] = {
        "state": np.asarray(transition.state, dtype=np.float32),
        "policy_targets": [np.asarray(p, dtype=np.float32) for p in transition.policy_targets],
        "value_target": float(transition.value_target),
        "policy_version": pv,
    }
    faction = str(getattr(transition, "faction", "") or "")
    if faction:
        row["faction"] = faction
    row.update(wire_dict_for_phase_meta(getattr(transition, "phase_meta", None)))
    return row


def az_transition_from_rollout_dict(raw: dict, *, default_policy_version: int = 0):
    """Десериализация AZTransition из rollout dict (обратная совместимость без phase_meta)."""
    from core.models.alphazero_replay import AZTransition
    import numpy as np

    if not isinstance(raw, dict):
        return None
    state_np = np.asarray(raw.get("state", []), dtype=np.float32)
    pi_raw = raw.get("policy_targets", [])
    if not isinstance(pi_raw, list):
        return None
    pi = [np.asarray(p, dtype=np.float32) for p in pi_raw]
    return AZTransition(
        state=state_np,
        policy_targets=pi,
        value_target=float(raw.get("value_target", 0.0) or 0.0),
        policy_version=int(raw.get("policy_version", default_policy_version) or default_policy_version),
        faction=str(raw.get("faction", "") or ""),
        phase_meta=ReplayPhaseMeta.from_dict(raw.get("phase_meta")),
    )


def gmz_transition_to_rollout_dict(transition, *, policy_version: int | None = None) -> dict[str, Any]:
    import numpy as np

    pv = int(
        policy_version
        if policy_version is not None
        else getattr(transition, "policy_version", 0)
    )
    row: dict[str, Any] = {
        "state": np.asarray(transition.state, dtype=np.float32),
        "action": np.asarray(transition.action, dtype=np.int64),
        "reward": float(transition.reward),
        "done": bool(transition.done),
        "policy_targets": [np.asarray(p, dtype=np.float32) for p in transition.policy_targets],
        "behavior_logits": [
            np.asarray(b, dtype=np.float32) for b in (getattr(transition, "behavior_logits", None) or [])
        ],
        "legal_masks_by_head": [
            np.asarray(m, dtype=np.float32) for m in (getattr(transition, "legal_masks_by_head", None) or [])
        ],
        "value_target": float(transition.value_target),
        "policy_version": pv,
    }
    row.update(wire_dict_for_phase_meta(getattr(transition, "phase_meta", None)))
    return row


def gmz_transition_from_rollout_dict(raw: dict, *, default_policy_version: int = 0):
    from core.models.gumbel_muzero_replay import GMZTransition
    import numpy as np

    if not isinstance(raw, dict):
        return None
    pi_raw = raw.get("policy_targets", [])
    if not isinstance(pi_raw, list):
        return None
    beh_raw = raw.get("behavior_logits", [])
    masks_raw = raw.get("legal_masks_by_head", [])
    return GMZTransition(
        state=np.asarray(raw.get("state", []), dtype=np.float32),
        action=np.asarray(raw.get("action", []), dtype=np.int64),
        reward=float(raw.get("reward", 0.0) or 0.0),
        done=bool(raw.get("done", False)),
        policy_targets=[np.asarray(p, dtype=np.float32) for p in pi_raw],
        behavior_logits=[
            np.asarray(b, dtype=np.float32) for b in (beh_raw if isinstance(beh_raw, list) else [])
        ],
        legal_masks_by_head=[
            np.asarray(m, dtype=np.float32) for m in (masks_raw if isinstance(masks_raw, list) else [])
        ],
        value_target=float(raw.get("value_target", 0.0) or 0.0),
        policy_version=int(raw.get("policy_version", default_policy_version) or default_policy_version),
        phase_meta=ReplayPhaseMeta.from_dict(raw.get("phase_meta")),
    )
