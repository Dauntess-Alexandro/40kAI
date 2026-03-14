2026-03-12 18:56:55 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-12 18:56:55 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-12 18:56:55 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-12 18:56:55 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-12 18:56:55 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 18:56:56 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 18:56:59 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-728405.pickle
2026-03-12 18:56:59 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-55-728405.pth
2026-03-12 18:56:59 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-12 18:57:08 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-12 18:57:08 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-12 18:57:08 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-12 18:57:08 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-12 18:57:08 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-12 18:57:08 | [DEPLOY] Order: model first, alternating
2026-03-12 18:57:08 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 18:57:08 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1148, coord=(19,8), attempt=1, reward=+0.022, score_before=0.000, score_after=0.437, reward_delta=+0.022, forward=0.139, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 18:57:08 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (19,8)
2026-03-12 18:57:08 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-12 18:57:09 | REQ: deploy cell accepted x=48, y=33
2026-03-12 18:57:09 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,48)
2026-03-12 18:57:09 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,48)
2026-03-12 18:57:09 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-12 18:57:09 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1751, coord=(29,11), attempt=1, reward=+0.001, score_before=0.437, score_after=0.449, reward_delta=+0.001, forward=0.164, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-12 18:57:09 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (29,11)
2026-03-12 18:57:09 | REQ: deploy cell accepted x=47, y=26
2026-03-12 18:57:10 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,47)
2026-03-12 18:57:10 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (26,47)
2026-03-12 18:57:10 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.022 total_deploy_reward=+0.022 avg_forward=0.152 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-12 18:57:10 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.02242806464327947, 'units': 2, 'total_deploy_reward': 0.02242806464327947, 'forward_sum': 0.30338983050847457, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.15169491525423728, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-12 18:57:10 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-12 18:57:10 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-12 18:57:10 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-12 18:57:10 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 18:57:10 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-12 18:57:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=10, cells_rapid=5, rapid_fire=1, source_cell=(14, 30), target_filter_size=2, max_target_dist=10, inferred_from_targets=1. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 18:57:10 | [VIEWER][SHOOT_RANGE][CELLS] Что случилось: по клеткам рассчитан overlay для Unit 12; source=(14, 30), full_cells=10, rapid_cells=5, вошло=420, rapid=121, не вошло=1980, всего=2400. Где: viewer/opengl_view.py (_build_shooting_overlay, cell-loop). Что делать дальше: если вошло заметно меньше ожидаемой геометрии (square Chebyshev), проверить метрику distance=max(|dx|,|dy|) и корректность full_cells.
2026-03-12 18:57:10 | [VIEWER][SHOOT_RANGE] Что случилось: рассчитан shooting-overlay для Unit 12 (Necron Warriors); weapon=Gauss flayer, source_range=24, request_range=None, cells_full=None, cells_rapid=None, rapid_fire=1, source_cell=(47, 26), target_filter_size=0, max_target_dist=0, inferred_from_targets=0. Где: viewer/opengl_view.py (_build_shooting_overlay). Что делать дальше: сравнить source_range/request_range/cells_full; если cells_full меньше source_range — проверить UI state -> active weapon и экспорт weapon_range из engine.
2026-03-12 18:57:10 | FX: перепроигрываю 30 строк(и) лога.
2026-03-12 18:57:12 | === БОЕВОЙ РАУНД 1 ===
2026-03-12 18:57:12 | --- ХОД PLAYER ---
2026-03-12 18:57:12 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:12 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:12 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:13 | REQ: move cell accepted (RMB) x=37, y=31, mode=advance
2026-03-12 18:57:13 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:13 | [COVER][MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 18:57:13 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:13 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 18:57:13 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 18:57:13 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 18:57:13 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:13 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 18:57:13 | Оружие: Gauss flayer
2026-03-12 18:57:13 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:13 | BS оружия: 4+
2026-03-12 18:57:13 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 18:57:13 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:13 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:13 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 18:57:13 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:13 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:13 | Правило: Overwatch: попадания только на 6+
2026-03-12 18:57:13 | Эффект: benefit of cover
2026-03-12 18:57:13 | Hit rolls:    [5, 3, 1, 4, 3, 5, 2, 4, 5, 3]  -> hits: 0
2026-03-12 18:57:13 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 18:57:13 | FX: найден итог урона = 0.0.
2026-03-12 18:57:13 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-12 18:57:13 | FX: позиция эффекта start=(276.0,708.0) end=(1164.0,804.0).
2026-03-12 18:57:13 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 18:57:13 | 📌 -------------------------

2026-03-12 18:57:14 | REQ: move cell accepted (RMB) x=36, y=25, mode=advance
2026-03-12 18:57:14 | [MODEL][MOVEMENT] Overwatch невозможен: недостаточно CP.
2026-03-12 18:57:14 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:14 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:14 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:14 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:14 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:14 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:14 | Нет доступных целей для чарджа.
2026-03-12 18:57:14 | --- ФАЗА БОЯ ---
2026-03-12 18:57:14 | --- ХОД MODEL ---
2026-03-12 18:57:14 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:14 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 8). Выбор: left, advance=нет, distance=5
2026-03-12 18:57:14 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 3)
2026-03-12 18:57:14 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-12 18:57:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 11). Выбор: left, advance=нет, distance=4
2026-03-12 18:57:14 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 7)
2026-03-12 18:57:14 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:17 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 18:57:17 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 18:57:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 18:57:17 | [COVER][SHOOTING] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 18:57:17 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:17 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 18:57:17 | 
🎲 Бросок сейвы (save): 3D6
2026-03-12 18:57:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (shooting)
2026-03-12 18:57:17 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=17, need<=3).
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 18:57:17 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 18:57:17 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 18:57:17 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:17 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 18:57:17 | Оружие: Gauss flayer
2026-03-12 18:57:17 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:17 | BS оружия: 4+
2026-03-12 18:57:17 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:17 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:17 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 18:57:17 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:17 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:17 | Эффект: benefit of cover
2026-03-12 18:57:17 | Hit rolls:    [3, 6, 3, 6, 6, 2, 3, 3, 5, 1]  -> hits: 4 (crits: 3)
2026-03-12 18:57:17 | Wound rolls:  [1]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 3 = 3
2026-03-12 18:57:17 | Save rolls:   [1, 2, 6]  (цель 3+) -> failed saves: 2
2026-03-12 18:57:17 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 18:57:17 | FX: найден итог урона = 2.0.
2026-03-12 18:57:17 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 18:57:17 | FX: позиция эффекта start=(276.0,708.0) end=(900.0,756.0).
2026-03-12 18:57:17 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 18:57:17 | 📌 -------------------------

2026-03-12 18:57:17 | Reward (шаг): стрельба delta=+0.110
2026-03-12 18:57:17 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:17 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 18:57:17 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 18:57:17 | [MODEL] Чардж: нет доступных целей
2026-03-12 18:57:17 | --- ФАЗА БОЯ ---
2026-03-12 18:57:17 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 18:57:17 | Reward (terrain/potential): gamma=0.990, phi_before=-0.033, phi_after=+0.000, delta=+0.033; cover=0.000->0.000, threat=-0.333->-0.000, guard=0.000->0.000
2026-03-12 18:57:17 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-12 18:57:17 | Reward (terrain/clamp): raw=+0.033, cap=±0.120, clamp не сработал
2026-03-12 18:57:17 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-12 18:57:17 | Итерация 0 завершена с наградой tensor([0.1433], device='cuda:0'), здоровье игрока [8.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 18:57:17 | {'model health': [10.0, 10.0], 'player health': [8.0, 10.0], 'model alive models': [10, 10], 'player alive models': [8, 10], 'modelCP': 1, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 18:57:17 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [8.0, 10.0]
CP MODEL: 1, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)

2026-03-12 18:57:18 | === БОЕВОЙ РАУНД 2 ===
2026-03-12 18:57:18 | --- ХОД PLAYER ---
2026-03-12 18:57:18 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:18 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 18:57:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 18:57:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=8, раны=[1, 1, 1, 1, 1, 1, 1, 1] всего=8
2026-03-12 18:57:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 18:57:21 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-12 18:57:21 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:21 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:22 | REQ: move cell accepted (RMB) x=26, y=32, mode=advance
2026-03-12 18:57:22 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:22 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 18:57:22 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:22 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-12 18:57:22 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 8. HP: 9.0 -> 8.0 (Overwatch)
2026-03-12 18:57:22 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-12 18:57:22 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 18:57:22 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 18:57:22 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 18:57:22 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:22 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 18:57:22 | Оружие: Gauss flayer
2026-03-12 18:57:22 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:22 | BS оружия: 4+
2026-03-12 18:57:22 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 18:57:22 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:22 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:22 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 18:57:22 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:22 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:22 | Правило: Overwatch: попадания только на 6+
2026-03-12 18:57:22 | Эффект: benefit of cover
2026-03-12 18:57:22 | Hit rolls:    [6, 4, 3, 2, 2, 1, 5, 3, 5, 3]  -> hits: 1 (crits: 1)
2026-03-12 18:57:22 | Save rolls:   [1]  (цель 3+) -> failed saves: 1
2026-03-12 18:57:22 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 18:57:22 | FX: найден итог урона = 1.0.
2026-03-12 18:57:22 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 18:57:22 | FX: позиция эффекта start=(84.0,468.0) end=(900.0,756.0).
2026-03-12 18:57:22 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 18:57:22 | 📌 -------------------------

2026-03-12 18:57:23 | REQ: move cell accepted (RMB) x=25, y=26, mode=advance
2026-03-12 18:57:23 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:23 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:23 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 18:57:23 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-12 18:57:23 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 18:57:23 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 18:57:23 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:23 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 18:57:23 | Оружие: Gauss flayer
2026-03-12 18:57:23 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:23 | BS оружия: 4+
2026-03-12 18:57:23 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 18:57:23 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:23 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:23 | Benefit of Cover: не активен.
2026-03-12 18:57:23 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:23 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:23 | Правило: Overwatch: попадания только на 6+
2026-03-12 18:57:23 | Hit rolls:    [6, 5, 3, 5, 5, 6, 5, 4, 1, 3]  -> hits: 2 (crits: 2)
2026-03-12 18:57:23 | Save rolls:   [5, 4]  (цель 4+) -> failed saves: 0
2026-03-12 18:57:23 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-12 18:57:23 | FX: найден итог урона = 0.0.
2026-03-12 18:57:23 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-12 18:57:23 | FX: позиция эффекта start=(84.0,468.0) end=(876.0,612.0).
2026-03-12 18:57:23 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 18:57:23 | 📌 -------------------------

2026-03-12 18:57:23 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:23 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:23 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:23 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:23 | Нет доступных целей для чарджа.
2026-03-12 18:57:23 | --- ФАЗА БОЯ ---
2026-03-12 18:57:23 | --- ХОД MODEL ---
2026-03-12 18:57:23 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:23 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:23 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (19, 3). Выбор: left, advance=нет, distance=3
2026-03-12 18:57:23 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (19, 0)
2026-03-12 18:57:23 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 7). Выбор: left, advance=нет, distance=4
2026-03-12 18:57:24 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (29, 3)
2026-03-12 18:57:24 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:25 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 18:57:25 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 18:57:25 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:25 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-12 18:57:25 | 
🎲 Бросок сейвы (save): 5D6
2026-03-12 18:57:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 6. HP: 8.0 -> 6.0 (shooting)
2026-03-12 18:57:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.060 (norm=0.100, dealt=2.00)
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.060 (norm=0.100, dealt=2.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.110
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 2.0
2026-03-12 18:57:25 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 18:57:25 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 18:57:25 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:25 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 18:57:25 | Оружие: Gauss flayer
2026-03-12 18:57:25 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:25 | BS оружия: 4+
2026-03-12 18:57:25 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:25 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:25 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 18:57:25 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:25 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:25 | Эффект: benefit of cover
2026-03-12 18:57:25 | Hit rolls:    [4, 6, 4, 3, 3, 5, 5, 5, 1, 4]  -> hits: 7 (crits: 1)
2026-03-12 18:57:25 | Wound rolls:  [2, 4, 2, 5, 4, 5]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 1 = 5
2026-03-12 18:57:25 | Save rolls:   [1, 6, 3, 2, 5]  (цель 3+) -> failed saves: 2
2026-03-12 18:57:25 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-12 18:57:25 | FX: найден итог урона = 2.0.
2026-03-12 18:57:25 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-12 18:57:25 | FX: позиция эффекта start=(84.0,468.0) end=(660.0,756.0).
2026-03-12 18:57:25 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 18:57:25 | 📌 -------------------------

2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 18:57:25 | [COVER][SHOOTING] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-12 18:57:25 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:25 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-12 18:57:25 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 18:57:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 5. HP: 6.0 -> 5.0 (shooting)
2026-03-12 18:57:25 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-12 18:57:25 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 18:57:25 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 18:57:25 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:25 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 18:57:25 | Оружие: Gauss flayer
2026-03-12 18:57:25 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:25 | BS оружия: 4+
2026-03-12 18:57:25 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:25 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:25 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-12 18:57:25 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:25 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:25 | Эффект: benefit of cover
2026-03-12 18:57:25 | Hit rolls:    [4, 5, 5, 6, 4, 3, 2, 5, 2, 3]  -> hits: 6 (crits: 1)
2026-03-12 18:57:25 | Wound rolls:  [6, 6, 3, 5, 2]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 1 = 4
2026-03-12 18:57:25 | Save rolls:   [1, 3, 6, 3]  (цель 3+) -> failed saves: 1
2026-03-12 18:57:25 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 18:57:25 | FX: найден итог урона = 1.0.
2026-03-12 18:57:25 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 18:57:25 | FX: позиция эффекта start=(180.0,708.0) end=(660.0,756.0).
2026-03-12 18:57:25 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 18:57:25 | 📌 -------------------------

2026-03-12 18:57:25 | Reward (шаг): стрельба delta=+0.190
2026-03-12 18:57:25 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:25 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 18:57:25 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 18:57:25 | [MODEL] Чардж: нет доступных целей
2026-03-12 18:57:25 | --- ФАЗА БОЯ ---
2026-03-12 18:57:25 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 18:57:25 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-12 18:57:25 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-12 18:57:25 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-12 18:57:25 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-12 18:57:25 | Итерация 1 завершена с наградой tensor([0.1707], device='cuda:0'), здоровье игрока [5.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-12 18:57:25 | {'model health': [10.0, 10.0], 'player health': [5.0, 10.0], 'model alive models': [10, 10], 'player alive models': [5, 10], 'modelCP': 1, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 18:57:25 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [5.0, 10.0]
CP MODEL: 1, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 2.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)

2026-03-12 18:57:26 | === БОЕВОЙ РАУНД 3 ===
2026-03-12 18:57:26 | --- ХОД PLAYER ---
2026-03-12 18:57:26 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:26 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-12 18:57:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-12 18:57:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-12 18:57:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-12 18:57:28 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-12 18:57:28 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:28 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:29 | REQ: move cell accepted (RMB) x=16, y=31, mode=advance
2026-03-12 18:57:29 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:29 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:29 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 18:57:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 5. HP: 6.0 -> 5.0 (Overwatch)
2026-03-12 18:57:29 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-12 18:57:29 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 18:57:29 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 18:57:29 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 18:57:29 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:29 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 18:57:29 | Оружие: Gauss flayer
2026-03-12 18:57:29 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:29 | BS оружия: 4+
2026-03-12 18:57:29 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 18:57:29 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:29 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:29 | Benefit of Cover: не активен.
2026-03-12 18:57:29 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:29 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:29 | Правило: Overwatch: попадания только на 6+
2026-03-12 18:57:29 | Hit rolls:    [5, 6, 4, 6, 4, 1, 5, 5, 2, 4]  -> hits: 2 (crits: 2)
2026-03-12 18:57:29 | Save rolls:   [6, 1]  (цель 4+) -> failed saves: 1
2026-03-12 18:57:29 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 18:57:29 | FX: найден итог урона = 1.0.
2026-03-12 18:57:29 | FX: дубликат отчёта, эффект не создаём.
2026-03-12 18:57:29 | 📌 -------------------------

2026-03-12 18:57:30 | REQ: move cell accepted (RMB) x=14, y=28, mode=advance
2026-03-12 18:57:31 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-12 18:57:31 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 18:57:31 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-12 18:57:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-12 18:57:31 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-12 18:57:31 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-12 18:57:31 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-12 18:57:31 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-12 18:57:31 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:31 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-12 18:57:31 | Оружие: Gauss flayer
2026-03-12 18:57:31 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:31 | BS оружия: 4+
2026-03-12 18:57:31 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-12 18:57:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:31 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:31 | Benefit of Cover: не активен.
2026-03-12 18:57:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:31 | Правило: Overwatch: попадания только на 6+
2026-03-12 18:57:31 | Hit rolls:    [2, 6, 1, 1, 1, 5, 5, 4, 1, 5, 1, 3, 2, 4, 6, 4, 4, 5, 4, 3]  -> hits: 2 (crits: 2)
2026-03-12 18:57:31 | Save rolls:   [5, 2]  (цель 4+) -> failed saves: 1
2026-03-12 18:57:31 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 18:57:31 | FX: найден итог урона = 1.0.
2026-03-12 18:57:31 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-12 18:57:31 | FX: позиция эффекта start=(36.0,444.0) end=(612.0,636.0).
2026-03-12 18:57:31 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-12 18:57:31 | 📌 -------------------------

2026-03-12 18:57:31 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:31 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:31 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-12 18:57:31 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:31 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:31 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-12 18:57:31 | Нет доступных целей для чарджа.
2026-03-12 18:57:31 | --- ФАЗА БОЯ ---
2026-03-12 18:57:31 | --- ХОД MODEL ---
2026-03-12 18:57:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-12 18:57:31 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-12 18:57:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=29.069, d_after=29.069, d_best=18.069, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (18, 1). Выбор: stay, advance=нет, distance=0
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (18, 1)
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.090 (obj=0, d_before=28.460, d_after=28.460, d_best=17.460, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.75, reason=no_move_missed_progress)
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (29, 3). Выбор: stay, advance=нет, distance=0
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (29, 3)
2026-03-12 18:57:31 | Reward (VP/объекты, движение): hold=-0.180, proximity=0.000, total=-0.180
2026-03-12 18:57:31 | Reward (шаг): движение delta=-0.180
2026-03-12 18:57:31 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 18:57:31 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-12 18:57:31 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-12 18:57:31 | 
🎲 Бросок сейвы (save): 4D6
2026-03-12 18:57:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 4. HP: 5.0 -> 4.0 (shooting)
2026-03-12 18:57:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=21, need<=3).
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-12 18:57:31 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 18:57:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 18:57:31 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:31 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-12 18:57:31 | Оружие: Gauss flayer
2026-03-12 18:57:31 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:31 | BS оружия: 4+
2026-03-12 18:57:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:31 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:31 | Benefit of Cover: не активен.
2026-03-12 18:57:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:31 | Hit rolls:    [4, 6, 1, 4, 3, 5, 2, 3, 6, 5]  -> hits: 6 (crits: 2)
2026-03-12 18:57:31 | Wound rolls:  [6, 2, 6, 3]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-12 18:57:31 | Save rolls:   [1, 5, 4, 4]  (цель 4+) -> failed saves: 1
2026-03-12 18:57:31 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-12 18:57:31 | FX: найден итог урона = 1.0.
2026-03-12 18:57:31 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-12 18:57:31 | FX: позиция эффекта start=(36.0,444.0) end=(396.0,756.0).
2026-03-12 18:57:31 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-12 18:57:31 | 📌 -------------------------

2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-12 18:57:31 | 
🎲 Бросок на попадание (to hit): 20D6
2026-03-12 18:57:31 | 
🎲 Бросок на ранение (to wound): 5D6
2026-03-12 18:57:31 | 
🎲 Бросок сейвы (save): 5D6
2026-03-12 18:57:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 0. HP: 4.0 -> 0.0 (shooting)
2026-03-12 18:57:31 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 0. Причина: потери моделей.
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): kill_bonus=+0.400
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.400, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.570
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 5.0
2026-03-12 18:57:31 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-12 18:57:31 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-12 18:57:31 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-12 18:57:31 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-12 18:57:31 | Оружие: Gauss flayer
2026-03-12 18:57:31 | FX: найдена строка оружия: Gauss flayer.
2026-03-12 18:57:31 | BS оружия: 4+
2026-03-12 18:57:31 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-12 18:57:31 | Save цели: 4+ (invul: нет)
2026-03-12 18:57:31 | Benefit of Cover: не активен.
2026-03-12 18:57:31 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-12 18:57:31 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-12 18:57:31 | Hit rolls:    [4, 4, 1, 2, 3, 4, 6, 1, 6, 2, 5, 2, 1, 3, 4, 2, 2, 6, 2, 6]  -> hits: 9 (crits: 4)
2026-03-12 18:57:31 | Wound rolls:  [4, 2, 3, 2, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 4 = 5
2026-03-12 18:57:31 | Save rolls:   [1, 3, 3, 2, 2]  (цель 4+) -> failed saves: 5
2026-03-12 18:57:31 | 
✅ Итог по движку: прошло урона = 5.0
2026-03-12 18:57:31 | FX: найден итог урона = 5.0.
2026-03-12 18:57:31 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=5.0).
2026-03-12 18:57:31 | FX: позиция эффекта start=(84.0,708.0) end=(396.0,756.0).
2026-03-12 18:57:31 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-12 18:57:31 | 📌 -------------------------

2026-03-12 18:57:31 | Reward (шаг): стрельба delta=+0.650
2026-03-12 18:57:31 | --- ФАЗА ЧАРДЖА ---
2026-03-12 18:57:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-12 18:57:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в 12": Unit 12 — Necrons Necron Warriors (x10 моделей). бросок: 2 + 1 = 3. Чардж пропущен при доступных целях (penalty=0).
2026-03-12 18:57:31 | --- ФАЗА БОЯ ---
2026-03-12 18:57:31 | [MODEL] Ближний бой: нет доступных атак
2026-03-12 18:57:31 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.033, delta=+0.034; cover=0.000->0.000, threat=-0.667->-0.333, guard=0.000->0.000
2026-03-12 18:57:31 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=2)
2026-03-12 18:57:31 | Reward (terrain/clamp): raw=+0.014, cap=±0.120, clamp не сработал
2026-03-12 18:57:31 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-12 18:57:31 | Итерация 2 завершена с наградой tensor([0.4837], device='cuda:0'), здоровье игрока [0.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-12 18:57:31 | {'model health': [10.0, 10.0], 'player health': [0.0, 9.0], 'model alive models': [10, 10], 'player alive models': [0, 9], 'modelCP': 1, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-12 18:57:31 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [0.0, 9.0]
CP MODEL: 1, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 5.0 раз(а)

2026-03-12 18:57:34 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 18:57:34 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель мертва. Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-12 18:57:34 | Модель победила!
2026-03-12 18:57:34 | FX: перепроигрываю 30 строк(и) лога.
