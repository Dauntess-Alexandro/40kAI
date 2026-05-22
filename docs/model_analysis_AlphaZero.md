# AlphaZero — Детальный анализ

## 1. Архитектура сети

### 1.1 Общая структура

```
Input (n_observations)
    → layer1: Linear(n_observations, 256)
    → ReLU
    → layer2: Linear(256, 256)
    → ReLU
    → Feature vector (256)
        ├── policy_heads: [Linear(256, size_1), Linear(256, size_2), ...]
        │   ↓ softmax
        │   policy_probabilities_per_head
        └── value_head: Linear(256, 1) → tanh → [-1, +1]
            ↓
        [policy_logits_per_head], value ∈ [-1, 1]
```

### 1.2 Компоненты

#### AlphaZeroPolicyValueNet

```python
class AlphaZeroPolicyValueNet(nn.Module):
    def __init__(self, n_observations, n_actions, hidden_size=256):
        super().__init__()
        self.n_observations = int(n_observations)
        self.action_sizes = [int(x) for x in n_actions]
        self.hidden_size = int(hidden_size)

        self.layer1 = nn.Linear(self.n_observations, self.hidden_size)
        self.layer2 = nn.Linear(self.hidden_size, self.hidden_size)
        self.policy_heads = nn.ModuleList([
            nn.Linear(self.hidden_size, n) for n in self.action_sizes
        ])
        self.value_head = nn.Linear(self.hidden_size, 1)
```

**Проблемы:**
- Идентичная архитектура DQN и PPO — нет общей абстракции
- `hidden_size` захардкожен = 256
- Нет residual connections
- Нет нормализации
- Value head использует tanh — ограничивает range to [-1, 1], но это правильно для AZ

#### Value head с tanh

```python
value = torch.tanh(self.value_head(x)).squeeze(-1)  # ∈ [-1, 1]
```

**Rationale:**
- AlphaZero использует tanh для ограничения value в [-1, 1]
- Это соответствует win/loss/draw outcome
- Loss: MSE between predicted and true outcome

**Проблемы:**
- tanh может "сжимать" уверенность сети
- Gradient через tanh: `(1 - tanh²) * upstream_grad`
- Для больших |x|, gradient ~ 0 (gradient vanishing)

### 1.3 Forward methods

#### Standard forward
```python
def forward(self, obs):
    x = self._encode(obs)
    policy_logits = [head(x) for head in self.policy_heads]
    value = torch.tanh(self.value_head(x)).squeeze(-1)
    return policy_logits, value
```

#### Infer с маскированием
```python
@torch.no_grad()
def infer(self, obs, masks_by_head=None):
    logits, value = self.forward(obs)
    probs = []
    for idx, head_logits in enumerate(logits):
        if masks_by_head is not None and idx < len(masks_by_head):
            mask = masks_by_head[idx]
            if mask is not None and mask.shape == head_logits.shape:
                safe_mask = torch.where(mask.any(dim=1), mask, torch.ones_like(mask))
                masked = head_logits.masked_fill(~safe_mask, -1e9)
        probs.append(torch.softmax(masked, dim=1))
    return probs, value
```

**Проблемы:**
- `mask.any(dim=1, keepdim=True)` — проверяет ЕСЛИ ЕСТЬ валидные действия
- Если все замаскированы, fallback на uniform
- Нет separate `apply_mask()` helper — дублирование кода с PPO

---

## 2. MCTS (AlphaZeroFactorizedMCTS)

### 2.1 Общая архитектура MCTS

```
AlphaZero MCTS:
┌────────────────────────────────────────────────────┐
│                    Root Node                       │
│  Prior probabilities P(s,a) from neural network   │
│  Visit counts N(s,a)                              │
│  Q-values Q(s,a)                                 │
└────────────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
    ┌─────────────────┐     ┌─────────────────┐
    │  Selection       │     │  Expansion      │
    │  UCB1/PUCT       │     │  New nodes       │
    │  argmax UCB     │     │  from action    │
    └─────────────────┘     └─────────────────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                ┌─────────────────┐
                │  Simulation     │
                │  (rollout/eval) │
                └─────────────────┘
                          │
                          ▼
                ┌─────────────────┐
                │  Backpropagation│
                │  Update N, Q   │
                └─────────────────┘
```

### 2.2 Текущая реализация: два режима

#### Режим "proxy" (быстрый, default)

```python
def _run_proxy(self, *, obs, legal_masks_by_head, temperature):
    # 1. Evaluate network once
    priors, value = self._evaluate_net(obs, legal_masks_by_head)

    # 2. Apply Dirichlet noise to priors (root only)
    for head_idx, prior in enumerate(priors):
        legal = legal_masks_by_head[head_idx]
        # Add Dirichlet noise for exploration
        noise = np.random.dirichlet([alpha] * legal_count)
        pi = (1 - eps) * prior + eps * noise
        pi = normalize(pi, legal)

    # 3. Sample action with temperature
    logits = log(pi) / temperature
    probs = softmax(logits)
    action = sample(probs)

    # 4. Return policy targets (priors)
    return policy_targets, selected_actions, value
```

**Это НЕ MCTS в классическом смысле:**
- Нет tree structure
- Нет expansion
- Нет backpropagation
- Просто: network eval + sampling

**Почему называется "proxy":**
- Это proxy для полноценного MCTS
- Используется как быстрая альтернатива для pre-training

#### Режим "tree" (глубокий поиск)

```python
def _run_tree(self, *, obs, legal_masks_by_head, temperature, env, ...):
    # 1. Root evaluation
    root_priors, root_value = self._evaluate_net(obs, legal_masks_by_head)

    # 2. Initialize search statistics
    visits = [np.zeros(size) for size in action_sizes]
    q_values = [np.zeros(size) for size in action_sizes]
    values_sum = [np.zeros(size) for size in action_sizes]

    # 3. Simulations
    for sim in range(num_simulations):
        # Selection: UCB-based
        for head_idx:
            u = q_values[head_idx] + c_puct * priors[head_idx] * sqrt(N_total) / (1 + visits[head_idx])
            u[~legal] = -inf
            action = argmax(u)

        # Simulation: step through environment
        with env.simulation_mode():
            for depth in range(max_depth):
                action_dict = convert_to_dict(action)
                next_obs, reward, done, info = env.step(action_dict)
                if done:
                    break

        # Get leaf value
        leaf_value = evaluate_network(next_obs)

        # Update statistics (backprop)
        for head_idx:
            visits[head_idx][action[head_idx]] += 1
            values_sum[head_idx][action[head_idx]] += leaf_value
            q_values[head_idx][action[head_idx]] = values_sum / visits

    # 4. Final policy from visit counts
    policy = visits / visits.sum()
    return policy, best_action, mean_leaf_value
```

### 2.3 Проблемы текущего MCTS

#### 1. Нет настоящего UCT/PUCT

```python
# Текущее (упрощённое):
u = q_values + c_puct * priors * sqrt(N_total) / (1 + visits)

# Правильное PUCT (AlphaZero):
# UCB(s,a) = Q(s,a) + c_puct * P(s,a) * sqrt(N_parent) / (1 + N(s,a))
u = Q(s,a) + c_puct * P(s,a) * sqrt(parent_visits) / (1 + visits)
```

**Проблемы:**
- `sqrt(N_total)` — должно быть `sqrt(parent_visits)`
- Нет proper UCT с log-фактором
- Для factored actions: нет cross-head exploration bonuses

#### 2. Нет proper tree structure

```python
# Текущая реализация:
# - Все симуляции share same root
# - Но каждый rollout делает fresh evaluation
# - Visit counts не накапливаются между симуляциями правильно

# Правильный подход:
class MCTSNode:
    children: dict[Action, MCTSNode]  # или dict[ActionTuple, MCTSNode]
    visit_count: int
    value_sum: float
    prior: float
```

#### 3. Environment simulation issues

```python
snapshot = env.snapshot_state() if hasattr(env, "snapshot_state") else None
# ...
if snapshot is not None and hasattr(env, "restore_state"):
    env.restore_state(snapshot)
```

**Проблемы:**
- `snapshot_state()` не гарантирует deep copy
- Для complex env (40k) snapshot может быть huge
- Нет rollback если `restore_state()` падает
- Каждая симуляция делает full env copy — slow

#### 4. No proper opponent modeling

```python
# В симуляции:
env.enemyTurn(trunc=False, policy_fn=enemy_policy_fn)
# Но enemy_policy_fn может быть None
```

**Проблемы:**
- Если нет opponent policy, используется default
- Нет proper self-play: need to alternate between two policies
- Opponent moves не влияют на search tree structure

#### 5. No cache for network evaluations

```python
# Каждый rollout делает:
_evaluate_net(obs)  # fresh inference каждый раз

# Правильно:
cache = {}
if obs in cache:
    priors, value = cache[obs]
else:
    priors, value = _evaluate_net(obs)
    cache[obs] = priors, value
```

### 2.4 PUCT formula details

```python
# AlphaZero PUCT (Schittkowski et al.):
def puct_score(node, parent_visits, c_puct=1.5):
    """
    PUCT = Q(s,a) + c_puct * P(s,a) * sqrt(N_parent) / (1 + N(s,a))

    где:
    - Q(s,a) = W(s,a) / N(s,a) — mean action value
    - P(s,a) = prior probability from network
    - N_parent = parent.visit_count
    - N(s,a) = child.visit_count
    - c_puct = exploration constant (~1.5 for Go, ~2.0 for Chess)
    """
    mean_value = node.value_sum / max(1, node.visit_count)
    prior_score = c_puct * node.prior * sqrt(parent_visits) / (1 + node.visit_count)
    return mean_value + prior_score
```

### 2.5 Temperature and exploration

#### Temperature schedule
```python
if moves_played < temperature_opening_moves:
    temperature = temperature_opening_value  # 0.9 — exploratory
else:
    temperature = temperature_late_value  # 0.15 — greedy
```

#### Dirichlet noise (root exploration)
```python
# Root node only
alpha = dirichlet_alpha  # 0.3
eps = dirichlet_eps  # 0.25

noise = np.random.dirichlet([alpha] * legal_actions)
noisy_prior = (1 - eps) * prior + eps * noise
```

**Проблемы:**
- Dirichlet parameters фиксированы — можно делать adaptive
- Noise добавляется только в root — не в child nodes

---

## 3. Replay Buffer (AlphaZeroReplayBuffer)

### 3.1 Структура

```python
@dataclass
class AZTransition:
    state: np.ndarray
    policy_targets: list[np.ndarray]  # factorized
    value_target: float  # ∈ [-1, 0, +1] or continuous
    policy_version: int = 0
```

### 3.2 Balanced outcome sampling

```python
def sample_balanced_outcome(self, batch_size):
    """
    Балансировка по исходам:
    - wins: value_target > 0.20
    - losses: value_target < -0.50
    - draws: everything else
    """
    wins = [t for t in self.buffer if t.value_target > 0.20]
    losses = [t for t in self.buffer if t.value_target < -0.50]
    draws = [t for t in self.buffer if -0.50 <= t.value_target <= 0.20]

    # Sample equally from each category
    per_group = batch_size // len(non_empty_groups)
    for group in [wins, losses, draws]:
        take = min(len(group), per_group)
        out.extend(random.sample(group, take))
```

**Проблемы:**
- Thresholds захардкожены (0.20, -0.50)
- Нет per-faction sampling
- Не учитывает game phase

### 3.3 Policy staleness

```python
# В trainer:
max_staleness = config.max_policy_staleness_updates
if max_staleness >= 0:
    min_ver = current_policy_version - max_staleness
    batch = [b for b in batch if b.policy_version >= min_ver]
```

**Rationale:**
- Old data trained на old policy может быть misleading
- Staleness limit = 600 updates (из hyperparams.json)
- После 600 updates — данные отбрасываются

---

## 4. Training Loop

### 4.1 Training step

```python
def train_alphazero_step(net, optimizer, replay, config, device):
    # 1. Sample batch
    if config.balanced_outcome_sampling:
        batch = replay.sample_balanced_outcome(config.batch_size)
    else:
        batch = replay.sample(config.batch_size)

    # 2. Filter by staleness
    if config.max_policy_staleness_updates >= 0:
        batch = [b for b in batch if b.policy_version >= min_ver]

    # 3. Compute losses
    obs = torch.tensor([b.state for b in batch])
    target_value = torch.tensor([b.value_target for b in batch])

    logits_by_head, value = net(obs)

    # Policy loss: cross-entropy
    policy_loss = 0
    for h_idx, logits in enumerate(logits_by_head):
        target_pi = [b.policy_targets[h_idx] for b in batch]
        target_pi = target_pi / target_pi.sum(dim=1, keepdim=True)  # normalize
        logp = F.log_softmax(logits, dim=1)
        policy_loss += -(target_pi * logp).sum(dim=1).mean()

    # Value loss: MSE
    value_loss = F.mse_loss(value, target_value)

    # L2 regularization
    l2 = sum((p ** 2).sum() for p in net.parameters())

    # Total loss
    loss = policy_loss + config.value_loss_weight * value_loss + config.l2_weight * l2

    # 4. Backprop
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
    optimizer.step()

    return loss_metrics
```

### 4.2 Loss functions

#### Policy loss (cross-entropy)

```python
# Standard cross-entropy
policy_loss = -Σ target_pi * log(predicted_pi)

# With masking:
# masked_policy_loss = -Σ_{legal} target_pi * log(predicted_pi)
```

**Rationale:**
- AlphaZero target = MCTS policy distribution (not one-hot)
- Cross-entropy penalizes deviation from target distribution
- Weighted by target probability — more weight on likely actions

#### Value loss (MSE)

```python
value_loss = (value_predicted - value_target)²
```

**Rationale:**
- AlphaZero value ∈ [-1, +1]
- MSE appropriate for regression
- Alternative: cross-entropy with discretized value bins

### 4.3 Self-play loop

```python
def play_episode_with_mcts(net, env, config, ...):
    transitions = []
    current_policy_version = net.policy_version

    obs = env.reset()
    while not done:
        # Get legal masks
        legal_masks = env.get_legal_action_masks_by_head()

        # Run MCTS
        policy_targets, actions, value = mcts.run(
            obs=obs,
            legal_masks_by_head=legal_masks,
            temperature=temperature,
            env=env,
            ...
        )

        # Environment step
        next_obs, reward, done, info = env.step(actions)

        # Store transition
        transitions.append(AZTransition(
            state=obs,
            policy_targets=policy_targets,
            value_target=value,  # or reward from episode
            policy_version=current_policy_version
        ))

        obs = next_obs

    return transitions
```

---

## 5. Configuration (hyperparams.json)

```json
"alphazero": {
    "learning_rate": 0.0003,
    "batch_size": 128,
    "value_loss_weight": 1.0,
    "l2_weight": 1e-06,

    "mcts_simulations": 128,
    "c_puct": 1.1,
    "dirichlet_alpha": 0.3,
    "dirichlet_eps": 0.25,
    "mcts_mode": "tree",
    "mcts_top_k_per_head": 12,
    "mcts_max_depth": 4,
    "mcts_root_dirichlet_only": 1,

    "temperature_opening_moves": 12,
    "temperature_opening_value": 0.9,
    "temperature_late_value": 0.15,

    "replay_capacity": 200000,
    "num_actors": 2,
    "actor_batch_send": 64,
    "actor_queue_max": 256,
    "sync_every_updates": 2,
    "updates_per_rollout": 2,
    "replay_min_size": 512,

    "balanced_outcome_sampling": 1,
    "max_policy_staleness_updates": 600,

    "det_eval_gate_win_min": 0.45,
    "det_eval_gate_turn_limit_max": 0.65,

    "outcome_only": 1,
    "outcome_value_win": 1.0,
    "outcome_value_loss": -1.0,
    "outcome_value_draw": -0.25
}
```

### Анализ параметров

#### c_puct = 1.1
- **Standard:** 1.5 (Go), 1.4 (Chess), 1.25 (Shogi)
- **Проблема:** 1.1 довольно низко — может недостаточно explore
- **Рекомендация:** Начать с 1.5, adjust based on win rate

#### mcts_simulations = 128
- **Standard:** 800-1600 (Go), 100-400 (Chess)
- **Проблема:** 128 может быть мало для сложных позиций
- **Рекомендация:** Увеличить до 256-512 если есть compute budget

#### mcts_max_depth = 4
- **Проблема:** Глубина 4 может быть недостаточно
- **Рекомендация:** Сделать adaptive: min(episodic_length - current_step, max_depth)

#### mcts_top_k_per_head = 12
- **Проблема:** Это pruning параметр — может отрезать good moves
- **Рекомендация:** Если action space большой (40k!), k должен быть больше

#### temperature_opening = 0.9
- **Standard:** 1.0-1.2 (exploratory phase)
- **Analysis:** 0.9 — умеренно exploratory

#### temperature_late = 0.15
- **Standard:** 0.0-0.1 (greedy phase)
- **Analysis:** 0.15 — still some exploration

---

## 6. Actor-Learner Architecture

### 6.1 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                       Actors                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Actor 1   │  │  Actor 2   │  │  Actor N   │        │
│  │ (CPU/env)  │  │ (CPU/env)  │  │ (CPU/env)  │        │
│  │   MCTS     │  │   MCTS     │  │   MCTS     │        │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘        │
│         │               │               │                │
│         └───────────────┼───────────────┘                │
│                         ▼                                │
│                   ┌─────────┐                            │
│                   │  Queue  │ (transitions)              │
│                   └────┬────┘                            │
└────────────────────────┼─────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Learner    │
                  │  (GPU/train) │
                  │  AlphaZero  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Sync File    │
                  │ (weights)    │
                  └─────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     ┌─────────┐    ┌─────────┐    ┌─────────┐
     │ Actor 1 │    │ Actor 2 │    │ Actor N │
     └─────────┘    └─────────┘    └─────────┘
```

### 6.2 Implementation details

```python
# Actor: Self-play with MCTS
def actor_loop(actor_id, queue, sync_path):
    net = AlphaZeroPolicyValueNet(...)
    mcts = AlphaZeroFactorizedMCTS(net, config)

    while True:
        # Load weights
        checkpoint = torch.load(sync_path)
        net.load_state_dict(checkpoint['state_dict'])

        # Self-play episode
        transitions = play_episode_with_mcts(net, env, mcts_config)

        # Send to learner
        queue.put(transitions)

# Learner: Training
def learner_loop(queue):
    net = AlphaZeroPolicyValueNet(...).to(device)
    optimizer = optim.Adam(net.parameters(), lr=lr)
    replay = AlphaZeroReplayBuffer(capacity=200000)
    policy_version = 0

    while True:
        # Collect from queue
        for _ in range(num_actors):
            if queue.full():
                break
            transitions = queue.get()
            replay.push_many(transitions)

        # Train
        if len(replay) >= replay_min_size:
            metrics = train_alphazero_step(net, optimizer, replay, config, device)
            policy_version += 1

            # Sync
            if policy_version % sync_every_updates == 0:
                torch.save({
                    'state_dict': net.state_dict(),
                    'policy_version': policy_version,
                }, sync_path)
```

---

## 7. Улучшения (Roadmap)

### 7.1 High Priority

#### A. Proper PUCT MCTS implementation

```python
class MCTSNode:
    def __init__(self, prior: float, parent: MCTSNode = None):
        self.parent = parent
        self.prior = prior
        self.children: dict[ActionTuple, MCTSNode] = {}
        self.visit_count = 0
        self.value_sum = 0.0
        self.action: ActionTuple | None = None

    def puct_score(self, c_puct: float = 1.5) -> float:
        if self.visit_count == 0:
            return float('inf')
        mean_q = self.value_sum / self.visit_count
        if self.parent is None:
            parent_visits = 1
        else:
            parent_visits = self.parent.visit_count
        exploration = c_puct * self.prior * sqrt(parent_visits) / (1 + self.visit_count)
        return mean_q + exploration

class AlphaZeroMCTS:
    def __init__(self, net, config):
        self.net = net
        self.cfg = config
        self.root: MCTSNode | None = None
        self.cache: dict[np.ndarray, tuple[list, float]] = {}

    def search(self, obs, legal_masks, num_simulations):
        # Initialize root
        priors, value = self._evaluate_net_with_cache(obs, legal_masks)
        self.root = MCTSNode(prior=1.0)

        for _ in range(num_simulations):
            node = self._select(self.root, legal_masks)
            node = self._expand(node, obs, legal_masks, priors)

            value = self._evaluate(node, obs)
            self._backpropagate(node, value)

        return self._get_policy(self.root), self._get_best_action(self.root)

    def _select(self, node, legal_masks):
        while node.children:
            best_score = float('-inf')
            best_child = None
            for child in node.children.values():
                score = child.puct_score(self.cfg.c_puct)
                if score > best_score:
                    best_score = score
                    best_child = child
            node = best_child
        return node

    def _expand(self, node, obs, legal_masks, priors):
        for action_idx in range(len(legal_masks)):
            if legal_masks[action_idx]:
                node.children[action_idx] = MCTSNode(
                    prior=priors[action_idx],
                    parent=node
                )
        return node

    def _evaluate(self, node, obs):
        # Use network or rollout
        if self.cfg.rollout:
            return self._rollout(obs, node.action)
        else:
            _, value = self._evaluate_net_with_cache(obs, ...)
            return value

    def _backpropagate(self, node, value):
        while node is not None:
            node.visit_count += 1
            node.value_sum += value
            node = node.parent
```

#### B. Cache for network evaluations

```python
class EvaluationCache:
    def __init__(self, max_size=10000):
        self.cache = {}
        self.max_size = max_size

    def get(self, obs):
        key = obs.tobytes()
        return self.cache.get(key)

    def set(self, obs, priors, value):
        key = obs.tobytes()
        if len(self.cache) > self.max_size:
            # LRU eviction
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = (priors, value)
```

#### C. Proper environment snapshot

```python
class CheckpointedEnv:
    def snapshot_state(self):
        return {
            'board': self.board.copy(),
            'units': [u.copy() for u in self.units],
            'game_state': self.game_state.copy(),
            'rng_state': np.random.get_state(),
        }

    def restore_state(self, snapshot):
        self.board = snapshot['board']
        self.units = snapshot['units']
        self.game_state = snapshot['game_state']
        np.random.set_state(snapshot['rng_state'])
```

### 7.2 Medium Priority

#### A. Adaptive c_puct

```python
def adaptive_c_puct(base: float, progress: float, min_c: float = 1.0, max_c: float = 2.0):
    """
    Early game: higher c_puct (more exploration)
    Late game: lower c_puct (more exploitation)
    """
    return min_c + (max_c - min_c) * (1 - progress)
```

#### B. Progressive widening

```python
def progressive_widening(visits, depth):
    """
    Child is expanded if:
    visits >= depth ** 1.5
    """
    return visits >= depth ** 1.5
```

#### C. Move averaging (draw reduction)

```python
def get_policy_with_move_averaging(visits, temperature, move_count):
    """
    Late game: use visit counts directly (greedy)
    Early game: average with prior
    """
    if move_count < early_game_moves:
        avg_visits = (visits + prior * early_game_weight) / (1 + early_game_weight)
        return softmax(log(avg_visits) / temperature)
    else:
        return softmax(log(visits) / temperature)
```

### 7.3 Low Priority

#### A. Neural network architecture improvements
- Residual blocks
- Layer normalization
- Attention mechanism

#### B. Self-play improvements
- Opponent pool (PFSP)
- Population-based training

#### C. Training improvements
- Learning rate warmup
- Checkpoint averaging
-分布式 training

---

## 8. Testing

### 8.1 Unit tests

```python
def test_alphazero_forward():
    net = AlphaZeroPolicyValueNet(n_observations=100, n_actions=[5, 3])
    x = torch.randn(32, 100)
    logits, value = net(x)
    assert len(logits) == 2
    assert value.shape == (32,)
    assert value.min() >= -1.0 and value.max() <= 1.0

def test_alphazero_infer():
    net = AlphaZeroPolicyValueNet(n_observations=100, n_actions=[5])
    x = torch.randn(32, 100)
    mask = torch.zeros(32, 5, dtype=torch.bool)
    mask[:, 2] = True
    probs, value = net.infer(x, masks_by_head=[mask])
    # probs[:, 2] должен быть ~1.0
    assert torch.allclose(probs[0][:, 2], torch.tensor(1.0), atol=1e-5)

def test_mcts_proxy():
    net = AlphaZeroPolicyValueNet(n_observations=100, n_actions=[5])
    mcts = AlphaZeroFactorizedMCTS(net, MCTSConfig(mode="proxy"))
    obs = np.random.randn(100).astype(np.float32)
    masks = [np.ones(5, dtype=bool)]
    policy, actions, value = mcts.run(obs=obs, legal_masks_by_head=masks)
    assert len(policy) == 1
    assert len(actions) == 1
    assert abs(value) <= 1.0

def test_mcts_tree():
    net = AlphaZeroPolicyValueNet(n_observations=100, n_actions=[5])
    mcts = AlphaZeroFactorizedMCTS(net, MCTSConfig(mode="tree", simulations=10))
    # Test requires env — skip or mock
```

### 8.2 Integration tests

```python
def test_alphazero_training_loop():
    net = AlphaZeroPolicyValueNet(n_observations=100, n_actions=[5])
    optimizer = optim.Adam(net.parameters(), lr=1e-3)
    replay = AlphaZeroReplayBuffer(capacity=1000)

    # Generate fake data
    for _ in range(100):
        obs = np.random.randn(100).astype(np.float32)
        policy = np.random.dirichlet([0.3]*5).astype(np.float32)
        value = np.random.choice([1.0, -1.0, 0.0])
        replay.push(AZTransition(
            state=obs,
            policy_targets=[policy],
            value_target=value
        ))

    # Training step
    config = AlphaZeroTrainConfig(batch_size=32)
    metrics = train_alphazero_step(net, optimizer, replay, config, 'cpu')
    assert 'loss' in metrics
```

---

## 9. Summary

| Aspect | Current | Recommended |
|--------|---------|-------------|
| MCTS mode | Proxy + simplified tree | Full PUCT tree |
| Tree structure | Flat arrays | Proper Node class |
| UCB formula | Simplified | AlphaZero PUCT |
| Environment sim | snapshot/restore | CheckpointedEnv |
| Network cache | None | LRU cache |
| c_puct | 1.1 | 1.5 (adaptive) |
| Simulations | 128 | 256-512 |
| Depth | 4 | Adaptive |
| Dirichlet | Fixed | Adaptive |
| Value head | tanh(Linear) | MLP + tanh |

---

*Дата: 2026-05-22*
*Файл: `docs/model_analysis_AlphaZero.md`*