# tests/engine/test_heur_metrics.py
import json
import unittest

from core.engine.heuristic_targeting import (
    aggregate_heur_records,
    new_heur_counters,
    record_heur_charge,
    record_heur_move,
)


class TestHeurCounters(unittest.TestCase):
    def test_new_counters_shape(self):
        c = new_heur_counters("kiter")
        self.assertEqual(c["profile"], "kiter")
        self.assertEqual(c["mode"], {"kite": 0, "hold": 0, "commit": 0})
        self.assertEqual(c["role"], {"ranged": 0, "hybrid": 0, "melee": 0})
        self.assertEqual(c["risk_n"], 0)

    def test_record_move_increments(self):
        c = new_heur_counters()
        record_heur_move(c, "kite", "ranged", 0.4)
        record_heur_move(c, "hold", "hybrid", 0.2)
        self.assertEqual(c["mode"], {"kite": 1, "hold": 1, "commit": 0})
        self.assertEqual(c["role"]["ranged"], 1)
        self.assertEqual(c["moves"], 2)
        self.assertAlmostEqual(c["risk_sum"], 0.6, places=6)

    def test_record_move_ignores_unknown(self):
        c = new_heur_counters()
        record_heur_move(c, "weird_mode", "weird_role", 0.1)
        self.assertEqual(c["moves"], 1)  # moves считается
        self.assertEqual(sum(c["mode"].values()), 0)  # но в известные не попало

    def test_record_charge(self):
        c = new_heur_counters()
        record_heur_charge(c, True)
        record_heur_charge(c, False)
        self.assertEqual(c["charge_attempts"], 2)
        self.assertEqual(c["charge_success"], 1)


class TestAggregateHeurRecords(unittest.TestCase):
    def test_aggregate_modes_and_entropy(self):
        # три записи (игры) с равномерными режимами -> максимальная энтропия
        recs = []
        for _ in range(3):
            c = new_heur_counters()
            record_heur_move(c, "kite", "ranged", 0.5)
            record_heur_move(c, "hold", "hybrid", 0.5)
            record_heur_move(c, "commit", "melee", 0.5)
            recs.append(c)
        agg = aggregate_heur_records(recs)
        self.assertEqual(agg["games"], 3)
        self.assertEqual(agg["mode_totals"], {"kite": 3, "hold": 3, "commit": 3})
        self.assertAlmostEqual(agg["style_entropy_norm"], 1.0, places=6)
        self.assertAlmostEqual(agg["avg_risk"], 0.5, places=6)

    def test_entropy_zero_when_single_mode(self):
        c = new_heur_counters()
        for _ in range(10):
            record_heur_move(c, "hold", "hybrid", 0.3)
        agg = aggregate_heur_records([c])
        self.assertAlmostEqual(agg["style_entropy_norm"], 0.0, places=6)

    def test_charge_success_rate_and_profiles(self):
        c1 = new_heur_counters("kiter")
        record_heur_charge(c1, True)
        record_heur_charge(c1, True)
        c2 = new_heur_counters("aggressor")
        record_heur_charge(c2, False)
        agg = aggregate_heur_records([c1, c2])
        self.assertAlmostEqual(agg["charge_success_rate"], 2 / 3, places=6)
        self.assertEqual(agg["profile_counts"], {"kiter": 1, "aggressor": 1})

    def test_empty_records_safe(self):
        agg = aggregate_heur_records([])
        self.assertEqual(agg["games"], 0)
        self.assertEqual(agg["style_entropy_norm"], 0.0)


def test_flush_skips_empty_and_writes_nonempty(monkeypatch, tmp_path):
    import types

    import core.envs.warhamEnv as we
    from core.envs.warhamEnv import Warhammer40kEnv

    monkeypatch.setattr(we, "ARTIFACTS_METRICS_DIR", tmp_path)
    out_dir = tmp_path / "heur_decisions"

    # 1) пустые счётчики (moves==0) -> ничего не пишется
    stub = types.SimpleNamespace(_heur_metric_counters=new_heur_counters("kiter"))
    Warhammer40kEnv._flush_heur_metrics(stub)
    assert not out_dir.exists() or not list(out_dir.glob("*.jsonl"))

    # 2) есть ход -> пишется одна JSONL-строка с профилем
    record_heur_move(stub._heur_metric_counters, "kite", "ranged", 0.5)
    Warhammer40kEnv._flush_heur_metrics(stub)
    files = list(out_dir.glob("heur_dec_*.jsonl"))
    assert len(files) == 1
    lines = [line for line in files[0].read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) == 1
    rec = json.loads(lines[0])
    assert rec["profile"] == "kiter"
    assert rec["mode"]["kite"] == 1


if __name__ == "__main__":
    unittest.main()
