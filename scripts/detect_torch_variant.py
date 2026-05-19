"""Определяет сборку PyTorch для install_deps.bat: cpu или cu128/cu126/...

Печатает одну строку ASCII (без кириллицы), чтобы cmd/for не ломал кодировку:
  variant|gpu_name|cuda_major|cuda_minor|status

status: ok | no_gpu | no_smi | no_cuda_ver | error
"""
from __future__ import annotations

import re
import subprocess
import sys


def detect() -> tuple[str, str, str, str, str]:
    """variant, gpu, cuda_major, cuda_minor, status"""
    try:
        q = subprocess.run(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        names = [ln.strip() for ln in (q.stdout or "").splitlines() if ln.strip()]
        if q.returncode != 0 or not names:
            return "cpu", "", "", "", "no_gpu"

        gpu = ", ".join(names[:2])
        if len(names) > 2:
            gpu += f" (+{len(names) - 2})"

        p = subprocess.run(["nvidia-smi"], capture_output=True, text=True, timeout=15)
        m = re.search(r"CUDA Version:\s*(\d+)\.(\d+)", p.stdout or "")
        if not m:
            return "cu128", gpu, "", "", "no_cuda_ver"

        maj, mn = int(m.group(1)), int(m.group(2))
        if (maj, mn) >= (12, 8):
            tag = "cu128"
        elif (maj, mn) >= (12, 6):
            tag = "cu126"
        elif (maj, mn) >= (12, 4):
            tag = "cu124"
        else:
            tag = "cu121"
        return tag, gpu, str(maj), str(mn), "ok"
    except FileNotFoundError:
        return "cpu", "", "", "", "no_smi"
    except Exception:
        return "cpu", "", "", "", "error"


def main() -> None:
    variant, gpu, maj, mn, status = detect()
    # Только ASCII — кириллицу добавляет install_deps.bat
    print(f"{variant}|{gpu}|{maj}|{mn}|{status}")


if __name__ == "__main__":
    main()
    sys.exit(0)
