# Временные настройки рендера (viewer)

Сейчас в OpenGL viewer оставлены только базовые слои: ground, grid, units, overlays и FX.

Отключено:
- props/ (террейн-объекты)
- decals/ (следы/кровь)
- shadows/ (тени от пропсов)

Включено:
- fx/ (частицы/вспышки)

Корень ассетов: `viewer/assets/`.

Чтобы вернуть террейн позже:
- В `viewer/opengl_view.py` выставить `render_terrain = True`,
  `render_decals = True`, `render_prop_shadows = True`,
  и вернуть вызовы `_draw_props_layer`/`_draw_decals_layer` в `paintGL`.
