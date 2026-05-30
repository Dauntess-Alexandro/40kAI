"""Default Gumbel MuZero hyperparams for GUI editor."""

from __future__ import annotations

# Вариант B (inference server) / A (GPU-акторы) — переключается одной галочкой в GUI.
GMZ_VARIANT_B_BUNDLE: dict[str, int | float | str] = {
    "inference_server_enabled": 1,
    "actor_device": "inference_server",
    "num_env_workers": 6,
    "num_actors": 6,
    "actor_max_cuda": 0,
}

GMZ_VARIANT_A_BUNDLE: dict[str, int | float | str] = {
    "inference_server_enabled": 0,
    "actor_device": "cuda",
    "num_env_workers": 6,
    "num_actors": 2,
    "actor_max_cuda": 2,
}

GMZ_INFERENCE_SERVER_CHECKBOX_TOOLTIP = (
    "Вариант B: 6 CPU env workers + 1 GPU inference server + learner. "
    "Выключено: вариант A (до 2 GPU-акторов). Требуется CUDA."
)

GMZ_LOCAL_IS_GUI_TOOLTIP = (
    "Локальный Inference Server (вариант B) на этом ПК.\n\n"
    "• 6 CPU env workers симулируют партии\n"
    "• 1 GPU-процесс на этом ПК делает MCTS/search (forward сети)\n"
    "• Learner на GPU этого же ПК обучает сеть\n\n"
    "Требуется CUDA. Выключено = вариант A (до 2 GPU-акторов без отдельного IS).\n"
    "При включённом LAN Inference server эта опция недоступна."
)

GMZ_LAN_IS_GUI_TOOLTIP = (
    "LAN Inference Server: инференс на втором ПК (ПК2) по сети.\n\n"
    "• На ПК1: learner (GPU) + CPU env workers\n"
    "• На ПК2: GPU inference server (tools\\pc2_remote_is.bat)\n"
    "• Веса: общая SMB-папка, latest_gmz_policy.pth\n"
    "• Связь: ZMQ (порт 5555), «Проверить соединение» перед train\n\n"
    "При включении локальный IS на ПК1 не запускается. Вариант B включается автоматически."
)

# Remote IS — только runtime/state/remote_is.json + GUI (Настройки → GMZ), не в presets.
GMZ_REMOTE_IS_KEYS: tuple[str, ...] = (
    "inference_server_mode",
    "inference_remote_host",
    "inference_remote_port",
    "inference_remote_timeout",
    "inference_remote_auth_token",
)

GMZ_HYPERPARAM_KEYS: tuple[str, ...] = (
    "learning_rate",
    "batch_size",
    "unroll_steps",
    "value_loss_weight",
    "reward_loss_weight",
    "consistency_loss_weight",
    "l2_weight",
    "max_grad_norm",
    "discount",
    "replay_capacity",
    "inference_server_enabled",
    "num_env_workers",
    "inference_batch_size",
    "inference_batch_interval_ms",
    "inference_timeout",
    "inference_request_queue_max",
    "inference_server_compile",
    "clear_tree_on_weight_sync",
    "actor_device",
    "actor_max_cuda",
    "num_actors",
    "actor_batch_send",
    "actor_queue_max",
    "sync_every_updates",
    "updates_per_rollout",
    "replay_min_size",
    "max_policy_staleness_updates",
    "reanalyze_fraction",
    "latent_dim",
    "hidden_dim",
    "action_embed_dim",
    "num_simulations",
    "root_top_k",
    "gumbel_scale",
    "prior_weight",
    "search_temperature",
    "batch_recurrent",
    "tree_reuse",
    "vtrace_full",
    "vtrace_rho_clip",
    "vtrace_c_clip",
    "atom_range",
    "ema_tau",
    "actor_compile",
    "learner_compile",
    "temperature_opening_moves",
    "temperature_opening_value",
    "temperature_late_value",
    "outcome_only",
    "outcome_value_win",
    "outcome_value_loss",
    "outcome_value_draw",
)

DEFAULT_GMZ_HYPERPARAMS: dict[str, int | float | str] = {
    "learning_rate": 0.0003,
    "batch_size": 128,
    "unroll_steps": 5,
    "value_loss_weight": 1.0,
    "reward_loss_weight": 1.0,
    "consistency_loss_weight": 1.0,
    "l2_weight": 1e-6,
    "max_grad_norm": 0.5,
    "discount": 0.997,
    "replay_capacity": 250000,
    **GMZ_VARIANT_B_BUNDLE,
    "inference_batch_size": 8,
    "inference_batch_interval_ms": 20.0,
    "inference_timeout": 5.0,
    "inference_request_queue_max": 32,
    "inference_server_compile": 1,
    "clear_tree_on_weight_sync": 0,
    "actor_batch_send": 64,
    "actor_queue_max": 256,
    "sync_every_updates": 2,
    "updates_per_rollout": 2,
    "replay_min_size": 512,
    "max_policy_staleness_updates": 600,
    "reanalyze_fraction": 0.15,
    "latent_dim": 256,
    "hidden_dim": 256,
    "action_embed_dim": 64,
    "num_simulations": 32,
    "root_top_k": 8,
    "gumbel_scale": 1.0,
    "prior_weight": 0.25,
    "search_temperature": 0.15,
    "batch_recurrent": 1,
    "tree_reuse": 1,
    "vtrace_full": 1,
    "vtrace_rho_clip": 0.7,
    "vtrace_c_clip": 0.7,
    "atom_range": "tight",
    "ema_tau": 0.005,
    "actor_compile": 1,
    "learner_compile": 1,
    "temperature_opening_moves": 12,
    "temperature_opening_value": 1.0,
    "temperature_late_value": 0.25,
    "outcome_only": 1,
    "outcome_value_win": 1.0,
    "outcome_value_loss": -1.0,
    "outcome_value_draw": -0.25,
}

# Порядок detect: very_heavy перед heavy (иначе частичное совпадение).
GMZ_PROFILE_DETECT_ORDER: tuple[str, ...] = ("fast", "balanced", "very_heavy", "heavy")

GMZ_PROFILE_PRESETS: dict[str, dict[str, int | float | str]] = {
    "fast": {
        **GMZ_VARIANT_B_BUNDLE,
        "num_simulations": 16,
        "root_top_k": 4,
        "batch_size": 96,
        "replay_capacity": 120000,
        "reanalyze_fraction": 0.05,
        "consistency_loss_weight": 0.5,
        "vtrace_full": 1,
        "tree_reuse": 1,
        "atom_range": "tight",
        "actor_compile": 1,
        "learner_compile": 1,
    },
    "balanced": {
        **GMZ_VARIANT_B_BUNDLE,
        "num_simulations": 32,
        "root_top_k": 8,
        "batch_size": 128,
        "replay_capacity": 250000,
        "reanalyze_fraction": 0.15,
        "consistency_loss_weight": 1.0,
        "vtrace_full": 1,
        "tree_reuse": 1,
        "atom_range": "tight",
        "actor_compile": 1,
        "learner_compile": 1,
    },
    "heavy": {
        **GMZ_VARIANT_B_BUNDLE,
        "num_env_workers": 10,
        "num_actors": 10,
        "num_simulations": 48,
        "root_top_k": 12,
        "inference_batch_size": 10,
        "inference_batch_interval_ms": 8.0,
        "batch_size": 160,
        "replay_capacity": 400000,
        "actor_queue_max": 512,
        "sync_every_updates": 2,
        "reanalyze_fraction": 0.15,
        "consistency_loss_weight": 1.0,
        "vtrace_full": 1,
        "tree_reuse": 1,
        "atom_range": "tight",
        "actor_compile": 0,
        "learner_compile": 1,
    },
    "very_heavy": {
        **GMZ_VARIANT_B_BUNDLE,
        # Качество поиска — как heavy (sims/top_k/temp/prior не трогаем)
        "num_simulations": 48,
        "root_top_k": 12,
        # Throughput: 2× env workers + широкое окно батча (LAN / 2 ПК)
        # ПК2 pc2_remote_is_config: GMZ_REMOTE_BATCH_SIZE=24, INTERVAL_MS=20
        "num_env_workers": 20,
        "num_actors": 20,
        "inference_batch_size": 20,
        "inference_batch_interval_ms": 20.0,
        "inference_timeout": 6.0,
        "inference_request_queue_max": 64,
        "updates_per_rollout": 3,
        # Обучение / replay — как heavy
        "batch_size": 160,
        "replay_capacity": 400000,
        "actor_queue_max": 512,
        "sync_every_updates": 2,
        "reanalyze_fraction": 0.15,
        "consistency_loss_weight": 1.0,
        "vtrace_full": 1,
        "tree_reuse": 1,
        "atom_range": "tight",
        "actor_compile": 0,
        "learner_compile": 1,
    },
}

GMZ_BASIC_KEYS: tuple[str, ...] = (
    "learning_rate",
    "batch_size",
    "num_simulations",
    "root_top_k",
    "unroll_steps",
    "num_actors",
    "vtrace_full",
    "reanalyze_fraction",
)

GMZ_GROUPS: tuple[dict[str, object], ...] = (
    {
        "id": "training",
        "title": "Обучение",
        "keys": (
            "learning_rate",
            "batch_size",
            "unroll_steps",
            "value_loss_weight",
            "reward_loss_weight",
            "consistency_loss_weight",
            "l2_weight",
            "max_grad_norm",
            "discount",
            "reanalyze_fraction",
        ),
        "default_collapsed": False,
    },
    {
        "id": "search",
        "title": "Поиск (MCTS)",
        "keys": (
            "num_simulations",
            "root_top_k",
            "gumbel_scale",
            "prior_weight",
            "search_temperature",
            "batch_recurrent",
            "tree_reuse",
        ),
        "default_collapsed": False,
    },
    {
        "id": "vtrace",
        "title": "V-trace / IS-коррекция",
        "keys": (
            "vtrace_full",
            "vtrace_rho_clip",
            "vtrace_c_clip",
            "atom_range",
        ),
        "default_collapsed": False,
    },
    {
        "id": "temperature",
        "title": "Температура",
        "keys": (
            "temperature_opening_moves",
            "temperature_opening_value",
            "temperature_late_value",
        ),
        "default_collapsed": True,
    },
    {
        "id": "actors_replay",
        "title": "Акторы и replay",
        "keys": (
            "inference_batch_size",
            "inference_batch_interval_ms",
            "inference_timeout",
            "inference_request_queue_max",
            "actor_batch_send",
            "actor_queue_max",
            "sync_every_updates",
            "updates_per_rollout",
            "replay_capacity",
            "replay_min_size",
            "max_policy_staleness_updates",
        ),
        "default_collapsed": False,
    },
    {
        "id": "compile_ema",
        "title": "Компиляция и EMA",
        "keys": (
            "actor_compile",
            "learner_compile",
            "ema_tau",
        ),
        "default_collapsed": True,
    },
    {
        "id": "arch_outcome",
        "title": "Архитектура и outcome",
        "keys": (
            "latent_dim",
            "hidden_dim",
            "action_embed_dim",
            "outcome_only",
            "outcome_value_win",
            "outcome_value_loss",
            "outcome_value_draw",
        ),
        "default_collapsed": True,
    },
)

GMZ_FIELD_TOOLTIPS: dict[str, str] = {
    "learning_rate": "Скорость обучения learner.",
    "batch_size": "Размер батча при обновлении весов.",
    "unroll_steps": "Глубина unroll по траектории.",
    "value_loss_weight": "Вес value loss.",
    "reward_loss_weight": "Вес reward loss.",
    "consistency_loss_weight": "Вес SimSiam consistency loss (EMA-цель). 0 = отключить. Рекомендуется 0.5-1.0.",
    "l2_weight": "L2-регуляризация.",
    "max_grad_norm": "Gradient clipping (max norm). 0.5 = рекомендуется для стабильности.",
    "discount": "Дисконт для n-step returns.",
    "reanalyze_fraction": "Доля обучающих шагов, на которых переоцениваются старые траектории (0=выкл, 0.15=15%).",
    "replay_capacity": "Ёмкость replay buffer.",
    "inference_server_enabled": "1 = вариант B: CPU env workers + 1 GPU inference server. 0 = вариант A (акторы).",
    "num_env_workers": "Число CPU env workers при inference_server_enabled=1.",
    "inference_batch_size": "Макс. запросов в одном batch inference server.",
    "inference_batch_interval_ms": "Окно сбора batch (мс).",
    "inference_timeout": "Таймаут ответа inference server (сек).",
    "inference_request_queue_max": "Backpressure: maxsize очереди request_q.",
    "inference_server_compile": "torch.compile на inference server (CUDA).",
    "clear_tree_on_weight_sync": "1 = сброс tree_reuse при обновлении весов.",
    "actor_device": "cuda/cpu = вариант A. inference_server = вариант B (нужна CUDA).",
    "actor_max_cuda": "Макс. GPU-акторов при actor_device=cuda. Ограничение VRAM: 2 актора + learner.",
    "num_actors": "Число параллельных акторов self-play (при cuda фактически min(num_actors, actor_max_cuda)).",
    "actor_batch_send": "Сколько переходов актор шлёт за раз.",
    "actor_queue_max": "Макс. размер очереди переходов.",
    "sync_every_updates": (
        "Каждые N gradient updates learner сохраняет веса в latest_gmz_policy.pth; "
        "inference server / GPU-акторы подхватывают их для self-play. "
        "1 = максимально свежая политика у акторов, но чаще torch.save и reload (медленнее). "
        "3–5 = меньше I/O и пауз pipeline, self-play чуть «старее» на 2–4 шага — "
        "обычно почти не влияет на качество при max_policy_staleness_updates=600."
    ),
    "updates_per_rollout": "Градиентных updates на один rollout.",
    "replay_min_size": "Мин. размер replay до старта обучения.",
    "max_policy_staleness_updates": "Макс. устаревание политики у акторов.",
    "latent_dim": "Размерность latent state.",
    "hidden_dim": "Размер скрытого слоя сети.",
    "action_embed_dim": "Размер embedding действия.",
    "num_simulations": "Число MCTS-симуляций на ход.",
    "root_top_k": "Top-K в корне Gumbel-поиска.",
    "gumbel_scale": "Масштаб Gumbel-шума.",
    "prior_weight": "Доля приора сети в корневой политике (0.2 = больше Q из sims, 0.3 = больше prior).",
    "search_temperature": "Температура в поиске.",
    "batch_recurrent": "1 = батчевый recurrent inference (быстрее на GPU). 0 = последовательный.",
    "tree_reuse": "1 = переиспользование дерева поиска (warm-start visits/Q) между ходами. Ускоряет сходимость.",
    "vtrace_full": "1 = V-trace на полном unroll (Retrace-стиль). Улучшает качество обучения по старым траекториям.",
    "vtrace_rho_clip": "Ограничение ρ для importance sampling (рекомендуется 0.7-1.0). Меньше = стабильнее.",
    "vtrace_c_clip": "Ограничение c для trace decay в V-trace (рекомендуется 0.7-1.0).",
    "atom_range": "Диапазон атомов: 'tight' = [-1.05,1.05] (рекомендуется), 'legacy' = [-20,20].",
    "ema_tau": "Скорость обновления EMA-цели для consistency loss (Conservative Polyak). 0.005 = медленно.",
    "actor_compile": (
        "torch.compile для варианта A на CPU-акторах. При CUDA в GUI ставится 0 автоматически "
        "(ускорение learner — learner_compile). Без CUDA ставится 1 автоматически. "
        "При inference server (вариант B) на акторов не влияет."
    ),
    "learner_compile": "1 = torch.compile для learner на CUDA (15-30% быстрее). 0 = выключить.",
    "temperature_opening_moves": "Ходов с повышенной температурой.",
    "temperature_opening_value": "Температура в дебюте.",
    "temperature_late_value": "Температура в эндшпиле.",
    "outcome_only": "1 = только outcome reward.",
    "outcome_value_win": "Награда за победу.",
    "outcome_value_loss": "Награда за поражение.",
    "outcome_value_draw": "Награда за ничью.",
}
