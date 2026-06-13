from core.models.alphazero_ids import (
    VALID_TRAIN_ALGOS,
    gaz_section_for,
    is_alphazero_net_algo,
    is_az_algo,
    is_gumbel_az_algo,
)


def test_gumbel_az_in_valid_train_algos():
    assert "gumbel_az" in VALID_TRAIN_ALGOS


def test_is_gumbel_az_algo():
    assert is_gumbel_az_algo("gumbel_az")
    assert not is_gumbel_az_algo("alphazero_tree")
    assert not is_gumbel_az_algo("")


def test_is_alphazero_net_family():
    # gumbel_az шарит AZ-сеть и формат чекпойнта
    assert is_alphazero_net_algo("alphazero_tree")
    assert is_alphazero_net_algo("alphazero_proxy")
    assert is_alphazero_net_algo("gumbel_az")
    assert not is_alphazero_net_algo("dqn")
    assert not is_alphazero_net_algo("gumbel_muzero")


def test_gumbel_az_is_not_az_puct_algo():
    # is_az_algo остаётся строго для PUCT tree/proxy
    assert not is_az_algo("gumbel_az")


def test_gaz_section_for():
    assert gaz_section_for("gumbel_az") == "gumbel_az"
