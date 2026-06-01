"""Integration test: AZ remote inference server over localhost ZMQ."""

from __future__ import annotations

import threading
import time

import numpy as np
import torch
import pytest

from core.models.alphazero_model import make_alphazero_net
from core.models.az_inference_transport import (
    RemoteAZInferenceTransport,
    az_remote_health_check,
)
from core.models.az_inference_client import RemoteEvaluator

N_OBS = 24
ACTION_SIZES = [5, 3]
PORT = 5599  # отдельный от дефолтов, чтобы не конфликтовать


def _free_port_server(tmp_path):
    """Запускает AZRemoteInferenceServer на CPU в фоновом потоке."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
    from az_remote_inference_server import AZRemoteInferenceServer

    # Сохраняем init-веса во временный файл
    net = make_alphazero_net(N_OBS, ACTION_SIZES, hidden_size=32, num_layers=1)
    net.eval()
    weights_path = tmp_path / "az_init.pth"
    torch.save({"policy_version": 7, "state_dict": net.state_dict()}, weights_path)

    cfg = {
        "obs_dim": N_OBS,
        "action_sizes": ACTION_SIZES,
        "hidden_size": 32,
        "num_layers": 1,
        "n_value_ensemble": 1,
    }
    server = AZRemoteInferenceServer(
        host="127.0.0.1",
        port=PORT,
        device="cpu",
        weights_path=str(weights_path),
        init_weights_path=str(weights_path),
        net_cfg=cfg,
        sync_interval=10.0,
        batch_size=8,
        batch_interval_ms=10.0,
        auth_token="",
        log_path=None,
    )
    return server, net


@pytest.fixture
def running_server(tmp_path):
    server, net = _free_port_server(tmp_path)
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    time.sleep(0.4)  # дать ROUTER забиндиться
    yield server, net
    server.stop()
    t.join(timeout=2.0)


class TestRemoteServer:
    def test_health_check(self, running_server):
        _server, _net = running_server
        hc = az_remote_health_check(host="127.0.0.1", port=PORT, timeout=3.0)
        assert hc["status"] == "ok"
        assert hc["policy_version"] == 7
        assert hc["gpu_name"] == "cpu"

    def test_infer_one_matches_net(self, running_server):
        _server, net = running_server
        ev = RemoteEvaluator(
            worker_id=0,
            transport=RemoteAZInferenceTransport(worker_id=0, host="127.0.0.1", port=PORT),
            timeout=5.0,
        )
        obs = np.random.randn(N_OBS).astype(np.float32)
        masks = [np.ones(a, dtype=bool) for a in ACTION_SIZES]
        priors, value = ev.evaluate_one(obs, masks)

        obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool).unsqueeze(0) for m in masks]
        with torch.no_grad():
            ref_p, ref_v = net.infer(obs_t, masks_by_head=masks_t)

        assert len(priors) == len(ACTION_SIZES)
        for h in range(len(ACTION_SIZES)):
            np.testing.assert_allclose(priors[h], ref_p[h].squeeze(0).numpy(), atol=1e-4)
        assert abs(value - float(ref_v.item())) < 1e-4
        ev.close()

    def test_evaluate_batch_leaves(self, running_server):
        _server, net = running_server
        ev = RemoteEvaluator(
            worker_id=1,
            transport=RemoteAZInferenceTransport(worker_id=1, host="127.0.0.1", port=PORT),
            timeout=5.0,
        )
        masks = [np.ones(a, dtype=bool) for a in ACTION_SIZES]
        leaves = [
            {"obs": np.random.randn(N_OBS).astype(np.float32), "legal_masks": masks}
            for _ in range(4)
        ]
        values = ev.evaluate_batch(leaves)
        assert len(values) == 4

        for i, leaf in enumerate(leaves):
            obs_t = torch.tensor(leaf["obs"], dtype=torch.float32).unsqueeze(0)
            masks_t = [torch.as_tensor(m, dtype=torch.bool).unsqueeze(0) for m in masks]
            with torch.no_grad():
                _, ref_v = net.infer(obs_t, masks_by_head=masks_t)
            assert abs(values[i] - float(ref_v.item())) < 1e-4, f"leaf {i}"
        ev.close()

    def test_protocol_version_mismatch(self, running_server):
        """Запрос с неверной версией протокола → error."""
        import zmq
        from core.models.az_inference_protocol import encode_message, decode_message
        ctx = zmq.Context.instance()
        sock = ctx.socket(zmq.DEALER)
        sock.setsockopt(zmq.IDENTITY, b"badver")
        sock.setsockopt(zmq.RCVTIMEO, 3000)
        sock.connect(f"tcp://127.0.0.1:{PORT}")
        sock.send(encode_message({"kind": "health_check", "protocol_version": 999}))
        resp = decode_message(sock.recv())
        assert resp["kind"] == "error"
        assert "protocol_version" in resp["message"]
        sock.close(linger=0)
