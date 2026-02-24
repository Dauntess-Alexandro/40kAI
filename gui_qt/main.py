import ast
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import time
import ctypes
from collections import deque
from dataclasses import dataclass
from typing import Optional

from PySide6 import QtCore, QtGui, QtQml
from PySide6.QtGui import QIcon


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
    missionChanged = QtCore.Signal(str)
    metricsChanged = QtCore.Signal()
    metricsLabelChanged = QtCore.Signal(str)
    metricsSummaryChanged = QtCore.Signal()
    playModelPathChanged = QtCore.Signal(str)
    playModelLabelChanged = QtCore.Signal(str)
    evalModelPathChanged = QtCore.Signal(str)
    evalModelLabelChanged = QtCore.Signal(str)
    evalGamesChanged = QtCore.Signal(int)
    evalLogTextChanged = QtCore.Signal(str)
    evalSummaryTextChanged = QtCore.Signal(str)
    boardTextChanged = QtCore.Signal(str)
    selfPlayFromCheckpointChanged = QtCore.Signal(bool)
    resumeFromCheckpointChanged = QtCore.Signal(bool)
    disableTrainLoggingChanged = QtCore.Signal(bool)
    factionIconSizeChanged = QtCore.Signal(int)
    unitIconSizeChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process: Optional[QtCore.QProcess] = None
        self._running = False
        self._repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self._is_windows = sys.platform.startswith("win")

        self._progress_value = 0.0
        self._progress_label = "ep=0/0 (0%)"
        self._progress_stats = "— it/s • elapsed 00:00"
        self._progress_text = "0%"

        self._num_games = 100
        self._mission_options = ["only_war"]
        self._selected_mission = "only_war"

        self._train_total_episodes = 0
        self._training_samples = deque()
        self._training_start_time = 0.0
        self._training_last_ui_update = 0.0

        self._available_units: list[UnitInfo] = []
        self._player_roster: list[RosterEntry] = []
        self._model_roster: list[RosterEntry] = []
        self._instance_counter = 1

        self._available_model = QtGui.QStandardItemModel(self)
        self._player_model = QtGui.QStandardItemModel(self)
        self._model_model = QtGui.QStandardItemModel(self)
        self._unit_icon_cache: dict[str, QIcon] = {}
        self._unit_icon_source_cache: dict[str, str] = {}
        self._icon_sizes = self._load_icon_sizes_config()
        self._unit_icon_size = QtCore.QSize(self._icon_sizes["unit"], self._icon_sizes["unit"])

        self._metrics_defaults = self._build_default_metrics()
        self._metrics_files = dict(self._metrics_defaults)
        self._metrics_paths = self._build_metrics_paths(self._metrics_files, cache_token=self._cache_token())
        self._metrics_mtimes: dict[str, Optional[float]] = {}
        self._metrics_label = "По умолчанию"
        self._selected_metrics_model_id = ""
        self._selected_metrics_model_path = ""
        self._metric_summary_texts = {
            "reward": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "loss": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "epLen": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "winrate": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "vpdiff": "Текущее: — | Среднее: — | Мин: — | Макс: —",
        }
        self._model_state_text = "Нет данных о состоянии модели."

        self._play_model_path = ""
        self._play_model_label = "Модель не выбрана"
        self._eval_model_path = ""
        self._eval_model_label = "Модель не выбрана"
        self._eval_games = 50
        self._eval_log_text = ""
        self._eval_summary_text = "Итог оценки появится после завершения eval.py."
        self._active_process_kind = ""
        self._board_text = "ASCII карта будет доступна после запуска игры."
        self._self_play_from_checkpoint = False
        self._resume_from_checkpoint = False
        self._disable_train_logging = False

        self._load_available_units()
        self._load_rosters_from_file()
        self._refresh_models()
        self._select_latest_metrics()
        self._select_latest_play_model(initial=True)
        self._select_latest_eval_model(initial=True)
        self._update_roster_summary()

        self._emit_status("Нажмите «Тренировка 8х» или «Самообучение», чтобы запустить обучение.")

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

    @QtCore.Property("QStringList", constant=True)
    def missionOptions(self):
        return self._mission_options

    @QtCore.Property(str, notify=missionChanged)
    def selectedMission(self) -> str:
        return self._selected_mission

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

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def rewardSummary(self) -> str:
        return self._metric_summary_texts["reward"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def lossSummary(self) -> str:
        return self._metric_summary_texts["loss"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def epLenSummary(self) -> str:
        return self._metric_summary_texts["epLen"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def winrateSummary(self) -> str:
        return self._metric_summary_texts["winrate"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def vpDiffSummary(self) -> str:
        return self._metric_summary_texts["vpdiff"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def modelStateText(self) -> str:
        return self._model_state_text

    @QtCore.Property(str, notify=playModelPathChanged)
    def playModelPath(self) -> str:
        return self._play_model_path

    @QtCore.Property(str, notify=playModelLabelChanged)
    def playModelLabel(self) -> str:
        return self._play_model_label

    @QtCore.Property(str, notify=evalModelPathChanged)
    def evalModelPath(self) -> str:
        return self._eval_model_path

    @QtCore.Property(str, notify=evalModelLabelChanged)
    def evalModelLabel(self) -> str:
        return self._eval_model_label

    @QtCore.Property(int, notify=evalGamesChanged)
    def evalGames(self) -> int:
        return self._eval_games

    @QtCore.Property(str, notify=evalLogTextChanged)
    def evalLogText(self) -> str:
        return self._eval_log_text

    @QtCore.Property(str, notify=evalSummaryTextChanged)
    def evalSummaryText(self) -> str:
        return self._eval_summary_text

    @QtCore.Property(str, notify=boardTextChanged)
    def boardText(self) -> str:
        return self._board_text

    @QtCore.Property(bool, notify=selfPlayFromCheckpointChanged)
    def selfPlayFromCheckpoint(self) -> bool:
        return self._self_play_from_checkpoint

    @QtCore.Property(bool, notify=resumeFromCheckpointChanged)
    def resumeFromCheckpoint(self) -> bool:
        return self._resume_from_checkpoint

    @QtCore.Property(bool, notify=disableTrainLoggingChanged)
    def disableTrainLogging(self) -> bool:
        return self._disable_train_logging

    @QtCore.Property(str, constant=True)
    def modelsFolderUrl(self) -> str:
        return self._to_file_url(os.path.join(self._repo_root, "models"))

    @QtCore.Property(int, notify=factionIconSizeChanged)
    def factionIconSize(self) -> int:
        return self._icon_sizes["faction"]

    @QtCore.Property(int, notify=unitIconSizeChanged)
    def unitIconSize(self) -> int:
        return self._icon_sizes["unit"]

    def _load_icon_sizes_config(self) -> dict[str, int]:
        defaults = {"unit": 18, "faction": 18}
        config_path = os.path.join(self._repo_root, "gui_qt", "icon_sizes.json")
        if not os.path.exists(config_path):
            return defaults

        try:
            with open(config_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            self._emit_log(
                "[GUI] Не удалось прочитать gui_qt/icon_sizes.json. "
                "Использую размеры иконок по умолчанию (18).",
                level="WARN",
            )
            return defaults

        result = dict(defaults)
        for key, target in (("unit_icon_size", "unit"), ("faction_icon_size", "faction")):
            value = payload.get(key, defaults[target])
            if isinstance(value, (int, float)):
                px = max(12, min(64, int(value)))
                result[target] = px
        return result

    def get_faction_icon(self, faction_name: str) -> QIcon:
        normalized = (faction_name or "").strip().lower()
        if normalized == "necrons":
            icon_path = os.path.join(self._repo_root, "gui_qt", "assets", "necrons.png")
            if os.path.exists(icon_path):
                return QIcon(icon_path)
        return QIcon()

    def normalize_unit_name(self, text: str) -> str:
        normalized = (text or "").strip()
        normalized = re.sub(r"\(x\d+\)\s*$", "", normalized, flags=re.IGNORECASE)
        return " ".join(normalized.split())

    def get_unit_icon(self, unit_name: str) -> QIcon:
        normalized = self.normalize_unit_name(unit_name)
        if not normalized:
            return QIcon()
        cache_key = normalized.casefold()
        if cache_key in self._unit_icon_cache:
            return self._unit_icon_cache[cache_key]

        icon_file_map = {
            "necron warriors": "necron_warriors_icon.png",
            "royal warden": "royal_warden_icon.png",
            "canoptek scarab swarms": "canoptek_scarab_swarms_icon.png",
        }
        icon_file = icon_file_map.get(cache_key)
        if not icon_file:
            icon = QIcon()
        else:
            icon_path = os.path.join(self._repo_root, "gui_qt", "assets", icon_file)
            icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        self._unit_icon_cache[cache_key] = icon
        return icon

    def get_unit_icon_source(self, unit_name: str) -> str:
        normalized = self.normalize_unit_name(unit_name)
        if not normalized:
            return ""
        cache_key = normalized.casefold()
        if cache_key in self._unit_icon_source_cache:
            return self._unit_icon_source_cache[cache_key]

        icon = self.get_unit_icon(normalized)
        if icon.isNull():
            self._unit_icon_source_cache[cache_key] = ""
            return ""

        pixmap = icon.pixmap(self._unit_icon_size)
        if pixmap.isNull():
            self._unit_icon_source_cache[cache_key] = ""
            return ""

        scaled = pixmap.scaled(
            self._unit_icon_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        image_dir = os.path.join(self._repo_root, "gui_qt", ".icon_cache")
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, f"{cache_key.replace(' ', '_')}.png")
        scaled.save(image_path, "PNG")
        source = self._to_file_url(image_path)
        self._unit_icon_source_cache[cache_key] = source
        return source

    @QtCore.Slot(str, result=str)
    def faction_icon_source(self, faction_name: str) -> str:
        icon = self.get_faction_icon(faction_name)
        if icon.isNull():
            return ""
        sizes = icon.availableSizes()
        pixmap = icon.pixmap(sizes[0] if sizes else QtCore.QSize(self._icon_sizes["faction"], self._icon_sizes["faction"]))
        if pixmap.isNull():
            return ""
        icon_path = os.path.join(self._repo_root, "gui_qt", "assets", "necrons.png")
        return self._to_file_url(icon_path)

    @QtCore.Slot(str, result=str)
    def unit_icon_source(self, unit_name: str) -> str:
        return self.get_unit_icon_source(unit_name)

    @QtCore.Slot(int)
    def set_num_games(self, value: int) -> None:
        if value <= 0:
            self._emit_status("Количество игр должно быть больше нуля.")
            return
        if self._num_games != value:
            self._num_games = value
            self.numGamesChanged.emit(value)

    @QtCore.Slot(str)
    def set_selected_mission(self, mission: str) -> None:
        normalized = (mission or "only_war").strip().lower().replace("-", "_").replace(" ", "_")
        if normalized not in self._mission_options:
            normalized = "only_war"
        if self._selected_mission != normalized:
            self._selected_mission = normalized
            self.missionChanged.emit(normalized)

    @QtCore.Slot(int)
    def set_selected_mission_index(self, index: int) -> None:
        if 0 <= index < len(self._mission_options):
            self.set_selected_mission(self._mission_options[index])

    @QtCore.Slot(int)
    def set_eval_games(self, value: int) -> None:
        if value <= 0:
            self._emit_status(
                "Некорректное значение количества игр для оценки. "
                "Где: gui_qt/main.py (set_eval_games). "
                "Что делать: укажите число больше нуля."
            )
            return
        if self._eval_games != value:
            self._eval_games = value
            self.evalGamesChanged.emit(value)

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

    @QtCore.Slot(bool)
    def set_self_play_from_checkpoint(self, value: bool) -> None:
        flag = bool(value)
        if self._self_play_from_checkpoint == flag:
            return
        self._self_play_from_checkpoint = flag
        self.selfPlayFromCheckpointChanged.emit(flag)

    @QtCore.Slot(bool)
    def set_resume_from_checkpoint(self, value: bool) -> None:
        flag = bool(value)
        if self._resume_from_checkpoint == flag:
            return
        self._resume_from_checkpoint = flag
        self.resumeFromCheckpointChanged.emit(flag)

    @QtCore.Slot(bool)
    def set_disable_train_logging(self, value: bool) -> None:
        flag = bool(value)
        if self._disable_train_logging == flag:
            return
        self._disable_train_logging = flag
        self.disableTrainLoggingChanged.emit(flag)

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

    @QtCore.Slot()
    def clear_agent_logs(self) -> None:
        try:
            self._truncate_agent_logs()
            self._emit_status("LOGS_FOR_AGENTS.md очищен.")
            self._emit_log("[GUI] LOGS_FOR_AGENTS.md очищен.")
        except OSError as exc:
            message = (
                "Не удалось очистить LOGS_FOR_AGENTS.md (gui_qt/main.py): "
                "проверьте путь и права доступа, затем повторите."
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
        self._selected_metrics_model_path = path
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

    @QtCore.Slot(str)
    def select_eval_model(self, file_url: str) -> None:
        path = self._to_local_file(file_url)
        if not path:
            self._emit_status("Модель для оценки не выбрана.")
            return
        if not os.path.exists(path):
            self._emit_status(
                "Файл модели для оценки не найден. "
                "Где: gui_qt/main.py (select_eval_model). "
                "Что делать: проверьте путь к .pickle и повторите."
            )
            return
        if not path.endswith(".pickle"):
            self._emit_status("Для оценки выберите файл модели .pickle.")
            return
        self._set_eval_model(path, source="manual")
        self._emit_status("Модель для оценки обновлена.")

    @QtCore.Slot()
    def select_latest_eval_model(self) -> None:
        if self._select_latest_eval_model(initial=False):
            self._emit_status("Для оценки выбрана последняя сохранённая модель.")
        else:
            self._emit_status(
                "Сохранённые модели для оценки не найдены. "
                "Что делать: запустите обучение или выберите модель вручную."
            )

    @QtCore.Slot()
    def select_best_eval_model(self) -> None:
        best_checkpoint = self._find_best_checkpoint_by_episode()
        if not best_checkpoint:
            self._emit_status(
                "Не найдено checkpoint_ep*.pth в models/. "
                "Где: gui_qt/main.py (select_best_eval_model). "
                "Что делать: запустите обучение и дождитесь сохранения чекпойнта."
            )
            return

        best_model = self._find_eval_pickle_for_checkpoint(best_checkpoint)
        if not best_model:
            self._emit_status(
                "Найден чекпойнт, но связанная .pickle модель для eval не найдена. "
                "Где: gui_qt/main.py (_find_eval_pickle_for_checkpoint). "
                "Что делать: убедитесь, что .pickle лежит рядом с checkpoint_ep*.pth "
                "или выберите модель вручную."
            )
            self._emit_log(
                f"[GUI] [EVAL] Чекпойнт без .pickle для eval: {best_checkpoint}",
                level="WARN",
            )
            return

        self._set_eval_model(best_model, source="best")
        checkpoint_name = os.path.basename(best_checkpoint)
        self._emit_status(f"Выбрана лучшая модель по чекпойнту: {checkpoint_name}.")

    @QtCore.Slot()
    def start_eval(self) -> None:
        if self._process is not None:
            self._emit_status("Процесс уже запущен. Сначала остановите текущий.")
            return
        if not self._check_torch_import():
            return

        model_path = self._resolve_eval_model_path()
        if model_path == "None":
            self._emit_status(
                "Не удалось запустить оценку: модель не найдена. "
                "Где: gui_qt/main.py (start_eval). "
                "Что делать: выберите .pickle вручную или обучите новую модель."
            )
            return

        eval_script = os.path.join(self._repo_root, "eval.py")
        if not os.path.exists(eval_script):
            self._emit_status(
                "Не удалось запустить оценку: не найден eval.py. "
                "Где: gui_qt/main.py (start_eval). "
                "Что делать: проверьте целостность репозитория и повторите."
            )
            return

        self._process = QtCore.QProcess(self)
        self._process.setWorkingDirectory(self._repo_root)

        self._set_eval_log_text("")
        self._set_eval_summary_text("Идёт оценка... Итог будет показан после завершения.")

        env = QtCore.QProcessEnvironment.systemEnvironment()
        env.insert("FORCE_GREEDY", "1")
        env.insert("EVAL_EPSILON", "0")
        env.insert("PYTHONPATH", self._pythonpath_with_gym_mod())
        env.insert("MISSION_NAME", self._selected_mission)
        self._process.setProcessEnvironment(env)

        self._process.readyReadStandardOutput.connect(self._read_stdout)
        self._process.readyReadStandardError.connect(self._read_stderr)
        self._process.errorOccurred.connect(self._on_error)
        self._process.finished.connect(self._on_finished)

        self._active_process_kind = "eval"
        self._train_total_episodes = 0
        self._reset_training_stats()
        self._set_progress(0, 0)
        self._progress_stats = "— it/s • elapsed 00:00"
        self.progressStatsChanged.emit(self._progress_stats)

        args = ["-u", "eval.py", "--games", str(self._eval_games), "--model", model_path]
        self._emit_log(
            f"[EVAL] Старт оценки: игр={self._eval_games}, модель={os.path.basename(model_path)}, "
            "противник=эвристика, exploration=off.",
            level="INFO",
        )
        self._append_eval_log_line(
            f"Старт оценки: игр={self._eval_games}, модель={os.path.basename(model_path)}, "
            "противник=эвристика, exploration=off."
        )
        self._emit_status("Оценка запущена...")
        self._process.start(sys.executable, args)
        if not self._process.waitForStarted(3000):
            self._emit_log(
                "[GUI] Не удалось запустить eval.py. Проверьте, что файл доступен и окружение корректно.",
                level="ERROR",
            )
            self._cleanup_process()
            return

        self._set_running(True)

    @QtCore.Slot()
    def play_in_terminal(self) -> None:
        model_path = self._resolve_play_model_path()
        if model_path == "None":
            self._emit_status("Сохранённые модели не найдены. Запускаю базовый режим.")
        if not self._check_torch_import():
            return
        script = self._script_path("launch_terminal_manual")
        if not os.path.exists(script):
            self._emit_status("Не найден скрипт запуска терминала. Проверьте репозиторий.")
            return
        self._persist_rosters()
        command = self._build_script_command(script, [model_path])
        env = os.environ.copy()
        env["MISSION_NAME"] = self._selected_mission
        subprocess.Popen(
            command,
            cwd=self._repo_root,
            env=env,
            start_new_session=True,
        )
        self._emit_status("Запуск игры в терминале.")

    @QtCore.Slot()
    def play_in_gui(self) -> None:
        model_path = self._resolve_play_model_path()
        if model_path == "None":
            self._emit_status("Сохранённые модели не найдены. Запускаю базовый режим.")
        if not self._check_torch_import():
            return
        if self._is_windows:
            script = os.path.join(self._repo_root, "scripts", "viewer.bat")
        else:
            script = os.path.join(self._repo_root, "scripts", "viewer.sh")
        if not os.path.exists(script):
            self._emit_status("Не найден скрипт Viewer. Проверьте репозиторий.")
            return
        self._persist_rosters()
        env = os.environ.copy()
        env["MODEL_PATH"] = model_path
        env["FIGHT_REPORT"] = "1"
        env["PLAY_NO_EXPLORATION"] = "1"
        env["MISSION_NAME"] = self._selected_mission
        command = self._build_script_command(script, [])
        subprocess.Popen(
            command,
            cwd=self._repo_root,
            env=env,
            start_new_session=True,
        )
        self._emit_log("[VIEWER] Запуск в greedy-режиме: exploration отключен (epsilon=0).", level="INFO")
        self._emit_status("Запуск игры в GUI через Viewer (greedy, без исследования).")

    def _check_torch_import(self) -> bool:
        command = [
            sys.executable,
            "-c",
            "import torch; print(torch.__version__)",
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=self._repo_root,
        )
        if result.returncode == 0:
            return True
        error_text = (result.stderr or result.stdout or "").strip()
        if error_text:
            error_text = f" Детали: {error_text}"
        self._emit_status(
            "Не удалось загрузить PyTorch (torch) при запуске игры. "
            "Где: проверка окружения перед запуском Viewer. "
            "Что делать дальше: переустановите torch под вашу версию Python, "
            "обновите Microsoft Visual C++ Redistributable и попробуйте снова."
            f"{error_text}"
        )
        return False

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
            status_prefix = "Обучение"
            env_overrides["NUM_ENVS"] = "12"
            env_overrides["USE_SUBPROC_ENVS"] = "1"
        elif mode == "selfplay":
            train_label = "SELFPLAY"
            status_prefix = "Самообучение"
            env_overrides["VEC_ENV_COUNT"] = "12"
            env_overrides["SELF_PLAY_ENABLED"] = "1"

        if mode == "selfplay" and self._self_play_from_checkpoint:
            checkpoint_path = self._find_latest_checkpoint_file()
            if not checkpoint_path:
                self._emit_status(
                    "Чекпойнты .pth не найдены. "
                    "Снимите галочку или включите сохранение чекпойнтов."
                )
                return
            env_overrides["SELF_PLAY_OPPONENT_MODE"] = "fixed_checkpoint"
            env_overrides["SELF_PLAY_FIXED_PATH"] = checkpoint_path

        if self._resume_from_checkpoint:
            resume_path = self._find_latest_resume_file()
            if not resume_path:
                self._emit_status(
                    "Resume включён, но checkpoint_ep*.pth и model-*.pth не найдены. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать: сохраните чекпойнт и запустите снова или снимите галочку resume."
                )
                return
            env_overrides["RESUME_CHECKPOINT"] = resume_path
            self._emit_log(f"[GUI] [RESUME] Использую чекпойнт: {resume_path}", level="INFO")

        self._emit_log(f"[GUI] Запуск {status_prefix.lower()}...", level="INFO")
        self._emit_status(f"{status_prefix}...")

        self._process = QtCore.QProcess(self)
        self._process.setWorkingDirectory(self._repo_root)

        env = QtCore.QProcessEnvironment.systemEnvironment()
        if self._disable_train_logging:
            env.insert("TRAIN_LOG_ENABLED", "0")
            env.insert("TRAIN_LOG_TO_CONSOLE", "0")
            env.insert("TRAIN_LOG_TO_FILE", "0")
            env.insert("REWARD_DEBUG", "0")
            env.insert("LOG_EVERY", "1000")
        else:
            env.insert("TRAIN_LOG_ENABLED", "1")
            env.insert("TRAIN_LOG_TO_CONSOLE", "1")
            env.insert("TRAIN_LOG_TO_FILE", "1")
            env.insert("REWARD_DEBUG", "1")
            env.insert("LOG_EVERY", "500")
        env.insert("PER_ENABLED", "1")
        env.insert("N_STEP", "3")
        env.insert("SAVE_EVERY", "500")
        env.insert("CLIP_REWARD", "1")
        env.insert("MISSION_NAME", self._selected_mission)
        for key, value in env_overrides.items():
            env.insert(key, value)
        self._process.setProcessEnvironment(env)

        self._process.readyReadStandardOutput.connect(self._read_stdout)
        self._process.readyReadStandardError.connect(self._read_stderr)
        self._process.errorOccurred.connect(self._on_error)
        self._process.finished.connect(self._on_finished)

        self._active_process_kind = "train"

        self._train_total_episodes = self._num_games
        self._reset_training_stats()
        self._set_progress(0, self._train_total_episodes)
        self._progress_stats = "— it/s • elapsed 00:00"
        self.progressStatsChanged.emit(self._progress_stats)

        start_message = f"Старт {status_prefix.lower()}: PER=1, N_STEP=3."
        self._emit_log(f"[{train_label}] {start_message}")
        if self._disable_train_logging:
            self._emit_log(
                f"[{train_label}] Speed-режим: TRAIN_LOG_*=0, REWARD_DEBUG=0, LOG_EVERY=1000.",
                level="INFO",
            )
        self._emit_status(start_message)

        script = self._script_path("train")
        if self._is_windows:
            self._process.start("cmd", ["/c", script])
        else:
            self._process.start(script)
        if not self._process.waitForStarted(3000):
            self._emit_log(
                "[GUI] Не удалось запустить train-скрипт. Проверьте, что файл доступен.",
                level="ERROR",
            )
            self._cleanup_process()
            return

        self._set_running(True)

    def _prepare_training_data(self) -> bool:
        try:
            self._persist_rosters()
            script = self._script_path("data")
            args = [
                str(self._num_games),
                "Necrons",
                "Necrons",
                "60",
                "40",
                self._selected_mission,
            ]
            command = self._build_script_command(script, args)
            result = subprocess.run(
                command,
                cwd=self._repo_root,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                message = (
                    "Ошибка подготовки данных (gui_qt/main.py): "
                    "проверьте data-скрипт и зависимости."
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
                "проверьте доступность data-скрипта."
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
                if self._active_process_kind == "eval":
                    self._append_eval_log_line(line)
                    self._maybe_update_eval_summary(line)
                if self._should_show_train_log(line):
                    self._emit_log(line)
                self._handle_progress_line(line)

    def _read_stderr(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            if line.strip():
                if self._active_process_kind == "eval":
                    self._append_eval_log_line(f"[stderr] {line}")
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
            "[EVAL]",
            "[TRAIN8] Старт",
            "[TRAIN] Старт",
            "[SELFPLAY] Старт",
            "[TRAIN][START]",
            "[DEVICE CHECK]",
            "[RESUME]",
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
        if self._active_process_kind == "eval":
            if exit_status == QtCore.QProcess.ExitStatus.NormalExit and exit_code == 0:
                self._emit_status("Оценка завершена.")
                if not self._eval_summary_text.strip() or "Идёт оценка" in self._eval_summary_text:
                    self._set_eval_summary_text(
                        "Оценка завершена, но итоговая строка [SUMMARY] не найдена. "
                        "Проверьте лог ниже (gui_qt/main.py, _on_finished)."
                    )
            else:
                self._emit_status("Оценка завершена с ошибкой. Проверьте лог.")
                self._set_eval_summary_text(
                    "Оценка завершена с ошибкой. Где: gui_qt/main.py (_on_finished). "
                    "Что делать: проверьте лог оценки и traceback внизу."
                )
        else:
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
        self._active_process_kind = ""
        self._set_running(False)

    def _emit_log(self, message: str, level: str | None = None) -> None:
        if level:
            payload = f"[{level}] {message}"
        else:
            payload = message
        self.logLine.emit(payload)

    def _emit_status(self, message: str) -> None:
        self.statusChanged.emit(message)

    def _set_eval_log_text(self, value: str) -> None:
        self._eval_log_text = value
        self.evalLogTextChanged.emit(value)

    def _append_eval_log_line(self, line: str) -> None:
        if not line:
            return
        if self._eval_log_text:
            self._eval_log_text += "\n"
        self._eval_log_text += line
        self.evalLogTextChanged.emit(self._eval_log_text)

    def _set_eval_summary_text(self, value: str) -> None:
        self._eval_summary_text = value
        self.evalSummaryTextChanged.emit(value)

    def _maybe_update_eval_summary(self, line: str) -> None:
        normalized = line.strip()
        summary_prefix = "[EVAL][SUMMARY] "
        if normalized.startswith(summary_prefix):
            payload = normalized[len(summary_prefix):]
            details = self._format_eval_summary(payload)
            self._set_eval_summary_text(details)

    def _format_eval_summary(self, payload: str) -> str:
        pairs = {
            key: value
            for key, value in re.findall(r"([a-zA-Z_]+)=([^=]+?)(?=\s+[a-zA-Z_]+=|$)", payload)
        }

        reason_labels = {
            "turn_limit": "Лимит ходов",
            "wipeout_enemy": "Уничтожение армии противника",
            "wipeout_model": "Уничтожение армии модели",
            "auto": "Авто-завершение",
            "unknown": "Неизвестно",
        }

        reason_text = pairs.get('end_reasons', '{}')
        try:
            reason_dict = ast.literal_eval(reason_text)
            if isinstance(reason_dict, dict):
                pretty_reasons = {
                    reason_labels.get(str(key), str(key)): value
                    for key, value in reason_dict.items()
                }
                reason_text = str(pretty_reasons)
        except (ValueError, SyntaxError):
            pass

        lines = ["Подробный результат оценки:"]
        lines.append(f"- Победы: {pairs.get('wins', '?')}")
        lines.append(f"- Поражения: {pairs.get('losses', '?')}")
        lines.append(f"- Ничьи: {pairs.get('draws', '?')}")
        lines.append(f"- Winrate (все игры): {pairs.get('winrate_all', '?')}")
        lines.append(f"- Winrate (без ничьих): {pairs.get('winrate_no_draw', '?')}")
        lines.append(f"- Средний VP diff: {pairs.get('avg_vp_diff', '?')}")
        lines.append(f"- Медианный VP diff: {pairs.get('median_vp_diff', '?')}")
        lines.append(f"- Причины завершения: {reason_text}")
        return "\n".join(lines)

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

    def _set_eval_model(self, path: str, source: str) -> None:
        self._eval_model_path = path
        if source == "latest":
            label_prefix = "Последняя модель"
        elif source == "best":
            label_prefix = "Лучшая модель"
        else:
            label_prefix = "Выбрана модель"
        self._eval_model_label = f"{label_prefix}: {os.path.basename(path)}"
        self.evalModelPathChanged.emit(self._eval_model_path)
        self.evalModelLabelChanged.emit(self._eval_model_label)

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

    def _select_latest_eval_model(self, initial: bool) -> bool:
        latest_model = self._find_latest_model_file()
        if not latest_model:
            if initial:
                self._eval_model_path = ""
                self._eval_model_label = "Модель не найдена"
                self.evalModelPathChanged.emit(self._eval_model_path)
                self.evalModelLabelChanged.emit(self._eval_model_label)
            return False
        self._set_eval_model(latest_model, source="latest")
        return True

    def _resolve_eval_model_path(self) -> str:
        if self._eval_model_path and os.path.exists(self._eval_model_path):
            return self._eval_model_path
        latest = self._find_latest_model_file()
        if latest:
            self._set_eval_model(latest, source="latest")
            return latest
        return "None"

    def _pythonpath_with_gym_mod(self) -> str:
        gym_mod_path = os.path.join(self._repo_root, "gym_mod")
        env_path = os.environ.get("PYTHONPATH", "")
        if not env_path:
            return gym_mod_path
        return os.pathsep.join([gym_mod_path, env_path])

    def _script_path(self, script_base: str) -> str:
        ext = "bat" if self._is_windows else "sh"
        return os.path.join(self._repo_root, f"{script_base}.{ext}")

    def _build_script_command(self, script: str, args: list[str]) -> list[str]:
        if self._is_windows:
            return ["cmd", "/c", script, *args]
        return [script, *args]

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
        self._selected_metrics_model_id = self._extract_model_id_from_metrics_json_path(json_path)
        self._set_metrics_files(updated)
        self._refresh_metrics_summaries()
        return True

    def _select_latest_metrics(self) -> bool:
        latest_model = self._find_latest_model_file()
        if latest_model:
            metrics_id = self._extract_metrics_id(latest_model)
            if metrics_id:
                json_path = os.path.join(self._repo_root, "models", f"data_{metrics_id}.json")
                if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                    self._selected_metrics_model_path = latest_model
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
        self._selected_metrics_model_id = ""
        self._selected_metrics_model_path = ""
        self._refresh_metrics_summaries()
        self.metricsLabelChanged.emit(self._metrics_label)
        return False

    def _extract_model_id_from_metrics_json_path(self, path: str) -> str:
        base = os.path.basename(path)
        match = re.search(r"^data_(.+)\.json$", base)
        if match:
            return match.group(1)
        return ""

    def _find_run_id_for_model_id(self, model_id: str) -> str:
        if not model_id:
            return ""
        results_path = os.path.join(self._repo_root, "results.txt")
        if not os.path.exists(results_path):
            return ""
        try:
            with open(results_path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            return ""

        needle = f"model-{model_id}"
        for line in reversed(lines):
            if needle not in line:
                continue
            match = re.search(r"run_id=(\d+)", line)
            if match:
                return match.group(1)
        return ""

    def _format_metric_summary(self, values: list[float], percent: bool = False) -> str:
        if not values:
            return "Текущее: — | Среднее: — | Мин: — | Макс: —"
        current = values[-1]
        avg = sum(values) / len(values)
        min_value = min(values)
        max_value = max(values)
        if percent:
            return (
                f"Текущее: {current * 100:.2f}% | Среднее: {avg * 100:.2f}% | "
                f"Мин: {min_value * 100:.2f}% | Макс: {max_value * 100:.2f}%"
            )
        return (
            f"Текущее: {current:.4f} | Среднее: {avg:.4f} | "
            f"Мин: {min_value:.4f} | Макс: {max_value:.4f}"
        )

    def _find_stats_csv_for_run(self) -> Optional[str]:
        metrics_dir = os.path.join(self._repo_root, "metrics")
        if not os.path.isdir(metrics_dir):
            return None
        run_id = self._find_run_id_for_model_id(self._selected_metrics_model_id)
        if run_id:
            exact = os.path.join(metrics_dir, f"stats_{run_id}.csv")
            if os.path.exists(exact):
                return exact
        latest_path = None
        latest_mtime = -1.0
        for name in os.listdir(metrics_dir):
            if not (name.startswith("stats_") and name.endswith(".csv")):
                continue
            path = os.path.join(metrics_dir, name)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                continue
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest_path = path
        return latest_path

    def _parse_selected_model_counters(self, rows_count: int) -> tuple[int, int, int, int]:
        total_episodes = max(0, int(rows_count))
        snapshot_episodes = 0
        fixed_episodes = 0
        selected_run_episodes = 0

        model_id = self._selected_metrics_model_id
        if not model_id:
            return total_episodes, total_episodes, 0, 0

        logs_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS.md")
        if os.path.exists(logs_path):
            try:
                run_ep_seen = 0
                run_snapshot_seen = 0
                run_fixed_seen = 0
                with open(logs_path, "r", encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        if "[TRAIN][START]" in line:
                            run_ep_seen = 0
                            run_snapshot_seen = 0
                            run_fixed_seen = 0

                        ep_match = re.search(r"\[TRAIN\]\[EP\]\s+ep=(\d+)", line)
                        if ep_match:
                            run_ep_seen = max(run_ep_seen, int(ep_match.group(1)))

                        if "[SELFPLAY] enabled=1 mode=snapshot" in line:
                            run_snapshot_seen += 1
                        elif "[SELFPLAY] enabled=1 mode=fixed_checkpoint" in line:
                            run_fixed_seen += 1

                        if "[SAVE] pickle" in line and f"model-{model_id}.pickle" in line:
                            selected_run_episodes = run_ep_seen
                            snapshot_episodes = run_snapshot_seen
                            fixed_episodes = run_fixed_seen
            except OSError:
                pass

        if selected_run_episodes > 0:
            total_episodes = selected_run_episodes

        selfplay_total = snapshot_episodes + fixed_episodes
        heuristic_episodes = max(total_episodes - selfplay_total, 0)
        return total_episodes, heuristic_episodes, snapshot_episodes, fixed_episodes

    def _extract_selected_model_meta(self) -> dict[str, str]:
        values = {
            "global_step": "—",
            "optimize_steps": "—",
            "episode": "—",
            "replay_size": "—",
            "eps": "—",
            "source": "не определён",
            "reason": "",
        }
        model_id = self._selected_metrics_model_id
        if not model_id:
            values["reason"] = "Не выбрана модель в метриках."
            return values

        self._emit_log(f"[GUI][METRICS] Поиск state для model_id={model_id}", level="INFO")

        selected_episode = self._detect_selected_model_episode(model_id)
        candidates = self._collect_selected_model_checkpoint_candidates(model_id, selected_episode)

        if not candidates:
            self._emit_log(
                f"[GUI][METRICS] Не найдено checkpoint-файлов для model_id={model_id}, пробую fallback по логам.",
                level="WARN",
            )
            log_values = self._extract_selected_model_meta_from_logs(model_id)
            if log_values:
                values.update(log_values)
                values["source"] = "логи (fallback)"
                self._emit_log(
                    f"[GUI][METRICS] State для model_id={model_id} восстановлен из LOGS_FOR_AGENTS.md.",
                    level="INFO",
                )
                return values
            values["reason"] = "Не найден checkpoint для выбранной модели (где искали: selected/models/checkpoint_ep/logs)."
            return values

        checkpoint = None
        selected_checkpoint = ""
        try:
            import torch

            for path in candidates:
                self._emit_log(f"[GUI][METRICS] Проверяю checkpoint-кандидат: {path}", level="INFO")
                try:
                    checkpoint = torch.load(path, map_location="cpu")
                    if not isinstance(checkpoint, dict):
                        self._emit_log(
                            f"[GUI][METRICS] Кандидат отклонён: checkpoint не dict ({path}).",
                            level="WARN",
                        )
                        continue
                    selected_checkpoint = path
                    required = ["global_step", "optimize_steps", "episode"]
                    missing = [k for k in required if k not in checkpoint]
                    if missing:
                        self._emit_log(
                            f"[GUI][METRICS] Кандидат принят частично ({os.path.basename(path)}), отсутствуют ключи: {missing}.",
                            level="WARN",
                        )
                    else:
                        self._emit_log(
                            f"[GUI][METRICS] Выбран checkpoint: {path}",
                            level="INFO",
                        )
                        break
                except Exception as exc:
                    self._emit_log(
                        f"[GUI][METRICS] Кандидат отклонён: ошибка загрузки ({path}): {exc}",
                        level="WARN",
                    )
                    continue
        except Exception as exc:
            self._emit_log(
                f"[GUI][METRICS] Не удалось импортировать torch для чтения checkpoint. Детали: {exc}",
                level="WARN",
            )
            log_values = self._extract_selected_model_meta_from_logs(model_id)
            if log_values:
                values.update(log_values)
                values["source"] = "логи (fallback)"
                values["reason"] = ""
                self._emit_log(
                    f"[GUI][METRICS] torch недоступен, state для model_id={model_id} восстановлен из LOGS_FOR_AGENTS.md.",
                    level="WARN",
                )
                return values
            values["reason"] = (
                "Не удалось открыть checkpoint: torch недоступен (gui_qt/main.py:_extract_selected_model_meta). "
                "Что делать: установите torch в окружение GUI или откройте модель с доступным LOGS_FOR_AGENTS.md."
            )
            return values

        if not isinstance(checkpoint, dict):
            values["reason"] = "Checkpoint найден, но не удалось прочитать словарь state."
            return values

        values["source"] = os.path.basename(selected_checkpoint) if selected_checkpoint else "не определён"

        values["global_step"] = str(int(checkpoint.get("global_step", 0) or 0))
        values["optimize_steps"] = str(int(checkpoint.get("optimize_steps", 0) or 0))
        values["episode"] = str(int(checkpoint.get("episode", 0) or 0))

        replay = checkpoint.get("replay_memory")
        replay_size = self._extract_replay_size(replay)
        if replay_size is None:
            values["replay_size"] = "—"
            self._emit_log(
                f"[GUI][METRICS] replay_size не определён для {values['source']}: неизвестная структура replay_memory.",
                level="WARN",
            )
        else:
            values["replay_size"] = str(replay_size)

        eps_start, eps_end, eps_decay = self._load_eps_hyperparams()
        eps = self._compute_eps_for_global_step(int(values["global_step"] or 0), eps_start, eps_end, eps_decay)
        values["eps"] = f"{eps:.4f}"

        return values

    def _collect_selected_model_checkpoint_candidates(self, model_id: str, selected_episode: Optional[int]) -> list[str]:
        candidates: list[tuple[int, float, str]] = []
        seen: set[str] = set()

        def _append(priority: int, path: str) -> None:
            norm = os.path.normpath(path)
            if norm in seen:
                return
            seen.add(norm)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                mtime = 0.0
            candidates.append((priority, -mtime, path))

        if self._selected_metrics_model_path:
            direct = os.path.splitext(self._selected_metrics_model_path)[0] + ".pth"
            if os.path.exists(direct):
                _append(1, direct)
            else:
                self._emit_log(f"[GUI][METRICS] Кандидат отклонён: не существует {direct}", level="WARN")

        models_path = os.path.join(self._repo_root, "models")
        model_dirs: set[str] = set()
        if self._selected_metrics_model_path:
            model_dirs.add(os.path.dirname(self._selected_metrics_model_path))

        if os.path.isdir(models_path):
            target_name = f"model-{model_id}.pth"
            for root, _, files in os.walk(models_path):
                if target_name in files:
                    path = os.path.join(root, target_name)
                    _append(2, path)
                    model_dirs.add(root)

        checkpoint_candidates: list[tuple[int, str]] = []
        for model_dir in model_dirs:
            if not os.path.isdir(model_dir):
                continue
            for name in os.listdir(model_dir):
                if not (name.startswith("checkpoint_ep") and name.endswith(".pth")):
                    continue
                episode = self._extract_checkpoint_episode(name)
                if episode is None:
                    continue
                checkpoint_candidates.append((episode, os.path.join(model_dir, name)))

        if checkpoint_candidates:
            checkpoint_candidates.sort(key=lambda item: item[0])
            fallback_path = checkpoint_candidates[-1][1]
            if selected_episode is not None:
                eligible = [item for item in checkpoint_candidates if item[0] <= selected_episode]
                if eligible:
                    fallback_path = eligible[-1][1]
            _append(3, fallback_path)

        candidates.sort(key=lambda item: (item[0], item[1], item[2]))
        return [path for _, _, path in candidates]

    def _detect_selected_model_episode(self, model_id: str) -> Optional[int]:
        results_path = os.path.join(self._repo_root, "results.txt")
        if not os.path.exists(results_path):
            return None
        pattern = re.compile(r"model-" + re.escape(model_id) + r".*?(?:episode|ep)=(\d+)", re.IGNORECASE)
        try:
            with open(results_path, "r", encoding="utf-8", errors="replace") as handle:
                for line in reversed(handle.readlines()):
                    match = pattern.search(line)
                    if match:
                        return int(match.group(1))
        except OSError:
            return None
        return None

    def _extract_replay_size(self, replay: object) -> Optional[int]:
        if not isinstance(replay, dict):
            return None
        for key in ("size", "length", "count"):
            if key in replay:
                try:
                    return int(replay.get(key, 0) or 0)
                except (TypeError, ValueError):
                    continue
        for key in ("memory", "items", "list", "deque"):
            value = replay.get(key)
            if hasattr(value, "__len__"):
                try:
                    return len(value)
                except TypeError:
                    continue
        nested = replay.get("buffer")
        if isinstance(nested, dict):
            for value in nested.values():
                if hasattr(value, "__len__"):
                    try:
                        return len(value)
                    except TypeError:
                        continue
        return None

    def _load_eps_hyperparams(self) -> tuple[float, float, float]:
        defaults = (0.9, 0.05, 20000.0)
        try:
            with open(os.path.join(self._repo_root, "hyperparams.json"), "r", encoding="utf-8", errors="replace") as handle:
                hp = json.load(handle)
            eps_start = float(hp.get("eps_start", defaults[0]))
            eps_end = float(hp.get("eps_end", defaults[1]))
            eps_decay = max(1.0, float(hp.get("eps_decay", defaults[2])))
            return eps_start, eps_end, eps_decay
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            self._emit_log(
                "[GUI][METRICS] Не удалось прочитать hyperparams.json, использую defaults eps_start=0.9 eps_end=0.05 eps_decay=20000. "
                f"Детали: {exc}",
                level="WARN",
            )
            return defaults

    def _compute_eps_for_global_step(self, global_step: int, eps_start: float, eps_end: float, eps_decay: float) -> float:
        progress = min(float(max(global_step, 0)) / max(1.0, float(eps_decay)), 1.0)
        return eps_start + (eps_end - eps_start) * progress

    def _extract_selected_model_meta_from_logs(self, model_id: str) -> dict[str, str]:
        logs_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS.md")
        if not os.path.exists(logs_path):
            return {}
        try:
            with open(logs_path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            return {}

        save_idx = -1
        needle = f"model-{model_id}.pickle"
        for idx, line in enumerate(lines):
            if "[SAVE] pickle" in line and needle in line:
                save_idx = idx
        if save_idx < 0:
            return {}

        start_idx = 0
        for idx in range(save_idx, -1, -1):
            if "[TRAIN][START]" in lines[idx]:
                start_idx = idx
                break
        scope = lines[start_idx : save_idx + 1]
        payload: dict[str, str] = {}
        for line in scope:
            for key in ("global_step", "optimize_steps", "episode", "replay_size"):
                match = re.search(rf"{key}=(\d+)", line)
                if match:
                    payload[key] = match.group(1)
        if "episode" not in payload:
            for line in scope:
                ep_match = re.search(r"\[TRAIN\]\[EP\]\s+ep=(\d+)", line)
                if ep_match:
                    payload["episode"] = ep_match.group(1)
        if not payload:
            return {}
        payload.setdefault("global_step", "—")
        payload.setdefault("optimize_steps", "—")
        payload.setdefault("episode", "—")
        payload.setdefault("replay_size", "—")
        eps_start, eps_end, eps_decay = self._load_eps_hyperparams()
        try:
            gs = int(payload["global_step"])
            payload["eps"] = f"{self._compute_eps_for_global_step(gs, eps_start, eps_end, eps_decay):.4f}"
        except (TypeError, ValueError):
            payload["eps"] = "—"
        return payload

    def _refresh_metrics_summaries(self) -> None:
        defaults = {
            "reward": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "loss": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "epLen": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "winrate": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "vpdiff": "Текущее: — | Среднее: — | Мин: — | Макс: —",
        }
        summaries = dict(defaults)
        csv_path = self._find_stats_csv_for_run()
        rows: list[dict[str, str]] = []
        if csv_path and os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding="utf-8", errors="replace") as handle:
                    reader = csv.DictReader(handle)
                    rows = list(reader)
            except (OSError, csv.Error):
                rows = []

        if rows:
            rewards = [float(r.get("ep_reward", 0.0) or 0.0) for r in rows]
            ep_len = [float(r.get("ep_len", 0.0) or 0.0) for r in rows]
            vp_diff = [float(r.get("vp_diff", 0.0) or 0.0) for r in rows]
            wins = [1.0 if (r.get("result") or "").strip() == "win" else 0.0 for r in rows]
            losses = []
            for idx in range(1, len(rows) + 1):
                loss_match = re.search(r"loss=([\d\.eE+-]+)", rows[idx - 1].get("loss", ""))
                if loss_match:
                    losses.append(float(loss_match.group(1)))

            summaries["reward"] = self._format_metric_summary(rewards)
            summaries["epLen"] = self._format_metric_summary(ep_len)
            summaries["vpdiff"] = self._format_metric_summary(vp_diff)
            summaries["winrate"] = self._format_metric_summary(wins, percent=True)
            if losses:
                summaries["loss"] = self._format_metric_summary(losses)

        total, heuristic, snapshot, fixed = self._parse_selected_model_counters(len(rows))
        resume = self._extract_selected_model_meta()
        model_state = (
            "Эпизоды\n"
            f"• Всего: {total}\n"
            f"• Против эвристики: {heuristic}\n"
            f"• Self-play snapshot: {snapshot}\n"
            f"• Self-play fixed: {fixed}\n\n"
            "Состояние модели\n"
            f"• global_step: {resume['global_step']}\n"
            f"• optimize_steps: {resume['optimize_steps']}\n"
            f"• episode: {resume['episode']}\n"
            f"• replay_size: {resume['replay_size']}\n"
            f"• eps: {resume['eps']}\n"
            f"Источник state: {resume.get('source', 'не определён')}"
        )
        reason = (resume.get("reason") or "").strip()
        if reason:
            model_state += f"\nПричина: {reason}"

        self._metric_summary_texts = summaries
        self._model_state_text = model_state
        self.metricsSummaryChanged.emit()

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

    def _find_latest_checkpoint_file(self) -> Optional[str]:
        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None
        latest_path = None
        latest_mtime = -1.0
        for root, _, files in os.walk(models_path):
            for name in files:
                if not name.startswith("checkpoint_ep"):
                    continue
                if not name.endswith(".pth"):
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

    def _extract_checkpoint_episode(self, filename: str) -> Optional[int]:
        match = re.search(r"checkpoint_ep(\d+)\.pth$", filename)
        if not match:
            return None
        return int(match.group(1))

    def _find_best_checkpoint_by_episode(self) -> Optional[str]:
        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None

        best_path = None
        best_episode = -1
        best_mtime = -1.0

        for root, _, files in os.walk(models_path):
            for name in files:
                episode = self._extract_checkpoint_episode(name)
                if episode is None:
                    continue
                path = os.path.join(root, name)
                try:
                    mtime = os.path.getmtime(path)
                except OSError:
                    continue

                if episode > best_episode or (episode == best_episode and mtime > best_mtime):
                    best_episode = episode
                    best_mtime = mtime
                    best_path = path

        return best_path

    def _find_eval_pickle_for_checkpoint(self, checkpoint_path: str) -> Optional[str]:
        checkpoint_dir = os.path.dirname(checkpoint_path)
        checkpoint_stem, _ = os.path.splitext(checkpoint_path)
        direct_pickle = f"{checkpoint_stem}.pickle"
        if os.path.exists(direct_pickle):
            return direct_pickle

        best_pickle = None
        best_mtime = -1.0
        try:
            entries = os.listdir(checkpoint_dir)
        except OSError:
            return None

        for name in entries:
            if not (name.endswith(".pickle") and name.startswith("model-")):
                continue
            candidate = os.path.join(checkpoint_dir, name)
            try:
                mtime = os.path.getmtime(candidate)
            except OSError:
                continue
            if mtime > best_mtime:
                best_mtime = mtime
                best_pickle = candidate

        return best_pickle

    def _find_latest_resume_file(self) -> Optional[str]:
        checkpoint_path = self._find_latest_checkpoint_file()
        if checkpoint_path:
            return checkpoint_path

        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None

        latest_path = None
        latest_mtime = -1.0
        for root, _, files in os.walk(models_path):
            for name in files:
                if not (name.startswith("model-") and name.endswith(".pth")):
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
        self._replace_model_items(
            self._available_model,
            [f"{unit.name} (x{unit.default_count})" for unit in self._available_units],
        )
        self._replace_model_items(
            self._player_model,
            [f"{entry.name} (x{entry.count})" for entry in self._player_roster],
        )
        self._replace_model_items(
            self._model_model,
            [f"{entry.name} (x{entry.count})" for entry in self._model_roster],
        )

    def _replace_model_items(self, model: QtGui.QStandardItemModel, values: list[str]) -> None:
        model.clear()
        for value in values:
            icon = self.get_unit_icon(value)
            item = QtGui.QStandardItem(value)
            item.setEditable(False)
            item.setData(icon, QtCore.Qt.DecorationRole)
            item.setData(self.get_unit_icon_source(value), QtCore.Qt.UserRole + 1)
            model.appendRow(item)

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
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("40kAI.GUI")

    app = QtGui.QGuiApplication(sys.argv)

    icon_path = os.path.join(os.path.dirname(__file__), "assets", "40kai_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    engine = QtQml.QQmlApplicationEngine()

    controller = GUIController()
    engine.rootContext().setContextProperty("controller", controller)

    qml_path = os.path.join(os.path.dirname(__file__), "qml", "Main.qml")
    engine.load(QtCore.QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        return 1

    if os.path.exists(icon_path):
        root = engine.rootObjects()[0]
        if hasattr(root, "setIcon"):
            root.setIcon(QIcon(icon_path))

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
