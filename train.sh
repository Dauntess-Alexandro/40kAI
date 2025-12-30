#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ".venv/bin/activate"

# ВАЖНО: заставляем Python брать пакет gym_mod из нужного места
export PYTHONPATH="$(pwd)/gym_mod:${PYTHONPATH:-}"

python -u train.py

