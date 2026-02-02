#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export PYTHONPATH="$(pwd)/gym_mod:${PYTHONPATH:-}"

python -u scripts/godot_play.py "${1:-None}"
