#!/usr/bin/env python3
"""
PostToolUse hook (40kAI): автоматический ruff по только что отредактированному .py.

Запускает безопасные авто-фиксы ruff (`check --fix`) для одного файла, который
агент изменил через Edit/Write/MultiEdit. Форматирование (`ruff format`) НЕ
включаем по умолчанию, чтобы не плодить шумные диффы на коде без истории форматирования.

Поведение «не мешать»:
  - если ruff не установлен — тихо выходим (exit 0);
  - если файл не .py или его нет — выходим;
  - любые ошибки самого хука не должны ломать работу агента (fail-open).

Контракт: на stdin приходит JSON с tool_input.file_path. Возвращаем 0.
Если ruff что-то поправил — пишем короткую заметку в stderr (видна агенту).
"""
import json
import os
import shutil
import subprocess
import sys

# Гарантируем UTF-8 для русских сообщений в stderr на Windows.
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    tool_input = data.get("tool_input", {})
    file_path = tool_input.get("file_path") if isinstance(tool_input, dict) else None
    if not isinstance(file_path, str) or not file_path.endswith(".py"):
        return 0
    if not os.path.isfile(file_path):
        return 0

    ruff = shutil.which("ruff")
    if not ruff:
        # ruff не установлен — это нормально, просто пропускаем.
        return 0

    try:
        subprocess.run(
            [ruff, "check", "--fix", "--quiet", file_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        sys.stderr.write(f"[40kAI ruff] прогнал ruff --fix по {os.path.basename(file_path)}\n")
    except Exception:
        # Любая ошибка ruff не должна блокировать агента.
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
