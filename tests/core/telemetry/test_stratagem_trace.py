import unittest
from types import SimpleNamespace

from core.telemetry.stratagem_trace import (
    collect_stratagem_attempt_specs,
    eval_side_label,
    new_stratagem_records,
    stratagem_attempt_from_action,
    stratagem_used_snapshot,
    trace_side_label,
    train_stratagem_trace_enabled,
)


class TestStratagemTrace(unittest.TestCase):
    def test_stratagem_used_snapshot(self) -> None:
        env = SimpleNamespace(stratagem_used=[("model", "insane_bravery", 1, "command", 0)])
        snap = stratagem_used_snapshot(env)
        self.assertEqual(snap, (("model", "insane_bravery", 1, "command", 0),))

    def test_new_stratagem_records_append_only(self) -> None:
        before = (("model", "insane_bravery", 1, "command", 0),)
        after = (
            ("model", "insane_bravery", 1, "command", 0),
            ("model", "overwatch", 1, "shoot", 1),
        )
        new = new_stratagem_records(before, after)
        self.assertEqual(new, [("model", "overwatch", 1, "shoot", 1)])

    def test_stratagem_attempt_from_action_use_cp(self) -> None:
        sid, unit = stratagem_attempt_from_action({"use_cp": 1, "cp_on": 0})
        self.assertEqual(sid, "insane_bravery")
        self.assertEqual(unit, 0)

        sid2, unit2 = stratagem_attempt_from_action({"use_cp": 0, "cp_on": 0})
        self.assertIsNone(sid2)
        self.assertIsNone(unit2)

    def test_trace_side_label(self) -> None:
        self.assertEqual(trace_side_label("model", "P1"), "P1")
        self.assertEqual(trace_side_label("enemy", "P1"), "P2")
        self.assertEqual(trace_side_label("model", "P2"), "P2")
        self.assertEqual(eval_side_label("enemy", "P2"), "P1")

    def test_collect_stratagem_attempt_specs(self) -> None:
        specs = collect_stratagem_attempt_specs(
            {"use_cp": 1, "cp_on": 0},
            {1: "hungry_void"},
        )
        self.assertEqual(
            specs,
            [("insane_bravery", 0, "use_cp"), ("hungry_void", 1, "fight_plan")],
        )

    def test_train_stratagem_trace_enabled_env(self) -> None:
        import os

        from core.telemetry.stratagem_trace import stratagem_trace_actor_ok

        old_v = os.environ.get("VERBOSE_LOGS")
        old_t = os.environ.get("TRAIN_STRATAGEM_TRACE")
        old_a = os.environ.get("TRAIN_STRATAGEM_TRACE_ACTOR")
        try:
            os.environ["VERBOSE_LOGS"] = "0"
            os.environ["TRAIN_STRATAGEM_TRACE"] = "0"
            os.environ.pop("MANUAL_DICE", None)
            self.assertFalse(train_stratagem_trace_enabled())
            os.environ["VERBOSE_LOGS"] = "1"
            self.assertTrue(train_stratagem_trace_enabled())
            os.environ["TRAIN_STRATAGEM_TRACE_ACTOR"] = "0"
            self.assertTrue(stratagem_trace_actor_ok(0))
            self.assertFalse(stratagem_trace_actor_ok(1))
            self.assertTrue(stratagem_trace_actor_ok(-1))
        finally:
            if old_v is None:
                os.environ.pop("VERBOSE_LOGS", None)
            else:
                os.environ["VERBOSE_LOGS"] = old_v
            if old_t is None:
                os.environ.pop("TRAIN_STRATAGEM_TRACE", None)
            else:
                os.environ["TRAIN_STRATAGEM_TRACE"] = old_t
            if old_a is None:
                os.environ.pop("TRAIN_STRATAGEM_TRACE_ACTOR", None)
            else:
                os.environ["TRAIN_STRATAGEM_TRACE_ACTOR"] = old_a


if __name__ == "__main__":
    unittest.main()
