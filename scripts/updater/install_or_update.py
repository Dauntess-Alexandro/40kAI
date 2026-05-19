#!/usr/bin/env python3
"""Установка/обновление зависимостей 40kAI с отчётом SKIP / UPDATE / FAILED."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

TORCH_PACKAGES = ("torch", "torchvision", "torchaudio")
PYTORCH_CUDA_INDEX = "https://download.pytorch.org/whl/{tag}"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _log(msg: str, log_file: Path | None) -> None:
    line = msg.rstrip()
    print(line, flush=True)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def _run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _parse_requirements(path: Path) -> list[str]:
    names: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!\[;]", line, maxsplit=1)[0].strip()
        if name and name.lower() not in {p.lower() for p in TORCH_PACKAGES}:
            names.append(name)
    return names


def _detect_torch_variant(root: Path) -> str:
    script = root / "scripts" / "detect_torch_variant.py"
    if not script.is_file():
        return "cpu"
    proc = _run([sys.executable, str(script)])
    if proc.returncode != 0:
        return "cpu"
    first = (proc.stdout or "").strip().splitlines()[0]
    return first.split("|", 1)[0].strip() or "cpu"


def _ensure_venv(root: Path, system_python: str, log: Path | None) -> Path:
    venv_py = root / ".venv" / "Scripts" / "python.exe"
    if venv_py.is_file():
        _log("[updater] .venv уже есть", log)
        return venv_py
    _log("[updater] Создаю .venv ...", log)
    proc = _run([system_python, "-m", "venv", str(root / ".venv")], cwd=root)
    if proc.returncode != 0:
        raise RuntimeError(f"venv failed: {proc.stderr or proc.stdout}")
    if not venv_py.is_file():
        raise RuntimeError(".venv/Scripts/python.exe не создан")
    return venv_py


def _pip_outdated(venv_py: Path) -> set[str]:
    proc = _run([str(venv_py), "-m", "pip", "list", "--outdated", "--format=json"])
    if proc.returncode != 0:
        return set()
    try:
        data = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        return set()
    return {str(item.get("name", "")).lower() for item in data if item.get("name")}


def _pip_installed(venv_py: Path, package: str) -> bool:
    proc = _run([str(venv_py), "-m", "pip", "show", package])
    return proc.returncode == 0


def _install_one(venv_py: Path, package: str, *, extra_args: list[str] | None = None) -> str:
    cmd = [str(venv_py), "-m", "pip", "install", "-U", package]
    if extra_args:
        cmd.extend(extra_args)
    proc = _run(cmd)
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode != 0:
        return "FAILED"
    if "Successfully installed" in out or "Installing collected packages" in out:
        return "UPDATED"
    if "Requirement already satisfied" in out:
        return "SKIP"
    return "UPDATED" if proc.returncode == 0 else "FAILED"


def _needs_update(venv_py: Path, package: str, outdated: set[str]) -> bool:
    key = package.lower().replace("_", "-")
    normalized = package.lower()
    if normalized in outdated or key in outdated:
        return True
    return not _pip_installed(venv_py, package)


def _install_torch_stack(venv_py: Path, variant: str, log: Path | None) -> dict[str, str]:
    results: dict[str, str] = {}
    if variant.lower() == "cpu":
        _log("[updater] PyTorch: CPU (PyPI)", log)
        proc = _run(
            [str(venv_py), "-m", "pip", "install", "-U", *TORCH_PACKAGES],
        )
    else:
        tag = variant.lower()
        _log(f"[updater] PyTorch: CUDA {tag} (pytorch.org)", log)
        proc = _run(
            [
                str(venv_py),
                "-m",
                "pip",
                "install",
                "-U",
                "--force-reinstall",
                *TORCH_PACKAGES,
                "--index-url",
                PYTORCH_CUDA_INDEX.format(tag=tag),
            ],
        )
    out = (proc.stdout or "") + (proc.stderr or "")
    status = "UPDATED" if proc.returncode == 0 else "FAILED"
    if proc.returncode == 0 and "Requirement already satisfied" in out and "Successfully installed" not in out:
        status = "SKIP"
    for name in TORCH_PACKAGES:
        results[name] = status
    if proc.returncode != 0:
        _log(f"[updater] Ошибка torch: {proc.stderr or proc.stdout}", log)
    return results


def run(
    root: Path,
    *,
    torch_variant: str = "auto",
    non_interactive: bool = True,
    log_path: Path | None = None,
) -> int:
    if log_path and log_path.exists():
        log_path.write_text("", encoding="utf-8")

    req_file = root / "requirements_windows.txt"
    if not req_file.is_file():
        _log(f"[updater] Нет {req_file}", log_path)
        return 1

    system_python = sys.executable
    _log(f"[updater] Корень: {root}", log_path)
    _log(f"[updater] Python: {system_python}", log_path)

    try:
        venv_py = _ensure_venv(root, system_python, log_path)
    except RuntimeError as exc:
        _log(f"[updater] {exc}", log_path)
        return 1

    _log("[updater] Обновляю pip ...", log_path)
    proc = _run([str(venv_py), "-m", "pip", "install", "-U", "pip"])
    if proc.returncode != 0:
        _log("[updater] pip upgrade failed", log_path)
        return 1

    packages = _parse_requirements(req_file)
    outdated = _pip_outdated(venv_py)
    stats = {"SKIP": 0, "UPDATED": 0, "FAILED": 0}

    _log("[updater] Пакеты из requirements_windows.txt:", log_path)
    for pkg in packages:
        if not _needs_update(venv_py, pkg, outdated):
            stats["SKIP"] += 1
            _log(f"  [SKIP] {pkg} — установлен, актуален", log_path)
            continue
        _log(f"  [UPDATE] {pkg} ...", log_path)
        status = _install_one(venv_py, pkg)
        stats[status] = stats.get(status, 0) + 1
        _log(f"  [{status}] {pkg}", log_path)

    variant = torch_variant.strip().lower()
    if variant in ("", "auto"):
        variant = _detect_torch_variant(root)
        _log(f"[updater] PyTorch авто: {variant}", log_path)

    torch_results = _install_torch_stack(venv_py, variant, log_path)
    for name, status in torch_results.items():
        stats[status] = stats.get(status, 0) + 1
        _log(f"  [{status}] {name} (stack)", log_path)

    verify = _run(
        [
            str(venv_py),
            "-c",
            "import torch; print(torch.__version__); print('cuda', torch.cuda.is_available())",
        ],
        cwd=root,
    )
    if verify.returncode == 0:
        for line in (verify.stdout or "").strip().splitlines():
            _log(f"[updater] torch: {line}", log_path)
    else:
        _log("[updater] torch import check failed", log_path)

    _log(
        f"[updater] Итого: SKIP={stats.get('SKIP', 0)} "
        f"UPDATED={stats.get('UPDATED', 0)} FAILED={stats.get('FAILED', 0)}",
        log_path,
    )
    return 1 if stats.get("FAILED", 0) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="40kAI dependency installer/updater")
    parser.add_argument(
        "--root",
        type=Path,
        default=_repo_root(),
        help="Корень установки (каталог с train.py)",
    )
    parser.add_argument(
        "--torch-variant",
        default="auto",
        help="auto | cpu | cu128 | cu126 | cu124 | cu121",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Без интерактива (для Install.exe)",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="Файл лога (по умолчанию runtime/logs/install.log)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    log_path = args.log or (root / "runtime" / "logs" / "install.log")
    return run(
        root,
        torch_variant=args.torch_variant,
        non_interactive=args.yes,
        log_path=log_path,
    )


if __name__ == "__main__":
    sys.exit(main())
