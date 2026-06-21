from __future__ import annotations

from pathlib import Path


def test_gui_updates_per_step_feeds_dqn_actor_learner_updates_per_batch():
    src = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
    assert 'env.insert("UPDATES_PER_BATCH"' in src
    assert 'hp.get("updates_per_step"' in src


def test_train_reads_legacy_updates_per_step_as_updates_per_batch_default():
    src = Path("train.py").read_text(encoding="utf-8")
    assert '_DQN_CFG.get("updates_per_batch")' in src
    assert '_DQN_CFG.get("updates_per_step")' in src
    assert 'data.get("updates_per_step")' in src
