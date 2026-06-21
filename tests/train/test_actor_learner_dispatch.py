from __future__ import annotations


def _run_main_dispatch_with_removed_legacy_flag(monkeypatch, capsys, *, algo: str, entrypoint: str):
    import train

    calls = []

    def fake_entrypoint(**kwargs):
        calls.append(kwargs)

    monkeypatch.setenv("PRO_ACTOR_LEARNER", "0")
    monkeypatch.delenv("TRAIN_EPISODES_OVERRIDE", raising=False)
    monkeypatch.setattr(train, "TRAIN_ALGO", algo)
    monkeypatch.setattr(train, "TRAIN_LOG_TO_FILE", False)
    monkeypatch.setattr(train, "TRAIN_LOG_TO_CONSOLE", True)
    monkeypatch.setattr(train, "set_active_io", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(train, "parse_clip_reward_config", lambda _raw: (False, 0.0, 0.0))
    monkeypatch.setattr(train, "_load_roster_config", lambda: {"totLifeT": 3})
    monkeypatch.setattr(train, entrypoint, fake_entrypoint)

    train.main()

    out = capsys.readouterr().out
    assert "PRO_ACTOR_LEARNER=0" in out
    assert "actor-learner" in out
    assert len(calls) == 1
    assert calls[0]["totLifeT"] == 3
    assert calls[0]["roster_config"] == {"totLifeT": 3}


def test_removed_legacy_flag_dispatches_dqn_actor_learner(monkeypatch, capsys):
    _run_main_dispatch_with_removed_legacy_flag(
        monkeypatch,
        capsys,
        algo="dqn",
        entrypoint="_main_actor_learner",
    )


def test_removed_legacy_flag_dispatches_ppo_actor_learner(monkeypatch, capsys):
    _run_main_dispatch_with_removed_legacy_flag(
        monkeypatch,
        capsys,
        algo="ppo",
        entrypoint="_main_actor_learner_ppo",
    )
