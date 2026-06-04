from app.gui_qt.telemetry.cards import build_cards


def _local():
    return {
        "cpu_name": "Ryzen 5 7600", "cpu_pct": 58.0, "ram_pct": 42.0, "ram_gb": 11.2, "ok": True,
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


def test_cpu_card_uses_system_metric_when_present():
    local = _local()
    local["cpu_pct_system"] = 91.0  # система загружена сильнее, чем дерево train (58%)
    cards = build_cards(local=local, remote=None, batch_avg=None,
                        batch_size_hint=None, algo="alphazero_tree", active=True)
    cpu = next(c for c in cards if c["id"] == "cpu")
    assert cpu["valueText"] == "91%"
    assert cpu["sub"] == "система"
    assert cpu["warn"] is True  # >= WARN_PCT (90)


def test_cpu_card_falls_back_to_process_metric():
    cards = build_cards(local=_local(), remote=None, batch_avg=None,
                        batch_size_hint=None, algo="dqn", active=True)
    cpu = next(c for c in cards if c["id"] == "cpu")
    assert cpu["valueText"] == "58%"  # нет cpu_pct_system → fallback на process cpu_pct


def test_two_pc_mode_prefixes_local_cards():
    remote = {"name": "RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55}
    local = _local()
    local["cpu_pct_system"] = 70.0
    cards = build_cards(local=local, remote=remote, batch_avg=None,
                        batch_size_hint=None, algo="alphazero_tree", active=True)
    gpu_local = cards[0]
    cpu = next(c for c in cards if c["id"] == "cpu")
    pc2 = next(c for c in cards if c["id"] == "pc2")
    assert gpu_local["label"].startswith("ПК1 · ")
    assert cpu["label"] == "ПК1 · Ryzen 5 7600"
    assert pc2["label"].startswith("ПК2 · ")


def test_pc2_cpu_card_present_and_ordered():
    remote = {"name": "RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55,
              "cpu_name": "Ryzen 5 1600", "cpu_pct_system": 38.0, "ram_pct_system": 31.0}
    local = _local()
    local["cpu_pct_system"] = 74.0
    cards = build_cards(local=local, remote=remote, batch_avg=None,
                        batch_size_hint=None, algo="alphazero_tree", active=True)
    ids = [c["id"] for c in cards]
    # порядок из UI-mock: ПК1 GPU, ПК2 GPU, ПК1 CPU, ПК2 CPU, RAM
    assert ids == ["gpu0", "pc2", "cpu", "pc2_cpu", "ram"]
    pc2_cpu = next(c for c in cards if c["id"] == "pc2_cpu")
    assert pc2_cpu["valueText"] == "38%"
    assert pc2_cpu["label"] == "ПК2 · Ryzen 5 1600"
    assert pc2_cpu["variant"] == "remote"


def test_pc2_cpu_card_absent_for_old_server():
    # старый ПК2 не шлёт cpu_pct_system → карточки ПК2 CPU нет (None)
    remote = {"name": "RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55,
              "cpu_pct_system": None}
    cards = build_cards(local=_local(), remote=remote, batch_avg=None,
                        batch_size_hint=None, algo="alphazero_tree", active=True)
    assert "pc2_cpu" not in [c["id"] for c in cards]


def test_labels_override_hardware_names():
    remote = {"name": "GeForce RTX 2060 SUPER", "util": 40, "mem_used_mb": 2048,
              "mem_total_mb": 8192, "proc_mem_mb": 2048, "temp_c": 55,
              "cpu_name": "amd64", "cpu_pct_system": 38.0}
    labels = {"pc1_gpu": "RTX 5060 Ti", "pc1_cpu": "Ryzen 5 7600",
              "pc2_gpu": "RTX 2060 Super", "pc2_cpu": "Ryzen 5 1600"}
    cards = build_cards(local=_local(), remote=remote, batch_avg=None,
                        batch_size_hint=None, algo="alphazero_tree", active=True, labels=labels)
    assert cards[0]["label"] == "ПК1 · RTX 5060 Ti"
    assert next(c for c in cards if c["id"] == "pc2")["label"] == "ПК2 · RTX 2060 Super"
    assert next(c for c in cards if c["id"] == "cpu")["label"] == "ПК1 · Ryzen 5 7600"
    assert next(c for c in cards if c["id"] == "pc2_cpu")["label"] == "ПК2 · Ryzen 5 1600"
