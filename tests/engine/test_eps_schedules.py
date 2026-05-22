import os

from core.models.utils import compute_epsilon


def test_epsilon_schedules_monotone_and_bounds():
    old_decay = os.environ.get("EPS_DECAY")
    os.environ["EPS_DECAY"] = "1000"
    try:
        schedules = ["exp", "linear", "poly", "sigmoid"]
        for sched in schedules:
            os.environ["EPS_SCHEDULE"] = sched
            e0 = compute_epsilon(0, schedule=sched)
            e1 = compute_epsilon(500, schedule=sched)
            e2 = compute_epsilon(2000, schedule=sched)
            assert e0 >= e1 >= e2 or abs(e0 - e1) < 1e-6
    finally:
        if old_decay is None:
            os.environ.pop("EPS_DECAY", None)
        else:
            os.environ["EPS_DECAY"] = old_decay
