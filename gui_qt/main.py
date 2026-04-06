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
    heuristicMetricsChanged = QtCore.Signal()
    playModelPathChanged = QtCore.Signal(str)
    playModelLabelChanged = QtCore.Signal(str)
    playModelMetaChanged = QtCore.Signal(str)
    playViewerPlayerRoleLabelChanged = QtCore.Signal(str)
    playViewerModelRoleLabelChanged = QtCore.Signal(str)
    evalModelPathChanged = QtCore.Signal(str)
    evalModelLabelChanged = QtCore.Signal(str)
    evalGamesChanged = QtCore.Signal(int)
    evalLogTextChanged = QtCore.Signal(str)
    evalSummaryTextChanged = QtCore.Signal(str)
    boardTextChanged = QtCore.Signal(str)
    selfPlayFromCheckpointChanged = QtCore.Signal(bool)
    resumeFromCheckpointChanged = QtCore.Signal(bool)
    disableTrainLoggingChanged = QtCore.Signal(bool)
    actionTraceChanged = QtCore.Signal(bool)
    autoClearLogsChanged = QtCore.Signal(bool)
    factionIconSizeChanged = QtCore.Signal(int)
    unitIconSizeChanged = QtCore.Signal(int)
    deploymentModeChanged = QtCore.Signal(str)
    learnerSideChanged = QtCore.Signal(str)
    learnerFactionChanged = QtCore.Signal(str)
    opponentPolicyChanged = QtCore.Signal(str)
    opponentSourceChanged = QtCore.Signal(str)
    specificOpponentOptionsChanged = QtCore.Signal()
    selectedSpecificOpponentIdChanged = QtCore.Signal(str)
    opponentPreviewTextChanged = QtCore.Signal(str)
    trainingHyperparamsChanged = QtCore.Signal()
    settingsDirtyChanged = QtCore.Signal(bool)
    settingsSaveStateChanged = QtCore.Signal(str)
    trainingAlgoChanged = QtCore.Signal(str)

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
        self._metrics_run_id = ""
        self._metrics_meta: dict[str, str] = {}
        # Быстрые значения для верхней summary-панели (последняя точка DET-eval).
        self._det_last = {
            "episode": "—",
            "winrate": "—",
            "reward": "—",
            "ep_len": "—",
            "train_loss": "—",
        }
        self._heuristic_metrics: dict[str, object] = {}
        self._heuristic_metrics_text = "Нет данных метрик эвристики."
        self._metric_summary_texts = {
            "reward": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "loss": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "epLen": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "winrate": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "avgvp": "Модель: — | Противник: —",
            "endreasons": "Последняя точка: —",
        }
        self._model_state_text = "Нет данных о состоянии модели."

        self._play_model_path = ""
        self._play_model_label = "Модель не выбрана"
        self._play_model_algo_label = "Алгоритм: —"
        self._play_model_checkpoint_label = "Checkpoint: —"
        self._play_viewer_player_role_label = "Ты: —"
        self._play_viewer_model_role_label = "ИИ: —"
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
        self._action_trace = str(os.getenv("ACTION_TRACE_ENABLED", "0")).strip() == "1"
        self._auto_clear_logs = True
        self._unit_faction_by_name: dict[str, str] = {}
        self._deployment_mode_options = ["manual_player", "auto", "rl_phase"]
        self._deployment_mode = str(os.getenv("DEPLOYMENT_MODE", "rl_phase")).strip().lower() or "rl_phase"
        if self._deployment_mode not in self._deployment_mode_options:
            self._deployment_mode = "rl_phase"
        self._learner_side_options = ["P1", "P2"]
        self._learner_side = str(os.getenv("LEARNER_SIDE", "P1")).strip().upper() or "P1"
        if self._learner_side not in self._learner_side_options:
            self._learner_side = "P1"
        self._learner_faction_options = ["Necrons", "SpaceMarines", "AstraMilitarum", "Aeldari"]
        self._learner_faction = str(os.getenv("LEARNER_FACTION", "Necrons")).strip() or "Necrons"
        if self._learner_faction not in self._learner_faction_options:
            self._learner_faction = "Necrons"
        self._opponent_policy_options = ["mirror", "cross_faction", "league"]
        self._opponent_policy = str(os.getenv("OPPONENT_POLICY", "mirror")).strip().lower() or "mirror"
        if self._opponent_policy not in self._opponent_policy_options:
            self._opponent_policy = "mirror"
        self._opponent_source_options = ["heuristic", "latest_snapshot", "specific_agent"]
        self._opponent_source = str(os.getenv("OPPONENT_SOURCE", "heuristic")).strip().lower() or "heuristic"
        if self._opponent_source not in self._opponent_source_options:
            self._opponent_source = "heuristic"
        self._specific_opponent_agent_ids: list[str] = []
        self._specific_opponent_agent_labels: list[str] = []
        self._specific_opponent_algo_by_id: dict[str, str] = {}
        self._selected_specific_opponent_id = ""
        self._opponent_preview_text = "Сейчас будет: —"

        self._training_algo_options = ["dqn", "ppo"]
        self._training_algo = str(os.getenv("TRAIN_ALGO", "dqn")).strip().lower() or "dqn"
        if self._training_algo not in self._training_algo_options:
            self._training_algo = "dqn"

        self._hyperparams_path = os.path.join(self._repo_root, "hyperparams.json")
        self._default_hyperparams = {
            "lr": 0.0001,
            "tau": 0.01,
            "eps_start": 0.9,
            "eps_end": 0.05,
            "eps_decay": 30000,
            "batch_size": 384,
            "gamma": 0.99,
            "updates_per_step": 6,
            "warmup_steps": 5000,
        }
        # Секция hyperparams.json["ppo"] — читает train.py (PPO_LR, PPO_GAMMA, …).
        self._default_ppo_hyperparams: dict[str, int | float] = {
            "learning_rate": 0.0003,
            "gamma": 0.99,
            "gae_lambda": 0.95,
            "clip_ratio": 0.2,
            "value_coef": 0.5,
            "entropy_coef": 0.01,
            "rollout_steps": 1024,
            "update_epochs": 4,
            "minibatch_size": 256,
            "max_grad_norm": 0.5,
            "target_kl": 0.03,
        }
        self._hyperparams = dict(self._default_hyperparams)
        self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
        self._settings_dirty = False
        self._settings_save_state = "✓ Сохранено"
        self._load_hyperparams_from_disk(log_errors=True)

        self._load_available_units()
        self._load_rosters_from_file()
        self._update_learner_faction_from_rosters()
        self._refresh_models()
        self._select_latest_metrics()
        self._load_latest_heuristic_metrics()
        self._select_latest_play_model(initial=True)
        self._select_latest_eval_model(initial=True)
        self._update_roster_summary()
        self._refresh_specific_opponent_options()

        self._emit_status("Нажмите «Тренировка 8х», чтобы запустить обучение.")

    def _infer_faction_from_roster(self, roster: list[RosterEntry]) -> str:
        if not roster:
            return self._learner_faction
        first_name = str(roster[0].name or "").strip()
        if not first_name:
            return self._learner_faction
        return self._unit_faction_by_name.get(first_name, self._learner_faction)

    def _update_learner_faction_from_rosters(self) -> None:
        # Фракция обучения берётся из ростера той стороны, которая выбрана как learner.
        if self._learner_side == "P1":
            inferred = self._infer_faction_from_roster(self._player_roster)
        else:
            inferred = self._infer_faction_from_roster(self._model_roster)
        if inferred and inferred != self._learner_faction:
            self._learner_faction = inferred
            try:
                self.learnerFactionChanged.emit(inferred)
            except Exception:
                pass
        self._update_opponent_preview_text()

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
    def metricsAvgVpPath(self) -> str:
        return self._metrics_paths["avgvp"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsHpDiffPath(self) -> str:
        return self._metrics_paths["hpdiff"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsKillDiffPath(self) -> str:
        return self._metrics_paths["killdiff"]

    @QtCore.Property(str, notify=metricsChanged)
    def metricsEndReasonPath(self) -> str:
        return self._metrics_paths["endreasons"]

    @QtCore.Property(str, notify=metricsLabelChanged)
    def metricsLabel(self) -> str:
        return self._metrics_label

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def metricsRunId(self) -> str:
        return str(self._metrics_run_id or "")

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def detEpisodeLast(self) -> str:
        return str(self._det_last.get("episode", "—"))

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def detWinrateLast(self) -> str:
        return str(self._det_last.get("winrate", "—"))

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def detRewardLast(self) -> str:
        return str(self._det_last.get("reward", "—"))

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def detEpLenLast(self) -> str:
        return str(self._det_last.get("ep_len", "—"))

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def detTrainLossLast(self) -> str:
        return str(self._det_last.get("train_loss", "—"))

    @QtCore.Property(int, constant=True)
    def detEvalEpisodes(self) -> int:
        # Параметры DET-eval для actor-learner (по умолчанию).
        try:
            return max(1, int(os.getenv("ACTOR_DET_EVAL_EPISODES", "12")))
        except ValueError:
            return 12

    @QtCore.Property(int, constant=True)
    def detEvalEvery(self) -> int:
        try:
            return max(1, int(os.getenv("ACTOR_DET_EVAL_EVERY_EPISODES", "100")))
        except ValueError:
            return 100

    @QtCore.Property(bool, constant=True)
    def selfPlayEnabled(self) -> bool:
        return str(os.getenv("SELF_PLAY_ENABLED", "0") or "0").strip() == "1"

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def opponentInfoLine(self) -> str:
        side = str(self._metrics_meta.get("opponent_side", "")).strip()
        faction = str(self._metrics_meta.get("opponent_faction", "")).strip()
        algo = str(self._metrics_meta.get("opponent_algo", "")).strip()
        source = str(self._metrics_meta.get("opponent_source", "")).strip()
        if not (side or faction or algo or source):
            return "Оппонент: —"
        parts = []
        if side or faction:
            parts.append(f"{side or '?'} ({faction or '?'})")
        if algo:
            parts.append(f"algo={algo}")
        if source:
            parts.append(f"source={source}")
        return "Оппонент: " + " | ".join(parts)

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def opponentSource(self) -> str:
        # Предпочитаем meta из data_*.json; иначе — текущая настройка GUI.
        v = str(self._metrics_meta.get("opponent_source", "")).strip()
        if v:
            return self._opponent_source_label(v)
        return self._opponent_source_label(str(self._opponent_source or ""))

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def opponentAlgo(self) -> str:
        v = str(self._metrics_meta.get("opponent_algo", "")).strip()
        if v:
            return str(v).upper()
        # Фолбэк: если self-play выключен — это эвристика.
        if str(os.getenv("SELF_PLAY_ENABLED", "0") or "0").strip() != "1":
            return "ЭВРИСТИКА"
        # Если self-play включён, но algo неизвестен, пусть будет "policy".
        return "POLICY"

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def opponentId(self) -> str:
        v = str(self._metrics_meta.get("opponent_id", "")).strip()
        return v

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
        # legacy accessor: оставляем имя для совместимости, но теперь это HP diff
        return self._metric_summary_texts["hpdiff"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def avgVpSummary(self) -> str:
        return self._metric_summary_texts["avgvp"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def hpDiffSummary(self) -> str:
        return self._metric_summary_texts["hpdiff"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def killDiffSummary(self) -> str:
        return self._metric_summary_texts["killdiff"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def endReasonSummary(self) -> str:
        return self._metric_summary_texts["endreasons"]

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def modelStateText(self) -> str:
        return self._model_state_text

    @QtCore.Property(str, notify=heuristicMetricsChanged)
    def heuristicMetricsText(self) -> str:
        return self._heuristic_metrics_text

    @QtCore.Property(str, notify=playModelPathChanged)
    def playModelPath(self) -> str:
        return self._play_model_path

    @QtCore.Property(str, notify=playModelLabelChanged)
    def playModelLabel(self) -> str:
        return self._play_model_label

    @QtCore.Property(str, notify=playModelMetaChanged)
    def playModelAlgoLabel(self) -> str:
        return self._play_model_algo_label

    @QtCore.Property(str, notify=playModelMetaChanged)
    def playModelCheckpointLabel(self) -> str:
        return self._play_model_checkpoint_label

    @QtCore.Property(str, notify=playViewerPlayerRoleLabelChanged)
    def playViewerPlayerRoleLabel(self) -> str:
        return self._play_viewer_player_role_label

    @QtCore.Property(str, notify=playViewerModelRoleLabelChanged)
    def playViewerModelRoleLabel(self) -> str:
        return self._play_viewer_model_role_label

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

    @QtCore.Property(bool, notify=actionTraceChanged)
    def actionTrace(self) -> bool:
        return self._action_trace

    @QtCore.Property(bool, notify=autoClearLogsChanged)
    def autoClearLogs(self) -> bool:
        return self._auto_clear_logs


    @QtCore.Property("QStringList", constant=True)
    def deploymentModeOptions(self):
        return self._deployment_mode_options

    @QtCore.Property(str, notify=deploymentModeChanged)
    def deploymentMode(self) -> str:
        return self._deployment_mode

    @QtCore.Property("QStringList", constant=True)
    def learnerSideOptions(self):
        return self._learner_side_options

    @QtCore.Property(str, notify=learnerSideChanged)
    def learnerSide(self) -> str:
        return self._learner_side

    @QtCore.Property("QStringList", constant=True)
    def learnerFactionOptions(self):
        return self._learner_faction_options

    @QtCore.Property(str, notify=learnerFactionChanged)
    def learnerFaction(self) -> str:
        return self._learner_faction

    @QtCore.Property("QStringList", constant=True)
    def opponentPolicyOptions(self):
        return self._opponent_policy_options

    @QtCore.Property(str, notify=opponentPolicyChanged)
    def opponentPolicy(self) -> str:
        return self._opponent_policy

    @QtCore.Property("QStringList", constant=True)
    def opponentSourceOptions(self):
        return self._opponent_source_options

    @QtCore.Property(str, notify=opponentSourceChanged)
    def opponentSource(self) -> str:
        return self._opponent_source

    @QtCore.Property("QStringList", notify=specificOpponentOptionsChanged)
    def specificOpponentAgentOptions(self):
        return self._specific_opponent_agent_labels

    @QtCore.Property(str, notify=selectedSpecificOpponentIdChanged)
    def selectedSpecificOpponentId(self) -> str:
        return self._selected_specific_opponent_id

    @QtCore.Property(str, notify=selectedSpecificOpponentIdChanged)
    def selectedSpecificOpponentLabel(self) -> str:
        if not self._selected_specific_opponent_id:
            return ""
        try:
            idx = self._specific_opponent_agent_ids.index(self._selected_specific_opponent_id)
        except ValueError:
            return ""
        if 0 <= idx < len(self._specific_opponent_agent_labels):
            return self._specific_opponent_agent_labels[idx]
        return ""

    @QtCore.Property(str, notify=opponentPreviewTextChanged)
    def opponentPreviewText(self) -> str:
        return self._opponent_preview_text

    @QtCore.Property("QStringList", constant=True)
    def trainingAlgoOptions(self):
        return self._training_algo_options

    @QtCore.Property(str, notify=trainingAlgoChanged)
    def trainingAlgo(self) -> str:
        return self._training_algo

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpLr(self) -> float:
        return float(self._hyperparams.get("lr", self._default_hyperparams["lr"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpTau(self) -> float:
        return float(self._hyperparams.get("tau", self._default_hyperparams["tau"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpEpsStart(self) -> float:
        return float(self._hyperparams.get("eps_start", self._default_hyperparams["eps_start"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpEpsEnd(self) -> float:
        return float(self._hyperparams.get("eps_end", self._default_hyperparams["eps_end"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpEpsDecay(self) -> int:
        return int(self._hyperparams.get("eps_decay", self._default_hyperparams["eps_decay"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpBatchSize(self) -> int:
        return int(self._hyperparams.get("batch_size", self._default_hyperparams["batch_size"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpGamma(self) -> float:
        return float(self._hyperparams.get("gamma", self._default_hyperparams["gamma"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpUpdatesPerStep(self) -> int:
        return int(self._hyperparams.get("updates_per_step", self._default_hyperparams["updates_per_step"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpWarmupSteps(self) -> int:
        return int(self._hyperparams.get("warmup_steps", self._default_hyperparams["warmup_steps"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoLearningRate(self) -> float:
        return float(self._ppo_hyperparams.get("learning_rate", self._default_ppo_hyperparams["learning_rate"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoGamma(self) -> float:
        return float(self._ppo_hyperparams.get("gamma", self._default_ppo_hyperparams["gamma"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoGaeLambda(self) -> float:
        return float(self._ppo_hyperparams.get("gae_lambda", self._default_ppo_hyperparams["gae_lambda"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoClipRatio(self) -> float:
        return float(self._ppo_hyperparams.get("clip_ratio", self._default_ppo_hyperparams["clip_ratio"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoValueCoef(self) -> float:
        return float(self._ppo_hyperparams.get("value_coef", self._default_ppo_hyperparams["value_coef"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoEntropyCoef(self) -> float:
        return float(self._ppo_hyperparams.get("entropy_coef", self._default_ppo_hyperparams["entropy_coef"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpPpoRolloutSteps(self) -> int:
        return int(self._ppo_hyperparams.get("rollout_steps", self._default_ppo_hyperparams["rollout_steps"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpPpoUpdateEpochs(self) -> int:
        return int(self._ppo_hyperparams.get("update_epochs", self._default_ppo_hyperparams["update_epochs"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpPpoMinibatchSize(self) -> int:
        return int(self._ppo_hyperparams.get("minibatch_size", self._default_ppo_hyperparams["minibatch_size"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoMaxGradNorm(self) -> float:
        return float(self._ppo_hyperparams.get("max_grad_norm", self._default_ppo_hyperparams["max_grad_norm"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpPpoTargetKl(self) -> float:
        return float(self._ppo_hyperparams.get("target_kl", self._default_ppo_hyperparams["target_kl"]))

    @QtCore.Property(bool, notify=settingsDirtyChanged)
    def settingsDirty(self) -> bool:
        return self._settings_dirty

    @QtCore.Property(str, notify=settingsSaveStateChanged)
    def settingsSaveState(self) -> str:
        return self._settings_save_state

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
        self._update_learner_faction_from_rosters()
        self._emit_status("Юнит добавлен в ростер P1.")

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
        self._update_learner_faction_from_rosters()
        self._emit_status("Юнит добавлен в ростер P2.")

    @QtCore.Slot(int)
    def remove_player_unit(self, index: int) -> None:
        if index < 0 or index >= len(self._player_roster):
            self._emit_status("Сначала выберите юнит P1 для удаления.")
            return
        self._player_roster.pop(index)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Юнит удалён из ростера P1.")

    @QtCore.Slot(int)
    def remove_model_unit(self, index: int) -> None:
        if index < 0 or index >= len(self._model_roster):
            self._emit_status("Сначала выберите юнит P2 для удаления.")
            return
        self._model_roster.pop(index)
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Юнит удалён из ростера P2.")

    @QtCore.Slot()
    def clear_player_roster(self) -> None:
        self._player_roster.clear()
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Ростер P1 очищен.")

    @QtCore.Slot()
    def clear_model_roster(self) -> None:
        self._model_roster.clear()
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Ростер P2 очищен.")

    @QtCore.Slot()
    def start_train(self) -> None:
        self._start_training(mode="train")

    @QtCore.Slot()
    def start_train_8x(self) -> None:
        # Единая кнопка "Тренировка 8х": режим выбирается по источнику оппонента.
        # Эвристика -> обычная тренировка, модель/агент -> self-play.
        mode = "selfplay" if self._opponent_source in {"latest_snapshot", "specific_agent"} else "train8"
        self._start_training(mode=mode)

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

    @QtCore.Slot(bool)
    @QtCore.Slot(bool)
    def set_action_trace(self, value: bool) -> None:
        flag = bool(value)
        if self._action_trace == flag:
            return
        self._action_trace = flag
        self.actionTraceChanged.emit(flag)

    @QtCore.Slot(bool)
    def set_auto_clear_logs(self, value: bool) -> None:
        flag = bool(value)
        if self._auto_clear_logs == flag:
            return
        self._auto_clear_logs = flag
        self.autoClearLogsChanged.emit(flag)


    @QtCore.Slot(str)
    def set_deployment_mode(self, value: str) -> None:
        mode = str(value or "").strip().lower()
        if mode not in self._deployment_mode_options:
            mode = "rl_phase"
        if self._deployment_mode == mode:
            return
        self._deployment_mode = mode
        self.deploymentModeChanged.emit(mode)
        self._emit_log(f"[GUI] DEPLOYMENT_MODE={mode}", level="INFO")
        self._emit_status(f"Режим деплоя: {self._deployment_mode_label(mode)}")
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_learner_side(self, value: str) -> None:
        side = str(value or "").strip().upper()
        if side not in self._learner_side_options:
            side = "P1"
        if side == self._learner_side:
            return
        self._learner_side = side
        self.learnerSideChanged.emit(side)
        self._update_learner_faction_from_rosters()
        self._refresh_specific_opponent_options()
        self._emit_status(f"Сторона обучения: {side}")
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_learner_faction(self, value: str) -> None:
        faction = str(value or "").strip() or "Necrons"
        if faction not in self._learner_faction_options:
            faction = "Necrons"
        if faction == self._learner_faction:
            return
        self._learner_faction = faction
        self.learnerFactionChanged.emit(faction)
        self._emit_status(f"Фракция обучения: {faction}")
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_opponent_policy(self, value: str) -> None:
        policy = str(value or "").strip().lower()
        if policy not in self._opponent_policy_options:
            policy = "mirror"
        if policy == self._opponent_policy:
            return
        self._opponent_policy = policy
        self.opponentPolicyChanged.emit(policy)
        self._emit_status(f"Политика оппонента: {policy}")
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_opponent_source(self, value: str) -> None:
        source = str(value or "").strip().lower()
        if source not in self._opponent_source_options:
            source = "latest_snapshot"
        if source == self._opponent_source:
            return
        self._opponent_source = source
        self.opponentSourceChanged.emit(source)
        self._refresh_specific_opponent_options()
        if source == "latest_snapshot" and self._specific_opponent_agent_ids:
            latest_id = self._specific_opponent_agent_ids[0]
            if latest_id != self._selected_specific_opponent_id:
                self._selected_specific_opponent_id = latest_id
                self.selectedSpecificOpponentIdChanged.emit(self._selected_specific_opponent_id)
                self._update_opponent_preview_text()
        self._emit_status(f"Источник оппонента: {self._opponent_source_label(source)}")
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_specific_opponent_agent(self, agent_id: str) -> None:
        normalized = str(agent_id or "").strip()
        if normalized and normalized not in self._specific_opponent_agent_ids:
            normalized = ""
        if normalized == self._selected_specific_opponent_id:
            return
        self._selected_specific_opponent_id = normalized
        self.selectedSpecificOpponentIdChanged.emit(self._selected_specific_opponent_id)
        self._update_opponent_preview_text()
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def set_specific_opponent_agent_by_label(self, label: str) -> None:
        text = str(label or "").strip()
        if not text:
            self.set_specific_opponent_agent("")
            return
        try:
            idx = self._specific_opponent_agent_labels.index(text)
        except ValueError:
            return
        if 0 <= idx < len(self._specific_opponent_agent_ids):
            self.set_specific_opponent_agent(self._specific_opponent_agent_ids[idx])

    @QtCore.Slot(str)
    def set_training_algo(self, value: str) -> None:
        algo = str(value or "").strip().lower()
        if algo not in self._training_algo_options:
            algo = "dqn"
        if algo == self._training_algo:
            return
        self._training_algo = algo
        self.trainingAlgoChanged.emit(algo)
        self._emit_log(f"[GUI] TRAIN_ALGO={algo}", level="INFO")
        self._emit_status(f"Алгоритм обучения: {algo}")
        # Превью матча зависит от TRAIN_ALGO (PPO/DQN), поэтому обновляем сразу.
        self._refresh_specific_opponent_options()
        self._update_opponent_preview_text()
        self.mark_settings_dirty()

    def _deployment_mode_label(self, mode: str) -> str:
        labels = {
            "manual_player": "Ручной игрок (клик в Viewer)",
            "auto": "Авто-деплой",
            "rl_phase": "RL-деплой модели (игрок вручную)",
        }
        return labels.get(mode, mode)

    def _opponent_source_label(self, source: str) -> str:
        labels = {
            "heuristic": "Эвристика",
            "latest_snapshot": "Последний снапшот",
            "specific_agent": "Конкретный агент",
        }
        return labels.get(source, source)

    def _collect_registered_agents_meta(self) -> list[dict[str, str]]:
        agents_root = os.path.join(self._repo_root, "models", "agents")
        if not os.path.isdir(agents_root):
            return []
        records: list[dict[str, str]] = []
        for root, _, files in os.walk(agents_root):
            if "meta.json" not in files:
                continue
            meta_path = os.path.join(root, "meta.json")
            try:
                with open(meta_path, "r", encoding="utf-8") as handle:
                    payload = json.load(handle)
            except (OSError, json.JSONDecodeError):
                continue
            agent_id = str(payload.get("agent_id", "")).strip()
            side = str(payload.get("side", "")).strip().upper()
            faction = str(payload.get("faction", "")).strip()
            created_at = str(payload.get("created_at", "")).strip()
            algo = str(payload.get("algo", "")).strip().lower()
            if algo not in {"dqn", "ppo"}:
                # Backward-compat: старые снапшоты могли не писать "algo" в meta.json.
                # Инферим по наличию target.pth: у DQN он есть, у PPO обычно отсутствует.
                paths = payload.get("paths") if isinstance(payload, dict) else None
                if isinstance(paths, dict):
                    target_path = paths.get("target")
                    algo = "ppo" if (target_path is None or str(target_path).strip() == "") else "dqn"
                else:
                    algo = "unknown"
            if not agent_id or side not in {"P1", "P2"}:
                continue
            records.append(
                {
                    "agent_id": agent_id,
                    "side": side,
                    "faction": faction or "Unknown",
                    "created_at": created_at,
                    "algo": algo,
                }
            )
        records.sort(key=lambda item: (item.get("created_at", ""), item["agent_id"]), reverse=True)
        return records

    def _refresh_specific_opponent_options(self) -> None:
        opposite_side = "P2" if self._learner_side == "P1" else "P1"
        records = [rec for rec in self._collect_registered_agents_meta() if rec.get("side") == opposite_side]
        self._specific_opponent_algo_by_id = {str(rec.get("agent_id")): str(rec.get("algo", "unknown")) for rec in records}
        self._specific_opponent_agent_ids = [str(rec["agent_id"]) for rec in records]
        self._specific_opponent_agent_labels = [
            self._format_agent_label(rec) for rec in records
        ]
        if self._selected_specific_opponent_id not in self._specific_opponent_agent_ids:
            self._selected_specific_opponent_id = self._specific_opponent_agent_ids[0] if self._specific_opponent_agent_ids else ""
            self.selectedSpecificOpponentIdChanged.emit(self._selected_specific_opponent_id)
        self.specificOpponentOptionsChanged.emit()
        self._update_opponent_preview_text()

    def _format_agent_label(self, rec: dict[str, str]) -> str:
        agent_id = str(rec.get("agent_id", "")).strip()
        faction = str(rec.get("faction", "Unknown")).strip() or "Unknown"
        algo = str(rec.get("algo", "unknown")).strip().lower() or "unknown"
        side = str(rec.get("side", "")).strip().upper()
        if side in {"P1", "P2"} and agent_id.startswith(side + "_"):
            rest = agent_id[len(side) + 1:]
            pretty = f"{side}_{algo}_{rest}"
        else:
            pretty = f"{agent_id}"
            if side in {"P1", "P2"}:
                pretty = f"{side}_{algo}_{agent_id}"
        return f"{pretty} ({faction})"

    def _display_faction_for_side(self, side: str) -> str:
        normalized_side = str(side or "").strip().upper()
        if normalized_side == "P1":
            return self._infer_faction_from_roster(self._player_roster)
        if normalized_side == "P2":
            return self._infer_faction_from_roster(self._model_roster)
        return "Unknown"

    def _update_opponent_preview_text(self) -> None:
        learner_side = self._learner_side
        opponent_side = "P2" if learner_side == "P1" else "P1"
        learner_faction = self._display_faction_for_side(learner_side)
        opponent_faction = self._display_faction_for_side(opponent_side)
        learner_algo = (self._training_algo or "dqn").strip().lower()
        if learner_algo not in {"dqn", "ppo"}:
            learner_algo = "dqn"

        opponent_algo = "unknown"
        if self._opponent_source == "heuristic":
            opponent_algo = "heuristic"
        elif self._selected_specific_opponent_id:
            lookup = getattr(self, "_specific_opponent_algo_by_id", {})
            opponent_algo = str(lookup.get(self._selected_specific_opponent_id, "unknown"))

        if self._opponent_source == "heuristic":
            suffix = "эвристика"
        elif self._opponent_source == "latest_snapshot":
            if self._selected_specific_opponent_id:
                suffix = f"последний снапшот, agent_id {self._selected_specific_opponent_id}"
            else:
                suffix = "последний снапшот"
        else:
            if self._selected_specific_opponent_id:
                suffix = f"agent_id {self._selected_specific_opponent_id}"
            else:
                suffix = "конкретный агент не выбран"

        text = (
            f"Сейчас будет: {learner_side} {learner_algo.upper()} {learner_faction} vs "
            f"{opponent_side} {str(opponent_algo).upper()} {opponent_faction} ({suffix})."
        )
        if text != self._opponent_preview_text:
            self._opponent_preview_text = text
            self.opponentPreviewTextChanged.emit(text)

    @QtCore.Slot(str, str)
    def set_training_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_hyperparams:
            return

        current = self._hyperparams.get(normalized_key, self._default_hyperparams[normalized_key])
        try:
            if isinstance(self._default_hyperparams[normalized_key], int):
                parsed = int(float(str(value).strip()))
            else:
                parsed = float(str(value).strip())
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение параметра '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return

        if current == parsed:
            return
        self._hyperparams[normalized_key] = parsed
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot(str, str)
    def set_ppo_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_ppo_hyperparams:
            return

        current = self._ppo_hyperparams.get(normalized_key, self._default_ppo_hyperparams[normalized_key])
        try:
            if isinstance(self._default_ppo_hyperparams[normalized_key], int):
                parsed: int | float = int(float(str(value).strip()))
            else:
                parsed = float(str(value).strip())
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение PPO-параметра '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return

        if current == parsed:
            return
        self._ppo_hyperparams[normalized_key] = parsed
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot()
    def reload_training_hyperparams(self) -> None:
        if self._load_hyperparams_from_disk(log_errors=True):
            self.mark_settings_saved("✓ Сохранено")
            self._emit_status("Параметры тренировки перечитаны из hyperparams.json.")

    @QtCore.Slot()
    def reset_training_hyperparams(self) -> None:
        self._hyperparams = dict(self._default_hyperparams)
        self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status("Параметры тренировки сброшены к значениям по умолчанию.")

    @QtCore.Slot()
    def save_training_hyperparams(self) -> None:
        error = self._validate_hyperparams(self._hyperparams)
        if error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {error}. "
                "Исправьте значения и повторите сохранение."
            )
            return
        ppo_error = self._validate_ppo_hyperparams(self._ppo_hyperparams)
        if ppo_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {ppo_error}. "
                "Исправьте значения PPO и повторите сохранение."
            )
            return
        try:
            # Сохраняем прочие ключи из файла; DQN-поля — merge сверху, секция ppo — целиком из формы.
            existing_payload: dict[str, object] = {}
            if os.path.exists(self._hyperparams_path):
                try:
                    with open(self._hyperparams_path, "r", encoding="utf-8") as read_handle:
                        loaded = json.load(read_handle)
                    if isinstance(loaded, dict):
                        existing_payload = dict(loaded)
                except (OSError, json.JSONDecodeError):
                    existing_payload = {}
            merged_payload = dict(existing_payload)
            merged_payload.update(self._hyperparams)
            merged_payload["ppo"] = dict(self._ppo_hyperparams)
            with open(self._hyperparams_path, "w", encoding="utf-8") as handle:
                json.dump(merged_payload, handle, indent=4, ensure_ascii=False)
                handle.write("\n")
        except OSError as exc:
            self._emit_status(
                "Не удалось записать hyperparams.json в Настройках. "
                f"Причина: {exc}. Проверьте права доступа и повторите."
            )
            self._emit_log(f"[GUI] Ошибка записи {self._hyperparams_path}: {exc}", level="ERROR")
            return

        self._emit_log(f"[GUI] hyperparams.json сохранён: {merged_payload}", level="INFO")
        self.mark_settings_saved("✓ Сохранено")
        self._emit_status("Параметры тренировки сохранены в hyperparams.json.")

    @QtCore.Slot()
    def mark_settings_dirty(self) -> None:
        if self._settings_dirty:
            return
        self._settings_dirty = True
        self._settings_save_state = "● Есть несохранённые изменения"
        self.settingsDirtyChanged.emit(True)
        self.settingsSaveStateChanged.emit(self._settings_save_state)

    def mark_settings_saved(self, text: str = "✓ Сохранено") -> None:
        self._settings_dirty = False
        self._settings_save_state = text
        self.settingsDirtyChanged.emit(False)
        self.settingsSaveStateChanged.emit(self._settings_save_state)

    def _validate_hyperparams(self, payload: dict[str, int | float]) -> str | None:
        lr = float(payload["lr"])
        tau = float(payload["tau"])
        eps_start = float(payload["eps_start"])
        eps_end = float(payload["eps_end"])
        eps_decay = int(payload["eps_decay"])
        batch_size = int(payload["batch_size"])
        gamma = float(payload["gamma"])
        updates_per_step = int(payload["updates_per_step"])
        warmup_steps = int(payload["warmup_steps"])

        if not (0.0 < lr <= 1.0):
            return "lr должен быть в диапазоне (0, 1]"
        if not (0.0 < tau <= 1.0):
            return "tau должен быть в диапазоне (0, 1]"
        if not (0.0 <= eps_end <= eps_start <= 1.0):
            return "должно выполняться 0 <= eps_end <= eps_start <= 1"
        if eps_decay < 1:
            return "eps_decay должен быть целым числом >= 1"
        if batch_size < 1:
            return "batch_size должен быть целым числом >= 1"
        if not (0.0 < gamma <= 1.0):
            return "gamma должен быть в диапазоне (0, 1]"
        if updates_per_step < 1:
            return "updates_per_step должен быть целым числом >= 1"
        if warmup_steps < 0:
            return "warmup_steps должен быть целым числом >= 0"
        return None

    def _validate_ppo_hyperparams(self, payload: dict[str, int | float]) -> str | None:
        lr = float(payload["learning_rate"])
        gamma = float(payload["gamma"])
        gae_lambda = float(payload["gae_lambda"])
        clip_ratio = float(payload["clip_ratio"])
        value_coef = float(payload["value_coef"])
        entropy_coef = float(payload["entropy_coef"])
        rollout_steps = int(payload["rollout_steps"])
        update_epochs = int(payload["update_epochs"])
        minibatch_size = int(payload["minibatch_size"])
        max_grad_norm = float(payload["max_grad_norm"])
        target_kl = float(payload["target_kl"])

        if not (0.0 < lr <= 1.0):
            return "ppo.learning_rate должен быть в диапазоне (0, 1]"
        if not (0.0 < gamma <= 1.0):
            return "ppo.gamma должен быть в диапазоне (0, 1]"
        if not (0.0 <= gae_lambda <= 1.0):
            return "ppo.gae_lambda должен быть в диапазоне [0, 1]"
        if not (0.0 < clip_ratio <= 1.0):
            return "ppo.clip_ratio должен быть в диапазоне (0, 1]"
        if value_coef < 0.0:
            return "ppo.value_coef должен быть >= 0"
        if entropy_coef < 0.0:
            return "ppo.entropy_coef должен быть >= 0"
        if rollout_steps < 1:
            return "ppo.rollout_steps должен быть целым числом >= 1"
        if update_epochs < 1:
            return "ppo.update_epochs должен быть целым числом >= 1"
        if minibatch_size < 1:
            return "ppo.minibatch_size должен быть целым числом >= 1"
        if max_grad_norm <= 0.0:
            return "ppo.max_grad_norm должен быть > 0"
        if target_kl <= 0.0:
            return "ppo.target_kl должен быть > 0"
        return None

    def _load_hyperparams_from_disk(self, log_errors: bool = False) -> bool:
        try:
            with open(self._hyperparams_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            self._hyperparams = dict(self._default_hyperparams)
            self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
            self.trainingHyperparamsChanged.emit()
            if log_errors:
                self._emit_status(
                    "Не удалось прочитать hyperparams.json в Настройках. "
                    f"Причина: {exc}. Использую значения по умолчанию."
                )
                self._emit_log(f"[GUI] Ошибка чтения {self._hyperparams_path}: {exc}", level="WARN")
            return False

        updated = dict(self._default_hyperparams)
        for key, default_value in self._default_hyperparams.items():
            raw = payload.get(key, default_value)
            try:
                if isinstance(default_value, int):
                    updated[key] = int(raw)
                else:
                    updated[key] = float(raw)
            except (TypeError, ValueError):
                updated[key] = default_value

        self._hyperparams = updated

        ppo_raw = payload.get("ppo", {})
        if not isinstance(ppo_raw, dict):
            ppo_raw = {}
        ppo_updated = dict(self._default_ppo_hyperparams)
        for key, default_value in self._default_ppo_hyperparams.items():
            raw = ppo_raw.get(key, default_value)
            try:
                if isinstance(default_value, int):
                    ppo_updated[key] = int(raw)
                else:
                    ppo_updated[key] = float(raw)
            except (TypeError, ValueError):
                ppo_updated[key] = default_value

        self._ppo_hyperparams = ppo_updated
        self.trainingHyperparamsChanged.emit()
        return True

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
            self._emit_status("Кэш моделей, LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt очищены.")
            self._emit_log("[GUI] Кэш моделей, LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt очищены.")
        except OSError as exc:
            message = (
                "Не удалось очистить кэш и логи. "
                "Где: gui_qt/main.py (clear_model_cache). "
                "Что делать: проверьте права доступа к models/, metrics/, LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt, затем повторите."
            )
            self._emit_status(message)
            self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")

    @QtCore.Slot()
    def clear_agent_logs(self) -> None:
        try:
            self._clear_runtime_logs()
            self._emit_status("LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt очищены.")
            self._emit_log("[GUI] LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt очищены.")
        except OSError as exc:
            message = (
                "Не удалось очистить логи. "
                "Где: gui_qt/main.py (clear_agent_logs). "
                "Что делать: проверьте путь и права доступа к LOGS_FOR_AGENTS_TRAIN.md, LOGS_FOR_AGENTS_PLAY.md и results.txt, затем повторите."
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
        env.insert("DEPLOYMENT_MODE", self._deployment_mode)
        env.insert("LEARNER_SIDE", self._learner_side)
        env.insert("LEARNER_FACTION", self._learner_faction)
        env.insert("LEAGUE_ENABLE", "1")
        env.insert("AGENT_LOG_FILE", "LOGS_FOR_AGENTS_TRAIN.md")
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
        env["DEPLOYMENT_MODE"] = self._deployment_mode
        env["AGENT_LOG_FILE"] = "LOGS_FOR_AGENTS_PLAY.md"
        player_label, model_label = self._infer_viewer_role_labels_from_model_pickle(model_path)
        env["VIEWER_PLAYER_ROLE_LABEL"] = player_label
        env["VIEWER_MODEL_ROLE_LABEL"] = model_label
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
        env["DEPLOYMENT_MODE"] = self._deployment_mode
        env["AGENT_LOG_FILE"] = "LOGS_FOR_AGENTS_PLAY.md"
        player_label, model_label = self._infer_viewer_role_labels_from_model_pickle(model_path)
        env["VIEWER_PLAYER_ROLE_LABEL"] = player_label
        env["VIEWER_MODEL_ROLE_LABEL"] = model_label
        command = self._build_script_command(script, [])
        subprocess.Popen(
            command,
            cwd=self._repo_root,
            env=env,
            start_new_session=True,
        )
        self._emit_log("[VIEWER] Запуск в greedy-режиме: exploration отключен (epsilon=0).", level="INFO")
        self._emit_status("Запуск игры в GUI через Viewer (greedy, без исследования).")

    def _infer_viewer_role_labels_from_model_pickle(self, pickle_path: str) -> tuple[str, str]:
        """
        Подписи для Viewer легенды.
        В Viewer: side=`player` = человек, side=`model` = policy (ИИ).
        В папке models/<safe_name>/model-*.pickle safe_name содержит:
          ...__learner_<P1|P2>_<Faction>
        и часть вида ..._vs_P_<EnemyFaction>__learner_...
        """
        default_player = "Игрок"
        default_model = "Модель"
        if not pickle_path or pickle_path == "None":
            return default_player, default_model

        try:
            folder = os.path.basename(os.path.dirname(pickle_path))
            ai_match = re.search(r"__learner_(P[12])_([^_].+?)$", folder)
            if not ai_match:
                # Фолбэк: если имя папки не содержит метаданных, берём текущие настройки GUI.
                # Это лучше, чем пустые/непонятные подписи для ppo-run-*.
                ai_side = str(getattr(self, "_learner_side", "P1") or "P1").strip().upper()
                if ai_side not in {"P1", "P2"}:
                    ai_side = "P1"
                human_side = "P2" if ai_side == "P1" else "P1"
                human_faction = self._display_faction_for_side(human_side)
                ai_faction = self._display_faction_for_side(ai_side)
                return f"Ты: {human_side} ({human_faction})", f"ИИ: {ai_side} ({ai_faction})"
            ai_side = ai_match.group(1)
            ai_faction = ai_match.group(2)

            enemy_match = re.search(r"_vs_P_(.*?)__learner_", folder)
            human_faction = enemy_match.group(1) if enemy_match else "Unknown"
            human_side = "P2" if ai_side == "P1" else "P1"

            return f"Ты: {human_side} ({human_faction})", f"ИИ: {ai_side} ({ai_faction})"
        except Exception:
            return default_player, default_model

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
        if self._auto_clear_logs:
            try:
                self._clear_runtime_logs(clear_play=False, clear_results=False)
                self._emit_log("[GUI] Автоочистка: LOGS_FOR_AGENTS_TRAIN.md очищен.", level="INFO")
            except OSError as exc:
                message = (
                    "Не удалось автоматически очистить логи перед тренировкой. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать: проверьте доступ к LOGS_FOR_AGENTS_TRAIN.md или снимите галочку автоочистки."
                )
                self._emit_status(message)
                self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")
                return
        if not self._prepare_training_data():
            return

        train_label = "TRAIN"
        status_prefix = "Обучение"
        env_overrides: dict[str, str] = {}
        selected_opponent_source = self._opponent_source
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

        if mode == "selfplay" and self._self_play_from_checkpoint and selected_opponent_source == "latest_snapshot":
            checkpoint_path = self._find_latest_resume_file()
            if not checkpoint_path:
                message = (
                    "Не найден checkpoint/model для самообучения от старой модели. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать дальше: сохраните checkpoint_ep*.pth (или model-*.pth) "
                    "или снимите галочку 'Самообучение от старой модели'."
                )
                self._emit_status(message)
                self._emit_log(f"[GUI] {message}", level="ERROR")
                return
            env_overrides["SELF_PLAY_OPPONENT_MODE"] = "fixed_checkpoint"
            env_overrides["SELF_PLAY_FIXED_PATH"] = checkpoint_path
            self._emit_log(f"[GUI] [SELFPLAY] fixed checkpoint: {checkpoint_path}", level="INFO")

        # Выбор источника оппонента из UI.
        env_overrides.pop("OPPONENT_AGENT_ID", None)
        if selected_opponent_source == "heuristic":
            env_overrides["SELF_PLAY_ENABLED"] = "0"
            env_overrides.pop("SELF_PLAY_FIXED_PATH", None)
            env_overrides.pop("SELF_PLAY_OPPONENT_MODE", None)
        elif selected_opponent_source == "latest_snapshot":
            env_overrides["SELF_PLAY_ENABLED"] = "1"
            env_overrides["SELF_PLAY_OPPONENT_MODE"] = env_overrides.get("SELF_PLAY_OPPONENT_MODE", "snapshot")
            # Для Actor-Learner self-play нам нужен конкретный agent_id (чтобы акторы могли загрузить снапшот).
            if self._selected_specific_opponent_id:
                env_overrides["OPPONENT_AGENT_ID"] = self._selected_specific_opponent_id
        elif selected_opponent_source == "specific_agent":
            if not self._selected_specific_opponent_id:
                self._emit_status(
                    "Не выбран конкретный агент-оппонент. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать: выберите agent_id в поле 'Конкретный агент' или смените источник оппонента."
                )
                return
            env_overrides["SELF_PLAY_ENABLED"] = "1"
            env_overrides["SELF_PLAY_OPPONENT_MODE"] = "snapshot"
            env_overrides["OPPONENT_AGENT_ID"] = self._selected_specific_opponent_id
            env_overrides.pop("SELF_PLAY_FIXED_PATH", None)

        # PRO actor-learner теперь режим по умолчанию (без галочки).
        # Для отката на старый pipeline: PRO_ACTOR_LEARNER=0 (ручной запуск/advanced).
        env_overrides.setdefault("PRO_ACTOR_LEARNER", "1")
        env_overrides.setdefault("NUM_ACTORS", "8")
        env_overrides.setdefault("ACTOR_BATCH_SEND", "32")
        env_overrides.setdefault("ACTOR_QUEUE_MAX", "256")

        if self._resume_from_checkpoint:
            resume_path = self._find_latest_resume_file()
            if not resume_path:
                message = (
                    "Resume включён, но checkpoint_ep*.pth и model-*.pth не найдены. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать дальше: сохраните чекпойнт и запустите снова или снимите галочку resume."
                )
                self._emit_status(message)
                self._emit_log(f"[GUI] {message}", level="ERROR")
                return
            env_overrides["RESUME_CHECKPOINT"] = resume_path
            self._emit_log(f"[GUI] [RESUME] Использую чекпойнт: {resume_path}", level="INFO")

        self._emit_log(
            "[GUI] Параметры запуска: "
            f"mode={mode}, self_play_from_checkpoint={int(self._self_play_from_checkpoint)}, "
            f"resume={int(self._resume_from_checkpoint)}, auto_clear_logs={int(self._auto_clear_logs)}, "
            f"disable_train_logging={int(self._disable_train_logging)}, "
            f"action_trace={int(self._action_trace)}, "
            f"train_algo={self._training_algo}, "
            f"opponent_source={selected_opponent_source}, "
            f"opponent_agent_id={self._selected_specific_opponent_id or '-'}",
            level="INFO",
        )
        # Доп. лог матчапа: кто против кого, включая algo (dqn/ppo/heuristic).
        opp_algo = "heuristic" if selected_opponent_source == "heuristic" else "unknown"
        if selected_opponent_source in {"latest_snapshot", "specific_agent"} and self._selected_specific_opponent_id:
            opp_algo = str(self._specific_opponent_algo_by_id.get(self._selected_specific_opponent_id, "unknown"))
        learner_algo = str(self._training_algo or "dqn").strip().lower()
        self._emit_log(
            f"[GUI] [MATCHUP] learner_algo={learner_algo} opponent_algo={opp_algo} opponent_agent_id={self._selected_specific_opponent_id or '-'}",
            level="INFO",
        )
        self._emit_log(
            "[GUI] [PRO_ACTOR_LEARNER] "
            f"enabled={env_overrides.get('PRO_ACTOR_LEARNER','1')} "
            f"actors={env_overrides.get('NUM_ACTORS','8')} "
            f"batch_send={env_overrides.get('ACTOR_BATCH_SEND','32')} "
            f"queue_max={env_overrides.get('ACTOR_QUEUE_MAX','256')}",
            level="INFO",
        )
        if self._training_algo == "ppo":
            vec_count = env_overrides.get("NUM_ENVS", env_overrides.get("VEC_ENV_COUNT", "1"))
            use_subproc = env_overrides.get("USE_SUBPROC_ENVS", "0")
            self._emit_log(f"[GUI] [PPO][CONFIG] vec_env_count={vec_count} use_subproc={use_subproc}", level="INFO")
            sp_enabled = env_overrides.get("SELF_PLAY_ENABLED", "0")
            opp_mode = env_overrides.get("SELF_PLAY_OPPONENT_MODE", "-")
            opp_id = env_overrides.get("OPPONENT_AGENT_ID", "-")
            if str(sp_enabled).strip() == "1":
                self._emit_log(
                    f"[GUI] [PPO][SELFPLAY] enabled=1 mode={opp_mode} opponent_agent_id={opp_id}",
                    level="INFO",
                )

        self._emit_log(f"[GUI] Запуск {status_prefix.lower()}...", level="INFO")
        self._emit_status(f"{status_prefix}...")

        self._process = QtCore.QProcess(self)
        self._process.setWorkingDirectory(self._repo_root)

        env = QtCore.QProcessEnvironment.systemEnvironment()
        if self._disable_train_logging:
            env.insert("TRAIN_LOG_ENABLED", "0")
            env.insert("TRAIN_LOG_TO_CONSOLE", "0")
            # Для отладки эвристики всегда пишем файл лога, даже в speed-режиме.
            env.insert("TRAIN_LOG_TO_FILE", "1")
            env.insert("REWARD_DEBUG", "1")
            env.insert("LOG_EVERY", "1000")
        else:
            env.insert("TRAIN_LOG_ENABLED", "1")
            env.insert("TRAIN_LOG_TO_CONSOLE", "1")
            env.insert("TRAIN_LOG_TO_FILE", "1")
            env.insert("REWARD_DEBUG", "1")
            env.insert("LOG_EVERY", "500")
        env.insert("HEURISTIC_MODE", "v2")
        env.insert("HEURISTIC_DEBUG", "1")
        env.insert("TRAIN_ALGO", self._training_algo)
        env.insert("PER_ENABLED", "1")
        env.insert("N_STEP", "3")
        # Для GUI критично, чтобы снапшоты появлялись и на коротких прогонах (300-1000 эпизодов),
        # иначе список "Конкретный агент" пустой, и в превью будет UNKNOWN.
        # train.py по умолчанию поднимает SAVE_EVERY до SAVE_EVERY_MIN=50, если не разрешить low.
        env.insert("SAVE_EVERY_ALLOW_LOW", "1")
        env.insert("SAVE_EVERY_MIN", "1")
        env.insert("SAVE_EVERY", "50")
        env.insert("CLIP_REWARD", "1")
        env.insert("MISSION_NAME", self._selected_mission)
        env.insert("LEARNER_SIDE", self._learner_side)
        env.insert("LEARNER_FACTION", self._learner_faction)
        env.insert("ACTION_TRACE_ENABLED", "1" if self._action_trace else "0")
        env.insert("LEAGUE_ENABLE", "1")
        env.insert("DEPLOYMENT_MODE", self._deployment_mode)
        if self._deployment_mode == "manual_player":
            self._emit_log(
                "[GUI] [TRAIN] DEPLOYMENT_MODE=manual_player не поддерживается для неинтерактивного train.py; "
                "принудительно переключаю в auto.",
                level="WARN",
            )
            env.insert("DEPLOYMENT_MODE", "auto")
        if self._deployment_mode == "rl_phase":
            env.insert("DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE", "0")
        env.insert("AGENT_LOG_FILE", "LOGS_FOR_AGENTS_TRAIN.md")
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
                f"[{train_label}] Speed-режим: TRAIN_LOG_TO_CONSOLE=0, TRAIN_LOG_TO_FILE=1, REWARD_DEBUG=1, LOG_EVERY=1000.",
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
            # initFile.py получает modelFaction/enemyFaction, а unit-списки берутся из gui/units.txt.
            # Поэтому faction для model/enemy берём из тех ростеров, которые мы записали в эти секции.
            if self._learner_side == "P1":
                model_faction = self._infer_faction_from_roster(self._player_roster)
                enemy_faction = self._infer_faction_from_roster(self._model_roster)
            else:
                model_faction = self._infer_faction_from_roster(self._model_roster)
                enemy_faction = self._infer_faction_from_roster(self._player_roster)

            args = [
                str(self._num_games),
                str(model_faction),
                str(enemy_faction),
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
        raw = self._process.readAllStandardOutput().data()
        data = self._decode_process_bytes(raw)
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
        raw = self._process.readAllStandardError().data()
        data = self._decode_process_bytes(raw)
        for line in data.splitlines():
            if line.strip():
                if self._active_process_kind == "eval":
                    self._append_eval_log_line(f"[stderr] {line}")
                if not self._is_tqdm_progress_line(line):
                    self._emit_log(line, level="ERROR")
                self._handle_progress_line(line)

    def _decode_process_bytes(self, raw: bytes) -> str:
        """
        stdout/stderr из subprocess в Windows иногда приходят в кодировке системы.
        Если декодировать строго как utf-8, получаем "�" (replacement chars).
        Пробуем несколько распространённых кодировок и берём ту, где меньше всего "�".
        """
        candidates = ("utf-8-sig", "utf-8", "cp1251", "latin-1")
        best_text: str = ""
        best_score: int | None = None
        for enc in candidates:
            text = raw.decode(enc, errors="replace")
            score = text.count("\ufffd")  # �
            if best_score is None or score < best_score:
                best_score = score
                best_text = text
            if score == 0:
                return text
        return best_text

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
            "[PPO]",
            "[TRAIN][START]",
            "[TRAIN][BOOT]",
            "[TRAIN][CONFIG]",
            "[TRAIN][ROSTER]",
            "[TRAIN][OPPONENT]",
            "[TRAIN][WARN]",
            "[RESUME]",
            "[metrics] saved:",
            "[SELFPLAY] loading",
            "[SELFPLAY] fixed checkpoint payload",
        )
        allowed_contains = (
            "Training...",
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
        normalized = line.strip()

        # Важно: парсим формат X/Y только для реальных tqdm-линий,
        # чтобы случайные "2/2" в других логах не ломали прогресс-бар.
        if self._is_tqdm_progress_line(normalized):
            tqdm_match = re.search(r"(\d+)\s*/\s*(\d+)", normalized)
            if tqdm_match:
                current = int(tqdm_match.group(1))
                parsed_total = int(tqdm_match.group(2))
                if fallback_total > 0:
                    parsed_total = max(parsed_total, fallback_total)
                return current, parsed_total

        ep_match = re.search(r"\bep=(\d+)(?:\s*/\s*(\d+))?", normalized)
        if ep_match:
            current = int(ep_match.group(1))
            if fallback_total > 0:
                return current, fallback_total
            total = int(ep_match.group(2)) if ep_match.group(2) else fallback_total
            return current, total

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
            self._load_latest_heuristic_metrics()
            self._refresh_specific_opponent_options()
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
            "reward": os.path.join(base_dir, "det_reward.png"),
            "loss": os.path.join(base_dir, "det_loss.png"),
            "epLen": os.path.join(base_dir, "det_ep_len.png"),
            "winrate": os.path.join(base_dir, "det_winrate.png"),
            "avgvp": os.path.join(base_dir, "det_avg_vp.png"),
            "hpdiff": os.path.join(base_dir, "det_hp_diff.png"),
            "killdiff": os.path.join(base_dir, "det_kill_diff.png"),
            "endreasons": os.path.join(base_dir, "det_endreasons.png"),
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

        checkpoint_path = self._resolve_checkpoint_for_pickle(path)
        algo = self._infer_algo_from_checkpoint_or_path(checkpoint_path, path)
        self._play_model_checkpoint_label = (
            f"Checkpoint: {os.path.basename(checkpoint_path)}" if checkpoint_path else "Checkpoint: —"
        )
        self._play_model_algo_label = f"Алгоритм: {algo}" if algo else "Алгоритм: —"
        self.playModelMetaChanged.emit(self._play_model_algo_label)

        # Подсказки для вкладки "Игра" (кто за кого играет).
        player_label, model_label = self._infer_viewer_role_labels_from_model_pickle(path)
        self._play_viewer_player_role_label = player_label
        self._play_viewer_model_role_label = model_label
        self.playViewerPlayerRoleLabelChanged.emit(player_label)
        self.playViewerModelRoleLabelChanged.emit(model_label)

    def _resolve_checkpoint_for_pickle(self, pickle_path: str) -> str:
        if not pickle_path or not os.path.isfile(pickle_path):
            return ""
        directory = os.path.dirname(os.path.abspath(pickle_path))
        base = os.path.splitext(os.path.basename(pickle_path))[0]

        primary = os.path.join(directory, base + ".pth")
        if os.path.isfile(primary):
            return primary

        m = re.match(r"^(model-\d+-\d+)", base)
        if m:
            fallback = os.path.join(directory, m.group(1) + ".pth")
            if os.path.isfile(fallback):
                return fallback

        best = os.path.join(directory, "best_eval_checkpoint.pth")
        if os.path.isfile(best):
            return best

        # PPO: checkpoint_ep{episode}.pth
        try:
            candidates: list[tuple[int, str]] = []
            for fn in os.listdir(directory):
                m_ep = re.match(r"^checkpoint_ep(\d+)\.pth$", str(fn))
                if not m_ep:
                    continue
                ep = int(m_ep.group(1))
                full = os.path.join(directory, fn)
                if os.path.isfile(full):
                    candidates.append((ep, full))
            if candidates:
                candidates.sort(key=lambda x: x[0])
                return candidates[-1][1]
        except Exception:
            pass
        return ""

    def _infer_algo_from_checkpoint_or_path(self, checkpoint_path: str, pickle_path: str) -> str:
        # 1) Самый надёжный вариант: поле algo в checkpoint.
        if checkpoint_path and os.path.isfile(checkpoint_path):
            try:
                import torch  # локальный импорт, чтобы GUI не падал при отсутствии torch

                payload = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
                if isinstance(payload, dict):
                    algo = str(payload.get("algo", "") or "").strip().lower()
                    if algo in {"ppo", "dqn"}:
                        return algo.upper()
                    net_type = str(payload.get("net_type", "") or "").strip().lower()
                    if "ppo" in net_type:
                        return "PPO"
                    if "dueling" in net_type or "basic" in net_type:
                        return "DQN"
            except Exception:
                pass

        # 2) Фолбэк по имени файла/папки.
        joined = (str(pickle_path or "") + " " + str(checkpoint_path or "")).lower()
        if "ppo-run-" in joined or "checkpoint_ep" in joined:
            return "PPO"
        if "actor_learner" in joined or re.search(r"model-\d+-\d+.*\.pth", joined):
            return "DQN"
        return ""

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
                self._play_model_algo_label = "Алгоритм: —"
                self._play_model_checkpoint_label = "Checkpoint: —"
                self.playModelPathChanged.emit(self._play_model_path)
                self.playModelLabelChanged.emit(self._play_model_label)
                self.playModelMetaChanged.emit(self._play_model_algo_label)
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
        # В legacy-формате было: model-<sec>-<micro>.pickle
        # В новом удобочитаемом формате может быть: model-<sec>-<micro>_P1_Faction_... .pickle
        match = re.search(r"model-(\d+-\d+)", base)
        if match:
            return match.group(1)
        match = re.search(r"model-(-?\d+)", base)
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

        # meta для Model Info (опционально присутствует в новых data_*.json)
        try:
            self._metrics_meta = {
                "algo": str(payload.get("algo", "") or ""),
                "mode": str(payload.get("mode", "") or ""),
                "learner_side": str(payload.get("learner_side", "") or ""),
                "learner_faction": str(payload.get("learner_faction", "") or ""),
                "opponent_side": str(payload.get("opponent_side", "") or ""),
                "opponent_faction": str(payload.get("opponent_faction", "") or ""),
                "opponent_algo": str(payload.get("opponent_algo", "") or ""),
                "opponent_source": str(payload.get("opponent_source", "") or ""),
                "opponent_id": str(payload.get("opponent_id", "") or ""),
            }
        except Exception:
            self._metrics_meta = {}

        if str(payload.get("metrics_mode", "") or "") == "det_eval" or payload.get("det_winrate"):
            updated = {
                "reward": self._resolve_metric_path(payload.get("det_reward"), self._metrics_defaults["reward"]),
                "loss": self._resolve_metric_path(payload.get("det_loss"), self._metrics_defaults["loss"]),
                "epLen": self._resolve_metric_path(payload.get("det_ep_len"), self._metrics_defaults["epLen"]),
                "winrate": self._resolve_metric_path(payload.get("det_winrate"), self._metrics_defaults["winrate"]),
                "avgvp": self._resolve_metric_path(payload.get("det_avg_vp"), self._metrics_defaults["avgvp"]),
                "hpdiff": self._resolve_metric_path(payload.get("det_hp_diff"), self._metrics_defaults["hpdiff"]),
                "killdiff": self._resolve_metric_path(payload.get("det_kill_diff"), self._metrics_defaults["killdiff"]),
                "endreasons": self._resolve_metric_path(payload.get("det_endreasons"), self._metrics_defaults["endreasons"]),
            }
        else:
            # Старые data_*.json: тренировочные графики + опционально actor_det_eval.
            updated = {
                "reward": self._resolve_metric_path(payload.get("reward"), self._metrics_defaults["reward"]),
                "loss": self._resolve_metric_path(payload.get("loss"), self._metrics_defaults["loss"]),
                "epLen": self._resolve_metric_path(payload.get("epLen"), self._metrics_defaults["epLen"]),
                "winrate": self._resolve_metric_path(payload.get("winrate"), self._metrics_defaults["winrate"]),
                "avgvp": self._metrics_defaults["avgvp"],
                "hpdiff": self._resolve_metric_path(payload.get("vpdiff"), self._metrics_defaults["hpdiff"]),
                "killdiff": self._metrics_defaults["killdiff"],
                "endreasons": self._resolve_metric_path(payload.get("endreasons"), self._metrics_defaults["endreasons"]),
            }
        self._metrics_run_id = self._extract_run_id_from_path(json_path)
        self._set_metrics_files(updated)
        self._refresh_metrics_summaries()
        return True

    def _select_latest_metrics(self) -> bool:
        # Сначала пробуем самый свежий data_*.json — это работает и для actor-learner,
        # и для обычных прогонов, и не зависит от наличия .pickle.
        latest_json = self._find_latest_metrics_json()
        if latest_json and self._load_metrics_from_json(latest_json):
            self._metrics_label = f"Файл: {os.path.basename(latest_json)}"
            self.metricsLabelChanged.emit(self._metrics_label)
            return True

        # Фолбэк: если есть .pickle — пытаемся маппить его на data_<metrics_id>.json.
        latest_model = self._find_latest_model_file()
        if latest_model:
            metrics_id = self._extract_metrics_id(latest_model)
            if metrics_id:
                json_path = os.path.join(self._repo_root, "models", f"data_{metrics_id}.json")
                if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                    self._metrics_label = f"Файл: {os.path.basename(latest_model)}"
                    self.metricsLabelChanged.emit(self._metrics_label)
                    return True

        self._set_metrics_files(dict(self._metrics_defaults))
        self._metrics_label = "По умолчанию"
        self._metrics_run_id = ""
        self._refresh_metrics_summaries()
        self.metricsLabelChanged.emit(self._metrics_label)
        return False

    def _extract_run_id_from_path(self, path: str) -> str:
        base = os.path.basename(path)
        match = re.search(r"_(\d+)\.json$", base)
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
        if self._metrics_run_id:
            exact = os.path.join(metrics_dir, f"stats_{self._metrics_run_id}.csv")
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

    def _parse_training_counters(self) -> tuple[int, int, int, int]:
        total_episodes = 0
        results_path = os.path.join(self._repo_root, "results.txt")
        if os.path.exists(results_path):
            try:
                with open(results_path, "r", encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        match = re.search(r"эпизоды=(\d+)", line)
                        if match:
                            total_episodes += int(match.group(1))
            except OSError:
                pass

        snapshot_episodes = 0
        fixed_episodes = 0
        logs_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS_TRAIN.md")
        if os.path.exists(logs_path):
            try:
                with open(logs_path, "r", encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        if "[SELFPLAY] enabled=1 mode=snapshot" in line:
                            snapshot_episodes += 1
                        elif "[SELFPLAY] enabled=1 mode=fixed_checkpoint" in line:
                            fixed_episodes += 1
            except OSError:
                pass

        selfplay_total = snapshot_episodes + fixed_episodes
        heuristic_episodes = max(total_episodes - selfplay_total, 0)
        return total_episodes, heuristic_episodes, snapshot_episodes, fixed_episodes

    def _extract_latest_resume_meta(self) -> dict[str, str]:
        values = {
            "global_step": "—",
            "optimize_steps": "—",
            "episode": "—",
            "replay_size": "—",
            "eps": "—",
        }
        logs_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS_TRAIN.md")
        if not os.path.exists(logs_path):
            return values
        try:
            with open(logs_path, "r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    if "[RESUME] loaded:" not in line:
                        continue
                    for key, raw_value in re.findall(r"(global_step|optimize_steps|episode|replay_size|eps)=([^\s]+)", line):
                        values[key] = raw_value
        except OSError:
            return values
        return values

    def _league_matchup_summary(self) -> str:
        path = os.path.join(self._repo_root, "models", "matchups.json")
        if not os.path.exists(path):
            return "League: нет данных матчапов."
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            return "League: не удалось прочитать matchups.json."
        records = payload.get("records", []) if isinstance(payload, dict) else []
        if not isinstance(records, list) or not records:
            return "League: матчапы пока не записаны."
        tail = records[-500:]
        by_opp: dict[str, dict[str, float]] = {}
        for rec in tail:
            if not isinstance(rec, dict):
                continue
            opp = str(rec.get("opponent_agent_id", "unknown"))
            stat = by_opp.setdefault(opp, {"games": 0.0, "wins": 0.0, "draws": 0.0, "vp": 0.0})
            stat["games"] += 1.0
            stat["wins"] += float(rec.get("win", 0.0))
            stat["draws"] += float(rec.get("draw", 0.0))
            stat["vp"] += float(rec.get("vp_diff", 0.0))
        ranked = sorted(by_opp.items(), key=lambda kv: kv[1]["games"], reverse=True)[:3]
        lines = ["League (top-3 по числу игр):"]
        for opp, stat in ranked:
            games = max(1.0, stat["games"])
            lines.append(
                f"• {opp}: games={int(stat['games'])}, winrate={stat['wins']/games:.2f}, draw={stat['draws']/games:.2f}, vp={stat['vp']/games:.2f}"
            )
        return "\n".join(lines)

    def _refresh_metrics_summaries(self) -> None:
        defaults = {
            "reward": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "loss": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "epLen": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "winrate": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "avgvp": "Модель: — | Противник: —",
            "hpdiff": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "killdiff": "Текущее: — | Среднее: — | Мин: — | Макс: —",
            "endreasons": "Последняя точка: —",
        }
        summaries = dict(defaults)

        run_id = str(self._metrics_run_id or "").strip()
        det_jsonl_path = os.path.join(self._repo_root, "metrics", f"actor_det_eval_{run_id}.jsonl") if run_id else ""
        det_points: list[dict] = []
        if det_jsonl_path and os.path.exists(det_jsonl_path):
            by_ep: dict[int, dict] = {}
            try:
                with open(det_jsonl_path, "r", encoding="utf-8", errors="replace") as handle:
                    for line in handle:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            payload = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if not isinstance(payload, dict):
                            continue
                        ep = int(payload.get("episode", 0) or 0)
                        if ep <= 0:
                            continue
                        by_ep[ep] = payload
            except OSError:
                by_ep = {}
            det_points = [by_ep[k] for k in sorted(by_ep.keys())]

        if det_points:
            reward_vals = [float(p.get("reward_mean", 0.0) or 0.0) for p in det_points]
            ep_len_vals = [float(p.get("ep_len_mean", 0.0) or 0.0) for p in det_points]
            model_vp_vals = [float(p.get("model_vp_mean", 0.0) or 0.0) for p in det_points]
            enemy_vp_vals = [float(p.get("enemy_vp_mean", 0.0) or 0.0) for p in det_points]
            hp_vals = [float(p.get("hp_diff_mean", 0.0) or 0.0) for p in det_points]
            kill_vals = [float(p.get("kill_diff_mean", 0.0) or 0.0) for p in det_points]
            win_vals = [float(p.get("win_rate", 0.0) or 0.0) for p in det_points]
            loss_vals: list[float] = []
            for p in det_points:
                raw = p.get("training_loss", None)
                if raw is None:
                    continue
                try:
                    loss_vals.append(float(raw))
                except (TypeError, ValueError):
                    continue
            summaries["reward"] = self._format_metric_summary(reward_vals)
            summaries["epLen"] = self._format_metric_summary(ep_len_vals)
            if model_vp_vals or enemy_vp_vals:
                summaries["avgvp"] = f"Модель: {model_vp_vals[-1]:.2f} | Противник: {enemy_vp_vals[-1]:.2f}"
            summaries["hpdiff"] = self._format_metric_summary(hp_vals)
            summaries["killdiff"] = self._format_metric_summary(kill_vals)
            summaries["winrate"] = self._format_metric_summary(win_vals, percent=True)
            if loss_vals:
                summaries["loss"] = self._format_metric_summary(loss_vals)
            else:
                summaries["loss"] = "Нет training_loss в JSONL (старый ран или точки без loss)."
            last = det_points[-1]
            summaries["endreasons"] = (
                f"Последняя точка ep≈{last.get('episode', '?')}: "
                f"wipeout_enemy={float(last.get('wipeout_enemy_rate', 0.0)):.2f}, "
                f"wipeout_model={float(last.get('wipeout_model_rate', 0.0)):.2f}, "
                f"turn_limit={float(last.get('turn_limit_rate', 0.0)):.2f}"
            )
            # Summary для верхней панели: берём последнюю точку DET-eval.
            try:
                last_ep = int(last.get("episode", 0) or 0)
            except (TypeError, ValueError):
                last_ep = 0
            try:
                last_win = float(last.get("win_rate", 0.0) or 0.0)
            except (TypeError, ValueError):
                last_win = 0.0
            try:
                last_reward = float(last.get("reward_mean", 0.0) or 0.0)
            except (TypeError, ValueError):
                last_reward = 0.0
            try:
                last_len = float(last.get("ep_len_mean", 0.0) or 0.0)
            except (TypeError, ValueError):
                last_len = 0.0
            last_loss_raw = last.get("training_loss", None)
            last_loss_str = "—"
            if last_loss_raw is not None:
                try:
                    last_loss_str = f"{float(last_loss_raw):.4f}"
                except (TypeError, ValueError):
                    last_loss_str = "—"

            self._det_last = {
                "episode": str(last_ep) if last_ep > 0 else "—",
                "winrate": f"{last_win * 100:.2f}%",
                "reward": f"{last_reward:.4f}",
                "ep_len": f"{last_len:.2f}",
                "train_loss": last_loss_str,
            }
        else:
            self._det_last = {
                "episode": "—",
                "winrate": "—",
                "reward": "—",
                "ep_len": "—",
                "train_loss": "—",
            }
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
                summaries["hpdiff"] = self._format_metric_summary(vp_diff)
                summaries["killdiff"] = "Нет DET kill diff (нужен actor_det_eval_*.jsonl)."
                summaries["winrate"] = self._format_metric_summary(wins, percent=True)
                if losses:
                    summaries["loss"] = self._format_metric_summary(losses)
                summaries["endreasons"] = "Нет actor_det_eval_*.jsonl — сводка по старым train-данным (CSV)."
            elif run_id:
                summaries["endreasons"] = f"Нет файла actor_det_eval_{run_id}.jsonl (DET-eval не писался)."

        total, heuristic, snapshot, fixed = self._parse_training_counters()
        resume = self._extract_latest_resume_meta()
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
            f"• eps: {resume['eps']}\n\n"
            f"{self._league_matchup_summary()}"
        )

        self._metric_summary_texts = summaries
        self._model_state_text = model_state
        self.metricsSummaryChanged.emit()
        self._load_latest_heuristic_metrics()

    def _load_latest_heuristic_metrics(self) -> None:
        path = os.path.join(self._repo_root, "metrics", "heur_metrics_latest.json")
        if not os.path.exists(path):
            self._heuristic_metrics = {}
            self._heuristic_metrics_text = "Нет данных метрик эвристики."
            self.heuristicMetricsChanged.emit()
            return
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError):
            self._heuristic_metrics = {}
            self._heuristic_metrics_text = "Не удалось прочитать metrics/heur_metrics_latest.json."
            self.heuristicMetricsChanged.emit()
            return
        self._heuristic_metrics = payload if isinstance(payload, dict) else {}
        mode_usage = self._heuristic_metrics.get("mode_usage", {}) or {}
        role_usage = self._heuristic_metrics.get("role_usage", {}) or {}
        run_id = str(self._heuristic_metrics.get("run_id", "-"))
        updated_at = str(self._heuristic_metrics.get("updated_at", "-"))

        lines = [
            f"Последний ран: {run_id}",
            f"Обновлено: {updated_at}",
            "",
            "Только метрики эвристики:",
            f"Винрейт эвристики (все train-игры): {float(self._heuristic_metrics.get('train_heur_winrate', 0.0)):.3f}",
            f"Доля ничьих (все train-игры): {float(self._heuristic_metrics.get('train_draw_rate', 0.0)):.3f}",
            f"Всего train-игр: {int(self._heuristic_metrics.get('train_total_games', 0))}",
            f"Invalid rate: {float(self._heuristic_metrics.get('invalid_rate_total', 0.0)):.4f}",
            f"Avg risk: {float(self._heuristic_metrics.get('avg_risk', 0.0)):.3f}",
            f"Avg cover: {float(self._heuristic_metrics.get('avg_cover', 0.0)):.3f}",
            f"Charge success: {float(self._heuristic_metrics.get('charge_success_rate', 0.0)):.3f}",
            f"Shoot overkill rate: {float(self._heuristic_metrics.get('shoot_overkill_rate', 0.0)):.3f}",
            f"Fallback rate: {float(self._heuristic_metrics.get('fallback_rate', 0.0)):.3f}",
            "Mode usage: "
            f"kite={int(mode_usage.get('kite', 0))}, hold={int(mode_usage.get('hold', 0))}, commit={int(mode_usage.get('commit', 0))}",
            "Role usage: "
            f"ranged={int(role_usage.get('ranged', 0))}, hybrid={int(role_usage.get('hybrid', 0))}, melee={int(role_usage.get('melee', 0))}",
        ]
        self._heuristic_metrics_text = "\n".join(lines)
        self.heuristicMetricsChanged.emit()

    def _find_latest_model_file(self) -> Optional[str]:
        models_path = os.path.join(self._repo_root, "models")
        if not os.path.isdir(models_path):
            return None
        def is_human_readable(name: str) -> bool:
            # Новый удобочитаемый формат:
            # model-<sec>-<micro>_P1_<Faction>_<mission>_final_ep<...>.pickle
            # Для выбора "Последней модели" приоритет отдаём именно ему.
            s = str(name or "")
            return ("final_ep" in s) and (re.search(r"(_P[12]_)", s) is not None)

        latest_human_path = None
        latest_human_mtime = -1.0
        latest_legacy_path = None
        latest_legacy_mtime = -1.0

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
                if is_human_readable(name):
                    if mtime > latest_human_mtime:
                        latest_human_mtime = mtime
                        latest_human_path = path
                else:
                    if mtime > latest_legacy_mtime:
                        latest_legacy_mtime = mtime
                        latest_legacy_path = path

        return latest_human_path or latest_legacy_path

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
            f"Юниты P1: {len(self._player_roster)} | "
            f"Юниты P2: {len(self._model_roster)}"
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
            # Используем для вывода faction из ростера (даже если UI сейчас показывает только часть фракций).
            self._unit_faction_by_name[str(name).strip()] = str(faction).strip()
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
                # Маппим секции файла gui/units.txt в P1/P2 в зависимости от learner_side.
                # Это обратное действие к логике _persist_rosters().
                if self._learner_side == "P1":
                    # В момент сохранения при learner_side=P1:
                    # - "Player Units" => P2
                    # - "Model Units" => P1
                    if section == "player":
                        self._model_roster.append(entry)
                    else:
                        self._player_roster.append(entry)
                else:
                    # В момент сохранения при learner_side=P2:
                    # - "Player Units" => P1
                    # - "Model Units" => P2
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
        # В файле gui/units.txt:
        # - "Player Units" попадает как enemy в initFile.py
        # - "Model Units" попадает как model в initFile.py
        # Поэтому записываем в эти секции так, чтобы learner-сторона стала model-стороной.
        if self._learner_side == "P1":
            enemy_roster = self._model_roster  # P2
            model_roster = self._player_roster  # P1
        else:
            enemy_roster = self._player_roster  # P1
            model_roster = self._model_roster  # P2

        lines = ["Player Units"]
        for entry in enemy_roster:
            lines.append(f"{entry.name}|{entry.count}|{entry.instance_id}")
        lines.append("Model Units")
        for entry in model_roster:
            lines.append(f"{entry.name}|{entry.count}|{entry.instance_id}")
        os.makedirs(os.path.dirname(units_path), exist_ok=True)
        with open(units_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))

    def _clear_cache_files(self) -> None:
        models_path = os.path.join(self._repo_root, "models")
        metrics_path = os.path.join(self._repo_root, "metrics")
        gui_img_path = os.path.join(self._repo_root, "gui", "img")
        # Полная очистка моделей/кеша (включая agents/registry).
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
        self._clear_runtime_logs()

    def _remove_contents(
        self,
        path: str,
        *,
        keep_dirs: set[str] | None = None,
        keep_files: set[str] | None = None,
    ) -> None:
        if not os.path.isdir(path):
            return
        keep_dirs = keep_dirs or set()
        keep_files = keep_files or set()
        for name in os.listdir(path):
            if name in keep_dirs or name in keep_files:
                continue
            target = os.path.join(path, name)
            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)

    def _clear_runtime_logs(
        self,
        *,
        clear_play: bool = True,
        clear_results: bool = True,
        clear_train: bool = True,
    ) -> None:
        if clear_train:
            train_log_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS_TRAIN.md")
            with open(train_log_path, "w", encoding="utf-8"):
                pass
        if clear_play:
            play_log_path = os.path.join(self._repo_root, "LOGS_FOR_AGENTS_PLAY.md")
            with open(play_log_path, "w", encoding="utf-8"):
                pass
        if clear_results:
            results_path = os.path.join(self._repo_root, "results.txt")
            with open(results_path, "w", encoding="utf-8"):
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
