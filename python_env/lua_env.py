import json
import os
import socket
import subprocess
import sys
import time
from typing import Any, Dict, Optional, Tuple


class LuaEnv:
    def __init__(self, host_port: int = 8765, host_cmd: Optional[list] = None) -> None:
        self.host_port = host_port
        self.host_cmd = host_cmd or self._default_host_cmd()
        self.host_process: Optional[subprocess.Popen] = None
        self.sock: Optional[socket.socket] = None
        self.debug_enabled = os.getenv("PY_ENV_DEBUG") == "1"

    def _default_host_cmd(self) -> list:
        lua_exe = os.getenv("LUA_EXE")
        if lua_exe:
            return [lua_exe, os.path.join("lua_host", "host.lua")]
        return ["lua", os.path.join("lua_host", "host.lua")]

    def _log(self, message: str) -> None:
        if self.debug_enabled:
            print(f"[PY_ENV] {message}")

    def start_host(self) -> None:
        if self.host_process:
            return
        env = os.environ.copy()
        env["HOST_PORT"] = str(self.host_port)
        self._log(f"Starting host: {self.host_cmd}")
        self.host_process = subprocess.Popen(
            self.host_cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        time.sleep(0.2)

    def connect(self, timeout_s: float = 3.0) -> None:
        if self.sock:
            return
        deadline = time.time() + timeout_s
        last_err: Optional[Exception] = None
        while time.time() < deadline:
            try:
                self.sock = socket.create_connection(("127.0.0.1", self.host_port), timeout=timeout_s)
                self.sock.settimeout(timeout_s)
                self._log("Connected to host")
                return
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                time.sleep(0.1)
        raise RuntimeError(f"Не удалось подключиться к Lua-host: {last_err}")

    def _send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not self.sock:
            raise RuntimeError("Сокет не подключен")
        data = json.dumps(payload).encode("utf-8") + b"\n"
        self._log(f">> {payload}")
        self.sock.sendall(data)
        response = b""
        while not response.endswith(b"\n"):
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            response += chunk
        if not response:
            raise RuntimeError("Пустой ответ от Lua-host")
        decoded = json.loads(response.decode("utf-8"))
        self._log(f"<< {decoded}")
        if not decoded.get("ok", False):
            raise RuntimeError(decoded.get("error", "Неизвестная ошибка Lua-host"))
        return decoded

    def reset(self, seed: int = 1) -> Dict[str, Any]:
        if not self.host_process:
            self.start_host()
        if not self.sock:
            self.connect()
        resp = self._send({"cmd": "reset", "seed": seed})
        return resp["obs"]

    def step(self, action: Dict[str, Any]) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        resp = self._send({"cmd": "step", "action": action})
        return resp["obs"], resp["reward"], resp["done"], resp.get("info", {})

    def close(self) -> None:
        if self.sock:
            try:
                self._send({"cmd": "close"})
            except Exception:  # noqa: BLE001
                pass
            try:
                self.sock.close()
            except Exception:  # noqa: BLE001
                pass
            self.sock = None
        if self.host_process:
            try:
                self.host_process.terminate()
                self.host_process.wait(timeout=2)
            except Exception:  # noqa: BLE001
                self.host_process.kill()
            self.host_process = None


if __name__ == "__main__":
    env = LuaEnv()
    try:
        obs = env.reset(seed=123)
        print(obs)
    finally:
        env.close()
