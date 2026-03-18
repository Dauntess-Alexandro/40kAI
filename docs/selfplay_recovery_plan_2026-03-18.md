# План выхода из "ничейной ямы" в self-play (2026-03-18)

## Цель
Снизить долю `turn_limit`/draw, увеличить долю решающих исходов (`wipeout_enemy`/победа по VP), и перевести контроль качества обучения с `loss/reward` на боевые метрики (`win/draw/wipeout/vp_diff`).

## Пункт 1 (сделать сразу)
**Усилить terminal/VP-ориентированный сигнал относительно dense shaping.**

### Что внедряется
1. Новые коэффициенты в `reward_config.py`:
   - `TURN_LIMIT_DRAW_PENALTY`
   - `TURN_LIMIT_VP_MARGIN_REWARD_SCALE`
   - `TURN_LIMIT_VP_MARGIN_PENALTY_SCALE`
   - `TURN_LIMIT_VP_MARGIN_CLAMP`
2. Новая ветка в `warhamEnv.step()`:
   - если `game_over and end_reason == "turn_limit"`:
     - штраф за `winner is None` (draw);
     - доп. бонус/штраф за VP margin (с clamp);
     - подробный лог `Reward (turn_limit endgame): ...`.

### Ожидаемый эффект
- Агенту станет менее выгодно застревать в ничьих концовках.
- Появится прямой градиент в сторону "дожима" по VP к концу партии.

## Пункт 2 (статус: выполнен)
**Добавить целевые eval-метрики в train-loop и алерты draw pit.**

### Что добавить
- Окно `N=100` эпизодов:
  - `win_rate_100`
  - `draw_rate_100`
  - `turn_limit_rate_100`
  - `wipeout_enemy_rate_100`
  - `wipeout_model_rate_100`
  - `vp_diff_mean_100`
- Лог-строку: `[TRAIN][EVAL_WINDOW] ...`
- Алерт: `[TRAIN][ALERT] draw_pit` при устойчивом `draw_rate` выше порога.

### Реализация
- В `train.py` добавлено окно `eval_window` и расчёт:
  - `win_rate`, `draw_rate`, `turn_limit_rate`, `wipeout_enemy_rate`, `wipeout_model_rate`, `vp_diff_mean`.
- Добавлен периодический лог `[TRAIN][EVAL_WINDOW]`.
- Добавлен алерт `[TRAIN][ALERT] draw_pit` с настраиваемым streak.

## Пункт 3 (статус: выполнен, v2)
**Self-play curriculum / opponent stability.**

- Не держать `opp_eps=0.0` на всём горизонте.
- Адаптивно менять `snapshot update_every` при высоком draw-rate.
- (Опционально) буфер старых оппонентов для разрыва симметричных паттернов.

### Реализация v1
- Добавлен scheduler `opp_eps` по эпизодам: `SELF_PLAY_OPPONENT_EPSILON_MAX -> ... -> SELF_PLAY_OPPONENT_EPSILON_MIN`.
- Добавлен adaptive `snapshot_update_every`:
  - при высоком `draw_rate` окно обновления снапшота увеличивается (стабилизация цели),
  - при низком `draw_rate` уменьшается (ускорение адаптации).
- Добавлены логи `[SELFPLAY] adaptive_update_every ...`.

### Реализация v2 (pool исторических оппонентов)
- Добавлен буфер исторических снапшотов оппонента (`SELF_PLAY_POOL_ENABLED`, `SELF_PLAY_POOL_SIZE`).
- При обновлении snapshot:
  - текущий снапшот добавляется в pool,
  - с вероятностью `SELF_PLAY_POOL_SAMPLE_OLD_PROB` выбирается старый оппонент из pool,
  - иначе используется latest.
- Добавлен smart-sampling (v2.1):
  - для исторических оппонентов ведутся stats (`games/wins/draws/vp_diff_sum`),
  - считается difficulty-score (трудность + draw-pressure + vp-pressure + explore bonus),
  - выбор старого оппонента идёт с весами по этому score.
- Добавлены логи источника оппонента:
  - `opponent_source=...` в `[TRAIN][EVAL_WINDOW]` и self-play end-of-episode логах,
  - `source=..., pool_size=...` в логе обновления снапшота.

## Валидация после пункта 1
1. Перезапуск 4 режимов:
   - baseline
   - selfplay snapshot
   - selfplay fixed_checkpoint
   - selfplay + resume
2. Метрики:
   - `turn_limit_rate` (должен снизиться)
   - `win_rate` (должен вырасти)
   - `wipeout_enemy_rate` (должен вырасти)
   - `vp_diff_mean` (не должен деградировать)
3. Критерий успеха:
   - снижение `turn_limit_rate` минимум на 20% относительно текущей self-play базы.

## Риски
- Слишком сильный anti-draw штраф может привести к "суицидной" агрессии.
- Контроль: мониторить рост `wipeout_model_rate` и при необходимости уменьшать `TURN_LIMIT_DRAW_PENALTY`.
