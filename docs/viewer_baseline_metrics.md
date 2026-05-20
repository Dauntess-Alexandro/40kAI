# Viewer baseline metrics (migration Sprint 1)

This file captures **repeatable performance snapshots** for the PySide6 viewer. Numbers are filled manually or appended by `tools/perf/measure_viewer.py`.

## Reference machine (fill before comparing PRs)

| Field | Value |
|---|---|
| Date | |
| OS | |
| Display resolution | |
| Windows scale / DPI % | |
| GPU | |
| Driver | |
| CPU | |
| Python | |
| PySide6 version | |

## Scenario definition

Describe how you drove the viewer (fresh match / replay / idle board):

-

## Measurements

| Scenario | FPS / frametime | Notes |
|---|---|---|
| Idle board | | |
| Mid-movement highlights | | |
| Shooting FX on | | |
| Long log tail | | |

### Automated frametime sampling

Enable env **`VIEWER_PERF_INSTRUMENT=1`** before launch. The board emits lines:

```text
[VIEWER_PERF] samples=<n> p50_ms=... p95_ms=...
```

Optional env:

- **`VIEWER_PERF_REPORT_FRAMES`** — emit every N painted frames (default `300`).

Run harness from repo root:

```powershell
python tools/perf/measure_viewer.py --duration 25 --state runtime/state/state.json --append-docs docs/viewer_baseline_metrics.md
```

---

<!-- Auto-generated snippets appended below -->
