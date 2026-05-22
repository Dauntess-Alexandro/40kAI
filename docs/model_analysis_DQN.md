# DQN (Deep Q-Network) — Детальный анализ

## 1. Архитектура сети

### 1.1 Общая структура

```
Input (n_observations) 
    → layer1: Linear(n_observations, 256)
    → ReLU
    → layer2: Linear(256, 256)
    → ReLU
    → Feature vector (256)
        ├── Dueling: value_heads + advantage_heads (per action head)
        ├── Distributional (C51): atoms × action_heads
        └── IQN: quantile-based Q-values (per action head)
```

### 1.2 Компоненты

#### Encoder (feature extractor)
```python
self.layer1 = layer_cls(n_observations, self.hidden_size, **layer_kwargs)
self.layer2 = layer_cls(self.hidden_size, self.hidden_size, **layer_kwargs)
```

**Проблемы:**
- `hidden_size` захардкожен = 256 (строка 83)
- Нет параметра для настройки в конструкторе
- Только 2 слоя без residual connections
- Нет нормализации (LayerNorm/BatchNorm)

#### Dueling Heads
```python
self.value_heads = nn.ModuleList([layer_cls(self.hidden_size, 1) for _ in self.action_sizes])
self.advantage_heads = nn.ModuleList([layer_cls(self.hidden_size, size) for size in self.action_sizes])
```

Формула: `Q(s,a) = V(s) + A(s,a) - mean(A(s,·))`

**Преимущества:**
- Разделение state value и action advantage
- Лучшая оценка state value
- Стандартная техника в modern DQN

**Проблемы:**
- `mean` reduction может терять информацию о dispersion advantage
- Можно использовать `max` вместо `mean` для sparsity

#### NoisyLinear слои
```python
class NoisyLinear(nn.Module):
    # mu: learnable mean weights
    self.weight_mu = nn.Parameter(torch.empty(out, in))
    self.weight_sigma = nn.Parameter(torch.empty(out, in))
    # sigma: learnable variance
    self.bias_mu = nn.Parameter(torch.empty(out))
    self.bias_sigma = nn.Parameter(torch.empty(out))
```

**Формула forward:**
```python
weight = weight_mu + weight_sigma * weight_epsilon
bias = bias_mu + bias_sigma * bias_epsilon
output = F.linear(x, weight, bias)
```

**Генерация шума (NoisyNet technique):**
```python
def _scale_noise(self, size):
    x = torch.randn(size, device=self.device)
    return x.sign().mul_(x.abs().sqrt_())
# ε_w = f(ε_i) · f(ε_j) где f — signed sqrt of |ε|
```

**Проблемы:**
- Noise генерируется только при reset_noise()
- При resume checkpoint нужно вызывать reset_noise() вручную
- Нет отдельной функции для инициализации sigma

### 1.3 Distributional RL компоненты

#### C51 (Categorical 51 atoms)
```python
self.register_buffer("support", torch.linspace(self.v_min, self.v_max, self.num_atoms))
# support = [-10.0, ..., +10.0] с num_atoms=51
```

**Forward:**
```python
logits = value_logits + (adv_logits - adv_logits.mean(dim=1, keepdim=True))
# Project to atoms: reshape to (batch, action, atoms)
probs = softmax(logits, dim=-1)
q_values = (probs * support).sum(dim=-1)
```

**Проблемы:**
- Hardcoded v_min=-10, v_max=+10
- Fixed number of atoms (51) без tuning
- projection loss требует额外 kl divergence

#### IQN (Implicit Quantile Networks)
```python
self.iqn_tau_fc = nn.Linear(self.iqn_embed_dim, self.hidden_size)
self.register_buffer("iqn_pi_multipliers", torch.arange(1, iqn_embed_dim+1))
```

**Embedding тау:**
```python
cos_in = taus * pi * iqn_pi_multipliers  # [B, Nq, 1] × [1, 1, embed_dim]
tau_embed = F.relu(self.iqn_tau_fc(torch.cos(cos_in)))  # [B, Nq, hidden]
```

**Проблемы:**
- Cosine embedding — нестандартный подход (обычно используют MLP)
- `iqn_embed_dim` должно быть привязано к `hidden_size` для consistency
- Нет layer normalization после tau embedding

**Улучшенная версия:**
```python
# Стандартный IQN использует:
phi(tau) = F.relu(W * cos(pi * tau * i) + b) для i = 1..embed_dim

# Текущий код (проблема):
cos_in = taus * self.iqn_pi_multipliers * math.pi  # умножение на pi перед cos
tau_embed = F.relu(self.iqn_tau_fc(torch.cos(cos_in)))

# Проблема: нет bias в cos_in, нет разумного масштабирования
```

### 1.4 Action Masking

```python
def infer(self, obs, masks_by_head):
    logits, value = self.forward(obs)
    probs = []
    for idx, head_logits in enumerate(logits):
        if masks_by_head is not None:
            mask = masks_by_head[idx]
            if mask is not None:
                safe_mask = torch.where(mask.any(), mask, torch.ones_like(mask))
                masked = head_logits.masked_fill(~safe_mask, -1e9)
        probs.append(torch.softmax(masked, dim=1))
    return probs, value
```

**Проблема:** `mask.any()` проверяет, есть ли хотя бы один валидный action. Если ВСЕ actions замаскированы, используется `torch.ones_like(mask)` — это fallback, но он может дать uniform distribution поверх всех элементов.

**Edge case:** Если `mask.shape != head_logits.shape` — маска не применяется вообще. Нет warning/error.

---

## 2. Процесс обучения (DQN)

### 2.1 Training loop (train.py)

```python
# Основной цикл
gamma = 0.99
tau = 0.01  # soft update
epsilon = 1.0 → 0.05 (exponential decay)

for step in range(total_steps):
    # 1. Collect experience
    action = select_action_with_epsilon(env, state, policy_net, epsilon, ...)
    next_state, reward, done, _ = env.step(action)
    memory.push(state, action, reward, next_state, done)
    state = next_state

    # 2. Update
    if len(memory) > batch_size:
        batch = memory.sample(batch_size)
        loss = compute_dqn_loss(policy_net, target_net, batch, gamma)

        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy_net.parameters(), max_norm=10.0)
        optimizer.step()

    # 3. Soft update target network
    if step % target_update_freq == 0:
        for target_param, policy_param in zip(target_net.parameters(), policy_net.parameters()):
            target_param.data.copy_(tau * policy_param + (1 - tau) * target_param)
```

### 2.2 Loss computation

```python
# Double DQN (если ENABLE_DOUBLE_DQN):
with torch.no_grad():
    next_actions = policy_net(next_states).argmax(1)
    next_q = target_net(next_states).gather(1, next_actions.unsqueeze(1))

# Standard DQN:
next_q = target_net(next_states).max(1)[0]

# Loss:
current_q = policy_net(states).gather(1, actions)
loss = F.mse_loss(current_q, next_q * gamma + rewards * (1 - dones))
```

### 2.3 IQN Loss (Implicit Quantile Networks)

```python
def compute_iqn_loss(policy_net, target_net, batch, gamma):
    batch_size = states.shape[0]
    n_quantiles = policy_net.iqn_num_quantiles
    n_target = policy_net.iqn_num_target_quantiles
    kappa = 1.0  # Huber loss parameter

    # Sample taus for current network
    taus = torch.rand(batch_size, n_quantiles, 1)

    # Get quantile values
    quantiles_current = policy_net.iqn(states, num_quantiles=n_quantiles, taus=taus)
    with torch.no_grad():
        # Get target quantiles with fixed tau=0.5 (median)
        target_taus = torch.full((batch_size, 1, 1), 0.5)
        quantiles_target = target_net.iqn(next_states, num_quantiles=n_target, taus=target_taus)

    # Compute TD error
    td_errors = rewards.unsqueeze(1) + gamma * quantiles_target - quantiles_current
    huber_loss = torch.where(td_errors.abs() <= kappa,
                             0.5 * td_errors.pow(2),
                             kappa * (td_errors.abs() - 0.5 * kappa))

    # Quantile Huber loss
    tau_bars = torch.abs(taus - (td_errors < 0).float()) * huber_loss
    loss = tau_bars.mean()
```

**Проблемы текущей реализации:**
- Huber loss kappa фиксирован = 1.0
- Нет tuning параметра
- quantile_weight (taus) используется для взвешивания, но не для gradient scaling

### 2.4 PER (Prioritized Experience Replay)

```python
# В memory.py
class PrioritizedReplayBuffer:
    def __init__(self, capacity, alpha=0.55):
        self.alpha = alpha  # prioritization strength
        self.beta = 0.4    # importance sampling correction
        self.max_priority = 1.0

    def sample(self, batch_size):
        # Sample proportional to priority
        probs = self.priorities ** self.alpha
        probs /= probs.sum()

        indices = np.random.choice(len(self), batch_size, p=probs, replace=False)
        weights = (len(self) * probs[indices]) ** (-self.beta)
        weights /= weights.max()  # normalize

        return batch[indices], weights, indices
```

**Проблемы:**
- `max_priority` инициализируется = 1.0, но при добавлении нового элемента используется `max_priority`
- Beta linear annealing не реализован в самом буфере (делается в train.py)
- Sum-tree не используется — O(n) sampling вместо O(log n)

---

## 3. Exploration

### 3.1 Epsilon-greedy
```python
epsilon = eps_end + (eps_start - eps_end) * exp(-step / eps_decay)
# eps_start = 0.9, eps_end = 0.05, eps_decay = 30000
```

### 3.2 NoisyNet
```python
# В training mode:
if self.training:
    weight = weight_mu + weight_sigma * weight_epsilon
else:
    weight = weight_mu  # deterministic
```

**Проблемы:**
- NoisyNet работает ТОЛЬКО в training mode
- При evaluation нужно явно выставлять `net.eval()`
- Noise не адаптивный — фиксированный sigma0

### 3.3 Рекомендации по exploration

1. **Epsilon decay schedule:**
   - Linear: `epsilon = max(eps_end, eps_start - step * decay_rate)`
   - Polynomial: `epsilon = (1 - step / total_steps) ** power`
   - Inverse sigmoid: `epsilon = eps_end + (eps_start - eps_end) * sig(-step)`

2. **NoisyNet improvements:**
   - Adaptive sigma: увеличивать sigma при высоком loss
   - Separate sigma для разных слоёв
   - Spectral normalization на весах

3. **Entropy bonus:**
   ```python
   entropy_coef = 0.01
   entropy = -torch.sum(softmax(q_values) * log(q_values), dim=-1).mean()
   loss = td_loss - entropy_coef * entropy
   ```

---

## 4. Configuration parameters

```json
{
    "lr": 0.0001,
    "tau": 0.01,
    "eps_start": 0.9,
    "eps_end": 0.05,
    "eps_decay": 30000,
    "batch_size": 384,
    "gamma": 0.99,
    "updates_per_step": 6,
    "warmup_steps": 5000,
    "dueling": true,
    "noisy": true,
    "distributional": "iqn",
    "num_atoms": 51,
    "v_min": -10.0,
    "v_max": 10.0,
    "iqn_num_quantiles": 32,
    "iqn_num_target_quantiles": 32,
    "iqn_num_tau_samples": 32,
    "iqn_embed_dim": 64,
    "iqn_kappa": 1.0
}
```

### Проблемы конфигурации:

1. **batch_size = 384** — относительно большой для 40k state space
2. **updates_per_step = 6** — может быть агрессивно (6 gradient updates на 1 step)
3. **tau = 0.01** — standard soft update rate
4. **gamma = 0.99** — standard для эпизодов ~100-200 шагов

---

## 5. Улучшения (Roadmap)

### 5.1 High Priority

#### A. Residual connections
```python
class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim)
        self.fc2 = nn.Linear(dim, dim)
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)

    def forward(self, x):
        residual = x
        x = F.relu(self.norm1(self.fc1(x)))
        x = self.norm2(self.fc2(x))
        return F.relu(x + residual)
```

#### B. Layer normalization
```python
# После каждого слоя
self.layer1 = nn.Sequential(
    nn.Linear(n_observations, hidden_size),
    nn.LayerNorm(hidden_size),
    nn.ReLU()
)
```

#### C. Configurable hidden size
```python
def __init__(self, n_observations, n_actions, hidden_size=256, num_layers=3, ...):
    self.hidden_size = hidden_size
    self.num_layers = num_layers
```

### 5.2 Medium Priority

#### A. Rainbow extensions
- Multi-step returns (n-step)
- Distributional + NoisyNet + Dueling + PER (Rainbow)
- Q-Ensemble для uncertainty

#### B. Dreamer-style RSSM
```python
class RSSM:
    """
    Recurrent State Space Model
    - stochastic state: p(st | st-1, at-1)
    - deterministic state: ht = f(ht-1, st-1, at-1)
    - observation model: p(ot | st)
    - reward model: p(rt | st, at)
    """
```

### 5.3 Low Priority

#### A. Neural Architecture Search
#### B. Distillation from MuZero/AZ to DQN
#### C. Meta-learning (MAML, RL^2)

---

## 6. Тестирование

### 6.1 Unit tests

```python
def test_dqn_forward():
    net = DQN(n_observations=100, n_actions=[5, 3, 10], dueling=True, noisy=True)
    x = torch.randn(32, 100)
    q_vals = net(x)
    assert len(q_vals) == 3
    assert q_vals[0].shape == (32, 5)
    assert q_vals[1].shape == (32, 3)
    assert q_vals[2].shape == (32, 10)

def test_dqn_masking():
    net = DQN(n_observations=100, n_actions=[5], dueling=True)
    x = torch.randn(32, 100)
    mask = torch.zeros(32, 5, dtype=torch.bool)
    mask[:, 2] = True  # только action 2 валиден
    q_vals = net.q_values(x)
    probs, _ = net.infer(x, masks_by_head=[mask])
    # Валидация: probs[:, 2] должен быть ~1.0
    assert torch.allclose(probs[0][:, 2], torch.tensor(1.0), atol=1e-5)

def test_iqn():
    net = DQN(n_observations=100, n_actions=[5], distributional="iqn")
    x = torch.randn(32, 100)
    q_vals = net.q_values(x)
    assert q_vals[0].shape == (32, 5)

def test_noisy_linear():
    layer = NoisyLinear(10, 20)
    x = torch.randn(5, 10)
    # Training mode — должен быть стохастичный
    layer.train()
    out1 = layer(x)
    layer.reset_noise()
    out2 = layer(x)
    assert not torch.allclose(out1, out2)

    # Eval mode — детерминированный
    layer.eval()
    out3 = layer(x)
    out4 = layer(x)
    assert torch.allclose(out3, out4)
```

### 6.2 Integration tests

```python
def test_dqn_training_step():
    net = DQN(n_observations=100, n_actions=[5, 3])
    target_net = DQN(n_observations=100, n_actions=[5, 3])
    target_net.load_state_dict(net.state_dict())

    optimizer = optim.Adam(net.parameters(), lr=1e-3)
    memory = ReplayBuffer(capacity=1000)

    # Fill memory with random transitions
    for _ in range(100):
        state = torch.randn(100)
        action = torch.tensor([1, 0])
        reward = torch.randn(1)
        next_state = torch.randn(100)
        done = False
        memory.push(state, action, reward, next_state, done)

    # Training step
    loss_before = compute_dqn_loss(net, target_net, memory)
    optimizer.zero_grad()
    loss_before.backward()
    optimizer.step()

    # Verify loss changed
    loss_after = compute_dqn_loss(net, target_net, memory)
    assert loss_after != loss_before
```

---

## 7. Resume/Checkpoint

### 7.1 Current implementation

```python
def save_checkpoint(path, net, optimizer, step, epsilon):
    torch.save({
        'step': step,
        'model_state_dict': net.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'epsilon': epsilon,
    }, path)

def load_checkpoint(path, net, optimizer):
    checkpoint = torch.load(path)
    net.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    return checkpoint['step'], checkpoint['epsilon']
```

### 7.2 Проблемы

1. **NoisyNet state** — `weight_epsilon` буффер, он не сохраняется автоматически
   ```python
   # После load_state_dict нужно:
   for module in net.modules():
       if isinstance(module, NoisyLinear):
           module.reset_noise()
   ```

2. **Target network** — не сохраняется в checkpoint, пересоздаётся

3. **NoisyNet sigma tracking** — можно добавить annealing schedule

### 7.3 Improved checkpoint

```python
@dataclass
class DQNCheckpoint:
    step: int
    epsilon: float
    model_state_dict: dict
    optimizer_state_dict: dict
    target_net_state_dict: dict | None  # опционально
    noisy_state: dict | None  # сохранение epsilon buffers

    def save(self, path):
        data = {
            'step': self.step,
            'epsilon': self.epsilon,
            'model_state_dict': self.model_state_dict,
            'optimizer_state_dict': self.optimizer_state_dict,
        }
        if self.target_net_state_dict:
            data['target_net_state_dict'] = self.target_net_state_dict
        torch.save(data, path)

    @classmethod
    def load(cls, path, net, optimizer, target_net=None):
        data = torch.load(path)
        net.load_state_dict(data['model_state_dict'])
        optimizer.load_state_dict(data['optimizer_state_dict'])

        if target_net and 'target_net_state_dict' in data:
            target_net.load_state_dict(data['target_net_state_dict'])

        # Reset noisy layers
        for module in net.modules():
            if isinstance(module, NoisyLinear):
                module.reset_noise()

        return cls(
            step=data['step'],
            epsilon=data['epsilon'],
            model_state_dict=data['model_state_dict'],
            optimizer_state_dict=data['optimizer_state_dict'],
            target_net_state_dict=data.get('target_net_state_dict'),
        )
```

---

## 8. Summary

| Aspect | Current | Recommended |
|--------|---------|-------------|
| Hidden layers | 2 (hardcoded 256) | 3-4 (configurable) |
| Normalization | None | LayerNorm |
| Skip connections | None | Residual blocks |
| Distributional | IQN | IQN + Rainbow extensions |
| Exploration | Epsilon + Noisy | Adaptive schedule |
| PER | O(n) sampling | Sum-tree O(log n) |
| Checkpoint | Basic | Full state + noisy reset |
| Testing | Minimal | Comprehensive |

---

*Дата: 2026-05-22*
*Файл: `docs/model_analysis_DQN.md`*