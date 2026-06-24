from core.engine.phases.obs_features import (
    matmul_obs_mismatch_hint,
    obs_dim_mismatch_message,
)


def test_no_message_when_match():
    assert obs_dim_mismatch_message(41, 41) is None
    assert obs_dim_mismatch_message(17, 17) is None


def test_message_on_mismatch_contains_both_dims_and_hint():
    msg = obs_dim_mismatch_message(17, 41)
    assert msg is not None
    assert "17" in msg and "41" in msg
    assert "search_cfg" in msg


def test_matmul_hint_parses_torch_error():
    msg = matmul_obs_mismatch_hint(
        "mat1 and mat2 shapes cannot be multiplied (1x41 and 17x256)"
    )
    assert msg is not None
    assert "17" in msg and "41" in msg and "search_cfg" in msg


def test_matmul_hint_none_on_unrelated_error():
    assert matmul_obs_mismatch_hint("some other runtime error") is None
