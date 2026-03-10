2026-03-10 19:02:21 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-03-10 19:02:21 | [VIEWER] Фоллбэк-рендер не активирован.
2026-03-10 19:02:21 | [VIEWER][TERRAIN] features=4 first=<barricade,barrel.png,3>
2026-03-10 19:02:21 | [VIEWER][TERRAIN] load sprite=barrel.png path=C:\40kAI\viewer\assets\props\terrain\barrel.png exists=True
2026-03-10 19:02:22 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 19:02:26 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-51-94641.pickle
2026-03-10 19:02:26 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-51-94641.pth
2026-03-10 19:02:26 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-03-10 19:02:28 | Roll-off Attacker/Defender: enemy=1 model=3 -> attacker=model
2026-03-10 19:02:28 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-03-10 19:02:28 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-03-10 19:02:28 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-03-10 19:02:28 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-03-10 19:02:28 | [DEPLOY] Order: model first, alternating
2026-03-10 19:02:28 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 19:02:28 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=2286, coord=(38,6), attempt=1, reward=+0.016, score_before=0.000, score_after=0.328, reward_delta=+0.016, forward=0.105, spread=1.000, edge=0.000, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 19:02:28 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (38,6)
2026-03-10 19:02:28 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-03-10 19:02:29 | REQ: deploy cell accepted x=51, y=25
2026-03-10 19:02:29 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,51)
2026-03-10 19:02:29 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (25,51)
2026-03-10 19:02:29 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.350
2026-03-10 19:02:29 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=2112, coord=(35,12), attempt=1, reward=-0.003, score_before=0.328, score_after=0.259, reward_delta=-0.003, forward=0.156, spread=0.500, edge=0.500, cover=0.000, cover_near=0.000, congestion=0.000, final_cover=0.000
2026-03-10 19:02:29 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (35,12)
2026-03-10 19:02:29 | REQ: deploy cell accepted x=51, y=14
2026-03-10 19:02:30 | [DEPLOY][MANUAL] accepted Unit 12 — Necrons Necron Warriors (x10 моделей) -> (14,51)
2026-03-10 19:02:30 | [DEPLOY][ENEMY] Unit 12 — Necrons Necron Warriors (x10 моделей) -> (14,51)
2026-03-10 19:02:30 | [DEPLOY][RL][SUMMARY] units=2 attempts=2 invalid=0 fallback=0 reward=+0.013 total_deploy_reward=+0.013 avg_forward=0.131 avg_spread=0.750 avg_edge=0.250 avg_cover=0.000
2026-03-10 19:02:30 | [DEPLOY] rl_phase stats: {'attempts': 2, 'invalid': 0, 'fallback': 0, 'reward': 0.012928655892786755, 'units': 2, 'total_deploy_reward': 0.012928655892786755, 'forward_sum': 0.26101694915254237, 'spread_sum': 1.5, 'edge_sum': 0.5, 'cover_sum': 0.0, 'avg_forward': 0.13050847457627118, 'avg_spread': 0.75, 'avg_edge': 0.25, 'avg_cover': 0.0}
2026-03-10 19:02:30 | [MISSION Only War] Post-deploy: currently no post-deploy units supported
2026-03-10 19:02:30 | [MODEL] Архитектура сети: dueling (источник: net_type)
2026-03-10 19:02:30 | 
Инструкции:
Игрок управляет юнитами, начинающимися с 1 (т.е. 11, 12 и т.д.).
Модель управляет юнитами, начинающимися с 2 (т.е. 21, 22 и т.д.).

2026-03-10 19:02:30 | {'model health': [10, 10], 'player health': [10, 10], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 0, 'playerCP': 0, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 1, 'battle round': 1, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 19:02:30 | Здоровье MODEL: [10, 10], здоровье PLAYER: [10, 10]
CP MODEL: 0, CP PLAYER: 0
VP MODEL: 0, VP PLAYER: 0

2026-03-10 19:02:30 | FX: перепроигрываю 30 строк(и) лога.
2026-03-10 19:02:31 | === БОЕВОЙ РАУНД 1 ===
2026-03-10 19:02:31 | --- ХОД PLAYER ---
2026-03-10 19:02:31 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 19:02:31 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 19:02:31 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 19:02:33 | REQ: move cell accepted (RMB) x=40, y=28, mode=advance
2026-03-10 19:02:34 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 19:02:35 | REQ: move cell accepted (RMB) x=40, y=25, mode=advance
2026-03-10 19:02:35 | [MODEL][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 19:02:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 19:02:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 19:02:35 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance без Assault — стрельба пропущена.
2026-03-10 19:02:35 | --- ФАЗА ЧАРДЖА ---
2026-03-10 19:02:35 | Unit 11 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 19:02:35 | Unit 12 — Necrons Necron Warriors (x10 моделей): был Advance — чардж невозможен.
2026-03-10 19:02:35 | Нет доступных целей для чарджа.
2026-03-10 19:02:35 | --- ФАЗА БОЯ ---
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | --- ХОД MODEL ---
2026-03-10 19:02:35 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 19:02:35 | [MODEL] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 19:02:35 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 19:02:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция до: (38, 6). Выбор: right, advance=нет, distance=1
2026-03-10 19:02:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Позиция после: (38, 7)
2026-03-10 19:02:35 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 19:02:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция до: (35, 12). Выбор: right, advance=нет, distance=1
2026-03-10 19:02:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Позиция после: (35, 13)
2026-03-10 19:02:35 | [PLAYER][MOVEMENT] Overwatch невозможен: нет доступных стреляющих юнитов.
2026-03-10 19:02:35 | --- ФАЗА СТРЕЛЬБЫ ---
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 21 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=31.00, range=24.00, delta=+7.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [TARGET][SHOOT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 12 — Necrons Necron Warriors (x10 моделей): цель вне дальности (distance=25.00, range=24.00, delta=+1.00, eps=0.10). Где: warhamEnv.get_shoot_targets_for_unit. Что делать дальше: проверить range/LOS/engagement и обновить выбор цели.
2026-03-10 19:02:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в дальности, стрельба пропущена.
2026-03-10 19:02:35 | --- ФАЗА ЧАРДЖА ---
2026-03-10 19:02:35 | [MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 19:02:35 | [MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей): Нет целей в 12", чардж пропущен.
2026-03-10 19:02:35 | [MODEL] Чардж: нет доступных целей
2026-03-10 19:02:35 | --- ФАЗА БОЯ ---
2026-03-10 19:02:35 | [MODEL] Ближний бой: нет доступных атак
2026-03-10 19:02:35 | Reward (progress к objective): d_before=23.431, d_after=22.672, delta=0.759, norm=0.127, bonus=+0.004
2026-03-10 19:02:35 | Reward (terrain/potential): gamma=0.990, phi_before=+0.000, phi_after=+0.000, delta=+0.000; cover=0.000->0.000, threat=-0.000->-0.000, guard=0.000->0.000
2026-03-10 19:02:35 | Reward (terrain/exposure): skip, reason=нет реальных угроз (threat_count=0).
2026-03-10 19:02:35 | Reward (terrain/clamp): raw=+0.000, cap=±0.120, clamp не сработал
2026-03-10 19:02:35 | === КОНЕЦ БОЕВОГО РАУНДА 1 ===
2026-03-10 19:02:35 | Итерация 0 завершена с наградой tensor([0.0038], device='cuda:0'), здоровье игрока [10.0, 10.0], здоровье модели [10.0, 10.0]
2026-03-10 19:02:35 | {'model health': [10.0, 10.0], 'player health': [10.0, 10.0], 'model alive models': [10, 10], 'player alive models': [10, 10], 'modelCP': 2, 'playerCP': 2, 'in attack': [[0, 0], [0, 0]], 'model VP': 0, 'player VP': 0, 'mission': 'Only War', 'turn': 2, 'battle round': 2, 'active side': 'enemy', 'phase': 'command', 'game over': False, 'end reason': '', 'winner': None}
2026-03-10 19:02:35 | Здоровье MODEL: [10.0, 10.0], здоровье PLAYER: [10.0, 10.0]
CP MODEL: 2, CP PLAYER: 2
VP MODEL: 0, VP PLAYER: 0

2026-03-10 19:02:42 | === БОЕВОЙ РАУНД 2 ===
2026-03-10 19:02:42 | --- ХОД PLAYER ---
2026-03-10 19:02:42 | --- ФАЗА КОМАНДОВАНИЯ ---
2026-03-10 19:02:42 | [ENEMY] Only War: end of Command phase -> controlled=0, gained=0, VP: 0 -> 0; objectives=[1], center=(30,20), controlled_by=none
2026-03-10 19:02:42 | --- ФАЗА ДВИЖЕНИЯ ---
2026-03-10 19:02:43 | REQ: move cell accepted (RMB) x=36, y=31, mode=normal
2026-03-10 19:02:44 | [MODEL][MOVEMENT] Триггер Overwatch: цель переместилась. Цель: Unit 11 — Necrons Necron Warriors (x10 моделей).
2026-03-10 19:02:44 | [COVER][MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей) -> Unit 11 — Necrons Necron Warriors (x10 моделей): применён Benefit of Cover (причина: obscured=True по LOS_DEBUG).
2026-03-10 19:02:44 | 
🎲 Бросок на попадание (to hit): 10D6
2026-03-10 19:02:44 | 
🎲 Бросок на ранение (to wound): 1D6
2026-03-10 19:02:44 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Потери: убито моделей 1. Осталось: 9. HP: 10.0 -> 9.0 (Overwatch)
2026-03-10 19:02:44 | [PLAYER] Unit 11 — Necrons Necron Warriors (x10 моделей): Когеренция автоматически обновлена. Живых моделей: 9. Причина: потери моделей.
2026-03-10 19:02:44 | [MODEL] [MOVEMENT] Unit 22 — Necrons Necron Warriors (x10 моделей): Правило/стратагема «Overwatch»: Цель: Unit 11 — Necrons Necron Warriors (x10 моделей). Стоимость: -1 CP. Итоговый урон: 1.0.
2026-03-10 19:02:44 | 
📌 --- ОТЧЁТ ПО OVERWATCH ---
2026-03-10 19:02:44 | FX: старт отчёта (overwatch), ts=no-ts.
2026-03-10 19:02:44 | Стреляет: Unit 22 — Necrons Necron Warriors (x10 моделей); цель: Unit 11 — Necrons Necron Warriors (x10 моделей)
2026-03-10 19:02:44 | FX: найдена строка стрельбы (attacker=22, target=11).
2026-03-10 19:02:44 | Оружие: Gauss flayer
2026-03-10 19:02:44 | FX: найдена строка оружия: Gauss flayer.
2026-03-10 19:02:44 | BS оружия: 4+
2026-03-10 19:02:44 | S vs T: 4 vs 4  -> базово ранение на 4+
2026-03-10 19:02:44 | Save цели: 4+ (invul: нет)
2026-03-10 19:02:44 | Benefit of Cover: активен (+1 к сейву цели против ranged).
2026-03-10 19:02:44 | Правило: Rapid Fire 1 (если цель в половине дальности: +1 атак)
2026-03-10 19:02:44 | Правило: Lethal Hits (крит-хиты авто-ранят)
2026-03-10 19:02:44 | Правило: Overwatch: попадания только на 6+
2026-03-10 19:02:44 | Эффект: benefit of cover
2026-03-10 19:02:44 | Hit rolls:    [3, 6, 1, 3, 1, 5, 5, 1, 4, 2]  -> hits: 4 (crits: 1)
2026-03-10 19:02:44 | Wound rolls:  [2]  (цель 4+) -> rolled wounds: 0 + auto(w/LETHAL): 1 = 1
2026-03-10 19:02:44 | Ошибка игры: 'RollLogger' object has no attribute '_append_agent_log'. Место: game_controller._run_game_loop (File "C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py", line 786, in print_shoot_report). Что делать дальше: проверьте traceback ниже и исправьте источник ошибки в указанном файле/строке.
2026-03-10 19:02:44 | Traceback (последние вызовы):
2026-03-10 19:02:44 | Traceback (most recent call last):
2026-03-10 19:02:44 |   File "C:\40kAI\gym_mod\gym_mod\engine\game_controller.py", line 242, in _run_game_loop
2026-03-10 19:02:44 |     done, info = env.unwrapped.player()
2026-03-10 19:02:44 |                  ^^^^^^^^^^^^^^^^^^^^^^
2026-03-10 19:02:44 |   File "C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py", line 5620, in player
2026-03-10 19:02:44 |     advanced_flags = self.movement_phase("enemy", manual=True, battle_shock=battle_shock)
2026-03-10 19:02:44 |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2026-03-10 19:02:44 |   File "C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py", line 3564, in movement_phase
2026-03-10 19:02:44 |     self._resolve_overwatch(
2026-03-10 19:02:44 |   File "C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py", line 2643, in _resolve_overwatch
2026-03-10 19:02:44 |     _logger.print_shoot_report(
2026-03-10 19:02:44 |   File "C:\40kAI\gym_mod\gym_mod\envs\warhamEnv.py", line 786, in print_shoot_report
2026-03-10 19:02:44 |     self._append_agent_log(
2026-03-10 19:02:44 |     ^^^^^^^^^^^^^^^^^^^^^^
2026-03-10 19:02:44 | AttributeError: 'RollLogger' object has no attribute '_append_agent_log'
