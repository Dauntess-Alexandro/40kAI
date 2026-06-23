"""Task 3: fight-план механизм полностью снесён.

TDD-тест: RED сначала (механизм ещё есть → тест падает).
После сноса → зелёный.
"""

from tests.engine.phases._helpers import build_env


def test_fight_plan_mechanism_removed():
    """Убеждаемся, что fight-план механизм полностью удалён.

    Проверяем:
    - env не имеет метода _apply_pending_fight_stratagem_plan
    - option_candidates не экспортирует attach_fight_stratagem_plan
    - option_candidates не содержит _fight_stratagem_plan_from_choices
    """
    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})

    # env не должен иметь метода fight-плана
    assert not hasattr(env, "_apply_pending_fight_stratagem_plan"), (
        "warhamEnv._apply_pending_fight_stratagem_plan должен быть удалён (Task 3)"
    )

    # option_candidates не должен экспортировать fight-план функции
    from core.models import option_candidates as oc
    assert not hasattr(oc, "attach_fight_stratagem_plan"), (
        "option_candidates.attach_fight_stratagem_plan должен быть удалён (Task 3)"
    )
    assert not hasattr(oc, "_fight_stratagem_plan_from_choices"), (
        "option_candidates._fight_stratagem_plan_from_choices должен быть удалён (Task 3)"
    )
