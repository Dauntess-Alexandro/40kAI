# Forensic: низкий winrate в self-play (2026-03-18)

## 1) Карта пайплайна

1. **Qt GUI (`gui_qt/main.py`)** выставляет env-переменные режима (`SELF_PLAY_ENABLED`, `SELF_PLAY_OPPONENT_MODE`, `SELF_PLAY_FIXED_PATH`, `RESUME_CHECKPOINT`, `DEPLOYMENT_MODE`, `NUM_ENVS/VEC_ENV_COUNT`, логи, PER/N-step).  
2. **`train.py`** читает env, логирует `[TRAIN][START]` и `[TRAIN][BOOT]`, строит env-векторы, policy/target/opponent, resume, replay, epsilon schedule.  
3. В цикле: `enemyTurn -> action_select -> step -> replay push (n-step) -> optimize`.  
4. На `done`: вычисляются `result/win/vp_diff/end_reason`, пишутся `[TRAIN][EP]`, `[TRAIN][ACTIONS]`, `metrics/stats_<run>.csv`, `results.txt`, optional checkpoint/snapshot update.

## 2) Что проверено

- Логи: `LOGS_FOR_AGENTS_TRAIN.md`, `LOGS_FOR_AGENTS_PLAY.md`.
- Метрики эпизодов: `metrics/stats_4114813.csv`, `metrics/stats_6233884.csv`, `metrics/stats_7190574.csv`.
- Конфиги/цепочка env: `gui_qt/main.py`, `train.py`, `hyperparams.json`, `reward_config.py`.
- Логика масок/действий/валидации: `model/utils.py`, `train.py`, `gym_mod/gym_mod/envs/warhamEnv.py`.

## 3) Первые подтвержденные аномалии

### A1. Резкий провал winrate при self-play подтвержден метриками

| mode | run_id | winrate mean±std | vp_diff mean±std | reward mean±std | ep_len mean±std | top end_reason |
|---|---:|---:|---:|---:|---:|---|
| baseline train | 4114813 | 0.5793 ± 0.4937 | -0.4733 ± 0.6271 | 0.4600 ± 0.3862 | 8.145 ± 1.998 | wipeout_enemy (865/1500) |
| selfplay snapshot | 6233884 | 0.0387 ± 0.1928 | +0.0313 ± 0.2090 | 0.0702 ± 0.0969 | 9.987 ± 0.157 | turn_limit_Only War (1472/1500) |
| selfplay + resume | 7190574 | 0.0780 ± 0.2682 | +0.0673 ± 0.3743 | 0.0952 ± 0.1133 | 9.958 ± 0.304 | turn_limit_Only War (1445/1500) |
| selfplay fixed_checkpoint | — | **нет данных в текущих логах/метриках** | — | — | — | — |

Вывод: self-play режимы ушли в почти сплошные `turn_limit`, при этом reward растет относительно худшего self-play, но winrate остается низким.

### A2. Текущий запуск self-play действительно идет как `snapshot + resume`

`LOGS_FOR_AGENTS_TRAIN.md` стартует с:
- `SELF_PLAY_ENABLED=1`, `SELF_PLAY_OPPONENT_MODE=snapshot`, `RESUME_CHECKPOINT=set`.
- Resume восстановил: `global_step=27276`, `optimize_steps=9258`, `episode=3000`, `replay_size=27258`, `eps=0.1272`.

### A3. Loss улучшается, но winrate не растет

По train-логам:
- ранние лог-точки: loss ~0.13,
- поздние: loss ~0.09–0.10,
- epsilon падает до 0.05.

При этом в `stats_7190574.csv`:
- winrate=0.078,
- 1445/1500 эпизодов — `turn_limit_Only War`.
- корреляции: `corr(reward, win)=0.5428`, `corr(reward, vp_diff)=0.1887`, `corr(vp_diff, win)=0.7247`.

=> оптимизация TD-loss улучшает аппроксимацию текущей цели Q, но не приводит к росту доли побед из-за доминирования ничьих/тайм-лимита.

### A4. В `TRAIN][ACTIONS]` была поломана диагностика (счетчики копились между эпизодами)

В `train.py` счетчики `action_head_*` и `shoot_windows_*` инициализировались в начале, но **не сбрасывались после reset эпизода**. Из-за этого к концу тренировки `skip_rate` и related-метрики становились кумулятивным мусором и могли вводить в заблуждение в forensic-анализе.

Исправлено патчем: счетчики теперь сбрасываются на каждом новом эпизоде.

### A5. Доп. дефект в invalid-check `shoot`

В `train.py` проверка invalid shoot использовала `shoot_raw >= len(valid_shoot_indices)`, что корректно только для contiguous индексов `[0..n-1]`. Исправлено на membership: `shoot_raw not in valid_shoot_indices`.

## 4) Что не удалось полноценно закрыть в этом окружении

- `LOGS_FOR_AGENTS_PLAY.md` пуст (0 строк) — нет данных Viewer-ветки для кросс-проверки train/play расхождений.
- В этой среде из коробки не было `torch`, поэтому новые полноразмерные прогонки 4 режимов + multi-seed не выполнены здесь; использованы уже сохраненные метрики `metrics/stats_*.csv` и train-лог.

## 5) Короткий практический вывод

1. Основная деградация self-play: почти все бои уходят в `turn_limit`, отсюда winrate ~0–8% даже при улучшении loss/reward.
2. По текущим логам self-play идет с resume + сильным greedy-opponent (`opp_eps=0.0`) и низким exploration у агента (`eps≈0.05`), что стабилизирует «ничейный» стиль.
3. До фикса `TRAIN][ACTIONS]` сами action-диагностики были частично недостоверны (кумулятивные счетчики).
