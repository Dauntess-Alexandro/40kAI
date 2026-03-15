2026-03-14 18:08:24 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-14 18:08:24 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-14 18:08:24 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-14 18:08:24 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-14 18:08:25 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-14 18:08:25 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-683909.pickle
2026-03-14 18:08:25 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-683909.pth
2026-03-14 18:08:25 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-14 18:08:34 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-03-14 18:08:34 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-14 18:08:34 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-14 18:08:34 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-14 18:08:34 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-14 18:08:34 | [DEPLOY] Order: model first, alternating
2026-03-14 18:08:34 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-14 18:08:34 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1083, coord=(18,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-14 18:08:34 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (18,3)
2026-03-14 18:08:34 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-14 18:08:35 | REQ: deploy cell accepted x=50, y=32
2026-03-14 18:08:35 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,50)
2026-03-14 18:08:35 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,50)
2026-03-14 18:08:35 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-14 18:08:35 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1623, coord=(27,3), attempt=1, reward=+0.000, score_before=0.397, score_after=0.397, reward_delta=+0.000, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-14 18:08:35 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (27,3)
2026-03-14 18:08:35 | REQ: deploy cell accepted x=49, y=19
2026-03-14 18:08:36 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-03-14 18:08:36 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (19,49)
2026-03-14 18:08:36 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.020 total_deploy_reward=+0.020 avg_forward=0.054 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-14 18:08:36 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.0198659834450138, 'units': 2, 'total_deploy_reward': 0.0198659834450138, 'forward_sum': 0.10847457627118645, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.054237288135593226, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-14 18:08:36 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-14 18:08:36 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-14 18:08:36 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-14 18:08:36 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-14 18:08:36 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-14 18:08:36 | FX: перепроигрываю 30 строк(и) лога.
2026-03-14 18:08:37 | === БОЕВОЙ РАУНД 1 ===
2026-03-14 18:08:37 | --- ХОД PLAYER ---
2026-03-14 18:08:37 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 18:08:37 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 18:08:37 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 18:08:46 | REQ: move cell accepted (RMB) x=39, y=31, mode=advance
2026-03-14 18:08:46 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-14 18:08:47 | REQ: move cell accepted (RMB) x=38, y=23, mode=advance
2026-03-14 18:08:48 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-14 18:08:48 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 18:08:48 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 18:08:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 18:08:48 | --- ФАЗА ЧАРДЖА ---
2026-03-14 18:08:48 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 18:08:48 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 18:08:48 | Нет доступных целей для чарджа.
2026-03-14 18:08:48 | --- ФАЗА БОЯ ---
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | --- ХОД MODEL ---
2026-03-14 18:08:48 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 18:08:48 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 18:08:48 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 18:08:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.074, d_after=27.074, d_best=16.074, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-14 18:08:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (18, 3). Выбор: stay, advance=нет, distance=0
2026-03-14 18:08:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (18, 3)
2026-03-14 18:08:48 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.893, d_after=27.893, d_best=16.893, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-14 18:08:48 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 3). Выбор: stay, advance=нет, distance=0
2026-03-14 18:08:48 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (27, 3)
2026-03-14 18:08:48 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-14 18:08:48 | Reward (шаг): движение delta=-0.120
2026-03-14 18:08:48 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=32.00, range=24.00, delta=+8.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-14 18:08:48 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-14 18:08:48 | --- ФАЗА ЧАРДЖА ---
2026-03-14 18:08:48 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-14 18:08:48 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-14 18:08:48 | [MODEL] Чардж: нет доступных целей
2026-03-14 18:08:48 | --- ФАЗА БОЯ ---
2026-03-14 18:08:48 | [MODEL] Ближний бой: нет доступных атак
2026-03-14 18:08:48 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=27.073972741361768->27.073972741361768, hold_penalty_events=2
2026-03-14 18:08:48 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-14 18:08:48 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-14 18:08:48 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-14 18:08:48 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-14 18:08:48 | Итерация 0 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-14 18:08:48 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-14 18:08:48 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-14 18:08:49 | === БОЕВОЙ РАУНД 2 ===
2026-03-14 18:08:49 | --- ХОД PLAYER ---
2026-03-14 18:08:49 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 18:08:49 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 18:08:49 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 18:08:50 | REQ: move cell accepted (RMB) x=28, y=32, mode=advance
2026-03-14 18:08:51 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-14 18:08:51 | [COVER][MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-14 18:08:51 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 18:08:51 | 
🎲 Бросок сейвы (save): 5D6
2026-03-14 18:08:51 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-14 18:08:51 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-14 18:08:51 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-14 18:08:51 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-14 18:08:51 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 18:08:51 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-14 18:08:51 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-14 18:08:51 | Оружие: Gauss flayer
2026-03-14 18:08:51 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 18:08:51 | BS оружия: 4+
2026-03-14 18:08:51 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-14 18:08:51 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 18:08:51 | Save цели: 4+ (invul: нет)
2026-03-14 18:08:51 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-14 18:08:51 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 18:08:51 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 18:08:51 | Правило: Overwatch: попадания только на 6+
2026-03-14 18:08:51 | Эффект: benefit of cover
2026-03-14 18:08:51 | Hit rolls:    [6, 6, 3, 2, 3, 2, 6, 6, 1, 6]  -> hits: 5 (crits: 5)
2026-03-14 18:08:51 | Save rolls:   [5, 1, 3, 3, 4]  (цель 3+) -> failed saves: 1
2026-03-14 18:08:51 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-14 18:08:51 | FX: найден итог урона = 1.0.
2026-03-14 18:08:51 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-14 18:08:51 | FX: позиция эффекта start=(84.0,660.0) end=(948.0,756.0).
2026-03-14 18:08:51 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-14 18:08:51 | 📌 -------------------------

2026-03-14 18:08:52 | REQ: move cell accepted (RMB) x=27, y=27, mode=advance
2026-03-14 18:08:52 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-14 18:08:52 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 18:08:52 | 
🎲 Бросок сейвы (save): 1D6
2026-03-14 18:08:52 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-14 18:08:52 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-14 18:08:52 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-14 18:08:52 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-14 18:08:52 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 18:08:52 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-14 18:08:52 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-14 18:08:52 | Оружие: Gauss flayer
2026-03-14 18:08:52 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 18:08:52 | BS оружия: 4+
2026-03-14 18:08:52 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-14 18:08:52 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 18:08:52 | Save цели: 4+ (invul: нет)
2026-03-14 18:08:52 | Benefit of Cover: не активен.
2026-03-14 18:08:52 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 18:08:52 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 18:08:52 | Правило: Overwatch: попадания только на 6+
2026-03-14 18:08:52 | Hit rolls:    [5, 3, 3, 4, 6, 3, 4, 2, 1, 4]  -> hits: 1 (crits: 1)
2026-03-14 18:08:52 | Save rolls:   [3]  (цель 4+) -> failed saves: 1
2026-03-14 18:08:52 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-14 18:08:52 | FX: найден итог урона = 1.0.
2026-03-14 18:08:52 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=1.0).
2026-03-14 18:08:52 | FX: позиция эффекта start=(84.0,444.0) end=(924.0,564.0).
2026-03-14 18:08:52 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-14 18:08:52 | 📌 -------------------------

2026-03-14 18:08:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 18:08:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 18:08:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-14 18:08:52 | --- ФАЗА ЧАРДЖА ---
2026-03-14 18:08:52 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 18:08:52 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-14 18:08:52 | Нет доступных целей для чарджа.
2026-03-14 18:08:52 | --- ФАЗА БОЯ ---
2026-03-14 18:08:52 | --- ХОД MODEL ---
2026-03-14 18:08:52 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 18:08:52 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 18:08:52 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.074, d_after=27.074, d_best=16.074, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (18, 3). Выбор: stay, advance=нет, distance=0
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (18, 3)
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=27.893, d_after=27.893, d_best=16.893, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (27, 3). Выбор: stay, advance=нет, distance=0
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (27, 3)
2026-03-14 18:08:52 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-14 18:08:52 | Reward (шаг): движение delta=-0.120
2026-03-14 18:08:52 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-14 18:08:52 | [COVER][SHOOTING] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-14 18:08:52 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 18:08:52 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-14 18:08:52 | 
🎲 Бросок сейвы (save): 2D6
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.000 (norm=0.000, dealt=0.00), kill=0.000, overkill=-0.000, quality=0.000, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.000
2026-03-14 18:08:52 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 0.0
2026-03-14 18:08:52 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-14 18:08:52 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 18:08:52 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-14 18:08:52 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-14 18:08:52 | Оружие: Gauss flayer
2026-03-14 18:08:52 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 18:08:52 | BS оружия: 4+
2026-03-14 18:08:52 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 18:08:52 | Save цели: 4+ (invul: нет)
2026-03-14 18:08:52 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-14 18:08:52 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 18:08:52 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 18:08:52 | Эффект: benefit of cover
2026-03-14 18:08:52 | Hit rolls:    [2, 6, 4, 6, 3, 1, 3, 3, 1, 1]  -> hits: 3 (crits: 2)
2026-03-14 18:08:52 | Wound rolls:  [2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-14 18:08:52 | Save rolls:   [5, 6]  (цель 3+) -> failed saves: 0
2026-03-14 18:08:52 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-14 18:08:52 | FX: найден итог урона = 0.0.
2026-03-14 18:08:52 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=0.0).
2026-03-14 18:08:52 | FX: позиция эффекта start=(84.0,444.0) end=(684.0,780.0).
2026-03-14 18:08:52 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-14 18:08:52 | 📌 -------------------------

2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-14 18:08:52 | [COVER][SHOOTING] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-14 18:08:52 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 18:08:52 | 
🎲 Бросок на ранение (to wound): 6D6
2026-03-14 18:08:52 | 
🎲 Бросок сейвы (save): 7D6
2026-03-14 18:08:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 3. Осталось: 6. HP: 9.0 -> 6.0 (shooting)
2026-03-14 18:08:52 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.090 (norm=0.150, dealt=3.00)
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=19, need<=3).
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.090 (norm=0.150, dealt=3.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.140
2026-03-14 18:08:52 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 3.0
2026-03-14 18:08:52 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-14 18:08:52 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-14 18:08:52 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-14 18:08:52 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-14 18:08:52 | Оружие: Gauss flayer
2026-03-14 18:08:52 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 18:08:52 | BS оружия: 4+
2026-03-14 18:08:52 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 18:08:52 | Save цели: 4+ (invul: нет)
2026-03-14 18:08:52 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-14 18:08:52 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 18:08:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 18:08:53 | Эффект: benefit of cover
2026-03-14 18:08:53 | Hit rolls:    [6, 1, 6, 5, 5, 4, 4, 4, 5, 6]  -> hits: 9 (crits: 3)
2026-03-14 18:08:53 | Wound rolls:  [6, 4, 6, 4, 2, 3]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 3 = 7
2026-03-14 18:08:53 | Save rolls:   [4, 5, 1, 5, 1, 5, 1]  (цель 3+) -> failed saves: 3
2026-03-14 18:08:53 | 
✅ Итог по движку: прошло урона = 3.0
2026-03-14 18:08:53 | FX: найден итог урона = 3.0.
2026-03-14 18:08:53 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=3.0).
2026-03-14 18:08:53 | FX: позиция эффекта start=(84.0,660.0) end=(684.0,780.0).
2026-03-14 18:08:53 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-14 18:08:53 | 📌 -------------------------

2026-03-14 18:08:53 | Reward (шаг): стрельба delta=+0.140
2026-03-14 18:08:53 | --- ФАЗА ЧАРДЖА ---
2026-03-14 18:08:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-14 18:08:53 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-14 18:08:53 | [MODEL] Чардж: нет доступных целей
2026-03-14 18:08:53 | --- ФАЗА БОЯ ---
2026-03-14 18:08:53 | [MODEL] Ближний бой: нет доступных атак
2026-03-14 18:08:53 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.067, delta=+0.001; cover=0.000->0.000, threat=-0.667->-0.667, guard=0.000->0.000
2026-03-14 18:08:53 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=4)
2026-03-14 18:08:53 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-14 18:08:53 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-14 18:08:53 | Итерация 1 завершена с наградой tensor([0.0007], device='cuda:0'), здоровье игрока [6.0, 9.0], здоровье модели [10.0, 10.0]
2026-03-14 18:08:53 | {'model health': [10.0, 10.0], 'player health': [6.0, 9.0], 'model alive models': [10, 10], 'player alive models': [6, 9], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-14 18:08:53 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [6.0, 9.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 0.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 3.0 раз(а)

2026-03-14 18:08:57 | === БОЕВОЙ РАУНД 3 ===
2026-03-14 18:08:57 | --- ХОД PLAYER ---
2026-03-14 18:08:57 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-14 18:08:57 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-14 18:08:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-14 18:08:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-14 18:08:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 18:08:58 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-14 18:08:58 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-14 18:09:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-14 18:09:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-14 18:09:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-14 18:09:00 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-14 18:09:00 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-14 18:09:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-14 18:09:14 | REQ: move cell accepted (RMB) x=29, y=33, mode=normal
2026-03-14 18:09:15 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-14 18:09:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-14 18:09:15 | 
🎲 Бросок сейвы (save): 3D6
2026-03-14 18:09:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 5. HP: 7.0 -> 5.0 (Overwatch)
2026-03-14 18:09:15 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-14 18:09:15 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-14 18:09:15 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-14 18:09:15 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-14 18:09:15 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-14 18:09:15 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-14 18:09:15 | Оружие: Gauss flayer
2026-03-14 18:09:15 | FX: найдена строка оружия: Gauss flayer.
2026-03-14 18:09:15 | BS оружия: 4+
2026-03-14 18:09:15 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-14 18:09:15 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-14 18:09:15 | Save цели: 4+ (invul: нет)
2026-03-14 18:09:15 | Benefit of Cover: не активен.
2026-03-14 18:09:15 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-14 18:09:15 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-14 18:09:15 | Правило: Overwatch: попадания только на 6+
2026-03-14 18:09:15 | Hit rolls:    [6, 2, 3, 3, 2, 6, 3, 4, 5, 6]  -> hits: 3 (crits: 3)
2026-03-14 18:09:15 | Save rolls:   [6, 3, 2]  (цель 4+) -> failed saves: 2
2026-03-14 18:09:15 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-14 18:09:15 | FX: найден итог урона = 2.0.
2026-03-14 18:09:15 | FX: создан FxShotEvent (attacker=22, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-14 18:09:15 | FX: позиция эффекта start=(84.0,660.0) end=(684.0,780.0).
2026-03-14 18:09:15 | FX: эффект добавлен в рендер (attacker=22, target=11).
2026-03-14 18:09:15 | 📌 -------------------------

2026-03-15 10:45:11 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-15 10:45:11 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-15 10:45:11 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-15 10:45:11 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-15 10:45:12 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-15 10:45:13 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-683909.pickle
2026-03-15 10:45:13 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-8-683909.pth
2026-03-15 10:45:13 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-15 10:45:17 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-15 10:45:17 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-15 10:45:17 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-15 10:45:17 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-15 10:45:17 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-15 10:45:17 | [DEPLOY] Order: model first, alternating
2026-03-15 10:45:17 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-15 10:45:17 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=303, coord=(5,3), attempt=1, reward=+0.020, score_before=0.000, score_after=0.397, reward_delta=+0.020, forward=0.054, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-15 10:45:17 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (5,3)
2026-03-15 10:45:17 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-15 10:45:18 | REQ: deploy cell accepted x=50, y=32
2026-03-15 10:45:18 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,50)
2026-03-15 10:45:18 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (32,50)
2026-03-15 10:45:18 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-15 10:45:18 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=1268, coord=(21,8), attempt=1, reward=+0.001, score_before=0.397, score_after=0.417, reward_delta=+0.001, forward=0.097, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-15 10:45:18 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (21,8)
2026-03-15 10:45:19 | REQ: deploy cell accepted x=47, y=23
2026-03-15 10:45:21 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,47)
2026-03-15 10:45:21 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (23,47)
2026-03-15 10:45:21 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.075 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-15 10:45:21 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.020851399290500592, 'units': 2, 'total_deploy_reward': 0.020851399290500592, 'forward_sum': 0.15084745762711865, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.07542372881355933, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-15 10:45:21 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-15 10:45:21 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-15 10:45:21 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-15 10:45:21 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-15 10:45:21 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-15 10:45:21 | FX: перепроигрываю 30 строк(и) лога.
2026-03-15 10:45:22 | === БОЕВОЙ РАУНД 1 ===
2026-03-15 10:45:22 | --- ХОД PLAYER ---
2026-03-15 10:45:22 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-15 10:45:22 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-15 10:45:22 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-15 10:45:24 | REQ: move cell accepted (RMB) x=39, y=31, mode=advance
2026-03-15 10:45:24 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-15 10:45:31 | REQ: move cell accepted (RMB) x=36, y=23, mode=advance
2026-03-15 10:45:32 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-15 10:45:32 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-15 10:45:32 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-15 10:45:32 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-15 10:45:32 | --- ФАЗА ЧАРДЖА ---
2026-03-15 10:45:32 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-15 10:45:32 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-15 10:45:32 | Нет доступных целей для чарджа.
2026-03-15 10:45:32 | --- ФАЗА БОЯ ---
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | --- ХОД MODEL ---
2026-03-15 10:45:32 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-15 10:45:32 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-15 10:45:32 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-15 10:45:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=30.887, d_after=30.887, d_best=19.887, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-15 10:45:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (5, 3). Выбор: stay, advance=нет, distance=0
2026-03-15 10:45:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (5, 3)
2026-03-15 10:45:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (VP/объекты): hold_penalty=-0.060 (obj=0, d_before=22.023, d_after=22.023, d_best=11.023, max_reach=11.000, could_reach_objective=0, severity=1.000, round_scale=0.50, reason=no_move_missed_progress)
2026-03-15 10:45:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (21, 8). Выбор: stay, advance=нет, distance=0
2026-03-15 10:45:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Движение пропущено (no move). Позиция после: (21, 8)
2026-03-15 10:45:32 | Reward (VP/объекты, движение): hold=-0.120, proximity=0.000, total=-0.120
2026-03-15 10:45:32 | Reward (шаг): движение delta=-0.120
2026-03-15 10:45:32 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=33.00, range=24.00, delta=+9.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-15 10:45:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-15 10:45:32 | --- ФАЗА ЧАРДЖА ---
2026-03-15 10:45:32 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-15 10:45:32 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-15 10:45:32 | [MODEL] Чардж: нет доступных целей
2026-03-15 10:45:32 | --- ФАЗА БОЯ ---
2026-03-15 10:45:32 | [MODEL] Ближний бой: нет доступных атак
2026-03-15 10:45:32 | Reward (idle вне цели): skip, reason=hold_penalty_already_applied, near_obj=0, vp_changed=0, control_changed=0, damage=0.00, kills=0, moved_closer=0, min_dist=22.02271554554524->22.02271554554524, hold_penalty_events=2
2026-03-15 10:45:32 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-15 10:45:32 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-15 10:45:32 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-15 10:45:32 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-15 10:45:32 | Итерация 0 завершена с наградой tensor([-0.1200], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-15 10:45:32 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-15 10:45:32 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

