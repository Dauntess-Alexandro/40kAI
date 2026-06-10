from __future__ import annotations

import types

from core.models.dqn_dist import (
    apply_dqn_arch_overrides,
    read_dqn_dist_train_context,
    write_dqn_dist_train_context,
)


def test_train_context_roundtrip_carries_arch_params(tmp_path, monkeypatch):
    """ПК1 кладёт арх-параметры сети в контекст, ПК2 их читает (без рассинхрона формы)."""
    sync = tmp_path / "actor_sync"
    sync.mkdir()
    monkeypatch.setenv("DQN_DIST_STOP_FLAG_PATH", str(sync / "az_dist_stop.flag"))

    write_dqn_dist_train_context(
        {"ensemble_size": 3, "hidden_size": 256, "num_layers": 2, "n_observations": 12}
    )
    ctx = read_dqn_dist_train_context()
    assert ctx["ensemble_size"] == 3
    assert ctx["hidden_size"] == 256
    assert ctx["num_layers"] == 2


def test_apply_dqn_arch_overrides_sets_train_globals():
    """Helper переносит арх-параметры из контекста на глобалы train (форма сети ПК2=ПК1)."""
    fake_train = types.SimpleNamespace(
        DQN_ENSEMBLE_SIZE=1, DQN_HIDDEN_SIZE=128, DQN_NUM_LAYERS=1
    )
    applied = apply_dqn_arch_overrides(
        fake_train, {"ensemble_size": 3, "hidden_size": 256, "num_layers": 2}
    )
    assert fake_train.DQN_ENSEMBLE_SIZE == 3
    assert fake_train.DQN_HIDDEN_SIZE == 256
    assert fake_train.DQN_NUM_LAYERS == 2
    assert applied == {"DQN_ENSEMBLE_SIZE": 3, "DQN_HIDDEN_SIZE": 256, "DQN_NUM_LAYERS": 2}


def test_apply_dqn_arch_overrides_ignores_missing_and_bad_values():
    """Отсутствующие/битые значения не трогают глобалы (бэк-компат со старым ПК1)."""
    fake_train = types.SimpleNamespace(
        DQN_ENSEMBLE_SIZE=1, DQN_HIDDEN_SIZE=128, DQN_NUM_LAYERS=1
    )
    applied = apply_dqn_arch_overrides(fake_train, {"ensemble_size": "oops"})
    assert fake_train.DQN_ENSEMBLE_SIZE == 1
    assert applied == {}
