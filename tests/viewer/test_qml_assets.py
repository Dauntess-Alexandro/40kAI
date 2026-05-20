"""Smoke: QML hybrid files exist for viewer.ui.qml_panels."""

from __future__ import annotations

import unittest
from pathlib import Path

from project_paths import APP_DIR


class TestViewerQmlAssets(unittest.TestCase):
    def test_viewer_main_qml_present(self) -> None:
        path = APP_DIR / "viewer" / "ui" / "qml" / "ViewerMain.qml"
        self.assertTrue(path.is_file(), f"missing {path}")

    def test_log_panel_qml_present(self) -> None:
        path = APP_DIR / "viewer" / "ui" / "qml" / "LogPanel.qml"
        self.assertTrue(path.is_file(), f"missing {path}")


if __name__ == "__main__":
    unittest.main()
