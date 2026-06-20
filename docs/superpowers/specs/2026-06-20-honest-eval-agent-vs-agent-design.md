# Честный eval agent-vs-agent (P1 ≡ P2 1:1) — дизайн

> **Дата:** 2026-06-20
> **Статус:** дизайн (одобрен), ждёт план реализации.
> **Связанные спеки:** [2026-06-19-ppo-smart-stratagems-design.md §4.1](2026-06-19-ppo-smart-stratagems-design.md) (both-sides путь),
> [2026-06-19-dqn-smart-stratagems-design.md](2026-06-19-dqn-smart-stratagems-design.md) (§4),
> [2026-06-20-ppo-subproc-smart-stratagems-design.md](2026-06-20-ppo-subproc-smart-stratagems-design.md).

## 0. Проблема

В текущем `eval.py` сторона «model»/P1 = learner, «enemy»/P2 = оппонент. Харнесс применяет к ним
**разный код и разные настройки** → результат сегрегирован и не отражает честное сравнение «агент против агента».
Цель — убрать сегрегацию: обе стороны должны проходить через **один и тот же код и одни и те же настройки**.

### 0.1 Аудит сегрегации (источник правды — код, ссылки на момент 2026-06-20)

**A. Путь выбора действий**

| algo | P1 / «model» (env.step) | P2 / «enemy» (enemyTurn) | расхождение |
|---|---|---|---|
| DQN | `select_action_with_epsilon` argmax+masks (`eval.py:833-842`) | `build_policy_fn` dqn argmax (`opponent_adapter.py:117-139`) | разные реализации; enemy без ε |
| PPO | `select_action_with_epsilon_ppo`, `deterministic=ε<=0` (`eval.py:285-291`) | `net.act(deterministic=True)` (`opponent_adapter.py:146-157`) | разные функции |
| AZ tree/proxy | MCTS `AZ_EVAL_MCTS_SIMS`, temp 0.06, +candidate_mode/window_nodes/joint_best_child (`eval.py:326-362`) | MCTS `AZ_EVAL_OPPONENT_MCTS_SIMS`, temp 0.10, `root_dirichlet_only`, без candidate_mode/window_nodes (`opponent_adapter.py:184-204`) | **реально разный поиск** |
| GAZ | gumbel-search `GAZ_EVAL_SIMS`, temp 0.05 (`eval.py:301-318`) | gumbel-search, без temp в run (`opponent_adapter.py:172-181`) | разные обёртки/temp |
| GMZ | `GMZ_EVAL_SIMS/TEMPERATURE`, ε-ветка (`eval.py:391-406`) | `GMZ_EVAL_OPPONENT_SIMS→fallback` (`opponent_adapter.py:268-289`) | конфиги форкнуты (fallback → совпадают по умолчанию); enemy без ε |
| SMZ | `SMZ_EVAL_NUM_SAMPLES/TEMP` (`eval.py:427-445`) | `SMZ_EVAL_OPPONENT_*→fallback` (`opponent_adapter.py:330-359`) | как GMZ |

Оппонент всегда грузится `deterministic=True` (`eval.py:1251`); learner — через ε/temperature.
`learner_side` (P1/P2) — косметика для логов (`eval.py:1433-1436`): сеть learner всегда управляет env-стороной «model».

**B. Реакции-стратагемы + fight-plan**

| algo | reaction-gate «model» | reaction-gate «enemy» | fight-plan «model» | fight-plan «enemy» |
|---|---|---|---|---|
| DQN | ✅ max-Q (`eval.py:1352-1356`) | ❌ legacy | ✅ `side="model"` (`eval.py:846-847`) | ❌ не строится |
| PPO | ✅ critic-V (`eval.py:1282-1289`) | ❌ legacy | ✅ `side="model"` (`eval.py:805-806`) | ❌ не строится |
| AZ/GAZ | ✅ value-gate (`eval.py:1299-1308`) | ❌ legacy | ✅ из MCTS (`eval.py:361`) | ❌ не отдаётся |
| GMZ | ❌ gate не ставится (`eval.py:1309-1321`) | ❌ нет | ❌ нет | ❌ нет |
| SMZ | ❌ gate не ставится (`eval.py:1322-1333`) | ❌ нет | ❌ нет | ❌ нет |

### 0.2 Корневые причины

**Общие (ядро уже двустороннее — лечится в харнессе eval):**
1. Односторонний словарь `_reaction_net_by_side = {"model": …}` (`eval.py:1286`, `1304`, и `install_dqn_stratagem_policy` → `1355`).
2. Сеть оппонента спрятана в замыкании `build_policy_fn` (`opponent_adapter.py:91-384`) → недоступна для gate.
3. Fight-plan строится только для `side="model"` (перед `env.step`), не строится перед `enemyTurn` (`eval.py:747` enemy логируется с `fight_plan=None`).
4. Два разных кодопути выбора действий с форкнутыми `*_OPPONENT_*` env и разным детерминизмом.

**Algo-специфичные:**
- DQN-bridge не side-generic: `install_dqn_stratagem_policy(env, net, device)` хардкодит `{"model": net}` (`dqn_stratagem_bridge.py:28-34`), в отличие от PPO (`ppo_stratagem_bridge.py:27-37`, принимает `net_by_side`).
- AZ enemy-поиск беднее learner-поиска (нет candidate_mode/window_nodes, другой temp).
- GMZ/SMZ без reaction-gate у обеих сторон (симметрично-legacy); fight-стратагемы не строятся.
- Единственная **движковая** асимметрия: `insane_bravery` enemy решается только из action-dict (`warhamEnv.py:4803-4804`), model — через value-gate (`warhamEnv.py:4723-4727`).

**Уже готовая инфраструктура (опора дизайна):**
- `make_stratagem_value_policy` резолвит `net_by_side.get(side)` для **любой** стороны (`reaction_value_policy.py:16-22`); `None → True` (legacy).
- Точки реакций в движке параметризованы `defender_side` (`warhamEnv.py:4233/4292/4411/4580`); apply fight-plan — `get(side)` (`warhamEnv.py:2336/6886`).
- train.py self-play AZ **уже** ставит симметрично `{"model": az_net, "enemy": az_net}` (`train.py:9031`, `9321`).

## 1. Инвариант честности

«Честно» = **харнесс применяет к обеим сторонам идентичный код и идентичные настройки** (загрузчик сети, search-конфиг, детерминизм, reaction-gate, fight-plan, obs/side). Любые различия в игре идут только из самих сетей/алгоритмов агентов, а не из eval-обвязки.

- Одинаковые algo → P1 ≡ P2 структурно (одна кодовая ветка, один конфиг).
- Разные algo → различия отражают реальные возможности алгоритмов (напр. у GMZ нет умного gate), а не привилегию стороны.

## 2. Архитектура: `EvalAgent`

Новый модуль `core/models/eval_agent.py`. Одна абстракция, которой ходят **обе** стороны.
Схлопывает 5 функций `select_action_with_epsilon_*` (`eval.py:285-445`) и 6 веток `build_policy_fn`
(`opponent_adapter.py`) в один per-algo конструктор.

### 2.1 Интерфейс

```python
@dataclass
class EvalSearchCfg:
    """Резолвится один раз из общих env-флагов; одинаков для обеих сторон."""
    algo: str
    # AZ/GAZ: sims, temperature, mode, candidate_mode, window_nodes, joint_best_child, c_puct, ...
    # GMZ/SMZ: sims/num_samples, temperature, root_top_k/sample_temperature, discount, ...
    deterministic: bool   # общий для обеих сторон (дефолт True)
    epsilon: float        # общий (дефолт 0.0)

class EvalAgent:
    algo: str
    net: nn.Module                 # policy/value net (CPU eval)
    reaction_net: nn.Module | None # value-сеть для gate (infer/infer_with_value); None у GMZ/SMZ
    search: object | None          # search-обёртка (AZ/GAZ/GMZ/SMZ) или None (DQN/PPO)
    cfg: EvalSearchCfg

    def select_action(self, env, side: str) -> tuple[dict, dict | None]:
        """Вернуть (action_dict, fight_plan|None) для полного хода стороны side.
        deterministic/epsilon берутся из self.cfg (одинаковы для обеих сторон)."""

    def as_policy_fn(self, env, side: str) -> Callable[[Any], dict]:
        """Адаптер для enemyTurn(policy_fn=…): при вызове считает действие и
        прикрепляет fight_plan к env (потребляется в fight_phase(side) этого же хода)."""
```

### 2.2 Per-algo `select_action`

| algo | действие | fight_plan |
|---|---|---|
| DQN | net forward → masked argmax → dict | `dqn_build_fight_plan(env, reaction_net, device, side=side)` если gate вкл, иначе None |
| PPO | `net.act(deterministic=cfg.deterministic)` → dict | `ppo_build_fight_plan(env, reaction_net, device, side=side)` если gate вкл, иначе None |
| AZ/GAZ | `search.run(obs, masks, env, len_model, enemy_policy_fn=None)` → action | `search.last_selected_fight_plan` (MCTS строит план для стороны через состояние env) |
| GMZ/SMZ | `search.run(obs, masks, deterministic=cfg.deterministic)` → action | None |

Сборка из чекпойнта/registry — теми же функциями, что и сейчас (`make_*`, `load_*`), вынесенными в фабрику
`build_eval_agent(algo, state_dict, contract, cfg)`. `build_policy_fn` становится тонкой обёрткой
`agent.as_policy_fn(...)` (или удаляется, а `opponent_adapter` оставляет только загрузку `OpponentSpec`).

**`enemy_policy_fn=None` для AZ/GAZ-поиска у обеих сторон** — ни один не моделирует оппонента в дереве
(симметрично; текущее поведение). Двусторонний opponent-modeling — out of scope (§10).

## 3. Поток хода (движок-runner'ы не трогаем)

Оставляем две точки входа движка — они уже симметричны внутри (реакции параметризованы `defender_side`,
apply fight-plan — `get(side)`):

- **model-ход:** `act, plan = p1.select_action(env, "model"); attach_fight_stratagem_plan(env, plan); env.step(act)`.
- **enemy-ход:** `env.enemyTurn(policy_fn=p2.as_policy_fn(env, "enemy"))`. Замыкание при вызове в начале
  `enemyTurn` (`warhamEnv.py:7234-7235`, до фаз) считает действие и прикрепляет `plan`; план потребляется
  в `fight_phase("enemy")` (`warhamEnv.py:6886`) — **зеркально** model-ходу (learner тоже строит план на
  старте хода перед `env.step`, применяет в `fight_phase("model")`).
- **Симметричный reaction-словарь:** `_reaction_net_by_side = {"model": p1.reaction_net, "enemy": p2.reaction_net}`,
  ставится один раз; `reaction_policy = make_stratagem_value_policy(_reaction_net_by_side, device=…)` включается,
  **только если хоть у одной стороны** `reaction_net is not None` (иначе оставляем `reaction_policy=None` → нулевой
  оверхед, legacy-симметрия для GMZ/SMZ).

## 4. Унификация конфига и детерминизма

- Единый `resolve_eval_search_cfg(algo, env) -> EvalSearchCfg`, который читают **обе** стороны. Форк
  `AZ_EVAL_OPPONENT_*` / `GMZ_EVAL_OPPONENT_*` / `SMZ_EVAL_OPPONENT_*` / `GAZ_EVAL_OPPONENT_*` уходит из
  честного пути: одинаковые sims/temp/mode/candidate_mode/window_nodes у обеих сторон.
- Единый `EVAL_DETERMINISTIC` (дефолт `1` → обе стороны argmax) и единый `EVAL_EPSILON` (дефолт `0`),
  применяемые идентично к обеим сторонам.
- `*_OPPONENT_*` оставляем только как **явный deprecated-override** для намеренной асимметрии,
  с предупреждением в логе `[EVAL][CONFIG][WARN] *_OPPONENT_* override активен → 1:1 нарушен`.

## 5. Движковая правка: `insane_bravery` enemy (единственная)

Только авто-путь `warhamEnv.py:4804`: зеркалим модельный блок (`warhamEnv.py:4723-4727`). Если
`reaction_policy is not None` — провести enemy-бравери через
`_should_use_stratagem("insane_bravery", "enemy", i, [i], "command", int(self.enemyCP), net=_reaction_net_by_side.get("enemy"))`;
иначе legacy `use_cp == 1 and cp_on == i`. Manual-пути (`4849`/`4895`) не трогаем.

При `reaction_policy is None` поведение не меняется → нулевой регресс-риск для существующих прогонов.

## 6. Double-header (симметрия стороны-назначения)

Режим `--swap-sides` (CLI-флаг eval): каждую пару агентов (A, B) играем двумя назначениями —
(A=model, B=enemy) и (B=model, A=enemy). **Каждое назначение — полный набор из N игр (итого 2N игр);**
бюджетный вариант (N/2 на назначение) — follow-up. Результаты тегируем по «цвету», репортим per-color
winrate + усреднённый честный итог. Свап = поменять местами `p1`/`p2` и ключи `_reaction_net_by_side`.
Roll-off attacker/defender уже рандомизирует первоход независимо от model/enemy (`eval.py:460`).

При выключенном флаге — прежнее поведение (одно назначение, `learner_side` как раньше для логов).

## 7. GMZ/SMZ — legacy-симметрично

`reaction_net = None` → reaction-gate не ставим вообще (нулевой оверхед, обе стороны жадные одинаково).
Унифицируем только action-path (через `EvalAgent` + общий конфиг). Умный gate для GMZ/SMZ — out of scope (§10).

## 8. Совместимость

- **Старые чекпойнты:** все загрузчики без изменений (`EvalAgent` использует те же `make_*`/`load_*`).
- **`install_dqn_stratagem_policy`** становится side-generic `(env, net_by_side, device)` как PPO.
  Правим 2 train.py-вызывателя (`train.py:4803`, `8322`) на `{"model": policy_net}` — поведение train не меняется.
- **Тренировочная сторона** (DQN/PPO self-play learner-only) в этом дизайне **не** меняется — отдельный follow-up (§10).
- **env-флаги:** `*_OPPONENT_*` уходят из честного пути (deprecated-override). Миграция документируется в `docs/`.
- **`LEARNER_SIDE`:** при выключенном double-header — прежняя косметика; при включённом — становится осмысленным per-color тегом.

## 9. Тесты (TDD — тест до кода)

- **Parity (страховка рефактора), по algo:** `EvalAgent.select_action` даёт то же действие, что старый
  learner-путь и старый opponent-путь при совпавшем конфиге и фиксированном seed/obs/masks.
- **Симметрия словаря:** для одинаковых algo `_reaction_net_by_side` имеет оба ключа non-None; для GMZ/SMZ —
  `reaction_policy is None`.
- **Симметрия исхода:** self-eval одной сетью в double-header → winrate ≈ 50% (стат. допуск на N играх).
- **Движок (insane_bravery):** за гардом `reaction_policy is None` существующие тесты зелёные; новый тест —
  value-net, предпочитающий «pass», не тратит enemy CP на бравери.
- **Конфиг:** `resolve_eval_search_cfg` даёт идентичный cfg для обеих сторон; `*_OPPONENT_*` override
  поднимает WARN и ломает идентичность (проверяем, что флаг работает и логируется).

## 10. Объём, файлы, риски

**Затрагиваем:**
- `core/models/eval_agent.py` — новый (фабрика + `EvalAgent` + `resolve_eval_search_cfg`).
- `eval.py` — `run_episode` и `main`: замена двух кодопутей на `EvalAgent`×2; double-header-обвязка;
  симметричный reaction-словарь; перенос трассировки/логов (они завязаны на текущую форму — переносим аккуратно).
- `core/models/opponent_adapter.py` — `build_policy_fn` → обёртка/удаление; `load_agent_opponent` остаётся.
- `core/models/dqn_stratagem_bridge.py` — `install_dqn_stratagem_policy` side-generic; `train.py` — 2 вызывателя.
- `core/envs/warhamEnv.py` — 1 точечная правка `insane_bravery` enemy (`4804`), за гардом.

**Риски:**
- Движок — низкий (одна гард-правка, поведение при `reaction_policy is None` неизменно).
- eval — средний (крупный рефактор диспетчеризации/логов), закрываем parity-тестами до правок.

## 11. Out of scope (follow-ups)

- Умный reaction value-gate для GMZ/SMZ (новая способность, не симметризация).
- Двусторонний opponent-modeling в AZ/GAZ-дереве (`enemy_policy_fn=p_other`) — намеренная не-1:1 фича.
- Both-sides reaction-gate в **train** self-play для DQN/PPO (сейчас learner-only; AZ уже both-sides).
- Полное удаление `*_OPPONENT_*` env (пока оставляем как deprecated-override).
