"""Evaluator implementations for AlphaZero MCTS (Evaluator interface + LocalNet + Remote)."""

from __future__ import annotations

import threading
from typing import Any, Optional, Protocol, runtime_checkable

import numpy as np
import torch

from core.models.alphazero_mcts import EvalCache


@runtime_checkable
class Evaluator(Protocol):
    """Интерфейс эвалуатора для AlphaZeroFactorizedMCTS.

    Реализации: LocalNetEvaluator (текущее поведение) и RemoteEvaluator (inference server).
    """

    def evaluate_one(
        self,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
    ) -> tuple[list[np.ndarray], float]:
        """Одиночный eval: root или intermediate (B=1).

        Returns:
            priors: list[np.ndarray] — masked softmax по головам, float32 [head_size] каждый.
            value: float ∈ [-1, 1].
        """
        ...

    def evaluate_batch(
        self,
        leaves: list[dict[str, Any]],
    ) -> list[float]:
        """Батч leaf eval (B=len(leaves)). Каждый элемент: {'obs': ndarray, 'legal_masks': list}.

        Returns:
            values: list[float] длиной len(leaves), ∈ [-1, 1].
        """
        ...


class LocalNetEvaluator:
    """Эвалуатор через локальную копию сети (поведение variant A, без IS).

    Реализует тот же кэш и infer-логику, что и AlphaZeroFactorizedMCTS._evaluate_net /
    _evaluate_value_batch, но за пределами MCTS — для явной передачи через evaluator=.
    """

    def __init__(
        self,
        net: Any,
        device: torch.device,
        eval_cache_size: int = 10000,
    ) -> None:
        self.net = net
        self.device = device
        self._eval_cache = EvalCache(max_size=eval_cache_size)

    def evaluate_one(
        self,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
    ) -> tuple[list[np.ndarray], float]:
        cached = self._eval_cache.get(obs, legal_masks_by_head)
        if cached is not None:
            return cached
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=self.device).unsqueeze(0)
        masks_t = [
            torch.as_tensor(m, dtype=torch.bool, device=self.device).unsqueeze(0)
            for m in legal_masks_by_head
        ]
        with torch.no_grad():
            priors_t, value_t = self.net.infer(obs_t, masks_by_head=masks_t)
        priors = [p.squeeze(0).detach().cpu().numpy().astype(np.float32) for p in priors_t]
        value = float(value_t.item())
        self._eval_cache.set(obs, legal_masks_by_head, priors, value)
        return priors, value

    def evaluate_batch(self, leaves: list[dict[str, Any]]) -> list[float]:
        n = len(leaves)
        if n == 0:
            return []
        values: list[Optional[float]] = [None] * n
        uncached: list[int] = []
        for i, leaf in enumerate(leaves):
            cached = self._eval_cache.get(leaf["obs"], leaf["legal_masks"])
            if cached is not None:
                values[i] = float(cached[1])
            else:
                uncached.append(i)
        if uncached:
            obs_batch = np.stack([leaves[i]["obs"] for i in uncached])
            obs_t = torch.tensor(obs_batch, dtype=torch.float32, device=self.device)
            num_heads = len(leaves[uncached[0]]["legal_masks"])
            masks_t: list[torch.Tensor] = []
            for h in range(num_heads):
                head_masks = np.stack([
                    np.asarray(leaves[i]["legal_masks"][h], dtype=bool) for i in uncached
                ])
                masks_t.append(torch.as_tensor(head_masks, dtype=torch.bool, device=self.device))
            with torch.no_grad():
                priors_t, values_t = self.net.infer(obs_t, masks_by_head=masks_t)
            for j, i in enumerate(uncached):
                priors_np = [priors_t[h][j].detach().cpu().numpy().astype(np.float32) for h in range(num_heads)]
                val = float(values_t[j].item())
                self._eval_cache.set(leaves[i]["obs"], leaves[i]["legal_masks"], priors_np, val)
                values[i] = val
        return [float(v) for v in values]  # type: ignore[arg-type]


class RemoteEvaluator:
    """Эвалуатор через inference server (local mp.Queue или remote ZMQ).

    Thread-safe: один RemoteEvaluator на воркер + threading.Lock вокруг send/recv.
    Это позволяет параллельным потокам EnvClonePool использовать evaluate_one безопасно.
    """

    def __init__(
        self,
        worker_id: int,
        transport: Any,
        timeout: float = 5.0,
        auth_token: str = "",
    ) -> None:
        self._worker_id = int(worker_id)
        self._transport = transport
        self._timeout = float(timeout)
        self._auth_token = str(auth_token or "")
        self._lock = threading.Lock()
        self._request_id = 0

    def _next_request_id(self) -> int:
        rid = self._request_id
        self._request_id += 1
        return rid

    def evaluate_one(
        self,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
    ) -> tuple[list[np.ndarray], float]:
        obs_arr = np.asarray(obs, dtype=np.float32)
        # Оборачиваем в батч B=1
        obs_batch = obs_arr[np.newaxis] if obs_arr.ndim == 1 else obs_arr
        masks_batch = [
            np.asarray(m)[np.newaxis] if np.asarray(m).ndim == 1 else np.asarray(m)
            for m in legal_masks_by_head
        ]
        from core.models.az_inference_protocol import build_infer_request
        with self._lock:
            req_id = self._next_request_id()
            req = build_infer_request(
                worker_id=self._worker_id,
                request_id=req_id,
                obs=obs_batch,
                legal_masks_by_head=masks_batch,
                want_priors=True,
                auth_token=self._auth_token,
            )
            self._transport.send(req)
            resp = self._transport.recv(self._timeout)
        self._check_error(resp)
        # Распаковываем B=1
        priors_batch = resp.get("priors", [])
        value_batch = np.asarray(resp["value"], dtype=np.float32)
        priors = [np.asarray(p, dtype=np.float32)[0] for p in priors_batch]
        value = float(value_batch[0])
        return priors, value

    def evaluate_batch(self, leaves: list[dict[str, Any]]) -> list[float]:
        if not leaves:
            return []
        obs_batch = np.stack([np.asarray(l["obs"], dtype=np.float32) for l in leaves])
        num_heads = len(leaves[0]["legal_masks"])
        masks_batch = [
            np.stack([np.asarray(l["legal_masks"][h], dtype=bool) for l in leaves])
            for h in range(num_heads)
        ]
        from core.models.az_inference_protocol import build_infer_request
        with self._lock:
            req_id = self._next_request_id()
            req = build_infer_request(
                worker_id=self._worker_id,
                request_id=req_id,
                obs=obs_batch,
                legal_masks_by_head=masks_batch,
                want_priors=False,  # листьям нужны только values
                auth_token=self._auth_token,
            )
            self._transport.send(req)
            resp = self._transport.recv(self._timeout)
        self._check_error(resp)
        values = np.asarray(resp["value"], dtype=np.float32)
        return [float(v) for v in values]

    def _check_error(self, resp: dict[str, Any]) -> None:
        if str(resp.get("kind", "")).lower() == "error":
            msg = str(resp.get("message", "inference error"))
            raise RuntimeError(
                f"[AZ][REMOTE_CLIENT] inference server вернул ошибку: {msg}. "
                "Где: RemoteEvaluator._check_error. "
                "Что делать: проверьте логи сервера [AZ][INF_SERVER] / [AZ][REMOTE_IS]."
            )

    def close(self) -> None:
        try:
            self._transport.close()
        except Exception:
            pass
