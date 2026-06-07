"""
TBLogger — единый тонкий враппер над TensorBoard для всех алгоритмов 40kAI
(DQN/PPO в train.py, AlphaZero, Gumbel MuZero).

Зачем: дать живые кривые обучения и сравнение прогонов поверх существующих
CSV/PNG (их не трогаем — TB добавляется рядом).

Принципы:
  - **no-op, если выключено или нет tensorboard.** Любой сбой при логировании
    не должен ронять обучение (fail-safe). Включение: env `TB_ENABLED` (по умолчанию "1").
  - Логи пишутся в `runtime/tb/<run_id>/` — этот каталог в .gitignore.
  - Скаляры группируются префиксами: `episode/*`, `train/*`, `sys/*` — так они
    раскладываются по секциям в UI TensorBoard.

Использование:
    from core.telemetry.tb_logger import make_tb_logger
    tb = make_tb_logger(run_id, algo="dqn")
    tb.log_episode(ep_row, step=episode_idx)
    tb.log_train({"loss": loss_val, "lr": lr}, step=global_step)
    tb.log_telemetry(step=global_step)
    ...
    tb.close()
"""
from __future__ import annotations

import os
from collections.abc import Mapping

from project_paths import RUNTIME_TB_DIR


def _tb_enabled() -> bool:
    """TB включён, если env TB_ENABLED не выключает явно (0/false/no)."""
    val = os.getenv("TB_ENABLED", "1").strip().lower()
    return val not in ("0", "false", "no", "off", "")


class TBLogger:
    """Тонкая обёртка над torch.utils.tensorboard.SummaryWriter.

    Все методы безопасны: если writer не создан (выключено/нет пакета) или
    при записи возникла ошибка — молча ничего не делаем, обучение не падает.
    """

    def __init__(self, run_id: str, algo: str | None = None, *, enabled: bool | None = None):
        self.run_id = run_id
        self.algo = algo or "run"
        self._writer = None
        self._gpu = None  # ленивый GpuBackend
        self._psutil = None
        self.logdir: str | None = None

        if enabled is None:
            enabled = _tb_enabled()
        if not enabled:
            return

        try:
            from torch.utils.tensorboard import SummaryWriter  # требует пакет tensorboard
        except Exception as exc:  # pragma: no cover — окружение без tensorboard
            print(
                "[TB] TensorBoard отключён: не удалось импортировать SummaryWriter "
                f"({exc}). Установи пакет `tensorboard` или выстави TB_ENABLED=0. "
                "Обучение продолжится без TB-логов."
            )
            return

        try:
            self.logdir = os.path.join(str(RUNTIME_TB_DIR), self.algo, run_id)
            os.makedirs(self.logdir, exist_ok=True)
            self._writer = SummaryWriter(log_dir=self.logdir)
            print(f"[TB] логи пишутся в {self.logdir} (смотреть: tensorboard --logdir runtime/tb)")
        except Exception as exc:
            print(f"[TB] не удалось создать SummaryWriter в {self.logdir}: {exc}. TB-логи выключены.")
            self._writer = None

    # ------------------------------------------------------------------ базовое
    @property
    def active(self) -> bool:
        return self._writer is not None

    def log_scalar(self, tag: str, value, step: int) -> None:
        if self._writer is None or value is None:
            return
        try:
            self._writer.add_scalar(tag, float(value), int(step))
        except Exception:
            # Один битый скаляр не должен ломать обучение.
            pass

    def log_scalars(self, prefix: str, mapping: Mapping[str, object], step: int) -> None:
        if self._writer is None or not mapping:
            return
        pfx = prefix.rstrip("/")
        for key, value in mapping.items():
            if value is None:
                continue
            self.log_scalar(f"{pfx}/{key}", value, step)

    # ------------------------------------------------------------- доменные хелперы
    def log_episode(self, row: Mapping[str, object], step: int) -> None:
        """Скаляры одного эпизода (формат ep_rows из train.save_extra_metrics)."""
        if self._writer is None or not row:
            return
        result = row.get("result")
        win = 1.0 if result == "win" else 0.0
        payload = {
            "reward": row.get("ep_reward"),
            "length": row.get("ep_len"),
            "turn": row.get("turn"),
            "vp_diff": row.get("vp_diff"),
            "model_vp": row.get("model_vp"),
            "player_vp": row.get("player_vp"),
            "win": win,
        }
        self.log_scalars("episode", payload, step)

    def log_train(self, mapping: Mapping[str, object], step: int) -> None:
        """Тренировочные величины: лоссы, learning rate и т.п."""
        self.log_scalars("train", mapping, step)

    def log_telemetry(self, step: int) -> None:
        """CPU/RAM (psutil) + GPU (GpuBackend) как скаляры под sys/*."""
        if self._writer is None:
            return
        # CPU / RAM
        try:
            if self._psutil is None:
                import psutil  # локальный импорт, чтобы не тянуть при no-op
                self._psutil = psutil
            ps = self._psutil
            self.log_scalar("sys/cpu_percent", ps.cpu_percent(interval=None), step)
            vm = ps.virtual_memory()
            self.log_scalar("sys/ram_used_mb", vm.used / (1024 * 1024), step)
            self.log_scalar("sys/ram_percent", vm.percent, step)
        except Exception:
            pass
        # GPU
        try:
            if self._gpu is None:
                from core.telemetry.gpu_backend import GpuBackend
                self._gpu = GpuBackend()
            if self._gpu.available():
                for dev in self._gpu.read_devices():
                    i = dev.index
                    self.log_scalar(f"sys/gpu{i}_util", dev.util, step)
                    self.log_scalar(f"sys/gpu{i}_mem_used_mb", dev.mem_used_mb, step)
                    self.log_scalar(f"sys/gpu{i}_temp_c", dev.temp_c, step)
        except Exception:
            pass

    def flush(self) -> None:
        if self._writer is None:
            return
        try:
            self._writer.flush()
        except Exception:
            pass

    def close(self) -> None:
        if self._writer is None:
            return
        try:
            self._writer.flush()
            self._writer.close()
        except Exception:
            pass
        finally:
            self._writer = None


def make_tb_logger(run_id: str, algo: str | None = None, *, enabled: bool | None = None) -> TBLogger:
    """Фабрика TBLogger. Возвращает рабочий или no-op логгер — вызовы всегда безопасны."""
    return TBLogger(run_id, algo=algo, enabled=enabled)


# --- Реестр логгеров по run_id ------------------------------------------------
# Позволяет единожды встроить TB в общую функцию (например, append_episode_diagnostics)
# и переиспользовать один writer на весь прогон без проброса объекта через сигнатуры.
_REGISTRY: dict[str, TBLogger] = {}


def get_tb_logger(run_id: str, algo: str | None = None) -> TBLogger:
    """Вернуть (создав при первом обращении) TBLogger для данного run_id."""
    key = str(run_id)
    tb = _REGISTRY.get(key)
    if tb is None:
        tb = TBLogger(key, algo=algo)
        _REGISTRY[key] = tb
    return tb


def close_tb_logger(run_id: str) -> None:
    """Закрыть и убрать из реестра логгер прогона (вызывать в конце обучения)."""
    tb = _REGISTRY.pop(str(run_id), None)
    if tb is not None:
        tb.close()


def _close_all_tb_loggers() -> None:
    """Закрыть все логгеры при выходе процесса — гарантирует flush event-файлов."""
    for tb in list(_REGISTRY.values()):
        try:
            tb.close()
        except Exception:
            pass
    _REGISTRY.clear()


import atexit as _atexit  # noqa: E402

_atexit.register(_close_all_tb_loggers)
