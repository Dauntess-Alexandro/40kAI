from app.gui_qt.telemetry.batch_meter import BatchMeter


def test_batch_meter_average_of_parsed_lines():
    m = BatchMeter(window=10)
    m.feed_line("[GMZ][INF_SERVER] batch=10 inference_ms=12.0 total_reqs=100")
    m.feed_line("[GMZ][INF_SERVER] batch=8 inference_ms=11.0 total_reqs=108")
    assert m.average() == 9.0


def test_batch_meter_ignores_non_batch_lines():
    m = BatchMeter(window=10)
    m.feed_line("some unrelated log line")
    m.feed_line("[GMZ][INF_SERVER] started batch=10 device=cuda")
    assert m.average() == 10.0


def test_batch_meter_empty_average_is_none():
    assert BatchMeter().average() is None


def test_batch_meter_window_evicts_old():
    m = BatchMeter(window=2)
    for v in (2, 4, 6):
        m.feed_line(f"batch={v}")
    assert m.average() == 5.0  # только последние два: (4+6)/2
