"""
Smoke-тест actor-learner для Sampled MuZero.

Покрывает:
1. Прямой шаг обучения (train_sampled_muzero_step) — юнит-аналог gmz-теста.
2. Интеграционный прогон _main_actor_learner_sampled_muzero с totLifeT=2:
   - минимальная сеть (latent/hidden=32, layers=1, action_embed=8),
   - tiny replay (min_size=4, batch=4),
   - 1 CPU-актор, num_samples=4,
   - SMZ_CONSISTENCY_W=0 (без EMA-target), SMZ_REANALYZE_FRACTION=0 (без переразбора),
   - SMZ_LEARNER_COMPILE=0, SMZ_ACTOR_COMPILE=0,
   - Ассертит: чекпойнт artifacts/models/sampled_muzero/checkpoint_ep*.pth содержит ключ sampled_muzero_net.
"""

from __future__ import annotations

import glob as _glob
import os
import time

import numpy as np
import torch

from core.models.gumbel_muzero_replay import GMZTransition, GumbelMuZeroReplayBuffer
from core.models.sampled_muzero_model import make_sampled_muzero_net
from core.models.sampled_muzero_trainer import SampledMuZeroTrainConfig, train_sampled_muzero_step

# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def _make_smz_transition(n_obs: int, n_actions: list[int], value: float, policy_version: int) -> GMZTransition:
    action = [np.random.randint(0, max(1, n_actions[h])) for h in range(len(n_actions))]
    return GMZTransition(
        state=np.random.randn(n_obs).astype(np.float32),
        action=np.asarray(action, dtype=np.int64),
        reward=float(np.random.uniform(-1.0, 1.0)),
        done=False,
        policy_targets=[np.ones(a, dtype=np.float32) / float(a) for a in n_actions],
        behavior_logits=[np.zeros(a, dtype=np.float32) for a in n_actions],
        value_target=float(value),
        policy_version=int(policy_version),
    )


# ---------------------------------------------------------------------------
# Юнит-тесты (аналог test_gumbel_muzero_actor_learner_smoke.py)
# ---------------------------------------------------------------------------


def test_sampled_muzero_train_step_runs():
    """train_sampled_muzero_step отрабатывает без ошибок и возвращает loss >= 0."""
    n_obs = 18
    n_actions = [5, 3, 7]
    net = make_sampled_muzero_net(
        obs_dim=n_obs,
        action_sizes=n_actions,
        latent_dim=64,
        hidden_dim=64,
        num_layers=1,
        action_embed_dim=16,
    )
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
    replay = GumbelMuZeroReplayBuffer(capacity=128)
    for _ in range(48):
        replay.push(_make_smz_transition(n_obs, n_actions, value=np.random.uniform(-1.0, 1.0), policy_version=9))

    cfg = SampledMuZeroTrainConfig(
        batch_size=16,
        unroll_steps=4,
        max_policy_staleness_updates=5,
    )
    out = train_sampled_muzero_step(
        net=net,
        optimizer=optimizer,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        current_policy_version=10,
    )
    assert out is not None
    assert float(out["loss"]) >= 0.0


def test_sampled_muzero_train_step_staleness_filter_skips_old():
    """Сэмплы с устаревшей policy_version отфильтровываются — шаг возвращает None."""
    n_obs = 12
    n_actions = [5, 3, 7]
    net = make_sampled_muzero_net(
        obs_dim=n_obs,
        action_sizes=n_actions,
        latent_dim=32,
        hidden_dim=32,
        num_layers=1,
        action_embed_dim=8,
    )
    optimizer = torch.optim.SGD(net.parameters(), lr=1e-2)
    replay = GumbelMuZeroReplayBuffer(capacity=64)
    # policy_version=0, current=10 → все устарели (max_policy_staleness_updates=0)
    for _ in range(32):
        replay.push(_make_smz_transition(n_obs, n_actions, value=1.0, policy_version=0))

    cfg = SampledMuZeroTrainConfig(
        batch_size=16,
        max_policy_staleness_updates=0,
    )
    out = train_sampled_muzero_step(
        net=net,
        optimizer=optimizer,
        replay=replay,
        config=cfg,
        device=torch.device("cpu"),
        current_policy_version=10,
    )
    assert out is None


# ---------------------------------------------------------------------------
# Интеграционный тест: _main_actor_learner_sampled_muzero
# ---------------------------------------------------------------------------

# Параметры, которые будут выставлены через monkeypatch на модуль train:
_SMOKE_SMZ_OVERRIDES = {
    "SMZ_LATENT_DIM": 32,
    "SMZ_HIDDEN_DIM": 32,
    "SMZ_NUM_LAYERS": 1,
    "SMZ_ACTION_EMBED_DIM": 8,
    "SMZ_NUM_SAMPLES": 4,
    "SMZ_BATCH_SIZE": 4,
    "SMZ_REPLAY_MIN_SIZE": 4,
    "SMZ_REPLAY_CAPACITY": 1024,
    "SMZ_NUM_ACTORS": 1,
    "SMZ_UPDATES_PER_ROLLOUT": 1,
    "SMZ_SYNC_EVERY_UPDATES": 1,
    "SMZ_MAX_POLICY_STALENESS_UPDATES": 999,
    "SMZ_UNROLL_STEPS": 2,
    "SMZ_TBPTT_TRUNCATE": 1,
    "SMZ_CONSISTENCY_W": 0.0,      # без EMA-target
    "SMZ_REANALYZE_FRACTION": 0.0, # без реанализа
    "SMZ_LEARNER_COMPILE": False,
    "SMZ_ACTOR_COMPILE": False,
    "SMZ_ACTOR_DEVICE_REQUESTED": "cpu",
    "SMZ_ACTOR_DEVICE_CUDA": False,
    "SMZ_ACTOR_USING_CUDA_FALLBACK": False,
    "SMZ_ACTOR_EFFECTIVE_NUM_ACTORS": 1,
    "SMZ_ACTOR_QUEUE_MAX": 64,
    "SMZ_ACTOR_BATCH_SEND": 8,
    "SMZ_VTRACE_FULL": True,
    "SMZ_VTRACE_RHO_CLIP": 0.7,
    "SMZ_VTRACE_C_CLIP": 0.7,
    "SMZ_DISCOUNT": 0.997,
    "SMZ_SEARCH_TEMP": 0.15,
    "SMZ_SAMPLE_TEMP": 1.0,
    "SMZ_PRIOR_WEIGHT": 0.0,
    "SMZ_DEDUP": True,
    "SMZ_EMA_TAU": 0.005,
    "SMZ_TEMP_OPENING_MOVES": 12,
    "SMZ_TEMP_OPENING": 1.0,
    "SMZ_TEMP_LATE": 0.25,
    "SMZ_OUTCOME_ONLY": True,
    "SMZ_OUTCOME_VALUE_WIN": 1.0,
    "SMZ_OUTCOME_VALUE_LOSS": -1.0,
    "SMZ_OUTCOME_VALUE_DRAW": -0.25,
    "SMZ_ATOM_RANGE": "tight",
    "SMZ_MAX_GRAD_NORM": 0.5,
    "SMZ_LR": 1e-3,
    "SMZ_LR_SCHEDULER": "none",
    "SMZ_LR_WARMUP_STEPS": 0,
    "SMZ_LR_TOTAL_STEPS": 0,
}


def test_sampled_muzero_actor_learner_smoke(tmp_path, monkeypatch):
    """
    Интеграционный smoke-тест:
    - Запускает _main_actor_learner_sampled_muzero с totLifeT=2, tiny net, tiny replay.
    - Ассертит, что чекпойнт сохранён и содержит ключ 'sampled_muzero_net'.
    """
    # Импортируем train после установки env vars; при повторном импорте
    # в pytest-сессии модуль уже закэширован, поэтому патчим его globals напрямую.
    import train as train_mod  # noqa: PLC0415

    # --- Перенаправляем артефакты в tmp_path ---
    tmp_models = str(tmp_path / "models")
    tmp_metrics = str(tmp_path / "metrics")
    os.makedirs(tmp_models, exist_ok=True)
    os.makedirs(tmp_metrics, exist_ok=True)
    monkeypatch.setattr(train_mod, "MODELS_DIR", tmp_models)
    monkeypatch.setattr(train_mod, "METRICS_DIR", tmp_metrics)

    # --- Изолируем agent-registry в tmp_path (иначе save_agent_artifact пишет в реальный
    #     artifacts/models/agents/ и agents_registry.json — каталог в .gitignore, но файлы копятся) ---
    import core.engine.agent_registry as _ar
    monkeypatch.setattr(_ar, "AGENTS_ROOT", str(tmp_path / "agents"))
    monkeypatch.setattr(_ar, "AGENTS_REGISTRY_PATH", str(tmp_path / "agents_registry.json"))

    # --- Патчим все SMZ_* globals ---
    for attr, val in _SMOKE_SMZ_OVERRIDES.items():
        monkeypatch.setattr(train_mod, attr, val)

    # --- Принудительно выключаем resume checkpoint ---
    monkeypatch.setattr(train_mod, "RESUME_CHECKPOINT", "")

    # --- Принудительно выключаем self-play и det-eval (не нужны для smoke) ---
    monkeypatch.setattr(train_mod, "SELF_PLAY_ENABLED", 0)
    monkeypatch.setattr(train_mod, "ACTOR_DET_EVAL_ENABLED", False)
    monkeypatch.setattr(train_mod, "SAVE_EVERY", 0)  # не сохранять на каждом эпизоде

    # roster_config — стандартный из _load_roster_config()
    roster_config = train_mod._load_roster_config()

    t0 = time.perf_counter()
    train_mod._main_actor_learner_sampled_muzero(
        roster_config=roster_config,
        totLifeT=2,
        clip_reward_enabled=False,
        clip_reward_min=-1.0,
        clip_reward_max=1.0,
    )
    elapsed = time.perf_counter() - t0

    # --- Проверяем чекпойнт ---
    ckpt_dir = os.path.join(tmp_models, "sampled_muzero")
    ckpt_files = _glob.glob(os.path.join(ckpt_dir, "checkpoint_ep*.pth"))
    assert ckpt_files, (
        f"Чекпойнт sampled_muzero не найден в {ckpt_dir}. "
        f"Содержимое tmp_models: {os.listdir(tmp_models) if os.path.isdir(tmp_models) else 'отсутствует'}. "
        f"Время выполнения: {elapsed:.1f}s"
    )

    ckpt_path = sorted(ckpt_files)[-1]
    payload = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    assert isinstance(payload, dict), f"Чекпойнт не является словарём: {type(payload)}"
    assert "sampled_muzero_net" in payload, (
        f"Ключ 'sampled_muzero_net' отсутствует в чекпойнте {ckpt_path}. "
        f"Ключи: {list(payload.keys())}"
    )
    assert payload["algo"] == "sampled_muzero", (
        f"Поле 'algo' в чекпойнте: {payload.get('algo')!r}, ожидалось 'sampled_muzero'"
    )

    print(f"\n[SMOKE][SMZ] OK: чекпойнт={ckpt_path}, elapsed={elapsed:.1f}s", flush=True)
