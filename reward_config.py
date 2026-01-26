"""
Конфигурация reward-шэйпинга.
Меняйте значения здесь, чтобы не лезть в код среды.
"""

# =========================
# Reward shaping (shooting)
# =========================
# Базовые коэффициенты — подбирайте экспериментально.
SHOOT_REWARD_DAMAGE_SCALE = 0.6
SHOOT_REWARD_KILL_BONUS = 0.8
SHOOT_REWARD_OVERKILL_PENALTY = 0.2
SHOOT_REWARD_SKIP_PENALTY = 0.15
SHOOT_REWARD_TARGET_LOW_HP = 0.1
SHOOT_REWARD_TARGET_ON_OBJ = 0.15
SHOOT_REWARD_TARGET_HIGH_OC = 0.1
