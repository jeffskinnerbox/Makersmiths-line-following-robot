# LFR Course — Development Plan

* **Project**: Line Following Robot (LFR) Course at Makersmiths
* **Author**: Instructor / Sole Developer
* **Created**: 2026-02-26
* **Last Updated**: 2026-02-26
* **Current Phase**: Phase 1 — Foundation (not yet started)

> Key decisions — GUI library, git workflow, testing strategy, MVP cut scope — emerged from a Q&A
> session. See [Appendix A][appendix-a] for the full dialogue.
> See [specification.md][spec] for the full project specification (hardware BOM, HAL interface
> definitions, module specs, test criteria). This plan does **not** duplicate those details;
> it adds build ordering, dependency tracking, and living-document machinery.

---------------

## How to Use This Document {#how-to-use}

This is a **living document**. Update it continuously as the project evolves.

**Every work session:**

* Tick completed deliverables (`[ ]` → `[x]`).
* Mark in-progress items (`[ ]` → `[~]`).
* Add any new blockers or decisions to [Open Questions][s-questions] or [Decision Log][s-decisions].

**After each phase milestone:**

* Update **Current Phase** in the header.
* Set phase status to `COMPLETE`.
* Create the git tag described in the phase section.
* Add a [Changelog][s-changelog] entry.

**When a decision changes:**

* Edit the existing entry in [Decision Log][s-decisions]; note the reversal date and reason.

**When a risk materialises:**

* Update the [Risk Register][s-risks] with outcome and resolution.

**For a new Claude Code session:**

* Point Claude at this file + `specification.md`. The [Document Status][s-status] and
    current-phase section give immediate context. Open Questions are the first thing to act on.

**Status markers used throughout:**

```text
[ ]  Pending — not yet started
[~]  In Progress — actively being worked
[x]  Done — complete and tested
```

---------------

## Table of Contents

1. [Document Status][s-status]
2. [Decision Log][s-decisions]
3. [Environment & Repository Bootstrap][s-env]
4. [Component Build Order & Dependency Map][s-buildorder]
5. [Phase 1 — Foundation][s-p1] (Month 1, Weeks 1–4)
6. [Phase 2 — Bang-Bang LFR + Simulator v1][s-p2] (Month 2, Weeks 5–8)
7. [Phase 3 — Track Designer + Sensor Upgrade][s-p3] (Month 3, Weeks 9–12)
8. [Phase 4 — WiFi UI + Open-Loop + PID][s-p4] (Month 4, Weeks 13–16)
9. [Phase 5 — Kalman Filter + Q-Learning][s-p5] (Month 5, Weeks 17–20)
10. [Phase 6 — Integration & Dress Rehearsal][s-p6] (Month 6, Weeks 21–24)
11. [MVP Cut — If Timeline Slips][s-mvp]
12. [Risk Register][s-risks]
13. [Open Questions Log][s-questions]
14. [Changelog][s-changelog]

[Appendix A — Development Dialogue][appendix-a]

---------------

## 1. Document Status {#s-status}

| Field | Value |
|:------|:------|
| Current phase | Phase 1 — Foundation |
| Phase status | In Progress |
| Last milestone reached | Phase 1 Weeks 1–3 all tasks complete (2026-02-28) |
| Next git tag to create | `phase1-foundation-complete` |

### What to work on right now

1. Phase 1 Weeks 1–3 code complete; one Week 3 task remaining (hardware).
2. Flash CircuitPython 9.x onto instructor Pico W; verify REPL — then tick Week 3 done.
3. Start Phase 1, Week 4 (chassis assembly + hardware integration).

---------------

## 2. Decision Log {#s-decisions}

Append-only. Newest entries at the top.

| ID | Date | Decision | Rationale |
|:---|:-----|:---------|:----------|
| D-008 | 2026-02-26 | Raspberry Pi Pico W GP8/Pin11 and GP9/PIN12 are consume by the board, no others | as stated on "Kitronik 5329 Product Page" and "Kitronik 5329 Datasheet" |
| D-007 | 2026-02-26 | MVP cut: Q-Learning hardware deployment deferred if Month 5 runs over | DS11 concept taught via simulator; Q-table not deployed to Pico W until post-course |
| D-006 | 2026-02-26 | Git workflow: tag main branch at each phase milestone | Simplest possible tracking; no branch overhead; tags are `phase1-foundation-complete`, etc. |
| D-005 | 2026-02-26 | Simulator parameter panel: pure pygame custom widgets | Fewest dependencies; full layout control; no extra pip packages |
| D-004 | 2026-02-26 | Desktop runtime: Python 3.12 / Ubuntu 24.04 LTS (Noble) | Newest LTS pair; stability for a 6-month development window |
| D-003 | 2026-02-26 | Testing strategy: simulator-first; hardware is final validation | One instructor robot during dev; simulator enables rapid iteration |
| D-002 | 2026-02-26 | LFR Simulator: custom Python / pygame build | Tight HAL integration required; existing simulators cannot run firmware modules unmodified |
| D-001 | 2026-02-26 | Line Track Designer: custom Python / pygame build | Exact tile size (11″×8.5″), shared `track.json` format, and PDF output make adaptation of existing tools as costly as building fresh |

---------------

## 3. Environment & Repository Bootstrap {#s-env}

**Do this once before any code is written. It is not phase-specific.**

### 3.1 Host Machine Requirements

| Item | Required Version | Notes |
|:-----|:----------------|:------|
| OS | Ubuntu 24.04 LTS (Noble) | [D-004][d-004] |
| Python | 3.12.x | System or `pyenv`; confirm with `python3 --version` |
| pip | latest | `pip install --upgrade pip` |
| git | ≥ 2.43 | Ships with Noble |

### 3.2 Python Dependencies

Install into a project virtualenv (`python3 -m venv .venv`):

```text
pygame          == 2.6.x    # simulator + track designer rendering
pytest          == 8.x      # all unit and simulation tests
pytest-cov                  # coverage reporting
reportlab       == 4.x      # PDF tile export (track designer)
```

No other third-party packages. Verify with `pip list` after install.

### 3.3 CircuitPython Constraint

Firmware modules (`firmware/`) must use **only CircuitPython-compatible syntax**.
They run on the Pico W (CircuitPython 9.x) *and* are imported by the desktop simulator
(Python 3.12). Restrictions:

* No `typing` module imports (use bare type hints in comments instead, or `from __future__ import annotations` only if CircuitPython 9 supports it — verify in [Q-002][q-002]).
* No `dataclasses`, no `threading`, no walrus operator.
* `abc.ABC` and `abc.abstractmethod` **are** available in CircuitPython 9.x — the HAL ABCs are safe.
* f-strings are safe (CircuitPython 7+).
* Keep all `import` statements at the top of each file (CircuitPython module loader limitation).

### 3.4 Repository Bootstrap

```bash
mkdir lfr_course && cd lfr_course
git init
python3 -m venv .venv
source .venv/bin/activate
pip install pygame pytest pytest-cov reportlab
```

Create the full directory skeleton (all `__init__.py` files and empty placeholder modules)
before writing any implementation code. This lets `pytest` discover all modules from day one
and lets the import graph be validated early.

```text
lfr_course/
    firmware/
        hal/
            __init__.py
            base.py             # HAL ABCs — write this first
            pico_hal.py
            sim_hal.py
        sensors/
            __init__.py
            ir_sensor.py
            reflectance_array.py
        speed_sensor/
            __init__.py
            speed_sensor.py
        controllers/
            __init__.py
            bang_bang.py
            open_loop.py
            pid.py
            kalman.py
            q_learning.py
        wifi/
            __init__.py
            web_server.py
        __init__.py
        config.py
        main.py
    simulator/
        __init__.py
        physics.py
        sensor_sim.py
        track.py
        visualization.py
        ui.py
        metrics.py
        plugin.py
        main.py
    track_designer/
        __init__.py
        tile_library.py
        canvas.py
        export.py
        save_load.py
        main.py
    tests/
        unit/
            __init__.py
        sim/
            __init__.py
        hardware/
            README.md           # checklists live here as markdown
    tracks/                     # track.json files saved here
    docs/                       # syllabus, lesson plans
    .venv/                      # gitignored
    pytest.ini
    .gitignore
    CLAUDE.md
    specification.md
    input/
        my-vision.md
        my-claude-prompts.md
        my-bom.md
    development-plan.md
```

`pytest.ini` minimum content:

```ini
[pytest]
testpaths = tests
addopts = --tb=short
```

`.gitignore` must include: `.venv/`, `__pycache__/`, `*.pyc`, `q_table.json` (regenerated by training).

---------------

## 4. Component Build Order & Dependency Map {#s-buildorder}

Build modules in strict dependency order. Never start a module before its dependencies exist
(even as stubs). This table is the authoritative build sequence.

```text
LAYER 0 — No dependencies
    config.py
    firmware/hal/base.py  (ABCs only — import from abc)

LAYER 1 — Depends on Layer 0
    firmware/hal/pico_hal.py       (implements base.py ABCs; hardware GPIO)
    firmware/hal/sim_hal.py        (implements base.py ABCs; delegates to simulator physics)
    simulator/physics.py           (standalone kinematics math)
    simulator/track.py             (loads track.json; no other project dep)

LAYER 2 — Depends on Layer 1
    firmware/sensors/ir_sensor.py  (uses SensorHAL from base.py)
    simulator/sensor_sim.py        (uses physics.py, track.py)
    firmware/main.py skeleton      (wires HAL + config; stubs only at this point)

LAYER 3 — Depends on Layer 2
    firmware/controllers/bang_bang.py     (uses SensorHAL, MotorHAL)
    simulator/visualization.py            (uses physics.py, track.py; pygame rendering)

LAYER 4 — Depends on Layer 3
    simulator/ui.py                (uses pygame; reads/writes config.py values)
    simulator/plugin.py            (importlib loader; requires controllers to exist)
    simulator/main.py              (wires all simulator modules)

LAYER 5 — Depends on simulator being functional
    track_designer/tile_library.py  (standalone SVG/geometry; no pygame yet)
    track_designer/canvas.py        (uses tile_library.py + pygame)
    track_designer/export.py        (uses tile_library.py + reportlab)
    track_designer/save_load.py     (standalone JSON)
    track_designer/main.py

LAYER 6 — Depends on Layers 0–4
    firmware/sensors/reflectance_array.py  (uses SensorHAL)
    firmware/wifi/web_server.py            (standalone; CircuitPython WiFi + HTTP)

LAYER 7 — Depends on Layer 6
    firmware/speed_sensor/speed_sensor.py  (uses SensorHAL interrupt GPIO)
    firmware/controllers/open_loop.py      (uses reflectance_array + speed_sensor HAL)
    firmware/controllers/pid.py            (uses reflectance_array)

LAYER 8 — Depends on Layer 7
    simulator/metrics.py                   (uses physics.py; no new firmware dep)
    firmware/controllers/kalman.py         (wraps pid.py)

LAYER 9 — Depends on Layer 8
    firmware/controllers/q_learning.py    (uses SensorHAL, MotorHAL; training in simulator)
```

**Rule**: A module may import only from layers below it. Any circular dependency is a design
error — fix it before continuing.

---------------

## 5. Phase 1 — Foundation {#s-p1}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 1 |
| **Weeks** | 1–4 |
| **Design Sessions covered** | Pre-DS (setup); DS2 (Chassis Assembly); DS3 (Hardware Integration) |
| **Git tag on completion** | `phase1-foundation-complete` |

**Goal**: All hardware on order; monorepo skeleton in place; HAL ABCs written; IR sensor reads
a line on the physical Pico W via the REPL.

**Pre-conditions**: None — this is the first phase.

### Week 1

* [x] Place all hardware orders from the BOM (verify against `specification.md` Section 3).
* [x] Confirm Motor Driver Board schematic downloaded — resolve [Q-001][q-001].
* [x] Create `lfr_course/` monorepo with full directory skeleton (see [Section 3.4][s-env]).
* [x] Create virtualenv; install `pygame`, `pytest`, `pytest-cov`, `reportlab`.
* [x] Verify `pytest` collects zero tests (no failures) on the empty skeleton.
* [x] Initial `git commit`; push to remote.

### Week 2

* [x] Write `firmware/hal/base.py` — `SensorHAL`, `MotorHAL`, `ControllerBase` ABCs
    (exact interface: see `specification.md` Section 5).
* [x] Write `firmware/hal/pico_hal.py` — GPIO-backed implementations.
    > **Blocker**: Motor Driver Board pin assignments must be confirmed from schematic
    > before this file can be completed. See [Q-001][q-001].
* [x] Write `firmware/hal/sim_hal.py` — stub only (returns zeros/False); will be completed
    in Phase 2 once `simulator/physics.py` exists.
* [x] Unit test `base.py`: verify all three ABCs raise `TypeError` when instantiated directly.

### Week 3

* [x] Write `firmware/config.py` with all default parameters from `specification.md` Section 5.
* [x] Write `firmware/main.py` skeleton: imports HAL + config; `while True` loop stub.
* [x] Write `firmware/sensors/ir_sensor.py` — `read_ir_pair()` using `SensorHAL`.
* [x] Write `tests/unit/test_ir_sensor.py` — all four IR input combinations → correct output.
* [ ] Flash CircuitPython 9.x onto the instructor Pico W; verify REPL over USB.

### Week 4

* [ ] Assemble instructor's Emo Chassis (DS2 milestone).
* [ ] Add all DS3 hardware to instructor chassis (motor driver board, breadboard,
    battery holder, buck converter, IR pair).
* [ ] Measure battery rail voltage; verify 5V at buck converter output.
* [ ] Run `ir_sensor.py` logic manually in REPL — confirm sensor reads line vs. white.
* [ ] Complete DS2 + DS3 hardware readiness checklists (see `specification.md` Section 8).
* [ ] `git tag phase1-foundation-complete`

**Phase 1 Milestone**: Instructor Pico W boots CircuitPython; IR sensor reports correct
binary readings over the REPL on a test line.

---------------

## 6. Phase 2 — Bang-Bang LFR + Simulator v1 {#s-p2}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 2 |
| **Weeks** | 5–8 |
| **Design Sessions covered** | DS4 (Simple LFR) |
| **Git tag on completion** | `phase2-bangbang-sim-complete` |

**Goal**: Bang-bang controller running on physical robot; simulator renders track + robot in 2D;
`test_bang_bang_oval` simulation test passing.

**Pre-conditions**: Phase 1 complete; `hal/base.py` + `hal/pico_hal.py` done; `ir_sensor.py` tested.

### Week 5

* [ ] Write `firmware/controllers/bang_bang.py` — implements `ControllerBase`; uses
    `SensorHAL.read_ir_pair()`. Logic: see `specification.md` Section 5.
* [ ] Write `tests/unit/test_bang_bang.py` — all 4 IR input combos → correct `(left, right)`
    motor output tuple.
* [ ] Write `simulator/physics.py` — differential drive kinematics (Euler integration).
    Parameters: `MAX_SPEED_M_S`, `WHEEL_BASE`, `WHEEL_RADIUS`; see spec Section 6.
* [ ] Write `simulator/track.py` — loads `track.json`; validates schema; raises `ValueError`
    on invalid input.
* [ ] Write `tests/unit/test_track.py` — valid JSON → Track object; missing fields → `ValueError`.

### Week 6

* [ ] Complete `firmware/hal/sim_hal.py` — `SensorHAL` and `MotorHAL` implementations that
    delegate to `simulator/physics.py` state. This is the critical bridge module.
* [ ] Write `simulator/sensor_sim.py` — samples the off-screen pygame Surface at sensor
    positions; IR pair mode (2 sample points); Gaussian noise configurable via σ parameter.
* [ ] Manually test `sim_hal.py` + `sensor_sim.py` together: instantiate robot at known
    position on a test track; verify sensor readings match expected values.

### Week 7

* [ ] Write `simulator/visualization.py` — pygame 2D top-down rendering:
  * Track viewport (full track visible in window)
  * Robot footprint at current pose
  * Sensor overlay (toggle with `S` key)
  * Trail overlay (fading path history; toggle with `T` key)
  * Target: 30 fps; use `pygame.time.Clock.tick(30)`
* [ ] Write `simulator/ui.py` — pure pygame sidebar panel (right side of window):
  * Controller selector (text list; arrow keys or click to select)
  * Parameter sliders for `BASE_SPEED` (Phase 2 only — others added later)
  * Buttons: Start, Stop, Reset, Load Track
  * Slider widget: draw filled rect for track, draggable thumb; display numeric value
  * **No external UI library** — all widgets are plain pygame drawing calls ([D-005][d-005])
* [ ] Write `simulator/plugin.py` — `load_controller(name, hal)` via `importlib`.
    Add `firmware/` to `sys.path` before importing (set `PYTHONPATH` in `simulator/main.py`).

### Week 8

* [ ] Write `simulator/main.py` — wires all simulator modules; main pygame event loop.
* [ ] Write `tests/sim/test_bang_bang_oval.py` — headless simulation (no display):
    load the simple oval `track.json`; run bang-bang controller; assert 3 laps complete;
    RMS path error < 0.05 m. Use `pygame.display.set_mode` with `flags=pygame.NOFRAME`
    or `os.environ['SDL_VIDEODRIVER'] = 'dummy'` for headless mode.
* [ ] Run the instructor robot on a printed oval track; verify it completes 3+ laps.
* [ ] Complete DS4 hardware readiness checklist.
* [ ] `git tag phase2-bangbang-sim-complete`

**Phase 2 Milestone**: `test_bang_bang_oval` passes; instructor robot completes 3 laps on
floor track; simulator visually matches robot behavior.

---------------

## 7. Phase 3 — Track Designer + Sensor Upgrade {#s-p3}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 3 |
| **Weeks** | 9–12 |
| **Design Sessions covered** | DS5 (Sensor Upgrade); Track Designer (cross-phase tool) |
| **Git tag on completion** | `phase3-designer-reflectance-complete` |

**Goal**: Line Track Designer functional and producing printable PDFs + valid `track.json`;
QTRX-MD-08RC reflectance array wired, calibrated, and tested on hardware; simulator updated
to 8-element sensor model.

**Pre-conditions**: Phase 2 complete; simulator renders a track; CircuitPython library for
QTRX sensor validated (see [Q-003][q-003]).

### Week 9

* [ ] Write `track_designer/tile_library.py` — tile type definitions; each tile stores:
  * Entry/exit edge pair(s)
  * Line path as a parametric curve (for rendering and `track.json` export)
  * SVG-compatible path data (for potential future SVG export)
  * Tile types must exactly match `specification.md` Section 6 Tile Types table.
* [ ] Verify tile adjacency: for every edge-pair combination, a connecting tile must exist
    in the library (no dead ends unless using `blank`).
* [ ] Write `track_designer/canvas.py` — pygame drag-and-drop grid editor:
  * Grid: up to 8 cols × 6 rows; default 4×3
  * Left-click empty cell → tile picker popup
  * Left-click placed tile → rotate 90° CW
  * Right-click placed tile → remove (set to blank)
  * Keys: `R` rotate, `Del` remove, `Ctrl+Z` undo, `Ctrl+S` save

### Week 10

* [ ] Write `track_designer/export.py` — two export functions:
  * `export_pdf(layout, path)` — one page per tile; 8.5″×11″; registration marks at
        corners; tile coords printed; uses `reportlab`
  * `export_json(layout, path)` — writes `track.json` per schema; validates before writing
* [ ] Write `track_designer/save_load.py` — `.layout` JSON persistence; separate from
    `track.json`
* [ ] Write `track_designer/main.py` — wires canvas + export + save/load; pygame event loop
* [ ] Write `tests/unit/test_export.py` — known layout → `export_json` → valid schema;
    invalid layout → `ValueError`

### Week 11

* [ ] **Do a test print run**: design the simple 4×3 oval in the designer; export PDF;
    print all 12 tiles; assemble on floor. Check:
  * Lines connect at tile edges (no gaps or misalignments)
  * Registration marks align across adjacent tiles
  * Line width is visible from robot sensor height
  * Fix any export geometry errors before proceeding.
* [ ] **Validate QTRX-MD-08RC CircuitPython library** — resolve [Q-003][q-003]:
  * Check Pololu or Adafruit for a CircuitPython QTRX driver
  * If no library exists: test raw GPIO bit-bang calibration in CircuitPython REPL
  * Document the chosen approach in the Decision Log before writing firmware
* [ ] Write `firmware/sensors/reflectance_array.py` — `read_reflectance_array()` returning
    8 normalised floats; startup calibration (white → 0.0, black → 1.0); weighted centroid
    position estimate ∈ [−3.5, +3.5]
* [ ] Write `tests/unit/test_reflectance_array.py` — centroid for known 8-element arrays;
    calibration logic; edge cases (all white, all black, single element high)

### Week 12

* [ ] Wire QTRX-MD-08RC to instructor's robot on GP12–GP19; run calibration in REPL;
    verify 8 individual sensor readings change correctly over black line and white surface.
* [ ] Update `simulator/sensor_sim.py` — add 8-element mode (8 evenly-spaced sample points
    across sensor width; same Gaussian noise model as IR pair mode).
* [ ] Update `simulator/ui.py` — add sensor mode selector (ir_pair / reflectance_array).
* [ ] Run `test_pid_oval` (Phase 4 deliverable, but reflectance mode can be tested headlessly
    now as a pre-validation — use stub PID if needed).
* [ ] Complete DS5 hardware readiness checklist.
* [ ] `git tag phase3-designer-reflectance-complete`

**Phase 3 Milestone**: Printed oval track on floor; instructor robot navigates with reflectance
array; Track Designer produces correct PDFs; `test_export.py` and `test_reflectance_array.py`
pass.

---------------

## 8. Phase 4 — WiFi UI + Open-Loop + PID {#s-p4}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 4 |
| **Weeks** | 13–16 |
| **Design Sessions covered** | DS6 (WiFi Interface); DS7 (Open-Loop Speed Control); DS8 (PID Controller) |
| **Git tag on completion** | `phase4-wifi-openloop-pid-complete` |

**Goal**: WiFi UI serving speed controls; wheel speed sensors counting pulses; open-loop and
PID controllers validated in simulator and on hardware.

**Pre-conditions**: Phase 3 complete; reflectance array working; Track Designer producing
correct `track.json`.

### Week 13

* [ ] Write `firmware/wifi/web_server.py` — Pico W in AP mode; HTTP server on port 80;
    serves single-page HTML5 UI; accepts `POST /config` with JSON body; updates `config.py`
    at runtime. DS6 UI: base speed slider only.
* [ ] Test WiFi AP at home (or equivalent): connect phone/laptop; verify slider changes
    `BASE_SPEED` and robot adjusts speed in real time.
* [ ] Pre-test at Makersmiths (interference check) — see [Risk R-006][r-006].
* [ ] Complete DS6 hardware readiness checklist.

### Week 14

* [ ] Wire 2× Speed Sensor Modules to instructor robot (GP20 = left, GP21 = right).
* [ ] Write `firmware/speed_sensor/speed_sensor.py` — interrupt-driven pulse counting;
    RPM conversion from pulse count + time delta; `read_wheel_speeds()` → `(left_rpm, right_rpm)`.
* [ ] Write `tests/unit/test_speed_sensor.py` — synthetic pulse sequences → correct RPM;
    zero-pulse edge case.
* [ ] Write `firmware/controllers/open_loop.py` — proportional speed correction per wheel;
    error = target_speed − measured_speed; no integral/derivative term.
* [ ] Write `tests/unit/test_open_loop.py` — speed error → correct correction output;
    gain boundary conditions.

### Week 15

* [ ] Verify speed sensor pulse counting on hardware (manual wheel spin test in REPL).
* [ ] Complete DS7 hardware readiness checklist.
* [ ] Write `firmware/controllers/pid.py` — line position error from reflectance array
    centroid; PID differential on left/right speeds; integral clamp; all gains tunable
    via `configure()`. See `specification.md` Section 5 for full algorithm.
* [ ] Write `tests/unit/test_pid.py` — step input → correct P/I/D contributions;
    integral clamp test; `configure()` updates gains correctly.
* [ ] Update `firmware/wifi/web_server.py` DS8 additions: Kp/Ki/Kd sliders;
    reset integrators button.

### Week 16

* [ ] Write `simulator/metrics.py` — records RMS path error, lap time, oscillation count,
    off-track events, max speed; logs to CSV; exposes live values to `ui.py`.
* [ ] Write `tests/sim/test_pid_oval.py` — simple oval; PID controller; 5 laps;
    RMS error < 0.02 m; oscillations < 10/lap.
* [ ] Write `tests/sim/test_pid_complex.py` — 4×3 track with curves; PID; 2 laps;
    zero off-track events.
* [ ] Update `simulator/ui.py` — add Kp/Ki/Kd sliders; metrics panel (live CSV values
    displayed in sidebar).
* [ ] Run both sim tests passing.
* [ ] Tune PID on instructor hardware; verify stable for 2+ laps; gains adjustable via WiFi UI.
* [ ] Complete DS8 hardware readiness checklist.
* [ ] `git tag phase4-wifi-openloop-pid-complete`

**Phase 4 Milestone**: `test_pid_oval` and `test_pid_complex` passing; PID robot stable on
hardware with gains tunable via WiFi UI in real time.

---------------

## 9. Phase 5 — Kalman Filter + Q-Learning {#s-p5}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 5 |
| **Weeks** | 17–20 |
| **Design Sessions covered** | DS9 (Kalman Filter); DS10 (Advanced Control Theory); DS11 (Q-Learning Controller) |
| **Git tag on completion** | `phase5-kalman-qlearn-complete` |

**Goal**: Kalman filter demonstrably reduces noise on hardware; Q-Learning Q-table trains and
converges in simulator; Q-table deployed to Pico W (time permitting — see [MVP Cut][s-mvp]).

**Pre-conditions**: Phase 4 complete; PID controller validated; `metrics.py` working.

### Week 17

* [ ] Write `firmware/controllers/kalman.py` — 1D Kalman filter wrapping `pid.py`; filters
    line position signal before PID input; Q and R tunable. See spec Section 5 for equations.
* [ ] Write `tests/unit/test_kalman.py` — noisy synthetic signal → Kalman output closer
    to true signal than raw input; Q/R parameter effects verified.
* [ ] Write `tests/sim/test_kalman_noise.py` — oval track at σ=0.3 noise; Kalman controller;
    assert RMS error < RMS error of pure PID at same noise level.
* [ ] Run all three tests passing.

### Week 18

* [ ] Deploy Kalman firmware to instructor robot; compare oscillation count vs. PID-only
    (both measured via `metrics.py` CSV export and simulator).
* [ ] Update `firmware/wifi/web_server.py` DS9 additions: Kalman Q, R sliders.
* [ ] Update `simulator/ui.py` — add Kalman Q, R sliders.
* [ ] Prepare side-by-side Kalman vs. no-Kalman simulator demo for class.
* [ ] Complete DS9 hardware readiness checklist.
* [ ] Finalize Q-Learning state/action space (confirm N=7 states, 5 actions from spec are
    sufficient for the oval track — test by estimating coverage). Document any changes
    in Decision Log.

### Week 19

* [ ] Write `firmware/controllers/q_learning.py` — training mode:
  * ε-greedy exploration
  * Q-table update rule (see spec Section 5)
  * Reward function: +1 on line, −10 off track, +0.5 speed bonus when centred
  * Serialize trained Q-table to `q_table.json`
* [ ] Write `tests/sim/test_qlearning_train.py` — training run on oval; assert Q-table
    converges in < 500 episodes (average reward plateaus).
* [ ] Write training visualisation in simulator: show episode count, cumulative reward,
    Q-table heatmap (sidebar); used as DS10 class demo.
* [ ] Run training test; if Q-table fails to converge see [Risk R-005][r-005].

### Week 20

* [ ] Write `tests/unit/test_q_learning.py` — inference mode (ε=0): load a known
    Q-table; verify greedy action selection; verify `configure()` and `reset()`.
* [ ] Write `tests/sim/test_qlearning_trained.py` — load pre-trained `q_table.json`;
    oval track; 3 laps complete without off-track events.
* [ ] **If time permits** (not MVP cut): deploy `q_table.json` to all 6 Pico Ws;
    complete DS11 hardware readiness checklist.
* [ ] **If time is tight** (MVP cut active): teach DS11 concept via simulator only;
    document deferral in Decision Log with reason.
* [ ] `git tag phase5-kalman-qlearn-complete`

**Phase 5 Milestone**: `test_kalman_noise`, `test_qlearning_train`, and `test_qlearning_trained`
passing; Kalman demonstrably better than PID on hardware; Q-table trained and converged.

---------------

## 10. Phase 6 — Integration & Dress Rehearsal {#s-p6}

| | |
|:--|:--|
| **Status** | Not started |
| **Month** | 6 |
| **Weeks** | 21–24 |
| **Design Sessions covered** | All DS — full integration and readiness |
| **Git tag on completion** | `phase6-course-ready` |

**Goal**: All 6 robots built and individually validated; full test suite green; instructor
has dry-run all 11 Design Sessions; course documents finalized.

**Pre-conditions**: Phases 1–5 complete; all hardware received.

### Week 21

* [ ] Build all 5 student robots (chassis → DS3 hardware integration → CircuitPython flash).
* [ ] Run per-robot hardware validation: battery voltage, REPL boot, IR sensor, WiFi AP
    (each robot must show its unique SSID LFR-1 through LFR-5; instructor is LFR-6).
* [ ] Verify all 6 QTRX arrays calibrate correctly.
* [ ] Verify all 12 speed sensor modules count pulses correctly.

### Week 22

* [ ] Run full Tier 1 test suite (`pytest tests/unit/`) — all tests pass, zero failures.
* [ ] Run full Tier 2 test suite (`pytest tests/sim/`) — all sim tests pass.
* [ ] WiFi multi-robot test: all 6 APs active simultaneously at Makersmiths;
    verify no SSID collision; verify each robot's UI is independently reachable.
* [ ] Fix any failures before proceeding.

### Week 23

* [ ] Instructor dry-run of all 11 Design Sessions (abbreviated, ~30 min each):
  * DS1: MiOYOOW demo; track ready
  * DS2–DS3: assembly guide walkthrough
  * DS4–DS5: bang-bang and reflectance array on floor track
  * DS6: WiFi UI demo
  * DS7–DS8: speed sensors + PID tuning demo
  * DS9: Kalman vs PID side-by-side
  * DS10: control theory overview + Q-Learning simulator demo
  * DS11: Q-Learning controller (hardware or simulator per MVP cut decision)
* [ ] Finalize all course documents: syllabus, all 11 lesson plans, BOM.
* [ ] Verify all documents are consistent (names, part numbers, DS structure).

### Week 24 (Buffer)

* [ ] Resolve any issues from dry-run.
* [ ] All robots cleaned, labeled, and individually packed.
* [ ] Course evaluation form prepared.
* [ ] Go/no-go checklist reviewed and signed off.
* [ ] `git tag phase6-course-ready`

**Phase 6 Milestone**: Pre-course dress rehearsal complete; all 6 robots functional; full
test suite green; all course documents finalized.

---------------

## 11. MVP Cut — If Timeline Slips {#s-mvp}

> **Decision [D-007][d-007]**: If Phase 5 runs over, Q-Learning hardware deployment is
> the first cut. See [Appendix A][appendix-a] for rationale.

### Trigger: When to activate the MVP cut

Activate if, at the end of Week 18 (start of Phase 5, Week 3), either:

* `test_qlearning_train` is not passing, **or**
* The Q-table is not converging within 500 episodes.

### What the MVP cut looks like

| Component | Full scope | MVP cut |
|:----------|:-----------|:--------|
| DS11 Q-Learning | Q-table trained + deployed to all 6 Pico Ws | Q-table trained in simulator; demo shown in class; Pico W deployment deferred |
| DS11 class content | Students run Q-Learning on their physical robots | Instructor demos simulator training; students observe and discuss |
| `tests/sim/test_qlearning_trained` | Required | Required (simulator only) |
| `tests/unit/test_q_learning` | Required | Required |
| DS11 hardware checklist | Full | Skipped |

### If the cut cascades further

If both Kalman (DS9) and Q-Learning (DS11) are at risk, protect DS9 — it has higher
teaching value for the class arc (students need to see a concrete improvement from PID).
Kalman stays; Q-Learning taught as concept only.

### Post-course backlog

Items deferred by the MVP cut are tracked here (not deleted):

* [ ] Deploy `q_table.json` to all 6 Pico Ws
* [ ] Full DS11 hardware readiness checklist
* [ ] Optional: Pure Pursuit or Fuzzy Logic controller (mentioned in `input/my-vision.md`)

---------------

## 12. Risk Register {#s-risks}

Updated continuously. Add new risks at the bottom with a new R-ID.

| ID | Risk | Likelihood | Impact | Status | Mitigation / Outcome |
|:---|:-----|:----------:|:------:|:-------|:---------------------|
| R-001 | Hardware shipping delays | M | H | Active | Order all components Week 1; buy spares for Pico W and QTRX |
| R-002 | Motor Driver Board pinout undocumented | L | H | Resolved 2026-02-26 — GP8/GP9 confirmed; pico_hal.py unblocked | Download schematic Month 1 before writing `pico_hal.py` |
| R-003 | CircuitPython library unavailable for QTRX-MD-08RC | L | H | Active — validate Week 11 ([Q-003][q-003]) | Pre-validate Month 3 Week 11; fallback: raw GPIO bit-bang |
| R-004 | Simulator physics diverges from hardware | M | M | Active | Tune physics model against hardware measurements in Phase 2 |
| R-005 | Q-Learning Q-table fails to converge | M | H | Active | Simplify state space; reward shaping; hard episode limit 500; activate MVP cut if needed |
| R-006 | WiFi interference / SSID collision at Makersmiths | M | M | Active | Pre-test at facility Week 13; assign fixed unique SSIDs; test all 6 APs simultaneously Week 22 |
| R-007 | Q-table inference too slow on Pico W | L | H | Active | Profile Week 20; if slow, quantize Q-table to int8 |
| R-008 | Track printing misalignment | L | M | Active | Test print run Week 11; registration marks in Designer export |
| R-009 | Student skill level lower than expected | H | M | Active | Pair younger students with adults; step-by-step print-out per DS |
| R-010 | 2-hour class too short for DS content | M | M | Active | Each DS documented with a "minimum viable" subset that splits across classes |
| R-011 | `reportlab` PDF rendering quality insufficient | L | L | Active | Evaluate Week 10; fallback: `matplotlib` PDF backend or SVG-to-print |
| R-012 | pygame 2.6.x incompatible with Ubuntu 24.04 Noble | L | L | Active | Verify `pip install pygame` on Noble before Week 5; pin version in requirements |

---------------

## 13. Open Questions Log {#s-questions}

Add new questions at the bottom. Mark resolved questions `[x]`.

| ID | Question | Phase needed by | Status |
|:---|:---------|:----------------|:-------|
| Q-001 | What are the exact GPIO pin assignments used by the Robotics Motor Driver Board? (Required before `pico_hal.py` can be completed.) | Phase 1, Week 2 | [x] Resolved 2026-02-26 — Raspberry Pi Pico W GP8/Pin11 and GP9/PIN12 are consume by the board, no others |
| Q-002 | Does CircuitPython 9.x support `from __future__ import annotations`? If not, how should type hints be handled in firmware modules that are also imported by the Python 3.12 simulator? | Phase 1, Week 2 | [x] Resolved 2026-02-26 — Use string literals for forward references |
| Q-003 | Is there a CircuitPython library for the QTRX-MD-08RC? If not, what is the fallback GPIO bit-bang protocol? | Phase 3, Week 11 | Open |
| Q-004 | Should the Track Designer's tile picker UI be a modal overlay (popup on tile click) or a persistent palette panel? The spec does not specify layout. | Phase 3, Week 9 | Open |

### How to close a question

When resolved: change `Open` → `[x] Resolved YYYY-MM-DD — <one-line answer>`, then add a
Decision Log entry if the answer drove an architectural choice.

---------------

## 14. Changelog {#s-changelog}

Newest entries at top. Add an entry whenever this document changes significantly.

| Date | Change |
|:-----|:-------|
| 2026-02-28 | Marked all Week 1 and Week 2 tasks [x]; updated last milestone |
| 2026-02-26 | Document created; all Q&A decisions incorporated; Phases 1–6 drafted |

---------------

## Appendix A — Development Dialogue {#appendix-a}

This appendix preserves the original prompt that initiated this development plan
and the full Q&A session that resolved the key planning decisions.

### A.1 — Original Prompt (verbatim)

> Read @input/my-vision.md and @specification.md and create a development plan, to be called
> "development-plan.md", describing how & when thing are to be created / build.
> The development plan must reflecting the incrementally build approach outline in the Line
> Following Robot (LFR) course.
>
> Make sure to cover the all major software components and their build order,
> key technical decisions to resolve upfront (e.g., which Python GUI library for the simulator),
> a rough phasing that mirrors your courses Design Sessions,
> and any external dependencies or risks (like CircuitPython library availability for the QTRX sensor).
>
> Produce the plan as a living document it can update as the project evolves,
> not just a one-time artifact.
> I want it to serves as an ongoing reference rather than going stale after the first few sessions.
> Given the scope of this project — firmware, a simulator, a track designer, and incremental
> design sessions — I want plan to save significant back-and-forth with Claude Code over the
> course of development.
>
> Within the development plan document you create (to be called "development-plan.md"), include
> this prompt, all question you ask me, along with my responses. Place this in an appendix and
> reference it at the beginning of the development plan and anywhere else in the text when its
> a useful reference.
>
> Think Hard about what must be done to create a robust plan.
> Use the AskUserQuestions tool for all things that require further clarification.

### A.2 — Q&A: Python & Ubuntu Version

**Question**: What Python version and Ubuntu version are you targeting for the desktop tools
(simulator + track designer)?

* Option A: Python 3.11 / Ubuntu 22.04 LTS (Jammy)
* Option B: **Python 3.12 / Ubuntu 24.04 LTS (Noble)**
* Option C: Whatever is already on my machine — I'll check

**Answer**: **Python 3.12 / Ubuntu 24.04 LTS (Noble)**

**Decision recorded**: [D-004][d-004] — Python 3.12 / Ubuntu 24.04 LTS for all desktop
tools. Affects: `pygame` version pin, `pytest` version, `reportlab` compatibility.

### A.3 — Q&A: Simulator UI Approach

**Question**: The spec says the simulator has a parameter control panel with sliders,
dropdowns, and buttons. How should that panel be built?

* Option A: **Pure pygame (custom widgets)** — fewest dependencies; full layout control
* Option B: pygame-gui (pygame + pygame_gui library) — pre-built themed widgets; one extra dep
* Option C: Hybrid: pygame track + tkinter sidebar — two event loops

**Answer**: **Pure pygame (custom widgets)**

**Decision recorded**: [D-005][d-005] — All simulator UI widgets (sliders, dropdowns,
buttons) are custom pygame drawing calls. No additional UI library. Affects: `simulator/ui.py`
implementation and the absence of `pygame-gui` from the dependency list.

### A.4 — Q&A: Git Workflow

**Question**: How do you want to track development progress in git across the ~11 Design Sessions?

* Option A: **Tags on main** (e.g., `ds4-complete`, `ds5-complete`)
* Option B: Feature branches per DS, merged to main when DS is ready
* Option C: GitHub milestones + issues only — no branch strategy

**Answer**: **Tags on main**

**Decision recorded**: [D-006][d-006] — Single `main` branch; git tags mark each phase
milestone. Tags follow the pattern `phase{N}-{name}-complete`. Affects: workflow guidance
throughout this document.

### A.5 — Q&A: MVP Cut

**Question**: If the 6-month timeline gets tight, which component is lowest priority and
could be deferred to after the first course run?

* Option A: **Q-Learning controller (DS11) — teach concept, skip hardware deployment**
* Option B: Kalman filter (DS9) — teach concept only
* Option C: WiFi web UI (DS6) — use `config.py` edits instead
* Option D: Nothing — I want all DS delivered on hardware

**Answer**: **Q-Learning controller (DS11) — teach concept, skip deployment**

**Decision recorded**: [D-007][d-007] — If Phase 5 runs over, the Q-Learning hardware
deployment (deploying `q_table.json` to Pico Ws) is the first deliverable cut. The simulator
training and class demonstration are preserved. Full scope remains the goal; this is the
fallback only. See [MVP Cut][s-mvp] section for trigger criteria.

---------------

[spec]: specification.md
[appendix-a]: #appendix-a
[s-status]: #s-status
[s-decisions]: #s-decisions
[s-env]: #s-env
[s-buildorder]: #s-buildorder
[s-p1]: #s-p1
[s-p2]: #s-p2
[s-p3]: #s-p3
[s-p4]: #s-p4
[s-p5]: #s-p5
[s-p6]: #s-p6
[s-mvp]: #s-mvp
[s-risks]: #s-risks
[s-questions]: #s-questions
[s-changelog]: #s-changelog

[d-004]: #s-decisions
[d-005]: #s-decisions
[d-006]: #s-decisions
[d-007]: #s-decisions

[r-005]: #s-risks
[r-006]: #s-risks

[q-001]: #s-questions
[q-002]: #s-questions
[q-003]: #s-questions
