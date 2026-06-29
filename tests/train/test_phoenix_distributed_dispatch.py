from __future__ import annotations


def _clear_phoenix_env(monkeypatch):
    for key in (
        "PHOENIX_NUM_ACTORS",
        "NUM_ACTORS",
        "PHOENIX_DISTRIBUTED_ACTORS",
    ):
        monkeypatch.delenv(key, raising=False)


def test_phoenix_num_actors_one_uses_single_process_path(monkeypatch):
    import train

    _clear_phoenix_env(monkeypatch)
    calls: list[str] = []
    logs: list[str] = []
    monkeypatch.setattr(train, "data", {"phoenix": {"num_actors": 1, "distributed_actors_enabled": 0}})
    monkeypatch.setattr(train, "append_agent_log", logs.append)
    monkeypatch.setattr(train, "_main_actor_learner_phoenix_single", lambda **_kwargs: calls.append("single"))
    monkeypatch.setattr(train, "_main_actor_learner_phoenix_distributed", lambda **_kwargs: calls.append("distributed"))

    train._main_actor_learner_phoenix(
        roster_config={},
        totLifeT=1,
        clip_reward_enabled=False,
        clip_reward_min=0.0,
        clip_reward_max=0.0,
    )

    assert calls == ["single"]
    assert any("mode=single_process" in line for line in logs)


def test_phoenix_num_actors_two_uses_actor_learner_path(monkeypatch):
    import train

    _clear_phoenix_env(monkeypatch)
    calls: list[object] = []
    monkeypatch.setattr(train, "data", {"phoenix": {"num_actors": 2, "distributed_actors_enabled": 0}})
    monkeypatch.setattr(train, "append_agent_log", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(train, "_main_actor_learner_phoenix_single", lambda **_kwargs: calls.append("single"))
    monkeypatch.setattr(
        train,
        "_main_actor_learner_phoenix_distributed",
        lambda **kwargs: calls.append(kwargs["cfg"]),
    )

    train._main_actor_learner_phoenix(
        roster_config={},
        totLifeT=1,
        clip_reward_enabled=False,
        clip_reward_min=0.0,
        clip_reward_max=0.0,
    )

    assert len(calls) == 1
    assert getattr(calls[0], "num_actors") == 2
