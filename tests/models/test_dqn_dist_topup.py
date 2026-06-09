# tests/models/test_dqn_dist_topup.py
"""DQN dist: добор ep на ПК1, когда учёт отстаёт от квот воркеров."""
from core.models.dqn_dist import DQN_DIST_TOPUP_ACTOR_IDX, compute_dqn_dist_topup_episodes


def test_topup_actor_idx_reserved():
    assert DQN_DIST_TOPUP_ACTOR_IDX >= 9000


def test_topup_zero_when_remote_alive():
    assert (
        compute_dqn_dist_topup_episodes(
            episodes_finished=100,
            total_episodes=800,
            local_actors_done=8,
            num_local_actors=8,
            remote_alive=2,
            topup_process_alive=False,
        )
        == 0
    )


def test_topup_zero_while_local_pending():
    assert (
        compute_dqn_dist_topup_episodes(
            episodes_finished=100,
            total_episodes=800,
            local_actors_done=3,
            num_local_actors=8,
            remote_alive=0,
            topup_process_alive=False,
        )
        == 0
    )


def test_topup_zero_while_topup_running():
    assert (
        compute_dqn_dist_topup_episodes(
            episodes_finished=675,
            total_episodes=800,
            local_actors_done=8,
            num_local_actors=8,
            remote_alive=0,
            topup_process_alive=True,
        )
        == 0
    )


def test_topup_shortfall_when_all_idle():
    assert (
        compute_dqn_dist_topup_episodes(
            episodes_finished=675,
            total_episodes=800,
            local_actors_done=8,
            num_local_actors=8,
            remote_alive=0,
            topup_process_alive=False,
        )
        == 125
    )


def test_topup_zero_when_target_reached():
    assert (
        compute_dqn_dist_topup_episodes(
            episodes_finished=800,
            total_episodes=800,
            local_actors_done=8,
            num_local_actors=8,
            remote_alive=0,
            topup_process_alive=False,
        )
        == 0
    )
