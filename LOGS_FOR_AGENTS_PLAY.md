2026-03-11 18:11:53 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-11 18:11:53 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-11 18:11:53 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-11 18:11:53 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-11 18:11:54 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 18:12:03 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-411748.pickle
2026-03-11 18:12:03 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-411748.pth
2026-03-11 18:12:03 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-11 18:12:09 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-11 18:12:09 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-11 18:12:09 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-11 18:12:09 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-11 18:12:09 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-11 18:12:09 | [DEPLOY] Order: model first, alternating
2026-03-11 18:12:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 18:12:09 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=792, coord=(13,12), attempt=1, reward=+0.023, score_before=0.000, score_after=0.468, reward_delta=+0.023, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 18:12:09 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (13,12)
2026-03-11 18:12:09 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 18:12:10 | REQ: deploy cell accepted x=48, y=30
2026-03-11 18:12:10 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,48)
2026-03-11 18:12:10 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,48)
2026-03-11 18:12:10 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 18:12:10 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1332, coord=(22,12), attempt=1, reward=+0.000, score_before=0.468, score_after=0.468, reward_delta=+0.000, forward=0.207, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 18:12:10 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (22,12)
2026-03-11 18:12:10 | Ошибка деплоя: reason=outside_deploy_zone, x=45, y=21. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-11 18:12:12 | REQ: deploy cell accepted x=47, y=21
2026-03-11 18:12:13 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,47)
2026-03-11 18:12:13 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,47)
2026-03-11 18:12:13 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.023 total_deploy_reward=+0.023 avg_forward=0.207 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-11 18:12:13 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02341348048876626, 'units': 2, 'total_deploy_reward': 0.02341348048876626, 'forward_sum': 0.4135593220338983, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.20677966101694914, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-11 18:12:13 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-11 18:12:13 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-11 18:12:13 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-11 18:12:13 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 18:12:13 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-11 18:12:13 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 18:12:14 | === БОЕВОЙ РАУНД 1 ===
2026-03-11 18:12:14 | --- ХОД PLAYER ---
2026-03-11 18:12:14 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 18:12:14 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 18:12:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 18:12:15 | REQ: move cell accepted (RMB) x=37, y=31, mode=advance
2026-03-11 18:12:15 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 18:12:15 | [COVER][MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-11 18:12:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 18:12:15 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-11 18:12:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-11 18:12:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 18:12:15 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-11 18:12:15 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 18:12:15 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 18:12:15 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 18:12:15 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-11 18:12:15 | Оружие: Gauss flayer
2026-03-11 18:12:15 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 18:12:16 | BS оружия: 4+
2026-03-11 18:12:16 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 18:12:16 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 18:12:16 | Save цели: 4+ (invul: нет)
2026-03-11 18:12:16 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-11 18:12:16 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 18:12:16 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 18:12:16 | Правило: Overwatch: попадания только на 6+
2026-03-11 18:12:16 | Эффект: benefit of cover
2026-03-11 18:12:16 | Hit rolls:    [5, 4, 6, 2, 5, 4, 4, 2, 2, 2]  -> hits: 1 (crits: 1)
2026-03-11 18:12:16 | Save rolls:   [2]  (цель 3+) -> failed saves: 1
2026-03-11 18:12:16 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 18:12:16 | FX: найден итог урона = 1.0.
2026-03-11 18:12:16 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-11 18:12:16 | FX: позиция эффекта start=(300.0,540.0) end=(1164.0,732.0).
2026-03-11 18:12:16 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-11 18:12:16 | 📌 -------------------------

2026-03-11 18:12:16 | REQ: move cell accepted (RMB) x=36, y=20, mode=advance
2026-03-11 18:12:16 | [MODEL][MOVEMENT] Overwatch невозможен: недостаточно CP.
2026-03-11 18:12:16 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 18:12:16 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 18:12:16 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 18:12:16 | --- ФАЗА ЧАРДЖА ---
2026-03-11 18:12:16 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 18:12:16 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 18:12:16 | Нет доступных целей для чарджа.
2026-03-11 18:12:16 | --- ФАЗА БОЯ ---
2026-03-11 18:12:16 | --- ХОД MODEL ---
2026-03-11 18:12:16 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 18:12:16 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 18:12:16 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 18:12:16 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 12). Выбор: right, advance=нет, distance=1
2026-03-11 18:12:16 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 13)
2026-03-11 18:12:16 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 18:12:18 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 12). Выбор: right, advance=да, бросок=6, макс=11, distance=11
2026-03-11 18:12:18 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 23)
2026-03-11 18:12:18 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-11 18:12:18 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-11 18:12:18 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 18:12:18 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-11 18:12:18 | 
🎲 Бросок сейвы (save): 1D6
2026-03-11 18:12:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-11 18:12:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=9, need<=3).
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-11 18:12:18 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 18:12:18 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 18:12:18 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 18:12:18 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 18:12:18 | Оружие: Gauss flayer
2026-03-11 18:12:18 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 18:12:18 | BS оружия: 4+
2026-03-11 18:12:18 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 18:12:18 | Save цели: 4+ (invul: нет)
2026-03-11 18:12:18 | Benefit of Cover: не активен.
2026-03-11 18:12:18 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 18:12:18 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 18:12:18 | Hit rolls:    [1, 3, 2, 2, 3, 6, 2, 2, 3, 4]  -> hits: 2 (crits: 1)
2026-03-11 18:12:18 | Wound rolls:  [2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-11 18:12:18 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-03-11 18:12:18 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 18:12:18 | FX: найден итог урона = 1.0.
2026-03-11 18:12:18 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-11 18:12:18 | FX: позиция эффекта start=(300.0,324.0) end=(876.0,492.0).
2026-03-11 18:12:18 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-11 18:12:18 | 📌 -------------------------

2026-03-11 18:12:18 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 18:12:18 | Reward (шаг): стрельба delta=+0.080
2026-03-11 18:12:18 | --- ФАЗА ЧАРДЖА ---
2026-03-11 18:12:18 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 18:12:18 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 18:12:18 | [MODEL] Чардж: нет доступных целей
2026-03-11 18:12:18 | --- ФАЗА БОЯ ---
2026-03-11 18:12:18 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 18:12:18 | Reward (progress к objective): d_before=18.111, d_after=7.280, delta=10.831, norm=1.805, bonus=+0.054
2026-03-11 18:12:18 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-11 18:12:18 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-11 18:12:18 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-11 18:12:18 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-11 18:12:18 | Итерация 0 завершена с наградой tensor([0.1148], device='cuda:0'), здоровье игрока [9.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-11 18:12:18 | {'model health': [10.0, 10.0], 'player health': [9.0, 9.0], 'model alive models': [10, 10], 'player alive models': [9, 9], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 18:12:18 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 9.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-11 18:12:19 | === БОЕВОЙ РАУНД 2 ===
2026-03-11 18:12:19 | --- ХОД PLAYER ---
2026-03-11 18:12:19 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 18:12:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 18:12:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 18:12:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 18:12:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 18:12:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 18:12:23 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 18:12:25 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 18:12:25 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 18:12:25 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 18:12:25 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 18:12:25 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 18:12:25 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 18:12:28 | Unit 11: movement stay (позиция сохранена x=37, y=31).
2026-03-11 18:12:29 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (37,31).
2026-03-11 18:12:30 | Unit 12: movement stay (позиция сохранена x=36, y=20).
2026-03-11 18:12:30 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (36,20).
2026-03-11 18:12:30 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 18:12:30 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-11 18:12:38 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:20:18 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-11 19:20:18 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-11 19:20:18 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-11 19:20:18 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-11 19:20:19 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 19:20:29 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-411748.pickle
2026-03-11 19:20:29 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-411748.pth
2026-03-11 19:20:29 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-11 19:20:32 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-03-11 19:20:32 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-11 19:20:32 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-11 19:20:32 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-11 19:20:32 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-11 19:20:32 | [DEPLOY] Order: model first, alternating
2026-03-11 19:20:32 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 19:20:32 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1924, coord=(32,4), attempt=1, reward=+0.020, score_before=0.000, score_after=0.405, reward_delta=+0.020, forward=0.071, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 19:20:32 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,4)
2026-03-11 19:20:32 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 19:20:33 | REQ: deploy cell accepted x=50, y=30
2026-03-11 19:20:33 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,50)
2026-03-11 19:20:33 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,50)
2026-03-11 19:20:33 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 19:20:33 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=241, coord=(4,1), attempt=1, reward=-0.003, score_before=0.405, score_after=0.347, reward_delta=-0.003, forward=0.046, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 19:20:33 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (4,1)
2026-03-11 19:20:33 | REQ: deploy cell accepted x=48, y=23
2026-03-11 19:20:34 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-11 19:20:34 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,48)
2026-03-11 19:20:34 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.058 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-11 19:20:34 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.0173433188805676, 'units': 2, 'total_deploy_reward': 0.0173433188805676, 'forward_sum': 0.11694915254237288, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.05847457627118644, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-11 19:20:34 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-11 19:20:34 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-11 19:20:34 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-11 19:20:34 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 19:20:34 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-11 19:20:34 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 19:20:35 | === БОЕВОЙ РАУНД 1 ===
2026-03-11 19:20:35 | --- ХОД PLAYER ---
2026-03-11 19:20:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:35 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:35 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:36 | REQ: move cell accepted (RMB) x=39, y=28, mode=advance
2026-03-11 19:20:36 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:36 | REQ: move cell accepted (RMB) x=38, y=25, mode=advance
2026-03-11 19:20:37 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:37 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:37 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:37 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:37 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:37 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:37 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:37 | Нет доступных целей для чарджа.
2026-03-11 19:20:37 | --- ФАЗА БОЯ ---
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | --- ХОД MODEL ---
2026-03-11 19:20:37 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:37 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:37 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (32, 4). Выбор: up, advance=да, бросок=5, макс=10, distance=10
2026-03-11 19:20:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (22, 4)
2026-03-11 19:20:37 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (4, 1). Выбор: up, advance=нет, distance=2
2026-03-11 19:20:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (2, 1)
2026-03-11 19:20:37 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:37 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=34.00, range=24.00, delta=+10.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-11 19:20:37 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:37 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 19:20:37 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 19:20:37 | [MODEL] Чардж: нет доступных целей
2026-03-11 19:20:37 | --- ФАЗА БОЯ ---
2026-03-11 19:20:37 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 19:20:37 | Reward (progress к objective): d_before=28.636, d_after=26.077, delta=2.559, norm=0.426, bonus=+0.013
2026-03-11 19:20:37 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-11 19:20:37 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-11 19:20:37 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-11 19:20:37 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-11 19:20:37 | Итерация 0 завершена с наградой tensor([0.0128], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-11 19:20:37 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 19:20:37 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-11 19:20:40 | === БОЕВОЙ РАУНД 2 ===
2026-03-11 19:20:40 | --- ХОД PLAYER ---
2026-03-11 19:20:40 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:40 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:40 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:41 | REQ: move cell accepted (RMB) x=28, y=29, mode=advance
2026-03-11 19:20:42 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:42 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 19:20:42 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 19:20:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-11 19:20:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-11 19:20:42 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 19:20:42 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:20:42 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:20:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:42 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 19:20:42 | Оружие: Gauss flayer
2026-03-11 19:20:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:42 | BS оружия: 4+
2026-03-11 19:20:42 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:20:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:42 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:42 | Benefit of Cover: не активен.
2026-03-11 19:20:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:42 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:20:42 | Hit rolls:    [1, 6, 1, 5, 2, 6, 5, 1, 3, 1]  -> hits: 2 (crits: 2)
2026-03-11 19:20:42 | Save rolls:   [2, 2]  (цель 4+) -> failed saves: 2
2026-03-11 19:20:42 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 19:20:42 | FX: найден итог урона = 2.0.
2026-03-11 19:20:42 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-11 19:20:42 | FX: позиция эффекта start=(108.0,540.0) end=(948.0,684.0).
2026-03-11 19:20:42 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 19:20:42 | 📌 -------------------------

2026-03-11 19:20:43 | REQ: move cell accepted (RMB) x=27, y=26, mode=advance
2026-03-11 19:20:43 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:43 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 19:20:43 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-11 19:20:43 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:20:43 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:20:43 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:43 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 19:20:43 | Оружие: Gauss flayer
2026-03-11 19:20:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:43 | BS оружия: 4+
2026-03-11 19:20:43 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:20:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:43 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:43 | Benefit of Cover: не активен.
2026-03-11 19:20:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:43 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:20:43 | Hit rolls:    [5, 2, 2, 1, 4, 2, 4, 4, 1, 2]  -> hits: 0
2026-03-11 19:20:43 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 19:20:43 | FX: найден итог урона = 0.0.
2026-03-11 19:20:43 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-11 19:20:43 | FX: позиция эффекта start=(108.0,540.0) end=(924.0,612.0).
2026-03-11 19:20:43 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-11 19:20:43 | 📌 -------------------------

2026-03-11 19:20:43 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:43 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:43 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:43 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:43 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:43 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:43 | Нет доступных целей для чарджа.
2026-03-11 19:20:43 | --- ФАЗА БОЯ ---
2026-03-11 19:20:43 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:43 | --- ХОД MODEL ---
2026-03-11 19:20:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:43 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:43 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (22, 4). Выбор: up, advance=нет, distance=3
2026-03-11 19:20:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 4)
2026-03-11 19:20:43 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (2, 1). Выбор: up, advance=нет, distance=2
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 1)
2026-03-11 19:20:45 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-11 19:20:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 19:20:45 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-11 19:20:45 | 
🎲 Бросок сейвы (save): 1D6
2026-03-11 19:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=18, need<=3).
2026-03-11 19:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-11 19:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-11 19:20:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 19:20:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 19:20:45 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:45 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 19:20:45 | Оружие: Gauss flayer
2026-03-11 19:20:45 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:45 | BS оружия: 4+
2026-03-11 19:20:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:45 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:45 | Benefit of Cover: не активен.
2026-03-11 19:20:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:45 | Hit rolls:    [3, 4, 1, 2, 4, 5, 3, 4, 4, 5]  -> hits: 6
2026-03-11 19:20:45 | Wound rolls:  [3, 2, 4, 3, 2, 3]  (цель 4+) -> wounds: 1
2026-03-11 19:20:45 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-03-11 19:20:45 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 19:20:45 | FX: найден итог урона = 0.0.
2026-03-11 19:20:45 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-11 19:20:45 | FX: позиция эффекта start=(108.0,540.0) end=(684.0,708.0).
2026-03-11 19:20:45 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 19:20:45 | 📌 -------------------------

2026-03-11 19:20:45 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-11 19:20:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 19:20:45 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-11 19:20:45 | 
🎲 Бросок сейвы (save): 3D6
2026-03-11 19:20:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (shooting)
2026-03-11 19:20:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-11 19:20:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 19:20:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 19:20:45 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:45 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-11 19:20:45 | Оружие: Gauss flayer
2026-03-11 19:20:45 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:45 | BS оружия: 4+
2026-03-11 19:20:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:45 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:45 | Benefit of Cover: не активен.
2026-03-11 19:20:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:45 | Hit rolls:    [4, 4, 6, 3, 3, 5, 4, 5, 1, 1]  -> hits: 6 (crits: 1)
2026-03-11 19:20:45 | Wound rolls:  [3, 2, 2, 4, 6]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-11 19:20:45 | Save rolls:   [2, 4, 6]  (цель 4+) -> failed saves: 1
2026-03-11 19:20:45 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 19:20:45 | FX: найден итог урона = 1.0.
2026-03-11 19:20:45 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-11 19:20:45 | FX: позиция эффекта start=(36.0,60.0) end=(660.0,636.0).
2026-03-11 19:20:45 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-11 19:20:45 | 📌 -------------------------

2026-03-11 19:20:45 | Reward (шаг): стрельба delta=+0.080
2026-03-11 19:20:45 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 19:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 19:20:45 | [MODEL] Чардж: нет доступных целей
2026-03-11 19:20:45 | --- ФАЗА БОЯ ---
2026-03-11 19:20:45 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 19:20:45 | Reward (progress к objective): d_before=26.077, d_after=26.019, delta=0.058, norm=0.010, bonus=+0.000
2026-03-11 19:20:45 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.050, delta=+0.001; cover=0.000->0.000, threat=-0.500->-0.500, guard=0.000->0.000
2026-03-11 19:20:45 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-11 19:20:45 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-11 19:20:45 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-11 19:20:45 | Итерация 1 завершена с наградой tensor([0.0608], device='cuda:0'), здоровье игрока [8.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-11 19:20:45 | {'model health': [10.0, 10.0], 'player health': [8.0, 9.0], 'model alive models': [10, 10], 'player alive models': [8, 9], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 19:20:45 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 9.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-11 19:20:46 | === БОЕВОЙ РАУНД 3 ===
2026-03-11 19:20:46 | --- ХОД PLAYER ---
2026-03-11 19:20:46 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 19:20:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 19:20:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-11 19:20:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 19:20:47 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 19:20:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-11 19:20:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 19:20:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 19:20:49 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:49 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:49 | REQ: move cell accepted (RMB) x=17, y=26, mode=advance
2026-03-11 19:20:50 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:50 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:20:50 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 19:20:50 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-11 19:20:50 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:20:50 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:20:50 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:50 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 19:20:50 | Оружие: Gauss flayer
2026-03-11 19:20:50 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:50 | BS оружия: 4+
2026-03-11 19:20:50 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:20:50 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:50 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:50 | Benefit of Cover: не активен.
2026-03-11 19:20:50 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:50 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:50 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:20:50 | Hit rolls:    [1, 1, 1, 5, 2, 5, 4, 4, 6, 3, 4, 1, 6, 3, 4, 3, 6, 1, 5, 3]  -> hits: 3 (crits: 3)
2026-03-11 19:20:50 | Save rolls:   [4, 5, 5]  (цель 4+) -> failed saves: 0
2026-03-11 19:20:50 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 19:20:50 | FX: найден итог урона = 0.0.
2026-03-11 19:20:50 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-11 19:20:50 | FX: позиция эффекта start=(108.0,468.0) end=(684.0,708.0).
2026-03-11 19:20:50 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 19:20:50 | 📌 -------------------------

2026-03-11 19:20:51 | REQ: move cell accepted (RMB) x=17, y=22, mode=advance
2026-03-11 19:20:51 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:51 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:20:51 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 19:20:51 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-11 19:20:51 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-11 19:20:51 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 19:20:51 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:20:51 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:20:51 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:51 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 19:20:51 | Оружие: Gauss flayer
2026-03-11 19:20:51 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:51 | BS оружия: 4+
2026-03-11 19:20:51 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:20:51 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:51 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:51 | Benefit of Cover: не активен.
2026-03-11 19:20:51 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:51 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:51 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:20:51 | Hit rolls:    [6, 6, 3, 1, 6, 4, 3, 5, 5, 5, 3, 4, 5, 4, 2, 1, 4, 4, 3, 5]  -> hits: 3 (crits: 3)
2026-03-11 19:20:51 | Save rolls:   [5, 1, 1]  (цель 4+) -> failed saves: 2
2026-03-11 19:20:51 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 19:20:51 | FX: найден итог урона = 2.0.
2026-03-11 19:20:51 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-11 19:20:51 | FX: позиция эффекта start=(108.0,468.0) end=(660.0,636.0).
2026-03-11 19:20:51 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-11 19:20:51 | 📌 -------------------------

2026-03-11 19:20:51 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:51 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:51 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 19:20:51 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:51 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:51 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 19:20:51 | Нет доступных целей для чарджа.
2026-03-11 19:20:51 | --- ФАЗА БОЯ ---
2026-03-11 19:20:51 | --- ХОД MODEL ---
2026-03-11 19:20:51 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:51 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:51 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:20:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 4). Выбор: left, advance=нет, distance=3
2026-03-11 19:20:51 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 1)
2026-03-11 19:20:51 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 1). Выбор: left, advance=нет, distance=1
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (1, 0)
2026-03-11 19:20:53 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 19:20:53 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-11 19:20:53 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:20:53 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-11 19:20:53 | 
🎲 Бросок сейвы (save): 6D6
2026-03-11 19:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 6. HP: 9.0 -> 6.0 (shooting)
2026-03-11 19:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-11 19:20:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 19:20:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 19:20:53 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:53 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 19:20:53 | Оружие: Gauss flayer
2026-03-11 19:20:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:53 | BS оружия: 4+
2026-03-11 19:20:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:53 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:53 | Benefit of Cover: не активен.
2026-03-11 19:20:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:53 | Hit rolls:    [6, 6, 3, 3, 3, 6, 6, 5, 1, 6, 5, 1, 2, 3, 1, 4, 2, 1, 4, 2]  -> hits: 9 (crits: 5)
2026-03-11 19:20:53 | Wound rolls:  [1, 1, 3, 5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 5 = 6
2026-03-11 19:20:53 | Save rolls:   [5, 5, 3, 2, 4, 3]  (цель 4+) -> failed saves: 3
2026-03-11 19:20:53 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-11 19:20:53 | FX: найден итог урона = 3.0.
2026-03-11 19:20:53 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=3.0).
2026-03-11 19:20:53 | FX: позиция эффекта start=(108.0,468.0) end=(420.0,636.0).
2026-03-11 19:20:53 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 19:20:53 | 📌 -------------------------

2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-11 19:20:53 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 19:20:53 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 19:20:53 | 
🎲 Бросок сейвы (save): 1D6
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-11 19:20:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 19:20:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 19:20:53 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:20:53 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-11 19:20:53 | Оружие: Gauss flayer
2026-03-11 19:20:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:20:53 | BS оружия: 4+
2026-03-11 19:20:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:20:53 | Save цели: 4+ (invul: нет)
2026-03-11 19:20:53 | Benefit of Cover: не активен.
2026-03-11 19:20:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:20:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:20:53 | Hit rolls:    [5, 2, 3, 1, 2, 1, 1, 2, 6, 5]  -> hits: 3 (crits: 1)
2026-03-11 19:20:53 | Wound rolls:  [2, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-11 19:20:53 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-03-11 19:20:53 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 19:20:53 | FX: найден итог урона = 0.0.
2026-03-11 19:20:53 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-11 19:20:53 | FX: позиция эффекта start=(36.0,36.0) end=(420.0,636.0).
2026-03-11 19:20:53 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-11 19:20:53 | 📌 -------------------------

2026-03-11 19:20:53 | Reward (шаг): стрельба delta=+0.140
2026-03-11 19:20:53 | --- ФАЗА ЧАРДЖА ---
2026-03-11 19:20:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 19:20:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 19:20:53 | [MODEL] Чардж: нет доступных целей
2026-03-11 19:20:53 | --- ФАЗА БОЯ ---
2026-03-11 19:20:53 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 19:20:53 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-11 19:20:53 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-11 19:20:53 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-11 19:20:53 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-11 19:20:53 | Итерация 2 завершена с наградой tensor([0.1207], device='cuda:0'), здоровье игрока [6.0, 8.0], здоровье модели [10.0, 10.0]
2026-03-11 19:20:53 | {'model health': [10.0, 10.0], 'player health': [6.0, 8.0], 'model alive models': [10, 10], 'player alive models': [6, 8], 'modelCP': 2, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 19:20:53 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [6.0, 8.0]
CP MODEL: 2, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-03-11 19:20:53 | === БОЕВОЙ РАУНД 4 ===
2026-03-11 19:20:53 | --- ХОД PLAYER ---
2026-03-11 19:20:53 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 19:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:55 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 19:20:55 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 19:20:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-11 19:20:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-11 19:20:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 19:20:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 19:20:58 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 19:20:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 19:21:00 | REQ: move cell accepted (RMB) x=12, y=21, mode=normal
2026-03-11 19:21:00 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:21:00 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:21:00 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 19:21:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (Overwatch)
2026-03-11 19:21:00 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-11 19:21:00 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 19:21:00 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:21:00 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:21:00 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:21:00 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 19:21:00 | Оружие: Gauss flayer
2026-03-11 19:21:00 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:21:00 | BS оружия: 4+
2026-03-11 19:21:00 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:21:00 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:21:00 | Save цели: 4+ (invul: нет)
2026-03-11 19:21:00 | Benefit of Cover: не активен.
2026-03-11 19:21:00 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:21:00 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:21:00 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:21:00 | Hit rolls:    [4, 1, 5, 6, 1, 3, 6, 1, 5, 1, 4, 3, 2, 3, 1, 4, 3, 1, 2, 2]  -> hits: 2 (crits: 2)
2026-03-11 19:21:00 | Save rolls:   [1, 1]  (цель 4+) -> failed saves: 2
2026-03-11 19:21:00 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 19:21:00 | FX: найден итог урона = 2.0.
2026-03-11 19:21:00 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 19:21:00 | 📌 -------------------------

2026-03-11 19:21:01 | REQ: move cell accepted (RMB) x=12, y=17, mode=normal
2026-03-11 19:21:01 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 19:21:01 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 19:21:01 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 19:21:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-11 19:21:01 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-11 19:21:01 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 19:21:01 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 19:21:01 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 19:21:01 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 19:21:01 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 19:21:01 | Оружие: Gauss flayer
2026-03-11 19:21:01 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 19:21:01 | BS оружия: 4+
2026-03-11 19:21:01 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 19:21:01 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 19:21:01 | Save цели: 4+ (invul: нет)
2026-03-11 19:21:01 | Benefit of Cover: не активен.
2026-03-11 19:21:01 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 19:21:01 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 19:21:01 | Правило: Overwatch: попадания только на 6+
2026-03-11 19:21:01 | Hit rolls:    [2, 2, 5, 3, 5, 2, 1, 6, 4, 3, 6, 3, 5, 6, 2, 2, 5, 4, 4, 3]  -> hits: 3 (crits: 3)
2026-03-11 19:21:01 | Save rolls:   [5, 1, 2]  (цель 4+) -> failed saves: 2
2026-03-11 19:21:01 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 19:21:01 | FX: найден итог урона = 2.0.
2026-03-11 19:21:01 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 19:21:01 | 📌 -------------------------

2026-03-11 19:21:01 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 19:21:01 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-11 19:21:13 | 
🎲 Бросок на попадание (to hit): 14D6
2026-03-11 19:21:13 | REQ: движок запросил кубы стрельбы (target=21, count=14).
2026-03-11 19:21:14 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:15 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:16 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:16 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:24 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:25 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:26 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:29 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:34 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:35 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:35 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:36 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:37 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:37 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:37 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:40 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:41 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:41 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:46 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:58 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:21:59 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:59 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:21:59 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
2026-03-11 19:22:13 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:22:16 | REQ: Cancel во время бросков. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: движок ожидает кубы для Unit 21. Что делать дальше: завершите текущий бросок; смена цели станет доступна в новом запросе выбора цели.
2026-03-11 19:22:16 | REQ: цель Unit 22 отклонена. Где: viewer/app.py (_open_shoot_popover). Что случилось: на шаге кубов цель уже зафиксирована как Unit 21. Что делать дальше: завершите текущий выстрел или нажмите Cancel и выберите цель заново.
