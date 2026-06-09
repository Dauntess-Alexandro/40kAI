"""Default hyperparams sections for GUI editors (DQN / PPO)."""

from __future__ import annotations

# Ключи, которые дублируются в корень hyperparams.json для utils.py и legacy train.
DQN_ROOT_SYNC_KEYS: tuple[str, ...] = (
    "lr",
    "tau",
    "eps_start",
    "eps_end",
    "eps_decay",
    "batch_size",
    "gamma",
    "updates_per_step",
    "warmup_steps",
)

DQN_HYPERPARAM_KEYS: tuple[str, ...] = DQN_ROOT_SYNC_KEYS + (
    "hidden_size",
    "num_layers",
    "ensemble_size",
    "lr_scheduler",
    "eps_schedule",
    "double_dqn",
    "dueling",
    "dist_type",
    "iqn_n_quantiles",
    "iqn_n_target_quantiles",
    "iqn_n_tau_samples",
    "iqn_embed_dim",
    "iqn_kappa",
    "noisy_sigma0",
    "noisy_disable_eps",
    "noisy_sigma_anneal",
    "per_ensemble_priority_lambda",
    "distributed_actors_enabled",
    "distributed_rollout_port",
    "distributed_auth_token",
    "distributed_local_episode_fraction",
    "distributed_pc2_num_workers",
    "distributed_actors_drain_sec",
    "distributed_wait_pc2",
    "distributed_wait_pc2_timeout_sec",
    "distributed_bind_retry_sec",
)

DEFAULT_DQN_HYPERPARAMS: dict[str, int | float | str] = {
    "lr": 0.0001,
    "tau": 0.01,
    "eps_start": 0.9,
    "eps_end": 0.05,
    "eps_decay": 30000,
    "batch_size": 384,
    "gamma": 0.99,
    "updates_per_step": 6,
    "warmup_steps": 5000,
    "hidden_size": 256,
    "num_layers": 2,
    "ensemble_size": 1,
    "lr_scheduler": "none",
    "eps_schedule": "exp",
    "double_dqn": 1,
    "dueling": 1,
    "dist_type": "iqn",
    "iqn_n_quantiles": 32,
    "iqn_n_target_quantiles": 32,
    "iqn_n_tau_samples": 32,
    "iqn_embed_dim": 64,
    "iqn_kappa": 1.0,
    "noisy_sigma0": 0.5,
    "noisy_disable_eps": 1,
    "noisy_sigma_anneal": 0,
    "per_ensemble_priority_lambda": 0.1,
    "distributed_actors_enabled": 0,
    "distributed_rollout_port": 5558,
    "distributed_auth_token": "",
    "distributed_local_episode_fraction": 0.7,
    "distributed_pc2_num_workers": 8,
    "distributed_actors_drain_sec": 30.0,
    "distributed_wait_pc2": 0,
    "distributed_wait_pc2_timeout_sec": 600.0,
    "distributed_bind_retry_sec": 25.0,
}

PPO_HYPERPARAM_KEYS: tuple[str, ...] = (
    "learning_rate",
    "gamma",
    "gae_lambda",
    "clip_ratio",
    "value_coef",
    "entropy_coef",
    "rollout_steps",
    "update_epochs",
    "minibatch_size",
    "max_grad_norm",
    "target_kl",
    "lr_scheduler",
    "adaptive_entropy",
    "entropy_target",
    "entropy_adapt_lr",
)

DEFAULT_PPO_HYPERPARAMS: dict[str, int | float | str] = {
    "learning_rate": 0.0003,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_ratio": 0.2,
    "value_coef": 0.5,
    "entropy_coef": 0.01,
    "rollout_steps": 1024,
    "update_epochs": 4,
    "minibatch_size": 256,
    "max_grad_norm": 0.5,
    "target_kl": 0.03,
    "lr_scheduler": "none",
    "adaptive_entropy": 0,
    "entropy_target": 0.5,
    "entropy_adapt_lr": 0.05,
}

PPO_PROFILE_PRESETS: dict[str, dict[str, int | float]] = {
    "fast": {"rollout_steps": 512, "update_epochs": 3, "minibatch_size": 128},
    "balanced": {"rollout_steps": 1024, "update_epochs": 4, "minibatch_size": 256},
    "heavy": {"rollout_steps": 2048, "update_epochs": 6, "minibatch_size": 512},
}

DQN_PROFILE_PRESETS: dict[str, dict[str, int | float]] = {
    "fast": {"batch_size": 256, "updates_per_step": 4, "hidden_size": 128},
    "balanced": {"batch_size": 384, "updates_per_step": 6, "hidden_size": 256},
    "heavy": {"batch_size": 512, "updates_per_step": 8, "hidden_size": 384, "ensemble_size": 2},
}

# No-preset дефолт = balanced (единый удобный дефолт для всех моделей).
# Активный hyperparams.json не затрагивается — только свежий/сброшенный конфиг.
DEFAULT_DQN_HYPERPARAMS = {**DEFAULT_DQN_HYPERPARAMS, **DQN_PROFILE_PRESETS["balanced"]}
DEFAULT_PPO_HYPERPARAMS = {**DEFAULT_PPO_HYPERPARAMS, **PPO_PROFILE_PRESETS["balanced"]}

DQN_BASIC_KEYS: tuple[str, ...] = (
    "lr",
    "gamma",
    "batch_size",
    "eps_start",
    "eps_end",
    "eps_decay",
    "hidden_size",
    "num_layers",
    "updates_per_step",
)

PPO_BASIC_KEYS: tuple[str, ...] = (
    "learning_rate",
    "gamma",
    "clip_ratio",
    "entropy_coef",
    "rollout_steps",
    "minibatch_size",
    "update_epochs",
)

DQN_GROUPS: tuple[dict[str, object], ...] = (
    {
        "id": "training",
        "title": "Обучение",
        "keys": ("lr", "gamma", "batch_size", "updates_per_step", "warmup_steps", "lr_scheduler", "tau"),
        "default_collapsed": False,
    },
    {
        "id": "exploration",
        "title": "Exploration (epsilon)",
        "keys": ("eps_start", "eps_end", "eps_decay", "eps_schedule"),
        "default_collapsed": False,
    },
    {
        "id": "arch",
        "title": "Архитектура",
        "keys": ("hidden_size", "num_layers", "ensemble_size", "dueling", "double_dqn"),
        "default_collapsed": True,
    },
    {
        "id": "iqn",
        "title": "Distributional (IQN)",
        "keys": (
            "dist_type",
            "iqn_n_quantiles",
            "iqn_n_target_quantiles",
            "iqn_n_tau_samples",
            "iqn_embed_dim",
            "iqn_kappa",
        ),
        "default_collapsed": True,
    },
    {
        "id": "noisy_per",
        "title": "Noisy / PER",
        "keys": ("noisy_sigma0", "noisy_disable_eps", "noisy_sigma_anneal", "per_ensemble_priority_lambda"),
        "default_collapsed": True,
    },
)

PPO_GROUPS: tuple[dict[str, object], ...] = (
    {
        "id": "training",
        "title": "Обучение",
        "keys": ("learning_rate", "gamma", "gae_lambda", "lr_scheduler"),
        "default_collapsed": False,
    },
    {
        "id": "loss",
        "title": "PPO loss",
        "keys": ("clip_ratio", "value_coef", "entropy_coef", "target_kl", "max_grad_norm"),
        "default_collapsed": False,
    },
    {
        "id": "rollout",
        "title": "Rollout",
        "keys": ("rollout_steps", "update_epochs", "minibatch_size"),
        "default_collapsed": False,
    },
    {
        "id": "adaptive",
        "title": "Adaptive entropy",
        "keys": ("adaptive_entropy", "entropy_target", "entropy_adapt_lr"),
        "default_collapsed": True,
    },
)

DQN_FIELD_TOOLTIPS: dict[str, str] = {
    "lr": "Скорость обучения.",
    "tau": "Скорость soft-update target-сети.",
    "eps_start": "Начальный epsilon exploration.",
    "eps_end": "Минимальный epsilon.",
    "eps_decay": "Шагов затухания epsilon.",
    "batch_size": "Размер батча при обучении.",
    "gamma": "Дисконтирование награды.",
    "updates_per_step": "Градиентных updates за шаг среды.",
    "warmup_steps": "Прогрев replay до полного обучения.",
    "hidden_size": "Размер скрытого слоя.",
    "num_layers": "Число слоёв trunk.",
    "ensemble_size": "Число голов-ансамблей.",
    "lr_scheduler": "none / cosine / plateau.",
    "eps_schedule": "Расписание epsilon: exp, linear, poly, sigmoid.",
    "double_dqn": "1 = Double DQN.",
    "dueling": "1 = Dueling architecture.",
    "dist_type": "Тип distributional head (iqn).",
    "iqn_n_quantiles": "Число квантилей IQN.",
    "iqn_n_target_quantiles": "Квантили в target-сети.",
    "iqn_n_tau_samples": "Сэмплы tau при обучении.",
    "iqn_embed_dim": "Размер embedding квантилей.",
    "iqn_kappa": "Huber kappa для IQN.",
    "noisy_sigma0": "Начальный sigma NoisyNet.",
    "noisy_disable_eps": "1 = отключить epsilon при NoisyNet.",
    "noisy_sigma_anneal": "1 = anneal sigma NoisyNet.",
    "per_ensemble_priority_lambda": "Вес приоритета PER для ансамбля.",
    "distributed_actors_enabled": "Принимать опыт со второго ПК (ПК2) в общий replay на этом ПК.",
    "distributed_rollout_port": "Порт приёма данных с ПК2 (обычно 5558).",
    "distributed_auth_token": "Общий пароль ПК1↔ПК2 (можно оставить пустым).",
    "distributed_local_episode_fraction": "Доля эпизодов на ПК1 (0.05–0.95); остальное на ПК2.",
    "distributed_pc2_num_workers": "Число env-воркеров на ПК2 (на ПК1 — NUM_ACTORS, обычно 8).",
    "distributed_actors_drain_sec": "Макс. секунд drain после лимита эпизодов (выход раньше, если ПК1+ПК2 уже idle).",
    "distributed_wait_pc2": "Не начинать сбор эпизодов, пока все воркеры ПК2 не подключатся (hello на порт приёма).",
    "distributed_wait_pc2_timeout_sec": "Сколько ждать ПК2 (сек); 0 = ждать бесконечно.",
    "distributed_bind_retry_sec": "Сколько секунд повторять bind порта приёма, если он занят прошлым прогоном.",
}

DQN_DIST_ACTORS_GUI_TOOLTIP = (
    "Распределённые акторы: второй ПК (ПК2) помогает собирать опыт для обучения DQN.\n\n"
    "Зачем:\n"
    "• Больше CPU на симуляцию партий — train на этом ПК идёт быстрее\n"
    "• ПК2 только играет и шлёт данные; обучение (GPU) остаётся здесь\n\n"
    "Что нужно:\n"
    "• Два ПК в одной сети, один и тот же код репозитория\n"
    "• Общая папка models по SMB (как для AZ/GMZ)\n"
    "• На этом ПК: включить переключатель и запустить train\n"
    "• На ПК2 после старта train: tools\\pc2_dqn_actors.bat "
    "(при «Ждать ПК2» train не начнёт сбор, пока не подключатся все воркеры)\n"
    "• Одинаковый ростер и миссия на обоих ПК\n"
    "• Доля эпизодов: distributed_local_episode_fraction "
    "(например 0.7 при 400 ep → 280 на ПК1, 120 на ПК2; воркеры по 8 на каждой машине)\n\n"
    "По умолчанию выключено — весь опыт собирают только процессы на этом ПК."
)

DQN_DIST_WAIT_PC2_GUI_TOOLTIP = (
    "Train поднимает приёмник на порту 5558 и пишет train-context на SMB, "
    "но локальные акторы не стартуют, пока с ПК2 не придёт hello от всех воркеров.\n\n"
    "Порядок: 1) Старт train на ПК1 → 2) pc2_dqn_actors.bat на ПК2.\n"
    "Таймаут 0 = ждать бесконечно."
)

PPO_FIELD_TOOLTIPS: dict[str, str] = {
    "learning_rate": "Скорость обучения PPO.",
    "gamma": "Дисконт для GAE.",
    "gae_lambda": "GAE lambda.",
    "clip_ratio": "PPO clip epsilon.",
    "value_coef": "Вес value loss.",
    "entropy_coef": "Вес энтропийного бонуса.",
    "rollout_steps": "Длина rollout перед update.",
    "update_epochs": "Эпох PPO на одном rollout.",
    "minibatch_size": "Размер минибатча.",
    "max_grad_norm": "Клип нормы градиента.",
    "target_kl": "Порог ранней остановки по KL.",
    "lr_scheduler": "none / cosine / plateau.",
    "adaptive_entropy": "1 = адаптивная энтропия.",
    "entropy_target": "Целевая энтропия.",
    "entropy_adapt_lr": "Скорость адаптации энтропии.",
}
