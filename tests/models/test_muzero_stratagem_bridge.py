import types

import pytest

from core.models.muzero_stratagem_bridge import (
    install_muzero_reaction_policy,
    maybe_install_muzero_reactions,
    muzero_reaction_value_policy_enabled,
)


class _FakeNet:
    # MuZero-подобная сеть: есть infer, НЕТ infer_with_value
    def parameters(self):
        import torch
        yield torch.zeros(1)

    def infer(self, obs, masks_by_head=None):
        return None, 0.0


def _fake_env():
    env = types.SimpleNamespace()
    env.unwrapped = env  # unwrap_env вернёт его же
    return env


def test_enabled_default_on(monkeypatch):
    monkeypatch.delenv("GMZ_REACTION_VALUE_POLICY", raising=False)
    assert muzero_reaction_value_policy_enabled("GMZ_REACTION_VALUE_POLICY") is True


def test_enabled_off(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    assert muzero_reaction_value_policy_enabled("GMZ_REACTION_VALUE_POLICY") is False


def test_install_sets_policy_both_sides():
    env = _fake_env()
    net = _FakeNet()
    ok = install_muzero_reaction_policy(env, net, log_tag="GMZ")
    assert ok is True
    assert callable(env.reaction_policy)
    assert env._reaction_net_by_side == {"model": net, "enemy": net}


def test_install_net_none_is_noop():
    env = _fake_env()
    ok = install_muzero_reaction_policy(env, None, log_tag="GMZ")
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None


def test_maybe_install_local_search(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _fake_env()
    search = types.SimpleNamespace(net=_FakeNet())
    ok = maybe_install_muzero_reactions(
        env, search=search, inference_fn=None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is True
    assert callable(env.reaction_policy)


def test_maybe_install_remote_skips(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "1")
    env = _fake_env()
    ok = maybe_install_muzero_reactions(
        env, search=None, inference_fn=lambda *a, **k: None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None


def test_maybe_install_flag_off(monkeypatch):
    monkeypatch.setenv("GMZ_REACTION_VALUE_POLICY", "0")
    env = _fake_env()
    search = types.SimpleNamespace(net=_FakeNet())
    ok = maybe_install_muzero_reactions(
        env, search=search, inference_fn=None,
        flag_env="GMZ_REACTION_VALUE_POLICY", log_tag="GMZ",
    )
    assert ok is False
    assert getattr(env, "reaction_policy", None) is None
