"""PC2 Launcher — чистая логика без Qt: роли, env, проверка SMB-шары.

Вынесено отдельно от Qt-контроллера, чтобы покрыть тестами (роли/порты/SMB).
Роли ПК2: запуск через существующие tools/pc2_*.bat (они сами делают setup/деривацию).
"""

from __future__ import annotations

import glob
import os
import tempfile
from dataclasses import dataclass


@dataclass(frozen=True)
class Pc2Role:
    """Роль ПК2 для лаунчера."""

    id: str
    label: str
    script: str  # путь к .bat относительно корня репо
    requires_gpu: bool
    port: int | None
    note: str


@dataclass(frozen=True)
class ShareCheck:
    """Результат проверки общей SMB-папки."""

    ok: bool
    exists: bool
    writable: bool
    has_weights: bool
    message: str


_ROLES: tuple[Pc2Role, ...] = (
    Pc2Role(
        id="dqn_actors",
        label="DQN актора (distributed)",
        script="tools/pc2_dqn_actors.bat",
        requires_gpu=False,
        port=5558,
        note="CPU env-воркеры → rollout на ПК1 (:5558). GPU не обязателен.",
    ),
    Pc2Role(
        id="az_actors",
        label="AZ актора (distributed)",
        script="tools/pc2_az_actors.bat",
        requires_gpu=False,
        port=5557,
        note="CPU env-воркеры AlphaZero → rollout на ПК1 (:5557).",
    ),
    Pc2Role(
        id="az_inference",
        label="AZ inference server (+ актора)",
        script="tools/pc2_remote_az_is.bat",
        requires_gpu=True,
        port=5555,
        note="GPU inference :5555. Не запускать вместе с GMZ inference (тот же порт).",
    ),
    Pc2Role(
        id="gmz_inference",
        label="GMZ inference server",
        script="tools/pc2_remote_is.bat",
        requires_gpu=True,
        port=5555,
        note="GPU inference :5555. Не запускать вместе с AZ inference (тот же порт).",
    ),
)


def pc2_roles() -> list[Pc2Role]:
    return list(_ROLES)


def resolve_role(role_id: str) -> Pc2Role | None:
    for r in _ROLES:
        if r.id == role_id:
            return r
    return None


def build_launch_env(share_root: str, base: dict[str, str] | None = None) -> dict[str, str]:
    """env для QProcess: ставим 40KAI_SHARE_ROOT, остальное .bat выводит сам."""
    env = dict(base if base is not None else os.environ)
    env["40KAI_SHARE_ROOT"] = str(share_root or "").strip()
    return env


def _actor_sync_of(share_root: str) -> str:
    base = str(share_root or "").rstrip("\\/")
    if os.path.basename(base).lower() == "actor_sync":
        return base
    return os.path.join(share_root, "actor_sync")


def validate_share_root(share_root: str) -> ShareCheck:
    """Проверка общей папки: существует / доступна на запись / есть ли веса."""
    path = str(share_root or "").strip()
    if not path:
        return ShareCheck(False, False, False, False, "Путь к общей папке не задан.")
    if not os.path.isdir(path):
        return ShareCheck(False, False, False, False, f"Папка недоступна или не существует: {path}")

    writable = False
    try:
        with tempfile.NamedTemporaryFile(dir=path, prefix=".40kai_smb_", delete=True):
            writable = True
    except OSError:
        writable = False

    actor_sync = _actor_sync_of(path)
    has_weights = bool(glob.glob(os.path.join(actor_sync, "latest_*.pth")))

    if not writable:
        msg = f"Папка видна, но без права записи (для весов нужно чтение; ПК1 пишет сам): {path}"
        return ShareCheck(True, True, False, has_weights, msg)

    weights_txt = "веса найдены" if has_weights else "весов пока нет (появятся при train на ПК1)"
    return ShareCheck(True, True, True, has_weights, f"Папка доступна ✓ ({weights_txt}).")
