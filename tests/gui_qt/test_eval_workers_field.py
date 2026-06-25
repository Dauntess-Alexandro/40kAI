from app.gui_qt.main import GUIController


class _Signal:
    def emit(self, *_args, **_kwargs):
        return None


def _controller_stub():
    ctrl = GUIController.__new__(GUIController)
    ctrl._eval_workers = 1
    ctrl.evalWorkersChanged = _Signal()
    ctrl.evalSetupChanged = _Signal()
    ctrl._emit_status = lambda *_args, **_kwargs: None
    return ctrl


def test_set_eval_workers_clamps_min_1():
    controller = _controller_stub()
    controller.set_eval_workers(4)
    assert controller._eval_workers == 4

    controller.set_eval_workers(0)
    assert controller._eval_workers == 4
