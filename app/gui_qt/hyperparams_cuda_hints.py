"""CUDA-dependent hyperparameter fields — подсветка и блокировка в Qt Settings."""

from __future__ import annotations

# Состояния для QML (hyperparam_cuda_field_state).
CUDA_FIELD_NEUTRAL = 0
CUDA_FIELD_OK = 1
CUDA_FIELD_MISSING = 2

CUDA_FIELD_OK_SUFFIX = "\n\n✓ CUDA доступна — параметр используется на GPU."
CUDA_FIELD_MISSING_SUFFIX = (
    "\n\n⚠ Требуется CUDA. Без GPU train переключится на CPU fallback "
    "(см. [GMZ][CONFIG][FALLBACK] в LOGS_FOR_AGENTS_TRAIN.md)."
)

# Поля, относящиеся к GPU-пути (подсветка зелёным при CUDA, красным при конфликте).
CUDA_RELATED_KEYS: dict[str, frozenset[str]] = {
    "gmz": frozenset(
        {
            "inference_server_enabled",
            "inference_server_compile",
            "learner_compile",
            "actor_device",
            "actor_max_cuda",
        }
    ),
    "dqn": frozenset(),
    "ppo": frozenset(),
    "tree": frozenset(),
    "proxy": frozenset(),
}


def gmz_value_requires_cuda(key: str, value) -> bool:
    """True, если при таком значении train ожидает CUDA."""
    k = str(key or "").strip()
    if k == "inference_server_enabled":
        return int(value or 0) == 1
    if k in ("inference_server_compile", "learner_compile"):
        return int(value or 0) == 1
    if k == "actor_device":
        v = str(value or "").strip().lower()
        return v in ("cuda", "inference_server")
    if k == "actor_max_cuda":
        return int(value or 0) > 0
    return False


def hyperparam_cuda_field_state(
    algo_section: str,
    key: str,
    value,
    cuda_available: bool,
) -> int:
    section = str(algo_section or "").strip().lower()
    k = str(key or "").strip()
    related = CUDA_RELATED_KEYS.get(section, frozenset())
    if k not in related:
        return CUDA_FIELD_NEUTRAL
    if cuda_available:
        return CUDA_FIELD_OK
    if section == "gmz" and gmz_value_requires_cuda(k, value):
        return CUDA_FIELD_MISSING
    return CUDA_FIELD_NEUTRAL


def would_gmz_hyperparam_violate_cuda(key: str, value, cuda_available: bool) -> bool:
    if cuda_available:
        return False
    return gmz_value_requires_cuda(str(key or "").strip(), value)


def hyperparam_cuda_tooltip_suffix(
    algo_section: str,
    key: str,
    value,
    cuda_available: bool,
) -> str:
    state = hyperparam_cuda_field_state(algo_section, key, value, cuda_available)
    if state == CUDA_FIELD_OK:
        return CUDA_FIELD_OK_SUFFIX
    if state == CUDA_FIELD_MISSING:
        return CUDA_FIELD_MISSING_SUFFIX
    return ""
