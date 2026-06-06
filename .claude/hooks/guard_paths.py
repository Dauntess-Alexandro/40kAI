#!/usr/bin/env python3
"""
PreToolUse hook (40kAI): защита критичных файлов от перезаписи агентом.

Блокирует Edit/Write/MultiEdit по двум группам путей:
  1) runtime/logs/LOGS_FOR_AGENTS_*.md — источник правды для отладки.
     По AGENTS.md формат логов переписывать нельзя (их пишет рантайм, не агент).
  2) runtime/state/*remote_is* и pc2-конфиги — LAN-настройки/секреты (в .gitignore).

Контракт хука Claude Code:
  - на stdin приходит JSON с полями tool_name и tool_input (в т.ч. file_path);
  - exit code 2 + текст в stderr  -> вызов БЛОКИРУЕТСЯ, текст уходит агенту;
  - exit code 0                   -> вызов разрешён.

Сообщение об ошибке: что случилось + где + что делать дальше (правило проекта).
"""
import json
import sys
from pathlib import PurePosixPath, PureWindowsPath

# Гарантируем UTF-8 для русских сообщений в stderr на Windows.
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# Паттерны защищённых путей (проверяем по нормализованному пути с '/').
PROTECTED = [
    # (подстрока-маркер, человекочитаемая причина, что делать)
    (
        "runtime/logs/logs_for_agents_",
        "это лог-файл «источник правды» для отладки (AGENTS.md)",
        "не переписывай его через Edit/Write. Логи пишет рантайм; "
        "если нужно поменять ФОРМАТ лога — правь код логирования "
        "(core/engine/logging_utils.py и места вызова), а не сам файл.",
    ),
    (
        "runtime/state/remote_is",
        "это конфиг remote inference server с LAN-настройками/секретами (в .gitignore)",
        "правь его вручную или через GUI/конфиг-генератор, не через агента.",
    ),
    (
        "runtime/state/pc2_remote",
        "это pc2-конфиг remote-сервера (в .gitignore, содержит сетевые параметры)",
        "правь его на ПК2 вручную или через tools/pc2_remote_*.bat, не через агента.",
    ),
]


def normalize(path: str) -> str:
    """Приводим путь к нижнему регистру со слэшами '/', чтобы матчить на любой ОС."""
    if not path:
        return ""
    # Учитываем и windows-, и posix-разделители.
    p = path.replace("\\", "/")
    try:
        # PureWindowsPath корректно разберёт и C:\..., и относительные пути.
        p = PureWindowsPath(path).as_posix()
    except Exception:
        p = PurePosixPath(path).as_posix() if "/" in path else p
    return p.lower()


def extract_paths(tool_input: dict) -> list[str]:
    """Достаём все целевые пути из tool_input (Edit/Write/MultiEdit)."""
    paths = []
    if not isinstance(tool_input, dict):
        return paths
    fp = tool_input.get("file_path")
    if isinstance(fp, str):
        paths.append(fp)
    # MultiEdit/прочее — на всякий случай собираем вложенные file_path.
    for key in ("edits", "files"):
        seq = tool_input.get(key)
        if isinstance(seq, list):
            for item in seq:
                if isinstance(item, dict) and isinstance(item.get("file_path"), str):
                    paths.append(item["file_path"])
    return paths


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        # Не смогли распарсить вход — не мешаем работе (fail-open).
        return 0

    tool_input = data.get("tool_input", {})
    for raw in extract_paths(tool_input):
        norm = normalize(raw)
        for marker, reason, what_to_do in PROTECTED:
            if marker in norm:
                sys.stderr.write(
                    "[40kAI guard] Правка ЗАБЛОКИРОВАНА.\n"
                    f"  Что: попытка изменить «{raw}».\n"
                    f"  Где: {reason}.\n"
                    f"  Что делать: {what_to_do}\n"
                )
                return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
