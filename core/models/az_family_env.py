"""Резолв env-флагов AZ-семейства с приоритетом GAZ_* → AZ_* → default.

Gumbel AlphaZero (gumbel_az, GAZ) едет на общей AZ-инфраструктуре (та же сеть
AlphaZeroPolicyValueNet, общие _main_actor_learner_alphazero/_az_env_worker_entry),
но управляется собственными GAZ_* env-флагами — чтобы не пересекаться с AZ-запусками
на той же машине/ПК2 (свои порты 5565/5567).

Правило резолва (для gumbel_az):  GAZ_*  →  AZ_*  →  default.
Для остальных алго (alphazero_tree/proxy и пр.) GAZ_* игнорируется — поведение AZ
не меняется (эквивалентно os.getenv(az_key, default)).
"""

from __future__ import annotations

import os
from collections.abc import Callable


def resolve_az_family_env[T](
    gaz_key: str,
    az_key: str,
    default: T,
    *,
    is_gumbel: bool,
    getenv: Callable[[str], str | None] = os.getenv,
) -> str | T:
    """Вернуть значение env по приоритету GAZ_* → AZ_* → default.

    - gaz_key: имя GAZ-env (учитывается только при is_gumbel=True);
    - az_key: имя AZ-env (fallback);
    - default: значение, если ни один env не задан;
    - is_gumbel: TRAIN_ALGO == gumbel_az;
    - getenv: инъекция для тестов (по умолчанию os.getenv).

    Пустая строка в env считается явно заданным значением (не None) и используется.
    """
    if is_gumbel:
        gaz_val = getenv(gaz_key)
        if gaz_val is not None:
            return gaz_val
    az_val = getenv(az_key)
    if az_val is not None:
        return az_val
    return default
