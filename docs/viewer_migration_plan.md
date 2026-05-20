# 40kAI Viewer Migration Plan — QML-hybrid (executable)

> **Status:** Draft, pending review.
> **Companion document:** [viewer_modernization_roadmap.md](viewer_modernization_roadmap.md) (strategy / phases / KPI).
> **This document:** sprint-level tasks, contracts, DoD, verifiable artefacts, governance, CI, packaging.

---

## Executive summary

| Phase | Span | Outcome |
|---|---|---|
| Sprints 1–2 | Weeks 1–2 | Baseline + frozen contracts + shared `tokens.json`; viewer visually aligned with launcher behind flag. |
| Sprints 3–5 | Weeks 3–5 | `ViewerController`; modular render layers; god-classes shrunk without behaviour change (flags). |
| Sprints 6–8 | Weeks 6–8 | FX polish; QML right column + log + key dialogs; protocol `1.0`; full A11y pass. |
| Sprint 9 | Week 9+ | Hardening, optional shader pilot, release candidate; flip defaults when stable. |

**Definition of “plan complete”:** all flags can default ON on `main`; legacy paths removable or deprecated one release later; companion docs listed in §17 exist and are kept current.

---

## 0. Decision record

- **Path chosen:** QML-hybrid. Game board stays as `OpenGLBoardWidget` (QPainter on `QOpenGLWidget`); UI "chrome" (right panel, status, log, commands, dialogs) migrates to QML and consumes the same theme tokens as `app/gui_qt`.
- **Path rejected:** Full Godot rewrite. Reason: doubles the runtime, doubles the contract surface (WS + state.json), and we already invested in QML for the launcher/training UI.
- **Path deferred:** Qt Quick 3D / shader-heavy board rewrite. Revisit only after Phase 4 ships and only if QPainter genuinely caps out.

---

## 1. Reality check (As-Is, measured 2026-05-20)

| Area | Fact | Implication |
|---|---|---|
| `app/viewer/app.py` | 3 534 LOC, `ViewerWindow` is one class spanning lines 279–3528 (~3 250 LOC god-class) | Cannot be migrated in one step. Must be sliced behind a controller before any QML is written. |
| `app/viewer/opengl_view.py` | 6 554 LOC, single `OpenGLBoardWidget` owns 16 helper classes (UnitRender, FX, particles, decals, popups, status layout, texture mgr) | Layer split is the prerequisite for any visual change without regression. |
| `app/gui_qt/qml/` | Ready: `ChamferPanel`, `HexAvatar`, `StyledComboBox`, `TacticalCheckBox`, `TacticalTabButton`, `TrainMiniBoard` | These are the **source of truth** for tokens. Viewer should consume them, not re-invent. |
| `app/viewer/styles.py` | 4 KB, viewer-local | Will be reduced to a thin adapter over shared tokens. |
| `app/viewer/viewer_config.json` | 287 B, minimal | Gets new sections: `theme`, `fx`, `animation`, `debug`. |
| State contract | Implicit — `ViewerWindow` reads `state.json` and `model_events` directly | Must be made explicit before slicing the controller. |

---

## 2. Architectural target

```
app/viewer/
  __main__.py
  config.py                       # typed access to viewer_config.json
  controller/
    viewer_controller.py          # QObject, single bridge for QML + Widgets
    state_adapter.py              # parses state.json -> typed snapshot
    commands.py                   # action dispatch (no business logic)
  rendering/
    board_widget.py               # thin QOpenGLWidget orchestrator
    layer_context.py
    board_geometry.py
    board_camera.py
    hit_test.py
    animation_timeline.py
    layers/
      ground_layer.py
      grid_layer.py
      objectives_layer.py
      labels_layer.py
      movement_layer.py
      shooting_layer.py
      units_layer.py
      fx_layer.py
      debug_overlay_layer.py      # behind viewer.debug.overlay flag
  ui/
    legacy/                       # current ViewerWindow, frozen during migration
    qml/
      ViewerMain.qml              # root QQuickWidget
      panels/
        StatusPanel.qml
        CommandsPanel.qml
        LogPanel.qml
        UnitInfoPanel.qml
      dialogs/                    # QML-side input dialogs (later phase)
  theme/
    tokens.py                     # Python view of shared tokens
```

`ViewerController` is the **only** object QML and the legacy window both talk to. No QML file may import from `core.engine.*`.

---

## 3. Contracts (freeze before Phase 1)

### 3.1 State snapshot (`StateSnapshot`)

Typed dataclass produced by `state_adapter.py`. Fields (initial set, extend per phase):

- `protocol_version: str` — bump on breaking changes.
- `round: int`, `phase: str`, `active_player: int`.
- `vp: dict[int, int]`, `cp: dict[int, int]`.
- `units: list[UnitSnapshot]` (id, owner, position, models, status, selected).
- `objectives: list[ObjectiveSnapshot]`.
- `pending_request: RequestSnapshot | None` (the "engine is waiting for input" marker).
- `model_events: list[ModelEvent]` — append-only since last snapshot, drained on read.
- `log_entries: list[LogEntry]` — last N, ring-buffered.

### 3.2 Controller surface (`ViewerController`)

**Properties (notify on change):** `round`, `phase`, `activePlayer`, `vp`, `cp`, `selectedUnitId`, `pendingRequest`, `boardCursor`, `fxQuality`.
**Signals:** `stateUpdated`, `unitSelected(id)`, `logAppended(entry)`, `fxTriggered(event)`.
**Slots (callable from QML or Widgets):** `selectUnit(id)`, `submitChoice(...)`, `cancelPending()`, `setFxQuality(level)`, `requestRedraw()`.

### 3.3 Theme tokens (`theme/tokens.json` — single source of truth)

**Canonical path (recommended):** `theme/tokens.json` at repo root (or `app/theme/tokens.json` — pick one in Sprint 2 kickoff PR and document here). Same file is loaded by:

- `app/gui_qt/qml/` via a small QML singleton / loader.
- `app/viewer/theme/tokens.py` for Widgets/`QPainter` colours.

Sections: `color` (bg/surface/text/accent/warn/danger + alpha tints), `radius`, `spacing`, `font` (family/size/weight per role), `motion` (durations, easings). Optional `schema_version` inside JSON for tooling.

**Validation:** JSON schema file `theme/tokens.schema.json`; validate on viewer **and** launcher startup (fail fast in dev; log + fallback to baked defaults in release only if explicitly allowed by flag).

**Ownership:** see §9 — theme owner approves any breaking token rename.

### 3.4 Feature flags (`viewer_config.json`)

- `viewer.theme.v2` — new tokens applied to viewer.
- `viewer.controller.v1` — controller-mediated state path.
- `viewer.render.layers_v2` — modular layer pipeline.
- `viewer.fx.v2` — improved effects.
- `viewer.ui.qml_panels` — QML right column.
- `viewer.debug.overlay` — hit-test / layer debug layer.
- `viewer.shaders.highlights` — shader path for highlights (Phase 5).

Each flag has a documented OFF behaviour identical to current main.

### 3.5 Reference machine (performance & visual baselines)

Lock one **reference Windows** profile for Sprint 1 and reuse for all frametime KPIs:

- OS build, display resolution, **Windows scale %**, GPU model & driver version, CPU tier.
- Document in `docs/viewer_baseline_metrics.md`.

Optional secondary profile (laptop iGPU) — **informational only** until Sprint 6; does not block merge unless regression > agreed threshold on reference machine.

---

## 4. Sprint plan

Each sprint = ~1 week. Adjust to actual cadence; gates are DoD, not calendar.

### Sprint 1 — Baseline & contract freeze

**Tasks**
1. Add `tools/perf/measure_viewer.py`: launches viewer with scripted scenario, records frametime p50/p95, CPU%, GPU% if available, dumps to `docs/viewer_baseline_metrics.md`.
2. Capture golden screenshots for: deploy start, mid-movement, shooting FX, long log scroll, end-of-round transition. Store in `docs/media/viewer_baseline/`.
3. Define `StateSnapshot` dataclass and write `state_adapter.py` (read-only path; no behaviour change yet).
4. Write `tests/viewer/test_state_adapter.py`: parse 5 recorded `state.json` fixtures, assert snapshot fields and event ordering.
5. Document state contract in `docs/viewer_state_contract.md`.

**DoD**
- Baseline numbers committed.
- `state_adapter` parses every fixture without error.
- No behaviour change for end users.

### Sprint 2 — Theme tokens extracted

**Tasks**
1. Extract current QML tokens from `ChamferPanel.qml`, `Tactical*.qml` into `theme/tokens.json`.
2. Add `theme/tokens.schema.json` and a tiny validator (Python stdlib `jsonschema` optional; if avoided, use hand-checked asserts + documented required keys).
3. Adapt `app/gui_qt/qml/` to read tokens from the JSON (one `Theme` singleton in QML).
4. Add `app/viewer/theme/tokens.py` reader; rewrite `app/viewer/styles.py` as adapter.
5. Apply tokens behind `viewer.theme.v2` flag to the easy widgets first: `QGroupBox`, `QLabel`, `QPushButton`. Leave `QTableWidget` / log list for next sprint.
6. Visual diff: capture same golden screenshots with flag ON, attach to PR.
7. **Early A11y gate:** contrast spot-check on text vs `bgSurface` / `bgElevated` for primary labels and buttons (WCAG AA target); fix token values before they propagate to every panel.

**DoD**
- Flag OFF == byte-identical to baseline (or within snapshot tolerance).
- Flag ON: launcher and viewer are visibly the same family.
- DPI sweep tested at 100 / 125 / 150 %.
- Early A11y checklist (§16.1) signed for token-derived surfaces only.

### Sprint 3 — `ViewerController` introduced

**Tasks**
1. Create `controller/viewer_controller.py` as `QObject` subclass; expose properties/signals/slots from §3.2.
2. Re-route `ViewerWindow` to read state via `controller`, not directly. Window becomes a *consumer*, not the owner.
3. Move ad-hoc presentation logic out of `ViewerWindow` into the controller. Goal: `ViewerWindow` < 2 000 LOC by end of sprint.
4. Add `tests/viewer/test_controller.py`: feed snapshots, assert signal emissions and selectedUnitId transitions.
5. Behind `viewer.controller.v1` flag; OFF path keeps current direct-state code.

**DoD**
- All UI updates flow through controller signals when flag is ON.
- Click/select/hover behaviour unchanged in golden scenarios.
- ViewerWindow LOC reduction documented in PR description.

### Sprint 4 — Render skeleton (easy layers)

**Tasks**
1. Introduce `LayerContext` (painter, transform, snapshot, config, debug-flags).
2. Extract `ground_layer`, `grid_layer`, `labels_layer`, `objectives_layer` out of `OpenGLBoardWidget`.
3. `OpenGLBoardWidget.paintGL` becomes: prepare context → iterate layer stack → debug overlay.
4. Add snapshot tests: render each layer to offscreen `QImage`, compare to fixture (per-pixel allowed delta documented).
5. Behind `viewer.render.layers_v2` flag.

**DoD**
- 4 layers extracted, each independently testable.
- Frametime within ±5 % of baseline.
- Visual diff under tolerance.

### Sprint 5 — Render skeleton (hard layers)

**Tasks**
1. Extract `movement_layer`, `shooting_layer`, `units_layer`, `fx_layer`.
2. Move `hit_test` into its own module; expose as `controller.hitTest(point) -> HitResult`.
3. Add `debug_overlay_layer` (hit-rects, last click, frame counter) behind `viewer.debug.overlay`.
4. Reduce `opengl_view.py` to ≤ 1 500 LOC orchestrator.

**DoD**
- All gameplay layers extracted.
- Interaction regression tests green.
- Soak test: 10-min match, no layer leak / FPS drift > 5 %.

### Sprint 6 — FX polish (no QML yet)

**Tasks**
1. Selection / hover / target unified visual language. Easing pulled from `theme/tokens.json` (`motion` section).
2. Movement animations: stagger per-model, cubic-out by default.
3. Shooting FX: cleaner glow, unified hit flashes, readable damage popups.
4. `fx_quality = low | medium | high` honoured by every effect; `low` must hit baseline frametime on the reference machine.
5. Hidden behind `viewer.fx.v2`.

**DoD**
- Side-by-side video baseline vs new attached to PR.
- Each quality level has its own measured frametime.

### Sprint 7 — QML right column (status + commands)

**Tasks**
1. Embed `QQuickWidget` as the right column container. Old widgets stay underneath behind a stack widget controlled by `viewer.ui.qml_panels`.
2. Implement `StatusPanel.qml` (round, phase, VP, CP, active unit) bound to controller properties.
3. Implement `CommandsPanel.qml` for the buttons currently in `ViewerWindow`. Slots route to `controller.submitChoice(...)`.
4. Hot-reload dev mode: env var `VIEWER_QML_RELOAD=1` enables `QQmlEngine.clearComponentCache()` on file change.
5. Tests: drive controller from Python, assert QML bindings update (use `QSignalSpy` on property change signals).

**DoD**
- Status + commands panels fully QML when flag ON.
- Keyboard shortcuts unchanged.
- No duplicated state between QML and Python.

### Sprint 8 — QML log panel + dialogs

**Tasks**
1. `LogPanel.qml` with virtualised list (`ListView` + delegate). Replaces `HoverLogListWidget` behind flag.
2. Migrate the most common input dialog (choice / dice prompt) to QML; others can wait.
3. Accessibility pass: contrast (WCAG AA), tab order, focus rings on QML controls.
4. Lock the contract from §3 — promote `protocol_version` to `1.0`.

**DoD**
- Right column is fully QML in flag-ON mode.
- A11y checklist signed off.
- All existing keyboard / shortcut tests green.

### Sprint 9 — Hardening + selective shaders (optional)

**Tasks**
1. Pilot one shader effect: highlight platform glow. Painter fallback stays under `viewer.shaders.highlights = off`. Auto-fallback on shader compile error (log once, switch flag).
2. Soak test: 60-min match with FX high, log p95 frametime per minute, no monotonic drift.
3. RDP smoke test (`QOpenGLWidget` known-flaky over RDP). Document supported/unsupported configs.
4. Release-candidate cut.
5. **Default-flag proposal:** document which flags flip to ON by default on `main` (requires perf + screenshot sign-off). Criteria in §14.

**DoD**
- Shader has measured win > 15 % over painter version on reference GPU, or it gets cut.
- Fallback verified by forcing compile failure in CI.
- Release notes drafted.
- Written decision on default flags + rollback procedure (§12).

---

### Sprint 10 — Cleanup & legacy retirement (recommended)

Run after Sprint 9 stabilises on reference machine for ≥1 week.

**Tasks**
1. Enable safe flags ON by default (`viewer.theme.v2`, `viewer.controller.v1`, `viewer.render.layers_v2`, `viewer.ui.qml_panels` subject to §14).
2. Delete or thin dead branches behind OFF paths where coverage proves parity.
3. Update `README.md` / `docs/START_HERE.md` with new viewer architecture diagram + env vars.
4. Final LOC audit: `ViewerWindow`, `opengl_view.py` vs targets from Sprint 3–5.

**DoD**
- Single supported path documented; deprecated paths tagged or removed.
- Installer/package smoke passes (§12).

---

## 5. Risk register (delta from roadmap §13)

| Risk | Mitigation in this plan |
|---|---|
| `ViewerWindow` god-class blocks every later sprint | Sprint 3 is dedicated to controller extraction *before* any visual work. |
| Two sources of truth for theme | Sprint 2 makes `theme/tokens.json` canonical; QML and Python both read it. |
| QML/Python state duplication | Hard rule: no `property var` in QML mirrors anything from `controller`. Reviewed in PR template. |
| OpenGL on RDP | Sprint 9 documents supported configs; raise earlier if any team member dev-RDPs. |
| Shader fallback drift | Painter path is the canonical reference; shader is a flagged optimisation, not a replacement. |
| Test brittleness from pixel snapshots | Allowed per-pixel delta documented per layer; visual tests run only on Linux/Windows reference DPI. |
| Silent shader/QML failures in the field | §14 observability + §12 installer verification + forced-failure tests in CI. |
| Parallel features re-expand god-classes | §13 freeze rules + PR template checklist. |

---

## 6. Verification matrix

For every sprint PR:

- [ ] Flag-OFF golden screenshots byte-equal (within tolerance) to previous sprint's baseline.
- [ ] Flag-ON screenshots attached, reviewed.
- [ ] Frametime p50/p95 reported (`tools/perf/measure_viewer.py`).
- [ ] Interaction regression test green (click / hover / select / drag).
- [ ] `tests/viewer/` green.
- [ ] No new dependency on `core.engine.*` from `ui/qml/`.
- [ ] CI matrix satisfied for changed areas (§11); if skipped, reason documented in PR.
- [ ] If tokens/QML/assets touched: packaged build smoke or documented manual installer check (§12).
- [ ] No duplicate mutable state introduced between QML and `ViewerController` (PR self-review checklist §13).

---

## 7. Out of scope (explicitly)

- Replacing `OpenGLBoardWidget` with `QQuickPaintedItem` or Qt Quick 3D. Reconsider after Sprint 9.
- Migrating game logic, AI, or `core/engine/*`.
- Network / multiplayer changes.
- Asset pipeline rework beyond DPI normalisation.
- Localisation overhaul (tokens leave room for it; no migration here).

---

## 8. First concrete step (kickoff)

Sprint 1, task 3 — write `controller/state_adapter.py` and freeze `StateSnapshot`. Everything else depends on that contract. No code touches `ViewerWindow` in Sprint 1.

---

## 9. Governance & ownership

| Artefact | Owner responsibility |
|---|---|
| `StateSnapshot` shape & `protocol_version` bumps | Viewer / integration owner — breaking changes require changelog entry in `docs/viewer_state_contract.md` |
| `theme/tokens.json` & schema | UI/theme owner — approves renames; coordinates launcher + viewer |
| Feature flags defaults | Tech lead — Sprint 9 decision + rollback owner |
| `ViewerController` API (properties/signals/slots) | Viewer owner — QML consumers must not bypass |
| Render layer boundaries | Rendering owner — prevents circular imports between layers |
| CI expectations | Repo maintainer — §11 gates |

**PR template checklist (copy into `.github/pull_request_template.md` when ready):**

- [ ] Flags documented (ON/OFF behaviour).
- [ ] No QML→`core.engine.*` imports.
- [ ] No mirrored `property var` state (QML binds to `controller` only).
- [ ] Screenshots or video for visual change.
- [ ] If contract change: `protocol_version` bump + compat note in `docs/viewer_state_contract.md`.

---

## 10. Protocol compatibility & `state.json`

`state.json` is **engine-owned**; the viewer only **adapts** it. Policy:

1. **`StateSnapshot.protocol_version`** follows semantic intent: bump **minor** for additive fields; **major** for renames/removals/changed meaning.
2. **Adapter behaviour**
   - Unknown fields: ignored (forward compatible).
   - Missing fields: adapter supplies documented defaults **or** sets `snapshot.degraded = True` with a user-visible banner (preferred for critical fields like board size).
   - Parse errors: log once + keep last good snapshot + show error overlay on board (no silent empty UI).
3. **Fixtures:** every adapter change adds or updates a fixture under `tests/viewer/fixtures/state_*.json` with a one-line comment describing the scenario.
4. **Engine sync:** if `core/engine` changes output shape, either update adapter in same PR or file a blocker with temporary `protocol_version` negotiation documented in `docs/viewer_state_contract.md`.

Promote **`protocol_version` to `1.0`** in Sprint 8 when QML panels and controller path are stable (as already noted in plan).

---

## 11. CI matrix & test environments

**Goals:** predictable green; avoid flaky OpenGL/DPI tests on random agents.

| Check | Where it runs | Notes |
|---|---|---|
| `tests/viewer/test_state_adapter.py` | Linux + Windows CI | Pure Python; always on |
| Controller unit tests | Linux + Windows | Mock `QObject`; headless OK |
| Layer pixel tests (Sprint 4+) | **Reference Windows agent only** OR nightly | Document tolerance; skip on other jobs with explicit `pytest.skip` reason |
| Optional: `measure_viewer.py` | Nightly / manual | May need GPU; not a merge blocker if documented |
| QML syntax / `qmlformat` | Optional | Add if team wants; not required day 1 |

**Headless / VM caveats:** document that GL context may differ; pixel tests must not run on configs without stable Qt GL.

---

## 12. Packaging, installer & rollback

**Requirement:** QML files and `theme/tokens.json` ship beside the viewer executable / Python bundle.

Checklist before flipping defaults:

1. Verify PyInstaller/spec or installer scripts include:
   - `app/viewer/ui/qml/**`
   - `theme/tokens.json` (+ schema if validated at runtime)
   - existing viewer assets under `app/viewer/assets/**`
2. Cold-start smoke: launch packaged viewer, open Play flow, verify right panel renders when flag ON.
3. **Rollback:** ship `viewer_config.json` defaults with conservative flags; document env overrides (`VIEWER_*`) if introduced.

If shader pilot ships: compile failure must **never** brick release — auto-disable + painter path (Sprint 9).

---

## 13. Parallel development & freeze rules

During Sprints 3–6 (controller + layers + FX):

1. **Avoid new UI logic inside `ViewerWindow`.** New presentation hooks go through `ViewerController` or board layers.
2. **Bugfixes** in legacy code allowed only if duplicated controller path is updated when `viewer.controller.v1` is ON.
3. **Feature freeze (soft):** non-migration viewer features require tech-lead ack and must land behind flags.
4. **Conflict resolution:** if two PRs touch `OpenGLBoardWidget.paintGL`, rendering owner rebases layer stack order explicitly.

---

## 14. Runtime observability & diagnostics

Minimal structured diagnostics (stderr or `runtime/logs/` viewer channel):

| Event | When |
|---|---|
| `viewer_startup_ms` | Total init until first frame |
| `qml_load_ok` / `qml_error` | QQuickWidget/engine failures |
| `tokens_validate_ok` / `tokens_fallback` | Theme load |
| `adapter_protocol` | Parsed `protocol_version` |
| `frametime_p95_sample` | Optional rolling window when `viewer.debug.perf=1` |
| `shader_compile_fail` | Sprint 9 — triggers auto-fallback |

Use `qWarning`/`print` with stable prefixes (e.g. `[VIEWER]`) so logs are grep-friendly. Do not collect personal data.

**Default-flag flip criteria:** all P0 scenarios pass on reference machine with flags ON; p95 frametime not worse than baseline by more than agreed budget (e.g. 5–10%); no open blocker bugs in QML load or adapter parse.

---

## 15. UX acceptance criteria (non-purely-metric)

Beyond FPS and pixels, each visual-affecting sprint should tick at least **two** relevant items:

1. Status line readable at a glance (round / phase / active side) without parsing dense text.
2. Target / valid move / invalid move visually distinct; colour is not the only cue.
3. Damage and shoot feedback readable within 200–500 ms without blocking the board.
4. Log panel scroll performance acceptable on long matches (no “stuck” feel).
5. Command area: primary action visually obvious; destructive actions guarded.
6. Keyboard flow: focus does not trap in QML panel (Sprint 7+).

---

## 16. Accessibility

### 16.1 Early gate (Sprint 2)

- Token contrast for body text and labels on surfaces (target WCAG AA where applicable).
- Focus visible on focusable Widgets touched by migration (buttons at minimum).

### 16.2 Full pass (Sprint 8)

- QML tab order, focus rings, `Accessible.name` / roles on key controls.
- No time-based-only information without static alternative (where applicable).
- Scale 125–150%: no clipped command labels in right column.

---

## 17. Companion artefacts (create as the work lands)

| Document | Created in | Purpose |
|---|---|---|
| `docs/viewer_baseline_metrics.md` | Sprint 1 | Perf numbers + reference machine |
| `docs/viewer_state_contract.md` | Sprint 1 | `StateSnapshot` + `state.json` field notes |
| `docs/media/viewer_baseline/` | Sprint 1 | Golden captures |
| `theme/tokens.json` + `theme/tokens.schema.json` | Sprint 2 | Shared design tokens |
| `docs/viewer_ci_matrix.md` | Sprint 2–4 | Expand §11 if CI grows |
| `docs/viewer_release_checklist.md` | Sprint 9 | Ship gates + rollback |

Keeping these updated is part of DoD for the sprint that introduces them.

---

## 18. Alignment with roadmap

This plan is the **executable slice** of [viewer_modernization_roadmap.md](viewer_modernization_roadmap.md):

- Roadmap §6–11 ↔ Sprints 2–9 here.
- Roadmap KPI ↔ §14 reference machine + verification matrix.
- Long-term backlog (roadmap §17) stays out of scope unless explicitly pulled into a sprint.
