from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Optional

import torch
from project_paths import ARTIFACTS_MODELS_DIR, PROJECT_ROOT


AGENTS_ROOT = str(ARTIFACTS_MODELS_DIR / "agents")
AGENTS_REGISTRY_PATH = str(ARTIFACTS_MODELS_DIR / "agents_registry.json")
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


def models_dir() -> str:
    """Корень artifacts/models (локально или SMB: MODELS_DIR / 40KAI_MODELS_DIR)."""
    custom = str(os.getenv("40KAI_MODELS_DIR", os.getenv("MODELS_DIR", "")) or "").strip()
    if custom:
        base = custom.rstrip("\\/")
        name = os.path.basename(base).lower()
        if name == "agents":
            parent = os.path.dirname(base)
            return parent if parent else base
        if name == "actor_sync":
            parent = os.path.dirname(base)
            return parent if parent else base
        return base
    return str(ARTIFACTS_MODELS_DIR)


def agents_registry_path() -> str:
    return os.path.join(models_dir(), "agents_registry.json")


def _remap_models_path(path: str) -> str:
    """Пути из meta с ПК1 (C:\\...\\artifacts\\models\\...) → MODELS_DIR на ПК2 (Z:\\)."""
    raw = str(path or "").strip()
    if not raw:
        return ""
    if os.path.exists(raw):
        return raw
    normalized = raw.replace("\\", "/")
    lowered = normalized.lower()
    for marker in ("/artifacts/models/", "artifacts/models/"):
        idx = lowered.find(marker)
        if idx >= 0:
            suffix = normalized[idx + len(marker) :].lstrip("/")
            candidate = os.path.join(models_dir(), suffix.replace("/", os.sep))
            if os.path.exists(candidate):
                return candidate
    if normalized.startswith("models/"):
        candidate = os.path.join(models_dir(), normalized[len("models/") :].replace("/", os.sep))
        if os.path.exists(candidate):
            return candidate
    candidate = str(ARTIFACTS_MODELS_DIR / normalized.replace("/", os.sep).lstrip(os.sep))
    if os.path.exists(candidate):
        return candidate
    candidate = os.path.join(str(PROJECT_ROOT), raw)
    if os.path.exists(candidate):
        return candidate
    return raw


def _resolve_legacy_models_path(path: Any) -> str:
    raw = str(path or "").strip()
    if not raw:
        return ""
    remapped = _remap_models_path(raw)
    if remapped and os.path.exists(remapped):
        return remapped
    return raw


def _resolve_agent_artifact_path(path: Any, artifact_dir: str, fallback_name: str) -> str:
    raw = _resolve_legacy_models_path(path)
    if raw and os.path.exists(raw):
        return raw
    root = str(artifact_dir or "").strip()
    if root:
        remapped_root = _remap_models_path(root)
        if remapped_root and os.path.isdir(remapped_root):
            candidate = os.path.join(remapped_root, fallback_name)
            if os.path.exists(candidate):
                return candidate
    return raw


def _find_agent_entry_on_disk(agent_id: str) -> Optional[dict[str, Any]]:
    target = str(agent_id or "").strip()
    root_agents = agents_meta_root()
    if not target or not os.path.isdir(root_agents):
        return None
    for root, _dirs, files in os.walk(root_agents):
        if "meta.json" not in files:
            continue
        meta_path = os.path.join(root, "meta.json")
        meta = _load_json(meta_path, {})
        if str((meta or {}).get("agent_id", "")).strip() != target:
            continue
        contract_path = os.path.join(root, "env_contract.json")
        side = str((meta or {}).get("side", "")).strip() or "P1"
        faction = str((meta or {}).get("faction", "")).strip() or "Unknown"
        ruleset = str((meta or {}).get("ruleset_version", "")).strip() or DEFAULT_RULESET_VERSION
        return {
            "agent_id": target,
            "side": side,
            "faction": faction,
            "ruleset_version": ruleset,
            "artifact_dir": root,
            "meta_path": meta_path,
            "contract_path": contract_path,
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        }
    return None


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


def agents_meta_root() -> str:
    """Корень agents/ (локальный repo или SMB через MODELS_DIR / 40KAI_MODELS_DIR)."""
    return os.path.join(models_dir(), "agents")


def collect_registered_agents_meta(*, agents_root: str | None = None) -> list[dict[str, str]]:
    """Список снапшотов из meta.json (как GUI «Последний снапшот»), новые первые."""
    root = str(agents_root or agents_meta_root())
    if not os.path.isdir(root):
        return []
    records: list[dict[str, str]] = []
    for dirpath, _, files in os.walk(root):
        if "meta.json" not in files:
            continue
        meta_path = os.path.join(dirpath, "meta.json")
        payload = _load_json(meta_path, {})
        if not isinstance(payload, dict):
            continue
        agent_id = str(payload.get("agent_id", "")).strip()
        side = str(payload.get("side", "")).strip().upper()
        faction = str(payload.get("faction", "")).strip()
        created_at = str(payload.get("created_at", "")).strip()
        algo = str(payload.get("algo", "")).strip().lower()
        if algo == "alphazero":
            continue
        if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
            paths = payload.get("paths")
            if isinstance(paths, dict):
                target_path = paths.get("target")
                algo = "ppo" if (target_path is None or str(target_path).strip() == "") else "dqn"
            else:
                algo = "unknown"
        if not agent_id or side not in {"P1", "P2"}:
            continue
        records.append(
            {
                "agent_id": agent_id,
                "side": side,
                "faction": faction or "Unknown",
                "created_at": created_at,
                "algo": algo,
            }
        )
    records.sort(key=lambda item: (item.get("created_at", ""), item["agent_id"]), reverse=True)
    return records


def resolve_latest_opponent_agent_id(*, learner_side: str = "P1", agents_root: str | None = None) -> str:
    """Последний снапшот на стороне оппонента (как GUI latest_snapshot)."""
    side = str(learner_side or "P1").strip().upper() or "P1"
    opponent_side = "P2" if side == "P1" else "P1"
    records = [
        rec
        for rec in collect_registered_agents_meta(agents_root=agents_root)
        if str(rec.get("side", "")).upper() == opponent_side
    ]
    if not records:
        return ""
    return str(records[0].get("agent_id", "") or "").strip()


def list_agents(*, side: Optional[str] = None, faction: Optional[str] = None) -> list[dict[str, Any]]:
    registry = _load_json(agents_registry_path(), {"agents": []})
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
        selected = _find_agent_entry_on_disk(agent_id)
    if selected is None:
        raise FileNotFoundError(f"Agent '{agent_id}' not found in registry or artifacts/models/agents.")

    artifact_dir = str(selected.get("artifact_dir", "") or "")
    contract_path = _resolve_agent_artifact_path(selected.get("contract_path"), artifact_dir, "env_contract.json")
    meta_path = _resolve_agent_artifact_path(selected.get("meta_path"), artifact_dir, "meta.json")
    contract = _load_json(contract_path, {})
    meta = _load_json(meta_path, {})
    paths = meta.get("paths") if isinstance(meta, dict) else {}
    paths = paths if isinstance(paths, dict) else {}
    policy_path = _resolve_agent_artifact_path(paths.get("policy"), artifact_dir, "policy.pth")
    target_path = _resolve_agent_artifact_path(paths.get("target"), artifact_dir, "target.pth")
    optimizer_path = _resolve_agent_artifact_path(paths.get("optimizer"), artifact_dir, "optimizer.pth")
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

