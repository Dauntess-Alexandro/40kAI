"""PC2 Launcher: QML грузится без ошибок и контроллер связан (offscreen)."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

PySide6 = pytest.importorskip("PySide6")

from PySide6 import QtCore, QtGui, QtQml  # noqa: E402

from app.gui_qt.pc2_launcher_controller import Pc2LauncherController  # noqa: E402

_QML = Path("app/gui_qt/qml/Pc2Launcher.qml").resolve()


def _app() -> QtGui.QGuiApplication:
    return QtGui.QGuiApplication.instance() or QtGui.QGuiApplication([])


def test_qml_loads_with_controller():
    _app()
    controller = Pc2LauncherController()
    engine = QtQml.QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)
    warnings: list[str] = []
    engine.warnings.connect(lambda ws: warnings.extend(w.toString() for w in ws))
    engine.load(QtCore.QUrl.fromLocalFile(str(_QML)))

    assert engine.rootObjects(), "QML не загрузился"
    assert not warnings, f"QML warnings: {warnings}"


def test_check_smb_emits_signal(tmp_path):
    _app()
    controller = Pc2LauncherController()
    received: list[tuple[bool, str]] = []
    controller.smbChecked.connect(lambda ok, msg: received.append((ok, msg)))

    controller.shareRoot = str(tmp_path)
    controller.checkSmb()

    assert received and received[-1][0] is True


def test_roles_exposed_to_qml():
    _app()
    controller = Pc2LauncherController()
    ids = [r["id"] for r in controller.rolesModel]
    assert ids == [
        "dqn_actors",
        "az_actors",
        "az_inference",
        "gmz_inference",
        "smz_inference",
        "gaz_inference",
        "gaz_actors",
    ]
