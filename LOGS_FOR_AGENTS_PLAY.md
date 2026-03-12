2026-03-12 10:56:05 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-12 10:56:05 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-12 10:56:05 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-12 10:56:05 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-12 10:56:06 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 10:56:11 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-22-323300.pickle
2026-03-12 10:56:11 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-22-323300.pth
2026-03-12 10:56:11 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-12 10:56:18 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-12 10:56:18 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-12 10:56:18 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-12 10:56:18 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-12 10:56:18 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-12 10:56:18 | [DEPLOY] Order: model first, alternating
2026-03-12 10:56:18 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 10:56:18 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=782, coord=(13,2), attempt=1, reward=+0.017, score_before=0.000, score_after=0.343, reward_delta=+0.017, forward=0.037, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 10:56:18 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (13,2)
2026-03-12 10:56:18 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 10:56:18 | REQ: deploy cell accepted x=52, y=29
2026-03-12 10:56:18 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,52)
2026-03-12 10:56:18 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (29,52)
2026-03-12 10:56:18 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 10:56:18 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1566, coord=(26,6), attempt=1, reward=+0.002, score_before=0.343, score_after=0.382, reward_delta=+0.002, forward=0.071, spread=1.000, edge=0.750, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 10:56:18 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (26,6)
2026-03-12 10:56:19 | REQ: deploy cell accepted x=51, y=19
2026-03-12 10:56:20 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,51)
2026-03-12 10:56:20 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,51)
2026-03-12 10:56:20 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.054 avg_spread=1.000 avg_edge=0.625 avg_cover=0.000
2026-03-12 10:56:20 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.019097359085534095, 'units': 2, 'total_deploy_reward': 0.019097359085534095, 'forward_sum': 0.10847457627118645, 'spread_sum': 2.0, 'edge_sum': 1.25, 'cover_sum': 0.0, 'avg_forward': 0.054237288135593226, 'avg_spread': 1.0, 'avg_edge': 0.625, 'avg_cover': 0.0}
2026-03-12 10:56:20 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-12 10:56:20 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-12 10:56:20 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-12 10:56:20 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:56:20 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-12 10:56:20 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 10:56:21 | === БОЕВОЙ РАУНД 1 ===
2026-03-12 10:56:21 | --- ХОД PLAYER ---
2026-03-12 10:56:21 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:21 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:22 | REQ: move cell accepted (RMB) x=41, y=27, mode=advance
2026-03-12 10:56:22 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:56:23 | REQ: move cell accepted (RMB) x=40, y=11, mode=advance
2026-03-12 10:56:24 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:56:24 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:24 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:24 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:24 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:24 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:24 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:24 | Нет доступных целей для чарджа.
2026-03-12 10:56:24 | --- ФАЗА БОЯ ---
2026-03-12 10:56:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:24 | --- ХОД MODEL ---
2026-03-12 10:56:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:24 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:24 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 2). Выбор: down, advance=нет, distance=1
2026-03-12 10:56:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 2)
2026-03-12 10:56:24 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:56:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (26, 6). Выбор: down, advance=да, бросок=5, макс=10, distance=10
2026-03-12 10:56:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (36, 6)
2026-03-12 10:56:24 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:56:24 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:24 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=35.00, range=24.00, delta=+11.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-12 10:56:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-12 10:56:24 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:24 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:56:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-12 10:56:24 | [MODEL] Чардж: нет доступных целей
2026-03-12 10:56:24 | --- ФАЗА БОЯ ---
2026-03-12 10:56:24 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:56:24 | Reward (idle вне цели): penalty=-0.020, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=24.73863375370596->28.635642126552707
2026-03-12 10:56:24 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-12 10:56:24 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-12 10:56:24 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-12 10:56:24 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-12 10:56:24 | Итерация 0 завершена с наградой tensor([-0.0200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 10:56:24 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:56:24 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-12 10:56:25 | === БОЕВОЙ РАУНД 2 ===
2026-03-12 10:56:25 | --- ХОД PLAYER ---
2026-03-12 10:56:25 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:25 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:25 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:27 | REQ: move cell accepted (RMB) x=30, y=30, mode=advance
2026-03-12 10:56:28 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:28 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:28 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 10:56:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-12 10:56:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-12 10:56:28 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 10:56:28 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:56:28 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:56:28 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:28 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 10:56:28 | Оружие: Gauss flayer
2026-03-12 10:56:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:28 | BS оружия: 4+
2026-03-12 10:56:28 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:56:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:28 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:28 | Benefit of Cover: не активен.
2026-03-12 10:56:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:28 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:56:28 | Hit rolls:    [6, 4, 6, 6, 4, 4, 6, 2, 1, 5]  -> hits: 4 (crits: 4)
2026-03-12 10:56:28 | Save rolls:   [4, 5, 6, 2]  (цель 4+) -> failed saves: 1
2026-03-12 10:56:28 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 10:56:28 | FX: найден итог урона = 1.0.
2026-03-12 10:56:28 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 10:56:28 | FX: позиция эффекта start=(156.0,876.0) end=(996.0,660.0).
2026-03-12 10:56:28 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 10:56:28 | 📌 -------------------------

2026-03-12 10:56:29 | REQ: move cell accepted (RMB) x=29, y=22, mode=advance
2026-03-12 10:56:29 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:29 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:29 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 10:56:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 6. HP: 10.0 -> 6.0 (Overwatch)
2026-03-12 10:56:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-12 10:56:29 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 4.0.
2026-03-12 10:56:29 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:56:29 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:56:29 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:29 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-12 10:56:29 | Оружие: Gauss flayer
2026-03-12 10:56:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:29 | BS оружия: 4+
2026-03-12 10:56:29 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:56:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:29 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:29 | Benefit of Cover: не активен.
2026-03-12 10:56:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:29 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:56:29 | Hit rolls:    [1, 1, 4, 2, 6, 2, 6, 6, 3, 6]  -> hits: 4 (crits: 4)
2026-03-12 10:56:29 | Save rolls:   [2, 2, 2, 3]  (цель 4+) -> failed saves: 4
2026-03-12 10:56:29 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-12 10:56:29 | FX: найден итог урона = 4.0.
2026-03-12 10:56:29 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=4.0).
2026-03-12 10:56:29 | FX: позиция эффекта start=(156.0,876.0) end=(972.0,276.0).
2026-03-12 10:56:29 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-12 10:56:29 | 📌 -------------------------

2026-03-12 10:56:29 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:29 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:29 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:29 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:29 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:29 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:29 | Нет доступных целей для чарджа.
2026-03-12 10:56:29 | --- ФАЗА БОЯ ---
2026-03-12 10:56:29 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:29 | --- ХОД MODEL ---
2026-03-12 10:56:29 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:29 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-12 10:56:29 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (14, 2). Выбор: left, advance=нет, distance=2
2026-03-12 10:56:29 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (14, 0)
2026-03-12 10:56:29 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:56:29 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (36, 6). Выбор: left, advance=да, бросок=1, макс=6, distance=6
2026-03-12 10:56:29 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (36, 0)
2026-03-12 10:56:29 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:30 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:30 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-12 10:56:30 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:30 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-12 10:56:30 | 
🎲 Бросок сейвы (save): 6D6
2026-03-12 10:56:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 4. HP: 6.0 -> 4.0 (shooting)
2026-03-12 10:56:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.120
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба/у цели): damage_bonus=+0.100 (dealt=2.00)
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.120, obj_damage=0.100, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.280
2026-03-12 10:56:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 10:56:30 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:56:30 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:56:30 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:30 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 10:56:30 | Оружие: Gauss flayer
2026-03-12 10:56:30 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:30 | BS оружия: 4+
2026-03-12 10:56:30 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:30 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:31 | Benefit of Cover: не активен.
2026-03-12 10:56:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:31 | Hit rolls:    [3, 6, 6, 6, 6, 5, 4, 3, 5, 1]  -> hits: 7 (crits: 4)
2026-03-12 10:56:31 | Wound rolls:  [4, 3, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 4 = 6
2026-03-12 10:56:31 | Save rolls:   [6, 4, 5, 6, 2, 3]  (цель 4+) -> failed saves: 2
2026-03-12 10:56:31 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 10:56:31 | FX: найден итог урона = 2.0.
2026-03-12 10:56:31 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-12 10:56:31 | FX: позиция эффекта start=(60.0,348.0) end=(708.0,540.0).
2026-03-12 10:56:31 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 10:56:31 | 📌 -------------------------

2026-03-12 10:56:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-12 10:56:31 | Reward (шаг): стрельба delta=+0.280
2026-03-12 10:56:31 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:56:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-12 10:56:31 | [MODEL] Чардж: нет доступных целей
2026-03-12 10:56:31 | --- ФАЗА БОЯ ---
2026-03-12 10:56:31 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:56:31 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=+0.000, delta=+0.050; cover=0.000->0.000, threat=-0.500->-0.000, guard=0.000->0.000
2026-03-12 10:56:31 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-12 10:56:31 | Reward (terrain/clamp): raw=+0.050, cap=±0.120, clamp не сработал
2026-03-12 10:56:31 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-12 10:56:31 | Итерация 1 завершена с наградой tensor([0.3300], device='cuda:0'), здоровье игрока [9.0, 4.0], здоровье модели [10.0, 10.0]
2026-03-12 10:56:31 | {'model health': [10.0, 10.0], 'player health': [9.0, 4.0], 'model alive models': [10, 10], 'player alive models': [9, 4], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:56:31 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [9.0, 4.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-12 10:56:31 | === БОЕВОЙ РАУНД 3 ===
2026-03-12 10:56:31 | --- ХОД PLAYER ---
2026-03-12 10:56:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:31 | Unit 12 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-12 10:56:31 | Бросок 2D6...
2026-03-12 10:56:33 | Бросок: 1 1
2026-03-12 10:56:33 | Unit 12 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-12 10:56:34 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:56:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:56:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-12 10:56:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-12 10:56:36 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=4, раны=[1, 1, 1, 1] всего=4
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:38 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-12 10:56:38 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:38 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:40 | REQ: move cell accepted (RMB) x=19, y=35, mode=advance
2026-03-12 10:56:40 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:40 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:40 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 10:56:40 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-12 10:56:40 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-12 10:56:40 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 10:56:40 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:56:40 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:56:40 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:40 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 10:56:40 | Оружие: Gauss flayer
2026-03-12 10:56:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:40 | BS оружия: 4+
2026-03-12 10:56:40 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:56:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:40 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:40 | Benefit of Cover: не активен.
2026-03-12 10:56:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:40 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:56:40 | Hit rolls:    [5, 4, 5, 2, 3, 4, 1, 6, 6, 3]  -> hits: 2 (crits: 2)
2026-03-12 10:56:40 | Save rolls:   [1, 6]  (цель 4+) -> failed saves: 1
2026-03-12 10:56:40 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 10:56:40 | FX: найден итог урона = 1.0.
2026-03-12 10:56:40 | FX: дубликат отчёта, эффект не создаём.
2026-03-12 10:56:40 | 📌 -------------------------

2026-03-12 10:56:41 | REQ: move cell accepted (RMB) x=18, y=33, mode=advance
2026-03-12 10:56:41 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:41 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:41 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 10:56:41 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:56:41 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:56:41 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:41 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 10:56:41 | Оружие: Gauss flayer
2026-03-12 10:56:41 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:41 | BS оружия: 4+
2026-03-12 10:56:41 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:56:41 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:41 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:41 | Benefit of Cover: не активен.
2026-03-12 10:56:41 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:41 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:41 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:56:41 | Hit rolls:    [3, 4, 4, 5, 5, 2, 1, 3, 1, 2]  -> hits: 0
2026-03-12 10:56:41 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 10:56:41 | FX: найден итог урона = 0.0.
2026-03-12 10:56:41 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-12 10:56:41 | FX: позиция эффекта start=(36.0,324.0) end=(708.0,540.0).
2026-03-12 10:56:41 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 10:56:41 | 📌 -------------------------

2026-03-12 10:56:41 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:41 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:41 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:56:41 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:41 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:41 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:56:41 | Нет доступных целей для чарджа.
2026-03-12 10:56:41 | --- ФАЗА БОЯ ---
2026-03-12 10:56:41 | --- ХОД MODEL ---
2026-03-12 10:56:41 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:41 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:41 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 1). Выбор: left, advance=нет, distance=1
2026-03-12 10:56:41 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 0)
2026-03-12 10:56:41 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 1). Выбор: left, advance=нет, distance=1
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (35, 0)
2026-03-12 10:56:43 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:56:43 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: выбор политики)
2026-03-12 10:56:43 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:43 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-12 10:56:43 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 10:56:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (shooting)
2026-03-12 10:56:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 10:56:43 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:56:43 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:56:43 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:43 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:56:43 | Оружие: Gauss flayer
2026-03-12 10:56:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:43 | BS оружия: 4+
2026-03-12 10:56:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:43 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:43 | Benefit of Cover: не активен.
2026-03-12 10:56:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:43 | Hit rolls:    [4, 4, 4, 1, 6, 5, 3, 3, 4, 1]  -> hits: 6 (crits: 1)
2026-03-12 10:56:43 | Wound rolls:  [4, 6, 4, 3, 1]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-12 10:56:43 | Save rolls:   [1, 2, 5, 6]  (цель 4+) -> failed saves: 2
2026-03-12 10:56:43 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 10:56:43 | FX: найден итог урона = 2.0.
2026-03-12 10:56:43 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 10:56:43 | FX: позиция эффекта start=(36.0,324.0) end=(468.0,852.0).
2026-03-12 10:56:43 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 10:56:43 | 📌 -------------------------

2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 10:56:43 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:56:43 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 10:56:43 | 
🎲 Бросок сейвы (save): 5D6
2026-03-12 10:56:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 5. Осталось: 2. HP: 7.0 -> 2.0 (shooting)
2026-03-12 10:56:43 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 2. Причина: потери моделей.
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.150 (norm=0.250, dealt=5.00)
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=22, need<=3).
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.150 (norm=0.250, dealt=5.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.200
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 5.0
2026-03-12 10:56:43 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:56:43 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:56:43 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:56:43 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 10:56:43 | Оружие: Gauss flayer
2026-03-12 10:56:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:56:43 | BS оружия: 4+
2026-03-12 10:56:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:56:43 | Save цели: 4+ (invul: нет)
2026-03-12 10:56:43 | Benefit of Cover: не активен.
2026-03-12 10:56:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:56:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:56:43 | Hit rolls:    [6, 5, 4, 6, 3, 6, 2, 3, 1, 6]  -> hits: 6 (crits: 4)
2026-03-12 10:56:43 | Wound rolls:  [5, 3]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 4 = 5
2026-03-12 10:56:43 | Save rolls:   [2, 1, 2, 1, 2]  (цель 4+) -> failed saves: 5
2026-03-12 10:56:43 | 
✅ Итог по движку: прошло урона = 5.0
2026-03-12 10:56:43 | FX: найден итог урона = 5.0.
2026-03-12 10:56:43 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=5.0).
2026-03-12 10:56:43 | FX: позиция эффекта start=(36.0,852.0) end=(468.0,852.0).
2026-03-12 10:56:43 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 10:56:43 | 📌 -------------------------

2026-03-12 10:56:43 | Reward (шаг): стрельба delta=+0.310
2026-03-12 10:56:43 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:56:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:56:43 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:56:43 | [MODEL] Чардж: нет доступных целей
2026-03-12 10:56:43 | --- ФАЗА БОЯ ---
2026-03-12 10:56:43 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:56:43 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-12 10:56:43 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-12 10:56:43 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 10:56:43 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-12 10:56:43 | Итерация 2 завершена с наградой tensor([0.2907], device='cuda:0'), здоровье игрока [2.0, 7.0], здоровье модели [10.0, 10.0]
2026-03-12 10:56:43 | {'model health': [10.0, 10.0], 'player health': [2.0, 7.0], 'model alive models': [10, 10], 'player alive models': [2, 7], 'modelCP': 2, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:56:43 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [2.0, 7.0]
CP MODEL: 2, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 5.0 раз(а)

2026-03-12 10:56:44 | === БОЕВОЙ РАУНД 4 ===
2026-03-12 10:56:44 | --- ХОД PLAYER ---
2026-03-12 10:56:44 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:56:44 | Unit 11 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-12 10:56:44 | Бросок 2D6...
2026-03-12 10:56:46 | Бросок: 1 1
2026-03-12 10:56:46 | Unit 11 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-12 10:56:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=2, раны=[1, 1] всего=2
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:48 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-12 10:56:48 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:56:49 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-12 10:56:49 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:56:49 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:56:52 | Unit 11: movement stay (позиция сохранена x=19, y=35).
2026-03-12 10:56:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (19,35).
2026-03-12 10:56:53 | Unit 12: movement stay (позиция сохранена x=17, y=32).
2026-03-12 10:56:53 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (17,32).
2026-03-12 10:56:53 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:56:53 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:57:05 | 
🎲 Бросок на попадание (to hit): 5D6
2026-03-12 10:57:05 | REQ: движок запросил кубы стрельбы (target=22, count=5).
2026-03-12 10:57:06 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:57:06 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 5D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:57:06 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:57:06 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:57:11 | 
🎲 Бросок на попадание (to hit): 5D6
2026-03-12 10:57:11 | REQ: движок запросил кубы стрельбы (target=21, count=5).
2026-03-12 10:57:17 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:57:17 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 5D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:57:17 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:57:17 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:57:19 | 
🎲 Бросок на попадание (to hit): 5D6
2026-03-12 10:57:19 | REQ: движок запросил кубы стрельбы (target=22, count=5).
2026-03-12 10:57:21 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:57:21 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 5D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:57:21 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:57:21 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:57:39 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-12 10:57:39 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-12 10:57:39 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-12 10:57:39 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-12 10:57:40 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 10:57:44 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-22-323300.pickle
2026-03-12 10:57:44 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-22-323300.pth
2026-03-12 10:57:44 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-12 10:57:49 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-12 10:57:49 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-12 10:57:49 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-12 10:57:49 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-12 10:57:49 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-12 10:57:49 | [DEPLOY] Order: model first, alternating
2026-03-12 10:57:49 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 10:57:49 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1627, coord=(27,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 10:57:49 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (27,7)
2026-03-12 10:57:49 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 10:57:50 | REQ: deploy cell accepted x=51, y=33
2026-03-12 10:57:50 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,51)
2026-03-12 10:57:50 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,51)
2026-03-12 10:57:50 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 10:57:50 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=610, coord=(10,10), attempt=1, reward=+0.001, score_before=0.429, score_after=0.441, reward_delta=+0.001, forward=0.147, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 10:57:50 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (10,10)
2026-03-12 10:57:50 | Ошибка деплоя: reason=outside_deploy_zone, x=43, y=23. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-12 10:57:50 | REQ: deploy cell accepted x=47, y=25
2026-03-12 10:57:51 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (25,47)
2026-03-12 10:57:51 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (25,47)
2026-03-12 10:57:51 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.135 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-12 10:57:51 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02203389830508475, 'units': 2, 'total_deploy_reward': 0.02203389830508475, 'forward_sum': 0.26949152542372884, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.13474576271186442, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-12 10:57:51 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-12 10:57:51 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-12 10:57:51 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-12 10:57:51 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:57:51 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-12 10:57:51 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 10:57:52 | === БОЕВОЙ РАУНД 1 ===
2026-03-12 10:57:52 | --- ХОД PLAYER ---
2026-03-12 10:57:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:57:52 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:57:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:57:54 | REQ: move cell accepted (RMB) x=40, y=33, mode=advance
2026-03-12 10:57:55 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:57:56 | REQ: move cell accepted (RMB) x=36, y=29, mode=advance
2026-03-12 10:57:56 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:57:56 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:57:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:57:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:57:56 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:57:56 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:57:56 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:57:56 | Нет доступных целей для чарджа.
2026-03-12 10:57:56 | --- ФАЗА БОЯ ---
2026-03-12 10:57:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:57:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:57:56 | --- ХОД MODEL ---
2026-03-12 10:57:56 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:57:56 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:57:56 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:57:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 7). Выбор: down, advance=нет, distance=1
2026-03-12 10:57:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (28, 7)
2026-03-12 10:57:56 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:57:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (10, 10). Выбор: down, advance=да, бросок=6, макс=11, distance=11
2026-03-12 10:57:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (21, 10)
2026-03-12 10:57:56 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 10:57:56 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:57:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:57:56 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 10:57:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-12 10:57:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-12 10:57:56 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:57:56 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:57:56 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-12 10:57:56 | [MODEL] Чардж: нет доступных целей
2026-03-12 10:57:56 | --- ФАЗА БОЯ ---
2026-03-12 10:57:56 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:57:56 | Reward (progress к objective): d_before=22.361, d_after=20.025, delta=2.336, norm=0.389, bonus=+0.012
2026-03-12 10:57:56 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-12 10:57:56 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-12 10:57:56 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-12 10:57:56 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-12 10:57:56 | Итерация 0 завершена с наградой tensor([0.0018], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 10:57:56 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:57:56 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-12 10:57:58 | === БОЕВОЙ РАУНД 2 ===
2026-03-12 10:57:58 | --- ХОД PLAYER ---
2026-03-12 10:57:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:57:58 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:57:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:57:59 | REQ: move cell accepted (RMB) x=29, y=33, mode=advance
2026-03-12 10:57:59 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:57:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:57:59 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 10:57:59 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 10:57:59 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:57:59 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:57:59 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:57:59 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:57:59 | Оружие: Gauss flayer
2026-03-12 10:57:59 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:57:59 | BS оружия: 4+
2026-03-12 10:57:59 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:57:59 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:57:59 | Save цели: 4+ (invul: нет)
2026-03-12 10:57:59 | Benefit of Cover: не активен.
2026-03-12 10:57:59 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:57:59 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:57:59 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:57:59 | Hit rolls:    [5, 3, 3, 1, 4, 6, 5, 2, 5, 1]  -> hits: 1 (crits: 1)
2026-03-12 10:57:59 | Save rolls:   [6]  (цель 4+) -> failed saves: 0
2026-03-12 10:57:59 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 10:57:59 | FX: найден итог урона = 0.0.
2026-03-12 10:57:59 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-12 10:57:59 | FX: позиция эффекта start=(180.0,684.0) end=(972.0,804.0).
2026-03-12 10:57:59 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 10:57:59 | 📌 -------------------------

2026-03-12 10:58:00 | REQ: move cell accepted (RMB) x=25, y=28, mode=advance
2026-03-12 10:58:00 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:00 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:58:00 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 10:58:00 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:58:00 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:58:00 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:00 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 10:58:00 | Оружие: Gauss flayer
2026-03-12 10:58:00 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:00 | BS оружия: 4+
2026-03-12 10:58:00 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:58:00 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:00 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:00 | Benefit of Cover: не активен.
2026-03-12 10:58:00 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:00 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:00 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:58:00 | Hit rolls:    [2, 3, 2, 4, 4, 5, 1, 4, 2, 1]  -> hits: 0
2026-03-12 10:58:00 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 10:58:00 | FX: найден итог урона = 0.0.
2026-03-12 10:58:00 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-12 10:58:00 | FX: позиция эффекта start=(180.0,684.0) end=(876.0,708.0).
2026-03-12 10:58:00 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 10:58:00 | 📌 -------------------------

2026-03-12 10:58:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:58:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:58:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:58:00 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:58:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:58:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:58:00 | Нет доступных целей для чарджа.
2026-03-12 10:58:00 | --- ФАЗА БОЯ ---
2026-03-12 10:58:00 | --- ХОД MODEL ---
2026-03-12 10:58:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:58:00 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:58:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:58:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (28, 7). Выбор: down, advance=нет, distance=1
2026-03-12 10:58:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 7)
2026-03-12 10:58:00 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 10). Выбор: down, advance=нет, distance=4
2026-03-12 10:58:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 10)
2026-03-12 10:58:02 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 10:58:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:58:03 | 
🎲 Бросок на ранение (to wound): 8D6
2026-03-12 10:58:03 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 10:58:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-03-12 10:58:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=17, need<=3).
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 10:58:03 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:58:03 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:58:03 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:03 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:58:03 | Оружие: Gauss flayer
2026-03-12 10:58:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:03 | BS оружия: 4+
2026-03-12 10:58:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:03 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:03 | Benefit of Cover: не активен.
2026-03-12 10:58:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:03 | Hit rolls:    [5, 4, 4, 3, 4, 4, 5, 4, 5, 2]  -> hits: 8
2026-03-12 10:58:03 | Wound rolls:  [6, 6, 6, 3, 1, 2, 3, 1]  (цель 4+) -> wounds: 3
2026-03-12 10:58:03 | Save rolls:   [3, 4, 3]  (цель 4+) -> failed saves: 2
2026-03-12 10:58:03 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 10:58:03 | FX: найден итог урона = 2.0.
2026-03-12 10:58:03 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 10:58:03 | FX: позиция эффекта start=(180.0,684.0) end=(708.0,804.0).
2026-03-12 10:58:03 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 10:58:03 | 📌 -------------------------

2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 10:58:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 10:58:03 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 10:58:03 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 10:58:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 6. HP: 8.0 -> 6.0 (shooting)
2026-03-12 10:58:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=13, need<=3).
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 10:58:03 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:58:03 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:58:03 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:03 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 10:58:03 | Оружие: Gauss flayer
2026-03-12 10:58:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:03 | BS оружия: 4+
2026-03-12 10:58:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:03 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:03 | Benefit of Cover: не активен.
2026-03-12 10:58:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:03 | Hit rolls:    [1, 2, 6, 5, 1, 6, 2, 5, 3, 6]  -> hits: 5 (crits: 3)
2026-03-12 10:58:03 | Wound rolls:  [1, 6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-12 10:58:03 | Save rolls:   [6, 1, 1, 5]  (цель 4+) -> failed saves: 2
2026-03-12 10:58:03 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 10:58:03 | FX: найден итог урона = 2.0.
2026-03-12 10:58:03 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 10:58:03 | FX: позиция эффекта start=(252.0,516.0) end=(708.0,804.0).
2026-03-12 10:58:03 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 10:58:03 | 📌 -------------------------

2026-03-12 10:58:03 | Reward (шаг): стрельба delta=+0.220
2026-03-12 10:58:03 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:58:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:58:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 10:58:03 | [MODEL] Чардж: нет доступных целей
2026-03-12 10:58:03 | --- ФАЗА БОЯ ---
2026-03-12 10:58:03 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:58:03 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-12 10:58:03 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-12 10:58:03 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 10:58:03 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-12 10:58:03 | Итерация 1 завершена с наградой tensor([0.2007], device='cuda:0'), здоровье игрока [6.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 10:58:03 | {'model health': [10.0, 10.0], 'player health': [6.0, 10.0], 'model alive models': [10, 10], 'player alive models': [6, 10], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:58:03 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [6.0, 10.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-12 10:58:03 | === БОЕВОЙ РАУНД 3 ===
2026-03-12 10:58:03 | --- ХОД PLAYER ---
2026-03-12 10:58:03 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:58:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:05 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-12 10:58:05 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:58:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:58:06 | REQ: move cell accepted (RMB) x=18, y=32, mode=advance
2026-03-12 10:58:07 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:07 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:58:07 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 10:58:07 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (Overwatch)
2026-03-12 10:58:07 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-12 10:58:07 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-12 10:58:07 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:58:07 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:58:07 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:07 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:58:07 | Оружие: Gauss flayer
2026-03-12 10:58:07 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:07 | BS оружия: 4+
2026-03-12 10:58:07 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:58:07 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:07 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:07 | Benefit of Cover: не активен.
2026-03-12 10:58:07 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:07 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:07 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:58:07 | Hit rolls:    [1, 4, 6, 6, 5, 5, 4, 6, 4, 5, 1, 4, 1, 3, 5, 4, 1, 4, 3, 6]  -> hits: 4 (crits: 4)
2026-03-12 10:58:07 | Save rolls:   [6, 1, 3, 4]  (цель 4+) -> failed saves: 2
2026-03-12 10:58:07 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 10:58:07 | FX: найден итог урона = 2.0.
2026-03-12 10:58:07 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 10:58:07 | FX: позиция эффекта start=(180.0,708.0) end=(708.0,804.0).
2026-03-12 10:58:07 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 10:58:07 | 📌 -------------------------

2026-03-12 10:58:07 | REQ: move cell accepted (RMB) x=14, y=30, mode=advance
2026-03-12 10:58:08 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:08 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:58:08 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-12 10:58:08 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 10:58:08 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:58:08 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:58:08 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:08 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 10:58:08 | Оружие: Gauss flayer
2026-03-12 10:58:08 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:08 | BS оружия: 4+
2026-03-12 10:58:08 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:58:08 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:08 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:08 | Benefit of Cover: не активен.
2026-03-12 10:58:08 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:08 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:08 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:58:08 | Hit rolls:    [3, 4, 1, 2, 4, 1, 4, 5, 1, 2, 2, 1, 2, 2, 6, 6, 6, 4, 1, 4]  -> hits: 3 (crits: 3)
2026-03-12 10:58:08 | Save rolls:   [5, 5, 4]  (цель 4+) -> failed saves: 0
2026-03-12 10:58:08 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 10:58:08 | FX: найден итог урона = 0.0.
2026-03-12 10:58:08 | FX: дубликат отчёта, эффект не создаём.
2026-03-12 10:58:08 | 📌 -------------------------

2026-03-12 10:58:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:58:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:58:08 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 10:58:08 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:58:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:58:08 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 10:58:08 | Нет доступных целей для чарджа.
2026-03-12 10:58:08 | --- ФАЗА БОЯ ---
2026-03-12 10:58:08 | --- ХОД MODEL ---
2026-03-12 10:58:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:58:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:58:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:58:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 7). Выбор: left, advance=нет, distance=3
2026-03-12 10:58:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 4)
2026-03-12 10:58:08 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:09 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 10). Выбор: left, advance=нет, distance=5
2026-03-12 10:58:09 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (25, 5)
2026-03-12 10:58:09 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:10 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 10:58:10 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:58:10 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-12 10:58:10 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 10:58:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 6. HP: 7.0 -> 6.0 (shooting)
2026-03-12 10:58:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=18, need<=3).
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-12 10:58:10 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:58:10 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:58:10 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:10 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:58:10 | Оружие: Gauss flayer
2026-03-12 10:58:10 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:10 | BS оружия: 4+
2026-03-12 10:58:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:10 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:10 | Benefit of Cover: не активен.
2026-03-12 10:58:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:10 | Hit rolls:    [3, 2, 1, 1, 2, 3, 5, 4, 4, 1, 1, 5, 5, 2, 3, 3, 2, 1, 3, 1]  -> hits: 5
2026-03-12 10:58:10 | Wound rolls:  [6, 2, 1, 4, 5]  (цель 4+) -> wounds: 3
2026-03-12 10:58:10 | Save rolls:   [3, 6, 4]  (цель 4+) -> failed saves: 1
2026-03-12 10:58:10 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 10:58:10 | FX: найден итог урона = 1.0.
2026-03-12 10:58:10 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 10:58:10 | FX: позиция эффекта start=(180.0,708.0) end=(444.0,780.0).
2026-03-12 10:58:10 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 10:58:10 | 📌 -------------------------

2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 10:58:10 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:58:10 | 
🎲 Бросок на ранение (to wound): 7D6
2026-03-12 10:58:10 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 10:58:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 5. HP: 6.0 -> 5.0 (shooting)
2026-03-12 10:58:10 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=17, need<=3).
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-12 10:58:10 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:58:10 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:58:10 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:10 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 10:58:10 | Оружие: Gauss flayer
2026-03-12 10:58:10 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:10 | BS оружия: 4+
2026-03-12 10:58:10 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:10 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:10 | Benefit of Cover: не активен.
2026-03-12 10:58:10 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:10 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:10 | Hit rolls:    [3, 5, 3, 4, 4, 5, 1, 2, 4, 3, 1, 1, 2, 2, 1, 6, 4, 5, 1, 6]  -> hits: 9 (crits: 2)
2026-03-12 10:58:10 | Wound rolls:  [3, 2, 2, 3, 2, 6, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-12 10:58:10 | Save rolls:   [5, 4, 2]  (цель 4+) -> failed saves: 1
2026-03-12 10:58:10 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 10:58:10 | FX: найден итог урона = 1.0.
2026-03-12 10:58:10 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 10:58:10 | FX: позиция эффекта start=(252.0,612.0) end=(444.0,780.0).
2026-03-12 10:58:10 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 10:58:10 | 📌 -------------------------

2026-03-12 10:58:10 | Reward (шаг): стрельба delta=+0.160
2026-03-12 10:58:10 | --- ФАЗА ЧАРДЖА ---
2026-03-12 10:58:10 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Доступные цели для чарджа: Unit 12 — Necrons Necron Warriors (x10 моделей). Решение: пропуск чарджа.
2026-03-12 10:58:10 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Доступные цели для чарджа: Unit 12 — Necrons Necron Warriors (x10 моделей). Решение: пропуск чарджа.
2026-03-12 10:58:10 | --- ФАЗА БОЯ ---
2026-03-12 10:58:10 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 10:58:10 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-12 10:58:10 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-12 10:58:10 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 10:58:10 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-12 10:58:10 | Итерация 2 завершена с наградой tensor([0.1407], device='cuda:0'), здоровье игрока [5.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 10:58:10 | {'model health': [10.0, 10.0], 'player health': [5.0, 10.0], 'model alive models': [10, 10], 'player alive models': [5, 10], 'modelCP': 2, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 10:58:10 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [5.0, 10.0]
CP MODEL: 2, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-12 10:58:11 | === БОЕВОЙ РАУНД 4 ===
2026-03-12 10:58:11 | --- ХОД PLAYER ---
2026-03-12 10:58:11 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 10:58:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 10:58:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 10:58:12 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 10:58:12 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 10:58:14 | REQ: move cell accepted (RMB) x=13, y=33, mode=normal
2026-03-12 10:58:14 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 10:58:14 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:58:14 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 10:58:14 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 10:58:14 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 10:58:14 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 10:58:14 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:14 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 10:58:14 | Оружие: Gauss flayer
2026-03-12 10:58:14 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:14 | BS оружия: 4+
2026-03-12 10:58:14 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 10:58:14 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:14 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:14 | Benefit of Cover: не активен.
2026-03-12 10:58:14 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:14 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:14 | Правило: Overwatch: попадания только на 6+
2026-03-12 10:58:14 | Hit rolls:    [5, 5, 4, 1, 1, 1, 6, 2, 2, 5, 4, 1, 1, 2, 2, 4, 4, 4, 2, 3]  -> hits: 1 (crits: 1)
2026-03-12 10:58:14 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-03-12 10:58:14 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 10:58:14 | FX: найден итог урона = 0.0.
2026-03-12 10:58:14 | FX: дубликат отчёта, эффект не создаём.
2026-03-12 10:58:14 | 📌 -------------------------

2026-03-12 10:58:16 | Unit 12: movement stay (позиция сохранена x=14, y=30).
2026-03-12 10:58:17 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (14,30).
2026-03-12 10:58:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 10:58:17 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:58:24 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-12 10:58:24 | REQ: движок запросил кубы стрельбы (target=21, count=16).
2026-03-12 10:58:25 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:58:25 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 16D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:58:25 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:58:25 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:58:30 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-12 10:58:30 | REQ: движок запросил кубы стрельбы (target=22, count=16).
2026-03-12 10:58:31 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:58:31 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 16D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:58:31 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:58:31 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:58:43 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-12 10:58:43 | REQ: движок запросил кубы стрельбы (target=21, count=16).
2026-03-12 10:58:45 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:58:45 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 16D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:58:45 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:58:45 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 10:58:46 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-12 10:58:46 | REQ: движок запросил кубы стрельбы (target=22, count=16).
2026-03-12 10:58:55 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 10:58:55 | REQ: движок запросил кубы стрельбы (target=22, count=4).
2026-03-12 10:58:56 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 10:58:56 | REQ: движок запросил кубы стрельбы (target=22, count=3).
2026-03-12 10:58:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-12 10:58:58 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-12 10:58:58 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:58 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 10:58:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 10:58:58 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 10:58:58 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-12 10:58:58 | Оружие: Gauss flayer
2026-03-12 10:58:58 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 10:58:58 | BS оружия: 4+
2026-03-12 10:58:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 10:58:58 | Save цели: 4+ (invul: нет)
2026-03-12 10:58:58 | Benefit of Cover: не активен.
2026-03-12 10:58:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 10:58:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 10:58:58 | Hit rolls:    [1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 1, 1, 1]  -> hits: 6 (crits: 2)
2026-03-12 10:58:58 | Wound rolls:  [1, 2, 3, 4]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-12 10:58:58 | Save rolls:   [1, 2, 3]  (цель 4+) -> failed saves: 3
2026-03-12 10:58:58 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-12 10:58:58 | FX: найден итог урона = 3.0.
2026-03-12 10:58:58 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=3.0).
2026-03-12 10:58:58 | FX: позиция эффекта start=(324.0,804.0) end=(132.0,612.0).
2026-03-12 10:58:58 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-12 10:58:58 | 📌 -------------------------

2026-03-12 10:58:58 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-12 10:58:58 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-12 10:58:58 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 10:59:02 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 10:59:02 | REQ: движок запросил кубы стрельбы (target=21, count=20).
2026-03-12 10:59:03 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 10:59:03 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 20D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 10:59:03 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 10:59:03 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
