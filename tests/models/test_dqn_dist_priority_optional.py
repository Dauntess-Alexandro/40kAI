# tests/models/test_dqn_dist_priority_optional.py
"""DQN dist: RemoteDataQ.put((kind,payload)) → sink.put(kind,payload); priority опционален."""
from core.models.dqn_dist import RemoteDataQ


class _SpySink:
    def __init__(self):
        self.calls = []

    def put(self, kind, payload):
        self.calls.append((kind, payload))

    def close(self):
        self.calls.append(("__closed__", None))


def test_remote_dataq_forwards_batch_tuple():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    batch = [("s", [1], 0.0, None, True, 1)]
    q.put(("batch", batch))
    assert sink.calls == [("batch", batch)]


def test_remote_dataq_forwards_ep_and_done():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    q.put(("ep", {"result": "win"}))
    q.put(("done", 3))
    assert sink.calls[0] == ("ep", {"result": "win"})
    assert sink.calls[1] == ("done", 3)


def test_remote_dataq_close_closes_sink():
    sink = _SpySink()
    q = RemoteDataQ(sink)
    q.close()
    assert ("__closed__", None) in sink.calls
