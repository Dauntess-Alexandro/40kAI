"""Регресс-тесты симметрии first-turn: инварианты reset и CP-прирост."""

import pytest

from tests.engine.phases._helpers import build_env


def _fresh(first: str):
    """Создать env с заданным first_turn_side и сбросить."""
    env = build_env()
    env.first_turn_side = first
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    return env


# ═══════════════════════════════════════════════════════════════════
# 1. Reset invariants
# ═══════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("first", ["model", "enemy"])
class TestResetInvariants:
    """После reset с заданным first_turn_side — раунд=1, active=first, order корректен."""

    def test_battle_round_is_one(self, first):
        env = _fresh(first)
        assert env.battle_round == 1

    def test_active_side_equals_first(self, first):
        env = _fresh(first)
        assert env.active_side == first

    def test_turn_order_first_then_other(self, first):
        env = _fresh(first)
        other = "model" if first == "enemy" else "enemy"
        assert env.turn_order == [first, other]

    def test_first_turn_side_preserved(self, first):
        env = _fresh(first)
        assert env.first_turn_side == first


# ═══════════════════════════════════════════════════════════════════
# 2. CP symmetry after a full command round
# ═══════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("first", ["model", "enemy"])
class TestCPSymmetry:
    """Каждая command_phase даёт +1 обеим сторонам.

    За полный раунд (обе стороны отыграли command) CP-дельта model == CP-дельта enemy,
    независимо от порядка хода.
    """

    def test_single_command_phase_grants_plus_one_both(self, first):
        """Одна command_phase первого игрока даёт +1 и model, и enemy."""
        env = _fresh(first)
        cp_m_before = env.modelCP
        cp_e_before = env.enemyCP

        # Вызываем command_phase для первого в порядке
        side = env.turn_order[0]
        if side == "enemy":
            env.command_phase(side, action={})
        else:
            env.command_phase(side, action=None)

        assert env.modelCP - cp_m_before == 1
        assert env.enemyCP - cp_e_before == 1

    def test_full_round_cp_delta_symmetric(self, first):
        """После command_phase обеих сторон — CP-дельта model == CP-дельта enemy."""
        env = _fresh(first)
        cp_m_before = env.modelCP
        cp_e_before = env.enemyCP

        # Первый в порядке
        side0 = env.turn_order[0]
        if side0 == "enemy":
            env.command_phase(side0, action={})
        else:
            env.command_phase(side0, action=None)

        # Второй в порядке
        side1 = env.turn_order[1]
        if side1 == "enemy":
            env.command_phase(side1, action={})
        else:
            env.command_phase(side1, action=None)

        delta_m = env.modelCP - cp_m_before
        delta_e = env.enemyCP - cp_e_before

        assert delta_m == delta_e, (
            f"CP несимметричны при first={first}: "
            f"delta_model={delta_m}, delta_enemy={delta_e}"
        )
        # Каждая command_phase даёт +1 → за 2 фазы обе стороны получают +2
        assert delta_m == 2
        assert delta_e == 2

    def test_cp_values_equal_after_full_round(self, first):
        """Model CP == Enemy CP после полного командного раунда (стартуют с 0)."""
        env = _fresh(first)
        assert env.modelCP == 0
        assert env.enemyCP == 0

        side0 = env.turn_order[0]
        if side0 == "enemy":
            env.command_phase(side0, action={})
        else:
            env.command_phase(side0, action=None)

        side1 = env.turn_order[1]
        if side1 == "enemy":
            env.command_phase(side1, action={})
        else:
            env.command_phase(side1, action=None)

        assert env.modelCP == env.enemyCP
