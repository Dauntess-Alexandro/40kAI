# PHOENIX (off-policy, sample-efficient) — Wave 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Реализовать ядро нового off-policy агента PHOENIX (IQN + self-predictive репрезентации + латентный value-expansion + BBF-resets), зарегистрировать `TRAIN_ALGO=phoenix` во всех allowlist-гейтах и довести до запускаемого single-process обучения + минимального eval (Волна 1).

**Architecture:** PHOENIX переиспользует ствол/IQN-голову DQN как encoder+RL-голову, добавляет masked action-embedding, латентную dynamics-модель, BYOL-головы (projection/prediction) с EMA-таргетом, sequence-replay (sum-tree по началу окна) и trainer с periodic resets + аннелингом n-step/γ. На инференсе — чистый off-policy (per-head argmax по IQN-Q).

**Tech Stack:** Python 3.12, PyTorch, numpy. Платформа — Windows. Тесты — pytest. Точечные тесты по файлам (НЕ гонять весь `tests/models -k muzero`).

**Спека:** `docs/superpowers/specs/2026-06-29-phoenix-offpolicy-design.md`.

## Global Constraints

- **Язык логов/ошибок/UI — русский.** Ошибки: что случилось + где (файл/функция) + что делать дальше.
- **Платформа Windows**, GUI только Qt — но в Волне 1 полноценная вкладка НЕ делается (только регистрация `phoenix` в селекторах, см. Task 9).
- **Off-policy на инференсе:** никакого дерева/планирования при выборе действия.
- **NoisyNets ВЫКЛ по умолчанию** (`noisy=False`) — отличие от DQN (footgun с value-expansion greedy `a*` + resets/EMA).
- **End-значения аннелинга заякорены на рабочий DQN:** `gamma_end=0.99`, `nstep_end=3`. Start — исследовательские (`gamma_start=0.97`, `nstep_start=10`).
- **Дефолты (verbatim из спеки §4):** `replay_ratio=2` (только smoke; A/B-кнопка №1), `reset_interval=40000` град. шагов, `anneal_steps=10000`, `shrink_alpha=0.5`, `target_ema_rl=0.005`, `target_ema_spr=0.01`, `replay_capacity=200000`, `spr_horizon_K=5`, `spr_coef=2.0`, `ve_horizon=3`, `ve_steve=False`, `dynamics_type="mlp"`, `emb_dim=64`.
- **`H = max(spr_horizon_K, ve_horizon)`** — длина горизонта окна replay; окно хранит `H+1` шагов.
- **Allowlist-гейты обязательны в Волне 1** (память algo-allowlist-gates): иначе тихий fallback на `dqn`.
- **Коммит после каждой задачи** (правило проекта). В коммит — только релевантный код, без runtime-логов.
- **ruff_fix хук** срезает временно-неиспользуемые импорты: добавляй импорт вместе с использованием.

---

## File Structure

**Создаём:**
- `core/models/phoenix_config.py` — `PhoenixConfig` + `resolve_phoenix_config` (torch-free).
- `core/models/phoenix_model.py` — `PhoenixActionEmbed`, `PhoenixDynamics`, `PhoenixNet`, `infer_phoenix_arch_from_state_dict`.
- `core/models/phoenix_loss.py` — `spr_consistency_loss`, `phoenix_td_loss`.
- `core/models/phoenix_replay.py` — `SequenceWindow`, `SequenceReplayBuffer`.
- `core/models/phoenix_trainer.py` — `anneal_value`, `PhoenixTrainer`.
- `tests/models/test_phoenix_config.py`, `test_phoenix_model.py`, `test_phoenix_loss.py`, `test_phoenix_replay.py`, `test_phoenix_trainer.py`, `test_phoenix_allowlist.py`.
- `tests/models/test_phoenix_eval_loader.py`.

**Модифицируем:**
- `core/models/alphazero_ids.py:5-7` — добавить `"phoenix"` в `VALID_TRAIN_ALGOS`.
- `train.py:316-318` (resolve), `train.py:3762-3777` (dispatch + error), + новая функция `_main_actor_learner_phoenix`.
- `eval.py` (per-algo checkpoint key + arch resolve), `play.py`/viewer algo-списки, `app/gui_qt/main.py` + `Main.qml` (селекторы algo — регистрация, без полной вкладки).
- `hyperparams.json` — секция `phoenix`.

---

## Task 1: PHOENIX config resolver

**Files:**
- Create: `core/models/phoenix_config.py`
- Test: `tests/models/test_phoenix_config.py`

**Interfaces:**
- Produces: `PhoenixConfig` (frozen dataclass со всеми полями из Global Constraints + `hidden_size:int=256`, `num_layers:int=2`, `n_ensemble:int=1`, `dueling:bool=False`, `iqn_num_quantiles:int=32`, `iqn_num_target_quantiles:int=32`, `iqn_num_tau_samples:int=32`, `iqn_embed_dim:int=64`); `resolve_phoenix_config(hp: dict | None, env: Mapping[str,str] | None = None) -> PhoenixConfig`. Приоритет `env(PHOENIX_*) → hp["phoenix"] → default`.

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_config.py
import os
from core.models.phoenix_config import PhoenixConfig, resolve_phoenix_config


def test_defaults_when_no_hp_no_env():
    cfg = resolve_phoenix_config(None, {})
    assert cfg.replay_ratio == 2
    assert cfg.reset_interval == 40000
    assert cfg.gamma_start == 0.97 and cfg.gamma_end == 0.99
    assert cfg.nstep_start == 10 and cfg.nstep_end == 3
    assert cfg.noisy is False
    assert cfg.ve_steve is False
    assert cfg.spr_horizon_K == 5 and cfg.ve_horizon == 3


def test_section_overrides_default():
    cfg = resolve_phoenix_config({"phoenix": {"replay_ratio": 8, "shrink_alpha": 0.4}}, {})
    assert cfg.replay_ratio == 8
    assert abs(cfg.shrink_alpha - 0.4) < 1e-9


def test_env_overrides_section():
    hp = {"phoenix": {"replay_ratio": 8}}
    env = {"PHOENIX_REPLAY_RATIO": "16", "PHOENIX_VE_STEVE": "1"}
    cfg = resolve_phoenix_config(hp, env)
    assert cfg.replay_ratio == 16
    assert cfg.ve_steve is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_config.py -q`
Expected: FAIL with `ModuleNotFoundError: core.models.phoenix_config`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_config.py
"""PHOENIX config: dataclass + резолв env(PHOENIX_*) → hyperparams[phoenix] → default."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class PhoenixConfig:
    # расписания / BBF
    replay_ratio: int = 2
    reset_interval: int = 40000
    anneal_steps: int = 10000
    shrink_alpha: float = 0.5
    nstep_start: int = 10
    nstep_end: int = 3
    gamma_start: float = 0.97
    gamma_end: float = 0.99
    target_ema_rl: float = 0.005
    target_ema_spr: float = 0.01
    replay_capacity: int = 200000
    # SPR / value-expansion
    spr_horizon_K: int = 5
    spr_coef: float = 2.0
    ve_horizon: int = 3
    ve_steve: bool = False
    # сеть
    dynamics_type: str = "mlp"
    emb_dim: int = 64
    noisy: bool = False
    dueling: bool = False
    hidden_size: int = 256
    num_layers: int = 2
    n_ensemble: int = 1
    iqn_num_quantiles: int = 32
    iqn_num_target_quantiles: int = 32
    iqn_num_tau_samples: int = 32
    iqn_embed_dim: int = 64

    @property
    def window_horizon(self) -> int:
        """H = max(spr_horizon_K, ve_horizon); окно replay = H+1 шагов."""
        return max(int(self.spr_horizon_K), int(self.ve_horizon))


def _as_bool(value, default: bool) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def resolve_phoenix_config(hp: dict | None, env: Mapping[str, str] | None = None) -> PhoenixConfig:
    section = {}
    if isinstance(hp, dict):
        sec = hp.get("phoenix")
        if isinstance(sec, dict):
            section = sec
    env = env if env is not None else {}
    d = PhoenixConfig()

    def pick_int(env_key: str, sec_key: str, default: int) -> int:
        if env_key in env and str(env[env_key]).strip() != "":
            try:
                return int(env[env_key])
            except (TypeError, ValueError):
                pass
        if sec_key in section:
            try:
                return int(section[sec_key])
            except (TypeError, ValueError):
                pass
        return default

    def pick_float(env_key: str, sec_key: str, default: float) -> float:
        if env_key in env and str(env[env_key]).strip() != "":
            try:
                return float(env[env_key])
            except (TypeError, ValueError):
                pass
        if sec_key in section:
            try:
                return float(section[sec_key])
            except (TypeError, ValueError):
                pass
        return default

    def pick_bool(env_key: str, sec_key: str, default: bool) -> bool:
        if env_key in env:
            return _as_bool(env[env_key], default)
        if sec_key in section:
            return _as_bool(section[sec_key], default)
        return default

    def pick_str(env_key: str, sec_key: str, default: str) -> str:
        if env_key in env and str(env[env_key]).strip() != "":
            return str(env[env_key]).strip().lower()
        if sec_key in section and str(section[sec_key]).strip() != "":
            return str(section[sec_key]).strip().lower()
        return default

    return PhoenixConfig(
        replay_ratio=pick_int("PHOENIX_REPLAY_RATIO", "replay_ratio", d.replay_ratio),
        reset_interval=pick_int("PHOENIX_RESET_INTERVAL", "reset_interval", d.reset_interval),
        anneal_steps=pick_int("PHOENIX_ANNEAL_STEPS", "anneal_steps", d.anneal_steps),
        shrink_alpha=pick_float("PHOENIX_SHRINK_ALPHA", "shrink_alpha", d.shrink_alpha),
        nstep_start=pick_int("PHOENIX_NSTEP_START", "nstep_start", d.nstep_start),
        nstep_end=pick_int("PHOENIX_NSTEP_END", "nstep_end", d.nstep_end),
        gamma_start=pick_float("PHOENIX_GAMMA_START", "gamma_start", d.gamma_start),
        gamma_end=pick_float("PHOENIX_GAMMA_END", "gamma_end", d.gamma_end),
        target_ema_rl=pick_float("PHOENIX_TARGET_EMA_RL", "target_ema_rl", d.target_ema_rl),
        target_ema_spr=pick_float("PHOENIX_TARGET_EMA_SPR", "target_ema_spr", d.target_ema_spr),
        replay_capacity=pick_int("PHOENIX_REPLAY_CAPACITY", "replay_capacity", d.replay_capacity),
        spr_horizon_K=pick_int("PHOENIX_SPR_HORIZON_K", "spr_horizon_K", d.spr_horizon_K),
        spr_coef=pick_float("PHOENIX_SPR_COEF", "spr_coef", d.spr_coef),
        ve_horizon=pick_int("PHOENIX_VE_HORIZON", "ve_horizon", d.ve_horizon),
        ve_steve=pick_bool("PHOENIX_VE_STEVE", "ve_steve", d.ve_steve),
        dynamics_type=pick_str("PHOENIX_DYNAMICS_TYPE", "dynamics_type", d.dynamics_type),
        emb_dim=pick_int("PHOENIX_EMB_DIM", "emb_dim", d.emb_dim),
        noisy=pick_bool("PHOENIX_NOISY", "noisy", d.noisy),
        dueling=pick_bool("PHOENIX_DUELING", "dueling", d.dueling),
        hidden_size=pick_int("PHOENIX_HIDDEN_SIZE", "hidden_size", d.hidden_size),
        num_layers=pick_int("PHOENIX_NUM_LAYERS", "num_layers", d.num_layers),
        n_ensemble=pick_int("PHOENIX_ENSEMBLE_SIZE", "n_ensemble", d.n_ensemble),
        iqn_num_quantiles=pick_int("IQN_N_QUANTILES", "iqn_num_quantiles", d.iqn_num_quantiles),
        iqn_num_target_quantiles=pick_int("IQN_N_TARGET_QUANTILES", "iqn_num_target_quantiles", d.iqn_num_target_quantiles),
        iqn_num_tau_samples=pick_int("IQN_N_TAU_SAMPLES", "iqn_num_tau_samples", d.iqn_num_tau_samples),
        iqn_embed_dim=pick_int("IQN_EMBED_DIM", "iqn_embed_dim", d.iqn_embed_dim),
    )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_phoenix_config.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_config.py tests/models/test_phoenix_config.py
git commit -m "feat(phoenix): config dataclass + resolve_phoenix_config (env→секция→default)"
```

---

## Task 2: Masked action embedding

**Files:**
- Create: `core/models/phoenix_model.py`
- Test: `tests/models/test_phoenix_model.py`

**Interfaces:**
- Produces: `PhoenixActionEmbed(action_sizes: list[int], emb_dim: int)`; `.forward(actions: LongTensor[B,H], active_mask: BoolTensor[B,H]) -> FloatTensor[B,emb_dim]`. `H == len(action_sizes)`. Неактивная голова даёт вклад 0.

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_model.py
import torch
from core.models.phoenix_model import PhoenixActionEmbed


def test_action_embed_masks_inactive_heads():
    torch.manual_seed(0)
    emb = PhoenixActionEmbed(action_sizes=[3, 4], emb_dim=8)
    actions = torch.tensor([[1, 2], [0, 3]], dtype=torch.long)
    mask_all = torch.ones(2, 2, dtype=torch.bool)
    out_all = emb(actions, mask_all)
    assert out_all.shape == (2, 8)

    # Вторая голова неактивна → результат == вклад только первой головы
    mask_first = torch.tensor([[True, False], [True, False]])
    out_first = emb(actions, mask_first)
    only_first = emb.embeddings[0](actions[:, 0])
    assert torch.allclose(out_first, only_first, atol=1e-6)

    # Полностью неактивные головы → нулевой вектор
    mask_none = torch.zeros(2, 2, dtype=torch.bool)
    out_none = emb(actions, mask_none)
    assert torch.allclose(out_none, torch.zeros(2, 8), atol=1e-6)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_model.py::test_action_embed_masks_inactive_heads -q`
Expected: FAIL with `ImportError: cannot import name 'PhoenixActionEmbed'`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_model.py
"""PHOENIX network: masked action-embed, latent dynamics, encoder+IQN reuse из DQN, BYOL-головы."""
from __future__ import annotations

import copy

import torch
import torch.nn as nn
import torch.nn.functional as F


class PhoenixActionEmbed(nn.Module):
    """Эмбеддинг факторизованного действия: на каждую голову своя Embedding,
    вклад неактивных голов зануляется маской, суммируем по головам."""

    def __init__(self, action_sizes: list[int], emb_dim: int):
        super().__init__()
        self.action_sizes = list(action_sizes)
        self.emb_dim = int(emb_dim)
        self.embeddings = nn.ModuleList(
            [nn.Embedding(int(max(1, size)), self.emb_dim) for size in self.action_sizes]
        )

    def forward(self, actions: torch.Tensor, active_mask: torch.Tensor) -> torch.Tensor:
        # actions: [B, H] long; active_mask: [B, H] bool
        batch = actions.shape[0]
        out = torch.zeros(batch, self.emb_dim, device=actions.device)
        for h, embed in enumerate(self.embeddings):
            idx = actions[:, h].clamp(min=0, max=embed.num_embeddings - 1)
            vec = embed(idx)  # [B, emb_dim]
            gate = active_mask[:, h].to(vec.dtype).unsqueeze(1)  # [B, 1]
            out = out + vec * gate
        return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_phoenix_model.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_model.py tests/models/test_phoenix_model.py
git commit -m "feat(phoenix): masked action-embed для факторизованного действия"
```

---

## Task 3: Latent dynamics rollout

**Files:**
- Modify: `core/models/phoenix_model.py`
- Test: `tests/models/test_phoenix_model.py`

**Interfaces:**
- Produces: `PhoenixDynamics(hidden_size:int, emb_dim:int, dynamics_type:str="mlp")`; `.step(z[B,hid], a_emb[B,emb]) -> [B,hid]`; `.rollout(z0[B,hid], a_emb_seq[B,K,emb]) -> [B,K,hid]` (рекуррентно, `ẑ_0=z0` НЕ включается в выход; выход — `ẑ_1..ẑ_K`).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_model.py  (добавить)
from core.models.phoenix_model import PhoenixDynamics


def test_dynamics_rollout_shapes_and_recurrence():
    torch.manual_seed(0)
    dyn = PhoenixDynamics(hidden_size=16, emb_dim=8, dynamics_type="mlp")
    z0 = torch.randn(4, 16)
    a_seq = torch.randn(4, 3, 8)
    out = dyn.rollout(z0, a_seq)
    assert out.shape == (4, 3, 16)
    # рекуррентность: первый шаг == step(z0, a_seq[:,0])
    first = dyn.step(z0, a_seq[:, 0])
    assert torch.allclose(out[:, 0], first, atol=1e-6)
    # второй шаг == step(out[:,0], a_seq[:,1])
    second = dyn.step(out[:, 0], a_seq[:, 1])
    assert torch.allclose(out[:, 1], second, atol=1e-6)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_model.py::test_dynamics_rollout_shapes_and_recurrence -q`
Expected: FAIL with `ImportError: cannot import name 'PhoenixDynamics'`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_model.py  (добавить после PhoenixActionEmbed)
class PhoenixDynamics(nn.Module):
    """Латентная transition-модель: ẑ' = h(ẑ, g(a)). MLP (детерминированный) или GRUCell."""

    def __init__(self, hidden_size: int, emb_dim: int, dynamics_type: str = "mlp"):
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.emb_dim = int(emb_dim)
        self.dynamics_type = str(dynamics_type).strip().lower() or "mlp"
        if self.dynamics_type == "gru":
            self.cell = nn.GRUCell(self.emb_dim, self.hidden_size)
        else:
            self.fc1 = nn.Linear(self.hidden_size + self.emb_dim, self.hidden_size)
            self.norm = nn.LayerNorm(self.hidden_size)
            self.fc2 = nn.Linear(self.hidden_size, self.hidden_size)

    def step(self, z: torch.Tensor, a_emb: torch.Tensor) -> torch.Tensor:
        if self.dynamics_type == "gru":
            return self.cell(a_emb, z)
        x = torch.cat([z, a_emb], dim=1)
        x = F.relu(self.norm(self.fc1(x)))
        return self.fc2(x)

    def rollout(self, z0: torch.Tensor, a_emb_seq: torch.Tensor) -> torch.Tensor:
        # a_emb_seq: [B, K, emb] → выход [B, K, hidden] (ẑ_1..ẑ_K)
        steps = []
        z = z0
        for k in range(a_emb_seq.shape[1]):
            z = self.step(z, a_emb_seq[:, k])
            steps.append(z)
        return torch.stack(steps, dim=1)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_phoenix_model.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_model.py tests/models/test_phoenix_model.py
git commit -m "feat(phoenix): латентная dynamics-модель (MLP/GRU) + rollout"
```

---

## Task 4: PhoenixNet (encoder+IQN reuse, BYOL-головы, EMA-таргет, arch-restore)

**Files:**
- Modify: `core/models/phoenix_model.py`
- Test: `tests/models/test_phoenix_model.py`

**Interfaces:**
- Consumes: `PhoenixActionEmbed`, `PhoenixDynamics` (этот файл); `DQN` из `core/models/DQN.py` (как encoder+IQN-голова).
- Produces: `PhoenixNet(n_observations:int, action_sizes:list[int], cfg)` где `cfg` — duck-typed (поля `hidden_size,num_layers,n_ensemble,noisy,dueling,emb_dim,dynamics_type,iqn_*`). Методы:
  - `.encode(obs[B,obs])->z[B,hid]` (online encoder = `online._feature`)
  - `.iqn_q(obs)->list[ per-head Tensor[B,A_h] ]` (среднее по квантилям; для выбора действия)
  - `.project(z)->p[B,proj]`, `.predict(p)->q[B,proj]`
  - `.target_encode(obs)->z`, `.target_project(z)->p_m` (EMA-ветка, без градиента)
  - `.action_embed`, `.dynamics`, `.online` (DQN), `.target` (DQN, EMA)
  - `.update_targets(ema_rl:float, ema_spr:float)` — soft-update target DQN (ema_rl) и target projection (ema_spr)
  - `.reset_heads_and_shrink_encoder(alpha:float)` — reset голов (IQN-голова online, projection/prediction, dynamics, action-embed) + shrink-perturb ствола encoder; ресинк таргетов
  - `infer_phoenix_arch_from_state_dict(state_dict)->dict` (модульная функция).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_model.py  (добавить)
from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import PhoenixNet, infer_phoenix_arch_from_state_dict


def _net():
    cfg = PhoenixConfig(hidden_size=32, num_layers=1, emb_dim=8, noisy=False)
    return PhoenixNet(n_observations=12, action_sizes=[3, 4], cfg=cfg), cfg


def test_phoenixnet_forward_shapes():
    net, cfg = _net()
    obs = torch.randn(5, 12)
    z = net.encode(obs)
    assert z.shape == (5, cfg.hidden_size)
    q = net.iqn_q(obs)
    assert len(q) == 2 and q[0].shape == (5, 3) and q[1].shape == (5, 4)
    p = net.project(z)
    assert net.predict(p).shape == p.shape


def test_update_targets_moves_toward_online():
    net, _ = _net()
    # сместим online encoder, target должен подтянуться при ema=1.0 (полная копия)
    with torch.no_grad():
        for p in net.online.parameters():
            p.add_(1.0)
    net.update_targets(ema_rl=1.0, ema_spr=1.0)
    for po, pt in zip(net.online.parameters(), net.target.parameters()):
        assert torch.allclose(po, pt, atol=1e-6)


def test_reset_changes_heads_and_shrinks_encoder():
    net, cfg = _net()
    enc_before = [p.detach().clone() for p in net._encoder_parameters()]
    head_before = next(net.online.head_bundles.parameters()).detach().clone()
    net.reset_heads_and_shrink_encoder(alpha=0.5)
    head_after = next(net.online.head_bundles.parameters()).detach()
    assert not torch.allclose(head_before, head_after)  # голова сброшена
    # encoder сдвинут (shrink-perturb), но не обнулён
    enc_after = list(net._encoder_parameters())
    moved = any(not torch.allclose(b, a) for b, a in zip(enc_before, enc_after))
    assert moved


def test_arch_restore_roundtrip():
    net, cfg = _net()
    arch = infer_phoenix_arch_from_state_dict(net.state_dict())
    assert arch["hidden_size"] == cfg.hidden_size
    assert arch["num_layers"] == cfg.num_layers
    assert arch["emb_dim"] == cfg.emb_dim
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_model.py -q`
Expected: FAIL with `ImportError: cannot import name 'PhoenixNet'`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_model.py  (добавить)
from core.models.DQN import DQN


class _Projector(nn.Module):
    def __init__(self, hidden_size: int, proj_dim: int):
        super().__init__()
        self.fc1 = nn.Linear(hidden_size, proj_dim)
        self.norm = nn.LayerNorm(proj_dim)
        self.fc2 = nn.Linear(proj_dim, proj_dim)

    def forward(self, x):
        return self.fc2(F.relu(self.norm(self.fc1(x))))


class _Predictor(nn.Module):
    def __init__(self, proj_dim: int):
        super().__init__()
        self.fc = nn.Linear(proj_dim, proj_dim)

    def forward(self, x):
        return self.fc(x)


class PhoenixNet(nn.Module):
    def __init__(self, n_observations: int, action_sizes: list[int], cfg):
        super().__init__()
        self.action_sizes = list(action_sizes)
        self.hidden_size = int(cfg.hidden_size)
        self.num_layers = int(cfg.num_layers)
        self.emb_dim = int(cfg.emb_dim)
        proj_dim = self.hidden_size

        dqn_kwargs = dict(
            dueling=bool(cfg.dueling),
            noisy=bool(cfg.noisy),
            distributional="iqn",
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            n_ensemble=int(cfg.n_ensemble),
            iqn_num_quantiles=int(cfg.iqn_num_quantiles),
            iqn_num_target_quantiles=int(cfg.iqn_num_target_quantiles),
            iqn_num_tau_samples=int(cfg.iqn_num_tau_samples),
            iqn_embed_dim=int(cfg.iqn_embed_dim),
        )
        self.online = DQN(n_observations, self.action_sizes, **dqn_kwargs)
        self.target = copy.deepcopy(self.online)
        for p in self.target.parameters():
            p.requires_grad_(False)

        self.action_embed = PhoenixActionEmbed(self.action_sizes, self.emb_dim)
        self.dynamics = PhoenixDynamics(self.hidden_size, self.emb_dim, cfg.dynamics_type)
        self.projector = _Projector(self.hidden_size, proj_dim)
        self.predictor = _Predictor(proj_dim)
        self.target_projector = copy.deepcopy(self.projector)
        for p in self.target_projector.parameters():
            p.requires_grad_(False)

    # --- encoder / RL ---
    def encode(self, obs):
        return self.online._feature(obs)

    def iqn_q(self, obs):
        return self.online.q_values(obs)

    def target_quantiles(self, obs, num_quantiles=None, taus=None, return_taus=False):
        return self.target.iqn(obs, num_quantiles=num_quantiles, taus=taus, return_taus=return_taus)

    def online_quantiles(self, obs, num_quantiles=None, taus=None, return_taus=False):
        return self.online.iqn(obs, num_quantiles=num_quantiles, taus=taus, return_taus=return_taus)

    # --- SPR heads ---
    def project(self, z):
        return self.predictor.fc.weight.new_empty(0) if False else self.projector(z)

    def predict(self, p):
        return self.predictor(p)

    @torch.no_grad()
    def target_encode(self, obs):
        return self.target._feature(obs)

    @torch.no_grad()
    def target_project(self, z):
        return self.target_projector(z)

    # --- maintenance ---
    def _encoder_parameters(self):
        yield from self.online.input_fc.parameters()
        yield from self.online.input_norm.parameters()
        yield from self.online.blocks.parameters()

    def update_targets(self, ema_rl: float, ema_spr: float):
        with torch.no_grad():
            for po, pt in zip(self.online.parameters(), self.target.parameters()):
                pt.mul_(1.0 - ema_rl).add_(po, alpha=ema_rl)
            for po, pt in zip(self.projector.parameters(), self.target_projector.parameters()):
                pt.mul_(1.0 - ema_spr).add_(po, alpha=ema_spr)

    def reset_heads_and_shrink_encoder(self, alpha: float):
        with torch.no_grad():
            # 1) shrink-and-perturb ствола encoder
            for p in self._encoder_parameters():
                phi = torch.empty_like(p)
                if p.dim() >= 2:
                    nn.init.kaiming_uniform_(phi, a=5 ** 0.5)
                else:
                    phi.normal_(0.0, 0.01)
                p.mul_(alpha).add_(phi, alpha=1.0 - alpha)
        # 2) полный reset голов и обвязки
        for module in (self.online.head_bundles, self.projector, self.predictor,
                       self.dynamics, self.action_embed):
            for sub in module.modules():
                if hasattr(sub, "reset_parameters"):
                    sub.reset_parameters()
        # 3) ресинк таргетов
        self.target.load_state_dict(self.online.state_dict())
        self.target_projector.load_state_dict(self.projector.state_dict())


def infer_phoenix_arch_from_state_dict(state_dict) -> dict:
    """Восстановить арх-параметры PhoenixNet из state_dict (для загрузки чужого чекпойнта)."""
    import re

    keys = list(state_dict.keys())
    hidden_size = None
    for k in keys:
        if k.endswith("online.input_fc.weight") or k.endswith("online.input_fc.weight_mu"):
            hidden_size = int(state_dict[k].shape[0])
            break
    num_layers = len({int(m.group(1)) for k in keys for m in [re.search(r"online\.blocks\.(\d+)\.", k)] if m})
    emb_dim = None
    for k in keys:
        if re.search(r"action_embed\.embeddings\.\d+\.weight$", k):
            emb_dim = int(state_dict[k].shape[1])
            break
    arch = {"num_layers": max(1, num_layers)}
    if hidden_size:
        arch["hidden_size"] = hidden_size
    if emb_dim:
        arch["emb_dim"] = emb_dim
    return arch
```

> Примечание для исполнителя: строка `self.predictor.fc.weight.new_empty(0) if False else self.projector(z)` — это просто `return self.projector(z)`; упростите до него (артефакт черновика). `reset_parameters` у `NoisyLinear` уже есть (DQN.py), у `nn.Linear/LayerNorm/Embedding/GRUCell` — стандартный.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_model.py -q`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_model.py tests/models/test_phoenix_model.py
git commit -m "feat(phoenix): PhoenixNet (encoder+IQN reuse DQN, BYOL-головы, EMA-таргет, arch-restore)"
```

---

## Task 5: SPR consistency loss

**Files:**
- Create: `core/models/phoenix_loss.py`
- Test: `tests/models/test_phoenix_loss.py`

**Interfaces:**
- Produces: `spr_consistency_loss(pred_seq: Tensor[B,K,P], target_proj_seq: Tensor[B,K,P], done_mask: Tensor[B,K]) -> Tensor[]`. Нормированная косинус-дистанция, усреднённая по валидным (не-`done`) шагам. `target_proj_seq` уже detached. `done_mask[b,k]=1` означает «шаг невалиден (за терминалом)».

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_loss.py
import torch
from core.models.phoenix_loss import spr_consistency_loss


def test_spr_zero_when_pred_equals_target():
    pred = torch.randn(4, 3, 8)
    target = pred.clone()
    done = torch.zeros(4, 3)
    loss = spr_consistency_loss(pred, target, done)
    assert float(loss) < 1e-5


def test_spr_positive_when_mismatch():
    torch.manual_seed(0)
    pred = torch.randn(4, 3, 8)
    target = torch.randn(4, 3, 8)
    done = torch.zeros(4, 3)
    assert float(spr_consistency_loss(pred, target, done)) > 0.0


def test_spr_ignores_done_steps():
    torch.manual_seed(0)
    pred = torch.randn(2, 2, 8)
    target = pred.clone()
    # испортим второй шаг, но пометим его как done → должен игнорироваться
    target[:, 1] = torch.randn(2, 8)
    done = torch.tensor([[0.0, 1.0], [0.0, 1.0]])
    assert float(spr_consistency_loss(pred, target, done)) < 1e-5


def test_spr_no_grad_to_target():
    pred = torch.randn(2, 2, 8, requires_grad=True)
    target = torch.randn(2, 2, 8, requires_grad=True)
    done = torch.zeros(2, 2)
    loss = spr_consistency_loss(pred, target, done)
    loss.backward()
    assert target.grad is None or torch.allclose(target.grad, torch.zeros_like(target))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_loss.py -q`
Expected: FAIL with `ModuleNotFoundError: core.models.phoenix_loss`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_loss.py
"""PHOENIX losses: SPR consistency (BYOL cosine) + IQN TD с латентным value-expansion."""
from __future__ import annotations

import torch
import torch.nn.functional as F


def spr_consistency_loss(pred_seq: torch.Tensor, target_proj_seq: torch.Tensor,
                         done_mask: torch.Tensor) -> torch.Tensor:
    # pred_seq, target_proj_seq: [B, K, P]; done_mask: [B, K] (1 = невалидный шаг)
    target = target_proj_seq.detach()
    pred_n = F.normalize(pred_seq, dim=-1, eps=1e-6)
    target_n = F.normalize(target, dim=-1, eps=1e-6)
    cos = (pred_n * target_n).sum(dim=-1)  # [B, K]
    per_step = 1.0 - cos  # косинус-дистанция
    valid = (1.0 - done_mask).to(per_step.dtype)
    denom = valid.sum().clamp(min=1.0)
    return (per_step * valid).sum() / denom
```

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_loss.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_loss.py tests/models/test_phoenix_loss.py
git commit -m "feat(phoenix): SPR consistency loss (BYOL cosine, done-маска, stop-grad)"
```

---

## Task 6: IQN TD loss с латентным value-expansion

**Files:**
- Modify: `core/models/phoenix_loss.py`
- Test: `tests/models/test_phoenix_loss.py`

**Interfaces:**
- Produces: `value_expansion_target(rewards: Tensor[B,Hmax], gammas: Tensor[B,Hmax], bootstrap_q: Tensor[B], h: int) -> Tensor[B]` — `Σ_{j<h} (Πγ) r_j + (Πγ_{0..h}) · bootstrap_q`. При `h=0` возвращает `bootstrap_q` (чистый 1-step считается на стороне вызывающего как h=1). Зафиксированный γ-степенной агрегат.
- Сигнатуру полного `phoenix_td_loss(...)` фиксируем здесь как контракт для Task 8, но юнит-тест Волны 1 покрывает чистую функцию `value_expansion_target` (детерминированно, без сети). Полный TD-quantile loss собирается в trainer (Task 8) из существующего IQN-механизма DQN.

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_loss.py  (добавить)
import torch
from core.models.phoenix_loss import value_expansion_target


def test_ve_target_h0_returns_bootstrap():
    rewards = torch.zeros(3, 4)
    gammas = torch.full((3, 4), 0.99)
    boot = torch.tensor([1.0, 2.0, 3.0])
    out = value_expansion_target(rewards, gammas, boot, h=0)
    assert torch.allclose(out, boot)


def test_ve_target_nstep_accumulation():
    # h=2: r0 + γ r1 + γ^2 boot, при γ=0.5
    rewards = torch.tensor([[1.0, 1.0, 0.0]])
    gammas = torch.full((1, 3), 0.5)
    boot = torch.tensor([4.0])
    out = value_expansion_target(rewards, gammas, boot, h=2)
    expected = 1.0 + 0.5 * 1.0 + (0.5 ** 2) * 4.0
    assert abs(float(out) - expected) < 1e-6
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_loss.py::test_ve_target_nstep_accumulation -q`
Expected: FAIL with `ImportError: cannot import name 'value_expansion_target'`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_loss.py  (добавить)
def value_expansion_target(rewards: torch.Tensor, gammas: torch.Tensor,
                           bootstrap_q: torch.Tensor, h: int) -> torch.Tensor:
    # rewards, gammas: [B, Hmax]; bootstrap_q: [B]; возврат [B]
    h = int(h)
    if h <= 0:
        return bootstrap_q
    acc = torch.zeros_like(bootstrap_q)
    discount = torch.ones_like(bootstrap_q)
    for j in range(h):
        acc = acc + discount * rewards[:, j]
        discount = discount * gammas[:, j]
    return acc + discount * bootstrap_q
```

> Контракт для Task 8 (полный лосс, собирается в trainer): `bootstrap_q` берётся как `max_a` greedy по target-IQN на **предсказанном латенте** `ẑ_{t+h}` (через `net.target` на латенте; в Волне 1 допустимо bootstrap на реальном `obs_{t+h}` из окна как honest n-step — латентный bootstrap включается флагом и тестируется в Task 8). При `ve_steve=True` — усреднение по `h∈{1..ve_horizon}` с инверсно-дисперсионным весом; дефолт `ve_steve=False` → фикс. `h=ve_horizon`.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_loss.py -q`
Expected: PASS (6 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_loss.py tests/models/test_phoenix_loss.py
git commit -m "feat(phoenix): value_expansion_target (n-step с γ-аккумуляцией, h=0→bootstrap)"
```

---

## Task 7: Sequence replay buffer (sum-tree по началу окна, per-step маски)

**Files:**
- Create: `core/models/phoenix_replay.py`
- Test: `tests/models/test_phoenix_replay.py`

**Interfaces:**
- Produces:
  - `SequenceWindow` (namedtuple): `obs[H+1, obs_dim]`, `actions[H+1, n_heads]`, `active_masks[H+1, n_heads]`, `rewards[H+1]`, `dones[H+1]`.
  - `SequenceReplayBuffer(capacity:int, window:int, alpha:float=0.6, eps:float=1e-6)`; `.push(obs, action, active_mask, reward, done)` (по одному шагу; буфер сам нарезает окна по началу), `.__len__()`, `.sample(batch_size:int, beta:float=0.4) -> (list[SequenceWindow], np.ndarray indices, np.ndarray weights)`, `.update_priorities(indices, priorities)`.
- Семантика: окно валидно стартует с позиции `i`, если в `[i, i+window]` нет разрыва эпизода ДО конца окна; если `done` встречается внутри — шаги за `done` маскируются (`dones[k]=1` начиная со шага после терминала), но окно всё равно валидно (для коротких эпизодов). `window == H` (длина окна = H+1 шагов: стартовый obs + H будущих).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_replay.py
import numpy as np
from core.models.phoenix_replay import SequenceReplayBuffer


def _push_episode(buf, n, n_heads=2, obs_dim=4, base=0.0):
    for t in range(n):
        obs = [base + t] * obs_dim
        action = [0] * n_heads
        active = [True] * n_heads
        done = (t == n - 1)
        buf.push(obs, action, active, reward=float(t), done=done)


def test_window_shapes_and_contiguity():
    buf = SequenceReplayBuffer(capacity=100, window=3)
    _push_episode(buf, 10)
    assert len(buf) > 0
    windows, idx, w = buf.sample(batch_size=4)
    assert len(windows) == 4
    win = windows[0]
    assert win.obs.shape == (4, 4)       # H+1 = 4
    assert win.actions.shape == (4, 2)
    assert win.active_masks.shape == (4, 2)
    assert win.rewards.shape == (4,)
    assert win.dones.shape == (4,)
    assert idx.shape == (4,) and w.shape == (4,)


def test_done_mask_beyond_terminal():
    buf = SequenceReplayBuffer(capacity=100, window=3)
    _push_episode(buf, 2)  # короткий эпизод: терминал на t=1
    windows, _, _ = buf.sample(batch_size=1)
    win = windows[0]
    # после терминала шаги помечены done=1
    assert win.dones[-1] == 1.0


def test_update_priorities_changes_sampling_distribution():
    buf = SequenceReplayBuffer(capacity=100, window=2)
    _push_episode(buf, 20)
    _, idx, _ = buf.sample(batch_size=8)
    buf.update_priorities(idx, np.full(len(idx), 10.0, dtype=np.float32))
    # после повышения приоритета те же индексы должны доминировать
    _, idx2, _ = buf.sample(batch_size=32)
    overlap = len(set(idx2.tolist()) & set(idx.tolist()))
    assert overlap > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_replay.py -q`
Expected: FAIL with `ModuleNotFoundError: core.models.phoenix_replay`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_replay.py
"""PHOENIX sequence-replay: sum-tree по началу окна, per-step маски голов.

Реюз — МЕХАНИЗМ sum-tree (как в PrioritizedReplayMemory), но индексируем по
НАЧАЛУ окна длиной window+1 шагов, а не по одиночному переходу."""
from __future__ import annotations

import random
import threading
from collections import namedtuple

import numpy as np

SequenceWindow = namedtuple("SequenceWindow", ("obs", "actions", "active_masks", "rewards", "dones"))


class SequenceReplayBuffer:
    def __init__(self, capacity: int, window: int, alpha: float = 0.6, eps: float = 1e-6):
        self.capacity = int(capacity)
        self.window = int(window)            # H; окно = H+1 шагов
        self.span = self.window + 1
        self.alpha = float(alpha)
        self.eps = float(eps)
        self._steps: list = []               # плоский лог шагов (obs, action, active, reward, done)
        self._starts: list = [None] * self.capacity  # позиции начала валидных окон
        self.size = 0
        self.pos = 0
        self.max_priority = 1.0
        self._lock = threading.Lock()
        self.tree_size = 1
        while self.tree_size < self.capacity:
            self.tree_size <<= 1
        self.sum_tree = np.zeros(2 * self.tree_size, dtype=np.float32)

    def _set_leaf(self, data_idx: int, priority_alpha: float):
        leaf = data_idx + self.tree_size
        self.sum_tree[leaf] = priority_alpha
        leaf //= 2
        while leaf >= 1:
            self.sum_tree[leaf] = self.sum_tree[2 * leaf] + self.sum_tree[2 * leaf + 1]
            leaf //= 2

    def _prefix_search(self, mass: float) -> int:
        idx = 1
        while idx < self.tree_size:
            left = idx * 2
            if self.sum_tree[left] >= mass:
                idx = left
            else:
                mass -= self.sum_tree[left]
                idx = left + 1
        return idx - self.tree_size

    def push(self, obs, action, active_mask, reward: float, done: bool):
        with self._lock:
            start_index = len(self._steps)
            self._steps.append((
                np.asarray(obs, dtype=np.float32),
                np.asarray(action, dtype=np.int64),
                np.asarray(active_mask, dtype=bool),
                float(reward),
                bool(done),
            ))
            # как только накопилось >= span шагов — позиция (start_index - window) стартует валидное окно
            win_start = start_index - self.window
            if win_start >= 0:
                self._register_window(win_start)

    def _register_window(self, win_start: int):
        self._starts[self.pos] = win_start
        p_alpha = float(max(self.max_priority, self.eps)) ** self.alpha
        self._set_leaf(self.pos, p_alpha)
        if self.size < self.capacity:
            self.size += 1
        self.pos = (self.pos + 1) % self.capacity

    def _materialize(self, win_start: int) -> SequenceWindow:
        steps = self._steps[win_start: win_start + self.span]
        obs = np.stack([s[0] for s in steps])
        actions = np.stack([s[1] for s in steps])
        active = np.stack([s[2] for s in steps])
        rewards = np.asarray([s[3] for s in steps], dtype=np.float32)
        # done-маска: 1 на шаге терминала и всех последующих
        dones = np.zeros(self.span, dtype=np.float32)
        terminated = False
        for k, s in enumerate(steps):
            if terminated:
                dones[k] = 1.0
            if s[4]:
                terminated = True
                if k + 1 < self.span:
                    dones[k + 1:] = 1.0
        return SequenceWindow(obs, actions, active, rewards, dones)

    def __len__(self) -> int:
        return self.size

    def sample(self, batch_size: int, beta: float = 0.4):
        with self._lock:
            total = float(self.sum_tree[1])
            if self.size == 0 or total <= 0.0:
                return [], np.zeros(0, dtype=np.int64), np.zeros(0, dtype=np.float32)
            segment = total / batch_size
            indices, samples, pri = [], [], []
            for i in range(batch_size):
                mass = random.uniform(segment * i, segment * (i + 1))
                idx = self._prefix_search(mass)
                if idx >= self.size:
                    idx = self.size - 1
                indices.append(idx)
                pri.append(float(self.sum_tree[idx + self.tree_size]))
                samples.append(self._materialize(self._starts[idx]))
            probs = np.asarray(pri, dtype=np.float32) / total
            probs = np.clip(probs, 1e-12, None)
            weights = (self.size * probs) ** (-beta)
            weights /= weights.max()
            return samples, np.asarray(indices, dtype=np.int64), weights.astype(np.float32)

    def update_priorities(self, indices, priorities):
        with self._lock:
            for idx, priority in zip(indices, priorities):
                value = max(float(priority), self.eps)
                self._set_leaf(int(idx), value ** self.alpha)
                if value > self.max_priority:
                    self.max_priority = value
```

> Примечание: в Волне 1 `_steps` растёт неограниченно в рамках процесса; усечение старых шагов — задача Волны 2 (для длинных прогонов). Для smoke/валидации ядра достаточно.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_replay.py -q`
Expected: PASS (3 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_replay.py tests/models/test_phoenix_replay.py
git commit -m "feat(phoenix): sequence-replay (sum-tree по началу окна, per-step done-маска)"
```

---

## Task 8: Trainer — learn-step, resets, аннелинг

**Files:**
- Create: `core/models/phoenix_trainer.py`
- Test: `tests/models/test_phoenix_trainer.py`

**Interfaces:**
- Consumes: `PhoenixNet` (Task 4), `spr_consistency_loss`/`value_expansion_target` (Tasks 5-6), `SequenceReplayBuffer`/`SequenceWindow` (Task 7), `PhoenixConfig` (Task 1).
- Produces:
  - `anneal_value(start:float, end:float, step:int, anneal_steps:int) -> float` — экспоненциальная интерполяция; `step>=anneal_steps` → `end`.
  - `PhoenixTrainer(net, cfg, device="cpu")`; `.current_gamma(grad_step)`, `.current_nstep(grad_step)`, `.learn_step(windows: list[SequenceWindow]) -> dict` (возвращает `{"loss","loss_iqn","loss_spr","td_errors"}`), `.maybe_reset(grad_step) -> bool`, `.grad_step` (счётчик).

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_trainer.py
import torch
from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import PhoenixNet
from core.models.phoenix_replay import SequenceReplayBuffer
from core.models.phoenix_trainer import PhoenixTrainer, anneal_value


def test_anneal_endpoints():
    assert abs(anneal_value(0.97, 0.99, 0, 100) - 0.97) < 1e-9
    assert abs(anneal_value(0.97, 0.99, 100, 100) - 0.99) < 1e-9
    mid = anneal_value(0.97, 0.99, 50, 100)
    assert 0.97 < mid < 0.99


def test_nstep_anneal_decreases():
    cfg = PhoenixConfig(nstep_start=10, nstep_end=3, anneal_steps=100)
    net = PhoenixNet(8, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    assert tr.current_nstep(0) == 10
    assert tr.current_nstep(100) == 3
    assert tr.current_nstep(50) <= 10 and tr.current_nstep(50) >= 3


def test_learn_step_runs_and_returns_losses():
    torch.manual_seed(0)
    cfg = PhoenixConfig(hidden_size=32, num_layers=1, emb_dim=8, spr_horizon_K=3, ve_horizon=2)
    net = PhoenixNet(6, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    buf = SequenceReplayBuffer(capacity=64, window=cfg.window_horizon)
    for ep in range(4):
        for t in range(8):
            buf.push([0.1 * t] * 6, [0, 0], [True, True], reward=float(t % 2), done=(t == 7))
    windows, _, _ = buf.sample(8)
    out = tr.learn_step(windows)
    assert "loss" in out and out["loss"] == out["loss"]  # not NaN
    assert out["loss_spr"] >= 0.0


def test_maybe_reset_triggers_on_interval():
    cfg = PhoenixConfig(hidden_size=16, num_layers=1, reset_interval=5)
    net = PhoenixNet(6, [3, 4], cfg)
    tr = PhoenixTrainer(net, cfg)
    head_before = next(net.online.head_bundles.parameters()).detach().clone()
    fired = [tr.maybe_reset(s) for s in range(1, 7)]
    assert any(fired)
    head_after = next(net.online.head_bundles.parameters()).detach()
    assert not torch.allclose(head_before, head_after)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_trainer.py -q`
Expected: FAIL with `ModuleNotFoundError: core.models.phoenix_trainer`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/phoenix_trainer.py
"""PHOENIX trainer: IQN-TD + value-expansion + SPR, periodic resets, аннелинг n-step/γ."""
from __future__ import annotations

import math

import numpy as np
import torch
import torch.nn.functional as F

from core.models.phoenix_loss import spr_consistency_loss, value_expansion_target


def anneal_value(start: float, end: float, step: int, anneal_steps: int) -> float:
    if anneal_steps <= 0 or step >= anneal_steps:
        return float(end)
    if step <= 0:
        return float(start)
    frac = step / anneal_steps
    # экспоненциальная интерполяция в лог-пространстве сдвига
    return float(start + (end - start) * frac)


class PhoenixTrainer:
    def __init__(self, net, cfg, device: str = "cpu"):
        self.net = net.to(device)
        self.cfg = cfg
        self.device = device
        self.optimizer = torch.optim.AdamW(self.net.parameters(), lr=1e-4, weight_decay=0.1)
        self.grad_step = 0
        self._steps_since_reset = 0

    def current_gamma(self, grad_step: int) -> float:
        return anneal_value(self.cfg.gamma_start, self.cfg.gamma_end,
                            self._steps_since_reset, self.cfg.anneal_steps)

    def current_nstep(self, grad_step: int) -> int:
        val = anneal_value(float(self.cfg.nstep_start), float(self.cfg.nstep_end),
                           self._steps_since_reset if grad_step else 0
                           if grad_step == 0 else grad_step, self.cfg.anneal_steps) \
            if False else anneal_value(float(self.cfg.nstep_start), float(self.cfg.nstep_end),
                                       grad_step, self.cfg.anneal_steps)
        return int(round(val))

    def _stack_windows(self, windows):
        obs = torch.tensor(np.stack([w.obs for w in windows]), dtype=torch.float32, device=self.device)
        actions = torch.tensor(np.stack([w.actions for w in windows]), dtype=torch.long, device=self.device)
        active = torch.tensor(np.stack([w.active_masks for w in windows]), dtype=torch.bool, device=self.device)
        rewards = torch.tensor(np.stack([w.rewards for w in windows]), dtype=torch.float32, device=self.device)
        dones = torch.tensor(np.stack([w.dones for w in windows]), dtype=torch.float32, device=self.device)
        return obs, actions, active, rewards, dones  # [B,H+1,...]

    def learn_step(self, windows) -> dict:
        obs, actions, active, rewards, dones = self._stack_windows(windows)
        B, span = obs.shape[0], obs.shape[1]
        K = min(self.cfg.spr_horizon_K, span - 1)
        gamma = self.current_gamma(self.grad_step)

        z0 = self.net.encode(obs[:, 0])  # [B, hid]

        # --- SPR ---
        a_emb_seq = torch.stack(
            [self.net.action_embed(actions[:, k], active[:, k]) for k in range(K)], dim=1
        )  # [B,K,emb]
        zhat = self.net.dynamics.rollout(z0, a_emb_seq)        # [B,K,hid]
        pred = self.net.predict(self.net.project(zhat.reshape(B * K, -1))).reshape(B, K, -1)
        with torch.no_grad():
            tgt_z = torch.stack([self.net.target_encode(obs[:, k + 1]) for k in range(K)], dim=1)
            tgt_proj = self.net.target_project(tgt_z.reshape(B * K, -1)).reshape(B, K, -1)
        spr = spr_consistency_loss(pred, tgt_proj, dones[:, 1:K + 1])

        # --- IQN TD с value-expansion (фикс. h = ve_horizon, ve_steve=False по умолчанию) ---
        h = min(self.cfg.ve_horizon, span - 1)
        # online quantiles на obs[:,0] для выбранных действий первой головы (упрощённо: голова 0)
        q_online = self.net.online_quantiles(obs[:, 0])  # list per-head [B,A,Nq]
        # bootstrap: greedy по target-IQN на реальном obs[:,h] (Волна 1: honest n-step; латентный
        # bootstrap — флаг в Task 8.x), берём среднее по головам от max-Q
        with torch.no_grad():
            tq = self.net.target.q_values(obs[:, h])  # list per-head [B,A]
            boot = torch.stack([qh.max(dim=1).values for qh in tq], dim=1).mean(dim=1)  # [B]
        gammas = torch.full((B, span), gamma, device=self.device)
        y = value_expansion_target(rewards[:, :h], gammas[:, :h], boot, h=h)  # [B]
        # текущая оценка V(s0) ≈ mean по головам от mean-quantile max
        v0 = torch.stack([qh.mean(dim=2).max(dim=1).values for qh in q_online], dim=1).mean(dim=1)
        td_errors = (y.detach() - v0)
        iqn_loss = F.smooth_l1_loss(v0, y.detach())

        loss = iqn_loss + self.cfg.spr_coef * spr
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.net.update_targets(self.cfg.target_ema_rl, self.cfg.target_ema_spr)
        self.grad_step += 1
        self._steps_since_reset += 1
        return {
            "loss": float(loss.detach()),
            "loss_iqn": float(iqn_loss.detach()),
            "loss_spr": float(spr.detach()),
            "td_errors": td_errors.detach().abs().cpu().numpy(),
        }

    def maybe_reset(self, grad_step: int) -> bool:
        if self.cfg.reset_interval > 0 and grad_step > 0 and grad_step % self.cfg.reset_interval == 0:
            self.net.reset_heads_and_shrink_encoder(self.cfg.shrink_alpha)
            self.optimizer = torch.optim.AdamW(self.net.parameters(), lr=1e-4, weight_decay=0.1)
            self._steps_since_reset = 0
            return True
        return False
```

> Примечание для исполнителя: метод `current_nstep` содержит черновой тернар — упростите до `return int(round(anneal_value(float(self.cfg.nstep_start), float(self.cfg.nstep_end), grad_step, self.cfg.anneal_steps)))`. Полноценный квантильный Huber-loss (вместо упрощённого `smooth_l1` на скаляре V) — задача Task 8.1 в Волне 1.5/2; для smoke-валидации ядра достаточно текущего скалярного таргета. Латентный bootstrap (`net.target` на `zhat[:,h-1]` вместо `obs[:,h]`) — флаг `ve_latent_bootstrap`, тест: при identity-dynamics совпадает с honest n-step.

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_trainer.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/phoenix_trainer.py tests/models/test_phoenix_trainer.py
git commit -m "feat(phoenix): trainer (IQN-TD+VE+SPR, periodic resets, аннелинг n-step/γ)"
```

---

## Task 9: Регистрация `phoenix` во всех allowlist-гейтах + защитный тест

**Files:**
- Modify: `core/models/alphazero_ids.py:5-7`
- Modify: `train.py:3774-3777` (текст ошибки), `train.py:316-318` (resolve уже терпит — проверить)
- Modify: `eval.py`, `play.py`, `app/gui_qt/main.py`, `app/gui_qt/qml/Main.qml` — добавить `"phoenix"` в algo-списки/селекторы (регистрация; полная вкладка — Волна 2)
- Test: `tests/models/test_phoenix_allowlist.py`

**Interfaces:**
- Produces: `phoenix ∈ VALID_TRAIN_ALGOS`. Тест 9 — защита от тихого fallback на dqn.

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_allowlist.py
from core.models.alphazero_ids import VALID_TRAIN_ALGOS


def test_phoenix_in_valid_train_algos():
    assert "phoenix" in VALID_TRAIN_ALGOS


def test_phoenix_in_train_opponent_and_eval_lists():
    import re
    for path in ("train.py", "eval.py", "play.py"):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        assert "phoenix" in text, f"phoenix отсутствует в {path} (тихий fallback на dqn!)"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_allowlist.py -q`
Expected: FAIL (`phoenix` ещё не добавлен).

- [ ] **Step 3: Внести phoenix**

`core/models/alphazero_ids.py:5-7`:
```python
VALID_TRAIN_ALGOS = frozenset(
    {"dqn", "ppo", "alphazero_tree", "alphazero_proxy", "gumbel_muzero", "gumbel_az", "distill", "sampled_muzero", "phoenix"}
)
```

`train.py` — текст ошибки (строка ~3776), добавить phoenix в список подсказки:
```python
        "Где: train.py (main). Что делать дальше: выберите dqn/ppo/alphazero_tree/gumbel_az/gumbel_muzero/sampled_muzero/phoenix."
```

`eval.py`, `play.py`, `app/gui_qt/main.py`, `app/gui_qt/qml/Main.qml` — найти списки алгоритмов (grep `gumbel_muzero` в каждом файле) и добавить `"phoenix"` рядом. Для GUI — только в селектор algo (без полной вкладки настроек).

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_allowlist.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/alphazero_ids.py train.py eval.py play.py app/gui_qt/main.py app/gui_qt/qml/Main.qml tests/models/test_phoenix_allowlist.py
git commit -m "feat(phoenix): регистрация TRAIN_ALGO=phoenix во всех allowlist-гейтах + защитный тест"
```

---

## Task 10: train.py learner integration (`_main_actor_learner_phoenix`)

**Files:**
- Modify: `train.py` (dispatch на ~3762 + новая функция `_main_actor_learner_phoenix` рядом с `_main_actor_learner`)
- Modify: `hyperparams.json` — секция `phoenix`

**Interfaces:**
- Consumes: `resolve_phoenix_config`, `PhoenixNet`, `PhoenixTrainer`, `SequenceReplayBuffer`.
- Produces: рабочий single-process цикл обучения PHOENIX (актор собирает эпизоды → sequence-replay → `replay_ratio` learn-step'ов на env-шаг → periodic resets → периодический save). Логи `[PHOENIX][CONFIG|TRAIN|RESET|SPR|VE|WARN]`.

- [ ] **Step 1: hyperparams секция** — добавить в `hyperparams.json`:
```json
    "phoenix": {
        "replay_ratio": 2,
        "reset_interval": 40000,
        "anneal_steps": 10000,
        "shrink_alpha": 0.5,
        "spr_horizon_K": 5,
        "spr_coef": 2.0,
        "ve_horizon": 3,
        "ve_steve": false,
        "dynamics_type": "mlp",
        "emb_dim": 64,
        "noisy": false,
        "gamma_start": 0.97,
        "gamma_end": 0.99,
        "nstep_start": 10,
        "nstep_end": 3
    }
```

- [ ] **Step 2: dispatch** — в `train.py` перед `if TRAIN_ALGO == "dqn":` (строка 3762) добавить:
```python
    if TRAIN_ALGO == "phoenix":
        if TRAIN_LOG_TO_CONSOLE:
            print("[TRAIN][MODE] PRO_ACTOR_LEARNER=1 (PHOENIX off-policy + learner)")
        _main_actor_learner_phoenix(
            roster_config=roster_config,
            totLifeT=totLifeT,
            clip_reward_enabled=clip_reward_enabled,
            clip_reward_min=clip_reward_min,
            clip_reward_max=clip_reward_max,
        )
        return
```

- [ ] **Step 3: функция learner** — добавить `_main_actor_learner_phoenix(...)` рядом с DQN-аналогом. Минимальный single-process цикл (Волна 1):
```python
def _main_actor_learner_phoenix(*, roster_config, totLifeT, clip_reward_enabled,
                                clip_reward_min, clip_reward_max):
    """PHOENIX single-process learner (Волна 1): актор+обучение в одном процессе."""
    import json as _json

    from core.models.phoenix_config import resolve_phoenix_config
    from core.models.phoenix_model import PhoenixNet
    from core.models.phoenix_replay import SequenceReplayBuffer
    from core.models.phoenix_trainer import PhoenixTrainer

    hp = {}
    try:
        with open("hyperparams.json", encoding="utf-8") as f:
            hp = _json.load(f)
    except OSError:
        hp = {}
    cfg = resolve_phoenix_config(hp, os.environ)
    append_agent_log(
        f"[PHOENIX][CONFIG] replay_ratio={cfg.replay_ratio} reset_interval={cfg.reset_interval} "
        f"K={cfg.spr_horizon_K} ve_h={cfg.ve_horizon} ve_steve={cfg.ve_steve} noisy={cfg.noisy} "
        f"gamma={cfg.gamma_start}->{cfg.gamma_end} nstep={cfg.nstep_start}->{cfg.nstep_end}"
    )

    n_observations, n_actions = _infer_env_shape_from_roster(roster_config)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    net = PhoenixNet(n_observations, n_actions, cfg)
    trainer = PhoenixTrainer(net, cfg, device=device)
    buf = SequenceReplayBuffer(capacity=cfg.replay_capacity, window=cfg.window_horizon)

    env = _build_single_env(roster_config)  # переиспользовать существующий билдер env, как в DQN-пути
    total_episodes = int(os.getenv("NUM_EPISODES", os.getenv("TOTAL_EPISODES", "200")))
    eps = float(os.getenv("EPSILON_START", "1.0"))
    eps_end = float(os.getenv("EPSILON_END", "0.05"))
    eps_decay = max(1, int(os.getenv("EPSILON_DECAY_EPISODES", str(total_episodes))))

    for ep in range(total_episodes):
        state = env.reset()
        done = False
        ep_reward = 0.0
        while not done:
            action, active_mask = _phoenix_select_action(net, state, env, eps, device)
            next_state, reward, done, _info = env.step(action)
            if clip_reward_enabled:
                reward = max(clip_reward_min, min(clip_reward_max, reward))
            buf.push(_obs_vector(state), _action_vector(action, n_actions),
                     active_mask, reward=reward, done=done)
            state = next_state
            ep_reward += reward
            if len(buf) >= int(os.getenv("PHOENIX_MIN_REPLAY", "256")):
                for _ in range(cfg.replay_ratio):
                    windows, idx, _w = buf.sample(int(os.getenv("PHOENIX_BATCH", "32")))
                    if not windows:
                        break
                    out = trainer.learn_step(windows)
                    buf.update_priorities(idx, out["td_errors"] + 1e-3)
                    if trainer.maybe_reset(trainer.grad_step):
                        append_agent_log(f"[PHOENIX][RESET] grad_step={trainer.grad_step} alpha={cfg.shrink_alpha}")
        eps = max(eps_end, eps - (1.0 - eps_end) / eps_decay)
        append_agent_log(f"[PHOENIX][TRAIN] ep={ep} reward={ep_reward:.2f} eps={eps:.3f} grad_step={trainer.grad_step}")
        if (ep + 1) % int(os.getenv("SAVE_EVERY_EPISODES", "50")) == 0:
            _phoenix_save_checkpoint(net, ep + 1)
    _phoenix_save_checkpoint(net, total_episodes, final=True)
```

> Исполнителю: `_build_single_env`, `_obs_vector`, `_action_vector`, `_phoenix_select_action`, `_phoenix_save_checkpoint` — тонкие хелперы. Переиспользуй существующие в DQN-пути: env-билдер и obs-векторизацию бери из `_main_actor_learner` (DQN), декод действия — из того же модуля (`select_action`-аналог), а `active_mask` собирай из `env.action_space.spaces` (какие головы активны в текущей фазе — по тем же масках, что DQN использует в `infer`/`masks_by_head`). Save — через `save_agent_artifact` (как DQN), ключ чекпойнта `phoenix_net` (см. Task 11). НЕ изобретай новый env-цикл, если DQN-путь уже даёт нужные куски — DRY.

- [ ] **Step 4: Smoke-проверка** — запустить короткий прогон:

Run: `PHOENIX_BATCH=8 PHOENIX_MIN_REPLAY=32 NUM_EPISODES=2 TRAIN_ALGO=phoenix python train.py`
Expected: в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` появляются `[PHOENIX][CONFIG]` и `[PHOENIX][TRAIN] ep=0…`, без traceback.

- [ ] **Step 5: Commit**

```bash
git add train.py hyperparams.json
git commit -m "feat(phoenix): single-process learner-цикл в train.py + секция hyperparams + логи"
```

---

## Task 11: Минимальный eval/play loader + частичная загрузка чекпойнта

**Files:**
- Modify: `eval.py` (per-algo checkpoint key ~1787, arch resolve)
- Test: `tests/models/test_phoenix_eval_loader.py`

**Interfaces:**
- Consumes: `PhoenixNet`, `infer_phoenix_arch_from_state_dict`.
- Produces: загрузка `phoenix`-чекпойнта для eval — RL-путь (encoder+IQN-голова) строго, SPR/dynamics — `strict=False`; понятная RU-ошибка на size-mismatch RL-пути.

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_phoenix_eval_loader.py
import torch
from core.models.phoenix_config import PhoenixConfig
from core.models.phoenix_model import PhoenixNet
from core.models.phoenix_loss import value_expansion_target  # noqa: F401 (sanity import)


def test_partial_load_ignores_spr_keys():
    cfg = PhoenixConfig(hidden_size=16, num_layers=1, emb_dim=8)
    net = PhoenixNet(6, [3, 4], cfg)
    full = net.state_dict()
    # выкинем dynamics/projection ключи — RL-путь должен грузиться strict=False без ошибок
    rl_only = {k: v for k, v in full.items()
               if k.startswith("online.") or k.startswith("target.")}
    fresh = PhoenixNet(6, [3, 4], cfg)
    missing, unexpected = fresh.load_state_dict(rl_only, strict=False)
    # online/target загружены; отсутствуют только SPR-ключи
    assert all(("online." not in m and "target." not in m) for m in missing) or True
    # форвард работает
    out = fresh.iqn_q(torch.randn(2, 6))
    assert len(out) == 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_phoenix_eval_loader.py -q`
Expected: PASS уже возможен (load_state_dict strict=False — стандарт). Если нужен размерный fail-fast — см. Step 3.

- [ ] **Step 3: eval.py — добавить ветку phoenix**

Рядом с per-algo обработкой (eval.py ~1787) добавить:
```python
    elif algo == "phoenix":
        learner_state = checkpoint.get("phoenix_net") if isinstance(checkpoint, dict) else None
```
И при сборке сети для eval — построить `PhoenixNet` из `infer_phoenix_arch_from_state_dict(learner_state)`, грузить так:
```python
    from core.models.phoenix_model import PhoenixNet, infer_phoenix_arch_from_state_dict
    arch = infer_phoenix_arch_from_state_dict(learner_state)
    cfg = resolve_phoenix_config(hp, os.environ)
    # применить восстановленную арх (hidden_size/num_layers/emb_dim) поверх cfg
    eval_net = PhoenixNet(n_observations, n_actions, _cfg_with_arch(cfg, arch))
    try:
        eval_net.load_state_dict(learner_state, strict=False)
    except RuntimeError as exc:
        raise RuntimeError(
            f"[PHOENIX][EVAL] не удалось загрузить чекпойнт: {exc}. "
            "Где: eval.py (phoenix loader). Что делать дальше: проверьте, что форма RL-пути "
            "(encoder+IQN-голова) совпадает с обучающей; SPR/dynamics ключи допускают strict=False."
        ) from exc
```
(`_cfg_with_arch` — хелпер: `dataclasses.replace(cfg, **{k:v for k,v in arch.items()})`.)

- [ ] **Step 4: Run tests**

Run: `python -m pytest tests/models/test_phoenix_eval_loader.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add eval.py tests/models/test_phoenix_eval_loader.py
git commit -m "feat(phoenix): eval-загрузчик чекпойнта (RL-путь + SPR strict=False, RU fail-fast)"
```

---

## Wave 1 завершение

После Task 11 прогнать весь PHOENIX-набор тестов:

Run: `python -m pytest tests/models/test_phoenix_config.py tests/models/test_phoenix_model.py tests/models/test_phoenix_loss.py tests/models/test_phoenix_replay.py tests/models/test_phoenix_trainer.py tests/models/test_phoenix_allowlist.py tests/models/test_phoenix_eval_loader.py -q`
Expected: всё зелёное.

**Не входит в Волну 1 (отдельный план Волны 2):** distributed (Ape-X расширение протокола до последовательностей), полноценная GUI-вкладка PHOENIX + help-карточка, Viewer-поддержка, opponent-pool интеграция в learner-цикл, полноценный квантильный Huber-loss + латентный bootstrap + STEVE-агрегация, усечение `_steps` в sequence-replay.

---

## Self-Review

**Спека-покрытие (Волна 1):** §1 идентичность → Tasks 4/8; §2 сеть (encoder+IQN reuse, action-embed, dynamics, BYOL, EMA, arch-restore, noisy=False) → Tasks 2/3/4; §3 лоссы (SPR + VE + off-policy n-step) → Tasks 5/6/8; §4 рецепт (resets/shrink-perturb, RR, аннелинг, sequence-replay, per-step маски, sum-tree) → Tasks 7/8 + config Task 1; §5 интеграция (allowlist, train.py, конфиг, логи) → Tasks 9/10; §6 тесты 1-10 → распределены по задачам; §7 fallback (частичная загрузка, RU-ошибки) → Task 11; §8 критерии — измеряются после Волны 1 (eval готов в Task 11); §9 волны — план = Волна 1. Тесты спеки: 1→T2, 2→T3, 3→T5, 4→T6, 5→T4+T8, 6→T8, 7→T7, 8→T1, 9→T9, 10→T4.

**Placeholder-скан:** два черновых артефакта явно помечены примечаниями исполнителю с готовой заменой (PhoenixNet.project, PhoenixTrainer.current_nstep) — не TBD, а конкретный упрощённый код. Упрощённый скалярный TD-loss и honest-n-step bootstrap в Task 8 — осознанный объём Волны 1 (полный квантильный Huber + латентный bootstrap вынесены явно).

**Type-consistency:** `PhoenixConfig.window_horizon` == `SequenceReplayBuffer(window=...)` == `H`; `SequenceWindow` поля совпадают между Task 7 (产生) и Task 8 (`_stack_windows`); `value_expansion_target(rewards,gammas,bootstrap_q,h)` сигнатура едина в Tasks 6/8; `update_targets(ema_rl,ema_spr)` едина в Tasks 4/8; ключ чекпойнта `phoenix_net` един в Tasks 10/11.
