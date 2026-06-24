# tests/models/test_muzero_selfplay_reaction_wiring.py
import types

import pytest

import core.models.gumbel_muzero_selfplay as gmz_sp
import core.models.sampled_muzero_selfplay as smz_sp


class _StopReset(Exception):
    pass


def _fake_env():
    # env, падающий на reset, чтобы остановиться сразу после install-пойнта
    env = types.SimpleNamespace()
    env.unwrapped = env
    env.model = []
    env.enemy = []
    env.first_turn_side = "model"

    def _reset(*a, **k):
        raise _StopReset()

    env.reset = _reset
    return env


def test_gmz_selfplay_calls_install(monkeypatch):
    calls = {}

    def _fake_maybe(env, *, search, inference_fn, flag_env, log_tag, log_fn=None):
        calls["flag_env"] = flag_env
        calls["log_tag"] = log_tag
        return True

    monkeypatch.setattr(gmz_sp, "maybe_install_muzero_reactions", _fake_maybe)
    with pytest.raises(_StopReset):
        gmz_sp.play_episode_with_gumbel_muzero(
            env=_fake_env(), search=object(), len_model=1
        )
    assert calls["flag_env"] == "GMZ_REACTION_VALUE_POLICY"
    assert calls["log_tag"] == "GMZ"


def test_smz_wrapper_forwards_smz_tag(monkeypatch):
    calls = {}

    def _fake_maybe(env, *, search, inference_fn, flag_env, log_tag, log_fn=None):
        calls["flag_env"] = flag_env
        calls["log_tag"] = log_tag
        return True

    monkeypatch.setattr(gmz_sp, "maybe_install_muzero_reactions", _fake_maybe)
    with pytest.raises(_StopReset):
        smz_sp.play_episode_with_sampled_muzero(
            env=_fake_env(), search=object(), len_model=1
        )
    assert calls["flag_env"] == "SMZ_REACTION_VALUE_POLICY"
    assert calls["log_tag"] == "SMZ"
