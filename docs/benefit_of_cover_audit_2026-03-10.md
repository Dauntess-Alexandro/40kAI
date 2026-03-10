# Аудит Benefit of Cover (TRAIN/PLAY) — 2026-03-10

Кратко:
- В движке формула сейва с Benefit of Cover реализована корректно: `save_target = Sv - cover_bonus - AP`, где `cover_bonus=1` только для ranged и только при `effect == "benefit of cover"`.
- Ветки shooting/overwatch/manual прокидывают `effects=effect` в `attack()`.
- Auto-cover при `obscured=True` включается через `_resolve_cover_effect_for_shot()`.
- В `LOGS_FOR_AGENTS_PLAY.md` есть сквозные подтверждения (cover -> save target 3+).
- В `LOGS_FOR_AGENTS_TRAIN.md` нет строк `Save цели`/`Save rolls`/`Benefit of Cover`, поэтому по TRAIN подтверждается только вычисление obscured/LOS, но не применение на сейвах.
