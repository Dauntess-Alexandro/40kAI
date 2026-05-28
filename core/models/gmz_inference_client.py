"""RPC client: env worker → GPU inference server (local or remote)."""

from __future__ import annotations

import time
from typing import Any

import numpy as np

from core.models.gmz_inference_protocol import build_infer_request
from core.models.gmz_inference_transport import InferenceTransport, LocalInferenceTransport


class GMZInferenceClient:
    """Отправляет obs/masks через transport, читает ответ."""

    def __init__(
        self,
        env_id: int,
        request_q: Any = None,
        reply_q: Any = None,
        *,
        transport: InferenceTransport | None = None,
        timeout: float = 5.0,
        max_retries: int = 2,
        auth_token: str = "",
    ) -> None:
        self.env_id = int(env_id)
        self.timeout = float(timeout)
        self.max_retries = max(1, int(max_retries))
        self._auth_token = str(auth_token or "")
        if transport is not None:
            self._transport = transport
        elif request_q is not None and reply_q is not None:
            self._transport = LocalInferenceTransport(request_q, reply_q)
        else:
            raise ValueError("GMZInferenceClient requires transport or request_q/reply_q")

    def infer(
        self,
        *,
        obs: np.ndarray,
        legal_masks_by_head: list[np.ndarray],
        step_in_episode: int,
        episode_id: int,
        is_new_episode: bool,
    ) -> dict[str, Any]:
        req = build_infer_request(
            env_id=self.env_id,
            obs=obs,
            legal_masks_by_head=legal_masks_by_head,
            step_in_episode=step_in_episode,
            episode_id=episode_id,
            is_new_episode=is_new_episode,
            auth_token=self._auth_token,
        )
        # Local path: raw dict without msgpack envelope (mp.Queue pickle).
        local_req = {
            "env_id": self.env_id,
            "step_in_episode": int(step_in_episode),
            "episode_id": int(episode_id),
            "obs": req["obs"],
            "legal_masks_by_head": req["legal_masks_by_head"],
            "is_new_episode": bool(is_new_episode),
        }
        use_wire = not isinstance(self._transport, LocalInferenceTransport)
        payload = req if use_wire else local_req

        last_exc: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                self._transport.send(payload)
                resp = self._transport.recv(self.timeout)
                if not isinstance(resp, dict):
                    raise TypeError(f"expected dict response, got {type(resp)}")
                if str(resp.get("kind", "")).strip().lower() == "infer_response":
                    return resp
                if "selected_actions" in resp:
                    return resp
                raise TypeError(f"unexpected infer response keys: {list(resp.keys())}")
            except Exception as exc:
                last_exc = exc
                time.sleep(0.05 * (attempt + 1))
        tag = "[GMZ][REMOTE_CLIENT]" if use_wire else "[GMZ][INF_CLIENT]"
        raise TimeoutError(
            f"{tag} env_id={self.env_id} timeout after {self.max_retries} tries"
        ) from last_exc

    def close(self) -> None:
        try:
            self._transport.close()
        except Exception:
            pass
