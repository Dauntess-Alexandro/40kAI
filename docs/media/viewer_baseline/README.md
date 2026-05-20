# Viewer baseline screenshots

Golden captures for visual regression during viewer migration.

## Required scenes (capture manually)

Save PNG files here with descriptive names, for example:

| Filename | Scene |
|---|---|
| `deploy_start.png` | Deployment phase just started |
| `mid_movement.png` | Movement overlay visible |
| `shooting_fx.png` | Shooting VFX active |
| `long_log.png` | Log scrolled deep into a match |
| `end_round.png` | Phase / round transition |

## Capture checklist

- Display scale: note 100% / 125% / 150% in PR or filename suffix.
- Viewer window maximised or fixed resolution — stay consistent across runs.
- Same `runtime/state/state.json` scenario where possible.

Once captures exist, reference them from migration PRs against Sprint 1 DoD.
