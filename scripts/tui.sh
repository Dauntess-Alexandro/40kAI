#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${PYTHON_BIN:-}" ]]; then
  if [[ -x "./.venv/bin/python" ]]; then
    PYTHON_BIN="./.venv/bin/python"
  elif [[ -x "./venv/bin/python" ]]; then
    PYTHON_BIN="./venv/bin/python"
  elif [[ -x "./env/bin/python" ]]; then
    PYTHON_BIN="./env/bin/python"
  else
    PYTHON_BIN="python"
  fi
fi
LOG_FILE="${TUI_LOG_FILE:-tui_launch.log}"

check_deps() {
  "$PYTHON_BIN" - <<'PY' >/dev/null 2>&1
import importlib
for name in ("rich", "textual"):
    importlib.import_module(name)
PY
}

if ! check_deps; then
  echo "TUI: не найдены зависимости (rich/textual) или неверный Python." | tee "$LOG_FILE"
  echo "Проверьте окружение: pip install -r requirements.txt" | tee -a "$LOG_FILE"
  echo "Можно задать PYTHON_BIN=/path/to/python" | tee -a "$LOG_FILE"
  read -r -p "Нажмите Enter, чтобы закрыть окно..." _
  exit 1
fi

echo "TUI: запуск наблюдателя..." > "$LOG_FILE"
if ! "$PYTHON_BIN" -m tui.watch "$@" 2>>"$LOG_FILE"; then
  echo "TUI: ошибка запуска, см. $LOG_FILE"
  read -r -p "Нажмите Enter, чтобы закрыть окно..." _
  exit 1
fi
