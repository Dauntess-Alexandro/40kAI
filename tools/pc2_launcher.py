#!/usr/bin/env python
"""ПК2 Launcher — окно для запуска распределённого обучения (DQN/AZ актора, AZ/GMZ inference).

Лёгкое отдельное окно: одна общая папка (40KAI_SHARE_ROOT) + выбор роли + лог.
Запуск на ПК2: python tools/pc2_launcher.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> int:
    from PySide6 import QtCore, QtGui, QtQml

    from app.gui_qt.pc2_launcher_controller import Pc2LauncherController

    app = QtGui.QGuiApplication(sys.argv)
    app.setApplicationName("40kAI ПК2 Launcher")

    controller = Pc2LauncherController()
    engine = QtQml.QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)

    qml_path = _REPO_ROOT / "app" / "gui_qt" / "qml" / "Pc2Launcher.qml"
    engine.load(QtCore.QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        print(f"[PC2][LAUNCHER][ERROR] не удалось загрузить QML: {qml_path}", flush=True)
        return 1

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
