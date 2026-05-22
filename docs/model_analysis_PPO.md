# PPO (Proximal Policy Optimization) — Детальный анализ

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
        └── value_head: Linear(256, 1)
            ↓
        [policy_logits_per_head], value
```

### 1.2 Компоненты

#### Encoder (feature extractor)
```python
class ActorCriticMultiHead(nn.Module):
    def __init__(self, n_observations, n_actions, hidden_size=256):
        super().__init__()
        self.action_sizes = [int(x) for x in n_actions]
        self.layer1 = nn.Linear(n_observations, hidden_size)
        self.layer2 = nn.Linear(hidden_size, hidden_size)
        self.policy_heads = nn.ModuleList([
            nn.Linear(hidden_size, size) for size in self.action_sizes
        ])
        self.value_head = nn.Linear(hidden_size, 1)
```

**Проблемы:**
- `hidden_size` захардкожен = 256
- Нет Residual connections
- Нет нормализации (LayerNorm/BatchNorm)
- Те же 2 слоя, что и в DQN — нет общей абстракции

#### Policy Heads (Multi-head)
```python
# Discrete policy: Categorical distribution
logits = [head(x) for head in self.policy_heads]
dist = Categorical(logits=logits)
action = dist.sample()
log_prob = dist.log_prob(action)
entropy = dist.entropy()
```

**Архитектура: Factorized policy**
- Каждая голова отвечает за независимое action sub-space
- Это соответствует структуре 40k actions (move, attack, shoot, charge, etc.)
- Преимущество: декомпозиция сложной задачи на подзадачи

**Проблемы:**
- Нет shared policy trunk — каждая голова имеет отдельный Linear
- Это ограничивает transfer learning между action types
- Можно использовать hierarchical policy с shared trunk

#### Value Head
```python
value = self.value_head(x).squeeze(-1)  # shape: [batch]
```

**Проблемы:**
- Single linear layer — нет separate value network
- Нет value variance output (uncertainty)
- Value prediction для 40k state space сложнее чем policy

### 1.3 Action Masking

```python
def _apply_action_mask(logits: torch.Tensor, mask: torch.Tensor | None) -> torch.Tensor:
    if mask is None:
        return logits
    mask = mask.to(dtype=torch.bool)
    valid_any = mask.any(dim=1, keepdim=True)
    safe_mask = torch.where(valid_any, mask, torch.ones_like(mask, dtype=torch.bool))
    masked_logits = logits.masked_fill(~safe_mask, -1e9)
    return masked_logits
```

**Проблемы:**
- `-1e9` фиксирован — можно использовать `-inf` для numerical stability
- `safe_mask` fallback на `ones_like` — создаёт uniform distribution

### 1.4 Forward methods

#### evaluate_actions
```python
def evaluate_actions(self, obs, actions, masks_by_head=None):
    logits_list, values = self.forward(obs)

    total_logprob = torch.zeros(obs.shape[0])
    total_entropy = torch.zeros(obs.shape[0])

    for idx, logits in enumerate(logits_list):
        mask = masks_by_head[idx] if masks_by_head else None
        logits = _apply_action_mask(logits, mask)
        dist = Categorical(logits=logits)

        head_actions = actions[:, idx]
        total_logprob = total_logprob + dist.log_prob(head_actions)
        total_entropy = total_entropy + dist.entropy()

    return total_logprob, total_entropy, values
```

**Проблемы:**
- Entropy возвращается, но не используется в loss напрямую
- PPO обычно использует `entropy_coef * entropy` в loss
- Нет separate entropy coefficient scheduling

#### act
```python
@torch.no_grad()
def act(self, obs, masks_by_head=None, deterministic=False):
    logits_list, values = self.forward(obs)

    actions = []
    total_logprob = torch.zeros(obs.shape[0])

    for idx, logits in enumerate(logits_list):
        mask = masks_by_head[idx] if masks_by_head else None
        logits = _apply_action_mask(logits, mask)
        dist = Categorical(logits=logits)

        if deterministic:
            head_actions = logits.argmax(dim=1)
        else:
            head_actions = dist.sample()
        total_logprob = total_logprob + dist.log_prob(head_actions)
        actions.append(head_actions)

    stacked_actions = torch.stack(actions, dim=1)
    return stacked_actions, total_logprob, values
```

**Проблемы:**
- `deterministic=True` используется для evaluation — нет temperature
- Нет separate evaluation method
- Action stacking может быть неэффективен для variable number of heads

---

## 2. Rollout Buffer (PPORolloutBuffer)

### 2.1 Структура буфера

```python
class PPORolloutBuffer:
    def __init__(self):
        self.obs = []          # List[np.ndarray]
        self.actions = []     # List[np.ndarray]
        self.logprobs = []    # List[float]
        self.rewards = []     # List[float]
        self.dones = []       # List[bool]
        self.values = []      # List[float]
        self.masks_by_head = [] # List[list[torch.Tensor]]
        self.env_ids = []     # List[int]
```

### 2.2 GAE Computation

```python
def compute_returns_and_advantages(self, gamma, gae_lambda):
    rewards = np.asarray(self.rewards, dtype=np.float32)
    dones = np.asarray(self.dones, dtype=np.float32)
    values = np.asarray(self.values, dtype=np.float32)
    env_ids = np.asarray(self.env_ids, dtype=np.int64)

    advantages = np.zeros_like(rewards, dtype=np.float32)
    last_gae_by_env = {}
    next_value_by_env = {}

    for t in reversed(range(len(rewards))):
        env_id = int(env_ids[t])

        if dones[t]:
            next_value = 0.0
            last_gae = 0.0
        else:
            next_value = float(next_value_by_env.get(env_id, 0.0))
            last_gae = float(last_gae_by_env.get(env_id, 0.0))

        non_terminal = 1.0 - dones[t]
        delta = rewards[t] + gamma * next_value * non_terminal - values[t]
        last_gae = delta + gamma * gae_lambda * non_terminal * last_gae

        advantages[t] = float(last_gae)
        last_gae_by_env[env_id] = float(last_gae)
        next_value_by_env[env_id] = float(values[t])

    returns = advantages + values
    return returns, advantages
```

**Проблемы:**
- GAE вычисляется в single loop — нет vectorization
- Для больших rollouts это может быть slow
- Можно vectorize с помощью torch operations

**Формула GAE(λ):**
```
δ_t = r_t + γ * V(s_{t+1}) - V(s_t)
A_t = δ_t + (γ * λ)^{1} * δ_{t+1} + (γ * λ)^{2} * δ_{t+2} + ...
    = Σ_{l=0}^{∞} (γ * λ)^{l} * δ_{t+l}
```

**Параметры:**
- γ (gamma) = 0.99 — discount factor
- λ (gae_lambda) = 0.95 — bias-variance tradeoff
  - λ = 0: high bias, low variance (TD(0))
  - λ = 1: low bias, high variance (MC)

### 2.3 Tensor conversion

```python
def to_tensors(self, device, gamma, gae_lambda, normalize_adv=True):
    returns, advantages = self.compute_returns_and_advantages(gamma, gae_lambda)

    if normalize_adv and len(advantages) > 1:
        adv_mean = advantages.mean()
        adv_std = advantages.std() + 1e-8
        advantages = (advantages - adv_mean) / adv_std

    obs_t = torch.tensor(...)
    actions_t = torch.tensor(...)
    logprobs_t = torch.tensor(...)
    returns_t = torch.tensor(...)
    adv_t = torch.tensor(advantages, ...)
    values_t = torch.tensor(...)
```

**Проблемы:**
- `torch.tensor()` копирует данные — нет reuse от numpy
- `normalize_adv` делает normalization по всему batch — это PPO standard, но можно делать per-env
- masks_by_head conversion неэффективен (stack per head)

---

## 3. Training Loop (PPO)

### 3.1 Hyperparameters (hyperparams.json)

```json
"ppo": {
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
    "target_kl": 0.03
}
```

### 3.2 PPO Loss

```python
def compute_ppo_loss(mb_obs, mb_actions, mb_old_logprobs, mb_returns, mb_advantages):
    # Forward pass
    new_logprobs, new_entropy, values = actor_critic.evaluate_actions(
        mb_obs, mb_actions, mb_masks_by_head
    )

    # Ratio for clipping
    ratio = torch.exp(new_logprobs - mb_old_logprobs)

    # Clipped objective
    surr1 = ratio * mb_advantages
    surr2 = torch.clamp(ratio, 1 - clip_ratio, 1 + clip_ratio) * mb_advantages
    policy_loss = -torch.min(surr1, surr2).mean()

    # Value loss (clipped)
    values_clipped = mb_old_values + torch.clamp(
        values - mb_old_values,
        -clip_ratio,
        clip_ratio
    )
    value_loss1 = (values - mb_returns).pow(2)
    value_loss2 = (values_clipped - mb_returns).pow(2)
    value_loss = torch.max(value_loss1, value_loss2).mean()

    # Entropy bonus
    entropy_loss = -new_entropy.mean()

    # Total loss
    loss = policy_loss + value_coef * value_loss + entropy_coef * entropy_loss

    # Gradient clipping
    torch.nn.utils.clip_grad_norm_(actor_critic.parameters(), max_grad_norm)
```

### 3.3 PPO Update Loop

```python
for epoch in range(update_epochs):
    for minibatch in minibatches:
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(actor_critic.parameters(), max_grad_norm)
        optimizer.step()

        # Compute KL for early stopping
        approx_kl = (mb_old_logprobs - new_logprobs).mean()
        if target_kl is not None and approx_kl > target_kl:
            break  # early stopping
```

### 3.4 KL Divergence Tracking

```python
# Approximate KL (from Schulman et al.)
approx_kl = (mb_old_logp - new_logp).mean().detach()

# Exact KL (expensive, not used)
# exact_kl = F.kl_div(old_logp, new_logp, reduction='batchmean').exp()
```

**KL-based early stopping:**
- `target_kl = 0.03` — если KL > target, прекращаем epoch
- Это предотвращает too large policy updates
- Standard в Stable-Baselines3

### 3.5 Clip Fraction Tracking

```python
# Fraction of clips
clip_frac = torch.mean(
    torch.abs(torch.clamp(ratio, 1 - clip_ratio, 1 + clip_ratio) - ratio) > 1e-6
)

# Track: если clip_frac > 0.3, policy слишком быстро меняется
# Если clip_frac < 0.01, policy не обновляется (learning rate too low)
```

---

## 4. Варианты реализации PPO

### 4.1 Standard PPO (Clipped)

```python
# Current implementation
L^{CLIP} = min(r_t * A_t, clip(r_t, 1-ε, 1+ε) * A_t)
```

**Преимущества:**
- Simple to implement
- Proven stable
- Industry standard

**Недостатки:**
- Clipping can lead to policy collapse if A_t has same sign
- Doesn't use trusted region explicitly

### 4.2 PPO with Adaptive KL (TRPO-like)

```python
# KL penalty variant
L^{KL} = L^{CLIP} - β * KL[π_old || π_new]

# Adaptive β:
if kl > target_kl * 2:
    β *= 2  # increase penalty
elif kl < target_kl / 2:
    β *= 0.5  # decrease penalty
```

### 4.3 PPO with Value Function Clipping

```python
# Current: value clipping in loss computation
value_loss = torch.max(
    (values - returns).pow(2),
    (values_clipped - returns).pow(2)
).mean()

# Alternative: soft value baseline
value_loss = F.mse_loss(values, returns)  # no clipping
value_loss = value_loss + 0.01 * (values - values.detach()).pow(2).mean()  # variance regularization
```

### 4.4 PPO-X (Multi-objective)

```python
# For different action types with different scales
for head_idx in range(num_heads):
    head_logp = logp[:, head_idx]
    head_adv = advantages / head_scales[head_idx]  # normalize per head
    head_loss = -min(ratio * head_adv, clip(ratio) * head_adv)
```

---

## 5. Vectorized Environments

### 5.1 Current implementation (train.py)

```python
# Multiple environments in parallel
vec_env_count = 8  # или больше
vec_env = make_vec_env('WarhammerEnv-v0', vec_env_count, seed=seed)

# Rollout
obs = vec_env.reset()
for step in range(rollout_steps):
    actions, logprobs, values = actor_critic.act(obs)
    next_obs, rewards, dones, infos = vec_env.step(actions)

    buffer.add_batch(obs, actions, logprobs, rewards, dones, values, masks, env_ids)
    obs = next_obs

    for env_id, done in enumerate(dones):
        if done:
            buffer.env_episode_done(env_id)
            obs[env_id] = vec_env.reset(env_id=env_id)[0]
```

### 5.2 GAE in vectorized setting

```python
# Per-environment tracking
env_ids = np.arange(num_envs)
for t in reversed(range(rollout_steps)):
    for env_id in range(num_envs):
        if dones[t, env_id]:
            advantages[t, env_id] = 0.0
            last_gae[env_id] = 0.0
        else:
            delta = rewards[t, env_id] + gamma * next_value[env_id] - values[t, env_id]
            last_gae[env_id] = delta + gamma * gae_lambda * last_gae[env_id]
            advantages[t, env_id] = last_gae[env_id]
```

### 5.3 Batch processing

```python
# Current: sequential per-step
for step in range(rollout_steps):
    with torch.no_grad():
        actions, _, values = actor_critic.act(obs)

# Improved: batch all environments
with torch.no_grad():
    actions, _, values = actor_critic.act(obs.reshape(-1, obs_dim))
    actions = actions.reshape(num_envs, -1, num_heads)
```

---

## 6. Actor-Learner Architecture

### 6.1 Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Actor 1   │     │   Actor 2   │ ... │   Actor N   │
│  (CPU/env)  │     │  (CPU/env)  │     │  (CPU/env)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ batch of rollouts
                           ▼
                   ┌─────────────┐
                   │   Queue     │
                   │ (MP Queue)  │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │   Learner   │
                   │ (GPU/train) │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │  Sync File  │
                   │ (weights)   │
                   └──────┬──────┘
                          │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Actor 1   │     │   Actor 2   │ ... │   Actor N   │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 6.2 Implementation details

```python
# Actor process
def actor_process(queue, sync_path, env_factory, num_envs):
    actor_critic = ActorCriticMultiHead(...)
    while True:
        # Load latest weights
        if os.path.exists(sync_path):
            checkpoint = torch.load(sync_path)
            actor_critic.load_state_dict(checkpoint['state_dict'])

        # Collect rollouts
        buffer = PPORolloutBuffer()
        obs = env_factory.reset()
        for step in range(rollout_steps):
            actions, logprobs, values = actor_critic.act(obs)
            next_obs, rewards, dones, infos = env.step(actions)
            buffer.add_batch(...)
            obs = next_obs

        # Send to queue
        batch = buffer.to_tensors(device='cpu')
        queue.put(batch)
```

```python
# Learner process
def learner_process(queue, num_actors):
    actor_critic = ActorCriticMultiHead(...).to(device)
    optimizer = optim.Adam(actor_critic.parameters(), lr=PPO_LR)

    while True:
        # Collect batches from all actors
        batches = []
        for _ in range(num_actors):
            batches.append(queue.get())

        # Concatenate
        obs = torch.cat([b.obs for b in batches])
        actions = torch.cat([b.actions for b in batches])
        ...

        # Update
        for epoch in range(update_epochs):
            for minibatch in minibatches:
                loss = compute_ppo_loss(...)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # Sync weights
        torch.save({'state_dict': actor_critic.state_dict()}, sync_path)
```

### 6.3 Проблемы current implementation

1. **MP Queue overhead** — multiprocessing queue имеет serialization overhead
2. **No priority queue** — все actors equal priority
3. **Sync file I/O** — запись в файл каждые N updates может быть узким местом
4. **No async training** — learner ждёт пока actors собирают данные

---

## 7. Улучшения

### 7.1 Architecture improvements

#### Shared policy trunk
```python
class ActorCriticSharedTrunk(nn.Module):
    def __init__(self, n_observations, n_actions, hidden_size=256):
        super().__init__()
        # Shared trunk
        self.trunk = nn.Sequential(
            nn.Linear(n_observations, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
        )

        # Shared policy representation
        self.policy_trunk = nn.Linear(hidden_size, hidden_size)

        # Per-head policy
        self.policy_heads = nn.ModuleList([...])

        # Separate value network (optional)
        self.value_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, 1)
        )
```

#### Multi-head attention for policy
```python
class MultiHeadAttentionPolicy(nn.Module):
    def __init__(self, hidden_size, num_heads, num_action_types):
        super().__init__()
        self.query = nn.Linear(hidden_size, hidden_size)
        self.key = nn.Linear(hidden_size, hidden_size)
        self.value = nn.Linear(hidden_size, hidden_size)
        self.num_heads = num_heads

        self.action_heads = nn.ModuleList([
            nn.Linear(hidden_size, action_size)
            for action_size in action_sizes
        ])

    def forward(self, x):
        # Multi-head attention
        Q = self.query(x).reshape(-1, self.num_heads, self.hidden_size // self.num_heads)
        K = self.key(x).reshape(-1, self.num_heads, self.hidden_size // self.num_heads)
        V = self.value(x).reshape(-1, self.num_heads, self.hidden_size // self.num_heads)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / sqrt(d)
        attn = F.softmax(scores, dim=-1)
        context = torch.matmul(attn, V).reshape(-1, self.hidden_size)

        # Action heads
        logits = [head(context) for head in self.action_heads]
        return logits
```

### 7.2 Buffer improvements

#### Vectorized GAE
```python
def compute_returns_vectorized(self, gamma, gae_lambda):
    rewards = torch.tensor(self.rewards, dtype=torch.float32)
    dones = torch.tensor(self.dones, dtype=torch.float32)
    values = torch.tensor(self.values, dtype=torch.float32)

    T = len(rewards)
    advantages = torch.zeros(T, dtype=torch.float32)

    gae = 0.0
    for t in reversed(range(T)):
        non_terminal = 1.0 - dones[t]
        delta = rewards[t] + gamma * values[t + 1] * non_terminal - values[t]
        gae = delta + gamma * gae_lambda * non_terminal * gae
        advantages[t] = gae

    returns = advantages + values
    return returns, advantages
```

### 7.3 Training improvements

#### Adaptive entropy coefficient
```python
def update_entropy_coef(entropy, target_entropy, lr=1e-3):
    """
    Adaptive entropy for automatic entropy bonus adjustment
    """
    current_coef = entropy_coef
    target_coef = target_entropy / (entropy + 1e-8)
    new_coef = current_coef + lr * (target_coef - current_coef)
    return new_coef.clamp(0.0, 1.0)
```

#### Learning rate scheduling
```python
# Linear warmup + decay
warmup_steps = 5000
total_steps = 100000

if step < warmup_steps:
    lr = initial_lr * step / warmup_steps
else:
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    lr = initial_lr * (1 - progress)
```

### 7.4 Advanced PPO variants

#### PPO with GAE-RT (Generalized Advantage Estimator with Return Targeting)
```python
# Use n-step returns for advantage
def compute_gae_rt(rewards, values, gamma, lambda_, n=5):
    T = len(rewards)
    advantages = torch.zeros(T)

    for t in range(T):
        ret = 0.0
        for k in range(t, min(t + n, T)):
            ret += gamma ** (k - t) * rewards[k]
        advantages[t] = ret - values[t]

    return advantages
```

#### PPO with Value Function Ensemble
```python
class EnsembleValueHead(nn.Module):
    def __init__(self, hidden_size, num_ensemble=5):
        super().__init__()
        self.heads = nn.ModuleList([
            nn.Linear(hidden_size, 1) for _ in range(num_ensemble)
        ])

    def forward(self, x):
        values = torch.stack([head(x) for head in self.heads])
        mean = values.mean(dim=0)
        std = values.std(dim=0)
        return mean.squeeze(-1), std.squeeze(-1)
```

---

## 8. Configuration deep-dive

### 8.1 Learning rate

**Current:** `lr = 0.0003`

**Analysis:**
- 0.0003 — standard PPO learning rate (Stable-Baselines3 default)
- Для 40k state space с большим action space можно попробовать:
  - Lower: 0.0001 (more stable, slower)
  - Higher: 0.0005 (faster, but risky)

### 8.2 Clip ratio

**Current:** `clip_ratio = 0.2`

**Analysis:**
- 0.2 — standard (Schulman et al.)
- Smaller (0.1): more conservative, slower learning
- Larger (0.3): faster learning, risk of collapse

### 8.3 GAE lambda

**Current:** `gae_lambda = 0.95`

**Analysis:**
- 0.95 — good balance
- Для коротких эпизодов: 0.9
- Для длинных эпизодов: 0.99

### 8.4 Entropy coefficient

**Current:** `entropy_coef = 0.01`

**Analysis:**
- 0.01 — standard
- Auto-entropy: dynamically adjust based on entropy target
- Higher (0.05): more exploration
- Lower (0.001): more exploitation

### 8.5 Value coefficient

**Current:** `value_coef = 0.5`

**Analysis:**
- 0.5 — standard (PPO paper uses 1.0)
- Для 40k state space, value prediction сложнее:
  - Можно сделать 1.0
  - Или adaptive: уменьшать когда value loss стабилен

---

## 9. Testing

### 9.1 Unit tests

```python
def test_ppo_forward():
    net = ActorCriticMultiHead(n_observations=100, n_actions=[5, 3, 10])
    x = torch.randn(32, 100)
    logits, value = net(x)
    assert len(logits) == 3
    assert value.shape == (32,)

def test_ppo_masking():
    net = ActorCriticMultiHead(n_observations=100, n_actions=[5])
    x = torch.randn(32, 100)
    mask = torch.zeros(32, 5, dtype=torch.bool)
    mask[:, 2] = True
    actions, logp, val = net.act(x, masks_by_head=[mask])
    assert actions.shape == (1, 1)  # single batch
    assert actions[0, 0].item() == 2

def test_ppo_buffer_gae():
    buffer = PPORolloutBuffer()
    gamma = 0.99
    gae_lambda = 0.95

    # Simple trajectory: no discount
    buffer.add(obs=[1.0], action=[0], logprob=0.0, reward=1.0, done=False, value=0.0, masks_by_head=[None])
    buffer.add(obs=[1.0], action=[0], logprob=0.0, reward=1.0, done=True, value=0.0, masks_by_head=[None])

    returns, advantages = buffer.compute_returns_and_advantages(gamma, gae_lambda)

    # With done=True at t=1: advantage at t=1 = 0
    # advantage at t=0 = reward + gamma * 0 - value = 1.0
    assert advantages[1] == 0.0
    assert abs(advantages[0] - 1.0) < 1e-5
```

### 9.2 Integration tests

```python
def test_ppo_training_loop():
    net = ActorCriticMultiHead(n_observations=100, n_actions=[5, 3])
    optimizer = optim.Adam(net.parameters(), lr=1e-3)
    buffer = PPORolloutBuffer()

    # Collect random rollouts
    for _ in range(100):
        obs = torch.randn(100)
        action = torch.randint(0, 5, (1,))
        logprob = torch.tensor(0.0)
        reward = torch.randn(1)
        done = random.random() < 0.1
        value = torch.tensor(0.0)
        buffer.add(obs, action, logprob, reward, done, value, [None])

    # Training step
    batch = buffer.to_tensors(device='cpu', gamma=0.99, gae_lambda=0.95)

    for _ in range(4):
        optimizer.zero_grad()
        new_logp, entropy, values = net.evaluate_actions(batch.obs, batch.actions)
        ratio = torch.exp(new_logp - batch.logprobs)
        surr1 = ratio * batch.advantages
        surr2 = torch.clamp(ratio, 1 - 0.2, 1 + 0.2) * batch.advantages
        loss = -torch.min(surr1, surr2).mean()
        loss.backward()
        optimizer.step()
```

---

## 10. Summary

| Aspect | Current | Recommended |
|--------|---------|-------------|
| Architecture | 2-layer MLP | Residual + LayerNorm |
| Policy | Independent heads | Shared trunk + attention |
| Value head | Single linear | Multi-layer with ensemble |
| Buffer | List-based | Vectorized tensors |
| GAE | Sequential loop | Vectorized |
| Entropy coef | Fixed (0.01) | Adaptive scheduling |
| Value coef | 0.5 | 0.5-1.0 adaptive |
| Learning rate | 0.0003 | Warmup + decay |
| Actor-Learner | MP Queue | Shared memory + Lock-free |
| Testing | Minimal | Comprehensive + benchmarks |

---

*Дата: 2026-05-22*
*Файл: `docs/model_analysis_PPO.md`*