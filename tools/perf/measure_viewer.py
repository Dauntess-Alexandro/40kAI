#!/usr/bin/env python3
"""Viewer frametime harness (migration Sprint 1).

Instrument ``OpenGLBoardWidget.paintGL`` when ``VIEWER_PERF_INSTRUMENT`` is set;
this script launches ``python -m app.viewer``, waits, terminates the process,
and collects ``[VIEWER_PERF]`` lines from stdout/stderr.

Example (repo root, venv activated)::

    python tools/perf/measure_viewer.py --duration 20 --state runtime/state/state.json

Append results into the baseline doc::

    python tools/perf/measure_viewer.py --duration 20 --append-docs docs/viewer_baseline_metrics.md

Requires a display / GL context where the viewer can render; headless setups may fail.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import textwrap
import time
from datetime import datetime, timezone
from pathlib import Path


_PERF_LINE = re.compile(r"\[VIEWER_PERF\]\s+samples=(?P<n>\d+)\s+p50_ms=(?P<p50>[\d.]+)\s+p95_ms=(?P<p95>[\d.]+)")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure viewer frametimes via VIEWER_PERF_INSTRUMENT.")
    parser.add_argument("--duration", type=float, default=25.0, help="Seconds to run before terminate.")
    parser.add_argument("--state", type=str, default="", help="Optional path passed to viewer --state.")
    parser.add_argument("--python", type=str, default=sys.executable, help="Python interpreter.")
    parser.add_argument(
        "--append-docs",
        type=str,
        default="",
        help="If set, append a markdown snippet to this file (repo-relative or absolute).",
    )
    args = parser.parse_args()

    root = _repo_root()
    env = os.environ.copy()
    env["VIEWER_PERF_INSTRUMENT"] = "1"
    env.setdefault("PYTHONUTF8", "1")

    cmd = [args.python, "-m", "app.viewer"]
    if args.state:
        cmd.extend(["--state", str(Path(args.state).resolve())])

    print("[measure_viewer] cwd=", root)
    print("[measure_viewer] cmd=", " ".join(cmd))
    print("[measure_viewer] duration_s=", args.duration)

    creation_flags = 0
    if sys.platform.startswith("win"):
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]

    proc = subprocess.Popen(
        cmd,
        cwd=str(root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=creation_flags,
    )
    try:
        time.sleep(max(0.5, args.duration))
        if proc.poll() is None:
            proc.terminate()
        out, _ = proc.communicate(timeout=45)
    except subprocess.TimeoutExpired:
        proc.kill()
        out, _ = proc.communicate()
    finally:
        if proc.poll() is None:
            proc.kill()

    lines_out = out.splitlines() if out else []
    for ln in lines_out:
        if "[VIEWER_PERF]" in ln:
            print(ln, flush=True)

    perf_lines = [ln for ln in lines_out if "[VIEWER_PERF]" in ln]
    parsed: list[dict[str, str]] = []
    for ln in perf_lines:
        m = _PERF_LINE.search(ln)
        if m:
            parsed.append(m.groupdict())

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    snippet = textwrap.dedent(
        f"""
        ### Auto-run {stamp}

        - Command: `{" ".join(cmd)}`
        - Duration requested: {args.duration}s
        - Raw perf lines: {len(perf_lines)}
        - Parsed samples: {len(parsed)}
        """
    ).strip()
    if parsed:
        last = parsed[-1]
        snippet += (
            f"\n- Last line: samples={last['n']} p50_ms={last['p50']} p95_ms={last['p95']}\n"
        )
    else:
        snippet += "\n- **Note:** No `[VIEWER_PERF]` lines captured (GPU/display/offscreen?). Fill manually.\n"

    print("\n--- snippet ---\n" + snippet + "\n---------------\n")

    if args.append_docs:
        doc_path = Path(args.append_docs)
        if not doc_path.is_absolute():
            doc_path = root / doc_path
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        with doc_path.open("a", encoding="utf-8") as handle:
            handle.write("\n\n" + snippet + "\n")

    code = proc.returncode
    if code is None:
        return 0
    # Terminated viewer often exits with non-zero; treat as OK for harness.
    if code in (0, 1, -15, 15):
        return 0
    return code


if __name__ == "__main__":
    raise SystemExit(main())
