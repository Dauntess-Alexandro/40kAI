#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ".venv/bin/activate"
export PYTHONPATH="$(pwd)/gym_mod:${PYTHONPATH:-}"
python -u train_alphazero.py
