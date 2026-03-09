2026-03-09 12:02:30 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-09 12:02:30 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-09 12:02:30 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-09 12:02:30 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-09 12:02:31 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 12:02:40 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-16-154396.pickle
2026-03-09 12:02:40 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-16-154396.pth
2026-03-09 12:02:40 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-09 12:02:44 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-03-09 12:02:44 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-09 12:02:44 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-09 12:02:44 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-09 12:02:44 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-09 12:02:44 | [DEPLOY] Order: model first, alternating
2026-03-09 12:02:44 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 12:02:44 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1869, coord=(31,9), attempt=1, reward=+0.022, score_before=0.000, score_after=0.445, reward_delta=+0.022, forward=0.156, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 12:02:44 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (31,9)
2026-03-09 12:02:44 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-09 12:02:45 | REQ: deploy cell accepted x=49, y=31
2026-03-09 12:02:45 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,49)
2026-03-09 12:02:45 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (31,49)
2026-03-09 12:02:45 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-09 12:02:45 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2281, coord=(38,1), attempt=1, reward=-0.004, score_before=0.445, score_after=0.367, reward_delta=-0.004, forward=0.088, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-09 12:02:45 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (38,1)
2026-03-09 12:02:45 | REQ: deploy cell accepted x=48, y=22
2026-03-09 12:02:46 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,48)
2026-03-09 12:02:46 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (22,48)
2026-03-09 12:02:46 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.018 total_deploy_reward=+0.018 avg_forward=0.122 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-09 12:02:46 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.018328734726054396, 'units': 2, 'total_deploy_reward': 0.018328734726054396, 'forward_sum': 0.24406779661016947, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.12203389830508474, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-09 12:02:46 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-09 12:02:46 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-09 12:02:46 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-09 12:02:46 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 12:02:46 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-09 12:02:46 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 12:02:47 | === БОЕВОЙ РАУНД 1 ===
2026-03-09 12:02:47 | --- ХОД PLAYER ---
2026-03-09 12:02:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:02:47 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 12:02:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:02:49 | REQ: move cell accepted (RMB) x=38, y=29, mode=advance
2026-03-09 12:02:49 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:02:49 | REQ: move cell accepted (RMB) x=38, y=20, mode=advance
2026-03-09 12:02:50 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:02:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:02:50 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 12:02:50 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-09 12:02:50 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:02:50 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 12:02:50 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-09 12:02:50 | Нет доступных целей для чарджа.
2026-03-09 12:02:50 | --- ФАЗА БОЯ ---
2026-03-09 12:02:50 | --- ХОД MODEL ---
2026-03-09 12:02:50 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:02:50 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 12:02:50 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:02:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (31, 9). Выбор: up, advance=да, бросок=1, макс=6, distance=6
2026-03-09 12:02:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 9)
2026-03-09 12:02:50 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:02:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 1). Выбор: up, advance=нет, distance=3
2026-03-09 12:02:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (35, 1)
2026-03-09 12:02:50 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:02:50 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:02:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-09 12:02:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 12:02:50 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:02:50 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-09 12:02:50 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 12:02:50 | [MODEL] Чардж: нет доступных целей
2026-03-09 12:02:50 | --- ФАЗА БОЯ ---
2026-03-09 12:02:50 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 12:02:50 | Reward (progress к objective): d_before=23.707, d_after=21.587, delta=2.120, norm=0.353, bonus=+0.011
2026-03-09 12:02:50 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-09 12:02:50 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 12:02:50 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-09 12:02:50 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-09 12:02:50 | Итерация 0 завершена с наградой tensor([0.0106], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-09 12:02:50 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 12:02:50 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-09 12:02:52 | === БОЕВОЙ РАУНД 2 ===
2026-03-09 12:02:52 | --- ХОД PLAYER ---
2026-03-09 12:02:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:02:52 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-09 12:02:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:02:53 | REQ: move cell accepted (RMB) x=36, y=30, mode=normal
2026-03-09 12:02:53 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:02:55 | REQ: move cell accepted (RMB) x=34, y=20, mode=normal
2026-03-09 12:02:55 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:02:55 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:02:55 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 12:02:55 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 12:02:55 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 12:02:55 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:02:55 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:02:55 | Оружие: Gauss flayer
2026-03-09 12:02:55 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:02:55 | BS оружия: 4+
2026-03-09 12:02:55 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:02:55 | Save цели: 4+ (invul: нет)
2026-03-09 12:02:55 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:02:55 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:02:55 | Правило: Overwatch: попадания только на 6+
2026-03-09 12:02:55 | Hit rolls:    [5, 3, 2, 1, 2, 1, 3, 5, 2, 5]  -> hits: 3
2026-03-09 12:02:55 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:02:55 | FX: найден итог урона = 0.0.
2026-03-09 12:02:55 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-09 12:02:55 | FX: позиция эффекта start=(228.0,612.0) end=(924.0,492.0).
2026-03-09 12:02:55 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 12:02:55 | 📌 -------------------------

2026-03-09 12:02:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:02:55 | REQ: валидные цели стрельбы для Unit 12: [21]
2026-03-09 12:03:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:03:22 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 12:03:24 | 
🎲 Бросок сейвы (save): 8D6
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 5. HP: 10.0 -> 5.0 (overwatch)
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-09 12:03:29 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 5.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:03:29 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:03:29 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:03:29 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:03:29 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-09 12:03:29 | Оружие: Gauss flayer
2026-03-09 12:03:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:03:29 | BS оружия: 4+
2026-03-09 12:03:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:03:29 | Save цели: 4+ (invul: нет)
2026-03-09 12:03:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:03:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:03:29 | Hit rolls:    [2, 3, 4, 5, 6, 6, 5, 6, 6, 6]  -> hits: 8 (crits: 5)
2026-03-09 12:03:29 | Wound rolls:  [4, 5, 5]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 5 = 8
2026-03-09 12:03:29 | Save rolls:   [2, 3, 4, 5, 6, 1, 2, 3]  (цель 4+) -> failed saves: 5
2026-03-09 12:03:29 | 
✅ Итог по движку: прошло урона = 5.0
2026-03-09 12:03:29 | FX: найден итог урона = 5.0.
2026-03-09 12:03:29 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=5.0).
2026-03-09 12:03:29 | FX: позиция эффекта start=(828.0,492.0) end=(228.0,612.0).
2026-03-09 12:03:29 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-03-09 12:03:29 | 📌 -------------------------

2026-03-09 12:03:29 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:03:29 | Нет доступных целей для чарджа.
2026-03-09 12:03:29 | --- ФАЗА БОЯ ---
2026-03-09 12:03:29 | --- ХОД MODEL ---
2026-03-09 12:03:29 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-09 12:03:29 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 12:03:29 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 9). Выбор: up, advance=да, бросок=6, макс=11, distance=11
2026-03-09 12:03:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 9)
2026-03-09 12:03:29 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:03:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 1). Выбор: up, advance=да, бросок=3, макс=8, distance=8
2026-03-09 12:03:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (27, 1)
2026-03-09 12:03:32 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:03:32 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:03:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-09 12:03:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-09 12:03:32 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:03:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-09 12:03:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-09 12:03:32 | [MODEL] Чардж: нет доступных целей
2026-03-09 12:03:32 | --- ФАЗА БОЯ ---
2026-03-09 12:03:32 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 12:03:32 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=21.587033144922902->21.840329667841555
2026-03-09 12:03:32 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-09 12:03:32 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 12:03:32 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-09 12:03:32 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-09 12:03:32 | Итерация 1 завершена с наградой tensor([-0.0298], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [6.0, 10.0]
2026-03-09 12:03:32 | {'model health': [6.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [6, 10], 'player alive models': [10, 10], 'modelCP': 3, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 12:03:32 | Здоровье MODEL: [6.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 3, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-09 12:03:32 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 12:03:32 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:03:32 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-09 12:03:32 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:03:32 | FX: найден итог урона = 5.0.
2026-03-09 12:03:32 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 12:03:34 | === БОЕВОЙ РАУНД 3 ===
2026-03-09 12:03:34 | --- ХОД PLAYER ---
2026-03-09 12:03:34 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:03:34 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 12:03:34 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:03:37 | REQ: move cell accepted (RMB) x=32, y=31, mode=normal
2026-03-09 12:03:37 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:03:39 | Unit 12: movement skipped (позиция сохранена x=34, y=20).
2026-03-09 12:03:39 | Unit 12 — Necrons Necron Warriors (x10 моделей): клетка (34,20) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-09 12:03:48 | Unit 12: movement skipped (позиция сохранена x=34, y=20).
2026-03-09 12:03:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): клетка (34,20) недостижима. Что делать дальше: выберите подсвеченную reachable-клетку.
2026-03-09 12:03:55 | REQ: move cell accepted (RMB) x=32, y=21, mode=normal
2026-03-09 12:03:55 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:03:55 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-09 12:03:55 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 12:03:55 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 12:03:55 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 12:03:55 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:03:55 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:03:55 | Оружие: Gauss flayer
2026-03-09 12:03:55 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:03:55 | BS оружия: 4+
2026-03-09 12:03:55 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:03:55 | Save цели: 4+ (invul: нет)
2026-03-09 12:03:55 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:03:55 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:03:55 | Правило: Overwatch: попадания только на 6+
2026-03-09 12:03:55 | Hit rolls:    [3, 4, 5, 1, 5, 5]  -> hits: 4
2026-03-09 12:03:55 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:03:55 | FX: найден итог урона = 0.0.
2026-03-09 12:03:55 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 12:03:55 | 📌 -------------------------

2026-03-09 12:03:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:03:55 | REQ: валидные цели стрельбы для Unit 12: [21]
2026-03-09 12:04:06 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:04:11 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:04:11 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:04:11 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:04:11 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:04:11 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-09 12:04:11 | Оружие: Gauss flayer
2026-03-09 12:04:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:04:11 | BS оружия: 4+
2026-03-09 12:04:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:04:11 | Save цели: 4+ (invul: нет)
2026-03-09 12:04:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:04:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:04:11 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 12:04:11 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:04:11 | FX: найден итог урона = 0.0.
2026-03-09 12:04:11 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=0.0).
2026-03-09 12:04:11 | FX: позиция эффекта start=(780.0,516.0) end=(228.0,348.0).
2026-03-09 12:04:11 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-03-09 12:04:11 | 📌 -------------------------

2026-03-09 12:04:11 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:04:11 | Нет доступных целей для чарджа.
2026-03-09 12:04:11 | --- ФАЗА БОЯ ---
2026-03-09 12:04:11 | --- ХОД MODEL ---
2026-03-09 12:04:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 12:04:11 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 12:04:11 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 9). Выбор: left, advance=нет, distance=3
2026-03-09 12:04:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 6)
2026-03-09 12:04:11 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:04:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 1). Выбор: left, advance=нет, distance=1
2026-03-09 12:04:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (27, 0)
2026-03-09 12:04:12 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-09 12:04:12 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 12:04:12 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 12:04:12 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 12:04:12 | 
🎲 Бросок сейвы (save): 3D6
2026-03-09 12:04:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-09 12:04:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.050 (dealt=1.00)
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=16, need<=3).
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.050, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.200
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-09 12:04:12 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:04:12 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:04:12 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:04:12 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:04:12 | Оружие: Gauss flayer
2026-03-09 12:04:12 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:04:12 | BS оружия: 4+
2026-03-09 12:04:12 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:04:12 | Save цели: 4+ (invul: нет)
2026-03-09 12:04:12 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:04:12 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:04:12 | Hit rolls:    [1, 2, 3, 4, 4, 2, 6, 2, 6]  -> hits: 4 (crits: 2)
2026-03-09 12:04:12 | Wound rolls:  [4, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-09 12:04:12 | Save rolls:   [5, 4, 2]  (цель 4+) -> failed saves: 1
2026-03-09 12:04:12 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-09 12:04:12 | FX: найден итог урона = 1.0.
2026-03-09 12:04:12 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-09 12:04:12 | FX: позиция эффекта start=(228.0,348.0) end=(780.0,516.0).
2026-03-09 12:04:12 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 12:04:12 | 📌 -------------------------

2026-03-09 12:04:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-09 12:04:12 | Reward (шаг): стрельба delta=+0.200
2026-03-09 12:04:12 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:04:12 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 12:04:12 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 12:04:12 | [MODEL] Чардж: нет доступных целей
2026-03-09 12:04:12 | --- ФАЗА БОЯ ---
2026-03-09 12:04:12 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 12:04:12 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 12:04:12 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=+0.000, delta=+0.017; cover=0.000->0.000, threat=-0.167->-0.000, guard=0.000->0.000
2026-03-09 12:04:12 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-09 12:04:12 | Reward (terrain/clamp): raw=+0.017, cap=±0.120, clamp не сработал
2026-03-09 12:04:12 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-09 12:04:12 | Итерация 2 завершена с наградой tensor([0.1667], device='cuda:0'), здоровье игрока [10.0, 9.0], здоровье модели [9.0, 10.0]
2026-03-09 12:04:12 | {'model health': [9.0, 10.0], 'player health': [10.0, 9.0], 'model alive models': [9, 10], 'player alive models': [10, 9], 'modelCP': 4, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 12:04:12 | Здоровье MODEL: [9.0, 10.0], здоровье PLAYER: [10.0, 9.0]
CP MODEL: 4, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 1
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-09 12:04:13 | === БОЕВОЙ РАУНД 4 ===
2026-03-09 12:04:13 | --- ХОД PLAYER ---
2026-03-09 12:04:13 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:04:13 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 12:04:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 12:04:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 12:04:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:04:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 12:04:14 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 1 -> 2, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 12:04:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:04:16 | REQ: move cell accepted (RMB) x=27, y=31, mode=normal
2026-03-09 12:04:16 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:04:16 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:04:16 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-09 12:04:16 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-09 12:04:16 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 12:04:16 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-09 12:04:16 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 12:04:16 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 12:04:16 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:04:16 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 12:04:16 | Оружие: Gauss flayer
2026-03-09 12:04:16 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:04:16 | BS оружия: 4+
2026-03-09 12:04:16 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:04:16 | Save цели: 4+ (invul: нет)
2026-03-09 12:04:16 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:04:16 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:04:16 | Правило: Overwatch: попадания только на 6+
2026-03-09 12:04:16 | Hit rolls:    [4, 5, 3, 6, 1, 3, 2, 6, 5, 6]  -> hits: 6 (crits: 3)
2026-03-09 12:04:16 | Wound rolls:  [3, 3, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-09 12:04:16 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 12:04:16 | FX: найден итог урона = 2.0.
2026-03-09 12:04:16 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-09 12:04:16 | FX: позиция эффекта start=(36.0,636.0) end=(756.0,732.0).
2026-03-09 12:04:16 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 12:04:16 | 📌 -------------------------

2026-03-09 12:04:27 | REQ: move cell accepted (RMB) x=30, y=21, mode=normal
2026-03-09 12:04:28 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:04:28 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-09 12:04:28 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-09 12:04:28 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-09 12:04:28 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-09 12:04:28 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 12:04:28 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:04:28 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:04:28 | Оружие: Gauss flayer
2026-03-09 12:04:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:04:28 | BS оружия: 4+
2026-03-09 12:04:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:04:28 | Save цели: 4+ (invul: нет)
2026-03-09 12:04:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:04:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:04:28 | Правило: Overwatch: попадания только на 6+
2026-03-09 12:04:28 | Hit rolls:    [5, 1, 5, 1, 5, 3, 6, 5, 2]  -> hits: 5 (crits: 1)
2026-03-09 12:04:28 | Wound rolls:  [4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 12:04:28 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:04:28 | FX: найден итог урона = 0.0.
2026-03-09 12:04:28 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 12:04:28 | 📌 -------------------------

2026-03-09 12:04:28 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:04:28 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-09 12:04:28 | REQ: валидные цели стрельбы для Unit 11: [22]
2026-03-09 12:04:36 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:37 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:40 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:40 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:40 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:44 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:44 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:45 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:45 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:46 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:46 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:47 | Выбрано на карте: unit_id=21, name=Necron Warriors
2026-03-09 12:04:47 | REQ: цель Unit 21 отклонена. Где: viewer/app.py (_on_target_selected). Что дальше: выберите цель из [22]
2026-03-09 12:04:52 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:52 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:54 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:57 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:04:57 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:05:00 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:05:00 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:05:01 | REQ: ПКМ по Unit 21 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [22]
2026-03-09 12:05:13 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-09 12:05:16 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:16 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:05:16 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:05:16 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:16 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-09 12:05:16 | Оружие: Gauss flayer
2026-03-09 12:05:16 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:05:16 | BS оружия: 4+
2026-03-09 12:05:16 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:05:16 | Save цели: 4+ (invul: нет)
2026-03-09 12:05:16 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:05:16 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:05:16 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 12:05:16 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:05:16 | FX: найден итог урона = 0.0.
2026-03-09 12:05:16 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-09 12:05:16 | FX: позиция эффекта start=(660.0,756.0) end=(36.0,636.0).
2026-03-09 12:05:16 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-09 12:05:16 | 📌 -------------------------

2026-03-09 12:05:16 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-09 12:05:16 | REQ: валидные цели стрельбы для Unit 12: [21]
2026-03-09 12:05:16 | FX: перепроигрываю 30 строк(и) лога.
2026-03-09 12:05:16 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-09 12:05:16 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:05:16 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:05:16 | FX: найден итог урона = 0.0.
2026-03-09 12:05:16 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 12:05:18 | REQ: ПКМ по Unit 22 отклонён. Где: viewer/app.py (_on_unit_right_clicked). Что дальше: выберите цель из [21]
2026-03-09 12:05:32 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:05:36 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:36 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:05:36 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:05:36 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:36 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-09 12:05:36 | Оружие: Gauss flayer
2026-03-09 12:05:36 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:05:36 | BS оружия: 4+
2026-03-09 12:05:36 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:05:36 | Save цели: 4+ (invul: нет)
2026-03-09 12:05:36 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:05:36 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:05:36 | Hit rolls:    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  -> hits: 0
2026-03-09 12:05:36 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:05:36 | FX: найден итог урона = 0.0.
2026-03-09 12:05:36 | FX: дубликат отчёта, эффект не создаём.
2026-03-09 12:05:36 | 📌 -------------------------

2026-03-09 12:05:36 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:05:36 | Нет доступных целей для чарджа.
2026-03-09 12:05:36 | --- ФАЗА БОЯ ---
2026-03-09 12:05:36 | --- ХОД MODEL ---
2026-03-09 12:05:36 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-09 12:05:36 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-09 12:05:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 6). Выбор: left, advance=нет, distance=3
2026-03-09 12:05:36 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 3)
2026-03-09 12:05:36 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (26, 1). Выбор: left, advance=нет, distance=1
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (26, 0)
2026-03-09 12:05:38 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-09 12:05:38 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 12:05:38 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:05:38 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-09 12:05:38 | 
🎲 Бросок сейвы (save): 5D6
2026-03-09 12:05:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-03-09 12:05:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.280
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-09 12:05:38 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:05:38 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:05:38 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:38 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-09 12:05:38 | Оружие: Gauss flayer
2026-03-09 12:05:38 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:05:38 | BS оружия: 4+
2026-03-09 12:05:38 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:05:38 | Save цели: 4+ (invul: нет)
2026-03-09 12:05:38 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:05:38 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:05:38 | Hit rolls:    [5, 4, 6, 6, 6, 1, 1, 5, 1, 5]  -> hits: 7 (crits: 3)
2026-03-09 12:05:38 | Wound rolls:  [3, 3, 5, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 3 = 5
2026-03-09 12:05:38 | Save rolls:   [6, 6, 1, 6, 3]  (цель 4+) -> failed saves: 2
2026-03-09 12:05:38 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-09 12:05:38 | FX: найден итог урона = 2.0.
2026-03-09 12:05:38 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-09 12:05:38 | FX: позиция эффекта start=(156.0,348.0) end=(732.0,516.0).
2026-03-09 12:05:38 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-09 12:05:38 | 📌 -------------------------

2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-09 12:05:38 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-09 12:05:38 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-09 12:05:38 | 
🎲 Бросок сейвы (save): 2D6
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-09 12:05:38 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-09 12:05:38 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-09 12:05:38 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-09 12:05:38 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-09 12:05:38 | Оружие: Gauss flayer
2026-03-09 12:05:38 | FX: найдена строка оружия: Gauss flayer.
2026-03-09 12:05:38 | BS оружия: 4+
2026-03-09 12:05:38 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-09 12:05:38 | Save цели: 4+ (invul: нет)
2026-03-09 12:05:38 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-09 12:05:38 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-09 12:05:38 | Hit rolls:    [4, 2, 3, 2, 3, 1, 4, 2, 2, 6]  -> hits: 3 (crits: 1)
2026-03-09 12:05:38 | Wound rolls:  [6, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-09 12:05:38 | Save rolls:   [4, 4]  (цель 4+) -> failed saves: 0
2026-03-09 12:05:38 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-09 12:05:38 | FX: найден итог урона = 0.0.
2026-03-09 12:05:38 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-09 12:05:38 | FX: позиция эффекта start=(36.0,636.0) end=(660.0,756.0).
2026-03-09 12:05:38 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-09 12:05:38 | 📌 -------------------------

2026-03-09 12:05:38 | Reward (шаг): стрельба delta=+0.280
2026-03-09 12:05:38 | --- ФАЗА ЧАРДЖА ---
2026-03-09 12:05:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 12:05:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-09 12:05:38 | [MODEL] Чардж: нет доступных целей
2026-03-09 12:05:38 | --- ФАЗА БОЯ ---
2026-03-09 12:05:38 | [MODEL] Ближний бой: нет доступных атак
2026-03-09 12:05:38 | Reward (VP diff): prev=-1, curr=-2, delta=-1, reward=+0.000, penalty=-0.050
2026-03-09 12:05:38 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=-0.017, delta=+0.017; cover=0.000->0.000, threat=-0.333->-0.167, guard=0.000->0.000
2026-03-09 12:05:38 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-09 12:05:38 | Reward (terrain/clamp): raw=+0.007, cap=±0.120, clamp не сработал
2026-03-09 12:05:38 | === КОНЕЦ БОЕВОГО РАУНДА 4 ===
2026-03-09 12:05:38 | Итерация 3 завершена с наградой tensor([0.2368], device='cuda:0'), здоровье игрока [8.0, 8.0], здоровье модели [10.0, 10.0]
2026-03-09 12:05:38 | {'model health': [10.0, 10.0], 'player health': [8.0, 8.0], 'model alive models': [10, 10], 'player alive models': [8, 8], 'modelCP': 4, 'playerCP': 8, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 2, 'mission': 'Only War', 'turn': 5, 'battle round': 5, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-09 12:05:38 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 8.0]
CP MODEL: 4, CP PLAYER: 8
VP MODEL: 0, VP PLAYER: 2
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

