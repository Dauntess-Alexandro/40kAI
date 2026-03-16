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


def test_model_steps_rebuild_from_state_and_snapshot_render():
    source = Path("viewer/app.py").read_text(encoding="utf-8")
    assert "def _rebuild_model_steps_from_state" in source
    assert "steps_raw = (state or {}).get(\"model_steps\")" in source
    assert "def _render_state_from_step_snapshot" in source
    assert "def _play_model_step_fx" in source
    assert "if not self._model_step_replay_active:" in source
    assert "self._model_step_replay_active = True" in source


def test_engine_exports_model_steps_payload():
    source = Path("gym_mod/gym_mod/engine/state_export.py").read_text(encoding="utf-8")
    assert 'payload["model_steps"] = list(model_steps)' in source
    assert 'payload["model_step_turn_token"]' in source


def test_env_collects_model_steps_with_snapshots():
    source = Path("gym_mod/gym_mod/envs/warhamEnv.py").read_text(encoding="utf-8")
    assert "def _append_viewer_model_step" in source
    assert '"snapshot": self._capture_viewer_units_snapshot()' in source
    assert "kind=\"phase_header\"" in source
    assert 'self._flush_state_snapshot(reason="viewer_model_step", force=True)' in source


def test_opengl_has_step_move_fx_hook():
    source = Path("viewer/opengl_view.py").read_text(encoding="utf-8")
    assert "def trigger_step_move_fx" in source
