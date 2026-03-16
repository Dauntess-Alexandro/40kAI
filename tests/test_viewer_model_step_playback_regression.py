from pathlib import Path


def test_model_step_struct_and_controls_present():
    source = Path("viewer/app.py").read_text(encoding="utf-8")
    assert "class ModelStep" in source
    assert "self.model_step_next_btn = QtWidgets.QPushButton(\"Следующий шаг\")" in source
    assert "self.model_step_play_btn = QtWidgets.QPushButton(\"Play\")" in source
    assert "self.model_step_label = QtWidgets.QLabel(\"MODEL · ожидание\")" in source


def test_model_step_hotkeys_present():
    source = Path("viewer/app.py").read_text(encoding="utf-8")
    assert "if key in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):" in source
    assert "self._next_model_step()" in source
    assert "if key == QtCore.Qt.Key_Space:" in source
    assert "self._toggle_model_step_play()" in source
    assert "if key == QtCore.Qt.Key_Escape:" in source
    assert "self._stop_model_step_playback()" in source


def test_model_steps_rebuild_from_events():
    source = Path("viewer/app.py").read_text(encoding="utf-8")
    assert "def _rebuild_model_steps_from_events" in source
    assert "phase_order = [\"command\", \"movement\", \"shooting\", \"charge\", \"fight\"]" in source
    assert "[VIEWER_DEBUG][MODEL_STEPS] создано шагов=" in source
