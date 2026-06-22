# Command Re-roll Monte-Carlo value (fight-first) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Заставить AI (DQN/PPO) реально выбирать Command Re-roll в fight-фазе через Monte-Carlo симуляцию исхода атаки в value-ветке (apply vs pass), а не слабый pre-roll value-lookahead.

**Architecture:** В value-ветке решения симулируется сама melee-атака engaged-юнита по его цели — с рероллом (apply) и без (pass), усреднение по N сэмплам, сравнение средних. Живёт в `warhamEnv`, алго-агностично через установленную `_reaction_net_by_side[side]` (DQN max-Q | PPO critic V — оба `infer_with_value`). Только fight; решение/подтип для `command_reroll` отдаётся MC, минуя слабый `_should_use_stratagem`.

**Tech Stack:** Python 3.12+, NumPy, PyTorch, Gymnasium-env (`Warhammer40kEnv`), pytest. Платформа Windows.

## Global Constraints

- **Источник дизайна:** `docs/superpowers/specs/2026-06-22-command-reroll-mc-value-design.md`.
- **Язык:** комментарии/логи/ошибки — русский; ошибка = что + где + что делать.
- **Платформа Windows**; тесты через `pytest`. Линт: после правки `.py` — `ruff check --fix <файл>` (есть PostToolUse-хук в Claude Code; вручную, если исполнитель без хука). Конфиг `ruff.toml`.
- **Только fight-фаза** (fight-first). Shooting/charge/advance MC — вне области (отдельный план). Не-fight ветка `_value_pick_command_reroll` остаётся как в Stage 4.
- **Всегда вкл (train+eval)**; гейт только по наличию `reaction_policy` + сети стороны → без них полный parity со Stage 4.
- **Не трогать `usage_limit` других стратагем; `hungry_void` и прочие сохраняют свой `apply→value` гейт** — меняется только путь `command_reroll`.
- **Конфиг:** `CMDREROLL_MC_SAMPLES` (env, дефолт 8), `CMDREROLL_MC_EPS` (env, дефолт 1e-3).
- **Baseline тестов:** `tests/engine/` имеет ~23 предсуществующих падения (не регрессии). Сверять счётчик, не «есть красные».
- **DRY/YAGNI/TDD, атомарные коммиты.** В коммит — только релевантный код.

---

## File Structure

| Файл | Ответственность | Задачи |
|------|-----------------|--------|
| `core/envs/warhamEnv.py` | `_reaction_net_value` (extract), `_simulate_fight_attack`, `_mc_value_command_reroll_fight`, fight-ветка `_value_pick_command_reroll`, MC-гейт в `_apply_pending_fight_stratagem_plan` | 1,2,4,5 |
| `core/models/dqn_stratagem_bridge.py` | пре-фильтр `command_reroll` в `dqn_build_fight_plan` | 5 |
| `core/models/ppo_stratagem_bridge.py` | пре-фильтр `command_reroll` в `ppo_build_fight_plan` | 5 |
| `core/engine/phases/stratagems.py` (или новый `core/models/...`) | конфиг-хелперы `_cmdreroll_mc_samples/eps` — **в warhamEnv** (локально) | 3 |
| `tests/models/test_command_reroll_mc_value.py` (новый) | MC-оценщик, fight-интеграция, DQN+PPO, parity, подтип | 2,4,5,6 |

Конфиг-хелперы держим module-level в `core/envs/warhamEnv.py` (рядом с прочими env-флагами), чтобы не плодить импорты.

---

## Task 1: extract `_reaction_net_value` (рефактор, без смены поведения)

**Files:** Modify `core/envs/warhamEnv.py` (`_simulate_reaction_branch` ~4263-4303). Test: существующие `tests/engine/phases/test_simulate_reaction_branch_dqn.py`, `test_simulate_reaction_branch_ppo.py`.

**Interfaces:**
- Produces: `Warhammer40kEnv._reaction_net_value(side: str, net) -> float` — value стороны: `net.infer_with_value(obs, masks_by_head)` (если есть) иначе `net.infer(obs)`; маски строятся как в `_simulate_reaction_branch`.

- [ ] **Step 1: Прогнать существующие тесты (зафиксировать зелёное до рефактора)**

Run: `pytest tests/engine/phases/test_simulate_reaction_branch_dqn.py tests/engine/phases/test_simulate_reaction_branch_ppo.py -v`
Expected: PASS (фиксируем baseline поведения).

- [ ] **Step 2: Добавить метод `_reaction_net_value` и переиспользовать его в `_simulate_reaction_branch`**

В `core/envs/warhamEnv.py` добавить метод (рядом с `_simulate_reaction_branch`):
```python
    def _reaction_net_value(self, side: str, net) -> float:
        """Value стороны от reaction-сети (DQN: masked max-Q; PPO: critic V). Без снапшота/мутаций."""
        import torch

        from core.models.action_contract import ordered_action_keys

        obs = torch.tensor(
            np.asarray([self.get_observation_for_side(side)], dtype=np.float32), dtype=torch.float32
        )
        if hasattr(net, "infer_with_value"):
            legal = self.get_legal_action_masks_by_head(side=side)
            n_units = len(self.unit_data) if side == "model" else len(self.enemy_data)
            keys = ordered_action_keys(int(n_units))
            masks_by_head = [
                torch.tensor(legal[k], dtype=torch.bool, device=obs.device).unsqueeze(0) for k in keys
            ]
            _, value = net.infer_with_value(obs, masks_by_head=masks_by_head)
        else:
            _, value = net.infer(obs)
        return float(value.reshape(-1)[0])
```
Внутри `_simulate_reaction_branch` заменить инлайн-блок вычисления value (от `import torch` до `v = float(value.reshape(-1)[0])`) на:
```python
                v = self._reaction_net_value(side, net)
```

- [ ] **Step 3: Прогнать те же тесты — поведение не изменилось**

Run: `pytest tests/engine/phases/test_simulate_reaction_branch_dqn.py tests/engine/phases/test_simulate_reaction_branch_ppo.py -v`
Expected: PASS (без изменений). Затем `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 4: Коммит**
```
git add core/envs/warhamEnv.py
git commit -m "refactor(env): extract _reaction_net_value из _simulate_reaction_branch"
```

---

## Task 2: `_simulate_fight_attack` + `_mc_value_command_reroll_fight`

**Files:** Modify `core/envs/warhamEnv.py`. Test: `tests/models/test_command_reroll_mc_value.py` (новый).

**Interfaces:**
- Consumes: `_reaction_net_value` (Task 1); `_fight_effects_for_attacker`, `_build_reroll_decider` (этапы 1–2); `_apply_stratagem` (модульный alias `apply`).
- Produces:
  - `_simulate_fight_attack(side: str, att_idx: int, def_idx: int) -> None` — симулирует melee-атаку att_idx по def_idx с активным reroll-эффектом (если есть запись), применяет урон.
  - `_mc_value_command_reroll_fight(side: str, unit_idx: int, subtype: str, samples: int) -> tuple[float, float]` — `(mean_apply, mean_pass)` по N сэмплам.

- [ ] **Step 1: Написать падающий тест (детерминированный стаб-attack + HP-aware net)**

Создать `tests/models/test_command_reroll_mc_value.py`:
```python
import torch

from tests.engine.phases._helpers import build_env


class _HpAwareNet:
    """value = -sum(HP врага стороны): меньше HP врага → выше value."""

    def __init__(self, env, side):
        self.env = env
        self.side = side

    def infer_with_value(self, obs, masks_by_head=None):
        opp = self.env.enemy_health if self.side == "model" else self.env.unit_health
        return None, torch.tensor([-float(sum(opp))])


def _engage(env):
    env.reset(options={"m": env.model, "e": env.enemy, "trunc": True})
    env.modelCP = 3
    env.stratagem_used = []
    env.active_stratagem_effects = []
    env.unit_health[0] = 6.0
    env.enemy_health[0] = 6.0
    env.unitInAttack[0] = [1, 0]
    env.enemyInAttack[0] = [1, 0]
    env._invalidate_target_cache("mc_test")


def test_mc_value_apply_beats_pass_when_reroll_adds_damage(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    # Детерминированная замена реальной атаки: при активной reroll-записи бьём сильнее.
    def fake_attack(side, att_idx, def_idx):
        dmg = 4.0 if env._command_reroll_record_exists(side, att_idx, "fight") else 1.0
        new_hp = max(0.0, float(env.enemy_health[def_idx]) - dmg)
        env._apply_health_update("enemy", def_idx, new_hp, reason="fight_sim")

    monkeypatch.setattr(env, "_simulate_fight_attack", fake_attack)
    mean_apply, mean_pass = env._mc_value_command_reroll_fight("model", 0, "wound", samples=4)
    assert mean_apply > mean_pass  # apply наносит больше урона → ниже HP врага → выше value


def test_mc_value_equal_when_reroll_no_benefit(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}

    def fake_attack(side, att_idx, def_idx):
        new_hp = max(0.0, float(env.enemy_health[def_idx]) - 1.0)  # одинаково в обеих ветках
        env._apply_health_update("enemy", def_idx, new_hp, reason="fight_sim")

    monkeypatch.setattr(env, "_simulate_fight_attack", fake_attack)
    mean_apply, mean_pass = env._mc_value_command_reroll_fight("model", 0, "wound", samples=4)
    assert mean_apply == mean_pass
```

- [ ] **Step 2: Запустить — убедиться, что падает**

Run: `pytest tests/models/test_command_reroll_mc_value.py -v`
Expected: FAIL — `AttributeError: ... has no attribute '_mc_value_command_reroll_fight'`.

- [ ] **Step 3: Реализация**

В `core/envs/warhamEnv.py` (рядом с `_value_pick_command_reroll`) добавить:
```python
    def _simulate_fight_attack(self, side: str, att_idx: int, def_idx: int) -> None:
        """Симулировать melee-атаку att_idx по def_idx (читает активный reroll-эффект), применить урон.

        Используется только в MC-симуляции (внутри snapshot/restore). reason='fight_sim'.
        """
        if side == "model":
            a_side, atk_h, atk_w, atk_d = "model", self.unit_health, self.unit_melee, self.unit_data
            d_side, def_h, def_d = "enemy", self.enemy_health, self.enemy_data
        else:
            a_side, atk_h, atk_w, atk_d = "enemy", self.enemy_health, self.enemy_melee, self.enemy_data
            d_side, def_h, def_d = "model", self.unit_health, self.unit_data
        ai, di = int(att_idx), int(def_idx)
        if not (0 <= ai < len(atk_h)) or atk_h[ai] <= 0:
            return
        if not (0 <= di < len(def_h)) or def_h[di] <= 0:
            return
        fight_effect = self._fight_effects_for_attacker(a_side, ai)
        reroll_decider = self._build_reroll_decider(a_side, ai, d_side, di)
        _dmg, mod_health = attack(
            atk_h[ai], atk_w[ai], atk_d[ai], def_h[di], def_d[di],
            rangeOfComb="Melee", effects=fight_effect, reroll_decider=reroll_decider,
        )
        self._apply_health_update(d_side, di, mod_health, reason="fight_sim")

    def _mc_value_command_reroll_fight(self, side: str, unit_idx: int, subtype: str, samples: int) -> tuple[float, float]:
        """MC-оценка реролла (subtype) для атаки engaged-юнита: (mean_apply, mean_pass).

        Для каждой ветки гоняет samples симуляций атаки (apply: реролл активен), усредняет value.
        Безопасно: (0.0, 0.0) при отсутствии сети/цели. Снапшот/restore на каждый сэмпл, recursion-guard.
        """
        net = getattr(self, "_reaction_net_by_side", {}).get(side)
        if net is None:
            return 0.0, 0.0
        in_attack = self.unitInAttack if side == "model" else self.enemyInAttack
        ui = int(unit_idx)
        if not (0 <= ui < len(in_attack)) or in_attack[ui][0] != 1:
            return 0.0, 0.0
        def_idx = int(in_attack[ui][1])
        means: dict[str, float] = {}
        for branch in ("pass", "apply"):
            vals: list[float] = []
            for _ in range(max(1, int(samples))):
                inner = self.snapshot_state()
                self._reaction_sim_active = True
                try:
                    with self.simulation_mode():
                        if branch == "apply":
                            _apply_stratagem(self, side, "command_reroll", ui, phase="fight", reroll_roll=str(subtype))
                        self._simulate_fight_attack(side, ui, def_idx)
                        vals.append(self._reaction_net_value(side, net))
                finally:
                    self._reaction_sim_active = False
                    self.restore_state(inner)
            means[branch] = sum(vals) / max(1, len(vals))
        return means["apply"], means["pass"]
```
(`attack`, `_apply_stratagem`, `np` уже импортированы в модуле.)

- [ ] **Step 4: Запустить — PASS**

Run: `pytest tests/models/test_command_reroll_mc_value.py -v`
Expected: PASS. Затем `ruff check --fix core/envs/warhamEnv.py tests/models/test_command_reroll_mc_value.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_value.py
git commit -m "feat(env): MC-оценщик value Command Re-roll для fight (_mc_value_command_reroll_fight)"
```

---

## Task 3: конфиг-хелперы `_cmdreroll_mc_samples` / `_cmdreroll_mc_eps`

**Files:** Modify `core/envs/warhamEnv.py` (module-level, рядом с прочими env-флаг-функциями). Test: `tests/models/test_command_reroll_mc_value.py`.

**Interfaces:**
- Produces (module-level): `_cmdreroll_mc_samples() -> int` (env `CMDREROLL_MC_SAMPLES`, дефолт 8, min 1); `_cmdreroll_mc_eps() -> float` (env `CMDREROLL_MC_EPS`, дефолт 1e-3).

- [ ] **Step 1: Падающий тест**
```python
def test_cmdreroll_mc_config_defaults(monkeypatch):
    import core.envs.warhamEnv as w
    monkeypatch.delenv("CMDREROLL_MC_SAMPLES", raising=False)
    monkeypatch.delenv("CMDREROLL_MC_EPS", raising=False)
    assert w._cmdreroll_mc_samples() == 8
    assert abs(w._cmdreroll_mc_eps() - 1e-3) < 1e-9
    monkeypatch.setenv("CMDREROLL_MC_SAMPLES", "3")
    monkeypatch.setenv("CMDREROLL_MC_EPS", "0.05")
    assert w._cmdreroll_mc_samples() == 3
    assert abs(w._cmdreroll_mc_eps() - 0.05) < 1e-9
```

- [ ] **Step 2: Падает.** Run: `pytest tests/models/test_command_reroll_mc_value.py::test_cmdreroll_mc_config_defaults -v` → FAIL (нет функций).

- [ ] **Step 3: Реализация** — в `core/envs/warhamEnv.py` (module-level, не метод):
```python
def _cmdreroll_mc_samples() -> int:
    try:
        return max(1, int(os.getenv("CMDREROLL_MC_SAMPLES", "8")))
    except (TypeError, ValueError):
        return 8


def _cmdreroll_mc_eps() -> float:
    try:
        return float(os.getenv("CMDREROLL_MC_EPS", "1e-3"))
    except (TypeError, ValueError):
        return 1e-3
```
(`os` уже импортирован в модуле.)

- [ ] **Step 4: PASS.** Run: `pytest tests/models/test_command_reroll_mc_value.py::test_cmdreroll_mc_config_defaults -v` → PASS. `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_value.py
git commit -m "feat(env): конфиг CMDREROLL_MC_SAMPLES/EPS"
```

---

## Task 4: интеграция MC в `_value_pick_command_reroll` (fight-ветка)

**Files:** Modify `core/envs/warhamEnv.py` (`_value_pick_command_reroll`). Test: `tests/models/test_command_reroll_mc_value.py`.

**Interfaces:**
- Consumes: `_mc_value_command_reroll_fight` (Task 2), `_cmdreroll_mc_samples/_cmdreroll_mc_eps` (Task 3).
- Produces: `_value_pick_command_reroll(side, unit_idx, "fight", rolls)` возвращает подтип с макс. `mean_apply` среди проходящих `mean_apply > mean_pass + eps`, иначе None. Не-fight фазы — прежнее Stage 4 поведение.

- [ ] **Step 1: Падающий тест (MC выбирает подтип, где выгода больше)**
```python
def test_value_pick_fight_uses_mc_and_picks_best_subtype(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False  # generic policy НЕ должен использоваться для fight

    # wound даёт больше урона, hit — нет.
    def fake_mc(side, unit_idx, subtype, samples):
        return (5.0, 1.0) if subtype == "wound" else (1.0, 1.0)

    monkeypatch.setattr(env, "_mc_value_command_reroll_fight", fake_mc)
    assert env._value_pick_command_reroll("model", 0, "fight", ("hit", "wound")) == "wound"


def test_value_pick_fight_none_when_mc_below_eps(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: True

    monkeypatch.setattr(env, "_mc_value_command_reroll_fight", lambda *a, **k: (1.0, 1.0))
    assert env._value_pick_command_reroll("model", 0, "fight", ("hit", "wound")) is None
```

- [ ] **Step 2: Падает.** Run: `pytest tests/models/test_command_reroll_mc_value.py -k value_pick_fight -v` → FAIL (текущая fight-ветка идёт через generic policy → вернёт None или не тот подтип).

- [ ] **Step 3: Реализация** — в `_value_pick_command_reroll`, после guards (policy/recursion/net/cp/record-exists), ПЕРЕД циклом по rolls вставить fight-ветку:
```python
        if str(phase) == "fight":
            samples = _cmdreroll_mc_samples()
            eps = _cmdreroll_mc_eps()
            best_roll = None
            best_apply = None
            for roll in rolls:
                mean_apply, mean_pass = self._mc_value_command_reroll_fight(side, int(unit_idx), str(roll), samples)
                if mean_apply > mean_pass + eps and (best_apply is None or mean_apply > best_apply):
                    best_apply = mean_apply
                    best_roll = roll
            return str(best_roll) if best_roll is not None else None
```
(Существующий generic-цикл по rolls остаётся ниже — для не-fight фаз.)

- [ ] **Step 4: PASS.** Run: `pytest tests/models/test_command_reroll_mc_value.py -v` → PASS. `ruff check --fix core/envs/warhamEnv.py`.

- [ ] **Step 5: Коммит**
```
git add core/envs/warhamEnv.py tests/models/test_command_reroll_mc_value.py
git commit -m "feat(env): fight-ветка _value_pick_command_reroll через MC (выбор подтипа)"
```

---

## Task 5: пре-фильтр в bridges + MC-гейт в `_apply_pending_fight_stratagem_plan`

**Files:** Modify `core/models/dqn_stratagem_bridge.py`, `core/models/ppo_stratagem_bridge.py`, `core/envs/warhamEnv.py` (`_apply_pending_fight_stratagem_plan`). Test: `tests/models/test_command_reroll_mc_value.py`, существующие `tests/models/test_dqn_stratagem_bridge.py`/`test_ppo_stratagem_bridge.py`.

**Interfaces:**
- Consumes: `_value_pick_command_reroll` (Task 4).
- Produces: `dqn_build_fight_plan`/`ppo_build_fight_plan` кладут `command_reroll` для engaged+CP юнитов без weak-гейта; `_apply_pending_fight_stratagem_plan` для `command_reroll` решает через `_value_pick_command_reroll` (MC), для colon-подтипа применяет напрямую, для прочих стратагем — прежний `_should_use_stratagem`.

- [ ] **Step 1: Падающий тест (план bridge содержит command_reroll для engaged-юнита без weak-гейта)**
```python
def test_dqn_build_fight_plan_prefilters_command_reroll():
    import torch

    from core.models.dqn_stratagem_bridge import dqn_build_fight_plan

    class _PassWinsNet:  # apply всегда хуже pass → weak-гейт отверг бы стратагему
        def infer_with_value(self, obs, masks_by_head=None):
            return None, torch.tensor([0.0])

    env = build_env()
    _engage(env)
    plan = dqn_build_fight_plan(env, _PassWinsNet(), torch.device("cpu"), side="model")
    assert plan.get(0) == "command_reroll"  # пре-фильтр кладёт несмотря на weak value
```

- [ ] **Step 2: Падает.** Run: `pytest tests/models/test_command_reroll_mc_value.py::test_dqn_build_fight_plan_prefilters_command_reroll -v` → FAIL (текущий weak-гейт `v_apply > v_pass+eps` с равными value не кладёт).

- [ ] **Step 3: Реализация**

В `dqn_build_fight_plan` ([core/models/dqn_stratagem_bridge.py:81-97](core/models/dqn_stratagem_bridge.py)) внутри `for u in range(len(health))`, сразу после проверок `health[u]<=0/in_attack/u in plan`, добавить ветку до snapshot-блока:
```python
            if d.id == "command_reroll":
                plan[u] = d.id  # пре-фильтр: финальное «да/нет» и подтип — MC в _apply_pending_fight_stratagem_plan
                continue
```
Идентичную ветку добавить в `ppo_build_fight_plan` ([core/models/ppo_stratagem_bridge.py:71-87](core/models/ppo_stratagem_bridge.py)).

В `core/envs/warhamEnv.py::_apply_pending_fight_stratagem_plan` заменить тело цикла применения (блок `_should_use_stratagem` + try/except apply) на разветвление по `command_reroll`:
```python
            sid_raw = str(sid)
            cp = self.modelCP if side == "model" else self.enemyCP
            try:
                if sid_raw.startswith("command_reroll:"):
                    _apply_stratagem(self, side, "command_reroll", ui, phase="fight", reroll_roll=sid_raw.split(":", 1)[1])
                elif sid_raw == "command_reroll":
                    roll = self._value_pick_command_reroll(side, ui, "fight", ("hit", "wound"))  # MC-гейт
                    if roll is None:
                        continue
                    _apply_stratagem(self, side, "command_reroll", ui, phase="fight", reroll_roll=roll)
                else:
                    if not self._should_use_stratagem(
                        sid_raw, side, ui, [ui], "fight", cp,
                        net=getattr(self, "_reaction_net_by_side", {}).get(side),
                    ):
                        continue
                    _apply_stratagem(self, side, sid_raw, ui, phase="fight")
            except Exception as exc:
                self._log(f"[STRATAGEM] pending fight plan: не применили {sid!r} на юните {ui}: {exc}")
```
(Удаляет прежний безусловный `_should_use_stratagem`-гейт перед apply: для `command_reroll` гейт — MC; для прочих — прежний.)

- [ ] **Step 4: PASS + регрессия bridges**

Run: `pytest tests/models/test_command_reroll_mc_value.py tests/models/test_dqn_stratagem_bridge.py tests/models/test_ppo_stratagem_bridge.py tests/engine/phases/test_windowed_fight_stratagem.py tests/models/test_eval_agent.py -v`
Expected: PASS. `ruff check --fix` по трём изменённым `.py`.

- [ ] **Step 5: Коммит**
```
git add core/models/dqn_stratagem_bridge.py core/models/ppo_stratagem_bridge.py core/envs/warhamEnv.py tests/models/test_command_reroll_mc_value.py
git commit -m "feat(ai): пре-фильтр command_reroll в bridges + MC-гейт в fight-плане"
```

---

## Task 6: e2e fight-интеграция (DQN+PPO), parity, верификация смоуком

**Files:** Test: `tests/models/test_command_reroll_mc_value.py`. Верификация — eval-смоук (наблюдательная, без кода).

**Interfaces:**
- Consumes: всё выше.

- [ ] **Step 1: Падающие тесты (fight применяет command_reroll под MC; parity без policy)**
```python
def test_fight_applies_command_reroll_under_mc(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: False
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    # MC: реролл выгоден → применяем wound.
    monkeypatch.setattr(
        env, "_mc_value_command_reroll_fight",
        lambda side, u, sub, n: (5.0, 1.0) if sub == "wound" else (1.0, 1.0),
    )
    env._apply_pending_fight_stratagem_plan("model")
    assert any(r[1] == "command_reroll" and r[3] == "fight" for r in env.stratagem_used)


def test_fight_skips_command_reroll_when_mc_negative(monkeypatch):
    env = build_env()
    _engage(env)
    env._reaction_net_by_side = {"model": _HpAwareNet(env, "model")}
    env.reaction_policy = lambda ctx: True
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    monkeypatch.setattr(env, "_mc_value_command_reroll_fight", lambda *a, **k: (1.0, 1.0))
    env._apply_pending_fight_stratagem_plan("model")
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)


def test_fight_parity_without_policy():
    env = build_env()
    _engage(env)
    # нет reaction_policy / нет _reaction_net_by_side
    env._pending_fight_stratagem_plan = {0: "command_reroll"}
    env._apply_pending_fight_stratagem_plan("model")
    assert not any(r[1] == "command_reroll" for r in env.stratagem_used)
```

- [ ] **Step 2: Запустить — убедиться, что падает (или частично)**

Run: `pytest tests/models/test_command_reroll_mc_value.py -k "fight_applies or fight_skips or fight_parity" -v`
Expected: `fight_applies` FAIL до Task 5-кода (если запускается изолированно — но Task 5 уже в дереве, поэтому здесь они скорее PASS). Если все PASS сразу — это нормально (Task 5 их закрыл); тогда тесты фиксируют поведение как регрессионные. Зафиксировать факт прогона.

- [ ] **Step 3: Доп. реализация не требуется** (поведение реализовано в Task 5; этот шаг добавляет покрытие). Если `fight_parity` падает — проверить, что без `_reaction_net_by_side` `_value_pick_command_reroll` возвращает None (guard `net is None`).

- [ ] **Step 4: Полный прогон**

Run: `pytest tests/models/ tests/engine/phases/ -q`
Expected: PASS. Затем `pytest tests/engine/ -q` → сверить: **23 failed (baseline), остальное passed** (0 новых падений). `ruff check --fix tests/models/test_command_reroll_mc_value.py`.

- [ ] **Step 5: Верификация смоуком (наблюдательная) + Коммит**

Прогнать eval-смоук с обученной моделью и проверить появление `command_reroll` в fight:
```
PYTHONIOENCODING=utf-8 PPO_REACTION_VALUE_POLICY=1 EVAL_TRACE_STYLE=warhammer \
  python eval.py --learner-agent-id P1_Necrons_only_war_v2_final_ep1000_20260621_193846 --games 5
```
Затем: `grep -i "applied=command_reroll" runtime/logs/LOGS_FOR_AGENTS_EVAL.md | head`.
Ожидаемо: ≥1 строка `[WH40K][STRATAGEM] applied=command_reroll ... phase=fight` (которой не было до изменений). Если 0 — это **сигнал** (см. open question по N/eps в спеке): поднять `CMDREROLL_MC_SAMPLES`, проверить чувствительность value-головы; **не подгонять тесты**, а разобраться.
Коммит покрытия:
```
git add tests/models/test_command_reroll_mc_value.py
git commit -m "test(ai): e2e fight Command Re-roll под MC + parity"
```

---

## Self-Review

**Spec coverage:**
- Подход B (MC resolve_trigger) — Task 2 (`_mc_value_command_reroll_fight` + `_simulate_fight_attack`). ✅
- Fight-first — все задачи ограничены fight; не-fight ветка не тронута (Task 4). ✅
- Единый DQN/PPO через `infer_with_value` — Task 1 (`_reaction_net_value`), используется обоими. ✅
- Пре-фильтр bridges (только command_reroll; hungry_void не трогаем) — Task 5. ✅
- Обход слабого `_should_use_stratagem` для command_reroll — Task 5. ✅
- Подтип через MC (фикс вырожденности) — Task 4 (выбор по max mean_apply). ✅
- Конфиг `CMDREROLL_MC_SAMPLES`/`EPS` — Task 3. ✅
- Тесты: MC-оценщик (Task 2), подтип (Task 4), интеграция DQN+PPO (Task 5/6), parity (Task 6). ✅
- Критерий готовности (command_reroll в eval-логах) — Task 6 Step 5. ✅
- Риск перфа (train-смоук) — **частично**: план не делает обязательный train-смоук-замер. Добавлено как примечание ниже; полноценный замер — после мержа (наблюдательно, env уже всегда-вкл).

**Placeholder scan:** код в шагах полный; команды и ожидаемый результат указаны. Шаг Task 6/Step 2 честно помечает, что тесты могут пройти сразу (Task 5 их закрывает) — это не placeholder, а реальная последовательность.

**Type consistency:** `_reaction_net_value(side, net)->float`; `_simulate_fight_attack(side,att,def)->None`; `_mc_value_command_reroll_fight(side,unit,subtype,samples)->(float,float)`; `_value_pick_command_reroll(...)->str|None`; `_cmdreroll_mc_samples()->int`, `_cmdreroll_mc_eps()->float` — единообразны во всех задачах.

**Примечание по перфу:** MC всегда-вкл в train (решение пользователя). После мержа — наблюдать скорость train (steps/s) на коротком прогоне; при деградации снизить `CMDREROLL_MC_SAMPLES` или ввести train-флаг отдельным мелким PR. В план не включаю замер как блокирующий шаг (требует длинного train-прогона).

---

## Execution Handoff

См. ниже выбор способа исполнения.
