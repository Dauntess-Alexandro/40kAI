2026-04-10 20:09:59 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-10 20:09:59 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-10 20:09:59 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-10 20:09:59 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-10 20:10:00 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-10 20:10:00 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-10 20:10:00 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-10 20:10:00 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-10 20:10:00 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-10 20:10:00 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-10 20:10:00 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-10 20:10:04 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-04-10 20:10:04 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-10 20:10:04 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-10 20:10:04 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-10 20:10:04 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-10 20:10:04 | [DEPLOY] Order: model first, alternating
2026-04-10 20:10:04 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-10 20:10:04 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1269, coord=(21,9), attempt=1, reward=+0.022, score_before=0.000, score_after=0.445, reward_delta=+0.022, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-10 20:10:04 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (21,9)
2026-04-10 20:10:04 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-10 20:10:05 | REQ: deploy cell accepted x=46, y=27
2026-04-10 20:10:05 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,46)
2026-04-10 20:10:05 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (27,46)
2026-04-10 20:10:05 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-10 20:10:05 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=248, coord=(4,8), attempt=1, reward=-0.000, score_before=0.445, score_after=0.441, reward_delta=-0.000, forward=0.147, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-10 20:10:05 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (4,8)
2026-04-10 20:10:06 | REQ: deploy cell accepted x=47, y=22
2026-04-10 20:10:06 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,47)
2026-04-10 20:10:06 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,47)
2026-04-10 20:10:06 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.152 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-10 20:10:06 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02203389830508475, 'units': 2, 'total_deploy_reward': 0.02203389830508475, 'forward_sum': 0.30338983050847457, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.15169491525423728, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-10 20:10:06 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-10 20:10:06 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-10 20:10:06 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-10 20:10:06 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-10 20:10:06 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-10 20:10:06 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-10 20:10:06 | FX: перепроигрываю 30 строк(и) лога.
2026-04-10 20:10:07 | === БОЕВОЙ РАУНД 1 ===
2026-04-10 20:10:07 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-10 20:10:07 | --- ХОД PLAYER ---
2026-04-10 20:10:07 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-10 20:10:07 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-10 20:10:07 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-10 20:10:07 | FX: перепроигрываю 30 строк(и) лога.
2026-04-10 20:10:07 | REQ: move cell accepted (RMB) x=35, y=30, mode=advance
2026-04-10 20:10:07 | [MOVE] unit=11 advance to=(35,30) dist=11 M=5 adv=6
2026-04-10 20:10:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-10 20:10:08 | REQ: move cell accepted (RMB) x=36, y=21, mode=advance
2026-04-10 20:10:08 | [MOVE] unit=12 advance to=(36,21) dist=11 M=5 adv=6
2026-04-10 20:10:09 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6]
2026-04-10 20:10:09 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-10 20:10:09 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-10 20:10:09 | 
🎲 Бросок сейвы (save): 1D6
2026-04-10 20:10:09 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-10 20:10:09 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-10 20:10:09 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-10 20:10:09 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-10 20:10:09 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-10 20:10:09 | Оружие: Gauss flayer
2026-04-10 20:10:09 | FX: найдена строка оружия: Gauss flayer.
2026-04-10 20:10:09 | BS оружия: 4+
2026-04-10 20:10:09 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-10 20:10:09 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-10 20:10:09 | Save цели: 4+ (invul: нет)
2026-04-10 20:10:09 | Benefit of Cover: не активен.
2026-04-10 20:10:09 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-10 20:10:09 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-10 20:10:09 | Правило: Overwatch: попадания только на 6+
2026-04-10 20:10:09 | Hit rolls:    [2, 4, 4, 3, 6, 4, 5, 5, 4, 2]  -> hits: 1 (crits: 1)
2026-04-10 20:10:09 | Save rolls:   [6]  (цель 4+) -> failed saves: 0
2026-04-10 20:10:09 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-10 20:10:09 | FX: найден итог урона = 0.0.
2026-04-10 20:10:09 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-04-10 20:10:09 | FX: позиция эффекта start=(228.0,516.0) end=(1140.0,540.0).
2026-04-10 20:10:09 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-10 20:10:09 | 📌 -------------------------

2026-04-10 20:10:09 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-10 20:10:09 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-10 20:10:09 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-10 20:10:09 | --- ФАЗА ЧАРДЖА ---
2026-04-10 20:10:09 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-10 20:10:09 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-10 20:10:09 | Нет доступных целей для чарджа.
2026-04-10 20:10:09 | --- ФАЗА БОЯ ---
2026-04-10 20:10:09 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:09 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:09 | --- ХОД MODEL ---
2026-04-10 20:10:09 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-10 20:10:09 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-10 20:10:09 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-10 20:10:11 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-10 20:10:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 9). Выбор reachable_idx=10/482, mode=normal, advance=нет, distance=5
2026-04-10 20:10:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 13)
2026-04-10 20:10:11 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-10 20:10:11 | FX: перепроигрываю 30 строк(и) лога.
2026-04-10 20:10:12 | FX: перепроигрываю 30 строк(и) лога.
2026-04-10 20:10:14 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-10 20:10:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 8). Выбор reachable_idx=6/319, mode=normal, advance=нет, distance=4
2026-04-10 20:10:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 8)
2026-04-10 20:10:14 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-10 20:10:14 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-10 20:10:14 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(36, 21), target_filter_size=1, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-10 20:10:14 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(36, 21), full_cells=24, rapid_cells=12, вошло=1920, rapid=625, не вошло=480, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-10 20:10:15 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 2, 4]
2026-04-10 20:10:15 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-10 20:10:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-10 20:10:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-10 20:10:15 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-10 20:10:15 | 
🎲 Бросок сейвы (save): 3D6
2026-04-10 20:10:15 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-10 20:10:15 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-10 20:10:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-10 20:10:15 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-10 20:10:15 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-10 20:10:15 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-10 20:10:15 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-10 20:10:15 | Оружие: Gauss flayer
2026-04-10 20:10:15 | FX: найдена строка оружия: Gauss flayer.
2026-04-10 20:10:15 | BS оружия: 4+
2026-04-10 20:10:15 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-10 20:10:15 | Save цели: 4+ (invul: нет)
2026-04-10 20:10:15 | Benefit of Cover: не активен.
2026-04-10 20:10:15 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-10 20:10:15 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-10 20:10:15 | Hit rolls:    [6, 2, 5, 5, 3, 5, 5, 3, 5, 4]  -> hits: 7 (crits: 1)
2026-04-10 20:10:15 | Wound rolls:  [1, 1, 3, 4, 6, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-04-10 20:10:15 | Save rolls:   [2, 2, 4]  (цель 4+) -> failed saves: 2
2026-04-10 20:10:15 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-10 20:10:15 | FX: найден итог урона = 2.0.
2026-04-10 20:10:15 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-04-10 20:10:15 | FX: позиция эффекта start=(324.0,396.0) end=(876.0,516.0).
2026-04-10 20:10:15 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-10 20:10:15 | 📌 -------------------------

2026-04-10 20:10:19 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-10 20:10:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-10 20:10:19 | --- ФАЗА ЧАРДЖА ---
2026-04-10 20:10:20 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-10 20:10:20 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-10 20:10:21 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-10 20:10:21 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-10 20:10:21 | [MODEL] Чардж: нет доступных целей
2026-04-10 20:10:21 | --- ФАЗА БОЯ ---
2026-04-10 20:10:21 | [MODEL] Ближний бой: нет доступных атак
2026-04-10 20:10:21 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-10 20:10:21 | Итерация 0 завершена с наградой tensor([0.1715], device='cuda:0'), здоровье игрока [10.0, 8.0], здоровье модели [10.0, 10.0]
2026-04-10 20:10:21 | {'model health': [10.0, 10.0], 'player health': [10.0, 8.0], 'model alive models': [10, 10], 'player alive models': [10, 8], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-10 20:10:21 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 8.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-04-10 20:10:21 | FX: перепроигрываю 30 строк(и) лога.
2026-04-10 20:10:21 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-10 20:10:21 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-10 20:10:21 | FX: найдена строка оружия: Gauss flayer.
2026-04-10 20:10:21 | FX: найден итог урона = 2.0.
2026-04-10 20:10:21 | FX: дубликат отчёта, эффект не создаём.
2026-04-10 20:10:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-10 20:10:22 | Модель победила!
