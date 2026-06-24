import types

from core.telemetry import stratagem_trace as st


def _env():
    return types.SimpleNamespace(
        stratagem_used=[
            ("model", "overwatch", 1, "shooting", 0),
            ("model", "go_to_ground", 1, "shooting", 1),
        ],
        _cmd_reroll_fired=0,
    )


def test_emit_disabled_without_verbose(monkeypatch):
    for k in ("VERBOSE_LOGS", "TRAIN_STRATAGEM_TRACE", "MANUAL_DICE"):
        monkeypatch.delenv(k, raising=False)
    assert st.emit_episode_stratagem_log(_env(), ep_label=1, tag="GMZ") is None


def test_emit_logs_when_verbose(monkeypatch):
    monkeypatch.setenv("VERBOSE_LOGS", "1")
    monkeypatch.delenv("TRAIN_STRATAGEM_TRACE", raising=False)
    monkeypatch.delenv("MANUAL_DICE", raising=False)
    captured = []
    monkeypatch.setattr(st, "append_train_stratagem_log", lambda line: captured.append(line))
    line = st.emit_episode_stratagem_log(_env(), ep_label=5, tag="GMZ")
    assert line is not None
    assert "[GMZ][STRATAGEM_SUMMARY]" in line
    assert "ep=5" in line and "overwatch" in line and "go_to_ground" in line
    assert captured == [line]


def test_emit_empty_env_no_log(monkeypatch):
    monkeypatch.setenv("VERBOSE_LOGS", "1")
    captured = []
    monkeypatch.setattr(st, "append_train_stratagem_log", lambda line: captured.append(line))
    empty = types.SimpleNamespace(stratagem_used=[], _cmd_reroll_fired=0)
    assert st.emit_episode_stratagem_log(empty, ep_label=1, tag="SMZ") is None
    assert captured == []
