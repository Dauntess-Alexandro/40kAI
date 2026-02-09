# State v2: snapshot + event stream

## Snapshot (`state.json`)
Снимок — это “истина мира”. Версия формата фиксируется полем `version=2`.

Минимальный набор полей:
```json
{
  "version": 2,
  "board": {"width": 60, "height": 40},
  "turn": 1,
  "round": 1,
  "phase": "command",
  "active": "player",
  "vp": {"player": 0, "model": 0},
  "cp": {"player": 0, "model": 0},
  "units": [
    {"side": "player", "id": 11, "name": "—", "hp": 10, "x": 5, "y": 5}
  ],
  "objectives": [{"id": 1, "x": 10, "y": 10}],
  "generated_at": "2025-01-01T00:00:00Z"
}
```

`log_tail` может присутствовать как служебный блок, но **не используется для FX/анимаций**.

## Event stream (`state_events.jsonl`)
JSONL, append-only, версия `version=2`.

Обязательные поля каждого события:
```
version=2, event_id:int, turn:int, phase:str, type:str, t_ms:int, unit_id?:int
```

Примеры:
```json
{"version":2,"event_id":1,"turn":1,"phase":"command","type":"phase_start","t_ms":1735689600000}
{"version":2,"event_id":2,"turn":1,"phase":"movement","type":"unit_selected","t_ms":1735689600500,"unit_id":21}
{"version":2,"event_id":3,"turn":1,"phase":"movement","type":"unit_move","t_ms":1735689600800,
 "unit_id":21,"from":{"x":5,"y":5},"to":{"x":7,"y":5}}
{"version":2,"event_id":4,"turn":1,"phase":"shooting","type":"shot","t_ms":1735689601200,
 "unit_id":21,"shooter":21,"target":12,"weapon":"Gauss flayer","hit":true,"damage":2,
 "line":{"start":{"x":7,"y":5},"end":{"x":9,"y":6}}}
{"version":2,"event_id":5,"turn":1,"phase":"shooting","type":"unit_hp","t_ms":1735689601300,
 "unit_id":12,"hp_before":10,"hp_after":8}
{"version":2,"event_id":6,"turn":1,"phase":"shooting","type":"unit_killed","t_ms":1735689601400,
 "unit_id":12}
```

### Типы событий (минимально достаточные)
- `phase_start`, `phase_end`
- `unit_selected`
- `unit_move`
- `shot`
- `unit_hp`, `unit_killed`
- `camera_focus` (опционально)
- `fx_spawn` (опционально)

## Playback правила (no-teleport)
1) Snapshot применяется **только когда очередь событий пуста** или при **ресинке**.
2) Все движения, стрельба, FX и камера проигрываются **строго по событиям**.
3) Перемотка фазы делается быстрым проигрыванием событий, без диффа snapshot.

## Порядок фаз и клавиши
Стандартный порядок фаз: `command → movement → shooting → charge → fight`.

Клавиши в GUI:
- **Left** — предыдущая фаза
- **Right** — следующая фаза
- **Enter/Space** — шаг по событию
- **Up/Down** — скорость (опционально)
