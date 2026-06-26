"""Mission-bootstrap для AZ/GAZ self-play под outcome_only.

Зачем: при outcome_only весь эпизод получает один скалярный value-target
(win/loss/draw). Если ростер/оппонент почти всегда сводят партию к ничьей по
turn_limit (vp_diff≈0), таргет становится константой draw (-0.7) для всех
состояний → value-голова коллапсирует в -0.7, политика не получает градиента
«играй миссию». См. диагностику draw-rate в LOGS_FOR_AGENTS_TRAIN.md.

Что делаем (слабый, опциональный сигнал, по умолчанию ВЫКЛ):
- terminal outcome остаётся главным источником истины: win=+1, loss=-1,
  draw=outcome_value_draw. Терминальная (последняя) транзиция всегда «чистая».
- Победа/поражение НЕ трогаются вовсе → VP-win == wipeout-win == win_value
  (нельзя делать VP-win «хуже», иначе модель предпочтёт wipeout миссии).
- Только в ничьих НЕтерминальные транзиции слегка сдвигаются mission-сигналом
  в пределах draw-полосы, не приближаясь к полноценным win/loss.

Сигнал — относительное доминирование (в [-1, 1]): доминирует контроль точек
(objective control), VP-diff и остаточный HP — добавки. В ничьих VP-diff≈0,
поэтому различитель «хорошей»/«плохой» ничьи — именно контроль точек и HP.
"""
from __future__ import annotations

from typing import Any

import numpy as np

# Веса компонент mission-сигнала. Контроль точек доминирует (это и есть «играй
# миссию»); VP и HP — вторичны. Сумма = 1.0, чтобы сигнал жил в [-1, 1].
_W_OBJ = 0.6
_W_HP = 0.2
_W_VP = 0.2


def _sum_hp(raw: Any) -> float:
    """Суммарный HP стороны из info['model health']/['player health']."""
    if isinstance(raw, (list, tuple, np.ndarray)):
        try:
            return float(sum(float(x) for x in raw))
        except (TypeError, ValueError):
            return 0.0
    try:
        return float(raw or 0.0)
    except (TypeError, ValueError):
        return 0.0


def _share(model_val: float, enemy_val: float) -> float:
    """Относительное доминирование (model - enemy)/(|model|+|enemy|) ∈ [-1, 1].

    Без магических нормировок: масштаб-независимо, при равенстве/нулях → 0.0.
    """
    m = float(model_val)
    e = float(enemy_val)
    denom = abs(m) + abs(e)
    if denom <= 1e-9:
        return 0.0
    return float(np.clip((m - e) / denom, -1.0, 1.0))


def outcome_kind_from_info(info: dict | None) -> str:
    """'win' | 'loss' | 'draw' по финальному info.

    Та же семантика, что в outcome_only-блоке play_episode_with_mcts: победа —
    winner∈{model,learner,ai} или wipeout_enemy; поражение — winner∈{enemy,
    player,opponent} или wipeout_model; иначе ничья.
    """
    info = info or {}
    winner = str(info.get("winner", "") or "").strip().lower()
    end_reason = str(info.get("end reason", "") or "").strip().lower()
    if winner in {"model", "learner", "ai"} or end_reason == "wipeout_enemy":
        return "win"
    if winner in {"enemy", "player", "opponent"} or end_reason == "wipeout_model":
        return "loss"
    return "draw"


def terminal_outcome_value(
    info: dict | None, *, win: float, loss: float, draw: float
) -> float:
    """Чистый terminal-таргет: win/loss/draw. Bootstrap его НЕ меняет."""
    kind = outcome_kind_from_info(info)
    if kind == "win":
        return float(win)
    if kind == "loss":
        return float(loss)
    return float(draw)


def mission_progress_signal(
    info: dict | None, *, w_obj: float = _W_OBJ, w_hp: float = _W_HP, w_vp: float = _W_VP
) -> float:
    """Слабый сигнал «играю ли я миссию», нормированный в [-1, 1].

    Контроль точек берём НАКОПИТЕЛЬНО за партию (az_cum_model_ctrl/
    az_cum_enemy_ctrl — сумма по ходам), если он есть: терминальный снимок в
    turn_limit-ничьих почти всегда 0/0 и сигнал умирал. Фолбэк на терминальный
    снимок — для обратной совместимости (старый info / тесты).
    """
    info = info or {}
    cum_m = info.get("az_cum_model_ctrl")
    cum_e = info.get("az_cum_enemy_ctrl")
    if cum_m is not None and cum_e is not None:
        m_obj = float(cum_m or 0.0)
        e_obj = float(cum_e or 0.0)
    else:
        m_obj = len(info.get("model controlled objectives", []) or [])
        e_obj = len(info.get("player controlled objectives", []) or [])
    m_hp = _sum_hp(info.get("model health", []))
    e_hp = _sum_hp(info.get("player health", []))
    m_vp = float(info.get("model VP", 0) or 0)
    e_vp = float(info.get("player VP", 0) or 0)
    s = (
        float(w_obj) * _share(m_obj, e_obj)
        + float(w_hp) * _share(m_hp, e_hp)
        + float(w_vp) * _share(m_vp, e_vp)
    )
    return float(np.clip(s, -1.0, 1.0))


def draw_band(draw_value: float) -> float:
    """Полоса допустимого сдвига ничьей: половина расстояния до полноценного
    исхода. Для draw=-0.7 → 0.15 (нудж не выйдет за [-0.85, -0.55])."""
    return 0.5 * (1.0 - abs(float(draw_value)))


def build_value_targets(
    *,
    n_transitions: int,
    outcome_value: float,
    outcome_kind: str,
    info: dict | None,
    coef: float,
    draw_value: float,
) -> list[float]:
    """Per-transition value-targets под outcome_only.

    - терминальная (последняя) транзиция всегда = outcome_value (чистый исход);
    - при coef>0 и ничьей НЕтерминальные транзиции двигаются
      coef*mission_signal, клип в пределах draw-полосы;
    - победа/поражение не трогаются вовсе.

    coef<=0 или не-ничья → константа outcome_value (поведение как без bootstrap).
    """
    n = int(max(0, n_transitions))
    base = [float(outcome_value)] * n
    if float(coef) <= 0.0 or str(outcome_kind) != "draw" or n <= 1:
        return base
    signal = mission_progress_signal(info)
    band = draw_band(draw_value)
    nudge = float(np.clip(float(coef) * signal, -band, band))
    targets = [float(outcome_value) + nudge] * n
    targets[-1] = float(outcome_value)  # терминал остаётся чистым
    return targets


def finalize_value_targets(
    *,
    n_transitions: int,
    last_info: dict,
    outcome_only: bool,
    raw_final_value: float,
    win: float,
    loss: float,
    draw: float,
    coef: float,
) -> tuple[list[float], float, str]:
    """Единая точка решения value-таргетов эпизода (тестируется без env).

    - outcome_only: исход → чистый terminal value (+ mission-bootstrap по ничьим);
    - не outcome_only: таргеты = константа raw_final_value (shaped-путь, как раньше).

    Сайд-эффект: проставляет в last_info чистый terminal-таргет для [TRAIN][EP]:
    last_info['az_outcome_value'] и (если outcome_only) ['az_outcome_kind'].

    Возвращает (value_targets, final_value, outcome_kind).
    """
    final_value = float(raw_final_value)
    value_targets = [final_value] * int(max(0, n_transitions))
    outcome_kind = ""
    if outcome_only:
        win_c = float(np.clip(float(win), -1.0, 1.0))
        loss_c = float(np.clip(float(loss), -1.0, 1.0))
        draw_c = float(np.clip(float(draw), -1.0, 1.0))
        outcome_kind = outcome_kind_from_info(last_info)
        final_value = terminal_outcome_value(last_info, win=win_c, loss=loss_c, draw=draw_c)
        value_targets = build_value_targets(
            n_transitions=n_transitions,
            outcome_value=final_value,
            outcome_kind=outcome_kind,
            info=last_info,
            coef=float(coef),
            draw_value=draw_c,
        )
    if isinstance(last_info, dict):
        last_info["az_outcome_value"] = float(final_value)
        if outcome_kind:
            last_info["az_outcome_kind"] = str(outcome_kind)
    return value_targets, float(final_value), outcome_kind
