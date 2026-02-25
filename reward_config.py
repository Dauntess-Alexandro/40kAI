"""
Конфигурация reward-шэйпинга.
Меняйте значения здесь, чтобы не лезть в код среды.
"""

# =========================================
# Шэйпинг наград (победа / victory points)
# =========================================
# Бонус за победу в матче (начисляется в конце эпизода).
WIN_BONUS = 3.0
# Штраф за поражение в матче (начисляется в конце эпизода).
LOSS_PENALTY = 2.0

# С какого боевого раунда начинать начислять VP по миссии Only War.
VP_START_SCORING_ROUND = 2
# Ограничение максимального VP за одну фазу командования.
VP_CAP_PER_COMMAND = 3

# Награды, связанные с удержанием/контролем objectives.
# Бонус за удержание objective.
VP_OBJECTIVE_HOLD_REWARD = 0.5
# Штраф за упущенное удержание/прогресс по objective.
VP_OBJECTIVE_HOLD_PENALTY = 0.12
# Бонус за приближение к objective.
VP_OBJECTIVE_PROXIMITY_REWARD = 0.5
# Нормировочный знаменатель для штрафа за пропущенный прогресс:
# penalty = -VP_OBJECTIVE_HOLD_PENALTY * clamp01(missed_progress / VP_OBJECTIVE_MISSED_PROGRESS_NORM)
VP_OBJECTIVE_MISSED_PROGRESS_NORM = 6.0
# Масштаб бонуса за улучшение разницы VP (vp_diff > 0).
VP_DIFF_REWARD_SCALE = 0.05
# Масштаб штрафа за ухудшение разницы VP (vp_diff < 0).
VP_DIFF_PENALTY_SCALE = 0.05
# Длина серии удержания objective для streak-бонуса.
VP_OBJECTIVE_STREAK_LEN = 2
# Дополнительный бонус за достижение серии удержания objective.
VP_OBJECTIVE_STREAK_BONUS = 0.2

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
MOVEMENT_MELEE_STAY_BONUS = 0.2
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
DAMAGE_TAKEN_SCALE = 0.5

# ==============================================
# Шэйпинг наград (objectives / utility-сигналы)
# ==============================================
# Штраф за бездействие вне целей (idle out of objective).
IDLE_OUT_OF_OBJECTIVE_PENALTY = 0.02
# Масштаб пошагового бонуса за прогресс к objective.
OBJECTIVE_PROGRESS_STEP_SCALE = 0.03
# Верхняя граница бонуса за прогресс к objective за шаг.
OBJECTIVE_PROGRESS_STEP_CAP = 0.10
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
# Вклад cover/terrain-компоненты (сейчас обычно 0.0, заглушка).
DEPLOYMENT_RL_COVER_W = 0.0

# Нормировки компонент deployment score.
# Целевая дистанция spread по row/y (после неё эффект насыщается).
DEPLOYMENT_RL_SPREAD_TARGET = 6.0
# Целевой минимальный отступ модели до границы поля (в клетках).
DEPLOYMENT_RL_EDGE_MARGIN_TARGET = 2.0


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
