# tests/models/test_dqn_dist_pc2_linger.py
"""ПК2: держать процесс (и телеметрию) до stop.flag ПК1 после доигрывания квоты."""
from core.models.dqn_dist import pc2_dist_should_exit


def test_exit_on_stop_flag_even_if_workers_alive():
    done, reason = pc2_dist_should_exit(
        stop_requested=True,
        all_workers_dead=False,
        workers_done_mono=None,
        now_mono=100.0,
        linger_sec=600.0,
    )
    assert done is True
    assert reason == "stop_flag"


def test_no_exit_while_workers_alive_and_no_stop():
    done, reason = pc2_dist_should_exit(
        stop_requested=False,
        all_workers_dead=False,
        workers_done_mono=None,
        now_mono=100.0,
        linger_sec=600.0,
    )
    assert done is False
    assert reason == ""


def test_no_exit_right_after_workers_done_within_linger():
    # Воркеры только что завершились — телеметрию держим, stop.flag ещё не пришёл.
    done, reason = pc2_dist_should_exit(
        stop_requested=False,
        all_workers_dead=True,
        workers_done_mono=100.0,
        now_mono=100.0 + 30.0,
        linger_sec=600.0,
    )
    assert done is False
    assert reason == ""


def test_exit_after_linger_elapsed_without_stop_flag():
    # Предохранитель: stop.flag не пришёл за linger — выходим, чтобы не висеть вечно.
    done, reason = pc2_dist_should_exit(
        stop_requested=False,
        all_workers_dead=True,
        workers_done_mono=100.0,
        now_mono=100.0 + 600.0,
        linger_sec=600.0,
    )
    assert done is True
    assert reason == "linger_elapsed"


def test_no_exit_when_workers_dead_but_done_mono_not_set_yet():
    done, reason = pc2_dist_should_exit(
        stop_requested=False,
        all_workers_dead=True,
        workers_done_mono=None,
        now_mono=9999.0,
        linger_sec=600.0,
    )
    assert done is False
    assert reason == ""
