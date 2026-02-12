# Аудит reward-системы (для новичка)

Дата: 2026-02-12

## Где считается reward

- Все начисления происходят в `warhamEnv.step()` и во внутренних фазах (`command_phase`, `movement_phase`, `shooting_phase`, `charge_phase`, `fight_phase`).
- Коэффициенты (веса) лежат в `reward_config.py`.

## Полный список reward-компонентов

## 1) Command phase

1. **Insane Bravery bonus**: `+0.5`
   - Когда юнит провалил Battle-shock, но агент тратит CP и CP хватает.
2. **Insane Bravery penalty**: `-0.5`
   - Когда агент пытается применить Insane Bravery, но CP не хватает.

## 2) Movement phase

1. **Hold objective (no move)**:
   - Если выбран `move=4` (стоять), для КАЖДОЙ objective marker:
     - если юнит рядом (`<=5`) => `+0.5`
     - иначе => `-0.5`
2. **Proximity to objective**:
   - После движения, за каждую цель в радиусе `<=5`: `+0.5`.
3. **Melee target already dead**: `+0.3`.
4. **Retreat from favorable melee**: `-0.5`.
   - Штраф дается, если юнит отступает, имея условно выгодный размен по HP.
5. **Stay in melee**: `+0.2`.

## 3) Shooting phase

Для каждой успешной стрельбы:

1. **Damage term**:
   - `+ (0.6 * normalized_damage)`
   - где `normalized_damage = dealt_damage / enemy_total_max_hp`.
2. **Kill bonus**: `+0.4` за добивание цели.
3. **Overkill penalty**:
   - `- 0.2 * (overkill / target_max_hp)`.
4. **Quality bonus** (может суммироваться):
   - `+0.05` если цель low HP (<=30% до выстрела),
   - `+0.07` если цель на objective,
   - `+0.05` если у цели высокий OC (`>=2`).
5. **Objective damage bonus**:
   - `+ 0.05 * raw_damage`, если цель на objective.
6. **Objective kill bonus**:
   - `+0.2`, если убили цель на objective.
7. **Action bonus**:
   - сейчас `0.0` (в конфиге).
8. **Invalid target penalty**:
   - если выбран невалидный индекс цели: `-(0.5 + 0.15) = -0.65`.

## 4) Charge phase

1. **Charge success bonus**: `+0.5`.
2. **Charge fail penalty**: `-0.5`.

## 5) Fight phase

1. **Melee damage term**: `+ 0.6 * normalized_melee_damage`.
2. **Melee kill term**: `+0.4 * kills`.
3. **Taken damage penalty**: `- 0.5 * normalized_model_damage_taken`.
4. **Advantage term**:
   - на основе разницы долей HP пары (model vs enemy), вес `0.15`.
5. **Strength term**:
   - сравнение melee power, шаг `+/-0.1`.
6. **Objective control term**:
   - `+ 0.2 * delta_controlled_objectives`.
7. **Objective damage in melee**:
   - `+ 0.05 * raw_damage_on_objective_targets`.
8. **Objective kill in melee**:
   - `+ 0.2 * kills_on_objective_targets`.

## 6) Post-phase / global in step()

После суммирования фаз:

1. **Damage taken penalty (global step)**:
   - `- 0.5 * (damage_taken / model_total_max_hp)`.
2. **Win bonus**: `+3.0`.
3. **Loss penalty**: `-2.0`.
4. **VP diff shaping**:
   - `+0.05 * max(vp_delta, 0)`
   - `-0.05 * max(-vp_delta, 0)`.
5. **Objective hold streak bonus**:
   - если объект удерживается подряд >=2 шагов, `+0.2` за каждую такую streak-цель.
6. **Idle outside objectives penalty**: `-0.05`.
   - Условия: не рядом с целями, VP/контроль не изменились, урон/киллы = 0, и не стало ближе к целям.

---

## Что видно по свежим логам (конкретно)

1. Часто встречается наказание за `hold_penalty=-0.5` на обоих юнитах в movement.
2. После этого часто добавляется `idle вне цели = -0.05`.
3. Есть кейсы `Advance без Assault — стрельба пропущена` (то есть потенциал фазы стрельбы полностью теряется).
4. Есть кейсы `Чардж: нет доступных целей` (фаза чарджа без reward-сигнала).
5. На примере «Итерация 2» общий reward эпизодного шага = `-0.05` при нулевом уроне и нулевом VP.

---

## Риски и перекосы в текущем reward

1. **Сильный ранний минус за no-move далеко от цели**
   - При 1 objective и 2 юнитах агент сразу получает `-1.0` только за факт “стою не на точке”.
   - Это агрессивный штраф и он может доминировать над слабым положительным сигналом от «двигаться ближе».

2. **Двойное наказание за “пустой ход”**
   - В одном и том же шаге одновременно срабатывают:
     - `hold_penalty` в movement,
     - и `idle вне цели` в конце step.

3. **Смешение нормализованного и ненормализованного урона**
   - В стрельбе/ближнем бою есть термы от нормализованного урона,
   - но objective damage bonus (`0.05 * raw_damage`) — от сырого урона.
   - Из-за этого масштаб награды зависит от профиля оружия/юнита не всегда предсказуемо.

4. **`CLIP_REWARD` не применяется в train.py**
   - Переменная окружения читается и логируется, но фактического клиппинга reward в пайплайне не видно.

5. **Метрика `ep_reward` в train.py — среднее за шаг, а не сумма**
   - Это не ошибка среды, но новичков часто путает: “reward per episode” здесь это average step reward.

---

## Топ-советы (что делать дальше)

1. **Сначала стабилизировать раннюю игру**
   - Уменьшить `VP_OBJECTIVE_HOLD_PENALTY` (например 0.5 -> 0.2),
   - либо начислять hold_penalty только если юнит _мог_ подойти к objective, но сознательно не сделал этого.

2. **Убрать двойной штраф за пустой ход**
   - Либо отключить `idle вне цели`, когда уже был `hold_penalty` в этом же step,
   - либо наоборот: оставить только `idle` как “мягкий универсальный штраф”.

3. **Унифицировать масштаб уронных термов**
   - Привести objective damage bonus к нормализованному виду (через max HP),
   - чтобы коэффициенты легче тюнились между ростерами.

4. **Реально внедрить `CLIP_REWARD`**
   - Если планировалось, добавить клиппинг перед записью в replay buffer.

5. **Явно переименовать/документировать `ep_reward` в train.py**
   - Например `ep_reward_mean_step`, чтобы новичок не думал, что это сумма.

6. **Для дебага reward включать короткий режим аудита**
   - Печатать не только `Reward (шаг): ...`, но и итог:
     - `phase_total`, `post_step_total`, `final_reward_before_buffer`.

