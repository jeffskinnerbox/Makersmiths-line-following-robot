# LFR Course — Specification Document

* **Project**: Line Following Robot (LFR) Course at Makersmiths
* **Author**: Instructor / Sole Developer
* **Date**: 2026-02-26
* **Status**: Pre-course development specification

> The key decisions driving this specification — choice of tools, testing strategy,
> and software architecture approach — emerged from a structured Q&A session.
> See [Appendix A][appendix-a] for the full development dialogue.

---------------

## Table of Contents

1. [Introduction & Purpose][s1]
2. [Course Overview][s2]
3. [Hardware Specification][s3]
4. [Software Architecture][s4]
5. [Firmware Specification][s5]
6. [LFR Simulator Specification][s6]
7. [Line Track Designer Specification][s7]
8. [Testing Strategy][s8]
9. [Development Timeline][s9]
10. [Risk Assessment][s10]

[Appendix A: Development Dialogue][appendix-a]

---------------

## 1. Introduction & Purpose {#s1}

This document specifies everything that must be designed, built, and validated
before the first class of the LFR course at Makersmiths. The course is scheduled
to begin in approximately 6 months. The instructor is the sole developer for all
software and the sole person responsible for hardware procurement and pre-assembly.

This specification covers:

* **Hardware** — all physical components per robot, per design session
* **Firmware** — CircuitPython modules running on the Raspberry Pi Pico W
* **LFR Simulator** — Python desktop tool for developing and testing control algorithms
* **Line Track Designer** — Python desktop tool for designing and printing test tracks
* **Testing strategy** — how the instructor validates each design session before class

The full development dialogue that produced the key architectural decisions in this
document is preserved verbatim in [Appendix A][appendix-a].

---------------

## 2. Course Overview {#s2}

### Student Profile & Class Logistics

| Attribute | Detail |
|:----------|:-------|
| Age range | 12–18 (some younger possible); adult participants (parents) |
| Coding background | Basic Scratch or introductory Python; no hardware experience |
| Expected enrollment | ~5 students + ~2 parent assistants |
| Total robots | 6 (5 student robots + 1 instructor robot) |
| Class duration | 2 hours per session |
| Class count | Driven by course goals; not fixed |
| Location | Makersmiths makerspace; flat floor area sufficient for a 4×3 tile track |
| Track size | 4 columns × 3 rows of 11" × 8.5" tiles (~44" × 25.5") + robot clearance |
| Robot ownership | Students keep their robots at course end |

### Design Session Map

Each Design Session (DS) represents a major functional milestone. A DS may span
more than one class period.

| DS | Title | Goal | Key Concepts |
|:---|:------|:-----|:-------------|
| DS1 | Course Kickoff | Demonstrate commercial LFR; set expectations | LFR fundamentals, course roadmap, competitive events |
| DS2 | Chassis Assembly | Build the base robot platform | Mechanical assembly, kit familiarization |
| DS3 | Hardware Integration | Add electronics to chassis | Power systems, GPIO, breadboarding |
| DS4 | Simple LFR | Bang-bang line follower on Pico W | CircuitPython, IR sensing, motor control, bang-bang logic |
| DS5 | Sensor Upgrade | Replace IR pair with 8-element reflectance array | Sensor arrays, line position estimation, speed tuning |
| DS6 | WiFi Interface | Pico W as WiFi AP; web UI for speed control | WiFi, HTTP server, dynamic control |
| DS7 | Open-Loop Speed Control | Add wheel speed sensors; open-loop control | Speed sensors, open-loop vs closed-loop, autonomy concepts |
| DS8 | PID Controller | Autonomous speed & direction via PID | PID tuning, Ziegler-Nichols, sensor noise, intro Kalman |
| DS9 | Kalman Filter | Add Kalman filtering to reduce sensor noise | State estimation, noise filtering, Kalman theory |
| DS10 | Advanced Control Theory | Survey ADRC, MPC, RL; decide on Q-Learning | Reinforcement learning, model-free control, Q-Learning |
| DS11 | Q-Learning Controller | Deploy Q-Learning controller; course wrap-up | Q-table, training, deployment, course reflection |

---------------

## 3. Hardware Specification {#s3}

### Per-Robot Component Manifest

Components are grouped by the design session when they are first introduced.
All quantities are per robot. Total robot count is 6.

#### DS1 — Instructor Demo Only

| Component | Qty | Notes |
|:----------|:----|:------|
| [MiOYOOW Line Following Robot Car Kit][mioyoow] | 1 | Instructor demo unit only; not built by students |

#### DS2 — Chassis Assembly

| Component | Qty | Notes |
|:----------|:----|:------|
| [Emo Smart Robot Car Chassis Kit][emo-chassis] | 1 | Base platform; students assemble |

#### DS3 — Hardware Integration

| Component | Qty | Notes |
|:----------|:----|:------|
| [8 × AA Battery Holder][battery-holder] | 1 | Primary motor power supply |
| [Raspberry Pi Pico W][pico-w] | 1 | Microcontroller; CircuitPython runtime |
| [Robotics Motor Driver Board][motor-driver] | 1 | Variable speed & direction for 2 DC motors; mounts Pico W |
| [IR Emitter/Phototransistor Pair][ir-pair] | 1 | Initial single-point line sensor (replaced in DS5) |
| [400 Pin Solderless Prototype Board][breadboard] | 1 | Breadboard for prototyping connections |
| [5V Buck Converter Module][buck-converter] | 1 | Steps battery voltage down to 5V for digital devices |

#### DS5 — Sensor Upgrade

| Component | Qty | Notes |
|:----------|:----|:------|
| [QTRX-MD-08RC Reflectance Sensor Array][qtrx] | 1 | 8-element array; replaces IR pair |

#### DS7 — Open-Loop Speed Control

| Component | Qty | Notes |
|:----------|:----|:------|
| [Speed Sensor Module][speed-sensor] | 2 | One per driven wheel; optical encoder disc |

### Per-Robot Parts Summary

| Component | Qty/Robot | First DS | Status at Course End |
|:----------|:---------:|:--------:|:---------------------|
| MiOYOOW Kit | 1 | DS1 | Instructor only |
| Emo Chassis Kit | 1 | DS2 | In robot |
| 8× AA Battery Holder | 1 | DS3 | In robot |
| Raspberry Pi Pico W | 1 | DS3 | In robot |
| Robotics Motor Driver Board | 1 | DS3 | In robot |
| IR Emitter/Phototransistor Pair | 1 | DS3 | Removed at DS5 |
| 400 Pin Solderless Prototype Board | 1 | DS3 | In robot |
| 5V Buck Converter Module | 1 | DS3 | In robot |
| QTRX-MD-08RC Reflectance Sensor Array | 1 | DS5 | In robot |
| Speed Sensor Module | 2 | DS7 | In robot |

### Raspberry Pi Pico W GPIO Pin Allocation

The Pico W provides 26 usable GPIO/PIO/PWM pins. When installed on the
Robotics Motor Driver Board, some pins are consumed by the board. The
remaining ~18 pins are available for LFR peripherals.

> **Decision**: Exact Motor Driver Board pin assignments must be confirmed
> against the [Robotics Motor Driver Board pinout][motor-driver] before
> firmware development begins. The table below marks board-consumed pins as
> TBD and lists planned peripheral assignments.

| GPIO | Function | Assigned To | First DS |
|:-----|:---------|:------------|:--------:|
| GP0 | I2C0 SDA | Reserved / future expansion | — |
| GP1 | I2C0 SCL | Reserved / future expansion | — |
| GP2–GP5 | Motor control A | Robotics Motor Driver Board | DS3 |
| GP6–GP7 | Motor control B | Robotics Motor Driver Board | DS3 |
| GP8–GP9 | Internal | used by Robotics Motor Driver Board | — |
| GP10 | Digital in | IR Sensor — Left emitter/detector | DS3 |
| GP11 | Digital in | IR Sensor — Right emitter/detector | DS3 |
| GP12–GP19 | Digital in | QTRX-MD-08RC — 8 sensor elements (replaces GP10/GP11 at DS5) | DS5 |
| GP20 | Digital in | Speed Sensor — Left wheel | DS7 |
| GP21 | Digital in | Speed Sensor — Right wheel | DS7 |
| GP22 | TBD | Available | — |
| GP23–GP25 | Internal | Pico W internal use (WiFi, VBUS sense, LED) | — |
| GP26–GP27 | Motor control B | Robotics Motor Driver Board | DS3 |
| GP28 (ADC2) | Analog in | Available | — |

> **Note**: WiFi on the Pico W uses the onboard CYW43439 chip via SPI internally;
> no user GPIO pins are consumed for WiFi.

---------------

## 4. Software Architecture {#s4}

### System Diagram

```text
+------------------------------------------------------------------+
|                        LFR Monorepo                              |
|                                                                  |
|  +----------------------------+  +----------------------------+  |
|  |  firmware/  (CircuitPython)|  |  Desktop Tools (Python)    |  |
|  |                            |  |                            |  |
|  |  main.py                   |  |  +----------------------+  |  |
|  |                            |  |  |   LFR Simulator      |  |  |
|  |  controllers/              |  |  |  physics.py          |  |  |
|  |    ControllerBase (ABC)    |  |  |  sensor_sim.py       |  |  |
|  |    bang_bang.py    (DS4)   |  |  |  visualization.py   |  |  |
|  |    open_loop.py    (DS7)   |<-+->|  metrics.py         |  |  |
|  |    pid.py          (DS8)   |  |  |  (shared HAL)       |  |  |
|  |    kalman.py       (DS9)   |  |  +----------+----------+  |  |
|  |    q_learning.py   (DS11)  |  |             |              |  |
|  |                            |  |         track.json         |  |
|  |  hal/                      |  |             |              |  |
|  |    base.py  (SensorHAL,    |  |  +----------v----------+  |  |
|  |             MotorHAL ABCs) |  |  | Line Track Designer  |  |  |
|  |    pico_hal.py             |  |  |  canvas.py           |  |  |
|  |    sim_hal.py              |  |  |  tile_library.py     |  |  |
|  |                            |  |  |  export.py (PDF/JSON)|  |  |
|  |  sensors/                  |  |  +---------------------+  |  |
|  |    ir_sensor.py            |  |                            |  |
|  |    reflectance_array.py    |  +----------------------------+  |
|  |                            |                                  |
|  |  speed_sensor/             |  +----------------------------+  |
|  |    speed_sensor.py         |  |  tests/                    |  |
|  |                            |  |    unit/  (algorithm only) |  |
|  |  wifi/                     |  |    sim/   (end-to-end sim) |  |
|  |    web_server.py           |  |    hardware/  (checklists) |  |
|  |                            |  +----------------------------+  |
|  |  config.py                 |                                  |
|  +----------------------------+                                  |
+------------------------------------------------------------------+
```

### Monorepo Layout

```text
lfr-course/
+-- firmware/                      # CircuitPython source (runs on Pico W)
|   +-- hal/
|   |   +-- base.py                # SensorHAL, MotorHAL, ControllerBase ABCs
|   |   +-- pico_hal.py            # Pico W hardware implementation
|   |   +-- sim_hal.py             # Simulator implementation
|   +-- sensors/
|   |   +-- ir_sensor.py           # IR Emitter/Phototransistor logic (DS3)
|   |   +-- reflectance_array.py   # QTRX-MD-08RC logic (DS5)
|   +-- speed_sensor/
|   |   +-- speed_sensor.py        # Wheel speed sensor logic (DS7)
|   +-- controllers/
|   |   +-- base.py                # ControllerBase ABC
|   |   +-- bang_bang.py           # Bang-bang controller (DS4)
|   |   +-- open_loop.py           # Open-loop speed controller (DS7)
|   |   +-- pid.py                 # PID controller (DS8)
|   |   +-- kalman.py              # Kalman filter wrapper (DS9)
|   |   +-- q_learning.py          # Q-Learning controller (DS11)
|   +-- wifi/
|   |   +-- web_server.py          # WiFi AP + HTTP server (DS6)
|   +-- config.py                  # Central tuning parameters
|   +-- main.py                    # Entry point; selects active controller
+-- simulator/                     # Desktop LFR simulator (Ubuntu/Python)
|   +-- physics.py                 # Differential drive kinematics
|   +-- sensor_sim.py              # Reads track image; computes sensor values
|   +-- track.py                   # Loads/validates track.json
|   +-- visualization.py           # 2D pygame rendering
|   +-- ui.py                      # Parameter control panel (sliders, buttons)
|   +-- metrics.py                 # Path error, lap time, oscillation count
|   +-- plugin.py                  # Controller plugin loader
|   +-- main.py                    # Simulator entry point
+-- track_designer/                # Line Track Designer (Ubuntu/Python)
|   +-- tile_library.py            # Tile type definitions and SVG assets
|   +-- canvas.py                  # Interactive tile placement GUI
|   +-- export.py                  # PDF (printable) + track.json export
|   +-- save_load.py               # Layout persistence (.layout files)
|   +-- main.py                    # Designer entry point
+-- tests/
|   +-- unit/                      # Pure algorithm tests; no hardware dependency
|   +-- sim/                       # End-to-end simulation tests
|   +-- hardware/                  # Pre-class hardware validation checklists
+-- tracks/                        # Saved track layout files (track.json)
+-- docs/                          # Course documentation (syllabus, lesson plans)
+-- input/                         # Instructor-authored source documents
+-- CLAUDE.md
+-- specification.md
```

### Hardware Abstraction Layer (HAL) Strategy

**Principle**: All firmware modules access hardware exclusively through HAL
interfaces. No firmware module ever imports a hardware-specific library directly.
This is what allows the same controller code to run on both the Pico W and the
desktop simulator.

```text
firmware module
    |
    v
hal/base.py  (abstract interface — SensorHAL, MotorHAL)
    |              |
    v              v
pico_hal.py    sim_hal.py
(real GPIO)   (simulator physics)
```

At startup, `main.py` receives a HAL implementation (Pico or Simulator) and
injects it into all modules. Controllers never know which HAL they are using.

### Simulator-First Development Philosophy

> **Decision** (see [Appendix A][appendix-a]): The primary development and
> validation environment is the desktop simulator. Control algorithms are
> developed, tuned, and validated in the simulator before deployment to hardware.

This approach:

* Eliminates hardware availability as a blocker during algorithm development
* Enables rapid iteration on tuning parameters (no reflash cycle)
* Provides measurable, repeatable test conditions (same track, same run)
* Allows visual demonstration in class (project simulator on screen)
* Requires that `sim_hal.py` faithfully model hardware behavior

Hardware validation is a final confirmation step, not the development environment.

---------------

## 5. Firmware Specification {#s5}

### HAL Interface Definitions

`firmware/hal/base.py` defines the abstract interfaces. All implementations
must satisfy these contracts exactly.

```python
from abc import ABC, abstractmethod

class SensorHAL(ABC):
    @abstractmethod
    def read_ir_pair(self) -> tuple[bool, bool]:
        """(left_on_line, right_on_line). True = sensor over dark line."""

    @abstractmethod
    def read_reflectance_array(self) -> list[float]:
        """8 normalized readings. 0.0 = white surface, 1.0 = black line."""

    @abstractmethod
    def read_wheel_speeds(self) -> tuple[float, float]:
        """(left_rpm, right_rpm). Positive = forward."""

class MotorHAL(ABC):
    @abstractmethod
    def set_speeds(self, left: float, right: float) -> None:
        """Set motor outputs. Range: -1.0 (full reverse) to 1.0 (full forward)."""

    @abstractmethod
    def stop(self) -> None:
        """Bring both motors to a halt immediately."""

class ControllerBase(ABC):
    @abstractmethod
    def compute(
        self,
        sensor: list[float],
        speed: tuple[float, float],
        dt: float,
    ) -> tuple[float, float]:
        """
        Compute motor output.

        Args:
            sensor: Normalized sensor readings (length matches active sensor).
            speed:  Current (left_rpm, right_rpm).
            dt:     Elapsed seconds since last call.

        Returns:
            (left_output, right_output) each in [-1.0, 1.0].
        """

    @abstractmethod
    def configure(self, params: dict) -> None:
        """Apply runtime tuning parameters (called from WiFi UI or config.py)."""

    @abstractmethod
    def reset(self) -> None:
        """Reset internal state (integrators, Q-table replay, etc.)."""
```

### Module Specifications

#### `config.py` (DS3)

Central store for all tunable parameters. Loaded at startup; updated at runtime
via `configure()` calls from `web_server.py`.

| Parameter | Type | Default | Description |
|:----------|:-----|:--------|:------------|
| `CONTROLLER` | `str` | `"bang_bang"` | Active controller module name |
| `BASE_SPEED` | `float` | `0.5` | Nominal forward speed (0.0–1.0) |
| `SENSOR_TYPE` | `str` | `"ir_pair"` | `"ir_pair"` or `"reflectance_array"` |
| `WIFI_SSID` | `str` | `"LFR-{id}"` | Per-robot unique WiFi SSID |
| `WIFI_PASSWORD` | `str` | `"lfr12345"` | AP password |
| `PID_KP` | `float` | `1.0` | PID proportional gain |
| `PID_KI` | `float` | `0.0` | PID integral gain |
| `PID_KD` | `float` | `0.1` | PID derivative gain |
| `KALMAN_Q` | `float` | `0.01` | Kalman process noise covariance |
| `KALMAN_R` | `float` | `0.1` | Kalman measurement noise covariance |
| `QL_ALPHA` | `float` | `0.1` | Q-Learning learning rate |
| `QL_GAMMA` | `float` | `0.9` | Q-Learning discount factor |
| `QL_EPSILON` | `float` | `0.1` | Q-Learning exploration rate |

#### `sensors/ir_sensor.py` (DS3)

Reads the single IR Emitter/Phototransistor Pair via `SensorHAL`. Implements
`read_ir_pair() -> tuple[bool, bool]`. Returns `(True, False)` when left
sensor sees line; `(False, True)` for right; `(True, True)` for centered;
`(False, False)` for off-track.

#### `sensors/reflectance_array.py` (DS5)

Reads the QTRX-MD-08RC 8-element array via `SensorHAL`. Implements
`read_reflectance_array() -> list[float]`. Performs calibration on startup
(white surface → 0.0, black line → 1.0). Computes weighted centroid for
line position estimate: position ∈ [-3.5, +3.5] where 0 = centered.

#### `speed_sensor/speed_sensor.py` (DS7)

Counts pulses from optical encoder discs via interrupt on GPIO pins. Converts
pulse count + time delta to RPM. Implements `read_wheel_speeds() -> tuple[float, float]`.

#### `wifi/web_server.py` (DS6)

Pico W configured as a WiFi access point (not a station). Runs a minimal HTTP
server on port 80. Serves a single-page HTML5 UI. Accepts `POST /config` with
JSON body to update `config.py` parameters at runtime. UI elements grow across
design sessions:

| DS | UI Feature Added |
|:---|:----------------|
| DS6 | Base speed slider |
| DS7 | Left/right speed trim |
| DS8 | PID Kp, Ki, Kd sliders; reset integrators button |
| DS9 | Kalman Q, R sliders |
| DS11 | Q-table status display; exploration rate slider |

#### `controllers/bang_bang.py` (DS4)

Implements `ControllerBase`. Uses `SensorHAL.read_ir_pair()`. Logic:

* Both sensors off line → stop or spin to search
* Left on, right off → turn left (reduce left motor, increase right)
* Right on, left off → turn right
* Both on → go straight at `BASE_SPEED`

No tunable parameters beyond `BASE_SPEED`.

#### `controllers/open_loop.py` (DS7)

Implements `ControllerBase`. Uses `SensorHAL.read_reflectance_array()` for line
position and `SensorHAL.read_wheel_speeds()` for feedback. Applies a
proportional correction to maintain target speed independently on each wheel.
Error = target_speed − measured_speed. No integral or derivative term.

#### `controllers/pid.py` (DS8)

Implements `ControllerBase`. Line position error = weighted centroid of
reflectance array readings. PID output adjusts differential between left and
right motor speeds.

```text
error(t)     = line_position(t)          # centroid, range [-3.5, 3.5]
integral(t)  = integral(t-1) + error * dt
derivative   = (error - prev_error) / dt
output       = Kp*error + Ki*integral + Kd*derivative
left_speed   = BASE_SPEED - output
right_speed  = BASE_SPEED + output
```

Integral is clamped to prevent windup. All gains tunable via `configure()`.

#### `controllers/kalman.py` (DS9)

Wraps `pid.py` with a 1D Kalman filter on the line position signal before
feeding it to the PID computation. State variable: line position. Reduces
sensor noise effects.

```text
Predict:  x_pred = x_prev              (constant position model)
          P_pred = P_prev + Q
Update:   K = P_pred / (P_pred + R)
          x_est = x_pred + K * (z - x_pred)
          P_est = (1 - K) * P_pred
```

Parameters Q (process noise) and R (measurement noise) tunable via `configure()`.

#### `controllers/q_learning.py` (DS11)

Implements `ControllerBase`. Model-free reinforcement learning; learns a policy
from experience. The Q-table is trained in the simulator, then serialized to
JSON and deployed to the Pico W (read-only at runtime).

**State space**: Line position quantized to N discrete buckets (default N=7:
far-left, left, slightly-left, center, slightly-right, right, far-right).

**Action space**: 5 discrete actions:
    0 = sharp left, 1 = gentle left, 2 = straight, 3 = gentle right, 4 = sharp right

**Reward function**: +1 for staying on line, −10 for leaving track,
    +0.5 bonus for high speed while centered.

**Q-table**: 7×5 matrix of float rewards. Trained in simulator, loaded from
`q_table.json` on Pico W at startup. Exploration (epsilon-greedy) disabled at
deploy time.

**Training** occurs only in the simulator. Hardware runs inference only.

---------------

## 6. LFR Simulator Specification {#s6}

> **Decision** (see [Appendix A][appendix-a]): The LFR Simulator is a **custom
> Python build** for Ubuntu. It is tightly integrated with the firmware HAL so
> that firmware controller modules run inside the simulator without modification.
>
> **Decision**: Rendering library is **pygame**. Chosen for interactive
> frame-rate rendering, event handling, and wide availability on Ubuntu.

### Robot Physics Model

The simulator uses a **differential drive kinematic model**.

```text
Inputs:   left_output, right_output  ([-1.0, 1.0] from controller)
          wheel_base  W  (meters)
          wheel_radius r (meters)

Left wheel speed:   v_L = left_output  * MAX_SPEED_M_S
Right wheel speed:  v_R = right_output * MAX_SPEED_M_S

Linear speed:    v = (v_R + v_L) / 2
Angular speed:   w = (v_R - v_L) / W

State update (Euler, dt seconds):
    x       += v * cos(heading) * dt
    y       += v * sin(heading) * dt
    heading += w * dt
```

Default physical parameters (adjustable in simulator UI):

| Parameter | Default | Units |
|:----------|:--------|:------|
| `MAX_SPEED_M_S` | 0.5 | m/s |
| `WHEEL_BASE` | 0.12 | m |
| `WHEEL_RADIUS` | 0.03 | m |
| `ROBOT_WIDTH` | 0.14 | m |
| `ROBOT_LENGTH` | 0.18 | m |

### Sensor Simulation Model

`sensor_sim.py` samples the track image beneath the robot's simulated sensor
positions to compute sensor readings.

* Track is rendered to an off-screen pygame Surface at full resolution
* For each sensor element, the pixel at the sensor's world position is sampled
* Pixel luminance maps to a normalized reading: 0.0 (white) → 1.0 (black)
* IR pair simulation: two sample points, left and right of center
* Reflectance array simulation: 8 sample points, evenly spaced across sensor width

Gaussian noise (configurable σ) is added to each sensor reading to approximate
real-world sensor noise.

### Track Format (track.json)

The track JSON format is the **shared contract** between the Line Track Designer
(which writes it) and the LFR Simulator (which reads it). Both tools must
validate against this schema.

**Schema**:

```json
{
    "version": "1.0",
    "name": "string",
    "created": "YYYY-MM-DD",
    "grid": {
        "cols": "integer (number of tile columns)",
        "rows": "integer (number of tile rows)",
        "tile_width_in": "float (physical width in inches, default 11.0)",
        "tile_height_in": "float (physical height in inches, default 8.5)",
        "tile_width_px": "integer (render resolution width per tile)",
        "tile_height_px": "integer (render resolution height per tile)"
    },
    "tiles": [
        {
            "col": "integer (0-indexed, left to right)",
            "row": "integer (0-indexed, top to bottom)",
            "type": "string (see Tile Types below)",
            "rotation_deg": "integer (0, 90, 180, or 270)"
        }
    ],
    "start": {
        "col": "integer",
        "row": "integer",
        "heading_deg": "float (0=east, 90=south, 180=west, 270=north)"
    },
    "line": {
        "width_px": "integer (rendered line width in pixels)",
        "color_hex": "string (line color, default '#000000')",
        "bg_color_hex": "string (background color, default '#FFFFFF')"
    }
}
```

**Tile Types**:

| Type | Description |
|:-----|:------------|
| `straight_h` | Horizontal straight |
| `straight_v` | Vertical straight |
| `curve_ne` | Curve connecting North and East edges |
| `curve_nw` | Curve connecting North and West edges |
| `curve_se` | Curve connecting South and East edges |
| `curve_sw` | Curve connecting South and West edges |
| `t_north` | T-junction open to North |
| `t_south` | T-junction open to South |
| `t_east` | T-junction open to East |
| `t_west` | T-junction open to West |
| `crossover` | 4-way intersection |
| `blank` | No line; empty tile |

**Example** (minimal 2-tile loop segment):

```json
{
    "version": "1.0",
    "name": "Test Oval",
    "created": "2026-02-26",
    "grid": {
        "cols": 4, "rows": 3,
        "tile_width_in": 11.0, "tile_height_in": 8.5,
        "tile_width_px": 880, "tile_height_px": 680
    },
    "tiles": [
        {"col": 0, "row": 0, "type": "curve_se", "rotation_deg": 0},
        {"col": 1, "row": 0, "type": "straight_h", "rotation_deg": 0},
        {"col": 2, "row": 0, "type": "straight_h", "rotation_deg": 0},
        {"col": 3, "row": 0, "type": "curve_sw", "rotation_deg": 0},
        {"col": 3, "row": 1, "type": "straight_v", "rotation_deg": 0},
        {"col": 3, "row": 2, "type": "curve_nw", "rotation_deg": 0},
        {"col": 2, "row": 2, "type": "straight_h", "rotation_deg": 0},
        {"col": 1, "row": 2, "type": "straight_h", "rotation_deg": 0},
        {"col": 0, "row": 2, "type": "curve_ne", "rotation_deg": 0},
        {"col": 0, "row": 1, "type": "straight_v", "rotation_deg": 0}
    ],
    "start": {"col": 0, "row": 0, "heading_deg": 90},
    "line": {"width_px": 20, "color_hex": "#000000", "bg_color_hex": "#FFFFFF"}
}
```

### Controller Plugin Interface

The simulator loads firmware controller modules at runtime via `plugin.py`.
Because controllers implement `ControllerBase`, the simulator uses them
without modification.

```python
# simulator/plugin.py
import importlib

def load_controller(name: str, hal: SimHAL) -> ControllerBase:
    module = importlib.import_module(f"firmware.controllers.{name}")
    cls = getattr(module, name.title().replace("_", ""))
    return cls(hal)
```

The `PYTHONPATH` must include the `firmware/` directory when running the
simulator. This is the only setup required to dual-run firmware modules.

### 2D Visualization

Implemented in `visualization.py` using pygame. The main window contains:

* **Track viewport**: scrollable/zoomable 2D top-down view of the track
* **Robot overlay**: robot footprint drawn at current position/heading
* **Sensor overlay** (toggle): visual markers at each sensor sample point
* **Trail overlay** (toggle): path history drawn as a fading line

Frame rate target: 30 fps.

### Parameter Control Panel

`ui.py` implements a sidebar panel with:

* Controller selector dropdown (bang_bang, open_loop, pid, kalman, q_learning)
* Sliders for controller parameters matching those in `config.py`
* Physics parameter sliders (MAX_SPEED, WHEEL_BASE, noise σ)
* Buttons: Start, Stop, Reset, Load Track, Export Metrics

### Performance Metrics

`metrics.py` computes and records:

| Metric | Definition |
|:-------|:-----------|
| Path error (RMS) | RMS distance of robot center from line centerline (meters) |
| Lap time | Elapsed time for one complete loop of the track (seconds) |
| Oscillation count | Number of times robot crosses line centerline per lap |
| Off-track events | Number of times all sensors read < 0.1 (completely off line) |
| Max speed | Highest linear speed achieved during run (m/s) |

Metrics are logged to CSV and displayed live in the control panel.

---------------

## 7. Line Track Designer Specification {#s7}

> **Decision** (see [Appendix A][appendix-a]): The Line Track Designer is a
> **custom Python build** for Ubuntu. It targets 11" × 8.5" printable tiles and
> exports the track.json format consumed by the LFR Simulator.

### Tile Library

`tile_library.py` defines all tile types. Each tile is rendered as a vector
SVG path. The line path within each tile is parameterized so that line width
and color match the `track.json` settings at export time.

Tile types match the [Track Format][s6] tile type list exactly. The tile
library is the canonical source; both the Designer and the Simulator import from
it (or from the exported JSON, respectively).

Default tile size: **11" × 8.5"** (landscape orientation, US Letter).
Tiles are designed to have matching line endpoints at each edge so adjacent
tiles connect seamlessly when printed and placed on the floor.

### Interactive Canvas

`canvas.py` implements a pygame-based drag-and-drop grid editor.

* Grid size: up to 8 columns × 6 rows (configurable; default 4×3)
* Left-click empty cell → opens tile type picker
* Left-click placed tile → rotate 90° clockwise
* Right-click placed tile → remove tile (replace with blank)
* Keyboard: `R` rotate, `Del` remove, `Ctrl+Z` undo, `Ctrl+S` save

### Export

`export.py` provides two export functions:

1. **PDF export** (`export_pdf(layout, path)`):
    * One page per tile; each page = exactly 8.5" × 11"
    * Line rendered at configured width and color
    * Page number and tile coordinates printed in corner (for assembly guide)
    * Registration marks at tile corners for precise physical alignment
    * Uses `reportlab` library

2. **JSON export** (`export_json(layout, path)`):
    * Writes `track.json` per the schema defined in [Section 6][s6]
    * Validates schema before writing; raises `ValueError` on invalid layouts
    * Overwrites existing file if path exists

### Save / Load

`save_load.py` persists the designer layout (including grid size, tile
placements, and display settings) to a `.layout` JSON file. This is separate
from `track.json`; the `.layout` file is the designer's native format.

```json
{
    "version": "1.0",
    "grid": {"cols": 4, "rows": 3},
    "tiles": [{"col": 0, "row": 0, "type": "curve_se"}],
    "display": {"tile_px": 120, "line_width_px": 12}
}
```

---------------

## 8. Testing Strategy {#s8}

### Overview

Three tiers of testing, applied progressively:

```text
Tier 1: Unit Tests       → pure algorithm correctness; no hardware; fast
Tier 2: Simulation Tests → end-to-end behavior in simulator; repeatable
Tier 3: Hardware Tests   → physical validation on actual robot; pre-class
```

### Tier 1 — Unit Tests (`tests/unit/`)

Test individual modules with synthetic inputs. No HAL, no GPIO, no pygame.
Run with `pytest`. Target: 100% branch coverage on all controller modules.

| Module | Test Focus |
|:-------|:-----------|
| `bang_bang.py` | All 4 IR input combinations → correct motor output |
| `open_loop.py` | Speed error → correct correction output; gain boundary |
| `pid.py` | Step input → correct P/I/D contributions; integral clamp |
| `kalman.py` | Noisy input sequence → smoothed output closer to true signal |
| `q_learning.py` | Q-table update rule; greedy action selection; epsilon=0 inference |
| `reflectance_array.py` | Centroid calculation for known sensor arrays |
| `web_server.py` | `POST /config` → `config.py` updated correctly |
| `track.py` (sim) | Valid JSON → Track object; invalid JSON → ValueError |
| `export.py` (designer) | Known layout → valid track.json schema |

### Tier 2 — Simulation Tests (`tests/sim/`)

End-to-end: load a track, run a controller, measure metrics. Tests pass if
metrics meet threshold criteria.

| Test | Track | Controller | Pass Criteria |
|:-----|:------|:-----------|:--------------|
| `test_bang_bang_oval` | Simple oval | bang_bang | Completes 3 laps; RMS error < 0.05 m |
| `test_pid_oval` | Simple oval | pid | Completes 5 laps; RMS error < 0.02 m; oscillations < 10/lap |
| `test_pid_complex` | 4×3 with curves | pid | Completes 2 laps without off-track events |
| `test_kalman_noise` | Simple oval (σ=0.3) | kalman | RMS error < RMS error of pid alone (same noise level) |
| `test_qlearning_trained` | Simple oval | q_learning | Loads pre-trained Q-table; completes 3 laps |
| `test_qlearning_train` | Simple oval | q_learning (training) | Q-table converges in < 500 episodes |

### Tier 3 — Hardware Validation (`tests/hardware/`)

Not automated; instructor runs these checklists before each design session.
Results recorded in a logbook.

#### Per-Design-Session Readiness Checklist

##### DS1 — Course Kickoff

* [ ] MiOYOOW kit assembled and tested on a printed track
* [ ] MiOYOOW demo track printed (at least one full loop)
* [ ] Presentation slides ready for course overview

##### DS2 — Chassis Assembly

* [ ] All 6 Emo chassis kits received and counted
* [ ] Instructor assembled one chassis; assembly instructions validated
* [ ] Assembly guide prepared for students

##### DS3 — Hardware Integration

* [ ] All hardware items received (verify against BOM)
* [ ] Instructor's modified chassis assembled and powered on
* [ ] Battery circuit measured: correct voltage at Pico W VIN and 5V rail
* [ ] Pico W boots CircuitPython (REPL accessible over USB)

##### DS4 — Simple LFR

* [ ] CircuitPython installed on all 6 Pico Ws
* [ ] `bang_bang.py` unit tests passing (Tier 1)
* [ ] Instructor's robot completes 3+ laps on printed oval track
* [ ] Simulator running bang-bang controller on same track layout
* [ ] DS4 track printed and assembled on floor

##### DS5 — Sensor Upgrade

* [ ] All 6 QTRX-MD-08RC arrays received and tested (individual sensor readings verified)
* [ ] `reflectance_array.py` calibration procedure documented and tested
* [ ] Instructor's robot with reflectance array completes 3+ laps
* [ ] Simulator updated to 8-element sensor model
* [ ] `test_pid_oval` simulation test passing with reflectance array model

##### DS6 — WiFi Interface

* [ ] WiFi AP tested at Makersmiths (interference check with facility WiFi)
* [ ] Web UI loads on a phone/laptop connected to robot's SSID
* [ ] Speed control slider adjusts robot speed in real time
* [ ] All 6 robots have unique SSIDs (LFR-1 through LFR-6)

##### DS7 — Open-Loop Speed Control

* [ ] 12 speed sensor modules received and mounted (2 per robot)
* [ ] Speed sensor readings verified (pulses counted correctly at test speed)
* [ ] `open_loop.py` unit tests passing
* [ ] Instructor's robot demonstrates open-loop speed control on track

##### DS8 — PID Controller

* [ ] `pid.py` unit tests passing with reference step-response data
* [ ] Instructor's robot stable for 2+ laps with tuned PID gains
* [ ] PID gains tunable via WiFi UI (live adjustment, no reflash)
* [ ] Simulator `test_pid_oval` and `test_pid_complex` passing
* [ ] Ziegler-Nichols tuning walkthrough prepared as teaching exercise

##### DS9 — Kalman Filter

* [ ] `kalman.py` unit tests passing with synthetic noisy signal
* [ ] Kalman filter demonstrably reduces oscillation vs. PID alone on hardware
* [ ] Simulator `test_kalman_noise` passing
* [ ] Side-by-side Kalman vs. no-Kalman simulator demo prepared

##### DS10 — Advanced Control Theory

* [ ] Teaching materials for ADRC, MPC, RL prepared and reviewed
* [ ] Q-Learning concept explained with simulator demo (training visualization)
* [ ] `test_qlearning_train` simulation test passing (Q-table converges)

##### DS11 — Q-Learning Controller

* [ ] `q_learning.py` unit tests passing (inference mode, ε=0)
* [ ] Pre-trained Q-table (`q_table.json`) deployed to all 6 Pico Ws
* [ ] Instructor's robot completes 3+ laps using Q-Learning controller
* [ ] All robots cleaned, labeled, and packed for student take-home
* [ ] Course evaluation form prepared

---------------

## 9. Development Timeline {#s9}

The instructor is the sole developer. Timeline assumes ~10 hours/week.
All Tier 1 and Tier 2 tests must pass before month-end milestones.

### Month 1 — Foundation

**Goal**: All hardware in hand; environment set up; HAL + core firmware running.

| Week | Deliverable |
|:-----|:------------|
| 1 | Order all hardware components (BOM complete) |
| 1 | Set up monorepo, Python environment, pytest, markdownlint |
| 2 | `hal/base.py` — SensorHAL, MotorHAL, ControllerBase ABCs |
| 2 | `pico_hal.py` — GPIO-backed implementations |
| 3 | `config.py`, `main.py` skeleton |
| 3 | `sensors/ir_sensor.py` + unit tests |
| 4 | `motors/motor_controller.py` + manual test on hardware |
| 4 | DS2 + DS3 hardware readiness checklists complete |

**Milestone**: Instructor's robot powered on; IR sensor reads line via Pico W REPL.

### Month 2 — Bang-Bang LFR + Simulator v1

**Goal**: Working bang-bang LFR on hardware; simulator renders track and robot.

| Week | Deliverable |
|:-----|:------------|
| 5 | `controllers/bang_bang.py` + unit tests |
| 5 | `sim_hal.py` — simulator HAL stub |
| 6 | `simulator/physics.py`, `simulator/track.py` |
| 6 | `simulator/sensor_sim.py` (IR pair mode) |
| 7 | `simulator/visualization.py` (pygame rendering) |
| 7 | `simulator/ui.py` (basic controls) |
| 8 | DS4 hardware readiness checklist complete |
| 8 | `test_bang_bang_oval` simulation test passing |

**Milestone**: Bang-bang robot runs 3 laps on floor track; simulator matches behavior.

### Month 3 — Track Designer + Sensor Upgrade

**Goal**: Line Track Designer functional; reflectance array on hardware.

| Week | Deliverable |
|:-----|:------------|
| 9 | `track_designer/tile_library.py` + tile SVGs |
| 9 | `track_designer/canvas.py` (pygame editor) |
| 10 | `track_designer/export.py` (PDF + JSON) |
| 10 | `track_designer/save_load.py` |
| 11 | Test print run: full 4×3 oval track printed and assembled |
| 11 | `sensors/reflectance_array.py` + unit tests |
| 12 | Reflectance array on hardware; DS5 checklist complete |
| 12 | Simulator updated: 8-element sensor model |

**Milestone**: Custom track designed, printed, assembled; robot navigates with reflectance array.

### Month 4 — WiFi UI + Open-Loop + PID

**Goal**: WiFi UI running; open-loop and PID controllers validated.

| Week | Deliverable |
|:-----|:------------|
| 13 | `wifi/web_server.py` — AP mode + base speed UI |
| 13 | DS6 hardware checklist complete |
| 14 | `speed_sensor/speed_sensor.py` + unit tests |
| 14 | `controllers/open_loop.py` + unit tests |
| 15 | DS7 hardware checklist complete |
| 15 | `controllers/pid.py` + unit tests |
| 16 | `simulator/metrics.py` |
| 16 | `test_pid_oval`, `test_pid_complex` passing; DS8 checklist complete |

**Milestone**: PID-controlled robot navigates complex track; gains tunable via WiFi UI.

### Month 5 — Kalman Filter + Q-Learning

**Goal**: Kalman and Q-Learning controllers validated in simulator and hardware.

| Week | Deliverable |
|:-----|:------------|
| 17 | `controllers/kalman.py` + unit tests |
| 17 | `test_kalman_noise` passing |
| 18 | DS9 hardware checklist complete |
| 18 | Q-Learning state/action space finalized (see [Section 5][s5]) |
| 19 | `controllers/q_learning.py` — training mode |
| 19 | `test_qlearning_train` passing (Q-table converges) |
| 20 | `q_table.json` trained and serialized; inference mode unit tests passing |
| 20 | DS11 hardware checklist complete |

**Milestone**: Q-Learning robot navigates oval track with pre-trained Q-table.

### Month 6 — Integration & Dress Rehearsal

**Goal**: All 6 robots built and tested; full course run-through completed.

| Week | Deliverable |
|:-----|:------------|
| 21 | All 5 student robots built; per-robot hardware tests complete |
| 22 | Full Tier 1 + Tier 2 test suite passing (all controllers) |
| 22 | WiFi unique-SSID test with all 6 robots active simultaneously |
| 23 | Instructor dry-run of all 11 design sessions (abbreviated) |
| 23 | All course documents finalized (syllabus, lesson plans, BOM) |
| 24 | Buffer week: resolve any outstanding issues |
| 24 | Go/no-go checklist reviewed; course start approved |

**Milestone**: Pre-course dress rehearsal complete; all robots ready for first class.

---------------

## 10. Risk Assessment {#s10}

| Risk | Likelihood | Impact | Mitigation |
|:-----|:----------:|:------:|:-----------|
| Hardware shipping delays | Medium | High | Order all components in Month 1; buy spares for critical items |
| Robotics Motor Driver Board pinout undocumented | Low | High | Download board schematic in Month 1 before writing `pico_hal.py` |
| CircuitPython library unavailable for QTRX-MD-08RC | Low | High | Pre-validate library in Month 3 Week 11; fall back to raw GPIO bit-bang |
| Simulator physics diverges from hardware behavior | Medium | Medium | Tune physics model against hardware measurements in Month 2 |
| Q-Learning Q-table fails to converge in simulator | Medium | High | Simplify state/action space; use reward shaping; set hard episode limit |
| Q-table inference too slow on Pico W | Low | High | Profile inference time Month 5; if too slow, quantize Q-table to int8 |
| WiFi interference / SSID collision at Makersmiths | Medium | Medium | Pre-test at facility; assign fixed unique SSIDs; test with all 6 APs active |
| Track printing misalignment (tile edges don't match) | Low | Medium | Test print run Month 3; add registration marks to designer export |
| Student skill level lower than expected | High | Medium | Pair younger students with adults; provide step-by-step print-out for each DS |
| 2-hour class too short for planned DS content | Medium | Medium | Document each DS with a "minimum viable" subset that can be split across classes |
| `reportlab` PDF rendering quality insufficient | Low | Low | Evaluate in Month 3; fall back to `matplotlib` PDF backend or SVG-to-print |
| pygame unavailable on target Ubuntu version | Low | Low | Specify tested Ubuntu + pygame versions in setup guide; use `apt`/`pip` |

---------------

## Appendix A — Development Dialogue {#appendix-a}

This appendix preserves the original prompt that initiated this specification
and the full Q&A session that resolved the key architectural decisions.

### A.1 — Original Prompt (verbatim)

> Read @input/my-vision.md and create a specification document, reflecting the
> incrementally development in the Line Following Robot (LFR) course.
>
> I need this this specification document to help prepare me for delivery of
> the course in about 6 months. I want all the components implied bellow (both
> hardware and software) to be built and tested in advance of the course.
>
> I want the software to be built in a modular form, such that, a software
> subsystem in step N can be pulled out a replaced with a new subsystem in
> step N+1 (e.g. PID Controller replaced with Q-Learning Controller)
>
> Make sure you include the Line Track Designer and LFR Simulators software in
> this specification document. Think harder about the software architecture and
> testing of the of this project.
>
> Within the specification document you create (to be called "specification.md"),
> include this prompt, all question you ask me, along with my responses. Place
> this in an appendix and reference it at the beginning of the development plan
> and anywhere else in the text when its a useful reference.
>
> Use the AskUserQuestions tool for all things that require further clarification.

### A.2 — Q&A: Line Track Designer

**Question**: For the Line Track Designer — build custom Python tool, adapt the
existing Quentin18/Line-Track-Designer GitHub project, or use the existing
online tool as-is (no dev work)?

* Option A: **Build custom** — Full control; fits exact tile size (11"×8.5");
    tightly integrated with track.json format. More development time. *(Recommended)*
* Option B: Adapt existing (GitHub project)
* Option C: Use existing online tool as-is

**Answer**: **Build custom (Option A)**

**Rationale recorded**: Custom build gives full control over tile dimensions,
export format (track.json), and PDF output layout. The tile size (11"×8.5") and
the shared track.json format with the simulator are specific enough that adapting
an existing tool would likely require as much effort as building from scratch.

### A.3 — Q&A: LFR Simulator

**Question**: For the LFR Simulator — build custom Python tool (tightly integrated
with firmware modules) or adapt one of the three referenced GitHub simulators?

* Option A: **Build custom** — Tight integration with firmware HAL; firmware
    controller modules run inside simulator without modification; can demo PID
    tuning, sensor arrays, Q-Learning training. More development time. *(Recommended)*
* Option B: Adapt existing (one of the referenced GitHub simulators)

**Answer**: **Build custom (Option A)**

**Rationale recorded**: The simulator-first testing strategy requires that firmware
controller modules (`bang_bang.py`, `pid.py`, etc.) run identically inside the
simulator and on the Pico W. This requires the shared HAL abstraction and plugin
interface — a level of integration that existing simulators do not provide.

### A.4 — Q&A: Testing Strategy

**Question**: Primary testing strategy for firmware (CircuitPython on Pico W) —
where does most development and iteration happen?

* Option A: **Simulator-first** — Develop and test control algorithms on desktop
    simulator before deploying to hardware. Hardware is the final validation
    step. *(Recommended)*
* Option B: Hardware-only — All testing on physical robot
* Option C: Parallel — Develop simultaneously on both platforms

**Answer**: **Simulator-first (Option A)**

**Rationale recorded**: Hardware availability is limited to one instructor robot
during development. The simulator enables rapid algorithm iteration (no reflash
cycle), repeatable test conditions, and visual demonstrations for class. Hardware
validation confirms simulator results but is not the development environment.

---------------

[s1]: #s1
[s2]: #s2
[s3]: #s3
[s4]: #s4
[s5]: #s5
[s6]: #s6
[s7]: #s7
[s8]: #s8
[s9]: #s9
[s10]: #s10
[appendix-a]: #appendix-a

[mioyoow]: https://www.amazon.com/MiOYOOW-Soldering-Electronics-Following-Competition/dp/B07ZH4XLQ3?th=1
[emo-chassis]: https://www.amazon.com/gp/product/B01LXY7CM3/ref=ewc_pr_img_1
[battery-holder]: https://www.amazon.com/Thicken-Battery-Holder-Standard-Connector/dp/B07WP1CYYW?th=1
[motor-driver]: https://www.pishop.us/product/robotics-board-for-raspberry-pi-pico/
[ir-pair]: https://www.amazon.com/Infrared-Avoidance-Transmitting-Receiving-Photoelectric/dp/B07PFCC76N?th=1
[pico-w]: https://www.amazon.com/Raspberry-Pi-Pico-Wireless-Bluetooth/dp/B0B5H17CMK
[qtrx]: https://www.pololu.com/product/4348
[breadboard]: https://www.amazon.com/DEYUE-breadboard-Set-Prototype-Board/dp/B07LFD4LT6
[buck-converter]: https://www.amazon.com/dp/B0F1WB3LJ5?th=1
[speed-sensor]: https://www.amazon.com/DAOKAI-Comparator-Measuring-Optocoupler-Detection/dp/B0B2NSQJDL
