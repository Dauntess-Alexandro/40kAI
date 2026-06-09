"""DQN dist: единый env_contract_hash ПК1↔ПК2 и ожидание воркеров."""

import pytest

from core.engine.agent_registry import make_env_contract
from core.models.dqn_dist import (
    dqn_dist_env_contract_extras,
    resolve_dqn_dist_contract_hash,
    wait_dqn_dist_remote_workers,
)


def test_dqn_dist_extras_match_pc1_pc2_style():
    extras_pc1 = dqn_dist_env_contract_extras(num_local_actors=8)
    extras_pc2 = dqn_dist_env_contract_extras(num_local_actors=8)
    assert extras_pc1 == extras_pc2 == {"actor_learner": 1, "num_actors": 8}


def test_resolve_contract_hash_prefers_context():
    ctx = {"env_contract_hash": "from_pc1_ctx"}
    got = resolve_dqn_dist_contract_hash(
        ctx=ctx,
        n_observations=17,
        n_actions=[5, 2, 2, 2, 5, 2, 24, 24],
        mission_name="only_war",
        ruleset_version="only_war_v1",
        num_local_actors=8,
    )
    assert got == "from_pc1_ctx"


def test_pc1_pc2_recomputed_hash_matches():
    n_act = [5, 2, 2, 2, 5, 2, 24, 24]
    extras = dqn_dist_env_contract_extras(num_local_actors=8)
    ec1 = make_env_contract(
        n_observations=17,
        n_actions=n_act,
        mission_name="only_war",
        ruleset_version="only_war_v1",
        extras=extras,
    )
    ec2 = make_env_contract(
        n_observations=17,
        n_actions=n_act,
        mission_name="only_war",
        ruleset_version="only_war_v1",
        extras=extras,
    )
    assert ec1["contract_hash"] == ec2["contract_hash"]


class _FakeReceiver:
    def __init__(self, counts: list[int]) -> None:
        self._counts = list(counts)
        self._i = 0

    def remote_worker_count(self) -> int:
        if self._i < len(self._counts):
            v = int(self._counts[self._i])
            self._i += 1
            return v
        return int(self._counts[-1])


def test_wait_dqn_dist_remote_workers_succeeds():
    rcv = _FakeReceiver([0, 1, 3, 8])
    wait_dqn_dist_remote_workers(rcv, min_workers=8, timeout_sec=5.0, poll_sec=0.01)


def test_wait_dqn_dist_remote_workers_timeout():
    rcv = _FakeReceiver([0, 1, 2])
    with pytest.raises(RuntimeError, match="ПК2 не подключился"):
        wait_dqn_dist_remote_workers(rcv, min_workers=8, timeout_sec=0.05, poll_sec=0.01)
