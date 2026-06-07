"""Тесты TBLogger: реальная запись event-файла и безопасный no-op."""

from core.telemetry.tb_logger import TBLogger, make_tb_logger


def test_disabled_is_noop(tmp_path, monkeypatch):
    """enabled=False → writer не создаётся, вызовы безопасны, файлов нет."""
    tb = make_tb_logger("test_run", algo="dqn", enabled=False)
    assert tb.active is False
    # Никаких исключений при логировании в no-op режиме.
    tb.log_episode({"ep_reward": 1.0, "result": "win", "vp_diff": 3}, step=0)
    tb.log_train({"loss": 0.5, "lr": 1e-3}, step=0)
    tb.log_telemetry(step=0)
    tb.flush()
    tb.close()


def test_env_flag_disables(monkeypatch):
    """TB_ENABLED=0 выключает логгер даже без enabled=False."""
    monkeypatch.setenv("TB_ENABLED", "0")
    tb = make_tb_logger("test_run", algo="ppo")
    assert tb.active is False


def test_writes_event_file(tmp_path, monkeypatch):
    """enabled=True пишет event-файл TensorBoard в runtime/tb/<algo>/<run_id>."""
    # Перенаправляем RUNTIME_TB_DIR в tmp, чтобы не мусорить в репозитории.

    import core.telemetry.tb_logger as tb_mod

    monkeypatch.setattr(tb_mod, "RUNTIME_TB_DIR", tmp_path / "tb")
    monkeypatch.setenv("TB_ENABLED", "1")

    try:
        from torch.utils.tensorboard import SummaryWriter  # noqa: F401
    except Exception:
        # Без пакета tensorboard этот тест нерелевантен.
        import pytest

        pytest.skip("tensorboard не установлен")

    tb = TBLogger("run42", algo="az", enabled=True)
    assert tb.active is True
    tb.log_episode({"ep_reward": 2.5, "ep_len": 17, "result": "win", "vp_diff": 4}, step=1)
    tb.log_train({"loss": 0.123, "lr": 5e-4}, step=1)
    tb.close()

    logdir = tmp_path / "tb" / "az" / "run42"
    assert logdir.is_dir()
    files = list(logdir.glob("events.out.tfevents.*"))
    assert files, f"event-файл не создан в {logdir}"
    assert files[0].stat().st_size > 0
