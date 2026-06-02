#!/usr/bin/env python
"""Standalone remote AlphaZero inference server (ZMQ ROUTER + GPU batched net.infer).

Запуск на ПК2. Net.infer выносится сюда; MCTS tree + env остаются на ПК1 (воркеры).
Веса (v1): только SMB — сервер читает latest_az_{tree|proxy}_policy.pth по сети.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import torch
import zmq

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from core.models.az_inference_protocol import (  # noqa: E402
    AZ_PROTOCOL_VERSION,
    build_health_response,
    decode_message,
    encode_message,
)
from core.models.az_inference_server import AZInferenceEngine  # noqa: E402
from core.models.alphazero_model import make_alphazero_net, load_alphazero_state_dict  # noqa: E402
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


class _Pending:
    __slots__ = ("identity", "request")

    def __init__(self, identity: bytes, request: dict[str, Any]) -> None:
        self.identity = identity
        self.request = request


class AZRemoteInferenceServer:
    def __init__(
        self,
        *,
        host: str,
        port: int,
        device: str,
        weights_path: str,
        init_weights_path: str | None,
        net_cfg: dict[str, Any],
        sync_interval: float,
        batch_size: int,
        batch_interval_ms: float,
        auth_token: str,
        log_path: Path | None,
        max_queue_depth: int = 128,
    ) -> None:
        self.host = str(host)
        self.port = int(port)
        self.weights_path = str(weights_path)
        self.batch_size = max(1, int(batch_size))
        self.batch_interval_s = float(batch_interval_ms) / 1000.0
        self.auth_token = str(auth_token or "")
        self.log_path = log_path
        self.max_queue_depth = max(8, int(max_queue_depth))
        self._running = True
        self._started_at = time.time()
        self._pending: deque[_Pending] = deque()
        self._queue_depth = 0
        self._batch_window: deque = deque(maxlen=30)

        if torch.cuda.is_available() and str(device).startswith("cuda"):
            idx = int(str(device).split(":")[-1]) if ":" in str(device) else 0
            torch.cuda.set_device(idx)
            torch_device = torch.device(device)
        else:
            torch_device = torch.device("cpu")

        obs_dim = int(net_cfg.get("obs_dim", 0))
        action_sizes = [int(x) for x in net_cfg.get("action_sizes", [])]
        net = make_alphazero_net(
            n_observations=obs_dim,
            n_actions=action_sizes,
            hidden_size=int(net_cfg.get("hidden_size", 256)),
            num_layers=int(net_cfg.get("num_layers", 2)),
            n_value_ensemble=int(net_cfg.get("n_value_ensemble", 1)),
        ).to(torch_device)

        weight_src = init_weights_path if init_weights_path and os.path.isfile(init_weights_path) else None
        if weight_src:
            payload = torch.load(weight_src, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else payload
            load_alphazero_state_dict(net, normalize_state_dict(sd), log_fn=None)
            _log(f"[AZ][REMOTE_IS] loaded init weights from {weight_src}", log_path)
        elif os.path.isfile(self.weights_path):
            payload = torch.load(self.weights_path, map_location="cpu", weights_only=False)
            sd = payload.get("state_dict") if isinstance(payload, dict) else payload
            load_alphazero_state_dict(net, normalize_state_dict(sd), log_fn=None)
            _log(f"[AZ][REMOTE_IS] loaded weights from {self.weights_path}", log_path)
        else:
            raise FileNotFoundError(
                f"Веса не найдены: {self.weights_path!r}. "
                "Где: az_remote_inference_server. "
                "Что делать: укажите --init-weights для первого старта или проверьте SMB-путь."
            )
        net.eval()

        self._engine = AZInferenceEngine(
            net=net,
            device=torch_device,
            sync_path=self.weights_path,
            sync_check_interval=float(sync_interval),
        )
        self._gpu_name = (
            torch.cuda.get_device_name(torch_device.index or 0)
            if torch_device.type == "cuda" else "cpu"
        )
        try:
            from core.telemetry.gpu_backend import GpuBackend
            self._gpu_backend = GpuBackend()
        except Exception:
            self._gpu_backend = None
        self._gpu_index = int(torch_device.index or 0) if torch_device.type == "cuda" else 0

        # P1: системные CPU/RAM ПК2 для телеметрии ПК1 (через health_check).
        try:
            import psutil  # noqa: F401

            self._psutil = psutil
            try:
                psutil.cpu_percent(None)  # прайминг: первый вызов всегда 0.0
            except Exception:
                pass
        except Exception:
            self._psutil = None
        # Имя CPU для подписи «ПК2 · …»: env (из конфига ПК2) → platform fallback.
        import platform
        self._cpu_label = (
            os.environ.get("40KAI_PC2_CPU_LABEL")
            or os.environ.get("AZ_REMOTE_CPU_LABEL")
            or platform.processor()
            or "CPU"
        )

        self._ctx = zmq.Context.instance()
        self._router = self._ctx.socket(zmq.ROUTER)
        self._router.setsockopt(zmq.LINGER, 0)
        self._router.bind(f"tcp://{self.host}:{self.port}")
        _log(f"[AZ][REMOTE_IS] listening on {self.host}:{self.port} device={torch_device}", log_path)
        # Маркер нового кода телеметрии: видно в логе ПК2 = health_check шлёт CPU/RAM ПК2.
        _log(
            f"[AZ][REMOTE_IS] telemetry cpu={'on' if self._psutil is not None else 'OFF(psutil?)'} "
            f"cpu_label={self._cpu_label!r}",
            log_path,
        )

    def stop(self) -> None:
        self._running = False
        try:
            self._engine.stop()
        except Exception:
            pass

    # --- validation ---
    def _check_auth(self, msg: dict[str, Any]) -> str | None:
        if not self.auth_token:
            return None
        if str(msg.get("auth_token", "") or "") != self.auth_token:
            return "auth token mismatch"
        return None

    def _check_protocol(self, msg: dict[str, Any]) -> str | None:
        ver = int(msg.get("protocol_version", 0) or 0)
        if ver != AZ_PROTOCOL_VERSION:
            return f"protocol_version mismatch, expected {AZ_PROTOCOL_VERSION}, got {ver}"
        return None

    @staticmethod
    def _router_recv(router: zmq.Socket, flags: int = 0) -> tuple[bytes, bytes]:
        parts = router.recv_multipart(flags=flags)
        if len(parts) == 2:
            return parts[0], parts[1]
        if len(parts) >= 3:
            return parts[0], parts[-1]
        raise ValueError(f"unexpected ROUTER frame count: {len(parts)}")

    def _send(self, identity: bytes, payload: dict[str, Any]) -> None:
        self._router.send_multipart([identity, encode_message(payload)])

    def _send_error(self, identity: bytes, message: str) -> None:
        self._send(identity, {"kind": "error", "message": str(message)})

    def _handle_health(self, identity: bytes, msg: dict[str, Any]) -> None:
        err = self._check_auth(msg) or self._check_protocol(msg)
        if err:
            self._send_error(identity, err)
            return
        avg_batch = (sum(self._batch_window) / len(self._batch_window)) if self._batch_window else None
        gpu_util = gpu_used = gpu_total = gpu_temp = None
        if self._gpu_backend is not None:
            try:
                for d in self._gpu_backend.read_devices():
                    if d.index == self._gpu_index:
                        gpu_util, gpu_used, gpu_total, gpu_temp = d.util, d.mem_used_mb, d.mem_total_mb, d.temp_c
                        break
            except Exception:
                pass
        cpu_pct_sys = ram_pct_sys = ram_gb_sys = None
        if self._psutil is not None:
            try:
                cpu_pct_sys = float(self._psutil.cpu_percent(None))
                vm = self._psutil.virtual_memory()
                ram_pct_sys = float(vm.percent)
                ram_gb_sys = float(vm.used) / 1e9
            except Exception:
                pass
        self._send(identity, build_health_response(
            policy_version=int(self._engine.weight_version),
            gpu_name=str(self._gpu_name),
            queue_depth=int(self._queue_depth),
            uptime_s=int(time.time() - self._started_at),
            avg_batch=avg_batch,
            gpu_util=gpu_util, gpu_mem_used_mb=gpu_used,
            gpu_mem_total_mb=gpu_total, gpu_temp_c=gpu_temp,
            cpu_name=str(self._cpu_label),
            cpu_pct_system=cpu_pct_sys,
            ram_pct_system=ram_pct_sys,
            ram_gb_system=ram_gb_sys,
        ))

    def _dispatch(self, identity: bytes, data: bytes) -> None:
        try:
            msg = decode_message(data)
        except Exception as exc:
            self._send_error(identity, f"decode error: {exc}")
            return
        kind = str(msg.get("kind", "infer")).strip().lower()
        if kind == "health_check":
            self._handle_health(identity, msg)
            return
        if kind not in ("infer", ""):
            self._send_error(identity, f"unknown kind: {kind}")
            return
        err = self._check_auth(msg) or self._check_protocol(msg)
        if err:
            self._send_error(identity, err)
            return
        if len(self._pending) >= self.max_queue_depth:
            self._send(identity, {"kind": "backpressure", "wait_ms": 50})
            return
        self._pending.append(_Pending(identity, msg))
        self._queue_depth = len(self._pending)

    def _collect_batch(self) -> list[_Pending]:
        deadline = time.perf_counter() + self.batch_interval_s
        batch: list[_Pending] = []
        while time.perf_counter() < deadline and len(batch) < self.batch_size:
            while self._pending and len(batch) < self.batch_size:
                batch.append(self._pending.popleft())
            self._queue_depth = len(self._pending)
            if len(batch) >= self.batch_size:
                break
            remaining_ms = max(1, int((deadline - time.perf_counter()) * 1000.0))
            if not self._router.poll(remaining_ms):
                break
            try:
                identity, data = self._router_recv(self._router, flags=zmq.NOBLOCK)
            except zmq.Again:
                break
            self._dispatch(identity, data)
        while self._pending and len(batch) < self.batch_size:
            batch.append(self._pending.popleft())
        self._queue_depth = len(self._pending)
        return batch

    def _process_and_reply(self, batch: list[_Pending]) -> None:
        if not batch:
            return
        self._batch_window.append(len(batch))

        # Конкатенируем obs/masks всех запросов в один forward
        obs_list, masks_list, want_any = [], [], False
        for item in batch:
            req = item.request
            obs_list.append(np.asarray(req["obs"], dtype=np.float32))
            masks_list.append([np.asarray(m) for m in req.get("legal_masks_by_head", [])])
            if bool(req.get("want_priors", True)):
                want_any = True

        try:
            obs_batch = np.concatenate(obs_list, axis=0)
            num_heads = len(masks_list[0])
            masks_batch = [np.concatenate([ml[h] for ml in masks_list], axis=0) for h in range(num_heads)]
            priors, values, version = self._engine.evaluate_batch(
                obs_batch, masks_batch, want_priors=want_any
            )
        except Exception as exc:
            for item in batch:
                self._send_error(item.identity, f"batch error: {exc}")
            _log(f"[AZ][REMOTE_IS] batch_error: {exc}", self.log_path)
            return

        cursor = 0
        for item in batch:
            req = item.request
            obs_arr = np.asarray(req["obs"], dtype=np.float32)
            b_i = obs_arr.shape[0] if obs_arr.ndim == 2 else 1
            want_i = bool(req.get("want_priors", True))
            resp_priors = (
                [p[cursor: cursor + b_i] for p in priors] if (want_i and priors) else []
            )
            resp = {
                "kind": "infer_response",
                "protocol_version": AZ_PROTOCOL_VERSION,
                "worker_id": int(req.get("worker_id", 0)),
                "request_id": int(req.get("request_id", 0)),
                "priors": resp_priors,
                "value": values[cursor: cursor + b_i],
                "policy_version": int(version),
            }
            cursor += b_i
            self._send(item.identity, resp)

    def run(self) -> None:
        while self._running:
            try:
                if self._router.poll(50):
                    identity, data = self._router_recv(self._router)
                    self._dispatch(identity, data)
                batch = self._collect_batch()
                if batch:
                    self._process_and_reply(batch)
            except KeyboardInterrupt:
                break
            except Exception as exc:
                _log(f"[AZ][REMOTE_IS] loop_error: {exc}", self.log_path)
                time.sleep(0.05)
        _log("[AZ][REMOTE_IS] shutdown complete", self.log_path)


def _load_cfg(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"--search-config не найден: {path}")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("search config должен быть JSON-объектом")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="40kAI AZ Remote Inference Server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5555)
    parser.add_argument("--device", default="cuda:0")
    parser.add_argument("--weights-path", required=True)
    parser.add_argument("--sync-method", choices=["smb"], default="smb")
    parser.add_argument("--init-weights", default=None)
    parser.add_argument("--search-config", default=None, help="JSON: obs_dim, action_sizes, hidden_size…")
    parser.add_argument("--sync-interval", type=float, default=0.5)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--batch-interval-ms", type=float, default=10.0)
    parser.add_argument("--auth-token", default="")
    parser.add_argument("--log-file", default=None)
    args = parser.parse_args()

    if args.sync_method != "smb":
        print("v1 поддерживает только --sync-method smb", file=sys.stderr)
        return 2

    log_path = Path(args.log_file) if args.log_file else (
        _REPO_ROOT / "runtime" / "logs" / f"az_remote_is_{datetime.now().strftime('%Y-%m-%d')}.log"
    )
    net_cfg = _load_cfg(args.search_config)
    server = AZRemoteInferenceServer(
        host=str(args.host),
        port=int(args.port),
        device=str(args.device),
        weights_path=str(args.weights_path),
        init_weights_path=str(args.init_weights) if args.init_weights else None,
        net_cfg=net_cfg,
        sync_interval=float(args.sync_interval),
        batch_size=int(args.batch_size),
        batch_interval_ms=float(args.batch_interval_ms),
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
