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
