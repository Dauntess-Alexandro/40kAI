# Batched-Search Inference for Gumbel MuZero Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заставить inference-сервер выполнять MCTS-поиск **батчем по средам** (один forward на `N` сред вместо `N` отдельных forward'ов), чтобы поднять загрузку GPU с ~40% до 80%+ и throughput в 3–8× без нового железа.

**Architecture:** Сейчас `GMZInferenceServer.build_batch_responses` собирает батч запросов от воркеров, но обрабатывает их **последовательно** — вызывает `GumbelMuZeroSearch.run` по одной среде. Сеть крошечная (256-dim, 2 слоя), поэтому каждый forward launch-bound, а GPU простаивает между запусками. Мы добавляем функцию `run_batched`, которая делает `initial_inference` батчем `[N, obs]`, а каждую симуляцию каждого head'а — `recurrent_inference` батчем `[N×sims, latent]`, схлопывая `N×num_heads` GPU-вызовов в `num_heads`. Поиск факторизован по head'ам (не настоящее дерево), candidate-выборка по Gumbel остаётся на CPU/numpy (дёшево). Сервер заменяет последовательный цикл на один вызов `run_batched`.

**Tech Stack:** Python 3, PyTorch (cu128, Windows — без Triton), NumPy, ZMQ/`multiprocessing.Queue`, pytest. Сеть: `core/models/gumbel_muzero_model.py::GumbelMuZeroNet`. Поиск: `core/models/gumbel_muzero_search.py`. Сервер: `core/models/gmz_inference_server.py`.

**Ключевой инвариант корректности:** при `deterministic=True` и одинаковом seed numpy `run_batched` обязан давать **по-средно идентичный** результат последовательным `GumbelMuZeroSearch.run` (политики совпадают с точностью `1e-5`, выбранные действия — точно). Это наш оракул в TDD. Для этого candidate-выборка по Gumbel в `run_batched` должна тянуть случайные числа в том же порядке, что и последовательный путь: **env-major, head-minor**, пропуская head'ы без легальных действий (как делает `run` через `continue`).

---

## File Structure

| Файл | Ответственность | Действие |
|---|---|---|
| `core/models/gumbel_muzero_search.py` | Алгоритм поиска. Добавляем `run_batched(...)` (stateless) и класс `BatchedGumbelMuZeroSearch` (tree-reuse по `env_id`). | Modify |
| `core/models/gmz_inference_server.py` | IS-движок. `build_batch_responses` зовёт батч-поиск вместо цикла. | Modify |
| `tests/models/test_gumbel_muzero_search_batched.py` | Тесты эквивалентности batched↔sequential, форма, stochastic. | Create |
| `tests/engine/test_gmz_inference_ipc.py` | Существующий IPC-тест сервера — прогнать на регресс. | Verify only |
| `app/gui_qt/gmz_hyperparams_defaults.py` | Пресеты `heavy`/`very_heavy`: `inference_batch_size`/`num_env_workers`/`batch_interval`. | Modify (Task 5) |

---

### Task 1: Эквивалентность-оракул — тест-харнес (RED)

Сначала пишем тест, который вызывает несуществующий `run_batched` и сравнивает его с последовательным `run`. Тест должен **падать** (функции нет). Это фиксирует контракт до реализации.

**Files:**
- Create: `tests/models/test_gumbel_muzero_search_batched.py`

- [ ] **Step 1: Написать падающий тест эквивалентности**

```python
# tests/models/test_gumbel_muzero_search_batched.py
import numpy as np
import torch

from core.models.gumbel_muzero_model import GumbelMuZeroNet
from core.models.gumbel_muzero_search import (
    GumbelMuZeroSearch,
    GumbelMuZeroSearchConfig,
    run_batched,
)


def _make_net(n_obs, n_actions):
    torch.manual_seed(0)
    return GumbelMuZeroNet(
        obs_dim=n_obs, action_sizes=n_actions,
        latent_dim=64, hidden_dim=64, num_layers=1, action_embed_dim=16,
    )


def _make_requests(n_obs, n_actions, n_envs, seed=7):
    rng = np.random.default_rng(seed)
    reqs = []
    for env_id in range(n_envs):
        obs = rng.standard_normal(n_obs).astype(np.float32)
        masks = []
        for size in n_actions:
            m = rng.integers(0, 2, size=size).astype(bool)
            if not m.any():
                m[0] = True  # хотя бы одно легальное действие
            masks.append(m)
        reqs.append({"env_id": env_id, "obs": obs, "legal_masks_by_head": masks})
    return reqs


def _cfg():
    return GumbelMuZeroSearchConfig(
        num_simulations=16, root_top_k=3, temperature=0.2,
        gumbel_scale=1.0, prior_weight=0.25, batch_recurrent=True, tree_reuse=False,
    )


def test_run_batched_matches_sequential_deterministic():
    n_obs, n_actions, n_envs = 12, [4, 3, 5], 6
    net = _make_net(n_obs, n_actions)
    cfg = _cfg()
    device = torch.device("cpu")
    reqs = _make_requests(n_obs, n_actions, n_envs)

    # Sequential oracle: свежий search на каждую среду, tree_reuse=False.
    np.random.seed(123)
    seq = []
    for r in reqs:
        s = GumbelMuZeroSearch(net=net, config=cfg, device=device)
        pi, beh, act, val = s.run(
            obs=r["obs"], legal_masks_by_head=r["legal_masks_by_head"], deterministic=True
        )
        seq.append((pi, beh, act, val))

    # Batched: тот же seed, тот же порядок розыгрыша Gumbel (env-major, head-minor).
    np.random.seed(123)
    bat = run_batched(net=net, cfg=cfg, device=device, requests=reqs, deterministic=True)

    assert len(bat) == n_envs
    for n, (pi, beh, act, val) in enumerate(seq):
        b = bat[n]
        assert b["env_id"] == reqs[n]["env_id"]
        assert b["selected_actions"] == list(act), f"env {n} actions mismatch"
        assert abs(b["value_est"] - val) < 1e-4, f"env {n} value mismatch"
        for h in range(len(n_actions)):
            np.testing.assert_allclose(b["policy_targets"][h], pi[h], atol=1e-5,
                                       err_msg=f"env {n} head {h} policy mismatch")
            np.testing.assert_allclose(b["behavior_logits"][h], beh[h], atol=1e-5,
                                       err_msg=f"env {n} head {h} behavior mismatch")
```

- [ ] **Step 2: Запустить тест — убедиться, что падает на импорте**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py -q`
Expected: FAIL — `ImportError: cannot import name 'run_batched'`.

- [ ] **Step 3: Commit (red-фиксация контракта)**

```bash
git add tests/models/test_gumbel_muzero_search_batched.py
git commit -m "test: add batched-search equivalence oracle (red)"
```

---

### Task 2: Реализовать `run_batched` (GREEN)

Stateless батч-поиск. Без tree-reuse (это Task 3). Логика числа в числе повторяет `GumbelMuZeroSearch.run`, но recurrent-инференс батчится по средам внутри каждого head'а.

**Files:**
- Modify: `core/models/gumbel_muzero_search.py` (добавить функцию в конец файла, после класса)

- [ ] **Step 1: Добавить `run_batched` в `gumbel_muzero_search.py`**

```python
@torch.no_grad()
def run_batched(
    *,
    net,
    cfg: GumbelMuZeroSearchConfig,
    device: torch.device,
    requests: list[dict],
    deterministic: bool = False,
    warm_start: dict[int, dict] | None = None,
) -> list[dict]:
    """Батч-вариант GumbelMuZeroSearch.run по средам.

    requests: список dict с ключами env_id, obs (np.ndarray), legal_masks_by_head (list[np.ndarray]).
    Возвращает список dict (в порядке requests): env_id, selected_actions, policy_targets,
    behavior_logits, value_est, _visits_by_head, _q_sums_by_head (последние два — для tree-reuse).

    warm_start: optional {env_id: {"visits": {h: arr}, "q_sums": {h: arr},
    "legal_masks": [arr]}} — пред-заполнение visits/q_sums (см. BatchedGumbelMuZeroSearch).
    """
    N = len(requests)
    if N == 0:
        return []

    sims = max(1, int(cfg.num_simulations))
    root_top_k = max(1, int(cfg.root_top_k))
    discount = float(cfg.discount)
    temp = float(cfg.temperature)
    gumbel_scale = float(cfg.gumbel_scale)
    prior_weight = float(cfg.prior_weight)

    num_heads = len(requests[0]["legal_masks_by_head"])

    # --- Батч-инференс корня ---
    obs_batch = torch.tensor(
        np.stack([np.asarray(r["obs"], dtype=np.float32) for r in requests], axis=0),
        device=device,
    )
    masks_batch = []
    for h in range(num_heads):
        mh = np.stack(
            [np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool) for n in range(N)],
            axis=0,
        )
        masks_batch.append(torch.as_tensor(mh, dtype=torch.bool, device=device))

    root_logits, root_value, _root_reward, latent = net.initial_inference(
        obs_batch, masks_by_head=masks_batch
    )
    root_logits_np = [
        root_logits[h].detach().cpu().numpy().astype(np.float32) for h in range(num_heads)
    ]
    root_value_np = root_value.detach().cpu().numpy().reshape(-1).astype(np.float32)
    base_action = np.stack([rl.argmax(axis=1) for rl in root_logits_np], axis=1)  # [N, num_heads]

    # --- Candidate-выборка (RNG-порядок: env-major, head-minor — как sequential) ---
    candidates = [[None] * num_heads for _ in range(N)]
    legal_np = [[None] * num_heads for _ in range(N)]
    behavior_logits = [[None] * num_heads for _ in range(N)]
    for n in range(N):
        for h in range(num_heads):
            logits_np = root_logits_np[h][n]
            legal = np.asarray(requests[n]["legal_masks_by_head"][h], dtype=bool)
            legal_np[n][h] = legal
            behavior_logits[n][h] = logits_np.copy()
            legal_idx = np.where(legal)[0]
            if legal_idx.size == 0:
                candidates[n][h] = np.empty(0, dtype=np.int64)
                continue
            local_logits = logits_np[legal_idx]
            gumbel = np.random.gumbel(
                loc=0.0, scale=max(1e-6, gumbel_scale), size=legal_idx.size
            ).astype(np.float32)
            ranking = np.argsort(local_logits + gumbel)[::-1]
            top_local = ranking[: min(root_top_k, ranking.size)]
            candidates[n][h] = legal_idx[top_local].astype(np.int64)

    # --- Аккумуляторы visits/q_sums (+ warm-start) ---
    visits = [
        [np.zeros(root_logits_np[h].shape[1], dtype=np.float32) for h in range(num_heads)]
        for _ in range(N)
    ]
    q_sums = [
        [np.zeros(root_logits_np[h].shape[1], dtype=np.float32) for h in range(num_heads)]
        for _ in range(N)
    ]
    value_samples: list[list[float]] = [[] for _ in range(N)]

    if warm_start:
        for n in range(N):
            env_id = int(requests[n].get("env_id", n))
            ws = warm_start.get(env_id)
            if not ws:
                continue
            prev_masks = ws.get("legal_masks")
            if prev_masks is None or len(prev_masks) != num_heads:
                continue
            if any(prev_masks[h].shape != legal_np[n][h].shape for h in range(num_heads)):
                continue
            for h in range(num_heads):
                pv = ws["visits"].get(h)
                pq = ws["q_sums"].get(h)
                if pv is None or pq is None:
                    continue
                clen = min(len(visits[n][h]), len(pv))
                if clen > 0:
                    visits[n][h][:clen] = pv[:clen]
                    q_sums[n][h][:clen] = pq[:clen]

    # --- Батч-recurrent по head'ам: один forward на N×sims строк ---
    for h in range(num_heads):
        active = [n for n in range(N) if candidates[n][h].size > 0]
        if not active:
            continue
        rows_action: list[np.ndarray] = []
        env_of_row: list[int] = []
        cand_of_row: list[int] = []
        for n in active:
            cand = candidates[n][h]
            for s in range(sims):
                c = int(cand[s % cand.size])
                av = base_action[n].copy()
                av[h] = c
                rows_action.append(av)
                env_of_row.append(n)
                cand_of_row.append(c)
        idx_t = torch.tensor(env_of_row, dtype=torch.long, device=device)
        latent_rep = latent.index_select(0, idx_t)
        action_t = torch.tensor(np.asarray(rows_action), dtype=torch.long, device=device)
        masks_rep = [masks_batch[h2].index_select(0, idx_t) for h2 in range(num_heads)]
        _p, val_b, rew_b, _nl = net.recurrent_inference(
            latent_rep, action_t, masks_by_head=masks_rep
        )
        val_b = val_b.detach().cpu().numpy().reshape(-1).astype(np.float32)
        rew_b = rew_b.detach().cpu().numpy().reshape(-1).astype(np.float32)
        for row in range(len(env_of_row)):
            n = env_of_row[row]
            c = cand_of_row[row]
            q = float(rew_b[row]) + discount * float(val_b[row])
            visits[n][h][c] += 1.0
            q_sums[n][h][c] += q
            value_samples[n].append(q)

    # --- Пост-обработка (numpy, как sequential): UCB → softmax → prior-mix → select ---
    results: list[dict] = []
    for n in range(N):
        policy_targets: list[np.ndarray] = []
        selected: list[int] = []
        v_by_head: dict[int, np.ndarray] = {}
        q_by_head: dict[int, np.ndarray] = {}
        for h in range(num_heads):
            logits_np = root_logits_np[h][n]
            legal = legal_np[n][h]
            legal_idx = np.where(legal)[0]
            v_by_head[h] = visits[n][h].copy()
            q_by_head[h] = q_sums[n][h].copy()
            if legal_idx.size == 0:
                policy_targets.append(
                    np.ones_like(logits_np, dtype=np.float32) / float(max(1, logits_np.size))
                )
                selected.append(0)
                continue
            prior_np = np.full_like(logits_np, -1e9)
            prior_np[legal_idx] = logits_np[legal_idx]
            prior_np -= prior_np[legal_idx].max()
            prior_exp = np.exp(prior_np)
            prior_exp[~legal] = 0.0
            prior_probs = prior_exp / max(prior_exp.sum(), 1e-12)

            vv = visits[n][h]
            qq = q_sums[n][h]
            q_values = np.where(vv > 0, qq / np.maximum(vv, 1.0), logits_np)
            q_values[~legal] = -1e9
            total_visits = vv.sum() + 1.0
            ucb_bonus = np.sqrt(np.log(total_visits + 1.0) / (vv + 1.0))
            ucb_q = np.where(legal, q_values + 0.3 * ucb_bonus, -1e9)
            q_soft = _masked_softmax(ucb_q, legal_mask=legal, temperature=temp)
            mixed = (1.0 - prior_weight) * q_soft + prior_weight * prior_probs
            mixed[~legal] = 0.0
            ms = mixed.sum()
            mixed = mixed / ms if ms > 1e-12 else legal.astype(np.float32) / float(legal.sum())
            action = (
                int(np.argmax(mixed))
                if deterministic
                else int(np.random.choice(np.arange(mixed.size), p=mixed))
            )
            policy_targets.append(mixed.astype(np.float32))
            selected.append(action)
        value_out = float(np.mean(value_samples[n]) if value_samples[n] else root_value_np[n])
        results.append(
            {
                "env_id": int(requests[n].get("env_id", n)),
                "selected_actions": selected,
                "policy_targets": policy_targets,
                "behavior_logits": behavior_logits[n],
                "value_est": value_out,
                "_visits_by_head": v_by_head,
                "_q_sums_by_head": q_by_head,
                "_legal_masks": [m.copy() for m in legal_np[n]],
            }
        )
    return results
```

- [ ] **Step 2: Запустить тест эквивалентности — должен пройти**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py::test_run_batched_matches_sequential_deterministic -q`
Expected: PASS.

Если падает на `selected_actions`/`policy` — проверь порядок розыгрыша Gumbel: он обязан быть env-major, head-minor, и head'ы без легальных действий **не** должны тянуть RNG.

- [ ] **Step 3: Добавить тест формы для stochastic-режима**

```python
def test_run_batched_stochastic_shapes_and_legality():
    n_obs, n_actions, n_envs = 10, [4, 3], 5
    net = _make_net(n_obs, n_actions)
    cfg = _cfg()
    reqs = _make_requests(n_obs, n_actions, n_envs, seed=42)
    np.random.seed(1)
    out = run_batched(net=net, cfg=cfg, device=torch.device("cpu"),
                      requests=reqs, deterministic=False)
    assert len(out) == n_envs
    for n, r in enumerate(out):
        assert len(r["policy_targets"]) == len(n_actions)
        for h, size in enumerate(n_actions):
            p = r["policy_targets"][h]
            assert p.shape[0] == size
            assert abs(float(p.sum()) - 1.0) < 1e-5
            # выбранное действие легально
            assert reqs[n]["legal_masks_by_head"][h][r["selected_actions"][h]]
```

- [ ] **Step 4: Запустить весь файл тестов**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py -q`
Expected: PASS (2 passed).

- [ ] **Step 5: Commit**

```bash
git add core/models/gumbel_muzero_search.py tests/models/test_gumbel_muzero_search_batched.py
git commit -m "feat: batched per-env Gumbel MuZero search (run_batched)"
```

---

### Task 3: `BatchedGumbelMuZeroSearch` — tree-reuse по `env_id` (опционально, gated)

`run_batched` уже отдаёт `_visits_by_head`/`_q_sums_by_head`/`_legal_masks`. Класс хранит их по `env_id` между ходами и передаёт обратно как `warm_start`. Это переносит warm-start из per-instance `GumbelMuZeroSearch` в батч-мир.

**Решение по запуску:** сначала отгрузить Task 2+4 с tree-reuse **выключенным** в батч-пути, замерить выигрыш (Task 5). Включать Task 3 только если throughput-выигрыш подтверждён — tree-reuse это оптимизация качества, а не throughput, и она усложняет жизнь.

**Files:**
- Modify: `core/models/gumbel_muzero_search.py` (добавить класс после `run_batched`)
- Modify: `tests/models/test_gumbel_muzero_search_batched.py`

- [ ] **Step 1: Написать тест tree-reuse (RED)**

```python
def test_batched_search_warm_start_accumulates_visits():
    from core.models.gumbel_muzero_search import BatchedGumbelMuZeroSearch
    n_obs, n_actions = 10, [4, 3]
    net = _make_net(n_obs, n_actions)
    cfg = GumbelMuZeroSearchConfig(num_simulations=8, root_top_k=2,
                                   prior_weight=0.25, tree_reuse=True)
    searcher = BatchedGumbelMuZeroSearch(net=net, config=cfg, device=torch.device("cpu"))
    reqs = _make_requests(n_obs, n_actions, n_envs=2, seed=5)
    for r in reqs:
        r["is_new_episode"] = False

    np.random.seed(3)
    first = searcher.run_batched_stateful(reqs)
    np.random.seed(3)
    second = searcher.run_batched_stateful(reqs)

    # Второй вызов с warm-start: суммарные визиты по env строго больше, чем у первого.
    assert searcher._tree_state[0]["visits"][0].sum() > first[0]["_visits_by_head"][0].sum() - 1e-6
    # Форма результата стабильна
    assert len(second) == 2
    assert len(second[0]["policy_targets"]) == len(n_actions)
```

- [ ] **Step 2: Запустить — падает (нет класса)**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py::test_batched_search_warm_start_accumulates_visits -q`
Expected: FAIL — `ImportError`/`AttributeError`.

- [ ] **Step 3: Реализовать класс**

```python
class BatchedGumbelMuZeroSearch:
    """Батч-поиск с tree-reuse по env_id. Обёртка над run_batched."""

    def __init__(self, *, net, config: GumbelMuZeroSearchConfig, device: torch.device):
        self.net = net
        self.cfg = config
        self.device = device
        self._tree_reuse = bool(getattr(config, "tree_reuse", True))
        self._tree_state: dict[int, dict] = {}

    def clear_tree_state(self, env_id: int | None = None) -> None:
        if env_id is None:
            self._tree_state.clear()
        else:
            self._tree_state.pop(int(env_id), None)

    def run_batched_stateful(self, requests: list[dict], deterministic: bool = False) -> list[dict]:
        # is_new_episode сбрасывает дерево конкретной среды
        for r in requests:
            if bool(r.get("is_new_episode", False)):
                self.clear_tree_state(int(r.get("env_id", 0)))

        warm = None
        if self._tree_reuse and self._tree_state:
            warm = {
                eid: {"visits": st["visits"], "q_sums": st["q_sums"],
                      "legal_masks": st["legal_masks"]}
                for eid, st in self._tree_state.items()
            }

        results = run_batched(
            net=self.net, cfg=self.cfg, device=self.device,
            requests=requests, deterministic=deterministic, warm_start=warm,
        )

        if self._tree_reuse:
            for r in results:
                eid = int(r["env_id"])
                self._tree_state[eid] = {
                    "visits": {h: v.copy() for h, v in r["_visits_by_head"].items()},
                    "q_sums": {h: v.copy() for h, v in r["_q_sums_by_head"].items()},
                    "legal_masks": [m.copy() for m in r["_legal_masks"]],
                }
        return results
```

- [ ] **Step 4: Запустить тест — должен пройти**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py::test_batched_search_warm_start_accumulates_visits -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add core/models/gumbel_muzero_search.py tests/models/test_gumbel_muzero_search_batched.py
git commit -m "feat: BatchedGumbelMuZeroSearch with per-env tree reuse"
```

---

### Task 4: Подключить батч-поиск к серверу

Заменить последовательный цикл `for env_id … search.run` в `build_batch_responses` на один вызов батч-поиска. Сервер уже получает до `inference_batch_size` запросов разом — именно их и батчим. Дублируем ответы для нескольких запросов одной среды (как раньше — по env_id).

**Files:**
- Modify: `core/models/gmz_inference_server.py:241-249` (заменить `_get_or_create_tree`/`_tree_states` на `BatchedGumbelMuZeroSearch`)
- Modify: `core/models/gmz_inference_server.py:177-227` (`build_batch_responses`)
- Verify: `tests/engine/test_gmz_inference_ipc.py`

- [ ] **Step 1: Заменить хранилище деревьев в `__init__`**

В `GMZInferenceServer.__init__`, после строки `self._tree_states: dict[int, GumbelMuZeroSearch] = {}` — заменить на:

```python
        from core.models.gumbel_muzero_search import BatchedGumbelMuZeroSearch

        self._batched_search = BatchedGumbelMuZeroSearch(
            net=self.net, config=self.search_cfg, device=self.device,
        )
        self._tree_states: dict[int, GumbelMuZeroSearch] = {}  # legacy, не используется в батч-пути
```

В `_poll_weights` (строки ~118-123) заменить обновление per-tree net на батч-сёрчер:

```python
                                self._batched_search.net = self.net
                                if self._clear_tree_on_weight_sync:
                                    self._batched_search.clear_tree_state()
```

(блок `for search in self._tree_states.values(): search.net = self.net` удалить.)

- [ ] **Step 2: Переписать `build_batch_responses`**

Заменить тело метода (строки 177-227) на:

```python
    def build_batch_responses(self, batch: list[dict[str, Any]]) -> list[dict[str, Any]]:
        t0 = time.perf_counter()
        if not batch:
            return []

        # Один запрос на среду в этом батче (последний выигрывает, как было).
        by_env: dict[int, dict[str, Any]] = {}
        for req in batch:
            by_env[int(req.get("env_id", 0))] = req

        requests = []
        for env_id, req in by_env.items():
            requests.append(
                {
                    "env_id": int(env_id),
                    "obs": np.asarray(req.get("obs"), dtype=np.float32),
                    "legal_masks_by_head": [
                        np.asarray(m) for m in (req.get("legal_masks_by_head") or [])
                    ],
                    "is_new_episode": bool(req.get("is_new_episode", False)),
                }
            )

        with torch.no_grad():
            if self._inference_stream is not None:
                with torch.cuda.stream(self._inference_stream):
                    batched = self._batched_search.run_batched_stateful(
                        requests, deterministic=False
                    )
            else:
                batched = self._batched_search.run_batched_stateful(
                    requests, deterministic=False
                )

        out_by_env: dict[int, dict[str, Any]] = {}
        for r in batched:
            out_by_env[int(r["env_id"])] = {
                "kind": "infer_response",
                "env_id": int(r["env_id"]),
                "selected_actions": list(r["selected_actions"]),
                "policy_targets": [np.asarray(p, dtype=np.float32) for p in r["policy_targets"]],
                "behavior_logits": [np.asarray(b, dtype=np.float32) for b in r["behavior_logits"]],
                "value_est": float(r["value_est"]),
                "policy_version": int(self._weight_version),
            }

        # По одному ответу на каждый исходный запрос (несколько запросов одной среды → копии).
        responses: list[dict[str, Any]] = []
        for req in batch:
            env_id = int(req.get("env_id", 0))
            resp = out_by_env.get(env_id)
            if resp is not None:
                responses.append(dict(resp))
                self._requests_total += 1

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        self._batches_total += 1
        self._last_batch_ms = float(elapsed_ms)
        return responses
```

Метод `_get_or_create_tree` (строки 241-249) становится мёртвым кодом — удалить его.

- [ ] **Step 3: Прогнать существующий IPC-тест сервера**

Run: `python -m pytest tests/engine/test_gmz_inference_ipc.py -q`
Expected: PASS. Тест гоняет реальный спавн сервера и round-trip запрос/ответ — это проверяет, что новый путь не сломал контракт `infer_response`.

- [ ] **Step 4: Прогнать весь GMZ-набор тестов на регресс**

Run: `python -m pytest tests/models/test_gumbel_muzero_search_batched.py tests/models/test_gumbel_muzero_search_root_gumbel.py tests/engine/test_gmz_inference_ipc.py tests/engine/test_gmz_remote_server.py -q`
Expected: PASS (все).

- [ ] **Step 5: Commit**

```bash
git add core/models/gmz_inference_server.py
git commit -m "feat: inference server uses batched per-env search"
```

---

### Task 5: Конфиг для наполнения батча + бенчмарк (gate на железо)

Батч-поиск выигрывает только если в `request_q` реально лежат `N` запросов одновременно. Это обеспечивают `num_env_workers` отдельных процессов, каждый блокирующийся на своём ходу. Условие наполнения: `num_env_workers ≥ inference_batch_size`, окно сбора достаточно велико, чтобы воркеры успели прислать (но не настолько, чтобы добавлять латентность). На текущем железе **код воркера менять не нужно** — это чисто конфиг + замер.

**Files:**
- Modify: `app/gui_qt/gmz_hyperparams_defaults.py` (пресеты `heavy`, `very_heavy`)

- [ ] **Step 1: Выставить `inference_batch_size ≈ num_env_workers` в `heavy`/`very_heavy`**

В `GMZ_PROFILE_PRESETS["heavy"]` и `["very_heavy"]` `num_env_workers=10` уже стоит. Поднять `inference_batch_size` до числа воркеров и уменьшить окно сбора:

```python
        # heavy:
        "inference_batch_size": 10,        # было 20 — теперь = num_env_workers
        "inference_batch_interval_ms": 8.0, # было 5.0 — чуть больше окно под наполнение
```

```python
        # very_heavy:
        "inference_batch_size": 10,
        "inference_batch_interval_ms": 8.0,
```

Обоснование: `inference_batch_size` ограничивает, сколько запросов сервер заберёт из очереди за раз. При батч-поиске «полезный» размер батча = число активных сред = `num_env_workers`. Брать больше воркеров нет смысла (они всё равно блокируются по одному ходу); брать меньше — недогрузить батч.

- [ ] **Step 2: Запустить короткий self-play прогон и снять метрики**

Run (PowerShell/bash, ПК1, локальный IS, профиль heavy, ~5 минут):
```bash
GMZ_INFERENCE_SERVER=1 GMZ_NUM_ENV_WORKERS=10 GMZ_INFERENCE_BATCH_SIZE=10 \
GMZ_INFERENCE_BATCH_INTERVAL_MS=8 python train.py
```
Смотреть в `runtime/logs/` строки `[GMZ][INF_SERVER] batch=...` — **средний `batch=` должен быть близок к 10**, а не к 1. Параллельно `nvidia-smi -l 1` — GPU должен быть >70–80%.

Expected: средний batch >> 1 (значит среды реально батчатся); GPU-utilization заметно выше базлайна.

- [ ] **Step 3: Сравнить throughput с базлайном LAN**

Снять `env_steps/s` (или `total_reqs` из лога за фикс. окно) для трёх конфигов при `num_simulations=48, root_top_k=12`:
1. старый LAN (до изменений, из git-тега/прошлых логов),
2. новый локальный IS на 2060S,
3. новый локальный IS на 5060Ti.

Записать в `docs/superpowers/plans/2026-05-28-gmz-batched-search.md` (раздел Results ниже) фактические числа.

Решение по 2-й GPU принимать **здесь**: если после батчинга одна 2060S даёт нужный throughput и GPU <85% — 2-я карта не нужна. Если 2060S насыщена >85% и learner голодает по данным — переходить к dual-IS shard (отдельный план).

- [ ] **Step 4: Commit**

```bash
git add app/gui_qt/gmz_hyperparams_defaults.py docs/superpowers/plans/2026-05-28-gmz-batched-search.md
git commit -m "tune: batch_size=num_env_workers for batched search; record benchmark"
```

---

## Results (заполнить после Task 5)

| Конфиг | средний batch | GPU% | env_steps/s | заметки |
|---|---|---|---|---|
| LAN базлайн (старый) | ~1 | ~40% | _TBD_ | до изменений |
| Локальный IS 2060S (новый) | _?_ | _?_ | _?_ | |
| Локальный IS 5060Ti (новый) | _?_ | _?_ | _?_ | |

**Вывод по 2-й GPU:** _заполнить на основе цифр._

---

## Антипаттерны (не делать в этом плане)

- ❌ Менять код воркера/делать «настоящий async» в Task 5 — `num_env_workers` отдельных процессов уже дают `N` конкурентных запросов. Глубокий рефактор (несколько env на воркер) — отдельный план, только если бенчмарк покажет голодание GPU при полном числе воркеров.
- ❌ Включать tree-reuse в батч-пути (Task 3) до подтверждения throughput-выигрыша.
- ❌ Тестировать эквивалентность в stochastic-режиме — порядок `np.random.choice` между путями различается by design. Эквивалентность только при `deterministic=True`.
- ❌ Полагаться на `torch.compile` для IS на Windows (нет Triton) — выигрыш только от батчинга/TF32.

## Self-Review (выполнено автором плана)

- **Покрытие спека:** Task 2 = батч-поиск (пункт 2 запроса); Task 5 = наполнение батча/конфиг (пункт 3); Task 4 = интеграция в сервер. Все три пункта закрыты.
- **Плейсхолдеры:** код в Task 1–4 полный и запускаемый; «_TBD_» только в таблице Results (это данные замера, не код).
- **Согласованность типов:** `run_batched(...)` (Task 2) ↔ `BatchedGumbelMuZeroSearch.run_batched_stateful` (Task 3) ↔ `build_batch_responses` (Task 4) используют одни и те же ключи (`env_id`, `selected_actions`, `policy_targets`, `behavior_logits`, `value_est`, `_visits_by_head`, `_q_sums_by_head`, `_legal_masks`). `warm_start` формат совпадает между Task 2 и Task 3.
