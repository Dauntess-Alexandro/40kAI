"""Тесты mission-bootstrap для AZ/GAZ self-play (outcome_only).

Инварианты (CLAUDE.md / задача):
- terminal outcome = главный источник истины: win=+1, loss=-1, draw=-0.7;
- VP-win и wipeout-win дают одинаковый terminal value +1 (нельзя делать VP-win «хуже»);
- VP-loss и wipeout-loss дают -1;
- mission-bootstrap НЕ меняет терминальный (последний) value-target;
- bootstrap полностью отключаем при coef=0 (бит-в-бит как без bootstrap);
- bootstrap двигает только НЕтерминальные транзиции ничьих и только в пределах draw-полосы.
"""
from __future__ import annotations

from core.models.az_mission_bootstrap import (
    build_reward_shaped_value_targets,
    build_value_targets,
    finalize_value_targets,
    mission_progress_signal,
    outcome_kind_from_info,
    side_mean_objective_distance,
    terminal_outcome_value,
)

WIN, LOSS, DRAW = 1.0, -1.0, -0.7


# --- terminal outcome mapping -------------------------------------------------

def test_vp_win_and_wipeout_win_both_plus_one():
    vp_win = {"winner": "model", "end reason": "turn_limit", "model VP": 5, "player VP": 2}
    wipe_win = {"winner": "", "end reason": "wipeout_enemy", "model VP": 0, "player VP": 0}
    v_vp = terminal_outcome_value(vp_win, win=WIN, loss=LOSS, draw=DRAW)
    v_wipe = terminal_outcome_value(wipe_win, win=WIN, loss=LOSS, draw=DRAW)
    assert v_vp == WIN
    assert v_wipe == WIN
    assert v_vp == v_wipe  # VP-win не должна быть «хуже» wipeout-win


def test_vp_loss_and_wipeout_loss_both_minus_one():
    vp_loss = {"winner": "enemy", "end reason": "turn_limit", "model VP": 1, "player VP": 4}
    wipe_loss = {"winner": "", "end reason": "wipeout_model"}
    assert terminal_outcome_value(vp_loss, win=WIN, loss=LOSS, draw=DRAW) == LOSS
    assert terminal_outcome_value(wipe_loss, win=WIN, loss=LOSS, draw=DRAW) == LOSS


def test_turn_limit_tie_is_draw():
    tie = {"winner": "", "end reason": "turn_limit", "model VP": 0, "player VP": 0}
    assert outcome_kind_from_info(tie) == "draw"
    assert terminal_outcome_value(tie, win=WIN, loss=LOSS, draw=DRAW) == DRAW


# --- bootstrap: terminal invariants ------------------------------------------

def test_bootstrap_disabled_when_coef_zero():
    info = {"end reason": "turn_limit", "model controlled objectives": [1, 2], "player controlled objectives": []}
    targets = build_value_targets(
        n_transitions=4, outcome_value=DRAW, outcome_kind="draw",
        info=info, coef=0.0, draw_value=DRAW,
    )
    assert targets == [DRAW, DRAW, DRAW, DRAW]


def test_bootstrap_does_not_touch_win_or_loss():
    # VP-win (с большим VP) и wipeout-win (VP=0) → все таргеты ровно WIN, без разницы.
    vp_win_info = {"model VP": 6, "player VP": 0, "model controlled objectives": [1, 2, 3]}
    wipe_win_info = {"model VP": 0, "player VP": 0, "model controlled objectives": []}
    t_vp = build_value_targets(n_transitions=5, outcome_value=WIN, outcome_kind="win",
                               info=vp_win_info, coef=0.1, draw_value=DRAW)
    t_wipe = build_value_targets(n_transitions=5, outcome_value=WIN, outcome_kind="win",
                                 info=wipe_win_info, coef=0.1, draw_value=DRAW)
    assert t_vp == [WIN] * 5
    assert t_wipe == [WIN] * 5

    loss_info = {"model VP": 0, "player VP": 6, "model controlled objectives": []}
    t_loss = build_value_targets(n_transitions=5, outcome_value=LOSS, outcome_kind="loss",
                                 info=loss_info, coef=0.1, draw_value=DRAW)
    assert t_loss == [LOSS] * 5


def test_bootstrap_terminal_transition_stays_pure_on_draw():
    info = {"end reason": "turn_limit", "model controlled objectives": [1, 2, 3],
            "player controlled objectives": [], "model health": [10, 10], "player health": [1]}
    targets = build_value_targets(n_transitions=4, outcome_value=DRAW, outcome_kind="draw",
                                  info=info, coef=0.1, draw_value=DRAW)
    assert targets[-1] == DRAW  # терминал не тронут
    # нетерминальные сдвинуты вверх (модель доминировала по точкам/HP)
    assert all(t > DRAW for t in targets[:-1])


def test_bootstrap_draw_nudge_stays_in_band():
    # Сильный коэффициент + полное доминирование → клип в пределах ±0.15 (для draw=-0.7).
    info = {"end reason": "turn_limit", "model controlled objectives": [1, 2, 3, 4, 5],
            "player controlled objectives": [], "model health": [50], "player health": []}
    targets = build_value_targets(n_transitions=3, outcome_value=DRAW, outcome_kind="draw",
                                  info=info, coef=10.0, draw_value=DRAW)
    band = 0.5 * (1.0 - abs(DRAW))
    for t in targets[:-1]:
        assert DRAW - band - 1e-9 <= t <= DRAW + band + 1e-9
    # никогда не дотягивает до полноценной победы/поражения
    assert all(t < WIN and t > LOSS for t in targets)


def test_bootstrap_bad_draw_nudges_down():
    # Модель проиграла по точкам и HP, но финал 0-0 (ничья) → нетерминальные ниже -0.7.
    info = {"end reason": "turn_limit", "model controlled objectives": [],
            "player controlled objectives": [1, 2, 3], "model health": [1], "player health": [20, 20]}
    targets = build_value_targets(n_transitions=4, outcome_value=DRAW, outcome_kind="draw",
                                  info=info, coef=0.1, draw_value=DRAW)
    assert targets[-1] == DRAW
    assert all(t < DRAW for t in targets[:-1])


def test_bootstrap_single_transition_episode_unchanged():
    info = {"end reason": "turn_limit", "model controlled objectives": [1, 2]}
    targets = build_value_targets(n_transitions=1, outcome_value=DRAW, outcome_kind="draw",
                                  info=info, coef=0.1, draw_value=DRAW)
    assert targets == [DRAW]


# --- mission signal -----------------------------------------------------------

def test_mission_signal_zero_when_symmetric():
    info = {"model controlled objectives": [1, 2], "player controlled objectives": [3, 4],
            "model health": [10, 10], "player health": [10, 10], "model VP": 3, "player VP": 3}
    assert abs(mission_progress_signal(info)) < 1e-9


def test_mission_signal_positive_when_model_dominates_objectives():
    info = {"model controlled objectives": [1, 2, 3], "player controlled objectives": [],
            "model health": [10], "player health": [10], "model VP": 0, "player VP": 0}
    assert mission_progress_signal(info) > 0.0


def test_mission_signal_bounded():
    info = {"model controlled objectives": [1, 2, 3, 4, 5], "player controlled objectives": [],
            "model health": [99], "player health": [], "model VP": 10, "player VP": 0}
    s = mission_progress_signal(info)
    assert -1.0 <= s <= 1.0


def test_mission_signal_prefers_cumulative_objectives_over_terminal():
    # Терминальный снимок 0/0 (как в turn_limit-ничьих), но накопительно за партию
    # модель доминировала по контролю точек → сигнал положительный.
    info = {
        "model controlled objectives": [], "player controlled objectives": [],  # терминал 0/0
        "az_cum_model_ctrl": 18.0, "az_cum_enemy_ctrl": 3.0,                     # накопительно
        "model health": [10], "player health": [10], "model VP": 0, "player VP": 0,
    }
    assert mission_progress_signal(info) > 0.0


def test_mission_signal_cumulative_zero_falls_back_to_hp():
    # Накопительный контроль ровно симметричен → объект-компонента 0, остаётся HP.
    info = {
        "az_cum_model_ctrl": 5.0, "az_cum_enemy_ctrl": 5.0,
        "model health": [20], "player health": [5], "model VP": 0, "player VP": 0,
    }
    assert mission_progress_signal(info) > 0.0  # за счёт HP-доминирования


def test_mission_signal_backward_compatible_terminal_only():
    # Старый info без накопительных ключей → используется терминальный снимок.
    info = {"model controlled objectives": [1, 2, 3], "player controlled objectives": [1]}
    assert mission_progress_signal(info) > 0.0


# --- distance/progress signal -------------------------------------------------

def test_side_mean_objective_distance_basic():
    # Юниты на (0,0) и (3,4); объектив в (0,0) → дистанции 0 и 5 → среднее 2.5.
    d = side_mean_objective_distance([[0, 0], [3, 4]], [1, 1], [[0, 0]])
    assert abs(d - 2.5) < 1e-6


def test_side_mean_objective_distance_filters_dead():
    # Второй юнит мёртв (health 0) → учитывается только первый (дист 0).
    d = side_mean_objective_distance([[0, 0], [10, 0]], [1, 0], [[0, 0]])
    assert d == 0.0


def test_side_mean_objective_distance_none_without_data():
    assert side_mean_objective_distance([], [], [[0, 0]]) is None
    assert side_mean_objective_distance([[0, 0]], [1], []) is None
    assert side_mean_objective_distance([[0, 0]], [1], None) is None


def test_side_mean_objective_distance_nearest_objective():
    # Два объектива; берётся ближайший.
    d = side_mean_objective_distance([[0, 0]], [1], [[10, 0], [1, 0]])
    assert abs(d - 1.0) < 1e-6


def test_mission_signal_positive_when_model_closer_to_objectives():
    # Контроль точек 0/0 (как в реальном региме), но модель в среднем БЛИЖЕ к точке.
    info = {
        "az_cum_model_ctrl": 0.0, "az_cum_enemy_ctrl": 0.0,
        "az_cum_model_dist": 5.0, "az_cum_enemy_dist": 20.0,  # модель ближе
        "model health": [10], "player health": [10], "model VP": 0, "player VP": 0,
    }
    assert mission_progress_signal(info) > 0.0


def test_mission_signal_negative_when_enemy_closer():
    info = {
        "az_cum_model_dist": 20.0, "az_cum_enemy_dist": 5.0,  # враг ближе
        "model health": [10], "player health": [10], "model VP": 0, "player VP": 0,
    }
    assert mission_progress_signal(info) < 0.0


def test_mission_signal_distance_absent_no_effect():
    # Без distance-ключей старое поведение: симметрия → 0.
    info = {"model controlled objectives": [1], "player controlled objectives": [1],
            "model health": [10], "player health": [10], "model VP": 1, "player VP": 1}
    assert abs(mission_progress_signal(info)) < 1e-9


# --- finalize_value_targets (wiring decision, без env) ------------------------

def test_finalize_outcome_only_win_sets_pure_value_and_info():
    info = {"winner": "model", "end reason": "turn_limit", "model VP": 5, "player VP": 1}
    targets, final_value, kind = finalize_value_targets(
        n_transitions=3, last_info=info, outcome_only=True,
        raw_final_value=0.0, win=WIN, loss=LOSS, draw=DRAW, coef=0.1,
    )
    assert kind == "win"
    assert final_value == WIN
    assert targets == [WIN, WIN, WIN]              # победа не сдвигается
    assert info["az_outcome_value"] == WIN          # чистый terminal в info
    assert info["az_outcome_kind"] == "win"


def test_finalize_outcome_only_draw_bootstraps_nonterminal_only():
    info = {"end reason": "turn_limit", "model VP": 0, "player VP": 0,
            "model controlled objectives": [1, 2, 3], "player controlled objectives": [],
            "model health": [10, 10], "player health": [1]}
    targets, final_value, kind = finalize_value_targets(
        n_transitions=4, last_info=info, outcome_only=True,
        raw_final_value=0.0, win=WIN, loss=LOSS, draw=DRAW, coef=0.1,
    )
    assert kind == "draw"
    assert final_value == DRAW
    assert targets[-1] == DRAW                      # терминал чистый
    assert all(t > DRAW for t in targets[:-1])      # нетерминальные сдвинуты вверх
    assert info["az_outcome_value"] == DRAW          # bootstrap не меняет terminal в info


def test_finalize_non_outcome_only_keeps_constant_raw_value():
    info = {"end reason": "turn_limit", "model controlled objectives": [1, 2, 3]}
    targets, final_value, kind = finalize_value_targets(
        n_transitions=3, last_info=info, outcome_only=False,
        raw_final_value=0.42, win=WIN, loss=LOSS, draw=DRAW, coef=0.1,
    )
    assert kind == ""
    assert final_value == 0.42
    assert targets == [0.42, 0.42, 0.42]            # shaped-путь не трогаем


# --- dense reward shaping (relaxed outcome_only) ------------------------------

def test_reward_shaping_weight_zero_returns_pure_outcome():
    t = build_reward_shaped_value_targets(
        rewards=[0.5, 0.3, 0.1], outcome_value=DRAW, weight=0.0,
    )
    assert t == [DRAW, DRAW, DRAW]


def test_reward_shaping_positive_rewards_raise_value():
    # Положительные per-step награды (прогресс к точке) → таргеты выше чистой ничьи.
    t = build_reward_shaped_value_targets(
        rewards=[0.4, 0.4, 0.4], outcome_value=DRAW, weight=0.3,
    )
    assert all(v > DRAW for v in t)
    # ранние состояния «видят» больше будущей награды → не ниже поздних
    assert t[0] >= t[-1] - 1e-9


def test_reward_shaping_negative_rewards_lower_value():
    t = build_reward_shaped_value_targets(
        rewards=[-0.4, -0.4, -0.4], outcome_value=DRAW, weight=0.3,
    )
    assert all(v < DRAW for v in t)


def test_reward_shaping_stays_bounded_and_outcome_dominant():
    # Огромные награды, но shaping ограничен tanh*weight → не флипает исход.
    t = build_reward_shaped_value_targets(
        rewards=[100.0] * 10, outcome_value=DRAW, weight=0.3,
    )
    for v in t:
        assert -1.0 <= v <= 1.0
        # ничья остаётся ничьёй: не дотягивает до полноценной победы
        assert v < WIN


def test_reward_shaping_win_outcome_with_shaping_stays_near_win():
    # При победе shaping не должен опускать значение далеко от +1.
    t = build_reward_shaped_value_targets(
        rewards=[0.1, 0.1], outcome_value=WIN, weight=0.3,
    )
    assert all(v <= WIN for v in t)
    assert all(v > 0.5 for v in t)


def test_reward_shaping_empty_rewards():
    assert build_reward_shaped_value_targets(rewards=[], outcome_value=DRAW, weight=0.3) == []
