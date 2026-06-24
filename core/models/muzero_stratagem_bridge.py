"""MuZero (GMZ/SMZ) ↔ умные реакции-стратагемы.

Ставит value-gate реакций (make_reaction_value_policy) в env.reaction_policy, используя
локальную MuZero-сеть (value через net.infer — фолбэк в env._reaction_net_value). Только
локальный режим (есть search.net); при remote inference гейт не ставится.
"""
from __future__ import annotations

import os

from core.models.utils import unwrap_env

_TRUTHY = frozenset({"1", "true", "yes", "on"})


def muzero_reaction_value_policy_enabled(flag_env: str, default: str = "1") -> bool:
    return str(os.getenv(flag_env, default)).strip().lower() in _TRUTHY


def install_muzero_reaction_policy(
    env, net, *, both_sides: bool = True, log_tag: str = "GMZ", log_fn=None
) -> bool:
    """Поставить value-gate реакций на env. net=None → no-op (False).

    Ошибка install не валит обучение: WARN-лог + возврат False (legacy-реакции).
    """
    if net is None:
        return False
    try:
        import torch

        from core.models.reaction_value_policy import make_reaction_value_policy

        try:
            device = next(net.parameters()).device
        except (StopIteration, AttributeError):
            device = torch.device("cpu")
        e = unwrap_env(env)
        e._reaction_net_by_side = {"model": net, "enemy": net} if both_sides else {"model": net}
        e.reaction_policy = make_reaction_value_policy(e._reaction_net_by_side, device=device)
        msg = f"[{log_tag}][REACTION] reaction_value_policy=ON (both_sides={both_sides})"
        (log_fn or print)(msg)
        return True
    except Exception as exc:  # noqa: BLE001 — install не должен ронять обучение
        msg = (
            f"[{log_tag}][REACTION][WARN] установка reaction_value_policy не удалась "
            f"(muzero_stratagem_bridge.install_muzero_reaction_policy): {exc}. "
            f"Продолжаем на legacy-реакциях."
        )
        (log_fn or print)(msg)
        return False


def maybe_install_muzero_reactions(
    env, *, search, inference_fn, flag_env: str, log_tag: str, log_fn=None
) -> bool:
    """Решение об install: флаг ВКЛ + локальный режим (search есть). Иначе skip."""
    if not muzero_reaction_value_policy_enabled(flag_env):
        return False
    if search is None or inference_fn is not None:
        (log_fn or print)(
            f"[{log_tag}][REACTION] skip: remote inference (local-only feature)"
        )
        return False
    net = getattr(search, "net", None)
    return install_muzero_reaction_policy(env, net, both_sides=True, log_tag=log_tag, log_fn=log_fn)
