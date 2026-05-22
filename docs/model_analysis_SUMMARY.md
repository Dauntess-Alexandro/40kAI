# Neural Network Models — Общий обзор

> **Документация:** Создано 2026-05-22
>
> **Связанные файлы:**
> - [model_analysis_DQN.md](model_analysis_DQN.md) — детальный анализ DQN
> - [model_analysis_PPO.md](model_analysis_PPO.md) — детальный анализ PPO
> - [model_analysis_AlphaZero.md](model_analysis_AlphaZero.md) — детальный анализ AlphaZero
> - [model_analysis_GumbelMuZero.md](model_analysis_GumbelMuZero.md) — детальный анализ GumbelMuZero

---

## Введение

Проект содержит **четыре нейросетевые модели** для обучения агентов в среде Warhammer 40k:

| Модель | Тип | Планирование | Модель среды |
|--------|-----|--------------|--------------|
| **DQN** | Value-based | Нет | Нет |
| **PPO** | Policy Gradient | Нет | Нет |
| **AlphaZero** | Tree Search | MCTS | Нет (реальная среда) |
| **GumbelMuZero** | Model-based RL | Gumbel Search | Есть (latent model) |

---

## 1. Архитектурные паттерны

### 1.1 Общая архитектура всех моделей

```
Input (observations)
    │
    ├────────────────────────────────────────────────────────────┐
    │                                                            │
    ▼                                                            ▼
┌──────────────────────┐                              ┌──────────────────────┐
│     Encoder/Trunk     │                              │    Policy Heads      │
│  (shared features)    │                              │  (factorized)        │
│                      │                              │                      │
│  DQN:  2x Linear(256)│                              │  move_head           │
│  PPO:  2x Linear(256)│                              │  attack_head         │
│  AZ:   2x Linear(256)│                              │  shoot_head          │
│  GMZ:  2x Linear(256)│                              │  charge_head         │
│          + ReLU       │                              │  ...                 │
│          + LayerNorm  │                              │                      │
│          + Residual   │                              └──────────────────────┘
│                      │
│          +           │                              ┌──────────────────────┐
│          │           │                              │     Value Head       │
│          │           │                              │                      │
│          ▼           │                              │  DQN: Q-values       │
│  ┌────────────────┐  │                              │  PPO: V(s)           │
│  │  Action Heads  │  │                              │  AZ:  V(s) ∈ [-1,1]  │
│  │  (factorized)   │  │                              │  GMZ: V(s) ∈ [-1,1]  │
│  └────────────────┘  │                              │                      │
│                      │                              └──────────────────────┘
└────────────────────────────────────────────────────────────┘
```

### 1.2 Проблемы общие для всех моделей

```python
# Проблема 1: Hardcoded hidden size
class BaseNet(nn.Module):
    hidden_size = 256  # захардкожен, нет параметра

# Решение:
def __init__(self, n_observations, n_actions, hidden_size=256, num_layers=3):
    self.hidden_size = hidden_size
    self.layers = nn.ModuleList([
        nn.Linear(n_observations if i == 0 else hidden_size, hidden_size)
        for i in range(num_layers)
    ])
```

```python
# Проблема 2: Нет нормализации
class BaseNet(nn.Module):
    # Current: только Linear + ReLU
    layer1 = nn.Linear(n_obs, 256)
    layer2 = nn.Linear(256, 256)

# Решение:
layer1 = nn.Sequential(
    nn.Linear(n_obs, 256),
    nn.LayerNorm(256),
    nn.ReLU()
)
```

```python
# Проблема 3: Нет residual connections
class BaseNet(nn.Module):
    # Current: sequential layers
    layer1 = nn.Linear(n_obs, 256)
    layer2 = nn.Linear(256, 256)

# Решение: Residual block
class ResidualBlock(nn.Module):
    def forward(self, x):
        residual = x
        x = self.layer1(x)
        x = F.relu(self.norm1(x))
        x = self.layer2(x)
        x = self.norm2(x)
        return F.relu(x + residual)
```

---

## 2. DQN (Deep Q-Network)

### 2.1 Архитектура

```
Input → layer1 → ReLU → layer2 → ReLU → Features
                                        │
                                        ├─── Dueling: value + advantage
                                        ├─── C51: distributional atoms
                                        └─── IQN: quantile regression
```

### 2.2 Особенности

- **Dueling DQN**: разделяет state value и action advantage
- **NoisyNet**: stochastic exploration (alternative к epsilon-greedy)
- **IQN (Implicit Quantile Networks)**: distributional RL с quantile regression
- **PER (Prioritized Experience Replay)**: приоритизация важных переходов

### 2.3 Гиперпараметры

```json
{
    "lr": 0.0001,
    "tau": 0.01,
    "gamma": 0.99,
    "batch_size": 384,
    "dueling": true,
    "noisy": true,
    "distributional": "iqn",
    "iqn_num_quantiles": 32
}
```

### 2.4 Когда использовать

| ✓ Хорошо | ✗ Плохо |
|---------|---------|
| Дискретные действия | Непрерывные действия |
| Простые state spaces | Визуальные state spaces |
| Быстрая тренировка | Долгие эпизоды |
| Стабильные reward signals | Sparse rewards |

### 2.5 Статус внедрения (код)

**Выполнено** — коммит `e29c4df0` (2026-05-22). Детали: [model_analysis_DQN.md](model_analysis_DQN.md).

- [x] `make_dqn` / `dqn_kwargs_from_env`, configurable `hidden_size`, `num_layers`
- [x] LayerNorm + ResidualBlock в trunk
- [x] Q-ensemble (`DQN_ENSEMBLE_SIZE`)
- [x] LR scheduler в checkpoint (`DQN_LR_SCHEDULER`)
- [x] Distill teacher→student, grid search tools, unit-тесты

---

## 3. PPO (Proximal Policy Optimization)

### 3.1 Архитектура

```
Input → layer1 → ReLU → layer2 → ReLU → Features
                                        │
                                        ├─── policy_heads (Categorical)
                                        └─── value_head (single value)
```

### 3.2 Особенности

- **Clipped PPO**: предотвращает слишком большие обновления политики
- **GAE (Generalized Advantage Estimation)**: bias-variance tradeoff
- **Multi-head factorized policy**: декомпозиция action space
- **Actor-Learner architecture**: parallel data collection

### 3.3 Гиперпараметры

```json
{
    "learning_rate": 0.0003,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_ratio": 0.2,
    "value_coef": 0.5,
    "entropy_coef": 0.01,
    "rollout_steps": 1024,
    "update_epochs": 4
}
```

### 3.4 Когда использовать

| ✓ Хорошо | ✗ Плохо |
|---------|---------|
| On-policy learning | Off-policy (sample inefficient) |
| Stable training | Very sparse rewards |
| Moderate action spaces | Extremely large action spaces |
| Discrete actions | Continuous actions |

### 3.5 Статус внедрения (код)

**Выполнено** — PPO-апгрейд по плану (зеркало DQN). Детали: [model_analysis_PPO.md](model_analysis_PPO.md).

- [x] `make_actor_critic` / `ppo_kwargs_from_env`, configurable `hidden_size`, `num_layers`
- [x] LayerNorm + ResidualBlock в trunk
- [x] Value ensemble (`PPO_VALUE_ENSEMBLE`)
- [x] Vectorized GAE (`PPO_VECTORIZED_GAE`)
- [x] LR scheduler в checkpoint (`PPO_LR_SCHEDULER`)
- [x] Adaptive entropy (`PPO_ADAPTIVE_ENTROPY`)
- [x] Grid search tools, unit-тесты
- [ ] Миграция ключей старых чекпоинтов `layer1/layer2` → новый trunk (нужно переобучение)

---

## 4. AlphaZero

### 4.1 Архитектура

```
Input → layer1 → ReLU → layer2 → ReLU → Features
                                        │
                                        ├─── policy_heads (MCTS policy targets)
                                        └─── value_head (∈ [-1, 1])
```

### 4.2 Особенности

- **MCTS (Monte Carlo Tree Search)**: planning с tree structure
- **Self-play**: учится играя против себя
- **Factorized MCTS**: search over factored action space
- **Two modes**: "proxy" (fast) и "tree" (deep search)
- **Balanced outcome sampling**: баланс win/loss/draw в replay buffer

### 4.3 MCTS Architecture

```
Root Node
    │
    ├── Selection (PUCT)
    │       │
    │       ▼
    ├── Expansion (new nodes)
    │       │
    │       ▼
    ├── Simulation (rollout or network eval)
    │       │
    │       ▼
    └── Backpropagation (update visit counts, Q-values)
```

### 4.4 Гиперпараметры

```json
{
    "learning_rate": 0.0003,
    "mcts_simulations": 128,
    "c_puct": 1.1,
    "dirichlet_alpha": 0.3,
    "dirichlet_eps": 0.25,
    "mcts_top_k_per_head": 12,
    "mcts_max_depth": 4,
    "temperature_opening": 0.9,
    "temperature_late": 0.15
}
```

### 4.5 Статус внедрения (код)

**Выполнено** — полный roadmap AlphaZero (архитектура + PUCT MCTS + adaptive search). Детали: [model_analysis_AlphaZero.md](model_analysis_AlphaZero.md) §10–11.

- [x] Split algo id: `alphazero_tree` / `alphazero_proxy` (отдельные hyperparams, meta `mcts_mode`, чекпоинты)
- [x] `make_alphazero_net` / `alphazero_kwargs_from_env`, configurable `hidden_size`, `num_layers`
- [x] LayerNorm + ResidualBlock в trunk
- [x] Value ensemble (`AZ_VALUE_ENSEMBLE`)
- [x] LR scheduler в checkpoint (`AZ_LR_SCHEDULER`)
- [x] Proper PUCT MCTS + `MCTSNode` + eval cache
- [x] Adaptive c_puct, progressive widening, move-averaging
- [x] Grid search tools, unit-тесты
- [ ] Миграция ключей старых чекпоинтов `layer1/layer2` → новый trunk (нужно переобучение)

### 4.6 Когда использовать

| ✓ Хорошо | ✗ Плохо |
|---------|---------|
| Self-play capable | Noisy/self-play not possible |
| Clear win/loss conditions | Ambiguous outcomes |
| Strategic depth | Tactical-only games |
| Long planning horizon | Real-time constraints |

---

## 5. GumbelMuZero

### 5.1 Архитектура

```
Input → Representation → latent
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
        Dynamics        Dynamics        Dynamics
     (latent, a1)    (latent, a2)    (latent, a3)
            │               │               │
            ▼               ▼               ▼
        next_latent    next_latent    next_latent
            │
            ▼
        Prediction → policy + value + reward
```

### 5.2 Компоненты

1. **Representation Network**: `obs → latent`
2. **Dynamics Network**: `(latent, action) → (next_latent, reward)`
3. **Prediction Network**: `latent → (policy, value)`
4. **Gumbel Search**: planning on latent space

### 5.3 Особенности

- **Learned model**: не использует реальную среду для planning
- **Gumbel-Softmax**: differentiable sampling
- **BPTT (Backprop Through Time)**: обучение на unrolled sequences
- **Model efficiency**: planning дешевле чем real environment simulation

### 5.4 Гиперпараметры

```json
{
    "learning_rate": 0.0003,
    "unroll_steps": 5,
    "discount": 0.997,
    "latent_dim": 256,
    "hidden_dim": 256,
    "action_embed_dim": 64,
    "num_simulations": 32,
    "root_top_k": 8,
    "gumbel_scale": 1.0,
    "search_temperature": 0.15
}
```

### 5.5 Когда использовать

| ✓ Хорошо | ✗ Плохо |
|---------|---------|
| Long-horizon planning | Short episodes |
| Expensive environment | Cheap environment |
| Model can learn accurately | Complex dynamics (hard to model) |
| Transfer learning desired | From scratch (no prior) |

---

## 6. Сравнение моделей

### 6.1 По сложности

```
DQN          ▓▓░░░░░░░░  Простая
PPO          ▓▓▓░░░░░░░  Средняя
AlphaZero    ▓▓▓▓▓░░░░░  Сложная
GumbelMuZero ▓▓▓▓▓▓░░░░  Очень сложная
```

### 6.2 По compute requirements

```
DQN          ▓░░░░░░░░░  Низкие
PPO          ▓▓░░░░░░░░  Низкие
AlphaZero    ▓▓▓▓▓░░░░░  Высокие (MCTS simulations)
GumbelMuZero ▓▓▓▓░░░░░░  Средние (model inference)
```

### 6.3 По sample efficiency

```
DQN          ▓▓▓▓▓▓▓░░░  Хорошая (off-policy)
PPO          ▓▓▓░░░░░░░  Средняя (on-policy)
AlphaZero    ▓▓▓▓▓░░░░░  Хорошая (self-play)
GumbelMuZero ▓▓▓▓▓▓░░░░  Отличная (model-based)
```

### 6.4 По стабильности тренировки

```
DQN          ▓▓▓▓░░░░░░  Средняя (target network, PER helps)
PPO          ▓▓▓▓▓░░░░░  Хорошая (clipping helps)
AlphaZero    ▓▓▓▓▓▓░░░░  Очень хорошая (self-play)
GumbelMuZero ▓▓▓░░░░░░░  Средняя (model errors accumulate)
```

### 6.5 Feature matrix

| Feature | DQN | PPO | AlphaZero | GumbelMuZero |
|---------|-----|-----|-----------|--------------|
| Model-free | ✓ | ✓ | ✗ | ✗ |
| Model-based | ✗ | ✗ | ✗ | ✓ |
| Planning | ✗ | ✗ | ✓ | ✓ |
| Self-play | ✗ | ✗ | ✓ | ✓ |
| Actor-Learner | ✓ | ✓ | ✓ | ✓ |
| PER | ✓ | ✗ | ✓ | ✓ |
| Noisy exploration | ✓ | ✗ | ✓ | ✗ |
| Distributional RL | ✓ | ✗ | ✗ | ✗ |
| Continuous actions | ✗ | ✗ | ✗ | ✗ |
| Multi-head policy | ✓ | ✓ | ✓ | ✓ |

---

## 7. Common Training Infrastructure

### 7.1 Replay Buffers

```python
# Unified interface
class ReplayBuffer:
    def push(self, transition): ...
    def sample(self, batch_size): ...
    def __len__(self): ...
    def state_dict(self): ...
    def load_state_dict(self, state): ...

# Specializations
class PrioritizedReplayBuffer(ReplayBuffer):
    # PER with priority calculation

class OutcomeBalancedReplayBuffer(ReplayBuffer):
    # AZ-style balanced sampling

class UnrolledReplayBuffer(ReplayBuffer):
    # GMZ-style unroll sequences
```

### 7.2 Training utilities

```python
def compute_loss_and_backward(net, optimizer, batch, config):
    # Shared utilities
    optimizer.zero_grad()
    loss = compute_loss(net, batch, config)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(net.parameters(), config.max_grad_norm)
    optimizer.step()
    return {'loss': loss.item(), ...}
```

### 7.3 Checkpoint management

```python
@dataclass
class ModelCheckpoint:
    step: int
    model_state_dict: dict
    optimizer_state_dict: dict
    policy_version: int
    metrics: dict

    def save(self, path):
        torch.save({
            'step': self.step,
            'model_state_dict': self.model_state_dict,
            'optimizer_state_dict': self.optimizer_state_dict,
            'policy_version': self.policy_version,
            'metrics': self.metrics,
        }, path)

    @classmethod
    def load(cls, path, net, optimizer):
        data = torch.load(path)
        net.load_state_dict(data['model_state_dict'])
        optimizer.load_state_dict(data['optimizer_state_dict'])
        return cls(**data)
```

---

## 8. Recommendations по использованию

### 8.1 По задаче

| Задача | Рекомендация |
|--------|--------------|
| Быстрый baseline | DQN или PPO |
| Стратегическое планирование | AlphaZero |
| Долгие эпизоды (>100 шагов) | GumbelMuZero |
| Self-play available | AlphaZero |
| Нестабильные rewards | PPO (clipping) |
| Sparse rewards | GumbelMuZero (model-based) |
| Transfer learning | GumbelMuZero |

### 8.2 По compute

| Compute | Рекомендация |
|---------|--------------|
| < 4 CPU cores | DQN |
| 4-16 CPU cores | PPO |
| GPU + 16+ CPU cores | AlphaZero, GumbelMuZero |
| Distributed | GumbelMuZero (actor-learner) |

### 8.3 По размеру action space

| Action space | Рекомендация |
|--------------|--------------|
| < 100 actions | DQN, PPO |
| 100-1000 actions | PPO, AlphaZero |
| > 1000 actions | AlphaZero (MCTS handles large) |
| 40k (текущий) | AlphaZero или GumbelMuZero |

---

## 9. Улучшения (Priority Matrix)

### 9.1 High Priority (все модели)

| Улучшение | DQN | PPO | AZ | GMZ | Impact |
|-----------|-----|-----|----|----|--------|
| Layer normalization | ✓ | ✓ | ✓ | ✓ | Training stability |
| Residual connections | ✓ | ✓ | ✓ | ✓ | Better gradients |
| Configurable hidden size | ✓ | ✓ | ✓ | ✓ | Flexibility |
| Adaptive learning rate | ✓ | ✓ | ✓ | ✓ | Faster convergence |
| Improved checkpointing | ✓ | ✓ | ✓ | ✓ | Reliability |

### 9.2 Medium Priority

| Улучшение | DQN | PPO | AZ | GMZ | Impact |
|-----------|-----|-----|----|----|--------|
| Rainbow extensions | ✓ | ✗ | ✗ | ✗ | Better exploration |
| Adaptive entropy | ✗ | ✓ | ✓ | ✗ | Better exploration |
| Proper PUCT MCTS | ✗ | ✗ | ✓ | ✗ | Planning quality |
| Gumbel-UCB search | ✗ | ✗ | ✗ | ✓ | Planning quality |
| Model ensemble | ✓ | ✓ | ✓ | ✓ | Uncertainty |

### 9.3 Low Priority

| Улучшение | DQN | PPO | AZ | GMZ | Impact |
|-----------|-----|-----|----|----|--------|
| Neural architecture search | ✓ | ✓ | ✓ | ✓ | Auto-tuning |
| Model distillation | ✗ | ✓ | ✓ | ✓ | Compression |
| Meta-learning | ✓ | ✓ | ✓ | ✓ | Few-shot |
| Distributed training | ✓ | ✓ | ✓ | ✓ | Scale |

---

## 10. Testing Infrastructure

### 10.1 Unit tests (required)

```python
# Shared test utilities
class ModelTests:
    @staticmethod
    def test_forward_pass(net):
        """Test basic forward pass"""
        x = torch.randn(32, net.n_observations)
        output = net(x)
        assert output is not None
        assert not torch.isnan(output).any()

    @staticmethod
    def test_backward_pass(net):
        """Test gradient computation"""
        x = torch.randn(32, net.n_observations)
        target = torch.randn(*output.shape)
        loss = F.mse_loss(net(x), target)
        loss.backward()
        assert any(p.grad is not None for p in net.parameters())

    @staticmethod
    def test_action_masking(net):
        """Test action masking"""
        x = torch.randn(32, net.n_observations)
        mask = [torch.zeros(s).fill_(True) for s in net.action_sizes]
        mask[0][0] = False  # disable action 0
        output = net.infer(x, masks_by_head=mask)
        # Action 0 should not be selected
        assert output[0][0, 0] < output[0][0, 1]

    @staticmethod
    def test_device_transfer(net):
        """Test moving between devices"""
        if torch.cuda.is_available():
            net_gpu = net.to('cuda')
            x = torch.randn(32, net.n_observations).to('cuda')
            output = net_gpu(x)
            assert output.device.type == 'cuda'
```

### 10.2 Integration tests (required)

```python
class IntegrationTests:
    def test_training_loop(self):
        """Test full training step"""
        # Setup
        net = create_model()
        optimizer = optim.Adam(net.parameters())
        buffer = create_buffer()
        config = create_config()

        # Collect data
        for _ in range(100):
            buffer.push(generate_transition())

        # Train
        for _ in range(10):
            batch = buffer.sample(config.batch_size)
            loss = train_step(net, optimizer, batch, config)
            assert loss > 0

    def test_checkpoint_save_load(self):
        """Test checkpoint persistence"""
        net1 = create_model()
        opt1 = optim.Adam(net1.parameters())

        # Save
        save_checkpoint('test.pth', net1, opt1, 100)

        # Load
        net2 = create_model()
        opt2 = optim.Adam(net2.parameters())
        load_checkpoint('test.pth', net2, opt2)

        # Verify weights match
        for p1, p2 in zip(net1.parameters(), net2.parameters()):
            assert torch.allclose(p1, p2)
```

---

## 11. Debugging Guide

### 11.1 DQN issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Loss = nan | Large gradients | Reduce learning rate, clip gradients |
| Q-values explode | Unstable target | Reduce tau, increase target update freq |
| No learning | Epsilon too high | Reduce epsilon decay rate |
| Agent stuck | NoisyNet not reset | Call `reset_noise()` after load |

### 11.2 PPO issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| KL divergence large | lr too high | Reduce learning rate |
| Entropy collapse | Policy too confident | Increase entropy_coef |
| Value divergence | Value loss too high | Increase value_coef, clip value |
| Clip fraction = 1.0 | Aggressive updates | Reduce clip_ratio |

### 11.3 AlphaZero issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| No improvement | MCTS mode wrong | Check mode="tree" |
| High draw rate | Temperature too low | Increase temperature_late |
| Slow simulation | Environment snapshot | Optimize snapshot/restore |
| Policy collapse | No dirichlet noise | Increase dirichlet_eps |

### 11.4 GumbelMuZero issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Model collapse | Unroll too long | Reduce unroll_steps |
| Reward prediction poor | Reward head too simple | Add hidden layers to reward |
| Latent instability | Normalization issue | Use LayerNorm in representation |
| Search not improving | Gumbel scale wrong | Tune gumbel_scale |

---

## 12. Summary таблица

| Аспект | DQN | PPO | AlphaZero | GumbelMuZero |
|--------|-----|-----|-----------|--------------|
| **Complexity** | Low | Medium | High | Very High |
| **Sample Efficiency** | Good | Medium | Good | Excellent |
| **Training Stability** | Medium | Good | Very Good | Medium |
| **Planning** | None | None | MCTS | Gumbel Search |
| **Model** | None | None | None | Learned |
| **Compute** | Low | Low | High | Medium |
| **Recommended for** | Baseline | Stable RL | Strategic | Long-horizon |

---

## 13. Roadmap

### Phase 1: Quick wins (1 week)
- [x] Add LayerNorm to all models — **DQN ✓** (`e29c4df0`), **PPO ✓**
- [x] Add residual connections — **DQN ✓**, **PPO ✓**
- [x] Fix configurable hidden size — **DQN ✓**, **PPO ✓**
- [x] Add adaptive learning rate — **DQN ✓**, **PPO ✓**, **AlphaZero ✓** (LR scheduler)
- [x] AlphaZero architecture + MCTS upgrades — **AlphaZero ✓**
- [ ] GumbelMuZero — в работе

### Phase 2: Major improvements (2-4 weeks)
- [x] Implement proper PUCT for AlphaZero MCTS
- [ ] Implement Gumbel-UCB search for GMZ
- [ ] Add model ensemble for uncertainty
- [ ] Improve checkpoint management

### Phase 3: Advanced features (1-2 months)
- [ ] Distributed training
- [ ] Model compression/distillation
- [ ] Meta-learning
- [ ] Neural architecture search

---

*Дата: 2026-05-22*
*Автор: Claude Code*
*Файлы: docs/model_analysis_*.md*