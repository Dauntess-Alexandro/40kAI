import os
import sys
from PySide6 import QtCore, QtGui, QtQml


class GUIController(QtCore.QObject):
    logLine = QtCore.Signal(str)
    statusChanged = QtCore.Signal(str)
    runningChanged = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process = None
        self._running = False

    @QtCore.Slot()
    def start_train(self) -> None:
        self._start_process([sys.executable, "train.py"], "TRAIN")

    @QtCore.Slot()
    def start_eval(self) -> None:
        self._start_process([sys.executable, "eval.py"], "EVAL")

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

    @QtCore.Property(bool, notify=runningChanged)
    def running(self) -> bool:
        return self._running

    def _set_running(self, value: bool) -> None:
        if self._running != value:
            self._running = value
            self.runningChanged.emit(value)

    def _start_process(self, args: list[str], label: str) -> None:
        if self._process is not None:
            self._emit_status("Процесс уже запущен. Сначала остановите текущий.")
            return

        self._emit_log(f"[GUI] Запуск {label}...", level="INFO")
        self._process = QtCore.QProcess(self)
        env = QtCore.QProcessEnvironment.systemEnvironment()
        env.insert("TRAIN_LOG_ENABLED", "1")
        env.insert("TRAIN_LOG_TO_CONSOLE", "1")
        env.insert("TRAIN_LOG_TO_FILE", "1")
        self._process.setProcessEnvironment(env)

        self._process.readyReadStandardOutput.connect(self._read_stdout)
        self._process.readyReadStandardError.connect(self._read_stderr)
        self._process.errorOccurred.connect(self._on_error)
        self._process.finished.connect(self._on_finished)

        self._process.start(args[0], args[1:])
        if not self._process.waitForStarted(3000):
            self._emit_log("[GUI] Не удалось запустить процесс. Проверьте Python и зависимости.", level="ERROR")
            self._cleanup_process()
            return

        self._set_running(True)
        self._emit_status(f"Запущено: {label}")

    def _read_stdout(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            if line.strip():
                self._emit_log(line)

    def _read_stderr(self) -> None:
        if self._process is None:
            return
        data = self._process.readAllStandardError().data().decode("utf-8", errors="replace")
        for line in data.splitlines():
            if line.strip():
                self._emit_log(line, level="ERROR")

    def _on_error(self, error: QtCore.QProcess.ProcessError) -> None:
        self._emit_log(f"[GUI] Ошибка процесса: {error}.", level="ERROR")
        self._emit_status("Ошибка запуска. Проверьте логи и зависимости.")
        self._cleanup_process()

    def _on_finished(self, exit_code: int, exit_status: QtCore.QProcess.ExitStatus) -> None:
        status_text = "нормально" if exit_status == QtCore.QProcess.ExitStatus.NormalExit else "с ошибкой"
        self._emit_log(f"[GUI] Процесс завершён ({status_text}), код: {exit_code}.")
        self._emit_status("Процесс завершён.")
        self._cleanup_process()

    def _cleanup_process(self) -> None:
        if self._process is None:
            return
        self._process.deleteLater()
        self._process = None
        self._set_running(False)

    def _emit_log(self, message: str, level: str | None = None) -> None:
        if level:
            payload = f"[{level}] {message}"
        else:
            payload = message
        self.logLine.emit(payload)

    def _emit_status(self, message: str) -> None:
        self.statusChanged.emit(message)


def main() -> int:
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()

    controller = GUIController()
    engine.rootContext().setContextProperty("controller", controller)

    qml_path = os.path.join(os.path.dirname(__file__), "qml", "Main.qml")
    engine.load(QtCore.QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        return 1

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
