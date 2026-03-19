# LFR Wiring Plan

* **Project:** Line Following Robot — Makersmiths Course
* **MCU:** Raspberry Pi Pico W seated in Kitronik Robotics Board for Pico (5329)
* **Reference:** `docs/lfr-specification.md` §2.3 (GPIO allocation), §2.4 (power architecture)

---

## How to Read This Document

Each milestone table lists every physical wire on the robot at that build stage. Milestones without new hardware list the cumulative connection count for reference only.

**Table columns:**

| Column | Meaning |
|:-------|:--------|
| # | Connection reference number |
| From | Source device |
| From Marking | Label or silkscreen text printed on the source device |
| To | Destination device |
| To Marking | Label or silkscreen text printed on the destination device |
| Notes | Wire color, breadboard column, or clarifying remarks |

**Physical notes:**
* The **Pico W seats directly into the Kitronik 5329** via the 40-pin header on the Kitronik board — no separate wiring required for that connection.
* The **breadboard** acts as the wiring hub for all sensors. Sensor power/GND wires land on the breadboard power rails; signal wires run from sensor output pads to the Kitronik board GPIO solder pads via the breadboard.
* The Kitronik board exposes Pico W GPIO pins as **solder pads labeled GP0–GP22 and GP26–GP28**, matching the Pico W silkscreen. Pin headers (from the BOM "Pin Header Connection") must be soldered to these pads before use.
* **⚠ VERIFY:** The Kitronik 5329 power input terminal marking. Assumed "VIN" (+) and "GND" (−) below. Confirm against the physical board before wiring.
* **⚠ VERIFY:** MOTOR 1 = left wheel, MOTOR 2 = right wheel. Swap motor wire pairs if a wheel spins the wrong direction at first power-on; do not modify firmware.

---

## M0 — Project Bootstrap

**No hardware connections.** Development environment setup only (Ubuntu, Python venv, pytest).

---

## M1 — Line Track Designer

**No hardware connections.** Software-only milestone — CLI tool that generates PDF track tiles.

---

## M2 — Firmware Foundation (DS3–DS5)

First physical assembly of the LFR. Establishes the permanent power architecture, motor wiring, and initial IR pair line sensors.

### Power

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| P1 | 9V Battery Clip Connector | Red wire (+) | Kitronik 5329 | VIN ⚠ VERIFY label | 9V powers motors + Pico via Kitronik on-board 3.3V regulator |
| P2 | 9V Battery Clip Connector | Black wire (−) | Kitronik 5329 | GND ⚠ VERIFY label | Battery negative / common ground |
| P3 | 8×AA Battery Holder | Red wire (+) | 5V Buck Converter | VIN+ (or IN+) | 12V input to buck converter |
| P4 | 8×AA Battery Holder | Black wire (−) | 5V Buck Converter | GND (or IN−) | Battery negative |
| P5 | 5V Buck Converter | VOUT+ (or OUT+) | Breadboard | + power rail | 5V regulated output → sensor supply |
| P6 | 5V Buck Converter | GND (or OUT−) | Breadboard | − (GND) rail | Converter ground → breadboard GND rail |
| P7 | Kitronik 5329 | GND solder pad | Breadboard | − (GND) rail | Ties Kitronik/Pico ground to sensor ground; common ground |

### Motors

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| M1 | Emo Chassis Left Motor | Wire A | Kitronik 5329 | MOTOR 1 — terminal 1 | Polarity sets forward/reverse; swap if direction wrong |
| M2 | Emo Chassis Left Motor | Wire B | Kitronik 5329 | MOTOR 1 — terminal 2 | |
| M3 | Emo Chassis Right Motor | Wire A | Kitronik 5329 | MOTOR 2 — terminal 1 | |
| M4 | Emo Chassis Right Motor | Wire B | Kitronik 5329 | MOTOR 2 — terminal 2 | |

### IR Pair Line Sensors (DS3–DS5 only — removed at M3)

Two individual IR Emitter/Phototransistor Pair modules: one mounted on left side, one on right side of the chassis front.

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| S1 | IR Pair — Left module | VCC | Breadboard | + power rail | 5V from buck converter |
| S2 | IR Pair — Left module | GND | Breadboard | − (GND) rail | |
| S3 | IR Pair — Left module | OUT | Kitronik 5329 | GP2 solder pad | Digital input; LOW = line detected |
| S4 | IR Pair — Right module | VCC | Breadboard | + power rail | 5V from buck converter |
| S5 | IR Pair — Right module | GND | Breadboard | − (GND) rail | |
| S6 | IR Pair — Right module | OUT | Kitronik 5329 | GP3 solder pad | Digital input; LOW = line detected |

**M2 total connections: 13**

---

## M3 — Firmware Sensor Array (DS6–DS7)

The IR pair is removed and replaced by the QTRX-MD-08RC 8-channel reflectance sensor array. Power and motor wiring from M2 is unchanged.

### Removals from M2

Disconnect and physically remove connections S1–S6 (the IR pair modules and all three wires per module).

### QTRX-MD-08RC Additions

The QTRX-MD-08RC has an 11-pin single-row 0.1" connector. Pin order (left to right, sensor face down, connector edge toward you):

> **CTRL — GND — VCC — S1 — S2 — S3 — S4 — S5 — S6 — S7 — S8**

Mount the QTRX under the chassis front, centered, facing down, ~3–5 mm above the floor surface. Use the Makersmiths-fabricated mounting bracket.

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| S1 | QTRX-MD-08RC | VCC | Breadboard | + power rail | 5V from buck converter; QTRX rated 2.9–5.5V |
| S2 | QTRX-MD-08RC | GND | Breadboard | − (GND) rail | |
| S3 | QTRX-MD-08RC | CTRL | Kitronik 5329 | GP10 solder pad | Digital output from Pico; HIGH = IR emitters on |
| S4 | QTRX-MD-08RC | S1 | Kitronik 5329 | GP0 solder pad | Leftmost sensor; RC timing input |
| S5 | QTRX-MD-08RC | S2 | Kitronik 5329 | GP1 solder pad | RC timing input |
| S6 | QTRX-MD-08RC | S3 | Kitronik 5329 | GP2 solder pad | Reused pad (was IR left OUT) |
| S7 | QTRX-MD-08RC | S4 | Kitronik 5329 | GP3 solder pad | Reused pad (was IR right OUT) |
| S8 | QTRX-MD-08RC | S5 | Kitronik 5329 | GP4 solder pad | RC timing input |
| S9 | QTRX-MD-08RC | S6 | Kitronik 5329 | GP5 solder pad | RC timing input |
| S10 | QTRX-MD-08RC | S7 | Kitronik 5329 | GP6 solder pad | RC timing input |
| S11 | QTRX-MD-08RC | S8 | Kitronik 5329 | GP7 solder pad | Rightmost sensor; RC timing input |

**M3 total connections: 18** (7 power/motor from M2 + 11 QTRX)

---

## M4 — Firmware WiFi + Browser UI (DS8)

**No new hardware connections.** WiFi is provided by the Pico W's onboard CYW43439 chip — no external antenna or wiring required. No GPIO pins are added.

**M4 total connections: 18** (unchanged from M3)

---

## M5 — Firmware Speed Sensors (DS9)

Two Speed Sensor Modules (IR optocoupler with LM393 comparator) are added — one on each wheel. Mount each module so the slotted encoder disc on the motor shaft passes through the sensor's IR gap.

Each module has 4 pins: **VCC — GND — D0 — A0**. Only VCC, GND, and D0 (digital output) are used. A0 (analog output) is left unconnected.

### Left Wheel Speed Sensor

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| W1 | Speed Sensor — Left | VCC | Breadboard | + power rail | 5V from buck converter |
| W2 | Speed Sensor — Left | GND | Breadboard | − (GND) rail | |
| W3 | Speed Sensor — Left | D0 | Kitronik 5329 | GP11 solder pad | Digital input; pulses as encoder slots pass |

### Right Wheel Speed Sensor

| # | From | From Marking | To | To Marking | Notes |
|:--|:-----|:-------------|:---|:-----------|:------|
| W4 | Speed Sensor — Right | VCC | Breadboard | + power rail | 5V from buck converter |
| W5 | Speed Sensor — Right | GND | Breadboard | − (GND) rail | |
| W6 | Speed Sensor — Right | D0 | Kitronik 5329 | GP12 solder pad | Digital input; pulses as encoder slots pass |

**M5 total connections: 24** (18 from M3/M4 + 6 speed sensors)

---

## M6 — Firmware PID (DS10)

**No new hardware connections.** PID controller is a firmware-only change. All sensors and motors remain wired as in M5.

**M6 total connections: 24** (unchanged from M5)

---

## M7 — LFR Simulator

**No hardware connections.** Python + Pygame simulation runs on the instructor's Ubuntu laptop. Does not interact with the physical robot.

---

## M8 — Firmware Kalman Filter (DS11)

**No new hardware connections.** Kalman filter is a firmware-only addition to the sensor pipeline.

**M8 total connections: 24** (unchanged from M5)

---

## M9 — Firmware Q-Learning Controller (DS12)

**No new hardware connections.** Q-Learning controller is a firmware-only module swap.

**M9 total connections: 24** (unchanged from M5)

---

## M10 — Final Prep & Course Readiness

**No new hardware connections.** Integration testing, track setup, and course material finalization.

**M10 total connections: 24** (unchanged from M5)

---

## Final Build Summary (M5 and beyond)

Complete connection reference for the fully-assembled LFR:

| # | From | From Marking | To | To Marking |
|:--|:-----|:-------------|:---|:-----------|
| P1 | 9V Battery Clip | + (red) | Kitronik 5329 | VIN |
| P2 | 9V Battery Clip | − (black) | Kitronik 5329 | GND |
| P3 | 8×AA Battery Holder | + (red) | 5V Buck Converter | VIN+ |
| P4 | 8×AA Battery Holder | − (black) | 5V Buck Converter | GND |
| P5 | 5V Buck Converter | VOUT+ | Breadboard | + power rail |
| P6 | 5V Buck Converter | GND | Breadboard | − (GND) rail |
| P7 | Kitronik 5329 | GND solder pad | Breadboard | − (GND) rail |
| M1 | Left Motor | Wire A | Kitronik 5329 | MOTOR 1 — terminal 1 |
| M2 | Left Motor | Wire B | Kitronik 5329 | MOTOR 1 — terminal 2 |
| M3 | Right Motor | Wire A | Kitronik 5329 | MOTOR 2 — terminal 1 |
| M4 | Right Motor | Wire B | Kitronik 5329 | MOTOR 2 — terminal 2 |
| S1 | QTRX-MD-08RC | VCC | Breadboard | + power rail |
| S2 | QTRX-MD-08RC | GND | Breadboard | − (GND) rail |
| S3 | QTRX-MD-08RC | CTRL | Kitronik 5329 | GP10 |
| S4 | QTRX-MD-08RC | S1 | Kitronik 5329 | GP0 |
| S5 | QTRX-MD-08RC | S2 | Kitronik 5329 | GP1 |
| S6 | QTRX-MD-08RC | S3 | Kitronik 5329 | GP2 |
| S7 | QTRX-MD-08RC | S4 | Kitronik 5329 | GP3 |
| S8 | QTRX-MD-08RC | S5 | Kitronik 5329 | GP4 |
| S9 | QTRX-MD-08RC | S6 | Kitronik 5329 | GP5 |
| S10 | QTRX-MD-08RC | S7 | Kitronik 5329 | GP6 |
| S11 | QTRX-MD-08RC | S8 | Kitronik 5329 | GP7 |
| W1 | Speed Sensor — Left | VCC | Breadboard | + power rail |
| W2 | Speed Sensor — Left | GND | Breadboard | − (GND) rail |
| W3 | Speed Sensor — Left | D0 | Kitronik 5329 | GP11 |
| W4 | Speed Sensor — Right | VCC | Breadboard | + power rail |
| W5 | Speed Sensor — Right | GND | Breadboard | − (GND) rail |
| W6 | Speed Sensor — Right | D0 | Kitronik 5329 | GP12 |

---

## Open Items to Verify at First Build

| # | Item | Where to Check |
|:--|:-----|:---------------|
| 1 | Kitronik 5329 power input terminal label (assumed "VIN" / "GND") | Physical board silkscreen |
| 2 | Kitronik 5329 motor terminal labels (assumed "MOTOR 1" / "MOTOR 2") | Physical board silkscreen |
| 3 | IR Pair module output pin label (assumed "OUT") | Module silkscreen; some variants print "DO" or "S" |
| 4 | Speed Sensor D0 output label (assumed "D0") | Module silkscreen; some variants print "DO" or "OUT" |
| 5 | Left/right motor assignment (assumed MOTOR 1 = left, MOTOR 2 = right) | Test spin at first power-on; swap wire pairs if reversed |
| 6 | QTRX S1 orientation (assumed S1 = leftmost when sensor faces down, connector toward rear) | Confirm with Pololu dimension diagram before mounting |
