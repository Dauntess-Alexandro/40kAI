# Viewer `state.json` contract (viewer-side adapter)

This document freezes the **viewer read contract** for migration Sprint 1+.  
The canonical writer is `core/engine/state_export.py`; the typed consumer entry point is:

- `app.viewer.controller.state_adapter.adapt_snapshot`
- `app.viewer.controller.state_adapter.adapt_snapshot_from_file` (wraps `app.viewer.state.load_state`)

Unknown top-level keys MUST be ignored by the adapter. Breaking changes to fields listed below require bumping **`viewer.state_protocol_version`** inside the JSON `viewer` object (see §3).

---

## 1. Root object

| Field | Type | Notes |
|---|---|---|
| `board` | object | Dimensions; see §2 |
| `turn` | int \| null | Turn marker |
| `round` | int \| null | Round marker |
| `phase` | string \| null | e.g. `command`, `movement`, `deployment` |
| `active` | string \| null | Active side; alias `active_side` |
| `vp` | object | Keys `player`, `model` → int VP |
| `cp` | object | Keys `player`, `model` → int CP |
| `units` | array | Unit payloads; see §4 |
| `objectives` | array | Objective markers |
| `terrain_features` | array | Terrain export blobs |
| `movement_overlay` | object \| null | Reachable cells overlay |
| `deployment` | object | Deploy-phase metadata |
| `viewer` | object | Viewer hints / protocol version |
| `log_tail` | array of string | Tail of textual log |
| `model_events` | array | Append-only engine/model events (ordering preserved) |
| `payload_kind`, `generated_at`, … | various | Ignored by adapter unless future sprint needs them |

Coordinates follow engine convention already documented in viewer code: **`x` = column, `y` = row** in state space.

---

## 2. `board`

Typical keys (first match wins per axis):

- Width: `width`, `cols`, `board_w`
- Height: `height`, `rows`, `board_h`

If missing after merge with viewer defaults: **60 × 40**.

---

## 3. Viewer meta / protocol version

Inside `viewer` (object):

| Field | Meaning |
|---|---|
| `state_protocol_version` | Adapter-visible semver-ish string (default **`0.0`** if absent) |
| `protocol_version` | Accepted alias for the above |

Breaking rename/removal of fields in §1–§4 ⇒ bump **major**. Additive optional fields ⇒ bump **minor** (convention).

If `viewer` is present but **not an object**, the adapter treats it as `{}`, sets **`degraded=true`**, and continues.

---

## 4. Unit entries (`units[]`)

Minimum fields used by `UnitSnapshot`:

| Field | Type |
|---|---|
| `side` | string |
| `id` | int |
| `name` | string |
| `x`, `y` | int |
| `hp` | number |
| `alive_models` | int |

Additional keys (`model_positions`, `unit_status`, weapons, …) are preserved in raw JSON for existing widgets but not duplicated on `UnitSnapshot` until later sprints expand the dataclass.

---

## 5. Default merge behaviour

`adapt_snapshot(..., merge_defaults=True)` merges into the same defaults as `app.viewer.state._default_state()` so behaviour matches historic viewer loading.

---

## 6. Fixtures & tests

Golden inputs live under `tests/viewer/fixtures/`.  
Parser regressions are covered by `tests/viewer/test_state_adapter.py`.

---

## 7. Pending_request / controller bridge

Engine prompts for dice/targets still flow through `GameController` in-process; **there is no stable `pending_request` blob in `state.json` today.**  
When/if it appears in export, extend `StateSnapshot` + this doc in the same PR.

---

## 8. ViewerController (`viewer.controller.v1`)

When flag **`viewer.controller.v1`** is enabled (`app/viewer/viewer_config.json` → `flags`, or env `VIEWER_FLAG_VIEWER_CONTROLLER_V1=1`), header/status strings are computed once via `compute_status_labels(...)` and pushed through **`ViewerController`** (`app/viewer/controller/viewer_controller.py`) before widgets refresh.

Slots (`selectUnit`, `submitChoice`, `cancelPending`, `setFxQuality`, `requestRedraw`) delegate to `ViewerWindow` where behaviour already exists; expand alongside Sprint 7 QML panels.
