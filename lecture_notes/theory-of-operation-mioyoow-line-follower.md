<!--
Maintainer:   jeffskinnerbox@yahoo.com / www.jeffskinnerbox.me
Version:      0.0.1

# convert markdown .md to MS Word .docx
pandoc -f gfm theory-of-operation-mioyoow-line-follower.md -o theory-of-operation-mioyoow-line-follower.docx
-->


# Theory of Operation: MiOYOOW Line Following Robot Car Kit (TT Motor)

**Subject:** MiOYOOW / WHDTS D2-1 analog line-following robot car kit
**Scope:** Broad — complete system from sensors to wheels
**Target Audience:** High school students and volunteer makerspace instructors with minimal electronics background
**Date:** 2026-02-19

## 1. Overview

The MiOYOOW Line Following Robot Car Kit is a battery-powered, two-wheeled car that autonomously follows a dark line on a light surface using purely analog electronics — no microcontroller or software. The core operating principle is differential light sensing: two photoresistors (LDRs) mounted at the front of the car detect how much light reflects off the surface below. A white surface reflects more light (lowering LDR resistance), while a dark line absorbs light (raising LDR resistance). An LM393 dual comparator IC converts these resistance changes into on/off decisions for two DC gear motors — one per wheel. When both sensors see white, both motors run and the car drives straight. When one sensor crosses over the dark line, that side's motor stops while the opposite motor continues, steering the car back toward the line.

The system has five functional stages: illumination (white LEDs light the surface), sensing (LDRs detect reflected light), decision (LM393 comparator compares sensor voltage to an adjustable threshold), amplification (S8550 PNP transistors switch motor current), and actuation (TT gear motors drive the wheels). The entire circuit runs on 3V from two AA batteries and requires no programming — all behavior emerges from the analog feedback loop between sensors and motors.


## 2. Detailed Operation

### Step 1: Surface Illumination

When the power switch is closed, the two AA batteries supply approximately 3V DC to the circuit. Two white LEDs mounted at the front of the PCB, angled downward toward the surface, illuminate the area directly below the two LDR sensors. Each LED has a current-limiting resistor (1K ohm) in series to prevent excess current and burnout. The LEDs provide a consistent, known light source so the LDRs respond to surface reflectance rather than ambient lighting conditions. The light from these LEDs strikes the surface and bounces back toward the LDRs — how much bounces back depends on the surface color. This reflected light is the input to Step 2.

### Step 2: Reflectance Sensing via LDR Voltage Dividers

Each LDR (light-dependent resistor) is paired with a fixed resistor to form a voltage divider. An LDR is a component whose electrical resistance changes with the amount of light hitting its surface — bright light produces low resistance (roughly 1K–5K ohms), while darkness produces high resistance (100K ohms or more). In each voltage divider, the LDR and a fixed resistor (from the kit's resistor set) are connected in series across the 3V supply. The voltage at the junction between them — the "sensor voltage" — shifts as the LDR resistance changes.

- **Over a white surface:** The LED light reflects strongly, flooding the LDR with light. The LDR resistance drops, and the sensor voltage shifts toward one rail.
- **Over a dark line:** The line absorbs most of the light, so little reflects back. The LDR resistance rises sharply, and the sensor voltage shifts toward the opposite rail.

Each sensor channel produces a continuously varying analog voltage that represents "how white" the surface is below that sensor. These two voltages — one from the left sensor, one from the right — feed into Step 3.

### Step 3: Threshold Comparison via LM393 Dual Comparator

The [LM393][01] is an 8-pin IC containing two independent voltage comparators. A comparator is a circuit that compares two voltages and outputs a simple high or low signal — think of it as a referee that decides "is voltage A higher or lower than voltage B?" Each comparator has two inputs: a non-inverting input (+) and an inverting input (−).

For each sensor channel:
- One comparator input receives the **sensor voltage** from the LDR voltage divider (Step 2).
- The other input receives a **reference voltage** set by a 10K ohm potentiometer (adjustable knob). Turning the potentiometer changes this reference voltage, which sets the light/dark threshold — the sensitivity of the sensor.

The comparator's behavior is straightforward:
- If the sensor voltage crosses the threshold in the direction indicating "dark line detected," the comparator output goes **low** (pulled to ground internally via the LM393's open-collector output transistor).
- If the sensor voltage indicates "white surface," the comparator output goes **high** (pulled up toward the supply voltage through a pull-up resistor).

The LM393's open-collector output means it can only actively pull the output low (to ground). To produce a high output, an external pull-up resistor connects the output to the positive supply — when the internal transistor turns off, the resistor pulls the voltage high. This is important because it determines how the output interfaces with the transistor motor drivers in Step 4.

The two potentiometers allow the user to calibrate left and right sensors independently, compensating for differences in LDR sensitivity, LED brightness, or mounting height. The two comparator outputs — one per sensor channel — feed into Step 4.

### Step 4: Motor Switching via S8550 PNP Transistors

Each comparator output drives the base of an [S8550 PNP transistor][02] through a base resistor (which limits current into the transistor's base to a safe level). The S8550 is a PNP bipolar junction transistor — a three-terminal semiconductor device that acts as an electrically controlled switch. In a PNP transistor, current flows from emitter to collector when the base voltage is pulled sufficiently below the emitter voltage (roughly 0.6V below).

The key to understanding this stage is the interaction between the LM393's open-collector output and the PNP transistor. The comparator input wiring and the PNP switching logic work together so that:

- **White surface detected → comparator output goes LOW** (open-collector transistor pulls output to ground). This pulls the PNP base well below the emitter voltage, turning the transistor **on** — current flows from emitter to collector through the motor, and the wheel spins.
- **Dark line detected → comparator output goes HIGH** (open-collector transistor releases, pull-up resistor brings output near the supply rail). The PNP base rises close to the emitter voltage, turning the transistor **off** — no current flows, and the motor stops.

The net result for each channel:
- **White surface → motor ON** (both wheels spin, car goes straight)
- **Dark line detected → motor OFF on that side** (car turns toward the line)

The S8550 transistor can handle up to 1.5A of collector current, well above the TT motor's typical draw of 100–200mA under load at 3V. The 100µF electrolytic capacitors across the motor supply smooth out voltage spikes caused by the motor's brushes and the inductive kickback when the motor switches on and off, protecting the comparator IC from noise. The switched motor current from each transistor feeds into Step 5.

### Step 5: Differential Drive via TT Gear Motors

The two [TT gear motors][03] — yellow plastic-bodied DC motors with built-in 1:48 gear reduction — convert the electrical drive signals into mechanical motion. Each motor drives one wheel independently. At 3V, a TT motor spins at roughly 90–120 RPM under no load, drawing approximately 100–150mA. Under the load of pushing the car, speed drops and current increases.

The line-following behavior emerges from **differential drive** — the two wheels being controlled independently:

| Left Sensor | Right Sensor | Left Motor | Right Motor | Car Behavior |
|:------------|:-------------|:-----------|:------------|:-------------|
| White | White | ON | ON | Drives straight forward |
| Dark line | White | OFF | ON | Turns left (toward line) |
| White | Dark line | ON | OFF | Turns right (toward line) |
| Dark line | Dark line | OFF | OFF | Stops (both sensors on line) |

When the car drifts so that one sensor crosses the dark line, that side's motor stops while the other continues. This pivots the car back toward the line. As the sensor moves off the line and sees white again, the motor restarts, straightening the car. This continuous correction produces a characteristic zigzag path — the car oscillates back and forth across the line edge, constantly correcting. The speed and width of the zigzag depend on the potentiometer threshold settings, motor speed, sensor spacing, and line width.

### Step 6: Continuous Analog Feedback Loop

The entire system operates as a closed-loop feedback system with no software, timers, or stored instructions. The loop runs continuously and near-instantaneously (the LM393's response time is approximately 1.3 microseconds):

1. LEDs illuminate the surface (Step 1)
2. LDRs sense reflected light and produce a voltage (Step 2)
3. Comparators decide "line or no line" by comparing sensor voltage to threshold (Step 3)
4. Transistors switch motor power on or off (Step 4)
5. Motors turn wheels, moving the car to a new position (Step 5)
6. The new position changes what the sensors see → back to step 2

This feedback loop is what makes the car autonomous — it continuously senses, decides, and acts without any human input or stored program. The behavior is entirely reactive: the car responds to what it sees *right now*, with no memory of where it has been or prediction of where it is going. This is both the elegance and the limitation of pure analog control.


## 3. Block Diagram

```
    3V Battery Supply
         │
         ├──────────────────────────────────┐
         │                                  │
    ┌────┴─────┐                      ┌─────┴────┐
    │ White LED│ (left)               │White LED  │ (right)
    │ + 1K R   │                      │ + 1K R    │
    └────┬─────┘                      └─────┬─────┘
         │ light                            │ light
         v                                  v
    ┌─────────┐                       ┌──────────┐
    │  LDR    │ (left)                │   LDR    │ (right)
    │ + fixed │                       │  + fixed │
    │ resistor│                       │  resistor│
    └────┬────┘                       └────┬─────┘
         │ sensor voltage                  │ sensor voltage
         v                                 v
    ┌──────────────────────────────────────────┐
    │           LM393 Dual Comparator          │
    │                                          │
    │  ┌──────────┐        ┌──────────┐        │
    │  │Comparator│        │Comparator│        │
    │  │    A     │        │    B     │        │
    │  └────┬─────┘        └────┬─────┘        │
    │       │                   │              │
    └───────┼───────────────────┼──────────────┘
            │                   │
       ref from            ref from
       10K pot              10K pot
       (left)               (right)
            │                   │
            │ on/off            │ on/off
            v                   v
    ┌──────────────┐    ┌──────────────┐
    │ S8550 PNP    │    │ S8550 PNP    │
    │ Transistor   │    │ Transistor   │
    │ (left motor  │    │ (right motor │
    │  switch)     │    │  switch)     │
    └──────┬───────┘    └──────┬───────┘
           │                   │
           v                   v
    ┌──────────────┐    ┌──────────────┐
    │  TT Motor    │    │  TT Motor    │
    │  (left)      │    │  (right)     │
    │  + wheel     │    │  + wheel     │
    └──────────────┘    └──────────────┘
```


## 4. Key Parameters

| Parameter | Typical Value | Notes |
|:----------|:-------------|:------|
| Supply voltage | 3V DC | Two AA batteries (1.5V × 2) |
| Supply current (both motors running) | 200–400 mA | Depends on load and surface friction |
| LDR resistance (bright / white surface) | 1K–10K ohm | Varies by specific LDR and illumination |
| LDR resistance (dark / black line) | 50K–200K ohm | Much higher due to absorbed light |
| Comparator response time | ~1.3 µs | LM393 propagation delay |
| Transistor max collector current | 1.5A | S8550 absolute max; motors draw far less |
| Motor no-load speed at 3V | ~90–120 RPM | After 1:48 gear reduction |
| Motor no-load current at 3V | ~100–150 mA | Increases significantly under load |
| Motor stall current at 3V | ~0.5–1.1A | Varies by TT motor variant |
| Smoothing capacitors | 100 µF electrolytic | Absorb motor switching noise |
| Sensitivity adjustment | 10K ohm potentiometer | One per sensor channel |


## 5. Common Misconceptions

- **Misconception:** "The sensors detect the color of the line."
  **Reality:** The LDRs detect *reflectance* — how much light bounces back, not what color the surface is. A dark blue or dark green line would work nearly as well as black. The system only distinguishes "reflects a lot of light" from "reflects little light."

- **Misconception:** "The potentiometers control motor speed."
  **Reality:** The potentiometers set the *comparator threshold* — the light level at which the circuit decides "this is a dark line." They control sensitivity, not speed. Motor speed is fixed by the battery voltage.

- **Misconception:** "The car follows the center of the line."
  **Reality:** The car follows the *edge* of the line. It oscillates back and forth across the line boundary, constantly correcting. It has no way to know where the center is — it only knows whether each sensor is currently over dark or light surface.

- **Misconception:** "The LM393 is an amplifier."
  **Reality:** The LM393 is a *comparator* — it makes a yes/no decision, not a proportional amplification. Its output is either high or low, nothing in between. This is why the motors are either fully on or fully off, with no speed variation based on how far off the line the car has drifted.


## 6. Sources & References

[01]:https://www.ti.com/lit/ds/symlink/lm393.pdf
[02]:https://components101.com/transistors/s8850-pinout-equivalent-datasheet
[03]:https://www.adafruit.com/product/3777
