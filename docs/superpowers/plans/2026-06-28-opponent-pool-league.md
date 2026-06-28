# Opponent Pool / League (PFSP) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заменить single-opponent self-play на сэмплинг оппонента из {эвристика-анкер, исторические снапшоты} с приоритетом PFSP, чтобы разбить ничейное нэш-равновесие зеркального self-play.

**Architecture:** Общий torch-free слой селекции (`OpponentPool` + `OpponentStatsStore` в `core/engine/opponent_pool.py`) решает «какой agent_id на эпизод»; тонкое per-algo потребление (`OpponentRuntimeCache` + `build_pool_for_actor` в `core/models/opponent_pool_runtime.py`) строит и кэширует policy_fn/net по agent_id. Интеграция в `train.py` — одинаковый паттерн в каждом алго-блоке (PPO первым). Конфиг глобальный: env `OPPONENT_POOL_*` → секция `opponent_pool` в `hyperparams.json` → default. GUI — отдельная вкладка «Лига».

**Tech Stack:** Python 3.12+, PyTorch, pytest, PySide6 + QML (Qt GUI), Windows.

**Спека:** `docs/superpowers/specs/2026-06-28-opponent-pool-league-design.md`

## Global Constraints

- **Платформа — Windows**; команды pytest: `python -m pytest <path> -v`.
- **Python 3.12+**; новые зависимости не требуются (stdlib: `random`, `json`, `dataclasses`, `collections.OrderedDict`).
- **Язык UI/логов/ошибок — русский**; ошибки в формате «что случилось + где + что делать».
- **GUI — только Qt (PySide6/QML)** в `app/gui_qt/`; старый GUI не трогать.
- **Формат логов не ломать** — добавлять новые строки `[POOL]…` аккуратно (AGENTS.md).
- **Пул по умолчанию ВЫКЛЮЧЕН** (`enabled=false`): при выключенном пуле путь обучения обязан быть байт-в-байт как сейчас (нулевая регрессия).
- **ruff_fix хук срезает неиспользуемые импорты** — добавляй импорт вместе с использованием; реэкспорт — сразу в `__all__`.
- **allowlist-гейты:** источник «pool» обязан пройти ВСЕ списки источников оппонента в GUI и train (тот же класс багов, что algo-allowlist).
- **PFSP-семантика:** `winrate` = winrate ЛЕРНЕРА против оппонента; вес `(1 - wr)^pfsp_power`; `result`: win=1.0, draw=0.5, loss=0.0; до `min_games_for_pfsp` игр winrate=0.5 (нейтрально).

---

## File Structure

**Создаются:**
- `core/engine/opponent_pool.py` — `PoolConfig`, `OpponentChoice`, `OpponentStatsStore`, `OpponentPool`, `resolve_pool_config`. Чистая логика, без torch.
- `core/models/opponent_pool_runtime.py` — `OpponentRuntimeCache`, `build_pool_for_actor`. Тонкое потребление (torch через `opponent_adapter`).
- `tests/engine/test_opponent_stats_store.py`
- `tests/engine/test_opponent_pool.py`
- `tests/engine/test_pool_config_resolve.py`
- `tests/models/test_opponent_pool_runtime.py`
- `app/gui_qt/qml/components/LeaguePanel.qml` — содержимое вкладки «Лига».

**Модифицируются:**
- `train.py` — снос мёртвого каркаса; врезка пула в PPO/DQN/AZ/GMZ/SMZ.
- `hyperparams.json` — секция `opponent_pool`.
- `app/gui_qt/main.py` — источник «pool», env-оверрайды, redirect league-сводки.
- `app/gui_qt/qml/Main.qml` — вкладка «Лига» + 4-й пункт dropdown источника.
- `AGENTS.md` — указатель на пул (раздел про self-play/лигу).

**Удаляются:**
- `core/engine/matchmaker.py`
- `tests/engine/test_matchmaker_compatibility.py`

---

### Task 1: Снос мёртвого каркаса (matchmaker / SELF_PLAY_POOL_* / LEAGUE_*)

**Files:**
- Delete: `core/engine/matchmaker.py`
- Delete: `tests/engine/test_matchmaker_compatibility.py`
- Modify: `train.py:85` (импорт), `train.py:383-393` + `train.py:491-504` (SELF_PLAY_POOL_*), `train.py:542` (LEAGUE_ENABLE)
- Modify: `app/gui_qt/main.py:5884`, `app/gui_qt/main.py:6920` (вставка LEAGUE_ENABLE)

**Interfaces:**
- Produces: ничего нового; убирает мёртвый код, чтобы он не мешал новому модулю.

- [ ] **Step 1: Подтвердить, что код мёртвый**

Run: `python -c "import subprocess; print('ok')"` затем
Run: `grep -rn "choose_opponent\|record_matchup\|SELF_PLAY_POOL_\|LEAGUE_ENABLE" train.py core app/gui_qt`
Expected: `choose_opponent` нигде кроме `matchmaker.py`/удаляемого теста; `record_matchup` только в импорте `train.py:85`; `SELF_PLAY_POOL_*`/`LEAGUE_ENABLE` только в перечисленных строках. (Если найдётся живой вызов — остановиться и сообщить.)

- [ ] **Step 2: Удалить файлы**

```bash
git rm core/engine/matchmaker.py tests/engine/test_matchmaker_compatibility.py
```

- [ ] **Step 3: Убрать импорт matchmaker из train.py**

Удалить строку `train.py:85`:
```python
from core.engine.matchmaker import record_matchup
```

- [ ] **Step 4: Удалить блок SELF_PLAY_POOL_* и его валидацию**

Удалить в `train.py` строки `383-393` (определения `SELF_PLAY_POOL_ENABLED … SELF_PLAY_POOL_MIN_GAMES_FOR_SMART`) и строки `491-504` (их клампинг `if SELF_PLAY_POOL_SIZE < 1: …`). Удалить строку `542` `LEAGUE_ENABLE = os.getenv("LEAGUE_ENABLE", "1") == "1"`.

- [ ] **Step 5: Убрать вставку LEAGUE_ENABLE из GUI**

В `app/gui_qt/main.py` удалить строки `5884` и `6920`:
```python
env.insert("LEAGUE_ENABLE", "1")
```

- [ ] **Step 6: Проверить компиляцию и существующие тесты**

Run: `python -m py_compile train.py app/gui_qt/main.py`
Expected: без ошибок (нет ссылок на удалённое).
Run: `python -m pytest tests/engine -q`
Expected: набор зелёный/как на baseline (учти, что tests/engine на baseline частично красный — сверь счётчик с `git stash`-чистым деревом, см. память engine-test-baseline-failures; test_matchmaker_compatibility исчез — это ожидаемо).

- [ ] **Step 7: Commit**

```bash
git add -A
git commit -m "chore(selfplay): снос мёртвого каркаса matchmaker/SELF_PLAY_POOL_*/LEAGUE_*"
```

---

### Task 2: OpponentStatsStore (персист EMA-winrate)

**Files:**
- Create: `core/engine/opponent_pool.py`
- Test: `tests/engine/test_opponent_stats_store.py`

**Interfaces:**
- Produces:
  - `OpponentStatsStore(path: str, *, ema_alpha: float = 0.15)`
  - `.update(*, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None`
  - `.winrate(agent_id: str) -> float` (EMA; 0.5 если игр нет)
  - `.games(agent_id: str) -> int`
  - `.record(agent_id: str) -> dict` (копия записи: games/ema_winrate/draws/vp_sum/updated_at)
  - `.all_records() -> dict[str, dict]`
  - `.save() -> None`
  - `@classmethod .load(cls, path: str, *, ema_alpha: float = 0.15) -> OpponentStatsStore`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_opponent_stats_store.py
import os
from core.engine.opponent_pool import OpponentStatsStore


def test_unknown_agent_neutral():
    store = OpponentStatsStore(":memory:", ema_alpha=0.15)
    assert store.games("X") == 0
    assert store.winrate("X") == 0.5


def test_ema_update_win():
    store = OpponentStatsStore(":memory:", ema_alpha=0.15)
    store.update(agent_id="A", win=True, draw=False, vp_diff=3.0)
    assert store.games("A") == 1
    # ema = 0.85*0.5 + 0.15*1.0 = 0.575
    assert abs(store.winrate("A") - 0.575) < 1e-9


def test_ema_update_draw_then_loss():
    store = OpponentStatsStore(":memory:", ema_alpha=0.5)
    store.update(agent_id="A", win=False, draw=True, vp_diff=0.0)   # result 0.5 -> ema 0.5
    store.update(agent_id="A", win=False, draw=False, vp_diff=-2.0) # result 0.0 -> ema 0.25
    assert store.games("A") == 2
    assert abs(store.winrate("A") - 0.25) < 1e-9


def test_round_trip(tmp_path):
    path = os.path.join(str(tmp_path), "stats.json")
    store = OpponentStatsStore(path, ema_alpha=0.2)
    store.update(agent_id="A", win=True, draw=False, vp_diff=1.0)
    store.save()
    loaded = OpponentStatsStore.load(path, ema_alpha=0.2)
    assert loaded.games("A") == 1
    assert abs(loaded.winrate("A") - store.winrate("A")) < 1e-9
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_opponent_stats_store.py -v`
Expected: FAIL (`ModuleNotFoundError` / `ImportError: cannot import name 'OpponentStatsStore'`).

- [ ] **Step 3: Реализовать OpponentStatsStore**

```python
# core/engine/opponent_pool.py
from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

__all__ = ["OpponentStatsStore"]


def _result_value(*, win: bool, draw: bool) -> float:
    if win:
        return 1.0
    if draw:
        return 0.5
    return 0.0


class OpponentStatsStore:
    """Персист per-opponent EMA-winrate ЛЕРНЕРА против каждого оппонента.

    Хранилище: JSON {opponents: {agent_id: {games, ema_winrate, draws, vp_sum, updated_at}}}.
    path == ":memory:" => без диска (для тестов/in-process).
    """

    def __init__(self, path: str, *, ema_alpha: float = 0.15) -> None:
        self._path = str(path)
        self._alpha = float(ema_alpha)
        self._data: dict[str, dict[str, Any]] = {}

    def update(self, *, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None:
        aid = str(agent_id or "").strip()
        if not aid:
            return
        rec = self._data.get(aid)
        result = _result_value(win=win, draw=draw)
        if rec is None:
            rec = {"games": 0, "ema_winrate": 0.5, "draws": 0, "vp_sum": 0.0, "updated_at": ""}
            self._data[aid] = rec
        rec["ema_winrate"] = (1.0 - self._alpha) * float(rec["ema_winrate"]) + self._alpha * result
        rec["games"] = int(rec["games"]) + 1
        rec["draws"] = int(rec["draws"]) + (1 if draw else 0)
        rec["vp_sum"] = float(rec["vp_sum"]) + float(vp_diff)
        rec["updated_at"] = datetime.now().isoformat(timespec="seconds")

    def winrate(self, agent_id: str) -> float:
        rec = self._data.get(str(agent_id or "").strip())
        return 0.5 if rec is None else float(rec["ema_winrate"])

    def games(self, agent_id: str) -> int:
        rec = self._data.get(str(agent_id or "").strip())
        return 0 if rec is None else int(rec["games"])

    def record(self, agent_id: str) -> dict[str, Any]:
        rec = self._data.get(str(agent_id or "").strip())
        return dict(rec) if rec else {"games": 0, "ema_winrate": 0.5, "draws": 0, "vp_sum": 0.0, "updated_at": ""}

    def all_records(self) -> dict[str, dict[str, Any]]:
        return {k: dict(v) for k, v in self._data.items()}

    def save(self) -> None:
        if self._path == ":memory:":
            return
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        tmp = self._path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump({"opponents": self._data}, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp, self._path)  # атомарная запись (SMB-safe, ср. state_export.py)

    @classmethod
    def load(cls, path: str, *, ema_alpha: float = 0.15) -> "OpponentStatsStore":
        store = cls(path, ema_alpha=ema_alpha)
        if path != ":memory:" and os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as handle:
                    payload = json.load(handle)
                opp = payload.get("opponents", {}) if isinstance(payload, dict) else {}
                if isinstance(opp, dict):
                    store._data = {str(k): dict(v) for k, v in opp.items() if isinstance(v, dict)}
            except (OSError, json.JSONDecodeError):
                store._data = {}
        return store
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_opponent_stats_store.py -v`
Expected: PASS (4 теста).

- [ ] **Step 5: Commit**

```bash
git add core/engine/opponent_pool.py tests/engine/test_opponent_stats_store.py
git commit -m "feat(pool): OpponentStatsStore с EMA-winrate и атомарным персистом"
```

---

### Task 2.5: PoolConfig + resolve_pool_config + секция hyperparams

**Files:**
- Modify: `core/engine/opponent_pool.py` (добавить `PoolConfig`, `resolve_pool_config`)
- Modify: `hyperparams.json` (секция `opponent_pool`)
- Test: `tests/engine/test_pool_config_resolve.py`

**Interfaces:**
- Consumes: ничего из других задач.
- Produces:
  - `@dataclass(frozen=True) PoolConfig` с полями: `enabled: bool=False, p_heuristic: float=0.30, pool_size: int=8, strategy: str="pfsp", pfsp_power: float=2.0, uniform_floor: float=0.10, novelty_bonus: float=0.25, min_games_for_pfsp: int=3, ema_alpha: float=0.15, seed: int|None=None`
  - `resolve_pool_config(*, section: dict | None, getenv=os.getenv) -> PoolConfig` (env `OPPONENT_POOL_*` → section → default)

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_pool_config_resolve.py
from core.engine.opponent_pool import PoolConfig, resolve_pool_config


def test_defaults_when_empty():
    cfg = resolve_pool_config(section=None, getenv=lambda k: None)
    assert cfg == PoolConfig()  # все дефолты, enabled=False


def test_section_overrides_default():
    section = {"enabled": True, "p_heuristic": 0.4, "pool_size": 5, "strategy": "uniform"}
    cfg = resolve_pool_config(section=section, getenv=lambda k: None)
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.4
    assert cfg.pool_size == 5
    assert cfg.strategy == "uniform"
    assert cfg.pfsp_power == 2.0  # из дефолта


def test_env_overrides_section():
    section = {"enabled": False, "p_heuristic": 0.4, "pool_size": 5}
    env = {"OPPONENT_POOL_ENABLED": "1", "OPPONENT_POOL_P_HEURISTIC": "0.1", "OPPONENT_POOL_SIZE": "12"}
    cfg = resolve_pool_config(section=section, getenv=lambda k: env.get(k))
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.1
    assert cfg.pool_size == 12


def test_clamps_invalid_values():
    env = {"OPPONENT_POOL_SIZE": "0", "OPPONENT_POOL_P_HEURISTIC": "1.5", "OPPONENT_POOL_UNIFORM_FLOOR": "-0.2"}
    cfg = resolve_pool_config(section=None, getenv=lambda k: env.get(k))
    assert cfg.pool_size == 1          # >=1
    assert cfg.p_heuristic == 1.0      # [0,1]
    assert cfg.uniform_floor == 0.0    # [0,1]
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_pool_config_resolve.py -v`
Expected: FAIL (`cannot import name 'PoolConfig'`).

- [ ] **Step 3: Реализовать PoolConfig + resolver**

Добавить в `core/engine/opponent_pool.py` (и в `__all__`: `"PoolConfig"`, `"resolve_pool_config"`):
```python
import os
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class PoolConfig:
    enabled: bool = False
    p_heuristic: float = 0.30
    pool_size: int = 8
    strategy: str = "pfsp"          # "pfsp" | "uniform"
    pfsp_power: float = 2.0
    uniform_floor: float = 0.10
    novelty_bonus: float = 0.25
    min_games_for_pfsp: int = 3
    ema_alpha: float = 0.15
    seed: int | None = None


def _as_bool(v: Any, default: bool) -> bool:
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


def _as_float(v: Any, default: float) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _as_int(v: Any, default: int) -> int:
    try:
        return int(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)


def resolve_pool_config(*, section: dict | None, getenv: Callable[[str], str | None] = os.getenv) -> PoolConfig:
    """Резолв конфига пула: env OPPONENT_POOL_* → секция hyperparams.opponent_pool → default."""
    s = section if isinstance(section, dict) else {}
    d = PoolConfig()

    def pick(env_key: str, sect_key: str):
        ev = getenv(env_key)
        if ev is not None:
            return ev
        return s.get(sect_key)

    strategy = str(pick("OPPONENT_POOL_STRATEGY", "strategy") or d.strategy).strip().lower()
    if strategy not in {"pfsp", "uniform"}:
        strategy = d.strategy

    pool_size = max(1, _as_int(pick("OPPONENT_POOL_SIZE", "pool_size"), d.pool_size))
    seed_raw = pick("OPPONENT_POOL_SEED", "seed")
    return PoolConfig(
        enabled=_as_bool(pick("OPPONENT_POOL_ENABLED", "enabled"), d.enabled),
        p_heuristic=_clamp01(_as_float(pick("OPPONENT_POOL_P_HEURISTIC", "p_heuristic"), d.p_heuristic)),
        pool_size=pool_size,
        strategy=strategy,
        pfsp_power=max(0.0, _as_float(pick("OPPONENT_POOL_PFSP_POWER", "pfsp_power"), d.pfsp_power)),
        uniform_floor=_clamp01(_as_float(pick("OPPONENT_POOL_UNIFORM_FLOOR", "uniform_floor"), d.uniform_floor)),
        novelty_bonus=max(0.0, _as_float(pick("OPPONENT_POOL_NOVELTY_BONUS", "novelty_bonus"), d.novelty_bonus)),
        min_games_for_pfsp=max(0, _as_int(pick("OPPONENT_POOL_MIN_GAMES", "min_games_for_pfsp"), d.min_games_for_pfsp)),
        ema_alpha=_clamp01(_as_float(pick("OPPONENT_POOL_EMA_ALPHA", "ema_alpha"), d.ema_alpha)) or d.ema_alpha,
        seed=_as_int(seed_raw, 0) if seed_raw is not None else None,
    )
```
Убедиться, что в начале файла есть `from typing import Any` (он уже добавлен в Task 2 — если нет, добавить).

- [ ] **Step 4: Добавить секцию в hyperparams.json**

Добавить верхнеуровневый ключ `opponent_pool` (рядом с другими секциями, напр. после `"dqn": {...}` блока — конкретно: вставить перед закрывающей `}` файла как новый ключ):
```json
    "opponent_pool": {
        "enabled": false,
        "p_heuristic": 0.3,
        "pool_size": 8,
        "strategy": "pfsp",
        "pfsp_power": 2.0,
        "uniform_floor": 0.1,
        "novelty_bonus": 0.25,
        "min_games_for_pfsp": 3,
        "ema_alpha": 0.15
    }
```
Run: `python -c "import json; json.load(open('hyperparams.json', encoding='utf-8')); print('json ok')"`
Expected: `json ok`.

- [ ] **Step 5: Запустить тесты**

Run: `python -m pytest tests/engine/test_pool_config_resolve.py -v`
Expected: PASS (4 теста).

- [ ] **Step 6: Commit**

```bash
git add core/engine/opponent_pool.py tests/engine/test_pool_config_resolve.py hyperparams.json
git commit -m "feat(pool): PoolConfig + resolve_pool_config (env->секция->default) и секция hyperparams"
```

---

### Task 3: OpponentPool.sample (PFSP / uniform / эвристика-анкер)

**Files:**
- Modify: `core/engine/opponent_pool.py` (добавить `OpponentChoice`, `OpponentPool` с `sample`)
- Test: `tests/engine/test_opponent_pool.py`

**Interfaces:**
- Consumes: `PoolConfig`, `OpponentStatsStore` (Task 2/2.5).
- Produces:
  - `@dataclass(frozen=True) OpponentChoice(kind: str, agent_id: str, reason: str, weight: float)` — `kind ∈ {"heuristic","snapshot"}`
  - `OpponentPool(*, learner_identity, learner_contract, config: PoolConfig, stats: OpponentStatsStore, rng: random.Random, candidate_provider: Callable[[], list[dict]] | None = None, log_fn=None)`
  - `.set_candidates(ids: list[str]) -> None` (для тестов/прямой подстановки)
  - `.sample() -> OpponentChoice`
  - внутренний `._weights(ids) -> tuple[list[float], list[str]]`

- [ ] **Step 1: Написать падающий тест**

```python
# tests/engine/test_opponent_pool.py
import random
from core.engine.opponent_pool import OpponentPool, OpponentStatsStore, PoolConfig


def _pool(cfg, *, candidates, stats=None, seed=0):
    stats = stats or OpponentStatsStore(":memory:", ema_alpha=cfg.ema_alpha)
    pool = OpponentPool(
        learner_identity=None, learner_contract={}, config=cfg,
        stats=stats, rng=random.Random(seed),
        candidate_provider=lambda: [{"agent_id": a, "side": "P2", "contract": {}} for a in candidates],
    )
    pool.set_candidates(candidates)
    return pool


def test_empty_pool_always_heuristic():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0)
    pool = _pool(cfg, candidates=[])
    assert all(pool.sample().kind == "heuristic" for _ in range(20))


def test_p_heuristic_one_always_heuristic():
    cfg = PoolConfig(enabled=True, p_heuristic=1.0)
    pool = _pool(cfg, candidates=["A", "B"])
    assert all(pool.sample().kind == "heuristic" for _ in range(20))


def test_pfsp_prefers_low_winrate():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", pfsp_power=2.0,
                     uniform_floor=0.0, min_games_for_pfsp=1)
    stats = OpponentStatsStore(":memory:")
    # A: проигрываем (wr низкий) -> должен выбираться чаще; B: уверенно бьём
    for _ in range(20):
        stats.update(agent_id="A", win=False, draw=False, vp_diff=-1.0)
        stats.update(agent_id="B", win=True, draw=False, vp_diff=1.0)
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", pfsp_power=2.0,
                     uniform_floor=0.0, min_games_for_pfsp=1, ema_alpha=0.3)
    pool = _pool(cfg, candidates=["A", "B"], stats=stats, seed=42)
    picks = [pool.sample().agent_id for _ in range(400)]
    assert picks.count("A") > picks.count("B") * 2


def test_uniform_strategy_balanced():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="uniform", seed=1)
    pool = _pool(cfg, candidates=["A", "B"], seed=1)
    picks = [pool.sample().agent_id for _ in range(400)]
    assert 0.35 < picks.count("A") / 400 < 0.65


def test_novelty_reason_for_unseen():
    cfg = PoolConfig(enabled=True, p_heuristic=0.0, strategy="pfsp", min_games_for_pfsp=3)
    pool = _pool(cfg, candidates=["NEW"])
    choice = pool.sample()
    assert choice.kind == "snapshot"
    assert choice.reason == "novelty"
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_opponent_pool.py -v`
Expected: FAIL (`cannot import name 'OpponentPool'`).

- [ ] **Step 3: Реализовать OpponentChoice + OpponentPool.sample/_weights/set_candidates**

Добавить в `core/engine/opponent_pool.py` (и в `__all__`: `"OpponentChoice"`, `"OpponentPool"`):
```python
import random


@dataclass(frozen=True)
class OpponentChoice:
    kind: str          # "heuristic" | "snapshot"
    agent_id: str
    reason: str        # "heuristic_anchor" | "pfsp" | "uniform_floor" | "novelty"
    weight: float


class OpponentPool:
    def __init__(self, *, learner_identity, learner_contract, config: PoolConfig,
                 stats: OpponentStatsStore, rng: random.Random,
                 candidate_provider: Callable[[], list[dict]] | None = None, log_fn=None) -> None:
        self.learner_identity = learner_identity
        self.learner_contract = dict(learner_contract or {})
        self.config = config
        self.stats = stats
        self._rng = rng
        self._provider = candidate_provider
        self._log = log_fn
        self._candidates: list[str] = []

    def set_candidates(self, ids: list[str]) -> None:
        self._candidates = [str(a) for a in ids if str(a or "").strip()]

    def _weights(self, ids: list[str]) -> tuple[list[float], list[str]]:
        cfg = self.config
        base: list[float] = []
        reasons: list[str] = []
        if cfg.strategy == "uniform":
            for _ in ids:
                base.append(1.0)
                reasons.append("uniform_floor")
        else:  # pfsp
            for aid in ids:
                if self.stats.games(aid) < cfg.min_games_for_pfsp:
                    base.append((1.0 - 0.5) ** cfg.pfsp_power + cfg.novelty_bonus)
                    reasons.append("novelty")
                else:
                    wr = self.stats.winrate(aid)
                    base.append((1.0 - wr) ** cfg.pfsp_power)
                    reasons.append("pfsp")
        n = len(ids)
        total = sum(base) or 1.0
        floor = cfg.uniform_floor
        probs = [(1.0 - floor) * (b / total) + floor * (1.0 / n) for b in base]
        return probs, reasons

    def sample(self) -> OpponentChoice:
        ids = list(self._candidates)
        if not ids:
            return OpponentChoice("heuristic", "", "heuristic_anchor", 1.0)
        if self._rng.random() < self.config.p_heuristic:
            return OpponentChoice("heuristic", "", "heuristic_anchor", self.config.p_heuristic)
        probs, reasons = self._weights(ids)
        r = self._rng.random()
        acc = 0.0
        idx = len(ids) - 1
        for i, p in enumerate(probs):
            acc += p
            if r <= acc:
                idx = i
                break
        return OpponentChoice("snapshot", ids[idx], reasons[idx], probs[idx])
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_opponent_pool.py -v`
Expected: PASS (5 тестов).

- [ ] **Step 5: Commit**

```bash
git add core/engine/opponent_pool.py tests/engine/test_opponent_pool.py
git commit -m "feat(pool): OpponentPool.sample (PFSP/uniform + эвристика-анкер + novelty)"
```

---

### Task 4: OpponentPool.refresh_candidates / record_result / state_for_ui

**Files:**
- Modify: `core/engine/opponent_pool.py`
- Test: `tests/engine/test_opponent_pool.py` (дописать)

**Interfaces:**
- Consumes: `agent_registry.compatible_contracts`, `agent_registry.AgentIdentity` (для стороны оппонента).
- Produces:
  - `.refresh_candidates() -> list[str]` — через `candidate_provider`: фильтр side==opponent_side + `compatible_contracts(learner_contract, contract)`, обрезка до `pool_size` (новые первыми), дедуп по agent_id. Сохраняет в `self._candidates`.
  - `.record_result(*, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None` — делегирует `stats.update`.
  - `.state_for_ui() -> dict` — `{pool_size, candidates: [{agent_id, games, winrate, prob, reason}], strategy, p_heuristic}`.

- [ ] **Step 1: Написать падающий тест (дописать в tests/engine/test_opponent_pool.py)**

```python
from core.engine.opponent_pool import OpponentPool


def test_refresh_filters_side_and_contract():
    learner_contract = {"ruleset_version": "r1", "obs_space_signature": "vec:10",
                        "action_space_signature": "heads:3,3"}
    same = dict(learner_contract)
    bad = dict(learner_contract, obs_space_signature="vec:999")
    provided = [
        {"agent_id": "p2_new", "side": "P2", "contract": same, "created_at": "2026-06-28T10:00:00"},
        {"agent_id": "p2_old", "side": "P2", "contract": same, "created_at": "2026-06-01T10:00:00"},
        {"agent_id": "p1_self", "side": "P1", "contract": same, "created_at": "2026-06-28T11:00:00"},
        {"agent_id": "p2_incompat", "side": "P2", "contract": bad, "created_at": "2026-06-28T12:00:00"},
    ]
    import random
    from core.engine.agent_registry import AgentIdentity
    from core.engine.opponent_pool import OpponentStatsStore, PoolConfig
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="Necrons"),
        learner_contract=learner_contract,
        config=PoolConfig(enabled=True, pool_size=8),
        stats=OpponentStatsStore(":memory:"), rng=random.Random(0),
        candidate_provider=lambda: provided,
    )
    ids = pool.refresh_candidates()
    assert ids == ["p2_new", "p2_old"]  # P1 (своя сторона) и несовместимый отфильтрованы; новые первыми


def test_refresh_trims_to_pool_size():
    import random
    from core.engine.agent_registry import AgentIdentity
    from core.engine.opponent_pool import OpponentStatsStore, PoolConfig
    c = {"ruleset_version": "r", "obs_space_signature": "vec:1", "action_space_signature": "heads:1"}
    provided = [{"agent_id": f"p2_{i}", "side": "P2", "contract": c,
                 "created_at": f"2026-06-{i+1:02d}T00:00:00"} for i in range(10)]
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="X"), learner_contract=c,
        config=PoolConfig(enabled=True, pool_size=3),
        stats=OpponentStatsStore(":memory:"), rng=random.Random(0),
        candidate_provider=lambda: provided,
    )
    ids = pool.refresh_candidates()
    assert len(ids) == 3
    assert ids == ["p2_9", "p2_8", "p2_7"]  # три самых новых


def test_record_result_updates_stats():
    import random
    from core.engine.agent_registry import AgentIdentity
    from core.engine.opponent_pool import OpponentStatsStore, PoolConfig
    stats = OpponentStatsStore(":memory:")
    pool = OpponentPool(
        learner_identity=AgentIdentity(side="P1", faction="X"), learner_contract={},
        config=PoolConfig(enabled=True), stats=stats, rng=random.Random(0),
        candidate_provider=lambda: [],
    )
    pool.record_result(agent_id="A", win=True, draw=False, vp_diff=2.0)
    assert stats.games("A") == 1
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/engine/test_opponent_pool.py -k "refresh or record_result" -v`
Expected: FAIL (`AttributeError: 'OpponentPool' object has no attribute 'refresh_candidates'`).

- [ ] **Step 3: Реализовать методы**

Добавить в класс `OpponentPool` (импорт `from core.engine.agent_registry import compatible_contracts` в начале файла — вместе с использованием, чтобы ruff не срезал):
```python
    def _opponent_side(self) -> str:
        side = ""
        if self.learner_identity is not None:
            side = str(getattr(self.learner_identity, "side", "") or "").upper()
        return "P1" if side == "P2" else "P2"

    def refresh_candidates(self) -> list[str]:
        if self._provider is None:
            return list(self._candidates)
        opp_side = self._opponent_side()
        rows = self._provider() or []
        # сортировка: новые первыми (по created_at, затем agent_id)
        rows = sorted(rows, key=lambda r: (str(r.get("created_at", "")), str(r.get("agent_id", ""))), reverse=True)
        out: list[str] = []
        seen: set[str] = set()
        filtered_contract = 0
        for r in rows:
            aid = str(r.get("agent_id", "") or "").strip()
            if not aid or aid in seen:
                continue
            if str(r.get("side", "")).upper() != opp_side:
                continue
            ok, _reason = compatible_contracts(self.learner_contract, r.get("contract", {}) or {})
            if not ok:
                filtered_contract += 1
                continue
            out.append(aid)
            seen.add(aid)
            if len(out) >= self.config.pool_size:
                break
        if self._log and filtered_contract:
            self._log(f"[POOL][REFRESH] filtered_incompatible={filtered_contract} kept={len(out)}")
        self._candidates = out
        return list(out)

    def record_result(self, *, agent_id: str, win: bool, draw: bool, vp_diff: float) -> None:
        if not str(agent_id or "").strip():
            return
        self.stats.update(agent_id=agent_id, win=win, draw=draw, vp_diff=vp_diff)

    def state_for_ui(self) -> dict:
        ids = list(self._candidates)
        probs, reasons = self._weights(ids) if ids else ([], [])
        rows = []
        for i, aid in enumerate(ids):
            rows.append({
                "agent_id": aid,
                "games": self.stats.games(aid),
                "winrate": round(self.stats.winrate(aid), 4),
                "prob": round(probs[i], 4) if probs else 0.0,
                "reason": reasons[i] if reasons else "",
            })
        return {
            "pool_size": len(ids),
            "strategy": self.config.strategy,
            "p_heuristic": self.config.p_heuristic,
            "candidates": rows,
        }
```

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/engine/test_opponent_pool.py -v`
Expected: PASS (8 тестов из этого файла).

- [ ] **Step 5: Commit**

```bash
git add core/engine/opponent_pool.py tests/engine/test_opponent_pool.py
git commit -m "feat(pool): refresh_candidates (contract+side фильтр), record_result, state_for_ui"
```

---

### Task 5: OpponentRuntimeCache + build_pool_for_actor (тонкое потребление)

**Files:**
- Create: `core/models/opponent_pool_runtime.py`
- Test: `tests/models/test_opponent_pool_runtime.py`

**Interfaces:**
- Consumes: `OpponentPool`, `OpponentStatsStore`, `PoolConfig` (engine); `opponent_adapter` (только в дефолтном провайдере/билдере — лениво).
- Produces:
  - `OpponentRuntimeCache(build_fn: Callable[[str], Any], maxsize: int)` с `.get(agent_id) -> Any` (LRU, без повторной сборки).
  - `default_candidate_provider() -> list[dict]` — обёртка над `agent_registry` (agent_id/side/contract/created_at).
  - `build_pool_for_actor(*, learner_identity, learner_contract, config: PoolConfig, stats_path: str, seed: int | None, log_fn=None) -> OpponentPool | None` — `None`, если `config.enabled` False; иначе создаёт стор+пул и зовёт `refresh_candidates()`.

- [ ] **Step 1: Написать падающий тест**

```python
# tests/models/test_opponent_pool_runtime.py
from core.models.opponent_pool_runtime import OpponentRuntimeCache, build_pool_for_actor
from core.engine.opponent_pool import PoolConfig


def test_cache_builds_once_per_id():
    calls = {"n": 0}
    def build(aid):
        calls["n"] += 1
        return f"net::{aid}"
    cache = OpponentRuntimeCache(build_fn=build, maxsize=2)
    assert cache.get("A") == "net::A"
    assert cache.get("A") == "net::A"
    assert calls["n"] == 1  # повтор не пересобирает


def test_cache_lru_eviction():
    calls = {"n": 0}
    def build(aid):
        calls["n"] += 1
        return aid
    cache = OpponentRuntimeCache(build_fn=build, maxsize=2)
    cache.get("A"); cache.get("B"); cache.get("C")  # A вытеснен
    cache.get("A")  # пересборка A
    assert calls["n"] == 4


def test_build_pool_disabled_returns_none():
    cfg = PoolConfig(enabled=False)
    pool = build_pool_for_actor(learner_identity=None, learner_contract={}, config=cfg,
                                stats_path=":memory:", seed=0)
    assert pool is None
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `python -m pytest tests/models/test_opponent_pool_runtime.py -v`
Expected: FAIL (`ModuleNotFoundError: core.models.opponent_pool_runtime`).

- [ ] **Step 3: Реализовать модуль**

```python
# core/models/opponent_pool_runtime.py
from __future__ import annotations

import random
from collections import OrderedDict
from collections.abc import Callable
from typing import Any

from core.engine.opponent_pool import OpponentPool, OpponentStatsStore, PoolConfig

__all__ = ["OpponentRuntimeCache", "default_candidate_provider", "build_pool_for_actor"]


class OpponentRuntimeCache:
    """LRU-кэш agent_id -> потребляемый объект (policy_fn/net). build_fn зовётся один раз на id."""

    def __init__(self, build_fn: Callable[[str], Any], maxsize: int) -> None:
        self._build = build_fn
        self._max = max(1, int(maxsize))
        self._store: "OrderedDict[str, Any]" = OrderedDict()

    def get(self, agent_id: str) -> Any:
        aid = str(agent_id)
        if aid in self._store:
            self._store.move_to_end(aid)
            return self._store[aid]
        obj = self._build(aid)
        self._store[aid] = obj
        self._store.move_to_end(aid)
        while len(self._store) > self._max:
            self._store.popitem(last=False)
        return obj


def default_candidate_provider() -> list[dict]:
    """Кандидаты из реестра: agent_id/side/contract/created_at (для OpponentPool.refresh_candidates)."""
    from core.engine.agent_registry import collect_registered_agents_meta, list_agents

    contracts: dict[str, dict] = {}
    for entry in list_agents():
        aid = str(entry.get("agent_id", "") or "")
        cpath = entry.get("contract_path")
        if aid and cpath:
            from core.engine.agent_registry import _load_json  # type: ignore[attr-defined]

            c = _load_json(str(cpath), {})
            contracts[aid] = c if isinstance(c, dict) else {}
    rows: list[dict] = []
    for rec in collect_registered_agents_meta():
        aid = str(rec.get("agent_id", "") or "")
        rows.append({
            "agent_id": aid,
            "side": str(rec.get("side", "")).upper(),
            "created_at": str(rec.get("created_at", "")),
            "contract": contracts.get(aid, {}),
        })
    return rows


def build_pool_for_actor(*, learner_identity, learner_contract, config: PoolConfig,
                         stats_path: str, seed: int | None, log_fn=None) -> OpponentPool | None:
    if not config.enabled:
        return None
    stats = OpponentStatsStore.load(stats_path, ema_alpha=config.ema_alpha)
    pool = OpponentPool(
        learner_identity=learner_identity, learner_contract=learner_contract or {},
        config=config, stats=stats, rng=random.Random(seed),
        candidate_provider=default_candidate_provider, log_fn=log_fn,
    )
    pool.refresh_candidates()
    return pool
```
Примечание: `_load_json` — приватная, но стабильная функция `agent_registry`; если ревью против её импорта, продублировать 4-строчный json-loader локально.

- [ ] **Step 4: Запустить — убедиться, что проходит**

Run: `python -m pytest tests/models/test_opponent_pool_runtime.py -v`
Expected: PASS (3 теста).

- [ ] **Step 5: Commit**

```bash
git add core/models/opponent_pool_runtime.py tests/models/test_opponent_pool_runtime.py
git commit -m "feat(pool): OpponentRuntimeCache (LRU) + build_pool_for_actor + provider реестра"
```

---

### Task 6: Врезка пула в PPO actor (эталонный алго)

**Files:**
- Modify: `train.py` — резолв конфига на уровне модуля (рядом с `SELF_PLAY_*`, ~после `train.py:393`); PPO actor `train.py:5965-5972` (создание пула/кэша) и цикл `for _ep` `train.py:5985`+ (сэмпл на эпизод) и хвост эпизода `train.py:6159`+ (record_result).
- Test: `tests/engine/test_train_pool_wiring.py` (smoke на резолв + no-op при выключенном пуле)

**Interfaces:**
- Consumes: `resolve_pool_config`, `build_pool_for_actor`, `OpponentRuntimeCache`, `load_agent_opponent`, `build_policy_fn`, `_episode_result` (уже есть в train.py).
- Produces: рантайм-поведение — при `enabled=0` путь не меняется; при `enabled=1` оппонент ротируется per-episode + пишется `[POOL]`/`[POOL][RESULT]`.

- [ ] **Step 1: Добавить резолв POOL_CONFIG на уровне модуля train.py**

После блока `SELF_PLAY_*` (где раньше был `SELF_PLAY_POOL_*`, ~`train.py:393`) добавить:
```python
from core.engine.opponent_pool import resolve_pool_config

# HYPERPARAMS — уже загруженный dict гиперпараметров в train.py (см. место чтения hyperparams.json).
POOL_CONFIG = resolve_pool_config(section=(HYPERPARAMS.get("opponent_pool") if isinstance(HYPERPARAMS, dict) else None))
```
ЕСЛИ переменная с гиперпараметрами называется иначе — найти её: `grep -n "hyperparams.json\|json.load" train.py` и подставить корректное имя dict. Если на уровне модуля dict недоступен — резолвить из `os.environ` только: `resolve_pool_config(section=None)`.

- [ ] **Step 2: Написать smoke-тест на резолв**

```python
# tests/engine/test_train_pool_wiring.py
import os


def test_pool_config_disabled_by_default(monkeypatch):
    for k in list(os.environ):
        if k.startswith("OPPONENT_POOL_"):
            monkeypatch.delenv(k, raising=False)
    from core.engine.opponent_pool import resolve_pool_config
    cfg = resolve_pool_config(section=None)
    assert cfg.enabled is False  # дефолт — пул выключен (нулевая регрессия)


def test_pool_config_env_enable(monkeypatch):
    monkeypatch.setenv("OPPONENT_POOL_ENABLED", "1")
    monkeypatch.setenv("OPPONENT_POOL_P_HEURISTIC", "0.25")
    from core.engine.opponent_pool import resolve_pool_config
    cfg = resolve_pool_config(section=None)
    assert cfg.enabled is True
    assert cfg.p_heuristic == 0.25
```

Run: `python -m pytest tests/engine/test_train_pool_wiring.py -v`
Expected: PASS (это проверяет публичный резолвер; врезку в train проверяем компиляцией + ручным smoke).

- [ ] **Step 3: Создать пул и кэш в PPO actor (перед циклом эпизодов)**

В `train.py` после построения одиночного `opponent_policy_fn` (`5965-5972`) и `opponent_net` (`5976`) добавить:
```python
        # --- Opponent Pool (PFSP) ---
        _pool = None
        _pool_cache = None
        if int(SELF_PLAY_ENABLED) == 1 and POOL_CONFIG.enabled:
            from core.models.opponent_pool_runtime import OpponentRuntimeCache, build_pool_for_actor

            _pool = build_pool_for_actor(
                learner_identity=learner_identity,
                learner_contract=env_contract,
                config=POOL_CONFIG,
                stats_path=os.path.join(MODELS_DIR, "opponent_pool_stats.json"),
                seed=(POOL_CONFIG.seed if POOL_CONFIG.seed is not None else int(actor_idx)),
                log_fn=append_agent_log,
            )
            if _pool is not None:
                def _ppo_build_opponent(aid, _env=env, _model=model):
                    spec = load_agent_opponent(agent_id=aid, expected_contract=env_contract)
                    return build_policy_fn(env=_env, len_model=len(_model), opponent=spec, deterministic=True)

                _pool_cache = OpponentRuntimeCache(build_fn=_ppo_build_opponent, maxsize=POOL_CONFIG.pool_size + 1)
                append_agent_log(
                    f"[POOL][INIT] actor={int(actor_idx)} enabled=1 strategy={POOL_CONFIG.strategy} "
                    f"p_heuristic={POOL_CONFIG.p_heuristic:.2f} pool_size={POOL_CONFIG.pool_size} "
                    f"candidates={len(_pool.refresh_candidates())}"
                )
```
(`learner_identity` и `env_contract` уже существуют в PPO-блоке — проверить именами через `grep -n "learner_identity\|env_contract" train.py` рядом с PPO-actor; если имя контракта иное, подставить.)

- [ ] **Step 4: Сэмпл оппонента на каждый эпизод**

Внутри `for _ep in range(int(episodes)):` (`5985`), в самом начале тела, добавить:
```python
            _pool_choice = None
            if _pool is not None and _pool_cache is not None:
                _pool_choice = _pool.sample()
                opponent_policy_fn = None if _pool_choice.kind == "heuristic" else _pool_cache.get(_pool_choice.agent_id)
                append_agent_log(
                    f"[POOL] actor={int(actor_idx)} ep={ep_idx_1based} kind={_pool_choice.kind} "
                    f"agent={_pool_choice.agent_id or '-'} reason={_pool_choice.reason} weight={_pool_choice.weight:.3f}"
                )
```
Это переопределяет `opponent_policy_fn` ТОЛЬКО когда пул активен; иначе строки из `5966-5972` работают как раньше.

- [ ] **Step 5: record_result в хвосте эпизода**

В блоке «episode row» (`6151`+), после вычисления `result` и `vp_diff` (`6159`), добавить:
```python
                if _pool is not None and _pool_choice is not None and _pool_choice.kind == "snapshot":
                    _pool.record_result(
                        agent_id=_pool_choice.agent_id,
                        win=(result == "win"), draw=(result == "draw"), vp_diff=float(vp_diff),
                    )
                    _pool.stats.save()
                    append_agent_log(
                        f"[POOL][RESULT] actor={int(actor_idx)} agent={_pool_choice.agent_id} "
                        f"win={int(result=='win')} draw={int(result=='draw')} vp={int(vp_diff)} "
                        f"ema_wr={_pool.stats.winrate(_pool_choice.agent_id):.3f} games={_pool.stats.games(_pool_choice.agent_id)}"
                    )
```

- [ ] **Step 6: Проверить компиляцию и отсутствие регрессии при выключенном пуле**

Run: `python -m py_compile train.py`
Expected: без ошибок.
Run: `python -m pytest tests/engine/test_train_pool_wiring.py -v`
Expected: PASS.
Ручной smoke (короткий прогон, пул ВЫКЛ — путь как раньше): запустить тренировку через Qt GUI (источник «heuristic» или «latest_snapshot»), убедиться, что в `runtime/logs/LOGS_FOR_AGENTS_TRAIN.md` НЕТ строк `[POOL]` и обучение идёт как прежде. (Скилл `/run-40kai`.)
Ручной smoke (пул ВКЛ): env `OPPONENT_POOL_ENABLED=1`, короткий прогон → в логе есть `[POOL][INIT]`, `[POOL] … kind=…`, `[POOL][RESULT] …`; файл `artifacts/models/opponent_pool_stats.json` создаётся.

- [ ] **Step 7: Commit**

```bash
git add train.py tests/engine/test_train_pool_wiring.py
git commit -m "feat(pool): врезка PFSP-пула в PPO actor (ротация per-episode + [POOL] логи)"
```

---

### Task 7: Врезка пула в DQN/AZ/GMZ/SMZ (тот же паттерн)

**Files:**
- Modify: `train.py` — DQN `~3900`, AZ `~6899`, GMZ `~8639`, SMZ `~9413` (загрузка оппонента) + их циклы эпизодов и хвосты.

**Interfaces:**
- Consumes: те же `build_pool_for_actor`, `OpponentRuntimeCache`, `_episode_result`/исход эпизода в каждом алго.
- Produces: ротация оппонента per-episode для всех алго при `enabled=1`; при `enabled=0` — без изменений.

**Замечание по потреблению:** селекция (agent_id) общая; различается только `build_fn` кэша — он строит ровно тот объект, который алго СЕЙЧАС строит из одиночного `OPPONENT_AGENT_ID` спека. Для каждого алго найти, как используется `opponent_spec`/`opponent_policy_fn`, и обернуть это построение в `build_fn(aid)`.

- [ ] **Step 1: DQN — пул**

Рядом с `train.py:~3900` (где `load_agent_opponent(agent_id=OPPONENT_AGENT_ID, ...)`). Повторить паттерн Task 6 Step 3–5: создать `_pool`/`_pool_cache` с `build_fn`, строящим DQN-оппонента так же, как из `opponent_spec` (см. как DQN использует `opponent_spec` в своём actor-цикле — `grep -n "opponent_spec" train.py` в DQN-блоке). Сэмпл на эпизод; `record_result` в хвосте (DQN-исход: найти, как считается win/draw/vp в DQN ep-row, использовать те же значения).
Run: `python -m py_compile train.py` → без ошибок.

- [ ] **Step 2: AZ — пул**

Рядом с `train.py:~6899`. AZ грузит `opponent_spec = load_agent_opponent(...)` и строит eval-агента/policy_fn для `enemyTurn`. `build_fn(aid)` = тот же путь построения по `aid`. Сэмпл на эпизод (в self-play цикле AZ), `record_result` по исходу AZ-эпизода.
Учесть distributed AZ: если actor — remote env-worker, пул живёт в воркере; stats-путь — на SMB-шаре (`models_dir()`), запись атомарная (уже в `OpponentStatsStore.save`). Если шара недоступна — `build_pool_for_actor` поднимет пустой стор; при отсутствии кандидатов `sample()` вернёт heuristic (запас прочности).
Run: `python -m py_compile train.py` → без ошибок.

- [ ] **Step 3: GMZ — пул**

Рядом с `train.py:~8639`. Аналогично AZ (GMZ едет на схожей инфре). `build_fn` строит GMZ-оппонента по `aid`.
Run: `python -m py_compile train.py` → без ошибок.

- [ ] **Step 4: SMZ — пул**

Рядом с `train.py:~9413`. Аналогично.
Run: `python -m py_compile train.py` → без ошибок.

- [ ] **Step 5: Регрессионное ревью движка**

Запустить субагента `engine-regression-reviewer` на диффе train.py (фазы/бой/self-play/MCTS на регрессии). Исправить замечания.

- [ ] **Step 6: Smoke по каждому алго (пул ВКЛ, короткий прогон через GUI)**

Для каждого алго: короткий self-play с `OPPONENT_POOL_ENABLED=1` → в соответствующем `LOGS_FOR_AGENTS_TRAIN.md` видны `[POOL][INIT]`/`[POOL]`/`[POOL][RESULT]`, обучение не падает. (Не гонять тяжёлые MuZero-наборы pytest — память muzero-test-subset-ram-heavy; smoke через GUI.)

- [ ] **Step 7: Commit**

```bash
git add train.py
git commit -m "feat(pool): врезка PFSP-пула в DQN/AZ/GMZ/SMZ (общий слой, тонкое потребление)"
```

---

### Task 8: GUI backend — источник «pool», env-оверрайды, league-сводка

**Files:**
- Modify: `app/gui_qt/main.py` — `_opponent_source_options` (`481`), label-map (`3658`), env-override блок (`6736-6760`), `_league_matchup_summary` (`8566`); новые Qt-проперти для настроек пула + чтение `opponent_pool_stats.json`.

**Interfaces:**
- Consumes: секция `opponent_pool` из hyperparams (через существующий загрузчик гиперпараметров в main.py); `OpponentStatsStore`-формат файла.
- Produces: при выборе источника «pool» → env `OPPONENT_POOL_ENABLED=1` + `SELF_PLAY_ENABLED=1` + проброс `OPPONENT_POOL_*` из UI; league-сводка читает новый stats-файл.

- [ ] **Step 1: Добавить «pool» в список источников и label**

`app/gui_qt/main.py:481`:
```python
        self._opponent_source_options = ["heuristic", "latest_snapshot", "specific_agent", "pool"]
```
В label-map (`~3658`, где `"latest_snapshot": "Последний снапшот"`) добавить:
```python
            "pool": "Пул / Лига (PFSP)",
```
Проверить все места, где `_opponent_source` сравнивается со списком (allowlist-гейты!): `grep -n "opponent_source\|latest_snapshot\|specific_agent" app/gui_qt/main.py` — убедиться, что «pool» обработан везде, где это нужно (минимум — env-override ниже; в `mode`-резолве `3484` self-play должен включаться и для «pool»).

`app/gui_qt/main.py:3484` — расширить условие self-play:
```python
        mode = "selfplay" if self._opponent_source in {"latest_snapshot", "specific_agent", "pool"} else "train8"
```

- [ ] **Step 2: Env-оверрайды для «pool»**

В блоке `6736-6760` добавить ветку (после `specific_agent`):
```python
        elif selected_opponent_source == "pool":
            env_overrides["SELF_PLAY_ENABLED"] = "1"
            env_overrides["SELF_PLAY_OPPONENT_MODE"] = "snapshot"
            env_overrides["OPPONENT_POOL_ENABLED"] = "1"
            # bootstrap: акторам нужен хотя бы один agent_id для совместимости контракта
            if self._selected_specific_opponent_id:
                env_overrides["OPPONENT_AGENT_ID"] = self._selected_specific_opponent_id
            pool_cfg = self._opponent_pool_settings()  # dict из UI (Step 3)
            env_overrides["OPPONENT_POOL_P_HEURISTIC"] = str(pool_cfg["p_heuristic"])
            env_overrides["OPPONENT_POOL_SIZE"] = str(pool_cfg["pool_size"])
            env_overrides["OPPONENT_POOL_STRATEGY"] = str(pool_cfg["strategy"])
            env_overrides["OPPONENT_POOL_PFSP_POWER"] = str(pool_cfg["pfsp_power"])
            env_overrides["OPPONENT_POOL_UNIFORM_FLOOR"] = str(pool_cfg["uniform_floor"])
            env_overrides["OPPONENT_POOL_NOVELTY_BONUS"] = str(pool_cfg["novelty_bonus"])
            env_overrides["OPPONENT_POOL_MIN_GAMES"] = str(pool_cfg["min_games_for_pfsp"])
            env_overrides["OPPONENT_POOL_EMA_ALPHA"] = str(pool_cfg["ema_alpha"])
            env_overrides.pop("SELF_PLAY_FIXED_PATH", None)
```

- [ ] **Step 3: Qt-проперти настроек пула + getter**

Добавить поля (в `__init__`, читая из секции `opponent_pool` hyperparams с дефолтами `PoolConfig`) и Qt Property/Slot сеттеры (по образцу существующих self-play проперти, напр. `selfPlayFromCheckpoint`). Минимум: `poolEnabled`, `poolPHeuristic`, `poolSize`, `poolStrategy`, `poolPfspPower`, `poolUniformFloor`, `poolNoveltyBonus`, `poolMinGames`, `poolEmaAlpha`. Плюс агрегатор:
```python
    def _opponent_pool_settings(self) -> dict:
        return {
            "p_heuristic": float(self._pool_p_heuristic),
            "pool_size": int(self._pool_size),
            "strategy": str(self._pool_strategy),
            "pfsp_power": float(self._pool_pfsp_power),
            "uniform_floor": float(self._pool_uniform_floor),
            "novelty_bonus": float(self._pool_novelty_bonus),
            "min_games_for_pfsp": int(self._pool_min_games),
            "ema_alpha": float(self._pool_ema_alpha),
        }
```

- [ ] **Step 4: Live-состояние пула + redirect league-сводки**

Добавить getter, читающий `opponent_pool_stats.json` (формат `OpponentStatsStore`) для таблицы вкладки:
```python
    def _opponent_pool_state(self) -> dict:
        path = os.path.join(str(ARTIFACTS_MODELS_DIR), "opponent_pool_stats.json")
        if not os.path.exists(path):
            return {"opponents": {}}
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                payload = json.load(handle)
            return payload if isinstance(payload, dict) else {"opponents": {}}
        except (OSError, json.JSONDecodeError):
            return {"opponents": {}}
```
Перенаправить `_league_matchup_summary` (`8566`) на этот же файл: читать `opponents` (dict agent_id→{games, ema_winrate, draws, vp_sum}), top-3 по games, строка вида `• {aid}: games={..}, winrate={ema_winrate:.2f}, draw≈{draws/games:.2f}, vp={vp_sum/games:.2f}`. (Старое чтение `matchups.json` убрать.)

- [ ] **Step 5: Проверка**

Run: `python -m py_compile app/gui_qt/main.py`
Expected: без ошибок.
Run: `python -m pytest tests/gui -q`
Expected: зелёный/как baseline.

- [ ] **Step 6: Commit**

```bash
git add app/gui_qt/main.py
git commit -m "feat(gui): источник оппонента 'pool', env-проброс OPPONENT_POOL_*, league-сводка из stats"
```

---

### Task 9: GUI QML — вкладка «Лига»

**Files:**
- Create: `app/gui_qt/qml/components/LeaguePanel.qml`
- Modify: `app/gui_qt/qml/Main.qml` — TacticalTabButton `555-561` + StackLayout-страница; 4-й пункт в dropdown источника `1909-1918`.

**Interfaces:**
- Consumes: Qt-проперти/слоты из Task 8 (`poolEnabled`, `poolPHeuristic`, … , `controller.opponentPoolState`).
- Produces: вкладка «Лига» с настройками (toggle, стратегия, p_heuristic, pool_size, advanced) и live-таблицей состояния.

- [ ] **Step 1: Добавить вкладку в TabBar и StackLayout**

`Main.qml` после `TacticalTabButton { text: "Оценка" }` (`560`) добавить:
```qml
            TacticalTabButton { text: "Лига" }
```
В `StackLayout` (`564`) добавить соответствующую страницу последним элементом:
```qml
            LeaguePanel { /* вкладка Opponent Pool / League */ }
```
(порядок страниц StackLayout обязан совпадать с порядком кнопок — «Лига» добавлена последней в обоих местах.)

- [ ] **Step 2: Реализовать LeaguePanel.qml**

Создать `app/gui_qt/qml/components/LeaguePanel.qml`, зеркаля паттерн существующих панелей (`ExpanderSection.qml` для advanced, `StyledComboBox.qml` для стратегии, `TacticalCheckBox.qml` для toggle). Содержимое — по мокапу §9 спеки: чекбокс «Включить пул», радиогруппа/комбо стратегии (PFSP/Uniform), слайдер `p_heuristic`, спин `pool_size`, `ExpanderSection` с advanced (pfsp_power, uniform_floor, novelty_bonus, min_games, ema_alpha), и `TableView`/`ListView`, биндящийся к `controller.opponentPoolState`. Все подписи — на русском.

- [ ] **Step 3: 4-й пункт в dropdown источника на «Главной»**

Убедиться, что модель dropdown источника оппонента (`1909-1918`) берёт варианты из `controller` (которые уже включают «pool» после Task 8); если список захардкожен в QML — добавить пункт «Пул / Лига (PFSP)» со значением `pool`.

- [ ] **Step 4: Проверка запуска GUI**

Запустить Qt GUI (скилл `/run-40kai` или `verify`): вкладка «Лига» открывается, контролы меняют значения, при источнике «pool» и старте self-play в логах появляется `[POOL][INIT]`. Таблица состояния заполняется после первых `[POOL][RESULT]` (или из существующего `opponent_pool_stats.json`).
Run (опционально): `python -m pytest tests/gui -q` → как baseline.

- [ ] **Step 5: Commit**

```bash
git add app/gui_qt/qml/components/LeaguePanel.qml app/gui_qt/qml/Main.qml
git commit -m "feat(gui): вкладка 'Лига' (Opponent Pool) — настройки PFSP + live-состояние пула"
```

---

### Task 10: Документация + память

**Files:**
- Modify: `AGENTS.md` (новый раздел про Opponent Pool / League)
- Create: запись памяти `opponent-pool-league.md` + строка в `MEMORY.md`

**Interfaces:**
- Consumes: финальное поведение фичи.
- Produces: указатель для будущих сессий + метрика успеха для A/B.

- [ ] **Step 1: Раздел в AGENTS.md**

Добавить раздел «## Opponent Pool / League (PFSP, self-play)»: флаги (`OPPONENT_POOL_ENABLED`/`OPPONENT_POOL_*`, секция `opponent_pool` в hyperparams, приоритет env→секция→default), общий слой (`core/engine/opponent_pool.py`) + потребление (`core/models/opponent_pool_runtime.py`), маркеры логов `[POOL]`/`[POOL][INIT]`/`[POOL][RESULT]`/`[POOL][REFRESH]`/`[POOL][WARN]`, GUI-вкладка «Лига», stats-файл `artifacts/models/opponent_pool_stats.json` (на SMB для distributed), метрика успеха (draw_rate↓/turn_limit↓ при не упавшем WR vs эвристики; A/B пул vs зеркало).

- [ ] **Step 2: Память сессии**

Создать `C:\Users\Professional\.claude\projects\c--40kAI\memory\opponent-pool-league.md` (type: project): что построено, где флаги, метрика успеха, ссылки `[[annihilation-training-findings]]`, `[[algo-allowlist-gates]]`. Добавить строку в `MEMORY.md`.

- [ ] **Step 3: Финальная проверка набора тестов пула**

Run: `python -m pytest tests/engine/test_opponent_pool.py tests/engine/test_opponent_stats_store.py tests/engine/test_pool_config_resolve.py tests/models/test_opponent_pool_runtime.py tests/engine/test_train_pool_wiring.py -v`
Expected: всё зелёное.

- [ ] **Step 4: Commit**

```bash
git add AGENTS.md
git commit -m "docs(pool): раздел Opponent Pool / League в AGENTS.md"
```

---

## Self-Review (выполнено при написании плана)

**Покрытие спеки:**
- §2 архитектура (слой+потребление) → Task 2–5. §3 API OpponentPool → Task 3–4. §4 stats+PFSP → Task 2, 3. §5 врезка train → Task 6, 7. §6 конфиг → Task 2.5. §7 снос каркаса → Task 1. §8 distributed → Task 7 (Step 2, stats на SMB + fallback). §9 GUI вкладка → Task 8, 9. §10 логи → Task 6 (маркеры), §11 миграция (enabled=false default) → Task 2.5/6. §12 риски (контракт-фильтр, LRU, fallback) → Task 4/5/7. §13 TDD-порядок → порядок задач 2→3→4→5→6→7.
- Метрика успеха (§1) → Task 10 (документирование A/B; сам прогон A/B — отдельная исследовательская активность вне кода, как в существующих харнессах).

**Плейсхолдеры:** в новых модулях (Task 1–5) код полный. В Task 6–9 (правки больших существующих функций train.py/GUI) даны точные строки-якоря, вставляемый код и команды проверки; имена существующих переменных (`learner_identity`, `env_contract`, `result`, `vp_diff`, `ep_idx_1based`, `actor_idx`, `MODELS_DIR`, `append_agent_log`) подтверждены по коду на момент написания — при расхождении исполнитель сверяет `grep`-ом (указано в шагах).

**Согласованность типов:** `OpponentStatsStore`/`OpponentPool`/`PoolConfig`/`OpponentChoice`/`resolve_pool_config`/`OpponentRuntimeCache`/`build_pool_for_actor`/`default_candidate_provider` — имена и сигнатуры одинаковы во всех задачах и тестах. `result ∈ {"win","loss","draw"}` (из `_episode_result`), маппинг в `record_result` консистентен.
