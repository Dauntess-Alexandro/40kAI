"""DQN distributed: разбиение эпизодов ПК1/ПК2 и квот по воркерам."""

from core.models.dqn_dist import resolve_dqn_dist_episode_split, split_count_among_workers


def test_resolve_episodes_70_30_of_400():
    local, remote = resolve_dqn_dist_episode_split(total_episodes=400, local_fraction=0.7)
    assert local == 280
    assert remote == 120


def test_split_episodes_among_8_workers_pc1():
    plan = split_count_among_workers(total=280, num_workers=8)
    assert sum(plan) == 280
    assert plan == [35] * 8


def test_split_episodes_among_8_workers_pc2():
    plan = split_count_among_workers(total=120, num_workers=8)
    assert sum(plan) == 120
    assert plan == [15] * 8
