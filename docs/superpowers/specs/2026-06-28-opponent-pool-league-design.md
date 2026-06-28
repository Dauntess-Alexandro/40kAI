# Дизайн: Opponent Pool / League (PFSP) для self-play

- **Дата:** 2026-06-28
- **Статус:** утверждён (brainstorming), готов к writing-plans
- **Ветка:** worktree2
- **Связанные памяти:** annihilation-training-findings, algo-allowlist-gates, heuristic-debug-flag-metrics, muzero-test-subset-ram-heavy

---

## 0. Контекст и текущее состояние кода (проверено)

RL-песочница W40k. Алгоритмы (`core/models/`): DQN, PPO, AlphaZero tree/proxy, Gumbel AZ,
Gumbel/Sampled MuZero. Точка входа — `train.py`, окружение — `core/envs/warhamEnv.py`.

**Проблема.** В self-play «сам против себя» (особенно миссия `annihilation`) обучение
схлопывается в пассивное ничейное равновесие (высокий `draw_rate`, `turn_limit`, агенты не
сближаются/не добивают). Против эвристики те же агенты играют агрессивно и выигрывают
(71–75% WR) — то есть это патология зеркального self-play (оверфит под одного оппонента +
равновесие Нэша двух идентичных политик). Точечный reward-шейпинг «иди вперёд» (variant-B)
в двух A/B сделал ХУЖЕ (camping↑, wipeouts→0, draws↑) и отвергнут. Пивот — на разнообразие
оппонента (fictitious self-play / лига, как AlphaStar).

**Что уже есть в коде:**
- Оппонент = ОДИН `OPPONENT_AGENT_ID` (env), GUI подставляет latest_snapshot / specific_agent.
  Все 5 алго грузят один спек через `opponent_adapter.load_agent_opponent(...)` и строят один
  `policy_fn` на весь прогон актора:
  - DQN `train.py:~3900`, PPO actor `train.py:5965-5972`, AZ `train.py:~6899`,
    GMZ `train.py:~8639`, SMZ `train.py:~9413`.
- Периодический snapshot-sync пересинхронит оппонента к текущему лернеру (= зеркало);
  каждая синхронизация уже СОХРАНЯЕТ агента в реестр (`save_agent_artifact`, маркер
  `[LEAGUE][SAVE]`, `train.py:5271`). В реестре уже накоплены сотни снапшотов — материал для пула есть.
- `core/engine/agent_registry.py`: `AgentIdentity`, `build_agent_id`, `save_agent_artifact`,
  `collect_registered_agents_meta`, `list_agents`, `compatible_contracts`,
  `resolve_latest_opponent_agent_id`, SMB-резолв путей (`resolve_share_models_root`,
  `agents_meta_root`).
- `core/models/opponent_adapter.py`: `load_agent_opponent` → `OpponentSpec`, `build_policy_fn`.

**Мёртвый каркас (решение: снести):**
- `core/engine/matchmaker.py` — `choose_opponent` (mirror/cross_faction/league), `record_matchup`,
  `_score_candidates`. `choose_opponent` НИГДЕ не импортируется; `record_matchup` импортирован в
  `train.py:85`, но НИ РАЗУ не вызывается.
- `train.py`: блок `SELF_PLAY_POOL_*` (`383-393`, валидация `491-504`) и `LEAGUE_ENABLE` (`542`) —
  определены/клампятся, но не читаются.
- `app/gui_qt/main.py`: вставка `LEAGUE_ENABLE` (`5884`, `6920`); `_league_matchup_summary`
  (`8566`) читает `matchups.json`, который никто не пишет.
- `tests/engine/test_matchmaker_compatibility.py` — проверяет наличие `def choose_opponent(`.

---

## 1. Цель и метрика успеха

**Цель.** Заменить single-opponent self-play на сэмплинг оппонента из
`{эвристика-анкер, исторические снапшоты}` с приоритетом PFSP (prioritized fictitious
self-play), чтобы разбить нэш-равновесие двух идентичных политик.

**Метрика успеха (A/B: пул vs зеркало, равные эпизоды и seed):**
- первичная: `draw_rate` ↓ и `turn_limit_rate` ↓ при не упавшем (или выросшем) WR против
  эвристики на eval;
- вторичная: `wipeout_enemy_rate` ↑, `ep_len_mean` ↓;
- анти-регресс: WR против фикс-эвристики не должен просесть более чем на 5 п.п.
  (защита от «забыл, как добивать»).

---

## 2. Архитектура: общий слой селекции + тонкое потребление

Три единицы, у каждой одна ответственность:

```
                ┌─────────────────────────────────────────┐
   registry  →  │  OpponentPool (core/engine/opponent_pool)│  ← stats store (PFSP winrate)
 (снапшоты)     │  • refresh_candidates() contract+side    │     opponent_pool_stats.json
                │  • sample() -> OpponentChoice            │
                │  • record_result(agent_id, win/draw/vp)  │
                └───────────────┬─────────────────────────┘
                                │ agent_id | "heuristic"
            ┌───────────────────┴───────────────────┐
            ▼ (тонкое потребление, per-algo)         ▼
   OpponentRuntimeCache                       enemyTurn(policy_fn=None)
   (agent_id -> policy_fn/net, LRU)           = встроенная эвристика
```

- **`OpponentPool`** — чистая, тестируемая логика выбора «какой `agent_id` на этот эпизод».
  **Не зависит от torch.** Единая для всех алго (требование anti-дублирования, ср. правило
  allowlist-гейтов).
- **`OpponentStatsStore`** — персист per-opponent EMA-winrate (нужно для PFSP). Один JSON.
- **`OpponentRuntimeCache`** (per-algo, тонкий) — `agent_id → потребляемый объект`. PPO:
  `build_policy_fn`. AZ/GMZ/SMZ: их net+search. LRU-кэш по `agent_id` (размер `pool_size+1`),
  чтобы ротация по эпизодам не стоила перезагрузки весов.

**Решение:** `OpponentPool` torch-free; вся работа с весами — в per-algo кэше.

---

## 3. Новый модуль `core/engine/opponent_pool.py` (API)

```python
@dataclass(frozen=True)
class PoolConfig:
    enabled: bool = False
    p_heuristic: float = 0.30      # доля эпизодов против эвристики-анкера
    pool_size: int = 8             # сколько последних совместимых снапшотов держать
    strategy: str = "pfsp"         # "pfsp" | "uniform"
    pfsp_power: float = 2.0        # вес = (1 - winrate)^power
    uniform_floor: float = 0.10    # подмешать равномерность (анти-коллапс на одного)
    novelty_bonus: float = 0.25    # доп. вес снапшотам с малым числом игр
    min_games_for_pfsp: int = 3    # пока игр меньше — winrate считаем 0.5 (нейтрально)
    ema_alpha: float = 0.15        # сглаживание winrate (свежие игры важнее)
    seed: int | None = None

@dataclass(frozen=True)
class OpponentChoice:
    kind: str        # "heuristic" | "snapshot"
    agent_id: str    # "" для heuristic
    reason: str      # "heuristic_anchor" | "pfsp" | "uniform_floor" | "novelty"
    weight: float    # для логов/диагностики

class OpponentPool:
    def __init__(self, *, learner_identity, learner_contract,
                 config: PoolConfig, stats: OpponentStatsStore,
                 rng: random.Random, log_fn=None): ...
    def refresh_candidates(self) -> list[str]: ...   # registry → фильтр contract+opponent_side → последние pool_size
    def sample(self) -> OpponentChoice: ...          # бросок heuristic vs snapshot, затем PFSP/uniform по весам
    def record_result(self, *, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None: ...
    def state_for_ui(self) -> dict: ...              # размер пула, веса/winrate по оппонентам, факт. доля эвристики
```

- `refresh_candidates` переиспользует `compatible_contracts` + `collect_registered_agents_meta`/
  `list_agents` (фильтр по стороне оппонента и контракту — как `matchmaker._entry_contract`, но без
  мёртвого scoring).
- Загрузка спека — через существующий `opponent_adapter.load_agent_opponent`.

---

## 4. Stats store + PFSP-математика

**`OpponentStatsStore`** → `artifacts/models/opponent_pool_stats.json`:
```json
{"opponents": {"<agent_id>": {"games": 12, "ema_winrate": 0.41, "draws": 5,
                              "vp_sum": -3.2, "updated_at": "..."}}}
```
- `ema_winrate ← (1-α)·ema + α·result`, где win=1.0, draw=0.5, loss=0.0.
- До `min_games_for_pfsp` отдаём 0.5 (нейтрально).
- Ключ — `opponent_agent_id` (лернер всегда «текущий»; устаревание winrate гасит EMA).

**PFSP-вес кандидата i** (winrate `wr_i` = winrate ЛЕРНЕРА против оппонента i):
```
w_i = (1 - wr_i)^pfsp_power  + (novelty_bonus, если games_i < min_games_for_pfsp)
P_i = (1 - uniform_floor) · w_i / Σw  +  uniform_floor · (1/N)
```
Смысл: чаще играем против тех, кого ПЛОХО бьём (анти-туртл-давление); `uniform_floor` не даёт
схлопнуться на одного; `novelty_bonus` форсит прогон новых снапшотов. `strategy="uniform"` ⇒
все `w_i = 1` (контроль для A/B).

**Решение:** только два режима — `pfsp` и `uniform`. Третий вариант (`pfsp_var`,
`wr·(1-wr)`) НЕ вводим (YAGNI; при необходимости добавится позже как новое значение `strategy`).

---

## 5. Точки врезки в `train.py` (тонкие, per-algo)

Сейчас оппонент строится ОДИН раз до цикла эпизодов в каждом алго (см. §0). Изменение —
одинаковый паттерн в каждом блоке:

1. До цикла: если пул включён — создать `OpponentPool` + `OpponentRuntimeCache` вместо
   одиночного спека.
2. В начале каждого эпизода (`for _ep ...`): `choice = pool.sample()`;
   `policy_fn = None if choice.kind == "heuristic" else cache.get(choice.agent_id)`.
3. После эпизода: `pool.record_result(agent_id=choice.agent_id, win=…, draw=…, vp_diff=…)`
   (исход уже считается для метрик).
4. Лог: `[POOL] ep=… kind=… agent=… reason=… weight=…`.

Если пул выключен (`enabled=0`) — путь ровно как сейчас (single `OPPONENT_AGENT_ID`), нулевая
регрессия. Snapshot-sync лернера в реестр (`train.py:5271`, `[LEAGUE][SAVE]`) не трогаем — он и
наполняет пул.

**Решение:** ротация per-episode (а не per-actor на всю жизнь). Для AZ/MuZero это смена
net+search раз в эпизод — LRU-кэш делает это дёшево (вес уже в RAM).

---

## 6. Конфиг: hyperparams + env + порядок резолва

**`hyperparams.json` — новая ГЛОБАЛЬНАЯ секция** (GUI — отдельная вкладка, конфиг общий, не per-algo):
```json
"opponent_pool": {
  "enabled": false, "p_heuristic": 0.3, "pool_size": 8,
  "strategy": "pfsp", "pfsp_power": 2.0, "uniform_floor": 0.1,
  "novelty_bonus": 0.25, "min_games_for_pfsp": 3, "ema_alpha": 0.15
}
```

**Env-флаги** (GUI их проставляет, как сейчас `SELF_PLAY_*`): `OPPONENT_POOL_ENABLED`,
`OPPONENT_POOL_P_HEURISTIC`, `OPPONENT_POOL_SIZE`, `OPPONENT_POOL_STRATEGY`,
`OPPONENT_POOL_PFSP_POWER`, `OPPONENT_POOL_UNIFORM_FLOOR`, `OPPONENT_POOL_NOVELTY_BONUS`,
`OPPONENT_POOL_MIN_GAMES`, `OPPONENT_POOL_EMA_ALPHA`.

**Резолв:** `OPPONENT_POOL_* (env) → секция opponent_pool (hyperparams) → default`. Namespace
глобальный (per-algo не нужен — слой общий), но хелпер-резолвер делаем в стиле
`resolve_az_family_env` (`core/models/az_family_env.py`) — с инъекцией `getenv` для юнит-тестов.

**Решение:** конфиг глобальный (одна секция на все алго).

---

## 7. Снос мёртвого каркаса

- Удалить `core/engine/matchmaker.py` целиком (`choose_opponent`, `OpponentPick`,
  `_score_candidates`, `record_matchup`).
- Удалить из `train.py`: импорт matchmaker (`85`), блок `SELF_PLAY_POOL_*` (`383-393`,
  валидация `491-504`), `LEAGUE_ENABLE` (`542`).
- `app/gui_qt/main.py`: убрать вставку `LEAGUE_ENABLE` (`5884`, `6920`); `_league_matchup_summary`
  (`8566`) перенаправить с `matchups.json` на новый `opponent_pool_stats.json` (теперь реально пишется).
- Удалить `tests/engine/test_matchmaker_compatibility.py`.
- `matchups.json` декоммиссится (его никто не писал).

---

## 8. Распределённый self-play (ПК1+ПК2)

- **Снапшоты:** remote-акторы уже читают реестр с SMB-шары через
  `resolve_share_models_root`/`agents_meta_root` (`agent_registry.py:112-118, 426-428`) —
  кандидаты пула видны без новой инфры.
- **PFSP-статистика (single source of truth на шаре):** лернер периодически пишет
  `opponent_pool_stats.json` в `actor_sync/`; акторы читают его по mtime — как существующий
  `opp_sync`/`latest_*.pth` polling (`train.py:5987-6015`).
- **Исходы от remote-акторов:** `opponent_agent_id` + исход пиггибекаем на rollout-сэмпл (канал
  actor→learner уже есть: `RolloutReceiver` PULL 5557 у AZ). Лернер агрегирует и переписывает
  stats-файл. Локальный (одно-процессный) режим — всё в RAM + периодический флаш.
- **Запас прочности:** если stats-файл недоступен (нет шары) — деградация к `strategy="uniform"`
  с логом `[POOL][WARN] stats unavailable → uniform`.

**Решение:** пиггибек исхода на rollout-метадату (без отдельного сокета/файла per-actor).

---

## 9. GUI: отдельная вкладка «Лига» (Qt/QML)

Новая `TacticalTabButton { text: "Лига" }` в TabBar (`Main.qml:555-561`) + страница в StackLayout.
На «Главной» в dropdown источника оппонента (`Main.qml:1909-1918`) добавить 4-й вариант
**«Пул / Лига»** → `controller._opponent_source_options += "pool"`; выбор «pool» включает
`OPPONENT_POOL_ENABLED=1` и берёт настройки со вкладки «Лига».

Мокап вкладки:
```
┌─ Лига / Opponent Pool ───────────────────────────────────────────┐
│ [✓] Включить пул оппонентов            Стратегия: (•)PFSP ( )Uniform│
│                                                                    │
│ Доля игр против эвристики p_heuristic   [====•====]  0.30          │
│ Размер пула (последних снапшотов)       [ 8  ▾]                     │
│ ── Advanced ▸ ─────────────────────────────────────────────────── │
│   PFSP power 2.0  | uniform floor 0.10 | novelty 0.25              │
│   min games 3     | EMA α 0.15                                     │
│                                                                    │
│ ┌─ Состояние пула (live) ─────────────────────────────────────┐   │
│ │ Размер: 8/8   Текущий оппонент: P2_Necrons_…_ep1450          │   │
│ │ Факт. доля эвристики: 0.29   Сэмплов: 1240                   │   │
│ │ ┌────────────────────────────────────────────────────────┐ │   │
│ │ │ agent_id            games  winrate  P(выбора)  reason   │ │   │
│ │ │ …_ep1450             54     0.38     0.21      pfsp     │ │   │
│ │ │ …_ep1300             47     0.55     0.09      pfsp     │ │   │
│ │ │ …_ep900 (new)         2      —       0.18      novelty  │ │   │
│ │ │ heuristic           300     0.71      —        anchor   │ │   │
│ │ └────────────────────────────────────────────────────────┘ │   │
│ └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```
- **В UI (видно сразу):** toggle, стратегия, `p_heuristic`, `pool_size`, таблица состояния.
- **В Advanced (свёрнуто, есть `ExpanderSection.qml`):** pfsp_power, uniform_floor, novelty_bonus,
  min_games, ema_alpha.
- **Live-состояние:** из `OpponentStatsStore` + последних `[POOL]`-строк лога (как метрики
  эвристики скрейпятся из лога). На «Главной» — компактная строка статуса
  «Лига: вкл, PFSP, эвристика 0.30, пул 8».
- QML мирроит существующий паттерн вкладок / `SectionHyperparamsEditor` / `ExpanderSection`.
  Правки только в Qt GUI (AGENTS.md).

---

## 10. Логи/диагностика

Новые маркеры:
- `[POOL][INIT] enabled=1 strategy=pfsp p_heuristic=0.30 pool_size=8 candidates=8`
- `[POOL] ep=123 kind=snapshot agent=…_ep900 reason=novelty weight=0.42` (или `kind=heuristic reason=anchor`)
- `[POOL][RESULT] agent=…_ep900 win=0 draw=1 vp=-1.5 ema_wr=0.47 games=3`
- `[POOL][REFRESH] candidates: +2 -1 (size 8)`
- `[POOL][WARN] …` (нет совместимых снапшотов → fallback heuristic; stats недоступны → uniform).

Формат логов не ломаем, добавляем строки (AGENTS.md). Доля оппонентов / winrate-таблица — из
stats store; «пул реально снизил draw» — из A/B по метрике §1.

---

## 11. План миграции с single-opponent

1. Пул по умолчанию выключен (`enabled=false`) — поведение байт-в-байт как сейчас
   (single `OPPONENT_AGENT_ID`).
2. Включение — только через GUI «источник = Пул/Лига» или env `OPPONENT_POOL_ENABLED=1`.
3. Снапшот-наполнение реестра уже работает — миграция данных не нужна.
4. Старый путь `latest_snapshot`/`specific_agent` остаётся (это «pool_size=1, p_heuristic=0»).

---

## 12. Риски

- **Стоимость ротации для AZ/MuZero** (смена net+search раз в эпизод): LRU-кэш в RAM смягчает;
  риск RAM при больших сетях — ограничить `pool_size`, LRU.
- **Контракт-несовместимость** старых снапшотов (obs/action signature) → молча выпадают из
  кандидатов; логируем, сколько отфильтровано.
- **Устаревший winrate** (лернер ушёл вперёд) → гасится EMA + `novelty_bonus`.
- **Distributed рассинхрон stats** → деградация к uniform + WARN, не падение.
- **allowlist-гейты:** добавление источника «pool» обязано пройти ВСЕ списки источников/режимов
  в GUI и train (тот же класс багов, что algo-allowlist).

---

## 13. План реализации по TDD (порядок)

1. **`OpponentStatsStore`** (чистый): EMA-апдейт, min_games→0.5, round-trip JSON. ← тест первым.
2. **`OpponentPool.sample`** с инъекцией `rng`+stats: доля эвристики ≈ `p_heuristic`; PFSP даёт
   больше веса низкому winrate; `uniform_floor`/`novelty` соблюдаются; пустой пул → heuristic.
   Детерминизм через seed.
3. **`refresh_candidates`**: фильтр по стороне+контракту, обрезка до `pool_size`, дедуп.
4. **Резолвер конфига** env→секция→default (как `resolve_az_family_env`).
5. **`OpponentRuntimeCache`**: LRU, повторный `agent_id` не перезагружает.
6. **Интеграция train (на одном алго — PPO):** пул выключен ⇒ путь не изменился; включён ⇒
   `record_result` зовётся, лог `[POOL]` пишется. Прочие алго — после зелёного PPO.
7. **GUI:** smoke на источник «pool» + env-проброс (как существующие тесты GUI train-log).

Прочие алго (DQN/AZ/GMZ/SMZ) подключаются тем же тонким паттерном после зелёного PPO — порядок
снижает риск регрессий движка (TDD по CLAUDE.md).

---

## Решённые развилки (brainstorming)

1. Судьба каркаса → **свежий модуль, мёртвый matchmaker/SELF_PLAY_POOL_*/LEAGUE_* снести**.
2. Стратегия сэмплинга → **PFSP** (приоритет по winrate) + эвристика-анкер; `uniform` как контроль.
3. Слой → **общий слой селекции + тонкое per-algo потребление**.
4. GUI → **отдельная вкладка «Лига / Opponent Pool»**.
5. Пул torch-free; конфиг глобальный; ротация per-episode; пиггибек исхода на rollout;
   третий PFSP-вариант не вводим.
