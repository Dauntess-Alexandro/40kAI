# Track 1 · Batch #1 — структурные opt-in эффекты в `attack()` — Design

**Дата:** 2026-06-17
**Ветка:** `feat/phase-decision-windows`
**Контекст:** доработка движка под некронские стратагемы. Трек 1 = обогащение боевой математики `core/engine/utils.py::attack()` (standalone, почти чистая функция, идеальна для TDD). Трек 2 (пошаговое исполнение по окнам + agent decision surfaces) — отдельно, позже, под golden-traces.

## Цель

Обобщить параметр `effects` функции `attack()` из одной строки (`"benefit of cover"`) в **набор композируемых эффектов**, применяемых только если переданы. Добавить механики, нужные стратагемам Awakened Dynasty: ре-ролл хитов, модификатор Силы, улучшение AP. **По умолчанию поведение боя идентично** (обучение/баланс не трогаем).

## Не-цели (вне batch #1)

- `expected_damage()` (`utils.py:129`) — аналитический EV-оценщик: НЕ трогаем (отдельная задача, если понадобится симметрия EV). Это значит EV пока не учитывает новые эффекты — приемлемо: на реальный исход боя влияет `attack()`.
- Подключение эффектов к стратагемам/решениям агента — это следующие задачи (после Трека 1) и Трек 2.
- Sustained Hits / Devastating Wounds / mortal wounds / reroll-wounds — не в этом батче (YAGNI: добавляем под конкретные стратагемы Awakened Dynasty по мере надобности).
- Wound/Hit «плоские» модификаторы (+1/-1 to hit/wound) — не сейчас (Awakened Dynasty ядро их не требует; Conquering Tyrant = ре-ролл, Hungry Void = +S/AP).

## Глобальные ограничения

- Windows; Python 3.12+; тесты `python -m pytest`; ruff `py312`.
- **Инвариант:** `attack(..., effects=None)` и `attack(..., effects="benefit of cover")` дают **тот же результат, что сейчас** (при одинаковом `roller`/RNG). Все существующие вызовы (`effects` всегда `None`/`"benefit of cover"`) не меняют поведение.
- Только `core/engine/utils.py::attack()` + новый приватный нормализатор. `expected_damage` не трогаем.

## Соответствие коду

- `attack()` — `core/engine/utils.py:318-497`. Ключевые точки: `s` (`:368`), `ap` (`:372`), `cover_bonus`/`save_target` (`:375-386`), hit-роллы и счёт (`:422-443`), wound (`:445-470`), save (`:472-487`).
- `effects` сейчас сравнивается строго со строкой `"benefit of cover"` (`:375`).
- `roller(num, max, stage)` инъектируется (стадии `"hit"/"wound"/"save"`) → детерминированные тесты.

## Архитектура

### Нормализатор эффектов

Новая приватная функция в `utils.py`:

```python
def _normalize_effects(effects):
    """Привести effects к dict со стабильными ключами.

    Назад-совместимость:
      None                -> все дефолты, cover=False
      "benefit of cover"  -> cover=True
      dict                -> читаем ключи (cover|benefit_of_cover, reroll_hits, strength_mod, ap_improve)
    """
    out = {"cover": False, "reroll_hits": None, "strength_mod": 0, "ap_improve": 0}
    if effects is None:
        return out
    if isinstance(effects, str):
        if effects.strip().lower() == "benefit of cover":
            out["cover"] = True
        return out
    if isinstance(effects, dict):
        out["cover"] = bool(effects.get("cover") or effects.get("benefit_of_cover"))
        rh = effects.get("reroll_hits")
        out["reroll_hits"] = rh if rh in ("ones", "all") else None
        out["strength_mod"] = int(effects.get("strength_mod", 0) or 0)
        out["ap_improve"] = int(effects.get("ap_improve", 0) or 0)
    return out
```

### Применение в `attack()`

1. В начале: `eff = _normalize_effects(effects)`.
2. `cover_bonus = 1 if (eff["cover"] and rangeOfComb == "Ranged") else 0` (вместо строкового сравнения; поведение для `"benefit of cover"` сохраняется).
3. `s = _to_int(attackerWeapon.get("S"), default=0) + int(eff["strength_mod"])`.
4. `ap = _to_int(attackerWeapon.get("AP"), default=0) - int(eff["ap_improve"])` (улучшение AP = более отрицательный; в 10ed AP отрицательный).
5. **Ре-ролл хитов** сразу после генерации `rolls` (до подсчёта `hits`):

```python
    if eff["reroll_hits"]:
        need = []
        for idx, r in enumerate(rolls):
            r = int(r)
            if eff["reroll_hits"] == "ones" and r == 1:
                need.append(idx)
            elif eff["reroll_hits"] == "all" and r != 6 and r < bs:
                need.append(idx)
        if need:
            new = _roll_with_stage(num=len(need), stage="hit")
            new = np.array([new] if isinstance(new, int) else list(new), dtype=int)
            for j, idx in enumerate(need):
                rolls[idx] = int(new[j])
```

Существующий цикл подсчёта хитов/критов работает на обновлённом `rolls` без изменений.

### Поток данных

`effects` (None | "benefit of cover" | dict) → `_normalize_effects` → влияет на cover/S/AP/ре-ролл. При None/строке всё как раньше.

## Обработка ошибок

- Неизвестный `reroll_hits` (не "ones"/"all") → трактуется как None (без ре-ролла), не падаем.
- Нечисловой `strength_mod`/`ap_improve` → `int(... or 0)` → 0.
- `effects` неизвестного типа → дефолты (как None).

## Тест-план

`tests/engine/test_attack_effects.py` (детерминированный `roller` со стадиями):
1. **back-compat None** — `attack(effects=None)` с фикс. roller даёт тот же `dmg`, что и без параметра (cover не применяется).
2. **back-compat cover** — `effects="benefit of cover"` → `save_target` снижается на 1 (тот же эффект, что сейчас): сценарий, где разница видна (например, Sv6 → засейвить на 5+).
3. **reroll_hits="ones"** — roller на стадии hit: первый бросок `[1]`, ре-ролл `[6]` → хит есть; без ре-ролла (None) тот же первый бросок → хита нет. Сравнить число хитов/урон.
4. **reroll_hits="all"** — промах (например `[2]` при bs=4) ре-роллится в `[5]` → хит.
5. **strength_mod=+1** — S4 vs T4 ранит на 4+, S5 vs T4 — на 3+: при wound-броске `[3]` с `strength_mod=1` ранит, без — нет.
6. **ap_improve=+1** — `save_target` ухудшается на 1 (Sv4, AP0 → 4+; с ap_improve=1 → 5+): save-бросок `[4]` сейвит без эффекта, не сейвит с эффектом.
7. **normalizer unit** — `_normalize_effects(None/"benefit of cover"/dict)` возвращает ожидаемые dict.
8. **dict cover** — `effects={"cover": True}` эквивалентно строке.

Регрессия: `tests/engine/test_expected_damage.py`, `test_charge_ev.py`, `test_shoot_targets_contract_regression.py`, весь `tests/engine/phases/` (реакции зовут `attack` с `effects="benefit of cover"`/None — поведение не меняется); ruff.

## Риски

- **Изменение боевой математики ломает обучение** — митигейт: строгий behavior-neutral при None/строке (тесты 1–2 + регрессия EV/charge); новые ветки активны только при dict-effects, которые сейчас никто не передаёт.
- **Ре-ролл и счёт критов** — re-rolled 6 = крит (нормально по правилам); тест 3/4 фиксирует.
- **`expected_damage` рассинхрон** — EV не учитывает новые эффекты (вне scope); отметить как известное, выровнять при необходимости позже.
