2026-03-10 16:09:22 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-10 16:09:22 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-10 16:09:22 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-10 16:09:22 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-10 16:09:23 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 16:09:34 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-23-167082.pickle
2026-03-10 16:09:34 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-23-167082.pth
2026-03-10 16:09:34 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-10 16:09:39 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-10 16:09:39 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-10 16:09:39 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-10 16:09:39 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-10 16:09:39 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-10 16:09:39 | [DEPLOY] Order: model first, alternating
2026-03-10 16:09:39 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 16:09:39 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1810, coord=(30,10), attempt=1, reward=+0.023, score_before=0.000, score_after=0.453, reward_delta=+0.023, forward=0.173, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 16:09:39 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (30,10)
2026-03-10 16:09:39 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 16:09:40 | Ошибка деплоя: нужно ввести X и Y. Где: viewer/app.py (_submit_text). Что делать дальше: кликните клетку на поле или введите два числа.
2026-03-10 16:09:41 | Ошибка деплоя: нужно ввести X и Y. Где: viewer/app.py (_submit_text). Что делать дальше: кликните клетку на поле или введите два числа.
2026-03-10 16:09:42 | REQ: deploy cell accepted x=47, y=28
2026-03-10 16:09:42 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,47)
2026-03-10 16:09:42 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,47)
2026-03-10 16:09:42 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 16:09:42 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=187, coord=(3,7), attempt=1, reward=-0.001, score_before=0.453, score_after=0.441, reward_delta=-0.001, forward=0.147, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 16:09:42 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (3,7)
2026-03-10 16:09:42 | REQ: deploy cell accepted x=50, y=21
2026-03-10 16:09:44 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,50)
2026-03-10 16:09:44 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (21,50)
2026-03-10 16:09:44 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.160 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-10 16:09:44 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02203389830508475, 'units': 2, 'total_deploy_reward': 0.02203389830508475, 'forward_sum': 0.32033898305084746, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.16016949152542373, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-10 16:09:44 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-10 16:09:44 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-10 16:09:44 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-10 16:09:44 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 16:09:44 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-10 16:09:44 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 16:09:44 | === БОЕВОЙ РАУНД 1 ===
2026-03-10 16:09:44 | --- ХОД PLAYER ---
2026-03-10 16:09:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 16:09:44 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 16:09:44 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 16:09:45 | REQ: move cell accepted (RMB) x=36, y=31, mode=advance
2026-03-10 16:09:46 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 16:09:46 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-10 16:09:46 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 16:09:46 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 16:09:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 16:09:46 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 16:09:46 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 16:09:46 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 16:09:46 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 16:09:46 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:09:46 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 16:09:46 | Оружие: Gauss flayer
2026-03-10 16:09:46 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:09:46 | BS оружия: 4+
2026-03-10 16:09:46 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:09:46 | Save цели: 4+ (invul: нет)
2026-03-10 16:09:46 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-10 16:09:46 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:09:46 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:09:46 | Правило: Overwatch: попадания только на 6+
2026-03-10 16:09:46 | Эффект: benefit of cover
2026-03-10 16:09:46 | Hit rolls:    [2, 1, 3, 6, 1, 3, 3, 1, 3, 6]  -> hits: 2 (crits: 2)
2026-03-10 16:09:46 | Wound rolls:  [6, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 16:09:46 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 16:09:46 | FX: найден итог урона = 1.0.
2026-03-10 16:09:46 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 16:09:46 | FX: позиция эффекта start=(252.0,732.0) end=(1140.0,684.0).
2026-03-10 16:09:46 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 16:09:46 | 📌 -------------------------

2026-03-10 16:09:47 | REQ: move cell accepted (RMB) x=39, y=11, mode=advance
2026-03-10 16:09:47 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 16:09:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 16:09:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 16:09:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 16:09:47 | --- ФАЗА ЧАРДЖА ---
2026-03-10 16:09:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 16:09:47 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 16:09:47 | Нет доступных целей для чарджа.
2026-03-10 16:09:47 | --- ФАЗА БОЯ ---
2026-03-10 16:09:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:09:47 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:09:47 | --- ХОД MODEL ---
2026-03-10 16:09:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 16:09:47 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 16:09:47 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 16:09:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 10). Выбор: right, advance=нет, distance=4
2026-03-10 16:09:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 14)
2026-03-10 16:09:47 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-10 16:09:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (3, 7). Выбор: right, advance=да, бросок=6, макс=11, distance=11
2026-03-10 16:09:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (3, 18)
2026-03-10 16:09:49 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 16:09:49 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 16:09:49 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:09:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 16:09:49 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-10 16:09:49 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 16:09:49 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 16:09:49 | 
🎲 Бросок сейвы (save): 2D6
2026-03-10 16:09:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=11, need<=3).
2026-03-10 16:09:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-10 16:09:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-10 16:09:49 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 16:09:49 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 16:09:49 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:09:49 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 16:09:49 | Оружие: Gauss flayer
2026-03-10 16:09:49 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:09:49 | BS оружия: 4+
2026-03-10 16:09:49 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:09:49 | Save цели: 4+ (invul: нет)
2026-03-10 16:09:49 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-10 16:09:49 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:09:49 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:09:49 | Эффект: benefit of cover
2026-03-10 16:09:49 | Hit rolls:    [3, 3, 6, 4, 1, 1, 6, 1, 1, 4]  -> hits: 4 (crits: 2)
2026-03-10 16:09:49 | Wound rolls:  [3, 1]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-10 16:09:49 | Save rolls:   [4, 4]  (цель 3+) -> failed saves: 0
2026-03-10 16:09:49 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 16:09:49 | FX: найден итог урона = 0.0.
2026-03-10 16:09:49 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-10 16:09:49 | FX: позиция эффекта start=(252.0,732.0) end=(876.0,756.0).
2026-03-10 16:09:49 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 16:09:49 | 📌 -------------------------

2026-03-10 16:09:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-10 16:09:49 | --- ФАЗА ЧАРДЖА ---
2026-03-10 16:09:49 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 16:09:49 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-10 16:09:49 | [MODEL] Чардж: нет доступных целей
2026-03-10 16:09:49 | --- ФАЗА БОЯ ---
2026-03-10 16:09:49 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 16:09:49 | Reward (progress к objective): d_before=22.361, d_after=18.868, delta=3.493, norm=0.582, bonus=+0.017
2026-03-10 16:09:49 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.050, delta=-0.033; cover=0.000->0.000, threat=-0.167->-0.500, guard=0.000->0.000
2026-03-10 16:09:49 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-10 16:09:49 | Reward (terrain/clamp): raw=-0.053, cap=±0.120, clamp не сработал
2026-03-10 16:09:49 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-10 16:09:49 | Итерация 0 завершена с наградой tensor([-0.0354], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 16:09:49 | {'model health': [10.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [10, 10], 'player alive models': [9, 10], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 16:09:49 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

2026-03-10 16:12:24 | === БОЕВОЙ РАУНД 2 ===
2026-03-10 16:12:24 | --- ХОД PLAYER ---
2026-03-10 16:12:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 16:12:24 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 16:12:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 2
2026-03-10 16:12:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 16:12:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 16:12:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 16:12:42 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 16:12:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 16:12:50 | Unit 11: movement stay (позиция сохранена x=36, y=31).
2026-03-10 16:12:50 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (36,31).
2026-03-10 16:12:58 | Unit 12: movement stay (позиция сохранена x=39, y=11).
2026-03-10 16:12:59 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (39,11).
2026-03-10 16:12:59 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 16:12:59 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:12:59 | REQ: валидные цели стрельбы для Unit 11: [21] | отфильтрованы: [22: цель вне дальности: range 26.00 > 24.00 (out_of_range by +2.00)]
2026-03-10 16:16:57 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 16:17:04 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-10 16:17:07 | 
🎲 Бросок сейвы (save): 4D6
2026-03-10 16:17:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-10 16:17:09 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-10 16:17:09 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:17:09 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 16:17:09 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 16:17:09 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:17:09 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-10 16:17:09 | Оружие: Gauss flayer
2026-03-10 16:17:09 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:17:09 | BS оружия: 4+
2026-03-10 16:17:09 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:17:09 | Save цели: 4+ (invul: нет)
2026-03-10 16:17:09 | Benefit of Cover: не активен.
2026-03-10 16:17:09 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:17:09 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:17:09 | Hit rolls:    [3, 4, 5, 6, 4, 5, 6, 5, 4, 3]  -> hits: 8 (crits: 2)
2026-03-10 16:17:09 | Wound rolls:  [3, 4, 5, 1, 2, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-10 16:17:09 | Save rolls:   [2, 3, 1, 4]  (цель 4+) -> failed saves: 3
2026-03-10 16:17:09 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-10 16:17:09 | FX: найден итог урона = 3.0.
2026-03-10 16:17:09 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=3.0).
2026-03-10 16:17:09 | FX: позиция эффекта start=(876.0,756.0) end=(348.0,732.0).
2026-03-10 16:17:09 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-10 16:17:09 | 📌 -------------------------

2026-03-10 16:17:09 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-10 16:17:09 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-10 16:17:09 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 16:17:21 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 16:17:54 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-10 16:17:56 | 
🎲 Бросок сейвы (save): 3D6
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 6. HP: 7.0 -> 6.0 (overwatch)
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-10 16:18:22 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:18:22 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 16:18:22 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 16:18:22 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:18:22 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-10 16:18:22 | Оружие: Gauss flayer
2026-03-10 16:18:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:18:22 | BS оружия: 4+
2026-03-10 16:18:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:18:22 | Save цели: 4+ (invul: нет)
2026-03-10 16:18:22 | Benefit of Cover: не активен.
2026-03-10 16:18:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:18:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:18:22 | Hit rolls:    [3, 4, 5, 6, 1, 1, 2, 3, 4, 5]  -> hits: 5 (crits: 1)
2026-03-10 16:18:22 | Wound rolls:  [3, 1, 4, 5]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-10 16:18:22 | Save rolls:   [3, 4, 5]  (цель 4+) -> failed saves: 1
2026-03-10 16:18:22 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 16:18:22 | FX: найден итог урона = 1.0.
2026-03-10 16:18:22 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=1.0).
2026-03-10 16:18:22 | FX: позиция эффекта start=(948.0,276.0) end=(348.0,732.0).
2026-03-10 16:18:22 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-03-10 16:18:22 | 📌 -------------------------

2026-03-10 16:18:22 | --- ФАЗА ЧАРДЖА ---
2026-03-10 16:18:22 | Нет доступных целей для чарджа.
2026-03-10 16:18:22 | --- ФАЗА БОЯ ---
2026-03-10 16:18:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:18:22 | --- ХОД MODEL ---
2026-03-10 16:18:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 2
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-10 16:18:22 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 16:18:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (30, 14). Выбор: right, advance=нет, distance=1
2026-03-10 16:18:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (30, 15)
2026-03-10 16:18:22 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-10 16:18:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (3, 18). Выбор: right, advance=нет, distance=1
2026-03-10 16:18:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (3, 19)
2026-03-10 16:18:30 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-10 16:18:31 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 16:18:31 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-10 16:18:31 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-10 16:18:31 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-10 16:18:31 | 
🎲 Бросок сейвы (save): 4D6
2026-03-10 16:18:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-03-10 16:18:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=10, need<=3).
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-10 16:18:31 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 16:18:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 16:18:31 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:18:31 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 16:18:31 | Оружие: Gauss flayer
2026-03-10 16:18:31 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:18:31 | BS оружия: 4+
2026-03-10 16:18:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:18:31 | Save цели: 4+ (invul: нет)
2026-03-10 16:18:31 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-10 16:18:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:18:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:18:31 | Эффект: benefit of cover
2026-03-10 16:18:31 | Hit rolls:    [4, 5, 6, 6, 2, 1, 5, 1]  -> hits: 5 (crits: 2)
2026-03-10 16:18:31 | Wound rolls:  [4, 4, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-10 16:18:31 | Save rolls:   [2, 6, 1, 4]  (цель 3+) -> failed saves: 2
2026-03-10 16:18:31 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-10 16:18:31 | FX: найден итог урона = 2.0.
2026-03-10 16:18:31 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-10 16:18:31 | FX: позиция эффекта start=(348.0,732.0) end=(876.0,756.0).
2026-03-10 16:18:31 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 16:18:31 | 📌 -------------------------

2026-03-10 16:18:31 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 16:18:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 16:18:31 | [COVER][SHOOTING] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-10 16:18:31 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 16:18:31 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 16:18:31 | 
🎲 Бросок сейвы (save): 3D6
2026-03-10 16:18:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=7, need<=3).
2026-03-10 16:18:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-10 16:18:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-10 16:18:31 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 16:18:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 16:18:31 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 16:18:31 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 16:18:31 | Оружие: Gauss flayer
2026-03-10 16:18:31 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 16:18:31 | BS оружия: 4+
2026-03-10 16:18:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 16:18:31 | Save цели: 4+ (invul: нет)
2026-03-10 16:18:31 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-10 16:18:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 16:18:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 16:18:31 | Эффект: benefit of cover
2026-03-10 16:18:31 | Hit rolls:    [3, 1, 3, 6, 5, 2, 3, 6, 2, 2]  -> hits: 3 (crits: 2)
2026-03-10 16:18:31 | Wound rolls:  [5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-10 16:18:31 | Save rolls:   [3, 5, 3]  (цель 3+) -> failed saves: 0
2026-03-10 16:18:31 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 16:18:31 | FX: найден итог урона = 0.0.
2026-03-10 16:18:31 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-10 16:18:31 | FX: позиция эффекта start=(444.0,84.0) end=(948.0,276.0).
2026-03-10 16:18:31 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-10 16:18:31 | 📌 -------------------------

2026-03-10 16:18:31 | Reward (шаг): стрельба delta=+0.110
2026-03-10 16:18:31 | --- ФАЗА ЧАРДЖА ---
2026-03-10 16:18:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 16:18:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 16:18:31 | [MODEL] Чардж: нет доступных целей
2026-03-10 16:18:31 | --- ФАЗА БОЯ ---
2026-03-10 16:18:31 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 16:18:31 | Reward (progress к objective): d_before=18.868, d_after=18.028, delta=0.840, norm=0.140, bonus=+0.004
2026-03-10 16:18:31 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.050, delta=+0.001; cover=0.000->0.000, threat=-0.500->-0.500, guard=0.000->0.000
2026-03-10 16:18:31 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-10 16:18:31 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-10 16:18:31 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-10 16:18:31 | Итерация 1 завершена с наградой tensor([0.0947], device='cuda:0'), здоровье игрока [8.0, 10.0], здоровье модели [8.0, 10.0]
2026-03-10 16:18:31 | {'model health': [8.0, 10.0], 'player health': [8.0, 10.0], 'model alive models': [8, 10], 'player alive models': [8, 10], 'modelCP': 3, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 16:18:31 | Здоровье MODEL: [8.0, 10.0], здоровье PLAYER: [8.0, 10.0]
CP MODEL: 3, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)

