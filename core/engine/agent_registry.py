from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Any

import torch

from project_paths import ARTIFACTS_MODELS_DIR, PROJECT_ROOT, resolve_share_models_root


# Lazy import to avoid circular import at module-load time.
def _phase_obs_features_enabled() -> bool:
    from core.engine.phases.obs_features import phase_obs_features_enabled

    return phase_obs_features_enabled()


def _env_bool(name: str, default: str = "0") -> bool:
    return str(os.getenv(str(name), str(default))).strip().lower() in {"1", "true", "yes", "on"}


# Каждый алго включает value-gate реакций своим env-флагом {TAG}_REACTION_VALUE_POLICY
# (см. core/models/*: GMZ/SMZ/AZ/GAZ/DQN/PPO). Контракт обязан резолвить флаг ПО АЛГО,
# иначе хардкод AZ молча пишет 0 для GMZ/SMZ-агентов, и eval отключает их умные реакции
# (тот же класс, что algo-allowlist).
_REACTION_FLAG_TAG_BY_ALGO = {
    "dqn": "DQN",
    "ppo": "PPO",
    "alphazero_tree": "AZ",
    "gumbel_az": "AZ",
    "gumbel_muzero": "GMZ",
    "sampled_muzero": "SMZ",
}

# Приоритет env-тегов по алго (повторяет runtime-резолв _az_family_env). gumbel_az
# едет на AZ-инфре, но управляется своим GAZ_*-флагом: runtime берёт GAZ_* → AZ_* →
# секция. Контракт обязан совпадать, иначе при GAZ_=1/AZ_=0 он писал 0, а сеть
# обучалась с reaction=1 → eval молча отключал реакции у GAZ-агента.
_REACTION_FLAG_TAG_PRIORITY_BY_ALGO = {
    "gumbel_az": ("GAZ", "AZ"),
}


def _reaction_value_policy_for_algo(algo: str | None) -> int:
    """reaction_value_policy для контракта по train_algo (дефолт ON у каждого флага).

    Резолв повторяет runtime: для gumbel_az — приоритет GAZ_* → AZ_* (как
    _az_family_env). Неизвестный/отсутствующий algo → AZ-флаг (back-compat).
    """
    a = str(algo or "").strip().lower()
    priority = _REACTION_FLAG_TAG_PRIORITY_BY_ALGO.get(a)
    if priority:
        for tag in priority:
            raw = os.getenv(f"{tag}_REACTION_VALUE_POLICY")
            if raw is not None:
                return int(str(raw).strip().lower() in {"1", "true", "yes", "on"})
        return 1  # дефолт ON, если ни один env не задан
    tag = _REACTION_FLAG_TAG_BY_ALGO.get(a, "AZ")
    return int(_env_bool(f"{tag}_REACTION_VALUE_POLICY", "1"))


AGENTS_ROOT = str(ARTIFACTS_MODELS_DIR / "agents")
AGENTS_REGISTRY_PATH = str(ARTIFACTS_MODELS_DIR / "agents_registry.json")
DEFAULT_RULESET_VERSION = "only_war_v2"


@dataclass(frozen=True)
class AgentIdentity:
    side: str
    faction: str
    ruleset_version: str = DEFAULT_RULESET_VERSION

    def normalized(self) -> AgentIdentity:
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
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return fallback


def _write_json(path: str, payload: Any) -> None:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def models_dir() -> str:
    """Корень artifacts/models (локально или SMB-шара ПК1).

    Единый резолвер из project_paths: 40KAI_SHARE_ROOT → 40KAI_MODELS_DIR →
    MODELS_DIR → локальный artifacts/models (хвост actor_sync/agents стрипится).
    """
    return resolve_share_models_root()


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


def _find_agent_entry_on_disk(agent_id: str) -> dict[str, Any] | None:
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
    extras: dict[str, Any] | None = None,
) -> dict[str, Any]:
    obs_signature = f"vec:{int(n_observations)}"
    act_signature = "heads:" + ",".join(str(int(v)) for v in n_actions)

    # Автоматически добавляем phase_obs_features и reaction_value_policy в extras
    # (не перетирая явно переданные ключи — agent-переданные ключи приоритетны).
    # reaction_value_policy резолвится ПО АЛГО (extras["train_algo"]): GMZ/SMZ имеют
    # свои флаги, хардкод AZ молча писал 0 для них и отключал умные реакции на eval.
    auto_extras: dict[str, Any] = {
        "phase_obs_features": int(_phase_obs_features_enabled()),
        "reaction_value_policy": _reaction_value_policy_for_algo((extras or {}).get("train_algo")),
    }
    merged_extras = {**auto_extras, **(extras or {})}

    payload = {
        "ruleset_version": str(ruleset_version or DEFAULT_RULESET_VERSION),
        "mission_name": str(mission_name or "only_war"),
        "obs_space_signature": obs_signature,
        "action_space_signature": act_signature,
        "extras": merged_extras,
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


_VALID_AGENT_ALGOS = frozenset(
    {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az", "sampled_muzero", "phoenix"}
)


def infer_algo_from_policy_state(policy_state: dict[str, Any] | None) -> str | None:
    """Определить алгоритм по ключам state_dict (meta может быть устаревшей)."""
    if not isinstance(policy_state, dict) or not policy_state:
        return None
    keys = [str(k) for k in policy_state.keys()]
    if any(
        k.startswith("action_embed.")
        or k.startswith("dynamics.")
        or k.startswith("projector.")
        or k.startswith("predictor.")
        for k in keys
    ):
        return "phoenix"
    if any(k.startswith("repr_input_fc.") or k.startswith("dyn_fc1.") for k in keys):
        return "gumbel_muzero"
    if any(
        k.startswith("head_bundles.")
        or k.startswith("q_heads.")
        or k == "iqn_pi_multipliers"
        for k in keys
    ):
        return "dqn"
    if any(k.startswith("actor.") or k.startswith("critic.") for k in keys):
        return "ppo"
    if any(k.startswith("policy_heads.") for k in keys):
        return "alphazero_tree"
    return None


def _refine_az_algo_from_meta(algo: str, meta: dict[str, Any] | None) -> str:
    if algo not in {"alphazero_tree", "alphazero_proxy"}:
        return algo
    mm = str((meta or {}).get("mcts_mode", "") or "").strip().lower()
    if mm == "proxy":
        return "alphazero_proxy"
    if mm == "tree":
        return "alphazero_tree"
    return algo


def resolve_agent_algo(
    *,
    meta: dict[str, Any] | None,
    policy_state: dict[str, Any] | None,
    target_state: dict[str, Any] | None = None,
    agent_id: str = "",
) -> str:
    """Согласовать meta.algo и фактическую архитектуру весов; при конфликте — доверять весам."""
    meta_algo = str((meta or {}).get("algo", "")).strip().lower()
    if meta_algo == "alphazero":
        meta_algo = "alphazero_tree"
    inferred = infer_algo_from_policy_state(policy_state)
    if inferred is not None:
        resolved = _refine_az_algo_from_meta(inferred, meta)
        # PPO и AlphaZero (tree/proxy) делят одну архитектуру сети
        # (input_fc/blocks/policy_heads/value_heads) — инференс по state_dict их не
        # различает и для PPO-весов даёт az-семейство. В этой неоднозначности
        # meta.algo авторитетна (её пишет тренер), иначе PPO грузится как AZ-tree.
        if resolved in {"alphazero_tree", "alphazero_proxy"} and meta_algo == "ppo":
            return "ppo"
        # gumbel_az шарит AZ-архитектуру (policy_heads/value_heads) — веса неотличимы
        # от AZ-tree; meta.algo авторитетна (её пишет тренер). Проверка ДО generic-блока ниже.
        if resolved in {"alphazero_tree", "alphazero_proxy"} and meta_algo == "gumbel_az":
            return "gumbel_az"
        # sampled_muzero шарит архитектуру GumbelMuZeroNet с gumbel_muzero — веса неотличимы
        # (repr_input_fc./dyn_fc1.), инференс по state_dict даёт "gumbel_muzero". meta.algo
        # авторитетна (её пишет тренер), иначе sampled-агент молча станет gumbel_muzero.
        if resolved == "gumbel_muzero" and meta_algo == "sampled_muzero":
            return "sampled_muzero"
        # Phoenix шарит DQN-ключи (online./head_bundles./iqn_pi_multipliers) — веса
        # без SPR-голов неотличимы от DQN; meta.algo авторитетна (её пишет тренер).
        if resolved == "dqn" and meta_algo == "phoenix":
            return "phoenix"
        if meta_algo in _VALID_AGENT_ALGOS and meta_algo != resolved:
            aid = str(agent_id or (meta or {}).get("agent_id", "") or "").strip()
            prefix = f"agent '{aid}'" if aid else "agent"
            print(
                f"[AGENT][WARN] {prefix}: meta.algo={meta_algo!r} не совпадает с весами "
                f"({resolved!r}); используем веса.",
                flush=True,
            )
        return resolved
    if meta_algo in _VALID_AGENT_ALGOS:
        return _refine_az_algo_from_meta(meta_algo, meta)
    if isinstance(target_state, dict) and bool(target_state):
        return "dqn"
    raise ValueError(
        f"agent '{agent_id or (meta or {}).get('agent_id', '')}': не удалось определить algo "
        f"(meta={meta_algo!r}; ожидается dqn/ppo/alphazero_tree/alphazero_proxy/gumbel_muzero/gumbel_az/sampled_muzero)."
    )


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
    target_state_dict: dict[str, Any] | None = None,
    optimizer_state_dict: dict[str, Any] | None = None,
    extra_meta: dict[str, Any] | None = None,
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
        if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az", "sampled_muzero"}:
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


def list_agents(*, side: str | None = None, faction: str | None = None) -> list[dict[str, Any]]:
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

