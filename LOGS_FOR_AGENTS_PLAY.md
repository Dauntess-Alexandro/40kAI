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
