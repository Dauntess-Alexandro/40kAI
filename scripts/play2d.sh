#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi

exec .venv/bin/python -m viewer2d
