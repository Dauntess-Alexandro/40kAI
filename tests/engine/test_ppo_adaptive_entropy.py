from core.models.PPO import update_ppo_entropy_coef


def test_entropy_coef_increases_when_entropy_below_target():
    coef = update_ppo_entropy_coef(0.01, observed_entropy=0.1, target_entropy=0.5, adapt_lr=0.1)
    assert coef > 0.01
    assert coef <= 0.1


def test_entropy_coef_decreases_when_entropy_above_target():
    coef = update_ppo_entropy_coef(0.05, observed_entropy=0.9, target_entropy=0.5, adapt_lr=0.1)
    assert coef < 0.05
    assert coef >= 1e-4


def test_entropy_coef_clamped():
    coef = update_ppo_entropy_coef(0.09, observed_entropy=0.0, target_entropy=10.0, adapt_lr=1.0)
    assert coef == 0.1
