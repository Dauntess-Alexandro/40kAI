# Love2D Viewer (только визуал)

Этот viewer читает состояние из `viewer_state.json` и рисует сцену в стиле grimdark/top-down.

## Быстрый старт
1. Установи Love2D (0.10+ / 11.x).
2. Скопируй папку ассетов в `viewer_love2d/assets` со структурой:
   - `assets/ground/`
   - `assets/props/`
   - `assets/shadows/`
   - `assets/fx/`
   - `assets/decals/`
   - `assets/units/`
3. Создай файл `viewer_state.json` рядом с `main.lua` (пример ниже).
4. Запусти:
   ```bash
   love viewer_love2d
   ```

## Пример `viewer_state.json`
```json
{
  "camera": {"x": 0, "y": 0, "zoom": 1.0},
  "ground": {"tile": "ground_01.png"},
  "units": [
    {"id": 1, "x": 520, "y": 310, "sprite": "necron_01.png", "shadow": "shadow_small.png", "dir": 90}
  ],
  "props": [
    {"x": 400, "y": 520, "sprite": "tree_01.png", "shadow": "shadow_medium.png"}
  ],
  "fx": [
    {"type": "smoke_01.png", "x": 540, "y": 300}
  ],
  "decals": [
    {"type": "blood_01.png", "x": 480, "y": 290, "rotation": 0.2, "scale": 1.0}
  ]
}
```

## Как обновлять данные из Python
- Python пишет `viewer_state.json` (например, раз в 100–200 мс).
- Love2D читает файл и перерисовывает сцену.

## Подсказки
- Тени должны быть отдельными спрайтами (рисуются под объектами).
- Декали (кровь/ожоги) рисуются на отдельном слое.
- Если нужно ускорить — можно увеличить интервал чтения JSON.

## Python-экспорт (минимальный пример)
Если хочешь, чтобы Python сам обновлял сцену, запусти скрипт:
```bash
python viewer_love2d/export_viewer_state.py
```
Скрипт будет каждые ~0.15 сек записывать `viewer_state.json`. Love2D автоматически подхватит изменения.
