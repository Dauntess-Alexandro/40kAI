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


if __name__ == "__main__":
    unittest.main()
