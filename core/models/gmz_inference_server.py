"""Centralized GPU inference server for Gumbel MuZero (variant B)."""

from __future__ import annotations

import os
import queue
import threading
import time
from typing import Any, Optional

import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import GumbelMuZeroSearch, GumbelMuZeroSearchConfig
from core.models.utils import normalize_state_dict


def _append_log(msg: str) -> None:
    try:
        from train import append_agent_log

        append_agent_log(msg)
    except Exception:
        pass


class GMZInferenceServer:
    """Батчит запросы env workers, выполняет GumbelMuZeroSearch.run на GPU."""

    def __init__(
        self,
        *,
        net: GumbelMuZeroNet,
        search_config: GumbelMuZeroSearchConfig,
        device: torch.device,
        request_queue: Any,
        reply_queues: list[Any],
        sync_path: str,
        sync_check_interval: float = 0.5,
        inference_batch_size: int = 8,
        inference_batch_interval_s: float = 0.02,
        compile_mode: bool = True,
        clear_tree_on_weight_sync: bool = False,
    ) -> None:
        self.net = net
        self.search_cfg = search_config
        self.device = device
        self.request_q = request_queue
        self.reply_queues = reply_queues
        self.sync_path = str(sync_path)
        self.sync_check_interval = float(sync_check_interval)
        self.max_batch_size = max(1, int(inference_batch_size))
        self._batch_interval = float(inference_batch_interval_s)

        self._tree_states: dict[int, GumbelMuZeroSearch] = {}
        self._pending: list[dict[str, Any]] = []
        self._pending_lock = threading.Lock()
        self._running = True
        self._weight_version = 0
        self._weight_lock = threading.Lock()
        self._clear_tree_on_weight_sync = bool(clear_tree_on_weight_sync)
        self._requests_total = 0
        self._batches_total = 0

        self._inference_stream = None
        if device.type == "cuda":
            self._inference_stream = torch.cuda.Stream()

        if compile_mode and device.type == "cuda" and hasattr(torch, "compile"):
            try:
                self.net = torch.compile(self.net, mode="reduce-overhead", fullgraph=False)
                _append_log("[GMZ][INF_SERVER] torch.compile enabled (mode=reduce-overhead)")
            except Exception as exc:
                _append_log(f"[GMZ][INF_SERVER] torch.compile skipped: {exc}")

        self._weight_thread = threading.Thread(target=self._poll_weights, daemon=True)
        self._weight_thread.start()

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
                                self.net.load_state_dict(normalize_state_dict(sd), strict=False)
                                self.net.eval()
                                self._weight_version = new_ver
                                for search in self._tree_states.values():
                                    search.net = self.net
                                if self._clear_tree_on_weight_sync:
                                    for search in self._tree_states.values():
                                        search.clear_tree_state()
                            last_mtime = float(mtime)
                            _append_log(f"[GMZ][INF_SERVER] weight_updated version={new_ver}")
            except Exception as exc:
                _append_log(f"[GMZ][INF_SERVER] weight_poll_error: {exc}")
            time.sleep(self.sync_check_interval)

    def run(self) -> None:
        while self._running:
            self._collect_and_process_batch()

    def _collect_and_process_batch(self) -> None:
        deadline = time.perf_counter() + self._batch_interval
        while len(self._pending) < self.max_batch_size:
            timeout = max(0.001, deadline - time.perf_counter())
            if timeout <= 0 and self._pending:
                break
            try:
                req = self.request_q.get(timeout=timeout if self._pending else self._batch_interval)
            except queue.Empty:
                break
            if req is None:
                self._running = False
                return
            if not isinstance(req, dict):
                continue
            with self._pending_lock:
                self._pending.append(req)
            if len(self._pending) >= self.max_batch_size:
                break

        with self._pending_lock:
            if not self._pending:
                return
            batch = list(self._pending)
            self._pending = []

        responses = self.build_batch_responses(batch)
        for resp in responses:
            env_id = int(resp.get("env_id", 0))
            try:
                self.reply_queues[int(env_id)].put_nowait(resp)
            except Exception:
                pass
        self._log_batch_stats(len(batch), responses)

    @property
    def weight_version(self) -> int:
        return int(self._weight_version)

    @property
    def requests_total(self) -> int:
        return int(self._requests_total)

    def build_batch_responses(self, batch: list[dict[str, Any]]) -> list[dict[str, Any]]:
        t0 = time.perf_counter()
        responses: list[dict[str, Any]] = []
        by_env: dict[int, list[dict[str, Any]]] = {}
        for req in batch:
            by_env.setdefault(int(req.get("env_id", 0)), []).append(req)

        for env_id, env_batch in by_env.items():
            search = self._get_or_create_tree(env_id)
            for req in env_batch:
                if bool(req.get("is_new_episode", False)):
                    search.clear_tree_state()

                obs = np.asarray(req.get("obs"), dtype=np.float32)
                masks_raw = req.get("legal_masks_by_head") or []
                legal_masks = [np.asarray(m) for m in masks_raw]

                with torch.no_grad():
                    if self._inference_stream is not None:
                        with torch.cuda.stream(self._inference_stream):
                            pi_targets, behavior_logits, actions, value_est = search.run(
                                obs=obs,
                                legal_masks_by_head=legal_masks,
                                deterministic=False,
                            )
                    else:
                        pi_targets, behavior_logits, actions, value_est = search.run(
                            obs=obs,
                            legal_masks_by_head=legal_masks,
                            deterministic=False,
                        )

                responses.append(
                    {
                        "kind": "infer_response",
                        "env_id": int(env_id),
                        "selected_actions": list(actions),
                        "policy_targets": [np.asarray(p, dtype=np.float32) for p in pi_targets],
                        "behavior_logits": [
                            np.asarray(b, dtype=np.float32) for b in behavior_logits
                        ],
                        "value_est": float(value_est),
                        "policy_version": int(self._weight_version),
                    }
                )
                self._requests_total += 1

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        self._batches_total += 1
        self._last_batch_ms = float(elapsed_ms)
        return responses

    def _log_batch_stats(self, batch_size: int, responses: list[dict[str, Any]]) -> None:
        elapsed_ms = float(getattr(self, "_last_batch_ms", 0.0))
        if batch_size > 1 or elapsed_ms > 200.0:
            _append_log(
                f"[GMZ][INF_SERVER] batch={batch_size} inference_ms={elapsed_ms:.1f} "
                f"total_reqs={self._requests_total}"
            )
        if elapsed_ms > 500.0:
            _append_log(f"[GMZ][INF_SERVER] slow_batch ms={elapsed_ms:.1f} for n={batch_size}")
        if not responses:
            return

    def _get_or_create_tree(self, env_id: int) -> GumbelMuZeroSearch:
        if env_id not in self._tree_states:
            with self._weight_lock:
                self._tree_states[env_id] = GumbelMuZeroSearch(
                    net=self.net,
                    config=self.search_cfg,
                    device=self.device,
                )
        return self._tree_states[env_id]


def gmz_inference_server_entry(
    request_q: Any,
    reply_queues: list[Any],
    sync_path: str,
    init_weights: dict,
    search_cfg_payload: dict,
    *,
    inference_batch_size: int = 8,
    inference_batch_interval_ms: float = 20.0,
    sync_check_interval: float = 0.5,
    inference_server_compile: bool = True,
    clear_tree_on_weight_sync: bool = False,
) -> None:
    """Top-level entry for Windows spawn."""
    server: Optional[GMZInferenceServer] = None
    try:
        if torch.cuda.is_available():
            torch.cuda.set_device(0)
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

        latent_dim = int(search_cfg_payload.get("latent_dim", 256))
        hidden_dim = int(search_cfg_payload.get("hidden_dim", 256))
        num_layers = int(search_cfg_payload.get("num_layers", 2))
        action_embed_dim = int(search_cfg_payload.get("action_embed_dim", 64))
        obs_dim = int(search_cfg_payload.get("obs_dim", 0))
        action_sizes = [int(x) for x in search_cfg_payload.get("action_sizes", [])]

        net = GumbelMuZeroNet(
            obs_dim=obs_dim,
            action_sizes=action_sizes,
            latent_dim=latent_dim,
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            action_embed_dim=action_embed_dim,
        ).to(device)
        net.load_state_dict(normalize_state_dict(init_weights))
        net.eval()

        search_config = GumbelMuZeroSearchConfig(
            num_simulations=int(search_cfg_payload.get("num_simulations", 32)),
            root_top_k=int(search_cfg_payload.get("root_top_k", 8)),
            discount=float(search_cfg_payload.get("discount", 0.997)),
            temperature=float(search_cfg_payload.get("temperature", 0.15)),
            gumbel_scale=float(search_cfg_payload.get("gumbel_scale", 1.0)),
            prior_weight=float(search_cfg_payload.get("prior_weight", 0.25)),
            batch_recurrent=bool(int(search_cfg_payload.get("batch_recurrent", 1))),
            tree_reuse=bool(int(search_cfg_payload.get("tree_reuse", 1))),
        )

        server = GMZInferenceServer(
            net=net,
            search_config=search_config,
            device=device,
            request_queue=request_q,
            reply_queues=reply_queues,
            sync_path=sync_path,
            sync_check_interval=sync_check_interval,
            inference_batch_size=inference_batch_size,
            inference_batch_interval_s=float(inference_batch_interval_ms) / 1000.0,
            compile_mode=bool(inference_server_compile),
            clear_tree_on_weight_sync=clear_tree_on_weight_sync,
        )
        _append_log(
            f"[GMZ][INF_SERVER] started batch={inference_batch_size} "
            f"device={device.type} workers={len(reply_queues)}"
        )
        server.run()
    except Exception as exc:
        _append_log(f"[GMZ][INF_SERVER] fatal: {exc}")
        raise
    finally:
        if server is not None:
            try:
                server.stop()
            except Exception:
                pass
