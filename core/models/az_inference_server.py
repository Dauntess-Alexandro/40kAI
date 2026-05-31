"""Centralized GPU inference server for AlphaZero tree (variant B)."""

from __future__ import annotations

import os
import queue
import threading
import time
from typing import Any, Optional

import numpy as np
import torch

from core.models.alphazero_model import AlphaZeroPolicyValueNet, load_alphazero_state_dict
from core.models.utils import normalize_state_dict


def _append_log(msg: str) -> None:
    try:
        from train import append_agent_log
        append_agent_log(msg)
    except Exception:
        pass


class AZInferenceEngine:
    """Stateless GPU evaluator: batched net.infer + weight polling.

    Не держит tree state (в отличие от GMZ) — AZ tree живёт на воркере.
    Потокобезопасен: weight_lock защищает net при обновлении весов.
    """

    def __init__(
        self,
        *,
        net: AlphaZeroPolicyValueNet,
        device: torch.device,
        sync_path: str,
        sync_check_interval: float = 0.5,
    ) -> None:
        self.net = net
        self.device = device
        self.sync_path = str(sync_path)
        self.sync_check_interval = float(sync_check_interval)
        self._weight_version = 0
        self._weight_lock = threading.Lock()
        self._running = True

        self._inference_stream: Optional[Any] = None
        if device.type == "cuda":
            self._inference_stream = torch.cuda.Stream()

        self._weight_thread = threading.Thread(target=self._poll_weights, daemon=True)
        self._weight_thread.start()

    @property
    def weight_version(self) -> int:
        return int(self._weight_version)

    def stop(self) -> None:
        self._running = False
        self._weight_thread.join(timeout=2.0)

    def _poll_weights(self) -> None:
        last_mtime = -1.0
        while self._running:
            try:
                if os.path.isfile(self.sync_path):
                    mtime = os.path.getmtime(self.sync_path)
                    if mtime > last_mtime:
                        payload = torch.load(
                            self.sync_path, map_location="cpu", weights_only=False
                        )
                        sd = payload.get("state_dict") if isinstance(payload, dict) else None
                        if isinstance(sd, dict):
                            new_ver = int(
                                payload.get("policy_version", self._weight_version)
                                or self._weight_version
                            )
                            with self._weight_lock:
                                load_alphazero_state_dict(
                                    self.net, normalize_state_dict(sd), log_fn=None
                                )
                                self.net.eval()
                                self._weight_version = new_ver
                            last_mtime = float(mtime)
                            _append_log(
                                f"[AZ][INF_SERVER] weight_updated version={new_ver} "
                                f"file={os.path.basename(self.sync_path)}"
                            )
            except Exception as exc:
                _append_log(f"[AZ][INF_SERVER] weight_poll_error: {exc}")
            time.sleep(self.sync_check_interval)

    def evaluate_batch(
        self,
        obs_np: np.ndarray,
        masks_np_by_head: list[np.ndarray],
        *,
        want_priors: bool = True,
    ) -> tuple[list[np.ndarray], np.ndarray, int]:
        """Batched forward pass.

        obs_np: float32 [B, obs_dim]
        masks_np_by_head: list num_heads × [B, head_size] bool

        Returns:
            priors: list num_heads × [B, head_size] float32 (пусто если want_priors=False)
            values: [B] float32
            policy_version: int
        """
        obs_t = torch.tensor(obs_np, dtype=torch.float32, device=self.device)
        masks_t = [
            torch.as_tensor(m, dtype=torch.bool, device=self.device)
            for m in masks_np_by_head
        ]

        ctx = (
            torch.cuda.stream(self._inference_stream)
            if self._inference_stream is not None
            else _null_context()
        )

        with torch.no_grad(), self._weight_lock, ctx:
            priors_t, values_t = self.net.infer(obs_t, masks_by_head=masks_t)
            version = int(self._weight_version)

        values = values_t.detach().cpu().numpy().astype(np.float32)
        if want_priors:
            priors = [p.detach().cpu().numpy().astype(np.float32) for p in priors_t]
        else:
            priors = []
        return priors, values, version


class _null_context:
    def __enter__(self):
        return self
    def __exit__(self, *a):
        pass


class AZInferenceServer:
    """Батчит запросы env-воркеров, выполняет AZInferenceEngine.evaluate_batch на GPU."""

    def __init__(
        self,
        *,
        engine: AZInferenceEngine,
        request_queue: Any,
        reply_queues: list[Any],
        inference_batch_size: int = 32,
        inference_batch_interval_s: float = 0.01,
    ) -> None:
        self._engine = engine
        self._request_q = request_queue
        self._reply_queues = reply_queues
        self._max_batch = max(1, int(inference_batch_size))
        self._batch_interval = float(inference_batch_interval_s)
        self._running = True
        self._requests_total = 0
        self._batches_total = 0

    def stop(self) -> None:
        self._running = False

    def run(self) -> None:
        _append_log(
            f"[AZ][INF_SERVER] loop started batch_max={self._max_batch} "
            f"interval_ms={int(self._batch_interval * 1000)}"
        )
        while self._running:
            self._collect_and_process_batch()

    def _collect_and_process_batch(self) -> None:
        deadline = time.perf_counter() + self._batch_interval
        pending: list[dict[str, Any]] = []

        while len(pending) < self._max_batch:
            timeout = max(0.001, deadline - time.perf_counter())
            if timeout <= 0 and pending:
                break
            try:
                req = self._request_q.get(
                    timeout=timeout if pending else self._batch_interval
                )
            except queue.Empty:
                break
            if req is None:
                self._running = False
                return
            if not isinstance(req, dict):
                continue
            pending.append(req)
            if len(pending) >= self._max_batch:
                break

        if not pending:
            return

        self._process_batch(pending)

    def _process_batch(self, batch: list[dict[str, Any]]) -> None:
        t0 = time.perf_counter()

        # Группируем запросы одного батч-форварда: конкатенируем obs/masks
        obs_list: list[np.ndarray] = []
        masks_list: list[list[np.ndarray]] = []
        want_priors_any = False
        for req in batch:
            obs_list.append(np.asarray(req["obs"], dtype=np.float32))
            masks_list.append([np.asarray(m) for m in req.get("legal_masks_by_head", [])])
            if bool(req.get("want_priors", True)):
                want_priors_any = True

        # Stack: obs [B, obs_dim], masks per head [B, head_size]
        obs_batch = np.concatenate(obs_list, axis=0)  # each obs already [B_i, obs_dim]
        num_heads = len(masks_list[0]) if masks_list else 0
        masks_batch: list[np.ndarray] = []
        for h in range(num_heads):
            masks_batch.append(np.concatenate([ml[h] for ml in masks_list], axis=0))

        try:
            priors, values, version = self._engine.evaluate_batch(
                obs_batch, masks_batch, want_priors=want_priors_any
            )
        except Exception as exc:
            _append_log(f"[AZ][INF_SERVER] batch_error: {exc}")
            # Отвечаем ошибкой каждому воркеру
            for req in batch:
                worker_id = int(req.get("worker_id", 0))
                try:
                    self._reply_queues[worker_id].put_nowait(
                        {"kind": "error", "message": str(exc)}
                    )
                except Exception:
                    pass
            return

        # Разбиваем ответы обратно по запросам (каждый запрос может иметь свой B_i)
        cursor = 0
        for req in batch:
            obs_arr = np.asarray(req["obs"], dtype=np.float32)
            b_i = obs_arr.shape[0] if obs_arr.ndim == 2 else 1
            worker_id = int(req.get("worker_id", 0))
            request_id = int(req.get("request_id", 0))

            resp_priors: list[np.ndarray] = []
            if priors:
                resp_priors = [p[cursor: cursor + b_i] for p in priors]
            resp_values = values[cursor: cursor + b_i]
            cursor += b_i

            resp = {
                "kind": "infer_response",
                "worker_id": worker_id,
                "request_id": request_id,
                "priors": resp_priors,
                "value": resp_values,
                "policy_version": version,
            }
            try:
                self._reply_queues[worker_id].put_nowait(resp)
            except Exception:
                pass
            self._requests_total += 1

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        self._batches_total += 1
        if len(batch) > 1 or elapsed_ms > 200.0:
            _append_log(
                f"[AZ][INF_SERVER] batch={len(batch)} inference_ms={elapsed_ms:.1f} "
                f"total_reqs={self._requests_total}"
            )
        if elapsed_ms > 500.0:
            _append_log(f"[AZ][INF_SERVER] slow_batch ms={elapsed_ms:.1f} n={len(batch)}")


def az_inference_server_entry(
    request_q: Any,
    reply_queues: list[Any],
    sync_path: str,
    init_weights: dict,
    net_cfg: dict,
    *,
    inference_batch_size: int = 32,
    inference_batch_interval_ms: float = 10.0,
    sync_check_interval: float = 0.5,
) -> None:
    """Top-level entry для Windows spawn (нет lambda/closure)."""
    engine: Optional[AZInferenceEngine] = None
    server: Optional[AZInferenceServer] = None
    try:
        if torch.cuda.is_available():
            torch.cuda.set_device(0)
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

        obs_dim = int(net_cfg.get("obs_dim", 0))
        action_sizes = [int(x) for x in net_cfg.get("action_sizes", [])]
        hidden_size = int(net_cfg.get("hidden_size", 256))
        num_layers = int(net_cfg.get("num_layers", 2))
        n_value_ensemble = int(net_cfg.get("n_value_ensemble", 1))

        from core.models.alphazero_model import make_alphazero_net
        net = make_alphazero_net(
            n_observations=obs_dim,
            n_actions=action_sizes,
            hidden_size=hidden_size,
            num_layers=num_layers,
            n_value_ensemble=n_value_ensemble,
        ).to(device)
        load_alphazero_state_dict(net, normalize_state_dict(init_weights), log_fn=None)
        net.eval()

        engine = AZInferenceEngine(
            net=net,
            device=device,
            sync_path=sync_path,
            sync_check_interval=sync_check_interval,
        )
        server = AZInferenceServer(
            engine=engine,
            request_queue=request_q,
            reply_queues=reply_queues,
            inference_batch_size=inference_batch_size,
            inference_batch_interval_s=float(inference_batch_interval_ms) / 1000.0,
        )
        _append_log(
            f"[AZ][INF_SERVER] started device={device.type} "
            f"batch={inference_batch_size} workers={len(reply_queues)}"
        )
        server.run()
    except Exception as exc:
        _append_log(f"[AZ][INF_SERVER] fatal: {exc}")
        raise
    finally:
        if engine is not None:
            try:
                engine.stop()
            except Exception:
                pass
