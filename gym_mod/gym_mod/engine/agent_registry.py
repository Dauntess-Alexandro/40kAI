from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional

import torch


AGENTS_ROOT = os.path.join("models", "agents")
AGENTS_REGISTRY_PATH = os.path.join("models", "agents_registry.json")
DEFAULT_RULESET_VERSION = "only_war_v1"


@dataclass(frozen=True)
class AgentIdentity:
    side: str
    faction: str
    ruleset_version: str = DEFAULT_RULESET_VERSION

    def normalized(self) -> "AgentIdentity":
        side = str(self.side or "").strip().upper()
        if side not in {"P1", "P2"}:
            side = "P1"
        faction = str(self.faction or "Unknown").strip() or "Unknown"
        return AgentIdentity(side=side, faction=faction, ruleset_version=str(self.ruleset_version or DEFAULT_RULESET_VERSION))


def _safe_name(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", str(value or "").strip())
    return cleaned or "unknown"


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _load_json(path: str, fallback: Any) -> Any:
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return fallback


def _write_json(path: str, payload: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _hash_compact(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16]


def make_env_contract(
    *,
    n_observations: int,
    n_actions: list[int],
    mission_name: str,
    ruleset_version: str = DEFAULT_RULESET_VERSION,
    extras: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    obs_signature = f"vec:{int(n_observations)}"
    act_signature = "heads:" + ",".join(str(int(v)) for v in n_actions)
    payload = {
        "ruleset_version": str(ruleset_version or DEFAULT_RULESET_VERSION),
        "mission_name": str(mission_name or "only_war"),
        "obs_space_signature": obs_signature,
        "action_space_signature": act_signature,
        "extras": extras or {},
    }
    payload["contract_hash"] = _hash_compact(
        {
            "ruleset_version": payload["ruleset_version"],
            "mission_name": payload["mission_name"],
            "obs_space_signature": payload["obs_space_signature"],
            "action_space_signature": payload["action_space_signature"],
            "extras": payload["extras"],
        }
    )
    return payload


def compatible_contracts(left: dict[str, Any], right: dict[str, Any]) -> tuple[bool, str]:
    if left.get("ruleset_version") != right.get("ruleset_version"):
        return False, "ruleset_version mismatch"
    if left.get("obs_space_signature") != right.get("obs_space_signature"):
        return False, "obs_space_signature mismatch"
    if left.get("action_space_signature") != right.get("action_space_signature"):
        return False, "action_space_signature mismatch"
    return True, ""


def build_agent_id(identity: AgentIdentity, step_or_tag: str | int) -> str:
    ident = identity.normalized()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{ident.side}_{_safe_name(ident.faction)}_{_safe_name(ident.ruleset_version)}_{_safe_name(step_or_tag)}_{now}"


def agent_dir(identity: AgentIdentity, agent_id: str) -> str:
    ident = identity.normalized()
    return os.path.join(AGENTS_ROOT, ident.side, _safe_name(ident.faction), _safe_name(agent_id))


def save_agent_artifact(
    *,
    identity: AgentIdentity,
    agent_id: str,
    env_contract: dict[str, Any],
    policy_state_dict: dict[str, Any],
    target_state_dict: Optional[dict[str, Any]] = None,
    optimizer_state_dict: Optional[dict[str, Any]] = None,
    extra_meta: Optional[dict[str, Any]] = None,
) -> str:
    ident = identity.normalized()
    root = agent_dir(ident, agent_id)
    _ensure_dir(root)

    policy_path = os.path.join(root, "policy.pth")
    target_path = os.path.join(root, "target.pth")
    optimizer_path = os.path.join(root, "optimizer.pth")
    meta_path = os.path.join(root, "meta.json")
    contract_path = os.path.join(root, "env_contract.json")

    torch.save(policy_state_dict, policy_path)
    if target_state_dict is not None:
        torch.save(target_state_dict, target_path)
    if optimizer_state_dict is not None:
        torch.save(optimizer_state_dict, optimizer_path)

    _write_json(contract_path, env_contract)
    meta = {
        "agent_id": agent_id,
        "side": ident.side,
        "faction": ident.faction,
        "ruleset_version": ident.ruleset_version,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "paths": {
            "policy": policy_path,
            "target": target_path if target_state_dict is not None else None,
            "optimizer": optimizer_path if optimizer_state_dict is not None else None,
            "contract": contract_path,
        },
    }
    if extra_meta:
        meta.update(extra_meta)
    _write_json(meta_path, meta)

    registry = _load_json(AGENTS_REGISTRY_PATH, {"agents": []})
    if not isinstance(registry, dict):
        registry = {"agents": []}
    entries = registry.get("agents")
    if not isinstance(entries, list):
        entries = []
    entries = [entry for entry in entries if str(entry.get("agent_id")) != agent_id]
    entries.append(
        {
            "agent_id": agent_id,
            "side": ident.side,
            "faction": ident.faction,
            "ruleset_version": ident.ruleset_version,
            "artifact_dir": root,
            "meta_path": meta_path,
            "contract_path": contract_path,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    registry["agents"] = entries
    _write_json(AGENTS_REGISTRY_PATH, registry)
    return root


def list_agents(*, side: Optional[str] = None, faction: Optional[str] = None) -> list[dict[str, Any]]:
    registry = _load_json(AGENTS_REGISTRY_PATH, {"agents": []})
    agents = registry.get("agents", []) if isinstance(registry, dict) else []
    if not isinstance(agents, list):
        return []
    result = []
    for entry in agents:
        if not isinstance(entry, dict):
            continue
        if side and str(entry.get("side", "")).upper() != str(side).upper():
            continue
        if faction and str(entry.get("faction", "")).lower() != str(faction).lower():
            continue
        result.append(entry)
    return result


def load_agent_by_id(agent_id: str) -> dict[str, Any]:
    agents = list_agents()
    selected = None
    for entry in agents:
        if str(entry.get("agent_id")) == str(agent_id):
            selected = entry
            break
    if selected is None:
        raise FileNotFoundError(f"Agent '{agent_id}' not found in registry.")

    contract_path = selected.get("contract_path")
    meta_path = selected.get("meta_path")
    contract = _load_json(contract_path, {})
    meta = _load_json(meta_path, {})
    policy_path = (meta.get("paths") or {}).get("policy")
    target_path = (meta.get("paths") or {}).get("target")
    optimizer_path = (meta.get("paths") or {}).get("optimizer")
    if not policy_path or not os.path.exists(policy_path):
        raise FileNotFoundError(f"Policy file missing for agent '{agent_id}'.")

    payload = {
        "agent_id": agent_id,
        "entry": selected,
        "meta": meta,
        "contract": contract,
        "policy_state": torch.load(policy_path, map_location="cpu"),
        "target_state": torch.load(target_path, map_location="cpu") if target_path and os.path.exists(target_path) else None,
        "optimizer_state": torch.load(optimizer_path, map_location="cpu") if optimizer_path and os.path.exists(optimizer_path) else None,
    }
    return payload

