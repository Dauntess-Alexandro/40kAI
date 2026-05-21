# Gauss FX и доработки viewer (2026-05)

Краткий отчёт о работе по viewer migration follow-ups, пайплайну оружейных эффектов Gauss и визуальной полировке. Для стратегии миграции см. [viewer_migration_plan.md](viewer_migration_plan.md).

---

## Итог одной строкой

Gauss Flayer / Gauss Reaper получили полноценный многослойный FX (6 PNG + процедурные слои), профили в `gun_fx.py`, спавн из лога боя; исправлены QML/рендер/краши GUI; scorch и glyphs/muzzle доведены до видимости в игре.

---

## 1. Viewer и GUI

### Миграция QML (флаги по умолчанию ON)

- `viewer_config.json` / `config._DEFAULTS`: QML-панели, лог, диалоги, `fx.v2` и связанные флаги включены по умолчанию.
- **QML log:** `LogPanel.qml` + модель лога в `app.py`.
- **Диалоги:** `ViewerDialogBridge` — toast / confirm из QML.
- **Вкладки:** `TacticalTabButton.qml`, `ChamferPanel.qml` — исправлена загрузка (в т.ч. `ResizeMode.SizeRootObjectToView` для PySide6 6.7).
- **Контроллер:** `ViewerController` — prompt, `submitChoiceAtIndex`, `submitAnswerPy`.

### Рендер доски

- **Чёрная доска + D3D11:** до `QApplication` выставляется `QSG_RHI_BACKEND=opengl` (`app/viewer/app.py`, `app/viewer/__main__.py`), общие GL-контексты для `QOpenGLWidget`.
- Фильтр спама D3D11 в message handler.

### Стабильность UI

- **QLabel «already deleted»:** при активных QML-панелях статус/points держатся на скрытом `mirror`-виджете, а не на выброшенном `legacy_right_top`.

### Доска

- Hover / selection, per-model **stagger** при `fx.v2`.
- Якорь выстрела: `unit_shoot_anchor_world()` — луч из центроида модели, не из угла клетки.

---

## 2. Пайплайн Gauss FX

### Цепочка вызовов

```
лог боя (FxLogParser)
  → app.py: _spawn_fx_for_event()
  → resolve_fx_profile(weapon_name)   # gun_fx.py
  → build_gauss_effect()              # opengl_view.py
  → add_effect()                      # + scorch decal spawn
  → paint_fx_layer → _draw_gauss_effects()
```

Scorch рисуется в **decals**-слое **под юнитами** (`rendering/layers/decals.py`), не в FX-слое.

### Оружие

| Ключ | Профиль | Файл |
|------|---------|------|
| `gauss flayer` | `GAUSS_FLAYER_FX` | `app/viewer/gun_fx.py` |
| `gauss reaper` | `GAUSS_REAPER_FX` (наследует Flayer + overrides) | то же |

Подстроки в имени оружия: `WEAPON_ALIASES` + `resolve_fx_profile()`. Убран жёсткий фильтр только на `"gauss flayer"` в `app.py`.

Другие пушки — без Gauss-профиля, пока не добавлены в `GUN_FX_CONFIGS`.

---

## 3. PNG-ассеты

Каталог: `app/viewer/assets/fx/`. Bake из крупных исходников: `python tools/viewer/bake_gauss_fx_assets.py` (бэкапы в `fx/_source/`, в gitignore).

| Файл | Размер (bake) | Где рисуется | Роль |
|------|---------------|--------------|------|
| `gauss_noise_stripe.png` | 512×16 | `_draw_gauss_effects` | Тайл вдоль луча, скролл UV |
| `gauss_glow_radial.png` | 128×128 | вдоль луча + **flash** на импакте | Штампы glow; вспышка в `fx.end` |
| `gauss_muzzle_atlas.png` | 256×64 (4 кадра) | у `fx.start`, первые `muzzle_life_s` | Вспышка у дула |
| `gauss_impact_ring.png` | 128×128 | `fx.end` | Кольцо попадания |
| `necron_glyphs_atlas.png` | 256×256 (4×4) | вдоль луча | Руны; fallback — процедурные штрихи |
| `gauss_scorch_decal.png` | 96×96 | decals под юнитами | Ожог земли у цели |

Загрузка: `_load_fx_assets()` в `opengl_view.py` → `self._fx_pixmaps`.

---

## 4. Слои отрисовки (порядок в `_draw_gauss_effects`)

1. Tube — толстая линия glow (pen)  
2. **noise_stripe** — tiled  
3. **glow_radial** — штампы по длине  
4. **muzzle_atlas** — 4 кадра  
5. Core — две параллельные линии  
6. Pulse — бегущие сегменты  
7. Edge specks — точки по краям (процедурно)  
8. Branches — ответвления (процедурно)  
9. **necron_glyphs** — атлас или линии  
10. **glow_radial** — impact flash  
11. **impact_ring**  
12. Particles у цели  

Порядок `paintGL` (релевантное): ground → grid → … → **decals** (scorch) → units → FX → popups.

---

## 5. Важные исправления

### Scorch не был виден

- **Причина:** `render_decals = False` по умолчанию — весь decals-слой, включая scorch, не вызывался.  
- **Исправление:** `paintGL` рисует decals, если `render_decals or _fx_scorch_decals`.  
- Размер scorch в **долях клетки** (`scorch_base` × `scorch_scale`), не в сырых пикселях текстуры.  
- Смещение перпендикулярно лучу (`scorch_offset_px_min/max`), `scorch_alpha` ≈ 0.95.

### Beam / профили

- Толщина луча и sprite-множители подогнаны под Flayer (тоньше) vs Reaper (тяжелее).  
- `*_px` в конфиге — экранные пиксели; `opengl_view._px_to_world()` переводит в координаты доски.

---

## 6. Текущие настройки видимости (после полировки)

### Глифы (оба оружия, блок `glyphs` у Flayer)

- `glyph_sprite_scale`: **1.6**  
- `alpha_min` / `alpha_max`: **0.12** / **0.26**  
- Reaper дополнительно: `glyph_count_scale` 1.28, `glyph_pulse_speed` 1.35  

### Muzzle

| | Flayer | Reaper |
|--|--------|--------|
| `muzzle_life_s` | 0.20 | 0.26 |
| `muzzle_scale` | 1.28 | 1.58 |
| `muzzle_stretch_x` | 1.06 | 1.28 |

Длительность и fade читаются из конфига в `opengl_view` (не захардкожены 0.14 с).

### Scorch (база в `_GAUSS_BEAM_SPRITE` + Reaper)

- Flayer: `scorch_base` 0.42, `scorch_scale` 1.2  
- Reaper: `scorch_base` 0.52, `scorch_scale` 1.55  

---

## 7. Ключевые файлы

| Область | Путь |
|---------|------|
| Профили FX | `app/viewer/gun_fx.py` |
| Отрисовка + spawn | `app/viewer/opengl_view.py` |
| Слой FX | `app/viewer/rendering/layers/fx.py` |
| Scorch decals | `app/viewer/rendering/layers/decals.py` |
| События лога | `app/viewer/app.py` |
| Bake ассетов | `tools/viewer/bake_gauss_fx_assets.py` |
| Ассеты | `app/viewer/assets/fx/*.png` |

---

## 8. Как проверить

1. Запустить viewer, бой с Necron Warriors (Gauss flayer / reaper).  
2. Выстрел: луч, muzzle у ствола (первые ~0.2–0.26 с), glyphs вдоль луча, импакт у цели.  
3. После попадания: scorch под ногами цели (~1.8–2 с), если не закрыт спрайтами.  
4. Сравнить Flayer (тоньше) и Reaper (толще, крупнее muzzle/импакт).  

Тесты QML-ассетов (если есть): `python -m unittest tests.viewer.test_qml_assets`.

---

## 9. Что не в scope / дальше

- Gauss только для оружий в `GUN_FX_CONFIGS` / `WEAPON_ALIASES`.  
- Pulse / edge specks / branches на скриншоте почти не читаются — отдельная настройка при желании.  
- Scorch намеренно **под** юнитами; для «героического» кадра можно поднять слой или `scorch_base`.  
- Shader pilot / полный отказ от QPainter — по [viewer_modernization_roadmap.md](viewer_modernization_roadmap.md).  

---

## 10. Связанные документы

- [viewer_migration_plan.md](viewer_migration_plan.md) — спринты, флаги, DoD  
- [viewer_modernization_roadmap.md](viewer_modernization_roadmap.md) — стратегия  
- [viewer_baseline_metrics.md](viewer_baseline_metrics.md) — метрики до/после  
