"""Stage 8.1: опциональные observation-фичи фаз/CP/стратагем.

Включается env `PHASE_OBS_FEATURES=1` (дефолт 0 — старый размер obs).
"""

from __future__ import annotations

import os

from core.engine.phases.stratagems import REGISTRY, Trigger, legal_stratagem_options
from core.engine.phases.types import ActionKind, Phase, Timing

_PHASE_ORDER: tuple[Phase, ...] = (
    Phase.COMMAND,
    Phase.MOVEMENT,
    Phase.SHOOTING,
    Phase.CHARGE,
    Phase.FIGHT,
    Phase.SCORING,
)

_ENV_PHASE_TO_ENUM: dict[str, Phase] = {p.value: p for p in _PHASE_ORDER}

_STRATAGEM_IDS: tuple[str, ...] = tuple(d.id for d in REGISTRY)

# one-hot phase(6) + timing main/reaction(2) + cp_norm self/opp(2)
# + stratagem_available(|REGISTRY|) + stratagem_used_this_phase(|REGISTRY|)
_PHASE_ONE_HOT_SIZE = len(_PHASE_ORDER)
_TIMING_SIZE = 2
_CP_NORM_SIZE = 2
_STRATAGEM_BLOCK_SIZE = len(_STRATAGEM_IDS)

PHASE_OBS_EXTENSION_SIZE = (
    _PHASE_ONE_HOT_SIZE + _TIMING_SIZE + _CP_NORM_SIZE + _STRATAGEM_BLOCK_SIZE + _STRATAGEM_BLOCK_SIZE
)

_CP_NORM_DENOM = 12.0


_TRUTHY = {"1", "true", "yes", "on"}


def phase_obs_features_enabled(explicit: bool | None = None) -> bool:
    if explicit is not None:
        return bool(explicit)
    raw = str(os.getenv("PHASE_OBS_FEATURES", "0")).strip().lower()
    return raw in _TRUTHY


def resolve_phase_obs_features(*, env_value: str | None, cfg_value) -> bool:
    """Резолв флага phase_obs_features: env-переменная приоритетнее hyperparams.

    `env_value` — сырое значение `PHASE_OBS_FEATURES` (или None/пустая строка, если не задано);
    `cfg_value` — значение из hyperparams `alphazero_tree.phase_obs_features` (0/1/bool/str).
    Используется в train/eval/GUI, чтобы значение совпадало во всех путях.
    """
    if env_value is not None and str(env_value).strip() != "":
        return str(env_value).strip().lower() in _TRUTHY
    return str(cfg_value).strip().lower() in _TRUTHY


def describe_obs_dim_mismatch(*, checkpoint_obs_dim: int, current_obs_dim: int) -> str | None:
    """Понятная ошибка при несовпадении размера obs (чекпойнт ↔ текущий env).

    Возвращает None, если размеры совпадают. Иначе — RU-сообщение (что/где/что делать).
    Если разница ровно PHASE_OBS_EXTENSION_SIZE — подсказываем переключить флаг phase_obs_features.
    """
    ckpt = int(checkpoint_obs_dim)
    cur = int(current_obs_dim)
    if ckpt == cur:
        return None
    base = (
        f"Размер obs не совпадает: чекпойнт={ckpt}, текущий env={cur}. "
        "Где: resume AlphaZero (train.py). "
    )
    if abs(ckpt - cur) == PHASE_OBS_EXTENSION_SIZE:
        ckpt_flag = "1" if ckpt > cur else "0"
        return (
            base
            + f"Разница = {PHASE_OBS_EXTENSION_SIZE} dims (phase_obs_features). "
            + f"Что делать: задайте phase_obs_features={ckpt_flag} (env PHASE_OBS_FEATURES={ckpt_flag}), "
            "как при обучении этого чекпойнта, либо начните обучение с нуля."
        )
    return base + "Что делать: укажите чекпойнт той же архитектуры/ростера или начните с нуля."


def obs_dim_mismatch_message(expected: int, actual: int) -> str | None:
    """RU-сообщение для remote IS при несовпадении obs_dim сети и входящего запроса.

    None, если размеры совпадают. Иначе — понятная подсказка (вместо cryptic mat1/mat2 ошибки):
    что случилось + что делать (перегенерить search_cfg, удалить старые веса, перезапустить).
    """
    if int(expected) == int(actual):
        return None
    return (
        f"[REMOTE_IS] obs_dim сети={int(expected)} != запрос={int(actual)}. "
        "Перегенери search_cfg на ПК1 (tools\\write_*_remote_search_cfg.bat) и удали старые "
        "latest_*_policy.pth на шаре, затем перезапусти сервер."
    )


def matmul_obs_mismatch_hint(exc_str: str) -> str | None:
    """Превратить cryptic torch-ошибку matmul (obs не совпал) в понятную RU-подсказку.

    None, если это не похоже на shape-mismatch входа. Парсит '(1x41 and 17x256)':
    actual obs=41, ожидаемый вход сети=17 → obs_dim_mismatch_message.
    """
    import re

    s = str(exc_str)
    if "mat1 and mat2" not in s and "cannot be multiplied" not in s:
        return None
    m = re.search(r"\(\d+x(\d+) and (\d+)x", s)
    if m:
        actual, expected = int(m.group(1)), int(m.group(2))
        msg = obs_dim_mismatch_message(expected, actual)
        if msg:
            return msg
    return (
        f"[REMOTE_IS] вход сети не совпал по размеру obs ({s}). "
        "Перегенери search_cfg на ПК1 (tools\\write_*_remote_search_cfg.bat) и удали старые "
        "latest_*_policy.pth на шаре, затем перезапусти сервер."
    )


def base_observation_length(n_model: int, n_enemy: int, n_objective_points: int) -> int:
    """Фактическая длина базового вектора get_observation_for_side (без phase-расширения)."""
    return int(n_model) * 3 + 1 + int(n_enemy) * 3 + 1 + int(n_objective_points) * 2 + 1


def legacy_observation_space_size(n_model: int, n_enemy: int, n_objective_points: int) -> int:
    """Размер observation_space при PHASE_OBS_FEATURES=0 (историческая формула)."""
    return int(n_model) * 3 + int(n_enemy) * 3 + int(n_objective_points) * 2 + 1


def build_phase_obs_signature_suffix(enabled: bool) -> str:
    if not enabled:
        return ""
    return f"+phase{PHASE_OBS_EXTENSION_SIZE}"


def _unwrap(env):
    return getattr(env, "unwrapped", env)


def _alive_indices(health) -> list[int]:
    return [i for i, hp in enumerate(health) if hp > 0]


def _phase_enum(env) -> Phase:
    e = _unwrap(env)
    return _ENV_PHASE_TO_ENUM.get(str(getattr(e, "phase", "command") or "command"), Phase.COMMAND)


def _timing_one_hot(env) -> tuple[float, float]:
    e = _unwrap(env)
    timing = str(getattr(e, "phase_timing", Timing.MAIN.value) or Timing.MAIN.value).lower()
    if timing == Timing.REACTION.value:
        return 0.0, 1.0
    return 1.0, 0.0


def _cp_pair_for_side(env, side: str) -> tuple[float, float]:
    e = _unwrap(env)
    if side == "model":
        self_cp = float(getattr(e, "modelCP", 0) or 0)
        opp_cp = float(getattr(e, "enemyCP", 0) or 0)
    else:
        self_cp = float(getattr(e, "enemyCP", 0) or 0)
        opp_cp = float(getattr(e, "modelCP", 0) or 0)
    denom = max(1.0, _CP_NORM_DENOM)
    return min(1.0, self_cp / denom), min(1.0, opp_cp / denom)


def _stratagem_available_flags(env, side: str) -> list[float]:
    e = _unwrap(env)
    phase = _phase_enum(e)
    health = e.unit_health if side == "model" else e.enemy_health
    alive = _alive_indices(health)
    available: set[str] = set()
    for trigger in Trigger:
        for opt in legal_stratagem_options(
            e,
            side,
            phase=phase,
            trigger=trigger,
            candidate_unit_idxs=alive,
        ):
            if opt.kind is ActionKind.USE_STRATAGEM:
                sid = str(opt.meta.get("stratagem_id", "") or "")
                if sid:
                    available.add(sid)
    return [1.0 if sid in available else 0.0 for sid in _STRATAGEM_IDS]


def _stratagem_used_this_phase_flags(env, side: str) -> list[float]:
    e = _unwrap(env)
    phase_name = str(getattr(e, "phase", "") or "")
    battle_round = int(getattr(e, "battle_round", 1) or 1)
    counts = {sid: 0 for sid in _STRATAGEM_IDS}
    for rec in list(getattr(e, "stratagem_used", None) or []):
        if len(rec) < 4:
            continue
        rec_side, sid, rec_round, rec_phase = rec[0], rec[1], rec[2], rec[3]
        if str(rec_side) != side or str(sid) not in counts:
            continue
        if int(rec_round) == battle_round and str(rec_phase) == phase_name:
            counts[str(sid)] += 1
    return [min(1.0, counts[sid] / 3.0) for sid in _STRATAGEM_IDS]


def phase_obs_vector(env, side: str) -> list[float]:
    """Вектор phase/CP/стратагем-фич (длина PHASE_OBS_EXTENSION_SIZE)."""
    e = _unwrap(env)
    phase = _phase_enum(e)
    phase_oh = [1.0 if p is phase else 0.0 for p in _PHASE_ORDER]
    timing = list(_timing_one_hot(e))
    cp_norm = list(_cp_pair_for_side(e, side))
    avail = _stratagem_available_flags(e, side)
    used = _stratagem_used_this_phase_flags(e, side)
    return [*phase_oh, *timing, *cp_norm, *avail, *used]


def append_phase_obs_features(env, side: str, obs: list) -> None:
    obs.extend(phase_obs_vector(env, side))
