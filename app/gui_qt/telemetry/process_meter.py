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
            # Прайминг системного cpu_percent: первый вызов всегда 0.0, делаем его сейчас,
            # чтобы первый tick уже отдавал осмысленную загрузку всей машины.
            try:
                psutil.cpu_percent(None)
            except Exception:
                pass
        except Exception:
            self._psutil = None

    def available(self) -> bool:
        return self._psutil is not None

    def _system_metrics(self) -> dict[str, Any]:
        """Загрузка всей машины (а не только дерева train) — для карточки CPU 'система'."""
        ps = self._psutil
        if ps is None:
            return {}
        try:
            vm = ps.virtual_memory()
            return {
                "cpu_pct_system": float(ps.cpu_percent(None)),
                "ram_pct_system": float(vm.percent),
                "ram_gb_system": float(vm.used) / 1e9,
            }
        except Exception:
            return {}

    def sample(self, pid: Optional[int]) -> dict[str, Any]:
        ps = self._psutil
        sys_metrics = self._system_metrics()
        if ps is None or pid is None:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False, **sys_metrics}
        try:
            root = ps.Process(int(pid))
            procs = [root] + root.children(recursive=True)
        except Exception:
            return {"cpu_pct": 0.0, "ram_pct": 0.0, "ram_gb": 0.0, "ok": False, **sys_metrics}

        samples: list[dict[str, Any]] = []
        live_pids: set[int] = set()
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

        result = aggregate_tree(samples, ncpu=ps.cpu_count() or 1, total_ram=ps.virtual_memory().total)
        result["pids"] = live_pids
        result.update(sys_metrics)
        return result
