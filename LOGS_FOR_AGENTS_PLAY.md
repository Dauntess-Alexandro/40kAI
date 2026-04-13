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
