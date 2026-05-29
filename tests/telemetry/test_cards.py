from app.gui_qt.telemetry.cards import build_cards


def _local():
    return {
        "cpu_pct": 58.0, "ram_pct": 42.0, "ram_gb": 11.2, "ok": True,
        "gpus": [{"index": 0, "name": "RTX 5060 Ti", "util": 81,
                  "mem_used_mb": 4096, "mem_total_mb": 16384,
                  "proc_mem_mb": 3500, "temp_c": 64}],
    }


def test_cards_local_only_gmz_active():
    cards = build_cards(local=_local(), remote=None, batch_avg=9.7,
                        batch_size_hint=10, algo="gumbel_muzero", active=True)
    ids = [c["id"] for c in cards]
    assert ids == ["gpu0", "cpu", "ram", "batch"]
    gpu = cards[0]
    assert gpu["pct"] == 81 and gpu["variant"] == "local"
    assert "16384" not in gpu["valueText"]  # value = util%, не память
    batch = cards[-1]
    assert batch["valueText"].startswith("9.7")


def test_cards_hide_batch_for_non_gmz():
    cards = build_cards(local=_local(), remote=None, batch_avg=None,
                        batch_size_hint=None, algo="dqn", active=True)
    assert "batch" not in [c["id"] for c in cards]


def test_cards_remote_inserted_after_local_gpus():
    remote = {"name": "RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55, "avg_batch": 9.5}
    cards = build_cards(local=_local(), remote=remote, batch_avg=9.7,
                        batch_size_hint=10, algo="gumbel_muzero", active=True)
    ids = [c["id"] for c in cards]
    assert ids == ["gpu0", "pc2", "cpu", "ram", "batch"]
    assert cards[1]["variant"] == "remote"


def test_cards_idle_dashes_project_metrics():
    cards = build_cards(local=_local(), remote=None, batch_avg=None,
                        batch_size_hint=None, algo="gumbel_muzero", active=False)
    cpu = next(c for c in cards if c["id"] == "cpu")
    assert cpu["valueText"] == "—"
    assert cpu["pct"] == 0


def test_cards_high_util_warns():
    local = _local()
    local["gpus"][0]["util"] = 95
    cards = build_cards(local=local, remote=None, batch_avg=None,
                        batch_size_hint=None, algo="dqn", active=True)
    assert cards[0]["warn"] is True
