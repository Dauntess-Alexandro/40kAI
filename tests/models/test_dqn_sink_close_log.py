"""DQN dist: итоговый лог RemoteRolloutSink — batch, не rollout."""

import pytest

from core.models.az_rollout_sink import RemoteRolloutSink


@pytest.fixture
def remote_sink(monkeypatch):
    pytest.importorskip("zmq")

    class _FakeSock:
        def setsockopt(self, *_args, **_kwargs):
            return None

        def connect(self, *_args, **_kwargs):
            return None

        def close(self, *_args, **_kwargs):
            return None

        def send(self, *_args, **_kwargs):
            return None

    class _FakeCtx:
        def socket(self, *_args, **_kwargs):
            return _FakeSock()

    import zmq

    monkeypatch.setattr(zmq.Context, "instance", classmethod(lambda cls: _FakeCtx()))
    return RemoteRolloutSink(
        host="127.0.0.1",
        port=5602,
        worker_id=100,
        env_contract_hash="H1",
    )


def test_dqn_sink_close_reports_batch_not_rollout(remote_sink, capsys):
    batch = [([0.0], [0, 0, 0], 1.0, [1.0], False, 1)] * 3
    remote_sink.put("batch", batch)
    remote_sink.put("ep", {"actor_idx": 100, "ep_reward": 0.5})
    remote_sink.close()
    out = capsys.readouterr().out
    assert "[DQN][DIST][SINK]" in out
    assert "sent_batch=1" in out
    assert "sent_transitions=3" in out
    assert "sent_ep=1" in out
    assert "sent_rollout" not in out
    assert "failed=0" in out


def test_dqn_sink_warns_when_ep_without_batch(remote_sink, capsys):
    remote_sink.put("ep", {"actor_idx": 100})
    remote_sink.close()
    out = capsys.readouterr().out
    assert "sent_batch=0" in out
    assert "sent_ep=1" in out
    assert "WARN: ep без batch" in out
