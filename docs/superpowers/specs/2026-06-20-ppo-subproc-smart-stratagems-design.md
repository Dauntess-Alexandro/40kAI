# PPO Subproc Smart Stratagems — дизайн

> Статус: спека (brainstorming, rev. 2026-06-20). Расширение PPO smart stratagems на subproc-режим (`USE_SUBPROC_ENVS=1`, кнопка «8х»).
> Связанные:
> - `docs/superpowers/specs/2026-06-19-ppo-smart-stratagems-design.md` (**базовая фича**: inline + spawn-actor пути),
> - `docs/superpowers/specs/2026-06-19-dqn-smart-stratagems-design.md` (эталон max-Q; spawn-actor паттерн с cpu_net),
> - `docs/superpowers/specs/2026-06-19-b3-reaction-value-policy-design.md` (reaction value-policy seam).

## 1. Контекст и мотивация

Базовая PPO-фича (smart stratagems) работает в **inline-пути** (`run_ppo_training`) и в **spawn-actor**
(`_actor_learner_actor_entry_ppo`). Но при `USE_SUBPROC_ENVS=1` (12 env, кнопка «8х» в GUI) PPO идёт
через **`run_ppo_training_subproc`**, где умные стратагемы **отключены** (сейчас — явный лог
`[PPO][CONFIG] reaction_value_policy недоступна при USE_SUBPROC_ENVS=1 …`, коммит 79e3f709).

**Почему отключены.** В subproc-режиме:
- Сеть `actor_critic` живёт в **главном процессе** (`run_ppo_training_subproc:3942`), он считает действия
  через `actor_critic.act` и шлёт `action_dict` воркерам по pipe.
- Воркер `_env_worker` (`train.py:2143`) только делает `env.step(payload)` — **сети у него нет**.
- А value-гейт (`_simulate_reaction_branch`) и fight-plan исполняются **внутри `env.step`/`enemyTurn`,
  т.е. в воркере**. Без сети в воркере гейтить нечем.

**Цель.** Дать воркеру CPU-копию `actor_critic` (с синком весов от learner'а) и поставить тот же
value-гейт в воркере. Паритет с inline-путём по умным стратагемам, при сохранении 12-env throughput.

**Не-цели.**
- Не трогаем движок, action-space, reaction_value_policy seam, `ppo_stratagem_bridge.py` (используем как есть).
- Не трогаем inline (`run_ppo_training`) и spawn-actor (`_actor_learner_actor_entry_ppo`) пути — они уже работают.
- Не делаем DQN-subproc (`_env_worker` у DQN тоже без сети) — переиспользуемые команды появятся, но
  DQN-сторона не реализуется здесь (отдельная задача).
- Не делаем both-sides (enemy умно реагирует) — learner_only, как в базовой фиче.

## 2. Принцип дизайна

**Opt-in, без регрессии inline/DQN.** Старые IPC-команды `_env_worker` не меняем; добавляем две
новые, которые шлёт **только** PPO-subproc-родитель при `PPO_REACTION_VALUE_POLICY=1`. DQN-subproc их
не шлёт → его поведение байт-в-байт прежнее. Сам гейт переиспользует `ppo_stratagem_bridge` (install +
`ppo_build_fight_plan`) и движковый seam как есть.

## 3. Архитектура

### 3.1 Data flow (subproc, с умными стратагемами)

```
[Родитель: run_ppo_training_subproc]                 [Воркер: _env_worker × N]
  actor_critic (device)
  spawn воркеров → handshake (state/info/mask)
  ЕСЛИ PPO_REACTION_VALUE_POLICY:
    для каждого воркера:
      send("init_reaction_net", {arch, n_obs, n_actions, weights_cpu}) ───────▶ строит cpu ActorCriticMultiHead
                                                                                 load_state_dict(weights)
                                                                                 install_ppo_stratagem_policy(env, cpu, {"model": net})
  LOOP:
    send("enemy_turn") ──────────────────────────────────────────────────────▶ env.enemyTurn()  # реакции model-side через гейт (net в ctx)
    action = actor_critic.act(obs)
    send("step", action_dict) ───────────────────────────────────────────────▶ ЕСЛИ net: attach_fight_stratagem_plan(env, ppo_build_fight_plan(env, net, cpu, "model"))
                                                                                 try: env.step(action_dict)  # bravery/overwatch/fight гейтятся
                                                                                 finally: attach_fight_stratagem_plan(env, None)
    ... rollout ...
    ЕСЛИ len(buffer) >= PPO_ROLLOUT_STEPS:
      _run_ppo_update_loop(actor_critic, ...)
      ЕСЛИ PPO_REACTION_VALUE_POLICY и (update % sync_every == 0):
        для каждого воркера: send("sync_weights", actor_critic.cpu_state_dict()) ▶ net.load_state_dict(weights)
```

### 3.2 Компоненты

| # | Файл / функция | Что меняем | Объём |
|---|---|---|---|
| 1 | `train.py` `_env_worker` (2143) | net-холдер в замыкании; 2 новые cmd: `init_reaction_net`, `sync_weights`; fight-plan в `step` | ~35 строк |
| 2 | `train.py` `run_ppo_training_subproc` (3934) | send `init_reaction_net` после handshake; broadcast `sync_weights` после update; заменить «недоступна»-лог | ~30 строк |
| 3 | `train.py` (флаги) | env-тормоз `PPO_SUBPROC_WEIGHT_SYNC_EVERY` (дефолт 1) | ~3 строки |

Движок, `ppo_stratagem_bridge.py`, `reaction_value_policy.py`, inline/spawn-actor пути — **0 изменений**.

### 3.3 Подробности

#### 3.3.1 `_env_worker` — net-холдер и новые команды

В начале `_env_worker` (после создания `env`, ~2192) завести локальную переменную `reaction_net = None`.
В цикле обработки команд (`while True`) добавить ветки:

```python
elif cmd == "init_reaction_net":
    # payload: {"arch": {...}, "n_obs": int, "n_actions": [...], "weights": state_dict}
    try:
        from core.models.PPO import make_actor_critic
        from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

        arch = payload.get("arch") or {}
        reaction_net = make_actor_critic(
            int(payload["n_obs"]), list(payload["n_actions"]), **arch
        ).to(torch.device("cpu"))
        reaction_net.load_state_dict(payload["weights"], strict=False)
        reaction_net.eval()
        install_ppo_stratagem_policy(env, torch.device("cpu"), {"model": reaction_net})
        conn.send({"ok": True})
    except Exception as exc:
        reaction_net = None
        conn.send({"ok": False, "error": str(exc)})
elif cmd == "sync_weights":
    if reaction_net is not None:
        try:
            reaction_net.load_state_dict(payload, strict=False)
        except Exception:
            pass
    conn.send(True)
```

В ветке `step` (2211-2219) — обернуть `env.step` fight-планом, если net установлен:

```python
elif cmd == "step":
    if reaction_net is not None:
        from core.models.option_candidates import attach_fight_stratagem_plan
        from core.models.ppo_stratagem_bridge import ppo_build_fight_plan

        attach_fight_stratagem_plan(env, ppo_build_fight_plan(env, reaction_net, torch.device("cpu"), side="model"))
    try:
        next_observation, reward, done, res, info = env.step(payload)
    finally:
        if reaction_net is not None:
            from core.models.option_candidates import attach_fight_stratagem_plan

            attach_fight_stratagem_plan(env, None)
    next_observation = _to_np_state(next_observation)
    ... (остальное без изменений: lean_info, next_mask, conn.send)
```

> Реакции (bravery/overwatch/smokescreen/heroic) гейтятся **автоматически** внутри `env.step` и
> `env.enemyTurn`, как только `reaction_policy` установлена на env (install в `init_reaction_net`).
> Отдельно их прокидывать не нужно — только fight-plan требует явного `attach`.

#### 3.3.2 `run_ppo_training_subproc` — init и sync

**Init после handshake.** Воркеры создаются/handshake'атся в общем env-setup; в самой
`run_ppo_training_subproc` `env_contexts` уже содержат `ctx["conn"]`. Заменить блок-лог «недоступна»
(текущий `:3973-3977`) на init-рассылку:

```python
PPO_SUBPROC_WEIGHT_SYNC_EVERY = max(1, int(os.getenv("PPO_SUBPROC_WEIGHT_SYNC_EVERY", "1")))
if PPO_REACTION_VALUE_POLICY:
    _arch = _ppo_arch_dict(actor_critic)
    _w_cpu = {k: v.detach().cpu() for k, v in actor_critic.state_dict().items()}
    _ok = 0
    for ctx in env_contexts:
        ctx["conn"].send(("init_reaction_net", {
            "arch": _arch, "n_obs": int(n_observations), "n_actions": list(n_actions), "weights": _w_cpu,
        }))
    for ctx in env_contexts:
        resp = ctx["conn"].recv()
        if isinstance(resp, dict) and resp.get("ok"):
            _ok += 1
        else:
            append_agent_log(f"[PPO][SUBPROC][WARN] init_reaction_net failed: {resp}")
    append_agent_log(
        f"[PPO][CONFIG] reaction_value_policy установлена (subproc workers, critic V): {_ok}/{len(env_contexts)} воркеров"
    )
```

> `_ppo_arch_dict(actor_critic)` уже есть (`train.py:3375`) → даёт `{hidden_size, num_layers, n_value_ensemble}`.
> Передаём один и тот же `_w_cpu` всем (send pickle'ит per-conn) — корректно.

**Sync после update.** После `_run_ppo_update_loop` (~`:4158`, в блоке `if len(buffer) >= …`):

```python
if PPO_REACTION_VALUE_POLICY and (ppo_update_step % PPO_SUBPROC_WEIGHT_SYNC_EVERY == 0):
    _w_cpu = {k: v.detach().cpu() for k, v in actor_critic.state_dict().items()}
    for ctx in env_contexts:
        ctx["conn"].send(("sync_weights", _w_cpu))
    for ctx in env_contexts:
        ctx["conn"].recv()
```

> Синхронный recv после send держит порядок IPC (как у существующих `enemy_turn`/`step`). `ppo_update_step`
> уже инкрементится на `+= updates` рядом; для устойчивости считаем по нему.

## 4. Флаги

| Флаг | Дефолт | Что |
|---|---|---|
| `PPO_REACTION_VALUE_POLICY` | `1` | (существующий) включает умные стратагемы; теперь и в subproc |
| `PPO_SUBPROC_WEIGHT_SYNC_EVERY` | `1` | синк весов воркерам каждые N PPO-обновлений |

## 5. Trade-offs

| Аспект | Плюс | Цена |
|---|---|---|
| Умные стратагемы в «8х» | Паритет с inline при 12-env throughput | +1 forward/реакция, +2/eligible-боец в fight, на CPU воркера (распределено) |
| Синк весов каждый update | Свежий критик у воркеров | Сериализация ~MB state_dict × N воркеров per update (терпимо; throttle `_EVERY`) |
| Opt-in IPC-команды | 0 регрессии inline/DQN/движка | Воркер держит CPU-копию сети (память × N) |
| Staleness ≤ 1 update | Просто, как у DQN actor-learner | Гейт по чуть-чуть устаревшему критику (приемлемо) |

## 6. Тестирование

### 6.1 Юнит-тесты
- **`tests/train/test_env_worker_reaction_net.py`** (новый, in-process, без реального spawn):
  Вызвать `_env_worker` логику через фейковый `conn` (duck-typed с `recv`/`send` очередями) либо вынести
  net-init/step-обёртку в тестируемый хелпер. Минимально: проверить, что после `init_reaction_net`
  на env стоит `reaction_policy` (через прямой вызов хелпера установки на mock-env).
  > Если рефакторить `_env_worker` ради тестируемости рискованно — ограничиться проверкой, что
  > `install_ppo_stratagem_policy` + `ppo_build_fight_plan` уже покрыты (Tasks 2-3 базовой фичи), а здесь
  > тестируем тонкий fake-conn протокол: `init_reaction_net` → `{"ok": True}`, `sync_weights` → `True`.

### 6.2 Регрессия
- Существующие subproc-тесты (если есть) и `import train` / `py_compile` — зелёные.
- DQN-subproc не задет: старые команды `_env_worker` без изменений; новые шлёт только PPO-родитель.

### 6.3 Smoke (live)
- GUI «8х» с PPO → в `LOGS_FOR_AGENTS_TRAIN.md`:
  - `[PPO][CONFIG] reaction_value_policy установлена (subproc workers, critic V): N/N воркеров` (вместо «недоступна»).
  - `[STRATAGEM]` со списанным CP появляются (выборочно).
- Сравнение `PPO_REACTION_VALUE_POLICY=0` (8х) → init не шлётся, гейта нет (legacy).
- `PPO_SUBPROC_WEIGHT_SYNC_EVERY=5` → синк реже, тренировка не падает.

## 7. Открытые вопросы (решено)

- ✅ Сеть воркеру: **CPU-копия `actor_critic`**, init через новую IPC-команду (opt-in), не через сигнатуру `_env_worker`.
- ✅ Синк: **после каждого PPO-обновления**, throttle `PPO_SUBPROC_WEIGHT_SYNC_EVERY` (дефолт 1).
- ✅ Fight-plan: строится **в воркере** перед `env.step` (реакции — автоматически через установленную `reaction_policy`).
- ✅ Scope: **только PPO**; DQN-subproc переиспользует команды позже.
- ✅ Staleness ≤ 1 update — приемлемо (паритет с DQN actor-learner).
- ✅ Старый «недоступна»-лог (79e3f709) — **заменяется** на «установлена (subproc workers)».
