import subprocess
import sys
from pathlib import Path


def test_alphazero_grid_search_script_runs():
    root = Path(__file__).resolve().parents[2]
    script = root / "tools" / "grid_search_alphazero.py"
    proc = subprocess.run(
        [sys.executable, str(script), "1"],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
