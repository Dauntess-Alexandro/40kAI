#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

MODEL="${1:-None}"

# включаем "ручные кубы" и режим логов (лог в файл включится в play_terminal_manual.sh)
export MANUAL_DICE=1
export VERBOSE_LOGS=1

RUN_CMD="cd \"$PWD\" && ./play_terminal_manual.sh \"$MODEL\""

# Пытаемся открыть нормальный терминал (Mint обычно gnome-terminal)
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
