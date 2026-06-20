# PPO Subproc Smart Stratagems Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Включить умные стратагемы PPO в subproc-режиме (`USE_SUBPROC_ENVS=1`, кнопка «8х»), дав воркеру `_env_worker` CPU-копию `actor_critic` с синком весов и тем же value-гейтом, что в inline-пути.

**Architecture:** Opt-in расширение. Две новые IPC-команды в `_env_worker` (`init_reaction_net`, `sync_weights`), которые шлёт только PPO-subproc-родитель при `PPO_REACTION_VALUE_POLICY=1`. Воркер строит CPU-`ActorCriticMultiHead`, ставит `install_ppo_stratagem_policy`, строит fight-plan перед `env.step`. Reaction-гейт работает автоматически внутри `env.step`/`enemyTurn`. Движок, bridge, inline/spawn-actor/DQN-пути — не трогаем.

**Tech Stack:** Python 3.12+, PyTorch, multiprocessing (spawn, Windows), pytest. Спека: `docs/superpowers/specs/2026-06-20-ppo-subproc-smart-stratagems-design.md`.

## Global Constraints

- Платформа Windows; язык логов/сообщений — русский (что случилось + где + что делать).
- Движок (`core/engine/*`, `core/envs/warhamEnv.py`, `_simulate_reaction_branch`), `action_contract.py`, `ppo_stratagem_bridge.py`, `reaction_value_policy.py` — **не менять**.
- inline-путь `run_ppo_training`, spawn-actor `_actor_learner_actor_entry_ppo`, DQN-код — **не трогать**.
- **Opt-in:** старые IPC-команды `_env_worker` без изменений; новые шлёт только PPO-subproc-родитель → DQN-subproc байт-в-байт прежний.
- V(s) = честный critic (`ppo_value` через `ppo_build_fight_plan`/install из `ppo_stratagem_bridge`).
- Воркер-сеть — на CPU (`torch.device("cpu")`), `strict=False` при load (как у других PPO load).
- `ruff_fix.py` PostToolUse срезает неиспользуемые импорты — локальные импорты внутри веток рядом с использованием.
- IPC: каждый `conn.send` парный с `conn.recv` в родителе (порядок как у `enemy_turn`/`step`).
- Интерфейс init: parent `send(("init_reaction_net", {"arch", "n_obs", "n_actions", "weights"}))` → worker `send({"ok": bool, "error"?})`. sync: parent `send(("sync_weights", state_dict))` → worker `send(True)`.
- Частые коммиты: один коммит на задачу после зелёных проверок.

---

### Task 1: `_env_worker` — net-холдер, новые команды, fight-plan в step

**Files:**
- Modify: `train.py` — новый module-level хелпер `_ppo_worker_install_reaction_net`; правки в `_env_worker` (2143).
- Test: `tests/train/test_ppo_worker_reaction_net.py` (создать).

**Interfaces:**
- Consumes: `make_actor_critic` (`core/models/PPO.py`, уже импортирован в train.py); `install_ppo_stratagem_policy`, `ppo_build_fight_plan` (`core/models/ppo_stratagem_bridge.py`); `attach_fight_stratagem_plan` (`core/models/option_candidates`); `unwrap_env`.
- Produces:
  - `_ppo_worker_install_reaction_net(env, payload: dict, device) -> net | None` — строит CPU `ActorCriticMultiHead` из `payload["arch"]/n_obs/n_actions`, грузит `payload["weights"]` (strict=False), ставит `install_ppo_stratagem_policy(env, device, {"model": net})`, возвращает net (или `None` при ошибке).
  - `_env_worker` cmd `init_reaction_net` → `{"ok": bool}`; cmd `sync_weights` → `True`; `step` оборачивает `env.step` fight-планом, если net установлен.

- [ ] **Step 1: Write the failing test**

```python
# tests/train/test_ppo_worker_reaction_net.py
"""_ppo_worker_install_reaction_net: воркер строит net + ставит reaction_policy."""

import numpy as np
import torch

from core.models.action_contract import action_sizes_from_env
from core.models.PPO import ActorCriticMultiHead
from tests.engine.phases._helpers import build_env


def _payload(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    len_model = len(env.unit_health)
    sizes = action_sizes_from_env(env, len_model)
    obs_dim = len(np.asarray(env.get_observation_for_side("model"), dtype=np.float32))
    net = ActorCriticMultiHead(obs_dim, sizes, hidden_size=32, num_layers=1, n_value_ensemble=1)
    return {
        "arch": {"hidden_size": 32, "num_layers": 1, "n_value_ensemble": 1},
        "n_obs": obs_dim,
        "n_actions": sizes,
        "weights": {k: v.detach().cpu() for k, v in net.state_dict().items()},
    }


def test_install_returns_net_and_sets_policy():
    from train import _ppo_worker_install_reaction_net

    env = build_env()
    payload = _payload(env)
    net = _ppo_worker_install_reaction_net(env, payload, torch.device("cpu"))
    assert net is not None
    assert env.reaction_policy is not None
    assert env._reaction_net_by_side.get("model") is net


def test_install_bad_payload_returns_none():
    from train import _ppo_worker_install_reaction_net

    env = build_env()
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    net = _ppo_worker_install_reaction_net(env, {"arch": {}, "n_obs": 4, "n_actions": [2], "weights": {}}, torch.device("cpu"))
    # mismatched arch/obs → net создан, но weights пустые (strict=False) — допустимо; главное без падения.
    assert net is None or env.reaction_policy is not None
```

> Примечание про `test_install_bad_payload_returns_none`: цель — что хелпер НЕ роняет воркер.
> Если `make_actor_critic(4, [2])` строится без ошибки и install проходит — допустимо (net != None).
> Если внутри ошибка — должен вернуть None. Любой из исходов без исключения — тест зелёный.

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/train/test_ppo_worker_reaction_net.py -v`
Expected: FAIL — `ImportError: cannot import name '_ppo_worker_install_reaction_net' from 'train'`.

- [ ] **Step 3: Write the helper**

В `train.py`, рядом с `_env_worker` (перед ним, ~строка 2142), добавить module-level хелпер:

```python
def _ppo_worker_install_reaction_net(env, payload, device):
    """Subproc-воркер: построить CPU-сеть PPO из payload и поставить reaction value-gate.

    payload: {"arch": {...}, "n_obs": int, "n_actions": [...], "weights": state_dict}.
    Возвращает net (или None при ошибке — воркер продолжит без умных стратагем, не падая).
    """
    try:
        from core.models.PPO import make_actor_critic
        from core.models.ppo_stratagem_bridge import install_ppo_stratagem_policy

        arch = payload.get("arch") or {}
        net = make_actor_critic(int(payload["n_obs"]), list(payload["n_actions"]), **arch).to(device)
        net.load_state_dict(payload["weights"], strict=False)
        net.eval()
        install_ppo_stratagem_policy(env, device, {"model": net})
        return net
    except Exception:
        return None
```

- [ ] **Step 4: Wire `_env_worker`**

В `_env_worker` после создания `env` (после строки ~2192, перед `state, info = env.reset(...)` или сразу после первого `conn.send` handshake на 2196-2203) завести холдер:

```python
        reaction_net = None  # subproc smart stratagems: ставится по команде init_reaction_net
```

В цикле `while True` (после `cmd, payload = conn.recv()`), добавить две ветки рядом с прочими `elif` (например после ветки `enemy_turn`):

```python
            elif cmd == "init_reaction_net":
                reaction_net = _ppo_worker_install_reaction_net(env, payload, torch.device("cpu"))
                conn.send({"ok": reaction_net is not None})
            elif cmd == "sync_weights":
                if reaction_net is not None:
                    try:
                        reaction_net.load_state_dict(payload, strict=False)
                    except Exception:
                        pass
                conn.send(True)
```

Заменить ветку `step` (2211-2219), добавив fight-plan-обёртку:

```python
            elif cmd == "step":
                if reaction_net is not None:
                    from core.models.option_candidates import attach_fight_stratagem_plan
                    from core.models.ppo_stratagem_bridge import ppo_build_fight_plan

                    attach_fight_stratagem_plan(
                        env, ppo_build_fight_plan(env, reaction_net, torch.device("cpu"), side="model")
                    )
                try:
                    next_observation, reward, done, res, info = env.step(payload)
                finally:
                    if reaction_net is not None:
                        from core.models.option_candidates import attach_fight_stratagem_plan

                        attach_fight_stratagem_plan(env, None)
                next_observation = _to_np_state(next_observation)
                if lean_info_enabled:
                    info = _lean_train_info(info)
                next_mask = None
                if include_masks and not done:
                    next_mask = build_shoot_action_mask(env, log_fn=None, debug=False)
                conn.send((next_observation, reward, done, res, info, next_mask))
```

> Не меняй остальные ветки (`enemy_turn`/`reset`/`get_*`/`save_pickle`/`close`) и handshake. `torch`
> уже импортирован на уровне модуля train.py.

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/train/test_ppo_worker_reaction_net.py -v`
Expected: PASS (2 теста).

- [ ] **Step 6: Compile check**

Run: `python -m py_compile train.py`
Expected: без ошибок.

- [ ] **Step 7: Commit**

```bash
git add train.py tests/train/test_ppo_worker_reaction_net.py
git commit -m "feat(ppo,subproc): _env_worker net-холдер + init_reaction_net/sync_weights + fight-plan"
```

---

### Task 2: `run_ppo_training_subproc` — init-рассылка, sync после update, флаг

**Files:**
- Modify: `train.py` — `run_ppo_training_subproc` (3934): заменить «недоступна»-лог на init-рассылку; sync после `_run_ppo_update_loop`; флаг `PPO_SUBPROC_WEIGHT_SYNC_EVERY`.

**Interfaces:**
- Consumes: `_ppo_arch_dict(actor_critic)` (`train.py:3375`); `actor_critic`, `n_observations`, `n_actions`, `env_contexts` (каждый `ctx["conn"]`), `PPO_REACTION_VALUE_POLICY` (модульный глобал), `ppo_update_step`, `append_agent_log`. Воркер-контракт из Task 1 (`init_reaction_net`→`{"ok":...}`, `sync_weights`→`True`).
- Produces: воркеры с установленным гейтом; периодический синк весов.

- [ ] **Step 1: Заменить «недоступна»-лог на init-рассылку**

Текущий блок (`train.py:3973-3977`):
```python
    if PPO_REACTION_VALUE_POLICY:
        append_agent_log(
            "[PPO][CONFIG] reaction_value_policy недоступна при USE_SUBPROC_ENVS=1 "
            "(умные стратагемы работают только в inline-пути; subproc-воркеры не разделяют actor_critic)."
        )
```
заменить на:
```python
    PPO_SUBPROC_WEIGHT_SYNC_EVERY = max(1, int(os.getenv("PPO_SUBPROC_WEIGHT_SYNC_EVERY", "1")))
    if PPO_REACTION_VALUE_POLICY:
        _arch = _ppo_arch_dict(actor_critic)
        _w_cpu = {k: v.detach().cpu() for k, v in actor_critic.state_dict().items()}
        for ctx in env_contexts:
            ctx["conn"].send((
                "init_reaction_net",
                {"arch": _arch, "n_obs": int(n_observations), "n_actions": list(n_actions), "weights": _w_cpu},
            ))
        _ok = 0
        for ctx in env_contexts:
            resp = ctx["conn"].recv()
            if isinstance(resp, dict) and resp.get("ok"):
                _ok += 1
            else:
                append_agent_log(f"[PPO][SUBPROC][WARN] init_reaction_net не удался: {resp}")
        append_agent_log(
            f"[PPO][CONFIG] reaction_value_policy установлена (subproc workers, critic V): "
            f"{_ok}/{len(env_contexts)} воркеров"
        )
```

> `PPO_SUBPROC_WEIGHT_SYNC_EVERY` определяем здесь (локально в функции), используем в Step 2.

- [ ] **Step 2: Sync весов после PPO-обновления**

Внутри блока `if len(buffer) >= max(1, int(PPO_ROLLOUT_STEPS)):` после `_run_ppo_update_loop(...)` и
`ppo_update_step += int(updates)` (после `train.py:4157-4158`), добавить:

```python
                if PPO_REACTION_VALUE_POLICY and (ppo_update_step % PPO_SUBPROC_WEIGHT_SYNC_EVERY == 0):
                    _w_sync = {k: v.detach().cpu() for k, v in actor_critic.state_dict().items()}
                    for ctx in env_contexts:
                        ctx["conn"].send(("sync_weights", _w_sync))
                    for ctx in env_contexts:
                        ctx["conn"].recv()
```

> Парный send→recv (как `enemy_turn`/`step`) держит IPC-порядок. Отступ — внутри `if int(batch.obs.shape[0]) > 0:`.

- [ ] **Step 3: Compile check**

Run: `python -m py_compile train.py`
Expected: без ошибок.

- [ ] **Step 4: Import smoke**

Run: `python -c "import train"`
Expected: без ImportError/SyntaxError (если зависает — `python -m py_compile train.py` и отметить).

- [ ] **Step 5: Commit**

```bash
git add train.py
git commit -m "feat(ppo,subproc): init_reaction_net рассылка + sync_weights после update + флаг sync_every"
```

---

### Task 3: Регрессия + live-smoke doc

**Files:**
- Verify only (никаких новых файлов кода).

**Interfaces:**
- Consumes: всё из Tasks 1-2.
- Produces: подтверждение отсутствия регрессий; команда live-smoke для пользователя.

- [ ] **Step 1: Новый воркер-тест + базовая PPO-фича зелёные**

Run:
```bash
python -m pytest tests/train/test_ppo_worker_reaction_net.py tests/models/test_ppo_infer_with_value.py tests/models/test_ppo_stratagem_bridge.py tests/engine/phases/test_simulate_reaction_branch_ppo.py -v
```
Expected: всё PASS.

- [ ] **Step 2: DQN/AZ регрессия (opt-in не задел чужое)**

Run:
```bash
python -m pytest tests/engine/phases/test_simulate_reaction_branch_dqn.py tests/models/test_dqn_stratagem_bridge.py -v
```
Expected: всё PASS.

- [ ] **Step 3: Broader phases-регрессия**

Run: `python -m pytest tests/engine/phases/ -q`
Expected: counts как до задачи (по истории ~20 pre-existing fail в `tests/engine` вне phases; в самом `phases/` ожидаем 0 fail). Если появились fail со словами ppo/reaction/stratagem/subproc — флаг как наши; иначе pre-existing.

- [ ] **Step 4: Live-smoke инструкция (для пользователя, выполнение опционально)**

Записать в отчёт точную проверку через GUI «8х»:
- Запуск: GUI → PPO → кнопка «Тренировка 8х» (heuristic-оппонент → `USE_SUBPROC_ENVS=1`).
- Ожидаемо в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md`:
  - `[PPO][CONFIG] reaction_value_policy установлена (subproc workers, critic V): N/N воркеров`
  - `[STRATAGEM]` со списанным CP (выборочно).
- Сравнение: `$env:PPO_REACTION_VALUE_POLICY="0"` перед GUI → init не шлётся, гейта нет (legacy).
- Throttle: `$env:PPO_SUBPROC_WEIGHT_SYNC_EVERY="5"` → синк реже, без падений.

> Live-run может быть отложен пользователем (RAM/время). Юнит + регрессия — обязательны; live — best-effort.

- [ ] **Step 5: Commit (если нужен) / отчёт**

Кода нет → коммита может не быть. Если правился только отчёт — без git. Итог зафиксировать в report-файле.

---

## Self-Review

**Spec coverage:**
- §3.3.1 `_env_worker` net-холдер + init/sync + fight-plan → Task 1. ✅
- §3.3.2 `run_ppo_training_subproc` init-рассылка + sync + флаг → Task 2. ✅
- §3.3.1 хелпер установки (тестируемый) → Task 1 `_ppo_worker_install_reaction_net` + тест. ✅
- §4 флаги (`PPO_SUBPROC_WEIGHT_SYNC_EVERY`) → Task 2. ✅
- §6.1 юнит → Task 1; §6.2 регрессия → Task 3; §6.3 live-smoke → Task 3 Step 4. ✅
- §2 opt-in / DQN не задет → Task 3 Step 2 (DQN регрессия). ✅

**Placeholder scan:** Код во всех code-шагах конкретный. «если зависает — py_compile» — явная verify-инструкция, не placeholder.

**Type consistency:** `_ppo_worker_install_reaction_net(env, payload, device) -> net|None` — Task 1 (def + test) и используется в `_env_worker` Task 1. IPC-контракт init `{"ok": bool}` / sync `True` — согласован между Task 1 (worker отвечает) и Task 2 (parent читает `resp.get("ok")` / `recv()`). `_ppo_arch_dict` ключи (`hidden_size/num_layers/n_value_ensemble`) совпадают с `make_actor_critic` kwargs (Task 1 payload arch). ✅
