"""
Конфигурация reward-шэйпинга.
Меняйте значения здесь, чтобы не лезть в код среды.
"""

# ==========================
# Reward shaping (win / VP)
# ==========================
# Бонус/штраф за результат боя.
WIN_BONUS = 3.0
LOSS_PENALTY = 2.0

# Настройки начисления VP (миссия Only War).
VP_START_SCORING_ROUND = 2
VP_CAP_PER_COMMAND = 3

# Награды, связанные с целями/объектами (VP-компоненты).
VP_OBJECTIVE_HOLD_REWARD = 0.5
VP_OBJECTIVE_HOLD_PENALTY = 0.5
VP_OBJECTIVE_PROXIMITY_REWARD = 0.5

# =========================
# Reward shaping (shooting)
# =========================
# Базовые коэффициенты — подбирайте экспериментально.
SHOOT_REWARD_DAMAGE_SCALE = 0.6
SHOOT_REWARD_KILL_BONUS = 0.4
SHOOT_REWARD_OVERKILL_PENALTY = 0.2
SHOOT_REWARD_SKIP_PENALTY = 0.15
SHOOT_REWARD_TARGET_LOW_HP = 0.05
SHOOT_REWARD_TARGET_ON_OBJ = 0.07
SHOOT_REWARD_TARGET_HIGH_OC = 0.05
SHOOT_REWARD_ACTION_BONUS = 0.0

# Penalize damage received during the model's step (normalized by model total max HP).
DAMAGE_TAKEN_SCALE = 0.5

# ======================
# Reward shaping (fight)
# ======================
# Базовые коэффициенты — подбирайте экспериментально.
MELEE_REWARD_DAMAGE_SCALE = 0.6
MELEE_REWARD_KILL_BONUS = 0.4
MELEE_REWARD_TAKEN_SCALE = 0.5
MELEE_ADVANTAGE_SCALE = 0.15
MELEE_STRENGTH_SCALE = 0.1
MELEE_OBJECTIVE_CONTROL_SCALE = 0.2
