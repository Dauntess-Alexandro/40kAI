from __future__ import annotations

from typing import Any, Callable, Optional


class RemoteTelemetryProbe:
    def __init__(
        self, *, host: str, port: int, auth_token: str = "", timeout: float = 2.0,
        health_fn: Optional[Callable[..., dict]] = None,
    ) -> None:
        self.host = str(host)
        self.port = int(port)
        self.auth_token = str(auth_token or "")
        self.timeout = float(timeout)
        if health_fn is not None:
            self._health_fn = health_fn
        else:
            from core.models.gmz_inference_transport import remote_health_check

            self._health_fn = remote_health_check

    def sample(self) -> Optional[dict[str, Any]]:
        try:
            hc = self._health_fn(
                host=self.host, port=self.port,
                auth_token=self.auth_token, timeout=self.timeout,
            )
        except Exception:
            return None
        if not isinstance(hc, dict) or str(hc.get("status", "")).lower() != "ok":
            return None
        return {
            "name": str(hc.get("gpu_name", "remote GPU")),
            "util": hc.get("gpu_util"),
            "mem_used_mb": hc.get("gpu_mem_used_mb"),
            "mem_total_mb": hc.get("gpu_mem_total_mb"),
            "proc_mem_mb": hc.get("gpu_mem_used_mb") or 0,
            "temp_c": hc.get("gpu_temp_c"),
            "avg_batch": hc.get("avg_batch"),
            "queue_depth": hc.get("queue_depth"),
            # P1: CPU/RAM ПК2 (None, если сервер старой версии — карточка не рисуется).
            "cpu_name": hc.get("cpu_name"),
            "cpu_pct_system": hc.get("cpu_pct_system"),
            "ram_pct_system": hc.get("ram_pct_system"),
            "ram_gb_system": hc.get("ram_gb_system"),
        }
