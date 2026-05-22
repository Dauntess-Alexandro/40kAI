import ast
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import ctypes
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Запуск вида `python app/gui_qt/main.py` добавляет в sys.path только app/gui_qt,
# из‑за этого не находится project_paths в корне репозитория — QML грузится без controller.
_REPO_ROOT = Path(__file__).resolve().parents[2]
_repo_root_str = str(_REPO_ROOT)
if _repo_root_str not in sys.path:
    sys.path.insert(0, _repo_root_str)

from PySide6 import QtCore, QtGui, QtQml
from PySide6.QtGui import QIcon
from PySide6.QtQuickControls2 import QQuickStyle
from theme.loader import ThemeTokenError, load_tokens_flat_for_qml
from core.models.alphazero_ids import is_az_algo
from app.gui_qt.algo_hyperparams_defaults import (
    DEFAULT_DQN_HYPERPARAMS,
    DEFAULT_PPO_HYPERPARAMS,
    DQN_HYPERPARAM_KEYS,
    DQN_PROFILE_PRESETS,
    DQN_ROOT_SYNC_KEYS,
    PPO_HYPERPARAM_KEYS,
    PPO_PROFILE_PRESETS,
)
from app.gui_qt.az_hyperparams_defaults import (
    AZ_HYPERPARAM_KEYS,
    AZ_PROXY_PROFILE_PRESETS,
    AZ_TREE_PROFILE_PRESETS,
    DEFAULT_AZ_PROXY_HYPERPARAMS,
    DEFAULT_AZ_TREE_HYPERPARAMS,
)
from project_paths import (
    AGENT_EVAL_LOG_PATH,
    AGENT_PLAY_LOG_PATH,
    AGENT_TRAIN_LOG_PATH,
    APP_DIR,
    ARTIFACTS_METRICS_DIR,
    ARTIFACTS_MODELS_DIR,
    BOARD_PATH,
    PROJECT_ROOT,
    RESULTS_PATH,
    RUNTIME_STATE_DIR,
    TRAIN_DATA_PATH,
    UNITS_PATH,
    ensure_runtime_dirs,
    get_runtime_python,
)

_GUI_CONTROLLER_REF = None


@dataclass
class RosterEntry:
    name: str
    count: int
    instance_id: str
    ranged_weapon: str = ""
    melee_weapon: str = ""


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
    evalSetupChanged = QtCore.Signal()
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
    trainSetupSummaryChanged = QtCore.Signal()
    rosterWeaponsPreviewChanged = QtCore.Signal()
    rosterOverviewChanged = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process: Optional[QtCore.QProcess] = None
        self._running = False
        self._repo_root = str(PROJECT_ROOT)
        self._runtime_python = get_runtime_python(PROJECT_ROOT)
        self._app_gui_dir = str(APP_DIR / "gui_qt")
        ensure_runtime_dirs()
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
        self._play_model_algo_key = ""
        self._play_model_checkpoint_label = "Checkpoint: —"
        self._play_agent_override_id = ""
        self._play_az_mode = "greedy"
        self._play_gmz_mode = "greedy"
        self._play_az_temperature = 0.06
        self._play_gmz_temperature = 0.10
        self._play_viewer_player_role_label = "Ты: —"
        self._play_viewer_model_role_label = "ИИ: —"
        self._eval_model_path = ""
        self._eval_model_label = "Модель не выбрана"
        self._eval_games = 50
        self._eval_log_text = ""
        self._eval_summary_text = "Итог оценки появится после завершения eval.py."
        self._eval_policy_options = ["heuristic", "agent"]
        self._eval_p1_policy = "agent"
        self._eval_p2_policy = "heuristic"
        self._eval_p1_agent_ids: list[str] = []
        self._eval_p1_agent_labels: list[str] = []
        self._eval_p2_agent_ids: list[str] = []
        self._eval_p2_agent_labels: list[str] = []
        self._eval_selected_p1_agent_id = ""
        self._eval_selected_p2_agent_id = ""
        self._eval_matchup_text = "Выберите политику P1 и P2 для оценки."
        self._eval_duel_title = "— vs —"
        self._eval_duel_subtitle = "Выберите состав матча."
        self._eval_p1_display_name = "P1: —"
        self._eval_p2_display_name = "P2: —"
        self._eval_p1_full_agent_id = ""
        self._eval_p2_full_agent_id = ""
        self._eval_p1_badges: list[str] = []
        self._eval_p2_badges: list[str] = []
        self._eval_p1_inference_mode = "greedy"
        self._eval_p2_inference_mode = "greedy"
        self._eval_p1_az_temperature = 0.06
        self._eval_p2_az_temperature = 0.06
        self._eval_p1_gmz_temperature = 0.10
        self._eval_p2_gmz_temperature = 0.10
        self._eval_p1_icon_text = "AI"
        self._eval_p2_icon_text = "HR"
        self._eval_scenario_text = "Сценарий: выберите политики P1/P2."
        self._eval_launch_ready = False
        self._eval_launch_status_text = "Нужно выбрать хотя бы одного агента."
        self._eval_mini_summary = "Игр: 50 • deterministic • epsilon=0"
        self._eval_agent_meta_by_id: dict[str, dict[str, str]] = {}
        self._eval_result_headline = "P1 vs P2: —"
        self._eval_result_winrate_p1 = "P1 winrate: —"
        self._eval_result_winrate_p2 = "P2 winrate: —"
        self._eval_result_avg_vp_diff = "Avg VP diff (P1-P2): —"
        self._eval_result_turn_limit_rate = "Turn-limit rate: —"
        self._eval_result_quality_hint = "Качество серии: нет данных."
        self._eval_live_games_done = 0
        self._eval_live_games_total = self._eval_games
        self._eval_live_p1_wins = 0
        self._eval_live_p2_wins = 0
        self._eval_live_draws = 0
        self._eval_live_last_game_idx = 0
        self._active_process_kind = ""
        self._board_text = "ASCII карта будет доступна после запуска игры."
        self._self_play_from_checkpoint = False
        self._resume_from_checkpoint = False
        self._disable_train_logging = False
        self._action_trace = str(os.getenv("ACTION_TRACE_ENABLED", "0")).strip() == "1"
        self._auto_clear_logs = True
        self._unit_faction_by_name: dict[str, str] = {}
        self._unit_weapons_by_name: dict[str, list[str]] = {}
        self._unit_keywords_by_name: dict[str, list[str]] = {}
        self._unit_models_by_name: dict[str, int] = {}
        self._unit_abilities_by_name: dict[str, list[str]] = {}
        self._unit_points_by_name: dict[str, int] = {}
        self._unit_core_by_name: dict[str, dict[str, object]] = {}
        self._weapon_type_by_army_name: dict[tuple[str, str], str] = {}
        self._weapon_data_by_army_name: dict[tuple[str, str], dict] = {}
        self._roster_available_preview_index = -1
        self._roster_template_weapons_by_unit: dict[str, tuple[str, str]] = {}
        self._roster_preview_melee: list[str] = []
        self._roster_preview_ranged: list[str] = []
        self._roster_preview_unknown: list[str] = []
        self._roster_preview_side = ""
        self._roster_preview_roster_index = -1
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
        self._train_context_learner_algo_short = "DQN"
        self._train_context_opponent_algo_short = "Эвристика"
        self._train_context_opponent_side = "P2"

        self._training_algo_options = ["dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"]
        self._training_algo = str(os.getenv("TRAIN_ALGO", "dqn")).strip().lower() or "dqn"
        if self._training_algo not in self._training_algo_options:
            self._training_algo = "dqn"

        self._hyperparams_path = os.path.join(self._repo_root, "hyperparams.json")
        self._default_dqn_hyperparams: dict[str, int | float | str] = dict(DEFAULT_DQN_HYPERPARAMS)
        self._default_ppo_hyperparams: dict[str, int | float | str] = dict(DEFAULT_PPO_HYPERPARAMS)
        self._dqn_profile_presets = dict(DQN_PROFILE_PRESETS)
        self._ppo_profile_presets = dict(PPO_PROFILE_PRESETS)
        # Секция hyperparams.json["gumbel_muzero"] — читает train.py (GMZ_*).
        self._default_gmz_hyperparams: dict[str, int | float] = {
            "learning_rate": 0.0003,
            "batch_size": 128,
            "unroll_steps": 5,
            "value_loss_weight": 1.0,
            "reward_loss_weight": 1.0,
            "l2_weight": 1e-6,
            "discount": 0.997,
            "replay_capacity": 250000,
            "num_actors": 8,
            "actor_batch_send": 64,
            "actor_queue_max": 256,
            "sync_every_updates": 2,
            "updates_per_rollout": 2,
            "replay_min_size": 512,
            "max_policy_staleness_updates": 600,
            "latent_dim": 256,
            "hidden_dim": 256,
            "action_embed_dim": 64,
            "num_simulations": 32,
            "root_top_k": 8,
            "gumbel_scale": 1.0,
            "search_temperature": 0.15,
            "temperature_opening_moves": 12,
            "temperature_opening_value": 1.0,
            "temperature_late_value": 0.25,
            "outcome_only": 1,
            "outcome_value_win": 1.0,
            "outcome_value_loss": -1.0,
            "outcome_value_draw": -0.25,
        }
        self._gmz_profile_presets: dict[str, dict[str, int]] = {
            "fast": {
                "num_actors": 8,
                "num_simulations": 16,
                "root_top_k": 4,
                "batch_size": 96,
                "replay_capacity": 120000,
            },
            "balanced": {
                "num_actors": 8,
                "num_simulations": 32,
                "root_top_k": 8,
                "batch_size": 128,
                "replay_capacity": 250000,
            },
            "heavy": {
                "num_actors": 8,
                "num_simulations": 128,
                "root_top_k": 20,
                "batch_size": 160,
                "replay_capacity": 400000,
                "actor_queue_max": 512,
            },
        }
        self._gmz_selected_profile = "custom"
        self._dqn_selected_profile = "custom"
        self._ppo_selected_profile = "custom"
        self._dqn_hyperparams = dict(self._default_dqn_hyperparams)
        self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
        self._gmz_hyperparams = dict(self._default_gmz_hyperparams)
        self._default_az_tree_hyperparams: dict[str, int | float | str] = dict(DEFAULT_AZ_TREE_HYPERPARAMS)
        self._default_az_proxy_hyperparams: dict[str, int | float | str] = dict(DEFAULT_AZ_PROXY_HYPERPARAMS)
        self._az_tree_hyperparams = dict(self._default_az_tree_hyperparams)
        self._az_proxy_hyperparams = dict(self._default_az_proxy_hyperparams)
        self._az_tree_profile_presets = dict(AZ_TREE_PROFILE_PRESETS)
        self._az_proxy_profile_presets = dict(AZ_PROXY_PROFILE_PRESETS)
        self._az_tree_selected_profile = "custom"
        self._az_proxy_selected_profile = "custom"
        self._settings_dirty = False
        self._settings_save_state = "✓ Сохранено"
        self._load_hyperparams_from_disk(log_errors=True)

        self._load_available_units()
        self._load_rosters_from_file()
        self._update_learner_faction_from_rosters()
        self._refresh_models()
        self._select_latest_metrics()
        self._load_latest_heuristic_metrics()
        self._apply_latest_play_selection(initial=True, emit_status=False)
        self._select_latest_eval_model(initial=True)
        self._update_roster_summary()
        self._refresh_specific_opponent_options()
        self._refresh_eval_agent_options()

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

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainRosterP1Faction(self) -> str:
        return self._display_faction_for_side("P1")

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainRosterP2Faction(self) -> str:
        return self._display_faction_for_side("P2")

    @QtCore.Property("QVariantList", notify=trainSetupSummaryChanged)
    def trainContextP1RosterCards(self) -> list[dict]:
        return self._train_context_roster_cards(self._player_roster)

    @QtCore.Property("QVariantList", notify=trainSetupSummaryChanged)
    def trainContextP2RosterCards(self) -> list[dict]:
        return self._train_context_roster_cards(self._model_roster)

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainContextLearnerAlgoShort(self) -> str:
        return self._train_context_learner_algo_short

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainContextOpponentAlgoShort(self) -> str:
        return self._train_context_opponent_algo_short

    @staticmethod
    def _train_algo_short_terminal_en(short: str) -> str:
        """Короткое имя алгоритма для «терминальной» строки UI (латиница)."""
        s = (short or "").strip()
        return {
            "Эвристика": "HEURISTIC",
            "Снапшот": "SNAPSHOT",
            "Агент не выбран": "NO_AGENT",
        }.get(s, s)

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainContextLearnerAlgoTerminal(self) -> str:
        return self._train_algo_short_terminal_en(self._train_context_learner_algo_short)

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainContextOpponentAlgoTerminal(self) -> str:
        return self._train_algo_short_terminal_en(self._train_context_opponent_algo_short)

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainContextOpponentSide(self) -> str:
        return self._train_context_opponent_side

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewUnitName(self) -> str:
        idx = int(self._roster_available_preview_index)
        if 0 <= idx < len(self._available_units):
            return str(self._available_units[idx].name)
        return "—"

    @QtCore.Property(int, notify=rosterWeaponsPreviewChanged)
    def rosterAvailableUnitListIndex(self) -> int:
        """Индекс выбранной строки в списке «Доступные юниты» (синхрон с верстаком)."""
        return int(self._roster_available_preview_index)

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewTarget(self) -> str:
        return "Сборка перед добавлением"

    @QtCore.Property("QStringList", notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewRanged(self) -> list[str]:
        return self._roster_preview_ranged

    @QtCore.Property("QStringList", notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewMelee(self) -> list[str]:
        return self._roster_preview_melee

    @QtCore.Property(int, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewRangedCount(self) -> int:
        return len(self._roster_preview_ranged)

    @QtCore.Property(int, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewMeleeCount(self) -> int:
        return len(self._roster_preview_melee)

    @QtCore.Property("QStringList", notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsPreviewUnknown(self) -> list[str]:
        return self._roster_preview_unknown

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsSelectedRanged(self) -> str:
        unit_name = self.rosterWeaponsPreviewUnitName
        rw, _mw = self._template_weapons_for_unit(unit_name)
        return rw

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterWeaponsSelectedMelee(self) -> str:
        unit_name = self.rosterWeaponsPreviewUnitName
        _rw, mw = self._template_weapons_for_unit(unit_name)
        return mw

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterDoctrineP1(self) -> str:
        return self._build_roster_doctrine("P1")

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterDoctrineP2(self) -> str:
        return self._build_roster_doctrine("P2")

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterKpiP1(self) -> str:
        return self._build_roster_kpi("P1")

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterKpiP2(self) -> str:
        return self._build_roster_kpi("P2")

    @QtCore.Property("QVariantList", notify=rosterOverviewChanged)
    def rosterKpiP1Columns(self) -> list[dict]:
        return self._roster_kpi_columns("P1")

    @QtCore.Property("QVariantList", notify=rosterOverviewChanged)
    def rosterKpiP2Columns(self) -> list[dict]:
        return self._roster_kpi_columns("P2")

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterCompositionDelta(self) -> str:
        return self._build_roster_composition_delta()

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterPointsP1(self) -> str:
        return f"{self._roster_points_total('P1')} pts"

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterPointsP2(self) -> str:
        return f"{self._roster_points_total('P2')} pts"

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterPointsDelta(self) -> str:
        p1 = self._roster_points_total("P1")
        p2 = self._roster_points_total("P2")
        return f"Δ pts {p1 - p2:+d}"

    @QtCore.Property(str, notify=rosterOverviewChanged)
    def rosterPointsDeltaColor(self) -> str:
        p1 = self._roster_points_total("P1")
        p2 = self._roster_points_total("P2")
        diff = p1 - p2
        if diff > 0:
            return "#8fb6e8"
        if diff < 0:
            return "#d58f8f"
        return "#9aa3b2"

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterActiveRangedStatline(self) -> str:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return "—"
        rw, _mw = self._template_weapons_for_unit(unit_name)
        return self._weapon_statline(unit_name, rw)

    @QtCore.Property(str, notify=rosterWeaponsPreviewChanged)
    def rosterActiveMeleeStatline(self) -> str:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return "—"
        _rw, mw = self._template_weapons_for_unit(unit_name)
        return self._weapon_statline(unit_name, mw)

    @QtCore.Property("QStringList", notify=rosterWeaponsPreviewChanged)
    def rosterActiveRangedBadges(self) -> list[str]:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return []
        rw, _mw = self._template_weapons_for_unit(unit_name)
        return self._weapon_ability_badges(unit_name, rw)

    @QtCore.Property("QStringList", notify=rosterWeaponsPreviewChanged)
    def rosterActiveMeleeBadges(self) -> list[str]:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return []
        _rw, mw = self._template_weapons_for_unit(unit_name)
        return self._weapon_ability_badges(unit_name, mw)

    def _weapon_icon_file_url(self, weapon_name: str) -> str:
        normalized = str(weapon_name or "").strip().lower()
        if not normalized:
            return ""
        icon_file = ""
        if "gauss reaper" in normalized:
            icon_file = "gauss_reaper_icon.png"
        elif "gauss flayer" in normalized:
            icon_file = "gauss_flayer_icon.png"
        elif "relic gauss blaster" in normalized:
            icon_file = "relic_gauss_blaster_icon.png"
        elif "necron close combat weapon" in normalized:
            icon_file = "necron_close_combat_weapon_icon.png"
        elif "royal warden close combat weapon" in normalized:
            icon_file = "necron_close_combat_weapon_icon.png"
        elif "close combat weapon" in normalized:
            icon_file = "necron_close_combat_weapon_icon.png"
        if not icon_file:
            return ""
        icon_path = os.path.join(self._app_gui_dir, "assets", icon_file)
        if not os.path.exists(icon_path):
            return ""
        return self._to_file_url(icon_path)

    @QtCore.Slot(str, result=str)
    def roster_weapon_icon_source(self, weapon_name: str) -> str:
        return self._weapon_icon_file_url(weapon_name)

    @QtCore.Slot(str, result=str)
    def roster_weapon_statline_for_selected(self, weapon_name: str) -> str:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return "—"
        return self._weapon_statline(unit_name, weapon_name)

    @QtCore.Slot(str, result="QStringList")
    def roster_weapon_stat_values_for_selected(self, weapon_name: str) -> list[str]:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return ["—", "—", "—", "—", "—", "—"]
        return self._weapon_stat_values(unit_name, weapon_name)

    @QtCore.Slot(str, result="QStringList")
    def roster_weapon_ability_badges_for_weapon(self, weapon_name: str) -> list[str]:
        """Бейджи способностей для конкретного профиля оружия (текущий юнит из списка «Доступные»)."""
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return []
        return self._weapon_ability_badges(unit_name, weapon_name)

    @QtCore.Property(str, notify=trainSetupSummaryChanged)
    def trainSetupSummaryLine(self) -> str:
        return self._format_train_setup_summary_line()

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
    def metricsAlgo(self) -> str:
        v = str(self._metrics_meta.get("algo", "")).strip()
        if v:
            return v.upper()
        return str(self._training_algo or "dqn").upper()

    @QtCore.Property(str, notify=metricsSummaryChanged)
    def metricsMode(self) -> str:
        v = str(self._metrics_meta.get("mode", "")).strip()
        if v:
            return v
        return "actor_learner"

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
            return max(1, int(os.getenv("ACTOR_DET_EVAL_EPISODES", "50")))
        except ValueError:
            return 50

    @QtCore.Property(int, constant=True)
    def detEvalEvery(self) -> int:
        try:
            return max(1, int(os.getenv("ACTOR_DET_EVAL_EVERY_EPISODES", "300")))
        except ValueError:
            return 300

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
        # Фолбэк строим от реального source, а не только от SELF_PLAY_ENABLED.
        source = str(self._metrics_meta.get("opponent_source", "") or self._opponent_source or "").strip().lower()
        if source in {"heuristic", "heuristic_auto"}:
            return "ЭВРИСТИКА"
        if source in {"specific_agent", "latest_snapshot", "snapshot_policy_fn", "fixed_checkpoint"}:
            try:
                lookup = getattr(self, "_specific_opponent_algo_by_id", {})
                selected_id = str(self._metrics_meta.get("opponent_id", "") or self._selected_specific_opponent_id or "").strip()
                resolved = str(lookup.get(selected_id, "")).strip()
                if resolved:
                    return resolved.upper()
            except Exception:
                pass
            return "POLICY"
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

    @QtCore.Property(bool, notify=playModelMetaChanged)
    def playInferenceModeVisible(self) -> bool:
        return is_az_algo(self._play_model_algo_key) or self._play_model_algo_key == "gumbel_muzero"

    @QtCore.Property(str, notify=playModelMetaChanged)
    def playInferenceModeLabel(self) -> str:
        if is_az_algo(self._play_model_algo_key):
            return "Режим AZ:"
        if self._play_model_algo_key == "gumbel_muzero":
            return "Режим GMZ:"
        return "Режим:"

    @QtCore.Property("QVariantList", notify=playModelMetaChanged)
    def playInferenceModeOptions(self):
        if is_az_algo(self._play_model_algo_key):
            return [
                {"value": "greedy", "label": "Greedy"},
                {"value": "mcts", "label": "MCTS"},
            ]
        if self._play_model_algo_key == "gumbel_muzero":
            return [
                {"value": "greedy", "label": "Greedy"},
                {"value": "search", "label": "Search"},
            ]
        return []

    @QtCore.Property(str, notify=playModelMetaChanged)
    def playInferenceMode(self) -> str:
        if is_az_algo(self._play_model_algo_key):
            return self._play_az_mode
        if self._play_model_algo_key == "gumbel_muzero":
            return self._play_gmz_mode
        return "greedy"

    @QtCore.Property(bool, notify=playModelMetaChanged)
    def playInferenceTemperatureVisible(self) -> bool:
        if is_az_algo(self._play_model_algo_key):
            return self._play_az_mode == "mcts"
        if self._play_model_algo_key == "gumbel_muzero":
            return self._play_gmz_mode == "search"
        return False

    @QtCore.Property(str, notify=playModelMetaChanged)
    def playInferenceTemperature(self) -> str:
        if is_az_algo(self._play_model_algo_key):
            return f"{float(self._play_az_temperature):.2f}"
        if self._play_model_algo_key == "gumbel_muzero":
            return f"{float(self._play_gmz_temperature):.2f}"
        return "0.10"

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

    @QtCore.Property("QStringList", constant=True)
    def evalPolicyOptions(self):
        return self._eval_policy_options

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1Policy(self) -> str:
        return self._eval_p1_policy

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2Policy(self) -> str:
        return self._eval_p2_policy

    @QtCore.Property("QStringList", notify=evalSetupChanged)
    def evalP1AgentOptions(self):
        return self._eval_p1_agent_labels

    @QtCore.Property("QStringList", notify=evalSetupChanged)
    def evalP2AgentOptions(self):
        return self._eval_p2_agent_labels

    def _eval_side_algo_key(self, side: str) -> str:
        normalized_side = str(side or "").strip().upper()
        if normalized_side == "P1":
            mode = str(self._eval_p1_policy).strip().lower()
            agent_id = str(self._eval_selected_p1_agent_id).strip()
        else:
            mode = str(self._eval_p2_policy).strip().lower()
            agent_id = str(self._eval_selected_p2_agent_id).strip()
        if mode != "agent" or not agent_id:
            return ""
        rec = self._eval_agent_meta_by_id.get(agent_id, {})
        return str(rec.get("algo", "")).strip().lower()

    def _eval_inference_options_for_algo(self, algo: str) -> list[dict[str, str]]:
        algo_key = str(algo or "").strip().lower()
        if is_az_algo(algo_key):
            return [
                {"value": "greedy", "label": "Greedy"},
                {"value": "mcts", "label": "MCTS"},
            ]
        if algo_key == "gumbel_muzero":
            return [
                {"value": "greedy", "label": "Greedy"},
                {"value": "search", "label": "Search"},
            ]
        return []

    @QtCore.Property(bool, notify=evalSetupChanged)
    def evalP1InferenceModeVisible(self) -> bool:
        return len(self._eval_inference_options_for_algo(self._eval_side_algo_key("P1"))) > 0

    @QtCore.Property(bool, notify=evalSetupChanged)
    def evalP2InferenceModeVisible(self) -> bool:
        return len(self._eval_inference_options_for_algo(self._eval_side_algo_key("P2"))) > 0

    @QtCore.Property("QVariantList", notify=evalSetupChanged)
    def evalP1InferenceModeOptions(self):
        return self._eval_inference_options_for_algo(self._eval_side_algo_key("P1"))

    @QtCore.Property("QVariantList", notify=evalSetupChanged)
    def evalP2InferenceModeOptions(self):
        return self._eval_inference_options_for_algo(self._eval_side_algo_key("P2"))

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1InferenceMode(self) -> str:
        return str(self._eval_p1_inference_mode or "greedy")

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2InferenceMode(self) -> str:
        return str(self._eval_p2_inference_mode or "greedy")

    def _eval_side_temp_visible(self, side: str) -> bool:
        algo = self._eval_side_algo_key(side)
        mode = self._eval_p1_inference_mode if str(side).upper() == "P1" else self._eval_p2_inference_mode
        if is_az_algo(algo):
            return mode == "mcts"
        if algo == "gumbel_muzero":
            return mode == "search"
        return False

    def _sanitize_temperature(self, raw: str, default: float) -> float:
        try:
            value = float(str(raw).strip().replace(",", "."))
        except Exception:
            return float(default)
        if not math.isfinite(value):
            return float(default)
        return float(max(0.001, min(2.0, value)))

    def _eval_side_temperature(self, side: str) -> float:
        side_key = str(side).upper()
        algo = self._eval_side_algo_key(side_key)
        if side_key == "P1":
            if is_az_algo(algo):
                return float(self._eval_p1_az_temperature)
            if algo == "gumbel_muzero":
                return float(self._eval_p1_gmz_temperature)
            return 0.10
        if is_az_algo(algo):
            return float(self._eval_p2_az_temperature)
        if algo == "gumbel_muzero":
            return float(self._eval_p2_gmz_temperature)
        return 0.10

    @QtCore.Property(bool, notify=evalSetupChanged)
    def evalP1InferenceTemperatureVisible(self) -> bool:
        return self._eval_side_temp_visible("P1")

    @QtCore.Property(bool, notify=evalSetupChanged)
    def evalP2InferenceTemperatureVisible(self) -> bool:
        return self._eval_side_temp_visible("P2")

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1InferenceTemperature(self) -> str:
        return f"{self._eval_side_temperature('P1'):.2f}"

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2InferenceTemperature(self) -> str:
        return f"{self._eval_side_temperature('P2'):.2f}"

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1SelectedAgentLabel(self) -> str:
        if not self._eval_selected_p1_agent_id:
            return ""
        try:
            idx = self._eval_p1_agent_ids.index(self._eval_selected_p1_agent_id)
        except ValueError:
            return ""
        return self._eval_p1_agent_labels[idx] if 0 <= idx < len(self._eval_p1_agent_labels) else ""

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2SelectedAgentLabel(self) -> str:
        if not self._eval_selected_p2_agent_id:
            return ""
        try:
            idx = self._eval_p2_agent_ids.index(self._eval_selected_p2_agent_id)
        except ValueError:
            return ""
        return self._eval_p2_agent_labels[idx] if 0 <= idx < len(self._eval_p2_agent_labels) else ""

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalMatchupText(self) -> str:
        return self._eval_matchup_text

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalDuelTitle(self) -> str:
        return self._eval_duel_title

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalDuelSubtitle(self) -> str:
        return self._eval_duel_subtitle

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1DisplayName(self) -> str:
        return self._eval_p1_display_name

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2DisplayName(self) -> str:
        return self._eval_p2_display_name

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1FullAgentId(self) -> str:
        return self._eval_p1_full_agent_id

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2FullAgentId(self) -> str:
        return self._eval_p2_full_agent_id

    @QtCore.Property("QStringList", notify=evalSetupChanged)
    def evalP1Badges(self):
        return self._eval_p1_badges

    @QtCore.Property("QStringList", notify=evalSetupChanged)
    def evalP2Badges(self):
        return self._eval_p2_badges

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP1IconText(self) -> str:
        return self._eval_p1_icon_text

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalP2IconText(self) -> str:
        return self._eval_p2_icon_text

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalScenarioText(self) -> str:
        return self._eval_scenario_text

    @QtCore.Property(bool, notify=evalSetupChanged)
    def evalLaunchReady(self) -> bool:
        return self._eval_launch_ready

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalLaunchStatusText(self) -> str:
        return self._eval_launch_status_text

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalMiniSummary(self) -> str:
        return self._eval_mini_summary

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultHeadline(self) -> str:
        return self._eval_result_headline

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultWinrateP1(self) -> str:
        return self._eval_result_winrate_p1

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultWinrateP2(self) -> str:
        return self._eval_result_winrate_p2

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultAvgVpDiff(self) -> str:
        return self._eval_result_avg_vp_diff

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultTurnLimitRate(self) -> str:
        return self._eval_result_turn_limit_rate

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalResultQualityHint(self) -> str:
        return self._eval_result_quality_hint

    @QtCore.Property(int, notify=evalSetupChanged)
    def evalLiveGamesDone(self) -> int:
        return self._eval_live_games_done

    @QtCore.Property(int, notify=evalSetupChanged)
    def evalLiveGamesTotal(self) -> int:
        return max(0, self._eval_live_games_total)

    @QtCore.Property(int, notify=evalSetupChanged)
    def evalLiveP1Wins(self) -> int:
        return self._eval_live_p1_wins

    @QtCore.Property(int, notify=evalSetupChanged)
    def evalLiveP2Wins(self) -> int:
        return self._eval_live_p2_wins

    @QtCore.Property(int, notify=evalSetupChanged)
    def evalLiveDraws(self) -> int:
        return self._eval_live_draws

    @QtCore.Property(float, notify=evalSetupChanged)
    def evalLiveP1Winrate(self) -> float:
        if self._eval_live_games_done <= 0:
            return 0.5
        return self._eval_live_p1_wins / float(self._eval_live_games_done)

    @QtCore.Property(float, notify=evalSetupChanged)
    def evalLiveP2Winrate(self) -> float:
        if self._eval_live_games_done <= 0:
            return 0.5
        return self._eval_live_p2_wins / float(self._eval_live_games_done)

    @QtCore.Property(float, notify=evalSetupChanged)
    def evalLiveLeadPercent(self) -> float:
        return (self.evalLiveP1Winrate - self.evalLiveP2Winrate) * 100.0

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalLiveLeaderSide(self) -> str:
        if self._eval_live_games_done <= 0:
            return "none"
        lead = self.evalLiveLeadPercent
        if abs(lead) < 2.0:
            return "draw"
        return "P1" if lead > 0 else "P2"

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalLiveStatusText(self) -> str:
        if self._eval_live_games_done <= 0:
            return "Ожидание первой игры"
        lead = self.evalLiveLeadPercent
        abs_lead = abs(lead)
        if abs_lead < 2.0:
            return "Равная серия"
        if abs_lead >= 20.0:
            return "Разгром P1" if lead > 0 else "Разгром P2"
        return "Преимущество P1" if lead > 0 else "Преимущество P2"

    @QtCore.Property(str, notify=evalSetupChanged)
    def evalLiveProgressText(self) -> str:
        total = max(self._eval_live_games_total, self._eval_games)
        if total <= 0:
            return "После 0 игр"
        done = min(self._eval_live_games_done, total)
        return f"После {done}/{total} игр"

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
        return float(self._dqn_hyperparams.get("lr", self._default_dqn_hyperparams["lr"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpTau(self) -> float:
        return float(self._dqn_hyperparams.get("tau", self._default_dqn_hyperparams["tau"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpEpsStart(self) -> float:
        return float(self._dqn_hyperparams.get("eps_start", self._default_dqn_hyperparams["eps_start"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpEpsEnd(self) -> float:
        return float(self._dqn_hyperparams.get("eps_end", self._default_dqn_hyperparams["eps_end"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpEpsDecay(self) -> int:
        return int(self._dqn_hyperparams.get("eps_decay", self._default_dqn_hyperparams["eps_decay"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpBatchSize(self) -> int:
        return int(self._dqn_hyperparams.get("batch_size", self._default_dqn_hyperparams["batch_size"]))

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpGamma(self) -> float:
        return float(self._dqn_hyperparams.get("gamma", self._default_dqn_hyperparams["gamma"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpUpdatesPerStep(self) -> int:
        return int(self._dqn_hyperparams.get("updates_per_step", self._default_dqn_hyperparams["updates_per_step"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpWarmupSteps(self) -> int:
        return int(self._dqn_hyperparams.get("warmup_steps", self._default_dqn_hyperparams["warmup_steps"]))

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

    @QtCore.Property(float, notify=trainingHyperparamsChanged)
    def hpGmzLearningRate(self) -> float:
        return float(self._gmz_hyperparams.get("learning_rate", self._default_gmz_hyperparams["learning_rate"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpGmzBatchSize(self) -> int:
        return int(self._gmz_hyperparams.get("batch_size", self._default_gmz_hyperparams["batch_size"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpGmzNumSimulations(self) -> int:
        return int(self._gmz_hyperparams.get("num_simulations", self._default_gmz_hyperparams["num_simulations"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpGmzRootTopK(self) -> int:
        return int(self._gmz_hyperparams.get("root_top_k", self._default_gmz_hyperparams["root_top_k"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpGmzUnrollSteps(self) -> int:
        return int(self._gmz_hyperparams.get("unroll_steps", self._default_gmz_hyperparams["unroll_steps"]))

    @QtCore.Property(int, notify=trainingHyperparamsChanged)
    def hpGmzNumActors(self) -> int:
        return int(self._gmz_hyperparams.get("num_actors", self._default_gmz_hyperparams["num_actors"]))

    @staticmethod
    def _profile_display_label(profile_key: str) -> str:
        labels = {
            "fast": "Fast",
            "balanced": "Balanced",
            "heavy": "Heavy",
            "custom": "Custom",
        }
        key = str(profile_key or "custom").strip().lower()
        return labels.get(key, "Custom")

    @QtCore.Property(str, notify=trainingHyperparamsChanged)
    def hpDqnPresetLabel(self) -> str:
        return self._profile_display_label(self._dqn_selected_profile)

    @QtCore.Property(str, notify=trainingHyperparamsChanged)
    def hpPpoPresetLabel(self) -> str:
        return self._profile_display_label(self._ppo_selected_profile)

    @QtCore.Property(str, notify=trainingHyperparamsChanged)
    def hpAzTreePresetLabel(self) -> str:
        return self._profile_display_label(self._az_tree_selected_profile)

    @QtCore.Property(str, notify=trainingHyperparamsChanged)
    def hpAzProxyPresetLabel(self) -> str:
        return self._profile_display_label(self._az_proxy_selected_profile)

    @QtCore.Property(str, notify=trainingHyperparamsChanged)
    def hpGmzPresetLabel(self) -> str:
        return self._profile_display_label(self._gmz_selected_profile)

    @QtCore.Property(bool, notify=settingsDirtyChanged)
    def settingsDirty(self) -> bool:
        return self._settings_dirty

    @QtCore.Property(str, notify=settingsSaveStateChanged)
    def settingsSaveState(self) -> str:
        return self._settings_save_state

    @QtCore.Property(str, constant=True)
    def modelsFolderUrl(self) -> str:
        return self._to_file_url(str(ARTIFACTS_MODELS_DIR))

    @QtCore.Property(int, notify=factionIconSizeChanged)
    def factionIconSize(self) -> int:
        return self._icon_sizes["faction"]

    @QtCore.Property(int, notify=unitIconSizeChanged)
    def unitIconSize(self) -> int:
        return self._icon_sizes["unit"]

    def _load_icon_sizes_config(self) -> dict[str, int]:
        defaults = {"unit": 18, "faction": 18}
        config_path = os.path.join(self._app_gui_dir, "icon_sizes.json")
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
            icon_path = os.path.join(self._app_gui_dir, "assets", "necrons.png")
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
            icon_path = os.path.join(self._app_gui_dir, "assets", icon_file)
            icon = QIcon(icon_path) if os.path.exists(icon_path) else QIcon()
        self._unit_icon_cache[cache_key] = icon
        return icon

    def get_unit_icon_source(self, unit_name: str, pixel_size: Optional[int] = None) -> str:
        normalized = self.normalize_unit_name(unit_name)
        if not normalized:
            return ""
        target_px = int(pixel_size) if pixel_size is not None else int(self._unit_icon_size.width())
        target_px = max(12, min(128, target_px))
        cache_key = normalized.casefold()
        source_key = f"{cache_key}:{target_px}"
        if source_key in self._unit_icon_source_cache:
            return self._unit_icon_source_cache[source_key]

        icon = self.get_unit_icon(normalized)
        if icon.isNull():
            self._unit_icon_source_cache[source_key] = ""
            return ""

        target_size = QtCore.QSize(target_px, target_px)
        pixmap = icon.pixmap(target_size)
        if pixmap.isNull():
            self._unit_icon_source_cache[source_key] = ""
            return ""

        scaled = pixmap.scaled(
            target_size,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        image_dir = os.path.join(self._app_gui_dir, ".icon_cache")
        os.makedirs(image_dir, exist_ok=True)
        image_path = os.path.join(image_dir, f"{cache_key.replace(' ', '_')}_{target_px}.png")
        scaled.save(image_path, "PNG")
        source = self._to_file_url(image_path)
        self._unit_icon_source_cache[source_key] = source
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
        icon_path = os.path.join(self._app_gui_dir, "assets", "necrons.png")
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
            self._emit_train_setup_summary_changed()

    @QtCore.Slot(str)
    def set_selected_mission(self, mission: str) -> None:
        normalized = (mission or "only_war").strip().lower().replace("-", "_").replace(" ", "_")
        if normalized not in self._mission_options:
            normalized = "only_war"
        if self._selected_mission != normalized:
            self._selected_mission = normalized
            self.missionChanged.emit(normalized)
            self._emit_train_setup_summary_changed()

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
            if self._eval_live_games_done <= 0:
                self._eval_live_games_total = value
            self.evalGamesChanged.emit(value)
            self._update_eval_matchup_text()
            self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p1_policy(self, value: str) -> None:
        policy = str(value or "").strip().lower()
        if policy not in self._eval_policy_options:
            policy = "heuristic"
        if policy == self._eval_p1_policy:
            return
        self._eval_p1_policy = policy
        self._update_eval_matchup_text()
        self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p2_policy(self, value: str) -> None:
        policy = str(value or "").strip().lower()
        if policy not in self._eval_policy_options:
            policy = "heuristic"
        if policy == self._eval_p2_policy:
            return
        self._eval_p2_policy = policy
        self._update_eval_matchup_text()
        self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p1_agent_by_label(self, label: str) -> None:
        text = str(label or "").strip()
        if not text:
            self._eval_selected_p1_agent_id = ""
            self._update_eval_matchup_text()
            self.evalSetupChanged.emit()
            return
        try:
            idx = self._eval_p1_agent_labels.index(text)
        except ValueError:
            return
        if 0 <= idx < len(self._eval_p1_agent_ids):
            selected = self._eval_p1_agent_ids[idx]
            if selected != self._eval_selected_p1_agent_id:
                self._eval_selected_p1_agent_id = selected
                self._update_eval_matchup_text()
                self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p2_agent_by_label(self, label: str) -> None:
        text = str(label or "").strip()
        if not text:
            self._eval_selected_p2_agent_id = ""
            self._update_eval_matchup_text()
            self.evalSetupChanged.emit()
            return
        try:
            idx = self._eval_p2_agent_labels.index(text)
        except ValueError:
            return
        if 0 <= idx < len(self._eval_p2_agent_ids):
            selected = self._eval_p2_agent_ids[idx]
            if selected != self._eval_selected_p2_agent_id:
                self._eval_selected_p2_agent_id = selected
                self._update_eval_matchup_text()
                self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p1_inference_mode(self, value: str) -> None:
        mode = str(value or "").strip().lower()
        algo = self._eval_side_algo_key("P1")
        allowed = {str(item.get("value", "")).strip().lower() for item in self._eval_inference_options_for_algo(algo)}
        if mode not in allowed:
            mode = "greedy"
        if mode == self._eval_p1_inference_mode:
            return
        self._eval_p1_inference_mode = mode
        self._update_eval_matchup_text()
        self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p2_inference_mode(self, value: str) -> None:
        mode = str(value or "").strip().lower()
        algo = self._eval_side_algo_key("P2")
        allowed = {str(item.get("value", "")).strip().lower() for item in self._eval_inference_options_for_algo(algo)}
        if mode not in allowed:
            mode = "greedy"
        if mode == self._eval_p2_inference_mode:
            return
        self._eval_p2_inference_mode = mode
        self._update_eval_matchup_text()
        self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p1_inference_temperature(self, value: str) -> None:
        algo = self._eval_side_algo_key("P1")
        parsed = self._sanitize_temperature(value, self._eval_side_temperature("P1"))
        changed = False
        if is_az_algo(algo):
            changed = abs(parsed - float(self._eval_p1_az_temperature)) > 1e-9
            self._eval_p1_az_temperature = parsed
        elif algo == "gumbel_muzero":
            changed = abs(parsed - float(self._eval_p1_gmz_temperature)) > 1e-9
            self._eval_p1_gmz_temperature = parsed
        if changed:
            self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_eval_p2_inference_temperature(self, value: str) -> None:
        algo = self._eval_side_algo_key("P2")
        parsed = self._sanitize_temperature(value, self._eval_side_temperature("P2"))
        changed = False
        if is_az_algo(algo):
            changed = abs(parsed - float(self._eval_p2_az_temperature)) > 1e-9
            self._eval_p2_az_temperature = parsed
        elif algo == "gumbel_muzero":
            changed = abs(parsed - float(self._eval_p2_gmz_temperature)) > 1e-9
            self._eval_p2_gmz_temperature = parsed
        if changed:
            self.evalSetupChanged.emit()

    @QtCore.Slot(str)
    def set_play_inference_mode(self, value: str) -> None:
        mode = str(value or "").strip().lower()
        if is_az_algo(self._play_model_algo_key):
            if mode not in {"greedy", "mcts"}:
                mode = "greedy"
            if mode == self._play_az_mode:
                return
            self._play_az_mode = mode
            self.playModelMetaChanged.emit(self._play_model_algo_label)
            self._emit_status(f"Режим AZ для игры: {mode}.")
            return
        if self._play_model_algo_key == "gumbel_muzero":
            if mode not in {"greedy", "search"}:
                mode = "greedy"
            if mode == self._play_gmz_mode:
                return
            self._play_gmz_mode = mode
            self.playModelMetaChanged.emit(self._play_model_algo_label)
            self._emit_status(f"Режим GMZ для игры: {mode}.")

    @QtCore.Slot(str)
    def set_play_inference_temperature(self, value: str) -> None:
        parsed = self._sanitize_temperature(value, 0.10)
        if is_az_algo(self._play_model_algo_key):
            if abs(parsed - float(self._play_az_temperature)) <= 1e-9:
                return
            self._play_az_temperature = parsed
            self.playModelMetaChanged.emit(self._play_model_algo_label)
            return
        if self._play_model_algo_key == "gumbel_muzero":
            if abs(parsed - float(self._play_gmz_temperature)) <= 1e-9:
                return
            self._play_gmz_temperature = parsed
            self.playModelMetaChanged.emit(self._play_model_algo_label)

    @QtCore.Slot()
    def refresh_eval_agents(self) -> None:
        self._refresh_eval_agent_options()
        self._emit_status("Список доступных агентов для оценки обновлён.")

    @QtCore.Slot(str)
    def copy_eval_agent_id(self, side: str) -> None:
        normalized_side = str(side or "").strip().upper()
        if normalized_side == "P1":
            agent_id = str(self._eval_p1_full_agent_id or "").strip()
        elif normalized_side == "P2":
            agent_id = str(self._eval_p2_full_agent_id or "").strip()
        else:
            agent_id = ""
        if not agent_id:
            self._emit_status(f"Для {normalized_side or 'стороны'} нет agent_id для копирования.")
            return
        clipboard = QtGui.QGuiApplication.clipboard()
        clipboard.setText(agent_id)
        self._emit_status(f"Скопирован agent_id для {normalized_side}: {agent_id}")

    @QtCore.Slot(int)
    def add_unit_to_player(self, index: int) -> None:
        if index < 0 or index >= len(self._available_units):
            self._emit_status("Сначала выберите юнит в списке доступных.")
            return
        unit = self._available_units[index]
        entry = self._create_roster_entry(unit)
        self._player_roster.append(entry)
        self._roster_preview_side = "P1"
        self._roster_preview_roster_index = len(self._player_roster) - 1
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
        self._roster_preview_side = "P2"
        self._roster_preview_roster_index = len(self._model_roster) - 1
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
        if self._roster_preview_side == "P1" and self._roster_preview_roster_index >= index:
            self._roster_preview_roster_index -= 1
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
        if self._roster_preview_side == "P2" and self._roster_preview_roster_index >= index:
            self._roster_preview_roster_index -= 1
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Юнит удалён из ростера P2.")

    @QtCore.Slot()
    def clear_player_roster(self) -> None:
        self._player_roster.clear()
        if self._roster_preview_side == "P1":
            self._roster_preview_side = ""
            self._roster_preview_roster_index = -1
        self._persist_rosters()
        self._refresh_models()
        self._update_roster_summary()
        self._update_learner_faction_from_rosters()
        self._emit_status("Ростер P1 очищен.")

    @QtCore.Slot()
    def clear_model_roster(self) -> None:
        self._model_roster.clear()
        if self._roster_preview_side == "P2":
            self._roster_preview_side = ""
            self._roster_preview_roster_index = -1
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
        self._update_opponent_preview_text()

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
        agents_root = os.path.join(str(ARTIFACTS_MODELS_DIR), "agents")
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
            if algo == "alphazero":
                continue
            if algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
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

    def _refresh_eval_agent_options(self) -> None:
        records = self._collect_registered_agents_meta()
        p1_records = [rec for rec in records if str(rec.get("side")) == "P1"]
        p2_records = [rec for rec in records if str(rec.get("side")) == "P2"]
        self._eval_agent_meta_by_id = {
            str(rec.get("agent_id")): {
                "agent_id": str(rec.get("agent_id", "")).strip(),
                "side": str(rec.get("side", "")).strip().upper(),
                "faction": str(rec.get("faction", "Unknown")).strip() or "Unknown",
                "algo": str(rec.get("algo", "unknown")).strip().lower() or "unknown",
            }
            for rec in records
        }
        self._eval_p1_agent_ids = [str(rec.get("agent_id")) for rec in p1_records]
        self._eval_p1_agent_labels = [self._format_eval_agent_option_label(rec) for rec in p1_records]
        self._eval_p2_agent_ids = [str(rec.get("agent_id")) for rec in p2_records]
        self._eval_p2_agent_labels = [self._format_eval_agent_option_label(rec) for rec in p2_records]

        if self._eval_selected_p1_agent_id not in self._eval_p1_agent_ids:
            self._eval_selected_p1_agent_id = self._eval_p1_agent_ids[0] if self._eval_p1_agent_ids else ""
        if self._eval_selected_p2_agent_id not in self._eval_p2_agent_ids:
            self._eval_selected_p2_agent_id = self._eval_p2_agent_ids[0] if self._eval_p2_agent_ids else ""

        if self._eval_p1_policy == "agent" and not self._eval_selected_p1_agent_id:
            self._eval_p1_policy = "heuristic"
        if self._eval_p2_policy == "agent" and not self._eval_selected_p2_agent_id:
            self._eval_p2_policy = "heuristic"

        self._update_eval_matchup_text()
        self.evalSetupChanged.emit()

    def _extract_epoch_tag(self, agent_id: str) -> str:
        text = str(agent_id or "")
        match = re.search(r"ep(\d+)", text, flags=re.IGNORECASE)
        if match:
            return f"ep{match.group(1)}"
        return "ep?"

    def _friendly_agent_name(self, rec: dict[str, str]) -> str:
        faction = str(rec.get("faction", "Unknown")).strip() or "Unknown"
        algo = str(rec.get("algo", "unknown")).strip().upper() or "UNKNOWN"
        agent_id = str(rec.get("agent_id", "")).strip()
        return f"{faction} {algo} ({self._extract_epoch_tag(agent_id)})"

    def _format_eval_agent_option_label(self, rec: dict[str, str]) -> str:
        side = str(rec.get("side", "")).strip().upper() or "P?"
        agent_id = str(rec.get("agent_id", "")).strip()
        suffix = agent_id[-6:] if len(agent_id) >= 6 else agent_id
        return f"{self._friendly_agent_name(rec)} [{side}] · {suffix}"

    def _eval_side_presentation(self, side: str, mode: str, agent_id: str) -> dict[str, object]:
        normalized_side = str(side or "").strip().upper()
        normalized_mode = str(mode or "").strip().lower()
        if normalized_mode == "heuristic":
            return {
                "title": f"{normalized_side}: Эвристика",
                "algo": "HEURISTIC",
                "faction": self._display_faction_for_side(normalized_side),
                "full_id": "",
                "icon": "HR",
                "badges": ["HEURISTIC", self._display_faction_for_side(normalized_side), normalized_side],
                "short": "Эвристика",
                "subtitle": "Правила и приоритеты без нейросети.",
            }
        rec = dict(self._eval_agent_meta_by_id.get(str(agent_id).strip(), {}))
        if not rec:
            return {
                "title": f"{normalized_side}: Агент не выбран",
                "algo": "UNKNOWN",
                "faction": self._display_faction_for_side(normalized_side),
                "full_id": "",
                "icon": "AI",
                "badges": ["AGENT", "UNKNOWN", normalized_side],
                "short": "Агент",
                "subtitle": "Нужно выбрать agent_id.",
            }
        friendly = self._friendly_agent_name(rec)
        algo = str(rec.get("algo", "unknown")).strip().upper() or "UNKNOWN"
        faction = str(rec.get("faction", "Unknown")).strip() or "Unknown"
        return {
            "title": f"{normalized_side}: {friendly}",
            "algo": algo,
            "faction": faction,
            "full_id": str(rec.get("agent_id", "")).strip(),
            "icon": "AI",
            "badges": [algo, faction, normalized_side],
            "short": algo,
            "subtitle": "Нейросетевой агент из registry.",
        }

    def _update_eval_matchup_text(self) -> None:
        p1 = self._eval_side_presentation("P1", self._eval_p1_policy, self._eval_selected_p1_agent_id)
        p2 = self._eval_side_presentation("P2", self._eval_p2_policy, self._eval_selected_p2_agent_id)
        left = str(p1.get("short", "—"))
        right = str(p2.get("short", "—"))
        self._eval_duel_title = f"{left} vs {right}"
        self._eval_duel_subtitle = f"{p1.get('faction', 'Unknown')} vs {p2.get('faction', 'Unknown')}"

        self._eval_p1_display_name = str(p1.get("title", "P1: —"))
        self._eval_p2_display_name = str(p2.get("title", "P2: —"))
        self._eval_p1_full_agent_id = str(p1.get("full_id", ""))
        self._eval_p2_full_agent_id = str(p2.get("full_id", ""))
        self._eval_p1_badges = [str(x) for x in list(p1.get("badges", []))]
        self._eval_p2_badges = [str(x) for x in list(p2.get("badges", []))]
        self._eval_p1_icon_text = str(p1.get("icon", "AI"))
        self._eval_p2_icon_text = str(p2.get("icon", "AI"))

        ok_cfg, _, err = self._build_eval_launch_config()
        self._eval_launch_ready = bool(ok_cfg)
        self._eval_launch_status_text = "Готово к запуску." if ok_cfg else err

        if self._eval_p1_policy == "agent" and self._eval_p2_policy == "agent":
            self._eval_scenario_text = "Сценарий: честный AI vs AI (лучше для ppo vs dqn)."
        elif self._eval_p1_policy == "heuristic" and self._eval_p2_policy == "agent":
            self._eval_scenario_text = "Сценарий: эвристика тестирует силу агента P2."
        elif self._eval_p1_policy == "agent" and self._eval_p2_policy == "heuristic":
            self._eval_scenario_text = "Сценарий: агент P1 против правил эвристики."
        else:
            self._eval_scenario_text = "Сценарий: обе стороны эвристика (недоступно для запуска)."

        self._eval_mini_summary = f"Игр: {self._eval_games} • deterministic • epsilon=0 • AZ-opponent=greedy"
        self._eval_matchup_text = (
            f"{self._eval_p1_display_name}\n"
            f"{self._eval_p2_display_name}\n"
            f"{self._eval_scenario_text}\n"
            f"Статус: {self._eval_launch_status_text}"
        )

    def _build_eval_launch_config(self) -> tuple[bool, dict[str, str], str]:
        p1_mode = str(self._eval_p1_policy).strip().lower()
        p2_mode = str(self._eval_p2_policy).strip().lower()
        p1_agent = str(self._eval_selected_p1_agent_id).strip()
        p2_agent = str(self._eval_selected_p2_agent_id).strip()

        if p1_mode == "heuristic" and p2_mode == "heuristic":
            return False, {}, "Нужно выбрать хотя бы одного агента: обе стороны не могут быть эвристикой."

        if p1_mode == "agent" and not p1_agent:
            return False, {}, "Нужно выбрать агента для P1."
        if p2_mode == "agent" and not p2_agent:
            return False, {}, "Нужно выбрать агента для P2."

        if p1_mode == "agent":
            learner_side = "P1"
            learner_agent_id = p1_agent
            opponent_agent_id = p2_agent if p2_mode == "agent" else ""
        else:
            learner_side = "P2"
            learner_agent_id = p2_agent
            opponent_agent_id = ""

        launch = {
            "learner_side": learner_side,
            "learner_agent_id": learner_agent_id,
            "opponent_agent_id": opponent_agent_id,
        }
        return True, launch, ""

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

    def _train_context_roster_cards(self, roster: list[RosterEntry]) -> list[dict]:
        """Карточки для «Контекст тренировки»: аватар, название, ДБ/ББ по имени; статы — только для тултипа."""
        if not roster:
            return []
        max_visible = 12
        cards: list[dict] = []
        for entry in roster[:max_visible]:
            name = str(entry.name or "").strip() or "—"
            try:
                cnt = int(entry.count)
            except (TypeError, ValueError):
                cnt = 0
            if cnt > 1:
                title = f"{name} ×{cnt}"
            else:
                title = name
            rw = str(entry.ranged_weapon or "").strip()
            mw = str(entry.melee_weapon or "").strip()
            ranged_name = rw or "—"
            melee_name = mw or "—"
            ranged_stat = self._weapon_statline(name, rw) if rw else "—"
            melee_stat = self._weapon_statline(name, mw) if mw else "—"
            inst = str(entry.instance_id or "").strip()
            core_stats = self._core_stat_display_values(name)
            keywords = [self._format_keyword_label(k) for k in self._unit_keywords_by_name.get(name, [])]
            abilities = list(self._unit_abilities_by_name.get(name, []))
            cards.append(
                {
                    "kind": "unit",
                    "title": title,
                    "unitName": name,
                    "instanceId": inst,
                    "unitIcon": self.get_unit_icon_source(name, pixel_size=72),
                    "rangedName": ranged_name,
                    "meleeName": melee_name,
                    "rangedStatline": ranged_stat,
                    "meleeStatline": melee_stat,
                    "rangedIcon": self._weapon_icon_file_url(rw),
                    "meleeIcon": self._weapon_icon_file_url(mw),
                    "coreStats": core_stats,
                    "keywords": keywords,
                    "abilities": abilities,
                }
            )
        remainder = len(roster) - max_visible
        if remainder > 0:
            cards.append(
                {
                    "kind": "more",
                    "title": f"+ещё {remainder}",
                    "unitName": "",
                    "instanceId": "",
                    "unitIcon": "",
                    "rangedName": "",
                    "meleeName": "",
                    "rangedStatline": "",
                    "meleeStatline": "",
                    "rangedIcon": "",
                    "meleeIcon": "",
                    "coreStats": [],
                    "keywords": [],
                    "abilities": [],
                }
            )
        return cards

    def _format_train_setup_summary_line(self) -> str:
        mission = (self._selected_mission or "—").strip().upper().replace("_", " ")
        algo = (self._training_algo or "dqn").strip().upper()
        episodes = int(self._num_games)
        p1 = self._display_faction_for_side("P1")
        p2 = self._display_faction_for_side("P2")
        side = (self._learner_side or "P1").strip().upper()
        src = (self._opponent_source or "heuristic").strip().lower()
        if src == "heuristic":
            opp_l = "ЭВРИСТИКА"
        elif src == "latest_snapshot":
            opp_l = "СНАПШОТ"
        else:
            opp_l = "КОНКР. АГЕНТ"
        return (
            f"{mission} · {algo} · {episodes} эп. · "
            f"P1={p1} · P2={p2} · ОБУЧЕНИЕ {side} · ОППОНЕНТ: {opp_l}"
        )

    def _emit_train_setup_summary_changed(self) -> None:
        self.trainSetupSummaryChanged.emit()

    def _update_opponent_preview_text(self) -> None:
        learner_side = self._learner_side
        opponent_side = "P2" if learner_side == "P1" else "P1"
        learner_faction = self._display_faction_for_side(learner_side)
        opponent_faction = self._display_faction_for_side(opponent_side)
        learner_algo = (self._training_algo or "dqn").strip().lower()
        if learner_algo not in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
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

        learner_short = learner_algo.upper()
        src = (self._opponent_source or "heuristic").strip().lower()
        if src == "heuristic":
            opponent_short = "Эвристика"
        elif src == "latest_snapshot":
            if self._selected_specific_opponent_id and str(opponent_algo).strip().lower() not in {"", "unknown"}:
                opponent_short = str(opponent_algo).upper()
            else:
                opponent_short = "Снапшот"
        else:
            if self._selected_specific_opponent_id and str(opponent_algo).strip().lower() not in {"", "unknown"}:
                opponent_short = str(opponent_algo).upper()
            else:
                opponent_short = "Агент не выбран"

        self._train_context_learner_algo_short = learner_short
        self._train_context_opponent_algo_short = opponent_short
        self._train_context_opponent_side = opponent_side

        self._emit_train_setup_summary_changed()

    @QtCore.Slot(str, str)
    def set_training_hyperparam(self, key: str, value: str) -> None:
        """Legacy: корневые DQN-ключи (lr, tau, …) — делегирует в set_dqn_hyperparam."""
        self.set_dqn_hyperparam(key, value)

    def _coerce_algo_hyperparam(self, key: str, value: str, default: int | float | str) -> int | float | str:
        if key in {"lr_scheduler", "eps_schedule", "dist_type"}:
            parsed = str(value or "").strip().lower()
            return parsed or str(default)
        if isinstance(default, int):
            return int(float(str(value).strip()))
        if isinstance(default, str):
            return str(value or "").strip().lower() or str(default)
        return float(str(value).strip())

    @QtCore.Slot(str, str)
    def set_dqn_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_dqn_hyperparams:
            return
        default = self._default_dqn_hyperparams[normalized_key]
        current = self._dqn_hyperparams.get(normalized_key, default)
        try:
            parsed = self._coerce_algo_hyperparam(normalized_key, value, default)
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение DQN-параметра '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return
        if current == parsed:
            return
        self._dqn_hyperparams[normalized_key] = parsed
        self._refresh_dqn_profile_label()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot(str, str)
    def set_ppo_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_ppo_hyperparams:
            return
        default = self._default_ppo_hyperparams[normalized_key]
        current = self._ppo_hyperparams.get(normalized_key, default)
        try:
            parsed = self._coerce_algo_hyperparam(normalized_key, value, default)
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение PPO-параметра '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return
        if current == parsed:
            return
        self._ppo_hyperparams[normalized_key] = parsed
        self._refresh_ppo_profile_label()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def apply_dqn_profile(self, profile: str) -> None:
        mode = str(profile or "").strip().lower()
        if mode not in {"fast", "balanced", "heavy"}:
            return
        base = dict(self._default_dqn_hyperparams)
        base.update(self._dqn_profile_presets.get(mode, {}))
        self._dqn_hyperparams.update(base)
        self._dqn_selected_profile = mode
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status(f"Применен профиль DQN: {mode}. Сохраните настройки.")

    @QtCore.Slot(str)
    def apply_ppo_profile(self, profile: str) -> None:
        mode = str(profile or "").strip().lower()
        if mode not in {"fast", "balanced", "heavy"}:
            return
        base = dict(self._default_ppo_hyperparams)
        base.update(self._ppo_profile_presets.get(mode, {}))
        self._ppo_hyperparams.update(base)
        self._ppo_selected_profile = mode
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status(f"Применен профиль PPO: {mode}. Сохраните настройки.")

    @QtCore.Slot(str, str)
    def set_gmz_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_gmz_hyperparams:
            return

        current = self._gmz_hyperparams.get(normalized_key, self._default_gmz_hyperparams[normalized_key])
        try:
            if isinstance(self._default_gmz_hyperparams[normalized_key], int):
                parsed: int | float = int(float(str(value).strip()))
            else:
                parsed = float(str(value).strip())
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение GMZ-параметра '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return

        if current == parsed:
            return
        self._gmz_hyperparams[normalized_key] = parsed
        self._refresh_gmz_profile_label()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    def _detect_profile(
        self,
        hyperparams: dict[str, int | float | str],
        presets: dict[str, dict[str, int | float]],
    ) -> str:
        for profile_name in ("fast", "balanced", "heavy"):
            expected = presets.get(profile_name, {})
            if expected and all(hyperparams.get(k) == v for k, v in expected.items()):
                return profile_name
        return "custom"

    def _detect_gmz_profile(self) -> str:
        return self._detect_profile(self._gmz_hyperparams, self._gmz_profile_presets)

    def _refresh_dqn_profile_label(self) -> None:
        self._dqn_selected_profile = self._detect_profile(self._dqn_hyperparams, self._dqn_profile_presets)

    def _refresh_ppo_profile_label(self) -> None:
        self._ppo_selected_profile = self._detect_profile(self._ppo_hyperparams, self._ppo_profile_presets)

    def _refresh_az_tree_profile_label(self) -> None:
        self._az_tree_selected_profile = self._detect_profile(
            self._az_tree_hyperparams, self._az_tree_profile_presets
        )

    def _refresh_az_proxy_profile_label(self) -> None:
        self._az_proxy_selected_profile = self._detect_profile(
            self._az_proxy_hyperparams, self._az_proxy_profile_presets
        )

    def _refresh_gmz_profile_label(self) -> None:
        self._gmz_selected_profile = self._detect_gmz_profile()

    def _refresh_training_profile_labels(self) -> None:
        self._refresh_dqn_profile_label()
        self._refresh_ppo_profile_label()
        self._refresh_az_tree_profile_label()
        self._refresh_az_proxy_profile_label()
        self._refresh_gmz_profile_label()

    @QtCore.Slot(str)
    def apply_gmz_profile(self, profile: str) -> None:
        mode = str(profile or "").strip().lower()
        if mode not in {"fast", "balanced", "heavy"}:
            return
        base = dict(self._default_gmz_hyperparams)
        base.update(self._gmz_profile_presets.get(mode, {}))
        self._gmz_hyperparams.update(base)
        self._gmz_selected_profile = mode
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status(f"Применен профиль Gumbel MuZero: {mode}. Сохраните настройки.")

    def _coerce_az_hyperparam(self, key: str, value: str, default: int | float | str) -> int | float | str:
        if key in {"lr_scheduler", "c_puct_schedule", "mcts_mode"}:
            parsed = str(value or "").strip().lower()
            return parsed or str(default)
        if isinstance(default, int):
            return int(float(str(value).strip()))
        return float(str(value).strip())

    @QtCore.Slot(str, str)
    def set_az_tree_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_az_tree_hyperparams:
            return
        default = self._default_az_tree_hyperparams[normalized_key]
        current = self._az_tree_hyperparams.get(normalized_key, default)
        try:
            parsed = self._coerce_az_hyperparam(normalized_key, value, default)
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение AlphaZero Tree '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return
        if normalized_key == "mcts_mode" and parsed != "tree":
            parsed = "tree"
        if current == parsed:
            return
        self._az_tree_hyperparams[normalized_key] = parsed
        self._refresh_az_tree_profile_label()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot(str, str)
    def set_az_proxy_hyperparam(self, key: str, value: str) -> None:
        normalized_key = str(key or "").strip()
        if normalized_key not in self._default_az_proxy_hyperparams:
            return
        default = self._default_az_proxy_hyperparams[normalized_key]
        current = self._az_proxy_hyperparams.get(normalized_key, default)
        try:
            parsed = self._coerce_az_hyperparam(normalized_key, value, default)
        except (TypeError, ValueError):
            self._emit_status(
                f"Некорректное значение AlphaZero Proxy '{normalized_key}' в Настройках. "
                "Проверьте формат и попробуйте снова."
            )
            return
        if normalized_key == "mcts_mode" and parsed != "proxy":
            parsed = "proxy"
        if current == parsed:
            return
        self._az_proxy_hyperparams[normalized_key] = parsed
        self._refresh_az_proxy_profile_label()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()

    @QtCore.Slot(str)
    def apply_az_tree_profile(self, profile: str) -> None:
        mode = str(profile or "").strip().lower()
        if mode not in {"fast", "balanced", "heavy"}:
            return
        base = dict(self._default_az_tree_hyperparams)
        base.update(self._az_tree_profile_presets.get(mode, {}))
        base["mcts_mode"] = "tree"
        self._az_tree_hyperparams.update(base)
        self._az_tree_selected_profile = mode
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status(f"Применен профиль AlphaZero Tree: {mode}. Сохраните настройки.")

    @QtCore.Slot(str)
    def apply_az_proxy_profile(self, profile: str) -> None:
        mode = str(profile or "").strip().lower()
        if mode not in {"fast", "balanced", "heavy"}:
            return
        base = dict(self._default_az_proxy_hyperparams)
        base.update(self._az_proxy_profile_presets.get(mode, {}))
        base["mcts_mode"] = "proxy"
        self._az_proxy_hyperparams.update(base)
        self._az_proxy_selected_profile = mode
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status(f"Применен профиль AlphaZero Proxy: {mode}. Сохраните настройки.")

    def _az_hyperparams_map_for_qml(self, payload: dict[str, int | float | str]) -> dict:
        """QML-friendly map: only str/int/float (no nested types)."""
        out: dict[str, object] = {}
        for key, raw in payload.items():
            if isinstance(raw, str):
                out[str(key)] = raw
            elif isinstance(raw, bool):
                out[str(key)] = int(raw)
            elif isinstance(raw, int) and not isinstance(raw, bool):
                out[str(key)] = int(raw)
            else:
                try:
                    out[str(key)] = float(raw)
                except (TypeError, ValueError):
                    out[str(key)] = str(raw)
        return out

    @QtCore.Property("QVariantMap", notify=trainingHyperparamsChanged)
    def hpAzTreeHyperparamsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._az_tree_hyperparams)

    @QtCore.Property("QVariantMap", notify=trainingHyperparamsChanged)
    def hpAzProxyHyperparamsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._az_proxy_hyperparams)

    @QtCore.Property("QVariantList", constant=True)
    def hpAzHyperparamKeys(self) -> list:
        return [str(k) for k in AZ_HYPERPARAM_KEYS]

    @QtCore.Property("QVariantMap", notify=trainingHyperparamsChanged)
    def hpDqnHyperparamsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._dqn_hyperparams)

    @QtCore.Property("QVariantMap", notify=trainingHyperparamsChanged)
    def hpPpoHyperparamsMap(self) -> dict:
        return self._az_hyperparams_map_for_qml(self._ppo_hyperparams)

    @QtCore.Property("QVariantList", constant=True)
    def hpDqnHyperparamKeys(self) -> list:
        return [str(k) for k in DQN_HYPERPARAM_KEYS]

    @QtCore.Property("QVariantList", constant=True)
    def hpPpoHyperparamKeys(self) -> list:
        return [str(k) for k in PPO_HYPERPARAM_KEYS]

    def _load_algo_hyperparams_section(
        self,
        payload: dict,
        section_key: str,
        defaults: dict[str, int | float | str],
        keys: tuple[str, ...],
        *,
        root_fallback: bool = False,
    ) -> dict:
        raw = payload.get(section_key, {})
        if not isinstance(raw, dict):
            raw = {}
        updated = dict(defaults)
        for key in keys:
            default_value = defaults.get(key)
            if default_value is None:
                continue
            if key in raw:
                raw_val = raw[key]
            elif root_fallback and key in payload:
                raw_val = payload[key]
            else:
                continue
            try:
                if key in {"lr_scheduler", "eps_schedule", "dist_type"}:
                    updated[key] = str(raw_val).strip().lower() or str(default_value)
                elif isinstance(default_value, int):
                    updated[key] = int(raw_val)
                elif isinstance(default_value, str):
                    updated[key] = str(raw_val).strip().lower() or str(default_value)
                else:
                    updated[key] = float(raw_val)
            except (TypeError, ValueError):
                updated[key] = default_value
        return updated

    def _validate_dqn_hyperparams(self, payload: dict[str, int | float | str]) -> str | None:
        root = {k: payload[k] for k in DQN_ROOT_SYNC_KEYS if k in payload}
        error = self._validate_hyperparams(root)
        if error:
            return error
        hidden_size = int(payload.get("hidden_size", 256))
        if hidden_size < 32:
            return "dqn.hidden_size должен быть >= 32"
        if int(payload.get("num_layers", 2)) < 1:
            return "dqn.num_layers должен быть >= 1"
        if int(payload.get("ensemble_size", 1)) < 1:
            return "dqn.ensemble_size должен быть >= 1"
        dist_type = str(payload.get("dist_type", "iqn")).strip().lower()
        if dist_type != "iqn":
            return "dqn.dist_type сейчас поддерживается только iqn (как в train.py)"
        eps_schedule = str(payload.get("eps_schedule", "exp")).strip().lower()
        if eps_schedule not in {"exp", "linear", "poly", "sigmoid"}:
            return "dqn.eps_schedule должен быть exp, linear, poly или sigmoid"
        lr_scheduler = str(payload.get("lr_scheduler", "none")).strip().lower()
        if lr_scheduler not in {"none", "cosine", "plateau"}:
            return "dqn.lr_scheduler должен быть none, cosine или plateau"
        return None

    def _validate_az_hyperparams(self, payload: dict[str, int | float | str], *, section: str) -> str | None:
        lr = float(payload["learning_rate"])
        batch_size = int(payload["batch_size"])
        mcts_simulations = int(payload["mcts_simulations"])
        num_actors = int(payload["num_actors"])
        replay_min_size = int(payload["replay_min_size"])
        if not (0.0 < lr <= 1.0):
            return f"{section}.learning_rate должен быть в диапазоне (0, 1]"
        if batch_size < 1:
            return f"{section}.batch_size должен быть >= 1"
        if mcts_simulations < 1:
            return f"{section}.mcts_simulations должен быть >= 1"
        if num_actors < 1:
            return f"{section}.num_actors должен быть >= 1"
        if replay_min_size < 1:
            return f"{section}.replay_min_size должен быть >= 1"
        return None

    def _apply_dqn_hyperparams_to_env(self, env: QtCore.QProcessEnvironment) -> None:
        hp = self._dqn_hyperparams
        env.insert("DOUBLE_DQN_ENABLED", str(int(hp.get("double_dqn", 1))))
        env.insert("DUELING_ENABLED", str(int(hp.get("dueling", 1))))
        env.insert("DIST_TYPE", str(hp.get("dist_type", "iqn")))
        env.insert("IQN_N_QUANTILES", str(int(hp.get("iqn_n_quantiles", 32))))
        env.insert("IQN_N_TARGET_QUANTILES", str(int(hp.get("iqn_n_target_quantiles", 32))))
        env.insert("IQN_N_TAU_SAMPLES", str(int(hp.get("iqn_n_tau_samples", 32))))
        env.insert("IQN_EMBED_DIM", str(int(hp.get("iqn_embed_dim", 64))))
        env.insert("IQN_KAPPA", str(float(hp.get("iqn_kappa", 1.0))))
        env.insert("NOISY_SIGMA0", str(float(hp.get("noisy_sigma0", 0.5))))
        env.insert("NOISY_DISABLE_EPS", str(int(hp.get("noisy_disable_eps", 1))))
        env.insert("NOISY_SIGMA_ANNEAL", str(int(hp.get("noisy_sigma_anneal", 0))))
        env.insert("DQN_HIDDEN_SIZE", str(max(32, int(hp.get("hidden_size", 256)))))
        env.insert("DQN_NUM_LAYERS", str(max(1, int(hp.get("num_layers", 2)))))
        env.insert("DQN_ENSEMBLE_SIZE", str(max(1, int(hp.get("ensemble_size", 1)))))
        env.insert("DQN_LR_SCHEDULER", str(hp.get("lr_scheduler", "none")))
        env.insert("PER_ENSEMBLE_PRIORITY_LAMBDA", str(float(hp.get("per_ensemble_priority_lambda", 0.1))))
        env.insert("EPS_SCHEDULE", str(hp.get("eps_schedule", "exp")))

    def _apply_ppo_hyperparams_to_env(self, env: QtCore.QProcessEnvironment) -> None:
        hp = self._ppo_hyperparams
        env.insert("PPO_LR_SCHEDULER", str(hp.get("lr_scheduler", "none")))
        env.insert("PPO_ADAPTIVE_ENTROPY", str(int(hp.get("adaptive_entropy", 0))))
        env.insert("PPO_ENTROPY_TARGET", str(float(hp.get("entropy_target", 0.5))))
        env.insert("PPO_ENTROPY_ADAPT_LR", str(float(hp.get("entropy_adapt_lr", 0.05))))

    def _load_az_hyperparams_section(self, payload: dict, section_key: str, defaults: dict) -> dict:
        raw = payload.get(section_key, {})
        if not isinstance(raw, dict):
            raw = {}
        updated = dict(defaults)
        for key in AZ_HYPERPARAM_KEYS:
            default_value = defaults.get(key)
            if default_value is None:
                continue
            raw_val = raw.get(key, default_value)
            try:
                if key in {"lr_scheduler", "c_puct_schedule", "mcts_mode"}:
                    updated[key] = str(raw_val).strip().lower() or str(default_value)
                elif isinstance(default_value, int):
                    updated[key] = int(raw_val)
                else:
                    updated[key] = float(raw_val)
            except (TypeError, ValueError):
                updated[key] = default_value
        return updated

    @QtCore.Slot()
    def reload_training_hyperparams(self) -> None:
        if self._load_hyperparams_from_disk(log_errors=True):
            self.mark_settings_saved("✓ Сохранено")
            self._emit_status("Параметры тренировки перечитаны из hyperparams.json.")

    @QtCore.Slot()
    def reset_training_hyperparams(self) -> None:
        self._dqn_hyperparams = dict(self._default_dqn_hyperparams)
        self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
        self._gmz_hyperparams = dict(self._default_gmz_hyperparams)
        self._az_tree_hyperparams = dict(self._default_az_tree_hyperparams)
        self._az_proxy_hyperparams = dict(self._default_az_proxy_hyperparams)
        self._refresh_training_profile_labels()
        self.trainingHyperparamsChanged.emit()
        self.mark_settings_dirty()
        self._emit_status("Параметры тренировки сброшены к значениям по умолчанию.")

    @QtCore.Slot()
    def save_training_hyperparams(self) -> None:
        dqn_error = self._validate_dqn_hyperparams(self._dqn_hyperparams)
        if dqn_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {dqn_error}. "
                "Исправьте значения DQN и повторите сохранение."
            )
            return
        ppo_error = self._validate_ppo_hyperparams(self._ppo_hyperparams)
        if ppo_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {ppo_error}. "
                "Исправьте значения PPO и повторите сохранение."
            )
            return
        gmz_error = self._validate_gmz_hyperparams(self._gmz_hyperparams)
        if gmz_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {gmz_error}. "
                "Исправьте значения Gumbel MuZero и повторите сохранение."
            )
            return
        az_tree_error = self._validate_az_hyperparams(self._az_tree_hyperparams, section="alphazero_tree")
        if az_tree_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {az_tree_error}. "
                "Исправьте значения AlphaZero Tree и повторите сохранение."
            )
            return
        az_proxy_error = self._validate_az_hyperparams(self._az_proxy_hyperparams, section="alphazero_proxy")
        if az_proxy_error:
            self._emit_status(
                f"Не удалось сохранить hyperparams.json в Настройках: {az_proxy_error}. "
                "Исправьте значения AlphaZero Proxy и повторите сохранение."
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
            for key in DQN_ROOT_SYNC_KEYS:
                merged_payload[key] = self._dqn_hyperparams[key]
            merged_payload["dqn"] = dict(self._dqn_hyperparams)
            merged_payload["ppo"] = dict(self._ppo_hyperparams)
            merged_payload["gumbel_muzero"] = dict(self._gmz_hyperparams)
            merged_payload["alphazero_tree"] = dict(self._az_tree_hyperparams)
            merged_payload["alphazero_proxy"] = dict(self._az_proxy_hyperparams)
            merged_payload.pop("alphazero", None)
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
        lr_scheduler = str(payload.get("lr_scheduler", "none")).strip().lower()
        if lr_scheduler not in {"none", "cosine", "plateau"}:
            return "ppo.lr_scheduler должен быть none, cosine или plateau"
        if int(payload.get("adaptive_entropy", 0)) not in {0, 1}:
            return "ppo.adaptive_entropy должен быть 0 или 1"
        entropy_target = float(payload.get("entropy_target", 0.5))
        if not (0.0 <= entropy_target <= 2.0):
            return "ppo.entropy_target должен быть в диапазоне [0, 2]"
        entropy_adapt_lr = float(payload.get("entropy_adapt_lr", 0.05))
        if not (0.0 < entropy_adapt_lr <= 1.0):
            return "ppo.entropy_adapt_lr должен быть в диапазоне (0, 1]"
        return None

    def _validate_gmz_hyperparams(self, payload: dict[str, int | float]) -> str | None:
        lr = float(payload["learning_rate"])
        batch_size = int(payload["batch_size"])
        unroll_steps = int(payload["unroll_steps"])
        discount = float(payload["discount"])
        replay_capacity = int(payload["replay_capacity"])
        num_actors = int(payload["num_actors"])
        num_simulations = int(payload["num_simulations"])
        root_top_k = int(payload["root_top_k"])
        if not (0.0 < lr <= 1.0):
            return "gumbel_muzero.learning_rate должен быть в диапазоне (0, 1]"
        if batch_size < 1:
            return "gumbel_muzero.batch_size должен быть >= 1"
        if unroll_steps < 1:
            return "gumbel_muzero.unroll_steps должен быть >= 1"
        if not (0.0 < discount <= 1.0):
            return "gumbel_muzero.discount должен быть в диапазоне (0, 1]"
        if replay_capacity < 1024:
            return "gumbel_muzero.replay_capacity должен быть >= 1024"
        if num_actors < 1:
            return "gumbel_muzero.num_actors должен быть >= 1"
        if num_simulations < 1:
            return "gumbel_muzero.num_simulations должен быть >= 1"
        if root_top_k < 1:
            return "gumbel_muzero.root_top_k должен быть >= 1"
        return None

    def _load_hyperparams_from_disk(self, log_errors: bool = False) -> bool:
        try:
            with open(self._hyperparams_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            self._dqn_hyperparams = dict(self._default_dqn_hyperparams)
            self._ppo_hyperparams = dict(self._default_ppo_hyperparams)
            self._gmz_hyperparams = dict(self._default_gmz_hyperparams)
            self._az_tree_hyperparams = dict(self._default_az_tree_hyperparams)
            self._az_proxy_hyperparams = dict(self._default_az_proxy_hyperparams)
            self._refresh_training_profile_labels()
            self.trainingHyperparamsChanged.emit()
            if log_errors:
                self._emit_status(
                    "Не удалось прочитать hyperparams.json в Настройках. "
                    f"Причина: {exc}. Использую значения по умолчанию."
                )
                self._emit_log(f"[GUI] Ошибка чтения {self._hyperparams_path}: {exc}", level="WARN")
            return False

        self._dqn_hyperparams = self._load_algo_hyperparams_section(
            payload,
            "dqn",
            self._default_dqn_hyperparams,
            DQN_HYPERPARAM_KEYS,
            root_fallback=True,
        )
        self._ppo_hyperparams = self._load_algo_hyperparams_section(
            payload,
            "ppo",
            self._default_ppo_hyperparams,
            PPO_HYPERPARAM_KEYS,
            root_fallback=False,
        )

        gmz_raw = payload.get("gumbel_muzero", {})
        if not isinstance(gmz_raw, dict):
            gmz_raw = {}
        gmz_updated = dict(self._default_gmz_hyperparams)
        for key, default_value in self._default_gmz_hyperparams.items():
            raw = gmz_raw.get(key, default_value)
            try:
                if isinstance(default_value, int):
                    gmz_updated[key] = int(raw)
                else:
                    gmz_updated[key] = float(raw)
            except (TypeError, ValueError):
                gmz_updated[key] = default_value
        self._gmz_hyperparams = gmz_updated
        self._az_tree_hyperparams = self._load_az_hyperparams_section(
            payload, "alphazero_tree", self._default_az_tree_hyperparams
        )
        self._az_proxy_hyperparams = self._load_az_hyperparams_section(
            payload, "alphazero_proxy", self._default_az_proxy_hyperparams
        )
        self._az_tree_hyperparams["mcts_mode"] = "tree"
        self._az_proxy_hyperparams["mcts_mode"] = "proxy"
        self._refresh_training_profile_labels()
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
            self._emit_status(
                "Кэш моделей, runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, runtime/logs/LOGS_FOR_AGENTS_PLAY.md, "
                "runtime/logs/LOGS_FOR_AGENTS_EVAL.md и artifacts/results/results.txt очищены."
            )
            self._emit_log(
                "[GUI] Кэш моделей, runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, runtime/logs/LOGS_FOR_AGENTS_PLAY.md, "
                "runtime/logs/LOGS_FOR_AGENTS_EVAL.md и artifacts/results/results.txt очищены."
            )
        except OSError as exc:
            message = (
                "Не удалось очистить кэш и логи. "
                "Где: gui_qt/main.py (clear_model_cache). "
                "Что делать: проверьте права доступа к artifacts/models/, artifacts/metrics/, "
                "runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, runtime/logs/LOGS_FOR_AGENTS_PLAY.md, "
                "runtime/logs/LOGS_FOR_AGENTS_EVAL.md и artifacts/results/results.txt, затем повторите."
            )
            self._emit_status(message)
            self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")

    @QtCore.Slot()
    def clear_agent_logs(self) -> None:
        try:
            self._clear_runtime_logs()
            self._emit_status(
                "runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, runtime/logs/LOGS_FOR_AGENTS_PLAY.md, "
                "runtime/logs/LOGS_FOR_AGENTS_EVAL.md и artifacts/results/results.txt очищены."
            )
            self._emit_log(
                "[GUI] runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, runtime/logs/LOGS_FOR_AGENTS_PLAY.md, "
                "runtime/logs/LOGS_FOR_AGENTS_EVAL.md и artifacts/results/results.txt очищены."
            )
        except OSError as exc:
            message = (
                "Не удалось очистить логи. "
                "Где: gui_qt/main.py (clear_agent_logs). "
                "Что делать: проверьте путь и права доступа к runtime/logs/LOGS_FOR_AGENTS_TRAIN.md, "
                "runtime/logs/LOGS_FOR_AGENTS_PLAY.md, runtime/logs/LOGS_FOR_AGENTS_EVAL.md "
                "и artifacts/results/results.txt, затем повторите."
            )
            self._emit_status(message)
            self._emit_log(f"[GUI] {message} Детали: {exc}", level="ERROR")

    @QtCore.Slot()
    def clear_eval_log(self) -> None:
        try:
            ensure_runtime_dirs()
            eval_log_path = str(AGENT_EVAL_LOG_PATH)
            with open(eval_log_path, "w", encoding="utf-8"):
                pass
            self._set_eval_log_text("")
            self._emit_status("Лог оценки очищен: runtime/logs/LOGS_FOR_AGENTS_EVAL.md.")
            self._emit_log("[GUI] Лог оценки очищен: runtime/logs/LOGS_FOR_AGENTS_EVAL.md.", level="INFO")
        except OSError as exc:
            message = (
                "Не удалось очистить лог оценки. "
                "Где: gui_qt/main.py (clear_eval_log). "
                "Что делать: проверьте права доступа к runtime/logs/LOGS_FOR_AGENTS_EVAL.md и повторите."
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
        json_path = os.path.join(str(ARTIFACTS_MODELS_DIR), f"data_{metrics_id}.json")
        if not os.path.exists(json_path):
            self._emit_status("Файл метрик не найден в artifacts/models/.")
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
        self._sync_metrics_with_model(path)
        self._emit_status("Модель для игры обновлена.")

    @QtCore.Slot()
    def select_latest_play_model(self) -> None:
        self._apply_latest_play_selection(initial=False, emit_status=True)

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
                "Не найдено checkpoint_ep*.pth в artifacts/models/. "
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

        ok_cfg, cfg, err = self._build_eval_launch_config()
        if not ok_cfg:
            self._emit_status(err)
            return
        learner_agent_id = str(cfg.get("learner_agent_id", "")).strip()
        opponent_agent_id = str(cfg.get("opponent_agent_id", "")).strip()
        learner_side = str(cfg.get("learner_side", "P1")).strip().upper() or "P1"
        opponent_side = "P2" if learner_side == "P1" else "P1"
        learner_algo = self._eval_side_algo_key(learner_side)
        opponent_algo = self._eval_side_algo_key(opponent_side)
        learner_mode = self._eval_p1_inference_mode if learner_side == "P1" else self._eval_p2_inference_mode
        opponent_mode = self._eval_p1_inference_mode if opponent_side == "P1" else self._eval_p2_inference_mode

        model_path = self._resolve_eval_model_path()
        if not learner_agent_id and model_path == "None":
            self._emit_status(
                "Не удалось запустить оценку: не выбрана модель и не выбран агент learner. "
                "Что делать: выберите хотя бы одного агента в P1/P2 либо укажите .pickle."
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
        self._reset_eval_kpi_state()

        env = QtCore.QProcessEnvironment.systemEnvironment()
        env.insert("FORCE_GREEDY", "1")
        env.insert("EVAL_EPSILON", "0")
        env.insert("PYTHONPATH", self._pythonpath_with_core())
        env.insert("MISSION_NAME", self._selected_mission)
        env.insert("DEPLOYMENT_MODE", self._deployment_mode)
        if self._deployment_mode == "manual_player":
            self._emit_log(
                "[GUI] [EVAL] DEPLOYMENT_MODE=manual_player не поддерживается для неинтерактивного eval.py; "
                "переключаю DEPLOYMENT_MODE=auto.",
                level="WARN",
            )
            env.insert("DEPLOYMENT_MODE", "auto")
        if self._deployment_mode == "rl_phase":
            env.insert("DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE", "0")
        env.insert("LEARNER_SIDE", learner_side)
        env.insert("LEARNER_FACTION", self._display_faction_for_side(learner_side))
        env.insert("LEAGUE_ENABLE", "1")
        az_eval_mode = learner_mode if is_az_algo(learner_algo) and learner_mode in {"greedy", "mcts"} else "greedy"
        az_opponent_mode = "greedy"
        if is_az_algo(opponent_algo) and opponent_mode in {"greedy", "mcts"}:
            az_opponent_mode = opponent_mode
        env.insert("AZ_EVAL_MODE", az_eval_mode)
        env.insert("AZ_EVAL_OPPONENT_MODE", az_opponent_mode)
        if az_eval_mode == "mcts" or az_opponent_mode == "mcts":
            if is_az_algo(learner_algo) and az_eval_mode == "mcts":
                env.insert("AZ_EVAL_MCTS_TEMPERATURE", f"{self._eval_side_temperature(learner_side):.3f}")
            if is_az_algo(opponent_algo) and az_opponent_mode == "mcts":
                env.insert("AZ_EVAL_OPPONENT_MCTS_TEMPERATURE", f"{self._eval_side_temperature(opponent_side):.3f}")
            env.insert("AZ_EVAL_MCTS_DIR_EPS", "0.0")
        # Fast GMZ eval preset: lower search budget + selectable mode for learner/opponent.
        env.insert("GMZ_EVAL_SIMS", "32")
        env.insert("GMZ_EVAL_ROOT_TOP_K", "8")
        gmz_eval_mode = learner_mode if learner_algo == "gumbel_muzero" and learner_mode in {"greedy", "search"} else "greedy"
        gmz_opponent_mode = opponent_mode if opponent_algo == "gumbel_muzero" and opponent_mode in {"greedy", "search"} else "greedy"
        env.insert("GMZ_EVAL_MODE", gmz_eval_mode)
        env.insert("GMZ_OPPONENT_MODE", gmz_opponent_mode)
        if learner_algo == "gumbel_muzero" and gmz_eval_mode == "search":
            env.insert("GMZ_EVAL_TEMPERATURE", f"{self._eval_side_temperature(learner_side):.3f}")
        if opponent_algo == "gumbel_muzero" and gmz_opponent_mode == "search":
            env.insert("GMZ_EVAL_OPPONENT_TEMPERATURE", f"{self._eval_side_temperature(opponent_side):.3f}")
        env.insert("AGENT_LOG_FILE", str(AGENT_TRAIN_LOG_PATH.relative_to(PROJECT_ROOT)))
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

        args = ["-u", "eval.py", "--games", str(self._eval_games)]
        if model_path != "None":
            args.extend(["--model", model_path])
        if learner_agent_id:
            args.extend(["--learner-agent-id", learner_agent_id])
        if opponent_agent_id:
            args.extend(["--opponent-agent-id", opponent_agent_id])
        mode_parts: list[str] = []
        if is_az_algo(learner_algo) or is_az_algo(opponent_algo):
            az_eval_tail = f"AZ-eval={az_eval_mode}"
            az_opp_tail = f"AZ-opponent-mode={az_opponent_mode}"
            if is_az_algo(learner_algo) and az_eval_mode == "mcts":
                az_eval_tail += f"(temp={self._eval_side_temperature(learner_side):.2f})"
            if is_az_algo(opponent_algo) and az_opponent_mode == "mcts":
                az_opp_tail += f"(temp={self._eval_side_temperature(opponent_side):.2f})"
            mode_parts.append(az_eval_tail)
            mode_parts.append(az_opp_tail)
        if learner_algo == "gumbel_muzero" or opponent_algo == "gumbel_muzero":
            gmz_eval_tail = f"GMZ-eval={gmz_eval_mode}(sims=32,top_k=8)"
            gmz_opp_tail = f"GMZ-opponent={gmz_opponent_mode}"
            if learner_algo == "gumbel_muzero" and gmz_eval_mode == "search":
                gmz_eval_tail += f"(temp={self._eval_side_temperature(learner_side):.2f})"
            if opponent_algo == "gumbel_muzero" and gmz_opponent_mode == "search":
                gmz_opp_tail += f"(temp={self._eval_side_temperature(opponent_side):.2f})"
            mode_parts.append(gmz_eval_tail)
            mode_parts.append(gmz_opp_tail)
        mode_tail = (", " + ", ".join(mode_parts)) if mode_parts else ""
        eval_start_msg = (
            f"Старт оценки: игр={self._eval_games}, learner_side={learner_side}, "
            f"learner_agent_id={learner_agent_id or '-'}, opponent_agent_id={opponent_agent_id or 'heuristic'}, "
            f"модель={os.path.basename(model_path) if model_path != 'None' else 'registry/roster'}"
            f"{mode_tail}, exploration=off."
        )
        self._emit_log(f"[EVAL] {eval_start_msg}", level="INFO")
        self._append_eval_log_line(eval_start_msg)
        self._emit_status("Оценка запущена...")
        self._process.start(self._runtime_python, args)
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
        if not self._refresh_train_data_json_from_rosters(expected_num_life=None):
            return
        command = self._build_script_command(script, [model_path])
        env = os.environ.copy()
        env["MISSION_NAME"] = self._selected_mission
        env["DEPLOYMENT_MODE"] = self._deployment_mode
        env["AGENT_LOG_FILE"] = str(AGENT_PLAY_LOG_PATH.relative_to(PROJECT_ROOT))
        if is_az_algo(self._play_model_algo_key):
            env["AZ_PLAY_MODE"] = self._play_az_mode
            if self._play_az_mode == "mcts":
                env["AZ_PLAY_MCTS_TEMPERATURE"] = f"{float(self._play_az_temperature):.3f}"
                env["AZ_PLAY_MCTS_DIR_EPS"] = "0.0"
        elif self._play_model_algo_key == "gumbel_muzero":
            env["GMZ_PLAY_MODE"] = self._play_gmz_mode
            if self._play_gmz_mode == "search":
                env["GMZ_PLAY_TEMPERATURE"] = f"{float(self._play_gmz_temperature):.3f}"
        if self._play_agent_override_id:
            env["VIEWER_AGENT_ID"] = self._play_agent_override_id
            player_label, model_label = self._infer_viewer_role_labels_from_agent_id(
                self._play_agent_override_id
            )
        else:
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
        if not self._is_windows:
            self._emit_status("Linux/macOS скрипты удалены. Используйте Windows .bat запуск.")
            return
        script = os.path.join(self._repo_root, "scripts", "viewer.bat")
        if not os.path.exists(script):
            self._emit_status("Не найден скрипт Viewer. Проверьте репозиторий.")
            return
        self._persist_rosters()
        if not self._refresh_train_data_json_from_rosters(expected_num_life=None):
            return
        env = os.environ.copy()
        env["MODEL_PATH"] = model_path
        env["FIGHT_REPORT"] = "1"
        env["PLAY_NO_EXPLORATION"] = "1"
        env["MISSION_NAME"] = self._selected_mission
        env["DEPLOYMENT_MODE"] = self._deployment_mode
        env["AGENT_LOG_FILE"] = str(AGENT_PLAY_LOG_PATH.relative_to(PROJECT_ROOT))
        if is_az_algo(self._play_model_algo_key):
            env["AZ_PLAY_MODE"] = self._play_az_mode
            if self._play_az_mode == "mcts":
                env["AZ_PLAY_MCTS_TEMPERATURE"] = f"{float(self._play_az_temperature):.3f}"
                env["AZ_PLAY_MCTS_DIR_EPS"] = "0.0"
        elif self._play_model_algo_key == "gumbel_muzero":
            env["GMZ_PLAY_MODE"] = self._play_gmz_mode
            if self._play_gmz_mode == "search":
                env["GMZ_PLAY_TEMPERATURE"] = f"{float(self._play_gmz_temperature):.3f}"
        if self._play_agent_override_id:
            env["VIEWER_AGENT_ID"] = self._play_agent_override_id
            player_label, model_label = self._infer_viewer_role_labels_from_agent_id(
                self._play_agent_override_id
            )
        else:
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
        mode_hint = "greedy"
        if is_az_algo(self._play_model_algo_key):
            mode_hint = self._play_az_mode
        elif self._play_model_algo_key == "gumbel_muzero":
            mode_hint = self._play_gmz_mode
        self._emit_log(f"[VIEWER] Запуск режима игры: {mode_hint} (exploration=off).", level="INFO")
        self._emit_status(f"Запуск игры в GUI через Viewer ({mode_hint}, без исследования).")

    def _infer_viewer_role_labels_from_model_pickle(self, pickle_path: str) -> tuple[str, str]:
        """
        Подписи для Viewer легенды.
        В Viewer: side=`player` = человек, side=`model` = policy (ИИ).
        В папке artifacts/models/<safe_name>/model-*.pickle safe_name содержит:
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

    def _infer_viewer_role_labels_from_agent_id(self, agent_id: str) -> tuple[str, str]:
        default_player = "Игрок"
        default_model = "Модель"
        raw = str(agent_id or "").strip()
        match = re.match(r"^(P[12])_([^_]+)", raw)
        if not match:
            return default_player, default_model
        ai_side = match.group(1)
        ai_faction = match.group(2)
        human_side = "P2" if ai_side == "P1" else "P1"
        human_faction = self._display_faction_for_side(human_side)
        return f"Ты: {human_side} ({human_faction})", f"ИИ: {ai_side} ({ai_faction})"

    def _check_torch_import(self) -> bool:
        command = [
            self._runtime_python,
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
        board_path = str(BOARD_PATH)
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
        self._update_opponent_preview_text()
        if self._auto_clear_logs:
            try:
                self._clear_runtime_logs(clear_play=False, clear_results=False)
                self._emit_log("[GUI] Автоочистка: runtime/logs/LOGS_FOR_AGENTS_TRAIN.md очищен.", level="INFO")
            except OSError as exc:
                message = (
                    "Не удалось автоматически очистить логи перед тренировкой. "
                    "Где: gui_qt/main.py (_start_training). "
                    "Что делать: проверьте доступ к runtime/logs/LOGS_FOR_AGENTS_TRAIN.md или снимите галочку автоочистки."
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
        effective_opp_id = str(env_overrides.get("OPPONENT_AGENT_ID", "") or "").strip()
        opp_algo = "heuristic" if selected_opponent_source == "heuristic" else "unknown"
        if selected_opponent_source in {"latest_snapshot", "specific_agent"} and effective_opp_id:
            opp_algo = str(self._specific_opponent_algo_by_id.get(effective_opp_id, "unknown"))
        learner_algo = str(self._training_algo or "dqn").strip().lower()
        self._emit_log(
            f"[GUI] [MATCHUP] learner_algo={learner_algo} opponent_algo={opp_algo} opponent_agent_id={effective_opp_id or '-'}",
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
        self._apply_dqn_hyperparams_to_env(env)
        if self._training_algo == "ppo":
            self._apply_ppo_hyperparams_to_env(env)
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
        if self._action_trace:
            # Полный лог матча для train: фазы/ходы/действия, включая AlphaZero self-play без trunc.
            env.insert("VERBOSE_LOGS", "1")
            env.insert("TRAIN_DEBUG", "1")
            env.insert("FIGHT_REPORT", "1")
        else:
            env.insert("VERBOSE_LOGS", "0")
            env.insert("TRAIN_DEBUG", "0")
            env.insert("FIGHT_REPORT", "0")
        env.insert("LEAGUE_ENABLE", "1")
        env.insert("DEPLOYMENT_MODE", self._deployment_mode)
        env.insert("TRAIN_EPISODES_OVERRIDE", str(int(self._num_games)))
        if self._training_algo == "gumbel_muzero":
            gmz_map = {
                "learning_rate": "GMZ_LR",
                "batch_size": "GMZ_BATCH_SIZE",
                "unroll_steps": "GMZ_UNROLL_STEPS",
                "value_loss_weight": "GMZ_VALUE_LOSS_WEIGHT",
                "reward_loss_weight": "GMZ_REWARD_LOSS_WEIGHT",
                "l2_weight": "GMZ_L2_WEIGHT",
                "discount": "GMZ_DISCOUNT",
                "replay_capacity": "GMZ_REPLAY_CAPACITY",
                "num_actors": "GMZ_NUM_ACTORS",
                "actor_batch_send": "GMZ_ACTOR_BATCH_SEND",
                "actor_queue_max": "GMZ_ACTOR_QUEUE_MAX",
                "sync_every_updates": "GMZ_SYNC_EVERY_UPDATES",
                "updates_per_rollout": "GMZ_UPDATES_PER_ROLLOUT",
                "replay_min_size": "GMZ_REPLAY_MIN_SIZE",
                "max_policy_staleness_updates": "GMZ_MAX_POLICY_STALENESS_UPDATES",
                "latent_dim": "GMZ_LATENT_DIM",
                "hidden_dim": "GMZ_HIDDEN_DIM",
                "action_embed_dim": "GMZ_ACTION_EMBED_DIM",
                "num_simulations": "GMZ_MCTS_SIMS",
                "root_top_k": "GMZ_ROOT_TOP_K",
                "gumbel_scale": "GMZ_GUMBEL_SCALE",
                "search_temperature": "GMZ_SEARCH_TEMPERATURE",
                "temperature_opening_moves": "GMZ_TEMP_OPENING_MOVES",
                "temperature_opening_value": "GMZ_TEMP_OPENING",
                "temperature_late_value": "GMZ_TEMP_LATE",
                "outcome_only": "GMZ_OUTCOME_ONLY",
                "outcome_value_win": "GMZ_OUTCOME_VALUE_WIN",
                "outcome_value_loss": "GMZ_OUTCOME_VALUE_LOSS",
                "outcome_value_draw": "GMZ_OUTCOME_VALUE_DRAW",
            }
            for key, env_key in gmz_map.items():
                env.insert(env_key, str(self._gmz_hyperparams.get(key, self._default_gmz_hyperparams.get(key))))
        if self._deployment_mode == "manual_player":
            self._emit_log(
                "[GUI] [TRAIN] DEPLOYMENT_MODE=manual_player не поддерживается для неинтерактивного train.py; "
                "принудительно переключаю в auto.",
                level="WARN",
            )
            env.insert("DEPLOYMENT_MODE", "auto")
        if self._deployment_mode == "rl_phase":
            env.insert("DEPLOYMENT_PLAYER_MANUAL_IN_RL_PHASE", "0")
        env.insert("AGENT_LOG_FILE", str(AGENT_TRAIN_LOG_PATH.relative_to(PROJECT_ROOT)))
        if is_az_algo(self._training_algo):
            az_hp = (
                self._az_tree_hyperparams
                if self._training_algo == "alphazero_tree"
                else self._az_proxy_hyperparams
            )
            az_mode = "tree" if self._training_algo == "alphazero_tree" else "proxy"
            env.insert("AZ_MCTS_SIMULATIONS", os.getenv("AZ_MCTS_SIMULATIONS", str(int(az_hp.get("mcts_simulations", 32)))))
            env.insert("AZ_NUM_ACTORS", os.getenv("AZ_NUM_ACTORS", env_overrides.get("NUM_ACTORS", str(int(az_hp.get("num_actors", 8))))))
            env.insert("AZ_MCTS_MAX_DEPTH", os.getenv("AZ_MCTS_MAX_DEPTH", str(int(az_hp.get("mcts_max_depth", 2 if az_mode == "tree" else 1)))))
            env.insert("AZ_MCTS_TOP_K_PER_HEAD", os.getenv("AZ_MCTS_TOP_K_PER_HEAD", str(int(az_hp.get("mcts_top_k_per_head", 8)))))
            env.insert("AZ_HEARTBEAT_SEC", os.getenv("AZ_HEARTBEAT_SEC", "15"))
            env.insert("AZ_ACTOR_HEARTBEAT_MOVES", os.getenv("AZ_ACTOR_HEARTBEAT_MOVES", "5"))
            env.insert("ACTOR_PROGRESS_STDOUT_EVERY", "1")
            az_sims = env.value("AZ_MCTS_SIMULATIONS", "32")
            az_actors = env.value("AZ_NUM_ACTORS", "8")
            az_depth = env.value("AZ_MCTS_MAX_DEPTH", "2")
            self._emit_log(
                f"[GUI] [AZ][CONFIG] train8: algo={self._training_algo} mcts_mode={az_mode} "
                f"sims={az_sims} depth={az_depth} actors={az_actors}",
                level="INFO",
            )
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

        if self._training_algo == "ppo":
            start_message = (
                f"Старт {status_prefix.lower()}: PPO="
                "on(lr=3e-4,gamma=0.99,gae=0.95,clip=0.2,rollout=1024,epochs=4,minibatch=256)."
            )
        elif self._training_algo == "alphazero_tree":
            az_hp = self._az_tree_hyperparams
            start_message = (
                f"Старт {status_prefix.lower()}: AlphaZero TREE="
                f"on(mcts={int(az_hp.get('mcts_simulations', 128))},depth={int(az_hp.get('mcts_max_depth', 4))},"
                "c_puct=1.1,batch=128)."
            )
        elif self._training_algo == "alphazero_proxy":
            az_hp = self._az_proxy_hyperparams
            start_message = (
                f"Старт {status_prefix.lower()}: AlphaZero PROXY="
                f"on(mcts={int(az_hp.get('mcts_simulations', 32))},depth={int(az_hp.get('mcts_max_depth', 1))},"
                "c_puct=1.1,batch=128)."
            )
        elif self._training_algo == "gumbel_muzero":
            gmz_sims = int(self._gmz_hyperparams.get("num_simulations", self._default_gmz_hyperparams["num_simulations"]))
            gmz_top_k = int(self._gmz_hyperparams.get("root_top_k", self._default_gmz_hyperparams["root_top_k"]))
            gmz_unroll = int(self._gmz_hyperparams.get("unroll_steps", self._default_gmz_hyperparams["unroll_steps"]))
            gmz_replay = int(self._gmz_hyperparams.get("replay_capacity", self._default_gmz_hyperparams["replay_capacity"]))
            gmz_batch = int(self._gmz_hyperparams.get("batch_size", self._default_gmz_hyperparams["batch_size"]))
            gmz_actors = int(self._gmz_hyperparams.get("num_actors", self._default_gmz_hyperparams["num_actors"]))
            start_message = (
                f"Старт {status_prefix.lower()}: GumbelMuZero="
                f"on(sims={gmz_sims},root_top_k={gmz_top_k},unroll={gmz_unroll},"
                f"replay={gmz_replay},batch={gmz_batch},actors={gmz_actors})."
            )
        else:
            dqn_hp = self._dqn_hyperparams
            start_message = (
                f"Старт {status_prefix.lower()}: trunk=residual+LN "
                f"hidden={int(dqn_hp.get('hidden_size', 256))} "
                f"layers={int(dqn_hp.get('num_layers', 2))} "
                f"ensemble={int(dqn_hp.get('ensemble_size', 1))} "
                f"lr_sched={dqn_hp.get('lr_scheduler', 'none')}, "
                "PER=1, N_STEP=3, "
                f"NoisyNet=on(sigma0={float(dqn_hp.get('noisy_sigma0', 0.5))}), "
                f"IQN=on(nq={int(dqn_hp.get('iqn_n_quantiles', 32))},"
                f"nt={int(dqn_hp.get('iqn_n_target_quantiles', 32))},"
                f"tau={int(dqn_hp.get('iqn_n_tau_samples', 32))},"
                f"embed={int(dqn_hp.get('iqn_embed_dim', 64))},"
                f"kappa={float(dqn_hp.get('iqn_kappa', 1.0))})."
            )
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

    def _refresh_train_data_json_from_rosters(self, *, expected_num_life: Optional[int] = None) -> bool:
        """Пересобрать runtime/state/data.json из runtime/state/units.txt (data.bat → initFile.py)."""
        script = self._script_path("data")
        # initFile.py: unit-списки и оружие по строкам — из units.txt; фракции — из ростеров learner/model.
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
        try:
            with open(str(TRAIN_DATA_PATH), "r", encoding="utf-8") as handle:
                payload = json.load(handle)
            actual_num_life = int(payload.get("numLife", 0) or 0)
        except Exception as exc:
            self._emit_status("Не удалось проверить runtime/state/data.json после подготовки данных.")
            self._emit_log(f"[GUI] Ошибка валидации runtime/state/data.json: {exc}", level="ERROR")
            return False
        if expected_num_life is not None and actual_num_life != int(expected_num_life):
            self._emit_status(
                f"Подготовка данных вернула numLife={actual_num_life}, ожидалось {int(expected_num_life)}. Запуск остановлен."
            )
            self._emit_log(
                "[GUI] Несоответствие numLife после data-скрипта: "
                f"expected={int(expected_num_life)} actual={actual_num_life}.",
                level="ERROR",
            )
            return False
        return True

    def _prepare_training_data(self) -> bool:
        try:
            self._persist_rosters()
            return self._refresh_train_data_json_from_rosters(expected_num_life=int(self._num_games))
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
                    self._maybe_update_eval_live(line)
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
            "[AZ]",
        )
        allowed_contains = (
            "Training...",
            "Generated metrics",
            "Forging model_train.gif",
            "genDisplay.makeGif:",
            "ep=",
            "mcts_mode=",
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
            self._refresh_eval_agent_options()
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
        for summary_prefix in ("[EVAL][SUMMARY_V2] ", "[SUMMARY_V2] "):
            if normalized.startswith(summary_prefix):
                payload = normalized[len(summary_prefix):]
                details = self._format_eval_summary_v2(payload)
                self._set_eval_summary_text(details)
                return
        for summary_prefix in ("[EVAL][SUMMARY] ", "[SUMMARY] "):
            if normalized.startswith(summary_prefix):
                payload = normalized[len(summary_prefix):]
                details = self._format_eval_summary(payload)
                self._set_eval_summary_text(details)
                return

    def _parse_eval_pairs(self, payload: str) -> dict[str, str]:
        return {
            key: value
            for key, value in re.findall(r"([a-zA-Z0-9_]+)=([^=]+?)(?=\s+[a-zA-Z0-9_]+=|$)", payload)
        }

    def _reset_eval_kpi_state(self) -> None:
        self._eval_result_headline = "P1 vs P2: —"
        self._eval_result_winrate_p1 = "P1 winrate: —"
        self._eval_result_winrate_p2 = "P2 winrate: —"
        self._eval_result_avg_vp_diff = "Avg VP diff (P1-P2): —"
        self._eval_result_turn_limit_rate = "Turn-limit rate: —"
        self._eval_result_quality_hint = "Качество серии: нет данных."
        self._reset_eval_live_state(emit=False)
        self.evalSetupChanged.emit()

    def _reset_eval_live_state(self, emit: bool = True) -> None:
        self._eval_live_games_done = 0
        self._eval_live_games_total = max(0, int(self._eval_games))
        self._eval_live_p1_wins = 0
        self._eval_live_p2_wins = 0
        self._eval_live_draws = 0
        self._eval_live_last_game_idx = 0
        if emit:
            self.evalSetupChanged.emit()

    def _set_eval_live_state(
        self,
        p1_wins: int,
        p2_wins: int,
        draws: int,
        total_games: int,
        *,
        emit: bool = True,
    ) -> None:
        self._eval_live_p1_wins = max(0, int(p1_wins))
        self._eval_live_p2_wins = max(0, int(p2_wins))
        self._eval_live_draws = max(0, int(draws))
        self._eval_live_games_done = self._eval_live_p1_wins + self._eval_live_p2_wins + self._eval_live_draws
        self._eval_live_games_total = max(int(total_games), self._eval_live_games_done, int(self._eval_games))
        self._eval_live_last_game_idx = max(self._eval_live_last_game_idx, self._eval_live_games_done)
        if emit:
            self.evalSetupChanged.emit()

    def _maybe_update_eval_live(self, line: str) -> None:
        normalized = line.strip()
        if "winner_side=" not in normalized or "Игра" not in normalized:
            return

        match = re.search(
            r"Игра\s+(?P<idx>\d+)\s*/\s*(?P<total>\d+):.*?\bwinner_side=(?P<winner>P1|P2|draw)\b",
            normalized,
        )
        if not match:
            return

        game_idx = int(match.group("idx"))
        total_games = int(match.group("total"))
        winner_side = str(match.group("winner"))

        if game_idx <= self._eval_live_last_game_idx:
            return
        if game_idx == 1 and self._eval_live_last_game_idx > 1:
            self._reset_eval_live_state(emit=False)

        if winner_side == "P1":
            self._eval_live_p1_wins += 1
        elif winner_side == "P2":
            self._eval_live_p2_wins += 1
        else:
            self._eval_live_draws += 1

        self._eval_live_games_done = self._eval_live_p1_wins + self._eval_live_p2_wins + self._eval_live_draws
        self._eval_live_games_total = max(total_games, self._eval_live_games_done, int(self._eval_games))
        self._eval_live_last_game_idx = game_idx
        self.evalSetupChanged.emit()

    def _format_eval_summary_v2(self, payload: str) -> str:
        pairs = self._parse_eval_pairs(payload)
        p1_wins = int(float(pairs.get("p1_wins", "0") or "0"))
        p2_wins = int(float(pairs.get("p2_wins", "0") or "0"))
        draws = int(float(pairs.get("draws", "0") or "0"))
        total_games = max(1, p1_wins + p2_wins + draws)

        wr_p1_all = float(pairs.get("winrate_p1_all", "0") or "0")
        wr_p2_all = float(pairs.get("winrate_p2_all", "0") or "0")
        wr_p1_dec = float(pairs.get("winrate_p1_decisive", "0") or "0")
        wr_p2_dec = float(pairs.get("winrate_p2_decisive", "0") or "0")
        avg_vp_diff = float(pairs.get("avg_vp_diff_p1_minus_p2", "0") or "0")
        avg_reward_learner = float(pairs.get("avg_reward_learner", "0") or "0")
        avg_hp_diff = float(pairs.get("avg_hp_diff_p1_minus_p2", "0") or "0")
        avg_kill_diff = float(pairs.get("avg_kill_diff_p1_minus_p2", "0") or "0")
        avg_ep_len = float(pairs.get("avg_ep_len", "0") or "0")
        turn_limit_count = int(float(pairs.get("turn_limit_count", "0") or "0"))
        turn_limit_rate = turn_limit_count / total_games

        if turn_limit_rate > 0.60:
            quality_hint = "Качество серии: много игр упёрлось в лимит ходов."
        elif turn_limit_rate > 0.35:
            quality_hint = "Качество серии: заметная доля игр дошла до лимита."
        else:
            quality_hint = "Качество серии: серия достаточно решающая."

        self._eval_result_headline = f"P1 win: {p1_wins}, P2 win: {p2_wins}, Draw: {draws}"
        self._eval_result_winrate_p1 = f"P1 winrate: {wr_p1_all:.1%} (решающие: {wr_p1_dec:.1%})"
        self._eval_result_winrate_p2 = f"P2 winrate: {wr_p2_all:.1%} (решающие: {wr_p2_dec:.1%})"
        self._eval_result_avg_vp_diff = f"Avg VP diff (P1-P2): {avg_vp_diff:+.3f}"
        self._eval_result_turn_limit_rate = f"Turn-limit rate: {turn_limit_rate:.1%} ({turn_limit_count}/{total_games})"
        self._eval_result_quality_hint = quality_hint
        self._set_eval_live_state(p1_wins, p2_wins, draws, total_games, emit=False)
        self.evalSetupChanged.emit()

        reason_text = pairs.get("end_reasons", "{}")
        try:
            reason_dict = ast.literal_eval(reason_text)
            reason_text = str(reason_dict) if isinstance(reason_dict, dict) else reason_text
        except (ValueError, SyntaxError):
            pass

        lines = ["Подробный результат оценки (P1 vs P2):"]
        lines.append(f"- Итог серии: P1 {p1_wins} • P2 {p2_wins} • Ничьи {draws}")
        lines.append(f"- Winrate P1/P2 (все): {wr_p1_all:.3f}/{wr_p2_all:.3f}")
        lines.append(f"- Winrate P1/P2 (решающие): {wr_p1_dec:.3f}/{wr_p2_dec:.3f}")
        lines.append(f"- Avg награда (learner): {avg_reward_learner:.3f}")
        lines.append(f"- Средний VP diff (P1-P2): {avg_vp_diff:.3f}")
        lines.append(f"- Avg HP diff (P1-P2): {avg_hp_diff:.3f}")
        lines.append(f"- Avg Kill diff (P1-P2): {avg_kill_diff:.3f}")
        lines.append(f"- Avg длина эпизода: {avg_ep_len:.3f}")
        lines.append(f"- Turn-limit: {turn_limit_count}/{total_games} ({turn_limit_rate:.3f})")
        lines.append(f"- Причины завершения: {reason_text}")
        lines.append("- Контекст: матч детерминированный, epsilon=0.")
        return "\n".join(lines)

    def _format_eval_summary(self, payload: str) -> str:
        pairs = self._parse_eval_pairs(payload)

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

        wins = int(float(pairs.get("wins", "0") or "0"))
        losses = int(float(pairs.get("losses", "0") or "0"))
        draws = int(float(pairs.get("draws", "0") or "0"))
        total_games = max(1, wins + losses + draws)
        turn_limit_count = 0
        try:
            reasons = ast.literal_eval(pairs.get("end_reasons", "{}"))
            if isinstance(reasons, dict):
                turn_limit_count = int(reasons.get("turn_limit", 0) or 0)
        except (ValueError, SyntaxError):
            pass
        turn_limit_rate = turn_limit_count / total_games
        self._eval_result_headline = f"P1 win: {wins}, P2 win: {losses}, Draw: {draws}"
        self._eval_result_winrate_p1 = f"P1 winrate all: {pairs.get('winrate_all', '?')}"
        self._eval_result_winrate_p2 = "P2 winrate all: —"
        self._eval_result_avg_vp_diff = f"Avg VP diff: {pairs.get('avg_vp_diff', '?')}"
        self._eval_result_turn_limit_rate = f"Turn-limit rate: {turn_limit_rate:.1%} ({turn_limit_count}/{total_games})"
        self._eval_result_quality_hint = "Качество серии: используется базовый summary."
        self._set_eval_live_state(wins, losses, draws, total_games, emit=False)
        self.evalSetupChanged.emit()

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
        base_dir = os.path.join(str(RUNTIME_STATE_DIR), "img")
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
        self._play_model_algo_key = str(algo or "").strip().lower()
        self._play_model_algo_label = f"Алгоритм: {self._format_algo_label(self._play_model_algo_key)}" if algo else "Алгоритм: —"
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
                    if algo in {"ppo", "dqn", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}:
                        return algo
                    if algo == "alphazero":
                        return ""
                    net_type = str(payload.get("net_type", "") or "").strip().lower()
                    if "ppo" in net_type:
                        return "ppo"
                    if "dueling" in net_type or "basic" in net_type:
                        return "dqn"
            except Exception:
                pass

        # 2) Фолбэк по имени файла/папки.
        joined = (str(pickle_path or "") + " " + str(checkpoint_path or "")).lower()
        if "gumbel_muzero" in joined or "gmz" in joined:
            return "gumbel_muzero"
        if "alphazero_tree" in joined:
            return "alphazero_tree"
        if "alphazero_proxy" in joined:
            return "alphazero_proxy"
        if "alphazero" in joined:
            return ""
        if "ppo-run-" in joined or "checkpoint_ep" in joined:
            return "ppo"
        if "actor_learner" in joined or re.search(r"model-\d+-\d+.*\.pth", joined):
            return "dqn"
        return ""

    def _format_algo_label(self, algo_key: str) -> str:
        key = str(algo_key or "").strip().lower()
        if key == "gumbel_muzero":
            return "GUMBEL_MUZERO"
        if key == "alphazero_tree":
            return "ALPHAZERO TREE"
        if key == "alphazero_proxy":
            return "ALPHAZERO PROXY"
        if key == "ppo":
            return "PPO"
        if key == "dqn":
            return "DQN"
        return key.upper() if key else "—"

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
            self._play_model_path = ""
            self._play_model_algo_key = ""
            self._play_agent_override_id = ""
            if initial:
                self._play_model_label = "Модель не найдена"
            else:
                self._play_model_label = "Последняя .pickle модель не найдена"
            self._play_model_algo_label = "Алгоритм: —"
            self._play_model_checkpoint_label = "Checkpoint: —"
            self._play_viewer_player_role_label = "Ты: —"
            self._play_viewer_model_role_label = "ИИ: —"
            self.playModelPathChanged.emit(self._play_model_path)
            self.playModelLabelChanged.emit(self._play_model_label)
            self.playModelMetaChanged.emit(self._play_model_algo_label)
            self.playViewerPlayerRoleLabelChanged.emit(self._play_viewer_player_role_label)
            self.playViewerModelRoleLabelChanged.emit(self._play_viewer_model_role_label)
            return False
        self._play_agent_override_id = ""
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

    def _pythonpath_with_core(self) -> str:
        gym_mod_path = os.path.join(self._repo_root, "core")
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
            candidate = os.path.join(str(RUNTIME_STATE_DIR), raw_path)
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
        run_id_from_payload = str(payload.get("run_id", "") or "").strip()
        self._metrics_run_id = run_id_from_payload or self._extract_run_id_from_path(json_path)
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
                json_path = os.path.join(str(ARTIFACTS_MODELS_DIR), f"data_{metrics_id}.json")
                if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                    self._metrics_label = f"Файл: {os.path.basename(latest_model)}"
                    self.metricsLabelChanged.emit(self._metrics_label)
                    return True

        # Резерв: если data_*.json ещё не создан, но DET-артефакты уже есть в artifacts/metrics.
        latest_det_json = os.path.join(str(ARTIFACTS_METRICS_DIR), "actor_det_eval_latest.json")
        if os.path.exists(latest_det_json):
            try:
                with open(latest_det_json, "r", encoding="utf-8", errors="replace") as handle:
                    det_payload = json.load(handle)
                run_id = str(det_payload.get("run_id", "") or "").strip()
                if run_id:
                    metric_map = {
                        "reward": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_reward_{run_id}.png"),
                        "loss": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_loss_{run_id}.png"),
                        "epLen": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_ep_len_{run_id}.png"),
                        "winrate": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_winrate_{run_id}.png"),
                        "avgvp": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_avg_vp_{run_id}.png"),
                        "hpdiff": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_hp_diff_{run_id}.png"),
                        "killdiff": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_kill_diff_{run_id}.png"),
                        "endreasons": os.path.join(str(ARTIFACTS_METRICS_DIR), f"det_endreasons_{run_id}.png"),
                    }
                    updated = {
                        key: (path if os.path.exists(path) else self._metrics_defaults[key])
                        for key, path in metric_map.items()
                    }
                    self._metrics_run_id = run_id
                    self._metrics_meta = {
                        "algo": str(det_payload.get("algo", "") or ""),
                        "mode": "actor_learner",
                        "learner_side": "",
                        "learner_faction": "",
                        "opponent_side": "",
                        "opponent_faction": "",
                        "opponent_algo": "",
                        "opponent_source": "",
                        "opponent_id": "",
                    }
                    self._set_metrics_files(updated)
                    self._refresh_metrics_summaries()
                    self._metrics_label = f"DET latest: run {run_id}"
                    self.metricsLabelChanged.emit(self._metrics_label)
                    return True
            except (OSError, json.JSONDecodeError, TypeError, ValueError):
                pass

        self._set_metrics_files(dict(self._metrics_defaults))
        self._metrics_label = "По умолчанию"
        self._metrics_run_id = ""
        self._metrics_meta = {}
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
        metrics_dir = str(ARTIFACTS_METRICS_DIR)
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
        results_path = str(RESULTS_PATH)
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
        logs_path = str(AGENT_TRAIN_LOG_PATH)
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
        logs_path = str(AGENT_TRAIN_LOG_PATH)
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
        path = os.path.join(str(ARTIFACTS_MODELS_DIR), "matchups.json")
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
        det_jsonl_path = str(ARTIFACTS_METRICS_DIR / f"actor_det_eval_{run_id}.jsonl") if run_id else ""
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
        self._load_latest_heuristic_metrics(run_id=str(run_id))

    def _load_latest_heuristic_metrics(self, run_id: str = "") -> None:
        preferred_run = str(run_id or "").strip()
        preferred_path = str(ARTIFACTS_METRICS_DIR / f"heur_metrics_{preferred_run}.json") if preferred_run else ""
        latest_path = str(ARTIFACTS_METRICS_DIR / "heur_metrics_latest.json")
        path = preferred_path if preferred_path and os.path.exists(preferred_path) else latest_path
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
            self._heuristic_metrics_text = f"Не удалось прочитать {path}."
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
            f"Источник: {os.path.basename(path)}",
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
        models_path = str(ARTIFACTS_MODELS_DIR)
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

        if latest_human_path and latest_legacy_path:
            return latest_human_path if latest_human_mtime >= latest_legacy_mtime else latest_legacy_path
        return latest_human_path or latest_legacy_path

    def _sync_metrics_with_model(self, model_path: str) -> bool:
        metrics_id = self._extract_metrics_id(model_path)
        if metrics_id:
            json_path = os.path.join(str(ARTIFACTS_MODELS_DIR), f"data_{metrics_id}.json")
            if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                self._metrics_label = f"Файл: {os.path.basename(json_path)}"
                self.metricsLabelChanged.emit(self._metrics_label)
                return True
        return self._select_latest_metrics()

    def _sync_metrics_with_agent(self, agent_id: str) -> bool:
        raw = str(agent_id or "").strip()
        match = re.search(r"_(\d{7})$", raw)
        if match:
            run_id = match.group(1)
            json_path = os.path.join(str(ARTIFACTS_MODELS_DIR), f"data_{run_id}.json")
            if os.path.exists(json_path) and self._load_metrics_from_json(json_path):
                self._metrics_label = f"Файл: {os.path.basename(json_path)}"
                self.metricsLabelChanged.emit(self._metrics_label)
                return True
        return self._select_latest_metrics()

    def _find_latest_registered_agent_id(self) -> str:
        records = self._collect_registered_agents_meta()
        if not records:
            return ""
        return str(records[0].get("agent_id", "")).strip()

    def _apply_latest_play_selection(self, *, initial: bool, emit_status: bool) -> bool:
        selected_pickle = self._select_latest_play_model(initial=initial)
        latest_agent_id = self._find_latest_registered_agent_id()
        if latest_agent_id:
            self._play_agent_override_id = latest_agent_id
            agent_algo = self._find_agent_algo_by_id(latest_agent_id)
            self._play_model_algo_key = str(agent_algo or "").strip().lower()
            if not selected_pickle:
                self._play_model_label = f"Последний agent: {latest_agent_id}"
                self.playModelLabelChanged.emit(self._play_model_label)
            self._play_model_algo_label = (
                f"Алгоритм: {self._format_algo_label(self._play_model_algo_key)}"
                if agent_algo in {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero"}
                else "Алгоритм: —"
            )
            self._play_model_checkpoint_label = f"Agent: {latest_agent_id}"
            self.playModelMetaChanged.emit(self._play_model_algo_label)
            self._sync_play_role_labels_with_agent(latest_agent_id)
            if selected_pickle and self._play_model_path:
                self._sync_metrics_with_model(self._play_model_path)
            else:
                self._sync_metrics_with_agent(latest_agent_id)
            if emit_status:
                if selected_pickle:
                    self._emit_status(
                        "Выбрана последняя сохранённая модель (для игры применится последний agent)."
                    )
                else:
                    self._emit_status("Для игры выбран последний agent из registry.")
            return True

        self._play_agent_override_id = ""
        self._play_model_algo_key = ""
        if selected_pickle:
            if self._play_model_path:
                self._sync_metrics_with_model(self._play_model_path)
            if emit_status:
                self._emit_status("Выбрана последняя сохранённая модель.")
            return True
        if emit_status:
            if self._select_latest_metrics():
                self._emit_status(
                    "Последняя .pickle модель не найдена, но метрики последнего прогона загружены."
                )
            else:
                self._emit_status(
                    "Сохранённые модели/агенты не найдены. "
                    "Что делать: запустите обучение или выберите модель вручную."
                )
        return False

    def _find_agent_algo_by_id(self, agent_id: str) -> str:
        target = str(agent_id or "").strip()
        if not target:
            return ""
        for rec in self._collect_registered_agents_meta():
            if str(rec.get("agent_id", "")).strip() == target:
                return str(rec.get("algo", "")).strip().lower()
        return ""

    def _sync_play_role_labels_with_agent(self, agent_id: str) -> None:
        player_label, model_label = self._infer_viewer_role_labels_from_agent_id(agent_id)
        self._play_viewer_player_role_label = player_label
        self._play_viewer_model_role_label = model_label
        self.playViewerPlayerRoleLabelChanged.emit(player_label)
        self.playViewerModelRoleLabelChanged.emit(model_label)

    def _find_latest_checkpoint_file(self) -> Optional[str]:
        models_path = str(ARTIFACTS_MODELS_DIR)
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
        models_path = str(ARTIFACTS_MODELS_DIR)
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

        models_path = str(ARTIFACTS_MODELS_DIR)
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
        models_path = str(ARTIFACTS_MODELS_DIR)
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
        rw, mw = self._template_weapons_for_unit(unit.name)
        entry = RosterEntry(
            name=unit.name,
            count=unit.default_count,
            instance_id=str(self._instance_counter),
            ranged_weapon=rw,
            melee_weapon=mw,
        )
        self._instance_counter += 1
        return entry

    def _refresh_models(self) -> None:
        for entry in self._player_roster:
            self._normalize_entry_weapons(entry)
        for entry in self._model_roster:
            self._normalize_entry_weapons(entry)
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
        self._normalize_roster_preview_target()
        self._rebuild_roster_weapons_preview()

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
        self.rosterOverviewChanged.emit()
        self._emit_train_setup_summary_changed()

    def _weapon_battlefield_kind(self, unit_name: str, weapon_name: str) -> str:
        army = str(self._unit_faction_by_name.get(str(unit_name).strip(), "") or "").strip().lower()
        wn = str(weapon_name or "").strip()
        if not wn:
            return "unknown"
        typ = self._weapon_type_by_army_name.get((army, wn.lower()), "")
        if not typ:
            typ = self._weapon_type_by_army_name.get((army, wn), "")
        typ_l = str(typ or "").strip().lower()
        if typ_l == "melee":
            return "melee"
        if typ_l == "ranged":
            return "ranged"
        return "unknown"

    def _weapon_options_for_unit(self, unit_name: str) -> tuple[list[str], list[str], list[str]]:
        melee: list[str] = []
        ranged: list[str] = []
        unknown: list[str] = []
        uname = str(unit_name or "").strip()
        for w in self._unit_weapons_by_name.get(uname, []):
            kind = self._weapon_battlefield_kind(uname, w)
            if kind == "melee":
                melee.append(w)
            elif kind == "ranged":
                ranged.append(w)
            else:
                unknown.append(w)
        return ranged, melee, unknown

    def _default_weapons_for_unit(self, unit_name: str) -> tuple[str, str]:
        ranged, melee, _unknown = self._weapon_options_for_unit(unit_name)
        rw = ranged[0] if ranged else ""
        mw = melee[0] if melee else ""
        return rw, mw

    def _template_weapons_for_unit(self, unit_name: str) -> tuple[str, str]:
        name = str(unit_name or "").strip()
        if not name:
            return "", ""
        tpl = self._roster_template_weapons_by_unit.get(name)
        if tpl is None:
            rw, mw = self._default_weapons_for_unit(name)
            self._roster_template_weapons_by_unit[name] = (rw, mw)
            return rw, mw
        return str(tpl[0] or ""), str(tpl[1] or "")

    def _normalize_entry_weapons(self, entry: RosterEntry) -> None:
        entry.ranged_weapon = self._normalize_selected_weapon(entry.name, entry.ranged_weapon, "ranged")
        entry.melee_weapon = self._normalize_selected_weapon(entry.name, entry.melee_weapon, "melee")
        default_r, default_m = self._default_weapons_for_unit(entry.name)
        if not entry.ranged_weapon:
            entry.ranged_weapon = default_r
        if not entry.melee_weapon:
            entry.melee_weapon = default_m

    def _normalize_selected_weapon(self, unit_name: str, weapon_name: str, expected_kind: str) -> str:
        selected = str(weapon_name or "").strip()
        if not selected:
            return ""
        kind = self._weapon_battlefield_kind(unit_name, selected)
        if kind == expected_kind:
            return selected
        return ""

    def _get_selected_roster_entry(self) -> Optional[RosterEntry]:
        side = str(self._roster_preview_side or "").strip().upper()
        idx = int(self._roster_preview_roster_index)
        if idx < 0:
            return None
        if side == "P1" and idx < len(self._player_roster):
            return self._player_roster[idx]
        if side == "P2" and idx < len(self._model_roster):
            return self._model_roster[idx]
        return None

    def _roster_for_side(self, side: str) -> list[RosterEntry]:
        normalized = str(side or "").strip().upper()
        if normalized == "P1":
            return self._player_roster
        if normalized == "P2":
            return self._model_roster
        return []

    def _format_keyword_label(self, keyword: str) -> str:
        raw = str(keyword or "").strip().replace("_", " ")
        if not raw:
            return "UNIT"
        return raw.upper()

    def _unit_role_label(self, unit_name: str) -> str:
        keys = self._unit_keywords_by_name.get(str(unit_name).strip(), [])
        upper_keys = [str(k).upper() for k in keys]
        if "CHARACTER" in upper_keys:
            return "CHARACTER"
        if "BATTLELINE" in upper_keys:
            return "BATTLELINE"
        if upper_keys:
            return self._format_keyword_label(upper_keys[0])
        return "UNIT"

    def _fmt_core_movement(self, v: object) -> str:
        if v is None:
            return "—"
        try:
            if isinstance(v, (int, float)):
                return f'{int(v)}"'
        except (TypeError, ValueError):
            pass
        s = str(v).strip()
        return s if s else "—"

    def _fmt_core_plus_stat(self, v: object) -> str:
        if v is None:
            return "—"
        try:
            if isinstance(v, (int, float)):
                return f"{int(v)}+"
        except (TypeError, ValueError):
            pass
        s = str(v).strip()
        return s if s else "—"

    def _fmt_core_plain_stat(self, v: object) -> str:
        if v is None:
            return "—"
        try:
            if isinstance(v, (int, float)):
                return str(int(v))
        except (TypeError, ValueError):
            pass
        s = str(v).strip()
        return s if s else "—"

    def _core_stat_display_values(self, unit_name: str) -> list[str]:
        core = self._unit_core_by_name.get(str(unit_name).strip(), {})
        if not core:
            return ["—", "—", "—", "—", "—", "—"]
        return [
            self._fmt_core_movement(core.get("Movement")),
            self._fmt_core_plain_stat(core.get("T")),
            self._fmt_core_plus_stat(core.get("Sv")),
            self._fmt_core_plain_stat(core.get("W")),
            self._fmt_core_plus_stat(core.get("Ld")),
            self._fmt_core_plain_stat(core.get("OC")),
        ]

    def _weapon_data(self, unit_name: str, weapon_name: str) -> dict:
        army = str(self._unit_faction_by_name.get(str(unit_name).strip(), "") or "").strip().lower()
        wn = str(weapon_name or "").strip().lower()
        if not wn:
            return {}
        return self._weapon_data_by_army_name.get((army, wn), {})

    def _weapon_statline(self, unit_name: str, weapon_name: str) -> str:
        data = self._weapon_data(unit_name, weapon_name)
        if not data:
            return "—"
        if str(data.get("Type", "")).strip().lower() == "melee":
            skill = f"WS{data.get('WS', '—')}+"
        else:
            skill = f"BS{data.get('BS', '—')}+"
        rng = f"{data.get('Range', '—')}\""
        attacks = f"A{data.get('A', '—')}"
        strength = f"S{data.get('S', '—')}"
        ap = f"AP{data.get('AP', '—')}"
        dmg = f"D{data.get('Damage', '—')}"
        return f"{rng} • {attacks} • {skill} • {strength} • {ap} • {dmg}"

    def _weapon_stat_values(self, unit_name: str, weapon_name: str) -> list[str]:
        data = self._weapon_data(unit_name, weapon_name)
        if not data:
            return ["—", "—", "—", "—", "—", "—"]
        if str(data.get("Type", "")).strip().lower() == "melee":
            skill = f"{data.get('WS', '—')}+"
        else:
            skill = f"{data.get('BS', '—')}+"
        return [
            f"{data.get('Range', '—')}\"",
            str(data.get("A", "—")),
            skill,
            str(data.get("S", "—")),
            str(data.get("AP", "—")),
            str(data.get("Damage", "—")),
        ]

    def _format_ability_badge(self, key: str, value: object) -> str:
        label = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(key or "").strip()).upper()
        if isinstance(value, bool):
            return label if value else ""
        val = str(value).strip()
        if not val:
            return label
        return f"{label} {val}"

    def _weapon_ability_badges(self, unit_name: str, weapon_name: str) -> list[str]:
        data = self._weapon_data(unit_name, weapon_name)
        abilities = data.get("Abilities", {})
        if not isinstance(abilities, dict):
            return []
        out: list[str] = []
        for k, v in abilities.items():
            badge = self._format_ability_badge(k, v)
            if badge:
                out.append(badge)
        return out

    def _entry_points(self, entry: RosterEntry) -> int:
        return int(self._unit_points_by_name.get(str(entry.name).strip(), 0) or 0)

    def _roster_points_total(self, side: str) -> int:
        roster = self._roster_for_side(side)
        total = 0
        for entry in roster:
            total += self._entry_points(entry)
        return total

    def _unit_wounds_per_model(self, unit_name: str) -> int:
        """Раны на одну модель с даташита (поле W в UnitData)."""
        core = self._unit_core_by_name.get(str(unit_name).strip(), {})
        w = core.get("W")
        if w is None:
            return 0
        try:
            if isinstance(w, (int, float)) and not isinstance(w, bool):
                return max(0, int(w))
        except (TypeError, ValueError):
            pass
        try:
            s = str(w).strip().replace(",", ".")
            if not s:
                return 0
            return max(0, int(float(s)))
        except (TypeError, ValueError):
            return 0

    def _roster_kpi_metrics(self, side: str) -> tuple[int, str, int, int]:
        """(unit_count, avg_ranged_range_display, total_hp_pool, total_models)."""
        roster = self._roster_for_side(side)
        if not roster:
            return 0, "—", 0, 0
        ranges: list[float] = []
        total_hp = 0
        total_models = 0
        for e in roster:
            wd = self._weapon_data(e.name, e.ranged_weapon)
            if wd and isinstance(wd.get("Range"), (int, float)):
                ranges.append(float(wd["Range"]))
            cnt = max(0, int(e.count))
            total_models += cnt
            total_hp += self._unit_wounds_per_model(e.name) * cnt
        avg_range = f"{(sum(ranges) / len(ranges)):.1f}\"" if ranges else "—"
        return len(roster), avg_range, total_hp, total_models

    def _roster_kpi_columns(self, side: str) -> list[dict]:
        n, avg_range, total_hp, total_models = self._roster_kpi_metrics(side)
        return [
            {"h": "UNITS", "v": str(n)},
            {"h": "MODELS", "v": str(total_models)},
            {"h": "HP", "v": str(total_hp)},
            {"h": "AVG.RNG", "v": avg_range},
        ]

    def _build_roster_kpi(self, side: str) -> str:
        n, avg_range, total_hp, total_models = self._roster_kpi_metrics(side)
        if n == 0:
            return "юнитов: 0 • модели: 0 • раны (всего): 0 • ср.дальнобой: —"
        return (
            f"юнитов: {n} • модели: {total_models} • раны (всего): {total_hp} • "
            f"ср.дальнобой: {avg_range}"
        )

    def _build_roster_doctrine(self, side: str) -> str:
        roster = self._roster_for_side(side)
        if not roster:
            return "Доктрина не определена"
        avg_range_val = 0.0
        ranges: list[float] = []
        characters = 0
        for e in roster:
            if self._unit_role_label(e.name) == "CHARACTER":
                characters += 1
            wd = self._weapon_data(e.name, e.ranged_weapon)
            if wd and isinstance(wd.get("Range"), (int, float)):
                ranges.append(float(wd["Range"]))
        if ranges:
            avg_range_val = sum(ranges) / len(ranges)
        if avg_range_val <= 12 and characters > 0:
            return "Ударная группа: ближний рубеж + командное ядро"
        if avg_range_val <= 12:
            return "Штурмовой контур: агрессивное сближение"
        if characters > 0:
            return "Линейный огонь под командованием"
        return "Линейная доктрина: удержание дистанции"

    def _build_roster_composition_delta(self) -> str:
        p1_units = len(self._player_roster)
        p2_units = len(self._model_roster)
        p1_models = sum(max(0, int(e.count)) for e in self._player_roster)
        p2_models = sum(max(0, int(e.count)) for e in self._model_roster)
        p1_pts = self._roster_points_total("P1")
        p2_pts = self._roster_points_total("P2")
        du = p1_units - p2_units
        dm = p1_models - p2_models
        return f"Δ состав: юниты {du:+d}, модели {dm:+d}, pts {p1_pts - p2_pts:+d}"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_role(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return self._unit_role_label(roster[int(index)].name)
        return "UNIT"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_models(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return str(max(0, int(roster[int(index)].count)))
        return "0"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_points(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return "—"
        entry = roster[int(index)]
        pts = int(self._unit_points_by_name.get(str(entry.name).strip(), 0) or 0)
        return f"{pts} pts" if pts > 0 else "— pts"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_abilities(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return "—"
        entry = roster[int(index)]
        abilities = self._unit_abilities_by_name.get(str(entry.name).strip(), [])
        if not abilities:
            return "—"
        return " • ".join(abilities)

    @QtCore.Slot(str, int, result=str)
    def roster_entry_ranged_weapon(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return str(roster[int(index)].ranged_weapon or "—")
        return "—"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_melee_weapon(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return str(roster[int(index)].melee_weapon or "—")
        return "—"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_display_name(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return str(roster[int(index)].name)
        return ""

    @QtCore.Slot(str, int, result=str)
    def roster_entry_count_label(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if 0 <= int(index) < len(roster):
            return f"[x{max(0, int(roster[int(index)].count))}]"
        return "[x0]"

    @QtCore.Slot(str, int, result=str)
    def roster_entry_pts_badge(self, side: str, index: int) -> str:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return "—"
        pts = self._entry_points(roster[int(index)])
        return f"{pts} PTS" if pts > 0 else "—"

    @QtCore.Slot(str, int, result="QStringList")
    def roster_entry_core_stat_values(self, side: str, index: int) -> list[str]:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return ["—", "—", "—", "—", "—", "—"]
        return self._core_stat_display_values(roster[int(index)].name)

    @QtCore.Slot(str, int, result="QStringList")
    def roster_entry_keyword_tags(self, side: str, index: int) -> list[str]:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return []
        name = str(roster[int(index)].name).strip()
        return list(self._unit_keywords_by_name.get(name, []))

    @QtCore.Slot(str, int, result="QStringList")
    def roster_entry_ability_lines(self, side: str, index: int) -> list[str]:
        roster = self._roster_for_side(side)
        if not (0 <= int(index) < len(roster)):
            return []
        name = str(roster[int(index)].name).strip()
        return list(self._unit_abilities_by_name.get(name, []))

    @QtCore.Slot(str, int, result=bool)
    def roster_entry_active(self, side: str, index: int) -> bool:
        return False

    def _rebuild_roster_weapons_preview(self) -> None:
        idx = int(self._roster_available_preview_index)
        if not (0 <= idx < len(self._available_units)):
            self._roster_preview_ranged = []
            self._roster_preview_melee = []
            self._roster_preview_unknown = []
            self.rosterWeaponsPreviewChanged.emit()
            return

        unit_name = str(self._available_units[idx].name).strip()
        ranged, melee, unknown = self._weapon_options_for_unit(unit_name)
        rw, mw = self._template_weapons_for_unit(unit_name)
        rw = self._normalize_selected_weapon(unit_name, rw, "ranged")
        mw = self._normalize_selected_weapon(unit_name, mw, "melee")
        if not rw and ranged:
            rw = ranged[0]
        if not mw and melee:
            mw = melee[0]
        self._roster_template_weapons_by_unit[unit_name] = (rw, mw)

        self._roster_preview_ranged = ranged
        self._roster_preview_melee = melee
        self._roster_preview_unknown = unknown
        self.rosterWeaponsPreviewChanged.emit()

    def _normalize_roster_preview_target(self) -> None:
        if not self._available_units:
            self._roster_available_preview_index = -1
        elif self._roster_available_preview_index < 0 or self._roster_available_preview_index >= len(self._available_units):
            self._roster_available_preview_index = 0

    @QtCore.Slot(str, int)
    def set_roster_weapon_target(self, side: str, index: int) -> None:
        # compatibility no-op: weapon target is now selected via available unit list
        self._rebuild_roster_weapons_preview()

    @QtCore.Slot(str)
    def set_selected_roster_ranged_weapon(self, weapon_name: str) -> None:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return
        normalized = self._normalize_selected_weapon(unit_name, weapon_name, "ranged")
        rw, mw = self._template_weapons_for_unit(unit_name)
        if normalized == rw:
            return
        self._roster_template_weapons_by_unit[unit_name] = (normalized, mw)
        self._rebuild_roster_weapons_preview()
        self.rosterOverviewChanged.emit()
        self._emit_log(
            f"[GUI][ROSTER] {self.rosterWeaponsPreviewTarget} {unit_name}: выбран ДБ '{normalized or '—'}'.",
            level="INFO",
        )

    @QtCore.Slot(str)
    def set_selected_roster_melee_weapon(self, weapon_name: str) -> None:
        unit_name = self.rosterWeaponsPreviewUnitName
        if unit_name == "—":
            return
        normalized = self._normalize_selected_weapon(unit_name, weapon_name, "melee")
        rw, mw = self._template_weapons_for_unit(unit_name)
        if normalized == mw:
            return
        self._roster_template_weapons_by_unit[unit_name] = (rw, normalized)
        self._rebuild_roster_weapons_preview()
        self.rosterOverviewChanged.emit()
        self._emit_log(
            f"[GUI][ROSTER] {self.rosterWeaponsPreviewTarget} {unit_name}: выбран ББ '{normalized or '—'}'.",
            level="INFO",
        )

    @QtCore.Slot(int)
    def set_roster_available_preview_index(self, index: int) -> None:
        self._roster_available_preview_index = int(index)
        self._normalize_roster_preview_target()
        self._rebuild_roster_weapons_preview()

    def _load_available_units(self) -> None:
        unit_path = os.path.join(self._repo_root, "core", "engine", "unitData.json")
        if not os.path.exists(unit_path):
            self._emit_log("[GUI] unitData.json не найден, список юнитов пуст.", level="WARN")
            return
        with open(unit_path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        self._available_units.clear()
        self._unit_faction_by_name.clear()
        self._unit_weapons_by_name.clear()
        self._unit_keywords_by_name.clear()
        self._unit_models_by_name.clear()
        self._unit_abilities_by_name.clear()
        self._unit_points_by_name.clear()
        self._unit_core_by_name.clear()
        self._weapon_type_by_army_name.clear()
        self._weapon_data_by_army_name.clear()

        units = payload.get("UnitData", [])
        for unit in units:
            name = unit.get("Name")
            faction = unit.get("Army")
            if not name or not faction:
                continue
            name_s = str(name).strip()
            fact_s = str(faction).strip()
            self._unit_faction_by_name[name_s] = fact_s
            self._unit_core_by_name[name_s] = {
                "Movement": unit.get("Movement"),
                "T": unit.get("T"),
                "Sv": unit.get("Sv"),
                "W": unit.get("W"),
                "Ld": unit.get("Ld"),
                "OC": unit.get("OC"),
            }
            raw_weapons = unit.get("Weapons") or []
            self._unit_weapons_by_name[name_s] = [str(x).strip() for x in raw_weapons if str(x).strip()]
            self._unit_keywords_by_name[name_s] = [str(x).strip() for x in (unit.get("KEYWORDS") or []) if str(x).strip()]
            self._unit_abilities_by_name[name_s] = [str(x).strip() for x in (unit.get("Abilities") or []) if str(x).strip()]
            try:
                self._unit_models_by_name[name_s] = int(unit.get("#OfModels", 0) or 0)
            except (TypeError, ValueError):
                self._unit_models_by_name[name_s] = 0
            raw_pts = unit.get("Points", unit.get("Pts", 0))
            try:
                pts = int(raw_pts or 0)
            except (TypeError, ValueError):
                pts = 0
            self._unit_points_by_name[name_s] = pts

        # Явные цены для текущего ростера Necrons (если в UnitData нет Points/Pts).
        fallback_pts = {
            "Necron Warriors": 90,
            "Royal Warden": 50,
            "Canoptek Scarab Swarms": 40,
        }
        for uname, pts in fallback_pts.items():
            if int(self._unit_points_by_name.get(uname, 0) or 0) <= 0:
                self._unit_points_by_name[uname] = int(pts)

        for w in payload.get("WeaponData", []):
            army = str(w.get("Army", "") or "").strip().lower()
            nm = str(w.get("Name", "") or "").strip()
            typ = str(w.get("Type", "") or "").strip()
            if nm:
                self._weapon_type_by_army_name[(army, nm.lower())] = typ
                self._weapon_data_by_army_name[(army, nm.lower())] = dict(w)

        for unit in units:
            name = unit.get("Name")
            faction = unit.get("Army")
            if not name or not faction:
                continue
            if str(faction).lower() != "necrons":
                continue
            default_count = unit.get("#OfModels", 1)
            self._available_units.append(UnitInfo(name=name, faction=faction, default_count=default_count))

        self.set_roster_available_preview_index(0 if self._available_units else -1)
        self.rosterOverviewChanged.emit()

    def _load_rosters_from_file(self) -> None:
        units_path = str(UNITS_PATH)
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
                # Маппим секции файла runtime/state/units.txt в P1/P2 в зависимости от learner_side.
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
        ranged_weapon = parts[3] if len(parts) >= 4 else ""
        melee_weapon = parts[4] if len(parts) >= 5 else ""
        if instance_id.isdigit():
            self._instance_counter = max(self._instance_counter, int(instance_id) + 1)
        return RosterEntry(
            name=name,
            count=count,
            instance_id=instance_id,
            ranged_weapon=ranged_weapon,
            melee_weapon=melee_weapon,
        )

    def _persist_rosters(self) -> None:
        units_path = str(UNITS_PATH)
        # В файле runtime/state/units.txt:
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
            lines.append(
                f"{entry.name}|{entry.count}|{entry.instance_id}|"
                f"{entry.ranged_weapon}|{entry.melee_weapon}"
            )
        lines.append("Model Units")
        for entry in model_roster:
            lines.append(
                f"{entry.name}|{entry.count}|{entry.instance_id}|"
                f"{entry.ranged_weapon}|{entry.melee_weapon}"
            )
        os.makedirs(os.path.dirname(units_path), exist_ok=True)
        with open(units_path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))

    def _clear_cache_files(self) -> None:
        models_path = str(ARTIFACTS_MODELS_DIR)
        metrics_path = str(ARTIFACTS_METRICS_DIR)
        gui_img_path = os.path.join(str(RUNTIME_STATE_DIR), "img")
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
        clear_eval: bool = True,
    ) -> None:
        logs_dir = str(AGENT_TRAIN_LOG_PATH.parent)
        os.makedirs(logs_dir, exist_ok=True)
        if clear_train:
            train_log_path = str(AGENT_TRAIN_LOG_PATH)
            with open(train_log_path, "w", encoding="utf-8"):
                pass
        if clear_play:
            play_log_path = str(AGENT_PLAY_LOG_PATH)
            with open(play_log_path, "w", encoding="utf-8"):
                pass
        if clear_eval:
            eval_log_path = str(AGENT_EVAL_LOG_PATH)
            with open(eval_log_path, "w", encoding="utf-8"):
                pass
        if clear_results:
            results_path = str(RESULTS_PATH)
            with open(results_path, "w", encoding="utf-8"):
                pass


def main() -> int:
    global _GUI_CONTROLLER_REF
    if sys.platform.startswith("win"):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("40kAI.GUI")

    # Use a non-native Controls style so Button background/content customization works.
    if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Fusion"
    QQuickStyle.setStyle(os.environ["QT_QUICK_CONTROLS_STYLE"])

    app = QtGui.QGuiApplication(sys.argv)
    theme_flat = None
    try:
        theme_flat = load_tokens_flat_for_qml()
    except (ThemeTokenError, OSError, ValueError) as exc:
        print(f"[40kAI] theme/tokens.json not applied to launcher: {exc}", flush=True)

    def _qc(key: str, fallback: str) -> QtGui.QColor:
        if theme_flat and key in theme_flat:
            return QtGui.QColor(theme_flat[key])
        return QtGui.QColor(fallback)

    app_palette = QtGui.QPalette()
    app_palette.setColor(QtGui.QPalette.Window, _qc("bgBase", "#0F172A"))
    app_palette.setColor(QtGui.QPalette.Base, _qc("bgSurface", "#131b2d"))
    app_palette.setColor(QtGui.QPalette.AlternateBase, _qc("bgElevated", "#1E293B"))
    app_palette.setColor(QtGui.QPalette.Button, _qc("bgElevated", "#1E293B"))
    app_palette.setColor(QtGui.QPalette.ButtonText, _qc("textPrimary", "#d7dde7"))
    app_palette.setColor(QtGui.QPalette.Text, _qc("textPrimary", "#d7dde7"))
    app_palette.setColor(QtGui.QPalette.WindowText, _qc("textPrimary", "#d7dde7"))
    app_palette.setColor(QtGui.QPalette.Highlight, _qc("accentP1", "#2f6ed8"))
    app_palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor("#ffffff"))
    app_palette.setColor(QtGui.QPalette.PlaceholderText, _qc("textSecondary", "#98a4b8"))
    app.setPalette(app_palette)

    gui_dir = Path(getattr(sys, "_MEIPASS", os.path.dirname(__file__)))
    icon_path = os.path.join(gui_dir, "assets", "40kai_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    engine = QtQml.QQmlApplicationEngine()

    _GUI_CONTROLLER_REF = GUIController()
    try:
        ownership = QtQml.QQmlEngine.CppOwnership
    except AttributeError:
        ownership = QtQml.QQmlEngine.ObjectOwnership.CppOwnership
    QtQml.QQmlEngine.setObjectOwnership(_GUI_CONTROLLER_REF, ownership)
    # Keep explicit strong references on app/engine side so QML context
    # never sees a collected/null controller object.
    app._controller_ref = _GUI_CONTROLLER_REF
    engine._controller_ref = _GUI_CONTROLLER_REF
    engine.rootContext().setContextProperty("controller", _GUI_CONTROLLER_REF)
    if theme_flat is not None:
        engine.rootContext().setContextProperty("themeTokens", theme_flat)

    qml_path = os.path.join(gui_dir, "qml", "Main.qml")
    engine.load(QtCore.QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        return 1

    root = engine.rootObjects()[0]

    # Один проход после входа в event loop — подтягивает отложенную компоновку/редрав Quick на Qt 6 + RHI.
    def _kick_first_frame_paint() -> None:
        try:
            root.update()
        except Exception:
            pass

    QtCore.QTimer.singleShot(0, _kick_first_frame_paint)

    if os.path.exists(icon_path):
        if hasattr(root, "setIcon"):
            root.setIcon(QIcon(icon_path))

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
