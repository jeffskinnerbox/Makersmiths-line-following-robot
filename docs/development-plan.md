# LFR Course — Development Plan

* **Organization:** [Makersmiths][L01] — a community [makerspace][L02] in Leesburg, Virginia
* **Course:** Evolving Design of a Line Following Robot
* **Course Start Date:** June 15, 2026
* **Development Window:** March 16 – June 14, 2026 (13 weeks)
* **Author:** Course instructor (volunteer)
* **Purpose:** Sequences all pre-course software development (LFR firmware, Line Track Designer, LFR Simulator) into milestones and phases with test-gates, maps each milestone to a class day, and serves as a living document updated throughout development
* **Reference:** See [Appendix A](#appendix-a-development-plan-prompt--qa) for the original prompt and all instructor Q&A that shaped this document

## Related Documents

| Document | File | Relationship |
|:---------|:-----|:-------------|
| Course Syllabus | `docs/lfr-syllabus.md` | Defines learning objectives, class schedule, and course structure |
| Lesson Plan | `docs/lfr-lesson-plan.md` | Detailed per-class teaching guide |
| System Specification | `docs/lfr-specification.md` | Defines module interfaces, test criteria, and hardware configurations |
| Bill of Materials | `input/my-bom.md` | Single source of truth for costs, quantities, and sourcing |
| Instructor Vision | `input/my-vision.md` | Original course vision and Design Session sequence |

> **How to use this document:** This is a living document. The [Status Tracker](#6-status-tracker) section is updated as phases and milestones are completed. Each milestone maps to a class day — when a milestone passes all its test-gates, all software for that class day is ready.
> The plan references test-gate definitions in the spec (§7.5) rather than duplicating them.

---

## Table of Contents

* [1. Executive Summary](#1-executive-summary)
* [2. Key Technical Decisions](#2-key-technical-decisions)
* [3. Development Timeline Overview](#3-development-timeline-overview)
* [4. Milestone & Phase Details](#4-milestone--phase-details)
  * [Milestone 0: Project Bootstrap](#milestone-0-project-bootstrap)
  * [Milestone 1: Line Track Designer](#milestone-1-line-track-designer)
  * [Milestone 2: Firmware Foundation — DS3–DS5](#milestone-2-firmware-foundation--ds3ds5)
  * [Milestone 3: Firmware Sensor Array — DS6–DS7](#milestone-3-firmware-sensor-array--ds6ds7)
  * [Milestone 4: Firmware WiFi + Browser UI — DS8](#milestone-4-firmware-wifi--browser-ui--ds8)
  * [Milestone 5: Firmware Speed Sensors — DS9](#milestone-5-firmware-speed-sensors--ds9)
  * [Milestone 6: Firmware PID — DS10](#milestone-6-firmware-pid--ds10)
  * [Milestone 7: LFR Simulator](#milestone-7-lfr-simulator)
  * [Milestone 8: Firmware Kalman — DS11 (Stretch)](#milestone-8-firmware-kalman--ds11-stretch)
  * [Milestone 9: Firmware Q-Learning — DS12 (Stretch)](#milestone-9-firmware-q-learning--ds12-stretch)
  * [Milestone 10: Final Prep & Course Readiness](#milestone-10-final-prep--course-readiness)
* [5. Risk Register](#5-risk-register)
* [6. Status Tracker](#6-status-tracker)
* [7. Dependency Graph](#7-dependency-graph)
* [Appendix A: Development Plan Prompt & Q&A](#appendix-a-development-plan-prompt--qa)

---

## 1. Executive Summary

### What Gets Built

Three software systems must be developed and tested before the course begins on June 15, 2026:

| System | Language | Purpose | Milestones |
|:-------|:---------|:--------|:-----------|
| **LFR Firmware** | CircuitPython 10.1.4 | Robot control software — modular, evolves across Design Sessions | M0, M2–M6, M8–M9 |
| **Line Track Designer** | Python 3 (CLI) | Generates printable PDF tile sheets for floor test tracks | M1 |
| **LFR Simulator** | Python 3 + Pygame | 2D visual simulation for instructor demos and parameter tuning | M7 |

### Timeline at a Glance

```text
Week  Dates            Milestones                                  Class Ready
────  ───────────────  ──────────────────────────────────────────  ───────────
 1    Mar 16–22        M0 Bootstrap ■■ + M1 Track Designer start
 2    Mar 23–29        M1 Track Designer ■■■■■                     Class 3
 3    Mar 30–Apr 5     M2 Firmware DS3–DS5 start ■■
 4    Apr 6–12         M2 Firmware DS3–DS5 ■■■■■ (QTRX arrives)   Classes 1–3
 5    Apr 13–19        M3 Firmware DS6–DS7 ■■■ + M7 Sim start
 6    Apr 20–26        M3 Firmware DS6–DS7 ■■■■■                   Classes 4–5
 7    Apr 27–May 3     M4 WiFi+UI DS8 ■■■■■                       Class 6
 8    May 4–10         M5 Speed Sensors DS9 ■■■■■                  Class 7
 9    May 11–17        M6 PID DS10 ■■■■■                           Class 8
10    May 18–24        M7 Simulator ■■■■■ + M8 Kalman start
11    May 25–31        M8 Kalman DS11 ■■■■■                        Class 9*
12    Jun 1–7          M9 Q-Learning DS12 ■■■■■                    Class 10*
13    Jun 8–14         M10 Final Prep ■■■■■                        All classes
```

*Classes 9–10 are stretch classes.

### Critical Path

```text
M0 → M1 → M2 → M3 (blocked by QTRX arrival) → M4 → M5 → M6 → M10
                                                                 ↑
M7 (Simulator, parallel) ───────────────────────────────────────┘
```

The Line Track Designer (M1) must be ready first — Class 3 needs printed test tracks. Firmware milestones (M2–M6) are sequential because each Design Session builds on the previous. The simulator (M7) runs in parallel and is off the critical path. Milestones 8–9 (Kalman, Q-Learning) are stretch goals.

---

## 2. Key Technical Decisions

These decisions are resolved upfront (drawn from spec §9 and planning Q&A). They prevent mid-development reversals.

| # | Decision | Resolution | Rationale |
|:--|:---------|:-----------|:----------|
| 1 | **CircuitPython version** | 10.1.4 | Latest stable with confirmed Pico W support (released 2026-03-09). See spec §3.11. |
| 2 | **Simulator GUI library** | Pygame | Best fit for 2D real-time simulation with animation, sliders, and keyboard control. See spec [Appendix A, Q2]. |
| 3 | **Track Designer output** | PDF via reportlab | Multi-page PDF, one tile per page, print directly. See spec [Appendix A, Q3]. |
| 4 | **Track Designer interface** | JSON config + CLI | No GUI needed; JSON track definitions, CLI for generate/validate. See spec [Appendix A, Q6]. |
| 5 | **Firmware modularity** | Plugin modules + abstract base classes | Swap subsystems by changing `config.py`. See spec §3.1. |
| 6 | **WiFi + control loop coexistence** | Cooperative polling (single loop) | No threading/asyncio. Main loop calls `server.poll()` each iteration. See spec §3.8. |
| 7 | **Motor control** | Kitronik library via I2C/PCA9685 | Evaluate Kitronik official CircuitPython library; adapt if needed. See spec §3.6. |
| 8 | **Firmware testing** | Desktop pytest + on-hardware manual tests | Conditional imports so firmware modules run on desktop Python. See spec §7.1. |
| 9 | **Q-Learning: sim vs robot** | Independent implementations, no transfer | Simulator for demos, robot for class. Same algorithm, separate Q-tables. See spec [Appendix A, Q4]. |
| 10 | **Simulator physics** | Differential drive model | Two-wheel model with independent motor speeds. See spec [Appendix A, Q11]. |

---

## 3. Development Timeline Overview

### Week-by-Week Schedule

| Week | Dates | Primary Work | Parallel Work | Milestone Completed | Class Unlocked |
|:-----|:------|:-------------|:-------------|:-------------------|:---------------|
| 1 | Mar 16–22 | M0: Repo setup, dev environment, CircuitPython flash | M1: Track Designer start | M0 | — |
| 2 | Mar 23–29 | M1: Track Designer core + course tracks | — | M1 | Class 3 (tracks) |
| 3 | Mar 30–Apr 5 | M2: Firmware base classes, IR pair sensor, motor driver | — | — | — |
| 4 | Apr 6–12 | M2: Bang-bang controller, oval track test | — | M2 | Classes 1–3 |
| 5 | Apr 13–19 | M3: QTRX driver, calibration | M7: Simulator scaffold | — | — |
| 6 | Apr 20–26 | M3: Proportional controller, sensor array tests | M7: Physics engine | M3 | Classes 4–5 |
| 7 | Apr 27–May 3 | M4: WiFi AP, web server, browser UI | M7: Sensor sim + track loader | M4 | Class 6 |
| 8 | May 4–10 | M5: Speed sensor driver, closed-loop feedback | M7: Controller integration | M5 | Class 7 |
| 9 | May 11–17 | M6: PID controller, tuning via browser UI | M7: UI + sliders | M6 | Class 8 |
| 10 | May 18–24 | M7: Simulator polish, all controllers working | M8: Kalman filter start | M7 | — |
| 11 | May 25–31 | M8: Kalman+PID controller, filter toggle UI | — | M8 | Class 9* |
| 12 | Jun 1–7 | M9: Q-Learning controller, training mode, Q-table save | — | M9 | Class 10* |
| 13 | Jun 8–14 | M10: Final prep, all-unit flash, course material review | — | M10 | All classes |

*Stretch classes.

### Build Order Rationale

1. **Track Designer first (M1)** — Needed by Class 3 for the oval test track. No hardware dependency. Good warm-up project with bounded scope.
2. **Firmware foundation next (M2)** — Base classes establish the modular architecture that all subsequent firmware milestones build on. Hardware (except QTRX) is in hand.
3. **QTRX sensor array (M3) at Week 5** — QTRX driver code can be written and desktop-tested earlier, but hardware integration testing waits for delivery (~April 2–6).
4. **WiFi → Speed Sensors → PID (M4–M6)** — Sequential; each adds a layer of capability.
5. **Simulator in parallel (M7)** — Doesn't block firmware. Shares controller algorithm concepts. Starts after firmware controllers are understood from M2–M3.
6. **Kalman and Q-Learning last (M8–M9)** — Stretch goals for stretch classes. Can be cut without affecting the 8-class core course.

---

## 4. Milestone & Phase Details

Each milestone contains one or more phases. Each phase has a specific deliverable and references the appropriate test-gates from spec §7.5.

---

### Milestone 0: Project Bootstrap

**Week:** 1 (Mar 16–22)
**Purpose:** Development environment ready; one Pico W booting CircuitPython
**Class unlocked:** None (infrastructure only)

#### Phase 0.1: Repository & Tooling Setup

**Deliverables:**
* Git repository initialized with directory structure per spec §3.2
* Python virtual environment for desktop development (pytest, reportlab, pygame, numpy)
* `markdownlint-cli2` configured and working on docs
* CircuitPython 10.1.4 flashed on instructor Pico W (unit 01) — manual step, see [circuitpython.org/board/raspberry_pi_pico_w](https://circuitpython.org/board/raspberry_pi_pico_w/)
* Mu Editor installed and tested

**Test-gates:**
1. `pytest --version` runs successfully in the virtual environment
2. `markdownlint-cli2 docs/*.md` runs without errors
3. Flash CircuitPython 10.1.4 on instructor Pico W (manual): follow [circuitpython.org/board/raspberry_pi_pico_w](https://circuitpython.org/board/raspberry_pi_pico_w/) — hold BOOTSEL, drag-and-drop `.uf2` to RPI-RP2 drive, confirm CIRCUITPY drive mounts
4. Mu Editor opens and connects to the Pico W (REPL accessible)

#### Phase 0.2: Hardware Verification

**Deliverables:**
* `src/firmware/test_m02.py` — hardware verification script (copy to `CIRCUITPY/main.py` to run)
* CIRCUITPY drive confirmed writable
* Both motors confirmed spinning via `test_m02.py` output

**Test-gates:**
1. CircuitPython 10.1.4 boots on the Pico W (REPL accessible via Mu Editor)
2. `gc.mem_free()` reports at least 100 KB available — verified by `test_m02.py` Gate 1+2 output
3. Both wheels spin when `test_m02.py` runs — copy to `CIRCUITPY/main.py`, confirm "PASS" in serial console

**Setup for test-gate 3:**
* Pico W must be seated in the Kitronik Robotics Board
* 9V battery connected to the Kitronik board (motors won't spin without it)
* Copy `src/firmware/test_m02.py` to `CIRCUITPY/main.py`
* Open Mu Editor serial console and press reset — output appears on boot
* Re-run anytime from REPL: `test_motors()`

---

### Milestone 1: Line Track Designer

**Weeks:** 1–2 (Mar 16–29)
**Purpose:** Produce printable PDF test tracks for all course classes
**Class unlocked:** Class 3 (DS4–DS5 need the simple oval track)
**Spec reference:** §4 Line Track Designer Specification

#### Phase 1.1: Core Engine

**Deliverables:**
* Track JSON schema and validation (`jsonschema`)
* Tile type registry with drawing functions for all 11 tile types (spec §4.3)
* PDF generation engine using `reportlab` — one 8.5×11" landscape page per tile
* Registration marks and tile border rendering
* CLI: `generate`, `validate`, `tiles` commands (spec §4.5)

**Test-gates:**
1. `python track_designer.py tiles` lists all 11 tile types
2. `python track_designer.py validate tracks/simple_oval.json` passes without errors
3. `python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf` produces a valid PDF
4. Generated PDF has correct page count (one per non-blank tile)
5. pytest suite passes: JSON parsing, tile registry, grid boundary validation, PDF generation

#### Phase 1.2: Course Track Designs

**Deliverables:**
* All 6 course track JSON files created (spec §4.6):
  * `simple_oval.json` — Class 3 (DS4–DS5)
  * `oval_tight.json` — Class 4 (DS6)
  * `figure_eight.json` — Classes 5–6 (DS7–DS8)
  * `figure_eight_chicane.json` — Class 7 (DS9)
  * `complex_course.json` — Classes 8–9 (DS10–DS11)
  * `competition_course.json` — Class 10 (DS12–DS13)
* PDFs generated for all tracks
* Preview mode working (`--preview` flag)

**Test-gates:**
1. All 6 track JSON files pass validation
2. All 6 PDFs generate without errors
3. Preview page renders all tiles in a single overview for each track
4. Manual verification: print `simple_oval.pdf`, measure line width with ruler (should be 19 mm ± 1 mm)
5. Manual verification: print and assemble the simple oval, confirm tiles align at edges

---

### Milestone 2: Firmware Foundation — DS3–DS5

**Weeks:** 3–4 (Mar 30–Apr 12)
**Purpose:** Base firmware architecture + first line follower working on hardware
**Class unlocked:** Classes 1–3 (DS1–DS5)
**Spec reference:** §3.1–§3.6, §3.8–§3.10

#### Phase 2.1: Firmware Architecture & Motor Driver

**Deliverables:**
* Abstract base classes: `LineSensor`, `Controller`, `MotorDriver`, `SpeedSensor` (spec §3.3)
* `config.py` with factory functions: `get_sensor()`, `get_controller()`, `get_motor_driver()`, etc. (spec §3.9)
* `motors/kitronik.py` — Kitronik Robotics Board motor driver via I2C/PCA9685 (spec §3.6)
* Main control loop structure (`main.py`) with cooperative polling (spec §3.8)
* Desktop pytest harness with conditional imports for hardware modules

**Test-gates:**
1. `config.py` factory functions instantiate correct module classes for each DS configuration
2. Motor driver desktop tests: `set_speeds()` and `stop()` accept valid inputs without error
3. Main loop structure runs on desktop with mock sensor/motor objects (no hardware)
4. On-hardware: motor test script drives both wheels forward 2 seconds, then stops (spec §7.5 DS3 gate 2)
5. On-hardware: motor test script turns left, then right — verifying wiring polarity (spec §7.5 DS3 gate 3)

#### Phase 2.2: IR Pair Sensor Module

**Deliverables:**
* `sensors/ir_pair.py` — IR Emitter/Phototransistor Pair driver (spec §3.4.1)
* Implements full `LineSensor` interface: `read_raw()`, `read_position()`, `calibrate()`, `line_detected()`
* Desktop unit tests with synthetic sensor data

**Test-gates:**
1. Desktop tests: `read_position()` returns −1.0 (left only), +1.0 (right only), 0.0 (both/neither)
2. Desktop tests: `line_detected()` returns correct boolean for all sensor combinations
3. On-hardware: IR pair reads "line" over black tape, "no line" over white paper (spec §7.5 DS3 gate 4)
4. Spec §7.5 DS3 gate 5: `gc.mem_free()` ≥ 100 KB with all DS3 modules loaded

#### Phase 2.3: Bang-Bang Controller & First Line Follower

**Deliverables:**
* `controllers/bang_bang.py` — simple on/off steering controller (spec §3.5.1)
* Implements full `Controller` interface: `update()`, `reset()`, `get_params()`, `set_params()`
* Integration: full pipeline running — IR pair → bang-bang → motors
* Tested on simple oval track (from M1)

**Test-gates — pass all DS4–DS5 test-gates (spec §7.5):**
1. Bang-bang controller follows the simple oval track for 1 complete lap
2. Robot recovers after being placed slightly off the line
3. Robot stops or reverses when it loses the line entirely
4. `read_position()` returns sensible values: negative when line is left, positive when right

---

### Milestone 3: Firmware Sensor Array — DS6–DS7

**Weeks:** 5–6 (Apr 13–26)
**Purpose:** QTRX sensor array driver + proportional controller
**Class unlocked:** Classes 4–5 (DS6–DS7)
**Spec reference:** §3.4.2, §3.5.2
**Hardware dependency:** QTRX-MD-08RC delivery (~April 2–6)

> **Note:** The QTRX driver code and desktop tests can be written in Week 4 while waiting for hardware. Hardware integration testing begins when the sensor array arrives.

#### Phase 3.1: QTRX Sensor Array Driver

**Deliverables:**
* `sensors/qtrx_array.py` — 8-channel reflectance sensor array via RC timing (spec §3.4.2)
* Calibration routine (drive over black and white surfaces, store min/max per sensor)
* LED control via CTRL pin (GP10)
* Line-lost memory (return last known position when line lost)
* Desktop unit tests with synthetic timing data

**Test-gates — pass DS6 test-gates 1–3 (spec §7.5):**
1. QTRX calibration completes without errors
2. All 8 sensors report distinct values for black vs white
3. `read_position()` accuracy: line under sensor 1 → ~−1.0, sensor 8 → ~+1.0

#### Phase 3.2: Proportional Controller + Sensor Array Integration

**Deliverables:**
* `controllers/proportional.py` — speed scales with position error (spec §3.5.2)
* Integration: QTRX array → proportional controller → motors
* `config.py` updated for DS6 and DS7 configurations (spec §3.10)
* Tested on oval-tight track and figure-eight track

**Test-gates — pass remaining DS6 + all DS7 test-gates (spec §7.5):**
1. Robot follows oval-tight track with smoother behavior than IR pair (DS6 gate 4)
2. Robot handles tighter curves than with the IR pair (DS6 gate 5)
3. Proportional controller adjusts speed based on position error (DS7 gate 1)
4. Robot goes faster on straights, slower on curves (DS7 gate 2)
5. Robot completes figure-eight track including crossover (DS7 gate 3)
6. Speed differential tunable via `kp` and `base_speed` parameters (DS7 gate 4)

---

### Milestone 4: Firmware WiFi + Browser UI — DS8

**Weeks:** 6–7 (Apr 20–May 3)
**Purpose:** WiFi access point + browser-based parameter control
**Class unlocked:** Class 6 (DS8)
**Spec reference:** §3.7, §6.1–§6.3

#### Phase 4.1: WiFi Access Point

**Deliverables:**
* `network/wifi_ap.py` — WiFi AP setup with unique SSID per unit (spec §3.7)
* AP starts on boot when `WIFI_ENABLED = True` in config
* IP address: `192.168.4.1`

**Test-gates:**
1. WiFi AP starts with correct SSID (e.g., `LFR-01`) (spec §7.5 DS8 gate 1)
2. Laptop connects to AP network
3. `gc.mem_free()` check: still sufficient RAM with WiFi active

#### Phase 4.2: Web Server & Browser Dashboard

**Deliverables:**
* `network/web_server.py` — minimal HTTP server, cooperative polling, non-blocking (spec §3.7)
* `network/ui_pages.py` — HTML templates for dashboard (spec §6.2 DS8 controls)
* API endpoints: `/`, `/params`, `/speed`, `/start`, `/stop`, `/status`, `/calibrate` (spec §6.3)
* Dashboard shows live sensor readings, speed control, start/stop

**Test-gates — pass all DS8 test-gates (spec §7.5):**
1. Laptop connects to AP and loads dashboard at `http://192.168.4.1/` (DS8 gate 2)
2. Live sensor readings update in the browser (DS8 gate 3)
3. Speed parameter changed via browser takes effect immediately (DS8 gate 4)
4. Start/Stop commands from browser work (DS8 gate 5)
5. Control loop maintains ≥20 Hz while serving HTTP requests (DS8 gate 6)

---

### Milestone 5: Firmware Speed Sensors — DS9

**Weeks:** 7–8 (Apr 27–May 10)
**Purpose:** Speed sensor driver + closed-loop feedback + browser display
**Class unlocked:** Class 7 (DS9)
**Spec reference:** §3.4.3, §6.2 DS9 controls

#### Phase 5.1: Speed Sensor Driver

**Deliverables:**
* `speed/optocoupler.py` — IR optocoupler wheel speed sensors (spec §3.4.3)
* Edge counting via `countio.Counter` (or polling fallback)
* RPM and cm/s conversion with wheel circumference calibration
* Desktop unit tests

**Test-gates:**
1. Both speed sensors report non-zero RPM when wheels spin (spec §7.5 DS9 gate 1)
2. RPM values proportional to actual wheel speed (DS9 gate 2)

#### Phase 5.2: Closed-Loop Integration + Browser Speed Display

**Deliverables:**
* Speed sensor data integrated into main control loop
* Browser UI updated: live RPM display, target vs actual speed (spec §6.2 DS9)
* Tested on figure-eight-chicane track

**Test-gates — pass remaining DS9 test-gates (spec §7.5):**
1. Speed sensor data displays correctly in browser UI (DS9 gate 3)
2. Robot runs 3 laps on figure-eight-chicane track with consistent lap times — within 10% variation (DS9 gate 4)

---

### Milestone 6: Firmware PID — DS10

**Weeks:** 8–9 (May 4–17)
**Purpose:** Full PID controller with browser-based tuning
**Class unlocked:** Class 8 (DS10) — core course capstone
**Spec reference:** §3.5.3, §6.2 DS10 controls

#### Phase 6.1: PID Controller Module

**Deliverables:**
* `controllers/pid.py` — full PID control with anti-windup (spec §3.5.3)
* All PID parameters exposed via `get_params()` / `set_params()` / `param_definitions`
* Desktop unit tests: P-only, PD, PID responses with known inputs
* Integral windup clamp working correctly

**Test-gates:**
1. PID controller compiles and runs without errors (spec §7.5 DS10 gate 1)
2. Desktop tests: P-only, PD, and full PID produce expected motor speed outputs for synthetic position data

#### Phase 6.2: PID Browser Tuning + Track Testing

**Deliverables:**
* Browser UI updated: PID parameter sliders (kp, ki, kd), error display, "Reset PID" button (spec §6.2 DS10)
* Tuning workflow validated: start with P only, add D, then I
* Tested on complex course track

**Test-gates — pass remaining DS10 test-gates (spec §7.5):**
1. All three PID parameters (kp, ki, kd) adjustable via browser UI (DS10 gate 2)
2. Changing kp visibly changes steering aggressiveness (DS10 gate 3)
3. Adding kd reduces oscillation compared to P-only control (DS10 gate 4)
4. Robot completes 3 laps on complex course track (DS10 gate 5)
5. Lap time improves by at least 20% compared to proportional controller on same track (DS10 gate 6)

> **Core course boundary:** Milestone 6 is the capstone for the 8-class core course. If the course stays at 8 classes, Classes 9–10 (Kalman, Q-Learning) become take-home exploration topics with provided code blocks. Milestones 8–9 below are stretch goals.

---

### Milestone 7: LFR Simulator

**Weeks:** 5–10 (Apr 13–May 24) — runs in parallel with firmware milestones
**Purpose:** 2D visual simulation for instructor demos and parameter tuning
**Class unlocked:** Not gated to a specific class; used by instructor throughout the course
**Spec reference:** §5 LFR Simulator Specification

> **Parallel track:** The simulator does not block any firmware milestone. It shares controller algorithms conceptually but has independent implementations. Work on it during evenings/weekends alongside firmware or in gaps between firmware milestones.

#### Phase 7.1: Simulator Scaffold & Physics Engine

**Weeks:** 5–6
**Deliverables:**
* Pygame window with track view area + sidebar panel layout (spec §5.6)
* Differential-drive physics engine (spec §5.2): position, heading, velocity from left/right wheel speeds
* Robot rendered as colored rectangle with heading arrow
* Time step control (10 ms simulation step, decoupled from render frame rate)
* Desktop pytest for physics model: known inputs → expected position/heading after N steps

**Test-gates:**
1. Pygame window opens with correct layout (track view + sidebar)
2. Physics model: robot drives straight forward for 1 second, position matches expected displacement
3. Physics model: differential steering produces expected turning radius
4. pytest suite passes for physics calculations

#### Phase 7.2: Track Loading & Sensor Simulation

**Weeks:** 6–7
**Deliverables:**
* Track loader: reads same JSON files as Line Track Designer (spec §5.5)
* Track rasterizer: renders track at ~1 mm/pixel resolution for sensor sampling
* IR pair sensor simulation (2 sample points) (spec §5.3)
* QTRX array sensor simulation (8 sample points + configurable noise) (spec §5.3)
* Speed sensor simulation (RPM from physics model + optional quantization noise)

**Test-gates:**
1. Track loads from JSON and renders correctly in the Pygame window
2. IR pair simulation: returns correct on/off line readings for known robot positions
3. QTRX simulation: `read_position()` returns weighted average matching firmware algorithm
4. Adding sensor noise produces visible variation in readings

#### Phase 7.3: Controller Integration

**Weeks:** 7–8
**Deliverables:**
* Simulator controller implementations mirroring firmware (spec §5.4):
  * `sim_bang_bang.py`, `sim_proportional.py`, `sim_pid.py`
* Controller selector dropdown in sidebar
* Robot follows line using each controller
* Same `update(position, dt) → (left, right)` interface as firmware

**Test-gates:**
1. Bang-bang controller: robot follows simple oval in simulation
2. Proportional controller: smoother tracking than bang-bang (visible)
3. PID controller: tuneable via sidebar sliders, reducing oscillation with kd
4. Controller algorithms produce identical outputs to firmware for same inputs (shared test data)

#### Phase 7.4: UI, Tuning Sliders & Polish

**Weeks:** 8–10
**Deliverables:**
* Parameter sliders for all controller parameters (spec §5.6 UI elements)
* Sensor bar display, position readout, speed readout, loop rate
* Start/Stop/Reset buttons
* Noise slider and simulation speed selector (1×, 2×, 5×, 10×)
* Keyboard shortcuts: Space, R, 1–5, +/− (spec §5.6)
* Save parameters to JSON
* Kalman+PID controller (`sim_kalman_pid.py`)
* Q-Learning controller (`sim_qlearning.py`) with accelerated training and Q-table display

**Test-gates:**
1. All parameter sliders adjust controller behavior in real time
2. Simulation runs at ≥30 fps at 1× speed
3. Q-Learning training at 10× speed shows reward increasing over episodes
4. Save/load parameters works correctly
5. All keyboard shortcuts function as documented

---

### Milestone 8: Firmware Kalman — DS11 (Stretch)

**Weeks:** 10–11 (May 18–31)
**Purpose:** Kalman filter preprocessing of sensor data before PID
**Class unlocked:** Class 9* (stretch)
**Spec reference:** §3.5.4, §6.2 DS11 controls

> **Stretch goal.** If development runs behind schedule, this milestone is the first to cut. Class 8 (PID) serves as the capstone, and Kalman filter becomes a take-home topic with provided code.

#### Phase 8.1: Kalman Filter Module

**Deliverables:**
* `controllers/kalman_pid.py` — 1D Kalman filter + PID (spec §3.5.4)
* Kalman predict/update cycle applied to position before PID processing
* Desktop tests with synthetic noisy position data: filtered output is smoother

**Test-gates:**
1. Kalman filter module runs without errors (spec §7.5 DS11 gate 1)
2. Desktop tests: filtered position variance < raw position variance for noisy input

#### Phase 8.2: Kalman Browser Integration + Track Testing

**Deliverables:**
* Browser UI updated: Q/R sliders, filter ON/OFF toggle, filtered vs raw position display (spec §6.2 DS11)
* Tested on complex course track

**Test-gates — pass remaining DS11 test-gates (spec §7.5):**
1. Filtered position noticeably smoother than raw position in browser readout (DS11 gate 2)
2. Filter ON/OFF toggle produces observable difference in robot smoothness (DS11 gate 3)
3. Robot completes 3 laps on complex course track with less wobble than unfiltered PID (DS11 gate 4)
4. Tuning Q and R via browser produces expected behavior (DS11 gate 5)

---

### Milestone 9: Firmware Q-Learning — DS12 (Stretch)

**Weeks:** 11–12 (May 25–Jun 7)
**Purpose:** Q-Learning reinforcement learning controller
**Class unlocked:** Class 10* (stretch)
**Spec reference:** §3.5.5, §6.2 DS12 controls

> **Stretch goal.** Second cut candidate if time is short.

#### Phase 9.1: Q-Learning Controller Module

**Deliverables:**
* `controllers/qlearning.py` — Q-table RL controller (spec §3.5.5)
* State discretization, action space, reward function
* Training mode (ε-greedy) and run mode (exploit learned policy)
* Q-table save/load to filesystem (`q_table.json`)
* Desktop tests: Q-table updates correctly for known state transitions

**Test-gates:**
1. Q-Learning controller runs in training mode without errors (spec §7.5 DS12 gate 1)
2. Desktop tests: Q-table values update per the Bellman equation for known inputs
3. Q-table saves and loads correctly (DS12 gate 4)

#### Phase 9.2: Q-Learning Browser Integration + Training

**Deliverables:**
* Browser UI updated: training mode toggle, state/action/reward display, episode counter, Q-table display, save/load buttons (spec §6.2 DS12)
* Physical robot training on track

**Test-gates — pass remaining DS12 test-gates (spec §7.5):**
1. Reward increases over 10 training episodes (DS12 gate 2)
2. Trained robot follows line without ε-greedy exploration (DS12 gate 3)
3. Browser UI displays training state: episode count, reward, current state/action (DS12 gate 5)

---

### Milestone 10: Final Prep & Course Readiness

**Weeks:** 12–13 (Jun 1–14)
**Purpose:** Flash all 6 LFR units, verify all tracks, prepare course materials
**Class unlocked:** All classes confirmed ready

#### Phase 10.1: Multi-Unit Flash & Verification

**Deliverables:**
* CircuitPython 10.1.4 + firmware flashed on all 6 Pico W units (5 student + 1 instructor)
* Each unit configured with unique `UNIT_NUMBER` (1–6) and WiFi SSID (`LFR-01` through `LFR-06`)
* Start at DS3 configuration (IR pair + bang-bang) — the first firmware students use
* Quick smoke test on each unit: motors spin, sensors read, REPL accessible

**Test-gates:**
1. All 6 units boot CircuitPython and reach REPL
2. All 6 units pass DS3 motor test (both wheels forward, then stop)
3. All 6 IR pair sensors read correctly (line vs no line)
4. All 6 units have unique SSID configured in `config.py`

#### Phase 10.2: Track Printing & Assembly Verification

**Deliverables:**
* All 6 course track PDFs printed on Makersmiths printer
* Simple oval track assembled on floor and alignment verified
* Spare track tiles printed (extras for damaged tiles)

**Test-gates:**
1. Simple oval track assembled; instructor unit (LFR-01) completes 3 laps
2. At least 3 different tracks printed and tiles align correctly
3. Line width measured on printed output: 19 mm ± 1 mm

#### Phase 10.3: Course Material Review

**Deliverables:**
* All docs reviewed for consistency: syllabus ↔ lesson plan ↔ spec ↔ development plan
* Student code templates prepared for each Design Session (the `config.py` variants)
* Instructor demo notes: which simulator demo to show at which class
* Backup copies of all firmware on USB drive

**Test-gates:**
1. Cross-document review: Design Session numbering consistent across all docs
2. A `config.py` file exists for each DS configuration (DS3 through DS12)
3. Simulator launches and runs a demo with PID controller on the complex course track
4. All materials accessible without internet (USB drive + local copies)

---

## 5. Risk Register

Risks from spec §9 plus development-specific risks. Sorted by impact.

| # | Risk | Category | Impact | Mitigation | Status |
|:--|:-----|:---------|:-------|:-----------|:-------|
| R1 | **QTRX RC timing via software GPIO** — CircuitPython is interpreted; µs-precision timing may be unreliable | Firmware | High | Test early in M3. Fallback: PIO-based timing on RP2040 if software timing insufficient. | Open |
| R2 | **Pico W RAM at DS12** — WiFi + HTTP + sensors + Q-table may exceed available RAM | Firmware | High | Profile `gc.mem_free()` at every milestone. Use `.mpy` compiled modules. Reduce Q-table size if needed. | Open |
| R3 | **`adafruit_httpserver` memory footprint** — may be too large for Pico W with other modules loaded | Firmware | Medium | Test at M4. Fallback: minimal raw-socket HTTP server (<100 lines). | Open |
| R4 | **QTRX sensor array delivery delay** — hardware not yet in hand; blocks M3 hardware testing | Procurement | Medium | QTRX driver code and desktop tests can proceed before hardware arrives. Order now if not already ordered. Expected ~April 2–6. | Open |
| R5 | **QTRX mounting on Emo chassis** — must be close to ground, centered in front | Hardware | Medium | May need 3D-printed or laser-cut bracket. Assess at first build in M3. Makersmiths has laser cutters available. | Open |
| R6 | **Emo chassis dimensions unknown** — axle width and wheel diameter affect simulator physics and speed calibration | Hardware | Medium | Measure at first build (M2 Phase 2.1). Update simulator physics parameters and firmware speed calculation constants. | Open |
| R7 | **`countio.Counter` availability** — needed for speed sensor edge counting in CP 10.1.4 | Firmware | Low | Fallback: polling-based edge counting in main loop. Less accurate at high RPM but functional. Test at M5. | Open |
| R8 | **Track tile alignment when printed** — printer margins may cause misalignment between tiles | Software | Low | Registration marks built into Track Designer (M1). Test with Makersmiths printer at M1 Phase 1.2. | Open |
| R9 | **Kitronik H-bridge IC unconfirmed** — assumed DRV8833; actual IC may differ | Hardware | Low | Inspect board at M2. PCA9685 control interface unchanged regardless of H-bridge IC. | Open |
| R10 | **Development time overrun** — 13 weeks is tight for 3 software systems | Schedule | Medium | Milestones 8–9 are explicit stretch goals. Simulator (M7) is off critical path and can be descoped. Core course (8 classes) needs only M0–M6 + M10. | Open |

---

## 6. Status Tracker

Update this table as phases are completed. Date format: YYYY-MM-DD.

### Milestone Status

| Milestone | Description | Target Week | Status | Date Completed | Notes |
|:----------|:-----------|:-----------|:-------|:---------------|:------|
| M0 | Project Bootstrap | Week 1 | Complete | 2026-03-17 | — |
| M1 | Line Track Designer | Week 2 | Not Started | — | — |
| M2 | Firmware Foundation DS3–DS5 | Week 4 | Not Started | — | — |
| M3 | Firmware Sensor Array DS6–DS7 | Week 6 | Not Started | — | Blocked by QTRX delivery for HW testing |
| M4 | Firmware WiFi + Browser UI DS8 | Week 7 | Not Started | — | — |
| M5 | Firmware Speed Sensors DS9 | Week 8 | Not Started | — | — |
| M6 | Firmware PID DS10 | Week 9 | Not Started | — | Core course capstone |
| M7 | LFR Simulator | Week 10 | Not Started | — | Parallel track; off critical path |
| M8 | Firmware Kalman DS11 | Week 11 | Not Started | — | Stretch goal |
| M9 | Firmware Q-Learning DS12 | Week 12 | Not Started | — | Stretch goal |
| M10 | Final Prep & Readiness | Week 13 | Not Started | — | — |

### Phase Status

| Milestone | Phase | Description | Status | Date Completed | Notes |
|:----------|:------|:-----------|:-------|:---------------|:------|
| M0 | 0.1 | Repo & tooling setup | Complete | 2026-03-17 | All 4 gates passed |
| M0 | 0.2 | Hardware verification | Complete | 2026-03-17 | All 3 gates passed |
| M1 | 1.1 | Track Designer core engine | Not Started | — | — |
| M1 | 1.2 | Course track designs | Not Started | — | — |
| M2 | 2.1 | Firmware architecture & motor driver | Not Started | — | — |
| M2 | 2.2 | IR pair sensor module | Not Started | — | — |
| M2 | 2.3 | Bang-bang controller & first line follower | Not Started | — | — |
| M3 | 3.1 | QTRX sensor array driver | Not Started | — | — |
| M3 | 3.2 | Proportional controller + integration | Not Started | — | — |
| M4 | 4.1 | WiFi access point | Not Started | — | — |
| M4 | 4.2 | Web server & browser dashboard | Not Started | — | — |
| M5 | 5.1 | Speed sensor driver | Not Started | — | — |
| M5 | 5.2 | Closed-loop integration + browser display | Not Started | — | — |
| M6 | 6.1 | PID controller module | Not Started | — | — |
| M6 | 6.2 | PID browser tuning + track testing | Not Started | — | — |
| M7 | 7.1 | Simulator scaffold & physics engine | Not Started | — | — |
| M7 | 7.2 | Track loading & sensor simulation | Not Started | — | — |
| M7 | 7.3 | Controller integration | Not Started | — | — |
| M7 | 7.4 | UI, tuning sliders & polish | Not Started | — | — |
| M8 | 8.1 | Kalman filter module | Not Started | — | — |
| M8 | 8.2 | Kalman browser integration + testing | Not Started | — | — |
| M9 | 9.1 | Q-Learning controller module | Not Started | — | — |
| M9 | 9.2 | Q-Learning browser integration + training | Not Started | — | — |
| M10 | 10.1 | Multi-unit flash & verification | Not Started | — | — |
| M10 | 10.2 | Track printing & assembly verification | Not Started | — | — |
| M10 | 10.3 | Course material review | Not Started | — | — |

---

## 7. Dependency Graph

### What Blocks What

```text
M0 (Bootstrap)
 ├──► M1 (Track Designer) ──► M2 Phase 2.3 (needs oval track for testing)
 └──► M2 (Firmware Foundation)
       └──► M3 (Sensor Array) ←── QTRX hardware delivery
             └──► M4 (WiFi + Browser UI)
                   └──► M5 (Speed Sensors)
                         └──► M6 (PID) ──► M10 (Final Prep)
                               └──► M8 (Kalman) ──► M9 (Q-Learning) ──► M10

M0 ──► M7 Phase 7.1 (Sim scaffold — needs no firmware, just Python)
M1 ──► M7 Phase 7.2 (Track loading — needs JSON format from M1)
M2 ──► M7 Phase 7.3 (Controller integration — needs algorithm design from M2)
M6 ──► M7 Phase 7.4 (PID/Kalman/Q-Learning controllers in sim — needs algorithms from M6+)
```

### External Dependencies

| Dependency | Blocks | Expected Resolution |
|:-----------|:-------|:-------------------|
| QTRX-MD-08RC sensor array delivery | M3 hardware testing | ~April 2–6 (2–3 weeks from project start) |
| Emo chassis physical measurements | M2 motor calibration, M7 physics params | Measured at M2 Phase 2.1 first build |
| Makersmiths printer access | M1 Phase 1.2, M10 Phase 10.2 | Coordinate with makerspace schedule |
| Makersmiths floor space for track | M2 Phase 2.3 onward | Confirm availability for testing sessions |

### Design Session Coverage Cross-Check

Every Design Session (DS3–DS12) is covered by a milestone:

| Design Session | Milestone | Class | Core/Stretch |
|:---------------|:----------|:------|:-------------|
| DS1–DS2 | *(No software — demo + chassis assembly)* | Class 1 | Core |
| DS3 | M2 (Phases 2.1–2.2) | Class 2 | Core |
| DS4–DS5 | M2 (Phase 2.3) | Class 3 | Core |
| DS6 | M3 (Phase 3.1) | Class 4 | Core |
| DS7 | M3 (Phase 3.2) | Class 5 | Core |
| DS8 | M4 | Class 6 | Core |
| DS9 | M5 | Class 7 | Core |
| DS10 | M6 | Class 8 | Core |
| DS11 | M8 | Class 9* | Stretch |
| DS12 | M9 | Class 10* | Stretch |

### Software System Coverage Cross-Check

| System | Milestones | Complete When |
|:-------|:-----------|:-------------|
| LFR Firmware | M0, M2, M3, M4, M5, M6, M8*, M9* | M6 (core) or M9 (stretch) |
| Line Track Designer | M1 | M1 |
| LFR Simulator | M7 | M7 |

---

## Appendix A: Development Plan Prompt & Q&A

### Original Prompt

The following prompt was used to generate this development plan (reproduced verbatim from the instructor's prompt document):

> Along with CLAUDE.md, read only @input/*.md and @docs/*.md files.
> Create a development plan, to be called @docs/development-plan.md,
> describing how & when things are to be created / built.
> The development plan must reflect the incremental build approach outlined in the Line Following Robot (LFR) course.
>
> Make sure to cover all major software components and their build order,
> key technical decisions to resolve upfront (e.g., which Python GUI library for the simulator),
> a rough phasing that mirrors your course's Design Sessions,
> and any external dependencies or risks (like CircuitPython library availability for the QTRX sensor).
>
> I want to build the LFR via a phased plan, and at the end of each build phase,
> three to eight tests, I'll call these "test-gates",
> will be performed to validate what has been created within that phase.
> Do not move onto the next phase until all test-gates pass.
>
> Within this phased plan, there will be sets of sequenced phases, when completed successfully,
> are called a milestone.
> A milestone will contain all the required software for a specific class day within the course.
>
> Produce the plan as a living document so it can be updated as the project evolves,
> not just a one-time artifact.
> I want it to serve as an ongoing reference rather than going stale after the first few sessions.
> Given the scope of this project — firmware, a simulator, a track designer, and incremental design sessions —
> I want this plan to save significant back-and-forth with Claude Code over the course of development.
>
> Within the document you create, include this prompt,
> all questions you ask me, along with my responses.
> Place this in an appendix and reference it at the beginning of the development plan
> and anywhere else in the text when its a useful reference.
>
> Think Hard about what must be done to create a robust plan.
>
> As a final step, review all @input/*.md and @docs/*.md files and make sure they are consistent and correct.
>
> I expect there will be some issues,
> so use the AskUserQuestions tool for all things that require further clarification.

### Instructor Q&A

All questions asked during development plan creation and the instructor's responses:

| # | Question | Answer |
|:--|:---------|:-------|
| 1 | How many hours per week can you dedicate to development? (5–10, 10–20, 20+) | *(Not answered — proceeding with schedule-based milestones rather than hour estimates)* |
| 2 | Have you ordered the physical hardware yet? | All hardware in hand except the sensor array |
| 3 | If you run short on time, what's your cut priority? (Simulator first, stretch classes first, both, must build everything) | *(Not answered — plan marks M8–M9 as stretch goals and M7 as off critical path, providing natural cut points)* |
| 4 | Do you want Claude Code sessions to build the actual code following this plan? | *(Not answered — plan is structured to support either approach: Claude-built or manually built)* |
| 5 | When do you expect the QTRX-MD-08RC sensor array to arrive? | 2–3 weeks (arriving approximately April 2–6) |

---

<!-- Reference-style links -->
[L01]:https://makersmiths.org/
[L02]:https://www.makerspaces.com/what-is-a-makerspace/
