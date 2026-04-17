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
2026-04-13 18:18:40 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:18:40 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:18:40 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:18:40 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:18:41 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:18:42 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:18:42 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:18:42 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:18:42 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:18:42 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:18:42 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:18:44 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-13 18:18:44 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:18:44 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:18:44 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:18:44 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:18:44 | [DEPLOY] Order: model first, alternating
2026-04-13 18:18:44 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:18:44 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1931, coord=(32,11), attempt=1, reward=+0.023, score_before=0.000, score_after=0.460, reward_delta=+0.023, forward=0.190, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:18:44 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,11)
2026-04-13 18:18:44 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:18:45 | REQ: deploy cell accepted x=50, y=24
2026-04-13 18:18:45 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,50)
2026-04-13 18:18:45 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,50)
2026-04-13 18:18:45 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:18:45 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2047, coord=(34,7), attempt=1, reward=-0.010, score_before=0.460, score_after=0.259, reward_delta=-0.010, forward=0.156, spread=0.333, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.333, final_cover=0.000
2026-04-13 18:18:45 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (34,7)
2026-04-13 18:18:45 | REQ: deploy cell accepted x=49, y=18
2026-04-13 18:18:45 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-04-13 18:18:45 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,49)
2026-04-13 18:18:45 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.013 total_deploy_reward=+0.013 avg_forward=0.173 avg_spread=0.667 avg_edge=1.000 avg_cover=0.000
2026-04-13 18:18:45 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.012928655892786751, 'units': 2, 'total_deploy_reward': 0.012928655892786751, 'forward_sum': 0.34576271186440677, 'spread_sum': 1.3333333333333333, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.17288135593220338, 'avg_spread': 0.6666666666666666, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-13 18:18:45 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:18:45 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:18:45 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:18:45 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:18:45 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:18:45 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:18:45 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:18:46 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:18:46 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:18:46 | --- ХОД PLAYER ---
2026-04-13 18:18:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:18:46 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:18:46 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:18:47 | REQ: move cell accepted (RMB) x=39, y=28, mode=advance
2026-04-13 18:18:47 | [MOVE] unit=11 advance to=(39,28) dist=11 M=5 adv=6
2026-04-13 18:18:47 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:18:48 | REQ: move cell accepted (RMB) x=38, y=24, mode=advance
2026-04-13 18:18:48 | [MOVE] unit=12 advance to=(38,24) dist=11 M=5 adv=6
2026-04-13 18:18:49 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:18:49 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:18:49 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:18:49 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:18:49 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:18:49 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:18:49 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:18:49 | Нет доступных целей для чарджа.
2026-04-13 18:18:49 | --- ФАЗА БОЯ ---
2026-04-13 18:18:49 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:18:49 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:18:49 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:18:49 | --- ХОД MODEL ---
2026-04-13 18:18:49 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:18:49 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:18:49 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:18:49 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:18:50 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:18:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 11). Выбор reachable_idx=10/435, mode=normal, advance=нет, distance=5
2026-04-13 18:18:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (27, 15)
2026-04-13 18:18:50 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:18:51 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:18:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 7). Выбор reachable_idx=6/321, mode=normal, advance=нет, distance=5
2026-04-13 18:18:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 7)
2026-04-13 18:18:51 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:18:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:18:51 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 24), target_filter_size=1, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:18:51 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(38, 24), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:18:54 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 4]
2026-04-13 18:18:54 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:18:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-04-13 18:18:54 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:18:54 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-13 18:18:54 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:18:54 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-13 18:18:54 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:18:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-13 18:18:54 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:18:54 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:18:54 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:18:54 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:18:54 | Оружие: Gauss flayer
2026-04-13 18:18:54 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:18:54 | BS оружия: 4+
2026-04-13 18:18:54 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:18:54 | Save цели: 4+ (invul: нет)
2026-04-13 18:18:54 | Benefit of Cover: не активен.
2026-04-13 18:18:54 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:18:54 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:18:54 | Hit rolls:    [6, 5, 5, 2, 4, 1, 1, 4, 5, 5]  -> hits: 7 (crits: 1)
2026-04-13 18:18:54 | Wound rolls:  [4, 1, 3, 3, 2, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-04-13 18:18:54 | Save rolls:   [3, 4]  (цель 4+) -> failed saves: 1
2026-04-13 18:18:54 | FX: найден failed saves = 1.
2026-04-13 18:18:54 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:18:54 | FX: найден итог урона = 1.0.
2026-04-13 18:18:54 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:18:54 | FX: позиция эффекта start=(372.0,660.0) end=(948.0,684.0).
2026-04-13 18:18:54 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:18:54 | 📌 -------------------------

2026-04-13 18:18:56 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:18:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:18:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:18:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:18:56 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:18:57 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:18:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:18:57 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:18:57 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:18:57 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:18:57 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:18:57 | FX: найден failed saves = 1.
2026-04-13 18:18:57 | FX: найден итог урона = 1.0.
2026-04-13 18:18:57 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:18:58 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:18:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:18:58 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:18:58 | --- ФАЗА БОЯ ---
2026-04-13 18:18:58 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:18:58 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:18:58 | Итерация 0 завершена с наградой tensor([0.1721], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-13 18:18:58 | {'model health': [10.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [10, 10], 'player alive models': [9, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:18:58 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-13 18:18:59 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:18:59 | --- ХОД PLAYER ---
2026-04-13 18:18:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:18:59 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:19:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:19:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-13 18:19:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:19:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-13 18:19:00 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:19:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:19:01 | REQ: move cell accepted (RMB) x=34, y=27, mode=normal
2026-04-13 18:19:01 | [MOVE] unit=11 normal to=(34,27) dist=5 M=5
2026-04-13 18:19:01 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2]
2026-04-13 18:19:02 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:19:02 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:19:02 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:19:02 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-13 18:19:02 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:19:02 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-13 18:19:02 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:19:02 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:19:02 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:02 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:19:02 | Оружие: Gauss flayer
2026-04-13 18:19:02 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:02 | BS оружия: 4+
2026-04-13 18:19:02 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:19:02 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:02 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:02 | Benefit of Cover: не активен.
2026-04-13 18:19:02 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:02 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:02 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:19:02 | Hit rolls:    [3, 5, 2, 2, 4, 5, 6, 1, 1, 5]  -> hits: 1 (crits: 1)
2026-04-13 18:19:02 | Save rolls:   [2]  (цель 4+) -> failed saves: 1
2026-04-13 18:19:02 | FX: найден failed saves = 1.
2026-04-13 18:19:02 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:19:02 | FX: найден итог урона = 1.0.
2026-04-13 18:19:02 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:19:02 | FX: позиция эффекта start=(372.0,660.0) end=(948.0,684.0).
2026-04-13 18:19:02 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:19:02 | 📌 -------------------------

2026-04-13 18:19:05 | REQ: move cell accepted (RMB) x=33, y=23, mode=normal
2026-04-13 18:19:05 | [MOVE] unit=12 normal to=(33,23) dist=5 M=5
2026-04-13 18:19:05 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4]
2026-04-13 18:19:05 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:19:05 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:19:05 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:19:05 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:19:05 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:19:05 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:19:05 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:05 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:19:05 | Оружие: Gauss flayer
2026-04-13 18:19:05 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:05 | BS оружия: 4+
2026-04-13 18:19:05 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:19:05 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:05 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:05 | Benefit of Cover: не активен.
2026-04-13 18:19:05 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:05 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:05 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:19:05 | Hit rolls:    [2, 3, 3, 5, 6, 1, 5, 1, 2, 1]  -> hits: 1 (crits: 1)
2026-04-13 18:19:05 | Save rolls:   [4]  (цель 4+) -> failed saves: 0
2026-04-13 18:19:05 | FX: найден failed saves = 0.
2026-04-13 18:19:05 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:19:05 | FX: найден итог урона = 0.0.
2026-04-13 18:19:05 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:19:05 | FX: позиция эффекта start=(372.0,660.0) end=(924.0,588.0).
2026-04-13 18:19:05 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:19:05 | 📌 -------------------------

2026-04-13 18:19:05 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:19:05 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-13 18:19:05 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(34, 27), target_filter_size=2, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:19:05 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(34, 27), full_cells=24, rapid_cells=12, вошло=1813, rapid=625, не вошло=587, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:19:08 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-13 18:19:08 | REQ: движок запросил кубы стрельбы (target=21, count=9, stage=hit).
2026-04-13 18:19:13 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-13 18:19:13 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:13 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:19:13 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:19:13 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:13 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-04-13 18:19:13 | Оружие: Gauss flayer
2026-04-13 18:19:13 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:13 | BS оружия: 4+
2026-04-13 18:19:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:13 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:13 | Benefit of Cover: не активен.
2026-04-13 18:19:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:13 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-04-13 18:19:13 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:19:13 | FX: найден итог урона = 0.0.
2026-04-13 18:19:13 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-13 18:19:13 | FX: позиция эффекта start=(828.0,660.0) end=(372.0,660.0).
2026-04-13 18:19:13 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-04-13 18:19:13 | 📌 -------------------------

2026-04-13 18:19:13 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-04-13 18:19:13 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-13 18:19:13 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 23), target_filter_size=2, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:19:13 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 23), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:19:13 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:19:13 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:19:13 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:19:13 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:13 | FX: найден failed saves = 0.
2026-04-13 18:19:13 | FX: найден итог урона = 0.0.
2026-04-13 18:19:13 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:19:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:19:15 | REQ: движок запросил кубы стрельбы (target=21, count=10, stage=hit).
2026-04-13 18:19:15 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(34, 27), target_filter_size=2, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:19:15 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(34, 27), full_cells=24, rapid_cells=12, вошло=1813, rapid=625, не вошло=587, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:19:16 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-04-13 18:19:16 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 10D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-04-13 18:19:16 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-04-13 18:19:16 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-13 18:19:16 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 23), target_filter_size=2, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:19:16 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 23), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:19:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:19:17 | REQ: движок запросил кубы стрельбы (target=21, count=10, stage=hit).
2026-04-13 18:19:23 | 
🎲 Бросок на ранение (to wound): 5D6
2026-04-13 18:19:23 | REQ: движок запросил кубы стрельбы (target=21, count=5, stage=wound).
2026-04-13 18:19:26 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:19:26 | REQ: движок запросил кубы стрельбы (target=21, count=2, stage=save).
2026-04-13 18:19:27 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 4]
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:19:27 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:27 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:19:27 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:19:27 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:27 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-13 18:19:27 | Оружие: Gauss flayer
2026-04-13 18:19:27 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:27 | BS оружия: 4+
2026-04-13 18:19:27 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:27 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:27 | Benefit of Cover: не активен.
2026-04-13 18:19:27 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:27 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:27 | Hit rolls:    [1, 1, 1, 2, 3, 4, 5, 5, 5, 5]  -> hits: 5
2026-04-13 18:19:27 | Wound rolls:  [3, 4, 5, 1, 2]  (цель 4+) -> wounds: 2
2026-04-13 18:19:27 | Save rolls:   [3, 4]  (цель 4+) -> failed saves: 1
2026-04-13 18:19:27 | FX: найден failed saves = 1.
2026-04-13 18:19:27 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:19:27 | FX: найден итог урона = 1.0.
2026-04-13 18:19:27 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:19:27 | FX: позиция эффекта start=(804.0,564.0) end=(372.0,660.0).
2026-04-13 18:19:27 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-04-13 18:19:27 | 📌 -------------------------

2026-04-13 18:19:27 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:19:27 | Нет доступных целей для чарджа.
2026-04-13 18:19:27 | --- ФАЗА БОЯ ---
2026-04-13 18:19:27 | --- ХОД MODEL ---
2026-04-13 18:19:27 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:19:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-13 18:19:27 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:19:27 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:19:31 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-13 18:19:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 15). Выбор reachable_idx=10/524, mode=normal, advance=нет, distance=5
2026-04-13 18:19:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 19)
2026-04-13 18:19:31 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:19:31 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:19:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:19:31 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-13 18:19:31 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:31 | FX: найден failed saves = 1.
2026-04-13 18:19:31 | FX: найден итог урона = 1.0.
2026-04-13 18:19:31 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:19:32 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:19:33 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-13 18:19:33 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 7). Выбор reachable_idx=6/417, mode=normal, advance=нет, distance=5
2026-04-13 18:19:33 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (24, 7)
2026-04-13 18:19:33 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:19:33 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:19:34 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:19:34 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:19:35 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 6, 2, 3]
2026-04-13 18:19:35 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-13 18:19:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:19:35 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:19:35 | 
🎲 Бросок на ранение (to wound): 4D6
2026-04-13 18:19:35 | 
🎲 Бросок сейвы (save): 4D6
2026-04-13 18:19:35 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-13 18:19:35 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-13 18:19:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-13 18:19:35 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:19:35 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:19:35 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:35 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:19:35 | Оружие: Gauss flayer
2026-04-13 18:19:35 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:35 | BS оружия: 4+
2026-04-13 18:19:35 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:35 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:35 | Benefit of Cover: не активен.
2026-04-13 18:19:35 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:35 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:35 | Hit rolls:    [1, 1, 2, 2, 4, 6, 4, 1, 1, 1, 6, 2, 6, 1, 2, 4, 3, 4, 1, 2]  -> hits: 7 (crits: 3)
2026-04-13 18:19:35 | Wound rolls:  [1, 4, 2, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-04-13 18:19:35 | Save rolls:   [4, 6, 2, 3]  (цель 4+) -> failed saves: 2
2026-04-13 18:19:35 | FX: найден failed saves = 2.
2026-04-13 18:19:35 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-13 18:19:35 | FX: найден итог урона = 2.0.
2026-04-13 18:19:35 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-13 18:19:35 | FX: позиция эффекта start=(468.0,540.0) end=(804.0,564.0).
2026-04-13 18:19:35 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:19:35 | 📌 -------------------------

2026-04-13 18:19:37 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 3, 1, 1]
2026-04-13 18:19:37 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-13 18:19:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:19:37 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:19:37 | 
🎲 Бросок на ранение (to wound): 4D6
2026-04-13 18:19:37 | 
🎲 Бросок сейвы (save): 4D6
2026-04-13 18:19:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 5. HP: 8.0 -> 5.0 (shooting)
2026-04-13 18:19:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-04-13 18:19:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-04-13 18:19:37 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:19:37 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:19:37 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:19:37 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:19:37 | Оружие: Gauss flayer
2026-04-13 18:19:37 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:19:37 | BS оружия: 4+
2026-04-13 18:19:37 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:19:37 | Save цели: 4+ (invul: нет)
2026-04-13 18:19:37 | Benefit of Cover: не активен.
2026-04-13 18:19:37 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:19:37 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:19:37 | Hit rolls:    [2, 5, 4, 1, 4, 6, 6, 3, 6, 5]  -> hits: 7 (crits: 3)
2026-04-13 18:19:37 | Wound rolls:  [2, 3, 1, 4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-04-13 18:19:37 | Save rolls:   [5, 3, 1, 1]  (цель 4+) -> failed saves: 3
2026-04-13 18:19:37 | FX: найден failed saves = 3.
2026-04-13 18:19:37 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:19:37 | FX: найден итог урона = 3.0.
2026-04-13 18:19:37 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:19:37 | FX: позиция эффекта start=(180.0,588.0) end=(804.0,564.0).
2026-04-13 18:19:37 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:19:37 | 📌 -------------------------

2026-04-13 18:19:37 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:25:35 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:25:35 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:25:35 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:25:35 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:25:36 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:25:36 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:25:36 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:25:36 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:25:36 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:25:36 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:25:36 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:25:38 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-13 18:25:38 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:25:38 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:25:38 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:25:38 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:25:38 | [DEPLOY] Order: model first, alternating
2026-04-13 18:25:38 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:25:38 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2287, coord=(38,7), attempt=1, reward=+0.017, score_before=0.000, score_after=0.336, reward_delta=+0.017, forward=0.122, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:25:38 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (38,7)
2026-04-13 18:25:38 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:25:39 | REQ: deploy cell accepted x=48, y=19
2026-04-13 18:25:39 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (19,48)
2026-04-13 18:25:39 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (19,48)
2026-04-13 18:25:39 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:25:39 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=304, coord=(5,4), attempt=1, reward=+0.002, score_before=0.336, score_after=0.371, reward_delta=+0.002, forward=0.097, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:25:39 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (5,4)
2026-04-13 18:25:39 | REQ: deploy cell accepted x=48, y=26
2026-04-13 18:25:39 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-13 18:25:39 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-13 18:25:39 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.109 avg_spread=1.000 avg_edge=0.250 avg_cover=0.000
2026-04-13 18:25:39 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018525817895151758, 'units': 2, 'total_deploy_reward': 0.018525817895151758, 'forward_sum': 0.21864406779661016, 'spread_sum': 2.0, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.10932203389830508, 'avg_spread': 1.0, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-04-13 18:25:39 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:25:39 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:25:39 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:25:39 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:25:39 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:25:39 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:25:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:25:40 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:25:40 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:25:40 | --- ХОД PLAYER ---
2026-04-13 18:25:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:25:40 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:25:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:25:41 | REQ: move cell accepted (RMB) x=37, y=27, mode=advance
2026-04-13 18:25:41 | [MOVE] unit=11 advance to=(37,27) dist=11 M=5 adv=6
2026-04-13 18:25:41 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:25:42 | REQ: move cell accepted (RMB) x=38, y=15, mode=advance
2026-04-13 18:25:42 | [MOVE] unit=12 advance to=(38,15) dist=11 M=5 adv=6
2026-04-13 18:25:42 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:25:42 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:25:42 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:25:42 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:25:42 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:25:42 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:25:42 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:25:42 | Нет доступных целей для чарджа.
2026-04-13 18:25:42 | --- ФАЗА БОЯ ---
2026-04-13 18:25:42 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:42 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:42 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:42 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:42 | --- ХОД MODEL ---
2026-04-13 18:25:42 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:25:42 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:25:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:25:43 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:25:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 7). Выбор reachable_idx=10/246, mode=normal, advance=нет, distance=5
2026-04-13 18:25:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 11)
2026-04-13 18:25:43 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:25:44 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:25:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (5, 4). Выбор reachable_idx=6/271, mode=normal, advance=нет, distance=5
2026-04-13 18:25:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 5)
2026-04-13 18:25:44 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:25:44 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:25:44 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 15), target_filter_size=1, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:25:44 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(38, 15), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:25:45 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 6, 4]
2026-04-13 18:25:45 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:25:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:25:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:25:45 | 
🎲 Бросок на ранение (to wound): 7D6
2026-04-13 18:25:45 | 
🎲 Бросок сейвы (save): 3D6
2026-04-13 18:25:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-04-13 18:25:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:25:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:25:45 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:25:45 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:25:45 | Оружие: Gauss flayer
2026-04-13 18:25:45 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:25:45 | BS оружия: 4+
2026-04-13 18:25:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:25:45 | Save цели: 4+ (invul: нет)
2026-04-13 18:25:45 | Benefit of Cover: не активен.
2026-04-13 18:25:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:25:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:25:45 | Hit rolls:    [5, 3, 6, 5, 4, 5, 5, 5, 2, 4]  -> hits: 8 (crits: 1)
2026-04-13 18:25:45 | Wound rolls:  [6, 2, 2, 2, 4, 2, 2]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-04-13 18:25:45 | Save rolls:   [5, 6, 4]  (цель 4+) -> failed saves: 0
2026-04-13 18:25:45 | FX: найден failed saves = 0.
2026-04-13 18:25:45 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:25:45 | FX: найден итог урона = 0.0.
2026-04-13 18:25:45 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:25:45 | FX: позиция эффекта start=(276.0,804.0) end=(900.0,660.0).
2026-04-13 18:25:45 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:25:45 | 📌 -------------------------

2026-04-13 18:25:47 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:25:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:25:47 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:25:48 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:25:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:25:49 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:25:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:25:49 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:25:49 | --- ФАЗА БОЯ ---
2026-04-13 18:25:49 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:25:49 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:25:49 | Итерация 0 завершена с наградой tensor([0.0807], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-13 18:25:49 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:25:49 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-04-13 18:25:49 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:49 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:25:49 | Модель победила!
2026-04-13 18:25:49 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:25:57 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:25:57 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:25:57 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:25:57 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:25:57 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:25:58 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:25:58 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:25:58 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:25:58 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:25:58 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:25:58 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:25:58 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:26:00 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-13 18:26:00 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:26:00 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:26:00 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:26:00 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:26:00 | [DEPLOY] Order: model first, alternating
2026-04-13 18:26:00 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:26:00 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=843, coord=(14,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:26:00 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (14,3)
2026-04-13 18:26:00 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:26:00 | REQ: deploy cell accepted x=49, y=29
2026-04-13 18:26:00 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-04-13 18:26:00 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-04-13 18:26:00 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:26:00 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1691, coord=(28,11), attempt=1, reward=+0.002, score_before=0.397, score_after=0.429, reward_delta=+0.002, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:26:00 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (28,11)
2026-04-13 18:26:01 | REQ: deploy cell accepted x=49, y=26
2026-04-13 18:26:01 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-13 18:26:01 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-13 18:26:01 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.088 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-13 18:26:01 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02144264879779267, 'units': 2, 'total_deploy_reward': 0.02144264879779267, 'forward_sum': 0.17627118644067796, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.08813559322033898, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-13 18:26:01 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:26:01 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:26:01 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:26:01 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:26:01 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:26:01 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:26:01 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:26:02 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:26:02 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:26:02 | --- ХОД PLAYER ---
2026-04-13 18:26:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:26:02 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:26:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:26:03 | REQ: move cell accepted (RMB) x=38, y=28, mode=advance
2026-04-13 18:26:03 | [MOVE] unit=11 advance to=(38,28) dist=11 M=5 adv=6
2026-04-13 18:26:03 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5]
2026-04-13 18:26:04 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:26:04 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:26:04 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:26:04 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:26:04 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:26:04 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:26:04 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:04 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-04-13 18:26:04 | Оружие: Gauss flayer
2026-04-13 18:26:04 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:04 | BS оружия: 4+
2026-04-13 18:26:04 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:26:04 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:26:04 | Save цели: 4+ (invul: нет)
2026-04-13 18:26:04 | Benefit of Cover: не активен.
2026-04-13 18:26:04 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:26:04 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:26:04 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:26:04 | Hit rolls:    [2, 1, 3, 4, 1, 2, 3, 4, 6, 2]  -> hits: 1 (crits: 1)
2026-04-13 18:26:04 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-04-13 18:26:04 | FX: найден failed saves = 0.
2026-04-13 18:26:04 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:26:04 | FX: найден итог урона = 0.0.
2026-04-13 18:26:04 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:26:04 | FX: позиция эффекта start=(276.0,684.0) end=(1188.0,708.0).
2026-04-13 18:26:04 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-04-13 18:26:04 | 📌 -------------------------

2026-04-13 18:26:04 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-04-13 18:26:04 | [MOVE] unit=12 advance to=(38,23) dist=11 M=5 adv=6
2026-04-13 18:26:04 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:26:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:26:04 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:26:04 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:26:04 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:26:04 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:26:04 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:26:04 | Нет доступных целей для чарджа.
2026-04-13 18:26:04 | --- ФАЗА БОЯ ---
2026-04-13 18:26:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:04 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:04 | --- ХОД MODEL ---
2026-04-13 18:26:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:26:04 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:26:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:26:06 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:26:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 3). Выбор reachable_idx=10/344, mode=normal, advance=нет, distance=4
2026-04-13 18:26:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 0)
2026-04-13 18:26:06 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:26:07 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:26:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 11). Выбор reachable_idx=6/528, mode=normal, advance=нет, distance=5
2026-04-13 18:26:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (23, 11)
2026-04-13 18:26:07 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:26:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:26:08 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:26:08 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 23), target_filter_size=1, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:26:08 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(38, 23), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:26:12 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:26:12 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:12 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:26:13 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 3, 5]
2026-04-13 18:26:13 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:26:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-13 18:26:13 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:26:13 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-13 18:26:13 | 
🎲 Бросок сейвы (save): 3D6
2026-04-13 18:26:13 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-13 18:26:13 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-13 18:26:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-13 18:26:13 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:26:13 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:26:13 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:13 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:26:13 | Оружие: Gauss flayer
2026-04-13 18:26:13 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:13 | BS оружия: 4+
2026-04-13 18:26:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:26:13 | Save цели: 4+ (invul: нет)
2026-04-13 18:26:13 | Benefit of Cover: не активен.
2026-04-13 18:26:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:26:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:26:13 | Hit rolls:    [4, 5, 4, 3, 4, 5, 5, 2, 1, 2]  -> hits: 6
2026-04-13 18:26:13 | Wound rolls:  [3, 5, 3, 1, 5, 5]  (цель 4+) -> wounds: 3
2026-04-13 18:26:13 | Save rolls:   [1, 3, 5]  (цель 4+) -> failed saves: 2
2026-04-13 18:26:13 | FX: найден failed saves = 2.
2026-04-13 18:26:13 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-13 18:26:13 | FX: найден итог урона = 2.0.
2026-04-13 18:26:13 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-13 18:26:13 | FX: позиция эффекта start=(276.0,564.0) end=(924.0,564.0).
2026-04-13 18:26:13 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:26:13 | 📌 -------------------------

2026-04-13 18:26:13 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:26:17 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:26:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:26:17 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:26:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:26:17 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:26:17 | --- ФАЗА БОЯ ---
2026-04-13 18:26:17 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:26:17 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:26:17 | Итерация 0 завершена с наградой tensor([0.1279], device='cuda:0'), здоровье игрока [10.0, 8.0], здоровье модели [10.0, 10.0]
2026-04-13 18:26:17 | {'model health': [10.0, 10.0], 'player health': [10.0, 8.0], 'model alive models': [10, 10], 'player alive models': [10, 8], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:26:17 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 8.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-04-13 18:26:18 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:26:18 | --- ХОД PLAYER ---
2026-04-13 18:26:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:26:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:26:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:26:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-13 18:26:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:26:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-13 18:26:20 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:26:20 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:26:21 | REQ: move cell accepted (RMB) x=33, y=25, mode=normal
2026-04-13 18:26:21 | [MOVE] unit=11 normal to=(33,25) dist=5 M=5
2026-04-13 18:26:22 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-13 18:26:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:26:22 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:26:22 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:26:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:26:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:26:22 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:22 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-04-13 18:26:22 | Оружие: Gauss flayer
2026-04-13 18:26:22 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:22 | BS оружия: 4+
2026-04-13 18:26:22 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:26:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:26:22 | Save цели: 4+ (invul: нет)
2026-04-13 18:26:22 | Benefit of Cover: не активен.
2026-04-13 18:26:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:26:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:26:22 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:26:22 | Hit rolls:    [3, 4, 3, 5, 3, 4, 5, 2, 2, 4]  -> hits: 0
2026-04-13 18:26:22 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:26:22 | FX: найден итог урона = 0.0.
2026-04-13 18:26:22 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-13 18:26:22 | FX: позиция эффекта start=(276.0,564.0) end=(924.0,684.0).
2026-04-13 18:26:22 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-04-13 18:26:22 | 📌 -------------------------

2026-04-13 18:26:24 | REQ: move cell accepted (RMB) x=33, y=21, mode=normal
2026-04-13 18:26:24 | [MOVE] unit=12 normal to=(33,21) dist=5 M=5
2026-04-13 18:26:25 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4]
2026-04-13 18:26:25 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:26:25 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:26:25 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:26:25 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:26:25 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:26:25 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:26:25 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:25 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:26:25 | Оружие: Gauss flayer
2026-04-13 18:26:25 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:25 | BS оружия: 4+
2026-04-13 18:26:25 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:26:25 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:26:25 | Save цели: 4+ (invul: нет)
2026-04-13 18:26:25 | Benefit of Cover: не активен.
2026-04-13 18:26:25 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:26:25 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:26:25 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:26:25 | Hit rolls:    [3, 1, 1, 4, 4, 6, 1, 2, 1, 1]  -> hits: 1 (crits: 1)
2026-04-13 18:26:25 | Save rolls:   [4]  (цель 4+) -> failed saves: 0
2026-04-13 18:26:25 | FX: найден failed saves = 0.
2026-04-13 18:26:25 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:26:25 | FX: найден итог урона = 0.0.
2026-04-13 18:26:25 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:26:25 | FX: позиция эффекта start=(276.0,564.0) end=(924.0,564.0).
2026-04-13 18:26:25 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:26:25 | 📌 -------------------------

2026-04-13 18:26:25 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:26:25 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:25 | REQ: валидные цели стрельбы для Unit 11: [22] | отфильтрованы: [21: цель вне дальности: range 29.00 > 24.00 (out_of_range by +5.00)]
2026-04-13 18:26:25 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 25), target_filter_size=1, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:26:25 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(33, 25), full_cells=24, rapid_cells=12, вошло=1911, rapid=625, не вошло=489, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:26:28 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:26:28 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-04-13 18:26:32 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-13 18:26:32 | REQ: движок запросил кубы стрельбы (target=22, count=6, stage=wound).
2026-04-13 18:26:36 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:26:36 | REQ: движок запросил кубы стрельбы (target=22, count=2, stage=save).
2026-04-13 18:26:39 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 5]
2026-04-13 18:26:39 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-04-13 18:26:39 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:26:39 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:39 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:26:39 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:26:39 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:26:39 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-04-13 18:26:39 | Оружие: Gauss flayer
2026-04-13 18:26:39 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:39 | BS оружия: 4+
2026-04-13 18:26:39 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:26:39 | Save цели: 4+ (invul: нет)
2026-04-13 18:26:39 | Benefit of Cover: не активен.
2026-04-13 18:26:39 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:26:39 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:26:39 | Hit rolls:    [1, 2, 3, 4, 5, 6, 5, 5, 5, 5]  -> hits: 7 (crits: 1)
2026-04-13 18:26:39 | Wound rolls:  [1, 2, 3, 4, 1, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-04-13 18:26:39 | Save rolls:   [1, 5]  (цель 4+) -> failed saves: 1
2026-04-13 18:26:39 | FX: найден failed saves = 1.
2026-04-13 18:26:39 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:26:39 | FX: найден итог урона = 1.0.
2026-04-13 18:26:39 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:26:39 | FX: позиция эффекта start=(804.0,612.0) end=(276.0,564.0).
2026-04-13 18:26:39 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-04-13 18:26:39 | 📌 -------------------------

2026-04-13 18:26:39 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:26:39 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-04-13 18:26:39 | REQ: валидные цели стрельбы для Unit 12: [22] | отфильтрованы: [21: цель вне дальности: range 29.00 > 24.00 (out_of_range by +5.00)]
2026-04-13 18:26:39 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 21), target_filter_size=1, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:26:39 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 21), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:26:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:26:39 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:26:39 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:26:39 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:26:39 | FX: найден failed saves = 0.
2026-04-13 18:26:39 | FX: найден итог урона = 0.0.
2026-04-13 18:26:39 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:28:24 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:28:24 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:28:24 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:28:24 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:28:24 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:28:24 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:28:24 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:28:24 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:24 | FX: найден failed saves = 0.
2026-04-13 18:28:24 | FX: найден итог урона = 0.0.
2026-04-13 18:28:24 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:28:24 | FX: позиция эффекта start=(276.0,564.0) end=(804.0,516.0).
2026-04-13 18:28:24 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:28:25 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:28:25 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:28:25 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:28:25 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:28:25 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:28:25 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:28:25 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:28:29 | Roll-off Attacker/Defender: enemy=2 model=6 -> attacker=model
2026-04-13 18:28:29 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:28:29 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:28:29 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:28:29 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:28:29 | [DEPLOY] Order: model first, alternating
2026-04-13 18:28:29 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:28:29 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1204, coord=(20,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:28:29 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (20,4)
2026-04-13 18:28:29 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:28:30 | REQ: deploy cell accepted x=49, y=28
2026-04-13 18:28:30 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,49)
2026-04-13 18:28:30 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,49)
2026-04-13 18:28:30 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:28:30 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=662, coord=(11,2), attempt=1, reward=-0.002, score_before=0.405, score_after=0.374, reward_delta=-0.002, forward=0.054, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:28:30 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (11,2)
2026-04-13 18:28:30 | REQ: deploy cell accepted x=48, y=21
2026-04-13 18:28:30 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,48)
2026-04-13 18:28:30 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,48)
2026-04-13 18:28:30 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.063 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-04-13 18:28:30 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018703192747339382, 'units': 2, 'total_deploy_reward': 0.018703192747339382, 'forward_sum': 0.12542372881355934, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.06271186440677967, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-04-13 18:28:30 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:28:30 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:28:30 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:28:30 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:28:30 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:28:30 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:28:30 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=22, cells_rapid=11, rapid_fire=1, source_cell=(33, 21), target_filter_size=1, max_target_dist=22, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:28:30 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 21), full_cells=22, rapid_cells=11, вошло=1800, rapid=529, не вошло=600, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:28:30 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(48, 21), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:28:30 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:28:31 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:28:31 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:28:31 | --- ХОД PLAYER ---
2026-04-13 18:28:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:28:31 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:28:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:28:32 | REQ: move cell accepted (RMB) x=38, y=29, mode=advance
2026-04-13 18:28:32 | [MOVE] unit=11 advance to=(38,29) dist=11 M=5 adv=6
2026-04-13 18:28:33 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:28:33 | REQ: move cell accepted (RMB) x=37, y=21, mode=advance
2026-04-13 18:28:33 | [MOVE] unit=12 advance to=(37,21) dist=11 M=5 adv=6
2026-04-13 18:28:34 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:28:34 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:28:34 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:28:34 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:28:34 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:28:34 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:28:34 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:28:34 | Нет доступных целей для чарджа.
2026-04-13 18:28:34 | --- ФАЗА БОЯ ---
2026-04-13 18:28:34 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:34 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:34 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:34 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:34 | --- ХОД MODEL ---
2026-04-13 18:28:34 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:28:34 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:28:34 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:28:35 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:28:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (20, 4). Выбор reachable_idx=10/366, mode=normal, advance=нет, distance=5
2026-04-13 18:28:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 9)
2026-04-13 18:28:35 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:28:35 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:28:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 2). Выбор reachable_idx=6/320, mode=normal, advance=нет, distance=5
2026-04-13 18:28:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (6, 5)
2026-04-13 18:28:35 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:28:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:28:35 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 21), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:28:35 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(37, 21), full_cells=24, rapid_cells=12, вошло=1880, rapid=625, не вошло=520, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:28:36 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:28:36 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:36 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:28:37 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:28:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:28:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:28:37 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:28:38 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:28:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:28:39 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:28:39 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:28:39 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:28:39 | --- ФАЗА БОЯ ---
2026-04-13 18:28:39 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:28:39 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:28:39 | Итерация 0 завершена с наградой tensor([0.0883], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-13 18:28:39 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:28:39 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:28:39 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:28:39 | --- ХОД PLAYER ---
2026-04-13 18:28:39 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:28:39 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:28:39 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:28:42 | REQ: move cell accepted (RMB) x=27, y=18, mode=advance
2026-04-13 18:28:42 | [MOVE] unit=11 advance to=(27,18) dist=11 M=5 adv=6
2026-04-13 18:28:42 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 2]
2026-04-13 18:28:43 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:28:43 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:28:43 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:28:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-13 18:28:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:28:43 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-13 18:28:43 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:28:43 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:28:43 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:28:43 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:28:43 | Оружие: Gauss flayer
2026-04-13 18:28:43 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:43 | BS оружия: 4+
2026-04-13 18:28:43 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:28:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:28:43 | Save цели: 4+ (invul: нет)
2026-04-13 18:28:43 | Benefit of Cover: не активен.
2026-04-13 18:28:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:28:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:28:43 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:28:43 | Hit rolls:    [3, 6, 3, 5, 2, 4, 6, 4, 2, 2]  -> hits: 2 (crits: 2)
2026-04-13 18:28:43 | Save rolls:   [5, 2]  (цель 4+) -> failed saves: 1
2026-04-13 18:28:43 | FX: найден failed saves = 1.
2026-04-13 18:28:43 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:28:43 | FX: найден итог урона = 1.0.
2026-04-13 18:28:43 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:28:43 | FX: позиция эффекта start=(228.0,372.0) end=(924.0,708.0).
2026-04-13 18:28:43 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:28:43 | 📌 -------------------------

2026-04-13 18:28:46 | REQ: move cell accepted (RMB) x=26, y=12, mode=advance
2026-04-13 18:28:46 | [MOVE] unit=12 advance to=(26,12) dist=11 M=5 adv=6
2026-04-13 18:28:46 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 5]
2026-04-13 18:28:47 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:28:47 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:28:47 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:28:47 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:28:47 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:28:47 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:28:47 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:28:47 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:28:47 | Оружие: Gauss flayer
2026-04-13 18:28:47 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:47 | BS оружия: 4+
2026-04-13 18:28:47 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:28:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:28:47 | Save цели: 4+ (invul: нет)
2026-04-13 18:28:47 | Benefit of Cover: не активен.
2026-04-13 18:28:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:28:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:28:47 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:28:47 | Hit rolls:    [5, 3, 6, 3, 5, 3, 3, 5, 6, 1]  -> hits: 2 (crits: 2)
2026-04-13 18:28:47 | Save rolls:   [5, 5]  (цель 4+) -> failed saves: 0
2026-04-13 18:28:47 | FX: найден failed saves = 0.
2026-04-13 18:28:47 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:28:47 | FX: найден итог урона = 0.0.
2026-04-13 18:28:47 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:28:47 | FX: позиция эффекта start=(228.0,372.0) end=(900.0,516.0).
2026-04-13 18:28:47 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:28:47 | 📌 -------------------------

2026-04-13 18:28:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:28:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:28:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:28:47 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:28:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:28:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:28:47 | Нет доступных целей для чарджа.
2026-04-13 18:28:47 | --- ФАЗА БОЯ ---
2026-04-13 18:28:47 | --- ХОД MODEL ---
2026-04-13 18:28:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:28:47 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:28:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:28:49 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-13 18:28:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 9). Выбор reachable_idx=10/481, mode=normal, advance=нет, distance=5
2026-04-13 18:28:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 13)
2026-04-13 18:28:49 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:28:49 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:28:49 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:28:49 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:28:49 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:49 | FX: найден failed saves = 0.
2026-04-13 18:28:49 | FX: найден итог урона = 0.0.
2026-04-13 18:28:49 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:28:50 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-13 18:28:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (6, 5). Выбор reachable_idx=6/304, mode=normal, advance=нет, distance=5
2026-04-13 18:28:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 5)
2026-04-13 18:28:50 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:28:50 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:28:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:28:52 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:28:52 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(26, 12), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:28:52 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(26, 12), full_cells=24, rapid_cells=12, вошло=1813, rapid=625, не вошло=587, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:28:53 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 3, 1, 5, 3, 5, 4, 2, 5, 5, 4, 1]
2026-04-13 18:28:53 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-13 18:28:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:28:53 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:28:53 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-13 18:28:53 | 
🎲 Бросок сейвы (save): 12D6
2026-04-13 18:28:53 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 5. HP: 10.0 -> 5.0 (shooting)
2026-04-13 18:28:53 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-04-13 18:28:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 5.0
2026-04-13 18:28:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:28:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:28:53 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:28:53 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:28:53 | Оружие: Gauss flayer
2026-04-13 18:28:53 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:53 | BS оружия: 4+
2026-04-13 18:28:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:28:53 | Save цели: 4+ (invul: нет)
2026-04-13 18:28:53 | Benefit of Cover: не активен.
2026-04-13 18:28:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:28:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:28:53 | Hit rolls:    [6, 5, 3, 3, 4, 6, 5, 6, 6, 6, 3, 6, 5, 3, 2, 2, 6, 6, 4, 4]  -> hits: 14 (crits: 8)
2026-04-13 18:28:53 | Wound rolls:  [4, 1, 5, 5, 5, 3]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 8 = 12
2026-04-13 18:28:53 | Save rolls:   [6, 3, 1, 5, 3, 5, 4, 2, 5, 5, 4, 1]  (цель 4+) -> failed saves: 5
2026-04-13 18:28:53 | FX: найден failed saves = 5.
2026-04-13 18:28:53 | 
✅ Итог по движку: прошло урона = 5.0
2026-04-13 18:28:53 | FX: найден итог урона = 5.0.
2026-04-13 18:28:53 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=5.0, outcome=damage).
2026-04-13 18:28:53 | FX: позиция эффекта start=(324.0,252.0) end=(636.0,300.0).
2026-04-13 18:28:53 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:28:53 | 📌 -------------------------

2026-04-13 18:28:59 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 5, 1, 3, 6]
2026-04-13 18:28:59 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-13 18:28:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:28:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:28:59 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-13 18:28:59 | 
🎲 Бросок сейвы (save): 5D6
2026-04-13 18:28:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 3. HP: 5.0 -> 3.0 (shooting)
2026-04-13 18:28:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 3. Причина: потери моделей.
2026-04-13 18:28:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-13 18:28:59 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:28:59 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:28:59 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:28:59 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:28:59 | Оружие: Gauss flayer
2026-04-13 18:28:59 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:28:59 | BS оружия: 4+
2026-04-13 18:28:59 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:28:59 | Save цели: 4+ (invul: нет)
2026-04-13 18:28:59 | Benefit of Cover: не активен.
2026-04-13 18:28:59 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:28:59 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:28:59 | Hit rolls:    [6, 6, 5, 2, 5, 1, 1, 4, 3, 6]  -> hits: 6 (crits: 3)
2026-04-13 18:28:59 | Wound rolls:  [4, 3, 5]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 3 = 5
2026-04-13 18:28:59 | Save rolls:   [6, 5, 1, 3, 6]  (цель 4+) -> failed saves: 2
2026-04-13 18:28:59 | FX: найден failed saves = 2.
2026-04-13 18:28:59 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-13 18:28:59 | FX: найден итог урона = 2.0.
2026-04-13 18:28:59 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-13 18:28:59 | FX: позиция эффекта start=(132.0,36.0) end=(636.0,300.0).
2026-04-13 18:28:59 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:28:59 | 📌 -------------------------

2026-04-13 18:28:59 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:30:58 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:30:58 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:30:58 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:30:58 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:30:58 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:30:58 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:30:58 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:30:58 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:30:58 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:30:58 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:30:58 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:31:00 | Roll-off Attacker/Defender: enemy=2 model=1 -> attacker=enemy
2026-04-13 18:31:00 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:31:00 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:31:00 | [DEPLOY][Only War] attacker=enemy -> LEFT x=0..14; defender=model -> RIGHT x=45..59
2026-04-13 18:31:00 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:31:00 | [DEPLOY] Order: enemy first, alternating
2026-04-13 18:31:00 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:31:00 | Ошибка деплоя: reason=outside_deploy_zone, x=47, y=26. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-13 18:31:02 | REQ: deploy cell accepted x=11, y=28
2026-04-13 18:31:02 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,11)
2026-04-13 18:31:02 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,11)
2026-04-13 18:31:02 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:31:02 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=950, coord=(15,50), attempt=1, reward=+0.022, score_before=0.000, score_after=0.441, reward_delta=+0.022, forward=0.149, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:31:02 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (15,50)
2026-04-13 18:31:02 | REQ: deploy cell accepted x=11, y=17
2026-04-13 18:31:02 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,11)
2026-04-13 18:31:02 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,11)
2026-04-13 18:31:02 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:31:02 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1196, coord=(19,56), attempt=1, reward=-0.007, score_before=0.441, score_after=0.302, reward_delta=-0.007, forward=0.098, spread=0.667, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:31:02 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (19,56)
2026-04-13 18:31:02 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.015 total_deploy_reward=+0.015 avg_forward=0.124 avg_spread=0.833 avg_edge=0.875 avg_cover=0.000
2026-04-13 18:31:02 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.015076862435947969, 'units': 2, 'total_deploy_reward': 0.015076862435947969, 'forward_sum': 0.24745762711864397, 'spread_sum': 1.6666666666666665, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.12372881355932198, 'avg_spread': 0.8333333333333333, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-04-13 18:31:02 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:31:02 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:31:02 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:31:02 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:31:02 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:31:02 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:31:02 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:04 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:31:04 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:31:04 | --- ХОД PLAYER ---
2026-04-13 18:31:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:31:04 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:31:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:31:04 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:05 | REQ: move cell accepted (RMB) x=22, y=28, mode=advance
2026-04-13 18:31:05 | [MOVE] unit=11 advance to=(22,28) dist=11 M=5 adv=6
2026-04-13 18:31:05 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:31:06 | REQ: move cell accepted (RMB) x=22, y=19, mode=advance
2026-04-13 18:31:06 | [MOVE] unit=12 advance to=(22,19) dist=11 M=5 adv=6
2026-04-13 18:31:07 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:31:07 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:31:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:31:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:31:07 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:31:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:31:07 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:31:07 | Нет доступных целей для чарджа.
2026-04-13 18:31:07 | --- ФАЗА БОЯ ---
2026-04-13 18:31:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:07 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:07 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:07 | --- ХОД MODEL ---
2026-04-13 18:31:07 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:31:07 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:31:07 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:31:08 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:31:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 50). Выбор reachable_idx=14/481, mode=normal, advance=нет, distance=4
2026-04-13 18:31:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (11, 47)
2026-04-13 18:31:08 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:31:09 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:31:09 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 56). Выбор reachable_idx=15/343, mode=normal, advance=нет, distance=4
2026-04-13 18:31:09 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 56)
2026-04-13 18:31:09 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:31:09 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:31:09 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(22, 19), target_filter_size=1, max_target_dist=25, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:31:09 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(22, 19), full_cells=24, rapid_cells=12, вошло=1880, rapid=625, не вошло=520, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:31:09 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1, 2]
2026-04-13 18:31:10 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:31:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-13 18:31:10 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:31:10 | 
🎲 Бросок на ранение (to wound): 7D6
2026-04-13 18:31:10 | 
🎲 Бросок сейвы (save): 3D6
2026-04-13 18:31:10 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (shooting)
2026-04-13 18:31:10 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-13 18:31:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-04-13 18:31:10 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:31:10 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:31:10 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:31:10 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:10 | Оружие: Gauss flayer
2026-04-13 18:31:10 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:10 | BS оружия: 4+
2026-04-13 18:31:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:31:10 | Save цели: 4+ (invul: нет)
2026-04-13 18:31:10 | Benefit of Cover: не активен.
2026-04-13 18:31:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:31:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:31:10 | Hit rolls:    [5, 6, 2, 4, 4, 5, 3, 5, 4, 5]  -> hits: 8 (crits: 1)
2026-04-13 18:31:10 | Wound rolls:  [3, 2, 3, 3, 5, 4, 3]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-04-13 18:31:10 | Save rolls:   [1, 1, 2]  (цель 4+) -> failed saves: 3
2026-04-13 18:31:10 | FX: найден failed saves = 3.
2026-04-13 18:31:10 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:31:10 | FX: найден итог урона = 3.0.
2026-04-13 18:31:10 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:31:10 | FX: позиция эффекта start=(1140.0,276.0) end=(540.0,468.0).
2026-04-13 18:31:10 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:31:10 | 📌 -------------------------

2026-04-13 18:31:12 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:31:12 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:12 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:31:12 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:31:14 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:31:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:31:14 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:31:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:31:14 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:31:14 | --- ФАЗА БОЯ ---
2026-04-13 18:31:14 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:31:14 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:31:14 | Итерация 0 завершена с наградой tensor([0.1246], device='cuda:0'), здоровье игрока [10.0, 7.0], здоровье модели [10.0, 10.0]
2026-04-13 18:31:14 | {'model health': [10.0, 10.0], 'player health': [10.0, 7.0], 'model alive models': [10, 10], 'player alive models': [10, 7], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:31:14 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 7.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

2026-04-13 18:31:14 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:14 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:31:14 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:14 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:14 | FX: найден failed saves = 3.
2026-04-13 18:31:14 | FX: найден итог урона = 3.0.
2026-04-13 18:31:14 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:31:17 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:31:17 | --- ХОД PLAYER ---
2026-04-13 18:31:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:31:17 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:31:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:31:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-13 18:31:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:31:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-13 18:31:18 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:31:18 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:31:20 | REQ: move cell accepted (RMB) x=33, y=23, mode=advance
2026-04-13 18:31:20 | [MOVE] unit=11 advance to=(33,23) dist=11 M=5 adv=6
2026-04-13 18:31:20 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 3, 4, 2]
2026-04-13 18:31:20 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:31:20 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:31:20 | 
🎲 Бросок сейвы (save): 4D6
2026-04-13 18:31:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (Overwatch)
2026-04-13 18:31:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-13 18:31:20 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 3.0.
2026-04-13 18:31:20 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:31:20 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:31:20 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:31:20 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:31:20 | Оружие: Gauss flayer
2026-04-13 18:31:20 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:20 | BS оружия: 4+
2026-04-13 18:31:20 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:31:20 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:31:20 | Save цели: 4+ (invul: нет)
2026-04-13 18:31:20 | Benefit of Cover: не активен.
2026-04-13 18:31:20 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:31:20 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:31:20 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:31:20 | Hit rolls:    [5, 2, 2, 6, 1, 6, 6, 5, 2, 3, 1, 4, 4, 2, 6, 3, 5, 4, 5, 2]  -> hits: 4 (crits: 4)
2026-04-13 18:31:20 | Save rolls:   [3, 3, 4, 2]  (цель 4+) -> failed saves: 3
2026-04-13 18:31:20 | FX: найден failed saves = 3.
2026-04-13 18:31:20 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:31:20 | FX: найден итог урона = 3.0.
2026-04-13 18:31:20 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:31:20 | FX: позиция эффекта start=(1140.0,276.0) end=(540.0,684.0).
2026-04-13 18:31:20 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:31:20 | 📌 -------------------------

2026-04-13 18:31:21 | REQ: move cell accepted (RMB) x=33, y=15, mode=advance
2026-04-13 18:31:21 | [MOVE] unit=12 advance to=(33,15) dist=11 M=5 adv=6
2026-04-13 18:31:22 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 2]
2026-04-13 18:31:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:31:22 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:31:22 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:31:22 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 6. HP: 8.0 -> 6.0 (Overwatch)
2026-04-13 18:31:22 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-04-13 18:31:22 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-13 18:31:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:31:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:31:22 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:31:22 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:22 | Оружие: Gauss flayer
2026-04-13 18:31:22 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:22 | BS оружия: 4+
2026-04-13 18:31:22 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:31:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:31:22 | Save цели: 4+ (invul: нет)
2026-04-13 18:31:22 | Benefit of Cover: не активен.
2026-04-13 18:31:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:31:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:31:22 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:31:22 | Hit rolls:    [1, 4, 4, 5, 4, 2, 1, 1, 3, 2, 3, 5, 3, 1, 4, 3, 2, 1, 6, 6]  -> hits: 2 (crits: 2)
2026-04-13 18:31:22 | Save rolls:   [2, 2]  (цель 4+) -> failed saves: 2
2026-04-13 18:31:22 | FX: найден failed saves = 2.
2026-04-13 18:31:22 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-13 18:31:22 | FX: найден итог урона = 2.0.
2026-04-13 18:31:22 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-13 18:31:22 | FX: позиция эффекта start=(1140.0,276.0) end=(540.0,468.0).
2026-04-13 18:31:22 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:31:22 | 📌 -------------------------

2026-04-13 18:31:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:31:22 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:31:22 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:31:22 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:31:22 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:31:22 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:31:22 | Нет доступных целей для чарджа.
2026-04-13 18:31:22 | --- ФАЗА БОЯ ---
2026-04-13 18:31:22 | --- ХОД MODEL ---
2026-04-13 18:31:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:31:22 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:31:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:31:32 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-13 18:31:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 47). Выбор reachable_idx=14/524, mode=normal, advance=нет, distance=4
2026-04-13 18:31:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 44)
2026-04-13 18:31:32 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:31:32 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:32 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:31:32 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:32 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:32 | FX: найден failed saves = 2.
2026-04-13 18:31:32 | FX: найден итог урона = 2.0.
2026-04-13 18:31:32 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:31:34 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:36 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-13 18:31:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 56). Выбор reachable_idx=15/344, mode=normal, advance=нет, distance=4
2026-04-13 18:31:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (11, 56)
2026-04-13 18:31:36 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:31:36 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:37 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:31:37 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:37 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 15), target_filter_size=2, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:31:37 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 15), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:31:39 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 4, 4, 3, 3, 1, 1, 5, 3, 1]
2026-04-13 18:31:39 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-13 18:31:39 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:31:39 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:31:39 | 
🎲 Бросок на ранение (to wound): 8D6
2026-04-13 18:31:39 | 
🎲 Бросок сейвы (save): 10D6
2026-04-13 18:31:39 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 6. Осталось: 0. HP: 6.0 -> 0.0 (shooting)
2026-04-13 18:31:39 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 0. Причина: потери моделей.
2026-04-13 18:31:39 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 6.0
2026-04-13 18:31:39 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:31:39 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:31:39 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:31:39 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:39 | Оружие: Gauss flayer
2026-04-13 18:31:39 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:39 | BS оружия: 4+
2026-04-13 18:31:39 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:31:39 | Save цели: 4+ (invul: нет)
2026-04-13 18:31:39 | Benefit of Cover: не активен.
2026-04-13 18:31:39 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:31:39 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:31:39 | Hit rolls:    [5, 2, 4, 2, 4, 1, 1, 6, 5, 4, 4, 6, 5, 6, 6, 1, 6, 5, 3, 1]  -> hits: 13 (crits: 5)
2026-04-13 18:31:39 | Wound rolls:  [5, 2, 2, 5, 4, 4, 6, 2]  (цель 4+) -> rolled wounds: 5 + auto(w/LETHAL): 5 = 10
2026-04-13 18:31:39 | Save rolls:   [4, 4, 4, 3, 3, 1, 1, 5, 3, 1]  (цель 4+) -> failed saves: 6
2026-04-13 18:31:39 | FX: найден failed saves = 6.
2026-04-13 18:31:39 | 
✅ Итог по движку: прошло урона = 6.0
2026-04-13 18:31:39 | FX: найден итог урона = 6.0.
2026-04-13 18:31:39 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=6.0, outcome=damage).
2026-04-13 18:31:39 | FX: позиция эффекта start=(1068.0,180.0) end=(804.0,372.0).
2026-04-13 18:31:39 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:31:39 | 📌 -------------------------

2026-04-13 18:31:41 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-13 18:31:41 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:31:41 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана недоступная цель (raw=1). Стрельба пропущена.
2026-04-13 18:31:41 | [MODEL][SHOOT] Невалидный выбор цели: raw=1, доступные=[0] (ожидался индекс 0..0). Стрельба пропущена.
2026-04-13 18:31:41 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:31:42 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-13 18:31:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:31:42 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:31:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:31:42 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:31:42 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:42 | FX: найден failed saves = 6.
2026-04-13 18:31:42 | FX: найден итог урона = 6.0.
2026-04-13 18:31:42 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:31:43 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-13 18:31:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:31:43 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:31:43 | --- ФАЗА БОЯ ---
2026-04-13 18:31:43 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:31:43 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-13 18:31:43 | Итерация 1 завершена с наградой tensor([0.4463], device='cuda:0'), здоровье игрока [7.0, 0.0], здоровье модели [10.0, 10.0]
2026-04-13 18:31:43 | {'model health': [10.0, 10.0], 'player health': [7.0, 0.0], 'model alive models': [10, 10], 'player alive models': [7, 0], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': [0]}
2026-04-13 18:31:43 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [7.0, 0.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 6.0 раз(а)

2026-04-13 18:31:44 | === БОЕВОЙ РАУНД 3 ===
2026-04-13 18:31:44 | --- ХОД PLAYER ---
2026-04-13 18:31:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:31:44 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:31:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:31:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-13 18:31:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:31:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-13 18:31:46 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:31:46 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:31:48 | REQ: move cell accepted (RMB) x=38, y=21, mode=normal
2026-04-13 18:31:48 | [MOVE] unit=11 normal to=(38,21) dist=5 M=5
2026-04-13 18:31:48 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 6]
2026-04-13 18:31:49 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:31:49 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:31:49 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:31:49 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:31:49 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:31:49 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:31:49 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:31:49 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:31:49 | Оружие: Gauss flayer
2026-04-13 18:31:49 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:31:49 | BS оружия: 4+
2026-04-13 18:31:49 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:31:49 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:31:49 | Save цели: 4+ (invul: нет)
2026-04-13 18:31:49 | Benefit of Cover: не активен.
2026-04-13 18:31:49 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:31:49 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:31:49 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:31:49 | Hit rolls:    [5, 3, 2, 2, 5, 3, 1, 2, 5, 6, 4, 4, 1, 2, 4, 6, 2, 1, 1, 1]  -> hits: 2 (crits: 2)
2026-04-13 18:31:49 | Save rolls:   [6, 6]  (цель 4+) -> failed saves: 0
2026-04-13 18:31:49 | FX: найден failed saves = 0.
2026-04-13 18:31:49 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:31:49 | FX: найден итог урона = 0.0.
2026-04-13 18:31:49 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:31:49 | FX: позиция эффекта start=(1068.0,180.0) end=(804.0,564.0).
2026-04-13 18:31:49 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:31:49 | 📌 -------------------------

2026-04-13 18:31:49 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:31:49 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-13 18:31:49 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 23), target_filter_size=2, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:31:49 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(33, 23), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:31:49 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 21), target_filter_size=2, max_target_dist=18, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:31:49 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(38, 21), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:31:51 | 
🎲 Бросок на попадание (to hit): 16D6
2026-04-13 18:31:51 | REQ: движок запросил кубы стрельбы (target=21, count=16, stage=hit).
2026-04-13 18:31:58 | 
🎲 Бросок на ранение (to wound): 8D6
2026-04-13 18:31:58 | REQ: движок запросил кубы стрельбы (target=21, count=8, stage=wound).
2026-04-13 18:32:02 | 
🎲 Бросок сейвы (save): 5D6
2026-04-13 18:32:02 | REQ: движок запросил кубы стрельбы (target=21, count=5, stage=save).
2026-04-13 18:32:06 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 2, 3, 4, 5]
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-13 18:32:06 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:32:06 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:32:06 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:32:06 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:32:06 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-04-13 18:32:06 | Оружие: Gauss flayer
2026-04-13 18:32:06 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:32:06 | BS оружия: 4+
2026-04-13 18:32:06 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:32:06 | Save цели: 4+ (invul: нет)
2026-04-13 18:32:06 | Benefit of Cover: не активен.
2026-04-13 18:32:06 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:32:06 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:32:06 | Hit rolls:    [2, 3, 4, 5, 6, 5, 6, 5, 4, 3, 4, 4, 3, 2, 3, 4]  -> hits: 10 (crits: 2)
2026-04-13 18:32:06 | Wound rolls:  [1, 2, 3, 4, 5, 6, 1, 2]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-04-13 18:32:06 | Save rolls:   [1, 2, 3, 4, 5]  (цель 4+) -> failed saves: 3
2026-04-13 18:32:06 | FX: найден failed saves = 3.
2026-04-13 18:32:06 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:32:06 | FX: найден итог урона = 3.0.
2026-04-13 18:32:06 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:32:06 | FX: позиция эффекта start=(924.0,516.0) end=(1068.0,180.0).
2026-04-13 18:32:06 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-04-13 18:32:06 | 📌 -------------------------

2026-04-13 18:32:06 | Unit 12 — Necrons Necron Warriors (x10 моделей): юнит мертв — стрельба пропущена.
2026-04-13 18:32:06 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:32:06 | Нет доступных целей для чарджа.
2026-04-13 18:32:06 | --- ФАЗА БОЯ ---
2026-04-13 18:32:06 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:32:06 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:32:06 | --- ХОД MODEL ---
2026-04-13 18:32:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:32:06 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-13 18:32:06 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:32:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:33:21 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:33:21 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:33:21 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:33:21 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:33:21 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:33:21 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:33:21 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:33:21 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:33:21 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:33:21 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:33:21 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:33:23 | Roll-off Attacker/Defender: enemy=2 model=4 -> attacker=model
2026-04-13 18:33:23 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:33:23 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:33:23 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:33:23 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:33:23 | [DEPLOY] Order: model first, alternating
2026-04-13 18:33:23 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:33:23 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2105, coord=(35,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:33:23 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,5)
2026-04-13 18:33:23 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:33:23 | REQ: deploy cell accepted x=50, y=26
2026-04-13 18:33:23 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-04-13 18:33:23 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,50)
2026-04-13 18:33:23 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:33:23 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=970, coord=(16,10), attempt=1, reward=+0.001, score_before=0.413, score_after=0.433, reward_delta=+0.001, forward=0.131, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:33:23 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (16,10)
2026-04-13 18:33:24 | REQ: deploy cell accepted x=50, y=22
2026-04-13 18:33:24 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,50)
2026-04-13 18:33:24 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,50)
2026-04-13 18:33:24 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.109 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-13 18:33:24 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021639731966890025, 'units': 2, 'total_deploy_reward': 0.021639731966890025, 'forward_sum': 0.21864406779661016, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10932203389830508, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-13 18:33:24 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:33:24 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:33:24 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:33:24 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:33:24 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:33:24 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:33:24 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:33:25 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:33:25 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:33:25 | --- ХОД PLAYER ---
2026-04-13 18:33:25 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:33:25 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:33:25 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:33:25 | REQ: move cell accepted (RMB) x=39, y=27, mode=advance
2026-04-13 18:33:25 | [MOVE] unit=11 advance to=(39,27) dist=11 M=5 adv=6
2026-04-13 18:33:26 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:33:26 | REQ: move cell accepted (RMB) x=39, y=20, mode=advance
2026-04-13 18:33:26 | [MOVE] unit=12 advance to=(39,20) dist=11 M=5 adv=6
2026-04-13 18:33:27 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:33:27 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:33:27 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:33:27 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:33:27 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:33:27 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:33:27 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:33:27 | Нет доступных целей для чарджа.
2026-04-13 18:33:27 | --- ФАЗА БОЯ ---
2026-04-13 18:33:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:27 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:27 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:27 | --- ХОД MODEL ---
2026-04-13 18:33:27 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:33:27 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:33:27 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:33:28 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:33:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 5). Выбор reachable_idx=10/271, mode=normal, advance=нет, distance=5
2026-04-13 18:33:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 9)
2026-04-13 18:33:28 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:33:29 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:33:29 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 10). Выбор reachable_idx=6/505, mode=normal, advance=нет, distance=5
2026-04-13 18:33:29 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (11, 10)
2026-04-13 18:33:29 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:33:29 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:33:29 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(39, 20), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:33:29 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(39, 20), full_cells=24, rapid_cells=12, вошло=1800, rapid=625, не вошло=600, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:33:29 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:33:29 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:29 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:33:30 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:33:30 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:30 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:33:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:33:30 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:33:31 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:33:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:33:31 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:33:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:33:31 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:33:31 | --- ФАЗА БОЯ ---
2026-04-13 18:33:31 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:33:31 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:33:31 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-13 18:33:31 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:33:31 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:33:32 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:33:32 | --- ХОД PLAYER ---
2026-04-13 18:33:32 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:33:32 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:33:32 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:33:34 | REQ: move cell accepted (RMB) x=28, y=28, mode=advance
2026-04-13 18:33:34 | [MOVE] unit=11 advance to=(28,28) dist=11 M=5 adv=6
2026-04-13 18:33:34 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5]
2026-04-13 18:33:34 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:33:34 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:33:34 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:33:34 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:33:34 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:33:34 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:33:34 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:33:34 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:33:34 | Оружие: Gauss flayer
2026-04-13 18:33:34 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:33:34 | BS оружия: 4+
2026-04-13 18:33:34 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:33:34 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:33:34 | Save цели: 4+ (invul: нет)
2026-04-13 18:33:34 | Benefit of Cover: не активен.
2026-04-13 18:33:34 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:33:34 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:33:34 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:33:34 | Hit rolls:    [2, 2, 6, 1, 4, 2, 5, 2, 3, 1]  -> hits: 1 (crits: 1)
2026-04-13 18:33:34 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-04-13 18:33:34 | FX: найден failed saves = 0.
2026-04-13 18:33:34 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:33:34 | FX: найден итог урона = 0.0.
2026-04-13 18:33:34 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:33:34 | FX: позиция эффекта start=(228.0,732.0) end=(948.0,660.0).
2026-04-13 18:33:34 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:33:34 | 📌 -------------------------

2026-04-13 18:33:35 | REQ: move cell accepted (RMB) x=28, y=22, mode=advance
2026-04-13 18:33:35 | [MOVE] unit=12 advance to=(28,22) dist=11 M=5 adv=6
2026-04-13 18:33:35 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6]
2026-04-13 18:33:36 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:33:36 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:33:36 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:33:36 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:33:36 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:33:36 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:33:36 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:33:36 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:33:36 | Оружие: Gauss flayer
2026-04-13 18:33:36 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:33:36 | BS оружия: 4+
2026-04-13 18:33:36 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:33:36 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:33:36 | Save цели: 4+ (invul: нет)
2026-04-13 18:33:36 | Benefit of Cover: не активен.
2026-04-13 18:33:36 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:33:36 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:33:36 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:33:36 | Hit rolls:    [1, 1, 4, 4, 2, 5, 3, 5, 6, 1]  -> hits: 1 (crits: 1)
2026-04-13 18:33:36 | Save rolls:   [6]  (цель 4+) -> failed saves: 0
2026-04-13 18:33:36 | FX: найден failed saves = 0.
2026-04-13 18:33:36 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:33:36 | FX: найден итог урона = 0.0.
2026-04-13 18:33:36 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:33:36 | FX: позиция эффекта start=(228.0,732.0) end=(948.0,492.0).
2026-04-13 18:33:36 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:33:36 | 📌 -------------------------

2026-04-13 18:33:36 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:33:36 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:33:36 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:33:36 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:33:36 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:33:36 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:33:36 | Нет доступных целей для чарджа.
2026-04-13 18:33:36 | --- ФАЗА БОЯ ---
2026-04-13 18:33:36 | --- ХОД MODEL ---
2026-04-13 18:33:36 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:33:36 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:33:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:33:38 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-13 18:33:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 9). Выбор reachable_idx=10/440, mode=normal, advance=нет, distance=5
2026-04-13 18:33:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 13)
2026-04-13 18:33:38 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:33:38 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:33:38 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:33:38 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:33:38 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:33:38 | FX: найден failed saves = 0.
2026-04-13 18:33:38 | FX: найден итог урона = 0.0.
2026-04-13 18:33:38 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:33:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:33:40 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-13 18:33:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 10). Выбор reachable_idx=6/505, mode=normal, advance=нет, distance=5
2026-04-13 18:33:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (6, 10)
2026-04-13 18:33:40 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:33:40 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:33:41 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:33:41 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(28, 22), target_filter_size=2, max_target_dist=18, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:33:41 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(28, 22), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:33:42 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 1, 3, 4, 6, 3, 4]
2026-04-13 18:33:42 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-13 18:33:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-13 18:33:42 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:33:42 | 
🎲 Бросок на ранение (to wound): 9D6
2026-04-13 18:33:42 | 
🎲 Бросок сейвы (save): 7D6
2026-04-13 18:33:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (shooting)
2026-04-13 18:33:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-13 18:33:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-04-13 18:33:42 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:33:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:33:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:33:42 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:33:42 | Оружие: Gauss flayer
2026-04-13 18:33:42 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:33:42 | BS оружия: 4+
2026-04-13 18:33:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:33:42 | Save цели: 4+ (invul: нет)
2026-04-13 18:33:42 | Benefit of Cover: не активен.
2026-04-13 18:33:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:33:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:33:42 | Hit rolls:    [4, 4, 1, 1, 3, 3, 4, 2, 4, 1, 4, 5, 2, 5, 2, 2, 2, 4, 4, 1]  -> hits: 9
2026-04-13 18:33:42 | Wound rolls:  [5, 2, 4, 1, 6, 4, 4, 4, 4]  (цель 4+) -> wounds: 7
2026-04-13 18:33:42 | Save rolls:   [4, 1, 3, 4, 6, 3, 4]  (цель 4+) -> failed saves: 3
2026-04-13 18:33:42 | FX: найден failed saves = 3.
2026-04-13 18:33:42 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:33:42 | FX: найден итог урона = 3.0.
2026-04-13 18:33:42 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:33:42 | FX: позиция эффекта start=(324.0,612.0) end=(684.0,540.0).
2026-04-13 18:33:42 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:33:42 | 📌 -------------------------

2026-04-13 18:57:59 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-13 18:57:59 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-13 18:57:59 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-13 18:57:59 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-13 18:58:00 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:58:00 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-13 18:58:00 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-13 18:58:00 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-13 18:58:00 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-13 18:58:00 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-13 18:58:00 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-13 18:58:11 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-13 18:58:11 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-13 18:58:11 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-13 18:58:11 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-13 18:58:11 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-13 18:58:11 | [DEPLOY] Order: model first, alternating
2026-04-13 18:58:11 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:58:11 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=432, coord=(7,12), attempt=1, reward=+0.023, score_before=0.000, score_after=0.468, reward_delta=+0.023, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:58:11 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (7,12)
2026-04-13 18:58:11 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-13 18:58:11 | REQ: deploy cell accepted x=49, y=26
2026-04-13 18:58:11 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-13 18:58:11 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-13 18:58:11 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-13 18:58:11 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=906, coord=(15,6), attempt=1, reward=-0.001, score_before=0.468, score_after=0.445, reward_delta=-0.001, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-13 18:58:11 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (15,6)
2026-04-13 18:58:12 | REQ: deploy cell accepted x=48, y=17
2026-04-13 18:58:12 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,48)
2026-04-13 18:58:12 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,48)
2026-04-13 18:58:12 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.181 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-13 18:58:12 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02223098147418211, 'units': 2, 'total_deploy_reward': 0.02223098147418211, 'forward_sum': 0.3627118644067796, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1813559322033898, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-13 18:58:12 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-13 18:58:12 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-13 18:58:12 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-13 18:58:12 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-13 18:58:12 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:58:12 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-13 18:58:12 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=18, cells_rapid=9, rapid_fire=1, source_cell=(28, 22), target_filter_size=2, max_target_dist=18, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:58:12 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(28, 22), full_cells=18, rapid_cells=9, вошло=1332, rapid=361, не вошло=1068, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:58:12 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(48, 17), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:58:12 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:13 | === БОЕВОЙ РАУНД 1 ===
2026-04-13 18:58:13 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-13 18:58:13 | --- ХОД PLAYER ---
2026-04-13 18:58:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:58:13 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:58:13 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:58:14 | REQ: move cell accepted (RMB) x=38, y=22, mode=advance
2026-04-13 18:58:14 | [MOVE] unit=11 advance to=(38,22) dist=11 M=5 adv=6
2026-04-13 18:58:14 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:58:14 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:15 | REQ: move cell accepted (RMB) x=37, y=15, mode=advance
2026-04-13 18:58:15 | [MOVE] unit=12 advance to=(37,15) dist=11 M=5 adv=6
2026-04-13 18:58:15 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6]
2026-04-13 18:58:15 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:58:15 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:58:15 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:58:15 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:58:15 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:58:15 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:15 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:58:15 | Оружие: Gauss flayer
2026-04-13 18:58:15 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:15 | BS оружия: 4+
2026-04-13 18:58:15 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:58:15 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:15 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:15 | Benefit of Cover: не активен.
2026-04-13 18:58:15 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:15 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:15 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:58:15 | Hit rolls:    [4, 3, 6, 4, 2, 4, 2, 2, 1, 1]  -> hits: 1 (crits: 1)
2026-04-13 18:58:15 | Save rolls:   [6]  (цель 4+) -> failed saves: 0
2026-04-13 18:58:15 | FX: найден failed saves = 0.
2026-04-13 18:58:15 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:58:15 | FX: найден итог урона = 0.0.
2026-04-13 18:58:15 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-13 18:58:15 | FX: позиция эффекта start=(300.0,180.0) end=(1164.0,420.0).
2026-04-13 18:58:15 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:58:15 | 📌 -------------------------

2026-04-13 18:58:15 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:58:15 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:58:15 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:58:15 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:58:15 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:58:15 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:58:15 | Нет доступных целей для чарджа.
2026-04-13 18:58:15 | --- ФАЗА БОЯ ---
2026-04-13 18:58:15 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:58:15 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:58:15 | --- ХОД MODEL ---
2026-04-13 18:58:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:58:15 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:58:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:58:17 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-13 18:58:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 12). Выбор reachable_idx=10/432, mode=normal, advance=нет, distance=5
2026-04-13 18:58:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (2, 16)
2026-04-13 18:58:17 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:17 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:18 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:19 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-13 18:58:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (15, 6). Выбор reachable_idx=6/413, mode=normal, advance=нет, distance=5
2026-04-13 18:58:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (10, 6)
2026-04-13 18:58:19 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-13 18:58:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:58:19 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:19 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 15), target_filter_size=1, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:58:19 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(37, 15), full_cells=24, rapid_cells=12, вошло=1880, rapid=625, не вошло=520, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:58:21 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1]
2026-04-13 18:58:21 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-13 18:58:21 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:58:21 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:58:21 | 
🎲 Бросок на ранение (to wound): 5D6
2026-04-13 18:58:21 | 
🎲 Бросок сейвы (save): 1D6
2026-04-13 18:58:21 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-13 18:58:21 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:58:21 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-13 18:58:21 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:58:21 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:58:21 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:21 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:58:21 | Оружие: Gauss flayer
2026-04-13 18:58:21 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:21 | BS оружия: 4+
2026-04-13 18:58:21 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:21 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:21 | Benefit of Cover: не активен.
2026-04-13 18:58:21 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:21 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:21 | Hit rolls:    [4, 4, 5, 5, 6, 2, 2, 1, 3, 5]  -> hits: 6 (crits: 1)
2026-04-13 18:58:21 | Wound rolls:  [1, 1, 2, 2, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-04-13 18:58:21 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-04-13 18:58:21 | FX: найден failed saves = 1.
2026-04-13 18:58:21 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:58:21 | FX: найден итог урона = 1.0.
2026-04-13 18:58:21 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:58:21 | FX: позиция эффекта start=(396.0,60.0) end=(900.0,372.0).
2026-04-13 18:58:21 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:58:21 | 📌 -------------------------

2026-04-13 18:58:24 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-13 18:58:24 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:58:24 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-13 18:58:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-13 18:58:24 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:58:25 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-13 18:58:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:58:26 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-13 18:58:26 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:58:26 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:58:26 | --- ФАЗА БОЯ ---
2026-04-13 18:58:26 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:58:26 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-13 18:58:26 | Итерация 0 завершена с наградой tensor([0.0703], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-04-13 18:58:26 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-13 18:58:26 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-13 18:58:26 | === БОЕВОЙ РАУНД 2 ===
2026-04-13 18:58:26 | --- ХОД PLAYER ---
2026-04-13 18:58:26 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:58:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-13 18:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-13 18:58:28 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-13 18:58:28 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:58:30 | REQ: move cell accepted (RMB) x=27, y=16, mode=advance
2026-04-13 18:58:30 | [MOVE] unit=11 advance to=(27,16) dist=11 M=5 adv=6
2026-04-13 18:58:31 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 5, 5]
2026-04-13 18:58:31 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:31 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:58:31 | 
🎲 Бросок сейвы (save): 3D6
2026-04-13 18:58:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-13 18:58:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-13 18:58:31 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-13 18:58:31 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:58:31 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:58:31 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:31 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-13 18:58:31 | Оружие: Gauss flayer
2026-04-13 18:58:31 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:31 | BS оружия: 4+
2026-04-13 18:58:31 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:58:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:31 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:31 | Benefit of Cover: не активен.
2026-04-13 18:58:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:31 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:58:31 | Hit rolls:    [2, 2, 2, 6, 1, 6, 4, 4, 4, 2, 4, 4, 2, 4, 2, 4, 4, 2, 6, 4]  -> hits: 3 (crits: 3)
2026-04-13 18:58:31 | Save rolls:   [3, 5, 5]  (цель 4+) -> failed saves: 1
2026-04-13 18:58:31 | FX: найден failed saves = 1.
2026-04-13 18:58:31 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:58:31 | FX: найден итог урона = 1.0.
2026-04-13 18:58:31 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:58:31 | FX: позиция эффекта start=(396.0,60.0) end=(924.0,540.0).
2026-04-13 18:58:31 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-13 18:58:31 | 📌 -------------------------

2026-04-13 18:58:33 | REQ: move cell accepted (RMB) x=27, y=11, mode=advance
2026-04-13 18:58:33 | [MOVE] unit=12 advance to=(27,11) dist=10 M=5 adv=5
2026-04-13 18:58:33 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 5]
2026-04-13 18:58:33 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:33 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:58:33 | 
🎲 Бросок сейвы (save): 2D6
2026-04-13 18:58:33 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-13 18:58:33 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-13 18:58:33 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:58:33 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:33 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:58:33 | Оружие: Gauss flayer
2026-04-13 18:58:33 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:33 | BS оружия: 4+
2026-04-13 18:58:33 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-13 18:58:33 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:33 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:33 | Benefit of Cover: не активен.
2026-04-13 18:58:33 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:33 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:33 | Правило: Overwatch: попадания только на 6+
2026-04-13 18:58:33 | Hit rolls:    [4, 6, 1, 1, 6, 3, 2, 2, 5, 2, 4, 2, 3, 1, 4, 3, 3, 2, 2, 1]  -> hits: 2 (crits: 2)
2026-04-13 18:58:33 | Save rolls:   [6, 5]  (цель 4+) -> failed saves: 0
2026-04-13 18:58:33 | FX: найден failed saves = 0.
2026-04-13 18:58:33 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-13 18:58:33 | FX: найден итог урона = 0.0.
2026-04-13 18:58:33 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:58:33 | 📌 -------------------------

2026-04-13 18:58:33 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:58:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:58:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-13 18:58:33 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:58:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:58:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-13 18:58:33 | Нет доступных целей для чарджа.
2026-04-13 18:58:33 | --- ФАЗА БОЯ ---
2026-04-13 18:58:33 | --- ХОД MODEL ---
2026-04-13 18:58:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:58:33 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:58:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-13 18:58:34 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-13 18:58:34 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 16). Выбор reachable_idx=10/316, mode=normal, advance=нет, distance=4
2026-04-13 18:58:34 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 20)
2026-04-13 18:58:34 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:34 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:34 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-13 18:58:34 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:58:34 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:34 | FX: найден failed saves = 0.
2026-04-13 18:58:34 | FX: найден итог урона = 0.0.
2026-04-13 18:58:34 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:58:36 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-13 18:58:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 6). Выбор reachable_idx=6/395, mode=normal, advance=нет, distance=5
2026-04-13 18:58:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 6)
2026-04-13 18:58:36 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-13 18:58:36 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:37 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-13 18:58:37 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:37 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(27, 11), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-13 18:58:37 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(27, 11), full_cells=24, rapid_cells=12, вошло=1764, rapid=600, не вошло=636, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-13 18:58:45 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 5, 5, 1, 1]
2026-04-13 18:58:45 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-13 18:58:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-13 18:58:45 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-13 18:58:45 | 
🎲 Бросок на ранение (to wound): 9D6
2026-04-13 18:58:45 | 
🎲 Бросок сейвы (save): 5D6
2026-04-13 18:58:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (shooting)
2026-04-13 18:58:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-13 18:58:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-04-13 18:58:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:58:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:58:45 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:45 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-13 18:58:45 | Оружие: Gauss flayer
2026-04-13 18:58:45 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:45 | BS оружия: 4+
2026-04-13 18:58:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:45 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:45 | Benefit of Cover: не активен.
2026-04-13 18:58:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:45 | Hit rolls:    [2, 6, 4, 6, 4, 4, 3, 4, 4, 2, 5, 5, 2, 4, 1, 5, 3, 2, 3, 3]  -> hits: 11 (crits: 2)
2026-04-13 18:58:45 | Wound rolls:  [1, 6, 3, 1, 2, 4, 3, 4, 3]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-04-13 18:58:45 | Save rolls:   [2, 5, 5, 1, 1]  (цель 4+) -> failed saves: 3
2026-04-13 18:58:45 | FX: найден failed saves = 3.
2026-04-13 18:58:45 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-13 18:58:45 | FX: найден итог урона = 3.0.
2026-04-13 18:58:45 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-13 18:58:45 | FX: позиция эффекта start=(468.0,36.0) end=(660.0,276.0).
2026-04-13 18:58:45 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-13 18:58:45 | 📌 -------------------------

2026-04-13 18:58:49 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 5, 5, 5]
2026-04-13 18:58:49 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-13 18:58:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-04-13 18:58:49 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-13 18:58:49 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-13 18:58:49 | 
🎲 Бросок сейвы (save): 4D6
2026-04-13 18:58:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 6. HP: 7.0 -> 6.0 (shooting)
2026-04-13 18:58:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-04-13 18:58:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-13 18:58:49 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-13 18:58:49 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:58:49 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-13 18:58:49 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:58:49 | Оружие: Gauss flayer
2026-04-13 18:58:49 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:49 | BS оружия: 4+
2026-04-13 18:58:49 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-13 18:58:49 | Save цели: 4+ (invul: нет)
2026-04-13 18:58:49 | Benefit of Cover: не активен.
2026-04-13 18:58:49 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-13 18:58:49 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-13 18:58:49 | Hit rolls:    [2, 1, 4, 2, 5, 5, 6, 6, 1, 3]  -> hits: 5 (crits: 2)
2026-04-13 18:58:49 | Wound rolls:  [6, 4, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-04-13 18:58:49 | Save rolls:   [1, 5, 5, 5]  (цель 4+) -> failed saves: 1
2026-04-13 18:58:49 | FX: найден failed saves = 1.
2026-04-13 18:58:49 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-13 18:58:49 | FX: найден итог урона = 1.0.
2026-04-13 18:58:49 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-13 18:58:49 | FX: позиция эффекта start=(156.0,132.0) end=(660.0,276.0).
2026-04-13 18:58:49 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-13 18:58:49 | 📌 -------------------------

2026-04-13 18:58:49 | --- ФАЗА ЧАРДЖА ---
2026-04-13 18:58:54 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-13 18:58:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:58:54 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-13 18:58:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-13 18:58:54 | [MODEL] Чардж: нет доступных целей
2026-04-13 18:58:54 | --- ФАЗА БОЯ ---
2026-04-13 18:58:54 | [MODEL] Ближний бой: нет доступных атак
2026-04-13 18:58:54 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-13 18:58:54 | Итерация 1 завершена с наградой tensor([0.2176], device='cuda:0'), здоровье игрока [9.0, 6.0], здоровье модели [10.0, 10.0]
2026-04-13 18:58:54 | {'model health': [10.0, 10.0], 'player health': [9.0, 6.0], 'model alive models': [10, 10], 'player alive models': [9, 6], 'modelCP': 1, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': [0]}
2026-04-13 18:58:54 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 6.0]
CP MODEL: 1, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-13 18:58:54 | FX: перепроигрываю 30 строк(и) лога.
2026-04-13 18:58:54 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-13 18:58:54 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-13 18:58:54 | FX: найдена строка оружия: Gauss flayer.
2026-04-13 18:58:54 | FX: найден failed saves = 1.
2026-04-13 18:58:54 | FX: найден итог урона = 1.0.
2026-04-13 18:58:54 | FX: дубликат отчёта, эффект не создаём.
2026-04-13 18:58:56 | === БОЕВОЙ РАУНД 3 ===
2026-04-13 18:58:56 | --- ХОД PLAYER ---
2026-04-13 18:58:56 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-13 18:58:56 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:58:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:58:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-13 18:58:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:58:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-13 18:58:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-13 18:59:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-13 18:59:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-04-13 18:59:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-13 18:59:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-13 18:59:01 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-13 18:59:01 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:03:40 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-14 18:03:40 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-14 18:03:40 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-14 18:03:40 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-14 18:03:41 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 18:03:41 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-14 18:03:41 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-14 18:03:41 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-14 18:03:41 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-14 18:03:41 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-14 18:03:41 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-14 18:03:43 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-04-14 18:03:43 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-14 18:03:43 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-14 18:03:43 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-14 18:03:43 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-14 18:03:43 | [DEPLOY] Order: model first, alternating
2026-04-14 18:03:43 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 18:03:43 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1504, coord=(25,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 18:03:43 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (25,4)
2026-04-14 18:03:43 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 18:03:44 | REQ: deploy cell accepted x=49, y=29
2026-04-14 18:03:44 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-04-14 18:03:44 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,49)
2026-04-14 18:03:44 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 18:03:44 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1808, coord=(30,8), attempt=1, reward=-0.002, score_before=0.405, score_after=0.374, reward_delta=-0.002, forward=0.105, spread=0.833, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 18:03:44 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (30,8)
2026-04-14 18:03:44 | REQ: deploy cell accepted x=49, y=22
2026-04-14 18:03:44 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,49)
2026-04-14 18:03:44 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,49)
2026-04-14 18:03:44 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.088 avg_spread=0.917 avg_edge=1.000 avg_cover=0.000
2026-04-14 18:03:44 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018722901064249117, 'units': 2, 'total_deploy_reward': 0.018722901064249117, 'forward_sum': 0.17627118644067796, 'spread_sum': 1.8333333333333335, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.08813559322033898, 'avg_spread': 0.9166666666666667, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-14 18:03:44 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-14 18:03:44 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-14 18:03:44 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-14 18:03:44 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-14 18:03:44 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 18:03:44 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-14 18:03:44 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:03:46 | === БОЕВОЙ РАУНД 1 ===
2026-04-14 18:03:46 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-14 18:03:46 | --- ХОД PLAYER ---
2026-04-14 18:03:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:03:46 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:03:46 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:03:46 | REQ: move cell accepted (RMB) x=38, y=33, mode=advance
2026-04-14 18:03:46 | [MOVE] unit=11 advance to=(38,33) dist=11 M=5 adv=6
2026-04-14 18:03:47 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:03:47 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-04-14 18:03:47 | [MOVE] unit=12 advance to=(38,23) dist=11 M=5 adv=6
2026-04-14 18:03:48 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:03:48 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:03:48 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:03:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:03:48 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:03:48 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:03:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:03:48 | Нет доступных целей для чарджа.
2026-04-14 18:03:48 | --- ФАЗА БОЯ ---
2026-04-14 18:03:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:48 | --- ХОД MODEL ---
2026-04-14 18:03:48 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:03:48 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:03:48 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:03:51 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-14 18:03:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 4). Выбор reachable_idx=10/366, mode=normal, advance=нет, distance=5
2026-04-14 18:03:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (20, 9)
2026-04-14 18:03:51 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:03:51 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-14 18:03:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 8). Выбор reachable_idx=6/418, mode=normal, advance=нет, distance=5
2026-04-14 18:03:51 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 8)
2026-04-14 18:03:51 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:03:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:03:51 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 23), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 18:03:51 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(38, 23), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 18:03:52 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-14 18:03:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-14 18:03:52 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-14 18:03:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:03:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-14 18:03:52 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:03:53 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-14 18:03:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:03:54 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-14 18:03:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:03:54 | [MODEL] Чардж: нет доступных целей
2026-04-14 18:03:54 | --- ФАЗА БОЯ ---
2026-04-14 18:03:54 | [MODEL] Ближний бой: нет доступных атак
2026-04-14 18:03:54 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-14 18:03:54 | Итерация 0 завершена с наградой tensor([0.0633], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-14 18:03:54 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 18:03:54 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-14 18:03:55 | === БОЕВОЙ РАУНД 2 ===
2026-04-14 18:03:55 | --- ХОД PLAYER ---
2026-04-14 18:03:55 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:03:55 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:03:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:03:56 | REQ: move cell accepted (RMB) x=27, y=29, mode=advance
2026-04-14 18:03:56 | [MOVE] unit=11 advance to=(27,29) dist=11 M=5 adv=6
2026-04-14 18:03:56 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2]
2026-04-14 18:03:56 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:03:56 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:03:56 | 
🎲 Бросок сейвы (save): 1D6
2026-04-14 18:03:56 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-14 18:03:56 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 18:03:56 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-14 18:03:56 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 18:03:56 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:03:56 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:03:56 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-14 18:03:56 | Оружие: Gauss flayer
2026-04-14 18:03:56 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:03:56 | BS оружия: 4+
2026-04-14 18:03:56 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 18:03:56 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:03:56 | Save цели: 4+ (invul: нет)
2026-04-14 18:03:56 | Benefit of Cover: не активен.
2026-04-14 18:03:56 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:03:56 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:03:56 | Правило: Overwatch: попадания только на 6+
2026-04-14 18:03:56 | Hit rolls:    [3, 5, 1, 2, 1, 5, 5, 6, 3, 2]  -> hits: 1 (crits: 1)
2026-04-14 18:03:56 | Save rolls:   [2]  (цель 4+) -> failed saves: 1
2026-04-14 18:03:56 | FX: найден failed saves = 1.
2026-04-14 18:03:56 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 18:03:56 | FX: найден итог урона = 1.0.
2026-04-14 18:03:56 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 18:03:56 | FX: позиция эффекта start=(228.0,492.0) end=(924.0,804.0).
2026-04-14 18:03:56 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-14 18:03:56 | 📌 -------------------------

2026-04-14 18:03:58 | REQ: move cell accepted (RMB) x=28, y=24, mode=advance
2026-04-14 18:03:58 | [MOVE] unit=12 advance to=(28,24) dist=10 M=5 adv=5
2026-04-14 18:03:58 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2]
2026-04-14 18:03:58 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:03:58 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:03:58 | 
🎲 Бросок сейвы (save): 1D6
2026-04-14 18:03:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-14 18:03:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 18:03:58 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-14 18:03:58 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 18:03:58 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:03:58 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:03:58 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 18:03:58 | Оружие: Gauss flayer
2026-04-14 18:03:58 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:03:58 | BS оружия: 4+
2026-04-14 18:03:58 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 18:03:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:03:58 | Save цели: 4+ (invul: нет)
2026-04-14 18:03:58 | Benefit of Cover: не активен.
2026-04-14 18:03:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:03:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:03:58 | Правило: Overwatch: попадания только на 6+
2026-04-14 18:03:58 | Hit rolls:    [5, 5, 4, 3, 5, 5, 2, 2, 6, 4]  -> hits: 1 (crits: 1)
2026-04-14 18:03:58 | Save rolls:   [2]  (цель 4+) -> failed saves: 1
2026-04-14 18:03:58 | FX: найден failed saves = 1.
2026-04-14 18:03:58 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 18:03:58 | FX: найден итог урона = 1.0.
2026-04-14 18:03:58 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 18:03:58 | FX: позиция эффекта start=(228.0,492.0) end=(924.0,564.0).
2026-04-14 18:03:58 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-14 18:03:58 | 📌 -------------------------

2026-04-14 18:03:58 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:03:58 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:03:58 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:03:58 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:03:58 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:03:58 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:03:58 | Нет доступных целей для чарджа.
2026-04-14 18:03:58 | --- ФАЗА БОЯ ---
2026-04-14 18:03:58 | --- ХОД MODEL ---
2026-04-14 18:03:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:03:58 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-14 18:03:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:04:00 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-14 18:04:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (20, 9). Выбор reachable_idx=10/481, mode=normal, advance=нет, distance=5
2026-04-14 18:04:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (15, 13)
2026-04-14 18:04:00 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:04:00 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:04:00 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:04:00 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 18:04:00 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:04:00 | FX: найден failed saves = 1.
2026-04-14 18:04:00 | FX: найден итог урона = 1.0.
2026-04-14 18:04:00 | FX: дубликат отчёта, эффект не создаём.
2026-04-14 18:04:02 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-14 18:04:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 8). Выбор reachable_idx=6/458, mode=normal, advance=нет, distance=5
2026-04-14 18:04:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (20, 8)
2026-04-14 18:04:02 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:04:02 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:04:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:04:03 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:04:03 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(28, 24), target_filter_size=2, max_target_dist=20, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 18:04:03 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(28, 24), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 18:04:04 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 2, 4, 6, 1, 1, 1, 3, 5, 5]
2026-04-14 18:04:04 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-14 18:04:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-14 18:04:04 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-14 18:04:04 | 
🎲 Бросок на ранение (to wound): 11D6
2026-04-14 18:04:04 | 
🎲 Бросок сейвы (save): 10D6
2026-04-14 18:04:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 6. Осталось: 3. HP: 9.0 -> 3.0 (shooting)
2026-04-14 18:04:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 3. Причина: потери моделей.
2026-04-14 18:04:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 6.0
2026-04-14 18:04:04 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 18:04:04 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 18:04:04 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:04:04 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 18:04:04 | Оружие: Gauss flayer
2026-04-14 18:04:04 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:04:04 | BS оружия: 4+
2026-04-14 18:04:04 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:04:04 | Save цели: 4+ (invul: нет)
2026-04-14 18:04:04 | Benefit of Cover: не активен.
2026-04-14 18:04:04 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:04:04 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:04:04 | Hit rolls:    [5, 2, 3, 4, 4, 5, 6, 1, 5, 6, 4, 5, 4, 5, 5, 1, 6, 1, 5, 6]  -> hits: 15 (crits: 4)
2026-04-14 18:04:04 | Wound rolls:  [6, 5, 1, 4, 6, 2, 1, 3, 3, 4, 5]  (цель 4+) -> rolled wounds: 6 + auto(w/LETHAL): 4 = 10
2026-04-14 18:04:04 | Save rolls:   [1, 2, 4, 6, 1, 1, 1, 3, 5, 5]  (цель 4+) -> failed saves: 6
2026-04-14 18:04:04 | FX: найден failed saves = 6.
2026-04-14 18:04:04 | 
✅ Итог по движку: прошло урона = 6.0
2026-04-14 18:04:04 | FX: найден итог урона = 6.0.
2026-04-14 18:04:04 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=6.0, outcome=damage).
2026-04-14 18:04:04 | FX: позиция эффекта start=(324.0,372.0) end=(684.0,588.0).
2026-04-14 18:04:04 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-14 18:04:04 | 📌 -------------------------

2026-04-14 18:04:07 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 1, 3, 3, 6]
2026-04-14 18:04:07 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-14 18:04:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-04-14 18:04:07 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:04:07 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-14 18:04:07 | 
🎲 Бросок сейвы (save): 5D6
2026-04-14 18:04:07 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 0. HP: 3.0 -> 0.0 (shooting)
2026-04-14 18:04:07 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 0. Причина: потери моделей.
2026-04-14 18:04:07 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 4.0
2026-04-14 18:04:07 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 18:04:07 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 18:04:07 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:04:07 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-14 18:04:07 | Оружие: Gauss flayer
2026-04-14 18:04:07 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:04:07 | BS оружия: 4+
2026-04-14 18:04:07 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:04:07 | Save цели: 4+ (invul: нет)
2026-04-14 18:04:07 | Benefit of Cover: не активен.
2026-04-14 18:04:07 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:04:07 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:04:07 | Hit rolls:    [4, 6, 6, 3, 1, 2, 2, 3, 6, 5]  -> hits: 5 (crits: 3)
2026-04-14 18:04:07 | Wound rolls:  [5, 6]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 3 = 5
2026-04-14 18:04:07 | Save rolls:   [2, 1, 3, 3, 6]  (цель 4+) -> failed saves: 4
2026-04-14 18:04:07 | FX: найден failed saves = 4.
2026-04-14 18:04:07 | 
✅ Итог по движку: прошло урона = 4.0
2026-04-14 18:04:07 | FX: найден итог урона = 4.0.
2026-04-14 18:04:07 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=4.0, outcome=damage).
2026-04-14 18:04:07 | FX: позиция эффекта start=(204.0,492.0) end=(684.0,588.0).
2026-04-14 18:04:07 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-14 18:04:07 | 📌 -------------------------

2026-04-14 18:04:07 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:04:08 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-14 18:04:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:04:09 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-14 18:04:09 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:04:09 | [MODEL] Чардж: нет доступных целей
2026-04-14 18:04:09 | --- ФАЗА БОЯ ---
2026-04-14 18:04:09 | [MODEL] Ближний бой: нет доступных атак
2026-04-14 18:04:09 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-14 18:04:09 | Итерация 1 завершена с наградой tensor([1.6893], device='cuda:0'), здоровье игрока [9.0, 0.0], здоровье модели [10.0, 10.0]
2026-04-14 18:04:09 | {'model health': [10.0, 10.0], 'player health': [9.0, 0.0], 'model alive models': [10, 10], 'player alive models': [9, 0], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 18:04:09 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 0.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 6.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 4.0 раз(а)

2026-04-14 18:04:10 | === БОЕВОЙ РАУНД 3 ===
2026-04-14 18:04:10 | --- ХОД PLAYER ---
2026-04-14 18:04:10 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:04:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-14 18:04:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-14 18:04:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-14 18:04:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-14 18:04:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-14 18:04:12 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:04:12 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:04:12 | REQ: move cell accepted (RMB) x=29, y=26, mode=normal
2026-04-14 18:04:12 | [MOVE] unit=11 normal to=(29,26) dist=3 M=5
2026-04-14 18:04:13 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1]
2026-04-14 18:04:13 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:04:13 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:04:13 | 
🎲 Бросок сейвы (save): 1D6
2026-04-14 18:04:13 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-14 18:04:13 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 18:04:13 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-14 18:04:13 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 18:04:13 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:04:13 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:04:13 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-14 18:04:13 | Оружие: Gauss flayer
2026-04-14 18:04:13 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:04:13 | BS оружия: 4+
2026-04-14 18:04:13 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 18:04:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:04:13 | Save цели: 4+ (invul: нет)
2026-04-14 18:04:13 | Benefit of Cover: не активен.
2026-04-14 18:04:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:04:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:04:13 | Правило: Overwatch: попадания только на 6+
2026-04-14 18:04:13 | Hit rolls:    [1, 4, 2, 6, 5, 2, 5, 3, 3, 5]  -> hits: 1 (crits: 1)
2026-04-14 18:04:13 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-04-14 18:04:13 | FX: найден failed saves = 1.
2026-04-14 18:04:13 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 18:04:13 | FX: найден итог урона = 1.0.
2026-04-14 18:04:13 | FX: дубликат отчёта, эффект не создаём.
2026-04-14 18:04:13 | 📌 -------------------------

2026-04-14 18:04:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:04:13 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-14 18:04:13 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(27, 29), target_filter_size=2, max_target_dist=19, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 18:04:13 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(27, 29), full_cells=24, rapid_cells=12, вошло=1715, rapid=575, не вошло=685, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 18:04:13 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(29, 26), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 18:04:13 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(29, 26), full_cells=24, rapid_cells=12, вошло=1862, rapid=625, не вошло=538, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 18:04:13 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:04:15 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-14 18:04:15 | REQ: движок запросил кубы стрельбы (target=22, count=9, stage=hit).
2026-04-14 18:04:21 | 
🎲 Бросок на ранение (to wound): 9D6
2026-04-14 18:04:21 | REQ: движок запросил кубы стрельбы (target=22, count=9, stage=wound).
2026-04-14 18:04:25 | 
🎲 Бросок сейвы (save): 5D6
2026-04-14 18:04:25 | REQ: движок запросил кубы стрельбы (target=22, count=5, stage=save).
2026-04-14 18:04:31 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 2, 3, 4, 5]
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-14 18:04:31 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:04:31 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 18:04:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 18:04:31 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:04:31 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-04-14 18:04:31 | Оружие: Gauss flayer
2026-04-14 18:04:31 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:04:31 | BS оружия: 4+
2026-04-14 18:04:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:04:31 | Save цели: 4+ (invul: нет)
2026-04-14 18:04:31 | Benefit of Cover: не активен.
2026-04-14 18:04:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:04:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:04:31 | Hit rolls:    [4, 4, 4, 4, 4, 4, 4, 4, 4]  -> hits: 9
2026-04-14 18:04:31 | Wound rolls:  [3, 4, 1, 2, 4, 4, 3, 4, 4]  (цель 4+) -> wounds: 5
2026-04-14 18:04:31 | Save rolls:   [1, 2, 3, 4, 5]  (цель 4+) -> failed saves: 3
2026-04-14 18:04:31 | FX: найден failed saves = 3.
2026-04-14 18:04:31 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-14 18:04:31 | FX: найден итог урона = 3.0.
2026-04-14 18:04:31 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-14 18:04:31 | FX: позиция эффекта start=(708.0,636.0) end=(204.0,492.0).
2026-04-14 18:04:31 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-04-14 18:04:31 | 📌 -------------------------

2026-04-14 18:04:31 | Unit 12 — Necrons Necron Warriors (x10 моделей): юнит мертв — стрельба пропущена.
2026-04-14 18:04:31 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:04:31 | Нет доступных целей для чарджа.
2026-04-14 18:04:31 | --- ФАЗА БОЯ ---
2026-04-14 18:04:31 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:04:31 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:04:31 | --- ХОД MODEL ---
2026-04-14 18:04:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-14 18:04:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-14 18:04:31 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:04:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:07:45 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-14 18:07:45 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-14 18:07:45 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-14 18:07:45 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-14 18:07:46 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 18:07:46 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-14 18:07:46 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-14 18:07:46 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-14 18:07:46 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-14 18:07:46 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-14 18:07:46 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-14 18:07:48 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-04-14 18:07:48 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-14 18:07:48 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-14 18:07:48 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-14 18:07:48 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-14 18:07:48 | [DEPLOY] Order: model first, alternating
2026-04-14 18:07:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 18:07:48 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1807, coord=(30,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 18:07:48 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (30,7)
2026-04-14 18:07:48 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 18:07:48 | REQ: deploy cell accepted x=49, y=26
2026-04-14 18:07:48 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-14 18:07:48 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,49)
2026-04-14 18:07:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 18:07:48 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1570, coord=(26,10), attempt=1, reward=-0.004, score_before=0.429, score_after=0.348, reward_delta=-0.004, forward=0.147, spread=0.667, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 18:07:48 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (26,10)
2026-04-14 18:07:49 | REQ: deploy cell accepted x=47, y=21
2026-04-14 18:07:49 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,47)
2026-04-14 18:07:49 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,47)
2026-04-14 18:07:49 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.135 avg_spread=0.833 avg_edge=1.000 avg_cover=0.000
2026-04-14 18:07:49 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01738273551438707, 'units': 2, 'total_deploy_reward': 0.01738273551438707, 'forward_sum': 0.26949152542372884, 'spread_sum': 1.6666666666666665, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.13474576271186442, 'avg_spread': 0.8333333333333333, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-14 18:07:49 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-14 18:07:49 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-14 18:07:49 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-14 18:07:49 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-14 18:07:49 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 18:07:49 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-14 18:07:49 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 18:07:50 | === БОЕВОЙ РАУНД 1 ===
2026-04-14 18:07:50 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-14 18:07:50 | --- ХОД PLAYER ---
2026-04-14 18:07:50 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:07:50 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:07:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:07:50 | REQ: move cell accepted (RMB) x=38, y=26, mode=advance
2026-04-14 18:07:50 | [MOVE] unit=11 advance to=(38,26) dist=11 M=5 adv=6
2026-04-14 18:07:51 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:07:52 | REQ: move cell accepted (RMB) x=37, y=23, mode=advance
2026-04-14 18:07:52 | [MOVE] unit=12 advance to=(37,23) dist=10 M=5 adv=5
2026-04-14 18:07:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:07:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:07:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:07:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:07:52 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:07:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:07:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:07:52 | Нет доступных целей для чарджа.
2026-04-14 18:07:52 | --- ФАЗА БОЯ ---
2026-04-14 18:07:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:07:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:07:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:07:52 | --- ХОД MODEL ---
2026-04-14 18:07:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:07:52 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:07:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:07:53 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-14 18:07:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 7). Выбор reachable_idx=10/397, mode=normal, advance=нет, distance=5
2026-04-14 18:07:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 11)
2026-04-14 18:07:53 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:07:54 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-14 18:07:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (26, 10). Выбор reachable_idx=6/458, mode=normal, advance=нет, distance=5
2026-04-14 18:07:54 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 8)
2026-04-14 18:07:54 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 18:07:54 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:07:54 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 23), target_filter_size=1, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 18:07:54 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(37, 23), full_cells=24, rapid_cells=12, вошло=1880, rapid=625, не вошло=520, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 18:07:55 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 2, 5]
2026-04-14 18:07:55 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-14 18:07:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-04-14 18:07:55 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:07:55 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-14 18:07:55 | 
🎲 Бросок сейвы (save): 3D6
2026-04-14 18:07:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-14 18:07:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 18:07:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-14 18:07:55 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 18:07:55 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 18:07:55 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:07:55 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-14 18:07:55 | Оружие: Gauss flayer
2026-04-14 18:07:55 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:07:55 | BS оружия: 4+
2026-04-14 18:07:55 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:07:55 | Save цели: 4+ (invul: нет)
2026-04-14 18:07:55 | Benefit of Cover: не активен.
2026-04-14 18:07:55 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:07:55 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:07:55 | Hit rolls:    [2, 3, 2, 2, 6, 4, 3, 2, 6, 5]  -> hits: 4 (crits: 2)
2026-04-14 18:07:55 | Wound rolls:  [2, 4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-04-14 18:07:55 | Save rolls:   [4, 2, 5]  (цель 4+) -> failed saves: 1
2026-04-14 18:07:55 | FX: найден failed saves = 1.
2026-04-14 18:07:55 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 18:07:55 | FX: найден итог урона = 1.0.
2026-04-14 18:07:55 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 18:07:55 | FX: позиция эффекта start=(276.0,612.0) end=(924.0,636.0).
2026-04-14 18:07:55 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-14 18:07:55 | 📌 -------------------------

2026-04-14 18:07:57 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-14 18:07:57 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:07:57 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 18:07:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-14 18:07:57 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:07:58 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-14 18:07:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:07:59 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-14 18:07:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 18:07:59 | [MODEL] Чардж: нет доступных целей
2026-04-14 18:07:59 | --- ФАЗА БОЯ ---
2026-04-14 18:07:59 | [MODEL] Ближний бой: нет доступных атак
2026-04-14 18:07:59 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-14 18:07:59 | Итерация 0 завершена с наградой tensor([0.0783], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-14 18:07:59 | {'model health': [10.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [10, 10], 'player alive models': [9, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 18:07:59 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-14 18:07:59 | === БОЕВОЙ РАУНД 2 ===
2026-04-14 18:07:59 | --- ХОД PLAYER ---
2026-04-14 18:07:59 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:07:59 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-14 18:08:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-14 18:08:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-14 18:08:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-14 18:08:01 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-14 18:08:01 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 18:08:01 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 18:08:02 | REQ: move cell accepted (RMB) x=28, y=27, mode=advance
2026-04-14 18:08:02 | [MOVE] unit=11 advance to=(28,27) dist=10 M=5 adv=5
2026-04-14 18:08:02 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 2]
2026-04-14 18:08:03 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:08:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:08:03 | 
🎲 Бросок сейвы (save): 2D6
2026-04-14 18:08:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-04-14 18:08:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-14 18:08:03 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-14 18:08:03 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 18:08:03 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:08:03 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:08:03 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-14 18:08:03 | Оружие: Gauss flayer
2026-04-14 18:08:03 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:08:03 | BS оружия: 4+
2026-04-14 18:08:03 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 18:08:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:08:03 | Save цели: 4+ (invul: нет)
2026-04-14 18:08:03 | Benefit of Cover: не активен.
2026-04-14 18:08:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:08:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:08:03 | Правило: Overwatch: попадания только на 6+
2026-04-14 18:08:03 | Hit rolls:    [6, 6, 4, 4, 3, 5, 1, 3, 2, 2]  -> hits: 2 (crits: 2)
2026-04-14 18:08:03 | Save rolls:   [1, 2]  (цель 4+) -> failed saves: 2
2026-04-14 18:08:03 | FX: найден failed saves = 2.
2026-04-14 18:08:03 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-14 18:08:03 | FX: найден итог урона = 2.0.
2026-04-14 18:08:03 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-14 18:08:03 | FX: позиция эффекта start=(276.0,612.0) end=(924.0,636.0).
2026-04-14 18:08:03 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-14 18:08:03 | 📌 -------------------------

2026-04-14 18:08:05 | REQ: move cell accepted (RMB) x=27, y=22, mode=advance
2026-04-14 18:08:05 | [MOVE] unit=12 advance to=(27,22) dist=10 M=5 adv=5
2026-04-14 18:08:05 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 5, 4, 1]
2026-04-14 18:08:05 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-14 18:08:05 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 18:08:05 | 
🎲 Бросок сейвы (save): 4D6
2026-04-14 18:08:05 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-14 18:08:05 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 18:08:05 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-14 18:08:05 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 18:08:05 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 18:08:05 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 18:08:05 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 18:08:05 | Оружие: Gauss flayer
2026-04-14 18:08:05 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 18:08:05 | BS оружия: 4+
2026-04-14 18:08:05 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 18:08:05 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 18:08:05 | Save цели: 4+ (invul: нет)
2026-04-14 18:08:05 | Benefit of Cover: не активен.
2026-04-14 18:08:05 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 18:08:05 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 18:08:05 | Правило: Overwatch: попадания только на 6+
2026-04-14 18:08:05 | Hit rolls:    [6, 1, 1, 6, 6, 3, 2, 6, 5, 3]  -> hits: 4 (crits: 4)
2026-04-14 18:08:05 | Save rolls:   [5, 5, 4, 1]  (цель 4+) -> failed saves: 1
2026-04-14 18:08:05 | FX: найден failed saves = 1.
2026-04-14 18:08:05 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 18:08:05 | FX: найден итог урона = 1.0.
2026-04-14 18:08:05 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 18:08:05 | FX: позиция эффекта start=(276.0,612.0) end=(900.0,564.0).
2026-04-14 18:08:05 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-14 18:08:05 | 📌 -------------------------

2026-04-14 18:08:05 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 18:08:05 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:08:05 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 18:08:05 | --- ФАЗА ЧАРДЖА ---
2026-04-14 18:08:05 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:08:05 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 18:08:05 | Нет доступных целей для чарджа.
2026-04-14 18:08:05 | --- ФАЗА БОЯ ---
2026-04-14 18:08:05 | --- ХОД MODEL ---
2026-04-14 18:08:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 18:08:05 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-14 18:08:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 19:05:17 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-14 19:05:17 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-14 19:05:17 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-14 19:05:17 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-14 19:05:18 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 19:05:18 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-14 19:05:18 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-14 19:05:18 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-14 19:05:18 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-14 19:05:18 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-14 19:05:18 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-14 19:05:19 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-14 19:05:19 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-14 19:05:19 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-14 19:05:19 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-14 19:05:19 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-14 19:05:19 | [DEPLOY] Order: model first, alternating
2026-04-14 19:05:19 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 19:05:19 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1981, coord=(33,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 19:05:19 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (33,1)
2026-04-14 19:05:19 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-14 19:05:20 | Ошибка деплоя: reason=outside_deploy_zone, x=45, y=24. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-14 19:05:20 | REQ: deploy cell accepted x=48, y=20
2026-04-14 19:05:20 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-04-14 19:05:20 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-04-14 19:05:20 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-14 19:05:20 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1143, coord=(19,3), attempt=1, reward=+0.003, score_before=0.289, score_after=0.343, reward_delta=+0.003, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-14 19:05:20 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (19,3)
2026-04-14 19:05:20 | REQ: deploy cell accepted x=48, y=26
2026-04-14 19:05:21 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-14 19:05:21 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-14 19:05:21 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.029 avg_spread=1.000 avg_edge=0.250 avg_cover=0.000
2026-04-14 19:05:21 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01714623571147024, 'units': 2, 'total_deploy_reward': 0.01714623571147024, 'forward_sum': 0.0576271186440678, 'spread_sum': 2.0, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.0288135593220339, 'avg_spread': 1.0, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-04-14 19:05:21 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-14 19:05:21 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-14 19:05:21 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-14 19:05:21 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-14 19:05:21 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 19:05:21 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-14 19:05:21 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 19:05:22 | === БОЕВОЙ РАУНД 1 ===
2026-04-14 19:05:22 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-14 19:05:22 | --- ХОД PLAYER ---
2026-04-14 19:05:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 19:05:22 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 19:05:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 19:05:23 | REQ: move cell accepted (RMB) x=37, y=21, mode=advance
2026-04-14 19:05:23 | [MOVE] unit=11 advance to=(37,21) dist=11 M=5 adv=6
2026-04-14 19:05:24 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 19:05:24 | REQ: move cell accepted (RMB) x=37, y=23, mode=advance
2026-04-14 19:05:24 | [MOVE] unit=12 advance to=(37,23) dist=11 M=5 adv=6
2026-04-14 19:05:24 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 19:05:24 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 19:05:24 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 19:05:24 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 19:05:24 | --- ФАЗА ЧАРДЖА ---
2026-04-14 19:05:24 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 19:05:24 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 19:05:24 | Нет доступных целей для чарджа.
2026-04-14 19:05:24 | --- ФАЗА БОЯ ---
2026-04-14 19:05:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:24 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:24 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:24 | --- ХОД MODEL ---
2026-04-14 19:05:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 19:05:24 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 19:05:24 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 19:05:25 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-14 19:05:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 1). Выбор reachable_idx=10/233, mode=normal, advance=нет, distance=4
2026-04-14 19:05:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 2)
2026-04-14 19:05:25 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 19:05:26 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-14 19:05:26 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 3). Выбор reachable_idx=6/343, mode=normal, advance=нет, distance=5
2026-04-14 19:05:26 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 5)
2026-04-14 19:05:26 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-14 19:05:26 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 19:05:26 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(36, 24), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 19:05:26 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(36, 24), full_cells=24, rapid_cells=12, вошло=1920, rapid=625, не вошло=480, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 19:05:27 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-14 19:05:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:27 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-14 19:05:27 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-14 19:05:27 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:27 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-14 19:05:27 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-14 19:05:27 | --- ФАЗА ЧАРДЖА ---
2026-04-14 19:05:28 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-14 19:05:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 19:05:29 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-14 19:05:29 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-14 19:05:29 | [MODEL] Чардж: нет доступных целей
2026-04-14 19:05:29 | --- ФАЗА БОЯ ---
2026-04-14 19:05:29 | [MODEL] Ближний бой: нет доступных атак
2026-04-14 19:05:29 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-14 19:05:29 | Итерация 0 завершена с наградой tensor([0.0262], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-14 19:05:29 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-14 19:05:29 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-14 19:05:30 | === БОЕВОЙ РАУНД 2 ===
2026-04-14 19:05:30 | --- ХОД PLAYER ---
2026-04-14 19:05:30 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 19:05:30 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-14 19:05:30 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 19:05:31 | REQ: move cell accepted (RMB) x=26, y=23, mode=advance
2026-04-14 19:05:31 | [MOVE] unit=11 advance to=(26,23) dist=11 M=5 adv=6
2026-04-14 19:05:31 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 4]
2026-04-14 19:05:31 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-14 19:05:31 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 19:05:31 | 
🎲 Бросок сейвы (save): 2D6
2026-04-14 19:05:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-14 19:05:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 19:05:31 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-14 19:05:31 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 19:05:31 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 19:05:31 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-14 19:05:31 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-14 19:05:31 | Оружие: Gauss flayer
2026-04-14 19:05:31 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 19:05:31 | BS оружия: 4+
2026-04-14 19:05:31 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 19:05:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 19:05:31 | Save цели: 4+ (invul: нет)
2026-04-14 19:05:31 | Benefit of Cover: не активен.
2026-04-14 19:05:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 19:05:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 19:05:31 | Правило: Overwatch: попадания только на 6+
2026-04-14 19:05:31 | Hit rolls:    [5, 4, 1, 6, 5, 6, 3, 1, 5, 3]  -> hits: 2 (crits: 2)
2026-04-14 19:05:31 | Save rolls:   [1, 4]  (цель 4+) -> failed saves: 1
2026-04-14 19:05:31 | FX: найден failed saves = 1.
2026-04-14 19:05:31 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 19:05:31 | FX: найден итог урона = 1.0.
2026-04-14 19:05:31 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 19:05:31 | FX: позиция эффекта start=(60.0,708.0) end=(900.0,516.0).
2026-04-14 19:05:31 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-14 19:05:31 | 📌 -------------------------

2026-04-14 19:05:33 | REQ: move cell accepted (RMB) x=26, y=18, mode=advance
2026-04-14 19:05:33 | [MOVE] unit=12 advance to=(26,18) dist=10 M=5 adv=5
2026-04-14 19:05:33 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 6, 5]
2026-04-14 19:05:33 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-14 19:05:33 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 19:05:33 | 
🎲 Бросок сейвы (save): 3D6
2026-04-14 19:05:33 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-14 19:05:33 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-14 19:05:33 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 19:05:33 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 19:05:33 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 19:05:33 | Оружие: Gauss flayer
2026-04-14 19:05:33 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 19:05:33 | BS оружия: 4+
2026-04-14 19:05:33 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-14 19:05:33 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 19:05:33 | Save цели: 4+ (invul: нет)
2026-04-14 19:05:33 | Benefit of Cover: не активен.
2026-04-14 19:05:33 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 19:05:33 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 19:05:33 | Правило: Overwatch: попадания только на 6+
2026-04-14 19:05:33 | Hit rolls:    [6, 5, 1, 2, 3, 6, 5, 1, 5, 6]  -> hits: 3 (crits: 3)
2026-04-14 19:05:33 | Save rolls:   [5, 6, 5]  (цель 4+) -> failed saves: 0
2026-04-14 19:05:33 | FX: найден failed saves = 0.
2026-04-14 19:05:33 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-14 19:05:33 | FX: найден итог урона = 0.0.
2026-04-14 19:05:33 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-14 19:05:33 | FX: позиция эффекта start=(60.0,708.0) end=(876.0,588.0).
2026-04-14 19:05:33 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-14 19:05:33 | 📌 -------------------------

2026-04-14 19:05:33 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 19:05:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 19:05:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-14 19:05:33 | --- ФАЗА ЧАРДЖА ---
2026-04-14 19:05:33 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 19:05:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-14 19:05:33 | Нет доступных целей для чарджа.
2026-04-14 19:05:33 | --- ФАЗА БОЯ ---
2026-04-14 19:05:33 | --- ХОД MODEL ---
2026-04-14 19:05:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-14 19:05:33 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-14 19:05:33 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-14 19:05:35 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-14 19:05:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 2). Выбор reachable_idx=10/307, mode=normal, advance=нет, distance=4
2026-04-14 19:05:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 1)
2026-04-14 19:05:35 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-14 19:05:35 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 19:05:35 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-14 19:05:35 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 19:05:35 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 19:05:35 | FX: найден failed saves = 0.
2026-04-14 19:05:35 | FX: найден итог урона = 0.0.
2026-04-14 19:05:35 | FX: дубликат отчёта, эффект не создаём.
2026-04-14 19:05:37 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 19:05:38 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-14 19:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 5). Выбор reachable_idx=6/389, mode=normal, advance=нет, distance=5
2026-04-14 19:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (9, 5)
2026-04-14 19:05:38 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-14 19:05:39 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-14 19:05:39 | FX: перепроигрываю 30 строк(и) лога.
2026-04-14 19:05:39 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(26, 18), target_filter_size=2, max_target_dist=25, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-14 19:05:39 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(26, 18), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-14 19:05:40 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 6, 6, 1]
2026-04-14 19:05:40 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-14 19:05:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-14 19:05:40 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 19:05:40 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-14 19:05:40 | 
🎲 Бросок сейвы (save): 4D6
2026-04-14 19:05:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-14 19:05:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-14 19:05:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-14 19:05:40 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 19:05:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 19:05:40 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 19:05:40 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-14 19:05:40 | Оружие: Gauss flayer
2026-04-14 19:05:40 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 19:05:40 | BS оружия: 4+
2026-04-14 19:05:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 19:05:40 | Save цели: 4+ (invul: нет)
2026-04-14 19:05:40 | Benefit of Cover: не активен.
2026-04-14 19:05:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 19:05:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 19:05:40 | Hit rolls:    [6, 1, 1, 6, 5, 5, 6, 2, 1, 3]  -> hits: 5 (crits: 3)
2026-04-14 19:05:40 | Wound rolls:  [5, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-04-14 19:05:40 | Save rolls:   [6, 6, 6, 1]  (цель 4+) -> failed saves: 1
2026-04-14 19:05:40 | FX: найден failed saves = 1.
2026-04-14 19:05:40 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 19:05:40 | FX: найден итог урона = 1.0.
2026-04-14 19:05:40 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 19:05:40 | FX: позиция эффекта start=(36.0,612.0) end=(636.0,444.0).
2026-04-14 19:05:40 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-14 19:05:40 | 📌 -------------------------

2026-04-14 19:05:44 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 6, 4]
2026-04-14 19:05:44 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-14 19:05:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-14 19:05:44 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-14 19:05:44 | 
🎲 Бросок на ранение (to wound): 4D6
2026-04-14 19:05:44 | 
🎲 Бросок сейвы (save): 3D6
2026-04-14 19:05:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (shooting)
2026-04-14 19:05:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-14 19:05:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-14 19:05:44 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-14 19:05:44 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-14 19:05:44 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-14 19:05:44 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-14 19:05:44 | Оружие: Gauss flayer
2026-04-14 19:05:44 | FX: найдена строка оружия: Gauss flayer.
2026-04-14 19:05:44 | BS оружия: 4+
2026-04-14 19:05:44 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-14 19:05:44 | Save цели: 4+ (invul: нет)
2026-04-14 19:05:44 | Benefit of Cover: не активен.
2026-04-14 19:05:44 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-14 19:05:44 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-14 19:05:44 | Hit rolls:    [5, 5, 2, 3, 5, 1, 4, 3, 3, 2]  -> hits: 4
2026-04-14 19:05:44 | Wound rolls:  [3, 4, 5, 6]  (цель 4+) -> wounds: 3
2026-04-14 19:05:44 | Save rolls:   [3, 6, 4]  (цель 4+) -> failed saves: 1
2026-04-14 19:05:44 | FX: найден failed saves = 1.
2026-04-14 19:05:44 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-14 19:05:44 | FX: найден итог урона = 1.0.
2026-04-14 19:05:44 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-14 19:05:44 | FX: позиция эффекта start=(132.0,228.0) end=(636.0,444.0).
2026-04-14 19:05:44 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-14 19:05:44 | 📌 -------------------------

2026-04-14 19:05:44 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:48:09 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 21:48:09 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 21:48:09 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 21:48:09 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 21:48:10 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:48:10 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 21:48:10 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 21:48:10 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 21:48:10 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 21:48:10 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 21:48:10 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 21:48:11 | Roll-off Attacker/Defender: enemy=2 model=1 -> attacker=enemy
2026-04-17 21:48:11 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 21:48:11 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 21:48:11 | [DEPLOY][Only War] attacker=enemy -> LEFT x=0..14; defender=model -> RIGHT x=45..59
2026-04-17 21:48:11 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 21:48:11 | [DEPLOY] Order: enemy first, alternating
2026-04-17 21:48:11 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:48:12 | Ошибка деплоя: reason=outside_deploy_zone, x=55, y=27. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 21:48:12 | Ошибка деплоя: reason=outside_deploy_zone, x=51, y=27. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 21:48:13 | REQ: deploy cell accepted x=9, y=26
2026-04-17 21:48:13 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,9)
2026-04-17 21:48:13 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,9)
2026-04-17 21:48:13 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:48:13 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=169, coord=(2,49), attempt=1, reward=+0.020, score_before=0.000, score_after=0.403, reward_delta=+0.020, forward=0.166, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:48:13 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (2,49)
2026-04-17 21:48:14 | REQ: deploy cell accepted x=10, y=18
2026-04-17 21:48:14 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,10)
2026-04-17 21:48:14 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,10)
2026-04-17 21:48:14 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:48:14 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1671, coord=(27,51), attempt=1, reward=+0.001, score_before=0.403, score_after=0.418, reward_delta=+0.001, forward=0.149, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:48:14 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,51)
2026-04-17 21:48:14 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.158 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-17 21:48:14 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.0209105242412298, 'units': 2, 'total_deploy_reward': 0.0209105242412298, 'forward_sum': 0.3152542372881355, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.15762711864406775, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-17 21:48:14 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 21:48:14 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 21:48:14 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 21:48:14 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 21:48:14 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:48:14 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 21:48:14 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:48:15 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 21:48:15 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 21:48:15 | --- ХОД PLAYER ---
2026-04-17 21:48:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:48:15 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:48:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:48:16 | REQ: move cell accepted (RMB) x=20, y=26, mode=advance
2026-04-17 21:48:16 | [MOVE] unit=11 advance to=(20,26) dist=11 M=5 adv=6
2026-04-17 21:48:17 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:48:18 | REQ: move cell accepted (RMB) x=21, y=17, mode=advance
2026-04-17 21:48:18 | [MOVE] unit=12 advance to=(21,17) dist=11 M=5 adv=6
2026-04-17 21:48:19 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:48:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:48:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:48:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:48:19 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:48:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:48:19 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:48:19 | Нет доступных целей для чарджа.
2026-04-17 21:48:19 | --- ФАЗА БОЯ ---
2026-04-17 21:48:19 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:48:19 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:48:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:48:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:48:19 | --- ХОД MODEL ---
2026-04-17 21:48:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:48:19 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:48:19 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:50:57 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 21:50:57 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 21:50:57 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 21:50:57 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 21:50:58 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:50:58 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 21:50:58 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 21:50:58 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 21:50:58 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 21:50:58 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 21:50:58 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 21:51:01 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-04-17 21:51:01 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 21:51:01 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 21:51:01 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 21:51:01 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 21:51:01 | [DEPLOY] Order: model first, alternating
2026-04-17 21:51:01 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:51:01 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2112, coord=(35,12), attempt=1, reward=+0.023, score_before=0.000, score_after=0.468, reward_delta=+0.023, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:51:01 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,12)
2026-04-17 21:51:01 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:51:01 | REQ: deploy cell accepted x=48, y=26
2026-04-17 21:51:01 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-17 21:51:01 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,48)
2026-04-17 21:51:01 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:51:01 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=130, coord=(2,10), attempt=1, reward=-0.002, score_before=0.468, score_after=0.437, reward_delta=-0.002, forward=0.190, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:51:01 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (2,10)
2026-04-17 21:51:01 | REQ: deploy cell accepted x=50, y=20
2026-04-17 21:51:02 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,50)
2026-04-17 21:51:02 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,50)
2026-04-17 21:51:02 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.198 avg_spread=1.000 avg_edge=0.875 avg_cover=0.000
2026-04-17 21:51:02 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021856523452897125, 'units': 2, 'total_deploy_reward': 0.021856523452897125, 'forward_sum': 0.3966101694915254, 'spread_sum': 2.0, 'edge_sum': 1.75, 'cover_sum': 0.0, 'avg_forward': 0.1983050847457627, 'avg_spread': 1.0, 'avg_edge': 0.875, 'avg_cover': 0.0}
2026-04-17 21:51:02 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 21:51:02 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 21:51:02 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 21:51:02 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 21:51:02 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:51:02 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 21:51:02 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:51:03 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 21:51:03 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 21:51:03 | --- ХОД PLAYER ---
2026-04-17 21:51:03 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:51:03 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:51:03 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:51:09 | REQ: move cell accepted (RMB) x=37, y=30, mode=advance
2026-04-17 21:51:09 | [MOVE] unit=11 advance to=(37,30) dist=11 M=5 adv=6
2026-04-17 21:51:09 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-17 21:51:09 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=benefit of cover cover_active=1 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-17 21:51:09 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:51:09 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-17 21:51:09 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:51:09 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-17 21:51:09 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:51:09 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:51:09 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:51:09 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 21:51:09 | Оружие: Gauss flayer
2026-04-17 21:51:09 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:51:09 | BS оружия: 4+
2026-04-17 21:51:09 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:51:09 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:51:09 | Save цели: 4+ (invul: нет)
2026-04-17 21:51:09 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-04-17 21:51:09 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:51:09 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:51:09 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:51:09 | Эффект: benefit of cover
2026-04-17 21:51:09 | Hit rolls:    [3, 3, 1, 5, 1, 4, 2, 1, 2, 2]  -> hits: 0
2026-04-17 21:51:09 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 21:51:09 | FX: найден итог урона = 0.0.
2026-04-17 21:51:09 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-17 21:51:09 | FX: позиция эффекта start=(300.0,852.0) end=(1164.0,636.0).
2026-04-17 21:51:09 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 21:51:09 | 📌 -------------------------

2026-04-17 21:51:11 | REQ: move cell accepted (RMB) x=39, y=24, mode=advance
2026-04-17 21:51:11 | [MOVE] unit=12 advance to=(39,24) dist=11 M=5 adv=6
2026-04-17 21:51:11 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:51:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:51:11 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:51:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:51:11 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:51:11 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:51:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:51:11 | Нет доступных целей для чарджа.
2026-04-17 21:51:11 | --- ФАЗА БОЯ ---
2026-04-17 21:51:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:51:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:51:11 | --- ХОД MODEL ---
2026-04-17 21:51:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:51:11 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:51:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:51:12 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-17 21:51:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 12). Выбор reachable_idx=10/367, mode=normal, advance=нет, distance=5
2026-04-17 21:51:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 16)
2026-04-17 21:51:12 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:51:12 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:51:14 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:51:15 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-17 21:51:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 10). Выбор reachable_idx=6/307, mode=normal, advance=нет, distance=2
2026-04-17 21:51:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 10)
2026-04-17 21:51:15 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:51:15 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:51:17 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-17 21:51:17 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=benefit of cover cover_active=1 save_base=4 ap=0 inv=0 save_target=3 save_rolls=[4, 4, 6, 6]
2026-04-17 21:51:17 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-17 21:51:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 21:51:17 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-04-17 21:51:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:51:17 | 
🎲 Бросок на ранение (to wound): 5D6
2026-04-17 21:51:17 | 
🎲 Бросок сейвы (save): 4D6
2026-04-17 21:51:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-04-17 21:51:17 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:51:17 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:51:17 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:51:17 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 21:51:17 | Оружие: Gauss flayer
2026-04-17 21:51:17 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:51:17 | BS оружия: 4+
2026-04-17 21:51:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:51:17 | Save цели: 4+ (invul: нет)
2026-04-17 21:51:17 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-04-17 21:51:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:51:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:51:17 | Эффект: benefit of cover
2026-04-17 21:51:17 | Hit rolls:    [2, 5, 4, 4, 5, 3, 2, 6, 5, 1]  -> hits: 6 (crits: 1)
2026-04-17 21:51:17 | Wound rolls:  [3, 4, 1, 4, 5]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-04-17 21:51:17 | Save rolls:   [4, 4, 6, 6]  (цель 3+) -> failed saves: 0
2026-04-17 21:51:17 | FX: найден failed saves = 0.
2026-04-17 21:51:17 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 21:51:17 | FX: найден итог урона = 0.0.
2026-04-17 21:51:17 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-17 21:51:17 | FX: позиция эффекта start=(396.0,732.0) end=(900.0,732.0).
2026-04-17 21:51:17 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 21:51:17 | 📌 -------------------------

2026-04-17 21:51:19 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-17 21:51:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:51:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:51:19 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 21:51:19 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:51:21 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-17 21:51:21 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:51:22 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-17 21:51:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:51:22 | [MODEL] Чардж: нет доступных целей
2026-04-17 21:51:22 | --- ФАЗА БОЯ ---
2026-04-17 21:51:22 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 21:51:22 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 21:51:22 | Итерация 0 завершена с наградой tensor([0.1149], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-17 21:51:22 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:51:22 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-04-17 21:51:23 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 21:51:23 | --- ХОД PLAYER ---
2026-04-17 21:51:23 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:51:23 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:51:23 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:51:24 | REQ: move cell accepted (RMB) x=26, y=29, mode=advance
2026-04-17 21:51:24 | [MOVE] unit=11 advance to=(26,29) dist=11 M=5 adv=6
2026-04-17 21:51:24 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-17 21:51:24 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:51:24 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 21:51:24 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-17 21:51:24 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:51:24 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:51:24 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:51:24 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 21:51:24 | Оружие: Gauss flayer
2026-04-17 21:51:24 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:51:24 | BS оружия: 4+
2026-04-17 21:51:24 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:51:24 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:51:24 | Save цели: 4+ (invul: нет)
2026-04-17 21:51:24 | Benefit of Cover: не активен.
2026-04-17 21:51:24 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:51:24 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:51:24 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:51:24 | Hit rolls:    [4, 5, 5, 1, 5, 1, 4, 4, 1, 3, 2, 1, 4, 3, 4, 1, 5, 1, 2, 2]  -> hits: 0
2026-04-17 21:51:24 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 21:51:24 | FX: найден итог урона = 0.0.
2026-04-17 21:51:24 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 21:51:24 | 📌 -------------------------

2026-04-17 21:51:26 | REQ: move cell accepted (RMB) x=34, y=24, mode=normal
2026-04-17 21:51:26 | [MOVE] unit=12 normal to=(34,24) dist=5 M=5
2026-04-17 21:51:26 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1]
2026-04-17 21:51:26 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:51:26 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:51:26 | 
🎲 Бросок сейвы (save): 1D6
2026-04-17 21:51:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 21:51:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 21:51:26 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 21:51:26 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:51:26 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:51:26 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:51:26 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:51:26 | Оружие: Gauss flayer
2026-04-17 21:51:26 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:51:26 | BS оружия: 4+
2026-04-17 21:51:26 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:51:26 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:51:26 | Save цели: 4+ (invul: нет)
2026-04-17 21:51:26 | Benefit of Cover: не активен.
2026-04-17 21:51:26 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:51:26 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:51:26 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:51:26 | Hit rolls:    [5, 4, 2, 4, 2, 3, 2, 5, 6, 3]  -> hits: 1 (crits: 1)
2026-04-17 21:51:26 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-04-17 21:51:26 | FX: найден failed saves = 1.
2026-04-17 21:51:26 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:51:26 | FX: найден итог урона = 1.0.
2026-04-17 21:51:26 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:51:26 | FX: позиция эффекта start=(396.0,732.0) end=(948.0,588.0).
2026-04-17 21:51:26 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 21:51:26 | 📌 -------------------------

2026-04-17 21:51:26 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:51:26 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:51:26 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 21:51:26 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(39, 24), target_filter_size=2, max_target_dist=30, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:51:26 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(39, 24), full_cells=24, rapid_cells=12, вошло=1800, rapid=625, не вошло=600, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:51:26 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(34, 24), target_filter_size=2, max_target_dist=25, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:51:26 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(34, 24), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:51:33 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-17 21:51:33 | REQ: движок запросил кубы стрельбы (target=21, count=9, stage=hit).
2026-04-17 21:54:01 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 21:54:01 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 21:54:01 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 21:54:01 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 21:54:02 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:54:02 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 21:54:02 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 21:54:02 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 21:54:02 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 21:54:02 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 21:54:02 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 21:54:03 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-04-17 21:54:03 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 21:54:03 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 21:54:03 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 21:54:03 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 21:54:03 | [DEPLOY] Order: model first, alternating
2026-04-17 21:54:03 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:54:03 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=542, coord=(9,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:54:04 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (9,2)
2026-04-17 21:54:04 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:54:04 | REQ: deploy cell accepted x=49, y=24
2026-04-17 21:54:04 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,49)
2026-04-17 21:54:04 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,49)
2026-04-17 21:54:04 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:54:04 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1811, coord=(30,11), attempt=1, reward=+0.003, score_before=0.343, score_after=0.402, reward_delta=+0.003, forward=0.114, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:54:04 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (30,11)
2026-04-17 21:54:04 | REQ: deploy cell accepted x=49, y=17
2026-04-17 21:54:04 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,49)
2026-04-17 21:54:04 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,49)
2026-04-17 21:54:04 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.075 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-17 21:54:04 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02008277493102089, 'units': 2, 'total_deploy_reward': 0.02008277493102089, 'forward_sum': 0.15084745762711863, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.07542372881355931, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-17 21:54:04 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 21:54:04 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 21:54:04 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 21:54:04 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 21:54:04 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:54:04 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 21:54:04 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:54:06 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 21:54:06 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 21:54:06 | --- ХОД PLAYER ---
2026-04-17 21:54:06 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:54:06 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:54:06 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:54:06 | REQ: move cell accepted (RMB) x=38, y=27, mode=advance
2026-04-17 21:54:06 | [MOVE] unit=11 advance to=(38,27) dist=11 M=5 adv=6
2026-04-17 21:54:07 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:54:07 | REQ: move cell accepted (RMB) x=38, y=18, mode=advance
2026-04-17 21:54:07 | [MOVE] unit=12 advance to=(38,18) dist=11 M=5 adv=6
2026-04-17 21:54:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:54:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:54:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:54:08 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:54:08 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:54:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:54:08 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:54:08 | Нет доступных целей для чарджа.
2026-04-17 21:54:08 | --- ФАЗА БОЯ ---
2026-04-17 21:54:08 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:08 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:08 | --- ХОД MODEL ---
2026-04-17 21:54:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:54:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:54:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:54:09 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-17 21:54:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 2). Выбор reachable_idx=10/293, mode=normal, advance=нет, distance=4
2026-04-17 21:54:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 1)
2026-04-17 21:54:09 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:54:10 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-17 21:54:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 11). Выбор reachable_idx=6/482, mode=normal, advance=нет, distance=5
2026-04-17 21:54:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 11)
2026-04-17 21:54:10 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:54:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:54:13 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-17 21:54:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:13 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 21:54:14 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 3]
2026-04-17 21:54:14 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-17 21:54:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-17 21:54:14 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:54:14 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-17 21:54:14 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 21:54:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-17 21:54:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 21:54:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-17 21:54:14 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:54:14 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:54:14 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:54:14 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 21:54:14 | Оружие: Gauss flayer
2026-04-17 21:54:14 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:54:14 | BS оружия: 4+
2026-04-17 21:54:14 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:54:14 | Save цели: 4+ (invul: нет)
2026-04-17 21:54:14 | Benefit of Cover: не активен.
2026-04-17 21:54:14 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:54:14 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:54:14 | Hit rolls:    [6, 4, 1, 1, 3, 5, 3, 6, 2, 2]  -> hits: 4 (crits: 2)
2026-04-17 21:54:14 | Wound rolls:  [1, 1]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-04-17 21:54:14 | Save rolls:   [5, 3]  (цель 4+) -> failed saves: 1
2026-04-17 21:54:14 | FX: найден failed saves = 1.
2026-04-17 21:54:14 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:54:14 | FX: найден итог урона = 1.0.
2026-04-17 21:54:14 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:54:14 | FX: позиция эффекта start=(276.0,612.0) end=(924.0,444.0).
2026-04-17 21:54:14 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 21:54:14 | 📌 -------------------------

2026-04-17 21:54:14 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:54:16 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-17 21:54:16 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:54:17 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-17 21:54:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:54:17 | [MODEL] Чардж: нет доступных целей
2026-04-17 21:54:17 | --- ФАЗА БОЯ ---
2026-04-17 21:54:17 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 21:54:17 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 21:54:17 | Итерация 0 завершена с наградой tensor([0.1068], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-04-17 21:54:17 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:54:17 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-17 21:54:18 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 21:54:18 | --- ХОД PLAYER ---
2026-04-17 21:54:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:54:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 21:54:19 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 21:54:19 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 21:54:19 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 21:54:19 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 21:54:19 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:54:19 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:54:20 | REQ: move cell accepted (RMB) x=27, y=27, mode=advance
2026-04-17 21:54:20 | [MOVE] unit=11 advance to=(27,27) dist=11 M=5 adv=6
2026-04-17 21:54:20 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 2, 1]
2026-04-17 21:54:21 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:54:21 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:54:21 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 21:54:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (Overwatch)
2026-04-17 21:54:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-17 21:54:21 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 3.0.
2026-04-17 21:54:21 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:54:21 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:54:21 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:54:21 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-04-17 21:54:21 | Оружие: Gauss flayer
2026-04-17 21:54:21 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:54:21 | BS оружия: 4+
2026-04-17 21:54:21 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:54:21 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:54:21 | Save цели: 4+ (invul: нет)
2026-04-17 21:54:21 | Benefit of Cover: не активен.
2026-04-17 21:54:21 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:54:21 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:54:21 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:54:21 | Hit rolls:    [2, 5, 2, 5, 6, 6, 4, 5, 6, 1]  -> hits: 3 (crits: 3)
2026-04-17 21:54:21 | Save rolls:   [3, 2, 1]  (цель 4+) -> failed saves: 3
2026-04-17 21:54:21 | FX: найден failed saves = 3.
2026-04-17 21:54:21 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-17 21:54:21 | FX: найден итог урона = 3.0.
2026-04-17 21:54:21 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-17 21:54:21 | FX: позиция эффекта start=(276.0,612.0) end=(924.0,660.0).
2026-04-17 21:54:21 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-04-17 21:54:21 | 📌 -------------------------

2026-04-17 21:54:21 | REQ: move cell accepted (RMB) x=33, y=19, mode=normal
2026-04-17 21:54:21 | [MOVE] unit=12 normal to=(33,19) dist=5 M=5
2026-04-17 21:54:21 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 3, 1]
2026-04-17 21:54:21 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:54:21 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:54:21 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 21:54:21 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-04-17 21:54:21 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 21:54:21 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-17 21:54:21 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:54:21 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:54:21 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:54:21 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 21:54:21 | Оружие: Gauss flayer
2026-04-17 21:54:21 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:54:21 | BS оружия: 4+
2026-04-17 21:54:21 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:54:21 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:54:21 | Save цели: 4+ (invul: нет)
2026-04-17 21:54:21 | Benefit of Cover: не активен.
2026-04-17 21:54:21 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:54:21 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:54:21 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:54:21 | Hit rolls:    [6, 6, 3, 2, 2, 2, 6, 4, 1, 1]  -> hits: 3 (crits: 3)
2026-04-17 21:54:21 | Save rolls:   [5, 3, 1]  (цель 4+) -> failed saves: 2
2026-04-17 21:54:21 | FX: найден failed saves = 2.
2026-04-17 21:54:21 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 21:54:21 | FX: найден итог урона = 2.0.
2026-04-17 21:54:21 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 21:54:21 | FX: позиция эффекта start=(276.0,612.0) end=(924.0,444.0).
2026-04-17 21:54:21 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 21:54:21 | 📌 -------------------------

2026-04-17 21:54:21 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:54:21 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:54:21 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:21 | REQ: валидные цели стрельбы для Unit 12: [22] | отфильтрованы: [21: цель вне дальности: range 29.00 > 24.00 (out_of_range by +5.00)]
2026-04-17 21:54:21 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(38, 18), target_filter_size=1, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:54:21 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(38, 18), full_cells=24, rapid_cells=12, вошло=1840, rapid=625, не вошло=560, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:54:21 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 19), target_filter_size=1, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:54:21 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 19), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:54:23 | 
🎲 Бросок на попадание (to hit): 8D6
2026-04-17 21:54:23 | REQ: движок запросил кубы стрельбы (target=22, count=8, stage=hit).
2026-04-17 21:54:32 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-04-17 21:54:32 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 8D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-04-17 21:54:32 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-04-17 21:54:32 | REQ: валидные цели стрельбы для Unit 12: [22] | отфильтрованы: [21: цель вне дальности: range 29.00 > 24.00 (out_of_range by +5.00)]
2026-04-17 21:54:36 | 
🎲 Бросок на попадание (to hit): 8D6
2026-04-17 21:54:36 | REQ: движок запросил кубы стрельбы (target=22, count=8, stage=hit).
2026-04-17 21:54:43 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-17 21:54:43 | REQ: движок запросил кубы стрельбы (target=22, count=3, stage=wound).
2026-04-17 21:54:44 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 21:54:44 | REQ: движок запросил кубы стрельбы (target=22, count=2, stage=save).
2026-04-17 21:54:46 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 4]
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 21:54:47 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:54:47 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:54:47 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:54:47 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:54:47 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-04-17 21:54:47 | Оружие: Gauss flayer
2026-04-17 21:54:47 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:54:47 | BS оружия: 4+
2026-04-17 21:54:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:54:47 | Save цели: 4+ (invul: нет)
2026-04-17 21:54:47 | Benefit of Cover: не активен.
2026-04-17 21:54:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:54:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:54:47 | Hit rolls:    [4, 6, 2, 3, 2, 4, 4, 1]  -> hits: 4 (crits: 1)
2026-04-17 21:54:47 | Wound rolls:  [3, 4, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-04-17 21:54:47 | Save rolls:   [1, 4]  (цель 4+) -> failed saves: 1
2026-04-17 21:54:47 | FX: найден failed saves = 1.
2026-04-17 21:54:47 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:54:47 | FX: найден итог урона = 1.0.
2026-04-17 21:54:47 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:54:47 | FX: позиция эффекта start=(804.0,468.0) end=(276.0,612.0).
2026-04-17 21:54:47 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-04-17 21:54:47 | 📌 -------------------------

2026-04-17 21:54:47 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:54:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:54:47 | Нет доступных целей для чарджа.
2026-04-17 21:54:47 | --- ФАЗА БОЯ ---
2026-04-17 21:54:47 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:54:47 | --- ХОД MODEL ---
2026-04-17 21:54:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 21:54:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 21:54:47 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 21:54:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:55:12 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-17 21:55:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (5, 1). Выбор reachable_idx=10/220, mode=normal, advance=нет, distance=4
2026-04-17 21:55:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 2)
2026-04-17 21:55:12 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:55:16 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-17 21:55:16 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 11). Выбор reachable_idx=6/528, mode=normal, advance=нет, distance=5
2026-04-17 21:55:16 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (20, 11)
2026-04-17 21:55:16 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:55:16 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:55:18 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:55:18 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:04 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 21:58:04 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 21:58:04 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 21:58:04 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 21:58:04 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:05 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:58:05 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 21:58:05 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 21:58:05 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 21:58:05 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 21:58:05 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 21:58:05 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 21:58:07 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-17 21:58:07 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 21:58:07 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 21:58:07 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 21:58:07 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 21:58:07 | [DEPLOY] Order: model first, alternating
2026-04-17 21:58:07 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:58:07 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1927, coord=(32,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:58:07 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,7)
2026-04-17 21:58:07 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 21:58:08 | REQ: deploy cell accepted x=51, y=26
2026-04-17 21:58:08 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,51)
2026-04-17 21:58:08 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,51)
2026-04-17 21:58:08 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 21:58:08 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=845, coord=(14,5), attempt=1, reward=-0.000, score_before=0.429, score_after=0.421, reward_delta=-0.000, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 21:58:08 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (14,5)
2026-04-17 21:58:08 | REQ: deploy cell accepted x=50, y=20
2026-04-17 21:58:08 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,50)
2026-04-17 21:58:08 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,50)
2026-04-17 21:58:08 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.114 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 21:58:08 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021048482459597954, 'units': 2, 'total_deploy_reward': 0.021048482459597954, 'forward_sum': 0.22711864406779664, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.11355932203389832, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 21:58:08 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 21:58:08 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 21:58:08 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 21:58:08 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 21:58:08 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:58:08 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 21:58:08 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(50, 20), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:58:08 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:09 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 21:58:09 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 21:58:09 | --- ХОД PLAYER ---
2026-04-17 21:58:09 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:58:09 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:58:09 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:58:10 | REQ: move cell accepted (RMB) x=40, y=28, mode=advance
2026-04-17 21:58:10 | [MOVE] unit=11 advance to=(40,28) dist=11 M=5 adv=6
2026-04-17 21:58:10 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:58:11 | REQ: move cell accepted (RMB) x=39, y=20, mode=advance
2026-04-17 21:58:11 | [MOVE] unit=12 advance to=(39,20) dist=11 M=5 adv=6
2026-04-17 21:58:11 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:58:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:58:11 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:58:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:58:11 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:58:11 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:58:11 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:58:11 | Нет доступных целей для чарджа.
2026-04-17 21:58:11 | --- ФАЗА БОЯ ---
2026-04-17 21:58:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:11 | --- ХОД MODEL ---
2026-04-17 21:58:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:58:11 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:58:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:58:12 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-17 21:58:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 7). Выбор reachable_idx=10/360, mode=normal, advance=нет, distance=5
2026-04-17 21:58:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (27, 11)
2026-04-17 21:58:12 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:58:13 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-17 21:58:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 5). Выбор reachable_idx=6/390, mode=normal, advance=нет, distance=5
2026-04-17 21:58:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (9, 5)
2026-04-17 21:58:13 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 21:58:13 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:58:14 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-17 21:58:14 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:14 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 21:58:15 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-17 21:58:15 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:15 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 21:58:15 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 21:58:15 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:58:15 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-17 21:58:15 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:58:16 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-17 21:58:16 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:58:16 | [MODEL] Чардж: нет доступных целей
2026-04-17 21:58:16 | --- ФАЗА БОЯ ---
2026-04-17 21:58:16 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 21:58:16 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 21:58:16 | Итерация 0 завершена с наградой tensor([0.1092], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-17 21:58:16 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 21:58:16 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-17 21:58:17 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 21:58:17 | --- ХОД PLAYER ---
2026-04-17 21:58:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:58:17 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 21:58:17 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:58:18 | REQ: move cell accepted (RMB) x=29, y=27, mode=advance
2026-04-17 21:58:18 | [MOVE] unit=11 advance to=(29,27) dist=11 M=5 adv=6
2026-04-17 21:58:18 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 3]
2026-04-17 21:58:19 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:19 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:58:19 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 21:58:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 21:58:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 21:58:19 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 21:58:19 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:58:19 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:19 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:19 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 21:58:19 | Оружие: Gauss flayer
2026-04-17 21:58:19 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:19 | BS оружия: 4+
2026-04-17 21:58:19 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:58:19 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:19 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:19 | Benefit of Cover: не активен.
2026-04-17 21:58:19 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:19 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:19 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:58:19 | Hit rolls:    [5, 3, 2, 2, 6, 6, 1, 4, 4, 4]  -> hits: 2 (crits: 2)
2026-04-17 21:58:19 | Save rolls:   [4, 3]  (цель 4+) -> failed saves: 1
2026-04-17 21:58:19 | FX: найден failed saves = 1.
2026-04-17 21:58:19 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:58:19 | FX: найден итог урона = 1.0.
2026-04-17 21:58:19 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:58:19 | FX: позиция эффекта start=(276.0,660.0) end=(972.0,684.0).
2026-04-17 21:58:19 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 21:58:19 | 📌 -------------------------

2026-04-17 21:58:20 | REQ: move cell accepted (RMB) x=28, y=23, mode=advance
2026-04-17 21:58:20 | [MOVE] unit=12 advance to=(28,23) dist=11 M=5 adv=6
2026-04-17 21:58:20 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 4, 1, 6, 4]
2026-04-17 21:58:20 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:20 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:58:20 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 21:58:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 21:58:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 21:58:20 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 21:58:20 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:58:20 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:20 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:20 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:58:20 | Оружие: Gauss flayer
2026-04-17 21:58:20 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:20 | BS оружия: 4+
2026-04-17 21:58:20 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:58:20 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:20 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:20 | Benefit of Cover: не активен.
2026-04-17 21:58:20 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:20 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:20 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:58:20 | Hit rolls:    [4, 3, 6, 6, 2, 6, 3, 6, 6, 2]  -> hits: 5 (crits: 5)
2026-04-17 21:58:20 | Save rolls:   [4, 4, 1, 6, 4]  (цель 4+) -> failed saves: 1
2026-04-17 21:58:20 | FX: найден failed saves = 1.
2026-04-17 21:58:20 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:58:20 | FX: найден итог урона = 1.0.
2026-04-17 21:58:20 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:58:20 | FX: позиция эффекта start=(276.0,660.0) end=(948.0,492.0).
2026-04-17 21:58:20 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 21:58:20 | 📌 -------------------------

2026-04-17 21:58:20 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:58:20 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:58:20 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 21:58:20 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:58:20 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:58:20 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 21:58:20 | Нет доступных целей для чарджа.
2026-04-17 21:58:20 | --- ФАЗА БОЯ ---
2026-04-17 21:58:20 | --- ХОД MODEL ---
2026-04-17 21:58:20 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:58:20 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 21:58:20 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:58:22 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-17 21:58:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 11). Выбор reachable_idx=10/528, mode=normal, advance=нет, distance=5
2026-04-17 21:58:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 15)
2026-04-17 21:58:22 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:22 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:22 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:58:22 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:22 | FX: найден failed saves = 1.
2026-04-17 21:58:22 | FX: найден итог урона = 1.0.
2026-04-17 21:58:22 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 21:58:23 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:24 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-17 21:58:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (9, 5). Выбор reachable_idx=6/356, mode=normal, advance=нет, distance=5
2026-04-17 21:58:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (4, 5)
2026-04-17 21:58:24 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:25 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:58:25 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:28 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 4, 6, 5, 6, 2]
2026-04-17 21:58:28 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-17 21:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 21:58:28 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 21:58:28 | 
🎲 Бросок на ранение (to wound): 5D6
2026-04-17 21:58:28 | 
🎲 Бросок сейвы (save): 6D6
2026-04-17 21:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (shooting)
2026-04-17 21:58:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-17 21:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-17 21:58:28 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:58:28 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:58:28 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:28 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:58:28 | Оружие: Gauss flayer
2026-04-17 21:58:28 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:28 | BS оружия: 4+
2026-04-17 21:58:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:28 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:28 | Benefit of Cover: не активен.
2026-04-17 21:58:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:28 | Hit rolls:    [2, 3, 1, 4, 2, 6, 3, 4, 5, 3, 1, 5, 5, 3, 2, 6, 6, 3, 6, 3]  -> hits: 9 (crits: 4)
2026-04-17 21:58:28 | Wound rolls:  [2, 5, 6, 2, 2]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 4 = 6
2026-04-17 21:58:28 | Save rolls:   [1, 4, 6, 5, 6, 2]  (цель 4+) -> failed saves: 2
2026-04-17 21:58:28 | FX: найден failed saves = 2.
2026-04-17 21:58:28 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 21:58:28 | FX: найден итог урона = 2.0.
2026-04-17 21:58:28 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 21:58:28 | FX: позиция эффекта start=(372.0,540.0) end=(684.0,564.0).
2026-04-17 21:58:28 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 21:58:28 | 📌 -------------------------

2026-04-17 21:58:30 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1]
2026-04-17 21:58:30 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-17 21:58:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 21:58:30 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 21:58:30 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-17 21:58:30 | 
🎲 Бросок сейвы (save): 1D6
2026-04-17 21:58:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 6. HP: 7.0 -> 6.0 (shooting)
2026-04-17 21:58:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-04-17 21:58:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-17 21:58:30 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:58:30 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:58:30 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:30 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 21:58:30 | Оружие: Gauss flayer
2026-04-17 21:58:30 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:30 | BS оружия: 4+
2026-04-17 21:58:30 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:30 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:30 | Benefit of Cover: не активен.
2026-04-17 21:58:30 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:30 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:30 | Hit rolls:    [1, 3, 2, 3, 2, 3, 5, 4, 1, 1]  -> hits: 2
2026-04-17 21:58:30 | Wound rolls:  [6, 1]  (цель 4+) -> wounds: 1
2026-04-17 21:58:30 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-04-17 21:58:30 | FX: найден failed saves = 1.
2026-04-17 21:58:30 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 21:58:30 | FX: найден итог урона = 1.0.
2026-04-17 21:58:30 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 21:58:30 | FX: позиция эффекта start=(132.0,108.0) end=(684.0,564.0).
2026-04-17 21:58:30 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 21:58:30 | 📌 -------------------------

2026-04-17 21:58:30 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:58:32 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-17 21:58:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:58:32 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-17 21:58:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 21:58:32 | [MODEL] Чардж: нет доступных целей
2026-04-17 21:58:32 | --- ФАЗА БОЯ ---
2026-04-17 21:58:32 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 21:58:32 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-17 21:58:32 | Итерация 1 завершена с наградой tensor([0.5630], device='cuda:0'), здоровье игрока [9.0, 6.0], здоровье модели [10.0, 10.0]
2026-04-17 21:58:32 | {'model health': [10.0, 10.0], 'player health': [9.0, 6.0], 'model alive models': [10, 10], 'player alive models': [9, 6], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': [0]}
2026-04-17 21:58:32 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 6.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-17 21:58:33 | === БОЕВОЙ РАУНД 3 ===
2026-04-17 21:58:33 | --- ХОД PLAYER ---
2026-04-17 21:58:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 21:58:33 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 21:58:34 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 21:58:34 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 21:58:34 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 21:58:34 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 21:58:34 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 21:58:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 21:58:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-04-17 21:58:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 21:58:40 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-17 21:58:40 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 21:58:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 21:58:41 | REQ: move cell accepted (RMB) x=24, y=26, mode=normal
2026-04-17 21:58:41 | [MOVE] unit=11 normal to=(24,26) dist=5 M=5
2026-04-17 21:58:41 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 6, 2, 3, 4]
2026-04-17 21:58:42 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:42 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 21:58:42 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 21:58:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-04-17 21:58:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 21:58:42 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-17 21:58:42 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:58:42 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:42 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 21:58:42 | Оружие: Gauss flayer
2026-04-17 21:58:42 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:42 | BS оружия: 4+
2026-04-17 21:58:42 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:58:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:42 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:42 | Benefit of Cover: не активен.
2026-04-17 21:58:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:42 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:58:42 | Hit rolls:    [6, 5, 4, 1, 5, 3, 6, 1, 6, 1, 5, 1, 6, 3, 4, 6, 5, 4, 2, 2]  -> hits: 5 (crits: 5)
2026-04-17 21:58:42 | Save rolls:   [6, 6, 2, 3, 4]  (цель 4+) -> failed saves: 2
2026-04-17 21:58:42 | FX: найден failed saves = 2.
2026-04-17 21:58:42 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 21:58:42 | FX: найден итог урона = 2.0.
2026-04-17 21:58:42 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 21:58:42 | FX: позиция эффекта start=(372.0,540.0) end=(708.0,660.0).
2026-04-17 21:58:42 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 21:58:42 | 📌 -------------------------

2026-04-17 21:58:42 | REQ: move cell accepted (RMB) x=26, y=21, mode=normal
2026-04-17 21:58:42 | [MOVE] unit=12 normal to=(26,21) dist=2 M=5
2026-04-17 21:58:43 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 2, 2, 4]
2026-04-17 21:58:43 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 21:58:43 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 21:58:43 | 
🎲 Бросок сейвы (save): 4D6
2026-04-17 21:58:43 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 4. HP: 7.0 -> 4.0 (Overwatch)
2026-04-17 21:58:43 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-04-17 21:58:43 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 3.0.
2026-04-17 21:58:43 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 21:58:43 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:43 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:43 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:58:43 | Оружие: Gauss flayer
2026-04-17 21:58:43 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:43 | BS оружия: 4+
2026-04-17 21:58:43 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 21:58:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:43 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:43 | Benefit of Cover: не активен.
2026-04-17 21:58:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:43 | Правило: Overwatch: попадания только на 6+
2026-04-17 21:58:43 | Hit rolls:    [6, 2, 6, 2, 3, 1, 3, 2, 5, 4, 2, 4, 5, 6, 4, 6, 2, 2, 4, 1]  -> hits: 4 (crits: 4)
2026-04-17 21:58:43 | Save rolls:   [1, 2, 2, 4]  (цель 4+) -> failed saves: 3
2026-04-17 21:58:43 | FX: найден failed saves = 3.
2026-04-17 21:58:43 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-17 21:58:43 | FX: найден итог урона = 3.0.
2026-04-17 21:58:43 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-17 21:58:43 | FX: позиция эффекта start=(372.0,540.0) end=(684.0,564.0).
2026-04-17 21:58:43 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 21:58:43 | 📌 -------------------------

2026-04-17 21:58:43 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 21:58:43 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-17 21:58:43 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(24, 26), target_filter_size=2, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:58:43 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(24, 26), full_cells=24, rapid_cells=12, вошло=1862, rapid=625, не вошло=538, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:58:44 | 
🎲 Бросок на попадание (to hit): 16D6
2026-04-17 21:58:44 | REQ: движок запросил кубы стрельбы (target=21, count=16, stage=hit).
2026-04-17 21:58:51 | 
🎲 Бросок на ранение (to wound): 6D6
2026-04-17 21:58:51 | REQ: движок запросил кубы стрельбы (target=21, count=6, stage=wound).
2026-04-17 21:58:54 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 21:58:54 | REQ: движок запросил кубы стрельбы (target=21, count=5, stage=save).
2026-04-17 21:58:58 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 1, 1, 4, 6]
2026-04-17 21:58:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-04-17 21:58:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-17 21:58:58 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:58 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:58:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:58:58 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:58:58 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-04-17 21:58:58 | Оружие: Gauss flayer
2026-04-17 21:58:58 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:58 | BS оружия: 4+
2026-04-17 21:58:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:58:58 | Save цели: 4+ (invul: нет)
2026-04-17 21:58:58 | Benefit of Cover: не активен.
2026-04-17 21:58:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:58:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:58:58 | Hit rolls:    [1, 2, 3, 4, 4, 6, 4, 6, 4, 3, 4, 3, 2, 1, 3, 4]  -> hits: 8 (crits: 2)
2026-04-17 21:58:58 | Wound rolls:  [1, 2, 3, 4, 6, 6]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-04-17 21:58:58 | Save rolls:   [3, 1, 1, 4, 6]  (цель 4+) -> failed saves: 3
2026-04-17 21:58:58 | FX: найден failed saves = 3.
2026-04-17 21:58:58 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-17 21:58:58 | FX: найден итог урона = 3.0.
2026-04-17 21:58:58 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-17 21:58:58 | FX: позиция эффекта start=(588.0,636.0) end=(372.0,540.0).
2026-04-17 21:58:58 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-04-17 21:58:58 | 📌 -------------------------

2026-04-17 21:58:58 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-04-17 21:58:58 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 21:58:58 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(26, 21), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:58:58 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(26, 21), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:58:58 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:58:58 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 21:58:58 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 21:58:58 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:58:58 | FX: найден failed saves = 3.
2026-04-17 21:58:58 | FX: найден итог урона = 3.0.
2026-04-17 21:58:58 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 21:59:14 | 
🎲 Бросок на попадание (to hit): 8D6
2026-04-17 21:59:14 | REQ: движок запросил кубы стрельбы (target=21, count=8, stage=hit).
2026-04-17 21:59:15 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-04-17 21:59:15 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 8D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-04-17 21:59:15 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-04-17 21:59:15 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 21:59:16 | 
🎲 Бросок на попадание (to hit): 8D6
2026-04-17 21:59:16 | REQ: движок запросил кубы стрельбы (target=21, count=8, stage=hit).
2026-04-17 21:59:18 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-04-17 21:59:18 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 8D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-04-17 21:59:18 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-04-17 21:59:18 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 21:59:20 | 
🎲 Бросок на попадание (to hit): 4D6
2026-04-17 21:59:20 | REQ: движок запросил кубы стрельбы (target=22, count=4, stage=hit).
2026-04-17 21:59:21 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-04-17 21:59:21 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 4D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-04-17 21:59:21 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-04-17 21:59:21 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 21:59:22 | 
🎲 Бросок на попадание (to hit): 8D6
2026-04-17 21:59:22 | REQ: движок запросил кубы стрельбы (target=21, count=8, stage=hit).
2026-04-17 21:59:25 | 
🎲 Бросок на ранение (to wound): 1D6
2026-04-17 21:59:25 | REQ: движок запросил кубы стрельбы (target=21, count=1, stage=wound).
2026-04-17 21:59:28 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-17 21:59:28 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:59:28 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 21:59:28 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:59:28 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:59:28 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-17 21:59:28 | Оружие: Gauss flayer
2026-04-17 21:59:28 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:59:28 | BS оружия: 4+
2026-04-17 21:59:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 21:59:28 | Save цели: 4+ (invul: нет)
2026-04-17 21:59:28 | Benefit of Cover: не активен.
2026-04-17 21:59:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 21:59:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 21:59:28 | Hit rolls:    [3, 1, 3, 4, 3, 3, 1, 3]  -> hits: 1
2026-04-17 21:59:28 | Wound rolls:  [3]  (цель 4+) -> wounds: 0
2026-04-17 21:59:28 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 21:59:28 | FX: найден итог урона = 0.0.
2026-04-17 21:59:28 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-17 21:59:28 | FX: позиция эффекта start=(636.0,516.0) end=(372.0,540.0).
2026-04-17 21:59:28 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-04-17 21:59:28 | 📌 -------------------------

2026-04-17 21:59:28 | --- ФАЗА ЧАРДЖА ---
2026-04-17 21:59:28 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(24, 26), target_filter_size=2, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:59:28 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(24, 26), full_cells=24, rapid_cells=12, вошло=1862, rapid=625, не вошло=538, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:59:28 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:59:33 | REQ: shooter changed Unit 12->Unit 21, target reset
2026-04-17 21:59:33 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 21 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(15, 22), target_filter_size=2, max_target_dist=11, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:59:33 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 21; source=(15, 22), full_cells=24, rapid_cells=12, вошло=1600, rapid=625, не вошло=800, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:59:37 | Бросок 2D6...
2026-04-17 21:59:40 | Бросок: 2 и 6
2026-04-17 21:59:40 | [PLAYER][CHARGE] Unit 11 — Necrons Necron Warriors (x10 моделей): Charge объявлен по цели Unit 21 — Necrons Necron Warriors (x10 моделей). Дистанция: 9.8. Бросок 2D6: 2 + 6 = 8.
2026-04-17 21:59:40 | Unit 11 — Necrons Necron Warriors (x10 моделей) успешно зачарджил Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 21:59:40 | [PLAYER][CHARGE] Unit 11 — Necrons Necron Warriors (x10 моделей): Движение чарджа: (26, 24) -> (24, 17), в контакте=True.
2026-04-17 21:59:40 | [MODEL][CHARGE] Heroic Intervention недоступен: нет подходящих юнитов в 6".
2026-04-17 21:59:40 | --- ФАЗА БОЯ ---
2026-04-17 21:59:40 | [PLAYER][FIGHT] Начало Fight phase. Первым выбирает активный игрок. Eligible MODEL: [21], Eligible PLAYER: [11].
2026-04-17 21:59:40 | 📌 --- FIGHT PHASE (DEBUG) ---
2026-04-17 21:59:40 | active_side=PLAYER
2026-04-17 21:59:40 | eligible_player=[11]
2026-04-17 21:59:40 | eligible_model=[21]
2026-04-17 21:59:40 | fights_first_player=[11]
2026-04-17 21:59:40 | fights_first_model=[]
2026-04-17 21:59:40 | computed_first_picker=ACTIVE
2026-04-17 21:59:40 | reason=чередование начинается с активной стороны
2026-04-17 21:59:40 | 📌 ---------------------------
2026-04-17 21:59:40 | REQ: shooter changed Unit 21->Unit 11, target reset
2026-04-17 21:59:40 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(24, 26), target_filter_size=2, max_target_dist=22, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:59:40 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(24, 26), full_cells=24, rapid_cells=12, вошло=1862, rapid=625, не вошло=538, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:59:40 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(17, 24), target_filter_size=2, max_target_dist=20, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 21:59:40 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(17, 24), full_cells=24, rapid_cells=12, вошло=1680, rapid=625, не вошло=720, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 21:59:40 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 21:59:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 21:59:40 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-17 21:59:40 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 21:59:40 | FX: найден итог урона = 0.0.
2026-04-17 21:59:40 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 21:59:44 | [FIGHT][ORDER] active_side=PLAYER bucket=first picker=PLAYER picked_unit=11 remaining_player=[] remaining_model=[21]
2026-04-17 21:59:44 | [PLAYER][FIGHT] Unit 11 — Necrons Necron Warriors (x10 моделей): Выбран для атаки. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:05:47 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:05:47 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:05:47 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:05:47 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:05:47 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:05:47 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:05:47 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-17 22:05:47 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:05:47 | FX: найден итог урона = 0.0.
2026-04-17 22:05:47 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-17 22:05:47 | FX: позиция эффекта start=(636.0,516.0) end=(372.0,540.0).
2026-04-17 22:05:47 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-04-17 22:05:48 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:05:48 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:05:48 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:05:48 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:05:48 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:05:48 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:05:48 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:05:49 | Roll-off Attacker/Defender: enemy=2 model=1 -> attacker=enemy
2026-04-17 22:05:49 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:05:49 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:05:49 | [DEPLOY][Only War] attacker=enemy -> LEFT x=0..14; defender=model -> RIGHT x=45..59
2026-04-17 22:05:49 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:05:49 | [DEPLOY] Order: enemy first, alternating
2026-04-17 22:05:49 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:05:50 | Ошибка деплоя: reason=outside_deploy_zone, x=51, y=27. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:05:50 | Ошибка деплоя: reason=outside_deploy_zone, x=45, y=25. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:05:51 | REQ: deploy cell accepted x=9, y=26
2026-04-17 22:05:51 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,9)
2026-04-17 22:05:51 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (26,9)
2026-04-17 22:05:51 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:05:51 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1976, coord=(32,56), attempt=1, reward=+0.017, score_before=0.000, score_after=0.348, reward_delta=+0.017, forward=0.047, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:05:51 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,56)
2026-04-17 22:05:51 | REQ: deploy cell accepted x=12, y=19
2026-04-17 22:05:51 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,12)
2026-04-17 22:05:51 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,12)
2026-04-17 22:05:51 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:05:51 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=471, coord=(7,51), attempt=1, reward=+0.002, score_before=0.348, score_after=0.391, reward_delta=+0.002, forward=0.090, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:05:51 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (7,51)
2026-04-17 22:05:51 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.069 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-04-17 22:05:51 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019530942057548285, 'units': 2, 'total_deploy_reward': 0.019530942057548285, 'forward_sum': 0.13728813559322023, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.06864406779661011, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-04-17 22:05:51 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:05:51 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:05:51 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:05:51 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:05:51 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:05:51 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:05:51 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:05:52 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:05:52 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:05:52 | --- ХОД PLAYER ---
2026-04-17 22:05:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:05:52 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:05:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:05:52 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:05:54 | REQ: move cell accepted (RMB) x=19, y=29, mode=advance
2026-04-17 22:05:54 | [MOVE] unit=11 advance to=(19,29) dist=10 M=5 adv=5
2026-04-17 22:05:55 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:05:55 | REQ: move cell accepted (RMB) x=23, y=23, mode=advance
2026-04-17 22:05:55 | [MOVE] unit=12 advance to=(23,23) dist=11 M=5 adv=6
2026-04-17 22:05:56 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:05:56 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:05:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:05:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:05:56 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:05:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:05:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:05:56 | Нет доступных целей для чарджа.
2026-04-17 22:05:56 | --- ФАЗА БОЯ ---
2026-04-17 22:05:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:56 | --- ХОД MODEL ---
2026-04-17 22:05:56 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:05:56 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:05:56 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:05:57 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-17 22:05:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 56). Выбор reachable_idx=14/284, mode=normal, advance=нет, distance=4
2026-04-17 22:05:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (28, 55)
2026-04-17 22:05:57 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:05:57 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-17 22:05:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 51). Выбор reachable_idx=15/379, mode=normal, advance=нет, distance=4
2026-04-17 22:05:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (3, 49)
2026-04-17 22:05:57 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:05:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:05:58 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-17 22:05:58 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:58 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:05:59 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 1, 5]
2026-04-17 22:05:59 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-17 22:05:59 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:05:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:05:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:05:59 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-17 22:05:59 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:05:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-17 22:05:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:05:59 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-17 22:05:59 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:05:59 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:05:59 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:05:59 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 22:05:59 | Оружие: Gauss flayer
2026-04-17 22:05:59 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:05:59 | BS оружия: 4+
2026-04-17 22:05:59 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:05:59 | Save цели: 4+ (invul: нет)
2026-04-17 22:05:59 | Benefit of Cover: не активен.
2026-04-17 22:05:59 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:05:59 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:05:59 | Hit rolls:    [2, 2, 6, 1, 3, 5, 2, 5, 1, 5]  -> hits: 4 (crits: 1)
2026-04-17 22:05:59 | Wound rolls:  [6, 2, 6]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-04-17 22:05:59 | Save rolls:   [6, 1, 5]  (цель 4+) -> failed saves: 1
2026-04-17 22:05:59 | FX: найден failed saves = 1.
2026-04-17 22:05:59 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:05:59 | FX: найден итог урона = 1.0.
2026-04-17 22:05:59 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:05:59 | FX: позиция эффекта start=(1188.0,84.0) end=(564.0,564.0).
2026-04-17 22:05:59 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 22:05:59 | 📌 -------------------------

2026-04-17 22:05:59 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:06:00 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-17 22:06:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:06:01 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-17 22:06:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:06:01 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:06:01 | --- ФАЗА БОЯ ---
2026-04-17 22:06:01 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:06:01 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 22:06:01 | Итерация 0 завершена с наградой tensor([0.0535], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-04-17 22:06:01 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:06:01 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-17 22:06:01 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 22:06:01 | --- ХОД PLAYER ---
2026-04-17 22:06:01 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:06:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:06:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:06:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:06:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:06:04 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP (всего 9 → 10)
2026-04-17 22:06:04 | FX: [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:06:04 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:06:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:06:06 | REQ: move cell accepted (RMB) x=24, y=32, mode=normal
2026-04-17 22:06:06 | [MOVE] unit=11 normal to=(24,32) dist=5 M=5
2026-04-17 22:06:06 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:06:07 | REQ: move cell accepted (RMB) x=28, y=26, mode=normal
2026-04-17 22:06:07 | [MOVE] unit=12 normal to=(28,26) dist=5 M=5
2026-04-17 22:06:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:06:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:06:08 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:08 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:08 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 22:06:08 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(23, 23), target_filter_size=2, max_target_dist=32, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:06:08 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(23, 23), full_cells=24, rapid_cells=12, вошло=1920, rapid=625, не вошло=480, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:06:08 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(28, 26), target_filter_size=2, max_target_dist=27, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:06:08 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(28, 26), full_cells=24, rapid_cells=12, вошло=1862, rapid=625, не вошло=538, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:06:10 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:06:10 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-04-17 22:06:17 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-17 22:06:17 | REQ: движок запросил кубы стрельбы (target=22, count=2, stage=wound).
2026-04-17 22:06:18 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 22:06:18 | REQ: движок запросил кубы стрельбы (target=22, count=2, stage=save).
2026-04-17 22:06:20 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1]
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:06:20 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:20 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:06:20 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:06:20 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:20 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-04-17 22:06:20 | Оружие: Gauss flayer
2026-04-17 22:06:20 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:20 | BS оружия: 4+
2026-04-17 22:06:20 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:20 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:20 | Benefit of Cover: не активен.
2026-04-17 22:06:20 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:20 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:20 | Hit rolls:    [2, 2, 2, 2, 2, 2, 3, 3, 4, 4]  -> hits: 2
2026-04-17 22:06:20 | Wound rolls:  [6, 6]  (цель 4+) -> wounds: 2
2026-04-17 22:06:20 | Save rolls:   [1, 1]  (цель 4+) -> failed saves: 2
2026-04-17 22:06:20 | FX: найден failed saves = 2.
2026-04-17 22:06:20 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:06:20 | FX: найден итог урона = 2.0.
2026-04-17 22:06:20 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:06:20 | FX: позиция эффекта start=(684.0,636.0) end=(1188.0,84.0).
2026-04-17 22:06:20 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-04-17 22:06:20 | 📌 -------------------------

2026-04-17 22:06:20 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:06:20 | Нет доступных целей для чарджа.
2026-04-17 22:06:20 | --- ФАЗА БОЯ ---
2026-04-17 22:06:20 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:20 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:20 | --- ХОД MODEL ---
2026-04-17 22:06:20 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 2
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:06:20 | 📌 [HEAL] Unit 22 • Reanimation Protocols: +2.0 HP (всего 8 → 10)
2026-04-17 22:06:20 | FX: [HEAL] Unit 22 • Reanimation Protocols: +2.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:06:20 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:06:20 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:06:30 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-17 22:06:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 55). Выбор reachable_idx=14/367, mode=normal, advance=нет, distance=4
2026-04-17 22:06:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (24, 53)
2026-04-17 22:06:30 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:06:31 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-17 22:06:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (3, 49). Выбор reachable_idx=15/329, mode=normal, advance=нет, distance=2
2026-04-17 22:06:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 47)
2026-04-17 22:06:31 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:06:31 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:06:32 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 4, 2, 4, 1]
2026-04-17 22:06:32 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-17 22:06:32 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:06:32 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:06:32 | 
🎲 Бросок на ранение (to wound): 2D6
2026-04-17 22:06:32 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:06:32 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-17 22:06:32 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:06:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-17 22:06:32 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:06:32 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:06:32 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:32 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:06:32 | Оружие: Gauss flayer
2026-04-17 22:06:32 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:32 | BS оружия: 4+
2026-04-17 22:06:32 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:32 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:32 | Benefit of Cover: не активен.
2026-04-17 22:06:32 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:32 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:32 | Hit rolls:    [2, 4, 6, 6, 6, 2, 1, 4, 6, 2]  -> hits: 6 (crits: 4)
2026-04-17 22:06:32 | Wound rolls:  [3, 4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 4 = 5
2026-04-17 22:06:32 | Save rolls:   [5, 4, 2, 4, 1]  (цель 4+) -> failed saves: 2
2026-04-17 22:06:32 | FX: найден failed saves = 2.
2026-04-17 22:06:32 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:06:32 | FX: найден итог урона = 2.0.
2026-04-17 22:06:32 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:06:32 | FX: позиция эффекта start=(1284.0,588.0) end=(684.0,636.0).
2026-04-17 22:06:32 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:06:32 | 📌 -------------------------

2026-04-17 22:06:33 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 6, 5, 4]
2026-04-17 22:06:33 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-17 22:06:33 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:33 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:06:33 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:06:33 | 
🎲 Бросок на ранение (to wound): 4D6
2026-04-17 22:06:33 | 
🎲 Бросок сейвы (save): 4D6
2026-04-17 22:06:33 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 0.0
2026-04-17 22:06:33 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:06:33 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:06:33 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:33 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 22:06:33 | Оружие: Gauss flayer
2026-04-17 22:06:33 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:33 | BS оружия: 4+
2026-04-17 22:06:33 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:33 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:33 | Benefit of Cover: не активен.
2026-04-17 22:06:33 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:33 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:33 | Hit rolls:    [1, 4, 4, 2, 6, 6, 4, 2, 3, 5]  -> hits: 6 (crits: 2)
2026-04-17 22:06:33 | Wound rolls:  [6, 3, 2, 5]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-04-17 22:06:33 | Save rolls:   [4, 6, 5, 4]  (цель 4+) -> failed saves: 0
2026-04-17 22:06:33 | FX: найден failed saves = 0.
2026-04-17 22:06:33 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 22:06:33 | FX: найден итог урона = 0.0.
2026-04-17 22:06:33 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-17 22:06:33 | FX: позиция эффекта start=(1140.0,36.0) end=(684.0,636.0).
2026-04-17 22:06:33 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 22:06:33 | 📌 -------------------------

2026-04-17 22:06:33 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:06:33 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:06:33 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:06:33 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:06:33 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:33 | FX: найден failed saves = 2.
2026-04-17 22:06:33 | FX: найден итог урона = 2.0.
2026-04-17 22:06:33 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 22:06:34 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-17 22:06:34 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:06:35 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-17 22:06:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:06:35 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:06:35 | --- ФАЗА БОЯ ---
2026-04-17 22:06:35 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:06:35 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-17 22:06:35 | Итерация 1 завершена с наградой tensor([0.1333], device='cuda:0'), здоровье игрока [10.0, 8.0], здоровье модели [10.0, 10.0]
2026-04-17 22:06:35 | {'model health': [10.0, 10.0], 'player health': [10.0, 8.0], 'model alive models': [10, 10], 'player alive models': [10, 8], 'modelCP': 4, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:06:35 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 8.0]
CP MODEL: 4, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-04-17 22:06:35 | === БОЕВОЙ РАУНД 3 ===
2026-04-17 22:06:35 | --- ХОД PLAYER ---
2026-04-17 22:06:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:06:35 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:06:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:06:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:06:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:37 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:06:37 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP (всего 8 → 9)
2026-04-17 22:06:37 | FX: дубликат [HEAL], pop-up пропущен.
2026-04-17 22:06:37 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:06:37 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:06:38 | REQ: move cell accepted (RMB) x=34, y=28, mode=advance
2026-04-17 22:06:38 | [MOVE] unit=11 advance to=(34,28) dist=11 M=5 adv=6
2026-04-17 22:06:39 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-17 22:06:39 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:06:39 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:06:39 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-17 22:06:39 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:06:39 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:06:39 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:39 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 22:06:39 | Оружие: Gauss flayer
2026-04-17 22:06:39 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:39 | BS оружия: 4+
2026-04-17 22:06:39 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:06:39 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:39 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:39 | Benefit of Cover: не активен.
2026-04-17 22:06:39 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:39 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:39 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:06:39 | Hit rolls:    [3, 4, 2, 1, 4, 4, 3, 1, 1, 3]  -> hits: 0
2026-04-17 22:06:39 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 22:06:39 | FX: найден итог урона = 0.0.
2026-04-17 22:06:39 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-17 22:06:39 | FX: позиция эффекта start=(1284.0,588.0) end=(564.0,804.0).
2026-04-17 22:06:39 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 22:06:39 | 📌 -------------------------

2026-04-17 22:06:40 | REQ: move cell accepted (RMB) x=33, y=24, mode=normal
2026-04-17 22:06:40 | [MOVE] unit=12 normal to=(33,24) dist=5 M=5
2026-04-17 22:06:40 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 6]
2026-04-17 22:06:40 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:06:40 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:06:40 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 22:06:40 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-17 22:06:40 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:06:40 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:06:40 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:40 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:06:40 | Оружие: Gauss flayer
2026-04-17 22:06:40 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:40 | BS оружия: 4+
2026-04-17 22:06:40 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:06:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:40 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:40 | Benefit of Cover: не активен.
2026-04-17 22:06:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:40 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:06:40 | Hit rolls:    [2, 1, 6, 1, 6, 4, 5, 1, 5, 1]  -> hits: 2 (crits: 2)
2026-04-17 22:06:40 | Save rolls:   [6, 6]  (цель 4+) -> failed saves: 0
2026-04-17 22:06:40 | FX: найден failed saves = 0.
2026-04-17 22:06:40 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 22:06:40 | FX: найден итог урона = 0.0.
2026-04-17 22:06:40 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0, outcome=save).
2026-04-17 22:06:40 | FX: позиция эффекта start=(1284.0,588.0) end=(684.0,636.0).
2026-04-17 22:06:40 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:06:40 | 📌 -------------------------

2026-04-17 22:06:40 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:06:40 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:06:40 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 22:06:40 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(28, 26), target_filter_size=2, max_target_dist=25, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:06:40 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(33, 24), target_filter_size=2, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:06:40 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(33, 24), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:06:42 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-17 22:06:42 | REQ: движок запросил кубы стрельбы (target=21, count=9, stage=hit).
2026-04-17 22:06:47 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:06:47 | REQ: движок запросил кубы стрельбы (target=21, count=5, stage=save).
2026-04-17 22:06:51 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1, 1, 1, 1]
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 5. HP: 10.0 -> 5.0 (overwatch)
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-04-17 22:06:51 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 5.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:51 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:06:51 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:06:51 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:06:51 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-17 22:06:51 | Оружие: Gauss flayer
2026-04-17 22:06:51 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:06:51 | BS оружия: 4+
2026-04-17 22:06:51 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:06:51 | Save цели: 4+ (invul: нет)
2026-04-17 22:06:51 | Benefit of Cover: не активен.
2026-04-17 22:06:51 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:06:51 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:06:51 | Hit rolls:    [1, 1, 1, 1, 6, 6, 6, 6, 6]  -> hits: 5 (crits: 5)
2026-04-17 22:06:51 | Save rolls:   [1, 1, 1, 1, 1]  (цель 4+) -> failed saves: 5
2026-04-17 22:06:51 | FX: найден failed saves = 5.
2026-04-17 22:06:51 | 
✅ Итог по движку: прошло урона = 5.0
2026-04-17 22:06:51 | FX: найден итог урона = 5.0.
2026-04-17 22:06:51 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=5.0, outcome=damage).
2026-04-17 22:06:51 | FX: позиция эффекта start=(804.0,588.0) end=(1284.0,588.0).
2026-04-17 22:06:51 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-04-17 22:06:51 | 📌 -------------------------

2026-04-17 22:06:51 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:06:51 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:06:51 | Нет доступных целей для чарджа.
2026-04-17 22:06:51 | --- ФАЗА БОЯ ---
2026-04-17 22:06:51 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:06:51 | --- ХОД MODEL ---
2026-04-17 22:06:51 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:06:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:06:51 | 📌 [HEAL] Unit 21 • Reanimation Protocols: +3.0 HP (всего 5 → 8)
2026-04-17 22:06:51 | FX: [HEAL] Unit 21 • Reanimation Protocols: +3.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:06:51 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 22:06:51 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:10 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:08:10 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:08:10 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:08:10 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:08:10 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:08:11 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:08:11 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:08:11 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:08:11 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:08:11 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:08:11 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:08:12 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-04-17 22:08:12 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:08:12 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:08:12 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:08:12 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:08:12 | [DEPLOY] Order: model first, alternating
2026-04-17 22:08:12 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:08:12 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=670, coord=(11,10), attempt=1, reward=+0.023, score_before=0.000, score_after=0.453, reward_delta=+0.023, forward=0.173, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:08:12 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (11,10)
2026-04-17 22:08:12 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:08:13 | Ошибка деплоя: reason=outside_deploy_zone, x=41, y=25. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:08:13 | Ошибка деплоя: reason=outside_deploy_zone, x=14, y=25. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:08:14 | Ошибка деплоя: reason=outside_deploy_zone, x=9, y=25. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:08:15 | REQ: deploy cell accepted x=52, y=25
2026-04-17 22:08:15 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,52)
2026-04-17 22:08:15 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,52)
2026-04-17 22:08:15 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:08:15 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1264, coord=(21,4), attempt=1, reward=-0.001, score_before=0.453, score_after=0.429, reward_delta=-0.001, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:08:15 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (21,4)
2026-04-17 22:08:15 | REQ: deploy cell accepted x=51, y=17
2026-04-17 22:08:16 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-04-17 22:08:16 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,51)
2026-04-17 22:08:16 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.147 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 22:08:16 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02144264879779267, 'units': 2, 'total_deploy_reward': 0.02144264879779267, 'forward_sum': 0.29491525423728815, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.14745762711864407, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 22:08:16 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:08:16 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:08:16 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:08:16 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:08:16 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:08:16 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:08:16 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:08:16 | FX: [HEAL] Unit 21 • Reanimation Protocols: +3.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:08:16 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:08:16 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:08:16 | --- ХОД PLAYER ---
2026-04-17 22:08:16 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:08:16 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:08:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:17 | REQ: move cell accepted (RMB) x=41, y=25, mode=advance
2026-04-17 22:08:17 | [MOVE] unit=11 advance to=(41,25) dist=11 M=5 adv=6
2026-04-17 22:08:18 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:08:18 | REQ: move cell accepted (RMB) x=40, y=17, mode=advance
2026-04-17 22:08:18 | [MOVE] unit=12 advance to=(40,17) dist=11 M=5 adv=6
2026-04-17 22:08:18 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:08:18 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:08:18 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:08:18 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:08:18 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:08:18 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:08:18 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:08:18 | Нет доступных целей для чарджа.
2026-04-17 22:08:18 | --- ФАЗА БОЯ ---
2026-04-17 22:08:18 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:18 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:18 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:18 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:18 | --- ХОД MODEL ---
2026-04-17 22:08:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:08:18 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:08:18 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:19 | [PACE] ack phase=movement unit_id=21 seq=1 step=before_unit ok=True
2026-04-17 22:08:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 10). Выбор reachable_idx=10/504, mode=normal, advance=нет, distance=5
2026-04-17 22:08:19 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (6, 14)
2026-04-17 22:08:19 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:08:20 | [PACE] ack phase=movement unit_id=22 seq=2 step=before_unit ok=True
2026-04-17 22:08:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 4). Выбор reachable_idx=6/367, mode=normal, advance=нет, distance=5
2026-04-17 22:08:20 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 5)
2026-04-17 22:08:20 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:08:20 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:08:20 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 1]
2026-04-17 22:08:20 | [PACE] ack phase=shooting unit_id=21 seq=3 step=before_unit ok=True
2026-04-17 22:08:20 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:08:20 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:08:20 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-17 22:08:20 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 22:08:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-17 22:08:20 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:08:20 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-17 22:08:20 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:08:20 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:08:20 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:20 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:20 | Оружие: Gauss flayer
2026-04-17 22:08:20 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:20 | BS оружия: 4+
2026-04-17 22:08:20 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:20 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:20 | Benefit of Cover: не активен.
2026-04-17 22:08:20 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:20 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:20 | Hit rolls:    [6, 5, 5, 3, 1, 1, 1, 2, 2, 4]  -> hits: 4 (crits: 1)
2026-04-17 22:08:20 | Wound rolls:  [2, 6, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-04-17 22:08:20 | Save rolls:   [4, 1]  (цель 4+) -> failed saves: 1
2026-04-17 22:08:20 | FX: найден failed saves = 1.
2026-04-17 22:08:20 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:08:20 | FX: найден итог урона = 1.0.
2026-04-17 22:08:20 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:08:20 | FX: позиция эффекта start=(348.0,156.0) end=(972.0,420.0).
2026-04-17 22:08:20 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:08:20 | 📌 -------------------------

2026-04-17 22:08:22 | [PACE] ack phase=shooting unit_id=22 seq=4 step=before_unit ok=True
2026-04-17 22:08:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:08:22 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:08:22 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:08:22 | [PACE] ack phase=charge unit_id=21 seq=5 step=before_unit ok=True
2026-04-17 22:08:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:08:23 | [PACE] ack phase=charge unit_id=22 seq=6 step=before_unit ok=True
2026-04-17 22:08:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:08:23 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:08:23 | --- ФАЗА БОЯ ---
2026-04-17 22:08:23 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:08:23 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 22:08:23 | Итерация 0 завершена с наградой tensor([0.0504], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-04-17 22:08:23 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:08:23 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-17 22:08:24 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 22:08:24 | --- ХОД PLAYER ---
2026-04-17 22:08:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:08:24 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:08:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:08:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:08:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:26 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:08:26 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP (всего 9 → 10)
2026-04-17 22:08:26 | FX: [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:08:26 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:08:26 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:27 | REQ: move cell accepted (RMB) x=30, y=22, mode=advance
2026-04-17 22:08:27 | [MOVE] unit=11 advance to=(30,22) dist=11 M=5 adv=6
2026-04-17 22:08:27 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 2]
2026-04-17 22:08:27 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:27 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:08:27 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 22:08:27 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-04-17 22:08:27 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:08:27 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-17 22:08:27 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:08:27 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:27 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:27 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 22:08:27 | Оружие: Gauss flayer
2026-04-17 22:08:27 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:27 | BS оружия: 4+
2026-04-17 22:08:27 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:08:27 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:27 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:27 | Benefit of Cover: не активен.
2026-04-17 22:08:27 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:27 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:27 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:08:27 | Hit rolls:    [4, 2, 5, 6, 5, 6, 1, 1, 5, 2]  -> hits: 2 (crits: 2)
2026-04-17 22:08:27 | Save rolls:   [3, 2]  (цель 4+) -> failed saves: 2
2026-04-17 22:08:27 | FX: найден failed saves = 2.
2026-04-17 22:08:27 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:08:27 | FX: найден итог урона = 2.0.
2026-04-17 22:08:27 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:08:27 | FX: позиция эффекта start=(348.0,156.0) end=(996.0,612.0).
2026-04-17 22:08:27 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 22:08:27 | 📌 -------------------------

2026-04-17 22:08:28 | REQ: move cell accepted (RMB) x=29, y=15, mode=advance
2026-04-17 22:08:28 | [MOVE] unit=12 advance to=(29,15) dist=11 M=5 adv=6
2026-04-17 22:08:28 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 6, 6, 2, 4]
2026-04-17 22:08:28 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:28 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 22:08:28 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:08:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-04-17 22:08:28 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:08:28 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-17 22:08:28 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:08:28 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:28 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:28 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:28 | Оружие: Gauss flayer
2026-04-17 22:08:28 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:28 | BS оружия: 4+
2026-04-17 22:08:28 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:08:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:28 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:28 | Benefit of Cover: не активен.
2026-04-17 22:08:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:28 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:08:28 | Hit rolls:    [2, 4, 4, 3, 4, 5, 4, 6, 3, 3, 5, 3, 3, 6, 5, 3, 4, 6, 6, 6]  -> hits: 5 (crits: 5)
2026-04-17 22:08:28 | Save rolls:   [3, 6, 6, 2, 4]  (цель 4+) -> failed saves: 2
2026-04-17 22:08:28 | FX: найден failed saves = 2.
2026-04-17 22:08:28 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:08:28 | FX: найден итог урона = 2.0.
2026-04-17 22:08:28 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:08:28 | FX: позиция эффекта start=(348.0,156.0) end=(972.0,420.0).
2026-04-17 22:08:28 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:08:28 | 📌 -------------------------

2026-04-17 22:08:28 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:08:28 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:08:28 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:08:28 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:08:28 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:08:28 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:08:28 | Нет доступных целей для чарджа.
2026-04-17 22:08:28 | --- ФАЗА БОЯ ---
2026-04-17 22:08:28 | --- ХОД MODEL ---
2026-04-17 22:08:28 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:08:28 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 22:08:28 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:29 | [PACE] ack phase=movement unit_id=21 seq=7 step=before_unit ok=True
2026-04-17 22:08:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (6, 14). Выбор reachable_idx=10/409, mode=normal, advance=нет, distance=5
2026-04-17 22:08:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 18)
2026-04-17 22:08:29 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:29 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:08:29 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:29 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:29 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:29 | FX: найден failed saves = 2.
2026-04-17 22:08:29 | FX: найден итог урона = 2.0.
2026-04-17 22:08:29 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 22:08:30 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:08:31 | [PACE] ack phase=movement unit_id=22 seq=8 step=before_unit ok=True
2026-04-17 22:08:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 5). Выбор reachable_idx=6/390, mode=normal, advance=нет, distance=5
2026-04-17 22:08:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (11, 5)
2026-04-17 22:08:31 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:32 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:08:32 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:08:33 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 4, 3, 2, 1, 6, 6, 3, 4]
2026-04-17 22:08:33 | [PACE] ack phase=shooting unit_id=21 seq=9 step=before_unit ok=True
2026-04-17 22:08:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:08:33 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 22:08:33 | 
🎲 Бросок на ранение (to wound): 7D6
2026-04-17 22:08:33 | 
🎲 Бросок сейвы (save): 9D6
2026-04-17 22:08:33 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 4. HP: 8.0 -> 4.0 (shooting)
2026-04-17 22:08:33 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-04-17 22:08:33 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 4.0
2026-04-17 22:08:33 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:08:33 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:08:33 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:33 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:33 | Оружие: Gauss flayer
2026-04-17 22:08:33 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:33 | BS оружия: 4+
2026-04-17 22:08:33 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:33 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:33 | Benefit of Cover: не активен.
2026-04-17 22:08:33 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:33 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:33 | Hit rolls:    [4, 3, 6, 1, 1, 4, 4, 5, 3, 4, 6, 5, 4, 1, 2, 1, 1, 6, 3, 6]  -> hits: 11 (crits: 4)
2026-04-17 22:08:33 | Wound rolls:  [5, 2, 6, 6, 1, 5, 4]  (цель 4+) -> rolled wounds: 5 + auto(w/LETHAL): 4 = 9
2026-04-17 22:08:33 | Save rolls:   [4, 4, 3, 2, 1, 6, 6, 3, 4]  (цель 4+) -> failed saves: 4
2026-04-17 22:08:33 | FX: найден failed saves = 4.
2026-04-17 22:08:33 | 
✅ Итог по движку: прошло урона = 4.0
2026-04-17 22:08:33 | FX: найден итог урона = 4.0.
2026-04-17 22:08:33 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=4.0, outcome=damage).
2026-04-17 22:08:33 | FX: позиция эффекта start=(444.0,36.0) end=(708.0,372.0).
2026-04-17 22:08:33 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:08:33 | 📌 -------------------------

2026-04-17 22:08:34 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[4, 6, 3, 4, 3]
2026-04-17 22:08:34 | [PACE] ack phase=shooting unit_id=22 seq=10 step=before_unit ok=True
2026-04-17 22:08:34 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:08:34 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:08:34 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-17 22:08:34 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:08:34 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 2. HP: 4.0 -> 2.0 (shooting)
2026-04-17 22:08:34 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 2. Причина: потери моделей.
2026-04-17 22:08:34 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-17 22:08:34 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:08:34 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:08:34 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:34 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-04-17 22:08:34 | Оружие: Gauss flayer
2026-04-17 22:08:34 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:34 | BS оружия: 4+
2026-04-17 22:08:34 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:34 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:34 | Benefit of Cover: не активен.
2026-04-17 22:08:34 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:34 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:34 | Hit rolls:    [5, 3, 3, 2, 6, 3, 5, 6, 6, 5]  -> hits: 6 (crits: 3)
2026-04-17 22:08:34 | Wound rolls:  [6, 5, 2]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 3 = 5
2026-04-17 22:08:34 | Save rolls:   [4, 6, 3, 4, 3]  (цель 4+) -> failed saves: 2
2026-04-17 22:08:34 | FX: найден failed saves = 2.
2026-04-17 22:08:34 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:08:34 | FX: найден итог урона = 2.0.
2026-04-17 22:08:34 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:08:34 | FX: позиция эффекта start=(132.0,276.0) end=(708.0,372.0).
2026-04-17 22:08:34 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-04-17 22:08:34 | 📌 -------------------------

2026-04-17 22:08:34 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:08:35 | [PACE] ack phase=charge unit_id=21 seq=11 step=before_unit ok=True
2026-04-17 22:08:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:08:35 | [PACE] ack phase=charge unit_id=22 seq=12 step=before_unit ok=True
2026-04-17 22:08:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:08:35 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:08:35 | --- ФАЗА БОЯ ---
2026-04-17 22:08:35 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:08:35 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-04-17 22:08:35 | Итерация 1 завершена с наградой tensor([0.2607], device='cuda:0'), здоровье игрока [8.0, 2.0], здоровье модели [10.0, 10.0]
2026-04-17 22:08:35 | {'model health': [10.0, 10.0], 'player health': [8.0, 2.0], 'model alive models': [10, 10], 'player alive models': [8, 2], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': [0]}
2026-04-17 22:08:35 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 2.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 4.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-04-17 22:08:36 | === БОЕВОЙ РАУНД 3 ===
2026-04-17 22:08:36 | --- ХОД PLAYER ---
2026-04-17 22:08:36 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:08:36 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-04-17 22:08:36 | Бросок 2D6...
2026-04-17 22:08:40 | Бросок: 1 1
2026-04-17 22:08:40 | Unit 12 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-04-17 22:08:41 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:08:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-17 22:08:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:08:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:08:42 | 📌 [HEAL] Unit 11 • Reanimation Protocols: +2.0 HP (всего 8 → 10)
2026-04-17 22:08:42 | FX: [HEAL] Unit 11 • Reanimation Protocols: +2.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:08:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=2, раны=[1, 1] всего=2
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:08:44 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-04-17 22:08:44 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +3.0 HP (всего 2 → 5)
2026-04-17 22:08:44 | FX: [HEAL] Unit 12 • Reanimation Protocols: +3.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:08:44 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 22:08:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:08:46 | REQ: move cell accepted (RMB) x=26, y=20, mode=normal
2026-04-17 22:08:46 | [MOVE] unit=11 normal to=(26,20) dist=4 M=5
2026-04-17 22:08:46 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 5, 5]
2026-04-17 22:08:46 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:46 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:08:46 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:08:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 22:08:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:08:46 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 22:08:46 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:08:46 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:46 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:46 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 22:08:46 | Оружие: Gauss flayer
2026-04-17 22:08:46 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:46 | BS оружия: 4+
2026-04-17 22:08:46 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:08:46 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:46 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:46 | Benefit of Cover: не активен.
2026-04-17 22:08:46 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:46 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:46 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:08:46 | Hit rolls:    [1, 6, 6, 5, 4, 6, 1, 1, 2, 2]  -> hits: 3 (crits: 3)
2026-04-17 22:08:46 | Save rolls:   [3, 5, 5]  (цель 4+) -> failed saves: 1
2026-04-17 22:08:46 | FX: найден failed saves = 1.
2026-04-17 22:08:46 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:08:46 | FX: найден итог урона = 1.0.
2026-04-17 22:08:46 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:08:46 | FX: позиция эффекта start=(444.0,36.0) end=(732.0,540.0).
2026-04-17 22:08:46 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 22:08:46 | 📌 -------------------------

2026-04-17 22:08:47 | REQ: move cell accepted (RMB) x=26, y=14, mode=normal
2026-04-17 22:08:47 | [MOVE] unit=12 normal to=(26,14) dist=3 M=5
2026-04-17 22:08:47 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 2, 3]
2026-04-17 22:08:47 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:08:47 | 
🎲 Бросок на попадание (to hit): 20D6
2026-04-17 22:08:47 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:08:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 3. HP: 5.0 -> 3.0 (Overwatch)
2026-04-17 22:08:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 3. Причина: потери моделей.
2026-04-17 22:08:47 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-04-17 22:08:47 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:08:47 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:47 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:47 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:47 | Оружие: Gauss flayer
2026-04-17 22:08:47 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:47 | BS оружия: 4+
2026-04-17 22:08:47 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:08:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:47 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:47 | Benefit of Cover: не активен.
2026-04-17 22:08:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:47 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:08:47 | Hit rolls:    [2, 2, 1, 1, 2, 5, 2, 5, 5, 5, 1, 3, 4, 2, 6, 2, 1, 6, 6, 5]  -> hits: 3 (crits: 3)
2026-04-17 22:08:47 | Save rolls:   [5, 2, 3]  (цель 4+) -> failed saves: 2
2026-04-17 22:08:47 | FX: найден failed saves = 2.
2026-04-17 22:08:47 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:08:47 | FX: найден итог урона = 2.0.
2026-04-17 22:08:47 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 22:08:47 | 📌 -------------------------

2026-04-17 22:08:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:08:47 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-17 22:08:47 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(26, 20), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:08:47 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(26, 20), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:08:49 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-17 22:08:49 | REQ: движок запросил кубы стрельбы (target=21, count=9, stage=hit).
2026-04-17 22:08:54 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:08:54 | REQ: движок запросил кубы стрельбы (target=21, count=5, stage=save).
2026-04-17 22:08:58 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 2, 1, 2, 2]
2026-04-17 22:08:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 5. HP: 10.0 -> 5.0 (overwatch)
2026-04-17 22:08:58 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-04-17 22:08:58 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 5.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:58 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:08:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:08:58 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:08:58 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-04-17 22:08:58 | Оружие: Gauss flayer
2026-04-17 22:08:58 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:58 | BS оружия: 4+
2026-04-17 22:08:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:08:58 | Save цели: 4+ (invul: нет)
2026-04-17 22:08:58 | Benefit of Cover: не активен.
2026-04-17 22:08:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:08:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:08:58 | Hit rolls:    [2, 2, 2, 2, 6, 6, 6, 6, 6]  -> hits: 5 (crits: 5)
2026-04-17 22:08:58 | Save rolls:   [2, 2, 1, 2, 2]  (цель 4+) -> failed saves: 5
2026-04-17 22:08:58 | FX: найден failed saves = 5.
2026-04-17 22:08:58 | 
✅ Итог по движку: прошло урона = 5.0
2026-04-17 22:08:58 | FX: найден итог урона = 5.0.
2026-04-17 22:08:58 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=5.0, outcome=damage).
2026-04-17 22:08:58 | FX: позиция эффекта start=(636.0,492.0) end=(444.0,36.0).
2026-04-17 22:08:58 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-04-17 22:08:58 | 📌 -------------------------

2026-04-17 22:08:58 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-04-17 22:08:58 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 22:08:58 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(26, 14), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:08:58 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(26, 14), full_cells=24, rapid_cells=12, вошло=1911, rapid=625, не вошло=489, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:08:58 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:08:58 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:08:58 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:08:58 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:08:58 | FX: найден failed saves = 2.
2026-04-17 22:08:58 | FX: найден итог урона = 2.0.
2026-04-17 22:08:58 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 22:09:05 | 
🎲 Бросок на попадание (to hit): 3D6
2026-04-17 22:09:05 | REQ: движок запросил кубы стрельбы (target=22, count=3, stage=hit).
2026-04-17 22:09:07 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:09:07 | REQ: движок запросил кубы стрельбы (target=22, count=3, stage=save).
2026-04-17 22:09:09 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1, 1]
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-04-17 22:09:10 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:09:10 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:09:10 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:09:10 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:09:10 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-04-17 22:09:10 | Оружие: Gauss flayer
2026-04-17 22:09:10 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:09:10 | BS оружия: 4+
2026-04-17 22:09:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:09:10 | Save цели: 4+ (invul: нет)
2026-04-17 22:09:10 | Benefit of Cover: не активен.
2026-04-17 22:09:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:09:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:09:10 | Hit rolls:    [6, 6, 6]  -> hits: 3 (crits: 3)
2026-04-17 22:09:10 | Save rolls:   [1, 1, 1]  (цель 4+) -> failed saves: 3
2026-04-17 22:09:10 | FX: найден failed saves = 3.
2026-04-17 22:09:10 | 
✅ Итог по движку: прошло урона = 3.0
2026-04-17 22:09:10 | FX: найден итог урона = 3.0.
2026-04-17 22:09:10 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=3.0, outcome=damage).
2026-04-17 22:09:10 | FX: позиция эффекта start=(636.0,348.0) end=(132.0,276.0).
2026-04-17 22:09:10 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-04-17 22:09:10 | 📌 -------------------------

2026-04-17 22:09:10 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:09:10 | Нет доступных целей для чарджа.
2026-04-17 22:09:10 | --- ФАЗА БОЯ ---
2026-04-17 22:09:10 | --- ХОД MODEL ---
2026-04-17 22:09:10 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:09:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:09:10 | 📌 [HEAL] Unit 21 • Reanimation Protocols: +3.0 HP (всего 5 → 8)
2026-04-17 22:09:10 | FX: дубликат [HEAL], pop-up пропущен.
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:09:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:09:10 | 📌 [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP (всего 7 → 8)
2026-04-17 22:09:10 | FX: [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:09:10 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 22:09:10 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:13:13 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:13:13 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:13:13 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:13:13 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:13:13 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:13:13 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:13:13 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:13:13 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:13:13 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:13:13 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:13:13 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:13:15 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-04-17 22:13:15 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:13:15 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:13:15 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:13:15 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:13:15 | [DEPLOY] Order: model first, alternating
2026-04-17 22:13:15 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:13:15 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1861, coord=(31,1), attempt=1, reward=+0.014, score_before=0.000, score_after=0.289, reward_delta=+0.014, forward=0.020, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:13:15 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (31,1)
2026-04-17 22:13:15 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:13:15 | Ошибка деплоя: reason=outside_deploy_zone, x=43, y=25. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-04-17 22:13:15 | REQ: deploy cell accepted x=46, y=18
2026-04-17 22:13:15 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (18,46)
2026-04-17 22:13:15 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (18,46)
2026-04-17 22:13:15 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:13:15 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=672, coord=(11,12), attempt=1, reward=+0.004, score_before=0.289, score_after=0.378, reward_delta=+0.004, forward=0.114, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:13:15 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (11,12)
2026-04-17 22:13:16 | REQ: deploy cell accepted x=51, y=10
2026-04-17 22:13:16 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (10,51)
2026-04-17 22:13:16 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (10,51)
2026-04-17 22:13:16 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.067 avg_spread=1.000 avg_edge=0.250 avg_cover=0.000
2026-04-17 22:13:16 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01891998423334647, 'units': 2, 'total_deploy_reward': 0.01891998423334647, 'forward_sum': 0.13389830508474576, 'spread_sum': 2.0, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.06694915254237288, 'avg_spread': 1.0, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-04-17 22:13:16 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:13:16 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:13:16 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:13:16 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:13:16 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:13:16 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:13:16 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:13:16 | FX: [HEAL] Unit 21 • Reanimation Protocols: +3.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:13:16 | FX: [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:13:17 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:13:17 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:13:17 | --- ХОД PLAYER ---
2026-04-17 22:13:17 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:13:17 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:13:17 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:13:18 | REQ: move cell accepted (RMB) x=51, y=24, mode=advance
2026-04-17 22:13:18 | [MOVE] unit=11 advance to=(51,24) dist=6 M=5 adv=1
2026-04-17 22:13:18 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:13:18 | REQ: move cell accepted (RMB) x=52, y=14, mode=normal
2026-04-17 22:13:18 | [MOVE] unit=12 normal to=(52,14) dist=4 M=5
2026-04-17 22:13:19 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:13:19 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:13:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=48.00, range=24.00, delta=+24.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:13:19 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:13:19 | Нет доступных целей для чарджа.
2026-04-17 22:13:19 | --- ФАЗА БОЯ ---
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=47.00, range=24.00, delta=+23.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=48.00, range=24.00, delta=+24.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=37.00, range=24.00, delta=+13.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:13:19 | --- ХОД MODEL ---
2026-04-17 22:13:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:13:19 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:13:19 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:17:24 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:17:24 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:17:24 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:17:24 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:17:24 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:17:24 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:17:24 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:17:24 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:17:24 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:17:24 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:17:24 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:17:33 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-04-17 22:17:33 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:17:33 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:17:33 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:17:33 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:17:33 | [DEPLOY] Order: model first, alternating
2026-04-17 22:17:33 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:17:33 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=368, coord=(6,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:17:33 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (6,8)
2026-04-17 22:17:33 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:17:34 | REQ: deploy cell accepted x=50, y=25
2026-04-17 22:17:34 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,50)
2026-04-17 22:17:34 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,50)
2026-04-17 22:17:34 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:17:34 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=791, coord=(13,11), attempt=1, reward=+0.001, score_before=0.437, score_after=0.449, reward_delta=+0.001, forward=0.164, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:17:34 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (13,11)
2026-04-17 22:17:34 | REQ: deploy cell accepted x=50, y=18
2026-04-17 22:17:34 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,50)
2026-04-17 22:17:34 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (18,50)
2026-04-17 22:17:34 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.152 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 22:17:34 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02242806464327947, 'units': 2, 'total_deploy_reward': 0.02242806464327947, 'forward_sum': 0.30338983050847457, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.15169491525423728, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 22:17:34 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:17:34 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:17:34 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:17:34 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:17:34 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:17:34 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:17:34 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:17:36 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:17:36 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:17:36 | --- ХОД PLAYER ---
2026-04-17 22:17:36 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:17:36 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:17:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:17:36 | REQ: move cell accepted (RMB) x=39, y=25, mode=advance
2026-04-17 22:17:36 | [MOVE] unit=11 advance to=(39,25) dist=11 M=5 adv=6
2026-04-17 22:17:37 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:17:37 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:17:37 | REQ: move cell accepted (RMB) x=39, y=18, mode=advance
2026-04-17 22:17:37 | [MOVE] unit=12 advance to=(39,18) dist=11 M=5 adv=6
2026-04-17 22:17:38 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:17:38 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:17:38 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:17:38 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:17:38 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:17:38 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:17:38 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:17:38 | Нет доступных целей для чарджа.
2026-04-17 22:17:38 | --- ФАЗА БОЯ ---
2026-04-17 22:17:38 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:17:38 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:17:38 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:17:38 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:17:38 | --- ХОД MODEL ---
2026-04-17 22:17:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:17:38 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:17:51 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-17 22:17:51 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:17:51 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:17:56 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-17 22:17:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (6, 8). Выбор reachable_idx=10/358, mode=normal, advance=нет, distance=5
2026-04-17 22:17:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 12)
2026-04-17 22:17:56 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:17:57 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-17 22:17:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 11). Выбор reachable_idx=6/525, mode=normal, advance=нет, distance=5
2026-04-17 22:17:57 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (8, 11)
2026-04-17 22:17:57 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:17:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:17:59 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[6, 3, 6, 5]
2026-04-17 22:17:59 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-17 22:17:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-04-17 22:17:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:17:59 | 
🎲 Бросок на ранение (to wound): 3D6
2026-04-17 22:17:59 | 
🎲 Бросок сейвы (save): 4D6
2026-04-17 22:17:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-04-17 22:17:59 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:17:59 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-04-17 22:17:59 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:17:59 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:17:59 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:17:59 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:17:59 | Оружие: Gauss flayer
2026-04-17 22:17:59 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:17:59 | BS оружия: 4+
2026-04-17 22:17:59 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:17:59 | Save цели: 4+ (invul: нет)
2026-04-17 22:17:59 | Benefit of Cover: не активен.
2026-04-17 22:17:59 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:17:59 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:17:59 | Hit rolls:    [2, 3, 6, 6, 2, 5, 6, 1, 5, 5]  -> hits: 6 (crits: 3)
2026-04-17 22:17:59 | Wound rolls:  [1, 1, 6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-04-17 22:17:59 | Save rolls:   [6, 3, 6, 5]  (цель 4+) -> failed saves: 1
2026-04-17 22:17:59 | FX: найден failed saves = 1.
2026-04-17 22:17:59 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:17:59 | FX: найден итог урона = 1.0.
2026-04-17 22:17:59 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:17:59 | FX: позиция эффекта start=(300.0,36.0) end=(948.0,444.0).
2026-04-17 22:17:59 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:17:59 | 📌 -------------------------

2026-04-17 22:18:00 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-17 22:18:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:18:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:18:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:18:00 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:18:01 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-17 22:18:01 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:18:02 | [PACE] ack phase=charge unit_id=22 seq=7 step=before_unit ok=True
2026-04-17 22:18:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:18:02 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:18:02 | --- ФАЗА БОЯ ---
2026-04-17 22:18:02 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:18:02 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 22:18:02 | Итерация 0 завершена с наградой tensor([0.0370], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [10.0, 10.0]
2026-04-17 22:18:02 | {'model health': [10.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [10, 10], 'player alive models': [10, 9], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:18:02 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-04-17 22:18:02 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 22:18:02 | --- ХОД PLAYER ---
2026-04-17 22:18:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:18:02 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:18:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:18:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:18:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:18:04 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:18:04 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP (всего 9 → 10)
2026-04-17 22:18:04 | FX: [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:18:04 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:18:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:18:06 | REQ: move cell accepted (RMB) x=34, y=20, mode=normal
2026-04-17 22:18:06 | [MOVE] unit=11 normal to=(34,20) dist=5 M=5
2026-04-17 22:18:06 | SHOT_DEBUG | attacker=Unit 22 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=- save_rolls=[]
2026-04-17 22:18:07 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:18:07 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:18:07 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-04-17 22:18:07 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:18:07 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:18:07 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:07 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-04-17 22:18:07 | Оружие: Gauss flayer
2026-04-17 22:18:07 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:18:07 | BS оружия: 4+
2026-04-17 22:18:07 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:18:07 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:18:07 | Save цели: 4+ (invul: нет)
2026-04-17 22:18:07 | Benefit of Cover: не активен.
2026-04-17 22:18:07 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:18:07 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:18:07 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:18:07 | Hit rolls:    [3, 3, 3, 2, 5, 2, 4, 2, 5, 1]  -> hits: 0
2026-04-17 22:18:07 | 
✅ Итог по движку: прошло урона = 0.0
2026-04-17 22:18:07 | FX: найден итог урона = 0.0.
2026-04-17 22:18:07 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0, outcome=miss).
2026-04-17 22:18:07 | FX: позиция эффекта start=(276.0,204.0) end=(948.0,612.0).
2026-04-17 22:18:07 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-04-17 22:18:07 | 📌 -------------------------

2026-04-17 22:18:07 | REQ: move cell accepted (RMB) x=35, y=14, mode=normal
2026-04-17 22:18:07 | [MOVE] unit=12 normal to=(35,14) dist=4 M=5
2026-04-17 22:18:07 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[3, 4, 5]
2026-04-17 22:18:07 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:18:07 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:18:07 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:18:07 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 22:18:07 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:18:07 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 22:18:07 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:18:07 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:18:07 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:07 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:18:07 | Оружие: Gauss flayer
2026-04-17 22:18:07 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:18:07 | BS оружия: 4+
2026-04-17 22:18:07 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:18:07 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:18:07 | Save цели: 4+ (invul: нет)
2026-04-17 22:18:07 | Benefit of Cover: не активен.
2026-04-17 22:18:07 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:18:07 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:18:07 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:18:07 | Hit rolls:    [2, 5, 2, 6, 3, 4, 5, 2, 6, 6]  -> hits: 3 (crits: 3)
2026-04-17 22:18:07 | Save rolls:   [3, 4, 5]  (цель 4+) -> failed saves: 1
2026-04-17 22:18:07 | FX: найден failed saves = 1.
2026-04-17 22:18:07 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:18:07 | FX: найден итог урона = 1.0.
2026-04-17 22:18:07 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:18:07 | FX: позиция эффекта start=(300.0,36.0) end=(948.0,444.0).
2026-04-17 22:18:07 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:18:07 | 📌 -------------------------

2026-04-17 22:18:07 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:18:07 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-04-17 22:18:07 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(34, 20), target_filter_size=2, max_target_dist=23, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:18:07 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(34, 20), full_cells=24, rapid_cells=12, вошло=1960, rapid=625, не вошло=440, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:18:09 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:18:09 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-04-17 22:18:12 | 
🎲 Бросок сейвы (save): 10D6
2026-04-17 22:18:12 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=save).
2026-04-17 22:18:16 | SHOT_DEBUG | attacker=Unit 11 — Necrons Necron Warriors (x10 моделей) target=Unit 22 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1, 1, 1, 1, 1, 6, 6, 6, 6]
2026-04-17 22:18:16 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 6. Осталось: 4. HP: 10.0 -> 4.0 (overwatch)
2026-04-17 22:18:16 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-04-17 22:18:16 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 6.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:16 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:18:16 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:18:16 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:16 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-04-17 22:18:16 | Оружие: Gauss flayer
2026-04-17 22:18:16 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:18:16 | BS оружия: 4+
2026-04-17 22:18:16 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:18:16 | Save цели: 4+ (invul: нет)
2026-04-17 22:18:16 | Benefit of Cover: не активен.
2026-04-17 22:18:16 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:18:16 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:18:16 | Hit rolls:    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]  -> hits: 10 (crits: 10)
2026-04-17 22:18:16 | Save rolls:   [1, 1, 1, 1, 1, 1, 6, 6, 6, 6]  (цель 4+) -> failed saves: 6
2026-04-17 22:18:16 | FX: найден failed saves = 6.
2026-04-17 22:18:16 | 
✅ Итог по движку: прошло урона = 6.0
2026-04-17 22:18:16 | FX: найден итог урона = 6.0.
2026-04-17 22:18:16 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=6.0, outcome=damage).
2026-04-17 22:18:16 | FX: позиция эффекта start=(828.0,492.0) end=(276.0,204.0).
2026-04-17 22:18:16 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-04-17 22:18:16 | 📌 -------------------------

2026-04-17 22:18:16 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-04-17 22:18:16 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-04-17 22:18:16 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(35, 14), target_filter_size=2, max_target_dist=24, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-04-17 22:18:16 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(35, 14), full_cells=24, rapid_cells=12, вошло=1911, rapid=625, не вошло=489, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-04-17 22:18:16 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:18:16 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:18:16 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:18:16 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:18:16 | FX: найден failed saves = 1.
2026-04-17 22:18:16 | FX: найден итог урона = 1.0.
2026-04-17 22:18:16 | FX: дубликат отчёта, эффект не создаём.
2026-04-17 22:18:19 | 
🎲 Бросок на попадание (to hit): 9D6
2026-04-17 22:18:19 | REQ: движок запросил кубы стрельбы (target=21, count=9, stage=hit).
2026-04-17 22:18:23 | 
🎲 Бросок на ранение (to wound): 1D6
2026-04-17 22:18:23 | REQ: движок запросил кубы стрельбы (target=21, count=1, stage=wound).
2026-04-17 22:18:26 | 
🎲 Бросок сейвы (save): 1D6
2026-04-17 22:18:26 | REQ: движок запросил кубы стрельбы (target=21, count=1, stage=save).
2026-04-17 22:18:27 | SHOT_DEBUG | attacker=Unit 12 — Necrons Necron Warriors (x10 моделей) target=Unit 21 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1]
2026-04-17 22:18:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-04-17 22:18:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:18:27 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:27 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:18:27 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:18:27 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:18:27 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-04-17 22:18:27 | Оружие: Gauss flayer
2026-04-17 22:18:27 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:18:27 | BS оружия: 4+
2026-04-17 22:18:27 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:18:27 | Save цели: 4+ (invul: нет)
2026-04-17 22:18:27 | Benefit of Cover: не активен.
2026-04-17 22:18:27 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:18:27 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:18:27 | Hit rolls:    [3, 3, 3, 3, 3, 3, 3, 3, 4]  -> hits: 1
2026-04-17 22:18:27 | Wound rolls:  [6]  (цель 4+) -> wounds: 1
2026-04-17 22:18:27 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-04-17 22:18:27 | FX: найден failed saves = 1.
2026-04-17 22:18:27 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:18:27 | FX: найден итог урона = 1.0.
2026-04-17 22:18:27 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:18:27 | FX: позиция эффекта start=(852.0,348.0) end=(300.0,36.0).
2026-04-17 22:18:27 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-04-17 22:18:27 | 📌 -------------------------

2026-04-17 22:18:27 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:18:27 | Нет доступных целей для чарджа.
2026-04-17 22:18:27 | --- ФАЗА БОЯ ---
2026-04-17 22:18:27 | --- ХОД MODEL ---
2026-04-17 22:18:28 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:18:36 | [PACE] ack phase=command unit_id=None seq=8 step=command_resolve ok=True
2026-04-17 22:18:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:18:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-04-17 22:18:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:18:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:18:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-04-17 22:18:36 | 📌 [HEAL] Unit 21 • Reanimation Protocols: +1.0 HP (всего 9 → 10)
2026-04-17 22:18:36 | FX: [HEAL] Unit 21 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:18:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:18:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:18:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=4, раны=[1, 1, 1, 1] всего=4
2026-04-17 22:18:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:18:36 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-04-17 22:18:36 | 📌 [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP (всего 4 → 5)
2026-04-17 22:18:36 | FX: [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:18:36 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-04-17 22:18:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:22:24 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:22:24 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:22:24 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:22:24 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:22:24 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:22:24 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:22:24 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:22:24 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:22:24 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:22:24 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:22:24 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:22:51 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-04-17 22:22:51 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:22:51 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:22:51 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:22:51 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:22:51 | [DEPLOY] Order: model first, alternating
2026-04-17 22:22:51 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:22:51 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2111, coord=(35,11), attempt=1, reward=+0.023, score_before=0.000, score_after=0.460, reward_delta=+0.023, forward=0.190, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:22:51 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (35,11)
2026-04-17 22:22:51 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:22:52 | REQ: deploy cell accepted x=52, y=22
2026-04-17 22:22:52 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (22,52)
2026-04-17 22:22:52 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (22,52)
2026-04-17 22:22:52 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:22:52 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=183, coord=(3,3), attempt=1, reward=-0.002, score_before=0.460, score_after=0.429, reward_delta=-0.002, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:22:52 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (3,3)
2026-04-17 22:22:52 | REQ: deploy cell accepted x=50, y=13
2026-04-17 22:22:53 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (13,50)
2026-04-17 22:22:53 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (13,50)
2026-04-17 22:22:53 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.156 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 22:22:53 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021442648797792667, 'units': 2, 'total_deploy_reward': 0.021442648797792667, 'forward_sum': 0.311864406779661, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1559322033898305, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 22:22:53 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:22:53 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:22:53 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:22:53 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:22:53 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:22:53 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:22:53 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:22:53 | FX: [HEAL] Unit 21 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:22:53 | FX: [HEAL] Unit 22 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:22:53 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:22:53 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:22:53 | --- ХОД PLAYER ---
2026-04-17 22:22:53 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:22:53 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:22:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:22:54 | REQ: move cell accepted (RMB) x=41, y=27, mode=advance
2026-04-17 22:22:54 | [MOVE] unit=11 advance to=(41,27) dist=11 M=5 adv=6
2026-04-17 22:22:55 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:22:55 | REQ: move cell accepted (RMB) x=41, y=20, mode=advance
2026-04-17 22:22:55 | [MOVE] unit=12 advance to=(41,20) dist=9 M=5 adv=4
2026-04-17 22:22:56 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:22:56 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:22:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:22:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:22:56 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:22:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:22:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:22:56 | Нет доступных целей для чарджа.
2026-04-17 22:22:56 | --- ФАЗА БОЯ ---
2026-04-17 22:22:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:22:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:22:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:22:56 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:22:56 | --- ХОД MODEL ---
2026-04-17 22:22:56 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:22:56 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:23:08 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-17 22:23:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:23:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:23:09 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-17 22:23:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 11). Выбор reachable_idx=10/367, mode=normal, advance=нет, distance=5
2026-04-17 22:23:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 15)
2026-04-17 22:23:09 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:23:10 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-17 22:23:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (3, 3). Выбор reachable_idx=6/224, mode=normal, advance=нет, distance=3
2026-04-17 22:23:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 5)
2026-04-17 22:23:10 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:23:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:23:11 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[1, 1, 6]
2026-04-17 22:23:11 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-17 22:23:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:23:11 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:23:11 | 
🎲 Бросок на ранение (to wound): 7D6
2026-04-17 22:23:11 | 
🎲 Бросок сейвы (save): 3D6
2026-04-17 22:23:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-17 22:23:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:23:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-17 22:23:11 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:23:11 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:23:11 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:23:11 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 22:23:11 | Оружие: Gauss flayer
2026-04-17 22:23:11 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:23:11 | BS оружия: 4+
2026-04-17 22:23:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:23:11 | Save цели: 4+ (invul: нет)
2026-04-17 22:23:11 | Benefit of Cover: не активен.
2026-04-17 22:23:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:23:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:23:11 | Hit rolls:    [5, 1, 5, 4, 5, 4, 5, 5, 3, 1]  -> hits: 7
2026-04-17 22:23:11 | Wound rolls:  [2, 3, 3, 6, 4, 6, 3]  (цель 4+) -> wounds: 3
2026-04-17 22:23:11 | Save rolls:   [1, 1, 6]  (цель 4+) -> failed saves: 2
2026-04-17 22:23:11 | FX: найден failed saves = 2.
2026-04-17 22:23:11 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:23:11 | FX: найден итог урона = 2.0.
2026-04-17 22:23:11 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:23:11 | FX: позиция эффекта start=(372.0,732.0) end=(996.0,660.0).
2026-04-17 22:23:11 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 22:23:11 | 📌 -------------------------

2026-04-17 22:23:13 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-17 22:23:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:23:13 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:23:13 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:23:13 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:47:45 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:47:45 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:47:45 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:47:45 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:47:46 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:47:46 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:47:46 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:47:46 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:47:46 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:47:46 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:47:46 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:47:48 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-04-17 22:47:48 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:47:48 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:47:48 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:47:48 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:47:48 | [DEPLOY] Order: model first, alternating
2026-04-17 22:47:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:47:48 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=728, coord=(12,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:47:48 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (12,8)
2026-04-17 22:47:48 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:47:48 | REQ: deploy cell accepted x=53, y=24
2026-04-17 22:47:48 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,53)
2026-04-17 22:47:48 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,53)
2026-04-17 22:47:48 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:47:48 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1627, coord=(27,7), attempt=1, reward=-0.000, score_before=0.437, score_after=0.433, reward_delta=-0.000, forward=0.131, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:47:48 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,7)
2026-04-17 22:47:49 | REQ: deploy cell accepted x=50, y=17
2026-04-17 22:47:49 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-04-17 22:47:49 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (17,50)
2026-04-17 22:47:49 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.135 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 22:47:49 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021639731966890025, 'units': 2, 'total_deploy_reward': 0.021639731966890025, 'forward_sum': 0.2694915254237288, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.1347457627118644, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 22:47:49 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:47:49 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:47:49 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:47:49 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:47:49 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:47:49 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:47:49 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:47:50 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:47:50 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:47:50 | --- ХОД PLAYER ---
2026-04-17 22:47:50 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:47:50 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:47:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:47:50 | REQ: move cell accepted (RMB) x=42, y=19, mode=advance
2026-04-17 22:47:50 | [MOVE] unit=11 advance to=(42,19) dist=11 M=5 adv=6
2026-04-17 22:47:51 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:47:51 | REQ: move cell accepted (RMB) x=40, y=12, mode=advance
2026-04-17 22:47:51 | [MOVE] unit=12 advance to=(40,12) dist=10 M=5 adv=5
2026-04-17 22:47:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:47:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:47:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:47:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:47:52 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:47:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:47:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:47:52 | Нет доступных целей для чарджа.
2026-04-17 22:47:52 | --- ФАЗА БОЯ ---
2026-04-17 22:47:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:52 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:52 | --- ХОД MODEL ---
2026-04-17 22:47:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:47:53 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-17 22:47:53 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:47:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:47:54 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-17 22:47:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (12, 8). Выбор reachable_idx=10/459, mode=normal, advance=нет, distance=5
2026-04-17 22:47:54 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 12)
2026-04-17 22:47:54 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:47:55 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-17 22:47:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 7). Выбор reachable_idx=6/436, mode=normal, advance=нет, distance=5
2026-04-17 22:47:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 7)
2026-04-17 22:47:55 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:47:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:47:55 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-17 22:47:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:47:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:48:06 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-17 22:48:06 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:48:06 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:48:06 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:48:06 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:48:13 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-17 22:48:13 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:48:14 | [PACE] ack phase=charge unit_id=22 seq=7 step=before_unit ok=True
2026-04-17 22:48:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:48:14 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:48:14 | --- ФАЗА БОЯ ---
2026-04-17 22:48:14 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:48:14 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 22:48:14 | Итерация 0 завершена с наградой tensor([0.0241], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-04-17 22:48:14 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:48:14 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:48:15 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 22:48:15 | --- ХОД PLAYER ---
2026-04-17 22:48:15 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:48:15 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:48:15 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:48:16 | REQ: move cell accepted (RMB) x=32, y=23, mode=advance
2026-04-17 22:48:16 | [MOVE] unit=11 advance to=(32,23) dist=10 M=5 adv=5
2026-04-17 22:48:16 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 11 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[2, 4]
2026-04-17 22:48:16 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-04-17 22:48:16 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:48:16 | 
🎲 Бросок сейвы (save): 2D6
2026-04-17 22:48:16 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-04-17 22:48:16 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-04-17 22:48:16 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-04-17 22:48:16 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-04-17 22:48:16 | FX: старт отчёта (overwatch), ts=no-ts.
2026-04-17 22:48:16 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:48:16 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-04-17 22:48:16 | Оружие: Gauss flayer
2026-04-17 22:48:16 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:48:16 | BS оружия: 4+
2026-04-17 22:48:16 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-04-17 22:48:16 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:48:16 | Save цели: 4+ (invul: нет)
2026-04-17 22:48:16 | Benefit of Cover: не активен.
2026-04-17 22:48:16 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:48:16 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:48:16 | Правило: Overwatch: попадания только на 6+
2026-04-17 22:48:16 | Hit rolls:    [4, 6, 5, 5, 3, 6, 4, 5, 5, 3]  -> hits: 2 (crits: 2)
2026-04-17 22:48:16 | Save rolls:   [2, 4]  (цель 4+) -> failed saves: 1
2026-04-17 22:48:16 | FX: найден failed saves = 1.
2026-04-17 22:48:16 | 
✅ Итог по движку: прошло урона = 1.0
2026-04-17 22:48:16 | FX: найден итог урона = 1.0.
2026-04-17 22:48:16 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0, outcome=damage).
2026-04-17 22:48:16 | FX: позиция эффекта start=(300.0,180.0) end=(1020.0,468.0).
2026-04-17 22:48:16 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-04-17 22:48:16 | 📌 -------------------------

2026-04-17 22:51:16 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-04-17 22:51:16 | [VIEWER] Фоллбэк-рендер не активирован.
2026-04-17 22:51:16 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-04-17 22:51:16 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-04-17 22:51:17 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:51:17 | [MODEL] checkpoint: используется C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth (рядом нет C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pth)
2026-04-17 22:51:17 | [MODEL] pickle=C:\40kAI\models\ppo\ppo-run-20260410-200950\model-20260410-200950.pickle
2026-04-17 22:51:17 | [MODEL] checkpoint=C:\40kAI\models\ppo\ppo-run-20260410-200950\checkpoint_ep300.pth
2026-04-17 22:51:17 | Action keys: dict_keys(['attack', 'charge', 'cp_on', 'move', 'move_num_0', 'move_num_1', 'shoot', 'use_cp'])
2026-04-17 22:51:17 | [MODEL] env отсутствовал в pickle: пересоздан (mission=only_war, b_len=40, b_hei=60)
2026-04-17 22:51:17 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-04-17 22:51:18 | Roll-off Attacker/Defender: enemy=2 model=3 -> attacker=model
2026-04-17 22:51:18 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-43', 10)]
2026-04-17 22:51:18 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-04-17 22:51:18 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-04-17 22:51:18 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-04-17 22:51:18 | [DEPLOY] Order: model first, alternating
2026-04-17 22:51:18 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:51:18 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=607, coord=(10,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:51:18 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (10,7)
2026-04-17 22:51:18 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-04-17 22:51:19 | REQ: deploy cell accepted x=48, y=25
2026-04-17 22:51:19 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,48)
2026-04-17 22:51:19 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,48)
2026-04-17 22:51:19 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-04-17 22:51:19 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1624, coord=(27,4), attempt=1, reward=-0.001, score_before=0.429, score_after=0.417, reward_delta=-0.001, forward=0.097, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-04-17 22:51:19 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,4)
2026-04-17 22:51:19 | REQ: deploy cell accepted x=47, y=19
2026-04-17 22:51:19 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,47)
2026-04-17 22:51:19 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,47)
2026-04-17 22:51:19 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.109 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-04-17 22:51:19 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020851399290500592, 'units': 2, 'total_deploy_reward': 0.020851399290500592, 'forward_sum': 0.21864406779661016, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10932203389830508, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-04-17 22:51:19 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-04-17 22:51:19 | [MODEL] n_actions (из env): [5, 2, 2, 2, 5, 2, 24, 24]
2026-04-17 22:51:19 | [MODEL] Архитектура сети: ppo_actor_critic
2026-04-17 22:51:19 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-04-17 22:51:19 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:51:19 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-04-17 22:51:19 | FX: перепроигрываю 30 строк(и) лога.
2026-04-17 22:51:20 | === БОЕВОЙ РАУНД 1 ===
2026-04-17 22:51:20 | [FIGHT][ENV] file=C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py exe=C:\40kAI\.venv\Scripts\python.exe cwd=C:\40kAI FIGHT_REPORT=1 VERBOSE_LOGS=1 MANUAL_DICE=1 PLAY_NO_EXPLORATION=1 TRAIN_DEBUG=0
2026-04-17 22:51:20 | --- ХОД PLAYER ---
2026-04-17 22:51:20 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:51:20 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:51:20 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:51:21 | REQ: move cell accepted (RMB) x=37, y=23, mode=advance
2026-04-17 22:51:21 | [MOVE] unit=11 advance to=(37,23) dist=11 M=5 adv=6
2026-04-17 22:51:22 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:51:22 | REQ: move cell accepted (RMB) x=36, y=16, mode=advance
2026-04-17 22:51:22 | [MOVE] unit=12 advance to=(36,16) dist=11 M=5 adv=6
2026-04-17 22:51:23 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:51:23 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:51:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:51:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-04-17 22:51:23 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:51:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:51:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-04-17 22:51:23 | Нет доступных целей для чарджа.
2026-04-17 22:51:23 | --- ФАЗА БОЯ ---
2026-04-17 22:51:23 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:23 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:23 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:23 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:23 | --- ХОД MODEL ---
2026-04-17 22:51:23 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:51:24 | [PACE] ack phase=command unit_id=None seq=1 step=command_resolve ok=True
2026-04-17 22:51:24 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:51:24 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:51:25 | [PACE] ack phase=movement unit_id=21 seq=2 step=before_unit ok=True
2026-04-17 22:51:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 7). Выбор reachable_idx=10/417, mode=normal, advance=нет, distance=5
2026-04-17 22:51:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (5, 11)
2026-04-17 22:51:25 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:51:27 | [PACE] ack phase=movement unit_id=22 seq=3 step=before_unit ok=True
2026-04-17 22:51:27 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 4). Выбор reachable_idx=6/367, mode=normal, advance=нет, distance=5
2026-04-17 22:51:27 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 5)
2026-04-17 22:51:27 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-04-17 22:51:27 | --- ФАЗА СТРЕЛЬБЫ ---
2026-04-17 22:51:30 | SHOT_DEBUG | attacker=Unit 21 — Necrons Necron Warriors (x10 моделей) target=Unit 12 — Necrons Necron Warriors (x10 моделей) effect=- cover_active=0 save_base=4 ap=0 inv=0 save_target=4 save_rolls=[5, 3, 5, 1, 4]
2026-04-17 22:51:30 | [PACE] ack phase=shooting unit_id=21 seq=4 step=before_unit ok=True
2026-04-17 22:51:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-04-17 22:51:30 | 
🎲 Бросок на попадание (to hit): 10D6
2026-04-17 22:51:30 | 
🎲 Бросок на ранение (to wound): 4D6
2026-04-17 22:51:30 | 
🎲 Бросок сейвы (save): 5D6
2026-04-17 22:51:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-04-17 22:51:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-04-17 22:51:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-04-17 22:51:30 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-04-17 22:51:30 | FX: старт отчёта (shooting), ts=no-ts.
2026-04-17 22:51:30 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-04-17 22:51:30 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-04-17 22:51:30 | Оружие: Gauss flayer
2026-04-17 22:51:30 | FX: найдена строка оружия: Gauss flayer.
2026-04-17 22:51:30 | BS оружия: 4+
2026-04-17 22:51:30 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-04-17 22:51:30 | Save цели: 4+ (invul: нет)
2026-04-17 22:51:30 | Benefit of Cover: не активен.
2026-04-17 22:51:30 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-04-17 22:51:30 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-04-17 22:51:30 | Hit rolls:    [5, 4, 5, 2, 6, 1, 4, 6, 3, 1]  -> hits: 6 (crits: 2)
2026-04-17 22:51:30 | Wound rolls:  [4, 1, 4, 4]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-04-17 22:51:30 | Save rolls:   [5, 3, 5, 1, 4]  (цель 4+) -> failed saves: 2
2026-04-17 22:51:30 | FX: найден failed saves = 2.
2026-04-17 22:51:30 | 
✅ Итог по движку: прошло урона = 2.0
2026-04-17 22:51:30 | FX: найден итог урона = 2.0.
2026-04-17 22:51:30 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0, outcome=damage).
2026-04-17 22:51:30 | FX: позиция эффекта start=(276.0,132.0) end=(876.0,396.0).
2026-04-17 22:51:30 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-04-17 22:51:30 | 📌 -------------------------

2026-04-17 22:51:34 | [PACE] ack phase=shooting unit_id=22 seq=5 step=before_unit ok=True
2026-04-17 22:51:34 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:34 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-04-17 22:51:34 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-04-17 22:51:34 | --- ФАЗА ЧАРДЖА ---
2026-04-17 22:51:35 | [PACE] ack phase=charge unit_id=21 seq=6 step=before_unit ok=True
2026-04-17 22:51:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:51:37 | [PACE] ack phase=charge unit_id=22 seq=7 step=before_unit ok=True
2026-04-17 22:51:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-04-17 22:51:37 | [MODEL] Чардж: нет доступных целей
2026-04-17 22:51:37 | --- ФАЗА БОЯ ---
2026-04-17 22:51:37 | [MODEL] Ближний бой: нет доступных атак
2026-04-17 22:51:37 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-04-17 22:51:37 | Итерация 0 завершена с наградой tensor([0.0844], device='cuda:0'), здоровье игрока [10.0, 8.0], здоровье модели [10.0, 10.0]
2026-04-17 22:51:37 | {'model health': [10.0, 10.0], 'player health': [10.0, 8.0], 'model alive models': [10, 10], 'player alive models': [10, 8], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None, 'model controlled objectives': [], 'player controlled objectives': []}
2026-04-17 22:51:37 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 8.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-04-17 22:51:39 | === БОЕВОЙ РАУНД 2 ===
2026-04-17 22:51:39 | --- ХОД PLAYER ---
2026-04-17 22:51:39 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-04-17 22:51:39 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-04-17 22:51:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-04-17 22:51:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-04-17 22:51:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-04-17 22:51:42 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-04-17 22:51:42 | 📌 [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP (всего 8 → 9)
2026-04-17 22:51:42 | FX: [HEAL] Unit 12 • Reanimation Protocols: +1.0 HP → FxShotEvent (report_type=heal).
2026-04-17 22:51:42 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-04-17 22:51:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-04-17 22:51:44 | REQ: move cell accepted (RMB) x=33, y=25, mode=normal
2026-04-17 22:51:44 | [MOVE] unit=11 normal to=(33,25) dist=4 M=5
2026-04-17 22:51:44 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
