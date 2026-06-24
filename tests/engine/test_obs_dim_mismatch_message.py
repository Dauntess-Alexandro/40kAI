from core.engine.phases.obs_features import obs_dim_mismatch_message


def test_no_message_when_match():
    assert obs_dim_mismatch_message(41, 41) is None
    assert obs_dim_mismatch_message(17, 17) is None


def test_message_on_mismatch_contains_both_dims_and_hint():
    msg = obs_dim_mismatch_message(17, 41)
    assert msg is not None
    assert "17" in msg and "41" in msg
    assert "search_cfg" in msg
