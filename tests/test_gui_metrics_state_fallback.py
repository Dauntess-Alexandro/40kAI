import json
import os
import tempfile
import types
import unittest
from unittest.mock import patch

import sys


class _DummySignal:
    def __init__(self, *args, **kwargs):
        pass

    def emit(self, *args, **kwargs):
        pass


class _DummyQObject:
    def __init__(self, *args, **kwargs):
        pass


class _DummyQUrl:
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def fromLocalFile(path):
        class _U:
            def toString(self):
                return path

        return _U()

    def isLocalFile(self):
        return False


def _dummy_prop(*args, **kwargs):
    def _wrap(func):
        return func

    return _wrap


class _DummyQProcess:
    class ProcessError:
        pass

    class ExitStatus:
        pass


class _DummyQtCore:
    QObject = _DummyQObject
    Signal = _DummySignal
    Slot = staticmethod(lambda *a, **k: (lambda f: f))
    Property = staticmethod(_dummy_prop)
    QUrl = _DummyQUrl
    QSize = staticmethod(lambda *a, **k: None)
    QProcess = _DummyQProcess

    def __getattr__(self, name):
        return object


qtcore = _DummyQtCore()
qtgui = types.SimpleNamespace(QIcon=object, QStandardItemModel=object)
qtqml = types.SimpleNamespace()
sys.modules.setdefault("PySide6", types.SimpleNamespace(QtCore=qtcore, QtGui=qtgui, QtQml=qtqml))
sys.modules.setdefault("PySide6.QtGui", types.SimpleNamespace(QIcon=object))

from gui_qt.main import GUIController


class _FakeTorch:
    @staticmethod
    def load(path, map_location=None):
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)


class GuiMetricsStateFallbackTests(unittest.TestCase):
    def _make_controller(self, root: str, model_id: str, model_path: str) -> GUIController:
        controller = GUIController.__new__(GUIController)
        controller._repo_root = root
        controller._selected_metrics_model_id = model_id
        controller._selected_metrics_model_path = model_path
        controller._metrics_torch_import_error = ""
        controller._metrics_torch_import_warned = False
        controller._emit_log = lambda *args, **kwargs: None
        return controller

    def test_pair_pth_priority(self):
        with tempfile.TemporaryDirectory() as td:
            models = os.path.join(td, "models", "run")
            os.makedirs(models, exist_ok=True)
            pickle_path = os.path.join(models, "model-1-1.pickle")
            open(pickle_path, "w", encoding="utf-8").close()
            with open(os.path.join(models, "model-1-1.pth"), "w", encoding="utf-8") as handle:
                json.dump({"global_step": 100, "optimize_steps": 10, "episode": 5, "replay_memory": {"size": 77}}, handle)
            with open(os.path.join(td, "hyperparams.json"), "w", encoding="utf-8") as handle:
                json.dump({"eps_start": 1.0, "eps_end": 0.1, "eps_decay": 1000}, handle)

            c = self._make_controller(td, "1-1", pickle_path)
            with patch.dict("sys.modules", {"torch": _FakeTorch}):
                meta = c._extract_selected_model_meta()

            self.assertEqual(meta["global_step"], "100")
            self.assertEqual(meta["replay_size"], "77")
            self.assertEqual(meta["source"], "model-1-1.pth")

    def test_checkpoint_fallback_when_model_missing(self):
        with tempfile.TemporaryDirectory() as td:
            models = os.path.join(td, "models", "run")
            os.makedirs(models, exist_ok=True)
            pickle_path = os.path.join(models, "model-2-2.pickle")
            open(pickle_path, "w", encoding="utf-8").close()
            with open(os.path.join(models, "checkpoint_ep15.pth"), "w", encoding="utf-8") as handle:
                json.dump({"global_step": 15, "optimize_steps": 3, "episode": 15, "replay_memory": {"items": [1, 2]}}, handle)

            c = self._make_controller(td, "2-2", pickle_path)
            with patch.dict("sys.modules", {"torch": _FakeTorch}):
                meta = c._extract_selected_model_meta()

            self.assertEqual(meta["episode"], "15")
            self.assertEqual(meta["replay_size"], "2")
            self.assertIn("checkpoint_ep15", meta["source"])

    def test_logs_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            models = os.path.join(td, "models", "run")
            os.makedirs(models, exist_ok=True)
            pickle_path = os.path.join(models, "model-3-3.pickle")
            open(pickle_path, "w", encoding="utf-8").close()
            with open(os.path.join(td, "LOGS_FOR_AGENTS.md"), "w", encoding="utf-8") as handle:
                handle.write("2026 | [TRAIN][START] run_id=1\n")
                handle.write("2026 | [RESUME] loaded checkpoint=... global_step=200 optimize_steps=11 episode=40 replay_size=123 eps=0.5000\n")
                handle.write("2026 | [SAVE] pickle сохранён: models/run/model-3-3.pickle\n")

            c = self._make_controller(td, "3-3", pickle_path)
            meta = c._extract_selected_model_meta()
            self.assertEqual(meta["global_step"], "200")
            self.assertEqual(meta["source"], "логи (fallback)")

    def test_torch_missing_uses_logs_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            models = os.path.join(td, "models", "run")
            os.makedirs(models, exist_ok=True)
            pickle_path = os.path.join(models, "model-4-4.pickle")
            open(pickle_path, "w", encoding="utf-8").close()
            with open(os.path.join(models, "model-4-4.pth"), "w", encoding="utf-8") as handle:
                handle.write("not used")
            with open(os.path.join(td, "LOGS_FOR_AGENTS.md"), "w", encoding="utf-8") as handle:
                handle.write("2026 | [TRAIN][START] run_id=1\n")
                handle.write("2026 | [RESUME] loaded checkpoint=... global_step=333 optimize_steps=44 episode=55 replay_size=66 eps=0.5000\n")
                handle.write("2026 | [SAVE] pickle сохранён: models/run/model-4-4.pickle\n")

            c = self._make_controller(td, "4-4", pickle_path)
            with patch.dict("sys.modules", {"torch": None}):
                meta = c._extract_selected_model_meta()

            self.assertEqual(meta["global_step"], "333")
            self.assertEqual(meta["source"], "логи (fallback)")
            self.assertEqual(meta["reason"], "")

    def test_no_sources_keeps_dashes_with_reason(self):
        with tempfile.TemporaryDirectory() as td:
            c = self._make_controller(td, "9-9", os.path.join(td, "models", "model-9-9.pickle"))
            meta = c._extract_selected_model_meta()
            self.assertEqual(meta["global_step"], "—")
            self.assertIn("Не найден checkpoint", meta["reason"])

    def test_eps_formula(self):
        c = GUIController.__new__(GUIController)
        eps = c._compute_eps_for_global_step(global_step=500, eps_start=1.0, eps_end=0.1, eps_decay=1000)
        self.assertAlmostEqual(eps, 0.55, places=6)

    def test_stale_selected_path_id_is_ignored(self):
        with tempfile.TemporaryDirectory() as td:
            run = os.path.join(td, "models", "run")
            os.makedirs(run, exist_ok=True)
            stale_pickle = os.path.join(run, "model-1-111111.pickle")
            open(stale_pickle, "w", encoding="utf-8").close()
            with open(os.path.join(run, "model-42-537303.pth"), "w", encoding="utf-8") as handle:
                json.dump({"global_step": 777, "optimize_steps": 12, "episode": 34, "replay_memory": {"count": 9}}, handle)

            c = self._make_controller(td, "42-537303", stale_pickle)
            with patch.dict("sys.modules", {"torch": _FakeTorch}):
                meta = c._extract_selected_model_meta()

            self.assertEqual(meta["global_step"], "777")
            self.assertEqual(meta["source"], "model-42-537303.pth")

    def test_load_metrics_json_sets_selected_pickle_by_model_id(self):
        with tempfile.TemporaryDirectory() as td:
            run = os.path.join(td, "models", "run")
            os.makedirs(run, exist_ok=True)
            with open(os.path.join(td, "models", "data_42-537303.json"), "w", encoding="utf-8") as handle:
                json.dump({}, handle)
            pickle_path = os.path.join(run, "model-42-537303.pickle")
            open(pickle_path, "w", encoding="utf-8").close()

            c = GUIController.__new__(GUIController)
            c._repo_root = td
            c._metrics_defaults = {k: "" for k in ("reward", "loss", "epLen", "winrate", "vpdiff", "endreasons")}
            c._resolve_metric_path = lambda value, default: default
            c._set_metrics_files = lambda updated: None
            c._refresh_metrics_summaries = lambda: None
            c._emit_status = lambda *args, **kwargs: None
            c._emit_log = lambda *args, **kwargs: None
            c._selected_metrics_model_id = ""
            c._selected_metrics_model_path = ""
            c._metrics_torch_import_error = ""
            c._metrics_torch_import_warned = False

            ok = c._load_metrics_from_json(os.path.join(td, "models", "data_42-537303.json"))
            self.assertTrue(ok)
            self.assertEqual(c._selected_metrics_model_id, "42-537303")
            self.assertEqual(c._selected_metrics_model_path, pickle_path)

    def test_torch_import_warn_is_emitted_once(self):
        c = self._make_controller("/tmp", "1-1", "/tmp/model-1-1.pickle")
        logs = []
        c._emit_log = lambda message, level=None: logs.append((level, message))

        with patch.dict("sys.modules", {"torch": None}):
            self.assertIsNone(c._get_torch_for_metrics_state())
            self.assertIsNone(c._get_torch_for_metrics_state())

        warn_lines = [item for item in logs if item[0] == "WARN" and "Не удалось импортировать torch" in item[1]]
        self.assertEqual(len(warn_lines), 1)


if __name__ == "__main__":
    unittest.main()
