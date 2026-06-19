# B3-full — Reaction value-policy (дизайн)

> Статус: спека (brainstorming). Часть Part B (windowed self-play) после B6/B1a-c/B4.
> Связанные: `docs/superpowers/plans/2026-06-18-windowed-selfplay-part-b-phase2-prompt.md`,
> `core/engine/phases/reaction_windows.py` (Stage 8.4g, opt-in слой окон).

## 1. Цель и не-цели

**Цель.** Заменить наивное «всегда реагировать» (`reaction_policy=None` → `_should_use_reaction`
возвращает `True`) на **net-value 1-ply lookahead с резолвом триггер-действия**: для каждой
реакции движок сравнивает value реагирующей стороны при `apply` и при `pass`, досимулировав
вызвавшее реакцию взаимодействие (стрельбу/чардж), и выбирает лучшее.

Реакции в области: `go_to_ground`, `smokescreen` (Shooting), `overwatch` (Movement/Charge),
`heroic_intervention` (Charge). Все уже исполняются движком и проходят через единый seam
`Warhammer40kEnv._should_use_reaction(stratagem_id, side, chosen, candidates, phase, cp) -> bool`.

**Не-цели (явно вне B3-full).**
- Реакции НЕ становятся узлами MCTS-дерева и НЕ входят в action-space (контракт не меняется).
- Не трогаем B2 (per-unit shoot/charge) — отдельный цикл.
- Не меняем правила стратагем (только решение «использовать ли»).

## 2. Флаг и parity

- Hyperparams: `alphazero_tree.reaction_value_policy: 0|1` (дефолт **0**).
- Env: `AZ_REACTION_VALUE_POLICY` (резолв как у прочих AZ-флагов: env приоритетнее hyperparams).
- GUI: поле в секции MCTS вкладки AlphaZero Tree (как `mcts_window_nodes`), дефолт 0.
- При **0** `env.reaction_policy` не ставится → код value-policy не на пути исполнения →
  поведение и parity идентичны текущим (gate: `windowed_parity_winrate` Δ=0pp при флаге 0).

## 3. Архитектура

### 3.1 Модуль `core/models/reaction_value_policy.py`
- `make_reaction_value_policy(net_by_side, *, device, value_eval) -> Callable[[dict], bool]`.
  - `net_by_side: dict[str, net|None]` — `{"model": learner_or_opp_net, "enemy": ...}`.
  - Возвращаемый callable — это `env.reaction_policy`. Получает `ctx` (как сейчас) **плюс**
    доступ к env через замыкание/`ctx["env"]` (см. 3.3 — seam расширяется ссылкой на env и
    harness-коллбэком).
- Логика callable на одно reaction-решение:
  1. `side = ctx["side"]`; если `net_by_side.get(side) is None` → вернуть `True` (legacy: сторона
     без сети, напр. heuristic-оппонент, реагирует как раньше).
  2. Если `env._reaction_sim_active` → вернуть `True` (recursion guard, см. 3.4).
  3. `snap = env.snapshot_state()`.
  4. Для `branch in ("pass", "apply")`: `env.restore_state(snap)`;
     `v[branch] = env._simulate_reaction_branch(ctx, apply=(branch=="apply"))` (3.3).
  5. `env.restore_state(snap)`.
  6. Решение: `apply` если `v["apply"] > v["pass"] + eps` иначе `pass`
     (`eps≥0`, тай → PASS: детерминизм + экономия CP). Вернуть bool.

### 3.2 Перспектива value
- `value` берётся для **реагирующей стороны**: `net.infer(obs)` где
  `obs = env.get_observation_for_side(side)`; используем value-голову (tanh∈[-1,1]).
- Максимизируем value реагирующей стороны (выгода реакции = рост её value после резолва).

### 3.3 Simulation-harness в `warhamEnv`
- Новый метод `Warhammer40kEnv._simulate_reaction_branch(ctx, *, apply: bool) -> float`:
  - входит в `simulation_mode()` (trunc, без логов/viewer), ставит `_reaction_sim_active=True`;
  - если `apply` — применяет реакцию (тот же путь, что в реальном резолве: `_apply_stratagem`
    + установка флага эффекта, напр. benefit_of_cover), иначе пропускает;
  - **досимулирует именно триггер-взаимодействие** через извлечённый коллбэк
    `ctx["resolve_trigger"](apply)` — функцию, замкнутую на конкретный сайт реакции (3.4),
    которая прогоняет вызвавшую стрельбу/чардж по этому юниту до конца;
  - считает `value = net_by_side[side].infer(get_observation_for_side(side))`;
  - снимает флаг, выходит из `simulation_mode`; возвращает float. Снапшот/restore — снаружи (3.1).
- Извлечение «резолва взаимодействия» в переиспользуемую функцию — основная инженерная работа:
  каждый из 4 сайтов оборачивает свой блок резолва так, чтобы его можно было вызвать (а) в
  симуляции для оценки и (б) в реале для коммита выбранной ветки.

### 3.4 Per-reaction сайты и recursion guard
Сайты в `warhamEnv`:
- `_maybe_use_go_to_ground` / `_maybe_use_smokescreen` — триггер: входящая стрельба по юниту.
- `_resolve_overwatch` — триггер: движущийся вражеский юнит (overwatch-стрельба по нему).
- `_resolve_heroic_intervention` — триггер: counter-charge по зашедшему врагу.

Каждый сайт:
1. зовёт `_should_use_reaction(stratagem_id, side, chosen, candidates, phase, cp, *, resolve_trigger=...)`
   — seam **расширяется** опциональным `resolve_trigger`; внутри метод кладёт в `ctx` ещё `env=self`
   и `resolve_trigger` (при `reaction_policy=None`/legacy `resolve_trigger` игнорируется);
2. при включённом флаге `reaction_policy` = value-policy, иначе — текущее поведение;
3. исполняет выбранную ветку реально.

**Recursion guard.** На время любой branch-симуляции `env._reaction_sim_active=True`; любые
вложенные реакции в этот период возвращают legacy-default (`True`), без рекурсивного lookahead.
Гарантирует завершимость и отсутствие комбинаторного взрыва.

### 3.5 Установка политики
- Self-play actor (`alphazero_selfplay` / `_az_env_worker_entry`): при `AZ_REACTION_VALUE_POLICY=1`
  ставит `env.reaction_policy = make_reaction_value_policy({learner_side: net, opp_side: opp_net})`
  перед роллаутом. В чистом self-play обе стороны — сети.
- Eval (`eval.py`): learner-сторона → learner-net; оппонент → его сеть, либо None (heuristic) →
  legacy. Лог `[EVAL][AZ][CONFIG] reaction_value_policy=…`.
- Train-лог: добавить `reaction_value_policy={0|1}` в строку `[AZ][CONFIG]`.

## 4. Тестирование

- **Harness-юнит (детерминированные кости / fake attack):**
  - `apply`, когда cover реально снижает входящий урон и value↑ перевешивает −1 CP;
  - `pass`, когда выгоды нет (урон 0) — сеть/детерминированная оценка предпочитает экономию CP;
  - recursion guard: внутри branch-симуляции вложенная реакция не уходит в lookahead;
  - **no side-effects:** после решения `snapshot==restore` (CP, stratagem_used, health, эффекты).
- **Parity:** при флаге 0 — `windowed_parity_winrate --episodes 50 --seed 1000` Δ=0pp.
- **Регресс:** `tests/engine/phases/` + `tests/models/test_mcts_*` зелёные.
- **Smoke:** self-play 10 ep с `AZ_REACTION_VALUE_POLICY=1` без краша; в логе виден флаг.

## 5. Инкрементальная поставка (для writing-plans)

1. Флаг (hyperparams/env/GUI/train-лог) + `reaction_value_policy.py` (policy + решение) + harness-каркас
   `_simulate_reaction_branch` + recursion guard. Тест каркаса с фейковым net (value-стаб).
2. `go_to_ground` end-to-end (извлечь резолв стрельбы как `resolve_trigger`, тест apply/pass).
3. `smokescreen` (тот же триггер-резолв; тест keyword `smoke`).
4. `overwatch` (триггер — overwatch-стрельба; тест).
5. `heroic_intervention` (триггер — counter-charge; тест).
6. Self-play wiring + eval wiring + smoke + parity-гейт.

Каждый пункт = отдельный логический коммит со своим тестом (TDD).

## 6. Риски

- **Извлечение резолва взаимодействия** из inline-кода `warhamEnv` без регрессий — главный риск;
  митигейт: по одной реакции, golden-тесты, parity-гейт, флаг по умолчанию выключен.
- **Производительность:** overwatch может триггериться часто; 2 симуляции на реакцию. Митигейт:
  флаг off по умолчанию; реакции редки относительно общего числа шагов; eps-тай → PASS.
- **Вложенные simulation_mode** (реакция во время MCTS-симуляции): guard + проверка, что
  `_reaction_sim_active` корректно сбрасывается в finally.
