#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
source .venv/bin/activate

export PYTHONPATH="$PWD/gym_mod:$PYTHONPATH"
export MANUAL_DICE=1

python -u play.py None False
