#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# venv
source .venv/bin/activate

# чтобы "python" внутри GUI был из venv
export PATH="$PWD/.venv/bin:$PATH"

# чтобы импортировался gym_mod из исходников
export PYTHONPATH="$PWD/gym_mod:$PYTHONPATH"

# ручные кубы
export MANUAL_DICE=1

# запускаем GUI
exec "$PWD/gui/build/Application"
