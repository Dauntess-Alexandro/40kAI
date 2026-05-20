"""Shared design tokens for 40kAI GUI and viewer."""

from theme.loader import (
    TOKENS_PATH,
    load_tokens,
    load_tokens_flat_for_qml,
    validate_tokens,
)

__all__ = [
    "TOKENS_PATH",
    "load_tokens",
    "load_tokens_flat_for_qml",
    "validate_tokens",
]
