from core.engine.agent_registry import compatible_contracts, make_env_contract


def test_contract_action_signature_changed():
    old = make_env_contract(n_observations=10, n_actions=[5, 2, 5, 2], mission_name="only_war")
    new = make_env_contract(
        n_observations=10,
        n_actions=[5, 2, 5, 2, 4, 4, 6, 6, 6, 6],
        mission_name="only_war",
    )
    ok, reason = compatible_contracts(old, new)
    assert ok is False
    assert reason == "action_space_signature mismatch"
