2026-03-10 15:03:24 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-10 15:03:24 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-10 15:03:24 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-10 15:03:24 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-10 15:03:25 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 15:03:34 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-23-822656.pickle
2026-03-10 15:03:34 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-23-822656.pth
2026-03-10 15:03:34 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-10 15:19:52 | Roll-off Attacker/Defender: enemy=1 model=6 -> attacker=model
2026-03-10 15:19:52 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-10 15:19:52 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-10 15:19:52 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-10 15:19:52 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-10 15:19:52 | [DEPLOY] Order: model first, alternating
2026-03-10 15:19:52 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 15:19:52 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1506, coord=(25,6), attempt=1, reward=+0.021, score_before=0.000, score_after=0.421, reward_delta=+0.021, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 15:19:52 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (25,6)
2026-03-10 15:19:52 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 15:19:54 | REQ: deploy cell accepted x=50, y=28
2026-03-10 15:19:54 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,50)
2026-03-10 15:19:54 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (28,50)
2026-03-10 15:19:54 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 15:19:54 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=67, coord=(1,7), attempt=1, reward=-0.002, score_before=0.421, score_after=0.378, reward_delta=-0.002, forward=0.114, spread=1.000, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 15:19:54 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (1,7)
2026-03-10 15:19:55 | REQ: deploy cell accepted x=51, y=12
2026-03-10 15:19:55 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (12,51)
2026-03-10 15:19:55 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (12,51)
2026-03-10 15:19:55 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.019 total_deploy_reward=+0.019 avg_forward=0.109 avg_spread=1.000 avg_edge=0.750 avg_cover=0.000
2026-03-10 15:19:55 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.01891998423334647, 'units': 2, 'total_deploy_reward': 0.01891998423334647, 'forward_sum': 0.2186440677966102, 'spread_sum': 2.0, 'edge_sum': 1.5, 'cover_sum': 0.0, 'avg_forward': 0.1093220338983051, 'avg_spread': 1.0, 'avg_edge': 0.75, 'avg_cover': 0.0}
2026-03-10 15:19:55 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-10 15:19:55 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-10 15:19:55 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-10 15:19:55 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 15:19:55 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-10 15:19:55 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 15:19:58 | === БОЕВОЙ РАУНД 1 ===
2026-03-10 15:19:58 | --- ХОД PLAYER ---
2026-03-10 15:19:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:19:58 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:19:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:02 | REQ: move cell accepted (RMB) x=39, y=31, mode=advance
2026-03-10 15:20:02 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:03 | REQ: move cell accepted (RMB) x=40, y=18, mode=advance
2026-03-10 15:20:04 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:04 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 15:20:04 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 15:20:04 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:04 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 15:20:04 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 15:20:04 | Нет доступных целей для чарджа.
2026-03-10 15:20:04 | --- ФАЗА БОЯ ---
2026-03-10 15:20:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:04 | --- ХОД MODEL ---
2026-03-10 15:20:04 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:04 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:04 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (25, 6). Выбор: up, advance=да, бросок=2, макс=7, distance=7
2026-03-10 15:20:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (18, 6)
2026-03-10 15:20:04 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 7). Выбор: up, advance=нет, distance=1
2026-03-10 15:20:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 7)
2026-03-10 15:20:04 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:04 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-10 15:20:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:04 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 15:20:04 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:04 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-10 15:20:04 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 15:20:04 | [MODEL] Чардж: нет доступных целей
2026-03-10 15:20:04 | --- ФАЗА БОЯ ---
2026-03-10 15:20:04 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 15:20:04 | Reward (progress к objective): d_before=24.515, d_after=24.083, delta=0.432, norm=0.072, bonus=+0.002
2026-03-10 15:20:04 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-10 15:20:04 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-10 15:20:04 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-10 15:20:04 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-10 15:20:04 | Итерация 0 завершена с наградой tensor([0.0022], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 15:20:04 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 15:20:04 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-10 15:20:05 | === БОЕВОЙ РАУНД 2 ===
2026-03-10 15:20:05 | --- ХОД PLAYER ---
2026-03-10 15:20:05 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:05 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:05 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:06 | REQ: move cell accepted (RMB) x=29, y=32, mode=advance
2026-03-10 15:20:07 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:07 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:07 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 15:20:07 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 15:20:07 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 15:20:07 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 15:20:07 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 15:20:07 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 15:20:07 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:07 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 15:20:07 | Оружие: Gauss flayer
2026-03-10 15:20:07 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:07 | BS оружия: 4+
2026-03-10 15:20:07 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:07 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:07 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:07 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:07 | Правило: Overwatch: попадания только на 6+
2026-03-10 15:20:07 | Hit rolls:    [3, 6, 2, 5, 5, 1, 3, 1, 3, 4]  -> hits: 4 (crits: 1)
2026-03-10 15:20:07 | Wound rolls:  [3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-10 15:20:07 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 15:20:07 | FX: найден итог урона = 1.0.
2026-03-10 15:20:07 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 15:20:07 | FX: позиция эффекта start=(156.0,444.0) end=(948.0,756.0).
2026-03-10 15:20:07 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 15:20:07 | 📌 -------------------------

2026-03-10 15:20:08 | REQ: move cell accepted (RMB) x=36, y=15, mode=normal
2026-03-10 15:20:08 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:08 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 15:20:08 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 21 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:08 | [TARGET][SHOOT] Unit 12 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:08 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:08 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 15:20:08 | Нет доступных целей для чарджа.
2026-03-10 15:20:08 | --- ФАЗА БОЯ ---
2026-03-10 15:20:08 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:08 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:08 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:08 | --- ХОД MODEL ---
2026-03-10 15:20:08 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:08 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:08 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (18, 6). Выбор: up, advance=нет, distance=1
2026-03-10 15:20:08 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (17, 6)
2026-03-10 15:20:08 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 6). Выбор: up, advance=нет, distance=1
2026-03-10 15:20:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 6)
2026-03-10 15:20:11 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 15:20:11 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:11 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 15:20:11 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:11 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-10 15:20:11 | 
🎲 Бросок сейвы (save): 6D6
2026-03-10 15:20:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 5. HP: 9.0 -> 5.0 (shooting)
2026-03-10 15:20:11 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=16, need<=3).
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.170
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 4.0
2026-03-10 15:20:11 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 15:20:11 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 15:20:11 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:11 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 15:20:11 | Оружие: Gauss flayer
2026-03-10 15:20:11 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:11 | BS оружия: 4+
2026-03-10 15:20:11 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:11 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:11 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:11 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:11 | Hit rolls:    [1, 3, 3, 3, 6, 4, 5, 4, 5, 6]  -> hits: 6 (crits: 2)
2026-03-10 15:20:11 | Wound rolls:  [4, 4, 4, 5]  (цель 4+) -> rolled wounds: 4 + auto(w/LETHAL): 2 = 6
2026-03-10 15:20:11 | Save rolls:   [6, 2, 4, 3, 1, 2]  (цель 4+) -> failed saves: 4
2026-03-10 15:20:11 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-10 15:20:11 | FX: найден итог урона = 4.0.
2026-03-10 15:20:11 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=4.0).
2026-03-10 15:20:11 | FX: позиция эффекта start=(156.0,444.0) end=(708.0,780.0).
2026-03-10 15:20:11 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 15:20:11 | 📌 -------------------------

2026-03-10 15:20:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:11 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=28.00, range=24.00, delta=+4.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 15:20:11 | Reward (шаг): стрельба delta=+0.170
2026-03-10 15:20:11 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:11 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 15:20:11 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 15:20:11 | [MODEL] Чардж: нет доступных целей
2026-03-10 15:20:11 | --- ФАЗА БОЯ ---
2026-03-10 15:20:11 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 15:20:11 | Reward (terrain/potential): gamma=0.990, phi_before=-0.017, phi_after=-0.017, delta=+0.000; cover=0.000->0.000, threat=-0.167->-0.167, guard=0.000->0.000
2026-03-10 15:20:11 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=1)
2026-03-10 15:20:11 | Reward (terrain/clamp): raw=-0.010, cap=±0.120, clamp не сработал
2026-03-10 15:20:11 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-10 15:20:11 | Итерация 1 завершена с наградой tensor([0.1602], device='cuda:0'), здоровье игрока [5.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 15:20:11 | {'model health': [10.0, 10.0], 'player health': [5.0, 10.0], 'model alive models': [10, 10], 'player alive models': [5, 10], 'modelCP': 3, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 15:20:11 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [5.0, 10.0]
CP MODEL: 3, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 4.0 раз(а)

2026-03-10 15:20:12 | === БОЕВОЙ РАУНД 3 ===
2026-03-10 15:20:12 | --- ХОД PLAYER ---
2026-03-10 15:20:12 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:12 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 15:20:14 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 15:20:14 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-10 15:20:14 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 15:20:14 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-10 15:20:14 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:14 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:18 | REQ: move cell accepted (RMB) x=27, y=32, mode=normal
2026-03-10 15:20:19 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:19 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:19 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-10 15:20:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 4. HP: 6.0 -> 4.0 (Overwatch)
2026-03-10 15:20:19 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 4. Причина: потери моделей.
2026-03-10 15:20:19 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-10 15:20:19 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 15:20:19 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 15:20:19 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:19 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 15:20:19 | Оружие: Gauss flayer
2026-03-10 15:20:19 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:19 | BS оружия: 4+
2026-03-10 15:20:19 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:19 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:19 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:19 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:19 | Правило: Overwatch: попадания только на 6+
2026-03-10 15:20:19 | Hit rolls:    [5, 2, 6, 1, 6, 5, 3, 1, 6, 5]  -> hits: 6 (crits: 3)
2026-03-10 15:20:19 | Wound rolls:  [5, 1, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-10 15:20:19 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-10 15:20:19 | FX: найден итог урона = 2.0.
2026-03-10 15:20:19 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-10 15:20:19 | FX: позиция эффекта start=(156.0,420.0) end=(708.0,780.0).
2026-03-10 15:20:19 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 15:20:19 | 📌 -------------------------

2026-03-10 15:20:28 | REQ: move cell accepted (RMB) x=25, y=11, mode=advance
2026-03-10 15:20:28 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:28 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:28 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 15:20:28 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-10 15:20:28 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 15:20:28 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 15:20:28 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:28 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-10 15:20:28 | Оружие: Gauss flayer
2026-03-10 15:20:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:28 | BS оружия: 4+
2026-03-10 15:20:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:28 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:28 | Правило: Overwatch: попадания только на 6+
2026-03-10 15:20:28 | Hit rolls:    [5, 6, 5, 4, 4, 2, 6, 1, 2, 5]  -> hits: 7 (crits: 2)
2026-03-10 15:20:28 | Wound rolls:  [5, 4]  (цель 4+) -> rolled wounds: 2 + auto(w/LETHAL): 2 = 4
2026-03-10 15:20:28 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-10 15:20:28 | FX: найден итог урона = 0.0.
2026-03-10 15:20:28 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-10 15:20:28 | FX: позиция эффекта start=(156.0,420.0) end=(876.0,372.0).
2026-03-10 15:20:28 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-10 15:20:28 | 📌 -------------------------

2026-03-10 15:20:28 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:28 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:28 | REQ: валидные цели стрельбы для Unit 11: [21] | отфильтрованы: [22: цель вне дальности: range 30.00 > 24.00 (out_of_range by +6.00)]
2026-03-10 15:20:34 | 
🎲 Бросок на попадание (to hit): 4D6
2026-03-10 15:20:37 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 15:20:40 | 
🎲 Бросок сейвы (save): 1D6
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 15:20:42 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:42 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 15:20:42 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 15:20:42 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:42 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-10 15:20:42 | Оружие: Gauss flayer
2026-03-10 15:20:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:42 | BS оружия: 4+
2026-03-10 15:20:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:42 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:42 | Hit rolls:    [2, 3, 4, 5]  -> hits: 2
2026-03-10 15:20:42 | Wound rolls:  [3, 4]  (цель 4+) -> wounds: 1
2026-03-10 15:20:42 | Save rolls:   [3]  (цель 4+) -> failed saves: 1
2026-03-10 15:20:42 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 15:20:42 | FX: найден итог урона = 1.0.
2026-03-10 15:20:42 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=1.0).
2026-03-10 15:20:42 | FX: позиция эффекта start=(660.0,780.0) end=(156.0,420.0).
2026-03-10 15:20:42 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-10 15:20:42 | 📌 -------------------------

2026-03-10 15:20:42 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 15:20:42 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:42 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 15:20:42 | Нет доступных целей для чарджа.
2026-03-10 15:20:42 | --- ФАЗА БОЯ ---
2026-03-10 15:20:42 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:42 | --- ХОД MODEL ---
2026-03-10 15:20:42 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 3
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-10 15:20:42 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (17, 6). Выбор: up, advance=нет, distance=1
2026-03-10 15:20:42 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (16, 6)
2026-03-10 15:20:42 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (1, 5). Выбор: up, advance=нет, distance=1
2026-03-10 15:20:44 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (0, 5)
2026-03-10 15:20:44 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-10 15:20:45 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 11 — Necrons Necron Warriors (x10 моделей), Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 11 — Necrons Necron Warriors (x10 моделей) (причина: цель с меньшим HP)
2026-03-10 15:20:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:45 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-10 15:20:45 | 
🎲 Бросок сейвы (save): 2D6
2026-03-10 15:20:45 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 3. HP: 4.0 -> 3.0 (shooting)
2026-03-10 15:20:45 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 3. Причина: потери моделей.
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.030 (norm=0.050, dealt=1.00)
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=16, need<=3).
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.030 (norm=0.050, dealt=1.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.080
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 11 — Necrons Necron Warriors (x10 моделей): 1.0
2026-03-10 15:20:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 15:20:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 15:20:45 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:45 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-10 15:20:45 | Оружие: Gauss flayer
2026-03-10 15:20:45 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:45 | BS оружия: 4+
2026-03-10 15:20:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:45 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:45 | Hit rolls:    [6, 2, 5, 3, 1, 2, 1, 5, 2, 6]  -> hits: 4 (crits: 2)
2026-03-10 15:20:45 | Wound rolls:  [3, 2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 2 = 2
2026-03-10 15:20:45 | Save rolls:   [2, 6]  (цель 4+) -> failed saves: 1
2026-03-10 15:20:45 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-10 15:20:45 | FX: найден итог урона = 1.0.
2026-03-10 15:20:45 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-10 15:20:45 | FX: позиция эффекта start=(156.0,420.0) end=(660.0,780.0).
2026-03-10 15:20:45 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-10 15:20:45 | 📌 -------------------------

2026-03-10 15:20:45 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=30.00, range=24.00, delta=+6.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Цели в дальности: Unit 12 — Necrons Necron Warriors (x10 моделей), выбрана: Unit 12 — Necrons Necron Warriors (x10 моделей) (причина: самая близкая)
2026-03-10 15:20:45 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 15:20:45 | 
🎲 Бросок на ранение (to wound): 4D6
2026-03-10 15:20:45 | 
🎲 Бросок сейвы (save): 5D6
2026-03-10 15:20:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 6. HP: 10.0 -> 6.0 (shooting)
2026-03-10 15:20:45 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 6. Причина: потери моделей.
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage_term=+0.120 (norm=0.200, dealt=4.00)
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): quality_bonus=+0.050
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (terrain event): бонус за выстрел из cover не начислен, причина: далеко от barricade (dist=18, need<=3).
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Reward (стрельба): damage=0.120 (norm=0.200, dealt=4.00), kill=0.000, overkill=-0.000, quality=0.050, obj_damage=0.000, obj_kill=0.000, action=0.000, terrain_event=0.000, total=0.170
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Итог урона по Unit 12 — Necrons Necron Warriors (x10 моделей): 4.0
2026-03-10 15:20:45 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-10 15:20:45 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-10 15:20:45 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-10 15:20:45 | FX: найдена строка стрельбы (attacker=22, target=12).
2026-03-10 15:20:45 | Оружие: Gauss flayer
2026-03-10 15:20:45 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 15:20:45 | BS оружия: 4+
2026-03-10 15:20:45 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 15:20:45 | Save цели: 4+ (invul: нет)
2026-03-10 15:20:45 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 15:20:45 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 15:20:45 | Hit rolls:    [2, 5, 6, 6, 5, 5, 3, 3, 4, 2]  -> hits: 6 (crits: 2)
2026-03-10 15:20:45 | Wound rolls:  [2, 4, 6, 5]  (цель 4+) -> rolled wounds: 3 + auto(w/LETHAL): 2 = 5
2026-03-10 15:20:45 | Save rolls:   [2, 3, 2, 4, 3]  (цель 4+) -> failed saves: 4
2026-03-10 15:20:45 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-10 15:20:45 | FX: найден итог урона = 4.0.
2026-03-10 15:20:45 | FX: создан FxShotEvent (attacker=22, target=12, weapon=Gauss flayer, damage=4.0).
2026-03-10 15:20:45 | FX: позиция эффекта start=(132.0,36.0) end=(612.0,276.0).
2026-03-10 15:20:45 | FX: эффект добавлен в рендер (attacker=22, target=12).
2026-03-10 15:20:45 | 📌 -------------------------

2026-03-10 15:20:45 | Reward (шаг): стрельба delta=+0.250
2026-03-10 15:20:45 | --- ФАЗА ЧАРДЖА ---
2026-03-10 15:20:45 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 15:20:45 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 15:20:45 | [MODEL] Чардж: нет доступных целей
2026-03-10 15:20:45 | --- ФАЗА БОЯ ---
2026-03-10 15:20:45 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 15:20:45 | Reward (terrain/potential): gamma=0.990, phi_before=-0.050, phi_after=-0.050, delta=+0.001; cover=0.000->0.000, threat=-0.500->-0.500, guard=0.000->0.000
2026-03-10 15:20:45 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=2, alive_units=2, threat_count=3)
2026-03-10 15:20:45 | Reward (terrain/clamp): raw=-0.019, cap=±0.120, clamp не сработал
2026-03-10 15:20:45 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-10 15:20:45 | Итерация 2 завершена с наградой tensor([0.2305], device='cuda:0'), здоровье игрока [3.0, 6.0], здоровье модели [10.0, 10.0]
2026-03-10 15:20:45 | {'model health': [10.0, 10.0], 'player health': [3.0, 6.0], 'model alive models': [10, 10], 'player alive models': [3, 6], 'modelCP': 3, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 15:20:45 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [3.0, 6.0]
CP MODEL: 3, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 0
Unit 21 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 11 — Necrons Necron Warriors (x10 моделей) 1.0 раз(а)
Unit 22 — Necrons Necron Warriors (x10 моделей) стреляет по Unit 12 — Necrons Necron Warriors (x10 моделей) 4.0 раз(а)

2026-03-10 15:20:47 | === БОЕВОЙ РАУНД 4 ===
2026-03-10 15:20:47 | --- ХОД PLAYER ---
2026-03-10 15:20:47 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 15:20:47 | Unit 11 — Necrons Necron Warriors (x10 моделей): ниже половины состава, тест Battle-shock.
2026-03-10 15:20:47 | Бросок 2D6...
2026-03-10 15:20:50 | Бросок: 1 2
2026-03-10 15:20:50 | Unit 11 — Necrons Necron Warriors (x10 моделей): тест Battle-shock провален.
2026-03-10 15:20:51 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 15:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 15:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=3, раны=[1, 1, 1] всего=3
2026-03-10 15:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 15:20:53 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=4, раны=[1, 1, 1, 1] всего=4
2026-03-10 15:20:53 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-10 15:20:55 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-10 15:20:55 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) До: моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-10 15:20:55 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-10 15:20:55 | [PLAYER] Unit 12 — Necrons Necron Warriors (x10 моделей) После:  моделей=7, раны=[1, 1, 1, 1, 1, 1, 1] всего=7
2026-03-10 15:20:55 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 15:20:55 | --- ФАЗА ДВИЖЕНИЯ ---
