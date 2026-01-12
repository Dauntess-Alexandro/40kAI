#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
source .venv/bin/activate

export PYTHONPATH="$PWD/gym_mod:${PYTHONPATH:-}"
export MANUAL_DICE=1

MODEL="${1:-None}"

mkdir -p logs
LOGFILE="$PWD/logs/run_$(date +%F_%H-%M-%S).log"

# Если VERBOSE_LOGS=1 — сохраняем лог в файл + выводим в терминал
if [[ "${VERBOSE_LOGS:-0}" == "1" ]]; then
  python -u play.py "$MODEL" False 2>&1 | tee "$LOGFILE"
else
  python -u play.py "$MODEL" False
fi
