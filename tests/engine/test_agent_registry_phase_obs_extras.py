"""Task 1: make_env_contract автоматически кладёт phase_obs_features/reaction_value_policy в extras.

Формат obs_space_signature НЕ меняется (vec:N).
Переданные явно extras не перетираются (agent-переданные ключи приоритетны).
"""

import os
from unittest.mock import patch

from core.engine.agent_registry import make_env_contract


def test_contract_auto_extras_phase_obs_on():
    """При PHASE_OBS_FEATURES=1 extras содержит phase_obs_features=1."""
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "1"}, clear=False):
        contract = make_env_contract(
            n_observations=10, n_actions=[5, 2], mission_name="only_war"
        )
    assert contract["extras"]["phase_obs_features"] == 1


def test_contract_auto_extras_reaction_value_policy_on():
    """При AZ_REACTION_VALUE_POLICY=1 extras содержит reaction_value_policy=1."""
    with patch.dict(os.environ, {"AZ_REACTION_VALUE_POLICY": "1"}, clear=False):
        contract = make_env_contract(
            n_observations=10, n_actions=[5, 2], mission_name="only_war"
        )
    assert contract["extras"]["reaction_value_policy"] == 1


def test_contract_auto_extras_defaults_off():
    """Без env-vars оба флага 0 по умолчанию."""
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "0", "AZ_REACTION_VALUE_POLICY": "0"}, clear=False):
        contract = make_env_contract(
            n_observations=10, n_actions=[5, 2], mission_name="only_war"
        )
    assert contract["extras"]["phase_obs_features"] == 0
    assert contract["extras"]["reaction_value_policy"] == 0


def test_contract_explicit_extras_not_overwritten():
    """Agent-переданные extras приоритетны — не перетираются auto-значениями."""
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "1", "AZ_REACTION_VALUE_POLICY": "1"}, clear=False):
        contract = make_env_contract(
            n_observations=10,
            n_actions=[5, 2],
            mission_name="only_war",
            extras={"phase_obs_features": 0, "reaction_value_policy": 0, "custom": 42},
        )
    assert contract["extras"]["phase_obs_features"] == 0
    assert contract["extras"]["reaction_value_policy"] == 0
    assert contract["extras"]["custom"] == 42


def test_contract_obs_space_signature_unchanged():
    """Формат obs_space_signature остаётся vec:N (без +phase)."""
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "1"}, clear=False):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war"
        )
    assert contract["obs_space_signature"] == "vec:41"
    assert "+phase" not in contract["obs_space_signature"]


def test_contract_hash_changes_with_phase_obs():
    """contract_hash меняется при смене extras (identity-функция)."""
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "0"}, clear=False):
        c0 = make_env_contract(n_observations=10, n_actions=[5, 2], mission_name="only_war")
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "1"}, clear=False):
        c1 = make_env_contract(n_observations=10, n_actions=[5, 2], mission_name="only_war")
    assert c0["contract_hash"] != c1["contract_hash"]


def test_contract_extras_do_not_affect_compatible_contracts():
    """compatible_contracts игнорирует extras (совместимость только по sig)."""
    from core.engine.agent_registry import compatible_contracts

    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "0"}, clear=False):
        c0 = make_env_contract(n_observations=10, n_actions=[5, 2], mission_name="only_war")
    with patch.dict(os.environ, {"PHASE_OBS_FEATURES": "1"}, clear=False):
        c1 = make_env_contract(n_observations=10, n_actions=[5, 2], mission_name="only_war")
    ok, reason = compatible_contracts(c0, c1)
    assert ok is True
    assert reason == ""
