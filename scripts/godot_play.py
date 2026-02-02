import json
import os
import time
from dataclasses import asdict
from typing import Optional

from gym_mod.engine.game_controller import GameController


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE_PATH = os.getenv("STATE_JSON_PATH", os.path.join(ROOT_DIR, "gui", "state.json"))
COMMAND_PATH = os.getenv("COMMAND_PATH", os.path.join(ROOT_DIR, "gui", "command.txt"))
REQUEST_PATH = os.getenv("REQUEST_PATH", os.path.join(ROOT_DIR, "gui", "request.json"))
POLL_INTERVAL = float(os.getenv("GODOT_POLL_INTERVAL", "0.2"))


def _write_request(request) -> None:
    if request is None:
        if os.path.exists(REQUEST_PATH):
            os.remove(REQUEST_PATH)
        return
    payload = asdict(request)
    os.makedirs(os.path.dirname(REQUEST_PATH), exist_ok=True)
    with open(REQUEST_PATH, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def _read_command() -> Optional[str]:
    if not os.path.exists(COMMAND_PATH):
        return None
    with open(COMMAND_PATH, "r", encoding="utf-8") as handle:
        lines = [line.strip() for line in handle.readlines() if line.strip()]
    if not lines:
        return None
    with open(COMMAND_PATH, "w", encoding="utf-8") as handle:
        handle.write("")
    return lines[-1]


def main() -> None:
    model_path = os.getenv("MODEL_PATH")
    if len(os.sys.argv) > 1 and os.sys.argv[1] != "None":
        model_path = os.sys.argv[1]
    controller = GameController(model_path=model_path or None, state_path=STATE_PATH)
    _, request = controller.start()
    _write_request(request)
    while True:
        if request is None and controller.is_finished:
            _write_request(None)
            break
        if request is None:
            time.sleep(POLL_INTERVAL)
            continue
        answer = _read_command()
        if answer is None:
            time.sleep(POLL_INTERVAL)
            continue
        _, request = controller.answer(answer)
        _write_request(request)


if __name__ == "__main__":
    main()
