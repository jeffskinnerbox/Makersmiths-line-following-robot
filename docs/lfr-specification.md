# LFR Course — System Specification

* **Organization:** [Makersmiths][L01] — a community [makerspace][L02] in Leesburg, Virginia
* **Course:** Evolving Design of a Line Following Robot
* **Start Date:** June 15, 2026
* **Author:** Course instructor (volunteer)
* **Purpose:** Defines all hardware configurations, software systems, module interfaces, and test criteria that must be built and validated before the course begins
* **Reference:** See [Appendix A](#appendix-a-specification-development-prompt--qa) for the original specification prompt and all instructor Q&A that shaped this document

## Related Documents

| Document | File | Relationship |
|:---------|:-----|:-------------|
| Course Syllabus | `docs/lfr-syllabus.md` | Defines learning objectives, class schedule, and course structure |
| Lesson Plan | `docs/lfr-lesson-plan.md` | Detailed per-class teaching guide referencing this spec's modules |
| Bill of Materials | `input/my-bom.md` | Single source of truth for costs, quantities, and sourcing |
| Development Plan | `docs/development-plan.md` | Phased build schedule derived from this spec (to be created) |
| Instructor Vision | `input/my-vision.md` | Original course vision and Design Session sequence |

> **Convention:** This spec defines *what* must be built and *how it must behave*. The development plan defines *when* and *in what order* to build it. The BOM defines *what to buy and where*. Cost/pricing/sourcing information belongs exclusively in the BOM.

---

## Table of Contents

* [1. System Overview](#1-system-overview)
* [2. Hardware Specification](#2-hardware-specification)
  * [2.1 Platform Components](#21-platform-components)
  * [2.2 Kitronik Robotics Board Architecture](#22-kitronik-robotics-board-architecture)
  * [2.3 GPIO Pin Allocation](#23-gpio-pin-allocation)
  * [2.4 Power Architecture](#24-power-architecture)
  * [2.5 Hardware Configuration by Design Session](#25-hardware-configuration-by-design-session)
* [3. LFR Firmware Specification](#3-lfr-firmware-specification)
  * [3.1 Architecture Overview](#31-architecture-overview)
  * [3.2 Directory Structure](#32-directory-structure)
  * [3.3 Module Interface Contracts](#33-module-interface-contracts)
  * [3.4 Sensor Modules](#34-sensor-modules)
  * [3.5 Controller Modules](#35-controller-modules)
  * [3.6 Motor Driver Module](#36-motor-driver-module)
  * [3.7 WiFi Access Point & Web Server](#37-wifi-access-point--web-server)
  * [3.8 Main Control Loop](#38-main-control-loop)
  * [3.9 Firmware Configuration](#39-firmware-configuration)
  * [3.10 Firmware by Design Session](#310-firmware-by-design-session)
  * [3.11 CircuitPython Dependencies](#311-circuitpython-dependencies)
* [4. Line Track Designer Specification](#4-line-track-designer-specification)
  * [4.1 Overview](#41-overview)
  * [4.2 Track Definition Format](#42-track-definition-format)
  * [4.3 Tile Types](#43-tile-types)
  * [4.4 Rendering & PDF Generation](#44-rendering--pdf-generation)
  * [4.5 CLI Interface](#45-cli-interface)
  * [4.6 Course Track Designs](#46-course-track-designs)
  * [4.7 Dependencies](#47-dependencies)
* [5. LFR Simulator Specification](#5-lfr-simulator-specification)
  * [5.1 Overview](#51-overview)
  * [5.2 Physics Model](#52-physics-model)
  * [5.3 Sensor Simulation](#53-sensor-simulation)
  * [5.4 Controller Integration](#54-controller-integration)
  * [5.5 Track Loading](#55-track-loading)
  * [5.6 Visualization & UI](#56-visualization--ui)
  * [5.7 Dependencies](#57-dependencies)
* [6. WiFi Browser User Interface Specification](#6-wifi-browser-user-interface-specification)
  * [6.1 Network Architecture](#61-network-architecture)
  * [6.2 UI Pages & Controls](#62-ui-pages--controls)
  * [6.3 API Endpoints](#63-api-endpoints)
* [7. Testing Strategy](#7-testing-strategy)
  * [7.1 Firmware Testing](#71-firmware-testing)
  * [7.2 Line Track Designer Testing](#72-line-track-designer-testing)
  * [7.3 LFR Simulator Testing](#73-lfr-simulator-testing)
  * [7.4 Hardware Integration Testing](#74-hardware-integration-testing)
  * [7.5 Test-Gate Definitions by Design Session](#75-test-gate-definitions-by-design-session)
* [8. Software Dependencies Summary](#8-software-dependencies-summary)
* [9. Unresolved Questions & Risks](#9-unresolved-questions--risks)
* [Appendix A: Specification Development Prompt & Q&A](#appendix-a-specification-development-prompt--qa)

---

## 1. System Overview

Three software systems must be built and tested before the course begins on June 15, 2026. All three are developed by the instructor on Ubuntu.

| System | Language | Runs On | Purpose |
|:-------|:---------|:--------|:--------|
| **LFR Firmware** | CircuitPython 10.1.4 | Raspberry Pi Pico W | Robot control software — evolves across 13 Design Sessions via modular, swappable subsystems |
| **Line Track Designer** | Python 3 | Ubuntu (CLI) | Generates printable PDF tile sheets (8.5 × 11 in) for floor-based test tracks |
| **LFR Simulator** | Python 3 + Pygame | Ubuntu (GUI) | 2D visual simulation for instructor demos — PID tuning, sensor comparison, Q-Learning training |

### Design Principle: Modular Swappability

The LFR firmware is structured so that a subsystem at Design Session N can be removed and replaced with a new subsystem at Design Session N+1 without modifying other modules. For example:

* **Sensor swap:** IR Emitter/Phototransistor Pair (DS3–DS5) → QTRX-MD-08RC Reflectance Sensor Array (DS6+)
* **Controller swap:** Bang-Bang (DS4–DS5) → Proportional (DS6–DS9) → PID (DS10) → Kalman+PID (DS11) → Q-Learning (DS12)

This is achieved through abstract base classes that define a common interface. Each concrete module implements that interface. The main control loop depends only on the interface, never on a specific implementation.

### Design Session to Class Mapping

For reference, Design Sessions map to classes per the syllabus (see [Appendix A, Q1](#appendix-a-specification-development-prompt--qa)):

| Class | Design Sessions | Focus |
|:------|:---------------|:------|
| 1 | DS1 + DS2 | MiOYOOW demo, chassis assembly |
| 2 | DS3 | Hardware install, CircuitPython flash, motor test |
| 3 | DS4 + DS5 | First line follower, testing |
| 4 | DS6 | Sensor array upgrade |
| 5 | DS7 | Variable speed, proportional control |
| 6 | DS8 | WiFi AP + browser UI |
| 7 | DS9 | Speed sensors, closed-loop feedback, control theory intro |
| 8 | DS10 | PID controller |
| 9* | DS11 | Kalman filter |
| 10* | DS12 + DS13 | Q-Learning, course wrap-up |

*Classes 9–10 are stretch classes.

---

## 2. Hardware Specification

### 2.1 Platform Components

Each LFR unit (6 total: 5 student + 1 instructor) contains these components. See the BOM (`input/my-bom.md`) for costs and sourcing.

| Component | Model | When Added | When Removed |
|:----------|:------|:-----------|:-------------|
| Car chassis | Emo Smart Robot Car Chassis Kit | DS2 (Class 1) | Never |
| Battery holder | 8 × AA Battery Holder (12V) | DS3 (Class 2) | Never |
| Battery clip | 9V Battery Clip Connector | DS3 (Class 2) | Never |
| Buck converter | 5V Buck Converter Module | DS3 (Class 2) | Never |
| Microcontroller | Raspberry Pi Pico W | DS3 (Class 2) | Never |
| Motor driver | Kitronik Robotics Board for Pico (5329) | DS3 (Class 2) | Never |
| Breadboard | 400 Pin Solderless Prototype Board | DS3 (Class 2) | Never |
| Initial sensors | IR Emitter/Phototransistor Pair | DS3 (Class 2) | DS6 (Class 4) — replaced by QTRX |
| Sensor array | QTRX-MD-08RC Reflectance Sensor Array | DS6 (Class 4) | Never |
| Speed sensors | Speed Sensor Module (×2) | DS9 (Class 7) | Never |

### 2.2 Kitronik Robotics Board Architecture

The Kitronik Robotics Board for Raspberry Pi Pico (model 5329) is the motor driver platform. Key characteristics:

* **Motor control via I2C:** The board uses a **PCA9685PW** 16-channel 12-bit PWM driver IC. All motor and servo signals are generated by the PCA9685, not by Pico GPIO pins directly.
* **I2C address:** `0x6C` (default). Configurable to `0x6D`, `0x6E`, or `0x6F` via solder bridges.
* **I2C bus:** Uses Pico **GP8** (SDA) and **GP9** (SCL) on the I2C0 bus.
* **H-bridge drivers:** Two dual H-bridge motor driver ICs (likely DRV8833) handle power switching to the motors. The PCA9685 PWM outputs feed the H-bridge inputs.
* **Motor channels:** 4 DC motor outputs. This project uses Motor 1 (left wheel) and Motor 2 (right wheel).
* **Servo channels:** 8 servo outputs (not used in this course).
* **GPIO freedom:** Since the board only consumes GP8 and GP9, **all other 26 GPIO pins remain available** for sensors and expansion.
* **Official library:** Kitronik provides a CircuitPython library at `github.com/KitronikLtd/Kitronik-Pico-Robotics-Board-CircuitPython` — evaluate for use or adapt.
* **Speed control:** PWM duty cycle 0–100% maps to PCA9685 counts 0–4095. Direction is set by which of two PCA9685 channels per motor receives the PWM signal (forward vs. reverse).

> **VERIFY:** The H-bridge IC is likely DRV8833 based on cross-referencing with the Kitronik 5331 Motor Driver Board. Confirm by inspecting the physical board or requesting the official schematic from Kitronik.

### 2.3 GPIO Pin Allocation

The Raspberry Pi Pico W has 26 GPIO pins (GP0–GP22, GP26–GP28). The allocation below reserves pins for all Design Sessions. Pins are assigned to minimize wiring changes between sessions.

| GPIO Pin | Function | Design Sessions | Notes |
|:---------|:---------|:---------------|:------|
| GP0 | QTRX sensor 1 | DS6+ | Digital I/O (RC timing) |
| GP1 | QTRX sensor 2 | DS6+ | Digital I/O (RC timing) |
| GP2 | IR pair: left sensor *or* QTRX sensor 3 | DS3–DS5 (IR), DS6+ (QTRX) | Reused after IR pair removed |
| GP3 | IR pair: right sensor *or* QTRX sensor 4 | DS3–DS5 (IR), DS6+ (QTRX) | Reused after IR pair removed |
| GP4 | QTRX sensor 5 | DS6+ | Digital I/O (RC timing) |
| GP5 | QTRX sensor 6 | DS6+ | Digital I/O (RC timing) |
| GP6 | QTRX sensor 7 | DS6+ | Digital I/O (RC timing) |
| GP7 | QTRX sensor 8 | DS6+ | Digital I/O (RC timing) |
| **GP8** | **I2C0 SDA** | **All** | **Kitronik board (PCA9685) — do not reassign** |
| **GP9** | **I2C0 SCL** | **All** | **Kitronik board (PCA9685) — do not reassign** |
| GP10 | QTRX CTRL (LED enable) | DS6+ | Digital output — controls IR LED emitters on QTRX |
| GP11 | Speed sensor: left wheel | DS9+ | Digital input, edge counting |
| GP12 | Speed sensor: right wheel | DS9+ | Digital input, edge counting |
| GP13–GP22 | **Available** | — | Reserved for future expansion or optional hardware |
| GP26 (ADC0) | **Available** | — | Analog-capable; could be used for battery voltage monitoring |
| GP27 (ADC1) | **Available** | — | Analog-capable |
| GP28 (ADC2) | **Available** | — | Analog-capable |

> **VERIFY at first build:** Confirm that the QTRX-MD-08RC RC timing reads work reliably on GP0–GP7 at the control loop rate. Timing-sensitive reads may need specific pin ordering or PIO-based reads if software timing is insufficient.

### 2.4 Power Architecture

```text
9V Battery Clip Connector (9V nominal)
    └──► Kitronik Robotics Board power input (3.0–10.8V) ✓ within spec
            ├──► On-board 3.3V regulator → Pico W (3.3V logic power)
            └──► DRV8833 H-bridges → DC motors (motor voltage = 9V)

8×AA Battery Holder (12V nominal)
    └──► 5V Buck Converter Module
            └──► Breadboard 5V rail → QTRX-MD-08RC VCC, Speed Sensor VCC
```

> **Note:** The 9V battery powers the Kitronik board directly (9V is within the 3.0–10.8V rated range).
> The 8×AA holder (12V) powers the 5V buck converter for sensors — it does NOT connect to the Kitronik board.
> This avoids the 12V-exceeds-10.8V-max issue entirely.

### 2.5 Hardware Configuration by Design Session

Each row shows what is physically installed on the robot at that Design Session.

| DS | Chassis | MCU + Motor Board | Sensors | Speed Sensors | WiFi | Battery |
|:---|:--------|:-----------------|:--------|:-------------|:-----|:--------|
| DS1 | — | — | — | — | — | — *(MiOYOOW demo only)* |
| DS2 | Emo chassis | — | — | — | — | — |
| DS3 | Emo chassis | Pico W + Kitronik | IR pair (2 sensors) | — | — | 9V clip + 8×AA + buck converter |
| DS4–DS5 | Emo chassis | Pico W + Kitronik | IR pair (2 sensors) | — | — | 9V clip + 8×AA + buck converter |
| DS6 | Emo chassis | Pico W + Kitronik | **QTRX-MD-08RC (8 sensors)** | — | — | 9V clip + 8×AA + buck converter |
| DS7 | Emo chassis | Pico W + Kitronik | QTRX-MD-08RC | — | — | 9V clip + 8×AA + buck converter |
| DS8 | Emo chassis | Pico W + Kitronik | QTRX-MD-08RC | — | **WiFi AP active** | 9V clip + 8×AA + buck converter |
| DS9 | Emo chassis | Pico W + Kitronik | QTRX-MD-08RC | **2× speed sensors** | WiFi AP active | 9V clip + 8×AA + buck converter |
| DS10–DS12 | Emo chassis | Pico W + Kitronik | QTRX-MD-08RC | 2× speed sensors | WiFi AP active | 9V clip + 8×AA + buck converter |

---

## 3. LFR Firmware Specification

### 3.1 Architecture Overview

The firmware uses a **plugin module architecture**. A central `main.py` imports concrete modules through a configuration mechanism. All sensor, controller, and motor modules implement abstract base classes, allowing any implementation to be swapped without changing the main loop or other modules.

```text
main.py                         ← Cooperative polling main loop
├── config.py                   ← Selects which modules to load
├── sensors/
│   ├── base.py                 ← Abstract LineSensor interface
│   ├── ir_pair.py              ← DS3–DS5: Two IR sensors
│   └── qtrx_array.py           ← DS6+: 8-channel reflectance array
├── controllers/
│   ├── base.py                 ← Abstract Controller interface
│   ├── bang_bang.py             ← DS4–DS5: Simple on/off steering
│   ├── proportional.py         ← DS6–DS9: Speed scales with error
│   ├── pid.py                  ← DS10: Full PID control
│   ├── kalman_pid.py           ← DS11: PID with Kalman-filtered sensor input
│   └── qlearning.py            ← DS12: Q-table reinforcement learning
├── motors/
│   ├── base.py                 ← Abstract MotorDriver interface
│   └── kitronik.py             ← Kitronik Robotics Board via I2C/PCA9685
├── speed/
│   ├── base.py                 ← Abstract SpeedSensor interface
│   └── optocoupler.py          ← DS9+: IR optocoupler wheel speed sensors
├── network/
│   ├── wifi_ap.py              ← WiFi access point setup (DS8+)
│   ├── web_server.py           ← Minimal HTTP server (cooperative, non-blocking)
│   └── ui_pages.py             ← HTML templates for browser UI
└── lib/
    └── kitronik_motor_board.py ← Kitronik official or adapted I2C driver
```

### 3.2 Directory Structure

On the Pico W filesystem (CIRCUITPY drive):

```text
CIRCUITPY/
├── main.py                 ← Entry point (auto-run by CircuitPython)
├── config.py               ← Module selection and parameters
├── sensors/
│   ├── base.py
│   ├── ir_pair.py
│   └── qtrx_array.py
├── controllers/
│   ├── base.py
│   ├── bang_bang.py
│   ├── proportional.py
│   ├── pid.py
│   ├── kalman_pid.py
│   └── qlearning.py
├── motors/
│   ├── base.py
│   └── kitronik.py
├── speed/
│   ├── base.py
│   └── optocoupler.py
├── network/
│   ├── wifi_ap.py
│   ├── web_server.py
│   └── ui_pages.py
└── lib/
    ├── kitronik_motor_board.py
    └── adafruit_*.mpy          ← Any required Adafruit CircuitPython libraries
```

> **Flash/RAM constraint:** The Pico W has 2 MB flash and 264 KB RAM. CircuitPython and its VM consume a significant portion.
> Only the modules needed for the current Design Session should be loaded.
> Unused modules can remain on the filesystem but should not be imported.
> Monitor free memory with `gc.mem_free()` during development.

### 3.3 Module Interface Contracts

#### LineSensor Interface (`sensors/base.py`)

```python
class LineSensor:
    """Abstract base class for all line sensor modules."""

    @property
    def num_sensors(self) -> int:
        """Number of individual sensor elements."""
        ...

    def calibrate(self) -> None:
        """Run calibration routine (drive over black and white surfaces).
        Stores min/max values per sensor for normalization."""
        ...

    def read_raw(self) -> list[int]:
        """Return raw sensor readings as a list of integers.
        Length == num_sensors. Higher value = more reflective (white)."""
        ...

    def read_position(self) -> float:
        """Return estimated line position as a float.
        Range: -1.0 (line fully left) to +1.0 (line fully right).
        0.0 = line centered under sensor array.
        Returns last known position if line is lost (for recovery)."""
        ...

    def line_detected(self) -> bool:
        """Return True if at least one sensor currently detects the line."""
        ...
```

#### Controller Interface (`controllers/base.py`)

```python
class Controller:
    """Abstract base class for all control algorithm modules."""

    def update(self, position: float, dt: float) -> tuple[float, float]:
        """Given the current line position and time delta, compute motor speeds.
        Args:
            position: Line position from LineSensor.read_position() (-1.0 to +1.0)
            dt: Time elapsed since last update, in seconds
        Returns:
            (left_speed, right_speed): Motor speeds, each -1.0 to +1.0
            Positive = forward, negative = reverse, 0.0 = stop
        """
        ...

    def reset(self) -> None:
        """Reset internal state (integral accumulator, Q-table episode, etc.)."""
        ...

    def get_params(self) -> dict:
        """Return current tunable parameters as a dict.
        Example: {'kp': 1.0, 'ki': 0.0, 'kd': 0.5, 'base_speed': 0.4}"""
        ...

    def set_params(self, params: dict) -> None:
        """Update tunable parameters from a dict (e.g., from browser UI)."""
        ...

    @property
    def param_definitions(self) -> list[dict]:
        """Return metadata about tunable parameters for the browser UI.
        Each dict: {'name': str, 'label': str, 'min': float, 'max': float, 'step': float, 'default': float}"""
        ...
```

#### MotorDriver Interface (`motors/base.py`)

```python
class MotorDriver:
    """Abstract base class for motor driver modules."""

    def set_speeds(self, left: float, right: float) -> None:
        """Set motor speeds. Range: -1.0 (full reverse) to +1.0 (full forward)."""
        ...

    def stop(self) -> None:
        """Immediately stop both motors (set speed to 0, not coast)."""
        ...
```

#### SpeedSensor Interface (`speed/base.py`)

```python
class SpeedSensor:
    """Abstract base class for wheel speed sensor modules."""

    def read_rpm(self) -> tuple[float, float]:
        """Return (left_rpm, right_rpm) — wheel rotations per minute.
        Returns 0.0 for a wheel that is stationary."""
        ...

    def read_speed(self) -> tuple[float, float]:
        """Return (left_speed, right_speed) in approximate cm/s.
        Requires wheel circumference calibration."""
        ...

    def reset_counters(self) -> None:
        """Reset edge counters (call when starting a new measurement period)."""
        ...
```

### 3.4 Sensor Modules

#### 3.4.1 IR Emitter/Phototransistor Pair — `sensors/ir_pair.py`

**Used in:** DS3–DS5 (Classes 2–3)
**Replaces:** Nothing (first sensor)
**Replaced by:** QTRX-MD-08RC at DS6

**Behavior:**
* 2 sensors: left (GP2), right (GP3)
* Digital read: line detected (low reflectance) or no line (high reflectance)
* `read_position()` returns: −1.0 (left only), +1.0 (right only), 0.0 (both or neither)
* `num_sensors` = 2
* `calibrate()` sets a threshold between line and background readings

**Implementation notes:**
* The IR pair module uses `digitalio` for reading sensor state
* Threshold-based: each sensor returns binary (on-line / off-line)
* `read_raw()` returns `[left_value, right_value]` where values are 0 (line) or 1 (no line)

#### 3.4.2 QTRX-MD-08RC Reflectance Sensor Array — `sensors/qtrx_array.py`

**Used in:** DS6+ (Class 4 onward)
**Replaces:** IR pair

**Behavior:**
* 8 sensors on GP0–GP7, LED control on GP10
* RC timing-based reads: drive pin high, then measure time to discharge (proportional to reflectance)
* `read_position()` returns weighted average of sensor positions: −1.0 to +1.0
* `num_sensors` = 8
* `calibrate()` drives robot over line and background, records min/max timing per sensor

**Implementation notes:**
* RC timing read sequence for each sensor:
  1. Set pin to output, drive high
  2. Wait 10 µs (charge capacitor)
  3. Set pin to input (high-impedance)
  4. Measure time until pin goes low (discharge time)
  5. Shorter time = more reflective (white), longer time = less reflective (black)
* Read all 8 sensors in sequence; total read time ~2–5 ms depending on surface
* CTRL pin (GP10): set high to enable IR LEDs during reading, low to disable (saves power, avoids ambient interference)
* Position calculation: weighted average — `position = Σ(sensor_value × sensor_index) / Σ(sensor_value)`, normalized to −1.0…+1.0
* **Line-lost memory:** When no sensor detects the line, return the last known position with a flag indicating the line is lost. This allows the controller to steer toward the last known direction.

> **VERIFY:** Measure actual RC timing values on black line vs. white paper with the 5V Buck Converter powering the QTRX VCC. Timing values vary with supply voltage and LED current. Calibration routine must handle this.

#### 3.4.3 Speed Sensor Module — `speed/optocoupler.py`

**Used in:** DS9+ (Class 7 onward)
**New addition** (not replacing anything)

**Behavior:**
* 2 sensors: left wheel (GP11), right wheel (GP12)
* Each sensor is an IR optocoupler with a slotted encoder disc attached to the wheel or motor shaft
* Digital output: pulses as slots pass through the sensor
* `read_rpm()` counts edges per time window and converts to RPM
* `read_speed()` converts RPM to cm/s using wheel circumference

**Implementation notes:**
* Use `countio.Counter` (CircuitPython) or manual edge counting via polling in the main loop
* The encoder disc slot count must be measured from the physical hardware — typical: 20 slots/revolution
* RPM = (edge_count / slots_per_revolution) / time_window_seconds × 60
* Speed (cm/s) = RPM × wheel_circumference_cm / 60
* Wheel circumference: measure from the Emo chassis wheels (approximately 20–21 cm; **VERIFY**)

> **VERIFY:** Determine whether `countio.Counter` is available and reliable in CircuitPython 10.1.4 on the Pico W. If not, fall back to polling-based edge counting in the main loop (less accurate at high speeds).

### 3.5 Controller Modules

All controllers implement the `Controller` interface from §3.3. Each is designed to be a drop-in replacement.

#### 3.5.1 Bang-Bang Controller — `controllers/bang_bang.py`

**Used in:** DS4–DS5 (Class 3)
**Purpose:** Mimics the MiOYOOW kit's behavior — simple on/off steering

**Algorithm:**
* If `position < 0` (line is to the left): turn left (slow/stop left motor, run right motor)
* If `position > 0` (line is to the right): turn right (run left motor, slow/stop right motor)
* If `position ≈ 0` (centered): both motors forward at base speed

**Tunable parameters:**
* `base_speed` (0.0–1.0): Forward speed when centered. Default: 0.3
* `turn_speed` (0.0–1.0): Inner wheel speed during turn. Default: 0.0 (full stop)

#### 3.5.2 Proportional Controller — `controllers/proportional.py`

**Used in:** DS6–DS9 (Classes 4–7)
**Replaces:** Bang-Bang
**Purpose:** Smoother steering with speed proportional to error magnitude

**Algorithm:**
* `error = position` (already −1.0 to +1.0)
* `left_speed = base_speed + kp × error`
* `right_speed = base_speed - kp × error`
* Clamp both speeds to −1.0…+1.0

**Tunable parameters:**
* `base_speed` (0.0–1.0): Default: 0.4
* `kp` (0.0–5.0): Proportional gain. Default: 1.0

#### 3.5.3 PID Controller — `controllers/pid.py`

**Used in:** DS10 (Class 8)
**Replaces:** Proportional
**Purpose:** Full PID control for precise, smooth line following

**Algorithm:**
* `error = position`
* `integral += error × dt` (clamped to prevent windup)
* `derivative = (error - prev_error) / dt`
* `correction = kp × error + ki × integral + kd × derivative`
* `left_speed = base_speed + correction`
* `right_speed = base_speed - correction`

**Tunable parameters:**
* `kp` (0.0–10.0): Proportional gain. Default: 1.5
* `ki` (0.0–5.0): Integral gain. Default: 0.0
* `kd` (0.0–10.0): Derivative gain. Default: 0.5
* `base_speed` (0.0–1.0): Default: 0.5
* `integral_limit` (0.0–100.0): Anti-windup clamp. Default: 50.0

**Teaching notes:** Students tune by starting with P only (ki=0, kd=0), adding D to reduce oscillation,
then I if there is steady-state offset. The WiFi browser UI provides real-time sliders for all parameters.
The Ziegler-Nichols method can be used as a systematic alternative
— increase kp until oscillation, then compute ki and kd from the critical gain and oscillation period.

#### 3.5.4 Kalman+PID Controller — `controllers/kalman_pid.py`

**Used in:** DS11 (Class 9*)
**Replaces:** PID
**Purpose:** Kalman filter preprocessing of sensor data fed into PID controller

**Architecture:**
* Simplified 1D Kalman filter applied to the `position` value before PID processing
* **State:** estimated position
* **Prediction:** position doesn't change much between reads (constant model)
* **Update:** blend prediction with new sensor reading based on noise parameters

**Algorithm (Kalman filter step):**
1. **Predict:** `predicted_position = last_estimate` (constant velocity model optional)
2. **Predict covariance:** `predicted_P = last_P + process_noise_Q`
3. **Update gain:** `K = predicted_P / (predicted_P + measurement_noise_R)`
4. **Update estimate:** `estimate = predicted_position + K × (measured_position - predicted_position)`
5. **Update covariance:** `P = (1 - K) × predicted_P`
6. Feed `estimate` into the PID algorithm from §3.5.3

**Tunable parameters:** All PID parameters (§3.5.3) plus:
* `process_noise_Q` (0.001–1.0): How much the position is expected to change between reads. Default: 0.1
* `measurement_noise_R` (0.001–1.0): How noisy the sensor reading is. Default: 0.3

**Teaching notes:** Mental model — the Kalman filter is a "smart average" that trusts the prediction more when the sensor is noisy, and trusts the sensor more when the prediction is uncertain. Demonstrate before/after by toggling the filter on/off during a run.

#### 3.5.5 Q-Learning Controller — `controllers/qlearning.py`

**Used in:** DS12 (Class 10*)
**Replaces:** Kalman+PID
**Purpose:** Robot learns a line-following policy through trial and error

**Architecture:**
* **States:** Discretized sensor position. Divide the −1.0 to +1.0 range into N bins (e.g., 11 bins: `[-1.0, -0.8, ..., 0.8, 1.0]`)
* **Actions:** Discrete motor speed pairs. E.g., 5 actions: `[hard_left, soft_left, straight, soft_right, hard_right]`
* **Q-Table:** 2D array `[num_states × num_actions]`, initialized to zeros
* **Reward:** +1.0 for centered (|position| < 0.1), −0.5 for off-center, −2.0 for line lost
* **Mode:** Training mode (explores with ε-greedy policy) and Run mode (exploits learned Q-table)

**Algorithm (per control loop iteration in training mode):**
1. Read current state `s` (discretized position)
2. Choose action `a` (ε-greedy: random with probability ε, best Q-value otherwise)
3. Execute action (set motor speeds)
4. Observe next state `s'` and reward `r`
5. Update: `Q[s][a] = Q[s][a] + α × (r + γ × max(Q[s']) - Q[s][a])`

**Tunable parameters:**
* `learning_rate_alpha` (0.01–1.0): Default: 0.1
* `discount_factor_gamma` (0.0–1.0): Default: 0.95
* `exploration_epsilon` (0.0–1.0): Default: 0.3 (training), 0.0 (run mode)
* `num_states` (5–21): Default: 11
* `base_speed` (0.0–1.0): Default: 0.3

**Training on physical robot:**
* Training happens on the physical track — multiple laps with decreasing ε
* Q-table is saved to filesystem (`q_table.json`) and persists across power cycles
* Browser UI shows: current state, chosen action, Q-table heatmap (simple text representation), episode reward

**Training in simulator (independent):**
* The simulator (§5) has its own Q-Learning implementation using the same state/action/reward scheme
* Used for instructor demos, not transferred to the physical robot
* Allows showing many training episodes quickly (fast simulation speed)

### 3.6 Motor Driver Module

#### Kitronik Motor Driver — `motors/kitronik.py`

**Used in:** DS3+ (all sessions with the Pico W)

**Behavior:**
* Communicates with the PCA9685 on the Kitronik board via I2C (GP8/GP9, address `0x6C`)
* `set_speeds(left, right)`: Converts −1.0…+1.0 float to PCA9685 PWM duty cycle (0–4095 counts)
* Positive speed → forward PWM channel active; negative → reverse channel active
* `stop()`: Sets all motor PWM to 0 immediately

**Implementation notes:**
* Use the Kitronik official CircuitPython library or adapt its PCA9685 register writes
* Motor 1 = left wheel, Motor 2 = right wheel (verify physical wiring at first build)
* Initialize PCA9685 at 50 Hz (default), or potentially higher for smoother motor control (**VERIFY** if 100–200 Hz is supported and beneficial)
* Include a deadband: speeds below ±0.05 are treated as 0 to prevent motor whine at very low duty cycles

### 3.7 WiFi Access Point & Web Server

**Used in:** DS8+ (Class 6 onward)

#### WiFi Access Point — `network/wifi_ap.py`

* Pico W creates a WiFi AP using `wifi.radio.start_ap()`
* **SSID format:** `LFR-XX` where `XX` is a 2-digit unit number (01–06). Stored in `config.py`.
* **Password:** `lfr12345` (simple, memorable for students)
* **IP address:** `192.168.4.1` (CircuitPython default for AP mode)
* **Channel:** Auto-select or fixed (e.g., channel 6)

#### Web Server — `network/web_server.py`

* Minimal HTTP server using `wifi` and `socketpool` modules
* **Non-blocking:** Uses the cooperative polling pattern — the main loop calls `server.poll()` each iteration, which checks for a pending HTTP request and responds if one is waiting
* **No framework dependency:** Raw socket-level HTTP handling (CircuitPython does not have Flask/Django)
* Serves HTML pages and handles form submissions (GET/POST)
* Max 1 client connection at a time (sufficient for single-user tuning)

#### HTML UI — `network/ui_pages.py`

* HTML templates stored as Python string constants (no filesystem template engine)
* Minimal CSS, no JavaScript frameworks — must work in any modern browser
* Pages and controls defined in [§6 WiFi Browser UI Specification](#6-wifi-browser-user-interface-specification)

### 3.8 Main Control Loop

The main loop uses **cooperative polling** — a single `while True` loop that sequentially reads sensors, computes control output, sets motor speeds, and checks for HTTP requests. No threading or asyncio.

```python
# Pseudocode for main.py

import config
sensor = config.get_sensor()         # Returns a LineSensor instance
controller = config.get_controller() # Returns a Controller instance
motors = config.get_motor_driver()   # Returns a MotorDriver instance
speed_sensor = config.get_speed_sensor()  # Returns SpeedSensor or None
server = config.get_web_server()     # Returns WebServer or None

last_time = time.monotonic()
running = True  # Can be toggled via browser UI

while True:
    now = time.monotonic()
    dt = now - last_time
    last_time = now

    # 1. Read sensors
    position = sensor.read_position()
    detected = sensor.line_detected()

    # 2. Read speed sensors (if installed)
    if speed_sensor:
        rpm = speed_sensor.read_rpm()

    # 3. Compute control (if running)
    if running and detected:
        left, right = controller.update(position, dt)
        motors.set_speeds(left, right)
    elif not detected:
        motors.stop()  # Safety: stop if line lost

    # 4. Handle HTTP request (if WiFi active)
    if server:
        server.poll(sensor, controller, motors, speed_sensor)

    # 5. Small sleep to prevent tight-loop CPU saturation
    time.sleep(0.005)  # ~200 Hz max loop rate; actual rate depends on sensor read time
```

**Target loop rate:** 20–50 Hz (sufficient for PID at typical LFR speeds). The QTRX RC timing read (~2–5 ms) is the bottleneck. With the HTTP poll overhead, expect ~30 Hz in practice. **VERIFY** actual loop rate on hardware.

### 3.9 Firmware Configuration

`config.py` selects which modules to load for the current Design Session:

```python
# config.py — Example for DS10 (PID Controller)

UNIT_NUMBER = 1          # Robot ID (1–6), used for WiFi SSID
SENSOR = "qtrx_array"    # Options: "ir_pair", "qtrx_array"
CONTROLLER = "pid"        # Options: "bang_bang", "proportional", "pid", "kalman_pid", "qlearning"
MOTOR_DRIVER = "kitronik" # Options: "kitronik"
SPEED_SENSOR = True       # True if speed sensors installed (DS9+)
WIFI_ENABLED = True       # True if WiFi AP active (DS8+)
WIFI_SSID = f"LFR-{UNIT_NUMBER:02d}"
WIFI_PASSWORD = "lfr12345"

# Controller-specific defaults (overridden via browser UI at runtime)
PID_KP = 1.5
PID_KI = 0.0
PID_KD = 0.5
BASE_SPEED = 0.5
```

The `config.py` file is the **only file students need to edit** when swapping Design Sessions. The `get_sensor()`, `get_controller()`, etc. factory functions read the string constants and import the appropriate module.

### 3.10 Firmware by Design Session

| DS | Sensor Module | Controller Module | Motor Module | Speed Sensor | WiFi | config.py Changes from Previous DS |
|:---|:-------------|:-----------------|:-------------|:------------|:-----|:----------------------------------|
| DS3 | `ir_pair` | *(motor test only — no controller)* | `kitronik` | No | No | Initial setup |
| DS4–DS5 | `ir_pair` | `bang_bang` | `kitronik` | No | No | Add `CONTROLLER = "bang_bang"` |
| DS6 | `qtrx_array` | `bang_bang`* | `kitronik` | No | No | Change `SENSOR = "qtrx_array"` |
| DS7 | `qtrx_array` | `proportional` | `kitronik` | No | No | Change `CONTROLLER = "proportional"` |
| DS8 | `qtrx_array` | `proportional` | `kitronik` | No | **Yes** | Add `WIFI_ENABLED = True` |
| DS9 | `qtrx_array` | `proportional` | `kitronik` | **Yes** | Yes | Add `SPEED_SENSOR = True` |
| DS10 | `qtrx_array` | `pid` | `kitronik` | Yes | Yes | Change `CONTROLLER = "pid"` |
| DS11 | `qtrx_array` | `kalman_pid` | `kitronik` | Yes | Yes | Change `CONTROLLER = "kalman_pid"` |
| DS12 | `qtrx_array` | `qlearning` | `kitronik` | Yes | Yes | Change `CONTROLLER = "qlearning"` |

*At DS6, the controller is initially still bang_bang to demonstrate that the sensor upgrade alone improves performance. Students then switch to proportional at DS7.

### 3.11 CircuitPython Dependencies

**CircuitPython version:** 10.1.4 (latest stable, confirmed Pico W support)

**Built-in modules used:**

| Module | Purpose |
|:-------|:--------|
| `digitalio` | GPIO digital read/write (IR pair, QTRX RC timing, speed sensors) |
| `busio` | I2C communication with PCA9685 on Kitronik board |
| `wifi` | WiFi AP mode |
| `socketpool` | TCP socket for HTTP server |
| `time` | `monotonic()` for timing, `sleep()` for loop pacing |
| `gc` | Memory monitoring (`gc.mem_free()`) |
| `json` | Saving/loading Q-table and configuration |
| `math` | Basic math operations for PID and Kalman |
| `countio` | Edge counting for speed sensors (if available; otherwise poll-based) |

**Adafruit libraries (from CircuitPython Library Bundle):**

| Library | Purpose | Notes |
|:--------|:--------|:------|
| `adafruit_httpserver` | HTTP server for browser UI | Evaluate if this simplifies web_server.py vs raw sockets. **VERIFY** memory footprint. |

**Kitronik library:**

| Library | Purpose | Notes |
|:--------|:--------|:------|
| `KitronikPicoRoboticsBoard.py` | PCA9685 motor control | From Kitronik GitHub repo. Evaluate for use or adapt into `motors/kitronik.py`. |

> **VERIFY:** Test that all needed modules fit in Pico W RAM simultaneously. If memory is tight at DS12 (Q-Learning + WiFi + QTRX + speed sensors), consider: (a) using `.mpy` compiled modules, (b) reducing Q-table size, (c) removing unused modules from filesystem.

---

## 4. Line Track Designer Specification

### 4.1 Overview

The Line Track Designer is a Python CLI tool that generates printable PDF tile sheets for floor-based LFR test tracks.
The instructor defines a track layout in a JSON configuration file,
then runs the tool to generate a multi-page PDF where each page is one 8.5 × 11 inch tile.
Tiles are printed, cut if needed, and taped together on the floor.

**Key constraints:**
* Maximum grid: 4 columns × 3 rows = 12 tiles
* Tile orientation: landscape (11 in wide × 8.5 in tall)
* Total track area: ~44 × 25.5 inches
* Line width: 19 mm (¾ inch) black line on white background — standard LFR competition width
* Robot clearance on all sides of the track grid

### 4.2 Track Definition Format

Tracks are defined in JSON files. Example:

```json
{
    "name": "Simple Oval",
    "description": "Gentle curves, wide track — validates basic 2-sensor line following",
    "grid_columns": 4,
    "grid_rows": 3,
    "line_width_mm": 19,
    "tiles": [
        ["blank",    "straight_h", "straight_h", "blank"   ],
        ["curve_se", "straight_h", "straight_h", "curve_sw"],
        ["curve_ne", "straight_h", "straight_h", "curve_nw"]
    ]
}
```

The `tiles` array is indexed `[row][column]`, top-to-bottom, left-to-right. Each element is a tile type string.

### 4.3 Tile Types

| Tile Type | Description | Line Geometry |
|:----------|:-----------|:-------------|
| `blank` | Empty tile, no line | White tile, no markings |
| `straight_h` | Horizontal straight | Line from left edge center to right edge center |
| `straight_v` | Vertical straight | Line from top edge center to bottom edge center |
| `curve_ne` | Northeast curve | Quarter-circle arc from bottom edge center to right edge center |
| `curve_nw` | Northwest curve | Quarter-circle arc from bottom edge center to left edge center |
| `curve_se` | Southeast curve | Quarter-circle arc from top edge center to right edge center |
| `curve_sw` | Southwest curve | Quarter-circle arc from top edge center to left edge center |
| `cross` | Crossover intersection | Horizontal + vertical straight overlaid |
| `chicane_lr` | Left-right S-curve | S-shaped line from left edge (offset up) to right edge (offset down) |
| `chicane_rl` | Right-left S-curve | S-shaped line from left edge (offset down) to right edge (offset up) |
| `start_h` | Horizontal start/finish | Horizontal straight with a perpendicular start/finish marker |
| `sharp_90_ne` | Sharp 90° NE turn | Right-angle turn (no arc) from bottom to right — tighter than curve |

> **Extensibility:** New tile types can be added by implementing a drawing function that renders the line geometry within the tile boundaries. The tile type registry is a dictionary mapping type strings to drawing functions.

### 4.4 Rendering & PDF Generation

* **Rendering engine:** Use `reportlab` (Python library) to generate PDF directly
* **Page size:** Letter (8.5 × 11 inches) in landscape orientation
* **Line rendering:** Black line of configured width (default 19 mm) on white background
* **Registration marks:** Small corner marks on each tile showing grid position (e.g., "R2C3" for row 2, column 3) — aids alignment when taping tiles together
* **Tile borders:** Light gray dashed border line to show tile edges (for cutting/alignment)
* **PDF output:** One page per tile, ordered left-to-right, top-to-bottom (reading order)
* **Preview mode:** Optionally generate a single-page overview showing the full grid at reduced scale (all tiles on one page) as the first page of the PDF

### 4.5 CLI Interface

```bash
# Generate PDF from a track definition
python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf

# Generate with preview page
python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf --preview

# List available tile types
python track_designer.py tiles

# Validate a track definition (check for disconnected lines, missing edge connections)
python track_designer.py validate tracks/figure_eight.json
```

**Arguments:**

| Command | Description |
|:--------|:-----------|
| `generate <json> -o <pdf>` | Generate PDF tile sheets from a track definition |
| `--preview` | Include a full-grid overview page as page 1 |
| `--line-width <mm>` | Override line width (default: from JSON or 19 mm) |
| `tiles` | List all available tile types with descriptions |
| `validate <json>` | Check track definition for errors (disconnected segments, out-of-grid tiles) |

### 4.6 Course Track Designs

These track JSON files must be created before the course:

| Track File | Used At | Design | Purpose |
|:-----------|:--------|:-------|:--------|
| `simple_oval.json` | Class 3 (DS4–DS5) | 4×3 oval with gentle curves | Validates basic 2-sensor line following |
| `oval_tight.json` | Class 4 (DS6) | Oval with tighter curves | Tests sensor array improvement vs IR pair |
| `figure_eight.json` | Classes 5–6 (DS7–DS8) | Figure-8 with crossover | Tests variable speed (slow curves, fast straights) |
| `figure_eight_chicane.json` | Class 7 (DS9) | Figure-8 + sharp S-curves | Tests speed sensor feedback and consistency |
| `complex_course.json` | Classes 8–9 (DS10–DS11) | All elements: straights, curves, S-curves, sharp turns | PID tuning and Kalman filter comparison |
| `competition_course.json` | Class 10 (DS12–DS13) | Instructor-designed final course | Final competition day |

### 4.7 Dependencies

| Package | Purpose | Install |
|:--------|:--------|:--------|
| `reportlab` | PDF generation | `pip install reportlab` |
| `jsonschema` | Track definition validation | `pip install jsonschema` |
| Python 3.10+ | Language runtime | System package |

---

## 5. LFR Simulator Specification

### 5.1 Overview

The LFR Simulator is a Python + Pygame desktop application for the instructor. It provides a 2D visual simulation of a differential-drive robot following a line track. The simulator is used for:

* **Instructor preparation:** Test and tune PID parameters before class
* **Classroom demos:** Show students how PID tuning, Kalman filtering, and Q-Learning affect robot behavior in real time
* **Q-Learning training:** Run many training episodes quickly at accelerated simulation speed

The simulator is **not** used by students directly, and is **not** connected to the physical robot. The simulator has its own implementations of the controller algorithms (mirroring the firmware controller interfaces from §3.3).

### 5.2 Physics Model

**Differential drive kinematics:**

The simulated robot has two independently driven wheels with a fixed axle width. The physics model computes robot position (x, y) and heading (θ) based on left and right wheel speeds.

| Parameter | Value | Notes |
|:----------|:------|:------|
| Axle width (L) | 130 mm | Approximate Emo chassis wheel-to-wheel distance (**VERIFY**) |
| Wheel diameter | 65 mm | Approximate Emo chassis wheel diameter (**VERIFY**) |
| Max wheel speed | 200 RPM | Approximate DC motor no-load speed (**VERIFY**) |
| Time step (dt) | 10 ms | Simulation step; decoupled from rendering frame rate |

**Update equations (per time step):**

```text
v_left  = left_speed × max_speed × wheel_circumference / 60   (cm/s)
v_right = right_speed × max_speed × wheel_circumference / 60  (cm/s)

v = (v_left + v_right) / 2          (linear velocity)
ω = (v_right - v_left) / L          (angular velocity)

θ += ω × dt
x += v × cos(θ) × dt
y += v × sin(θ) × dt
```

**Additional physics (optional, instructor-configurable):**
* Motor response lag (first-order filter on speed commands)
* Sensor noise (Gaussian noise added to simulated sensor readings)
* Wheel slip (random perturbation to effective wheel speed)

### 5.3 Sensor Simulation

The simulator models the sensor array by sampling the track image at positions corresponding to where physical sensors would be on the robot.

**IR Pair simulation (2 sensors):**
* Two sample points: left and right of robot center, offset by sensor spacing
* Each point checks if it overlaps the black line (binary: on-line / off-line)

**QTRX Array simulation (8 sensors):**
* 8 sample points evenly spaced across the sensor bar width (~50 mm total span, **VERIFY**)
* Each point samples the track image grayscale value at its world position
* Add configurable Gaussian noise to simulate real sensor noise
* Apply the same `read_position()` weighted-average calculation as the firmware module

**Speed sensor simulation:**
* Report the actual simulated wheel RPM (derived from the physics model)
* Optionally add quantization noise to simulate the slotted encoder disc resolution

### 5.4 Controller Integration

The simulator contains its own Python implementations of all controller algorithms, mirroring the firmware interfaces:

| Simulator Controller | Mirrors Firmware Module | Notes |
|:---------------------|:----------------------|:------|
| `sim_bang_bang.py` | `controllers/bang_bang.py` | Identical algorithm |
| `sim_proportional.py` | `controllers/proportional.py` | Identical algorithm |
| `sim_pid.py` | `controllers/pid.py` | Identical algorithm |
| `sim_kalman_pid.py` | `controllers/kalman_pid.py` | Identical algorithm |
| `sim_qlearning.py` | `controllers/qlearning.py` | Same Q-Learning algorithm; can run at accelerated speed |

The simulator controllers use the **same interface** as the firmware controllers (`update(position, dt) → (left, right)`), allowing the same tuning parameters and behavior.

**Q-Learning in the simulator:**
* Can run at 10×–100× real-time speed (no physical constraints)
* Displays Q-table evolution during training
* Training is independent from the physical robot (per [Appendix A, Q4](#appendix-a-specification-development-prompt--qa))

### 5.5 Track Loading

The simulator loads track definitions from the same JSON files used by the Line Track Designer (§4.2). It renders the track at a scale appropriate for the display window.

**Track rendering in simulator:**
* Rasterize the track at a resolution sufficient for sensor sampling (~1 mm per pixel)
* White background with black line
* The rasterized track is used for sensor point-sampling (check pixel color at sensor world position)

### 5.6 Visualization & UI

**Display layout (Pygame window):**

```text
┌─────────────────────────────────────┬──────────────────┐
│                                     │  Controller:     │
│                                     │  [PID ▼]         │
│                                     │                  │
│         Track + Robot View          │  Parameters:     │
│         (2D top-down)               │  kp: [===|==] 1.5│
│                                     │  ki: [=|=====] 0.0│
│         Robot shown as a            │  kd: [====|=] 0.5│
│         colored rectangle           │  speed: [==|==]  │
│         with heading arrow          │                  │
│                                     │  Sensor Display: │
│         Sensor points shown         │  ■■□□■■■■        │
│         as colored dots             │  Position: -0.12 │
│                                     │                  │
│                                     │  Speed: 24 cm/s  │
│                                     │  Loop: 47 Hz     │
│                                     │                  │
│                                     │  [Start] [Stop]  │
│                                     │  [Reset] [Save]  │
│                                     │                  │
│                                     │  Noise: [==|==]  │
│                                     │  Sim speed: [1x] │
└─────────────────────────────────────┴──────────────────┘
```

**UI elements:**

| Element | Type | Description |
|:--------|:-----|:-----------|
| Track view | Canvas | Top-down view of track with robot position and heading |
| Robot | Rectangle + arrow | Colored rectangle showing robot body, arrow showing heading |
| Sensor dots | Colored circles | Green = on line, red = off line, positioned on the robot |
| Controller selector | Dropdown | Select which controller algorithm to use |
| Parameter sliders | Sliders | Real-time adjustment of all controller parameters (see §3.5 for parameter definitions) |
| Sensor bar | Block display | Visual representation of 8 sensor readings |
| Position readout | Text | Numeric line position value |
| Speed readout | Text | Simulated robot speed in cm/s |
| Loop rate | Text | Simulation steps per second |
| Start/Stop | Button | Start or pause simulation |
| Reset | Button | Return robot to start position, reset controller state |
| Save | Button | Save current parameters to JSON file |
| Noise slider | Slider | Adjust sensor noise level (0 = perfect, 1 = very noisy) |
| Sim speed | Selector | 1×, 2×, 5×, 10× simulation speed (useful for Q-Learning training) |

**Keyboard shortcuts:**
* `Space` — Start/Stop toggle
* `R` — Reset
* `1`–`5` — Select controller (1=bang_bang, 2=proportional, 3=PID, 4=Kalman+PID, 5=Q-Learning)
* `+`/`-` — Increase/decrease simulation speed

### 5.7 Dependencies

| Package | Purpose | Install |
|:--------|:--------|:--------|
| `pygame` | Window, rendering, event handling | `pip install pygame` |
| `numpy` | Physics calculations, array operations | `pip install numpy` |
| `json` | Track loading, parameter saving | Built-in |
| `math` | Trigonometry for kinematics | Built-in |
| Python 3.10+ | Language runtime | System package |

---

## 6. WiFi Browser User Interface Specification

### 6.1 Network Architecture

```text
Student laptop                     Pico W (LFR robot)
┌──────────┐     WiFi AP         ┌─────────────────┐
│ Browser  │◄───────────────────►│ AP: LFR-01      │
│ (any)    │  SSID: LFR-01       │ IP: 192.168.4.1 │
│          │  Pass: lfr12345     │ Port: 80        │
└──────────┘                     └─────────────────┘

URL: http://192.168.4.1/
```

* Each robot has a unique SSID (`LFR-01` through `LFR-06`)
* No internet access — isolated AP network
* Single client at a time (one student laptop per robot)
* HTTP only (no HTTPS — not needed on isolated network)

### 6.2 UI Pages & Controls

#### Dashboard Page (`/`)

The main page shown when a student connects. Content evolves by Design Session:

**DS8 (first WiFi session):**
* Robot name and unit number
* Live sensor readings (auto-refresh every 500 ms via meta-refresh or simple JavaScript `setTimeout`)
* Speed control: base speed slider (0.0–1.0) + Apply button
* Start/Stop button

**DS9 (speed sensors added):**
* All DS8 controls plus:
* Live speed readings: left wheel RPM, right wheel RPM
* Target speed vs actual speed display

**DS10 (PID controller):**
* All DS9 controls plus:
* PID parameter sliders: kp, ki, kd (each with min/max/step from `param_definitions`)
* Current error value display
* "Reset PID" button (clears integral accumulator)

**DS11 (Kalman filter):**
* All DS10 controls plus:
* Kalman filter parameter sliders: Q (process noise), R (measurement noise)
* "Filter ON/OFF" toggle for before/after comparison
* Filtered vs raw position display

**DS12 (Q-Learning):**
* All DS9 controls plus:
* Training mode ON/OFF toggle
* Current state, action, reward display
* Episode count and cumulative reward
* Q-table display (text-based heatmap or table)
* "Save Q-Table" / "Load Q-Table" buttons

#### Calibration Page (`/calibrate`)

* Guide for sensor calibration: "Place robot on white surface, press Calibrate White. Place sensor over line, press Calibrate Black."
* Calibrate White button
* Calibrate Black button
* Raw sensor values display (updates live)

### 6.3 API Endpoints

The web server handles these HTTP endpoints:

| Method | Path | Purpose |
|:-------|:-----|:--------|
| GET | `/` | Dashboard page (HTML) |
| GET | `/calibrate` | Calibration page (HTML) |
| POST | `/params` | Update controller parameters (form data: `kp=1.5&ki=0.0&kd=0.5`) |
| POST | `/speed` | Set base speed (form data: `base_speed=0.4`) |
| POST | `/start` | Start line following |
| POST | `/stop` | Stop robot |
| POST | `/calibrate/white` | Record white (background) sensor values |
| POST | `/calibrate/black` | Record black (line) sensor values |
| POST | `/reset` | Reset controller state |
| POST | `/qlearning/train` | Toggle Q-Learning training mode |
| POST | `/qlearning/save` | Save Q-table to filesystem |
| POST | `/qlearning/load` | Load Q-table from filesystem |
| GET | `/status` | JSON response with current sensor data, speeds, controller state (for AJAX refresh) |

> **Implementation note:** All POST endpoints redirect back to `/` after processing (POST-redirect-GET pattern). The `/status` endpoint returns JSON for lightweight polling updates.

---

## 7. Testing Strategy

Testing uses **pytest for automated tests** and **manual verification for visual/physical outputs**. All tests must pass before the course begins.

### 7.1 Firmware Testing

Firmware modules have two test layers:

#### Layer 1: Desktop unit tests (pytest on Ubuntu)

* Test controller algorithms in isolation using synthetic position data
* Test sensor `read_position()` calculation logic with known raw values
* Test `config.py` factory functions (correct module instantiation)
* Test Q-table update math
* Test Kalman filter state estimation with known inputs
* These tests import the firmware Python modules directly on desktop Python (not CircuitPython).
  Modules must be written to avoid CircuitPython-only imports at the top level
  — use conditional imports or dependency injection for hardware modules (`digitalio`, `busio`, `wifi`, etc.)

#### Layer 2: On-hardware integration tests (manual, on Pico W)
* Flash firmware, verify each module works on real hardware
* Test sensor reads with known surfaces (white paper, black tape)
* Test motor response to speed commands
* Test WiFi AP creation and browser UI access
* Documented as manual test procedures with expected outcomes

### 7.2 Line Track Designer Testing

**Automated tests (pytest):**
* Track JSON parsing and validation (valid and invalid inputs)
* Tile type registry (all types present, draw functions callable)
* Grid boundary validation (tiles don't exceed grid dimensions)
* PDF generation (output file is a valid PDF with correct page count)
* Line width rendering (verify line width in PDF matches specification)

**Manual verification:**
* Print a test tile at actual size, measure line width with ruler (should be 19 mm)
* Print a full track, assemble on floor, verify tiles align at edges
* Visual inspection: curves are smooth, intersections align, no gaps at tile boundaries

### 7.3 LFR Simulator Testing

**Automated tests (pytest):**
* Physics model: given known left/right speeds, verify position and heading after N steps
* Sensor simulation: given known robot position on a known track, verify sensor readings
* Controller algorithms: same tests as firmware layer 1 (shared test data)
* Track loading: verify JSON parsing produces correct internal representation

**Manual verification:**
* Visual: robot follows the line smoothly in the Pygame window
* PID tuning: adjusting sliders changes behavior in expected ways (increase kp → more aggressive steering)
* Q-Learning: robot improves over training episodes (visible in behavior and reward)
* Performance: simulation runs at ≥30 fps at 1× speed on the target Ubuntu machine

### 7.4 Hardware Integration Testing

Performed on the instructor's LFR unit (unit 01) before the course:

| Test | Procedure | Pass Criteria |
|:-----|:----------|:-------------|
| Motor direction | Set left forward, verify left wheel spins forward. Repeat for right. | Both motors respond correctly to direction commands |
| Motor speed | Ramp from 0% to 100% in 10% increments | Smooth, monotonic speed increase; no stalling below 20% |
| IR pair detection | Place sensor over white paper, then black line | Clear distinction in digital readings; threshold-based detection works |
| QTRX array calibration | Run calibration routine on white paper + black line | All 8 sensors report distinguishable min/max values |
| QTRX position accuracy | Place line under each sensor in sequence | `read_position()` returns expected value (−1.0 to +1.0) in correct direction |
| Speed sensor counting | Spin each wheel by hand at known rate | RPM reading matches expected value within 10% |
| WiFi AP | Connect laptop to LFR-01 network | Laptop connects, browser loads dashboard at 192.168.4.1 |
| Browser UI tuning | Adjust PID sliders via browser | Robot behavior changes in real time; parameter values persist until next change |
| Full run: PID | Run robot on complex course track | Robot completes 3 laps without losing the line |
| Full run: Q-Learning | Train robot for 20 laps, then run | Reward increases over training; trained robot follows line better than untrained |

### 7.5 Test-Gate Definitions by Design Session

Each Design Session has test-gates that must pass before moving to the next session. These are validated on the instructor's unit during pre-course development, and again by students during the course.

#### DS3 Test-Gates (Hardware Install + CircuitPython)

1. CircuitPython 10.1.4 boots on the Pico W (REPL accessible via Mu Editor)
2. Motor test script drives both wheels forward for 2 seconds, then stops
3. Motor test script turns left, then right (verifying wiring polarity)
4. IR pair sensor reads "line" when placed over black tape, "no line" over white paper
5. Pico W memory check: `gc.mem_free()` reports at least 100 KB available

#### DS4–DS5 Test-Gates (First Line Follower)

1. Bang-bang controller follows the simple oval track for 1 complete lap
2. Robot recovers after being placed slightly off the line
3. Robot stops or reverses when it loses the line entirely
4. `read_position()` returns sensible values: negative when line is left, positive when right

#### DS6 Test-Gates (Sensor Array Upgrade)

1. QTRX calibration completes without errors
2. All 8 sensors report distinct values for black vs white
3. `read_position()` accuracy: line under sensor 1 → ~−1.0, sensor 8 → ~+1.0
4. Robot follows the oval-tight track with noticeably smoother behavior than with IR pair
5. Robot handles tighter curves than it could with the IR pair

#### DS7 Test-Gates (Variable Speed)

1. Proportional controller adjusts speed based on position error
2. Robot goes faster on straight sections, slower on curves (observable behavior)
3. Robot completes the figure-eight track including crossover
4. Speed differential is tunable via `kp` and `base_speed` parameters

#### DS8 Test-Gates (WiFi AP + Browser UI)

1. WiFi AP starts with correct SSID (e.g., `LFR-01`)
2. Laptop connects to AP and loads dashboard at `http://192.168.4.1/`
3. Live sensor readings update in the browser
4. Speed parameter can be changed via browser and takes effect immediately
5. Start/Stop commands from browser work
6. Control loop maintains ≥20 Hz while serving HTTP requests

#### DS9 Test-Gates (Speed Sensors + Closed-Loop)

1. Both speed sensors report non-zero RPM when wheels spin
2. RPM values are proportional to actual wheel speed (faster = higher RPM)
3. Speed sensor data displays correctly in the browser UI
4. Robot runs 3 laps on figure-eight-chicane track with consistent lap times (within 10% variation)

#### DS10 Test-Gates (PID Controller)

1. PID controller compiles and runs without errors
2. All three PID parameters (kp, ki, kd) are adjustable via browser UI
3. Changing kp visibly changes steering aggressiveness
4. Adding kd reduces oscillation compared to P-only control
5. Robot completes 3 laps on the complex course track
6. Lap time improves by at least 20% compared to proportional controller on the same track

#### DS11 Test-Gates (Kalman Filter)

1. Kalman filter module runs without errors; parameters adjustable via browser UI
2. Filtered position is noticeably smoother than raw position (visible in browser readout)
3. "Filter ON/OFF" toggle produces observable difference in robot smoothness
4. Robot completes 3 laps on the complex course track with less wobble than unfiltered PID
5. Tuning Q and R via browser produces expected behavior (high R → trusts prediction more, high Q → trusts sensor more)

#### DS12 Test-Gates (Q-Learning)

1. Q-Learning controller runs in training mode without errors
2. Reward increases over 10 training episodes (measurable trend)
3. Trained robot (run mode) follows the line without ε-greedy exploration
4. Q-table saves to filesystem and loads correctly after power cycle
5. Browser UI displays training state: episode count, reward, current state/action

---

## 8. Software Dependencies Summary

### Pico W (CircuitPython 10.1.4)

| Dependency | Source | Notes |
|:-----------|:-------|:------|
| CircuitPython 10.1.4 | circuitpython.org | Flash onto Pico W before course |
| CircuitPython Library Bundle | circuitpython.org/libraries | Version matched to CP 10.x |
| Kitronik Robotics Board library | github.com/KitronikLtd | Evaluate and adapt for `motors/kitronik.py` |

### Ubuntu Development Machine (Python 3.10+)

**Line Track Designer:**

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `reportlab` | latest | PDF generation |
| `jsonschema` | latest | Track JSON validation |
| `pytest` | latest | Automated testing |

**LFR Simulator:**

| Package | Version | Purpose |
|:--------|:--------|:--------|
| `pygame` | latest | Window, rendering, UI |
| `numpy` | latest | Physics, array math |
| `pytest` | latest | Automated testing |

**Shared development tools:**

| Tool | Purpose |
|:-----|:--------|
| `git` | Version control |
| `markdownlint-cli2` | Markdown linting for documentation |
| `mu-editor` | CircuitPython code editor (also used by students) |

---

## 9. Unresolved Questions & Risks

| # | Item | Category | Impact | Notes |
|:--|:-----|:---------|:-------|:------|
| 1 | ~~**RESOLVED.**~~ 9V clip powers Kitronik board (within 3.0–10.8V spec). 8×AA powers buck converter only. | HW | — | No voltage issue. See §2.4 Power Architecture. |
| 2 | ~~**RESOLVED.**~~ 9V Battery Clip Connector powers Kitronik board directly. | HW | — | Confirmed by instructor. See §2.4 Power Architecture. |
| 3 | **QTRX RC timing via software GPIO.** Needs µs precision; CP is interpreted. | FW | Medium | Test early; consider PIO-based timing on RP2040. |
| 4 | **Pico W RAM at DS12.** WiFi + HTTP + sensors + Q-table may push near RAM limit. | FW | Medium | Profile memory at each DS. Use `.mpy` modules. Remove unused imports. |
| 5 | **Kitronik H-bridge IC confirmation.** Assumed DRV8833 from cross-ref. | HW | Low | Inspect board at purchase. PCA9685 behavior unchanged regardless. |
| 6 | **Emo chassis dimensions.** Axle width, wheel diameter affect sim and calibration. | HW | Medium | Measure at first build. Update sim physics and firmware values. |
| 7 | **`countio.Counter` availability.** Needed for speed sensor edge counting. | FW | Low | Fallback: polling-based edge counting. Less accurate at high RPM. |
| 8 | **`adafruit_httpserver` memory.** If too large, need raw-socket HTTP server. | FW | Medium | Test early. Fallback: minimal HTTP handler (<100 lines). |
| 9 | **QTRX mounting on Emo chassis.** Must be close to ground, in front. | HW | Medium | May need 3D-printed/laser-cut bracket. Assess at first build. |
| 10 | **Track tile alignment when printed.** Printer margins may cause misalignment. | SW | Low | Registration marks + test with Makersmiths printer. |

---

## Appendix A: Specification Development Prompt & Q&A

### Original Prompt

The following prompt was used to generate this specification (reproduced verbatim from the instructor):

> Along with CLAUDE.md, read only @input/*.md and @docs/*.md files.
> Create a specification document, reflecting the incrementally development in the Line Following Robot (LFR) course.
> I need this specification document to help prepare me for delivering the course and all software required for the course.
> I want all the components implied below (both hardware and software) to be built and tested in advance of the course.
> Place your creation in the file @docs/lfr-specification.md.
>
> I want the LFR software to be built in a modular form, such that, a software subsystem in step N
> can be pulled out and replaced with a new subsystem in step N+1 (e.g. PID Controller replaced with Q-Learning Controller).
> Make sure you include the Line Track Designer and LFR Simulators software in this specification document.
> I plan to build and test all software prior to the start of the course.
> Think harder about the software architecture and testing of this project.
>
> Within the document you create, include this prompt,
> all questions you ask me, along with my responses.
> Place this in an appendix and reference it at the beginning of the specification
> and anywhere else in the text when it's a useful reference.
>
> In subsequent steps, I need this specification document to help prepare a detailed development plan.
> Think Very Hard about what must be specified in the specification document so a robust development plan can be created.
>
> I expect there will be some issues,
> so use the AskUserQuestions tool for all things that require further clarification.

### Instructor Q&A

All questions asked during specification development and the instructor's responses:

| # | Question | Answer |
|:--|:---------|:-------|
| 1 | You asked to place the specification in `docs/lfr-lesson-plan.md`, but that file already contains the lesson plan. CLAUDE.md says the specification goes in `docs/lfr-specification.md`. Which file? | `docs/lfr-specification.md` — separate file per convention |
| 2 | For the LFR Simulator, which Python GUI library should it use? | **Pygame** — best for 2D real-time simulation with animation |
| 3 | For the Line Track Designer, what should the output format be? | **PDF tiles** — multi-page PDF, one tile per page, print directly |
| 4 | Should Q-Learning training happen on the physical robot, in the simulator, or both? | **Both independently** — simulator for instructor demos, on-robot for class; no transfer between them |
| 5 | What CircuitPython version should the spec target? | **CircuitPython 10.1.4** (latest stable, confirmed Pico W support, released 2026-03-09) |
| 6 | For the Line Track Designer, does it need a GUI or is a config file + CLI sufficient? | **Config file + CLI** — JSON definition, command to preview and generate PDF |
| 7 | For firmware modularity, how should swappable subsystems be structured? | **Plugin modules imported by main.py** — swap by changing config variable, clean Pythonic architecture |
| 8 | How should the WiFi browser UI + control loop coexist on the Pico W? | **Cooperative polling loop** — single main loop, check for HTTP requests each iteration, ~20–50 Hz target |
| 9 | Do you have the Kitronik Robotics Board GPIO pin assignments, or should I spec from the product page? | **Spec from product page** — research the Kitronik board pinout and document it |
| 10 | For testing desktop tools, what's your preference? | **pytest + manual verification** — automated unit tests for logic, manual visual verification for rendered output |
| 11 | Should the simulator model differential-drive physics or a simpler point-mass model? | **Differential drive** — two-wheel model with independent motor speeds, realistic turning |
| 12 | Should the simulator support real-time parameter tuning during playback? | **Yes, real-time sliders** — Pygame sidebar with sliders for PID gains, speed, noise level |

---

<!-- Reference-style links -->
[L01]:https://makersmiths.org/
[L02]:https://www.makerspaces.com/what-is-a-makerspace/
