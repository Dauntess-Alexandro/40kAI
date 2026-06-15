"""Регрессионный тест на «реестровый путь» sampled_muzero.

До фикса агент sampled_muzero классифицировался как gumbel_muzero (а из него — как
dqn в collect_registered_agents_meta из-за неполного списка algo), т.к. веса
SampledMuZeroNet (= GumbelMuZeroNet) неотличимы от gumbel_muzero по state_dict.

Фикс в core/engine/agent_registry.py:
- resolve_agent_algo доверяет meta.algo="sampled_muzero", когда инференс по весам
  даёт "gumbel_muzero" (см. _refine_az_algo_from_meta-блок и проверку
  `resolved == "gumbel_muzero" and meta_algo == "sampled_muzero"`).
- _VALID_AGENT_ALGOS и collect_registered_agents_meta включают "sampled_muzero".

Этот тест фиксирует поведение, чтобы регрессия не вернулась.
"""

from __future__ import annotations

import pathlib
import sys

import pytest

_PROJECT_ROOT = str(pathlib.Path(__file__).parent.parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.engine import agent_registry
from core.engine.agent_registry import (
    _VALID_AGENT_ALGOS,
    AgentIdentity,
    collect_registered_agents_meta,
    resolve_agent_algo,
    save_agent_artifact,
)
from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.utils import normalize_state_dict

N_OBS = 14
N_ACTIONS = [4, 2, 6]
_SMALL_KWARGS = dict(latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8)


def _sampled_policy_state() -> dict:
    net = make_sampled_muzero_net(N_OBS, N_ACTIONS, **_SMALL_KWARGS)
    return normalize_state_dict(net.state_dict())


def test_sampled_muzero_in_valid_agent_algos():
    assert "sampled_muzero" in _VALID_AGENT_ALGOS


def test_resolve_agent_algo_trusts_sampled_meta():
    """Веса sampled_muzero (= GumbelMuZeroNet) дают inferred="gumbel_muzero",
    но meta.algo="sampled_muzero" авторитетна — resolve_agent_algo обязан
    вернуть "sampled_muzero", а не "gumbel_muzero"."""
    policy_state = _sampled_policy_state()

    meta = {"algo": "sampled_muzero", "agent_id": "P1_TestFaction_sampled_test"}
    resolved = resolve_agent_algo(meta=meta, policy_state=policy_state, agent_id=meta["agent_id"])
    assert resolved == "sampled_muzero"

    # Контроль: без meta.algo="sampled_muzero" инференс по весам действительно
    # даёт "gumbel_muzero" — подтверждает, что фикс работает именно на доверии meta.
    resolved_no_meta = resolve_agent_algo(meta={}, policy_state=policy_state, agent_id="P1_no_meta")
    assert resolved_no_meta == "gumbel_muzero"


def test_collect_registered_agents_meta_reports_sampled(tmp_path, monkeypatch):
    """save_agent_artifact с algo="sampled_muzero" + sampled-весами -> collect_registered_agents_meta
    должен вернуть этого агента с algo == "sampled_muzero" (не dqn/gumbel_muzero)."""
    agents_root = tmp_path / "agents"
    registry_path = tmp_path / "agents_registry.json"
    monkeypatch.setattr(agent_registry, "AGENTS_ROOT", str(agents_root))
    monkeypatch.setattr(agent_registry, "AGENTS_REGISTRY_PATH", str(registry_path))
    monkeypatch.setattr(agent_registry, "models_dir", lambda: str(tmp_path))

    identity = AgentIdentity(side="P1", faction="TestFaction")
    agent_id = "P1_TestFaction_sampled_only_war_v1_test_001"

    policy_state = _sampled_policy_state()
    env_contract = agent_registry.make_env_contract(
        n_observations=N_OBS,
        n_actions=N_ACTIONS,
        mission_name="only_war",
    )

    save_agent_artifact(
        identity=identity,
        agent_id=agent_id,
        env_contract=env_contract,
        policy_state_dict=policy_state,
        extra_meta={"algo": "sampled_muzero", "arch": _SMALL_KWARGS},
    )

    records = collect_registered_agents_meta(agents_root=str(agents_root))
    matching = [r for r in records if r["agent_id"] == agent_id]
    assert len(matching) == 1, f"Агент {agent_id} не найден среди {records}"
    assert matching[0]["algo"] == "sampled_muzero"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
