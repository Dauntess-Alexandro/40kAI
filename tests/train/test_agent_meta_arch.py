# tests/train/test_agent_meta_arch.py
"""Source-guard: каждый non-DQN extra_meta в train.py должен нести "arch".

Связано с планом docs/superpowers/plans/2026-06-25-eval-arch-parity.md (Task 6):
eval читает "arch" из registry-meta, чтобы строить оппонента/learner 1:1.
DQN намеренно исключён — его арка инферится из state_dict.
"""
import re
from pathlib import Path


def _extra_meta_blocks(src: str) -> list[str]:
    # Грубо выделяем тело каждого extra_meta={ ... } (до парной }), для проверки наличия "arch".
    blocks = []
    for m in re.finditer(r"extra_meta=\{", src):
        i = m.end()
        depth = 1
        while i < len(src) and depth:
            depth += src[i] == "{"
            depth -= src[i] == "}"
            i += 1
        blocks.append(src[m.start():i])
    return blocks


# Маркеры, по которым блок относится к конкретному non-DQN алгоритму.
# AZ final использует "algo": TRAIN_ALGO (без буквального 'alphazero'),
# поэтому дополнительно ловим его по "mcts_mode"/AZ_MCTS_MODE.
_ALGO_MARKERS = (
    "ppo",
    "alphazero",
    "gumbel_muzero",
    "sampled_muzero",
    "mcts_mode",
    "AZ_MCTS_MODE",
)


def test_train_writes_arch_into_agent_meta():
    src = Path("train.py").read_text(encoding="utf-8")
    blocks = _extra_meta_blocks(src)
    assert blocks, "не найдено ни одного extra_meta={...} в train.py"
    # У каждого алго-агента (кроме dqn) extra_meta должен нести 'arch'.
    for b in blocks:
        m = re.search(r'"algo":\s*"([^"]+)"', b) or re.search(r'"algo":\s*([A-Z_]+)', b)
        algo = (m.group(1) if m else "").lower()
        if "dqn" in algo:
            continue
        if any(a in b for a in _ALGO_MARKERS):
            assert '"arch"' in b, f"extra_meta без arch для блока:\n{b[:200]}"
