from __future__ import annotations

import os
import sys
from pathlib import Path


def _find_app_root(start: Path) -> Path:
    """Ищем каталог с train.py и project_paths.py (репо или Program Files\\40kAI)."""
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / "train.py").is_file() and (candidate / "project_paths.py").is_file():
            return candidate
    # запасной вариант: родитель папки 40kAI_GUI (старая логика Install.exe)
    if start.name.lower() == "40kai_gui":
        return start.parent
    return start


def _resolve_project_root() -> Path:
    """Корень установки: env 40KAI_INSTALL_ROOT, поиск от exe вверх, или каталог репозитория."""
    env_root = os.environ.get("40KAI_INSTALL_ROOT", "").strip()
    if env_root:
        return Path(env_root).resolve()
    if getattr(sys, "frozen", False):
        return _find_app_root(Path(sys.executable).resolve().parent)
    return Path(__file__).resolve().parent


def get_runtime_python(root: Path | None = None) -> str:
    """Python для train/eval/viewer: .venv в корне установки, иначе текущий интерпретатор."""
    base = root or PROJECT_ROOT
    venv_py = base / ".venv" / "Scripts" / "python.exe"
    if venv_py.is_file():
        return str(venv_py)
    return sys.executable


PROJECT_ROOT = _resolve_project_root()

# New canonical directories (clean-break layout)
APP_DIR = PROJECT_ROOT / "app"
CORE_DIR = PROJECT_ROOT / "core"
CONFIGS_DIR = PROJECT_ROOT / "configs"
DATA_DIR = PROJECT_ROOT / "data"
DOCS_DIR = PROJECT_ROOT / "docs"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
TESTS_DIR = PROJECT_ROOT / "tests"

ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
ARTIFACTS_MODELS_DIR = ARTIFACTS_DIR / "models"
ARTIFACTS_METRICS_DIR = ARTIFACTS_DIR / "metrics"
ARTIFACTS_RESULTS_DIR = ARTIFACTS_DIR / "results"

RUNTIME_DIR = PROJECT_ROOT / "runtime"
RUNTIME_LOGS_DIR = RUNTIME_DIR / "logs"
RUNTIME_STATE_DIR = RUNTIME_DIR / "state"
RUNTIME_CACHE_DIR = RUNTIME_DIR / "cache"
RUNTIME_TB_DIR = RUNTIME_DIR / "tb"  # event-файлы TensorBoard (в .gitignore)

AGENT_TRAIN_LOG_PATH = RUNTIME_LOGS_DIR / "LOGS_FOR_AGENTS_TRAIN.md"
AGENT_PLAY_LOG_PATH = RUNTIME_LOGS_DIR / "LOGS_FOR_AGENTS_PLAY.md"
AGENT_EVAL_LOG_PATH = RUNTIME_LOGS_DIR / "LOGS_FOR_AGENTS_EVAL.md"
RESULTS_PATH = ARTIFACTS_RESULTS_DIR / "results.txt"
BOARD_PATH = RUNTIME_STATE_DIR / "board.txt"
UNITS_PATH = RUNTIME_STATE_DIR / "units.txt"
STATE_JSON_PATH = RUNTIME_STATE_DIR / "state.json"
RESPONSE_PATH = RUNTIME_STATE_DIR / "response.txt"
TRAIN_DATA_PATH = RUNTIME_STATE_DIR / "data.json"


def resolve_share_models_root() -> str:
    """Корень общих моделей (локально или SMB-шара ПК1) — единая точка для ПК1↔ПК2.

    Приоритет env: ``40KAI_SHARE_ROOT`` → ``40KAI_MODELS_DIR`` → ``MODELS_DIR`` →
    локальный ``artifacts/models``. Резолвится динамически (на ПК2 переменные
    задаются после импорта). Forgiving: если путь указывает прямо на ``actor_sync``
    или ``agents`` — возвращаем родительский корень ``models``.
    """
    custom = ""
    for var in ("40KAI_SHARE_ROOT", "40KAI_MODELS_DIR", "MODELS_DIR"):
        val = str(os.getenv(var, "") or "").strip()
        if val:
            custom = val
            break
    if not custom:
        return str(ARTIFACTS_MODELS_DIR)
    base = custom.rstrip("\\/")
    if base.endswith(":"):
        # Корень mapped-диска (Z:\) — без хвостового слэша станет drive-relative.
        return base + os.sep
    if os.path.basename(base).lower() in {"actor_sync", "agents"}:
        parent = os.path.dirname(base)
        if not parent:
            return base
        # Убираем хвостовой разделитель от dirname, но сохраняем корень диска (X:\).
        stripped = parent.rstrip("\\/")
        return stripped if stripped and not stripped.endswith(":") else parent
    return base


def share_actor_sync_dir() -> str:
    """Папка ``actor_sync`` в общем корне моделей (веса/контекст/stop.flag на SMB)."""
    return os.path.join(resolve_share_models_root(), "actor_sync")


def ensure_runtime_dirs() -> None:
    for directory in (
        ARTIFACTS_MODELS_DIR,
        ARTIFACTS_METRICS_DIR,
        ARTIFACTS_RESULTS_DIR,
        RUNTIME_LOGS_DIR,
        RUNTIME_STATE_DIR,
        RUNTIME_CACHE_DIR,
        RUNTIME_TB_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)

