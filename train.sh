#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source ".venv/bin/activate"

# ВАЖНО: заставляем Python брать пакет gym_mod из нужного места
export PYTHONPATH="$(pwd)/gym_mod:${PYTHONPATH:-}"

# Дефолты для ускорения обучения/чекпойнтов (не переопределяем, если заданы в окружении)
: "${NUM_ENVS:=16}"
: "${BATCH_ACT:=1}"
: "${USE_AMP:=1}"
: "${USE_COMPILE:=1}"
: "${PREFETCH:=1}"
: "${PIN_MEMORY:=1}"
: "${SAVE_EVERY:=200}"

export NUM_ENVS
export BATCH_ACT
export USE_AMP
export USE_COMPILE
export PREFETCH
export PIN_MEMORY
export SAVE_EVERY

python -u train.py
