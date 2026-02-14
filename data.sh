#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ".venv/bin/activate"
python -u gym_mod/gym_mod/engine/initFile.py "$1" "$2" "$3" "$4" "$5" "${6:-only_war}"

