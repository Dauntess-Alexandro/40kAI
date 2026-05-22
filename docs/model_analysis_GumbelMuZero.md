# GumbelMuZero (GMZ) — Детальный анализ

## 1. Концептуальная основа

### 1.1 MuZero Overview

MuZero — это model-based RL алгоритм, который:
1. Learns **representation** — наблюдение → латентное состояние
2. Learns **dynamics** — латентное состояние + действие → следующее латентное состояние + reward
3. Learns **prediction** — латентное состояние → policy + value

```
Real Environment:
obs → [Environment] → next_obs, reward

MuZero (learned model):
obs → representation → latent
latent + action → dynamics → next_latent, reward_predicted
latent → prediction → policy, value
```

### 1.2 Gumbel additions

GumbelMuZero добавляет:
- **Gumbel-Softmax** для differentiable sampling
- **Gumbel search** для planning (replaces MCTS)

### 1.3 Relationship to other algorithms

```
MuZero:
  - Learned model (representation + dynamics + prediction)
  - MCTS for planning
  - Atari: 0.99 discount, ~800 simulations

GumbelMuZero:
  - Same learned model as MuZero
  - Gumbel-Softmax for discrete actions
  - Gumbel search (root planning)
  - Can use higher discount (0.997)

AlphaZero:
  - No learned model
  - Uses real environment
  - MCTS for planning
  - No reward prediction

DQN/PPO:
  - No model
  - Direct policy/value estimation
  - No planning
```

---

## 2. Архитектура сети

### 2.1 Общая структура

```
Input (obs_dim)
    │
    ├─── REPRESENTATION: obs → latent ─────────────────────────┐
    │    Linear(obs_dim, 256)                                  │
    │    ReLU                                                   │
    │    Linear(256, latent_dim)                                │
    │    ReLU                                                   │
    │    ↓ normalize                                           │
    │    latent (latent_dim)                                   │
    │                                                           │
    ├─── DYNAMICS: (latent, action) → next_latent + reward ────┤
    │    action_embed = [Embedding(action_i) for action_i]       │
    │    concat: [latent, emb_1, emb_2, ..., emb_k]            │
    │    → dynamics_torso: Linear(total, 256)                   │
    │    → ReLU                                                 │
    │    → Linear(256, 256)                                    │
    │    → ReLU                                                 │
    │    ├─→ next_latent_head: Linear(256, latent_dim)         │
    │    │       ↓ normalize                                    │
    │    └─→ reward_head: Linear(256, 1)                        │
    │           ↓                                              │
    │           reward                                         │
    │                                                           │
    └─── PREDICTION: latent → policy + value ────────────────────
         prediction_torso: Linear(latent_dim, 256)
         ReLU
         ├─→ policy_heads: [Linear(256, size_i) for size_i]
         │       ↓ softmax (with mask)
         │       policy_probs
         └─→ value_head: Linear(256, 1)
                 ↓ tanh
                 value ∈ [-1, 1]
```

### 2.2 Representation Network

```python
self.representation = nn.Sequential(
    nn.Linear(self.obs_dim, self.hidden_dim),
    nn.ReLU(),
    nn.Linear(self.hidden_dim, self.latent_dim),
    nn.ReLU(),
)
```

**Проблемы:**
- Simple MLP — не использует spatial структуру 40k
- No attention mechanism
- No residual connections
- Hidden dim = 256 захардкожен

### 2.3 Action Embeddings

```python
self.action_embeddings = nn.ModuleList([
    nn.Embedding(int(size), self.action_embed_dim)
    for size in self.action_sizes
])

def _embed_actions(self, actions):
    embeds = []
    for idx, emb in enumerate(self.action_embeddings):
        head_actions = actions[:, idx].long().clamp(min=0, max=self.action_sizes[idx] - 1)
        embeds.append(emb(head_actions))
    return torch.cat(embeds, dim=1)
```

**Проблемы:**
- Simple embedding lookup — не учитывает структуру действий
- Для 40k действий embedding может быть sparse
- Нет shared embeddings между похожими действиями
- No action history encoding

**Embedding dimensions:**
- `action_embed_dim = 64` (from hyperparams.json)
- Для 10 действий: 64 * 10 = 640 dims в dynamics input

### 2.4 Dynamics Model

```python
dyn_in = self.latent_dim + self.action_embed_dim * self.num_heads
self.dynamics_torso = nn.Sequential(
    nn.Linear(dyn_in, self.hidden_dim),  # 256 + 640 = 896 → 256
    nn.ReLU(),
    nn.Linear(self.hidden_dim, self.hidden_dim),  # 256 → 256
    nn.ReLU(),
)
self.next_latent_head = nn.Linear(self.hidden_dim, self.latent_dim)
self.reward_head = nn.Linear(self.hidden_dim, 1)
```

**Forward dynamics:**
```python
def dynamics(self, latent, actions):
    action_emb = self._embed_actions(actions)
    h = self.dynamics_torso(torch.cat([latent, action_emb], dim=1))
    next_latent = _normalize_latent(self.next_latent_head(h))
    reward = self.reward_head(h).squeeze(1)
    return next_latent, reward
```

**Проблемы:**
- Reward head = single linear (no hidden layer)
- No skip connection from input latent
- Нет GRU/LSTM — stateless dynamics
- `action_embed_dim * num_heads` может быть очень большим для 40k

### 2.5 Prediction Network

```python
self.prediction_torso = nn.Sequential(
    nn.Linear(self.latent_dim, self.hidden_dim),
    nn.ReLU(),
)
self.policy_heads = nn.ModuleList([
    nn.Linear(self.hidden_dim, int(size)) for size in self.action_sizes
])
self.value_head = nn.Linear(self.hidden_dim, 1)
```

### 2.6 Latent Normalization

```python
def _normalize_latent(latent, eps=1e-6):
    mean = latent.mean(dim=1, keepdim=True)
    std = latent.std(dim=1, keepdim=True).clamp_min(eps)
    return (latent - mean) / std
```

**Проблемы:**
- Normalization per-batch — может давать разные масштабы
- Mean/std computed from batch — not from population
- Better: LayerNorm or running statistics

---

## 3. Inference Methods

### 3.1 Initial Inference (from observation)

```python
def initial_inference(self, obs, masks_by_head=None):
    latent = self.encode(obs)  # representation network
    policy_logits, value = self.predict(latent, masks_by_head=masks_by_head)
    reward = torch.zeros_like(value)  # no reward at initial state
    return policy_logits, value, reward, latent
```

**Usage:** Start of episode, root node of search tree

### 3.2 Recurrent Inference (from latent state)

```python
def recurrent_inference(self, latent, actions, masks_by_head=None):
    next_latent, reward = self.dynamics(latent, actions)
    policy_logits, value = self.predict(next_latent, masks_by_head=masks_by_head)
    return policy_logits, value, reward, next_latent
```

**Usage:** After taking action, inner nodes of search tree

### 3.3 Inference (wrapper for non-MCTS usage)

```python
@torch.no_grad()
def infer(self, obs, masks_by_head=None):
    logits, value, _reward, _latent = self.initial_inference(obs, masks_by_head=masks_by_head)
    probs = [F.softmax(x, dim=1) for x in logits]
    return probs, value
```

---

## 4. GumbelMuZero Search

### 4.1 Architecture

```
Root node:
    obs → initial_inference → latent_root, policy_logits

    For each action head:
        For each simulation:
            1. Sample top-k candidates (Gumbel-based)
            2. For each candidate:
               latent + action → recurrent_inference → value
               Q(a) = reward + discount * value
            3. Mix Q-values with priors
            4. Sample final action
```

### 4.2 Search implementation

```python
@torch.no_grad()
def run(self, *, obs, legal_masks_by_head, deterministic=True):
    # 1. Initial inference
    obs_t = torch.tensor(obs).unsqueeze(0)
    masks_t = [torch.as_tensor(m).unsqueeze(0) for m in legal_masks_by_head]
    root_logits, root_value, _reward, latent = self.net.initial_inference(obs_t, masks_t)

    # 2. Base action from greedy policy
    base_action = [int(torch.argmax(head).item()) for head in root_logits]

    # 3. Gumbel sampling per head
    for head_idx, head_logits in enumerate(root_logits):
        logits_np = head_logits.squeeze(0).cpu().numpy()
        legal = legal_masks_by_head[head_idx]

        # Gumbel trick for top-k selection
        gumbel = np.random.gumbel(0, gumbel_scale, size=legal.size)
        ranking = np.argsort(logits_np + gumbel)[::-1]
        top_k = ranking[:root_top_k]
        candidates = legal_idx[top_k]

        # 4. Simulate each candidate
        for candidate in candidates:
            action_vec = base_action.copy()
            action_vec[head_idx] = candidate

            _, val_next, rew_next, _ = self.net.recurrent_inference(
                latent, action_vec, masks_t
            )
            q = rew_next.item() + discount * val_next.item()

            visits[candidate] += 1
            q_values[candidate] += q

        # 5. Final policy from Q-values
        mixed_logits = q_values.copy()
        pi = masked_softmax(mixed_logits, legal_mask=legal, temperature=temp)
        action = argmax(pi) if deterministic else sample(pi)
```

### 4.3 Проблемы текущей реализации

#### 1. Round-robin simulation

```python
for sim in range(sims):
    candidate = candidate_actions[sim % candidate_actions.size]
    # ...
```

**Проблема:** Это round-robin, НЕ proper sampling
- Если simulations = 32 и candidates = 8, то каждый candidate симулируется 4 раза
- Но это не stochastic sampling
- Gumbel используется только для выбора top-k, не для самих симуляций

#### 2. No proper Gumbel-UCB

```python
# Правильный Gumbel-UCB:
# score(action) = Q(action) + gumbel * temperature * (visits / total_visits)

# Текущий код:
# Q-values просто усредняются по visits
q_values[candidate] = q_values_sum / per_action_counts
```

#### 3. No uncertainty in Q-values

```python
# Текущее: только mean Q-value
q_values[candidate] = q_values_sum / per_action_counts

# Лучше: mean + uncertainty
q_values[candidate] = mean + beta * std
```

#### 4. No prior mixing

```python
# Текущее:
pi = _masked_softmax(q_values, ...)  # только Q-values

# Правильный подход (MuZero style):
# pi = (1 - w) * softmax(Q / temperature) + w * prior
# где w — weight for prior, decays over time
```

### 4.4 Gumbel-Softmax theory

**Standard Gumbel-Max:**
```python
z = logits + gumbel  # gumbel noise
action = argmax(z)  # discrete sample
```

**Gumbel-Softmax (Concrete distribution):**
```python
temperature = 1.0
gumbel = -log(-log(uniform(0,1)))
z = (logits + gumbel) / temperature
probs = softmax(z)  # differentiable
```

**Reparameterization trick:**
```python
def gumbel_softmax_sample(logits, temperature):
    gumbel = -log(-log(uniform(0,1)))
    return softmax((logits + gumbel) / temperature)
```

---

## 5. Replay Buffer (GumbelMuZeroReplayBuffer)

### 5.1 Структура

```python
@dataclass
class GMZTransition:
    state: np.ndarray
    action: np.ndarray
    reward: float
    done: bool
    policy_targets: list[np.ndarray]  # from search
    value_target: float  # n-step bootstrap
    policy_version: int = 0
```

### 5.2 Unrolled sampling

```python
def sample_unroll(self, batch_size, unroll_steps, ...):
    # Sample start positions
    starts = random.sample(range(len(self.buffer)), batch_size)

    for start in starts:
        seq_states = []
        seq_actions = []
        seq_rewards = []
        seq_policies = []
        seq_values = []

        for k in range(unroll_steps):
            idx = min(start + k, len(self.buffer) - 1)
            tr = self.buffer[idx]
            seq_states.append(tr.state)
            seq_actions.append(tr.action)
            seq_rewards.append(tr.reward)
            seq_policies.append(tr.policy_targets)
            seq_values.append(tr.value_target)

            if tr.done:
                break

        # Return full sequence for BPTT
        yield {
            'states': seq_states,
            'actions': seq_actions,
            'rewards': seq_rewards,
            'policy_targets': seq_policies,
            'value_targets': seq_values,
        }
```

**Проблемы:**
- Не проверяется staleness до построения последовательности
- Если start близко к концу буфера, последовательность короткая
- Нет truncation backpropagation through time (TBPTT)

---

## 6. Training Loop

### 6.1 Training step

```python
def train_gumbel_muzero_step(net, optimizer, replay, config, device):
    # 1. Sample unrolled sequences
    batch = replay.sample_unroll(
        batch_size=config.batch_size,
        unroll_steps=config.unroll_steps,
        ...
    )

    # 2. Initial inference
    obs0 = torch.tensor(states[0]).unsqueeze(0)
    logits, value, reward0, latent = net.initial_inference(obs0)

    # Policy loss at t=0
    policy_loss = _policy_ce_loss(logits, policies[0])
    value_loss = F.mse_loss(value, values[0])
    reward_loss = F.mse_loss(reward0, 0.0)  # no reward at initial

    # 3. Unroll dynamics
    for t in range(1, unroll_steps):
        action_t = torch.tensor(actions[t-1]).unsqueeze(0)
        logits_t, value_t, reward_t, latent = net.recurrent_inference(
            latent, action_t
        )

        policy_loss += _policy_ce_loss(logits_t, policies[t])
        value_loss += F.mse_loss(value_t, values[t])
        reward_loss += F.mse_loss(reward_t, rewards[t-1])

    # 4. Total loss
    loss = (
        policy_loss
        + config.value_loss_weight * value_loss
        + config.reward_loss_weight * reward_loss
        + config.l2_weight * l2
    )

    # 5. Backprop
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
    optimizer.step()
```

### 6.2 Unrolled loss

```
L_total = Σ_{t=0}^{T} [
    L_policy(π_t, π_target_t)
    + λ_v * L_value(v_t, z_t)
    + λ_r * L_reward(r_t, u_t)
]

где:
- T = unroll_steps
- π_t = predicted policy at step t
- π_target_t = target policy from search
- v_t = predicted value
- z_t = n-step return
- r_t = predicted reward
- u_t = actual reward
```

### 6.3 BPTT (Backpropagation Through Time)

```python
# Forward:
latent_0 = encode(obs_0)
for t in range(T):
    latent_{t+1}, reward_t = dynamics(latent_t, action_t)
    policy_t, value_t = predict(latent_{t+1})

# Backward:
loss.backward()  # gradients flow through all T steps
# Это работает потому что все операции differentiable
```

**Проблемы:**
- BPTT through T steps — vanishing gradients для длинных sequences
- MuZero paper рекомендует TBPTT (truncate after K steps)
- Нет optimization for long sequences

---

## 7. Configuration (hyperparams.json)

```json
"gumbel_muzero": {
    "learning_rate": 0.0003,
    "batch_size": 128,
    "unroll_steps": 5,
    "value_loss_weight": 1.0,
    "reward_loss_weight": 1.0,
    "l2_weight": 1e-06,
    "discount": 0.997,

    "replay_capacity": 250000,
    "num_actors": 8,
    "actor_batch_send": 64,
    "actor_queue_max": 256,
    "sync_every_updates": 2,
    "updates_per_rollout": 2,
    "replay_min_size": 512,

    "max_policy_staleness_updates": 600,

    "latent_dim": 256,
    "hidden_dim": 256,
    "action_embed_dim": 64,

    "num_simulations": 32,
    "root_top_k": 8,
    "gumbel_scale": 1.0,
    "search_temperature": 0.15,

    "temperature_opening_moves": 12,
    "temperature_opening_value": 1.0,
    "temperature_late_value": 0.25,

    "outcome_only": 1,
    "outcome_value_win": 1.0,
    "outcome_value_loss": -1.0,
    "outcome_value_draw": -0.25
}
```

### Анализ параметров

#### discount = 0.997
- **MuZero standard:** 0.997 (Atari), 0.99 (shorter games)
- **Rationale:** Higher discount позволяет планировать дальше
- **Проблема:** Для долгих эпизодов 40k, 0.997 всё ещё большой

#### unroll_steps = 5
- **MuZero standard:** 5-10
- **Проблема:** 5 может быть мало для сложных states
- **Рекомендация:** 5-10, adaptive based on game phase

#### num_simulations = 32
- **MuZero:** 50-800 depending on compute
- **Проблема:** 32 очень мало для сложных игр
- **Рекомендация:** 64-128 если есть compute

#### root_top_k = 8
- **Проблема:** Если action space большой (40k!), k=8 может быть мало
- **Рекомендация:** Сделать adaptive: max(8, sqrt(action_space_size))

#### gumbel_scale = 1.0
- **Проблема:** Фиксированный scale — не adaptive
- **Рекомендация:** Decay scale over training

---

## 8. Actor-Learner Architecture

### 8.1 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                          Actors                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Actor 1   │  │  Actor 2   │  │  Actor N   │          │
│  │ (CPU/env)  │  │ (CPU/env)  │  │ (CPU/env)  │          │
│  │ GMZ Search │  │ GMZ Search │  │ GMZ Search │          │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘          │
│         │               │               │                   │
│         └───────────────┼───────────────┘                   │
│                         ▼                                   │
│                   ┌─────────┐                              │
│                   │  Queue  │ (transitions)               │
│                   └────┬────┘                              │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Learner    │
                  │  (GPU/train) │
                  │   GumbelMZ   │
                  │   + BPTT     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Sync File    │
                  │ (weights)    │
                  └──────────────┘
```

### 8.2 Actor loop

```python
def actor_loop_gumbel_muzero(actor_id, queue, sync_path):
    net = GumbelMuZeroNet(...).to('cpu')
    search = GumbelMuZeroSearch(net, config)
    env = WarhammerEnv()

    while True:
        # Load weights
        checkpoint = torch.load(sync_path, map_location='cpu')
        net.load_state_dict(checkpoint['state_dict'])

        # Episode
        obs = env.reset()
        done = False
        transitions = []

        while not done:
            # Get masks
            legal_masks = env.get_legal_action_masks_by_head()

            # Gumbel search
            policy, actions, value = search.run(
                obs=obs,
                legal_masks_by_head=legal_masks,
            )

            # Step
            next_obs, reward, done, info = env.step(actions)

            # Store
            transitions.append(GMZTransition(
                state=obs,
                action=np.array(actions),
                reward=reward,
                done=done,
                policy_targets=policy,
                value_target=value,
            ))

            obs = next_obs

        # Send to learner
        queue.put(transitions)
```

### 8.3 Learner loop

```python
def learner_loop_gumbel_muzero(queue):
    net = GumbelMuZeroNet(...).to(device)
    optimizer = optim.Adam(net.parameters(), lr=lr)
    replay = GumbelMuZeroReplayBuffer(capacity=250000)
    policy_version = 0

    while True:
        # Collect transitions
        for _ in range(num_actors):
            if not queue.empty():
                transitions = queue.get()
                replay.push_many(transitions)

        # Train
        if len(replay) >= replay_min_size:
            for _ in range(updates_per_rollout):
                metrics = train_gumbel_muzero_step(
                    net, optimizer, replay, config, device
                )
                policy_version += 1

            # Sync
            if policy_version % sync_every_updates == 0:
                torch.save({
                    'state_dict': net.state_dict(),
                    'policy_version': policy_version,
                }, sync_path)
```

---

## 9. Улучшения (Roadmap)

### 9.1 High Priority

#### A. Residual dynamics

```python
class ResidualDynamics(nn.Module):
    def __init__(self, latent_dim, action_dim, hidden_dim):
        super().__init__()
        self.gru = nn.GRUCell(action_dim, latent_dim)
        self.mlp = nn.Sequential(
            nn.Linear(latent_dim * 2, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.ReLU(),
        )
        self.latent_head = nn.Linear(hidden_dim, latent_dim)
        self.reward_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, latent, action_emb):
        # GRU for deterministic transition
        next_latent_det = self.gru(action_emb, latent)

        # MLP for residual
        combined = torch.cat([next_latent_det, latent], dim=-1)
        h = self.mlp(combined)

        next_latent = self.latent_head(h) + next_latent_det  # residual
        reward = self.reward_head(h)

        return next_latent, reward
```

#### B. Separate value network

```python
# В MuZero, value often needs separate network
class SeparateValueNetwork(nn.Module):
    def __init__(self, latent_dim, hidden_dim):
        super().__init__()
        self.value_head = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, latent):
        return torch.tanh(self.value_head(latent))
```

#### C. Better reward head

```python
self.reward_head = nn.Sequential(
    nn.Linear(self.hidden_dim, self.hidden_dim // 2),
    nn.LayerNorm(self.hidden_dim // 2),
    nn.ReLU(),
    nn.Linear(self.hidden_dim // 2, self.hidden_dim // 4),
    nn.ReLU(),
    nn.Linear(self.hidden_dim // 4, 1)
)
```

#### D. Proper Gumbel search with UCB

```python
def gumbel_ucb_search(self, latent, priors, legal_masks, num_simulations):
    num_heads = len(priors)
    visits = [np.zeros(s) for s in action_sizes]
    q_values = [np.zeros(s) for s in action_sizes]
    q_sums = [np.zeros(s) for s in action_sizes]

    for sim in range(num_simulations):
        for head_idx in range(num_heads):
            prior = priors[head_idx]
            legal = legal_masks[head_idx]

            # Gumbel-UCB score
            gumbel = np.random.gumbel(0, self.gumbel_scale, legal.sum())
            scores = prior[legal] * np.exp(gumbel / self.search_temperature)
            scores = scores / scores.sum()

            # Sample candidate
            candidate = np.random.choice(len(legal), p=scores)

            # Get Q-value
            action_vec = base_action.copy()
            action_vec[head_idx] = candidate
            _, value, reward, _ = self.net.recurrent_inference(
                latent, action_vec
            )
            q = reward + self.discount * value

            # Update
            visits[head_idx][candidate] += 1
            q_sums[head_idx][candidate] += q
            q_values[head_idx] = q_sums[head_idx] / np.maximum(visits[head_idx], 1)

    # Final policy
    policy = []
    for head_idx in range(num_heads):
        legal = legal_masks[head_idx]
        pi = masked_softmax(q_values[head_idx], legal, self.search_temperature)
        policy.append(pi)

    return policy
```

### 9.2 Medium Priority

#### A. MuZero Reanalyze

```python
class ReanalyzeBuffer:
    """
    MuZero Reanalyze: use recent value estimates to re-label old data
    """
    def reanalyze(self, net, states, num_reanalyze=5):
        reanalyzed_values = []

        latent = net.encode(states[0])
        for t in range(len(states)):
            _, value, _, latent = net.recurrent_inference(
                latent, actions[t]
            )
            reanalyzed_values.append(value)

        # Use new values as targets
        return reanalyzed_values
```

#### B. Model-based imagination

```python
def imagine_rollout(net, initial_latent, policy, horizon=10):
    """
    Imagined trajectory using learned model
    """
    latent = initial_latent
    imagined_states = []
    imagined_rewards = []

    for t in range(horizon):
        policy_logits, value = net.predict(latent)
        action = sample_from_policy(policy_logits, policy[t])

        next_latent, reward = net.dynamics(latent, action)

        imagined_states.append(latent)
        imagined_rewards.append(reward)

        latent = next_latent

    return imagined_states, imagined_rewards
```

#### C. Opponent modeling in dynamics

```python
class OpponentAwareDynamics(nn.Module):
    """
    Dynamics that considers opponent actions
    """
    def forward(self, latent, my_action, opponent_action, opponent_latent):
        combined = torch.cat([
            latent,
            my_action_embed,
            opponent_action_embed,
            opponent_latent,
        ], dim=-1)
        # ...
```

### 9.3 Low Priority

#### A. Distributed training (SEED RL style)
#### B. Learned latent space visualization
#### C. Model predictive control (MPC) on learned model
#### D. Model-based RL with uncertainty

---

## 10. Testing

### 10.1 Unit tests

```python
def test_gumbel_muzero_encode():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    obs = torch.randn(32, 100)
    latent = net.encode(obs)
    assert latent.shape == (32, 256)
    # Latent should be normalized (mean~0, std~1)
    assert abs(latent.mean()) < 0.1
    assert abs(latent.std() - 1.0) < 0.1

def test_gumbel_muzero_dynamics():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    latent = torch.randn(4, 256)
    actions = torch.randint(0, 5, (4, 2))

    next_latent, reward = net.dynamics(latent, actions)

    assert next_latent.shape == (4, 256)
    assert reward.shape == (4,)
    # Next latent should be normalized
    assert abs(next_latent.mean()) < 0.2

def test_gumbel_muzero_initial_inference():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    obs = torch.randn(4, 100)

    logits, value, reward, latent = net.initial_inference(obs)

    assert len(logits) == 2
    assert value.shape == (4,)
    assert reward.shape == (4,)
    assert abs(reward).max() < 1e-6  # should be zero
    assert value.min() >= -1.0 and value.max() <= 1.0

def test_gumbel_muzero_recurrent_inference():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    latent = torch.randn(4, 256)
    actions = torch.randint(0, 5, (4, 2))

    logits, value, reward, next_latent = net.recurrent_inference(
        latent, actions
    )

    assert len(logits) == 2
    assert value.shape == (4,)
    assert reward.shape == (4,)
    assert next_latent.shape == (4, 256)

def test_unroll_training():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    optimizer = optim.Adam(net.parameters(), lr=1e-3)

    # Simulate unroll
    obs0 = torch.randn(1, 100)
    actions = [torch.tensor([[1, 0]]), torch.tensor([[2, 1]]), torch.tensor([[0, 2]])]
    rewards = [0.5, 0.3, 0.8]
    policies = [[torch.softmax(torch.randn(5), dim=-1), torch.softmax(torch.randn(3), dim=-1)]
                for _ in range(4)]

    latent = net.encode(obs0)
    policy_loss = 0
    value_loss = 0
    reward_loss = 0

    for t in range(3):
        logits, value, reward, latent = net.recurrent_inference(
            latent, actions[t]
        )
        # Compute losses (simplified)
        policy_loss = policy_loss + sum(F.cross_entropy(l, p) for l, p in zip(logits, policies[t]))
        value_loss = value_loss + F.mse_loss(value, torch.tensor(0.5))
        reward_loss = reward_loss + F.mse_loss(reward, torch.tensor(rewards[t]))

    loss = policy_loss + value_loss + reward_loss
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    assert loss.item() > 0
```

### 10.2 Integration tests

```python
def test_gumbel_muzero_search():
    net = GumbelMuZeroNet(obs_dim=100, action_sizes=[5, 3])
    search = GumbelMuZeroSearch(net, GumbelMuZeroSearchConfig())

    obs = np.random.randn(100).astype(np.float32)
    masks = [np.ones(5, dtype=bool), np.ones(3, dtype=bool)]

    policy, actions, value = search.run(obs=obs, legal_masks_by_head=masks)

    assert len(policy) == 2
    assert len(actions) == 2
    assert abs(value) <= 1.0

def test_replay_buffer_unroll():
    buffer = GumbelMuZeroReplayBuffer(capacity=1000)

    # Add transitions
    for i in range(100):
        buffer.push(GMZTransition(
            state=np.random.randn(100),
            action=np.array([1, 0]),
            reward=0.1 * i,
            done=i == 99,
            policy_targets=[np.random.rand(5), np.random.rand(3)],
            value_target=0.5,
        ))

    # Sample unroll
    samples = buffer.sample_unroll(batch_size=10, unroll_steps=5)

    for sample in samples:
        assert len(sample['states']) == 5
        assert len(sample['actions']) == 5
        assert len(sample['rewards']) == 4  # rewards are between states
```

---

## 11. Comparison with AlphaZero

| Aspect | AlphaZero | GumbelMuZero |
|--------|-----------|--------------|
| Model | None (real env) | Learned (obs→latent→dynamics) |
| Planning | MCTS on real states | Gumbel search on latent |
| Reward prediction | Implicit (MCTS value) | Explicit (dynamics head) |
| Environment cost | High (full sim) | Low (model inference) |
| Model errors | None | Accumulate over unroll |
| Transfer | N/A | Good (model reusable) |
| Hyperparameters | c_puct, sims | discount, unroll_steps |
| Training | Supervised on MCTS | Model-based RL |

---

## 12. Summary

| Aspect | Current | Recommended |
|--------|---------|-------------|
| Representation | Simple MLP | Residual MLP + Attention |
| Dynamics | Simple MLP | GRU + Residual |
| Reward head | Linear | MLP with hidden layers |
| Latent norm | Batch norm | LayerNorm or running stats |
| Action embed | Simple lookup | Structured embeddings |
| Search | Round-robin | Proper Gumbel-UCB |
| Prior mixing | None | Weighted mixture |
| Unroll | 5 steps | 5-10 adaptive |
| Discount | 0.997 | 0.997 (good) |
| Simulations | 32 | 64-128 |
| Reanalyze | None | MuZero-style |

---

*Дата: 2026-05-22*
*Файл: `docs/model_analysis_GumbelMuZero.md`*