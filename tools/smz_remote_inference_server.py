#!/usr/bin/env python
"""Standalone remote Sampled MuZero inference server (ZMQ ROUTER + GPU batch infer)."""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import threading
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

import torch
import zmq

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.models.gmz_inference_protocol import (  # noqa: E402
    PROTOCOL_VERSION,
    decode_message,
    encode_message,
)
from core.models.sampled_muzero_model import make_sampled_muzero_net  # noqa: E402
from core.models.sampled_muzero_search import SampledMuZeroSearchConfig  # noqa: E402
from core.models.smz_inference_server import SMZInferenceServer  # noqa: E402
from core.models.utils import normalize_state_dict  # noqa: E402


def _log(msg: str, log_path: Path | None) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    if log_path is None:
        return
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


class _PendingRequest:
    __slots__ = ("identity", "request")

    def __init__(self, identity: bytes, request: dict[str, Any]) -> None:
        self.identity = identity
        self.request = request


class SMZRemoteInferenceServer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        device: str,
        weights_path: str,
        init_weights_path: str | None,
        search_cfg: dict[str, Any],
        sync_interval: float,
        batch_size: int,
        batch_interval_ms: float,
        compile_mode: bool,
        auth_token: str,
        log_path: Path | None,
        max_queue_depth: int = 64,
    ) -> None:
        self.host = str(host)
        self.port = int(port)
        self.weights_path = str(weights_path)
        self.sync_interval = float(sync_interval)
        self.batch_size = max(1, int(batch_size))
        self.batch_interval_s = float(batch_interval_ms) / 1000.0
        self.auth_token = str(auth_token or "")
        self.log_path = log_path
        self.max_queue_depth = max(8, int(max_queue_depth))
        self._running = True
        self._started_at = time.time()
        self._pending: deque[_PendingRequest] = deque()
        self._pending_lock = threading.Lock()
        self._queue_depth = 0

        if torch.cuda.is_available() and str(device).startswith("cuda"):
            idx = 0
            if ":" in str(device):
                idx = int(str(device).split(":")[-1])
            torch.cuda.set_device(idx)
            torch_device = torch.device(device)
        else:
            torch_device = torch.device("cpu")

        latent_dim = int(search_cfg.get("latent_dim", 256))
        hidden_dim = int(search_cfg.get("hidden_dim", 256))
        num_layers = int(search_cfg.get("num_layers", 2))
        action_embed_dim = int(search_cfg.get("action_embed_dim", 64))
        obs_dim = int(search_cfg.get("obs_dim", 0))
        action_sizes = [int(x) for x in search_cfg.get("action_sizes", [])]
        if obs_dim <= 0 or not action_sizes:
            raise ValueError(
                "smz_inference_server: search_cfg пуст (obs_dim<=0 или action_sizes=[]). "
                "Что делать: сгенерируйте search-cfg на ПК1 через tools/write_smz_remote_search_cfg.bat "
                "и положите smz_remote_search_cfg.json рядом с весами (SMB/actor_sync)."
            )

        net = make_sampled_muzero_net(
            obs_dim=obs_dim,
            action_sizes=action_sizes,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            action_embed_dim=action_embed_dim,
        ).to(torch_device)

        def _log_mismatch(load_result) -> None:
            missing = len(getattr(load_result, "missing_keys", []) or [])
            unexpected = len(getattr(load_result, "unexpected_keys", []) or [])
            if missing or unexpected:
                _log(
                    f"[SMZ][REMOTE_IS] weight load: missing={missing} unexpected={unexpected}",
                    log_path,
                )

        weight_src = init_weights_path if init_weights_path and os.path.isfile(init_weights_path) else None
        if weight_src:
            payload = torch.load(weight_src, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else payload
            _log_mismatch(net.load_state_dict(normalize_state_dict(sd), strict=False))
            _log(f"[SMZ][REMOTE_IS] loaded init weights from {weight_src}", log_path)
        elif os.path.isfile(self.weights_path):
            payload = torch.load(self.weights_path, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else payload
            _log_mismatch(net.load_state_dict(normalize_state_dict(sd), strict=False))
            _log(f"[SMZ][REMOTE_IS] loaded weights from {self.weights_path}", log_path)
        else:
            raise FileNotFoundError(
                f"weights not found: {self.weights_path!r}; pass --init-weights for first start"
            )
        net.eval()

        search_config = SampledMuZeroSearchConfig(
            num_samples=int(search_cfg.get("num_samples", 24)),
            discount=float(search_cfg.get("discount", 0.997)),
            temperature=float(search_cfg.get("temperature", 0.15)),
            sample_temperature=float(search_cfg.get("sample_temperature", 1.0)),
            prior_weight=float(search_cfg.get("prior_weight", 0.0)),
            dedup=bool(int(search_cfg.get("dedup", 1))),
        )

        # Dummy queues — remote server uses build_batch_responses + ZMQ sendback.
        import multiprocessing as mp

        ctx = mp.get_context("spawn")
        dummy_q = ctx.Queue()
        dummy_replies = [ctx.Queue() for _ in range(max(8, int(search_cfg.get("max_clients", 8))))]
        self._engine = SMZInferenceServer(
            net=net,
            search_config=search_config,
            device=torch_device,
            request_queue=dummy_q,
            reply_queues=dummy_replies,
            sync_path=self.weights_path,
            sync_check_interval=self.sync_interval,
            inference_batch_size=self.batch_size,
            inference_batch_interval_s=self.batch_interval_s,
            compile_mode=bool(compile_mode),
            clear_tree_on_weight_sync=False,
        )
        self._gpu_name = (
            torch.cuda.get_device_name(torch_device.index or 0)
            if torch_device.type == "cuda"
            else "cpu"
        )

        from core.telemetry.pc2_telemetry import detect_cpu_name

        self._cpu_name = detect_cpu_name()

        from collections import deque as _deque

        from core.telemetry.gpu_backend import GpuBackend

        self._batch_window: _deque = _deque(maxlen=30)
        self._gpu_backend = GpuBackend()
        self._gpu_index = int(torch_device.index or 0) if torch_device.type == "cuda" else 0

        self._ctx = zmq.Context.instance()
        self._router = self._ctx.socket(zmq.ROUTER)
        self._router.setsockopt(zmq.LINGER, 0)
        self._router.bind(f"tcp://{self.host}:{self.port}")
        _log(f"[SMZ][REMOTE_IS] listening on {self.host}:{self.port} device={torch_device}", log_path)

    def stop(self) -> None:
        self._running = False
        try:
            self._engine.stop()
        except Exception:
            pass

    def _check_auth(self, msg: dict[str, Any]) -> str | None:
        if not self.auth_token:
            return None
        token = str(msg.get("auth_token", "") or "")
        if token != self.auth_token:
            return "auth token mismatch"
        return None

    def _check_protocol(self, msg: dict[str, Any]) -> str | None:
        ver = int(msg.get("protocol_version", 0) or 0)
        if ver != PROTOCOL_VERSION:
            return f"protocol_version mismatch, expected {PROTOCOL_VERSION}, got {ver}"
        return None

    @staticmethod
    def _router_send(router: zmq.Socket, identity: bytes, payload: bytes) -> None:
        router.send_multipart([identity, payload])

    @staticmethod
    def _router_recv(router: zmq.Socket, flags: int = 0) -> tuple[bytes, bytes]:
        parts = router.recv_multipart(flags=flags)
        if len(parts) == 2:
            return parts[0], parts[1]
        if len(parts) >= 3:
            return parts[0], parts[-1]
        raise ValueError(f"unexpected ROUTER frame count: {len(parts)}")

    def _send_error(self, identity: bytes, message: str) -> None:
        payload = encode_message({"kind": "error", "message": str(message)})
        self._router_send(self._router, identity, payload)

    def _handle_health_check(self, identity: bytes, msg: dict[str, Any]) -> None:
        err = self._check_auth(msg) or self._check_protocol(msg)
        if err:
            self._send_error(identity, err)
            return
        avg_batch = (sum(self._batch_window) / len(self._batch_window)) if self._batch_window else None
        gpu_util = gpu_used = gpu_total = gpu_temp = None
        try:
            for d in self._gpu_backend.read_devices():
                if d.index == self._gpu_index:
                    gpu_util, gpu_used, gpu_total, gpu_temp = (
                        d.util, d.mem_used_mb, d.mem_total_mb, d.temp_c
                    )
                    break
        except Exception:
            pass
        from core.telemetry.pc2_telemetry import sample_cpu_ram_system

        cpu = sample_cpu_ram_system()
        resp = build_health_payload(
            protocol_version=PROTOCOL_VERSION,
            policy_version=int(self._engine.weight_version),
            gpu_name=str(self._gpu_name),
            queue_depth=int(self._queue_depth),
            uptime_s=int(time.time() - self._started_at),
            avg_batch=avg_batch,
            gpu_util=gpu_util, gpu_mem_used_mb=gpu_used,
            gpu_mem_total_mb=gpu_total, gpu_temp_c=gpu_temp,
            cpu_name=self._cpu_name,
            cpu_pct_system=cpu["cpu_pct_system"],
            ram_pct_system=cpu["ram_pct_system"],
            ram_gb_system=cpu["ram_gb_system"],
        )
        self._router_send(self._router, identity, encode_message(resp))

    def _enqueue(self, identity: bytes, request: dict[str, Any]) -> None:
        with self._pending_lock:
            if len(self._pending) >= self.max_queue_depth:
                wait_ms = 50
                payload = encode_message({"kind": "backpressure", "wait_ms": wait_ms})
                self._router_send(self._router, identity, payload)
                return
            self._pending.append(_PendingRequest(identity, request))
            self._queue_depth = len(self._pending)

    def _collect_batch(self) -> list[_PendingRequest]:
        deadline = time.perf_counter() + self.batch_interval_s
        batch: list[_PendingRequest] = []
        while time.perf_counter() < deadline and len(batch) < self.batch_size:
            with self._pending_lock:
                while self._pending and len(batch) < self.batch_size:
                    batch.append(self._pending.popleft())
                self._queue_depth = len(self._pending)
            if len(batch) >= self.batch_size:
                break
            remaining_ms = max(1, int((deadline - time.perf_counter()) * 1000.0))
            poll = zmq.Poller()
            poll.register(self._router, zmq.POLLIN)
            if not poll.poll(remaining_ms):
                break
            try:
                identity, data = self._router_recv(self._router, flags=zmq.NOBLOCK)
            except zmq.Again:
                break
            self._dispatch_incoming(identity, data)
        with self._pending_lock:
            while self._pending and len(batch) < self.batch_size:
                batch.append(self._pending.popleft())
            self._queue_depth = len(self._pending)
        return batch

    def _dispatch_incoming(self, identity: bytes, data: bytes) -> None:
        try:
            msg = decode_message(data)
        except Exception as exc:
            self._send_error(identity, f"decode error: {exc}")
            return
        kind = str(msg.get("kind", "infer")).strip().lower()
        if kind == "health_check":
            self._handle_health_check(identity, msg)
            return
        if kind not in ("infer", ""):
            self._send_error(identity, f"unknown kind: {kind}")
            return
        err = self._check_auth(msg) or self._check_protocol(msg)
        if err:
            self._send_error(identity, err)
            return
        self._enqueue(identity, msg)

    def _process_and_reply(self, batch: list[_PendingRequest]) -> None:
        if not batch:
            return
        self._batch_window.append(len(batch))
        req_dicts = [item.request for item in batch]
        try:
            responses = self._engine.build_batch_responses(req_dicts)
        except Exception as exc:
            for item in batch:
                self._send_error(item.identity, f"batch error: {exc}")
            _log(f"[SMZ][REMOTE_IS] batch_error: {exc}", self.log_path)
            return
        by_env = {int(r.get("env_id", 0)): r for r in responses}
        for item in batch:
            env_id = int(item.request.get("env_id", 0))
            resp = by_env.get(env_id)
            if resp is None:
                self._send_error(item.identity, "missing infer response")
                continue
            wire = dict(resp)
            wire["kind"] = "infer_response"
            wire["protocol_version"] = PROTOCOL_VERSION
            self._router_send(self._router, item.identity, encode_message(wire))

    def run(self) -> None:
        while self._running:
            try:
                if self._router.poll(50):
                    identity, data = self._router_recv(self._router)
                    self._dispatch_incoming(identity, data)
                batch = self._collect_batch()
                if batch:
                    self._process_and_reply(batch)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                _log(f"[SMZ][REMOTE_IS] loop_error: {exc}", self.log_path)
                time.sleep(0.05)
        _log("[SMZ][REMOTE_IS] shutdown complete", self.log_path)


def build_health_payload(
    *,
    protocol_version: int,
    policy_version: int,
    gpu_name: str,
    queue_depth: int,
    uptime_s: int,
    avg_batch,
    gpu_util,
    gpu_mem_used_mb,
    gpu_mem_total_mb,
    gpu_temp_c,
    cpu_name: str | None = None,
    cpu_pct_system=None,
    ram_pct_system=None,
    ram_gb_system=None,
) -> dict:
    # cpu_*/ram_* — опциональны (телеметрия CPU/RAM ПК2). Старый ПК2 их не шлёт → None,
    # старый ПК1 (GUI) игнорирует. Обратная совместимость health_check сохраняется.
    return {
        "kind": "health_check",
        "status": "ok",
        "protocol_version": int(protocol_version),
        "policy_version": int(policy_version),
        "gpu_name": str(gpu_name),
        "queue_depth": int(queue_depth),
        "uptime_s": int(uptime_s),
        "avg_batch": (None if avg_batch is None else float(avg_batch)),
        "gpu_util": gpu_util,
        "gpu_mem_used_mb": gpu_mem_used_mb,
        "gpu_mem_total_mb": gpu_mem_total_mb,
        "gpu_temp_c": gpu_temp_c,
        "cpu_name": (None if cpu_name is None else str(cpu_name)),
        "cpu_pct_system": cpu_pct_system,
        "ram_pct_system": ram_pct_system,
        "ram_gb_system": ram_gb_system,
    }


def _load_search_config(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"--search-config not found: {path}")
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in {".json"}:
        data = json.loads(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise TypeError("search config must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="40kAI Sampled MuZero Remote Inference Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5560)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--weights-path", required=True)
    parser.add_argument("--sync-method", choices=["smb"], default="smb")
    parser.add_argument("--init-weights", default=None)
    parser.add_argument("--search-config", default=None, help="JSON with obs_dim, action_sizes, num_samples…")
    parser.add_argument("--sync-interval", type=float, default=0.5)
    parser.add_argument("--compile", action="store_true")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--batch-interval-ms", type=float, default=20.0)
    parser.add_argument("--auth-token", default="")
    parser.add_argument("--log-file", default=None)
    args = parser.parse_args()

    if args.sync_method != "smb":
        print("v1 supports only --sync-method smb", file=sys.stderr)
        return 2

    log_path = Path(args.log_file) if args.log_file else None
    if log_path is None:
        logs_dir = _REPO_ROOT / "runtime" / "logs"
        stamp = datetime.now().strftime("%Y-%m-%d")
        log_path = logs_dir / f"smz_remote_is_{stamp}.log"

    search_cfg = _load_search_config(args.search_config)
    server = SMZRemoteInferenceServer(
        host=str(args.host),
        port=int(args.port),
        device=str(args.device),
        weights_path=str(args.weights_path),
        init_weights_path=str(args.init_weights) if args.init_weights else None,
        search_cfg=search_cfg,
        sync_interval=float(args.sync_interval),
        batch_size=int(args.batch_size),
        batch_interval_ms=float(args.batch_interval_ms),
        compile_mode=bool(args.compile),
        auth_token=str(args.auth_token or ""),
        log_path=log_path,
    )

    def _on_signal(_sig, _frame) -> None:
        server.stop()

    signal.signal(signal.SIGINT, _on_signal)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, _on_signal)
    server.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
