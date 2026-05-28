"""Integration tests for remote GMZ inference server (localhost, CPU)."""

from __future__ import annotations

import json
import tempfile
import threading
import time
from pathlib import Path

import numpy as np
import pytest
import torch

pytest.importorskip("zmq")

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gmz_inference_transport import remote_health_check
from core.models.utils import normalize_state_dict
from tools.gmz_remote_inference_server import GMZRemoteInferenceServer


def _write_dummy_weights(path: Path, obs_dim: int = 4, action_sizes: list[int] | None = None) -> None:
    action_sizes = action_sizes or [3, 3]
    net = GumbelMuZeroNet(
        obs_dim=obs_dim,
        action_sizes=action_sizes,
        latent_dim=32,
        hidden_dim=32,
        num_layers=1,
        action_embed_dim=16,
    )
    torch.save(
        {"state_dict": normalize_state_dict(net.state_dict()), "policy_version": 1},
        str(path),
    )


def _search_cfg(obs_dim: int = 4, action_sizes: list[int] | None = None) -> dict:
    action_sizes = action_sizes or [3, 3]
    return {
        "obs_dim": obs_dim,
        "action_sizes": action_sizes,
        "latent_dim": 32,
        "hidden_dim": 32,
        "num_layers": 1,
        "action_embed_dim": 16,
        "num_simulations": 2,
        "root_top_k": 2,
        "batch_recurrent": 0,
        "tree_reuse": 0,
    }


def test_remote_server_healthcheck_localhost():
    with tempfile.TemporaryDirectory() as tmp:
        weights = Path(tmp) / "w.pth"
        _write_dummy_weights(weights)
        port = 15555
        server = GMZRemoteInferenceServer(
            host="127.0.0.1",
            port=port,
            device="cpu",
            weights_path=str(weights),
            init_weights_path=str(weights),
            search_cfg=_search_cfg(),
            sync_interval=60.0,
            batch_size=2,
            batch_interval_ms=5.0,
            compile_mode=False,
            auth_token="",
            log_path=None,
        )
        th = threading.Thread(target=server.run, daemon=True)
        th.start()
        time.sleep(0.3)
        try:
            resp = remote_health_check(host="127.0.0.1", port=port, timeout=3.0)
            assert resp.get("status") == "ok"
            assert int(resp.get("protocol_version", 0)) == 1
        finally:
            server.stop()


def test_remote_server_infer_localhost():
    from core.models.gmz_inference_client import GMZInferenceClient
    from core.models.gmz_inference_transport import RemoteInferenceTransport

    with tempfile.TemporaryDirectory() as tmp:
        weights = Path(tmp) / "w.pth"
        _write_dummy_weights(weights)
        cfg_path = Path(tmp) / "search.json"
        cfg_path.write_text(json.dumps(_search_cfg()), encoding="utf-8")
        port = 15556
        server = GMZRemoteInferenceServer(
            host="127.0.0.1",
            port=port,
            device="cpu",
            weights_path=str(weights),
            init_weights_path=str(weights),
            search_cfg=_search_cfg(),
            sync_interval=60.0,
            batch_size=2,
            batch_interval_ms=5.0,
            compile_mode=False,
            auth_token="tok",
            log_path=None,
        )
        th = threading.Thread(target=server.run, daemon=True)
        th.start()
        time.sleep(0.3)
        try:
            transport = RemoteInferenceTransport(
                worker_id=0,
                host="127.0.0.1",
                port=port,
                auth_token="tok",
            )
            client = GMZInferenceClient(0, transport=transport, timeout=5.0, auth_token="tok")
            resp = client.infer(
                obs=np.zeros(4, dtype=np.float32),
                legal_masks_by_head=[np.ones(3, dtype=bool), np.ones(3, dtype=bool)],
                step_in_episode=0,
                episode_id=0,
                is_new_episode=True,
            )
            assert "selected_actions" in resp
            client.close()
        finally:
            server.stop()
