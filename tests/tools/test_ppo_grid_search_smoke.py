import subprocess
import sys
from pathlib import Path


def test_ppo_grid_search_smoke():
    root = Path(__file__).resolve().parents[2]
    script = root / "tools" / "ppo_grid_search.py"
    proc = subprocess.run(
        [sys.executable, str(script), "1"],
        cwd=str(root),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
