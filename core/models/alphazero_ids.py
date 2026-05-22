"""AlphaZero algorithm id helpers (alphazero_tree / alphazero_proxy)."""

from __future__ import annotations

VALID_TRAIN_ALGOS = frozenset({"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "distill"})
VALID_AZ_ALGOS = frozenset({"alphazero_tree", "alphazero_proxy"})
LEGACY_AZ_ALGO = "alphazero"


def is_az_algo(algo: str) -> bool:
    return str(algo or "").strip().lower() in VALID_AZ_ALGOS


def az_section_for(algo: str) -> str:
    key = str(algo or "").strip().lower()
    if key not in VALID_AZ_ALGOS:
        raise ValueError(f"expected alphazero_tree or alphazero_proxy, got {algo!r}")
    return key


def az_mcts_mode_for(algo: str) -> str:
    key = str(algo or "").strip().lower()
    if key == "alphazero_proxy":
        return "proxy"
    if key == "alphazero_tree":
        return "tree"
    raise ValueError(f"expected alphazero_tree or alphazero_proxy, got {algo!r}")


def az_mcts_mode_from_payload(algo: str, payload: dict | None = None) -> str:
    """Resolve MCTS mode from algo id and optional checkpoint/meta dict."""
    if is_az_algo(algo):
        meta_mode = ""
        if isinstance(payload, dict):
            meta_mode = str(payload.get("mcts_mode", "") or "").strip().lower()
        if meta_mode in {"tree", "proxy"}:
            return meta_mode
        return az_mcts_mode_for(algo)
    return "tree"
