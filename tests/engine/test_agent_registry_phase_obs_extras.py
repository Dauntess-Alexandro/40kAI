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


# --- reaction_value_policy резолвится ПО АЛГО (а не хардкод AZ для всех) ---
# Регрессия: GMZ/SMZ-агенты получали reaction_value_policy=0 по AZ-флагу, хотя
# обучались с реакциями ON через свой флаг → eval молча отключал умные реакции.


def test_contract_reaction_gmz_uses_gmz_flag_not_az():
    """gumbel_muzero: reaction берётся из GMZ_REACTION_VALUE_POLICY, не из AZ."""
    with patch.dict(
        os.environ,
        {"GMZ_REACTION_VALUE_POLICY": "1", "AZ_REACTION_VALUE_POLICY": "0"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "gumbel_muzero"},
        )
    assert contract["extras"]["reaction_value_policy"] == 1


def test_contract_reaction_smz_uses_smz_flag_not_az():
    """sampled_muzero: reaction берётся из SMZ_REACTION_VALUE_POLICY, не из AZ."""
    with patch.dict(
        os.environ,
        {"SMZ_REACTION_VALUE_POLICY": "1", "AZ_REACTION_VALUE_POLICY": "0"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "sampled_muzero"},
        )
    assert contract["extras"]["reaction_value_policy"] == 1


def test_contract_reaction_az_uses_az_flag():
    """alphazero_tree: reaction по AZ_REACTION_VALUE_POLICY (другие флаги не влияют)."""
    with patch.dict(
        os.environ,
        {"AZ_REACTION_VALUE_POLICY": "0", "GMZ_REACTION_VALUE_POLICY": "1"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "alphazero_tree"},
        )
    assert contract["extras"]["reaction_value_policy"] == 0


def test_contract_reaction_gumbel_az_rides_az_flag():
    """gumbel_az едет на AZ-инфре → reaction по AZ_REACTION_VALUE_POLICY."""
    with patch.dict(
        os.environ,
        {"AZ_REACTION_VALUE_POLICY": "1", "GMZ_REACTION_VALUE_POLICY": "0"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "gumbel_az"},
        )
    assert contract["extras"]["reaction_value_policy"] == 1


def test_contract_reaction_unknown_algo_falls_back_to_az():
    """Нет/неизвестный train_algo → прежнее поведение (AZ-флаг), back-compat."""
    with patch.dict(os.environ, {"AZ_REACTION_VALUE_POLICY": "1"}, clear=False):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
        )
    assert contract["extras"]["reaction_value_policy"] == 1


# --- Регрессия: контракт gumbel_az должен совпадать с runtime-резолвом ---
# Runtime резолвит reaction по приоритету GAZ_* → AZ_* → секция (_az_family_env).
# Раньше контракт читал только AZ_*: при GAZ_=1, AZ_=0 контракт писал 0, а сеть
# обучалась с reaction=1 → eval молча отключал умные реакции у GAZ-агента.


def test_contract_reaction_gumbel_az_prefers_gaz_flag_over_az():
    """gumbel_az: GAZ_REACTION_VALUE_POLICY приоритетнее AZ_ (как в runtime)."""
    with patch.dict(
        os.environ,
        {"GAZ_REACTION_VALUE_POLICY": "1", "AZ_REACTION_VALUE_POLICY": "0"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "gumbel_az"},
        )
    assert contract["extras"]["reaction_value_policy"] == 1


def test_contract_reaction_gumbel_az_gaz_off_beats_az_on():
    """gumbel_az: явный GAZ_=0 побеждает AZ_=1 (GAZ_ приоритетнее)."""
    with patch.dict(
        os.environ,
        {"GAZ_REACTION_VALUE_POLICY": "0", "AZ_REACTION_VALUE_POLICY": "1"},
        clear=False,
    ):
        contract = make_env_contract(
            n_observations=41, n_actions=[5, 2], mission_name="only_war",
            extras={"train_algo": "gumbel_az"},
        )
    assert contract["extras"]["reaction_value_policy"] == 0
