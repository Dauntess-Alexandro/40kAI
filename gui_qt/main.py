import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import deque
from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore, QtGui, QtQml


@dataclass
class RosterEntry:
    name: str
    count: int
    instance_id: str


@dataclass
class UnitInfo:
    name: str
    faction: str
    default_count: int


class GUIController(QtCore.QObject):
    logLine = QtCore.Signal(str)
    statusChanged = QtCore.Signal(str)
    runningChanged = QtCore.Signal(bool)
    progressValueChanged = QtCore.Signal(float)
    progressLabelChanged = QtCore.Signal(str)
    progressStatsChanged = QtCore.Signal(str)
    progressTextChanged = QtCore.Signal(str)
    rosterSummaryChanged = QtCore.Signal(str)
    numGamesChanged = QtCore.Signal(int)
    boardXChanged = QtCore.Signal(int)
    boardYChanged = QtCore.Signal(int)
    metricsChanged = QtCore.Signal()
    metricsLabelChanged = QtCore.Signal(str)
    playModelPathChanged = QtCore.Signal(str)
    playModelLabelChanged = QtCore.Signal(str)
    boardTextChanged = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process: Optional[QtCore.QProcess] = None
        self._running = False
        self._repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        self._progress_value = 0.0
        self._progress_label = "ep=0/0 (0%)"
        self._progress_stats = "— it/s • elapsed 00:00"
        self._progress_text = "0%"

        self._num_games = 100
        self._board_x = 60
        self._board_y = 40

        self._train_total_episodes = 0
        self._training_samples = deque()
        self._training_start_time = 0.0
        self._training_last_ui_update = 0.0

        self._available_units: list[UnitInfo] = []
        self._player_roster: list[RosterEntry] = []
        self._model_roster: list[RosterEntry] = []
        self._instance_counter = 1

        self._available_model = QtCore.QStringListModel()
        self._player_model = QtCore.QStringListModel()
        self._model_model = QtCore.QStringListModel()

        self._metrics_defaults = self._build_default_metrics()
        self._metrics_files = dict(self._metrics_defaults)
        self._metrics_paths = self._build_metrics_paths(self._metrics_files, cache_token=self._cache_token())
        self._metrics_mtimes: dict[str, Optional[float]] = {}
        self._metrics_label = "По умолчанию"

        self._play_model_path = ""
        self._play_model_label = "Модель не выбрана"
        self._board_text = "ASCII карта будет доступна после запуска игры."

        self._load_available_units()
        self._load_rosters_from_file()
        self._refresh_models()
        self._select_latest_metrics()
        self._select_latest_play_model(initial=True)
        self._update_roster_summary()

        self._emit_status("Нажмите Train, чтобы запустить обучение.")

    @QtCore.Property(QtCore.QObject, constant=True)
    def availableUnitsModel(self) -> QtCore.QObject:
        return self._available_model

    @QtCore.Property(QtCore.QObject, constant=True)
    def playerRosterModel(self) -> QtCore.QObject:
        return self._player_model

    @QtCore.Property(QtCore.QObject, constant=True)
    def modelRosterModel(self) -> QtCore.QObject:
        return self._model_model

    @QtCore.Property(bool, notify=runningChanged)
    def running(self) -> bool:
        return self._running

    @QtCore.Property(float, notify=progressValueChanged)
    def progressValue(self) -> float:
        return self._progress_value

    @QtCore.Property(str, notify=progressLabelChanged)
    def progressLabel(self) -> str:
        return self._progress_label

    @QtCore.Property(str, notify=progressStatsChanged)
    def progressStats(self) -> str:
        return self._progress_stats

    @QtCore.Property(str, notify=progressTextChanged)
    def progressText(self) -> str:
        return self._progress_text

    @QtCore.Property(str, notify=rosterSummaryChanged)
    def rosterSummary(self) -> str:
        return self._roster_summary

    @QtCore.Property(int, notify=numGamesChanged)
    def numGames(self) -> int:
        return self._num_games

    @QtCore.Property(int, notify=boardXChanged)
    def boardX(self) -> int:
        return self._board_x

    @QtCore.Property(int, notify=boardYChanged)
    def boardY(self) -> int:
        return self._board_y

    @QtCore.Property(str, notify=metricsChanged)
    def metricsRewardPath(self) -> str:
        return self._metrics_paths["reward"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsLossPath(self) -> str:
        return self._metrics_paths["loss"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsEpLenPath(self) -> str:
        return self._metrics_paths["epLen"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsWinratePath(self) -> str:
        return self._metrics_paths["winrate"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsVpDiffPath(self) -> str:
        return self._metrics_paths["vpdiff"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsEndReasonPath(self) -> str:
        return self._metrics_paths["endreasons"]

    @QtCore.Property(str, notify=metricsLabelChanged)
    def metricsLabel(self) -> str:
        return self._metrics_label

    @QtCore.Property(str, notify=playModelPathChanged)
    def playModelPath(self) -> str:
        return self._play_model_path

    @QtCore.Property(str, notify=playModelLabelChanged)
    def playModelLabel(self) -> str:
        return self._play_model_label

    @QtCore.Property(str, notify=boardTextChanged)
    def boardText(self) -> str:
        return self._board_text

    @QtCore.Property(str, constant=True)
    def modelsFolderUrl(self) -> str:
        return self._to_file_url(os.path.join(self._repo_root, "models"))

    @QtCore.Slot(int)
    def set_num_games(self, value: int) -> None:
        if value <= 0:
            self._emit_status("Количество игр должно быть больше нуля.")
            return
        if self._num_games != value:
            self._num_games = value
            self.numGamesChanged.emit(value)

    @QtCore.Slot(int)
    def set_board_x(self, value: int) -> None:
        if value <= 0:
            self._emit_status("X должен быть больше нуля.")
            return
        if self._board_x != value:
            self._board_x = value
            self.boardXChanged.emit(value)

    @QtCore.Slot(int)
    def set_board_y(self, value: int) -> None:
        if value <= 0:
            self._emit_status("Y должен быть больше нуля.")
            return
        if self._board_y != value:
            self._board_y = value
            self.boardYChanged.emit(value)

    @QtCore.Slot()
    def increment_board_x(self) -> None:
        self.set_board_x(self._board_x + 10)

    @QtCore.Slot()
    def decrement_board_x(self) -> None:
        self.set_board_x(max(10, self._board_x - 10))

    @QtCore.Slot()
    def increment_board_y(self) -> None:
        self.set_board_y(self._board_y + 10)

    @QtCore.Slot()
    def decrement_board_y(self) -> None:
        self.set_board_y(max(10, self._board_y - 10))

    @QtCore.Slot(int)
    def add_unit_to_player(self, index: int) -> None:
        if index < 0 or index >= len(self._available_units):
            self._emit_status("Сначала выберите юнит в списке доступных.")
            return
        unit = self._available_units[index]
        entry = self._create_roster_entry(unit)
        self._player_roster.append(entry)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Юнит добавлен в ростер игрока.")

    @QtCore.Slot(int)
    def add_unit_to_model(self, index: int) -> None:
        if index < 0 or index >= len(self._available_units):
            self._emit_status("Сначала выберите юнит в списке доступных.")
            return
        unit = self._available_units[index]
        entry = self._create_roster_entry(unit)
        self._model_roster.append(entry)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Юнит добавлен в ростер модели.")

    @QtCore.Slot(int)
    def remove_player_unit(self, index: int) -> None:
        if index < 0 or index >= len(self._player_roster):
            self._emit_status("Сначала выберите юнит игрока для удаления.")
            return
        self._player_roster.pop(index)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Юнит удалён из ростера игрока.")

    @QtCore.Slot(int)
    def remove_model_unit(self, index: int) -> None:
        if index < 0 or index >= len(self._model_roster):
            self._emit_status("Сначала выберите юнит модели для удаления.")
            return
        self._model_roster.pop(index)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Юнит удалён из ростера модели.")

    @QtCore.Slot()
    def clear_player_roster(self) -> None:
        self._player_roster.clear()
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Ростер игрока очищен.")

    @QtCore.Slot()
    def clear_model_roster(self) -> None:
        self._model_roster.clear()
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._emit_status("Ростер модели очищен.")

    @QtCore.Slot()
    def start_train(self) -> None:
        self._start_training(mode="train")

    @QtCore.Slot()
    def start_train_8x(self) -> None:
        self._start_training(mode="train8")

    @QtCore.Slot()
    def start_self_play(self) -> None:
        self._start_training(mode="selfplay")

    @QtCore.Slot()
    def stop_process(self) -> None:
        if self._process is None:
            self._emit_status("Нет активного процесса для остановки.")
            return
        self._emit_log("[GUI] Останавливаю процесс...", level="INFO")
        self._process.terminate()
        if not self._process.waitForFinished(3000):
            self._emit_log("[GUI] Процесс не завершился, принудительное завершение.", level="WARN")
            self._process.kill()
        self._cleanup_process()

    @QtCore.Slot()
    def clear_model_cache(self) -> None:
        try:
            self._clear_cache_files()
            self._emit_status("Кэш моделей и LOGS_FOR_AGENTS.md очищены.")
            self._emit_log("[GUI] Кэш моделей и LOGS_FOR_AGENTS.md очищены.")
        except OSError as exc:
            message = (
                "Не удалось очистить кэш (gui_qt/main.py): "
                "проверьте права доступа и повторите."
            )
            self._emit_status(message)
            self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")

    @QtCore.Slot(str)
    def select_metrics_file(self, file_url: str) -> None:
        path = self._to_local_file(file_url)
        if not path:
            self._emit_status("Файл метрик не выбран.")
            return
        if not os.path.exists(path):
            self._emit_status("Файл модели не найден. Проверьте путь.")
            return
        metrics_id = self._extract_metrics_id(path)
        if not metrics_id:
            self._emit_status("Не удалось определить ID метрик из имени файла.")
            return
        json_path = os.path.join(self._repo_root, "models", f"data_{metrics_id}.json")
        if not os.path.exists(json_path):
            self._emit_status("Файл метрик не найден в models/.")
            self._emit_log(f"[GUI] metrics json не найден: {json_path}", level="WARN")
            return
        if not self._load_metrics_from_json(json_path):
            return
        self._metrics_label = f"Файл: {os.path.basename(path)}"
        self.metricsLabelChanged.emit(self._metrics_label)
        self._emit_status("Метрики обновлены.")

    @QtCore.Slot()
    def select_latest_metrics(self) -> None:
        if self._select_latest_metrics():
            self._emit_status("Подключены метрики последней модели.")
        else:
            self._emit_status("Метрики по умолчанию (сохранённые модели не найдены).")

    @QtCore.Slot(str)
    def select_play_model(self, file_url: str) -> None:
        path = self._to_local_file(file_url)
        if not path:
            self._emit_status("Модель не выбрана.")
            return
        if not os.path.exists(path):
            self._emit_status("Файл модели не найден. Проверьте путь.")
            return
        if not path.endswith(".pickle"):
            self._emit_status("Выберите файл модели .pickle.")
            return
        self._set_play_model(path, source="manual")
        self._emit_status("Модель для игры обновлена.")

    @QtCore.Slot()
    def select_latest_play_model(self) -> None:
        if self._select_latest_play_model(initial=False):
            self._emit_status("Выбрана последняя сохранённая модель.")
        else:
            self._emit_status("Сохранённые модели не найдены.")

    @QtCore.Slot()
    def play_in_terminal(self) -> None:
        model_path = self._resolve_play_model_path()
        if model_path == "None":
            self._emit_status("Сохранённые модели не найдены. Запускаю базовый режим.")
        script = os.path.join(self._repo_root, "launch_terminal_manual.sh")
        if not os.path.exists(script):
            self._emit_status("Не найден launch_terminal_manual.sh. Проверьте репозиторий.")
            return
        self._persist_rosters()
        subprocess.Popen(
            [script, model_path],
            cwd=self._repo_root,
            env=os.environ.copy(),
            start_new_session=True,
        )
        self._emit_status("Запуск игры в терминале.")

    @QtCore.Slot()
    def play_in_gui(self) -> None:
        model_path = self._resolve_play_model_path()
        if model_path == "None":
            self._emit_status("Сохранённые модели не найдены. Запускаю базовый режим.")
        script = os.path.join(self._repo_root, "play.sh")
        if not os.path.exists(script):
            self._emit_status("Не найден play.sh. Проверьте репозиторий.")
            return
        self._persist_rosters()
        env = os.environ.copy()
        env["PLAY_NO_EXPLORATION"] = "1"
        env["FIGHT_REPORT"] = "1"
        subprocess.Popen(
            [script, model_path, "True"],
            cwd=self._repo_root,
            env=env,
            start_new_session=True,
        )
        self._emit_status("Запуск игры в GUI.")

    @QtCore.Slot()
    def refresh_board_text(self) -> None:
        board_path = os.path.join(self._repo_root, "board.txt")
        self._board_text = self._render_board_ascii(board_path)
        self.boardTextChanged.emit(self._board_text)

    def _set_running(self, value: bool) -> None:
        if self._running != value:
            self._running = value
            self.runningChanged.emit(value)

    def _set_progress(self, current: int, total: int) -> None:
        if total <= 0:
            self._progress_value = 0.0
            self._progress_text = "0%"
            self._progress_label = f"ep={current}/?"
        else:
            fraction = max(0.0, min(1.0, current / total))
            percent = int(round(fraction * 100))
            self._progress_value = fraction
            self._progress_text = f"{percent}%"
            self._progress_label = f"ep={current}/{total} ({percent}%)"
        self.progressValueChanged.emit(self._progress_value)
        self.progressTextChanged.emit(self._progress_text)
        self.progressLabelChanged.emit(self._progress_label)

    def _update_progress_stats(self, current_episode: int) -> None:
        now = time.time()
        if self._training_start_time <= 0:
            return
        self._training_samples.append((now, current_episode))
        while len(self._training_samples) > 32:
            self._training_samples.popleft()
        cutoff = now - 20
        while len(self._training_samples) > 2 and self._training_samples[0][0] < cutoff:
            self._training_samples.popleft()

        it_per_sec = 0.0
        if len(self._training_samples) >= 2:
            first_t, first_ep = self._training_samples[0]
            last_t, last_ep = self._training_samples[-1]
            elapsed = max(last_t - first_t, 1e-6)
            it_per_sec = max(0.0, (last_ep - first_ep) / elapsed)

        elapsed_total = max(0, int(now - self._training_start_time))
        eta_text = ""
        show_eta = it_per_sec > 0 and self._train_total_episodes > current_episode
        if show_eta:
            remaining = max(0, self._train_total_episodes - current_episode)
            eta_seconds = int(remaining / it_per_sec) if it_per_sec > 0 else 0
            eta_text = f" • ETA {self._format_duration(eta_seconds)}"

        rate_text = f"{it_per_sec:.1f} it/s" if it_per_sec > 0 else "— it/s"
        self._progress_stats = f"{rate_text} • elapsed {self._format_duration(elapsed_total)}{eta_text}"
        self.progressStatsChanged.emit(self._progress_stats)

    def _start_training(self, mode: str) -> None:
        if self._process is not None:
            self._emit_status("Процесс уже запущен. Сначала остановите текущий.")
            return
        if not self._prepare_training_data():
            return

        train_label = "TRAIN"
        status_prefix = "Обучение"
        env_overrides: dict[str, str] = {}
        if mode == "train8":
            train_label = "TRAIN8"
            status_prefix = "Обучение 8x"
            env_overrides["VEC_ENV_COUNT"] = "8"
        elif mode == "selfplay":
            train_label = "SELFPLAY"
            status_prefix = "Самообучение"
            env_overrides["SELF_PLAY_ENABLED"] = "1"

        self._emit_log(f"[GUI] Запуск {status_prefix.lower()}...", level="INFO")
        self._emit_status(f"{status_prefix}...")

        self._process = QtCore.QProcess(self)
        self._process.setWorkingDirectory(self._repo_root)

        env = QtCore.QProcessEnvironment.systemEnvironment()
        env.insert("TRAIN_LOG_ENABLED", "1")
        env.insert("TRAIN_LOG_TO_CONSOLE", "1")
        env.insert("TRAIN_LOG_TO_FILE", "1")
        env.insert("PER_ENABLED", "1")
        env.insert("N_STEP", "3")
        for key, value in env_overrides.items():
            env.insert(key, value)
        self._process.setProcessEnvironment(env)

        self._process.readyReadStandardOutput.connect(self._read_stdout)
        self._process.readyReadStandardError.connect(self._read_stderr)
        self._process.errorOccurred.connect(self._on_error)
        self._process.finished.connect(self._on_finished)

        self._train_total_episodes = self._num_games
        self._reset_training_stats()
        self._set_progress(0, self._train_total_episodes)
        self._progress_stats = "— it/s • elapsed 00:00"
        self.progressStatsChanged.emit(self._progress_stats)

        start_message = f"Старт {status_prefix.lower()}: PER=1, N_STEP=3."
        self._emit_log(f"[{train_label}] {start_message}")
        self._emit_status(start_message)

        self._process.start("./train.sh")
        if not self._process.waitForStarted(3000):
            self._emit_log(
                "[GUI] Не удалось запустить train.sh. Проверьте, что файл доступен.",
                level="ERROR",
            )
            self._cleanup_process()
            return

        self._set_running(True)

    def _prepare_training_data(self) -> bool:
        try:
            self._persist_rosters()
            args = [
                "./data.sh",
                str(self._num_games),
                "Necrons",
                "Necrons",
                str(self._board_x),
                str(self._board_y),
            ]
            result = subprocess.run(
                args,
                cwd=self._repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                message = (
                    "Ошибка подготовки данных (gui_qt/main.py): "
                    "проверьте data.sh и зависимости."
                )
                self._emit_status(message)
                self._emit_log(
                    f"[GUI] {message}\nstdout: {result.stdout}\nstderr: {result.stderr}",
                    level="ERROR",
                )
                return False
            return True
        except OSError as exc:
            message = (
                "Ошибка подготовки данных (gui_qt/main.py): "
                "проверьте доступность data.sh."
            )
            self._emit_status(message)
            self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")
            return False

    def _read_stdout(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            if line.strip():
                if self._should_show_train_log(line):
                    self._emit_log(line)
                self._handle_progress_line(line)

    def _read_stderr(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            if line.strip():
                if not self._is_tqdm_progress_line(line):
                    self._emit_log(line, level="ERROR")
                self._handle_progress_line(line)

    def _is_tqdm_progress_line(self, line: str) -> bool:
        normalized = line.strip()
        if not normalized:
            return False
        return bool(re.search(r"\d+%\|.+\|\s*\d+\s*/\s*\d+", normalized))

    def _should_show_train_log(self, line: str) -> bool:
        normalized = line.strip()
        if not normalized:
            return False
        if normalized.startswith("[GUI]"):
            return True
        if normalized.startswith("[ERROR]") or normalized.startswith("[WARN]"):
            return True
        allowed_prefixes = (
            "[TRAIN8] Старт",
            "[TRAIN] Старт",
            "[SELFPLAY] Старт",
            "[TRAIN][START]",
            "[DEVICE CHECK]",
            "[metrics] saved:",
        )
        allowed_contains = (
            "Training...",
            "Model Units:",
            "Enemy Units:",
            "Action keys:",
            "Generated metrics",
            "Forging model_train.gif",
            "genDisplay.makeGif:",
        )
        if normalized.startswith(allowed_prefixes):
            return True
        if any(token in normalized for token in allowed_contains):
            return True
        if normalized.startswith("Name:"):
            return True
        if normalized.startswith("[") and re.match(r"^\[\s*\d", normalized):
            return True
        if normalized == "[]":
            return True
        return False

    def _handle_progress_line(self, line: str) -> None:
        current, total = self._parse_training_progress(line, self._train_total_episodes)
        if current is None:
            return
        self._set_progress(current, total)
        now = time.time()
        if now - self._training_last_ui_update >= 0.25:
            self._training_last_ui_update = now
            self._update_progress_stats(current)

    def _parse_training_progress(self, line: str, fallback_total: int) -> tuple[Optional[int], int]:
        tqdm_match = re.search(r"(\d+)\s*/\s*(\d+)", line)
        if tqdm_match:
            return int(tqdm_match.group(1)), int(tqdm_match.group(2))
        ep_match = re.search(r"\bep=(\d+)", line)
        if ep_match:
            return int(ep_match.group(1)), fallback_total
        return None, fallback_total

    def _reset_training_stats(self) -> None:
        self._training_samples.clear()
        now = time.time()
        self._training_start_time = now
        self._training_last_ui_update = now - 1

    def _on_error(self, error: QtCore.QProcess.ProcessError) -> None:
        self._emit_log(f"[GUI] Ошибка процесса: {error}.", level="ERROR")
        self._emit_status("Ошибка запуска. Проверьте логи и зависимости.")
        self._cleanup_process()

    def _on_finished(self, exit_code: int, exit_status: QtCore.QProcess.ExitStatus) -> None:
        status_text = "нормально" if exit_status == QtCore.QProcess.ExitStatus.NormalExit else "с ошибкой"
        self._emit_log(f"[GUI] Процесс завершён ({status_text}), код: {exit_code}.")
        if exit_status == QtCore.QProcess.ExitStatus.NormalExit:
            self._emit_status("Обучение завершено.")
        else:
            self._emit_status("Обучение завершено с ошибкой.")
        self._select_latest_metrics()
        self._cleanup_process()

    def _cleanup_process(self) -> None:
        if self._process is None:
            return
        self._process.deleteLater()
        self._process = None
        self._set_running(False)

    def _emit_log(self, message: str, level: str | None = None) -> None:
        if level:
            payload = f"[{level}] {message}"
        else:
            payload = message
        self.logLine.emit(payload)

    def _emit_status(self, message: str) -> None:
        self.statusChanged.emit(message)

    def _format_duration(self, seconds: int) -> str:
        minutes, secs = divmod(max(0, seconds), 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        return f"{minutes:02d}:{secs:02d}"

    def _build_default_metrics(self) -> dict[str, str]:
        base_dir = os.path.join(self._repo_root, "gui", "img")
        return {
            "reward": os.path.join(base_dir, "reward.png"),
            "loss": os.path.join(base_dir, "loss.png"),
            "epLen": os.path.join(base_dir, "epLen.png"),
            "winrate": os.path.join(base_dir, "winrate.png"),
            "vpdiff": os.path.join(base_dir, "vpdiff.png"),
            "endreasons": os.path.join(base_dir, "endreasons.png"),
        }

    def _set_metrics_files(self, paths: dict[str, str]) -> None:
        self._metrics_files = paths
        self._refresh_metrics_paths(force=True)

    def _set_play_model(self, path: str, source: str) -> None:
        self._play_model_path = path
        label_prefix = "Последняя модель" if source == "latest" else "Выбрана модель"
        self._play_model_label = f"{label_prefix}: {os.path.basename(path)}"
        self.playModelPathChanged.emit(self._play_model_path)
        self.playModelLabelChanged.emit(self._play_model_label)

    def _select_latest_play_model(self, initial: bool) -> bool:
        latest_model = self._find_latest_model_file()
        if not latest_model:
            if initial:
                self._play_model_path = ""
                self._play_model_label = "Модель не найдена"
                self.playModelPathChanged.emit(self._play_model_path)
                self.playModelLabelChanged.emit(self._play_model_label)
            return False
        self._set_play_model(latest_model, source="latest")
        return True

    def _resolve_play_model_path(self) -> str:
        if self._play_model_path and os.path.exists(self._play_model_path):
            return self._play_model_path
        latest = self._find_latest_model_file()
        if latest:
            self._set_play_model(latest, source="latest")
            return latest
        return "None"

    def _render_board_ascii(self, board_path: str) -> str:
        if not os.path.exists(board_path):
            return "board.txt не найден. Запустите игру, чтобы сформировать карту."
        try:
            with open(board_path, "r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError as exc:
            return f"Не удалось прочитать board.txt: {exc}"
        full = []
        last = "\0"
        for ch in content:
            if ch.isspace():
                continue
            if last == "0" and ch != ",":
                full.append("\n")
            elif ch == "0" and last.isdigit():
                full.append("\n")
            elif ch.isdigit() and ch not in {"0", "3"}:
                full.append(ch)
            elif ch.isdigit() and ch == "3":
                full.append("0 ")
            else:
                full.append("_ ")
            last = ch
        return "".join(full)

    def _refresh_metrics_paths(self, force: bool = False) -> None:
        changed = False
        for key, path in self._metrics_files.items():
            mtime = None
            if os.path.exists(path):
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    mtime = None
            if force or self._metrics_mtimes.get(key) != mtime:
                self._metrics_mtimes[key] = mtime
                changed = True
        if not changed:
            return
        self._metrics_paths = self._build_metrics_paths(self._metrics_files, cache_token=self._cache_token())
        self.metricsChanged.emit()

    def _build_metrics_paths(self, files: dict[str, str], cache_token: str) -> dict[str, str]:
        return {key: f"{self._to_file_url(path)}?v={cache_token}" for key, path in files.items()}

    def _cache_token(self) -> str:
        return str(int(time.time() * 1000))

    def _resolve_metric_path(self, raw_path: Optional[str], fallback: str) -> str:
        if not raw_path:
            return fallback
        if os.path.isabs(raw_path):
            candidate = raw_path
        else:
            candidate = os.path.join(self._repo_root, "gui", raw_path)
        if os.path.exists(candidate):
            return candidate
        return fallback

    def _to_file_url(self, path: str) -> str:
        return QtCore.QUrl.fromLocalFile(path).toString()

    def _to_local_file(self, path_or_url: str) -> str:
        if not path_or_url:
            return ""
        url = QtCore.QUrl(path_or_url)
        if url.isLocalFile():
            return url.toLocalFile()
        return path_or_url

    def _extract_metrics_id(self, path: str) -> str:
        base = os.path.basename(path)
        match = re.search(r"model-(\d+-\d+)\.pickle$", base)
        if match:
            return match.group(1)
        match = re.search(r"model-(-?\d+)\.pickle$", base)
        if match:
            return match.group(1)
        tail = path[-16:-7]
        if tail and tail[0] == "-":
            return path[-15:-7]
        return tail

    def _load_metrics_from_json(self, json_path: str) -> bool:
        try:
            with open(json_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            self._emit_status("Не удалось прочитать метрики. Проверьте файл.")
            self._emit_log(f"[GUI] Ошибка чтения метрик: {exc}", level="ERROR")
            return False

        updated = {
            "reward": self._resolve_metric_path(payload.get("reward"), self._metrics_defaults["reward"]),
            "loss": self._resolve_metric_path(payload.get("loss"), self._metrics_defaults["loss"]),
            "epLen": self._resolve_metric_path(payload.get("epLen"), self._metrics_defaults["epLen"]),
            "winrate": self._resolve_metric_path(payload.get("winrate"), self._metrics_defaults["winrate"]),
            "vpdiff": self._resolve_metric_path(payload.get("vpdiff"), self._metrics_defaults["vpdiff"]),
            "endreasons": self._resolve_metric_path(payload.get("endreasons"), self._metrics_defaults["endreasons"]),
        }
        self._set_metrics_files(updated)
        return True

    def _select_latest_metrics(self) -> bool:
        latest_model = self._find_latest_model_file()
        if latest_model:
            metrics_id = self._extract_metrics_id(latest_model)
            if metrics_id:
                json_path = os.path.join(self._repo_root, "models", f"data_{metrics_id}.json")
                if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                    self._metrics_label = f"Файл: {os.path.basename(latest_model)}"
                    self.metricsLabelChanged.emit(self._metrics_label)
                    return True
        latest_json = self._find_latest_metrics_json()
        if latest_json and self._load_metrics_from_json(latest_json):
            self._metrics_label = f"Файл: {os.path.basename(latest_json)}"
            self.metricsLabelChanged.emit(self._metrics_label)
            return True
        self._set_metrics_files(dict(self._metrics_defaults))
        self._metrics_label = "По умолчанию"
        self.metricsLabelChanged.emit(self._metrics_label)
        return False

    def _find_latest_model_file(self) -> Optional[str]:
        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None
        latest_path = None
        latest_mtime = -1.0
        for root, _, files in os.walk(models_path):
            for name in files:
                if not name.endswith(".pickle"):
                    continue
                if "model-" not in name:
                    continue
                path = os.path.join(root, name)
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    continue
                if mtime > latest_mtime:
                    latest_mtime = mtime
                    latest_path = path
        return latest_path

    def _find_latest_metrics_json(self) -> Optional[str]:
        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None
        latest_path = None
        latest_mtime = -1.0
        for name in os.listdir(models_path):
            if not (name.startswith("data_") and name.endswith(".json")):
                continue
            path = os.path.join(models_path, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_path = path
        return latest_path

    def _create_roster_entry(self, unit: UnitInfo) -> RosterEntry:
        entry = RosterEntry(name=unit.name, count=unit.default_count, instance_id=str(self._instance_counter))
        self._instance_counter += 1
        return entry

    def _refresh_models(self) -> None:
        self._available_model.setStringList(
            [f"{unit.name} (x{unit.default_count})" for unit in self._available_units]
        )
        self._player_model.setStringList(
            [f"{entry.name} (x{entry.count})" for entry in self._player_roster]
        )
        self._model_model.setStringList(
            [f"{entry.name} (x{entry.count})" for entry in self._model_roster]
        )

    def _update_roster_summary(self) -> None:
        self._roster_summary = (
            f"Юниты игрока: {len(self._player_roster)} | "
            f"Юниты модели: {len(self._model_roster)}"
        )
        self.rosterSummaryChanged.emit(self._roster_summary)

    def _load_available_units(self) -> None:
        unit_path = os.path.join(self._repo_root, "gym_mod", "gym_mod", "engine", "unitData.json")
        if not os.path.exists(unit_path):
            self._emit_log("[GUI] unitData.json не найден, список юнитов пуст.", level="WARN")
            return
        with open(unit_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        units = payload.get("UnitData", [])
        for unit in units:
            name = unit.get("Name")
            faction = unit.get("Army")
            if not name or not faction:
                continue
            if faction.lower() != "necrons":
                continue
            default_count = unit.get("#OfModels", 1)
            self._available_units.append(UnitInfo(name=name, faction=faction, default_count=default_count))

    def _load_rosters_from_file(self) -> None:
        units_path = os.path.join(self._repo_root, "gui", "units.txt")
        if not os.path.exists(units_path):
            return
        section = None
        with open(units_path, "r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if not line:
                    continue
                if line == "Player Units":
                    section = "player"
                    continue
                if line == "Model Units":
                    section = "model"
                    continue
                if section not in {"player", "model"}:
                    continue
                entry = self._parse_roster_line(line)
                if entry is None:
                    continue
                if section == "player":
                    self._player_roster.append(entry)
                else:
                    self._model_roster.append(entry)

    def _parse_roster_line(self, line: str) -> Optional[RosterEntry]:
        if "|" not in line:
            return RosterEntry(name=line, count=0, instance_id="")
        parts = [part.strip() for part in line.split("|")]
        name = parts[0] if parts else ""
        count = 0
        if len(parts) >= 2:
            try:
                count = int(parts[1])
            except ValueError:
                count = 0
        instance_id = parts[2] if len(parts) >= 3 else ""
        if instance_id.isdigit():
            self._instance_counter = max(self._instance_counter, int(instance_id) + 1)
        return RosterEntry(name=name, count=count, instance_id=instance_id)

    def _persist_rosters(self) -> None:
        units_path = os.path.join(self._repo_root, "gui", "units.txt")
        lines = ["Player Units"]
        for entry in self._player_roster:
            lines.append(f"{entry.name}|{entry.count}|{entry.instance_id}")
        lines.append("Model Units")
        for entry in self._model_roster:
            lines.append(f"{entry.name}|{entry.count}|{entry.instance_id}")
        os.makedirs(os.path.dirname(units_path), exist_ok=True)
        with open(units_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))

    def _clear_cache_files(self) -> None:
        models_path = os.path.join(self._repo_root, "models")
        metrics_path = os.path.join(self._repo_root, "metrics")
        gui_img_path = os.path.join(self._repo_root, "gui", "img")
        self._remove_contents(models_path)
        self._remove_contents(metrics_path)
        if os.path.isdir(gui_img_path):
            keep = {"epLen.png", "reward.png", "loss.png", "icon.png"}
            for name in os.listdir(gui_img_path):
                if name in keep:
                    continue
                target = os.path.join(gui_img_path, name)
                if os.path.isdir(target):
                    shutil.rmtree(target)
                else:
                    os.remove(target)
        self._truncate_agent_logs()

    def _remove_contents(self, path: str) -> None:
        if not os.path.isdir(path):
            return
        for name in os.listdir(path):
            target = os.path.join(path, name)
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)

    def _truncate_agent_logs(self) -> None:
        log_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS.md")
        with open(log_path, "w", encoding="utf-8"):
            pass


def main() -> int:
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()

    controller = GUIController()
    engine.rootContext().setContextProperty("controller", controller)

    qml_path = os.path.join(os.path.dirname(__file__), "qml", "Main.qml")
    engine.load(QtCore.QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        return 1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
