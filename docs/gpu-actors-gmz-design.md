# GPU-акторы для GMZ (вариант A)

## Цель

Перенести inference Gumbel MuZero (search) с CPU на GPU при self-play, не переписывая архитектуру PRO_ACTOR_LEARNER.

## Архитектура

- **Learner**: CUDA (как раньше) — обучение, reanalyze.
- **Акторы**: `actor_device=cpu` (по умолчанию, до 8 процессов) или `actor_device=cuda` (до `actor_max_cuda`, по умолчанию 2).
- **Env / enemyTurn / opponent PPO**: остаются на CPU в процессе актора.

## Конфигурация

| Параметр | Источник | По умолчанию |
|----------|----------|--------------|
| `actor_device` | `hyperparams.json` → `GMZ_CFG`, env `GMZ_ACTOR_DEVICE` | `cuda` |
| `actor_max_cuda` | `hyperparams.json` → `GMZ_CFG`, env `GMZ_ACTOR_MAX_CUDA` | `2` |
| `num_actors` | пресеты / balanced | `2` |

При `actor_device=cuda` и доступной CUDA: `effective_num_actors = min(num_actors, actor_max_cuda)`.

### Fallback без CUDA

Если в конфиге `cuda`, но `torch.cuda.is_available()` ложно — train автоматически:
- `actor_device=cpu`
- `num_actors=8` (прежний CPU-дефолт)
- строка `[GMZ][CONFIG][FALLBACK]` в `LOGS_FOR_AGENTS_TRAIN.md`

## Рекомендация для RTX 5060 Ti 16 GB

```json
"actor_device": "cuda",
"actor_max_cuda": 2,
"num_actors": 2,
"num_simulations": 40,
"batch_recurrent": 1,
"learner_compile": 0
```

Профиль **heavy** в GUI уже близок к этим значениям.

## Ограничения

- Несколько CUDA-процессов на одной GPU → contention с learner; следить за VRAM.
- `torch.compile` для акторов отключён на GPU.
- Opponent inference (PPO) по-прежнему на CPU.

## Критерии успеха

- В логах: `[GMZ][ACTOR] device=cuda`, `[GMZ][CONFIG] GPU actors: 2`.
- GPU utilization > 0% во время self-play.
- Нет CUDA OOM при `actor_max_cuda=2`.
- `actor_device=cpu` — поведение как до изменений (без cap, если `num_actors=8`).

## Следующий шаг

Вариант B: единый GPU inference server + CPU env workers (см. обсуждение в чате).
