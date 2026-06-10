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


def test_wait_for_pc1_live_stop_requested_returns_false_without_probing():
    """Запрошен stop → актёров не запускаем, сетевую пробу не делаем."""
    probed = {"n": 0}

    def reachable(_h, _p, timeout=1.0):
        probed["n"] += 1
        return False

    ok = pc2.wait_for_pc1_live(
        "127.0.0.1",
        5557,
        total_wait_sec=10.0,
        should_stop=lambda: True,
        reachable=reachable,
        log=lambda *_: None,
    )
    assert ok is False
    assert probed["n"] == 0


def test_wait_for_pc1_live_disabled_when_zero():
    """total_wait_sec<=0 — гейт выключен (старое поведение): сразу True."""
    assert pc2.wait_for_pc1_live("127.0.0.1", 5557, total_wait_sec=0.0) is True
