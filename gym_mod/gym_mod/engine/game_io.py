from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List
import re
import os
import threading
import queue
import atexit
import time

from gym_mod.engine.io_profiler import get_io_profiler


LOG_DEFAULT_PATH = os.path.join(os.getcwd(), "gui", "response.txt")


class _AsyncLogWriter:
    def __init__(self) -> None:
        self._queue: queue.Queue = queue.Queue(maxsize=10000)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._worker, name="game-io-log-writer", daemon=True)
        self._thread.start()

    def submit(self, path: str, message: str) -> None:
        if message is None:
            return
        try:
            self._queue.put_nowait((path, message.rstrip("\n") + "\n"))
        except queue.Full:
            # Не блокируем игровой поток из-за переполнения очереди логов.
            return

    def _worker(self) -> None:
        batch_size = max(1, int(os.getenv("GUI_LOG_BATCH_SIZE", "32") or "32"))
        flush_interval = max(0.05, float(os.getenv("GUI_LOG_FLUSH_INTERVAL_SEC", "0.20") or "0.20"))
        pending: dict[str, list[str]] = {}
        last_flush = time.monotonic()

        while not self._stop.is_set() or not self._queue.empty():
            timeout = max(0.01, flush_interval - (time.monotonic() - last_flush))
            try:
                path, payload = self._queue.get(timeout=timeout)
                pending.setdefault(path, []).append(payload)
            except queue.Empty:
                pass

            buffered = sum(len(lines) for lines in pending.values())
            should_flush = buffered >= batch_size or (time.monotonic() - last_flush) >= flush_interval
            if not should_flush or not pending:
                continue

            for path, lines in pending.items():
                try:
                    os.makedirs(os.path.dirname(path), exist_ok=True)
                    with get_io_profiler().timed("log append"):
                        with open(path, "a", encoding="utf-8") as handle:
                            handle.writelines(lines)
                except OSError:
                    continue
            pending.clear()
            last_flush = time.monotonic()

    def shutdown(self) -> None:
        self._stop.set()
        self._thread.join(timeout=1.0)


_ASYNC_LOG_WRITER = _AsyncLogWriter()
atexit.register(_ASYNC_LOG_WRITER.shutdown)


@dataclass
class Request:
    kind: str
    prompt: str
    options: Optional[List[str]] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    count: Optional[int] = None
    meta: Optional[dict] = None


class BaseIO:
    def log(self, message: str) -> None:
        raise NotImplementedError

    def request_bool(self, prompt: str) -> Optional[bool]:
        raise NotImplementedError

    def request_int(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None):
        raise NotImplementedError

    def request_choice(self, prompt: str, options: list[str]):
        raise NotImplementedError

    def request_direction(self, prompt: str, options: list[str]):
        raise NotImplementedError

    def request_dice(
        self,
        prompt: str,
        count: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        raise NotImplementedError

    def request_deploy_coord(
        self,
        prompt: str,
        *,
        x_min: int,
        x_max: int,
        y_min: int,
        y_max: int,
    ):
        raise NotImplementedError


def parse_dice_values(text: str, count: int, min_value: int = 1, max_value: int = 6) -> list[int]:
    if text is None:
        raise ValueError("пустой ввод")
    stripped = text.strip()
    if not stripped:
        raise ValueError("пустой ввод")
    if stripped.isdigit() and len(stripped) == count:
        values = [int(ch) for ch in stripped]
    else:
        parts = [part for part in re.split(r"[,\s]+", stripped) if part]
        try:
            values = [int(part) for part in parts]
        except ValueError as exc:
            raise ValueError("есть нечисловые значения") from exc
    if len(values) != count:
        raise ValueError(f"ожидалось {count}, получено {len(values)}")
    for value in values:
        if value < min_value or value > max_value:
            raise ValueError(f"значение вне диапазона {min_value}..{max_value}")
    return values


def _append_log_line(message: str, path: Optional[str] = None) -> None:
    if message is None:
        return
    log_path = path or LOG_DEFAULT_PATH
    async_enabled = os.getenv("GUI_LOG_ASYNC_WRITE", "1") == "1"
    if async_enabled:
        _ASYNC_LOG_WRITER.submit(log_path, message)
        return

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with get_io_profiler().timed("log append"):
        with open(log_path, "a", encoding="utf-8") as handle:
            handle.write(message.rstrip("\n") + "\n")


class ConsoleIO(BaseIO):
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = log_path or LOG_DEFAULT_PATH

    def log(self, message: str) -> None:
        if message is None:
            return
        print(message)
        _append_log_line(message, self.log_path)

    def request_bool(self, prompt: str) -> Optional[bool]:
        while True:
            response = input(prompt).strip().lower()
            if response in ("y", "yes", "да", "д"):
                return True
            if response in ("n", "no", "нет", "н"):
                return False
            if response in ("q", "quit"):
                return None
            self.log("Неверный ввод: нужно Да/Нет.")

    def request_int(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None):
        while True:
            response = input(prompt).strip()
            if response.lower() in ("q", "quit"):
                return None
            try:
                value = int(response)
            except ValueError:
                self.log("Неверный ввод: нужно число.")
                continue
            if min_value is not None and value < min_value:
                self.log(f"Значение меньше минимума {min_value}.")
                continue
            if max_value is not None and value > max_value:
                self.log(f"Значение больше максимума {max_value}.")
                continue
            return value

    def request_choice(self, prompt: str, options: list[str]):
        response = input(prompt).strip()
        if response.lower() in ("q", "quit"):
            return None
        return response

    def request_direction(self, prompt: str, options: list[str]):
        response = input(prompt).strip().lower()
        if response in ("q", "quit"):
            return None
        return response

    def request_dice(
        self,
        prompt: str,
        count: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        min_val = 1 if min_value is None else min_value
        max_val = 6 if max_value is None else max_value
        while True:
            response = input(prompt).strip()
            if response.lower() in ("q", "quit"):
                return None
            try:
                return parse_dice_values(response, count=count, min_value=min_val, max_value=max_val)
            except ValueError:
                self.log(
                    f"Ошибка ввода кубов: нужно ввести {count} значений от {min_val} до {max_val}."
                )

    def request_deploy_coord(
        self,
        prompt: str,
        *,
        x_min: int,
        x_max: int,
        y_min: int,
        y_max: int,
    ):
        self.log(prompt)
        self.log(f"Допустимый диапазон: X={x_min}..{x_max}, Y={y_min}..{y_max}")
        while True:
            raw = input("Введите X,Y (например 10,5) или q для авто: ").strip()
            if raw.lower() in ("q", "quit"):
                return None
            parts = [p for p in re.split(r"[\s,;:]+", raw) if p]
            if len(parts) != 2:
                self.log("Неверный ввод: нужно два числа X и Y.")
                continue
            try:
                x = int(parts[0])
                y = int(parts[1])
            except ValueError:
                self.log("Неверный ввод: X и Y должны быть целыми числами.")
                continue
            return {"x": x, "y": y}


class GuiIO(BaseIO):
    def __init__(
        self,
        request_queue: queue.Queue,
        answer_queue: queue.Queue,
        log_path: Optional[str] = None,
    ):
        self.request_queue = request_queue
        self.answer_queue = answer_queue
        self.log_path = log_path or LOG_DEFAULT_PATH
        self._messages: list[str] = []
        self._lock = threading.Lock()

    def consume_messages(self) -> list[str]:
        with self._lock:
            messages = list(self._messages)
            self._messages.clear()
        return messages

    def log(self, message: str) -> None:
        if message is None:
            return
        with self._lock:
            self._messages.append(message)
        _append_log_line(message, self.log_path)

    def _wait_for_answer(self):
        return self.answer_queue.get()

    def request_bool(self, prompt: str) -> Optional[bool]:
        request = Request(kind="bool", prompt=prompt, options=["Да", "Нет"])
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if isinstance(answer, bool):
            return answer
        if isinstance(answer, str):
            lowered = answer.strip().lower()
            if lowered in ("y", "yes", "да", "д"):
                return True
            if lowered in ("n", "no", "нет", "н"):
                return False
            if lowered in ("q", "quit"):
                return None
        return None

    def request_int(self, prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None):
        request = Request(kind="int", prompt=prompt, min_value=min_value, max_value=max_value)
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if isinstance(answer, int):
            return answer
        if isinstance(answer, str):
            try:
                return int(answer.strip())
            except ValueError:
                return None
        return None

    def request_choice(self, prompt: str, options: list[str]):
        request = Request(kind="choice", prompt=prompt, options=list(options))
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if answer is None:
            return None
        return str(answer).strip()

    def request_direction(self, prompt: str, options: list[str]):
        request = Request(kind="direction", prompt=prompt, options=list(options))
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if answer is None:
            return None
        return str(answer).strip().lower()

    def request_dice(
        self,
        prompt: str,
        count: int,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
    ):
        request = Request(
            kind="dice",
            prompt=prompt,
            min_value=min_value,
            max_value=max_value,
            count=count,
        )
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if answer is None:
            return None
        if isinstance(answer, list):
            return answer
        if isinstance(answer, str):
            try:
                min_val = 1 if min_value is None else min_value
                max_val = 6 if max_value is None else max_value
                return parse_dice_values(answer, count=count, min_value=min_val, max_value=max_val)
            except ValueError:
                return None
        return None

    def request_deploy_coord(
        self,
        prompt: str,
        *,
        x_min: int,
        x_max: int,
        y_min: int,
        y_max: int,
    ):
        request = Request(
            kind="deploy_coord",
            prompt=prompt,
            min_value=x_min,
            max_value=x_max,
            meta={"x_min": x_min, "x_max": x_max, "y_min": y_min, "y_max": y_max},
        )
        self.request_queue.put(request)
        answer = self._wait_for_answer()
        if answer is None:
            return None
        if isinstance(answer, dict):
            try:
                return {"x": int(answer.get("x")), "y": int(answer.get("y"))}
            except (TypeError, ValueError):
                return None
        if isinstance(answer, (list, tuple)) and len(answer) >= 2:
            try:
                return {"x": int(answer[0]), "y": int(answer[1])}
            except (TypeError, ValueError):
                return None
        if isinstance(answer, str):
            parts = [p for p in re.split(r"[\s,;:]+", answer.strip()) if p]
            if len(parts) != 2:
                return None
            try:
                return {"x": int(parts[0]), "y": int(parts[1])}
            except ValueError:
                return None
        return None


_ACTIVE_IO: Optional[BaseIO] = None


def set_active_io(io: BaseIO) -> None:
    global _ACTIVE_IO
    _ACTIVE_IO = io


def get_active_io() -> BaseIO:
    global _ACTIVE_IO
    if _ACTIVE_IO is None:
        _ACTIVE_IO = ConsoleIO()
    return _ACTIVE_IO
