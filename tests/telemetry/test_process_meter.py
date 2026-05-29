from app.gui_qt.telemetry.process_meter import ProcessMeter, aggregate_tree


def test_aggregate_tree_sums_and_normalizes():
    # cpu_percent уже нормализован per-process (может быть >100 на многоядерных)
    samples = [
        {"cpu": 120.0, "rss": 2_000_000_000},
        {"cpu": 80.0, "rss": 1_000_000_000},
    ]
    out = aggregate_tree(samples, ncpu=4, total_ram=8_000_000_000)
    assert abs(out["cpu_pct"] - 50.0) < 1e-6   # (120+80)/4 = 50
    assert abs(out["ram_gb"] - 3.0) < 1e-6
    assert abs(out["ram_pct"] - 37.5) < 1e-6   # 3/8 *100
    assert out["ok"] is True


def test_aggregate_tree_clamps_cpu_to_100():
    samples = [{"cpu": 800.0, "rss": 0}]
    out = aggregate_tree(samples, ncpu=4, total_ram=8_000_000_000)
    assert out["cpu_pct"] == 100.0


def test_aggregate_tree_empty_is_not_ok():
    out = aggregate_tree([], ncpu=4, total_ram=8_000_000_000)
    assert out["ok"] is False
    assert out["cpu_pct"] == 0.0
