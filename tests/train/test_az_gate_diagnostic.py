"""AZ GATE: мёртвая ветка (запись latest_az_*_opponent.pth + лог [AZ][GATE]) удалена.

gate_pass остаётся как чистая диагностика DET-eval (аннотация в det-eval JSON):
оппонент AZ фиксирован весь прогон, файл-оппонент никем не читался.
"""

from __future__ import annotations

import train


def _payload(win: float, turn_limit: float, draw: float) -> dict:
    return {"win_rate": win, "turn_limit_rate": turn_limit, "draw_rate": draw}


def test_gate_pass_when_all_thresholds_met():
    assert train._az_det_eval_gate_pass(_payload(win=0.50, turn_limit=0.10, draw=0.10)) is True


def test_gate_blocked_on_low_win_rate():
    assert train._az_det_eval_gate_pass(_payload(win=0.10, turn_limit=0.10, draw=0.10)) is False


def test_gate_blocked_on_high_turn_limit_rate():
    assert train._az_det_eval_gate_pass(_payload(win=0.90, turn_limit=0.99, draw=0.10)) is False


def test_gate_blocked_on_high_draw_rate():
    assert train._az_det_eval_gate_pass(_payload(win=0.90, turn_limit=0.10, draw=0.99)) is False


def test_gate_defaults_blocked_on_empty_payload():
    assert train._az_det_eval_gate_pass({}) is False


def test_train_source_has_no_dead_az_gate_branch():
    with open(train.__file__, encoding="utf-8") as f:
        src = f.read()
    assert "_opponent.pth" not in src, (
        "latest_az_*_opponent.pth не должен записываться: файл никем не читается (мёртвый GATE)"
    )
    assert "[AZ][GATE]" not in src, (
        "лог [AZ][GATE] pass/blocked удалён; gate_pass — только аннотация в det-eval JSON"
    )
