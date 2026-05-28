"""RPC client: env worker → GPU inference server."""

from __future__ import annotations

import time
from typing import Any

import numpy as np


class GMZInferenceClient:
    """Отправляет obs/masks в request_q, читает ответ из private reply_q."""

    def __init__(
        self,
        env_id: int,
        request_q: Any,
        reply_q: Any,
        *,
        timeout: float = 5.0,
        max_retries: int = 2,
    ) -> None:
        self.env_id = int(env_id)
        self.request_q = request_q
        self.reply_q = reply_q
        self.timeout = float(timeout)
        self.max_retries = max(1, int(max_retries))

    def infer(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        step_in_episode: int,
        episode_id: int,
        is_new_episode: bool,
    ) -> dict[str, Any]:
        req = {
            "env_id": self.env_id,
            "step_in_episode": int(step_in_episode),
            "episode_id": int(episode_id),
            "obs": np.asarray(obs, dtype=np.float32),
            "legal_masks_by_head": [np.asarray(m) for m in legal_masks_by_head],
            "is_new_episode": bool(is_new_episode),
        }
        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                self.request_q.put(req)
                resp = self.reply_q.get(timeout=self.timeout)
                if not isinstance(resp, dict):
                    raise TypeError(f"expected dict response, got {type(resp)}")
                return resp
            except Exception as exc:
                last_exc = exc
                time.sleep(0.05 * (attempt + 1))
        raise TimeoutError(
            f"[GMZ][INF_CLIENT] env_id={self.env_id} timeout after {self.max_retries} tries"
        ) from last_exc
