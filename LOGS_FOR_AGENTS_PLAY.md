2026-03-14 13:48:36 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-14 13:48:36 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-14 13:48:36 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-14 13:48:36 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-14 13:48:37 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-14 13:48:42 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-41-914302.pickle
2026-03-14 13:48:42 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-41-914302.pth
2026-03-14 13:48:42 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-14 13:48:49 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-14 13:48:49 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-14 13:48:49 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-14 13:48:49 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-14 13:48:49 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-14 13:48:49 | [DEPLOY] Order: model first, alternating
2026-03-14 13:48:49 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-14 13:48:49 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1992, coord=(33,12), attempt=1, reward=+0.023, score_before=0.000, score_after=0.468, reward_delta=+0.023, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-14 13:48:49 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (33,12)
2026-03-14 13:48:49 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-14 13:48:49 | REQ: deploy cell accepted x=48, y=32
2026-03-14 13:48:49 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,48)
2026-03-14 13:48:49 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,48)
2026-03-14 13:48:49 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-14 13:48:49 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1508, coord=(25,8), attempt=1, reward=-0.001, score_before=0.468, score_after=0.453, reward_delta=-0.001, forward=0.173, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-14 13:48:49 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (25,8)
2026-03-14 13:48:50 | REQ: deploy cell accepted x=46, y=22
2026-03-14 13:48:51 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,46)
2026-03-14 13:48:51 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,46)
2026-03-14 13:48:51 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.023 total_deploy_reward=+0.023 avg_forward=0.190 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-14 13:48:51 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.022625147812376824, 'units': 2, 'total_deploy_reward': 0.022625147812376824, 'forward_sum': 0.37966101694915255, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.18983050847457628, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-14 13:48:51 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-14 13:48:51 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-14 13:48:51 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-14 13:48:51 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-14 13:48:51 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-14 13:48:51 | FX: перепроигрываю 30 строк(и) лога.
2026-03-14 13:48:54 | === БОЕВОЙ РАУНД 1 ===
2026-03-14 13:48:54 | --- ХОД PLAYER ---
2026-03-14 13:48:54 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 13:48:54 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 13:48:54 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 13:48:55 | REQ: move cell accepted (RMB) x=37, y=31, mode=advance
2026-03-14 13:48:55 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-14 13:48:55 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-14 13:48:55 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 13:48:55 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-14 13:48:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-14 13:48:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-14 13:48:55 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-14 13:48:55 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-14 13:48:55 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 13:48:55 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:48:55 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-14 13:48:55 | Оружие: Gauss flayer
2026-03-14 13:48:55 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:48:55 | BS оружия: 4+
2026-03-14 13:48:55 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-14 13:48:55 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 13:48:55 | Save цели: 4+ (invul: нет)
2026-03-14 13:48:55 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-14 13:48:55 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 13:48:55 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 13:48:55 | Правило: Overwatch: попадания только на 6+
2026-03-14 13:48:55 | Эффект: benefit of cover
2026-03-14 13:48:55 | Hit rolls:    [4, 3, 3, 5, 4, 5, 6, 2, 4, 3]  -> hits: 1 (crits: 1)
2026-03-14 13:48:55 | Save rolls:   [2]  (цель 3+) -> failed saves: 1
2026-03-14 13:48:55 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-14 13:48:55 | FX: найден итог урона = 1.0.
2026-03-14 13:48:55 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-14 13:48:56 | FX: позиция эффекта start=(300.0,804.0) end=(1164.0,780.0).
2026-03-14 13:48:56 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-14 13:48:56 | 📌 -------------------------

2026-03-14 13:48:56 | REQ: move cell accepted (RMB) x=35, y=29, mode=advance
2026-03-14 13:48:57 | [MODEL][MOVEMENT] Overwatch невозможен: недостаточно CP.
2026-03-14 13:48:57 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 13:48:57 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 13:48:57 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 13:48:57 | --- ФАЗА ЧАРДЖА ---
2026-03-14 13:48:57 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 13:48:57 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 13:48:57 | Нет доступных целей для чарджа.
2026-03-14 13:48:57 | --- ФАЗА БОЯ ---
2026-03-14 13:48:57 | --- ХОД MODEL ---
2026-03-14 13:48:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 13:48:57 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 13:48:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 13:48:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 12). Выбор: right, advance=да, бросок=2, макс=7, distance=7
2026-03-14 13:48:57 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 19)
2026-03-14 13:48:57 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-14 13:49:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 8). Выбор: right, advance=нет, distance=3
2026-03-14 13:49:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 11)
2026-03-14 13:49:00 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-14 13:49:01 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 13:49:01 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-14 13:49:01 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 13:49:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-14 13:49:01 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 13:49:01 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-14 13:49:01 | 
🎲 Бросок сейвы (save): 1D6
2026-03-14 13:49:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=13, need<=3).
2026-03-14 13:49:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-14 13:49:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-14 13:49:01 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-14 13:49:01 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 13:49:01 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:49:01 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-14 13:49:01 | Оружие: Gauss flayer
2026-03-14 13:49:01 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:49:01 | BS оружия: 4+
2026-03-14 13:49:01 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 13:49:01 | Save цели: 4+ (invul: нет)
2026-03-14 13:49:01 | Benefit of Cover: не активен.
2026-03-14 13:49:01 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 13:49:01 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 13:49:01 | Hit rolls:    [3, 2, 3, 5, 4, 1, 3, 3, 2, 6]  -> hits: 3 (crits: 1)
2026-03-14 13:49:01 | Wound rolls:  [1, 3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-14 13:49:01 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-03-14 13:49:01 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-14 13:49:01 | FX: найден итог урона = 0.0.
2026-03-14 13:49:01 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-14 13:49:01 | FX: позиция эффекта start=(204.0,612.0) end=(828.0,684.0).
2026-03-14 13:49:01 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-14 13:49:01 | 📌 -------------------------

2026-03-14 13:49:01 | --- ФАЗА ЧАРДЖА ---
2026-03-14 13:49:01 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-14 13:49:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-14 13:49:01 | [MODEL] Чардж: нет доступных целей
2026-03-14 13:49:01 | --- ФАЗА БОЯ ---
2026-03-14 13:49:01 | [MODEL] Ближний бой: нет доступных атак
2026-03-14 13:49:01 | Reward (progress к objective): d_before=22.204, d_after=17.029, delta=5.174, norm=0.862, bonus=+0.026
2026-03-14 13:49:01 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.067, delta=-0.016; cover=0.000->0.000, threat=-0.500->-0.667, guard=0.000->0.000
2026-03-14 13:49:01 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-14 13:49:01 | Reward (terrain/clamp): raw=-0.036, cap=±0.120, clamp не сработал
2026-03-14 13:49:01 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-14 13:49:01 | Итерация 0 завершена с наградой tensor([-0.0101], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-14 13:49:01 | {'model health': [10.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [10, 10], 'player alive models': [9, 10], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-14 13:49:01 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-03-14 13:49:02 | === БОЕВОЙ РАУНД 2 ===
2026-03-14 13:49:02 | --- ХОД PLAYER ---
2026-03-14 13:49:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 13:49:02 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-14 13:49:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-14 13:49:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-14 13:49:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:49:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-14 13:49:03 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 13:49:03 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 13:49:08 | Unit 11: movement stay (позиция сохранена x=37, y=31).
2026-03-14 13:49:09 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (37,31).
2026-03-14 13:49:10 | REQ: move cell accepted (RMB) x=29, y=31, mode=normal
2026-03-14 13:49:10 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-14 13:49:10 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-14 13:49:10 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-14 13:49:10 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-14 13:49:10 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-14 13:49:10 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 13:49:10 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:49:10 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-14 13:49:10 | Оружие: Gauss flayer
2026-03-14 13:49:10 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:49:10 | BS оружия: 4+
2026-03-14 13:49:10 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-14 13:49:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 13:49:10 | Save цели: 4+ (invul: нет)
2026-03-14 13:49:10 | Benefit of Cover: не активен.
2026-03-14 13:49:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 13:49:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 13:49:10 | Правило: Overwatch: попадания только на 6+
2026-03-14 13:49:10 | Hit rolls:    [1, 3, 4, 1, 1, 4, 6, 5, 5, 5, 6, 3, 5, 6, 3, 2, 3, 5, 3, 1]  -> hits: 3 (crits: 3)
2026-03-14 13:49:10 | Save rolls:   [5, 4, 4]  (цель 4+) -> failed saves: 0
2026-03-14 13:49:10 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-14 13:49:10 | FX: найден итог урона = 0.0.
2026-03-14 13:49:10 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-14 13:49:10 | FX: позиция эффекта start=(468.0,804.0) end=(828.0,684.0).
2026-03-14 13:49:10 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-14 13:49:10 | 📌 -------------------------

2026-03-14 13:49:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 13:49:10 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-14 13:49:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 31), target_filter_size=2, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-14 13:49:10 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(37, 31), full_cells=24, rapid_cells=12, вошло=1551, rapid=525, не вошло=849, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-14 13:49:18 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 13:49:18 | REQ: движок запросил кубы стрельбы (target=21, count=10, stage=hit).
2026-03-14 13:49:24 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-14 13:49:24 | REQ: движок запросил кубы стрельбы (target=21, count=4, stage=wound).
2026-03-14 13:49:27 | 
🎲 Бросок сейвы (save): 4D6
2026-03-14 13:49:27 | REQ: движок запросил кубы стрельбы (target=21, count=4, stage=save).
2026-03-14 13:49:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (overwatch)
2026-03-14 13:49:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-14 13:49:32 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 2.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:49:32 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-14 13:49:32 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 13:49:32 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:49:32 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-14 13:49:32 | Оружие: Gauss flayer
2026-03-14 13:49:32 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:49:32 | BS оружия: 4+
2026-03-14 13:49:32 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 13:49:32 | Save цели: 4+ (invul: нет)
2026-03-14 13:49:32 | Benefit of Cover: не активен.
2026-03-14 13:49:32 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 13:49:32 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 13:49:32 | Hit rolls:    [3, 4, 5, 6, 1, 2, 3, 4, 5, 6]  -> hits: 6 (crits: 2)
2026-03-14 13:49:32 | Wound rolls:  [3, 4, 5, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-14 13:49:32 | Save rolls:   [3, 4, 5, 1]  (цель 4+) -> failed saves: 2
2026-03-14 13:49:32 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-14 13:49:32 | FX: найден итог урона = 2.0.
2026-03-14 13:49:32 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=2.0).
2026-03-14 13:49:32 | FX: позиция эффекта start=(900.0,756.0) end=(468.0,804.0).
2026-03-14 13:49:32 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-14 13:49:32 | 📌 -------------------------

2026-03-14 13:49:32 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-14 13:49:32 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-14 13:49:32 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(29, 31), target_filter_size=2, max_target_dist=18, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-14 13:49:32 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(29, 31), full_cells=24, rapid_cells=12, вошло=1617, rapid=525, не вошло=783, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-14 13:49:32 | FX: перепроигрываю 30 строк(и) лога.
2026-03-14 13:49:32 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 13:49:32 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-14 13:49:32 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:49:32 | FX: найден итог урона = 0.0.
2026-03-14 13:49:32 | FX: дубликат отчёта, эффект не создаём.
2026-03-14 13:49:37 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-14 13:49:37 | REQ: движок запросил кубы стрельбы (target=21, count=20, stage=hit).
2026-03-14 13:49:38 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-14 13:49:38 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 20D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-14 13:49:38 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-14 13:49:38 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-14 13:49:39 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 13:49:39 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-03-14 13:49:44 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-14 13:49:44 | REQ: движок запросил кубы стрельбы (target=22, count=4, stage=wound).
2026-03-14 13:50:05 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-14 13:50:05 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 4D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-14 13:50:05 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на ранение (to wound)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-14 13:50:05 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-14 13:50:23 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 13:50:23 | REQ: движок запросил кубы стрельбы (target=22, count=10, stage=hit).
2026-03-14 13:50:48 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-14 13:50:48 | REQ: движок запросил кубы стрельбы (target=22, count=4, stage=wound).
2026-03-14 13:50:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-14 13:50:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-14 13:50:58 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:50:58 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-14 13:50:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 13:50:58 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-14 13:50:58 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-14 13:50:58 | Оружие: Gauss flayer
2026-03-14 13:50:58 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:50:58 | BS оружия: 4+
2026-03-14 13:50:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 13:50:58 | Save цели: 4+ (invul: нет)
2026-03-14 13:50:58 | Benefit of Cover: не активен.
2026-03-14 13:50:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 13:50:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 13:50:58 | Hit rolls:    [1, 1, 1, 1, 1, 1, 6, 6, 6, 6]  -> hits: 4 (crits: 4)
2026-03-14 13:50:58 | Save rolls:   [1, 2, 3, 4]  (цель 4+) -> failed saves: 3
2026-03-14 13:50:58 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-14 13:50:58 | FX: найден итог урона = 3.0.
2026-03-14 13:50:58 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=3.0).
2026-03-14 13:50:58 | FX: позиция эффекта start=(708.0,756.0) end=(276.0,612.0).
2026-03-14 13:50:58 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-14 13:50:58 | 📌 -------------------------

2026-03-14 13:50:58 | --- ФАЗА ЧАРДЖА ---
2026-03-14 13:50:58 | FX: перепроигрываю 30 строк(и) лога.
2026-03-14 13:50:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 13:50:58 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-14 13:50:58 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 13:50:58 | FX: найден итог урона = 2.0.
2026-03-14 13:50:58 | FX: дубликат отчёта, эффект не создаём.
2026-03-14 13:51:05 | Unit 12 — Necrons Necron Warriors (x10 моделей) решил пропустить чардж.
2026-03-14 13:51:05 | --- ФАЗА БОЯ ---
2026-03-14 13:51:05 | --- ХОД MODEL ---
2026-03-14 13:51:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 13:51:05 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-14 13:51:05 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 13:51:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 19). Выбор: right, advance=да, бросок=2, макс=7, distance=7
2026-03-14 13:51:05 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 26)
2026-03-14 13:51:05 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-14 13:51:05 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(37, 31), target_filter_size=2, max_target_dist=26, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-14 13:51:05 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(37, 31), full_cells=24, rapid_cells=12, вошло=1551, rapid=525, не вошло=849, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
