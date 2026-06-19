# B2 — Per-unit shoot/charge (дизайн)

> Статус: спека (brainstorming). Часть Part B (windowed self-play), после B3-full.
> **Жёсткий разрыв контракта** (по решению): без флага, старые чекпойнты несовместимы.

## 1. Цель и не-цели

**Цель.** Сделать стрельбу и чардж **per-unit** в плоском (flat) action-контракте: вместо
одиночных голов `shoot`/`charge` (одна цель/rank на весь ход, общая для всех юнитов) — головы
`shoot_num_i`/`charge_num_i` на каждый модельный юнит. Это убирает lossy-ограничение
`legacy_compiler.compile_options_to_action_dict` («одна голова на ход → последняя побеждает»)
и даёт политике выбирать разные цели для разных юнитов и во flat-режиме (как уже умеет
windowed через `decide_shoot(i)`/`decide_charge`).

**Не-цели.**
- Не вводим флаг/обратную совместимость — это осознанный hard break (переобучение всех моделей).
- Не меняем семантику головы: `shoot_num_i` остаётся **rank-индексом** в списке легальных целей
  юнита i (как сейчас одиночный `shoot`), размер `Discrete(len(enemy))`. Не переходим на
  абсолютный индекс цели.
- Не трогаем `move` (уже per-unit `move_num_i`), `attack`, `use_cp`, `cp_on`.
- Не трогаем reaction-стратагемы/B3.

## 2. Контракт действий (`core/models/action_contract.py`)

- `BASE_ACTION_HEADS = ["move", "attack", "use_cp", "cp_on"]` — убрать `shoot`, `charge`.
- `ordered_action_keys(len_model)` возвращает:
  base + `move_num_0..N-1` + `shoot_num_0..N-1` + `charge_num_0..N-1` (сгруппировано по типу,
  N=len_model). Порядок фиксирован и един для env/масок/голов сетей.
- `action_sizes_from_env`, `action_tensor_to_dict`, `FactorizedLegalMasks.as_ordered_list` —
  работают по `ordered_action_keys`, кода менять не нужно (берут ключи из неё).

## 3. Env (`core/envs/warhamEnv.py`)

- **action_space** (конструктор): убрать `'shoot'`/`'charge'`; добавить в цикле по модельным юнитам
  `action_spaces[f"shoot_num_{i}"] = spaces.Discrete(len(enemy))` и
  `action_spaces[f"charge_num_{i}"] = spaces.Discrete(len(enemy))`.
- **Маски** (`_build_*_action_masks` / там, где строится `masks["shoot"]`): вместо одной
  `masks["shoot"]`/`masks["charge"]` строить per-unit `masks[f"shoot_num_{i}"]` из
  `get_shoot_targets_for_unit(side, i)` и `masks[f"charge_num_{i}"]` из charge-таргетов юнита i.
  Длина каждой маски = `len(enemy)`; True на валидных rank-позициях.
- **Потребление flat-режима:**
  - `shooting_phase(... decide_shoot=None)`: строка `raw = action["shoot"]` →
    `raw = action[f"shoot_num_{i}"]` (и для enemy-ветки аналогично, по её юниту i).
  - charge-фаза: симметрично, `action["charge"]` → `action[f"charge_num_{i}"]`.
  - Windowed-путь (`decide_shoot(i)`/charge) уже per-unit — не меняется.
- `build_env_contract_from_spaces`/`action_space_signature` автоматически отразят новый набор
  голов (heads:... строка) → контракт-хэш сменится.

## 4. Модели

- **AZ / GAZ / GMZ / SMZ / PPO** — generic по `n_actions` (головы строятся из списка размеров,
  маски — `FactorizedLegalMasks` по ключам). Код не трогаем; число голов вырастет автоматически.
- **DQN** (`core/models/utils.py`):
  - `select_action`: хардкод `if head_idx == 2 and shoot_mask is not None` (shoot=индекс 2) и
    `sampled_action["shoot"]`/`["charge"]` — обобщить: применять per-unit маски к головам
    `shoot_num_i`/`charge_num_i` по их позиции в `ordered_action_keys` (не по числу 2).
  - `build_shoot_action_mask`: вернуть набор per-unit масок (dict по ключам) либо принимать
    unit_idx; согласовать с `select_action`.
- Грепнуть остальные модели на хардкод `"shoot"`/`"charge"`/индексов голов; ожидаем только DQN.

## 5. Windowed / legacy mapping

- `core/engine/phases/legacy_compiler.py`:
  - `default_action_dict(len_model)`: убрать `"shoot": 0`/`"charge": 0`; добавить
    `shoot_num_i=0`/`charge_num_i=0` по юнитам.
  - `compile_options_to_action_dict`: legacy_patch опций теперь пишет `shoot_num_{unit}` /
    `charge_num_{unit}` → **исчезает lossy-override**; обновить docstring.
- `core/engine/phases/option_generator.py` / `windowed_selfplay.py`: проверить, что
  `ActionOption.legacy_patch` для SHOOT/CHARGE кладёт per-unit ключ (`shoot_num_{unit_idx}`),
  а не одиночный `shoot`.

## 6. Потребители action_dict

- `play.py`, `eval.py`, эвристические билдеры action_dict, `_step_verdict`/трейсы, использующие
  `action.get("shoot")`/`["charge"]` — перевести на per-unit ключи или строить через
  `default_action_dict`. Viewer-строки с «shoot»/«charge» — это **имена фаз/ActionKind**, не
  головы контракта, их не трогаем.

## 7. Миграция (hard break)

- Бамп `ENV_RULESET_VERSION` (напр. `only_war_v2`) → `action_space_signature` меняется →
  `compatible_contracts` отклоняет старые чекпойнты/оппоненты с понятной RU-ошибкой
  (что/где/что делать: переобучить под новый контракт). Авто-миграции нет.
- Дефолты hyperparams/GUI — без нового поля (флага нет). README/доки не трогаем (могут устареть).

## 8. Тестирование

- **Контракт:** `ordered_action_keys`/`action_sizes_from_env` содержат `shoot_num_i`/`charge_num_i`,
  нет одиночных `shoot`/`charge`; размер = base + 3·len_model голов.
- **Маски:** формы `shoot_num_i`/`charge_num_i` = `len(enemy)`; валидные ранги по
  `get_shoot_targets_for_unit`.
- **Per-unit поведение:** во flat-режиме два юнита с разными `shoot_num_i` бьют **разные** цели
  (раньше было невозможно); регресс на синтетическом сценарии.
- **DQN:** маски применяются к каждой `shoot_num_i` голове (а не к индексу 2).
- **Windowed↔flat consistency:** windowed уже per-unit; после правки flat-план из
  `compile_options_to_action_dict` даёт тот же результат (нет потери при нескольких стреляющих).
- **Миграция:** загрузка старого чекпойнта → понятная ошибка `action_space_signature mismatch`.
- **Регресс:** `tests/engine/phases/`, `tests/models/`; smoke train AZ + DQN (новый контракт) без
  краша; parity windowed↔legacy на новом контракте.

## 9. Инкрементальная поставка (для writing-plans)

1. `action_contract.py` (новые ключи, убрать shoot/charge) + тест размеров.
2. Env action_space + per-unit маски + тест форм.
3. Потребление shoot (flat) per-unit + тест «разные цели».
4. Потребление charge (flat) per-unit + тест.
5. DQN `select_action`/маски по ключам + тест.
6. `legacy_compiler`/option_generator per-unit + тест (нет lossy).
7. Потребители action_dict (play/eval/эвристика).
8. Бамп `ENV_RULESET_VERSION` + тест mismatch; smoke AZ+DQN + parity.

## 10. Риски

- **Широкая поверхность** (контракт+env+DQN+windowed+потребители) — главный риск; митигейт:
  инкрементально по голове, golden-тесты, smoke на двух алго (AZ generic + DQN hardcoded).
- **Скрытые хардкоды индекса головы** (как DQN `head_idx==2`) — грепнуть все модели/утилиты до
  правки; не полагаться на позицию.
- **Маски-форма для сетей**: число голов растёт — проверить, что инференс/боевые маски
  согласованы по `ordered_action_keys` во всех алго (особенно remote IS search_cfg).
