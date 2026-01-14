## What changed (Jan 2026)

### Gameplay / Engine
- Added **Necrons** faction support and **Necron Warriors (x10)** unit data.
- Fixed weapon resolution when weapons were passed as strings (normalized names, removed tags like `[PISTOL]`, safe fallback to avoid crashes).
- Fixed unit data consistency issues (e.g. `Weapons` key usage) so training/play works reliably.
- Increased episode turn limit from **5 to 10** turns.

### Manual play improvements
- Added **MANUAL_DICE=1** mode for entering dice results in terminal.
- Added verbose roll logging / shooting reports (hit/wound/save/damage breakdown) when manual dice or `VERBOSE_LOGS=1`.

### Metrics
- Added extra training metrics: **winrate**, **VP diff**, and **end reasons** (wipe / turn_limit / etc).
- Metrics export includes CSV + additional plots.

### GUI
- Added **Necrons** faction to Model/Player faction selectors and Army Viewer.
- Fixed radio-button layout overlap (Necrons no longer overlaps Tau).
