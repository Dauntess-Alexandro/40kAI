"""Журнал тренировки (TrainLogView): раскраска AZ-логов, фильтры, автоскролл.

Контракт: компонент существует, подключён в Main.qml вместо plain-TextArea,
мёртвая ветка GATE не логируется/не раскрашивается (удалена из train.py).
Поведение: appendLine классифицирует строки, голый прогресс ep=N/M скрыт,
фильтры считают видимые строки, WARN виден при любом фильтре.
"""
import os
import unittest
from pathlib import Path

QML_PATH = Path("app/gui_qt/qml/components/TrainLogView.qml")
MAIN_QML_PATH = Path("app/gui_qt/qml/Main.qml")


class TestTrainLogViewContract(unittest.TestCase):
    def setUp(self) -> None:
        self.assertTrue(
            QML_PATH.exists(),
            f"Нет компонента журнала: {QML_PATH}. Что делать: создать TrainLogView.qml.",
        )
        self.source = QML_PATH.read_text(encoding="utf-8")

    def test_component_api(self):
        # Публичный API: добавление строки, очистка, фильтр, счётчики.
        self.assertIn("function appendLine(", self.source)
        self.assertIn("function clearAll(", self.source)
        self.assertIn("property string activeFilter", self.source)
        self.assertIn("property int lineCount", self.source)
        self.assertIn("property int visibleCount", self.source)

    def test_uses_listview_not_textarea(self):
        # Красивый журнал = ListView + модель; TextArea.text += тормозит на длинных тренировках.
        self.assertIn("ListView", self.source)
        self.assertNotIn("TextArea {", self.source)

    def test_no_gate_branch(self):
        # Ветка AZ GATE удалена из train.py — журнал её не знает.
        self.assertNotIn("GATE", self.source)

    def test_marker_vocabulary_classified(self):
        # Словарь всех алгоритмов: AZ/DQN/PPO/GMZ/TRAIN/LEAGUE/TRACE + подгруппы.
        for token in (
            "AZ|DQN|PPO|GMZ|TRAIN|LEAGUE",
            "ACTOR",
            "ENV_WORKER",
            "REMOTE_CLIENT",
            "INF_SERVER",
            "LOCAL_TRANSPORT",
            "[TRACE]",
            "[ALERT]",
            "[WARN]",
        ):
            self.assertIn(token, self.source, f"Токен {token} не классифицируется")

    def test_autoscroll_follow(self):
        # Пауза автоскролла при ручном скролле + плашка «N новых».
        self.assertIn("atYEnd", self.source)
        self.assertIn("hiddenNewCount", self.source)

    def test_main_qml_wiring(self):
        main_src = MAIN_QML_PATH.read_text(encoding="utf-8")
        self.assertIn("TrainLogView", main_src)
        self.assertIn("trainLog.appendLine(message)", main_src)
        self.assertNotIn("logArea.text +=", main_src)


class TestTrainEpLineContract(unittest.TestCase):
    """Богатая строка эпизода [TRAIN][EP] должна быть во всех путях, не только в sync-DQN.

    В dist/actor-learner режиме раньше печатался только служебный ep=N/M (журнал его
    скрывает как дубль прогресс-бара) — эпизоды пропадали из журнала.
    """

    def test_train_ep_emitted_in_all_loops(self):
        train_src = Path("train.py").read_text(encoding="utf-8")
        # DQN/PPO sync + actor-learner DQN/PPO/AZ/GMZ через log_train_episode_line.
        self.assertGreaterEqual(train_src.count("log_train_episode_line("), 6)

    def test_gui_explains_learner_queue_lag(self):
        # Полоски сбора полные, а верхний бар идёт по обработанным эпизодам —
        # GUI обязан объяснить разрыв текстом фазы.
        gui_src = Path("app/gui_qt/main.py").read_text(encoding="utf-8")
        self.assertIn("обучение разбирает очередь", gui_src)


class TestTrainLogViewBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtQml import QQmlComponent, QQmlEngine

        cls.app = QGuiApplication.instance() or QGuiApplication([])
        cls.engine = QQmlEngine()
        cls.component = QQmlComponent(cls.engine, QUrl.fromLocalFile(str(QML_PATH.resolve())))
        if cls.component.isError():
            raise AssertionError(
                "TrainLogView.qml не компилируется: "
                + "; ".join(e.toString() for e in cls.component.errors())
            )

    def _new(self):
        obj = self.component.create()
        self.assertIsNotNone(obj, "create() вернул None")
        self.addCleanup(obj.deleteLater)
        return obj

    @staticmethod
    def _append(obj, line: str) -> None:
        from PySide6.QtCore import Q_ARG, QMetaObject, Qt

        QMetaObject.invokeMethod(
            obj, "appendLine", Qt.ConnectionType.DirectConnection, Q_ARG("QVariant", line)
        )

    def test_append_counts_and_bare_progress_skipped(self):
        v = self._new()
        self._append(v, "[AZ][ACTOR] actor=0 move=5 mcts_mode=tree")
        self._append(v, "ep=5/300")  # служебный дубль для прогресс-бара — в журнал не попадает
        self._append(v, "[TRAIN][EP] ep=5/300 algo=az actor=4 result=draw end_reason=turn_limit vp_diff=0 ep_reward=0.0000 turns=10")
        self.assertEqual(v.property("lineCount"), 2)
        self.assertEqual(v.property("visibleCount"), 2)

    def test_warn_filter_shows_only_warnings(self):
        v = self._new()
        self._append(v, "[AZ][ACTOR] actor=1 move=15 mcts_mode=tree")
        self._append(v, "[AZ][DIST][WARN] не удалось записать stop.flag")
        v.setProperty("activeFilter", "warn")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_warn_visible_under_any_filter(self):
        v = self._new()
        self._append(v, "[AZ][UPDATE] step=10 policy_version=2 loss=0.1 policy_loss=0.05 value_loss=0.05 replay=40")
        self._append(v, "[AZ][RESUME][WARN] arch mismatch")
        v.setProperty("activeFilter", "dist")
        # WARN не прячем никаким фильтром.
        self.assertEqual(v.property("visibleCount"), 1)

    def test_dist_filter_groups_remote_markers(self):
        v = self._new()
        self._append(v, "[AZ][DIST][SINK] pushed=12 stale_drop=0%")
        self._append(v, "[AZ][REMOTE_CLIENT] health_check ok host=192.168.1.101")
        self._append(v, "[AZ][INF_SERVER] process spawned pid=123")
        self._append(v, "[AZ][UPDATE] step=1 loss=0.2")
        v.setProperty("activeFilter", "dist")
        self.assertEqual(v.property("visibleCount"), 3)

    def test_episode_filter(self):
        v = self._new()
        self._append(v, "[TRAIN][EP] ep=7/300 algo=az actor=3 result=draw end_reason=turn_limit vp_diff=0 ep_reward=0.0000 turns=12")
        self._append(v, "[AZ][ENV_WORKER] worker=3 local_ep=3/38 starting")
        v.setProperty("activeFilter", "episodes")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_dqn_lines_classified(self):
        v = self._new()
        self._append(v, "[TRAIN][EP] ep=12/300 algo=dqn result=win end_reason=wipeout_enemy vp_diff=3 ep_reward=1.2500 turns=15")
        self._append(v, "[TRAIN][EVAL_WINDOW] ep=100 window=100 win_rate=0.640")
        self._append(v, "[DQN][DIST] ПК2 готов: workers=8/8")
        self._append(v, "[DQN][ACTOR] actor=2 stop.flag — выход")
        v.setProperty("activeFilter", "episodes")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "dist")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "actors")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_ppo_episode_lines(self):
        v = self._new()
        self._append(v, "[TRAIN][EP] ep=20/300 algo=ppo result=win end_reason=wipeout_enemy vp_diff=2 ep_reward=0.5000 turns=14")
        self._append(v, "[PPO][METRICS] ep=20/300 reward=0.5000 loss=0.1")
        self._append(v, "[PPO][UPDATE] kl=0.01")
        v.setProperty("activeFilter", "episodes")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "train")
        self.assertEqual(v.property("visibleCount"), 3)

    def test_gmz_lines_classified(self):
        v = self._new()
        self._append(v, "[GMZ][ENV_WORKER] worker=1 started episodes=37")
        self._append(v, "[GMZ][REMOTE_CLIENT] health_check ok")
        self._append(v, "[GMZ][CHECKPOINT] ep=50 path=artifacts/models/x.pth")
        v.setProperty("activeFilter", "actors")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "dist")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "train")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_train_alert_is_warning(self):
        v = self._new()
        self._append(v, "[TRAIN][ALERT] win_rate просел ниже порога")
        self._append(v, "[TRAIN][PHASE] evaluating")
        v.setProperty("activeFilter", "warn")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_league_and_trace_groups(self):
        v = self._new()
        self._append(v, "[LEAGUE][SAVE] agent_id=P1_x artifact_dir=artifacts/league/x")
        self._append(v, "[TRACE][EP] ep=3 lines=120/120")
        v.setProperty("activeFilter", "train")
        self.assertEqual(v.property("visibleCount"), 1)
        v.setProperty("activeFilter", "actors")
        self.assertEqual(v.property("visibleCount"), 1)

    def test_clear_all(self):
        v = self._new()
        self._append(v, "[AZ][ACTOR] actor=0 move=5")
        from PySide6.QtCore import QMetaObject, Qt

        QMetaObject.invokeMethod(v, "clearAll", Qt.ConnectionType.DirectConnection)
        self.assertEqual(v.property("lineCount"), 0)
        self.assertEqual(v.property("visibleCount"), 0)


if __name__ == "__main__":
    unittest.main()
