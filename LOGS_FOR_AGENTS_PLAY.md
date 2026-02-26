2026-02-26 14:34:28 | [VIEWER] Рендер: OpenGL (QOpenGLWidget).
2026-02-26 14:34:28 | [VIEWER] Фоллбэк-рендер не активирован.
2026-02-26 14:34:28 | [VIEWER][RESET] reason=new_game_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-02-26 14:34:39 | [MODEL] pickle=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-49-275138.pickle
2026-02-26 14:34:39 | [MODEL] checkpoint=C:\40kAI\models\M_Necrons_vs_P_Necrons\model-49-275138.pth
2026-02-26 14:34:39 | [MODEL] Viewer запущен в greedy-режиме: exploration отключен (epsilon=0).
2026-02-26 14:34:42 | Roll-off Attacker/Defender: enemy=1 model=2 -> attacker=model
2026-02-26 14:34:42 | Юниты: [('Necron Warriors', '1', 10), ('Necron Warriors', 'unit-1', 10)]
2026-02-26 14:34:42 | [DEPLOY] mode=rl_phase, strategy=template_jitter, seed=none
2026-02-26 14:34:42 | [DEPLOY][Only War] attacker=model -> LEFT x=0..14; defender=enemy -> RIGHT x=45..59
2026-02-26 14:34:42 | [DEPLOY][AUTO] mode=rl_phase strategy=template_jitter seed=none
2026-02-26 14:34:42 | [DEPLOY] Order: model first, alternating
2026-02-26 14:34:42 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.000
2026-02-26 14:34:42 | [DEPLOY][RL] accepted Unit 21 — Necrons Necron Warriors (x10 моделей): flat=1932, coord=(32,12), attempt=1, reward=+0.028, score_before=0.000, score_after=0.559, reward_delta=+0.028, forward=0.207, spread=1.000, edge=1.000, cover=0.000
2026-02-26 14:34:42 | [DEPLOY][MODEL] Unit 21 — Necrons Necron Warriors (x10 моделей) -> (32,12)
2026-02-26 14:34:42 | [VIEWER][RESET] reason=manual_deploy_start. Где: viewer/app.py. Что делаем: очищаем visual state прошлой сессии.
2026-02-26 14:34:43 | REQ: deploy cell accepted x=52, y=23
2026-02-26 14:34:43 | [DEPLOY][MANUAL] accepted Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,52)
2026-02-26 14:34:43 | [DEPLOY][ENEMY] Unit 11 — Necrons Necron Warriors (x10 моделей) -> (23,52)
2026-02-26 14:34:43 | [DEPLOY][RL] score_config scale=0.050 w_forward=1.000 w_spread=0.600 w_edge=0.200 w_cover=0.000
2026-02-26 14:34:43 | [DEPLOY][RL] accepted Unit 22 — Necrons Necron Warriors (x10 моделей): flat=850, coord=(14,10), attempt=1, reward=-0.000, score_before=0.559, score_after=0.550, reward_delta=-0.000, forward=0.190, spread=1.000, edge=1.000, cover=0.000
2026-02-26 14:34:43 | [DEPLOY][MODEL] Unit 22 — Necrons Necron Warriors (x10 моделей) -> (14,10)
2026-02-26 14:34:44 | REQ: deploy cell accepted x=50, y=13
