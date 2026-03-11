2026-03-11 13:56:28 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-11 13:56:28 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-11 13:56:28 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-11 13:56:28 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-11 13:56:29 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 13:56:39 | [MODEL] pickle=models/M_Necrons_vs_P_Necrons\model-45-834651.pickle
2026-03-11 13:56:39 | [MODEL] checkpoint=models/M_Necrons_vs_P_Necrons\model-45-834651.pth
2026-03-11 13:56:39 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-11 13:56:55 | Roll-off Attacker/Defender: enemy=1 model=5 -> attacker=model
2026-03-11 13:56:55 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-11 13:56:55 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-11 13:56:55 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-11 13:56:55 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-11 13:56:55 | [DEPLOY] Order: model first, alternating
2026-03-11 13:56:55 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 13:56:55 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1987, coord=(33,7), attempt=1, reward=+0.021, score_before=0.000, score_after=0.429, reward_delta=+0.021, forward=0.122, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 13:56:55 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (33,7)
2026-03-11 13:56:55 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-11 13:56:55 | Ошибка деплоя: reason=outside_deploy_zone, x=40, y=35. Где: viewer/app.py (_on_cell_clicked). Что делать дальше: выберите клетку в зоне деплоя без коллизий.
2026-03-11 13:56:56 | REQ: deploy cell accepted x=50, y=33
2026-03-11 13:56:56 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,50)
2026-03-11 13:56:56 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (33,50)
2026-03-11 13:56:56 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-11 13:56:56 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=425, coord=(7,5), attempt=1, reward=-0.000, score_before=0.429, score_after=0.421, reward_delta=-0.000, forward=0.105, spread=1.000, edge=1.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-11 13:56:56 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (7,5)
2026-03-11 13:56:56 | REQ: deploy cell accepted x=48, y=20
2026-03-11 13:56:57 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-03-11 13:56:57 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (20,48)
2026-03-11 13:56:57 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.021 total_deploy_reward=+0.021 avg_forward=0.114 avg_spread=1.000 avg_edge=1.000 avg_cover=0.000
2026-03-11 13:56:57 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.021048482459597954, 'units': 2, 'total_deploy_reward': 0.021048482459597954, 'forward_sum': 0.22711864406779664, 'spread_sum': 2.0, 'edge_sum': 2.0, 'cover_sum': 0.0, 'avg_forward': 0.11355932203389832, 'avg_spread': 1.0, 'avg_edge': 1.0, 'avg_cover': 0.0}
2026-03-11 13:56:57 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-11 13:56:57 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-11 13:56:57 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-11 13:56:57 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 13:56:57 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-11 13:56:57 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 13:56:58 | === БОЕВОЙ РАУНД 1 ===
2026-03-11 13:56:58 | --- ХОД PLAYER ---
2026-03-11 13:56:58 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 13:56:58 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 13:56:58 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 13:56:59 | REQ: move cell accepted (RMB) x=39, y=32, mode=advance
2026-03-11 13:56:59 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 13:57:00 | REQ: move cell accepted (RMB) x=37, y=20, mode=advance
2026-03-11 13:57:00 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 13:57:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 13:57:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 13:57:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-11 13:57:00 | --- ФАЗА ЧАРДЖА ---
2026-03-11 13:57:00 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 13:57:00 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-11 13:57:00 | Нет доступных целей для чарджа.
2026-03-11 13:57:00 | --- ФАЗА БОЯ ---
2026-03-11 13:57:00 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:00 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:00 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:00 | --- ХОД MODEL ---
2026-03-11 13:57:00 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 13:57:00 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 13:57:00 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 13:57:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 7). Выбор: right, advance=нет, distance=4
2026-03-11 13:57:00 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 11)
2026-03-11 13:57:00 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 13:57:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 5). Выбор: right, advance=да, бросок=3, макс=8, distance=8
2026-03-11 13:57:00 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 13)
2026-03-11 13:57:00 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-11 13:57:00 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 13:57:01 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=29.00, range=24.00, delta=+5.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:01 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=27.00, range=24.00, delta=+3.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:57:01 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-11 13:57:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 13:57:01 | --- ФАЗА ЧАРДЖА ---
2026-03-11 13:57:01 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-11 13:57:01 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 13:57:01 | [MODEL] Чардж: нет доступных целей
2026-03-11 13:57:01 | --- ФАЗА БОЯ ---
2026-03-11 13:57:01 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 13:57:01 | Reward (progress к objective): d_before=26.420, d_after=21.401, delta=5.019, norm=0.836, bonus=+0.025
2026-03-11 13:57:01 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-11 13:57:01 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-11 13:57:01 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-11 13:57:01 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-11 13:57:01 | Итерация 0 завершена с наградой tensor([0.0251], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-11 13:57:01 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 13:57:01 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-11 13:57:02 | === БОЕВОЙ РАУНД 2 ===
2026-03-11 13:57:02 | --- ХОД PLAYER ---
2026-03-11 13:57:02 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 13:57:02 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 13:57:02 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 13:57:03 | REQ: move cell accepted (RMB) x=36, y=31, mode=normal
2026-03-11 13:57:03 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:57:03 | [COVER][MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-11 13:57:03 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 13:57:03 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-11 13:57:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-11 13:57:03 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 13:57:03 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-11 13:57:03 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 13:57:03 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:57:03 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:57:03 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 13:57:03 | Оружие: Gauss flayer
2026-03-11 13:57:03 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:57:03 | BS оружия: 4+
2026-03-11 13:57:03 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 13:57:03 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:57:03 | Save цели: 4+ (invul: нет)
2026-03-11 13:57:03 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-11 13:57:03 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:57:03 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:57:03 | Правило: Overwatch: попадания только на 6+
2026-03-11 13:57:03 | Эффект: benefit of cover
2026-03-11 13:57:03 | Hit rolls:    [1, 4, 4, 6, 4, 2, 1, 1, 2, 5]  -> hits: 1 (crits: 1)
2026-03-11 13:57:03 | Wound rolls:  [2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-11 13:57:03 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 13:57:03 | FX: найден итог урона = 1.0.
2026-03-11 13:57:03 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=1.0).
2026-03-11 13:57:03 | FX: позиция эффекта start=(276.0,804.0) end=(948.0,780.0).
2026-03-11 13:57:03 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 13:57:03 | 📌 -------------------------

2026-03-11 13:57:06 | REQ: move cell accepted (RMB) x=33, y=20, mode=normal
2026-03-11 13:57:06 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:57:06 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 13:57:06 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-11 13:57:06 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-11 13:57:06 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 13:57:06 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:57:06 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:57:06 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 13:57:06 | Оружие: Gauss flayer
2026-03-11 13:57:06 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:57:06 | BS оружия: 4+
2026-03-11 13:57:06 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 13:57:06 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:57:06 | Save цели: 4+ (invul: нет)
2026-03-11 13:57:06 | Benefit of Cover: не активен.
2026-03-11 13:57:06 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:57:06 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:57:06 | Правило: Overwatch: попадания только на 6+
2026-03-11 13:57:06 | Hit rolls:    [5, 6, 4, 1, 4, 2, 5, 3, 1, 3]  -> hits: 1 (crits: 1)
2026-03-11 13:57:06 | Wound rolls:  [5]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 1 = 2
2026-03-11 13:57:06 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 13:57:06 | FX: найден итог урона = 0.0.
2026-03-11 13:57:06 | FX: создан FxShotEvent (attacker=21, target=12, weapon=Gauss flayer, damage=0.0).
2026-03-11 13:57:06 | FX: позиция эффекта start=(276.0,804.0) end=(900.0,492.0).
2026-03-11 13:57:06 | FX: эффект добавлен в рендер (attacker=21, target=12).
2026-03-11 13:57:06 | 📌 -------------------------

2026-03-11 13:57:06 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 13:57:06 | REQ: валидные цели стрельбы для Unit 11: [21, 22] | отфильтрованы: [—]
2026-03-11 13:57:13 | 
🎲 Бросок на попадание (to hit): 9D6
2026-03-11 13:57:30 | 
🎲 Бросок на ранение (to wound): 2D6
2026-03-11 13:57:34 | 
🎲 Бросок сейвы (save): 1D6
2026-03-11 13:57:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (overwatch)
2026-03-11 13:57:53 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-11 13:57:53 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 1.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:57:53 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 13:57:53 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 13:57:53 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:57:53 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-11 13:57:53 | Оружие: Gauss flayer
2026-03-11 13:57:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:57:53 | BS оружия: 4+
2026-03-11 13:57:53 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:57:53 | Save цели: 4+ (invul: нет)
2026-03-11 13:57:53 | Benefit of Cover: не активен.
2026-03-11 13:57:53 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:57:53 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:57:53 | Hit rolls:    [1, 2, 3, 4, 5, 6, 3, 3, 1]  -> hits: 3 (crits: 1)
2026-03-11 13:57:53 | Wound rolls:  [2, 3]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-11 13:57:53 | Save rolls:   [3]  (цель 4+) -> failed saves: 1
2026-03-11 13:57:53 | 
✅ Итог по движку: прошло урона = 1.0
2026-03-11 13:57:53 | FX: найден итог урона = 1.0.
2026-03-11 13:57:53 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=1.0).
2026-03-11 13:57:53 | FX: позиция эффекта start=(876.0,756.0) end=(276.0,804.0).
2026-03-11 13:57:53 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-11 13:57:53 | 📌 -------------------------

2026-03-11 13:57:53 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-11 13:57:53 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-11 13:57:53 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 13:57:53 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:57:53 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 13:57:53 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:57:53 | FX: найден итог урона = 0.0.
2026-03-11 13:57:53 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 13:58:15 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 13:58:21 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 13:58:23 | 
🎲 Бросок сейвы (save): 7D6
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 5. HP: 9.0 -> 5.0 (overwatch)
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 5. Причина: потери моделей.
2026-03-11 13:58:28 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 4.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:58:28 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 13:58:28 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 13:58:28 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:58:28 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-11 13:58:28 | Оружие: Gauss flayer
2026-03-11 13:58:28 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:58:28 | BS оружия: 4+
2026-03-11 13:58:28 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:58:28 | Save цели: 4+ (invul: нет)
2026-03-11 13:58:28 | Benefit of Cover: не активен.
2026-03-11 13:58:28 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:58:28 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:58:28 | Hit rolls:    [3, 4, 5, 6, 5, 6, 6, 6, 6, 6]  -> hits: 9 (crits: 6)
2026-03-11 13:58:28 | Wound rolls:  [3, 4, 1]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 6 = 7
2026-03-11 13:58:28 | Save rolls:   [3, 4, 5, 1, 2, 3, 4]  (цель 4+) -> failed saves: 4
2026-03-11 13:58:28 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-11 13:58:28 | FX: найден итог урона = 4.0.
2026-03-11 13:58:28 | FX: создан FxShotEvent (attacker=12, target=21, weapon=Gauss flayer, damage=4.0).
2026-03-11 13:58:28 | FX: позиция эффекта start=(804.0,492.0) end=(276.0,804.0).
2026-03-11 13:58:28 | FX: эффект добавлен в рендер (attacker=12, target=21).
2026-03-11 13:58:28 | 📌 -------------------------

2026-03-11 13:58:28 | --- ФАЗА ЧАРДЖА ---
2026-03-11 13:58:28 | Нет доступных целей для чарджа.
2026-03-11 13:58:28 | --- ФАЗА БОЯ ---
2026-03-11 13:58:28 | --- ХОД MODEL ---
2026-03-11 13:58:28 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) До: моделей=5, раны=[1, 1, 1, 1, 1] всего=5
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) После:  моделей=6, раны=[1, 1, 1, 1, 1, 1] всего=6
2026-03-11 13:58:28 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-11 13:58:28 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (33, 11). Выбор: right, advance=да, бросок=5, макс=10, distance=10
2026-03-11 13:58:28 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (33, 21)
2026-03-11 13:58:28 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 21 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:58:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 13). Выбор: right, advance=да, бросок=2, макс=7, distance=7
2026-03-11 13:58:30 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 20)
2026-03-11 13:58:30 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:58:31 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 13:58:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 13:58:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 13:58:31 | --- ФАЗА ЧАРДЖА ---
2026-03-11 13:58:31 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 13:58:31 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 13:58:31 | [MODEL] Чардж: нет доступных целей
2026-03-11 13:58:31 | --- ФАЗА БОЯ ---
2026-03-11 13:58:31 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 13:58:31 | Reward (progress к objective): d_before=21.401, d_after=15.811, delta=5.590, norm=0.932, bonus=+0.028
2026-03-11 13:58:31 | Reward (terrain/potential): gamma=0.990, phi_before=-0.067, phi_after=-0.011, delta=+0.056; cover=0.000->0.500, threat=-0.667->-0.667, guard=0.000->0.400
2026-03-11 13:58:31 | Reward (terrain/exposure): penalty=-0.010 (exposed_units=1, alive_units=2, threat_count=4)
2026-03-11 13:58:31 | Reward (terrain/clamp): raw=+0.046, cap=±0.120, clamp не сработал
2026-03-11 13:58:31 | === КОНЕЦ БОЕВОГО РАУНДА 2 ===
2026-03-11 13:58:31 | Итерация 1 завершена с наградой tensor([0.0741], device='cuda:0'), здоровье игрока [9.0, 10.0], здоровье модели [6.0, 10.0]
2026-03-11 13:58:31 | {'model health': [6.0, 10.0], 'player health': [9.0, 10.0], 'model alive models': [6, 10], 'player alive models': [9, 10], 'modelCP': 2, 'playerCP': 4, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 3, 'battle round': 3, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 13:58:31 | Здоровье MODEL: [6.0, 10.0], здоровье PLAYER: [9.0, 10.0]
CP MODEL: 2, CP PLAYER: 4
VP MODEL: 0, VP PLAYER: 0

2026-03-11 13:58:31 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 13:58:33 | === БОЕВОЙ РАУНД 3 ===
2026-03-11 13:58:33 | --- ХОД PLAYER ---
2026-03-11 13:58:33 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 13:58:33 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
2026-03-11 13:58:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Reanimation Protocols: бросок D3 = 1
2026-03-11 13:58:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) До: моделей=9, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1] всего=9
2026-03-11 13:58:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Возвращена уничтоженная модель с 1 раной
2026-03-11 13:58:36 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) После:  моделей=10, раны=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1] всего=10
2026-03-11 13:58:36 | [ENEMY] Only War: end of Command phase -> controlled=1, gained=1, VP: 0 -> 1, objectives=[1]; objectives=[1], center=(30,20), controlled_by=enemy
2026-03-11 13:58:36 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 13:58:39 | REQ: move cell accepted (RMB) x=31, y=35, mode=normal
2026-03-11 13:58:40 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:58:40 | 
🎲 Бросок на попадание (to hit): 12D6
2026-03-11 13:58:40 | 
🎲 Бросок на ранение (to wound): 3D6
2026-03-11 13:58:40 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 8. HP: 10.0 -> 8.0 (Overwatch)
2026-03-11 13:58:40 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 8. Причина: потери моделей.
2026-03-11 13:58:40 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 2.0.
2026-03-11 13:58:40 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 13:58:40 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:58:40 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:58:40 | FX: найдена строка стрельбы (attacker=21, target=11).
2026-03-11 13:58:40 | Оружие: Gauss flayer
2026-03-11 13:58:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:58:40 | BS оружия: 4+
2026-03-11 13:58:40 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 13:58:40 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:58:40 | Save цели: 4+ (invul: нет)
2026-03-11 13:58:40 | Benefit of Cover: не активен.
2026-03-11 13:58:40 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:58:40 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:58:40 | Правило: Overwatch: попадания только на 6+
2026-03-11 13:58:40 | Hit rolls:    [1, 5, 6, 3, 5, 6, 2, 5, 5, 4, 3, 6]  -> hits: 3 (crits: 3)
2026-03-11 13:58:40 | Wound rolls:  [1, 4, 2]  (цель 4+) -> rolled wounds: 1 + auto(w/LETHAL): 3 = 4
2026-03-11 13:58:40 | 
✅ Итог по движку: прошло урона = 2.0
2026-03-11 13:58:40 | FX: найден итог урона = 2.0.
2026-03-11 13:58:40 | FX: создан FxShotEvent (attacker=21, target=11, weapon=Gauss flayer, damage=2.0).
2026-03-11 13:58:40 | FX: позиция эффекта start=(516.0,804.0) end=(876.0,756.0).
2026-03-11 13:58:40 | FX: эффект добавлен в рендер (attacker=21, target=11).
2026-03-11 13:58:40 | 📌 -------------------------

2026-03-11 13:58:42 | REQ: move cell accepted (RMB) x=28, y=15, mode=normal
2026-03-11 13:58:42 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 12 — Necrons Necron Warriors (x10 моделей).
2026-03-11 13:58:42 | 
🎲 Бросок на попадание (to hit): 6D6
2026-03-11 13:58:42 | [MODEL] [MOVEMENT] Unit 21 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 12 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 0.0.
2026-03-11 13:58:42 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-11 13:58:42 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:58:42 | Стреляет: Unit 21 — Necrons Necron Warriors (x10 моделей); цель: Unit 12 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:58:42 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 13:58:42 | Оружие: Gauss flayer
2026-03-11 13:58:42 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:58:42 | BS оружия: 4+
2026-03-11 13:58:42 | Overwatch: для попадания используется только натуральная 6+ (игнор BS оружия).
2026-03-11 13:58:42 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:58:42 | Save цели: 4+ (invul: нет)
2026-03-11 13:58:42 | Benefit of Cover: не активен.
2026-03-11 13:58:42 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:58:42 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:58:42 | Правило: Overwatch: попадания только на 6+
2026-03-11 13:58:42 | Hit rolls:    [5, 4, 1, 3, 3, 4]  -> hits: 0
2026-03-11 13:58:42 | 
✅ Итог по движку: прошло урона = 0.0
2026-03-11 13:58:42 | FX: найден итог урона = 0.0.
2026-03-11 13:58:42 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 13:58:42 | 📌 -------------------------

2026-03-11 13:58:42 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 13:58:42 | [TARGET][SHOOT] Unit 11 — Necrons Necron Warriors (x10 моделей) -> Unit 22 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 13:58:42 | REQ: shooter changed Unit 12->Unit 11, target reset
2026-03-11 13:58:42 | REQ: валидные цели стрельбы для Unit 11: [21] | отфильтрованы: [22: цель вне дальности: range 26.00 > 24.00 (out_of_range by +2.00)]
2026-03-11 13:59:27 | 
🎲 Бросок на попадание (to hit): 16D6
2026-03-11 13:59:36 | 
🎲 Бросок на ранение (to wound): 14D6
2026-03-11 13:59:43 | 
🎲 Бросок сейвы (save): 6D6
2026-03-11 13:59:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 4. Осталось: 2. HP: 6.0 -> 2.0 (overwatch)
2026-03-11 13:59:47 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 2. Причина: потери моделей.
2026-03-11 13:59:47 | Unit 11 — Necrons Necron Warriors (x10 моделей) нанёс 4.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:59:47 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 13:59:47 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 13:59:47 | Стреляет: Unit 11 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 13:59:47 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-11 13:59:47 | Оружие: Gauss flayer
2026-03-11 13:59:47 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:59:47 | BS оружия: 4+
2026-03-11 13:59:47 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 13:59:47 | Save цели: 4+ (invul: нет)
2026-03-11 13:59:47 | Benefit of Cover: не активен.
2026-03-11 13:59:47 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 13:59:47 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 13:59:47 | Hit rolls:    [3, 4, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]  -> hits: 15 (crits: 1)
2026-03-11 13:59:47 | Wound rolls:  [4, 5, 6, 2, 3, 4, 5, 1, 1, 1, 1, 1, 1, 1]  (цель 4+) -> rolled wounds: 5 + auto(w/LETHAL): 1 = 6
2026-03-11 13:59:47 | Save rolls:   [3, 4, 1, 2, 3, 5]  (цель 4+) -> failed saves: 4
2026-03-11 13:59:47 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-11 13:59:47 | FX: найден итог урона = 4.0.
2026-03-11 13:59:47 | FX: создан FxShotEvent (attacker=11, target=21, weapon=Gauss flayer, damage=4.0).
2026-03-11 13:59:47 | FX: позиция эффекта start=(756.0,852.0) end=(516.0,804.0).
2026-03-11 13:59:47 | FX: эффект добавлен в рендер (attacker=11, target=21).
2026-03-11 13:59:47 | 📌 -------------------------

2026-03-11 13:59:47 | REQ: shooter changed Unit 11->Unit 12, target reset
2026-03-11 13:59:47 | REQ: валидные цели стрельбы для Unit 12: [21, 22] | отфильтрованы: [—]
2026-03-11 13:59:47 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 13:59:47 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-11 13:59:47 | FX: найдена строка стрельбы (attacker=21, target=12).
2026-03-11 13:59:47 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 13:59:47 | FX: найден итог урона = 0.0.
2026-03-11 13:59:47 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 14:00:10 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-11 14:00:16 | 
🎲 Бросок на ранение (to wound): 9D6
2026-03-11 14:00:22 | 
🎲 Бросок сейвы (save): 6D6
2026-03-11 14:00:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 2. Осталось: 0. HP: 2.0 -> 0.0 (overwatch)
2026-03-11 14:00:27 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 0. Причина: потери моделей.
2026-03-11 14:00:27 | Unit 12 — Necrons Necron Warriors (x10 моделей) нанёс 4.0 урона по Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 14:00:27 | 
📌 --- ОТЧЁТ ПО СТРЕЛЬБЕ ---
2026-03-11 14:00:27 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 14:00:27 | Стреляет: Unit 12 — Necrons Necron Warriors (x10 моделей); цель: Unit 21 — Necrons Necron Warriors (x10 моделей)
2026-03-11 14:00:27 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-11 14:00:27 | Оружие: Gauss flayer
2026-03-11 14:00:27 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 14:00:27 | BS оружия: 4+
2026-03-11 14:00:27 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-11 14:00:27 | Save цели: 4+ (invul: нет)
2026-03-11 14:00:27 | Benefit of Cover: не активен.
2026-03-11 14:00:27 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-11 14:00:27 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-11 14:00:27 | Hit rolls:    [4, 4, 5, 4, 1, 4, 5, 4, 5, 4]  -> hits: 9
2026-03-11 14:00:27 | Wound rolls:  [3, 4, 5, 1, 2, 4, 6, 6, 6]  (цель 4+) -> wounds: 6
2026-03-11 14:00:27 | Save rolls:   [3, 1, 5, 6, 1, 2]  (цель 4+) -> failed saves: 4
2026-03-11 14:00:27 | 
✅ Итог по движку: прошло урона = 4.0
2026-03-11 14:00:27 | FX: найден итог урона = 4.0.
2026-03-11 14:00:27 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 14:00:27 | 📌 -------------------------

2026-03-11 14:00:27 | --- ФАЗА ЧАРДЖА ---
2026-03-11 14:00:27 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 14:00:27 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 14:00:27 | FX: найдена строка стрельбы (attacker=11, target=21).
2026-03-11 14:00:27 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 14:00:27 | FX: найден итог урона = 4.0.
2026-03-11 14:00:27 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 14:00:38 | Unit 12 — Necrons Necron Warriors (x10 моделей) решил пропустить чардж.
2026-03-11 14:00:38 | --- ФАЗА БОЯ ---
2026-03-11 14:00:38 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=26.00, range=24.00, delta=+2.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-11 14:00:38 | --- ХОД MODEL ---
2026-03-11 14:00:38 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 14:00:38 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-11 14:00:38 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-11 14:00:38 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Юнит мертв, движение пропущено. Позиция: (33, 21)
2026-03-11 14:00:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (7, 20). Выбор: right, advance=да, бросок=2, макс=7, distance=7
2026-03-11 14:00:38 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (7, 27)
2026-03-11 14:00:38 | [PLAYER][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 22 — Necrons Necron Warriors (x10 моделей).
2026-03-11 14:00:40 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-11 14:00:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Юнит мертв, стрельба пропущена.
2026-03-11 14:00:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance без Assault — стрельба пропущена.
2026-03-11 14:00:40 | --- ФАЗА ЧАРДЖА ---
2026-03-11 14:00:40 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Юнит мертв, чардж пропущен.
2026-03-11 14:00:40 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Advance — чардж невозможен.
2026-03-11 14:00:40 | [MODEL] Чардж: нет доступных целей
2026-03-11 14:00:40 | --- ФАЗА БОЯ ---
2026-03-11 14:00:40 | [MODEL] Ближний бой: нет доступных атак
2026-03-11 14:00:40 | Reward (VP diff): prev=0, curr=-1, delta=-1, reward=+0.000, penalty=-0.050
2026-03-11 14:00:40 | Reward (progress к objective): d_before=16.401, d_after=13.342, delta=3.060, norm=0.510, bonus=+0.015
2026-03-11 14:00:40 | Reward (terrain/potential): gamma=0.990, phi_before=+0.035, phi_after=-0.033, delta=-0.068; cover=0.500->0.000, threat=-0.333->-0.333, guard=0.700->0.000
2026-03-11 14:00:40 | Reward (terrain/exposure): penalty=-0.020 (exposed_units=1, alive_units=1, threat_count=1)
2026-03-11 14:00:40 | Reward (terrain/clamp): raw=-0.088, cap=±0.120, clamp не сработал
2026-03-11 14:00:40 | === КОНЕЦ БОЕВОГО РАУНДА 3 ===
2026-03-11 14:00:40 | Итерация 2 завершена с наградой tensor([-0.1224], device='cuda:0'), здоровье игрока [8.0, 10.0], здоровье модели [0.0, 10.0]
2026-03-11 14:00:40 | {'model health': [0.0, 10.0], 'player health': [8.0, 10.0], 'model alive models': [0, 10], 'player alive models': [8, 10], 'modelCP': 2, 'playerCP': 6, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 1, 'mission': 'Only War', 'turn': 4, 'battle round': 4, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-11 14:00:40 | Здоровье MODEL: [0.0, 10.0], здоровье PLAYER: [8.0, 10.0]
CP MODEL: 2, CP PLAYER: 6
VP MODEL: 0, VP PLAYER: 1

2026-03-11 14:00:40 | FX: перепроигрываю 30 строк(и) лога.
2026-03-11 14:00:40 | FX: старт отчёта (shooting), ts=no-ts.
2026-03-11 14:00:40 | FX: найдена строка стрельбы (attacker=12, target=21).
2026-03-11 14:00:40 | FX: найдена строка оружия: Gauss flayer.
2026-03-11 14:00:40 | FX: найден итог урона = 4.0.
2026-03-11 14:00:40 | FX: дубликат отчёта, эффект не создаём.
2026-03-11 14:00:42 | === БОЕВОЙ РАУНД 4 ===
2026-03-11 14:00:42 | --- ХОД PLAYER ---
2026-03-11 14:00:42 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-11 14:00:42 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей) Используется способность: Reanimation Protocols
