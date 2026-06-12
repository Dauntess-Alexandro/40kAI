"""
Конфигурация reward-шэйпинга.
Меняйте значения здесь, чтобы не лезть в код среды.
"""

import json
import os

# =========================================
# Шэйпинг наград (победа / victory points)
# =========================================
# Бонус за победу в матче (начисляется в конце эпизода).
WIN_BONUS = 3.0
# Штраф за поражение в матче (начисляется в конце эпизода).
LOSS_PENALTY = 2.0

# С какого боевого раунда начинать начислять VP по миссии Only War.
VP_START_SCORING_ROUND = 1
# Ограничение максимального VP за одну фазу командования.
VP_CAP_PER_COMMAND = 3

# Награды, связанные с удержанием/контролем objectives.
# Бонус за удержание objective.
VP_OBJECTIVE_HOLD_REWARD = 1.0
# Штраф за упущенное удержание/прогресс по objective.
VP_OBJECTIVE_HOLD_PENALTY = 0.12
# Бонус за приближение к objective.
VP_OBJECTIVE_PROXIMITY_REWARD = 0.8
# Нормировочный знаменатель для штрафа за пропущенный прогресс:
# penalty = -VP_OBJECTIVE_HOLD_PENALTY * clamp01(missed_progress / VP_OBJECTIVE_MISSED_PROGRESS_NORM)
VP_OBJECTIVE_MISSED_PROGRESS_NORM = 6.0
# Масштаб бонуса за улучшение разницы VP (vp_diff > 0).
VP_DIFF_REWARD_SCALE = 0.14
# Масштаб штрафа за ухудшение разницы VP (vp_diff < 0).
VP_DIFF_PENALTY_SCALE = 0.14
# Доп. штраф за ничью на turn_limit (анти "ничейная яма").
TURN_LIMIT_DRAW_PENALTY = 3.2
# Доп. масштаб бонуса за победу по VP на turn_limit.
TURN_LIMIT_VP_MARGIN_REWARD_SCALE = 1.2
# Доп. масштаб штрафа за проигрыш по VP на turn_limit.
TURN_LIMIT_VP_MARGIN_PENALTY_SCALE = 0.75
# Ограничение абсолютного VP margin для turn_limit shaping.
TURN_LIMIT_VP_MARGIN_CLAMP = 6.0
# Длина серии удержания objective для streak-бонуса.
VP_OBJECTIVE_STREAK_LEN = 1
# Дополнительный бонус за достижение серии удержания objective.
VP_OBJECTIVE_STREAK_BONUS = 0.25
# Масштаб награды за изменение перевеса OC на objectives (delta по шагу).
VP_OBJECTIVE_OC_MARGIN_SCALE = 0.02
# Ограничение абсолютной delta по OC-margin (чтобы не раздувать шэйпинг).
VP_OBJECTIVE_OC_MARGIN_DELTA_CLAMP = 12.0
# Максимальный множитель линейного streak-бонуса (для глубокой серии удержания).
VP_OBJECTIVE_STREAK_LINEAR_CAP = 2.0

# ===============================
# Шэйпинг наград (прочие фазы)
# ===============================
# Бонус за успешное применение Insane Bravery в фазе командования.
COMMAND_INSANE_BRAVERY_REWARD = 0.5
# Штраф за неэффективное/ошибочное применение Insane Bravery.
COMMAND_INSANE_BRAVERY_PENALTY = 0.5
# Бонус в движении, если цель в мили уже уничтожена/достигнута выгодная ситуация.
MOVEMENT_MELEE_TARGET_DEAD_BONUS = 0.3
# Штраф за отступление из мили (fallback), когда это нежелательно.
MOVEMENT_MELEE_RETREAT_PENALTY = 0.5
# Бонус за удержание выгодного мили-контакта (stay in melee).
MOVEMENT_MELEE_STAY_BONUS = 0.1
# Бонус за успешный чардж.
CHARGE_SUCCESS_REWARD = 0.5
# Штраф за неуспешный чардж.
CHARGE_FAIL_PENALTY = 0.0

# =============================
# Шэйпинг наград (стрельба)
# =============================
# Масштаб награды за нанесённый урон в стрельбе.
SHOOT_REWARD_DAMAGE_SCALE = 0.6
# Фиксированный бонус за убийство модели/цели стрельбой.
SHOOT_REWARD_KILL_BONUS = 0.4
# Штраф за избыточный урон (overkill).
SHOOT_REWARD_OVERKILL_PENALTY = 0.2
# Штраф за пропуск стрельбы, когда действие ожидалось.
SHOOT_REWARD_SKIP_PENALTY = 0.15
# Доп. бонус за выбор цели с низким HP.
SHOOT_REWARD_TARGET_LOW_HP = 0.05
# Доп. бонус за урон/фокус по цели на objective.
SHOOT_REWARD_TARGET_ON_OBJ = 0.07
# Доп. бонус за урон/фокус по цели с высоким OC.
SHOOT_REWARD_TARGET_HIGH_OC = 0.05
# Доп. бонус за «правильное» action-решение в стрельбе (если используется).
SHOOT_REWARD_ACTION_BONUS = 0.0

# Масштаб штрафа за полученный урон в шаге модели
# (нормируется относительно суммарного максимального HP модели).
DAMAGE_TAKEN_SCALE = 0.32

# ==============================================
# Шэйпинг наград (objectives / utility-сигналы)
# ==============================================
# Штраф за бездействие вне целей (idle out of objective).
IDLE_OUT_OF_OBJECTIVE_PENALTY = 0.06
# Масштаб пошагового бонуса за прогресс к objective.
OBJECTIVE_PROGRESS_STEP_SCALE = 0.26
# Верхняя граница бонуса за прогресс к objective за шаг.
OBJECTIVE_PROGRESS_STEP_CAP = 0.35
# Штраф за "мертвое окно": нет валидных целей стрельбы и нет contest objective.
NO_TARGET_NO_CONTEST_PENALTY = 0.04
# Рост штрафа за "мертвое окно" по раундам после старта скоринга.
NO_TARGET_NO_CONTEST_ROUND_SCALE = 0.03
# Верхняя граница мультипликатора раундового роста для "мертвого окна".
NO_TARGET_NO_CONTEST_MAX_MULT = 2.0
# Бонус за убийство цели, находящейся на objective.
KILL_ON_OBJECTIVE_BONUS = 0.2
# Масштаб бонуса за нанесение урона цели на objective.
DAMAGE_ON_OBJECTIVE_SCALE = 0.05

# Контекстные штрафы за «пропуск» действий.
# Штраф за попытку стрельбы в невалидную/несуществующую цель.
SHOOT_REWARD_INVALID_TARGET_PENALTY = 0.20
# Штраф за пропуск чарджа при наличии валидных целей для чарджа.
CHARGE_SKIP_WITH_TARGETS_PENALTY = 0.00

# ===============================
# Шэйпинг наград (деплой / RL)
# ===============================
# RL deployment (Only War): вспомогательный сигнал качества расстановки.
# Используется как delta-глобального score: score_after - score_before.
# Бонус за валидный placement (по умолчанию нейтральный, т.к. mask-only).
DEPLOYMENT_RL_VALID_REWARD = 0.0
# Штраф за невалидный placement (по умолчанию нейтральный).
DEPLOYMENT_RL_INVALID_PENALTY = 0.0
# Общий масштаб delta-score в deploy-reward.
DEPLOYMENT_RL_SCORE_SCALE = 0.05

# Веса компонент глобального deployment score.
# Вклад «передней» постановки (готовность к выходу вперёд).
DEPLOYMENT_RL_FORWARD_W = 1.0
# Вклад покрытия линий (spread по row/y между своими юнитами).
DEPLOYMENT_RL_SPREAD_W = 0.6
# Вклад запаса до краёв карты (edge margin).
DEPLOYMENT_RL_EDGE_W = 0.2
# Вклад cover/terrain-компоненты (бонус за близость к укрытиям и отсутствие скученности).
DEPLOYMENT_RL_COVER_W = 0.35

# Нормировки компонент deployment score.
# Целевая дистанция spread по row/y (после неё эффект насыщается).
DEPLOYMENT_RL_SPREAD_TARGET = 6.0
# Целевой минимальный отступ модели до границы поля (в клетках).
DEPLOYMENT_RL_EDGE_MARGIN_TARGET = 2.0
# Радиус (Chebyshev) поиска ближайшего террейна для cover-бонуса.
DEPLOYMENT_RL_COVER_RADIUS = 2.0
# Нормировка количества «прикрытых» клеток отряда (после неё эффект насыщается).
DEPLOYMENT_RL_COVER_NEAR_TARGET = 3.0
# Нормировка штрафа за скученность рядом со своими моделями (после неё штраф насыщается).
DEPLOYMENT_RL_COVER_CONGESTION_TARGET = 6.0


# ======================================
# Terrain shaping (боевые шаги, RL step)
# ======================================
# Потенциал: r_potential = gamma * Φ(s') - Φ(s)
TERRAIN_POTENTIAL_GAMMA = 0.99
# Φ(s) = w_cover * cover_score + w_threat * threat_score + w_guard * guard_score
TERRAIN_POTENTIAL_W_COVER = 0.08
TERRAIN_POTENTIAL_W_THREAT = 0.10
TERRAIN_POTENTIAL_W_GUARD = 0.04

# Cover-score: INFANTRY + within 3" (Chebyshev/grid) от barricade + not fully visible.
TERRAIN_COVER_RADIUS = 3.0
# Нормировка cover-score по количеству живых юнитов.
TERRAIN_COVER_SCORE_NORM = 2.0

# Threat-score: только реальные угрозы (LOS + range + enemy_can_shoot).
TERRAIN_THREAT_COUNT_NORM = 3.0

# Guard-score: слабый сигнал охраны objective из cover.
TERRAIN_GUARD_RANGE_NORM = 12.0
TERRAIN_GUARD_PROGRESS_BONUS = 0.20

# Event-бонус за выстрел из cover при не-росте угрозы, 1 раз за ход/юнит.
TERRAIN_EVENT_SHOT_FROM_COVER_BONUS = 0.03

# Exposure penalty: fully_visible=True при наличии реальной угрозы.
TERRAIN_EXPOSURE_PENALTY = 0.02

# Митигировать штраф за полученный урон, если модель в cover под угрозой.
# Итоговый множитель: penalty *= clamp(1 - K * cover_score_after, min=MIN_MULT, max=1)
TERRAIN_DAMAGE_TAKEN_COVER_MITIGATION_K = 0.25
TERRAIN_DAMAGE_TAKEN_COVER_MITIGATION_MIN_MULT = 0.75

# Микробонус: если cover_score вырос И модель реально двигалась в этот шаг.
TERRAIN_MOVE_INTO_COVER_BONUS_SCALE = 0.03

# Командный бонус: доля живых INFANTRY (под угрозой) в cover.
TERRAIN_TEAM_COVER_THRESHOLD = 0.50
TERRAIN_TEAM_COVER_BONUS = 0.02

# Анти-абьюз: clamp суммарного terrain-shaping за шаг.
TERRAIN_SHAPING_STEP_RCAP = 0.12


# ==========================================
# Anti-draw / mission pressure (Only War)
# ==========================================
# Доп. штраф, если после старта скоринга никто не contest'ит objectives
# (обе стороны имеют 0 OC на всех objectives). Это ломает "вечные" бои в стороне от миссии.
MISSION_NO_CONTEST_PENALTY = 0.20
# С какого battle round включать этот штраф (обычно совпадает со START_SCORING_ROUND).
MISSION_NO_CONTEST_START_ROUND = VP_START_SCORING_ROUND
# После этого раунда штраф мягко усиливается (динамика late-game anti-draw).
MISSION_NO_CONTEST_LATE_ROUND = 10
# +15% к базовому штрафу после LATE_ROUND (0.10..0.15 обычно достаточно).
MISSION_NO_CONTEST_LATE_MULT = 1.25

# Anti-stall по VP diff: если серия шагов без изменения VP слишком длинная.
VP_STALL_STEPS_THRESHOLD = 5
VP_STALL_PENALTY = 0.08
VP_STALL_STEP_GROWTH = 0.08
VP_STALL_PENALTY_MAX_MULT = 2.0

# Anti-loop по повторяющимся action tuples (move/attack/shoot/charge/use_cp/cp_on)
# Штраф включается при длинной серии одинаковых действий.
ACTION_REPEAT_STEPS_THRESHOLD = 3
ACTION_REPEAT_PENALTY = 0.04
ACTION_REPEAT_STEP_GROWTH = 0.20
ACTION_REPEAT_PENALTY_MAX_MULT = 2.5
# 1: применять только если у модели были реальные альтернативы (move>1 или shoot>1)
ACTION_REPEAT_REQUIRE_OPTIONS = 1

# Round-aware scaling: ранняя игра = больше прогресса к objective; поздняя = удержание/deny.
REWARD_ROUND_EARLY_END = 4
REWARD_ROUND_LATE_START = 10
REWARD_PROGRESS_EARLY_MULT = 1.15
REWARD_PROGRESS_LATE_MULT = 1.00
REWARD_HOLD_EARLY_MULT = 0.95
REWARD_HOLD_LATE_MULT = 1.08


# =========================
# Шэйпинг наград (ближний бой)
# =========================
# Масштаб награды за нанесённый урон в ближнем бою.
MELEE_REWARD_DAMAGE_SCALE = 0.6
# Фиксированный бонус за убийство в ближнем бою.
MELEE_REWARD_KILL_BONUS = 0.4
# Масштаб штрафа за полученный урон в ближнем бою.
MELEE_REWARD_TAKEN_SCALE = 0.5
# Масштаб бонуса/штрафа за advantage в ближнем бою.
MELEE_ADVANTAGE_SCALE = 0.15
# Масштаб компоненты «сила позиции/отряда» в ближнем бою.
MELEE_STRENGTH_SCALE = 0.1
# Масштаб бонуса за контроль objective через ближний бой.
MELEE_OBJECTIVE_CONTROL_SCALE = 0.2

# ===========================================
# Enemy heuristic (профили и matchup-дистанция)
# ===========================================
# Порог разницы между ranged/melee профилями для роли юнита.
ENEMY_HEUR_PROFILE_GAP_THRESHOLD = 0.05
# Буфер дистанции для режима kite (ranged vs melee).
ENEMY_HEUR_KITE_BUFFER = 3.0
# Веса компонент enemy movement heuristic (matchup-aware).
ENEMY_HEUR_MATCHUP_DIST_W = 0.38
ENEMY_HEUR_TARGET_DIST_W = 0.26
ENEMY_HEUR_MODE_W = 0.16
ENEMY_HEUR_PROGRESS_W = 0.15
ENEMY_HEUR_OBJECTIVE_DIST_W = 0.14
ENEMY_HEUR_OBJECTIVE_CONTROL_W = 0.42
ENEMY_HEUR_RISK_W = 0.18
ENEMY_HEUR_COVER_W = 0.18
ENEMY_HEUR_LOOKAHEAD_TOP_K = 4
ENEMY_HEUR_LOOKAHEAD_W = 0.30
ENEMY_HEUR_TEAM_FOCUS_PENALTY_W = 0.12
ENEMY_HEUR_OBJECTIVE_PRESSURE_W = 0.18
ENEMY_HEUR_THREAT_W = 0.18

# Feature flags / strategy layers
ENEMY_HEUR_ROLE_SWITCH_ENABLED = 1
ENEMY_HEUR_LOW_HP_THRESHOLD = 0.45
ENEMY_HEUR_HIGH_RISK_THRESHOLD = 0.55
ENEMY_HEUR_TEAM_TACTIC_ENABLED = 1
ENEMY_HEUR_OBJECTIVE_CONTROL_ENABLED = 1
ENEMY_HEUR_LOOK2_ENABLED = 1
ENEMY_HEUR_LOOK2_TOP_K = 3
ENEMY_HEUR_LOOK2_FUTURE_W = 0.35
ENEMY_HEUR_LOOK2_RISK_W = 0.20
ENEMY_HEUR_THREAT_MAP_CACHE = 1
# Phase 7: профили-«характеры» врага между партиями (balanced/kiter/aggressor/
# objective/turtle), выбор по seed на reset. Curriculum-разнообразие стилей движения.
ENEMY_HEUR_PROFILE_RANDOMIZATION_ENABLED = 1
# First-class метрики эвристики: env копит счётчики решений (mode/role/risk/charge) и
# пишет per-game JSONL в artifacts/metrics/heur_decisions/. Не зависит от HEURISTIC_DEBUG.
# Отчёт: python tools/heur_metrics_report.py
ENEMY_HEUR_METRICS_ENABLED = 1
# LoS-гейт risk/threat: огонь model-стрелка учитывается только при реальной линии
# видимости до клетки (террейн/стены укрывают). Лечит гибель эвристики вайпаутом.
ENEMY_HEUR_LOS_GATE_ENABLED = 1

# Веса выбора целей для enemy heuristic (стрельба/чардж).
ENEMY_HEUR_SHOOT_KILL_W = 0.45
ENEMY_HEUR_SHOOT_DAMAGE_W = 0.30
ENEMY_HEUR_SHOOT_OBJECTIVE_W = 0.15
ENEMY_HEUR_SHOOT_OVERKILL_W = 0.18
ENEMY_HEUR_CHARGE_MATCHUP_W = 0.40
ENEMY_HEUR_CHARGE_DISTANCE_W = 0.35
ENEMY_HEUR_CHARGE_OBJECTIVE_W = 0.25

# EV target-selection (enemy heuristic)
ENEMY_HEUR_SHOOT_EV_KILL_VALUE_W = 1.00
ENEMY_HEUR_SHOOT_EV_DMG_VALUE_W = 0.95
ENEMY_HEUR_SHOOT_EV_RETURN_RISK_W = 0.45
# Charge-EV v2: реальная 2d6-вероятность успеха + EV рукопашного размена
# (expected_damage melee в обе стороны) вместо фейковой кривой и абстрактного delta.
ENEMY_HEUR_CHARGE_EV_V2_ENABLED = 1
# Skip явно суицидального чарджа (best trade < TRADE_MIN). DEFAULT OFF — это
# поведенческое изменение, требует A/B (включать вместе с замером). Нужен EV_V2.
ENEMY_HEUR_CHARGE_SKIP_BAD_ENABLED = 0
ENEMY_HEUR_CHARGE_SKIP_TRADE_MIN = -0.5
ENEMY_HEUR_CHARGE_EV_SUCCESS_W = 1.15
ENEMY_HEUR_CHARGE_EV_LOCK_W = 0.35
ENEMY_HEUR_CHARGE_EV_COUNTER_W = 0.25

# Quota logic: минимальные доли режимов движения при подходящих условиях
ENEMY_HEUR_MODE_QUOTA_ENABLED = 1
ENEMY_HEUR_MODE_QUOTA_START_ROUND = 3
ENEMY_HEUR_MODE_QUOTA_MIN_KITE_RATIO = 0.04
ENEMY_HEUR_MODE_QUOTA_MIN_COMMIT_RATIO = 0.06
ENEMY_HEUR_MODE_QUOTA_COMMIT_DELTA_MIN = 0.04
ENEMY_HEUR_MODE_QUOTA_ONLY_WHEN_BEHIND = 1
ENEMY_HEUR_MODE_QUOTA_MAX_RISK = 0.52
ENEMY_HEUR_MODE_QUOTA_MIN_TARGET_DIST = 5.5

# Phase calibration (early/mid/late): динамика весов по раундам
ENEMY_HEUR_PHASE_CALIBRATION_ENABLED = 1
ENEMY_HEUR_EARLY_MAX_ROUND = 2
ENEMY_HEUR_MID_MAX_ROUND = 3
ENEMY_HEUR_EARLY_RISK_MULT = 1.03
ENEMY_HEUR_EARLY_OBJ_MULT = 0.98
ENEMY_HEUR_EARLY_MODE_MULT = 1.0
ENEMY_HEUR_MID_RISK_MULT = 1.0
ENEMY_HEUR_MID_OBJ_MULT = 1.0
ENEMY_HEUR_MID_MODE_MULT = 1.0
ENEMY_HEUR_LATE_RISK_MULT = 0.97
ENEMY_HEUR_LATE_OBJ_MULT = 1.08
ENEMY_HEUR_LATE_MODE_MULT = 0.99


_HEUR_CALIBRATION_BLOCKED_SUFFIXES = ("_ENABLED", "_TOP_K", "_CACHE")


def _validate_heur_calibration_override(name: str, value) -> float:
    key = str(name or "").strip()
    if not key.startswith("ENEMY_HEUR_"):
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: key {key!r} must start with ENEMY_HEUR_.")
    if key.endswith(_HEUR_CALIBRATION_BLOCKED_SUFFIXES):
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: key {key!r} is a feature flag/cache/top-k value, not a Phase 8 weight.")
    if key not in globals():
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: unknown reward_config key {key!r}.")
    current = globals()[key]
    if isinstance(current, bool) or not isinstance(current, (int, float)):
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: key {key!r} is not numeric.")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: value for {key!r} must be numeric.") from exc
    if parsed < 0.0:
        raise ValueError(f"HEUR_CALIBRATION_OVERRIDES_JSON: value for {key!r} must be >= 0.")
    return parsed


def apply_heur_calibration_overrides(raw_json: str | None = None) -> dict[str, float]:
    raw = os.getenv("HEUR_CALIBRATION_OVERRIDES_JSON", "") if raw_json is None else str(raw_json or "")
    raw = raw.strip()
    if not raw:
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("HEUR_CALIBRATION_OVERRIDES_JSON: invalid JSON object.") from exc
    if not isinstance(payload, dict):
        raise ValueError("HEUR_CALIBRATION_OVERRIDES_JSON: expected JSON object.")

    applied: dict[str, float] = {}
    for key, value in payload.items():
        parsed = _validate_heur_calibration_override(str(key), value)
        current = globals()[str(key)]
        globals()[str(key)] = int(parsed) if isinstance(current, int) and float(parsed).is_integer() else float(parsed)
        applied[str(key)] = float(parsed)
    return applied


_HEUR_CALIBRATION_APPLIED_OVERRIDES = apply_heur_calibration_overrides()
