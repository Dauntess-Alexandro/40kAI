from __future__ import annotations

import socket

import tools.pc2_az_actors as pc2


def test_wait_for_pc1_live_returns_true_when_receiver_reachable():
    """Если приёмник ПК1 слушает — гейт сразу пускает актёров."""
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind(("127.0.0.1", 0))
    srv.listen(1)
    host, port = srv.getsockname()
    try:
        assert pc2.wait_for_pc1_live(host, port, total_wait_sec=5.0, poll_sec=0.05) is True
    finally:
        srv.close()


def test_wait_for_pc1_live_times_out_when_no_receiver():
    """Нет ПК1 → гейт возвращает False (актёры не запускаются — без спама)."""
    calls = {"sleep": 0}
    # Свободный порт без слушателя.
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    free_port = s.getsockname()[1]
    s.close()

    fake_now = [0.0]

    def now():
        return fake_now[0]

    def sleep(sec):
        calls["sleep"] += 1
        fake_now[0] += sec

    ok = pc2.wait_for_pc1_live(
        "127.0.0.1",
        free_port,
        total_wait_sec=1.0,
        poll_sec=0.5,
        log=lambda *_: None,
        sleep=sleep,
        now=now,
    )
    assert ok is False
    assert calls["sleep"] >= 1


def test_wait_for_pc1_live_stop_during_wait_returns_false():
    """Stop, появившийся уже во время ожидания (а не залежавшийся на входе),
    останавливает гейт: актёры не запускаются."""
    fake_now = [0.0]
    state = {"probe": 0}

    def now():
        return fake_now[0]

    def sleep(sec):
        fake_now[0] += sec

    def reachable(_h, _p, timeout=1.0):
        state["probe"] += 1
        return False

    # Флага нет на входе; он "появляется" после 2-й пробы (живой stop текущего прогона).
    def should_stop():
        return state["probe"] >= 2

    ok = pc2.wait_for_pc1_live(
        "127.0.0.1",
        5557,
        total_wait_sec=100.0,
        poll_sec=1.0,
        should_stop=should_stop,
        reachable=reachable,
        log=lambda *_: None,
        sleep=sleep,
        now=now,
    )
    assert ok is False


def test_wait_for_pc1_live_ignores_stale_stop_flag_until_pc1_appears():
    """Залежавшийся stop.flag (есть уже на входе) НЕ должен мгновенно глушить гейт:
    ждём ПК1, и когда приёмник появляется — пускаем актёров (True)."""
    fake_now = [0.0]
    probe = {"n": 0}

    def now():
        return fake_now[0]

    def sleep(sec):
        fake_now[0] += sec

    def reachable(_h, _p, timeout=1.0):
        probe["n"] += 1
        return probe["n"] >= 3  # ПК1 поднимается к 3-й пробе (свежий train очистил флаг)

    ok = pc2.wait_for_pc1_live(
        "127.0.0.1",
        5557,
        total_wait_sec=100.0,
        poll_sec=1.0,
        should_stop=lambda: True,  # stale-флаг присутствует всё время
        reachable=reachable,
        log=lambda *_: None,
        sleep=sleep,
        now=now,
    )
    assert ok is True
    assert probe["n"] >= 3


def test_wait_for_pc1_live_stale_flag_waits_then_times_out():
    """Stale stop.flag на входе + ПК1 так и не появился → False по таймауту,
    но гейт реально ждал (а не вышел мгновенно)."""
    fake_now = [0.0]
    calls = {"sleep": 0, "probe": 0}

    def now():
        return fake_now[0]

    def sleep(sec):
        calls["sleep"] += 1
        fake_now[0] += sec

    def reachable(_h, _p, timeout=1.0):
        calls["probe"] += 1
        return False

    ok = pc2.wait_for_pc1_live(
        "127.0.0.1",
        5557,
        total_wait_sec=2.0,
        poll_sec=0.5,
        should_stop=lambda: True,
        reachable=reachable,
        log=lambda *_: None,
        sleep=sleep,
        now=now,
    )
    assert ok is False
    assert calls["sleep"] >= 1
    assert calls["probe"] >= 1


def test_wait_for_pc1_live_disabled_when_zero():
    """total_wait_sec<=0 — гейт выключен (старое поведение): сразу True."""
    assert pc2.wait_for_pc1_live("127.0.0.1", 5557, total_wait_sec=0.0) is True
