#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

RUN_CMD="cd \"$PWD\" && ./scripts/tui.sh; echo; read -r -p \"Нажмите Enter, чтобы закрыть окно...\" _"

if command -v x-terminal-emulator >/dev/null 2>&1; then
  x-terminal-emulator -e bash -lc "$RUN_CMD"
elif command -v gnome-terminal >/dev/null 2>&1; then
  gnome-terminal -- bash -lc "$RUN_CMD"
elif command -v mate-terminal >/dev/null 2>&1; then
  mate-terminal -- bash -lc "$RUN_CMD"
elif command -v xfce4-terminal >/dev/null 2>&1; then
  xfce4-terminal -- bash -lc "$RUN_CMD"
elif command -v konsole >/dev/null 2>&1; then
  konsole -e bash -lc "$RUN_CMD"
else
  echo "Не нашёл терминал-эмулятор. Запускаю в текущем терминале:"
  bash -lc "$RUN_CMD"
fi
