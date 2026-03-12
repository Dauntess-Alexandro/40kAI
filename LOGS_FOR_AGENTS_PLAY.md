2026-03-12 15:08:36 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-12 15:08:36 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-12 15:08:36 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-12 15:08:36 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-12 15:08:36 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 15:08:36 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 15:08:41 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-17-813611.pickle
2026-03-12 15:08:41 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-17-813611.pth
2026-03-12 15:08:41 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-12 15:08:46 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-12 15:08:46 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-12 15:08:46 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-12 15:08:46 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-12 15:08:46 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-12 15:08:46 | [DEPLOY] Order: model first, alternating
2026-03-12 15:08:46 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 15:08:46 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2292, coord=(38,12), attempt=1, reward=+0.019, score_before=0.000, score_after=0.375, reward_delta=+0.019, forward=0.207, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 15:08:46 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (38,12)
2026-03-12 15:08:46 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 15:08:46 | REQ: deploy cell accepted x=53, y=30
2026-03-12 15:08:46 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,53)
2026-03-12 15:08:46 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (30,53)
2026-03-12 15:08:46 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 15:08:46 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=661, coord=(11,1), attempt=1, reward=-0.002, score_before=0.375, score_after=0.332, reward_delta=-0.002, forward=0.114, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 15:08:46 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (11,1)
2026-03-12 15:08:46 | REQ: deploy cell accepted x=49, y=20
2026-03-12 15:08:47 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,49)
2026-03-12 15:08:47 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,49)
2026-03-12 15:08:47 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.017 total_deploy_reward=+0.017 avg_forward=0.160 avg_spread=1.000 avg_edge=0.000 avg_cover=0.000
2026-03-12 15:08:47 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.016594402837997638, 'units': 2, 'total_deploy_reward': 0.016594402837997638, 'forward_sum': 0.3203389830508474, 'spread_sum': 2.0, 'edge_sum': 0.0, 'cover_sum': 0.0, 'avg_forward': 0.1601694915254237, 'avg_spread': 1.0, 'avg_edge': 0.0, 'avg_cover': 0.0}
2026-03-12 15:08:47 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-12 15:08:47 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-12 15:08:47 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-12 15:08:47 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 15:08:47 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-12 15:08:47 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=10, cells_rapid=5, rapid_fire=1, source_cell=(14, 30), target_filter_size=2, max_target_dist=10, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 15:08:47 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(14, 30), full_cells=10, rapid_cells=5, вошло=420, rapid=121, не вошло=1980, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-12 15:08:47 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(49, 20), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 15:08:47 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 15:08:48 | === БОЕВОЙ РАУНД 1 ===
2026-03-12 15:08:48 | --- ХОД PLAYER ---
2026-03-12 15:08:48 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:08:48 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:08:48 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:08:49 | REQ: move cell accepted (RMB) x=42, y=32, mode=advance
2026-03-12 15:08:50 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:08:51 | REQ: move cell accepted (RMB) x=38, y=27, mode=advance
2026-03-12 15:08:52 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:08:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:08:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 15:08:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 15:08:52 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:08:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 15:08:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 15:08:52 | Нет доступных целей для чарджа.
2026-03-12 15:08:52 | --- ФАЗА БОЯ ---
2026-03-12 15:08:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 15:08:52 | --- ХОД MODEL ---
2026-03-12 15:08:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:08:52 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:08:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 12). Выбор: down, advance=нет, distance=1
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (39, 12)
2026-03-12 15:08:52 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (11, 1). Выбор: down, advance=да, бросок=1, макс=6, distance=6
2026-03-12 15:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (17, 1)
2026-03-12 15:08:52 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:08:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:08:52 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-12 15:08:52 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 15:08:52 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 15:08:52 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 15:08:52 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-03-12 15:08:52 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=14, need<=3).
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 15:08:52 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:08:52 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:08:52 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:08:52 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 15:08:52 | Оружие: Gauss flayer
2026-03-12 15:08:52 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:08:52 | BS оружия: 4+
2026-03-12 15:08:52 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:08:52 | Save цели: 4+ (invul: нет)
2026-03-12 15:08:52 | Benefit of Cover: не активен.
2026-03-12 15:08:52 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:08:52 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:08:52 | Hit rolls:    [2, 3, 3, 5, 6, 4, 6, 1, 1, 6]  -> hits: 5 (crits: 3)
2026-03-12 15:08:52 | Wound rolls:  [5, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-12 15:08:52 | Save rolls:   [5, 6, 3, 1]  (цель 4+) -> failed saves: 2
2026-03-12 15:08:52 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 15:08:52 | FX: найден итог урона = 2.0.
2026-03-12 15:08:52 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=2.0).
2026-03-12 15:08:52 | FX: позиция эффекта start=(300.0,924.0) end=(1188.0,492.0).
2026-03-12 15:08:52 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 15:08:52 | 📌 -------------------------

2026-03-12 15:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-12 15:08:52 | Reward (шаг): стрельба delta=+0.110
2026-03-12 15:08:52 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 15:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-12 15:08:52 | [MODEL] Чардж: нет доступных целей
2026-03-12 15:08:52 | --- ФАЗА БОЯ ---
2026-03-12 15:08:52 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 15:08:52 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-12 15:08:52 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-12 15:08:52 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-12 15:08:52 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-12 15:08:52 | Итерация 0 завершена с наградой tensor([0.1002], device='cuda:0'), здоровье игрока [10.0, 8.0], здоровье модели [10.0, 10.0]
2026-03-12 15:08:52 | {'model health': [10.0, 10.0], 'player health': [10.0, 8.0], 'model alive models': [10, 10], 'player alive models': [10, 8], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 15:08:52 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 8.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-12 15:09:14 | === БОЕВОЙ РАУНД 2 ===
2026-03-12 15:09:14 | --- ХОД PLAYER ---
2026-03-12 15:09:14 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:09:14 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 15:09:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 15:09:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 15:09:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 15:09:18 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-12 15:09:18 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:09:18 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:09:20 | REQ: move cell accepted (RMB) x=31, y=38, mode=advance
2026-03-12 15:09:20 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:09:20 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 15:09:20 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 15:09:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-12 15:09:20 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-12 15:09:20 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 15:09:20 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 15:09:20 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 15:09:20 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:20 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 15:09:20 | Оружие: Gauss flayer
2026-03-12 15:09:20 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:20 | BS оружия: 4+
2026-03-12 15:09:20 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 15:09:20 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:20 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:20 | Benefit of Cover: не активен.
2026-03-12 15:09:20 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:20 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:20 | Правило: Overwatch: попадания только на 6+
2026-03-12 15:09:20 | Hit rolls:    [3, 3, 1, 1, 3, 6, 2, 3, 2, 4]  -> hits: 1 (crits: 1)
2026-03-12 15:09:20 | Save rolls:   [1]  (цель 4+) -> failed saves: 1
2026-03-12 15:09:20 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 15:09:20 | FX: найден итог урона = 1.0.
2026-03-12 15:09:20 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 15:09:20 | FX: позиция эффекта start=(276.0,924.0) end=(1020.0,780.0).
2026-03-12 15:09:20 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 15:09:20 | 📌 -------------------------

2026-03-12 15:09:21 | REQ: move cell accepted (RMB) x=27, y=35, mode=advance
2026-03-12 15:09:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:09:22 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 15:09:22 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 15:09:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 15:09:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 15:09:22 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:22 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 15:09:22 | Оружие: Gauss flayer
2026-03-12 15:09:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:22 | BS оружия: 4+
2026-03-12 15:09:22 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 15:09:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:22 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:22 | Benefit of Cover: не активен.
2026-03-12 15:09:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:22 | Правило: Overwatch: попадания только на 6+
2026-03-12 15:09:22 | Hit rolls:    [4, 2, 3, 3, 3, 1, 4, 2, 1, 3]  -> hits: 0
2026-03-12 15:09:22 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 15:09:22 | FX: найден итог урона = 0.0.
2026-03-12 15:09:22 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-12 15:09:22 | FX: позиция эффекта start=(276.0,924.0) end=(924.0,660.0).
2026-03-12 15:09:22 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 15:09:22 | 📌 -------------------------

2026-03-12 15:09:22 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:09:22 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 15:09:22 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 15:09:22 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:09:22 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 15:09:22 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 15:09:22 | Нет доступных целей для чарджа.
2026-03-12 15:09:22 | --- ФАЗА БОЯ ---
2026-03-12 15:09:22 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 15:09:22 | --- ХОД MODEL ---
2026-03-12 15:09:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:09:22 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:09:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:09:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 11). Выбор: left, advance=нет, distance=1
2026-03-12 15:09:22 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (38, 10)
2026-03-12 15:09:22 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 1). Выбор: left, advance=нет, distance=1
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (17, 0)
2026-03-12 15:09:23 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:09:23 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 15:09:23 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 15:09:23 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-12 15:09:23 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 15:09:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 7. HP: 9.0 -> 7.0 (shooting)
2026-03-12 15:09:23 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=15, need<=3).
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 15:09:23 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:09:23 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:09:23 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:23 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 15:09:23 | Оружие: Gauss flayer
2026-03-12 15:09:23 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:23 | BS оружия: 4+
2026-03-12 15:09:23 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:23 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:23 | Benefit of Cover: не активен.
2026-03-12 15:09:23 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:23 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:23 | Hit rolls:    [4, 2, 1, 5, 6, 3, 4, 2, 5, 4]  -> hits: 6 (crits: 1)
2026-03-12 15:09:23 | Wound rolls:  [3, 4, 1, 4, 3]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 1 = 3
2026-03-12 15:09:23 | Save rolls:   [3, 4, 1]  (цель 4+) -> failed saves: 2
2026-03-12 15:09:23 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 15:09:23 | FX: найден итог урона = 2.0.
2026-03-12 15:09:23 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 15:09:23 | FX: позиция эффекта start=(276.0,924.0) end=(756.0,924.0).
2026-03-12 15:09:23 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 15:09:23 | 📌 -------------------------

2026-03-12 15:09:23 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-12 15:09:23 | [COVER][SHOOTING] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 15:09:23 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 15:09:23 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-12 15:09:23 | 
🎲 Бросок сейвы (save): 2D6
2026-03-12 15:09:23 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (shooting)
2026-03-12 15:09:23 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-12 15:09:23 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:09:23 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:09:23 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:23 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-12 15:09:23 | Оружие: Gauss flayer
2026-03-12 15:09:23 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:23 | BS оружия: 4+
2026-03-12 15:09:23 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:23 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:23 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 15:09:23 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:23 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:23 | Эффект: benefit of cover
2026-03-12 15:09:23 | Hit rolls:    [2, 4, 2, 1, 2, 1, 3, 4, 4, 3]  -> hits: 3
2026-03-12 15:09:23 | Wound rolls:  [4, 6, 2]  (цель 4+) -> wounds: 2
2026-03-12 15:09:23 | Save rolls:   [1, 3]  (цель 3+) -> failed saves: 1
2026-03-12 15:09:23 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 15:09:23 | FX: найден итог урона = 1.0.
2026-03-12 15:09:23 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-12 15:09:23 | FX: позиция эффекта start=(36.0,420.0) end=(660.0,852.0).
2026-03-12 15:09:23 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-12 15:09:23 | 📌 -------------------------

2026-03-12 15:09:23 | Reward (шаг): стрельба delta=+0.190
2026-03-12 15:09:23 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:09:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 15:09:23 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 15:09:23 | [MODEL] Чардж: нет доступных целей
2026-03-12 15:09:23 | --- ФАЗА БОЯ ---
2026-03-12 15:09:23 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 15:09:23 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.050, delta=+0.001; cover=0.000->0.000, threat=-0.500->-0.500, guard=0.000->0.000
2026-03-12 15:09:23 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-12 15:09:23 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 15:09:23 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-12 15:09:23 | Итерация 1 завершена с наградой tensor([0.1705], device='cuda:0'), здоровье игрока [7.0, 8.0], здоровье модели [10.0, 10.0]
2026-03-12 15:09:23 | {'model health': [10.0, 10.0], 'player health': [7.0, 8.0], 'model alive models': [10, 10], 'player alive models': [7, 8], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 15:09:23 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [7.0, 8.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-12 15:09:24 | === БОЕВОЙ РАУНД 3 ===
2026-03-12 15:09:24 | --- ХОД PLAYER ---
2026-03-12 15:09:24 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:09:24 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 15:09:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 15:09:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-12 15:09:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 15:09:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 15:09:25 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 15:09:27 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 15:09:27 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 15:09:27 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 15:09:27 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-12 15:09:27 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:09:27 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:09:28 | REQ: move cell accepted (RMB) x=26, y=39, mode=normal
2026-03-12 15:09:28 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:09:28 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 15:09:28 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 15:09:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 6. HP: 8.0 -> 6.0 (Overwatch)
2026-03-12 15:09:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-12 15:09:28 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-12 15:09:28 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 15:09:28 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 15:09:28 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:28 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 15:09:28 | Оружие: Gauss flayer
2026-03-12 15:09:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:28 | BS оружия: 4+
2026-03-12 15:09:28 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 15:09:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:28 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:28 | Benefit of Cover: не активен.
2026-03-12 15:09:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:28 | Правило: Overwatch: попадания только на 6+
2026-03-12 15:09:28 | Hit rolls:    [4, 6, 2, 3, 4, 1, 4, 1, 3, 4, 6, 1, 2, 2, 3, 5, 4, 5, 5, 4]  -> hits: 2 (crits: 2)
2026-03-12 15:09:28 | Save rolls:   [1, 2]  (цель 4+) -> failed saves: 2
2026-03-12 15:09:28 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 15:09:28 | FX: найден итог урона = 2.0.
2026-03-12 15:09:28 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 15:09:28 | FX: позиция эффекта start=(252.0,924.0) end=(756.0,924.0).
2026-03-12 15:09:28 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 15:09:28 | 📌 -------------------------

2026-03-12 15:09:29 | REQ: move cell accepted (RMB) x=22, y=34, mode=normal
2026-03-12 15:09:29 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:09:29 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 15:09:29 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 15:09:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (Overwatch)
2026-03-12 15:09:29 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 15:09:29 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 15:09:29 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 15:09:29 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 15:09:29 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:09:29 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 15:09:29 | Оружие: Gauss flayer
2026-03-12 15:09:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:09:29 | BS оружия: 4+
2026-03-12 15:09:29 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 15:09:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:09:29 | Save цели: 4+ (invul: нет)
2026-03-12 15:09:29 | Benefit of Cover: не активен.
2026-03-12 15:09:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:09:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:09:29 | Правило: Overwatch: попадания только на 6+
2026-03-12 15:09:29 | Hit rolls:    [6, 1, 3, 4, 4, 2, 5, 3, 1, 2, 6, 2, 4, 6, 5, 5, 6, 5, 3, 2]  -> hits: 4 (crits: 4)
2026-03-12 15:09:29 | Save rolls:   [4, 4, 6, 1]  (цель 4+) -> failed saves: 1
2026-03-12 15:09:29 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 15:09:29 | FX: найден итог урона = 1.0.
2026-03-12 15:09:29 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-12 15:09:29 | FX: позиция эффекта start=(252.0,924.0) end=(660.0,852.0).
2026-03-12 15:09:29 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 15:09:29 | 📌 -------------------------

2026-03-12 15:09:29 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:09:29 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:09:29 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(25, 38), target_filter_size=2, max_target_dist=24, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 15:09:29 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(25, 38), full_cells=24, rapid_cells=12, вошло=1274, rapid=350, не вошло=1126, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-12 15:09:34 | 
🎲 Бросок на попадание (to hit): 12D6
2026-03-12 15:09:34 | REQ: движок запросил кубы стрельбы (target=21, count=12).
2026-03-12 15:09:35 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:09:35 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 12D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:09:35 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:09:35 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:09:49 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-12 15:09:49 | REQ: движок запросил кубы стрельбы (target=22, count=6).
2026-03-12 15:09:50 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:09:50 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 6D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:09:50 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:09:50 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:09:51 | 
🎲 Бросок на попадание (to hit): 12D6
2026-03-12 15:09:51 | REQ: движок запросил кубы стрельбы (target=21, count=12).
2026-03-12 15:09:53 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:09:53 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 12D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:09:53 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:09:53 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:09:55 | 
🎲 Бросок на попадание (to hit): 12D6
2026-03-12 15:09:55 | REQ: движок запросил кубы стрельбы (target=21, count=12).
2026-03-12 15:09:56 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:09:56 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 12D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:09:56 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:09:56 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:09:58 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-12 15:09:58 | REQ: движок запросил кубы стрельбы (target=22, count=6).
2026-03-12 15:09:59 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 22 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:09:59 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 6D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:09:59 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:09:59 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:10:21 | 
🎲 Бросок на попадание (to hit): 12D6
2026-03-12 15:10:21 | REQ: движок запросил кубы стрельбы (target=21, count=12).
2026-03-12 15:10:22 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:10:22 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 12D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:10:22 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:10:22 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-12 15:10:23 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-12 15:10:23 | REQ: движок запросил кубы стрельбы (target=22, count=6).
2026-03-12 15:10:26 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 15:10:26 | REQ: движок запросил кубы стрельбы (target=22, count=1).
2026-03-12 15:10:29 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 0.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:10:29 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:10:29 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:10:29 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:10:29 | FX: найдена строка стрельбы (attacker=11, target=22).
2026-03-12 15:10:29 | Оружие: Gauss flayer
2026-03-12 15:10:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:10:29 | BS оружия: 4+
2026-03-12 15:10:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:10:29 | Save цели: 4+ (invul: нет)
2026-03-12 15:10:29 | Benefit of Cover: не активен.
2026-03-12 15:10:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:10:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:10:29 | Hit rolls:    [1, 1, 1, 1, 1, 6]  -> hits: 1 (crits: 1)
2026-03-12 15:10:29 | Save rolls:   [5]  (цель 4+) -> failed saves: 0
2026-03-12 15:10:29 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 15:10:29 | FX: найден итог урона = 0.0.
2026-03-12 15:10:29 | FX: создан FxShotEvent (attacker=11, target=22, weapon=Gauss flayer, damage=0.0).
2026-03-12 15:10:29 | FX: позиция эффекта start=(612.0,924.0) end=(36.0,396.0).
2026-03-12 15:10:29 | FX: эффект добавлен в рендер (attacker=11, target=22).
2026-03-12 15:10:29 | 📌 -------------------------

2026-03-12 15:10:29 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-12 15:10:29 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-12 15:10:29 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(22, 34), target_filter_size=2, max_target_dist=21, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 15:10:29 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(22, 34), full_cells=24, rapid_cells=12, вошло=1410, rapid=450, не вошло=990, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-12 15:10:29 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 15:12:14 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-12 15:12:14 | REQ: движок запросил кубы стрельбы (target=21, count=16).
2026-03-12 15:12:15 | REQ: Cancel во время бросков принят. Где: viewer/app.py (_cancel_shoot_sequence). Что случилось: отменяем текущий dice-request для Unit 21 и сбрасываем выбор цели. Что делать дальше: выберите новую цель в следующем запросе стрельбы.
2026-03-12 15:12:15 | REQ: бросок отменён пользователем. Где: warhamEnv.player_dice(multi). Что случилось: текущий бросок 16D6 отменён до ввода кубов. Что делать дальше: выберите цель заново в следующем запросе стрельбы.
2026-03-12 15:12:15 | REQ: бросок отменён пользователем. Где: warhamEnv.RollLogger.roll. Что случилось: отмена на этапе 'на попадание (to hit)'. Что делать дальше: выберите цель заново и повторите выстрел.
2026-03-12 15:12:15 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-12 15:12:16 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-12 15:12:16 | REQ: движок запросил кубы стрельбы (target=22, count=8).
2026-03-12 15:12:20 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 15:12:20 | REQ: движок запросил кубы стрельбы (target=22, count=2).
2026-03-12 15:12:25 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 15:12:25 | REQ: движок запросил кубы стрельбы (target=22, count=4).
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 7. HP: 10.0 -> 7.0 (overwatch)
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 7. Причина: потери моделей.
2026-03-12 15:12:28 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 3.0 урона по Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:12:28 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:12:28 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:12:28 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 22 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:12:28 | FX: найдена строка стрельбы (attacker=12, target=22).
2026-03-12 15:12:28 | Оружие: Gauss flayer
2026-03-12 15:12:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:12:28 | BS оружия: 4+
2026-03-12 15:12:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:12:28 | Save цели: 4+ (invul: нет)
2026-03-12 15:12:28 | Benefit of Cover: не активен.
2026-03-12 15:12:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:12:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:12:28 | Hit rolls:    [6, 6, 5, 5, 1, 1, 1, 1]  -> hits: 4 (crits: 2)
2026-03-12 15:12:28 | Wound rolls:  [4, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-12 15:12:28 | Save rolls:   [1, 2, 3, 4]  (цель 4+) -> failed saves: 3
2026-03-12 15:12:28 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-12 15:12:28 | FX: найден итог урона = 3.0.
2026-03-12 15:12:28 | FX: создан FxShotEvent (attacker=12, target=22, weapon=Gauss flayer, damage=3.0).
2026-03-12 15:12:28 | FX: позиция эффекта start=(540.0,828.0) end=(36.0,396.0).
2026-03-12 15:12:28 | FX: эффект добавлен в рендер (attacker=12, target=22).
2026-03-12 15:12:28 | 📌 -------------------------

2026-03-12 15:12:28 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:12:28 | Нет доступных целей для чарджа.
2026-03-12 15:12:28 | --- ФАЗА БОЯ ---
2026-03-12 15:12:28 | --- ХОД MODEL ---
2026-03-12 15:12:28 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) До: моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 15:12:28 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) После:  моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 15:12:28 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 15:12:28 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 15:12:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 10). Выбор: down, advance=нет, distance=1
2026-03-12 15:12:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (39, 10)
2026-03-12 15:12:28 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 15:12:28 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 11 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=24, cells_full=24, cells_rapid=12, rapid_fire=1, source_cell=(25, 38), target_filter_size=2, max_target_dist=24, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 15:12:28 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 11; source=(25, 38), full_cells=24, rapid_cells=12, вошло=1274, rapid=350, не вошло=1126, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (16, 1). Выбор: down, advance=нет, distance=3
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 1)
2026-03-12 15:12:30 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 15:12:30 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 15:12:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-12 15:12:30 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 15:12:30 | 
🎲 Бросок на ранение (to wound): 7D6
2026-03-12 15:12:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=16, need<=3).
2026-03-12 15:12:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-12 15:12:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-12 15:12:30 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:12:30 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:12:30 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:12:30 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 15:12:30 | Оружие: Gauss flayer
2026-03-12 15:12:30 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:12:30 | BS оружия: 4+
2026-03-12 15:12:30 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:12:30 | Save цели: 4+ (invul: нет)
2026-03-12 15:12:30 | Benefit of Cover: не активен.
2026-03-12 15:12:30 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:12:30 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:12:30 | Hit rolls:    [1, 1, 4, 4, 3, 2, 4, 3, 1, 5, 5, 2, 1, 4, 1, 3, 3, 3, 5, 1]  -> hits: 7
2026-03-12 15:12:30 | Wound rolls:  [3, 3, 2, 3, 2, 1, 3]  (цель 4+) -> wounds: 0
2026-03-12 15:12:30 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 15:12:30 | FX: найден итог урона = 0.0.
2026-03-12 15:12:30 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-12 15:12:30 | FX: позиция эффекта start=(252.0,924.0) end=(540.0,828.0).
2026-03-12 15:12:30 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 15:12:30 | 📌 -------------------------

2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-12 15:12:30 | 
🎲 Бросок на попадание (to hit): 8D6
2026-03-12 15:12:30 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 15:12:30 | 
🎲 Бросок сейвы (save): 7D6
2026-03-12 15:12:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 5. HP: 8.0 -> 5.0 (shooting)
2026-03-12 15:12:30 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-12 15:12:30 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 15:12:30 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 15:12:30 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 15:12:30 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-12 15:12:30 | Оружие: Gauss flayer
2026-03-12 15:12:30 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 15:12:30 | BS оружия: 4+
2026-03-12 15:12:30 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 15:12:30 | Save цели: 4+ (invul: нет)
2026-03-12 15:12:30 | Benefit of Cover: не активен.
2026-03-12 15:12:30 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 15:12:30 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 15:12:30 | Hit rolls:    [6, 6, 6, 4, 6, 1, 6, 6]  -> hits: 7 (crits: 6)
2026-03-12 15:12:30 | Wound rolls:  [6]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 6 = 7
2026-03-12 15:12:30 | Save rolls:   [6, 4, 5, 1, 3, 2, 4]  (цель 4+) -> failed saves: 3
2026-03-12 15:12:30 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-12 15:12:30 | FX: найден итог урона = 3.0.
2026-03-12 15:12:30 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=3.0).
2026-03-12 15:12:30 | FX: позиция эффекта start=(36.0,396.0) end=(540.0,828.0).
2026-03-12 15:12:30 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-12 15:12:30 | 📌 -------------------------

2026-03-12 15:12:30 | Reward (шаг): стрельба delta=+0.140
2026-03-12 15:12:30 | --- ФАЗА ЧАРДЖА ---
2026-03-12 15:12:30 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 15:12:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 15:12:30 | [MODEL] Чардж: нет доступных целей
2026-03-12 15:12:30 | --- ФАЗА БОЯ ---
2026-03-12 15:12:30 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 15:12:30 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-12 15:12:30 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-12 15:12:30 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 15:12:30 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-12 15:12:30 | Итерация 2 завершена с наградой tensor([0.1207], device='cuda:0'), здоровье игрока [6.0, 5.0], здоровье модели [10.0, 8.0]
2026-03-12 15:12:30 | {'model health': [10.0, 8.0], 'player health': [6.0, 5.0], 'model alive models': [10, 8], 'player alive models': [6, 5], 'modelCP': 2, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 15:12:30 | Здоровье MODEL: [10.0, 8.0], здоровье PLAYER: [6.0, 5.0]
CP MODEL: 2, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

