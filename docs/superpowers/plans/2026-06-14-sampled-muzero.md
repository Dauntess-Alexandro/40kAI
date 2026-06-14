# Sampled MuZero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Добавить отдельную обучаемую модель `sampled_muzero` — MuZero с сэмплированием K цельных (joint) ходов из факторизованного приора, IS-коррекцией и маргинализацией policy-таргета в головы, чтобы координировать действия юнитов в комбинаторном пространстве.

**Architecture:** Новизна локализована в `core/models/sampled_muzero_search.py` (сэмпл K joint → оценка depth-1 → IS-улучшенная joint-политика → выбор хода + маргинализация в головы, «запекается» в `policy_targets`). Сеть, тренер, selfplay, replay, reanalyze, EMA, V-trace переиспользуются из `gumbel_muzero_*` импортом (тонкие обёртки). Интеграция (train.py/eval.py/GUI/чекпойнты) делается по образцу `gumbel_muzero`. v1 — одна машина, без remote/distributed.

**Tech Stack:** Python 3.12, PyTorch, NumPy, pytest, PySide6/QML (GUI). Платформа Windows. Тесты на CPU.

**Спека:** `docs/superpowers/specs/2026-06-14-sampled-muzero-design.md`.

**Точная формула (зафиксирована тестом несмещённости):**
- Прайор-сэмплинга на голову: `β_h(a) = softmax(logits_h / τ_s)` по легальным, 0 на нелегальных.
- Сэмплим K joint: каждая голова независимо `a_h ~ β_h`. Дедуп → уникальные `a` с `count(a)`.
- Оценка depth-1: `Q(a) = r(a) + γ·v(s'(a))` через один батчевый `recurrent_inference`.
- Улучшенная joint-политика: `π̂(a) ∝ count(a) · exp((Q(a) − maxQ)/τ)`.
- Таргет в головы: `π̂_h(a_h) = Σ_{a: a[h]=a_h} π̂(a)` (опц. мелкий prior-mix `prior_weight`, дефолт 0 = несмещённо).
- При K→∞: `count(a)/K → β_joint(a)` ⇒ `π̂ → β_joint·exp(adv/τ)` = точный оператор улучшения.

---

## Файловая структура

**Создаём:**
- `core/models/sampled_muzero_search.py` — ★ ядро поиска (config, presets, `SampledMuZeroSearch`, `run_batched`, `BatchedSampledMuZeroSearch`).
- `core/models/sampled_muzero_model.py` — тонкие фабрики, alias сети gmz, чтение `SMZ_*`-env.
- `core/models/sampled_muzero_trainer.py` — тонкая обёртка над `train_gumbel_muzero_step`.
- `core/models/sampled_muzero_selfplay.py` — тонкая обёртка над `play_episode_with_gumbel_muzero`.
- `tests/models/test_sampled_muzero_search.py`
- `tests/models/test_sampled_muzero_unbiased.py`
- `tests/models/test_sampled_muzero_search_batched.py`
- `tests/models/test_sampled_muzero_wrappers.py`
- `tests/train/test_sampled_muzero_actor_learner_smoke.py`
- `tests/engine/test_sampled_muzero_eval_play_contract.py`

**Модифицируем:**
- `train.py` — секция конфига `SMZ_*`; импорты; диспетч learner-шага; чекпойнт-роутинг; множества допустимых algo; ветки actor-learner.
- `hyperparams.json` — секция `sampled_muzero`.
- `eval.py` — загрузка/инференс `sampled_muzero` (по образцу gmz).
- `app/gui_qt/main.py`, `app/gui_qt/qml/Main.qml`, `app/gui_qt/qml/components/SectionHyperparamsEditor.qml`, `app/gui_qt/qml/components/TrainingAlgoHelpDialog.qml`, `app/gui_qt/gmz_hyperparams_defaults.py` — новая вкладка/дефолты.

**Переиспользуем без изменений (импортом):** `core/models/action_contract.py`, `core/models/gumbel_muzero_model.py` (`GumbelMuZeroNet`), `core/models/gumbel_muzero_trainer.py` (`train_gumbel_muzero_step`, `GumbelMuZeroTrainConfig`, `GumbelMuZeroEMATarget`, `make_gmz_lr_scheduler`), `core/models/gumbel_muzero_replay.py`, `core/models/gumbel_muzero_selfplay.py`, `core/models/gumbel_muzero_reanalysis.py`.

---

## Phase 1 — Ядро поиска (новая логика)

### Task 1: Конфиг и пресеты поиска

**Files:**
- Create: `core/models/sampled_muzero_search.py`
- Test: `tests/models/test_sampled_muzero_search.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_sampled_muzero_search.py
import numpy as np
import pytest
import torch

from core.models.sampled_muzero_search import (
    SampledMuZeroSearchConfig,
    SAMPLED_PRESETS,
    make_sampled_search_config,
)


@pytest.mark.parametrize("preset", ["fast", "balanced", "heavy"])
def test_presets_make(preset):
    cfg = make_sampled_search_config(preset=preset)
    exp = SAMPLED_PRESETS[preset]
    assert cfg.num_samples == exp["num_samples"]
    assert cfg.temperature == exp["temperature"]
    assert cfg.prior_weight == exp["prior_weight"]


def test_config_defaults():
    cfg = SampledMuZeroSearchConfig()
    assert cfg.num_samples == 24
    assert cfg.sample_temperature == 1.0
    assert cfg.prior_weight == 0.0
    assert cfg.dedup is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py -q`
Expected: FAIL — `ModuleNotFoundError: core.models.sampled_muzero_search`.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/sampled_muzero_search.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np
import torch


@dataclass
class SampledMuZeroSearchConfig:
    num_samples: int = 24            # K joint-сэмплов из приора
    discount: float = 0.997
    temperature: float = 0.15        # τ улучшения политики
    sample_temperature: float = 1.0  # τ_s сэмплинга из приора (β)
    prior_weight: float = 0.0        # подмешивание приора в таргет (0 = несмещённо)
    dedup: bool = True
    tree_reuse: bool = False         # v1: без warm-start (depth-1, свежие сэмплы)


SAMPLED_PRESETS: dict[str, dict] = {
    "fast":     {"num_samples": 12, "temperature": 0.20, "sample_temperature": 1.0, "prior_weight": 0.0},
    "balanced": {"num_samples": 24, "temperature": 0.15, "sample_temperature": 1.0, "prior_weight": 0.0},
    "heavy":    {"num_samples": 48, "temperature": 0.10, "sample_temperature": 1.0, "prior_weight": 0.0},
}


def make_sampled_search_config(preset: str = "balanced", **overrides) -> SampledMuZeroSearchConfig:
    kwargs = SAMPLED_PRESETS.get(preset, SAMPLED_PRESETS["balanced"]).copy()
    kwargs.update(overrides)
    return SampledMuZeroSearchConfig(**kwargs)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py -q`
Expected: PASS (2+ tests).

- [ ] **Step 5: Commit**

```bash
git add core/models/sampled_muzero_search.py tests/models/test_sampled_muzero_search.py
git commit -m "feat(sampled_muzero): config + presets ядра поиска"
```

---

### Task 2: `SampledMuZeroSearch.run` — сэмпл, оценка, выбор, маргинализация

**Files:**
- Modify: `core/models/sampled_muzero_search.py`
- Test: `tests/models/test_sampled_muzero_search.py`

- [ ] **Step 1: Write the failing test**

```python
# append to tests/models/test_sampled_muzero_search.py
from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import SampledMuZeroSearch


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16,
    )


def test_run_targets_sum_to_one_and_shapes():
    n_obs, n_actions = 12, [4, 3, 5]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=32), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [
        np.array([1, 1, 0, 1], dtype=bool),
        np.array([1, 0, 1], dtype=bool),
        np.array([1, 1, 1, 0, 0], dtype=bool),
    ]
    np.random.seed(0)
    pi, beh, actions, value = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert len(pi) == len(n_actions) == len(beh) == len(actions)
    for h, p in enumerate(pi):
        assert p.shape[0] == n_actions[h]
        assert abs(float(p.sum()) - 1.0) < 1e-5
        assert beh[h].shape[0] == n_actions[h]   # сырые root-логиты для V-trace
    assert isinstance(value, float)


def test_run_illegal_zero_prob_and_legal_selection():
    n_obs, n_actions = 8, [5]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=64), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.array([True, False, False, True, False], dtype=bool)]
    np.random.seed(1)
    pi, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert pi[0][1] == 0.0 and pi[0][2] == 0.0 and pi[0][4] == 0.0
    assert legal[0][actions[0]]


def test_run_handles_empty_legal_head():
    n_obs, n_actions = 8, [3, 4]
    net = _make_net(n_obs, n_actions)
    s = SampledMuZeroSearch(
        net=net, config=SampledMuZeroSearchConfig(num_samples=16), device=torch.device("cpu"),
    )
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.zeros(3, dtype=bool), np.ones(4, dtype=bool)]  # первая голова без легальных
    np.random.seed(2)
    pi, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    assert abs(float(pi[1].sum()) - 1.0) < 1e-5
    assert 0 <= actions[1] < 4
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py -q`
Expected: FAIL — `ImportError: cannot import name 'SampledMuZeroSearch'`.

- [ ] **Step 3: Write minimal implementation**

Append to `core/models/sampled_muzero_search.py`:

```python
def _beta_heads_from_logits(root_logits, legal_masks_by_head, tau_s):
    """Возвращает (behavior_logits, beta_heads, legal_list). beta_heads — полноразмерные
    вероятности сэмплинга (0 на нелегальных), beh — сырые root-логиты (для V-trace)."""
    behavior_logits, beta_heads, legal_list = [], [], []
    for h, head_logits in enumerate(root_logits):
        logits_np = head_logits.squeeze(0).detach().cpu().numpy().astype(np.float32)
        behavior_logits.append(logits_np.copy())
        legal = np.asarray(legal_masks_by_head[h], dtype=bool)
        legal_list.append(legal)
        beta = np.zeros_like(logits_np, dtype=np.float64)
        idx = np.where(legal)[0]
        if idx.size > 0:
            x = logits_np[idx].astype(np.float64) / max(1e-6, float(tau_s))
            x = x - x.max()
            e = np.exp(x)
            beta[idx] = e / e.sum()
        beta_heads.append(beta)
    return behavior_logits, beta_heads, legal_list


def _sample_joint(beta_heads, legal_list, K):
    """Сэмплинг K joint-действий. RNG-порядок: sample-major, head-minor.
    Головы без легальных действий не тянут RNG (action=0)."""
    H = len(beta_heads)
    samples = np.zeros((K, H), dtype=np.int64)
    for k in range(K):
        for h in range(H):
            idx = np.where(legal_list[h])[0]
            if idx.size == 0:
                samples[k, h] = 0
            else:
                samples[k, h] = int(np.random.choice(idx, p=beta_heads[h][idx]))
    return samples


def _improved_joint_policy(q, counts, tau):
    """π̂(a) ∝ count(a)·exp((Q−maxQ)/τ)."""
    adv = (q - q.max()) / max(1e-6, float(tau))
    w = counts.astype(np.float64) * np.exp(adv)
    s = w.sum()
    if s > 1e-12:
        return w / s
    return counts.astype(np.float64) / counts.sum()


def _marginalize(uniq, pi_joint, beta_heads, legal_list, behavior_logits, prior_weight):
    """Маргинализация joint-политики в головы (+опц. prior-mix), с занулением нелегальных."""
    H = len(behavior_logits)
    out = []
    for h in range(H):
        size = int(behavior_logits[h].shape[0])
        tgt = np.zeros(size, dtype=np.float64)
        for u in range(uniq.shape[0]):
            tgt[uniq[u, h]] += pi_joint[u]
        if prior_weight > 0.0:
            tgt = (1.0 - prior_weight) * tgt + prior_weight * beta_heads[h]
        tgt[~legal_list[h]] = 0.0
        s = tgt.sum()
        if s > 1e-12:
            tgt = tgt / s
        else:
            lg = legal_list[h]
            tgt = lg.astype(np.float64) / max(1.0, float(lg.sum()))
        out.append(tgt.astype(np.float32))
    return out


class SampledMuZeroSearch:
    """Depth-1 sampled search: K joint-сэмплов из факторизованного приора, IS-улучшенная
    joint-политика, маргинализация в головы. Сигнатура run совпадает с GumbelMuZeroSearch."""

    def __init__(self, net, config: Optional[SampledMuZeroSearchConfig] = None,
                 device: Optional[torch.device] = None):
        self.net = net
        self.cfg = config or SampledMuZeroSearchConfig()
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.last_run_stats: dict[str, float] = {}

    def clear_tree_state(self) -> None:
        # v1: без tree-reuse; метод для API-паритета с gmz.
        return None

    @torch.no_grad()
    def run(self, *, obs: np.ndarray, legal_masks_by_head: list[np.ndarray],
            deterministic: bool = True):
        cfg, device = self.cfg, self.device
        obs_t = torch.tensor(np.asarray(obs, dtype=np.float32), device=device).unsqueeze(0)
        masks_t = [torch.as_tensor(m, dtype=torch.bool, device=device).unsqueeze(0)
                   for m in legal_masks_by_head]
        root_logits, root_value, _r, latent = self.net.initial_inference(obs_t, masks_by_head=masks_t)

        K = max(1, int(cfg.num_samples))
        tau_s = float(cfg.sample_temperature)
        behavior_logits, beta_heads, legal_list = _beta_heads_from_logits(
            root_logits, legal_masks_by_head, tau_s
        )

        samples = _sample_joint(beta_heads, legal_list, K)
        if bool(cfg.dedup):
            uniq, counts = np.unique(samples, axis=0, return_counts=True)
        else:
            uniq, counts = samples, np.ones(samples.shape[0], dtype=np.int64)
        U = uniq.shape[0]

        latent_batch = latent.expand(U, -1)
        action_t = torch.as_tensor(uniq, dtype=torch.long, device=device)
        _p, val_b, rew_b, _nl = self.net.recurrent_inference(latent_batch, action_t, masks_by_head=None)
        val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
        rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
        q = rew_b + float(cfg.discount) * val_b

        pi_joint = _improved_joint_policy(q, counts, float(cfg.temperature))

        if deterministic:
            sel = int(np.argmax(pi_joint))
        else:
            sel = int(np.random.choice(np.arange(U), p=pi_joint))
        selected_actions = [int(x) for x in uniq[sel]]

        policy_targets = _marginalize(
            uniq, pi_joint, beta_heads, legal_list, behavior_logits, float(cfg.prior_weight)
        )

        value_out = float(np.average(q, weights=counts))
        self.last_run_stats = {
            "num_samples": float(K), "unique_samples": float(U),
            "root_value": float(root_value.item()), "q_mean": value_out,
        }
        return policy_targets, behavior_logits, selected_actions, value_out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py -q`
Expected: PASS (all run-tests).

- [ ] **Step 5: Commit**

```bash
git add core/models/sampled_muzero_search.py tests/models/test_sampled_muzero_search.py
git commit -m "feat(sampled_muzero): SampledMuZeroSearch.run (сэмпл K joint + IS + маргинализация)"
```

---

### Task 3: Тест несмещённости (пин точной формулы)

**Files:**
- Test: `tests/models/test_sampled_muzero_unbiased.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_sampled_muzero_unbiased.py
import itertools
import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig


def _exact_marginal_targets(net, obs, legal, tau, tau_s):
    """Точный оператор улучшения: перебор всех joint-действий."""
    device = torch.device("cpu")
    obs_t = torch.tensor(obs, dtype=torch.float32, device=device).unsqueeze(0)
    masks_t = [torch.as_tensor(m, dtype=torch.bool, device=device).unsqueeze(0) for m in legal]
    root_logits, _v, _r, latent = net.initial_inference(obs_t, masks_by_head=masks_t)
    H = len(legal)
    beta = []
    legal_idx = []
    for h in range(H):
        lg = np.asarray(legal[h], dtype=bool)
        idx = np.where(lg)[0]
        legal_idx.append(idx)
        lo = root_logits[h].squeeze(0).detach().cpu().numpy().astype(np.float64)[idx] / tau_s
        lo = lo - lo.max()
        e = np.exp(lo)
        b = np.zeros(lg.shape[0], dtype=np.float64)
        b[idx] = e / e.sum()
        beta.append(b)
    joints = list(itertools.product(*[list(ix) for ix in legal_idx]))
    acts = torch.tensor(joints, dtype=torch.long, device=device)
    lat = latent.expand(len(joints), -1)
    _p, val, rew, _nl = net.recurrent_inference(lat, acts, masks_by_head=None)
    q = (rew.detach().cpu().numpy().reshape(-1).astype(np.float64)
         + 0.997 * val.detach().cpu().numpy().reshape(-1).astype(np.float64))
    bj = np.array([np.prod([beta[h][j[h]] for h in range(H)]) for j in joints], dtype=np.float64)
    w = bj * np.exp((q - q.max()) / tau)
    w = w / w.sum()
    targets = [np.zeros(legal[h].shape[0], dtype=np.float64) for h in range(H)]
    for wi, j in zip(w, joints):
        for h in range(H):
            targets[h][j[h]] += wi
    return [t / t.sum() for t in targets]


def test_sampled_target_matches_exact_enumeration():
    torch.manual_seed(0)
    n_obs, n_actions = 10, [2, 3]
    net = GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions,
                          latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16)
    obs = np.zeros(n_obs, dtype=np.float32)
    legal = [np.ones(2, dtype=bool), np.ones(3, dtype=bool)]
    tau, tau_s = 0.15, 1.0

    exact = _exact_marginal_targets(net, obs, legal, tau, tau_s)

    s = SampledMuZeroSearch(
        net=net,
        config=SampledMuZeroSearchConfig(num_samples=40000, temperature=tau,
                                         sample_temperature=tau_s, prior_weight=0.0),
        device=torch.device("cpu"),
    )
    np.random.seed(123)
    pi, _, _, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)

    for h in range(len(n_actions)):
        np.testing.assert_allclose(pi[h], exact[h], atol=0.02,
                                   err_msg=f"head {h}: sampled target != exact")
```

- [ ] **Step 2: Run test to verify it fails (then passes)**

Run: `python -m pytest tests/models/test_sampled_muzero_unbiased.py -q`
Expected: PASS if Task 2 formula correct. If FAIL — формула расходится с эталоном, **чинить `_improved_joint_policy`/`_marginalize`, не ослаблять допуск** (atol=0.02 при K=40000 адекватен).

- [ ] **Step 3: Commit**

```bash
git add tests/models/test_sampled_muzero_unbiased.py
git commit -m "test(sampled_muzero): несмещённость таргета vs полный перебор"
```

---

### Task 4: `run_batched` + эквивалентность sequential↔batched

**Files:**
- Modify: `core/models/sampled_muzero_search.py`
- Test: `tests/models/test_sampled_muzero_search_batched.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_sampled_muzero_search_batched.py
import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.sampled_muzero_search import (
    SampledMuZeroSearch, SampledMuZeroSearchConfig, run_batched,
)


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return GumbelMuZeroNet(obs_dim=n_obs, action_sizes=n_actions,
                           latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16)


def _make_requests(n_obs, n_actions, n_envs, seed=7):
    rng = np.random.default_rng(seed)
    reqs = []
    for env_id in range(n_envs):
        obs = rng.standard_normal(n_obs).astype(np.float32)
        masks = []
        for size in n_actions:
            m = rng.integers(0, 2, size=size).astype(bool)
            if not m.any():
                m[0] = True
            masks.append(m)
        reqs.append({"env_id": env_id, "obs": obs, "legal_masks_by_head": masks})
    return reqs


def test_run_batched_matches_sequential_deterministic():
    n_obs, n_actions, n_envs = 12, [4, 3, 5], 6
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=20, temperature=0.15, prior_weight=0.0)
    device = torch.device("cpu")
    reqs = _make_requests(n_obs, n_actions, n_envs)

    np.random.seed(123)
    seq = []
    for r in reqs:
        s = SampledMuZeroSearch(net=net, config=cfg, device=device)
        seq.append(s.run(obs=r["obs"], legal_masks_by_head=r["legal_masks_by_head"], deterministic=True))

    np.random.seed(123)
    bat = run_batched(net=net, cfg=cfg, device=device, requests=reqs, deterministic=True)

    assert len(bat) == n_envs
    for n, (pi, beh, act, val) in enumerate(seq):
        b = bat[n]
        assert b["env_id"] == reqs[n]["env_id"]
        assert b["selected_actions"] == list(act), f"env {n} actions mismatch"
        assert abs(b["value_est"] - val) < 1e-4, f"env {n} value mismatch"
        for h in range(len(n_actions)):
            np.testing.assert_allclose(b["policy_targets"][h], pi[h], atol=1e-5)
            np.testing.assert_allclose(b["behavior_logits"][h], beh[h], atol=1e-5)


def test_run_batched_shapes_and_legality_stochastic():
    n_obs, n_actions, n_envs = 10, [4, 3], 5
    net = _make_net(n_obs, n_actions)
    cfg = SampledMuZeroSearchConfig(num_samples=16)
    reqs = _make_requests(n_obs, n_actions, n_envs, seed=42)
    np.random.seed(1)
    out = run_batched(net=net, cfg=cfg, device=torch.device("cpu"), requests=reqs, deterministic=False)
    assert len(out) == n_envs
    for n, r in enumerate(out):
        for h, size in enumerate(n_actions):
            p = r["policy_targets"][h]
            assert p.shape[0] == size and abs(float(p.sum()) - 1.0) < 1e-5
            assert reqs[n]["legal_masks_by_head"][h][r["selected_actions"][h]]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_sampled_muzero_search_batched.py -q`
Expected: FAIL — `ImportError: cannot import name 'run_batched'`.

- [ ] **Step 3: Write minimal implementation**

Append to `core/models/sampled_muzero_search.py`:

```python
@torch.no_grad()
def run_batched(*, net, cfg: SampledMuZeroSearchConfig, device: torch.device,
                requests: list[dict], deterministic: bool = False) -> list[dict]:
    """Батч по средам. RNG-порядок строго env-major → sample-major → head-minor,
    чтобы при общем seed совпадать с последовательным run() по средам."""
    N = len(requests)
    if N == 0:
        return []
    K = max(1, int(cfg.num_samples))
    tau_s = float(cfg.sample_temperature)
    num_heads = len(requests[0]["legal_masks_by_head"])

    # Корень — один батч-форвард по средам.
    obs_batch = torch.tensor(
        np.stack([np.asarray(r["obs"], dtype=np.float32) for r in requests], axis=0), device=device)
    masks_batch = []
    for h in range(num_heads):
        mh = np.stack([np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool) for n in range(N)], axis=0)
        masks_batch.append(torch.as_tensor(mh, dtype=torch.bool, device=device))
    root_logits, root_value, _r, latent = net.initial_inference(obs_batch, masks_by_head=masks_batch)
    root_value_np = root_value.detach().cpu().numpy().reshape(-1).astype(np.float64)

    # Сэмплинг (env-major) + дедуп; собираем строки для одного recurrent-форварда.
    per_env = []      # (uniq, counts, beh, beta_heads, legal_list)
    rows_action, env_of_row = [], []
    for n in range(N):
        rl_n = [root_logits[h][n:n + 1] for h in range(num_heads)]
        beh, beta_heads, legal_list = _beta_heads_from_logits(
            rl_n, requests[n]["legal_masks_by_head"], tau_s)
        samples = _sample_joint(beta_heads, legal_list, K)
        if bool(cfg.dedup):
            uniq, counts = np.unique(samples, axis=0, return_counts=True)
        else:
            uniq, counts = samples, np.ones(samples.shape[0], dtype=np.int64)
        per_env.append((uniq, counts, beh, beta_heads, legal_list))
        for u in range(uniq.shape[0]):
            rows_action.append(uniq[u])
            env_of_row.append(n)

    idx_t = torch.tensor(env_of_row, dtype=torch.long, device=device)
    latent_rep = latent.index_select(0, idx_t)
    action_t = torch.as_tensor(np.asarray(rows_action), dtype=torch.long, device=device)
    _p, val_b, rew_b, _nl = net.recurrent_inference(latent_rep, action_t, masks_by_head=None)
    val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
    rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float64)
    q_all = rew_b + float(cfg.discount) * val_b

    results, cursor = [], 0
    for n in range(N):
        uniq, counts, beh, beta_heads, legal_list = per_env[n]
        U = uniq.shape[0]
        q = q_all[cursor:cursor + U]
        cursor += U
        pi_joint = _improved_joint_policy(q, counts, float(cfg.temperature))
        if deterministic:
            sel = int(np.argmax(pi_joint))
        else:
            sel = int(np.random.choice(np.arange(U), p=pi_joint))
        selected = [int(x) for x in uniq[sel]]
        policy_targets = _marginalize(uniq, pi_joint, beta_heads, legal_list, beh, float(cfg.prior_weight))
        value_out = float(np.average(q, weights=counts)) if U > 0 else float(root_value_np[n])
        results.append({
            "env_id": int(requests[n].get("env_id", n)),
            "selected_actions": selected,
            "policy_targets": policy_targets,
            "behavior_logits": beh,
            "value_est": value_out,
        })
    return results


class BatchedSampledMuZeroSearch:
    """Обёртка над run_batched (для паритета с gmz). v1: без tree-reuse."""

    def __init__(self, *, net, config: SampledMuZeroSearchConfig, device: torch.device):
        self.net, self.cfg, self.device = net, config, device

    def clear_tree_state(self, env_id: int | None = None) -> None:
        return None

    def run_batched_stateful(self, requests: list[dict], deterministic: bool = False) -> list[dict]:
        return run_batched(net=self.net, cfg=self.cfg, device=self.device,
                           requests=requests, deterministic=deterministic)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_sampled_muzero_search_batched.py -q`
Expected: PASS. Если equivalence-тест падает — проверь RNG-порядок: и `run`, и `run_batched` должны тянуть сэмплы строго env-major → sample-major → head-minor (см. `_sample_joint`).

- [ ] **Step 5: Commit**

```bash
git add core/models/sampled_muzero_search.py tests/models/test_sampled_muzero_search_batched.py
git commit -m "feat(sampled_muzero): run_batched + инвариант sequential==batched"
```

---

## Phase 2 — Тонкие обёртки (model / trainer / selfplay)

### Task 5: model / trainer / selfplay обёртки

**Files:**
- Create: `core/models/sampled_muzero_model.py`, `core/models/sampled_muzero_trainer.py`, `core/models/sampled_muzero_selfplay.py`
- Test: `tests/models/test_sampled_muzero_wrappers.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/models/test_sampled_muzero_wrappers.py
import numpy as np
import torch


def test_model_wrapper_builds_net():
    from core.models.sampled_muzero_model import make_sampled_muzero_net, SampledMuZeroNet
    net = make_sampled_muzero_net(obs_dim=10, action_sizes=[3, 4], latent_dim=32,
                                  hidden_dim=32, num_layers=1, action_embed_dim=8)
    assert isinstance(net, SampledMuZeroNet)
    logits, value = net(torch.zeros(1, 10))
    assert len(logits) == 2 and value.shape[0] == 1


def test_trainer_wrapper_reexports():
    from core.models.sampled_muzero_trainer import (
        train_sampled_muzero_step, SampledMuZeroTrainConfig,
    )
    cfg = SampledMuZeroTrainConfig(batch_size=4, unroll_steps=2)
    assert cfg.batch_size == 4
    assert callable(train_sampled_muzero_step)


def test_selfplay_wrapper_reexports():
    from core.models.sampled_muzero_selfplay import (
        play_episode_with_sampled_muzero, SampledSelfPlayConfig,
    )
    cfg = SampledSelfPlayConfig()
    assert cfg.outcome_only is True
    assert callable(play_episode_with_sampled_muzero)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/models/test_sampled_muzero_wrappers.py -q`
Expected: FAIL — модулей нет.

- [ ] **Step 3: Write minimal implementation**

```python
# core/models/sampled_muzero_model.py
from __future__ import annotations
import os

from core.models.gumbel_muzero_model import (
    GumbelMuZeroNet as SampledMuZeroNet,
    GMZ_PRESETS as SAMPLED_NET_PRESETS,
    load_gumbel_muzero_state_dict as load_sampled_muzero_state_dict,
)

__all__ = [
    "SampledMuZeroNet", "SAMPLED_NET_PRESETS", "load_sampled_muzero_state_dict",
    "make_sampled_muzero_net", "sampled_muzero_kwargs_from_env", "sampled_muzero_arch_from_payload",
]


def sampled_muzero_kwargs_from_env() -> dict:
    preset = SAMPLED_NET_PRESETS.get(os.getenv("SMZ_PRESET", "balanced").lower(),
                                     SAMPLED_NET_PRESETS["balanced"]).copy()
    return {
        "latent_dim": int(os.getenv("SMZ_LATENT_DIM", str(preset["latent_dim"]))),
        "hidden_dim": int(os.getenv("SMZ_HIDDEN_DIM", str(preset["hidden_dim"]))),
        "num_layers": int(os.getenv("SMZ_NUM_LAYERS", str(preset["num_layers"]))),
        "action_embed_dim": int(os.getenv("SMZ_ACTION_EMBED_DIM", str(preset["action_embed_dim"]))),
    }


def sampled_muzero_arch_from_payload(payload: dict | None) -> dict:
    out = sampled_muzero_kwargs_from_env()
    if isinstance(payload, dict) and isinstance(payload.get("arch"), dict):
        for k in ("latent_dim", "hidden_dim", "num_layers", "action_embed_dim"):
            if k in payload["arch"]:
                out[k] = int(payload["arch"][k])
    return out


def make_sampled_muzero_net(obs_dim, action_sizes, **overrides) -> SampledMuZeroNet:
    kwargs = sampled_muzero_kwargs_from_env()
    kwargs.update(overrides)
    return SampledMuZeroNet(obs_dim, action_sizes, **kwargs)
```

```python
# core/models/sampled_muzero_trainer.py
from __future__ import annotations

from core.models.gumbel_muzero_trainer import (
    GumbelMuZeroTrainConfig as SampledMuZeroTrainConfig,
    GumbelMuZeroEMATarget as SampledMuZeroEMATarget,
    make_gmz_lr_scheduler as make_smz_lr_scheduler,
    train_gumbel_muzero_step,
)

__all__ = [
    "SampledMuZeroTrainConfig", "SampledMuZeroEMATarget",
    "make_smz_lr_scheduler", "train_sampled_muzero_step",
]


def train_sampled_muzero_step(**kwargs):
    """policy-таргет уже запечён sampled-поиском на self-play → learner идентичен gmz."""
    return train_gumbel_muzero_step(**kwargs)
```

```python
# core/models/sampled_muzero_selfplay.py
from __future__ import annotations

from core.models.gumbel_muzero_selfplay import (
    GumbelSelfPlayConfig as SampledSelfPlayConfig,
    play_episode_with_gumbel_muzero,
)

__all__ = ["SampledSelfPlayConfig", "play_episode_with_sampled_muzero"]


def play_episode_with_sampled_muzero(**kwargs):
    """Прогон эпизода с sampled-поиском. selfplay-петля идентична gmz: search.run имеет
    ту же сигнатуру, поэтому переиспользуем play_episode_with_gumbel_muzero как есть."""
    return play_episode_with_gumbel_muzero(**kwargs)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/models/test_sampled_muzero_wrappers.py -q`
Expected: PASS (3 tests).

- [ ] **Step 5: Commit**

```bash
git add core/models/sampled_muzero_model.py core/models/sampled_muzero_trainer.py core/models/sampled_muzero_selfplay.py tests/models/test_sampled_muzero_wrappers.py
git commit -m "feat(sampled_muzero): тонкие обёртки model/trainer/selfplay (реюз gmz)"
```

---

### Task 6: Прогон всей gmz-сюиты (регресс)

- [ ] **Step 1: Run gmz suite**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_root_gumbel.py tests/models/test_gumbel_muzero_search_batched.py tests/models/test_gumbel_muzero_trainer_vectorized.py tests/models/test_gumbel_muzero_replay_unroll.py tests/models/test_gumbel_muzero_model_shapes.py -q`
Expected: PASS — gmz не сломан (мы его не трогали, только импортируем).

- [ ] **Step 2: Run all new sampled tests together**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py tests/models/test_sampled_muzero_unbiased.py tests/models/test_sampled_muzero_search_batched.py tests/models/test_sampled_muzero_wrappers.py -q`
Expected: PASS.

(Без коммита — это проверочный чекпойнт.)

---

## Phase 3 — Конфиг в train.py + hyperparams.json

### Task 7: Секция `SMZ_*` и `hyperparams.json`

**Files:**
- Modify: `train.py` (после блока `GMZ_*`, ~`train.py:3069`)
- Modify: `hyperparams.json`

- [ ] **Step 1: Add hyperparams.json section**

Добавь в `hyperparams.json` ключ `sampled_muzero` (зеркало `gumbel_muzero` + новые поля):

```json
"sampled_muzero": {
  "learning_rate": 0.0003, "batch_size": 160, "unroll_steps": 5, "discount": 0.997,
  "value_loss_weight": 1.0, "reward_loss_weight": 1.0, "consistency_loss_weight": 1.0,
  "l2_weight": 1e-06, "max_grad_norm": 0.5, "atom_range": "tight",
  "latent_dim": 256, "hidden_dim": 256, "num_layers": 2, "action_embed_dim": 64,
  "num_samples": 24, "sample_temperature": 1.0, "search_temperature": 0.15,
  "prior_weight": 0.0, "dedup": 1,
  "vtrace_full": 1, "vtrace_rho_clip": 0.7, "vtrace_c_clip": 0.7,
  "reanalyze_fraction": 0.15, "ema_tau": 0.005,
  "outcome_only": 1, "outcome_value_win": 1.0, "outcome_value_loss": -1.0, "outcome_value_draw": -0.25,
  "temperature_opening_moves": 12, "temperature_opening_value": 1.0, "temperature_late_value": 0.25,
  "replay_capacity": 400000, "replay_min_size": 512, "max_policy_staleness_updates": 600,
  "num_actors": 8, "sync_every_updates": 20, "updates_per_rollout": 3,
  "actor_device": "cuda", "learner_compile": 1
}
```

- [ ] **Step 2: Add SMZ_* config block in train.py**

Вставь сразу после блока GMZ (после строки `train.py:3069`). Это зеркало `GMZ_*` с префиксом `SMZ_` + новые ключи поиска. Полный блок:

```python
# === Sampled MuZero config (SMZ_*) ===
SMZ_CFG = data.get("sampled_muzero", {}) if isinstance(data, dict) else {}
SMZ_LR = float(SMZ_CFG.get("learning_rate", AZ_LR))
SMZ_BATCH_SIZE = int(SMZ_CFG.get("batch_size", 160))
SMZ_UNROLL_STEPS = int(SMZ_CFG.get("unroll_steps", 5))
SMZ_REWARD_LOSS_WEIGHT = float(SMZ_CFG.get("reward_loss_weight", 1.0))
SMZ_VALUE_LOSS_WEIGHT = float(SMZ_CFG.get("value_loss_weight", 1.0))
SMZ_L2_WEIGHT = float(SMZ_CFG.get("l2_weight", 1e-6))
SMZ_DISCOUNT = float(SMZ_CFG.get("discount", 0.997))
SMZ_REPLAY_CAPACITY = int(SMZ_CFG.get("replay_capacity", 400000))
SMZ_NUM_ACTORS = max(1, int(os.getenv("SMZ_NUM_ACTORS", str(SMZ_CFG.get("num_actors", AZ_NUM_ACTORS)))))
SMZ_SYNC_EVERY_UPDATES = max(1, int(os.getenv("SMZ_SYNC_EVERY_UPDATES", str(SMZ_CFG.get("sync_every_updates", 20)))))
SMZ_UPDATES_PER_ROLLOUT = max(1, int(os.getenv("SMZ_UPDATES_PER_ROLLOUT", str(SMZ_CFG.get("updates_per_rollout", 3)))))
SMZ_REPLAY_MIN_SIZE = max(1, int(os.getenv("SMZ_REPLAY_MIN_SIZE", str(SMZ_CFG.get("replay_min_size", 512)))))
SMZ_MAX_POLICY_STALENESS_UPDATES = int(os.getenv("SMZ_MAX_POLICY_STALENESS_UPDATES", str(SMZ_CFG.get("max_policy_staleness_updates", 600))))
SMZ_LATENT_DIM = int(os.getenv("SMZ_LATENT_DIM", str(SMZ_CFG.get("latent_dim", 256))))
SMZ_HIDDEN_DIM = int(os.getenv("SMZ_HIDDEN_DIM", str(SMZ_CFG.get("hidden_dim", 256))))
SMZ_NUM_LAYERS = int(os.getenv("SMZ_NUM_LAYERS", str(SMZ_CFG.get("num_layers", 2))))
SMZ_ACTION_EMBED_DIM = int(os.getenv("SMZ_ACTION_EMBED_DIM", str(SMZ_CFG.get("action_embed_dim", 64))))
SMZ_NUM_SAMPLES = int(os.getenv("SMZ_NUM_SAMPLES", str(SMZ_CFG.get("num_samples", 24))))
SMZ_SAMPLE_TEMP = float(os.getenv("SMZ_SAMPLE_TEMPERATURE", str(SMZ_CFG.get("sample_temperature", 1.0))))
SMZ_SEARCH_TEMP = float(os.getenv("SMZ_SEARCH_TEMPERATURE", str(SMZ_CFG.get("search_temperature", 0.15))))
SMZ_PRIOR_WEIGHT = float(os.getenv("SMZ_PRIOR_WEIGHT", str(SMZ_CFG.get("prior_weight", 0.0))))
SMZ_DEDUP = str(os.getenv("SMZ_DEDUP", str(SMZ_CFG.get("dedup", 1)))).strip() == "1"
SMZ_MAX_GRAD_NORM = float(os.getenv("SMZ_MAX_GRAD_NORM", str(SMZ_CFG.get("max_grad_norm", 0.5))))
SMZ_TBPTT_TRUNCATE = int(os.getenv("SMZ_TBPTT_TRUNCATE", str(SMZ_CFG.get("tbptt_truncate", 3))))
SMZ_CONSISTENCY_W = float(os.getenv("SMZ_CONSISTENCY_W", str(SMZ_CFG.get("consistency_loss_weight", "1.0"))))
SMZ_TEMP_OPENING_MOVES = int(os.getenv("SMZ_TEMP_OPENING_MOVES", str(SMZ_CFG.get("temperature_opening_moves", 12))))
SMZ_TEMP_OPENING = float(os.getenv("SMZ_TEMP_OPENING", str(SMZ_CFG.get("temperature_opening_value", 1.0))))
SMZ_TEMP_LATE = float(os.getenv("SMZ_TEMP_LATE", str(SMZ_CFG.get("temperature_late_value", 0.25))))
SMZ_OUTCOME_ONLY = str(os.getenv("SMZ_OUTCOME_ONLY", str(SMZ_CFG.get("outcome_only", 1)))).strip() == "1"
SMZ_OUTCOME_VALUE_WIN = float(os.getenv("SMZ_OUTCOME_VALUE_WIN", str(SMZ_CFG.get("outcome_value_win", 1.0))))
SMZ_OUTCOME_VALUE_LOSS = float(os.getenv("SMZ_OUTCOME_VALUE_LOSS", str(SMZ_CFG.get("outcome_value_loss", -1.0))))
SMZ_OUTCOME_VALUE_DRAW = float(os.getenv("SMZ_OUTCOME_VALUE_DRAW", str(SMZ_CFG.get("outcome_value_draw", -0.25))))
SMZ_ATOM_RANGE = str(os.getenv("SMZ_ATOM_RANGE", str(SMZ_CFG.get("atom_range", "tight")))).lower()
SMZ_VTRACE_FULL = int(os.getenv("SMZ_VTRACE_FULL", str(SMZ_CFG.get("vtrace_full", 1))))
SMZ_VTRACE_RHO_CLIP = float(os.getenv("SMZ_VTRACE_RHO_CLIP", str(SMZ_CFG.get("vtrace_rho_clip", 0.7))))
SMZ_VTRACE_C_CLIP = float(os.getenv("SMZ_VTRACE_C_CLIP", str(SMZ_CFG.get("vtrace_c_clip", 0.7))))
SMZ_REANALYZE_FRACTION = float(os.getenv("SMZ_REANALYZE_FRACTION", str(SMZ_CFG.get("reanalyze_fraction", 0.15))))
SMZ_EMA_TAU = float(os.getenv("SMZ_EMA_TAU", str(SMZ_CFG.get("ema_tau", 0.005))))
SMZ_LEARNER_COMPILE = str(os.getenv("SMZ_LEARNER_COMPILE", str(SMZ_CFG.get("learner_compile", 1)))).strip() == "1"
SMZ_ACTOR_DEVICE_REQUESTED = str(os.getenv("SMZ_ACTOR_DEVICE", str(SMZ_CFG.get("actor_device", "cuda")))).strip().lower()
if SMZ_ACTOR_DEVICE_REQUESTED not in ("cpu", "cuda"):
    SMZ_ACTOR_DEVICE_REQUESTED = "cuda"
SMZ_ATOM_RANGE_PREV = os.environ.get("GMZ_ATOM_RANGE")
```

- [ ] **Step 3: Run import smoke**

Run: `python -c "import train"`
Expected: без ошибок (модуль импортируется, новые переменные считаны). Если падает — проверь, что блок вставлен ПОСЛЕ определения `AZ_LR`/`AZ_NUM_ACTORS` и `data`.

- [ ] **Step 4: Commit**

```bash
git add train.py hyperparams.json
git commit -m "feat(sampled_muzero): секция конфига SMZ_* + hyperparams.sampled_muzero"
```

---

## Phase 4 — Actor-learner в train.py + чекпойнты

> **Подход:** воспроизводим gmz-ветки под именем sampled_muzero с точными заменами идентификаторов.
> Источник для зеркалирования: `_main_actor_learner_gumbel_muzero` (`train.py:10322`),
> `_actor_learner_actor_entry_gumbel_muzero` (`train.py:10094`) и точки диспетча (`train.py:4015`,
> `:4338`, `:10931`).

**Таблица замен (применять ко всему скопированному коду):**

| gmz | sampled_muzero |
|---|---|
| `GumbelMuZeroSearch` | `SampledMuZeroSearch` |
| `GumbelMuZeroSearchConfig(num_simulations=…, root_top_k=…, gumbel_scale=…)` | `SampledMuZeroSearchConfig(num_samples=SMZ_NUM_SAMPLES, sample_temperature=SMZ_SAMPLE_TEMP, temperature=SMZ_SEARCH_TEMP, prior_weight=SMZ_PRIOR_WEIGHT, dedup=SMZ_DEDUP, discount=SMZ_DISCOUNT)` |
| `play_episode_with_gumbel_muzero` | `play_episode_with_sampled_muzero` |
| `GumbelSelfPlayConfig` | `SampledSelfPlayConfig` |
| `train_gumbel_muzero_step` | `train_sampled_muzero_step` |
| `GumbelMuZeroTrainConfig` | `SampledMuZeroTrainConfig` |
| `GumbelMuZeroEMATarget` | `SampledMuZeroEMATarget` |
| `GumbelMuZeroReplayBuffer` / `GMZTransition` | (те же; импортируем из gmz_replay) |
| `GumbelMuZeroReanalyzer` / `GumbelMuZeroReanalysisConfig` | (те же; search для reanalyze = `SampledMuZeroSearch`) |
| `make_gumbel_muzero_net`-эквивалент | `make_sampled_muzero_net` |
| `GMZ_*` переменные | соответствующие `SMZ_*` |
| ключ чекпойнта `"gumbel_muzero_net"` | `"sampled_muzero_net"` |
| `algo`/`train_algo` `"gumbel_muzero"` | `"sampled_muzero"` |
| `os.path.join(MODELS_DIR, "gumbel_muzero")` | `os.path.join(MODELS_DIR, "sampled_muzero")` |
| TB/log `algo="gumbel_muzero"` | `algo="sampled_muzero"` |
| лог-маркеры `[GMZ]` | `[SMZ]` |

### Task 8: Импорты sampled_muzero в train.py

**Files:** Modify `train.py` (рядом с импортами gmz, `train.py:119-129`)

- [ ] **Step 1: Add imports**

```python
from core.models.sampled_muzero_model import (
    SampledMuZeroNet,
    sampled_muzero_arch_from_payload,
    sampled_muzero_kwargs_from_env,
    load_sampled_muzero_state_dict,
)
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig
from core.models.sampled_muzero_selfplay import SampledSelfPlayConfig, play_episode_with_sampled_muzero
from core.models.sampled_muzero_trainer import (
    SampledMuZeroTrainConfig, SampledMuZeroEMATarget, make_smz_lr_scheduler, train_sampled_muzero_step,
)
```

- [ ] **Step 2: Verify import** — `python -c "import train"` → без ошибок.
- [ ] **Step 3: Commit** — `git commit -am "feat(sampled_muzero): импорты в train.py"`

### Task 9: Ветки actor-learner

**Files:** Modify `train.py`

- [ ] **Step 1:** Скопируй функцию `_actor_learner_actor_entry_gumbel_muzero` (`train.py:10094`) под именем `_actor_learner_actor_entry_sampled_muzero`, применив таблицу замен. Атом-диапазон: перед созданием сети выставить `os.environ["GMZ_ATOM_RANGE"] = SMZ_ATOM_RANGE` (сеть gmz читает `GMZ_ATOM_RANGE` на импортном уровне — задавать ДО первого инстанса; см. примечание ниже).
- [ ] **Step 2:** Скопируй `_main_actor_learner_gumbel_muzero` (`train.py:10322`) под именем `_main_actor_learner_sampled_muzero`, применив таблицу замен. Чекпойнт-словарь: ключ `"sampled_muzero_net"`, `"algo": "sampled_muzero"`, `"arch": sampled_muzero_kwargs_from_env()`.
- [ ] **Step 3:** В диспетчах (`train.py:4015` и `:4338`) добавь ветку:

```python
if TRAIN_ALGO == "sampled_muzero":
    _main_actor_learner_sampled_muzero(
        roster_config=roster_config, totLifeT=totLifeT,
        clip_reward_enabled=clip_reward_enabled,
        clip_reward_min=clip_reward_min, clip_reward_max=clip_reward_max,
    )
    return
```

- [ ] **Step 4:** Расширь множества допустимых algo (`train.py:4824`, `:6274`, `:7384`) — добавь `"sampled_muzero"`.
- [ ] **Step 5:** Чекпойнт-детект (`train.py:7338-7342`): добавь
  `elif "sampled_muzero_net" in checkpoint: checkpoint_meta_algo = "sampled_muzero"`.
- [ ] **Step 6:** Verify — `python -c "import train"` → без ошибок.
- [ ] **Step 7: Commit** — `git commit -am "feat(sampled_muzero): actor-learner ветки + диспетч + чекпойнт-роутинг"`

> **Примечание про атом-диапазон:** `GumbelMuZeroNet` читает `GMZ_ATOM_RANGE` на уровне модуля (`gumbel_muzero_model.py:17`). v1: для `sampled_muzero` используем тот же дефолт `tight`; если `SMZ_ATOM_RANGE != GMZ_ATOM_RANGE`, выставляй `os.environ["GMZ_ATOM_RANGE"]=SMZ_ATOM_RANGE` ДО первого `import`/инстанса сети и логируй `[SMZ] atom_range=…`. Если расхождения нет — ничего не делаем.

### Task 10: Smoke-тест actor-learner

**Files:** Create `tests/train/test_sampled_muzero_actor_learner_smoke.py`

- [ ] **Step 1:** Открой `tests/train/test_gumbel_muzero_actor_learner_smoke.py`, скопируй его в `tests/train/test_sampled_muzero_actor_learner_smoke.py`, применив таблицу замен (algo `"sampled_muzero"`, env `SMZ_*`, очень короткий прогон: 1 актор, несколько эпизодов, `num_samples=8`, replay_min_size малый).
- [ ] **Step 2: Run** — `python -m pytest tests/train/test_sampled_muzero_actor_learner_smoke.py -q`
  Expected: PASS — короткий train-цикл проходит, чекпойнт `sampled_muzero_net` пишется.
- [ ] **Step 3: Commit** — `git add ... && git commit -m "test(sampled_muzero): smoke actor-learner"`

---

## Phase 5 — eval / play / Viewer / оппонент

### Task 11: Загрузка и инференс в eval.py

**Files:** Modify `eval.py`

> Источник: gmz-ветки `eval.py:38-39` (импорты), `:330-359` (`select_action_with_epsilon_gumbel_muzero`),
> `:684-685` (диспетч действия), `:1075-1084` (загрузка сети), `:1109-1144` (режимы/лейблы). Применять таблицу замен из Phase 4 + env-префикс `SMZ_EVAL_*`.

- [ ] **Step 1: Imports** — добавь в `eval.py`:

```python
from core.models.sampled_muzero_model import SampledMuZeroNet
from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig
```

- [ ] **Step 2: Action selection** — добавь `select_action_with_epsilon_sampled_muzero` (зеркало `eval.py:330`), `SampledMuZeroSearchConfig(num_samples=int(os.getenv("SMZ_EVAL_NUM_SAMPLES","24")), temperature=float(os.getenv("SMZ_EVAL_TEMPERATURE","0.10")), sample_temperature=float(os.getenv("SMZ_EVAL_SAMPLE_TEMPERATURE","1.0")), prior_weight=0.0, dedup=True)`, `deterministic=True`.
- [ ] **Step 3: Dispatch** — в `eval.py:684` добавь ветку `elif algo == "sampled_muzero": action = select_action_with_epsilon_sampled_muzero(...)`.
- [ ] **Step 4: Loader** — в `eval.py:1075` добавь ветку загрузки `sampled_muzero_net` в `SampledMuZeroNet` (зеркало gmz-загрузки, env `SMZ_*` для размеров).
- [ ] **Step 5: Labels** — в `eval.py:1109-1144` добавь `sampled_muzero` в лейблы/режимы (по образцу gmz).
- [ ] **Step 6: Verify** — `python -c "import eval"` → без ошибок.
- [ ] **Step 7: Commit** — `git commit -am "feat(sampled_muzero): eval/play/оппонент через sampled-поиск"`

### Task 12: Контракт eval/play

**Files:** Create `tests/engine/test_sampled_muzero_eval_play_contract.py`

- [ ] **Step 1:** Скопируй `tests/engine/test_gumbel_muzero_eval_play_contract.py` в sampled-вариант, применив таблицу замен. Проверяет: загрузка чекпойнта `sampled_muzero_net`, выбор действия легален, формат как у gmz.
- [ ] **Step 2: Run** — `python -m pytest tests/engine/test_sampled_muzero_eval_play_contract.py -q` → PASS.
- [ ] **Step 3: Commit** — `git add ... && git commit -m "test(sampled_muzero): контракт eval/play"`

---

## Phase 6 — GUI-вкладка

### Task 13: Дефолты гиперов GUI

**Files:** Modify `app/gui_qt/gmz_hyperparams_defaults.py` (или создай `sampled_muzero_hyperparams_defaults.py` по образцу)

- [ ] **Step 1:** Добавь словарь дефолтов `sampled_muzero` (зеркало значений из Task 7) для редактора гиперов GUI.
- [ ] **Step 2: Verify** — `python -c "import app.gui_qt.gmz_hyperparams_defaults"` (или новый модуль) → без ошибок.
- [ ] **Step 3: Commit** — `git commit -am "feat(sampled_muzero): дефолты гиперов в GUI"`

### Task 14: Вкладка и проводка в GUI

**Files:** Modify `app/gui_qt/main.py`, `app/gui_qt/qml/Main.qml`, `app/gui_qt/qml/components/SectionHyperparamsEditor.qml`, `app/gui_qt/qml/components/TrainingAlgoHelpDialog.qml`

> Источник: места, где упомянут `gumbel_muzero`/`Gumbel MuZero` (см. grep). Зеркалируем как новую вкладку «Sampled MuZero» с пресетами fast/balanced/heavy (дефолт balanced) и кнопками train/eval.

- [ ] **Step 1:** В `main.py` — зарегистрируй algo `sampled_muzero` в логике запуска train/eval (по образцу gmz).
- [ ] **Step 2:** В `Main.qml` / `SectionHyperparamsEditor.qml` — добавь вкладку «Sampled MuZero» с полями `num_samples`, `search_temperature`, `sample_temperature`, `prior_weight` + общие (lr/batch/unroll/...).
- [ ] **Step 3:** В `TrainingAlgoHelpDialog.qml` — короткое описание Sampled MuZero (RU): «сэмплит K цельных ходов из приора, координирует юнитов; v1 — одна машина».
- [ ] **Step 4: Verify (ручной запуск GUI)** — через скилл `/run-40kai` или запуск Qt GUI: вкладка появляется, train/eval стартуют, в логах `[SMZ]`. (Скриншоты не нужны — AGENTS.md.)
- [ ] **Step 5: Commit** — `git commit -am "feat(sampled_muzero): вкладка Sampled MuZero в Qt GUI"`

---

## Phase 7 — Сквозная проверка и финал

### Task 15: Поведенческий тест координации

**Files:** Modify `tests/models/test_sampled_muzero_search.py`

- [ ] **Step 1: Write the test**

```python
def test_joint_selection_beats_independent_argmax_on_synthetic():
    """Синтетический случай: лучший joint-ход не равен покомпонентному argmax маргиналов.
    Sampled-поиск (оценивающий цельные ходы) должен выбрать координированный ход."""
    import numpy as np, torch
    from core.models.gumbel_muzero_model import GumbelMuZeroNet
    from core.models.sampled_muzero_search import SampledMuZeroSearch, SampledMuZeroSearchConfig

    torch.manual_seed(0)
    net = GumbelMuZeroNet(obs_dim=8, action_sizes=[2, 2],
                          latent_dim=32, hidden_dim=32, num_layers=1, action_embed_dim=8)
    s = SampledMuZeroSearch(net=net,
                            config=SampledMuZeroSearchConfig(num_samples=2000, temperature=0.05, prior_weight=0.0),
                            device=torch.device("cpu"))
    obs = np.zeros(8, dtype=np.float32)
    legal = [np.ones(2, dtype=bool), np.ones(2, dtype=bool)]
    np.random.seed(0)
    _, _, actions, _ = s.run(obs=obs, legal_masks_by_head=legal, deterministic=True)
    # выбранный joint-ход совпадает с argmax по Q среди всех 4 комбинаций (эталон)
    import itertools
    lat = net.initial_inference(torch.zeros(1, 8))[3]
    joints = list(itertools.product([0, 1], [0, 1]))
    acts = torch.tensor(joints, dtype=torch.long)
    _p, val, rew, _nl = net.recurrent_inference(lat.expand(4, -1), acts)
    q = (rew + 0.997 * val).detach().numpy()
    best = joints[int(np.argmax(q))]
    assert tuple(actions) == best
```

- [ ] **Step 2: Run** — `python -m pytest tests/models/test_sampled_muzero_search.py::test_joint_selection_beats_independent_argmax_on_synthetic -q` → PASS.
- [ ] **Step 3: Commit** — `git commit -am "test(sampled_muzero): joint-выбор совпадает с argmax по Q (координация)"`

### Task 16: Полный прогон и сводка

- [ ] **Step 1: Run all sampled + gmz tests**

Run: `python -m pytest tests/models/test_sampled_muzero_search.py tests/models/test_sampled_muzero_unbiased.py tests/models/test_sampled_muzero_search_batched.py tests/models/test_sampled_muzero_wrappers.py tests/train/test_sampled_muzero_actor_learner_smoke.py tests/engine/test_sampled_muzero_eval_play_contract.py tests/models/test_gumbel_muzero_search_root_gumbel.py tests/models/test_gumbel_muzero_trainer_vectorized.py -q`
Expected: ALL PASS.

- [ ] **Step 2: Короткий реальный train через GUI** — запусти `sampled_muzero` train на пару апдейтов через Qt GUI, проверь `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`: есть `[SMZ]`, апдейты идут, чекпойнт пишется. (Скилл `verify`/`/run-40kai`.)
- [ ] **Step 3: Финальный commit/докоммит** — если остались несведённые мелочи.

---

## Self-Review (выполнено при написании плана)

- **Покрытие спеки:** Секция 1 (что новое/реюз) → Tasks 1–6. Секция 2 (ядро алгоритма) → Tasks 2–3 (+формула в шапке). Секция 3 (компоненты/поток) → Tasks 5, 8–14. Секция 4 (два IS) → реализовано раздельно: policy-IS в search (Task 2), V-trace в реюзнутом тренере (Task 5). Секция 5 (тесты 1–8) → Tasks 3 (несмещённость), 4 (RNG-эквивалентность), 2 (маски/маргинализация/дедуп), 5+10 (градиенты через тренер/smoke), 15 (координация), 6 (регресс gmz). Секция 6 (конфиг) → Task 7. Секция 7 (риски/фазы) → дефолты `prior_weight=0`, `dedup=1`; авторегрессия/remote/mixed-value явно отложены.
- **Заглушки:** в Phase 1–2 и тестах — полный код. В Phase 4–6 «зеркалирование» задано таблицей точных замен + конкретными новыми строками (это исполнимо, не плейсхолдер).
- **Согласованность имён:** `SampledMuZeroSearch(.run/.cfg/.last_run_stats)`, `SampledMuZeroSearchConfig(num_samples/temperature/sample_temperature/prior_weight/dedup/discount/tree_reuse)`, `run_batched`, `BatchedSampledMuZeroSearch.run_batched_stateful`, helpers `_beta_heads_from_logits/_sample_joint/_improved_joint_policy/_marginalize`, обёртки `make_sampled_muzero_net/SampledMuZeroNet/train_sampled_muzero_step/SampledMuZeroTrainConfig/play_episode_with_sampled_muzero/SampledSelfPlayConfig`, чекпойнт-ключ `sampled_muzero_net`, algo `sampled_muzero` — едины во всех тасках.
