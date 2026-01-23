#!/usr/bin/env bash
set -euo pipefail

if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

if [ -z "${DISPLAY:-}" ] && [ -z "${WAYLAND_DISPLAY:-}" ]; then
  export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-offscreen}"
fi

python -m viewer "$@"
status=$?

if [ $status -ne 0 ] && [ -z "${QT_QPA_PLATFORM:-}" ]; then
  echo "Viewer failed, retrying with QT_QPA_PLATFORM=offscreen..." >&2
  QT_QPA_PLATFORM=offscreen python -m viewer "$@"
  exit $?
fi

exit $status
