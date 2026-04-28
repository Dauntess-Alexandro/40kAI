from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent

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

AGENT_TRAIN_LOG_PATH = RUNTIME_LOGS_DIR / "LOGS_FOR_AGENTS_TRAIN.md"
AGENT_PLAY_LOG_PATH = RUNTIME_LOGS_DIR / "LOGS_FOR_AGENTS_PLAY.md"
RESULTS_PATH = ARTIFACTS_RESULTS_DIR / "results.txt"
BOARD_PATH = RUNTIME_STATE_DIR / "board.txt"
UNITS_PATH = RUNTIME_STATE_DIR / "units.txt"
STATE_JSON_PATH = RUNTIME_STATE_DIR / "state.json"
RESPONSE_PATH = RUNTIME_STATE_DIR / "response.txt"
TRAIN_DATA_PATH = RUNTIME_STATE_DIR / "data.json"


def ensure_runtime_dirs() -> None:
    for directory in (
        ARTIFACTS_MODELS_DIR,
        ARTIFACTS_METRICS_DIR,
        ARTIFACTS_RESULTS_DIR,
        RUNTIME_LOGS_DIR,
        RUNTIME_STATE_DIR,
        RUNTIME_CACHE_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)

