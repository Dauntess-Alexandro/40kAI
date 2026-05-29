from __future__ import annotations

from typing import Any, Optional


def aggregate_tree(samples: list[dict[str, Any]], *, ncpu: int, total_ram: int) -> dict[str, Any]:
    """Свести список {cpu, rss} процессов дерева в нормализованные cpu_pct/ram."""
    if not samples:
        return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}
    cpu_sum = sum(float(s.get("cpu", 0.0)) for s in samples)
    rss_sum = sum(int(s.get("rss", 0)) for s in samples)
    ncpu = max(1, int(ncpu))
    cpu_pct = min(100.0, cpu_sum / ncpu)
    ram_gb = rss_sum / 1e9
    ram_pct = min(100.0, (rss_sum / float(total_ram)) * 100.0) if total_ram else 0.0
    return {"cpu_pct": cpu_pct, "ram_pct": ram_pct, "ram_gb": ram_gb, "ok": True}


class ProcessMeter:
    """Stateful: кэширует psutil.Process для корректного cpu_percent между тиками."""

    def __init__(self) -> None:
        self._cache: dict[int, Any] = {}
        self._psutil = None
        try:
            import psutil  # noqa: F401

            self._psutil = psutil
        except Exception:
            self._psutil = None

    def available(self) -> bool:
        return self._psutil is not None

    def sample(self, pid: Optional[int]) -> dict[str, Any]:
        ps = self._psutil
        if ps is None or pid is None:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}
        try:
            root = ps.Process(int(pid))
            procs = [root] + root.children(recursive=True)
        except Exception:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False}

        samples: list[dict[str, Any]] = []
        live_pids = set()
        for p in procs:
            live_pids.add(p.pid)
            cached = self._cache.get(p.pid)
            if cached is None:
                cached = p
                self._cache[p.pid] = p
                try:
                    cached.cpu_percent(None)  # прайминг, вернёт 0 в первый раз
                except Exception:
                    pass
            try:
                cpu = cached.cpu_percent(None)
                rss = cached.memory_info().rss
            except Exception:
                continue
            samples.append({"cpu": cpu, "rss": rss})
        # вычистить мёртвые pid'ы из кэша
        for dead in [k for k in self._cache if k not in live_pids]:
            self._cache.pop(dead, None)

        return aggregate_tree(samples, ncpu=ps.cpu_count() or 1, total_ram=ps.virtual_memory().total)
