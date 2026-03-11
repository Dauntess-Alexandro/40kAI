2026-03-11 17:30:35 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-11 17:30:35 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-11 17:30:35 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-11 17:30:35 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-11 17:30:35 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 17:30:35 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:30:35 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-11 17:30:35 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:30:35 | FX: найден итог урона = 4.0.
2026-03-11 17:30:35 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=4.0).
2026-03-11 17:30:35 | FX: не удалось получить координаты для эффекта (attacker=12, target=21).
2026-03-11 17:30:36 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 17:30:47 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-9-477449.pickle
2026-03-11 17:30:47 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-9-477449.pth
2026-03-11 17:30:47 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-11 17:30:50 | Roll-off Attacker/Defender: enemy=1 model=4 -> attacker=model
2026-03-11 17:30:50 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-11 17:30:50 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-11 17:30:50 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-11 17:30:50 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-11 17:30:50 | [DEPLOY] Order: model first, alternating
2026-03-11 17:30:50 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 17:30:50 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=785, coord=(13,5), attempt=1, reward=+0.021, score_before=0.000, score_after=0.413, reward_delta=+0.021, forward=0.088, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 17:30:50 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (13,5)
2026-03-11 17:30:50 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 17:30:50 | REQ: deploy cell accepted x=55, y=24
2026-03-11 17:30:50 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,55)
2026-03-11 17:30:50 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (24,55)
2026-03-11 17:30:50 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 17:30:50 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2048, coord=(34,8), attempt=1, reward=+0.001, score_before=0.413, score_after=0.425, reward_delta=+0.001, forward=0.114, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 17:30:50 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (34,8)
2026-03-11 17:30:50 | REQ: deploy cell accepted x=49, y=16
2026-03-11 17:30:51 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-11 17:30:51 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (16,49)
2026-03-11 17:30:51 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.101 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-11 17:30:51 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021245565628695312, 'units': 2, 'total_deploy_reward': 0.021245565628695312, 'forward_sum': 0.20169491525423727, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.10084745762711864, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-11 17:30:51 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-11 17:30:51 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-11 17:30:51 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-11 17:30:51 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 17:30:51 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-11 17:30:51 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 17:30:53 | === БОЕВОЙ РАУНД 1 ===
2026-03-11 17:30:53 | --- ХОД PLAYER ---
2026-03-11 17:30:53 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:30:53 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 17:30:53 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:30:54 | REQ: move cell accepted (RMB) x=44, y=26, mode=advance
2026-03-11 17:30:55 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 17:30:55 | REQ: move cell accepted (RMB) x=41, y=19, mode=advance
2026-03-11 17:30:55 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 17:30:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:30:55 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 17:30:55 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 17:30:55 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:30:55 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 17:30:55 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 17:30:55 | Нет доступных целей для чарджа.
2026-03-11 17:30:55 | --- ФАЗА БОЯ ---
2026-03-11 17:30:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 17:30:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 17:30:55 | --- ХОД MODEL ---
2026-03-11 17:30:55 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:30:55 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 17:30:55 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:30:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 5). Выбор: right, advance=нет, distance=1
2026-03-11 17:30:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 6)
2026-03-11 17:30:55 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 17:30:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 8). Выбор: right, advance=да, бросок=4, макс=9, distance=9
2026-03-11 17:30:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (34, 17)
2026-03-11 17:30:55 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 17:30:55 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:30:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=36.00, range=24.00, delta=+12.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 17:30:55 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 17:30:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-11 17:30:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 17:30:55 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:30:55 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 17:30:55 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 17:30:55 | [MODEL] Чардж: нет доступных целей
2026-03-11 17:30:55 | --- ФАЗА БОЯ ---
2026-03-11 17:30:55 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 17:30:55 | Reward (progress к objective): d_before=25.962, d_after=19.105, delta=6.857, norm=1.143, bonus=+0.034
2026-03-11 17:30:55 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-11 17:30:55 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-11 17:30:55 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-11 17:30:55 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-11 17:30:55 | Итерация 0 завершена с наградой tensor([0.0343], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-11 17:30:55 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 17:30:55 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-11 17:30:57 | === БОЕВОЙ РАУНД 2 ===
2026-03-11 17:30:57 | --- ХОД PLAYER ---
2026-03-11 17:30:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:30:57 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 17:30:57 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:30:58 | REQ: move cell accepted (RMB) x=33, y=28, mode=advance
2026-03-11 17:30:59 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:30:59 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 17:30:59 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 17:30:59 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-11 17:30:59 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-11 17:30:59 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 17:30:59 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 17:30:59 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 17:30:59 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:30:59 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-11 17:30:59 | Оружие: Gauss flayer
2026-03-11 17:30:59 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:30:59 | BS оружия: 4+
2026-03-11 17:30:59 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 17:30:59 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:30:59 | Save цели: 4+ (invul: нет)
2026-03-11 17:30:59 | Benefit of Cover: не активен.
2026-03-11 17:30:59 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:30:59 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:30:59 | Правило: Overwatch: попадания только на 6+
2026-03-11 17:30:59 | Hit rolls:    [2, 3, 6, 4, 6, 5, 3, 3, 3, 3]  -> hits: 2 (crits: 2)
2026-03-11 17:30:59 | Save rolls:   [2, 3]  (цель 4+) -> failed saves: 2
2026-03-11 17:30:59 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 17:30:59 | FX: найден итог урона = 2.0.
2026-03-11 17:30:59 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-11 17:30:59 | FX: позиция эффекта start=(420.0,828.0) end=(1068.0,636.0).
2026-03-11 17:30:59 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-11 17:30:59 | 📌 -------------------------

2026-03-11 17:31:00 | REQ: move cell accepted (RMB) x=30, y=24, mode=advance
2026-03-11 17:31:00 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:31:00 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 17:31:00 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 17:31:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-11 17:31:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 17:31:00 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-11 17:31:00 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 17:31:00 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 17:31:00 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:31:00 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 17:31:00 | Оружие: Gauss flayer
2026-03-11 17:31:00 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:31:00 | BS оружия: 4+
2026-03-11 17:31:00 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 17:31:00 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:31:00 | Save цели: 4+ (invul: нет)
2026-03-11 17:31:00 | Benefit of Cover: не активен.
2026-03-11 17:31:00 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:31:00 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:31:00 | Правило: Overwatch: попадания только на 6+
2026-03-11 17:31:00 | Hit rolls:    [1, 5, 4, 5, 1, 6, 6, 4, 1, 4]  -> hits: 2 (crits: 2)
2026-03-11 17:31:00 | Save rolls:   [2, 4]  (цель 4+) -> failed saves: 1
2026-03-11 17:31:00 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 17:31:00 | FX: найден итог урона = 1.0.
2026-03-11 17:31:00 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-11 17:31:00 | FX: позиция эффекта start=(156.0,324.0) end=(996.0,468.0).
2026-03-11 17:31:00 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-11 17:31:00 | 📌 -------------------------

2026-03-11 17:31:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:31:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 17:31:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 17:31:00 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:31:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 17:31:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 17:31:00 | Нет доступных целей для чарджа.
2026-03-11 17:31:00 | --- ФАЗА БОЯ ---
2026-03-11 17:31:00 | --- ХОД MODEL ---
2026-03-11 17:31:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:31:00 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-11 17:31:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:31:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 6). Выбор: right, advance=нет, distance=3
2026-03-11 17:31:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 9)
2026-03-11 17:31:00 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:31:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 17). Выбор: right, advance=нет, distance=3
2026-03-11 17:31:02 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (34, 20)
2026-03-11 17:31:02 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:31:03 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-11 17:31:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 17:31:03 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 17:31:03 | 
🎲 Бросок сейвы (save): 3D6
2026-03-11 17:31:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 7. HP: 8.0 -> 7.0 (shooting)
2026-03-11 17:31:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=13, need<=3).
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-11 17:31:03 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:31:03 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:31:03 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:31:03 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 17:31:03 | Оружие: Gauss flayer
2026-03-11 17:31:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:31:03 | BS оружия: 4+
2026-03-11 17:31:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:31:03 | Save цели: 4+ (invul: нет)
2026-03-11 17:31:03 | Benefit of Cover: не активен.
2026-03-11 17:31:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:31:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:31:03 | Hit rolls:    [6, 4, 1, 6, 1, 2, 2, 2, 4, 1]  -> hits: 4 (crits: 2)
2026-03-11 17:31:03 | Wound rolls:  [5, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 2 = 3
2026-03-11 17:31:03 | Save rolls:   [5, 6, 3]  (цель 4+) -> failed saves: 1
2026-03-11 17:31:03 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 17:31:03 | FX: найден итог урона = 1.0.
2026-03-11 17:31:03 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-11 17:31:03 | FX: позиция эффекта start=(156.0,324.0) end=(804.0,684.0).
2026-03-11 17:31:03 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 17:31:03 | 📌 -------------------------

2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-11 17:31:03 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 17:31:03 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-11 17:31:03 | 
🎲 Бросок сейвы (save): 4D6
2026-03-11 17:31:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 4. HP: 7.0 -> 4.0 (shooting)
2026-03-11 17:31:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=5, need<=3).
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-11 17:31:03 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:31:03 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:31:03 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:31:03 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-11 17:31:03 | Оружие: Gauss flayer
2026-03-11 17:31:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:31:03 | BS оружия: 4+
2026-03-11 17:31:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:31:03 | Save цели: 4+ (invul: нет)
2026-03-11 17:31:03 | Benefit of Cover: не активен.
2026-03-11 17:31:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:31:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:31:03 | Hit rolls:    [3, 4, 3, 2, 1, 4, 1, 6, 1, 5, 5, 1, 3, 6, 5, 2, 1, 1, 4, 2]  -> hits: 8 (crits: 2)
2026-03-11 17:31:03 | Wound rolls:  [4, 1, 4, 3, 1, 1]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-11 17:31:03 | Save rolls:   [1, 3, 5, 3]  (цель 4+) -> failed saves: 3
2026-03-11 17:31:03 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-11 17:31:03 | FX: найден итог урона = 3.0.
2026-03-11 17:31:03 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=3.0).
2026-03-11 17:31:03 | FX: позиция эффекта start=(420.0,828.0) end=(804.0,684.0).
2026-03-11 17:31:03 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-11 17:31:03 | 📌 -------------------------

2026-03-11 17:31:03 | Reward (шаг): стрельба delta=+0.220
2026-03-11 17:31:03 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:31:03 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 17:31:03 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 17:31:03 | [MODEL] Чардж: нет доступных целей
2026-03-11 17:31:03 | --- ФАЗА БОЯ ---
2026-03-11 17:31:03 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 17:31:03 | Reward (progress к objective): d_before=19.105, d_after=17.205, delta=1.900, norm=0.317, bonus=+0.010
2026-03-11 17:31:03 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-11 17:31:03 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-11 17:31:03 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-11 17:31:03 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-11 17:31:03 | Итерация 1 завершена с наградой tensor([0.2102], device='cuda:0'), здоровье игрока [4.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-11 17:31:03 | {'model health': [10.0, 10.0], 'player health': [4.0, 9.0], 'model alive models': [10, 10], 'player alive models': [4, 9], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 17:31:03 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [4.0, 9.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

2026-03-11 17:31:05 | === БОЕВОЙ РАУНД 3 ===
2026-03-11 17:31:05 | --- ХОД PLAYER ---
2026-03-11 17:31:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:31:05 | Unit 11 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-11 17:31:05 | Бросок 2D6...
2026-03-11 17:31:07 | Бросок: 1 1
2026-03-11 17:31:07 | Unit 11 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-11 17:31:09 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=4, раны=[1, 1, 1, 1] всего=4
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 17:31:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-11 17:31:11 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 17:31:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-11 17:31:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 17:31:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 17:31:12 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 17:31:12 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-11 17:31:12 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:31:16 | Unit 11: movement stay (позиция сохранена x=33, y=28).
2026-03-11 17:31:16 | Unit 11 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (33,28).
2026-03-11 17:31:17 | Unit 12: movement stay (позиция сохранена x=30, y=24).
2026-03-11 17:31:17 | Unit 12 — Necrons Necron Warriors (x10 моделей): движение stay (mode=stay). Позиция сохранена: (30,24).
2026-03-11 17:31:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:31:17 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-11 17:31:17 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 17:31:28 | 
🎲 Бросок на попадание (to hit): 7D6
2026-03-11 17:31:58 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:31:58 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:31:58 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:31:58 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:31:58 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-11 17:31:58 | Оружие: Gauss flayer
2026-03-11 17:31:58 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:31:58 | BS оружия: 4+
2026-03-11 17:31:58 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:31:58 | Save цели: 4+ (invul: нет)
2026-03-11 17:31:58 | Benefit of Cover: не активен.
2026-03-11 17:31:58 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:31:58 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:31:58 | Hit rolls:    [3, 3, 3, 3, 3, 3, 3]  -> hits: 0
2026-03-11 17:31:58 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 17:31:58 | FX: найден итог урона = 0.0.
2026-03-11 17:31:58 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=0.0).
2026-03-11 17:31:58 | FX: позиция эффекта start=(804.0,684.0) end=(228.0,324.0).
2026-03-11 17:31:58 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-11 17:31:58 | 📌 -------------------------

2026-03-11 17:31:58 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-11 17:31:58 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-11 17:31:58 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 17:32:16 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 17:32:37 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-11 17:32:43 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:32:43 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:32:43 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:32:43 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:32:43 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-11 17:32:43 | Оружие: Gauss flayer
2026-03-11 17:32:43 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:32:43 | BS оружия: 4+
2026-03-11 17:32:43 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:32:43 | Save цели: 4+ (invul: нет)
2026-03-11 17:32:43 | Benefit of Cover: не активен.
2026-03-11 17:32:43 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:32:43 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:32:43 | Hit rolls:    [1, 1, 1, 1, 6, 6, 6, 6, 6, 6]  -> hits: 6 (crits: 6)
2026-03-11 17:32:43 | Save rolls:   [5, 6, 4, 3, 1, 2]  (цель 4+) -> failed saves: 3
2026-03-11 17:32:43 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-11 17:32:43 | FX: найден итог урона = 3.0.
2026-03-11 17:32:43 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=3.0).
2026-03-11 17:32:43 | FX: позиция эффекта start=(732.0,588.0) end=(228.0,324.0).
2026-03-11 17:32:43 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-03-11 17:32:43 | 📌 -------------------------

2026-03-11 17:32:43 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:32:43 | Нет доступных целей для чарджа.
2026-03-11 17:32:43 | --- ФАЗА БОЯ ---
2026-03-11 17:32:43 | --- ХОД MODEL ---
2026-03-11 17:32:43 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-11 17:32:43 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-11 17:32:43 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (13, 9). Выбор: right, advance=нет, distance=3
2026-03-11 17:32:43 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (13, 12)
2026-03-11 17:32:43 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (34, 20). Выбор: right, advance=нет, distance=3
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (34, 23)
2026-03-11 17:32:47 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-11 17:32:47 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-11 17:32:47 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-11 17:32:47 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 17:32:47 | 
🎲 Бросок сейвы (save): 4D6
2026-03-11 17:32:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 6. HP: 7.0 -> 6.0 (shooting)
2026-03-11 17:32:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=10, need<=3).
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-11 17:32:47 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:32:47 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:32:47 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:32:47 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 17:32:47 | Оружие: Gauss flayer
2026-03-11 17:32:47 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:32:47 | BS оружия: 4+
2026-03-11 17:32:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:32:47 | Save цели: 4+ (invul: нет)
2026-03-11 17:32:47 | Benefit of Cover: не активен.
2026-03-11 17:32:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:32:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:32:47 | Hit rolls:    [6, 1, 5, 1, 2, 6, 5, 4]  -> hits: 5 (crits: 2)
2026-03-11 17:32:47 | Wound rolls:  [1, 6, 6]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-11 17:32:47 | Save rolls:   [2, 4, 6, 6]  (цель 4+) -> failed saves: 1
2026-03-11 17:32:47 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 17:32:47 | FX: найден итог урона = 1.0.
2026-03-11 17:32:47 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 17:32:47 | 📌 -------------------------

2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-11 17:32:47 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-11 17:32:47 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-11 17:32:47 | 
🎲 Бросок сейвы (save): 6D6
2026-03-11 17:32:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 4. HP: 6.0 -> 4.0 (shooting)
2026-03-11 17:32:47 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): shot_from_cover=+0.030 (cover_soft=1.000, threat=2->2).
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.030, total=0.140
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-11 17:32:47 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 17:32:47 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 17:32:47 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 17:32:47 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-11 17:32:47 | Оружие: Gauss flayer
2026-03-11 17:32:47 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 17:32:47 | BS оружия: 4+
2026-03-11 17:32:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 17:32:47 | Save цели: 4+ (invul: нет)
2026-03-11 17:32:47 | Benefit of Cover: не активен.
2026-03-11 17:32:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 17:32:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 17:32:47 | Hit rolls:    [2, 4, 6, 3, 2, 6, 6, 2, 3, 2, 3, 5, 2, 6, 1, 6, 2, 4, 5, 4]  -> hits: 10 (crits: 5)
2026-03-11 17:32:47 | Wound rolls:  [1, 3, 3, 2, 6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 5 = 6
2026-03-11 17:32:47 | Save rolls:   [5, 1, 4, 6, 6, 1]  (цель 4+) -> failed saves: 2
2026-03-11 17:32:47 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 17:32:47 | FX: найден итог урона = 2.0.
2026-03-11 17:32:47 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-11 17:32:47 | FX: позиция эффекта start=(492.0,828.0) end=(804.0,684.0).
2026-03-11 17:32:47 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-11 17:32:47 | 📌 -------------------------

2026-03-11 17:32:47 | Reward (шаг): стрельба delta=+0.220
2026-03-11 17:32:47 | --- ФАЗА ЧАРДЖА ---
2026-03-11 17:32:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Чардж цели: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана Unit 12 — Necrons Necron Warriors (x10 моделей). бросок: 3 + 6 = 9. Результат: провал (цель недоступна).
2026-03-11 17:32:47 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (чардж): fail_penalty=-0.000
2026-03-11 17:32:47 | --- ФАЗА БОЯ ---
2026-03-11 17:32:47 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 17:32:47 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-03-11 17:32:47 | Reward (progress к objective): d_before=17.205, d_after=15.652, delta=1.552, norm=0.259, bonus=+0.008
2026-03-11 17:32:47 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.011, delta=+0.056; cover=0.000->0.500, threat=-0.667->-0.667, guard=0.000->0.400
2026-03-11 17:32:47 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=4)
2026-03-11 17:32:47 | Reward (terrain/clamp): raw=+0.046, cap=±0.120, clamp не сработал
2026-03-11 17:32:47 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-11 17:32:47 | Итерация 2 завершена с наградой tensor([0.2239], device='cuda:0'), здоровье игрока [4.0, 10.0], здоровье модели [8.0, 10.0]
2026-03-11 17:32:47 | {'model health': [8.0, 10.0], 'player health': [4.0, 10.0], 'model alive models': [8, 10], 'player alive models': [4, 10], 'modelCP': 4, 'playerCP': 5, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 17:32:47 | Здоровье MODEL: [8.0, 10.0], здоровье PLAYER: [4.0, 10.0]
CP MODEL: 4, CP PLAYER: 5
VP MODEL: 0, VP PLAYER: 1
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

