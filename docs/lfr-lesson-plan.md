# Lesson Plan: Evolving Design of a Line Following Robot

* **Organization:** [Makersmiths][01] — a community [makerspace][02] in Leesburg, Virginia
* **Format:** Hands-on workshop, 2 hours per class, weekly meetings
* **Audience:** Students ages 12–18 (adults welcome as helpers or independent learners)
* **Classes:** 8 core classes + up to 2 stretch classes (10 max)
* **Start Date:** June 15, 2026
* **Instructor:** 1 volunteer instructor who also develops pre-course software
* **Code Editor:** [Mu Editor][04] for all students
* **Reference:** See [Appendix A](#appendix-a-lesson-plan-development-prompt--qa) for the original development prompt and all instructor Q&A

---

## Table of Contents

* [Track Progression](#track-progression)
* [Soldering Plan](#soldering-plan)
* [Instructor-Provided Code Blocks](#instructor-provided-code-blocks)
* **Phase 1: Foundation — Build It, Make It Move (Classes 1–3)**
  * [Class 1 — Course Kickoff: MiOYOOW Demo & Chassis Assembly](#class-1--course-kickoff-mioyoow-demo--chassis-assembly)
  * [Class 2 — Upgrading the Brain: Pico W + Motor Driver + IR Sensors](#class-2--upgrading-the-brain-pico-w--motor-driver--ir-sensors)
  * [Class 3 — First Line Follower: Code, Flash, Test](#class-3--first-line-follower-code-flash-test)
* **Phase 2: Smart Control — Better Sensing, Speed Control, WiFi (Classes 4–7)**
  * [Class 4 — Sensor Array Upgrade](#class-4--sensor-array-upgrade)
  * [Class 5 — Variable Speed & Better Line Following](#class-5--variable-speed--better-line-following)
  * [Class 6 — WiFi Access Point & Browser Control UI](#class-6--wifi-access-point--browser-control-ui)
  * [Class 7 — Speed Sensors + Closed-Loop Feedback](#class-7--speed-sensors--closed-loop-feedback)
* **Phase 3: Autonomous — PID, Kalman, Q-Learning (Classes 8–10)**
  * [Class 8 — PID Controller: Tuning for Performance](#class-8--pid-controller-tuning-for-performance)
  * [Class 9* — Kalman Filter: Smoothing the Noise](#class-9--kalman-filter-smoothing-the-noise) *(stretch)*
  * [Class 10* — Q-Learning + Course Wrap-Up & Final Competition](#class-10--q-learning--course-wrap-up--final-competition) *(stretch)*
* [Appendix A: Lesson Plan Development Prompt & Q&A](#appendix-a-lesson-plan-development-prompt--qa)

---

## Track Progression

Line tracks are printed on standard 8.5 × 11 inch white paper tiles using the Line Track Designer tool. The testing area requires approximately 44 × 25.5 inches minimum with robot clearance on all sides.

| Class | Track Design | Rationale |
|:------|:-------------|:----------|
| 2 | No track — motor test only | Students test motors on tabletop (straight line, 3 ft) |
| 3 | Simple oval | Gentle curves, wide line — validates basic 2-sensor following |
| 4 | Oval + tighter curves | Tests sensor array improvement vs IR pair |
| 5 | Figure-8 | Medium curves + crossover — tests variable speed (slow on curves, fast on straights) |
| 6 | Same figure-8 | Focus is WiFi UI, not new track |
| 7 | Figure-8 + chicane | Add sharp S-curves — tests speed sensor feedback and consistency |
| 8 | Complex course | All elements: straights, gentle curves, sharp turns, S-curves — PID tuning |
| 9* | Same complex course | Kalman filter comparison on same track |
| 10* | Competition course | Instructor designs a final course for competition day |

> **Line width:** ¾ inch (19 mm) black line on white paper — standard LFR competition width. [VERIFY at first print]

---

## Soldering Plan

| What | When | Method |
|:-----|:-----|:-------|
| Pico W header pins | Pre-course (instructor prep) | Instructor pre-solders headers on all 6 Pico W boards |
| Motor leads to chassis | Class 1 (chassis assembly) | Students solder motor leads — guided intro to soldering |
| Battery holder leads | Class 2 | Solder or use pre-attached connector [VERIFY at purchase] |
| IR sensor pair wires | Class 2 | Breadboard + jumper wires |
| Sensor array (QTRX) | Class 4 | Header pins + breadboard jumpers |
| Speed sensor module | Class 7 | Breadboard + jumper wires |
| All other connections | Throughout | Breadboard + jumper wires |

> **Safety:** Students must wear protective eye gear during all soldering sessions. Soldering equipment is provided by [Makersmiths][01].

---

## Instructor-Provided Code Blocks

The instructor develops and tests all code blocks before the course begins. Students receive these as working templates to load, modify, and experiment with using the [Mu Editor][04].
Younger students (12–14) receive pre-written templates; older students (15–18) are encouraged to modify and extend them.

| Code Block | First Used | Functional Description |
|:-----------|:-----------|:-----------------------|
| Motor test script | Class 2 | Reads GPIO pins for sensor input, sets PWM signals for motor speed and direction; supports forward, stop, and turn commands |
| Basic line follower | Class 3 | Two-sensor if/else logic: left sensor detects line → turn right, right sensor detects line → turn left, both clear → go straight |
| Sensor array reader | Class 4 | Reads all 8 channels of the QTRX-MD-08RC array using RC timing, computes a weighted line position value (-1.0 to +1.0 scale) |
| Variable speed controller | Class 5 | Scales motor speed based on line position: centered = fast, off-center = slow; tunable speed parameters |
| WiFi Access Point + Browser UI | Class 6 | Pico W creates a WiFi AP with unique SSID per robot, hosts a webpage on port 80, displays live sensor data, accepts speed parameter adjustments via browser form |
| Speed sensor reader | Class 7 | Reads wheel speed from IR optocoupler modules via GPIO interrupts, calculates RPM per wheel, displays values in browser UI |
| Open-loop speed controller | Class 7 | Sets a target motor speed, measures actual speed via speed sensors, displays the difference; demonstrates open-loop limitations |
| PID controller | Class 8 | Implements proportional, integral, and derivative control of motor speed based on line position error; P, I, and D parameters adjustable in real time via browser UI |
| Kalman filter module | Class 9* | Filters noisy sensor array readings using a simplified Kalman filter; tunable process/measurement noise parameters via browser UI; before/after comparison mode |
| Q-Learning controller | Class 10* | States = discretized sensor readings, actions = motor speed pairs, reward = staying centered on line; trains on the track over multiple runs; replaces PID when trained |

---

## Phase 1: Foundation — Build It, Make It Move (Classes 1–3)

---

## Class 1 — Course Kickoff: MiOYOOW Demo & Chassis Assembly

> Design Sessions 1 & 2 · Phase 1: Foundation · Duration: 2 hours · Prerequisites: None

### 1. Class Overview

This is the first class of the course. Students meet the instructor and each other, learn what a line following robot is and why it matters, watch a live demonstration of the MiOYOOW Line Following Robot Car Kit, and then begin assembling their own robot from the Emo Smart Robot Car Chassis Kit.
By the end of this class, students will have a fully assembled chassis with motors, wheels, and battery holder — the mechanical foundation for every future upgrade. Students also solder motor leads to the chassis, which serves as their introduction to soldering.

### 2. Learning Goals

* Explain what a line following robot does and give one real-world example of where they are used
* Identify the mechanical components of the Emo Smart Robot Car Chassis Kit: motors, wheels, caster wheel, battery holder, frame plates
* Safely solder motor leads to the chassis motor terminals under instructor guidance
* Begin a build journal with a sketch of the assembled chassis and notes on what was learned

### 3. Preparation Checklist

* [ ] Pre-solder header pins onto all 6 Raspberry Pi Pico W boards — 30 min
* [ ] Assemble the MiOYOOW Line Following Robot Car Kit for demonstration — 45 min (do this days before)
* [ ] Test the MiOYOOW demo on a simple line track to confirm it works — 10 min
* [ ] Lay out 6 Emo Smart Robot Car Chassis Kits on workstations, one per student — 10 min
* [ ] Set up 2 soldering stations with soldering iron, solder, flux, solder wick, and solder sucker — 15 min
* [ ] Print a simple oval line track for MiOYOOW demo (4 × 3 tile layout) — 5 min
* [ ] Prepare a welcome handout or whiteboard with: course schedule, what students will build, WiFi password
* [ ] Have spare motor wires, screws, and standoffs available
* [ ] Prepare a brief slideshow or printout showing competitive LFR events

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Emo Smart Robot Car Chassis Kit | 1 | Base platform — students keep at course end |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| MiOYOOW Line Following Robot Car Kit | Pre-assembled instructor demo unit |
| Soldering iron, solder, flux, solder wick, solder sucker | Provided by Makersmiths |
| Protective eye gear | Students must bring or borrow |
| Printed oval line track | For MiOYOOW demo |
| Spare motor wires and chassis screws | In case of lost or damaged parts |

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

*First class — no prior material to review. Use this time for introductions.*

* Welcome students and parents/helpers; have everyone introduce themselves (name, age, one thing they want to learn)
* Course overview: 8 classes, build a robot that follows a line, each class adds new capabilities
* Set expectations: no grades, build journals instead of tests, friendly competitions, keep your robot at the end
* Mention the [Appendix A](#appendix-a-lesson-plan-development-prompt--qa) as background on how this course was designed
* **What to say:** "By the end of this course, your robot will be able to follow a line on its own, adjust its speed around curves, and even learn from experience. Today we start with the basics."
* **Time check:** Move on at 0:10 even if introductions are still going — they can continue informally during the build

#### 5b. Mini-Lecture (0:10–0:30)

*Topic: What is a line following robot? MiOYOOW demonstration.*

* **Live demo:** Place the MiOYOOW kit on the printed oval track and let it run. Let students watch it follow the line, lose the line, and recover
* **Key talking points (aim for 3–5 minutes each):**
  1. **What it does:** The robot uses sensors to detect a black line on a white surface and steers itself to stay on the line
  2. **How it works (MiOYOOW):** Two light-dependent resistors (LDRs) detect the line; analog comparators decide "turn left" or "turn right"; it is a simple on/off system with no brain — just wires and components
  3. **Limitations:** Only two sensors, no variable speed, can't handle sharp turns well, no programmability — you can't change its behavior without re-wiring
  4. **Why it matters:** Line following robots are used in warehouses (Amazon), factories (assembly lines), and there are [competitive LFR events][09] around the world
  5. **The design journey:** "Your robot will start simple like this one, but over the next 8 weeks we'll upgrade it with a programmable brain, better sensors, speed control, WiFi, and even machine learning"
* **Questions to ask students:**
  * "What do you think happens when the line curves sharply?"
  * "What would happen if we added more sensors?"
  * "How could we make it go faster without falling off the line?"
* **Common misconception:** Students may think the robot "sees" the line like a camera — clarify that the sensors only detect light vs. dark, not shapes
* **What to watch for:** Keep the demo engaging but brief — students are eager to build. If the MiOYOOW loses the line during demo, use it as a teaching moment about limitations

#### 5c. Guided Build (0:30–1:30)

*Activity: Emo Smart Robot Car Chassis Kit assembly + motor lead soldering.*

**Chassis Assembly (0:30–1:00, ~30 min):**

* Hand out one Emo Smart Robot Car Chassis Kit per student
* Walk through the [assembly guide][10] step by step — do each step together as a group
* **Assembly sequence:**
  1. Identify all parts: 2 frame plates (top and bottom), 2 DC motors, 2 wheels, 1 caster wheel, battery holder, screws, standoffs, wiring
  2. Mount the 2 DC motors to the bottom frame plate using the provided brackets and screws
  3. Attach the caster wheel to the rear of the bottom frame plate
  4. Press-fit the 2 drive wheels onto the motor shafts
  5. Mount the battery holder to the bottom plate (or between plates, depending on kit version)
  6. Attach standoffs and connect the top frame plate
* **Checkpoints:**
  * After step 2: "Hold up your bottom plate — I want to see both motors mounted"
  * After step 5: "Spin each wheel by hand — does the motor shaft turn freely?"
* **What to watch for:**
  * Motors mounted backwards (shaft facing wrong direction) — most common mistake
  * Over-tightening screws and cracking the acrylic frame
  * Caster wheel not seated properly — robot will wobble
  * Lost small screws — have spares ready

**Motor Lead Soldering (1:00–1:30, ~30 min):**

* **Safety first:** All students put on protective eye gear. Review soldering safety: hot iron, fumes, don't touch the tip
* Instructor demonstrates soldering one motor lead on the demo chassis
* **Soldering steps:**
  1. Tin the soldering iron tip
  2. Strip ~5 mm of insulation from the motor lead wire
  3. Hold the wire to the motor terminal
  4. Touch the iron to the joint, feed solder, remove iron — aim for a shiny, cone-shaped joint
  5. Repeat for the second wire on the same motor, then both wires on the other motor (4 joints total)
* Rotate students through 2 soldering stations (2–3 students per station at a time)
* While waiting for a soldering station, students work on their build journal (sketch the chassis)
* **What to watch for:**
  * Cold solder joints (dull, blobby) — reheat and add flux
  * Solder bridges between terminals — use solder wick to remove excess
  * Students holding the iron too long on the motor terminal — can damage the motor
  * Burns — have a first aid kit accessible
* **Hardware checkpoint:** Each student's chassis should have 4 soldered motor connections. Instructor visually inspects each joint before the student moves on.

#### 5d. Testing & Documentation (1:30–1:50)

* **Mechanical test:** Students spin each wheel by hand to verify motors turn freely and connections are solid
* No electrical test today — the Pico W and motor driver are added in Class 2
* **Build journal entry:** Students sketch their assembled chassis, label the parts (motors, wheels, caster, frame, battery holder), and write 2–3 sentences about what they learned
* **What to say:** "Your journal is yours — there's no right or wrong way to do it. A quick sketch and a few notes is perfect. This becomes your reference for the whole course."
* Walk around and check journals, ask questions, give encouragement

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "Today you assembled your chassis and soldered your first connections. Your robot has a body and muscles (motors) but no brain yet."
* **Preview Class 2:** "Next week we add the brain — the Raspberry Pi Pico W — plus a motor driver board, power supply, and your first sensors. By the end of Class 2, your robot will move under its own power."
* **Take-home:** Continue your build journal. Look up [competitive LFR events][09] if curious. Bring your laptop next week with a USB port available.
* Remind students to bring protective eye gear to every class
* Store robots safely at Makersmiths (or students take home — instructor decides)

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Motor shaft doesn't spin freely | Motor bracket screws too tight | Loosen bracket screws slightly; ensure motor body isn't pinched |
| Wheel won't press onto motor shaft | Shaft/wheel size mismatch | Press firmly; if still stuck, check you have the correct wheel for that shaft |
| Caster wheel wobbles excessively | Not fully seated in mount | Remove and reseat; check that the ball moves freely |
| Cold solder joint (dull, blobby) | Iron not hot enough or moved too soon | Reheat the joint, add a small amount of flux, and reflow |
| Solder bridge between motor terminals | Too much solder applied | Use solder wick to remove excess; reheat and clean |
| Acrylic frame plate cracked | Over-tightened screws | Use a spare plate if available; finger-tight is enough |
| Student burned by soldering iron | Touched hot tip or joint | Apply cold water, use first aid kit; review safety rules with class |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Pair each younger student with an adult helper for chassis assembly
* Provide a printed, labeled diagram of the assembled chassis showing where each part goes
* For soldering: instructor holds the wire and iron position, student feeds the solder (assisted soldering)
* Build journal: provide a template with labeled boxes ("Sketch your chassis here," "What did you learn?")

**Older students (15–18) and adults:**

* Encourage them to assemble from the parts and instructions before looking at the step-by-step guide — learn by figuring it out
* For soldering: let them attempt independently after watching the demo, instructor supervises
* Challenge extension: sketch a wiring diagram predicting how the Pico W and motor driver will connect (preview of Class 2)
* Ask them to help younger students if they finish early

### 8. Assessment

No milestone assignment or competition this class. Assessment begins at Class 2 with Mini-Challenge #1.

Build journals are reviewed informally — confirm every student started one.

### 9. Instructor Tips

* **Pacing:** Chassis assembly takes longer than you think. The biggest time sink is students struggling with small screws and standoffs. Have a small Phillips-head screwdriver for each workstation.
* **Soldering rotation:** With 5 students and 2 stations, plan for ~6 minutes per student at the station. Start the rotation early. Students waiting can work on journals or study the MiOYOOW demo unit.
* **Energy management:** The MiOYOOW demo is the hook — make it exciting. Let students hold it, examine the underside, trace the wires. Once they've seen it work, they're motivated to build their own.
* **Parents as helpers:** Direct parents to assist with chassis assembly but let the student do the soldering (with supervision). Building confidence matters more than speed.
* **If you run long:** Soldering can slide into Class 2 if needed. The chassis must be assembled today; motor lead soldering can be finished at the start of Class 2 if time runs out.
* **MiOYOOW backup:** Charge the MiOYOOW batteries the night before. Bring spare batteries. Test it on the track before students arrive.

### 10. Resources & References

* [Emo Smart Robot Car Chassis Assembly Guide][10] — step-by-step chassis build instructions
* [Advanced Line Following Robot][09] — example of a capable LFR (Instructables)
* [Makersmiths][01] — course host makerspace
* [What is a Makerspace?][02] — overview of makerspaces for students new to the concept

---

## Class 2 — Upgrading the Brain: Pico W + Motor Driver + IR Sensors

> Design Session 3 · Phase 1: Foundation · Duration: 2 hours · Prerequisites: Class 1 (chassis assembled, motor leads soldered)

### 1. Class Overview

Students install the electronic brain of the robot: the Raspberry Pi Pico W seated on the Robotics Motor Driver Board.
Power comes from two sources: a 9V battery clip (powers the Kitronik board and Pico W) and the 8×AA battery holder through a 5V buck converter (provides 5V for sensors).
An IR emitter/phototransistor pair provides basic line sensing.
They flash [CircuitPython][03] onto the Pico W, install the [Mu Editor][04] on their laptops, and write their first program — reading sensor values and making the motors spin. By the end, students have a powered, programmable robot that can drive in a straight line.

**Software prerequisites:** Motor test script (instructor-provided code block) must be ready.

**Track requirements:** No line track needed — motor test uses a tabletop straight line (3 ft measured with tape).

### 2. Learning Goals

* Install the Raspberry Pi Pico W onto the Robotics Motor Driver Board and seat it on the chassis
* Wire the 8×AA battery holder and 5V buck converter to power the system
* Connect the IR emitter/phototransistor pair to the Pico W for basic line sensing
* Flash [CircuitPython][03] onto the Pico W and verify it works using the [Mu Editor][04] serial console
* Run the motor test script to make the robot drive forward, stop, and turn
* Document the wiring in the build journal

### 3. Preparation Checklist

* [ ] Verify all 6 Pico W boards have pre-soldered headers — should be done pre-course
* [ ] Pre-test one complete assembly (Pico W + motor driver + battery + buck converter + IR sensor) to confirm everything works — 60 min (do this days before)
* [ ] Download [CircuitPython UF2 file][05] for Pico W onto a USB drive as backup in case WiFi is slow — 5 min
* [ ] Prepare 6 sets of components at workstations: Robotics Motor Driver Board, 8×AA battery holder (with 8 AA batteries installed), 9V battery clip connector, 5V buck converter module, IR emitter/phototransistor pair, 400-pin solderless prototype board, jumper wires — 15 min
* [ ] Install [Mu Editor][04] on the instructor laptop and verify it connects to a Pico W — 10 min
* [ ] Print a wiring diagram showing all connections for this class (one per student) — 5 min
* [ ] Lay out a 3-foot straight line on the tabletop with electrical tape for the motor test challenge
* [ ] Have the motor test script ready on USB drive and/or printed as a handout
* [ ] Set up 2 soldering stations in case battery holder leads need soldering [VERIFY at purchase]
* [ ] Ensure Makersmiths WiFi is working (needed for CircuitPython download)

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Raspberry Pi Pico W | 1 | Pre-soldered headers (instructor prep) |
| Robotics Motor Driver Board | 1 | Pico W seats directly into this board |
| 9V Battery Clip Connector | 1 | Powers the Kitronik motor driver board (9V within its 3.0–10.8V range); board's on-board regulator provides 3.3V to Pico W |
| 8×AA Battery Holder | 1 | 12V power source; feeds the 5V buck converter for sensor power |
| 5V Buck Converter Module | 1 | Steps 12V from 8×AA holder down to 5V for sensors (QTRX array, speed sensors in later classes) |
| IR Emitter/Phototransistor Pair | 1 | Left + right line detection sensors |
| 400-Pin Solderless Prototype Board | 1 | Breadboard for wiring connections |
| Jumper wires (assorted M-M, M-F) | ~20 | For all connections |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| AA batteries | 8 per student, from shared supply (48 total) |
| USB cables (micro-USB or USB-C, depending on Pico W variant) | For flashing CircuitPython |
| Soldering stations | In case battery holder leads need soldering |
| Electrical tape | For marking 3-foot straight line on tabletop |

**Student-Provided:**

| Item | Notes |
|:-----|:------|
| Laptop computer | Windows, Mac, or Linux — no Chromebooks |
| Protective eye gear | For any soldering needed |

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Quick recap of Class 1: "You built the body. Today we add the brain, power, and senses."
* Check build journals — did everyone sketch their chassis?
* Ask: "Who looked up LFR competitions? Find anything interesting?"
* Address any chassis assembly issues (loose screws, wobbly caster) — fix now before adding electronics
* **Time check:** Move on at 0:10. Any remaining chassis fixes can happen during the build.

#### 5b. Mini-Lecture (0:10–0:30)

*Topic: The electronic brain — Pico W, motor driver, power, and sensors.*

* **Key talking points:**
  1. **The Pico W is the brain:** It's a tiny computer that runs [CircuitPython][03] — you write code, it controls the robot. Unlike the MiOYOOW's analog circuits, this brain is programmable.
  2. **The motor driver translates brain signals to muscle power:** The Pico W can't power motors directly — the Robotics Motor Driver Board amplifies its tiny signals into enough power to spin the motors. It also lets us control speed (via PWM) and direction.
  3. **Power system:** Two power sources work together.
     The 9V battery clip powers the Kitronik motor driver board directly (9V is within its rated range) — the board's built-in regulator provides 3.3V to the Pico W, and the H-bridge drivers send 9V to the motors.
     The 8×AA battery holder (12V) feeds the 5V buck converter, which provides 5V power for sensors on the breadboard.
     Think of it like two power adapters — one for the brain and muscles, one for the eyes.
  4. **IR sensor pair — the robot's eyes:** The IR emitter shines invisible light down at the surface. The phototransistor detects how much bounces back.
     White surface = lots of reflection. Black line = little reflection. Two sensors (left and right) let the robot detect which side of the line it's on.
  5. **MiOYOOW comparison:** The MiOYOOW uses LDRs (light-dependent resistors) with analog comparators — same basic idea, but not programmable. Our IR pair connects to the Pico W, so we can write any logic we want.
* **Demo:** Show the IR sensor pair up close. Shine it on white paper vs. black tape and display the readings on the serial console (instructor's pre-tested unit).
* **Questions to ask:**
  * "Why do we need two sensors instead of one?"
  * "What happens if the line is directly between the two sensors?"
  * "Why can't the Pico W power the motors directly?" (Hint: it only outputs ~3.3V at a few milliamps)

#### 5c. Guided Build (0:30–1:30)

*Activity: Full electronic assembly + CircuitPython flashing + first code.*

**Step 1 — Seat the Pico W on the Motor Driver Board (0:30–0:40, ~10 min):**

* Align the Pico W header pins with the Motor Driver Board sockets
* Press down firmly and evenly — don't bend pins
* **Checkpoint:** "Wiggle the Pico W gently — it should be snug, not loose"
* Mount the Motor Driver Board assembly onto the chassis top plate using standoffs or adhesive [VERIFY mounting method]

**Step 2 — Wire the Power System (0:40–0:55, ~15 min):**

* Connect 9V battery clip leads to the Kitronik Motor Driver Board power input (9V is within the board's 3.0–10.8V rated range)
* Wire the 8×AA battery holder to the 5V buck converter; buck converter output goes to the breadboard 5V rail for sensor power
* **Wiring detail:**
  * 9V clip RED → Kitronik Motor Driver Board VIN+
  * 9V clip BLACK → Kitronik Motor Driver Board GND
  * 8×AA holder RED → Buck converter IN+
  * 8×AA holder BLACK → Buck converter IN-
  * Buck converter OUT+ → Breadboard 5V rail (powers sensors in this and future classes)
  * Buck converter OUT- → Breadboard GND rail
  * Breadboard GND rail → Pico W GND (common ground)
* **Critical safety check:** Do NOT connect batteries yet. Verify all wiring first. Instructor inspects each student's wiring before power-on.
* **What to watch for:** Reversed polarity (will damage components), loose connections, buck converter output not set to 5V (some modules need adjustment via trim pot), 12V from 8×AA must NOT connect directly to the Kitronik board (exceeds its 10.8V max rating)

**Step 3 — Connect IR Sensor Pair (0:55–1:05, ~10 min):**

* Mount IR emitter/phototransistor pair under the chassis, facing down, ~5–10 mm above the surface
* Wire to breadboard and then to Pico W GPIO pins:
  * Left sensor signal → GP2 (digital I/O)
  * Right sensor signal → GP3 (digital I/O)
  * Sensor VCC → 3.3V from Pico W
  * Sensor GND → GND
* **Checkpoint:** "Look under your chassis — can you see the IR emitters glow faintly?" (Some IR LEDs have a faint red glow visible to cameras)

**Step 4 — Flash CircuitPython (1:05–1:15, ~10 min):**

* Connect Pico W to laptop via USB cable
* Hold BOOTSEL button while plugging in — Pico W appears as a USB drive called "RPI-RP2"
* Drag the [CircuitPython UF2 file][05] onto the drive — it reboots and reappears as "CIRCUITPY"
* Open [Mu Editor][04], select CircuitPython mode, verify the serial console shows the REPL prompt (`>>>`)
* **What to watch for:**
  * "RPI-RP2" drive doesn't appear → BOOTSEL button not held during plug-in; retry
  * Mu Editor doesn't detect the board → check USB cable (some are charge-only, not data)
  * Wrong CircuitPython version → ensure the UF2 is for Pico W specifically, not plain Pico

**Step 5 — Run Motor Test Script (1:15–1:30, ~15 min):**

* Load the instructor-provided motor test script onto the Pico W via Mu Editor
* **Motor test script — functional description:**
  * **What it does:** Reads GPIO pin states for the IR sensors, sets PWM signals for motor speed and direction through the motor driver board
  * **Inputs:** IR sensor analog values (left and right), button or serial command to start/stop
  * **Outputs:** PWM signals to motor driver for left and right motors (speed 0–100%, direction forward/reverse)
  * **Commands:** `forward` (both motors forward), `stop` (both motors off), `left` (left motor slower), `right` (right motor slower)
  * **How students interact:** Run the script, observe motor behavior, modify speed values in the code to see the effect
* Disconnect USB, connect battery power
* **Hardware checkpoint:** Robot drives forward when the script runs. Both wheels spin in the correct direction at roughly the same speed. If one wheel spins backward, swap its motor wire connections.
* **What to watch for:** Motors not spinning (check battery holder switch, verify power wiring), one motor spinning backward (swap motor leads), robot veering hard to one side (motor speed imbalance — adjust PWM values in code)

#### 5d. Testing & Documentation (1:30–1:50)

* **Mini-Challenge #1: Motor Test** — Who can make their robot drive in a straight line for 3 feet?
  * Mark a 3-foot line on the tabletop with electrical tape
  * Students place their robot at one end, run the motor test script, see how straight it goes
  * Multiple attempts allowed — students can adjust motor speed values between runs
  * **Competition rules:** Best of 3 attempts, measure deviation from the straight line at the 3-foot mark
  * **Age brackets:** 12–14, 15–18, Adults (if enough per bracket)
  * **Awards:** Recognition only — "Straightest Drive" award
  * Keep it fun: celebrate everyone who got their robot moving at all
* **Build journal:** Document the wiring (sketch the circuit), note which GPIO pins are used, record motor test results

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "Your robot has a brain, power, and basic senses. It can drive, but it can't follow a line yet."
* **Preview Class 3:** "Next week we write the line-following logic — the code that reads your sensors and decides which way to turn. We'll test on a real line track for the first time."
* **Take-home:** Review the motor test script in Mu Editor. Try changing the speed values. What happens if you make one motor faster than the other?
* Students should ensure [Mu Editor][04] is working on their laptops before Class 3

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Pico W not recognized by computer | Bad USB cable (charge-only) | Try a different USB cable — must be a data cable |
| "RPI-RP2" drive doesn't appear | BOOTSEL not held during plug-in | Unplug, hold BOOTSEL, plug in again |
| CircuitPython won't flash | Wrong UF2 file (plain Pico vs Pico W) | Download the Pico W-specific UF2 from [circuitpython.org][03] |
| Mu Editor doesn't detect board | Wrong mode selected | Select "CircuitPython" mode in Mu's mode selector |
| Motors don't spin | Battery holder switch off or batteries dead | Check switch, replace batteries, verify power LED on motor driver |
| One motor spins backward | Motor leads swapped | Swap the two wires on that motor's terminal |
| Robot veers hard to one side | Unequal motor speeds | Adjust PWM values in code to compensate; check for mechanical drag |
| IR sensor reads constant value | Sensor not wired correctly or too far from surface | Check wiring; adjust sensor height to 5–10 mm above surface |
| Buck converter outputs wrong voltage | Module not adjusted | Use multimeter to verify 5V output; adjust trim pot if present |
| Breadboard connections intermittent | Jumper wires not fully seated | Press jumper wires firmly into breadboard; use shorter wires |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a color-coded wiring diagram with each wire labeled (e.g., "RED wire from battery → VIN+")
* Pre-strip and pre-tin wire ends if soldering is needed for battery connections
* For CircuitPython flashing: walk through each step on the projector while students follow along
* For the motor test script: provide the code pre-loaded on a USB drive — students copy it to CIRCUITPY
* Pair with an adult helper for power system wiring (reversing polarity can damage the Pico W)

**Older students (15–18) and adults:**

* Give them the wiring schematic (not color-coded) and let them figure out the connections
* Challenge: modify the motor test script to add a "spin in place" command (one motor forward, one reverse)
* Ask them to read the sensor values in the serial console and explain what they observe (white surface vs. dark surface)
* Encourage them to read the [Raspberry Pi Pico W datasheet][32] to understand the GPIO pin layout

### 8. Assessment

**Mini-Challenge #1: Motor Test** — evaluated during the Testing & Documentation segment (see 5d above).

No milestone assignment this class.

### 9. Instructor Tips

* **Power-on anxiety:** The first time batteries go in is stressful. Do a "power-on parade" — inspect each robot's wiring, then power them on one at a time with the class watching. This prevents damage and creates excitement.
* **USB cable trap:** Charge-only USB cables are the #1 frustration. Bring 6+ known-good data cables. Label them "DATA" with tape.
* **Mu Editor install:** Some school-managed laptops block software installation. Have students install Mu Editor at home before class. Bring a spare laptop as backup.
* **Motor direction:** If both motors spin but the robot goes backward, both motor connections are reversed — swap both pairs. This is very common and not a failure.
* **Battery life:** 8×AA alkaline batteries last ~2–4 hours of active use. Have spare batteries ready. Remind students to switch off the battery holder when not testing.
* **9V Battery Clip Connector:** Powers the Kitronik motor driver board directly (9V is within the board's 3.0–10.8V input range). The board's on-board 3.3V regulator then powers the Pico W. Do NOT use the 12V 8×AA holder for this — 12V exceeds the board's 10.8V maximum.

### 10. Resources & References

* [CircuitPython][03] — official CircuitPython site
* [CircuitPython Installation on Pico W][05] — how to flash CircuitPython
* [Mu Editor Installation][04] — getting started with Mu Editor
* [Raspberry Pi Pico W Datasheet][32] — pinout and specifications
* [Circuit Canvas][08] — online tool for creating circuit wiring diagrams

---

## Class 3 — First Line Follower: Code, Flash, Test

> Design Sessions 4 & 5 · Phase 1: Foundation · Duration: 2 hours · Prerequisites: Class 2 (Pico W flashed, motors working, IR sensors connected)

### 1. Class Overview

Students write their first line-following algorithm — a simple two-sensor if/else logic that steers the robot based on IR sensor readings. They flash the code and test on a printed oval line track for the first time, observing the robot actually follow a line.
Students explore the strengths and weaknesses of the two-sensor approach, compare performance to the MiOYOOW demo from Class 1, and discuss what improvements would help. This class concludes Phase 1 with the Foundation Complete milestone assignment.

**Software prerequisites:** Basic line follower code block (instructor-provided) must be ready.

**Track requirements:** Simple oval — gentle curves, wide line. Print using the Line Track Designer tool on standard 8.5 × 11 inch paper tiles.

### 2. Learning Goals

* Explain the logic of a two-sensor line-following algorithm in plain language
* Load and run the basic line follower code block on the Pico W using Mu Editor
* Test the robot on a printed oval line track and observe its behavior
* Identify at least two weaknesses of the two-sensor design (wobble, can't handle sharp turns, no speed control)
* Complete the Phase 1 milestone assignment: robot follows a line, build journal documents the journey

### 3. Preparation Checklist

* [ ] Print the simple oval line track on standard 8.5 × 11 inch paper (4 × 3 tile layout, ¾" black line) — 10 min
* [ ] Lay the track on the flat floor area at Makersmiths, tape tiles together so they don't shift — 10 min
* [ ] Test the basic line follower code block on the instructor's robot to confirm it works on the printed track — 15 min
* [ ] Prepare the basic line follower code block on USB drive and as a printed handout with annotations — 5 min
* [ ] Have the MiOYOOW demo unit charged and ready for comparison run — 5 min
* [ ] Bring spare batteries, jumper wires, and IR sensor pairs in case of failures
* [ ] Set up a whiteboard or projector to display the line-following logic as a flowchart

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 2 | 1 | Chassis + Pico W + motor driver + batteries + IR sensors — all from prior classes |
| Laptop with Mu Editor | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed oval line track | 4 × 3 tile layout on floor |
| MiOYOOW demo unit | For comparison run |
| Spare AA batteries | Replacements for dead batteries |
| Spare jumper wires and IR sensor pairs | In case of hardware failures |

> No new hardware is introduced this class. Students use components from Classes 1–2.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 2: "You have a robot with a brain, power, and two eyes (IR sensors). Last week it could drive straight. Today it learns to follow a line."
* Quick check: "Did anyone experiment with the motor test script at home? What did you discover?"
* Verify all robots are functional: motors spin, sensors read values, Mu Editor connects. Fix any issues from Class 2 now.
* **Time check:** If more than 2 robots have issues, split the class — helpers fix hardware while the instructor starts the mini-lecture with functional robots.

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: How two-sensor line following works.*

* **Draw the logic on the whiteboard as a flowchart:**

  ```text
  Read left sensor, Read right sensor
           |
    Left sees line? ──Yes──→ Turn RIGHT
           |
           No
           |
    Right sees line? ──Yes──→ Turn LEFT
           |
           No
           |
      Go STRAIGHT
  ```

* **Key talking points:**
  1. **Binary decisions:** Each sensor reports "I see the line" or "I don't see the line." That's only 4 possible combinations: both off (straight), left on (turn right), right on (turn left), both on (on a wide section or lost).
  2. **Why it wobbles:** The robot can't see *how far* off the line it is — only that it's off. So it over-corrects, then over-corrects back. This is called "bang-bang" control.
  3. **Comparison to MiOYOOW:** The MiOYOOW does exactly this same logic, but with analog components instead of code. Our advantage: we can change the logic with software.
  4. **What could be better?** More sensors would tell us *how far* off the line we are. Variable speed would let us go faster on straights and slower on curves. We'll add both in future classes.
* **Questions to ask:**
  * "If both sensors see the line, what should the robot do?"
  * "What happens on a sharp curve where both sensors are off the line?"
  * "How would you make the robot go faster?"

#### 5c. Guided Build (0:25–1:25)

*Activity: Load line follower code, calibrate sensors, test on the track.*

**Step 1 — Load the Basic Line Follower Code (0:25–0:40, ~15 min):**

* Distribute the code block via USB drive or have students type it from the printed handout
* **Basic line follower — functional description:**
  * **What it does:** Continuously reads left and right IR sensor values, compares each to a threshold, and sets motor speeds/directions to steer the robot along a black line on a white surface
  * **Inputs:** Digital readings from left IR sensor (GP2) and right IR sensor (GP3); a configurable threshold value that separates "line detected" from "no line"
  * **Outputs:** PWM signals to left and right motors via the motor driver board — forward, turn left, turn right, or stop
  * **Logic:** If left sensor < threshold (sees dark line), slow/stop left motor and speed up right motor (turn right). If right sensor < threshold, do the opposite. If neither sees the line, both motors forward. If both see the line, both motors forward (on wide section).
  * **How students interact:** Modify the threshold value to calibrate for their specific sensor height and lighting conditions. Adjust motor speed values to find a balance between speed and stability.
  * **Key parameters to modify:** `THRESHOLD` (sensor reading that separates black from white), `SPEED` (base motor speed), `TURN_SPEED` (motor speed during turns)
* Walk through the code line by line on the projector — explain each section
* Students save the code as `code.py` on the CIRCUITPY drive

**Step 2 — Calibrate Sensors (0:40–0:55, ~15 min):**

* Place robot on white paper and read sensor values in Mu Editor serial console → note the "white" reading
* Place robot with sensors over the black line → note the "black" reading
* Set the `THRESHOLD` to the midpoint between white and black readings
* **What to say:** "Every robot will have slightly different sensor readings because of mounting height and ambient light. That's why we calibrate."
* **What to watch for:** Sensors mounted too high (readings too similar for black vs. white), sensors at an angle (inconsistent readings), ambient light from windows affecting readings

**Step 3 — Test on the Oval Track (0:55–1:25, ~30 min):**

* Move to the floor track area. Students take turns testing, 2–3 robots on the track at a time.
* **First run:** Just observe. Does it follow the line? Where does it lose the line?
* **Second run:** Adjust `THRESHOLD` and `SPEED` values based on observations
* **Third run:** Try to complete a full lap
* Encourage students to observe each other's robots — "What's different about theirs? Why does it follow better/worse?"
* **Run the MiOYOOW on the same track** for direct comparison — students should see similar behavior (wobble, occasional line loss)
* **Group discussion (last 5 minutes of build time):**
  * "What works well with two sensors?"
  * "What doesn't work?" (Expected answers: wobbles, loses the line on curves, can't go fast, no speed adjustment)
  * "What would make it better?" (More sensors, variable speed, smarter logic)
  * "How does your robot compare to the MiOYOOW from Class 1?"

#### 5d. Testing & Documentation (1:25–1:50)

* **Mini-Challenge #2: First Run** — Complete one lap of the oval test track (any speed, just finish!)
  * Multiple attempts allowed — best run counts
  * No timing yet — the challenge is simply completing a full lap without leaving the track
  * Age brackets: 12–14, 15–18, Adults
  * Awards: "First Lap" recognition for everyone who completes a lap; "Smoothest Run" for least wobble
  * Celebrate every robot that moves toward the line, even if it doesn't complete a lap — this is the first real test
* **Milestone Assignment: Phase 1 — Foundation Complete:**
  * Robot assembled, programmed, and follows a line
  * Build journal entry with: wiring diagram (from Class 2), code description (what each section does), test observations (what worked, what didn't, sensor calibration values, lap results)
  * **What "complete" looks like:** The robot attempts to follow the line. It doesn't need to be perfect — wobbling is expected and fine. The journal documents the journey, not perfection.
  * **Instructor review:** Walk around during the documentation period, check journals, ask each student "What was the hardest part?" and "What would you change?" — this is feedback, not grading.

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "Your robot follows a line! It wobbles, it might lose the line on curves, but it works. That's exactly how real engineering goes — get a basic version working, then improve it."
* **Preview Class 4:** "Next week we replace those two sensors with an 8-sensor array. Instead of 'I see the line' or 'I don't,' the robot will know exactly where the line is. This is the single biggest upgrade in the course."
* **Phase 1 complete:** Congratulate students — they built a working line-following robot in 3 classes.
* **Take-home:** Finish Phase 1 build journal entry if not completed in class.

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Robot doesn't respond to the line at all | Threshold value wrong | Read raw sensor values on serial console; recalibrate threshold |
| Robot oscillates wildly (extreme wobble) | Turn speed too high or threshold too sensitive | Reduce `TURN_SPEED`; widen the threshold gap |
| Robot runs off the track on curves | Sensors too far apart or too high | Adjust sensor mounting; lower sensors closer to the track surface |
| Robot follows the line but goes backward | Motor direction reversed in code | Swap the motor direction values in the code (or swap motor wires) |
| Sensor reads the same value on black and white | Sensor too far from surface or dead | Lower sensor to 5–10 mm; try swapping with a spare IR pair |
| Robot stops and won't move | Battery depleted | Replace AA batteries; check battery holder switch |
| Code error in Mu Editor | Typo in code | Compare line by line against the printed handout; check indentation |
| Track tiles shift during testing | Tiles not secured | Tape all tile edges to the floor |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide the code pre-loaded on USB drive — they copy it to CIRCUITPY and focus on calibration and testing
* Use the annotated printout that highlights the 3 values they should change (THRESHOLD, SPEED, TURN_SPEED) with suggested ranges
* Pair with a helper for sensor calibration — reading serial console values can be confusing at first
* Build journal: provide a template — "My sensor reads ***on white and*** on black. My threshold is ___."

**Older students (15–18) and adults:**

* Have them type the code from the handout rather than copying from USB — better for understanding
* Challenge: add a "both sensors see the line" behavior (e.g., speed up because you're on a wide section)
* Challenge: add a "both sensors see white" timeout — if the robot loses the line for more than 1 second, stop and spin in place to search
* Ask them to predict what will happen before each test run and compare prediction to reality

### 8. Assessment

**Mini-Challenge #2: First Run** — see section 5d above.

**Milestone Assignment: Phase 1 — Foundation Complete** — see section 5d above. Reviewed informally during class; students who need more time can finish the journal entry at home.

### 9. Instructor Tips

* **Track matters:** A poorly printed track causes more frustration than any code bug. Test the track yourself beforehand. Ensure the line is solid black, consistent width, and the tiles align without gaps.
* **Calibration is the lesson:** Don't skip it. The process of reading raw values and setting a threshold teaches how sensors actually work — this is more valuable than the line following itself.
* **Comparison moment:** Running the MiOYOOW on the same track as student robots is a powerful teaching moment. Students see their robot does roughly the same thing — validating their work — and also see the same limitations, motivating the upgrades ahead.
* **Don't chase perfection:** Some robots won't complete a full lap today. That's fine. The goal is understanding, not perfect performance. Celebrate partial success.
* **Managing the track:** With 5–6 robots, track time is limited. Run 2–3 robots simultaneously if the track is wide enough, or set up a rotation with a timer (3 minutes per student).
* **Phase 1 milestone:** Keep it informal. Walk around, look at journals, ask questions. If a student's robot follows the line at all and they wrote about it, they pass the milestone.

### 10. Resources & References

* [CircuitPython][03] — official CircuitPython site
* [Mu Editor Installation][04] — getting started with Mu Editor
* [Advanced Line Following Robot][09] — Instructables guide (good reference for students curious about next steps)
* [Make a FAST Line Follower Robot Using PID!][23] — preview of PID-based LFR (for curious older students)

---

## Phase 2: Smart Control — Better Sensing, Speed Control, WiFi (Classes 4–7)

---

## Class 4 — Sensor Array Upgrade

> Design Session 6 · Phase 2: Smart Control · Duration: 2 hours · Prerequisites: Class 3 (basic line follower working, Phase 1 milestone complete)

### 1. Class Overview

Students remove the IR emitter/phototransistor pair and replace it with the QTRX-MD-08RC Reflectance Sensor Array — an 8-channel sensor that provides precise line position data instead of simple left/right detection.
They load the sensor array reader code block, calibrate the array, and test on a track with tighter curves.
This is the single biggest upgrade in the course: the robot goes from knowing "the line is somewhere to my left" to knowing "the line is exactly 3.2 mm to my left." Students observe dramatically smoother line following compared to the two-sensor approach.

**Software prerequisites:** Sensor array reader code block (instructor-provided) must be ready.

**Track requirements:** Oval + tighter curves — tests sensor array improvement vs IR pair. Print a new track or modify the Class 3 oval by adding tighter corners.

### 2. Learning Goals

* Remove the IR sensor pair and install the QTRX-MD-08RC Reflectance Sensor Array
* Explain how the 8-sensor array provides position data — "8 tiny eyes instead of 2"
* Run the sensor array reader code block and interpret the line position value (-1.0 to +1.0 scale)
* Test on the tighter-curve track and compare performance to the two-sensor approach from Class 3
* Articulate why more sensor data enables better control

### 3. Preparation Checklist

* [ ] Print the oval + tighter curves track on 8.5 × 11 inch paper (4 × 3 tile layout) — 10 min
* [ ] Lay the track on the flat floor area and tape tiles down — 10 min
* [ ] Pre-test the sensor array reader code block on the instructor's robot with the QTRX array — 20 min
* [ ] Prepare 6 QTRX-MD-08RC Reflectance Sensor Arrays with header pins pre-soldered (or verify they come with headers) [VERIFY at purchase]
* [ ] Prepare wiring diagrams for the QTRX array → Pico W connections (one per student) — 10 min
* [ ] Have the sensor array reader code block on USB drive and as printed handout
* [ ] Bring spare jumper wires and header pins
* [ ] Keep the Class 3 oval track available for side-by-side comparison if floor space permits

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| QTRX-MD-08RC Reflectance Sensor Array | 1 | 8-sensor array; replaces IR pair |
| Header pins (if not pre-attached to QTRX) | 1 set | From shared supplies |
| Jumper wires (M-F) | ~10 | For array-to-breadboard connections |

**Per Student (from prior classes):**

| Component | Notes |
|:----------|:------|
| Assembled robot with Pico W, motor driver, batteries | From Classes 1–3 |
| IR Emitter/Phototransistor Pair | Will be removed this class — students keep as spare |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed oval + tighter curves track | New track for this class |
| Class 3 oval track (optional) | For comparison if space allows |

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Phase 1: "You built a robot that follows a line with two sensors. It works, but it wobbles and struggles on curves. Why?"
* Answer: "Two sensors only tell you left or right. You can't tell *how far* off the line you are."
* Check build journals from Class 3. Ask 1–2 students to share an observation from their testing.
* **Transition:** "Today we fix the biggest limitation. We're replacing 2 sensors with 8."

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: How a reflectance sensor array works.*

* **Key talking points:**
  1. **8 sensors instead of 2:** The QTRX-MD-08RC has 8 infrared sensors in a row. Each one measures how much IR light bounces back from the surface — dark = low value, white = high value.
  2. **Mental model — 8 tiny eyes:** Imagine you're walking along a line with your eyes closed. Two fingers touching the ground (our old setup) can tell you "line is to the left" or "line is to the right."
     Now imagine 8 fingers spread out — you can tell exactly *where* the line is and *how far* you are from center.
  3. **Line position value:** The code reads all 8 sensors and calculates a single number (-1.0 to +1.0) representing where the line is. -1.0 = far left, 0.0 = centered, +1.0 = far right. This is called a weighted average.
  4. **RC timing method:** The QTRX sensors use an RC timing technique — the Pico W drives each sensor pin high to charge the capacitor, then switches to input and measures how long it takes to discharge. Darker surfaces discharge faster (see spec §3.4.2).
  5. **Why this matters:** With a position number instead of left/right, we can make the robot turn gently when slightly off-center and sharply when way off — proportional response instead of bang-bang.
* **Demo:** Show the QTRX array up close. Point out the 8 sensor pairs (emitter + detector). If possible, show raw sensor readings on the instructor's robot as you slide it across a line.
* **Questions to ask:**
  * "If the line position reads 1000, which direction should the robot turn?"
  * "What would the reading be if the line was perfectly centered under the array?"
  * "Why is a precise number like 0.0 or -0.3 more useful than just 'left' or 'right'?"

#### 5c. Guided Build (0:25–1:25)

*Activity: Remove IR pair, install QTRX array, load code, calibrate, test.*

**Step 1 — Remove IR Pair (0:25–0:30, ~5 min):**

* Disconnect the IR emitter/phototransistor pair from the breadboard
* Remove the physical sensor from under the chassis
* Students keep the IR pair as a spare part
* **What to say:** "Keep this — it's a good sensor for other projects. But 8 sensors is a major upgrade."

**Step 2 — Mount QTRX Array (0:30–0:45, ~15 min):**

* Mount the QTRX-MD-08RC under the chassis, facing down, centered on the robot's width
* The array should be 3–5 mm above the track surface [VERIFY optimal height for QTRX-MD-08RC]
* **Mounting method:** Use standoffs, double-sided tape, or a 3D-printed bracket (see BOM "QTRX Sensor Array Mounting Hardware" — fabricate at Makersmiths)
* Ensure the array is perpendicular to the direction of travel (not angled)
* **What to watch for:** Array too high (weak readings), array tilted (inconsistent readings across sensors), array not centered (robot will bias to one side)

**Step 3 — Wire QTRX Array to Pico W (0:45–1:00, ~15 min):**

* Connect the QTRX array's 8 signal pins to Pico W GPIO pins via the breadboard
* **Wiring detail (per spec §2.3 GPIO Pin Allocation):**
  * QTRX sensor 1 → GP0
  * QTRX sensor 2 → GP1
  * QTRX sensor 3 → GP2 (reused — was IR pair left)
  * QTRX sensor 4 → GP3 (reused — was IR pair right)
  * QTRX sensor 5 → GP4
  * QTRX sensor 6 → GP5
  * QTRX sensor 7 → GP6
  * QTRX sensor 8 → GP7
  * QTRX VCC → 5V from buck converter (breadboard 5V rail)
  * QTRX GND → GND
  * QTRX CTRL/LED ON pin → GP10 (controls IR emitters)
  * **Important:** GP8 and GP9 are reserved for the motor driver board I2C bus — do not use for sensors
* **Checkpoint:** "Count your wires — you should have 8 signal wires (GP0–GP7) plus the CTRL wire (GP10), power, and ground. That's 11 wires total."
* **What to watch for:** Wires in wrong breadboard rows, signal wires swapped (sensor 1 in sensor 8's pin), VCC/GND reversed, accidentally wiring to GP8/GP9 (reserved for motor driver I2C)

**Step 4 — Load Sensor Array Reader Code (1:00–1:10, ~10 min):**

* Load the instructor-provided sensor array reader code block via Mu Editor
* **Sensor array reader — functional description:**
  * **What it does:** Reads all 8 channels of the QTRX-MD-08RC array using RC timing. Each channel returns a value proportional to surface reflectance (low = dark/line, high = white/no line).
    Computes a weighted line position value on a -1.0 to +1.0 scale where -1.0 = far left, 0.0 = centered, +1.0 = far right.
  * **Inputs:** 8 GPIO pins connected to QTRX sensor channels, plus a control pin for the IR emitters
  * **Outputs:** Array of 8 raw sensor values, computed line position (-1.0 to +1.0), motor control signals based on line position
  * **How students interact:** Run in calibration mode first (slide the robot across the line to learn min/max values per sensor). Then run in follow mode — the robot uses the position value to steer. Students can view raw sensor values and computed position on the serial console.
  * **Key parameters to modify:** `BASE_SPEED` (forward speed when centered), `TURN_FACTOR` (how aggressively to turn when off-center)

**Step 5 — Calibrate and Test (1:10–1:25, ~15 min):**

* **Calibration:** Run the calibration routine — slowly slide the robot left and right across the line so each sensor sees both the line and the white background. This stores min/max values per sensor.
* **First test on the new track (oval + tighter curves):**
  * Place robot on track, run the follow mode
  * Observe: Is it smoother than the two-sensor version? Can it handle the tighter curves?
  * Adjust `BASE_SPEED` and `TURN_FACTOR` as needed
* **Comparison:** If the Class 3 oval is still set up, run on both tracks to see the difference
* **What to watch for:** Calibration values all the same (sensor too high), robot still wobbles significantly (TURN_FACTOR too high), robot doesn't turn enough on curves (TURN_FACTOR too low)

#### 5d. Testing & Documentation (1:25–1:50)

* Let all students run on the tighter-curve track and compare performance
* **Group discussion:** "How does 8 sensors compare to 2? What's better? What's still not great?"
  * Expected answer: much smoother, handles curves better, but speed is still fixed — goes the same speed on straights and curves
* **Build journal:** Compare IR pair vs. sensor array results. Sketch the new wiring diagram. Record calibration values and TURN_FACTOR settings. Note: "What's still missing?"
* **What to say:** "The robot follows better, but it's still slow. On a straight section it could go faster, but it has to go slow enough for the curves. What if it could change speed automatically?"

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "You upgraded from 2 eyes to 8. The robot now knows exactly where the line is — and it shows in how smoothly it follows."
* **Preview Class 5:** "Next week we add variable speed. The robot will go fast on straights and slow on curves. The sensor array makes this possible because we know *how far* off-center the robot is."
* **Take-home:** Experiment with different `TURN_FACTOR` values. Try very high and very low — what happens? Record results in your journal.

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| All sensor readings are the same value | Array too far from surface | Lower array to 3–5 mm above the track |
| Only some sensors respond | Wiring error — some signal wires disconnected | Check each signal wire connection at both ends |
| Line position jumps erratically | Calibration not done or done poorly | Recalibrate: slowly sweep the robot fully across the line |
| Robot turns the wrong direction | Sensor numbering reversed (1 and 8 swapped) | Swap the QTRX sensor wire connections or reverse the array in code |
| Robot follows line but wobbles | TURN_FACTOR too high | Reduce TURN_FACTOR by half; try again |
| Robot doesn't turn enough on curves | TURN_FACTOR too low | Increase TURN_FACTOR gradually until curves are handled |
| Serial console shows error about pin in use | GPIO conflict with motor driver | QTRX uses GP0–GP7 + GP10; motor driver uses GP8–GP9 (I2C). Verify no wiring crosses these boundaries. |
| Array mounting comes loose | Tape or standoffs failed | Reattach with fresh double-sided tape; use the QTRX mounting bracket from BOM |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a pre-labeled wiring diagram with the exact breadboard row for each QTRX sensor wire (color-coded)
* Do the calibration step together as a class — instructor demonstrates, then each student replicates
* For testing: pair with an older student to interpret serial console values
* Build journal template: "With 2 sensors, my robot [describe behavior]. With 8 sensors, my robot [describe behavior]."

**Older students (15–18) and adults:**

* Challenge: read the raw 8-sensor values on the serial console and manually calculate the weighted position — verify it matches the code's output
* Challenge: what happens if you cover sensors 1–2 and only use 3–8? How does that affect position tracking?
* Encourage them to look up the QTRX-MD-08RC documentation and understand the RC timing method
* Ask them to explain the weighted average concept to a younger student

### 8. Assessment

No milestone assignment or competition this class. The Phase 1 milestone was completed last class.

### 9. Instructor Tips

* **The "wow" moment:** The transition from 2 sensors to 8 is the most dramatic improvement in the course. Make sure students see the contrast — run the old 2-sensor code first (if possible), then switch to the array code. The difference in smoothness is immediately visible.
* **Calibration is critical:** A poorly calibrated array will perform worse than the IR pair. Take the time to do it right. If a student's robot performs poorly after the upgrade, recalibration fixes it 90% of the time.
* **Mounting is the hard part:** The physical mounting of the QTRX array is more difficult than wiring it. The array needs to be level, centered, and at the right height. Pre-make mounting brackets at Makersmiths (3D print or laser cut — see BOM "QTRX Sensor Array Mounting Hardware").
* **Serial console is your friend:** Have students watch the 8-sensor values change in real time as they move the robot across the line. This "seeing the data" builds intuition faster than any explanation.
* **GPIO availability:** The QTRX array uses GP0–GP7 (8 data pins) + GP10 (LED control) = 9 pins total. The Kitronik motor driver board uses GP8 (SDA) and GP9 (SCL) for I2C. No conflicts — these pin assignments are confirmed in the spec (§2.3).

### 10. Resources & References

* [Emo Chassis Assembly Guide][10] — reference for chassis mounting points
* [Raspberry Pi Pico W Datasheet][32] — GPIO pin reference
* [Circuit Canvas][08] — for creating wiring diagrams
* [Line Follower Robot: RP2040 Pico – QTR-8RC – PID][24] — Pico-based LFR with QTR sensor array (reference build)

---

## Class 5 — Variable Speed & Better Line Following

> Design Session 7 · Phase 2: Smart Control · Duration: 2 hours · Prerequisites: Class 4 (QTRX sensor array installed and calibrated)

### 1. Class Overview

Students implement variable speed control — the robot goes faster on straight sections and slower on curves, using the sensor array's position value to scale motor speed dynamically.
This is the first time the robot adjusts its own behavior based on sensor data beyond simple steering.
Students tune speed parameters through trial and error on a figure-8 track that includes both straight sections and curves, discovering that the right speed settings make a dramatic difference in performance.

**Software prerequisites:** Variable speed controller code block (instructor-provided) must be ready.

**Track requirements:** Figure-8 — medium curves + crossover. Tests variable speed (slow on curves, fast on straights).

### 2. Learning Goals

* Explain the concept of variable speed control: faster when centered, slower when off-center
* Load and run the variable speed controller code block
* Tune speed parameters (base speed, max speed, turn speed) through trial and error on the figure-8 track
* Record lap times and speed settings in the build journal — observe the relationship between parameter values and performance
* Describe why dynamic speed control is better than fixed speed

### 3. Preparation Checklist

* [ ] Print the figure-8 track on 8.5 × 11 inch paper (4 × 3 tile layout) — 10 min
* [ ] Lay the track on the floor and tape tiles down — 10 min
* [ ] Test the variable speed controller code block on the instructor's robot with the figure-8 track — 15 min
* [ ] Prepare a timing method — stopwatch app on phone or laptop — 5 min
* [ ] Have the variable speed controller code block on USB drive and as printed handout
* [ ] Bring spare batteries — variable speed testing drains batteries faster

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 4 | 1 | Chassis + Pico W + motor driver + QTRX array + batteries |
| Laptop with Mu Editor | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed figure-8 track | New track for this class |
| Stopwatch (phone or laptop app) | For timing laps |
| Spare AA batteries | Speed testing drains batteries |

> No new hardware is introduced this class. This is a software-focused session.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 4: "You upgraded to 8 sensors. The robot follows much more smoothly. But it still goes the same speed everywhere."
* Ask: "If you're driving a car and the road curves sharply, what do you do? Slow down. And on a long straight highway? Speed up. Your robot should do the same."
* Quick check: any sensor array issues from last week? Fix now if so.
* Show the new figure-8 track — point out straights, curves, and the crossover point.

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: Why variable speed matters and how to implement it.*

* **Key talking points:**
  1. **Fixed speed is a compromise:** Right now the robot runs at one speed. If you set it fast, it flies off on curves. If you set it slow, it crawls on straights. Variable speed solves this.
  2. **The sensor array tells you when to speed up and slow down:** When the line position is near 0.0 (centered), the robot is on a straight section — go fast. When the position is far from 0.0 (near -1.0 or +1.0), the robot is on a curve — slow down.
  3. **The math is simple:** `speed = BASE_SPEED - (TURN_FACTOR × distance_from_center)`. The farther from center, the slower you go. Centered = maximum speed.
  4. **Mental model — driving a mountain road:** You check the curve ahead and adjust your speed. The sensor array is your look-ahead — it tells you how sharp the curve is *right now*.
  5. **Tuning is experimentation:** There is no single "right" answer for speed settings. Different robots, different tracks, different batteries all affect optimal settings. This is real engineering — test, adjust, repeat.
* **Questions to ask:**
  * "What happens if BASE_SPEED is too high for the tightest curve on the track?"
  * "Should the robot ever go to zero speed? When?"
  * "How will we know if our speed settings are good?" (Answer: lap times and whether the robot stays on the line)

#### 5c. Guided Build (0:25–1:25)

*Activity: Load variable speed code, tune parameters, test on figure-8.*

**Step 1 — Load Variable Speed Controller Code (0:25–0:40, ~15 min):**

* Load the instructor-provided variable speed controller code block via Mu Editor
* **Variable speed controller — functional description:**
  * **What it does:** Reads the line position from the sensor array (-1.0 to +1.0 scale) and scales motor speed proportionally. When the line is centered (position ~0.0), both motors run at maximum speed.
    As the line moves off-center, the inner motor slows while the outer motor maintains speed, creating a smooth turn. The further off-center, the slower the inner motor.
  * **Inputs:** Computed line position from the sensor array reader (-1.0 to +1.0)
  * **Outputs:** Left and right motor PWM values (speed + direction)
  * **Key parameters to modify:**
    * `MAX_SPEED` — fastest the robot will go (on straight sections)
    * `MIN_SPEED` — slowest the robot will go (on tight curves)
    * `BASE_SPEED` — starting speed before position adjustment
    * `TURN_FACTOR` — how aggressively speed changes with position offset
  * **How students interact:** Adjust the 4 parameters, run on the track, time the lap, try again. The goal is to find the fastest settings that still complete a lap without leaving the track.
* Walk through the code on the projector — highlight where the speed calculation happens

**Step 2 — First Test Run (0:40–0:55, ~15 min):**

* Use the default (conservative) parameter values for the first run
* **Time the lap:** Instructor or a student uses a stopwatch
* **Observe:** Does the robot slow down on curves? Speed up on straights?
* Record the lap time and parameters in the build journal
* **What to watch for:** Robot flying off on curves (MAX_SPEED too high), robot barely moving on curves (MIN_SPEED too low), robot not speeding up on straights (TURN_FACTOR too low)

**Step 3 — Tuning Session (0:55–1:25, ~30 min):**

* Students modify parameters, test, record results, repeat
* **Suggested tuning approach:**
  1. Start with MAX_SPEED and find the fastest speed the robot handles on a straight
  2. Reduce MIN_SPEED until curves are handled smoothly
  3. Adjust TURN_FACTOR to control the transition between fast and slow
  4. Fine-tune all three together for best lap time
* Run 3–5 laps with different settings, recording time and parameters each run
* **Group tip:** Encourage students to share their settings with each other — "Student X got a 15-second lap with these values. Can you beat it?"
* **What to say:** "Every time you change a number and test it, you're doing exactly what engineers do. This is called parameter tuning."

#### 5d. Testing & Documentation (1:25–1:50)

* **Mini-Challenge #3: Speed Run** — Fastest lap time on the figure-8 track while staying on the line
  * Rules: Robot must complete the full figure-8 without leaving the track. If the robot loses the line, the lap doesn't count. Multiple attempts allowed — best lap time counts.
  * Timing: Stopwatch, start when robot crosses start line, stop when it returns
  * Age brackets: 12–14, 15–18, Adults
  * Awards: "Speed Demon" (fastest lap), "Most Improved" (biggest improvement from first to final run)
  * **Keep it fun:** Celebrate improvement over raw speed. A student who went from 30 seconds to 20 seconds deserves as much recognition as the student who hit 15 seconds.
* **Build journal:** Record speed settings and lap times in a table. Note which changes had the biggest impact. Sketch or describe the figure-8 track.

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "Your robot now adjusts its own speed — fast on straights, slow on curves. But you had to find the right settings by hand. Imagine if the robot could figure out the best settings itself. That's coming later."
* **Preview Class 6:** "Next week we add WiFi. You'll connect to your robot from your laptop's web browser and adjust these speed settings in real time — no more plugging in a USB cable every time you want to change a number."
* **Take-home:** If you have access to the track, keep tuning. Try extreme values — what's the fastest possible lap?

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Robot flies off the track on curves | MAX_SPEED or BASE_SPEED too high | Reduce MAX_SPEED by 20%; ensure MIN_SPEED is low enough for tight curves |
| Robot crawls on straight sections | MAX_SPEED too low or TURN_FACTOR too high | Increase MAX_SPEED gradually; reduce TURN_FACTOR |
| Robot doesn't change speed noticeably | TURN_FACTOR too low or speed range too narrow | Increase TURN_FACTOR; widen gap between MAX_SPEED and MIN_SPEED |
| One wheel seems slower than the other | Motor imbalance or battery voltage drop | Add a motor speed offset in code; replace batteries |
| Robot loses the line at the figure-8 crossover | Crossover confuses the sensor array (sees two lines) | Add "continue straight" logic for when all sensors see lines [challenge extension] |
| Battery dies during testing | Speed testing drains batteries fast | Replace with fresh batteries; consider rechargeable AAs for future classes |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a parameter tuning worksheet with suggested starting values and a table to fill in (Setting 1: MAX_SPEED=***, Lap Time=***)
* Start with a narrow speed range (e.g., MAX_SPEED=60, MIN_SPEED=30) so the robot is less likely to fly off the track
* Pair with a helper for timing and recording results
* Focus on the relationship: "Change this number, watch what happens" — don't worry about optimal values

**Older students (15–18) and adults:**

* Challenge: find the absolute fastest lap time possible without the robot leaving the track
* Challenge: can you handle the figure-8 crossover without the robot getting confused? (Requires code modification)
* Encourage them to graph their results — parameter values vs. lap time — and find the trend
* Ask: "Why does the optimal speed depend on the track? Would different tracks need different settings?"

### 8. Assessment

**Mini-Challenge #3: Speed Run** — see section 5d above.

No milestone assignment this class.

### 9. Instructor Tips

* **Battery management:** Variable speed testing runs motors at higher speeds and drains batteries fast. Start with fresh batteries. Have at least 2 sets of spare AA batteries per student.
* **Track fairness:** All students should test on the same track. If tiles shift, re-tape before competition. The crossover point in the figure-8 is the hardest part — watch for robots that "cheat" by cutting across.
* **Don't over-tune:** Some students will want to spend the entire class on tuning. That's fine — this is the lesson. The act of changing parameters and observing results is the engineering skill.
* **Competitive energy:** The Speed Run challenge is the first time students truly compete on performance. Channel it positively — celebrate improvement, share strategies, and remind students that their settings are just one combination of many.
* **Prepare for WiFi preview:** Mention that next week's WiFi interface will let them change these same parameters from a web browser without plugging in a USB cable. This builds anticipation.

### 10. Resources & References

* [CircuitPython][03] — official CircuitPython site
* [Mu Editor Installation][04] — getting started with Mu Editor
* [Make a FAST Line Follower Robot Using PID!][23] — Instructables PID-based LFR (preview of where speed control is heading)
* [High Performance Line Follower Robot][25] — high-performance LFR design reference

---

## Class 6 — WiFi Access Point & Browser Control UI

> Design Session 8 · Phase 2: Smart Control · Duration: 2 hours · Prerequisites: Class 5 (variable speed controller working)

### 1. Class Overview

Students configure the Raspberry Pi Pico W as a WiFi Access Point with a unique SSID per robot. The instructor-provided WiFi AP + Browser UI code block hosts a webpage that displays live sensor data and lets students adjust speed parameters from a web browser — no more USB cable required for tuning.
This is a pure software session with no new hardware. Students connect their laptops to their robot's WiFi network and tune speed settings in real time while the robot runs on the track.

**Software prerequisites:** WiFi Access Point + Browser UI code block (instructor-provided) must be ready.

**Track requirements:** Same figure-8 track from Class 5 — focus this class is WiFi UI, not new track challenges.

### 2. Learning Goals

* Explain what a WiFi Access Point is and how it differs from connecting to a router
* Connect a laptop to the robot's WiFi Access Point and access the browser-based UI
* View live sensor data (8 sensor values and line position) in the browser
* Adjust speed parameters (MAX_SPEED, MIN_SPEED, TURN_FACTOR) via the browser and observe real-time effects
* Describe why remote tuning is useful: no USB cable, no reprogramming, real-time adjustments

### 3. Preparation Checklist

* [ ] Test the WiFi AP + Browser UI code block on the instructor's robot — verify the webpage loads, sensor data displays, and parameter changes take effect — 20 min
* [ ] Prepare a list of unique SSIDs for each robot (e.g., "LFR-01" through "LFR-06") — 5 min
* [ ] Verify the figure-8 track from Class 5 is still laid out; re-tape if needed — 5 min
* [ ] Have the WiFi code block on USB drive and as printed handout
* [ ] Prepare a one-page "How to Connect" handout: SSID (LFR-01 through LFR-06), password (`lfr12345`), browser URL (`http://192.168.4.1`)
* [ ] Test that all student laptops can connect to a Pico W AP — some laptops have issues with captive portal detection or WiFi band compatibility [VERIFY]
* [ ] Bring spare batteries

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 5 | 1 | Chassis + Pico W + motor driver + QTRX array + batteries |
| Laptop with Mu Editor and web browser | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed figure-8 track | Reused from Class 5 |
| Spare AA batteries | For extended testing |

> No new hardware. This is a software-only upgrade that leverages the Pico W's built-in WiFi.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 5: "You tuned speed parameters by changing code, saving, unplugging USB, testing, plugging back in, changing code... tedious, right?"
* "Today we eliminate that loop. You'll change settings from your laptop's web browser *while the robot is running*."
* Quick hardware check: any robots with issues? Fix now.

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: WiFi Access Point and web-based control.*

* **Key talking points:**
  1. **Access Point vs. client:** Normally your laptop connects to a WiFi router (the router is the AP). Today, your *robot* becomes the router. Your laptop connects directly to the robot's WiFi network.
  2. **Unique SSID:** Each robot will broadcast its own network name (e.g., "LFR-01"). You connect to your robot and only your robot.
  3. **Web server on the Pico W:** The robot runs a tiny web server on port 80. When you open a browser and go to `http://192.168.4.1` (the robot's IP address), you see a control page.
  4. **What the UI shows:** Live sensor readings (all 8 values + computed line position), current speed parameters, input fields to change parameters, a start/stop button.
  5. **Why this matters for engineering:** Real-world robots and industrial systems are tuned this way — through web interfaces, not by reprogramming. Tesla updates cars over WiFi. Factory robots have web dashboards. This is how it's done professionally.
* **Demo:** Show the instructor's robot running on the track, open the browser UI on the projector, change a speed parameter, and watch the robot's behavior change in real time.
* **Questions to ask:**
  * "Why is changing parameters in real time better than editing code?"
  * "What else could we display on this web page? What other controls would be useful?" (Preview: PID tuning knobs in Class 8)
  * "Could you control the robot from a phone?" (Yes — any device with WiFi and a browser)

#### 5c. Guided Build (0:25–1:25)

*Activity: Load WiFi code, configure SSID, connect laptop, tune via browser.*

**Step 1 — Load WiFi AP + Browser UI Code (0:25–0:40, ~15 min):**

* Load the instructor-provided code block via Mu Editor
* **WiFi AP + Browser UI — functional description:**
  * **What it does:** Configures the Pico W's built-in WiFi radio as an Access Point with a unique SSID (e.g., "LFR-01"). Starts a web server on port 80 that serves an HTML page.
    The page displays live sensor data (refreshes every 500 ms), shows current speed parameters, and provides input fields + a submit button to change parameters.
  * **Inputs:** HTTP requests from the student's browser (GET for page load, POST for parameter changes)
  * **Outputs:** HTML page with sensor data table, parameter input form, and current speed settings; updated motor control parameters when form is submitted
  * **How students interact:** Connect laptop WiFi to the robot's SSID. Open a web browser, navigate to `http://192.168.4.1`. View sensor data. Change MAX_SPEED, MIN_SPEED, or TURN_FACTOR values in the form and click Submit. Changes take effect immediately — no restart needed.
  * **Network details:**
    * SSID: "LFR-XX" where XX is the student's robot number (01–06)
    * Password: `lfr12345`
    * IP address: `192.168.4.1` (Pico W default AP address)
    * Port: 80 (standard HTTP)
* Each student sets their unique SSID in the code (change the string "LFR-XX" to their number)
* Save to CIRCUITPY, disconnect USB, power on with batteries

**Step 2 — Connect Laptop to Robot WiFi (0:40–0:55, ~15 min):**

* Students open their laptop WiFi settings and look for their robot's SSID
* Connect to the SSID (no internet — just a local connection to the robot)
* Open a web browser, navigate to `http://192.168.4.1`
* **Checkpoint:** "You should see a page with your sensor readings. Wave your hand under the robot — do the numbers change?"
* **What to watch for:**
  * Laptop doesn't see the SSID — robot may not have started the AP. Check serial console via USB for errors.
  * Laptop connects but browser shows "no internet" warning — this is expected. The robot has no internet. Proceed to the URL.
  * Browser shows "site can't be reached" — verify URL is `http://192.168.4.1`, or the web server crashed. Check serial console.
  * Multiple students see each other's SSID — this is normal. Make sure each connects to their own.

**Step 3 — Live Tuning on the Track (0:55–1:25, ~30 min):**

* Place robot on the figure-8 track
* From the laptop (connected to the robot's WiFi), adjust speed parameters and submit
* Watch the robot's behavior change in real time
* **Tuning experiment:**
  1. Start with the settings from Class 5 (as a baseline)
  2. Increase MAX_SPEED by 10% — does the robot still handle curves?
  3. Decrease MIN_SPEED by 10% — does it slow down enough on tight curves?
  4. Adjust TURN_FACTOR — find the sweet spot
* Students should do at least 3 tuning iterations, recording settings and lap times in their journal
* **What to say:** "This is what real-time tuning feels like. No reprogramming, no USB cable. Change a number, watch the result, adjust again."

#### 5d. Testing & Documentation (1:25–1:50)

* Free testing time: students tune their robots on the figure-8 track via the browser UI
* **No formal competition this class** — Class 6 is between challenges
* **Build journal:** Screenshot or sketch the browser interface. Note how remote tuning changed the workflow compared to editing code directly. Record best speed settings achieved with the browser UI.
* **Group discussion:** "What else would be useful on this web page?" Gather ideas — common answers will include: start/stop button, battery level indicator, lap counter, PID tuning knobs (coming in Class 8)

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "You can now tune your robot from a web browser, in real time, wirelessly. This is how professional robotics systems are controlled."
* **Preview Class 7:** "Next week we add speed sensors to the wheels. Right now you set a motor speed, but you don't know if the wheels are actually going that fast. Speed sensors measure actual wheel speed — and that opens the door to real feedback control."
* **Take-home:** Show someone the browser UI — connect from a phone if you want. Can you tune from a phone browser?

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Robot's SSID doesn't appear in laptop WiFi list | AP not started or code error | Connect via USB, check serial console for errors; verify WiFi code loaded correctly |
| Laptop connects to SSID but browser won't load page | Wrong IP address or web server crashed | Try `http://192.168.4.1`; check serial console; restart robot |
| "No internet" warning on laptop | Expected behavior — robot is not a router | Dismiss the warning; proceed to the URL manually |
| Parameter changes don't take effect | Form submission error or code bug | Check serial console for HTTP request logs; verify form action URL |
| Sensor data doesn't update on webpage | Page refresh not working | Add auto-refresh meta tag or click refresh; check if code sends updated data |
| Multiple robots interfere with each other | Duplicate SSIDs | Ensure each robot has a unique SSID (LFR-01 through LFR-06) |
| Laptop keeps reconnecting to the building WiFi | OS prefers known networks | "Forget" the building WiFi temporarily, or set robot WiFi as priority |
| Browser UI looks broken (no formatting) | HTML/CSS not loading properly | Simplify the HTML; verify the code sends complete HTML response |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a step-by-step "How to Connect" handout with screenshots: open WiFi settings → find LFR-XX → connect → open browser → type URL → see the page
* Pre-configure SSIDs in the code before distributing — younger students just load and run
* During tuning: suggest specific parameter changes to try ("Change MAX_SPEED from 70 to 80, then test")
* Help with the "no internet" warning — this confuses younger students who think WiFi means internet

**Older students (15–18) and adults:**

* Challenge: modify the HTML to add a new field (e.g., a "Reverse" button or a "Calibrate" button)
* Challenge: try connecting from a phone browser — does it work?
* Ask them to explain the client-server model: "Your laptop is the client, the Pico W is the server. What does each do?"
* Encourage them to read the code that generates the HTML — how does a web server work on a microcontroller?

### 8. Assessment

No milestone assignment or competition this class. The WiFi UI will be used in all future classes for tuning.

### 9. Instructor Tips

* **WiFi debugging is painful:** The #1 issue is laptops that refuse to connect or keep switching back to the building WiFi. Test every student's laptop with a Pico W AP *before* class if possible. Have a troubleshooting checklist ready.
* **Demo first:** The live demo of changing a parameter and watching the robot react is the most compelling moment of this class. Make sure your demo works flawlessly before class.
* **No new hardware = catch-up opportunity:** If any students are behind on hardware assembly or calibration from previous classes, this is a good catch-up session. The WiFi code can be loaded onto any working robot quickly.
* **Security note:** The WiFi AP is an open network (or simple password). This is fine for a classroom setting. Mention to older students that real IoT devices need proper security — this is intentionally simplified.
* **Future classes depend on this UI:** Classes 7, 8, 9, and 10 all use the browser interface to display additional data and tuning parameters. Make sure every student has WiFi working before leaving today.

### 10. Resources & References

* [CircuitPython][03] — official CircuitPython site
* [Raspberry Pi Pico W Datasheet][32] — WiFi specifications and pinout
* [CircuitPython Installation on Pico W][05] — includes WiFi setup notes

---

## Class 7 — Speed Sensors + Closed-Loop Feedback

> Design Session 9 · Phase 2: Smart Control · Duration: 2 hours · Prerequisites: Class 6 (WiFi AP and browser UI working)

### 1. Class Overview

Students install a Speed Sensor Module on each wheel (2 total) and wire them to the Pico W.
They load the speed sensor reader and open-loop speed controller code blocks, measure actual wheel speed (RPM) via the browser UI, and discover the difference between *setting* a speed and *achieving* a speed.
The instructor introduces open-loop vs. closed-loop control, feedback control, and the concept of autonomous control — laying the groundwork for the PID controller in Class 8. This class completes Phase 2 with the Smart Control milestone assignment.

**Software prerequisites:** Speed sensor reader and open-loop speed controller code blocks (instructor-provided) must be ready.

**Track requirements:** Figure-8 + chicane — add sharp S-curves to the figure-8 track. Tests speed sensor feedback and consistency.

### 2. Learning Goals

* Install Speed Sensor Modules (1 per wheel) and wire them to the Pico W
* Read wheel speed (RPM) from the speed sensors and display values in the browser UI
* Explain the difference between open-loop and closed-loop control in plain language
* Observe that setting a motor speed does not guarantee the wheels turn at that speed (friction, battery voltage, load)
* Complete the Phase 2 milestone assignment: sensor array, variable speed, WiFi, and speed sensors all working

### 3. Preparation Checklist

* [ ] Print the figure-8 + chicane track (add sharp S-curves to existing figure-8) — 10 min
* [ ] Lay the new track on the floor and tape down — 10 min
* [ ] Pre-test speed sensor modules on the instructor's robot — verify RPM readings are reasonable — 20 min
* [ ] Prepare 12 Speed Sensor Modules (2 per robot × 6 robots) with mounting hardware — 10 min
* [ ] Prepare wiring diagrams for speed sensor → Pico W connections — 5 min
* [ ] Have code blocks on USB drive and as printed handouts
* [ ] Set up a whiteboard diagram showing open-loop vs. closed-loop control
* [ ] Bring spare jumper wires, speed sensor modules, and batteries

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Speed Sensor Module | 2 | One per wheel; IR optocoupler for speed detection |
| Jumper wires (M-F) | ~6 | For speed sensor connections |

**Per Student (from prior classes):**

| Component | Notes |
|:----------|:------|
| Assembled robot with Pico W, QTRX array, WiFi, batteries | From Classes 1–6 |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed figure-8 + chicane track | New track for this class |
| Spare speed sensor modules | In case of defective units |

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 6: "You can now tune your robot wirelessly via a web browser. The sensor array tells you where the line is. Variable speed helps with curves. But there's a gap — you *set* a motor speed, but do the wheels actually spin at that speed?"
* **Experiment prompt:** "If I tell the motor to go at 70% power, and the battery is half dead, does the wheel actually go at 70%? How would you know?" (Answer: you wouldn't, without measuring)
* Quick hardware check. Verify WiFi UI works for all robots.

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: Speed sensing, open-loop vs. closed-loop control.*

* **Key talking points:**
  1. **Speed sensors measure reality:** The Speed Sensor Module uses an IR optocoupler — an IR light shines through a slotted disc attached to the wheel. Each slot breaks the beam, creating a pulse. Count pulses per second = RPM (rotations per minute).
  2. **Open-loop vs. closed-loop control:** [Open-loop][11]: you set a speed and hope for the best (like setting an oven temperature without a thermometer). [Closed-loop][13]: you set a speed, measure the actual speed, and adjust if it's wrong (like a thermostat).
  3. **Why this matters:** Battery voltage drops over time, surfaces have different friction, one motor may be slightly stronger than the other. Without measuring actual speed, you're guessing.
  4. **Today = open-loop:** We'll install sensors and *measure* speed, but we won't close the loop yet. We'll see how bad the gap is between set speed and actual speed.
  5. **Next class = closing the loop:** We'll add a PID controller that reads actual speed and adjusts motor power automatically. That's [feedback control][13] — the foundation of [control theory][15].
* **History context:** Briefly mention how [PID controllers were invented][16] — originally for steering ships, now everywhere from cruise control to drones.
* **Questions to ask:**
  * "Your oven is set to 350°F. Is the actual temperature always exactly 350?" (No — it fluctuates. A thermostat compensates.)
  * "What would happen if a self-driving car didn't measure its actual speed?"

#### 5c. Guided Build (0:25–1:25)

*Activity: Install speed sensors, wire to Pico W, load code, test, observe.*

**Step 1 — Install Speed Sensor Modules (0:25–0:45, ~20 min):**

* Mount one Speed Sensor Module on each wheel's motor assembly
* The slotted disc (encoder wheel) attaches to the motor shaft or wheel hub [VERIFY mounting method for this specific module]
* Position the IR optocoupler so the slotted disc passes through the gap
* **What to watch for:**
  * Disc not aligned with the sensor gap — it should spin freely through the gap without touching
  * Sensor mounted too far from the disc — weak or no signal
  * Disc rubbing on the chassis — causes friction and inaccurate readings

**Step 2 — Wire Speed Sensors to Pico W (0:45–0:55, ~10 min):**

* Connect speed sensor signals to Pico W GPIO pins via breadboard:
  * Left wheel speed sensor signal (D0) → GP11
  * Right wheel speed sensor signal (D0) → GP12
  * Speed sensor VCC → 5V from buck converter (breadboard 5V rail)
  * Speed sensor GND → GND
* **Checkpoint:** "Spin each wheel by hand — does the speed sensor LED blink on and off?" (Most modules have an indicator LED)

**Step 3 — Load Speed Sensor Reader Code (0:55–1:05, ~10 min):**

* Load the instructor-provided speed sensor reader code block
* **Speed sensor reader — functional description:**
  * **What it does:** Monitors GPIO interrupt pins connected to the speed sensor modules. Counts the pulses generated by the slotted disc as the wheel turns.
    Calculates RPM for each wheel based on pulse count, time interval, and number of slots on the encoder disc. Displays RPM values in the browser UI.
  * **Inputs:** Digital pulses from left and right speed sensor modules (GPIO interrupt pins)
  * **Outputs:** Left wheel RPM and right wheel RPM, displayed on the browser UI page alongside sensor array data
  * **How students interact:** View RPM values in the browser while the robot runs. Compare left vs. right wheel speeds. Observe how RPM changes with battery level and surface conditions.

**Step 4 — Load Open-Loop Speed Controller Code (1:05–1:15, ~10 min):**

* Load the open-loop speed controller code block (extends the speed sensor reader)
* **Open-loop speed controller — functional description:**
  * **What it does:** Lets the student set a target speed (RPM) via the browser UI. Displays both the target speed and the actual measured speed side by side. Does NOT automatically adjust — it just shows the difference. This demonstrates the gap between intent and reality.
  * **Inputs:** Target speed set by the student via browser UI, actual speed from speed sensor reader
  * **Outputs:** Browser UI display showing: target RPM, actual left RPM, actual right RPM, difference (error)
  * **How students interact:** Set a target speed, watch the robot run, see how far off the actual speed is. Try different target speeds. Observe how the error changes with battery level, surface friction, and curves.

**Step 5 — Test and Observe (1:15–1:25, ~10 min):**

* Run the robot on the figure-8 + chicane track
* In the browser UI: set a target speed and watch actual RPM
* **Key observations students should discover:**
  * Actual RPM is rarely equal to the target — there's always some error
  * Error gets worse as batteries drain
  * The two wheels may have different RPMs even at the same setting (motor imbalance)
  * RPM drops on curves (more load on the inner wheel)
* **What to say:** "See the gap between target and actual? That's what open-loop control looks like. Next week, we close that gap."

#### 5d. Testing & Documentation (1:25–1:50)

* **Mini-Challenge #4: Consistency** — Most consistent lap times across 3 runs on the figure-8 + chicane track
  * Each student runs 3 timed laps
  * Score = difference between fastest and slowest lap (lowest difference wins)
  * Multiple sets of 3 attempts allowed — best set counts
  * Age brackets: 12–14, 15–18, Adults
  * Awards: "Most Consistent" (smallest time spread across 3 laps)
  * **What to say:** "This challenge isn't about speed — it's about doing the same thing every time. Consistency is harder than speed."
* **Milestone Assignment: Phase 2 — Smart Control Complete:**
  * Sensor array installed and reading line position
  * Variable speed working (fast on straights, slow on curves)
  * WiFi interface operational (browser UI shows sensor data, accepts parameter changes)
  * Speed sensors reporting RPM data in the browser UI
  * Build journal entry comparing performance at each upgrade step (IR pair → sensor array → variable speed → WiFi → speed sensors)
  * **What "complete" looks like:** All four systems work together. The browser UI shows sensor data and RPM. The robot follows the figure-8 + chicane track. The journal documents the full Phase 2 journey.

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "You now have real speed data from each wheel. You've seen the gap between setting a speed and achieving it.
  Phase 2 is complete — your robot can see the line (8 sensors), adjust its speed (variable control), be tuned wirelessly (WiFi), and measure how fast it's actually going (speed sensors)."
* **Preview Class 8:** "Next week we close the loop. The [PID controller][16] will read actual speed, compare it to the target, and adjust motor power automatically — hundreds of times per second. This is the same technology used in cruise control, drone flight, and industrial robots."
* **Phase 2 complete:** Congratulate students on completing the second milestone.
* **Take-home:** Read about [open-loop vs. closed-loop control][12]. Think about examples in everyday life (thermostat, cruise control, manual vs. automatic transmission).

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Speed sensor always reads 0 RPM | Slotted disc not aligned with sensor, or wiring error | Check disc alignment in the sensor gap; verify signal wire connection |
| Speed sensor reads constant high RPM | Sensor triggered by ambient light or always-on signal | Shield sensor from ambient light; check for wiring short |
| Left and right RPM significantly different at same speed | Motor imbalance or one sensor miscounting | Normal to some degree; large differences suggest sensor mounting issue |
| RPM values are noisy/jumping | Disc wobble or poor sensor mounting | Secure disc and sensor; add software filtering (moving average) |
| Speed sensor LED doesn't blink when wheel spins | No power to sensor or disc not breaking beam | Check VCC/GND wiring; adjust disc position in sensor gap |
| GPIO interrupt error in code | Pin conflict with other peripherals | Speed sensors use GP11 and GP12, which are free — no conflict with QTRX (GP0–GP7, GP10) or motor driver (GP8–GP9) |
| Browser UI doesn't show RPM values | Code not integrated with WiFi UI | Verify the speed sensor code is merged into the WiFi server code |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a pre-labeled wiring diagram for speed sensor connections (color-coded)
* Help with physical mounting — aligning the slotted disc is fiddly for small hands
* For the open-loop observation: focus on "Is the number the same? No? That's the point." Don't dwell on the math.
* Build journal template: "My target speed was ***. My actual speed was***. The difference was ___."

**Older students (15–18) and adults:**

* Challenge: calculate the theoretical maximum RPM based on motor specs and battery voltage — compare to measured values
* Challenge: add a graph to the browser UI showing RPM over time (if they know basic HTML/JavaScript)
* Ask them to explain the open-loop/closed-loop difference to a younger student in their own words
* Have them read about [control theory][15] and [feedback systems][13] and identify 3 examples in everyday life

### 8. Assessment

**Mini-Challenge #4: Consistency** — see section 5d above.

**Milestone Assignment: Phase 2 — Smart Control Complete** — see section 5d above.

### 9. Instructor Tips

* **Speed sensor mounting is fiddly:** This is the hardest physical installation in Phase 2. The slotted disc must be aligned precisely with the IR optocoupler gap.
  Pre-test the mounting method on the instructor's robot and figure out the best approach before class. Consider making a jig or template.
* **Open-loop observation is the lesson:** Don't rush to close the loop. The "aha" moment is seeing that the actual speed doesn't match the target speed. Students need to internalize this gap before the PID controller will make sense.
* **Consistency challenge is enlightening:** Students who optimized for speed in Class 5 will discover that their robot isn't consistent. This naturally motivates the PID controller: "How do I make it do the same thing every time?"
* **Phase 2 milestone review:** Check that all four systems work together. The most common issue is the WiFi UI not displaying speed sensor data — this is usually a code integration problem (speed sensor code not merged into the WiFi server code).
* **Battery warning:** By Class 7, students have been using the same batteries for 3–4 classes. Performance drops are likely. Start with fresh batteries today and note that battery-related speed variation is part of the open-loop lesson.

### 10. Resources & References

* [Open-Loop Controller][11] — Wikipedia overview of open-loop control
* [Open-Loop vs. Closed-Loop Control][12] — comparison of control approaches
* [Closed-Loop Controller (Feedback)][13] — Wikipedia overview of feedback control
* [Control Theory][15] — Wikipedia introduction to control theory
* [History of PID Controllers][16] — how PID control was invented and evolved
* [Raspberry Pi Pico W Datasheet][32] — GPIO interrupt capabilities

---

## Phase 3: Autonomous — PID, Kalman, Q-Learning (Classes 8–10)

---

## Class 8 — PID Controller: Tuning for Performance

> Design Session 10 · Phase 3: Autonomous · Duration: 2 hours · Prerequisites: Class 7 (speed sensors installed, open-loop control demonstrated, Phase 2 milestone complete)

### 1. Class Overview

Students load the PID controller code block and experience their first closed-loop control system. The instructor introduces PID as three tuning knobs — P (how far off?), I (how long have I been off?), D (how fast am I drifting?) — using mental models rather than math.
Students tune all three parameters in real time via the WiFi browser UI while the robot runs on a complex track with straights, curves, sharp turns, and S-curves.
This is the capstone of the 8-class core course. If the course does not extend to stretch classes, Class 8 includes a modified final competition.

**Software prerequisites:** PID controller code block (instructor-provided) must be ready.

**Track requirements:** Complex course — all elements: straights, gentle curves, sharp turns, S-curves. This is the most challenging track in the course.

### 2. Learning Goals

* Describe the PID controller as three tuning knobs using mental models: P = steering wheel, I = memory, D = anticipation
* Load the PID controller code block and use the WiFi browser UI to tune P, I, and D parameters in real time
* Follow a systematic tuning approach: start with P only, then add D, then add I
* Observe how each parameter affects robot behavior on the complex track
* Identify that sensor noise causes jittery movement — motivating the Kalman filter (Class 9)

### 3. Preparation Checklist

* [ ] Print the complex course track (straights, gentle curves, sharp turns, S-curves) on 8.5 × 11 inch paper (4 × 3 tile layout) — 10 min
* [ ] Lay the track on the floor and tape down — 10 min
* [ ] Pre-test the PID controller code block on the instructor's robot — tune to reasonable starting values — 30 min
* [ ] Have the PID code block on USB drive and as printed handout
* [ ] Prepare a whiteboard diagram showing the PID feedback loop (sensor → error → PID → motor → sensor)
* [ ] Prepare a one-page PID tuning guide handout with the mental models and tuning steps
* [ ] Bring spare batteries — PID tuning involves lots of testing
* [ ] If this is the final class (no stretch): prepare modified final competition materials (certificates, categories)

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 7 | 1 | Fully equipped: chassis + Pico W + QTRX array + WiFi + speed sensors + batteries |
| Laptop with Mu Editor and web browser | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Printed complex course track | New track — most challenging yet |
| Spare AA batteries | PID tuning drains batteries |
| PID tuning guide handout | Mental models and tuning steps |

> No new hardware. This is the final software upgrade in the core course.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 7: "You saw the gap between setting a speed and achieving it. Open-loop control can't fix that. Today we close the loop."
* Ask: "What are the three things open-loop control can't handle?" (Battery drain, motor imbalance, varying friction)
* Quick hardware check. Ensure all WiFi UIs are working.
* Show the new complex course track — point out the different challenge sections.

#### 5b. Mini-Lecture (0:10–0:30)

*Topic: PID controller — three tuning knobs.*

* **Key talking points:**
  1. **P = Proportional — the steering wheel:** How far off the line am I right now? If I'm a little off, turn a little. If I'm way off, turn a lot. P tells the robot *how hard to correct* based on the current error.
  2. **I = Integral — the memory:** Have I been off the line for a while? Even a tiny offset, if it persists, should be corrected. I builds up over time — it remembers past errors and pushes harder to eliminate them. Like a friend who keeps nudging you back on track.
  3. **D = Derivative — the anticipation:** Am I drifting *toward* the line or *away* from it? If the error is shrinking (I'm correcting), ease off. If the error is growing (I'm drifting away), react faster. D prevents overshooting.
  4. **Mental model — driving a car:** P = how much you turn the steering wheel based on how far off-center you are. I = noticing you've been slightly left of center for a mile and correcting. D = seeing a curve coming and starting to turn before you reach it.
  5. **Tuning order:** Start with P only (I=0, D=0). Get the robot to follow the line, even if it wobbles. Then add D to reduce the wobble. Finally, add a small I to eliminate any persistent offset.
* **Demo:** Show the instructor's robot with only P tuned — it wobbles. Add D — wobble reduces. Add I — it tracks the line tightly. This live demo is the most important teaching moment of the class.
* **Mention the [Ziegler-Nichols tuning method][16]** as a systematic alternative for older students.
* **Questions to ask:**
  * "If P is too high, what happens?" (Robot oscillates wildly — overshooting in both directions)
  * "If I is too high, what happens?" (Robot overcorrects for past errors — sluggish, then suddenly jerks)
  * "If D is too high, what happens?" (Robot becomes twitchy — reacts to every tiny sensor change)

#### 5c. Guided Build (0:30–1:25)

*Activity: Load PID code, systematic tuning, test on complex track.*

**Step 1 — Load PID Controller Code (0:30–0:40, ~10 min):**

* Load the instructor-provided PID controller code block via Mu Editor
* **PID controller — functional description:**
  * **What it does:** Implements a standard PID control loop. Reads the line position from the sensor array, calculates the error (distance from center = 0.0), and computes a motor correction value using: `correction = (Kp × error) + (Ki × integral_of_error) + (Kd × derivative_of_error)`.
    Applies the correction to the left and right motor speeds. Runs this loop continuously, many times per second.
  * **Inputs:** Line position from sensor array (-1.0 to +1.0), current motor speeds from speed sensors
  * **Outputs:** Adjusted left and right motor PWM values
  * **Browser UI additions:** Three new input fields for Kp, Ki, and Kd. Real-time display of: current error, integral accumulation, derivative value, motor correction output. Start/stop button.
  * **How students interact:** Set Kp, Ki, Kd values via the browser UI. Watch the robot run on the track. Observe how each parameter change affects behavior. Use the displayed error values to understand what the PID is doing.
  * **Key parameters:**
    * `Kp` — proportional gain (start here, range 0.0–10.0, default 1.5 per spec §3.5.3)
    * `Ki` — integral gain (add second, range 0.0–5.0, default 0.0, start at 0 per spec §3.5.3)
    * `Kd` — derivative gain (add after P, range 0.0–10.0, default 0.5 per spec §3.5.3)

**Step 2 — P-Only Tuning (0:40–0:55, ~15 min):**

* Set Ki=0, Kd=0. Start with a low Kp value.
* Run on the complex track. Increase Kp until the robot follows the line but oscillates.
* Then reduce Kp slightly — find the sweet spot between "doesn't turn enough" and "oscillates wildly."
* Record the Kp value and track behavior in the build journal.
* **What to say:** "P-only control works, but the robot wobbles. It's always overshooting. We need something to dampen that."

**Step 3 — Add D (0:55–1:10, ~15 min):**

* Keep Kp at the value found in Step 2. Start adding small Kd values.
* Run on the track. Observe: the wobble should decrease.
* Increase Kd until the robot follows smoothly but isn't sluggish.
* **What to say:** "D is the anticipation knob. It sees the error changing and reacts. Too much D makes the robot twitchy. Too little and the wobble stays."

**Step 4 — Add I (1:10–1:20, ~10 min):**

* Keep Kp and Kd at their tuned values. Add a very small Ki value.
* Run on the track. Observe: any persistent offset should be corrected.
* **Warning:** Ki is the most dangerous parameter — too much causes integral windup (the robot accumulates error and then jerks violently). Start very small.
* **What to say:** "I fixes the small, persistent errors. But be careful — a little I goes a long way."

**Step 5 — Fine-Tune and Compare (1:20–1:25, ~5 min):**

* Students make final adjustments to all three parameters
* Run the robot with the PID controller on the complex track
* **What to watch for:** Sensor noise causing jittery PID output — this is normal and sets up the motivation for the Kalman filter in Class 9
* **What to say:** "Your PID is tuned, but look at the error values in the browser — they're noisy. The sensors aren't perfectly clean. Next time, we'll add a filter to smooth that out."

#### 5d. Testing & Documentation (1:25–1:50)

* **If stretch classes (9–10) are planned:** No competition this class. Free tuning time on the complex track. Students continue refining PID values.
* **If this is the final class (8 of 8) — Modified Final Competition:**
  * **Fastest lap** — best lap time on the complex course
  * **Most consistent** — smallest variation across 3 laps
  * **Best build journal** — instructor selects based on completeness, diagrams, and observations throughout the course
  * Multiple attempts allowed, age brackets (12–14, 15–18, Adults)
  * Awards: certificates for each category
  * Course wrap-up: What did we learn? How could we keep improving? Students take robots home.
  * **Milestone Assignment: Phase 3 — Autonomous Complete** (PID tuning only for 8-class version): PID controller tuned, build journal documents PID tuning values and observations.
* **Build journal:** Record PID tuning values (Kp, Ki, Kd) and describe what each change did. Note the effect of sensor noise on PID behavior.

#### 5e. Wrap-Up (1:50–2:00)

* **If stretch classes planned:**
  * **Summary:** "Your robot now has real closed-loop control — it measures, adjusts, measures again, hundreds of times per second. The PID controller is used in everything from cruise control to drones to factory robots."
  * **Preview Class 9:** "The PID works great, but those noisy sensor readings are causing jitter. Next week we add a [Kalman filter][17] — a smart averaging tool that smooths the noise before the PID ever sees it."
  * **Take-home:** Try different tracks if possible. Do your PID values work on a different track layout, or do you need to retune?
* **If this is the final class:** Course wrap-up speech. Students take robots home. Distribute Kalman filter and Q-Learning code blocks as take-home exploration topics.

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Robot oscillates wildly | Kp too high | Reduce Kp by 50%; ensure Ki and Kd are near zero during initial tuning |
| Robot doesn't turn enough on curves | Kp too low | Increase Kp gradually until the robot responds to curves |
| Robot overshoots and then jerks back | Ki too high (integral windup) | Reduce Ki dramatically; add integral clamping in code if available |
| Robot is twitchy / jittery | Kd too high, amplifying sensor noise | Reduce Kd; consider adding a low-pass filter on the derivative term |
| Robot follows straight sections but loses line on sharp turns | PID output saturates (can't turn fast enough) | Increase motor speed range or add special handling for large errors |
| Browser UI doesn't show PID parameters | Code not properly integrated with WiFi UI | Verify PID parameters are exposed in the web server code |
| PID values reset when robot restarts | Values not saved to flash | Normal behavior — re-enter values each session; advanced: save to file on CIRCUITPY |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Provide a PID tuning cheat sheet: "Start with Kp=1.0, Ki=0, Kd=0. Increase Kp until it wobbles. Then add Kd=0.5. Then try Ki=0.1."
* Focus on the mental models — steering wheel, memory, anticipation — not the math
* Pair with a helper for browser UI tuning while the robot runs on the track
* Build journal template: "My Kp is ***. When I changed it to***, the robot [describe behavior]."

**Older students (15–18) and adults:**

* Challenge: implement the [Ziegler-Nichols tuning method][16] — find the ultimate gain (Ku) where the robot oscillates at constant amplitude, then calculate Kp, Ki, Kd from Ku
* Challenge: graph the error over time (via serial output or browser) and identify oscillation frequency
* Ask them to explain why the PID controller is "closing the loop" — draw the feedback diagram
* Discuss where PID is used in the real world: cruise control, drone flight controllers, industrial process control

### 8. Assessment

**If final class (no stretch):** Modified Final Competition and Phase 3 milestone — see section 5d above.

**If stretch classes planned:** No milestone or competition this class. PID tuning is documented in the build journal.

### 9. Instructor Tips

* **The live demo sells PID:** Before students touch their robots, demonstrate PID tuning on the instructor's robot on the projector. Show P-only (wobble), P+D (smooth), P+I+D (precise). This 5-minute demo is worth more than 30 minutes of lecture.
* **Integral windup is scary:** When students crank up Ki, the robot will accumulate error during a sharp turn and then jerk violently when it recovers. Warn them: "Ki is powerful but dangerous. Start at 0.01, not 1.0."
* **Sensor noise is a feature, not a bug:** The jitter caused by noisy sensor data is visible in the PID output. Point it out — "See how the motors twitch even on a straight line? That's noise in the sensor data being amplified by the PID, especially the D term. We'll fix that next week."
* **If this is the final class:** Make it celebratory. Certificates for competition categories. Take a group photo. Emphasize the journey from Class 1 (no motors) to Class 8 (autonomous PID control). Distribute Kalman filter and Q-Learning code blocks as take-home exploration.
* **PID is the most reusable concept:** Students will encounter PID controllers in any future robotics, automation, or engineering work. Emphasize this — "You just learned the most important algorithm in industrial control."

### 10. Resources & References

* [History of PID Controllers][16] — how PID control was invented and evolved
* [Control Theory][15] — Wikipedia introduction to control theory
* [Closed-Loop Controller (Feedback)][13] — Wikipedia overview of feedback control
* [Kalman Filter Explained Simply][17] — preview for next class
* [Make a FAST Line Follower Robot Using PID!][23] — Instructables PID-based LFR build
* [Line Follower Robot: RP2040 Pico – QTR-8RC – PID][24] — Pico-based LFR with PID control

---

## Class 9* — Kalman Filter: Smoothing the Noise

> STRETCH CLASS · Design Session 11 · Phase 3: Autonomous · Duration: 2 hours · Prerequisites: Class 8 (PID controller tuned and working)

### 1. Class Overview

Students add a Kalman filter module to the sensor pipeline, positioned between the sensor array reader and the PID controller. The filter smooths noisy sensor data before the PID processes it, resulting in less jittery motor control and smoother line following.
Students compare robot behavior with and without the filter on the same complex track, tuning filter parameters via the browser UI. The instructor introduces the Kalman filter as "smart averaging" — blending what the sensor says now with what we predicted based on the last reading.

**Software prerequisites:** Kalman filter module code block (instructor-provided) must be ready.

**Track requirements:** Same complex course from Class 8 — allows direct before/after comparison.

### 2. Learning Goals

* Explain what sensor noise is and why it causes problems for the PID controller
* Describe the Kalman filter as "smart averaging" — combining measurement and prediction
* Add the Kalman filter module to the robot's sensor pipeline
* Tune filter parameters (process noise, measurement noise) via the browser UI
* Compare filtered vs. unfiltered performance on the same track and quantify the improvement

### 3. Preparation Checklist

* [ ] Verify the complex course track from Class 8 is still laid out — re-tape if needed — 5 min
* [ ] Pre-test the Kalman filter module on the instructor's robot — verify before/after comparison mode works — 20 min
* [ ] Have the Kalman filter code block on USB drive and as printed handout
* [ ] Prepare a one-page Kalman filter mental model handout (weather forecast analogy)
* [ ] Bring spare batteries

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 8 | 1 | Fully equipped with PID controller |
| Laptop with Mu Editor and web browser | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Complex course track | Reused from Class 8 |
| Spare AA batteries | For extended testing |

> No new hardware. Software-only upgrade.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap Class 8: "Your PID controller works great, but remember the jitter? The D term was amplifying sensor noise, making the motors twitch."
* Show a quick demo: run the instructor's robot *without* the Kalman filter — point out the jitter
* Ask: "What if we could clean up the sensor data *before* the PID sees it?"
* **What to say:** "Today we add a filter that's so smart it's used in GPS navigation, spacecraft guidance, and self-driving cars."

#### 5b. Mini-Lecture (0:10–0:25)

*Topic: Kalman filter — smart averaging.*

* **Key talking points:**
  1. **What is sensor noise?** Every sensor reading has some error — slight variations due to electrical interference, surface imperfections, or sensor quirks. On a smooth surface, the sensor might read 0.00, -0.02, +0.02, +0.01 — all slightly different. This is noise.
  2. **Why noise hurts PID:** The P term doesn't mind much, but the D term (derivative) measures *change*. If the reading goes from 0.00 to +0.02 due to noise (not actual movement), D thinks the robot is drifting and corrects — causing jitter.
  3. **The [Kalman filter][17] — smart averaging:** Imagine you're predicting tomorrow's temperature. You have two sources: the thermometer (noisy, fluctuates) and your prediction based on yesterday (smoother, but might be wrong).
     The Kalman filter blends them — trusting the thermometer more when your prediction is uncertain, and trusting the prediction more when the thermometer is noisy.
  4. **Two tuning parameters:**
     * **Process noise (Q):** How much do we trust our prediction? Low Q = trust the prediction (smoother but slower to react). High Q = don't trust the prediction (noisier but faster to react).
     * **Measurement noise (R):** How much do we trust the sensor? Low R = trust the sensor (noisier output). High R = don't trust the sensor (smoother output but may miss real changes).
  5. **Before/after comparison:** We'll run the robot with and without the filter on the same track. The difference should be visible — less wobble, smoother turns, quieter motors.
* **Questions to ask:**
  * "If you turn R very high (don't trust the sensor), what happens?" (Robot responds slowly — may lose the line on sharp turns)
  * "If you turn Q very high (don't trust the prediction), what happens?" (Filter does very little — almost the same as no filter)

#### 5c. Guided Build (0:25–1:20)

*Activity: Add Kalman filter, tune parameters, compare before/after.*

**Step 1 — Load Kalman Filter Module (0:25–0:35, ~10 min):**

* Load the instructor-provided Kalman filter code block via Mu Editor
* **Kalman filter module — functional description:**
  * **What it does:** Sits between the sensor array reader and the PID controller in the processing pipeline. Takes the raw line position value (-1.0 to +1.0), applies Kalman filtering to smooth out noise, and passes the filtered value to the PID controller.
    Implements a simplified 1D Kalman filter with tunable process noise (Q) and measurement noise (R) parameters.
  * **Inputs:** Raw line position from sensor array reader
  * **Outputs:** Filtered line position (smoother version of the same -1.0 to +1.0 value)
  * **Browser UI additions:** Two new input fields for Q and R. Toggle switch for "Filter ON/OFF" (comparison mode). Display shows both raw and filtered line position values side by side.
  * **How students interact:** Toggle the filter on and off while the robot runs. Observe the difference. Adjust Q and R to find the best balance between smoothness and responsiveness.
  * **Key parameters:**
    * `Q` (process noise) — start at 0.1, range 0.001–1.0 (per spec §3.5.4)
    * `R` (measurement noise) — start at 0.3, range 0.001–1.0 (per spec §3.5.4)

**Step 2 — Before/After Comparison (0:35–0:55, ~20 min):**

* **Run 1 — Filter OFF:** Run the robot on the complex track with the filter disabled. Record lap time, observe jitter, listen to motor sounds (twitchy motors = noise).
* **Run 2 — Filter ON (default settings):** Enable the filter with default Q and R values. Run the same track. Record lap time, observe the difference.
* **What to look for:** Smoother motor control, less wobble, potentially faster laps (less energy wasted on jittery corrections)
* **What to say:** "The robot is doing the same thing, on the same track, with the same PID values. The only difference is cleaner sensor data."

**Step 3 — Tune Filter Parameters (0:55–1:20, ~25 min):**

* Experiment with different Q and R values
* **Suggested experiments:**
  1. Set Q=0.01, R=10 — very smooth but slow to react. Does it lose the line on sharp turns?
  2. Set Q=10, R=0.1 — barely any filtering. Is it different from no filter?
  3. Find a middle ground that's smooth on straights but responsive on curves
* Record settings and observations in the build journal
* **What to watch for:** Over-filtering (robot misses sharp turns because the filter delays position data), under-filtering (no visible improvement)

#### 5d. Testing & Documentation (1:20–1:50)

* **Mini-Challenge #5: Smooth Operator** — Smoothest line following (least wobble) over 3 laps on the complex course
  * Judging: Instructor observes visually (least visible wobble), and/or use the browser UI's raw vs. filtered data to quantify smoothness
  * Multiple attempts allowed — best set of 3 laps counts
  * Age brackets: 12–14, 15–18, Adults
  * Awards: "Smooth Operator" (smoothest following)
  * **What to say:** "This isn't about speed — it's about grace. Which robot follows the line like it's on rails?"
* **Build journal:** Compare filtered vs. unfiltered performance. Record Q and R settings. Describe the before/after difference in your own words.

#### 5e. Wrap-Up (1:50–2:00)

* **Summary:** "You just added the same filtering technology used in GPS, spacecraft navigation, and self-driving cars. Your robot's sensor data is now cleaner, your PID is smoother, and your line following is tighter."
* **Preview Class 10:** "Next week is our last class. We'll try something completely different — instead of programming the robot with rules (PID), we'll let the robot *learn* the best behavior by trying things and getting rewarded.
  It's called [Q-Learning][19] — a type of [reinforcement learning][18]. And then: the final competition."
* **Take-home:** Think about other places where filtering noisy data would help. What about filtering audio? Photos? Financial data?

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Robot misses sharp turns with filter on | R too high (over-filtering) | Reduce R to trust the sensor more on quick changes |
| No visible difference with filter on | Q too high (under-filtering) | Reduce Q to rely more on the prediction |
| Filtered value lags behind raw value | Filter response too slow | Increase Q or decrease R — allow faster tracking |
| Robot behavior worse with filter | Filter parameters causing delay on critical turns | Try Q=1.0, R=1.0 as neutral starting point; tune from there |
| Browser UI doesn't show filter toggle | Code integration issue | Verify Kalman filter code is merged into WiFi server |
| NaN or overflow errors in serial console | Numerical instability in filter | Check for division by zero; ensure initial values are reasonable |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Focus on the weather forecast analogy — "The filter combines what the sensor says now with what it expected to say, and picks the best answer."
* Provide a simple tuning guide: "Try Filter ON with the default values. Is it smoother? Then try R=5 and R=0.5 — which is better?"
* Use the browser UI's before/after display to make the difference visual — point at the numbers changing
* Build journal template: "Without filter: [describe wobble]. With filter: [describe smoothness]. My settings: Q=***, R=***."

**Older students (15–18) and adults:**

* Challenge: read about the [Kalman filter math][17] and map the equations to the code — identify the predict and update steps
* Challenge: what happens if you chain two Kalman filters? Does double-filtering help or hurt?
* Discuss where Kalman filters are used: GPS (every phone), Apollo program (moon landing navigation), financial trading
* Ask: "Why not just use a simple moving average instead?" (Kalman adapts to changing conditions; moving average is fixed)

### 8. Assessment

**Mini-Challenge #5: Smooth Operator** — see section 5d above.

No milestone assignment this class.

### 9. Instructor Tips

* **Before/after is the lesson:** The value of this class is the comparison. Make sure every student runs with the filter off, then on, on the same track. The visual difference sells the concept.
* **Don't go deep on the math:** The Kalman filter involves matrices and covariance in its general form. For this class, students just need to understand "it blends prediction with measurement." Save the math for older students who ask.
* **Audio analogy works well:** "You know how noise-canceling headphones filter out background noise so you hear the music clearly? The Kalman filter does the same thing for sensor data — it filters out the noise so the PID hears the signal."
* **Filter can hurt on sharp turns:** Some students will over-filter and find the robot performs *worse* on sharp turns. This is a great teaching moment — filtering is a trade-off between smoothness and responsiveness.
* **Competition calibration:** For the Smooth Operator challenge, have the instructor (or a student volunteer) serve as the judge for "least wobble." If using browser data, compare the standard deviation of the filtered line position across 3 laps.

### 10. Resources & References

* [Kalman Filter Explained Simply][17] — plain-language Kalman filter explanation
* [Control Theory][15] — Wikipedia introduction to control theory
* [Model-Free Reinforcement Learning][18] — preview for next class
* [Q-Learning in Python][19] — preview for next class

---

## Class 10* — Q-Learning + Course Wrap-Up & Final Competition

> STRETCH CLASS · Design Sessions 12 & 13 · Phase 3: Autonomous · Duration: 2 hours · Prerequisites: Class 9 (Kalman filter installed and tuned)

### 1. Class Overview

The final class of the course. Students load the Q-Learning controller code block, which replaces the PID controller with a reinforcement learning algorithm. They watch the robot *learn* to follow the line through trial and error — no tuning required.
The robot starts badly, tries random actions, gets rewarded for staying on the line, and gradually improves over multiple training runs.
After training, students compare Q-Learning performance to their tuned PID controller. The class concludes with the Final Competition across multiple categories, course wrap-up, and students taking their robots home.

**Software prerequisites:** Q-Learning controller code block (instructor-provided) must be ready.

**Track requirements:** Competition course — instructor designs a final course layout for competition day. Students have not seen this course before.

### 2. Learning Goals

* Explain [reinforcement learning][18] and [Q-Learning][19] using the "training a pet" mental model
* Load the Q-Learning controller and observe the robot learning from scratch
* Compare Q-Learning performance to PID performance — describe trade-offs of each approach
* Participate in the Final Competition across multiple categories
* Reflect on the full design journey: analog kit → sensor array → PID → Kalman → Q-Learning

### 3. Preparation Checklist

* [ ] Print the competition course track — a layout students have not seen before — 10 min
* [ ] Lay the track on the floor, tape down, and verify it's challenging but completable — 10 min
* [ ] Pre-test the Q-Learning controller on the instructor's robot — train for ~20 runs to verify it learns — 30 min (do days before)
* [ ] Have the Q-Learning code block on USB drive and as printed handout
* [ ] Prepare Final Competition materials: certificates/awards for each category, scoring sheets, timing method
* [ ] Prepare a "course journey" slideshow or poster: photos from each class showing the robot's evolution
* [ ] Prepare take-home materials: Kalman and Q-Learning code blocks for students who missed Classes 9–10 in a non-stretch scenario
* [ ] Bring fresh batteries for all robots — competition day demands peak performance

### 4. Materials & Components

**Per Student:**

| Component | Quantity | Notes |
|:----------|:--------:|:------|
| Robot from Class 9 | 1 | Fully equipped with PID + Kalman filter |
| Laptop with Mu Editor and web browser | 1 | Student-provided |

**Shared / Instructor:**

| Item | Notes |
|:-----|:------|
| Competition course track | New, unseen layout |
| Certificates/awards | For each competition category |
| Fresh AA batteries | 8 per robot for competition |

> No new hardware. Q-Learning is the final software upgrade.

### 5. Class Timeline

#### 5a. Review & Q&A (0:00–0:10)

* Recap the full journey: "Class 1: a chassis with no brain. Today: a robot that can learn on its own. Let's review how we got here."
* Quick timeline: analog demo → chassis → Pico W → 2 sensors → 8 sensors → variable speed → WiFi → speed sensors → PID → Kalman filter → today: Q-Learning
* Ask: "What if the robot could figure out the best way to follow a line *without* you tuning any parameters?"
* **What to say:** "PID required you to tune three knobs. Q-Learning tunes itself. You just watch it learn."

#### 5b. Mini-Lecture (0:10–0:30)

*Topic: Reinforcement learning and Q-Learning.*

* **Key talking points:**
  1. **[Reinforcement learning][18] — learning from experience:** Instead of programming rules (if/else, PID), the robot tries actions randomly, observes the result, and remembers what worked. Over time, it builds a strategy.
  2. **Mental model — training a pet:** Give a treat (reward) when the dog sits on command. Ignore bad behavior. Over hundreds of repetitions, the dog learns what to do. The robot does the same thing: it gets a reward for staying on the line and nothing for losing it.
  3. **[Q-Learning][19] — the specific algorithm:** The robot has a table (Q-table) that maps every state (sensor reading) to every action (motor speed combination).
     Each entry has a score — "how good is this action in this state?" The robot tries actions, updates scores based on rewards, and gradually learns the best action for each state.
  4. **State, action, reward:**
     * **State** = discretized sensor readings (e.g., "line is slightly left" = state 3 of 10)
     * **Action** = motor speed pair (e.g., "left motor 60%, right motor 80%")
     * **Reward** = +1 for staying centered, -1 for losing the line, 0 for being off-center
  5. **Trade-offs vs. PID:** PID is deterministic, fast to deploy, works immediately if tuned well. Q-Learning takes time to train, but adapts to any track without manual tuning. In practice, real robots often use both — Q-Learning for high-level strategy, PID for low-level motor control.
* **Brief mention of other approaches (awareness only):** [Active disturbance rejection control, model predictive control][14], [fuzzy logic control][20]. These exist but are beyond our scope.
* **Mention [Pure Pursuit Controller][21]** — requires look-ahead and [odometry][22], also beyond scope. These are future explorations.
* **Questions to ask:**
  * "How many training runs do you think the robot needs to learn?" (Depends on the track — typically 10–50 runs)
  * "Will Q-Learning work on a track the robot has never seen?" (Partially — it generalizes from learned states, but a very different track may require retraining)

#### 5c. Guided Build (0:30–1:10)

*Activity: Load Q-Learning, train the robot, compare to PID.*

**Step 1 — Load Q-Learning Controller (0:30–0:40, ~10 min):**

* Load the instructor-provided Q-Learning controller code block via Mu Editor
* **Q-Learning controller — functional description:**
  * **What it does:** Replaces the PID controller with a Q-Learning algorithm. Discretizes the sensor array's line position into a set of states (e.g., 10 states from "far left" to "far right"). Defines a set of actions (motor speed combinations).
    Maintains a Q-table mapping state-action pairs to expected rewards. During training, uses an epsilon-greedy strategy (mostly exploit learned knowledge, occasionally explore random actions). Updates the Q-table after each action based on the reward received.
  * **Inputs:** Discretized line position (state), reward signal (computed from how centered the robot is)
  * **Outputs:** Motor speed pair (action) selected from the Q-table
  * **Browser UI additions:** Training mode toggle, episode counter, Q-table visualization (heatmap of state-action values), learning rate and epsilon parameters, "Reset Q-table" button
  * **How students interact:** Start training mode, place robot on track, watch it learn. Initially the robot moves randomly. Over 10–50 training runs, it improves. Switch to exploit-only mode (no exploration) and see the trained behavior. Compare to PID on the same track.

**Step 2 — Train the Robot (0:40–1:00, ~20 min):**

* Place robot on the training track (use the complex course from Class 8/9, NOT the competition course)
* Start training mode via the browser UI
* **What to observe:**
  * **Runs 1–3:** Robot moves mostly randomly, falls off the line frequently
  * **Runs 5–10:** Robot starts making better decisions, stays on the line longer
  * **Runs 15–20:** Robot follows the line with increasing competence
  * **Runs 25+:** Robot performance stabilizes — it has learned a policy
* Let students watch each other's robots learn — it's fascinating to see random behavior become purposeful
* **What to say:** "Nobody told the robot how to follow the line. It figured it out by trying things and learning from the results."

**Step 3 — Compare Q-Learning vs. PID (1:00–1:10, ~10 min):**

* Switch back to PID mode (code should support swapping controllers)
* Run on the same track with the best PID settings from Class 8
* Compare: Which is faster? Which is smoother? Which handles sharp turns better?
* **Discussion:** "PID was instant — you tuned it and it worked. Q-Learning took 20+ runs to learn. But Q-Learning didn't need any manual tuning. Which is better? It depends on the situation."

#### 5d. Testing & Documentation (1:10–1:50)

* **Final Competition** — on the competition course track (unseen by students):
  * **Fastest lap** — best lap time with any controller (PID or Q-Learning, student's choice)
  * **Most consistent** — smallest time variation across 3 laps
  * **Smoothest** — least wobble, judged by instructor
  * **Best build journal** — instructor selects based on completeness, diagrams, and quality of observations across all 10 classes
  * **People's choice** — all participants vote for their favorite robot (most creative modification, best decorated, coolest name, etc.)
  * Rules: Multiple attempts allowed, best run counts. Age brackets: 12–14, 15–18, Adults. All categories get certificates.
  * **Setup:** Fresh batteries in all robots. 3 minutes per student per attempt. Instructor times with stopwatch.
* **Milestone Assignment: Phase 3 — Autonomous Complete:**
  * PID controller tuned
  * Kalman filter added and tuned
  * Q-Learning tested (trained and compared to PID)
  * Final build journal entry reflecting on the full design journey from analog kit to autonomous robot
  * **What "complete" looks like:** The student participated in all three phases, their robot works with at least the PID controller, and their journal documents the journey.

#### 5e. Wrap-Up (1:50–2:00)

* **Course wrap-up:**
  * "In 10 weeks, you went from a chassis on a table to a robot that can learn to follow a line by itself. That's real engineering — building something simple and making it better, one step at a time."
  * Recognize each student's journey — call out a specific achievement or moment for each one
  * Award certificates for all competition categories
  * **What to say:** "You built this. You wired it, you coded it, you tuned it. The robot is yours — take it home and keep improving it."
* **Where to go from here:**
  * Local robotics competitions and LFR events
  * [Makersmiths][01] has tools and space for continued projects
  * The code blocks are yours — modify them, extend them, break them and fix them
  * Explore [Pure Pursuit controllers][21], better motors, camera-based vision
* **Students take robots home**
* Group photo

### 6. Troubleshooting Guide

| Problem | Likely Cause | Fix |
|:--------|:-------------|:----|
| Q-Learning robot doesn't improve after 20+ runs | Reward function not working or learning rate too low | Check reward calculation; increase learning rate; verify state discretization |
| Robot gets stuck in one action (always turns left) | Q-table converged on a bad policy | Reset Q-table and retrain; increase epsilon (exploration rate) |
| Training is too slow (robot takes forever per run) | Too many states or actions | Reduce state discretization (fewer buckets); reduce action set |
| Q-table displays NaN values | Numerical error in Q-value updates | Check for division by zero; cap Q-values at reasonable bounds |
| Can't switch between PID and Q-Learning | Code doesn't support controller swapping | Verify both controllers are loaded and the toggle in the browser UI works |
| Robot performs worse on competition track than training track | Q-Learning overfitted to training track | Expected behavior — Q-Learning generalizes partially. PID may perform better on unseen tracks. |

### 7. Age Differentiation Notes

**Younger students (12–14):**

* Focus on the "training a pet" analogy — show the robot learning visually, don't explain the Q-table math
* Let them watch the robot learn and cheer when it improves — the entertainment value is high
* For the competition: emphasize participation over winning. Every robot that crosses the finish line is a success.
* Build journal: provide a reflection template — "My favorite class was ***. The hardest part was***. The coolest thing my robot did was ___."

**Older students (15–18) and adults:**

* Challenge: examine the Q-table after training — which states have the highest/lowest values? Does it make intuitive sense?
* Challenge: can they modify the reward function to encourage faster following (not just staying on the line)?
* Ask them to compare PID and Q-Learning in writing: "Which would you use for a warehouse robot? Why?"
* Discuss the broader field of AI and machine learning — Q-Learning is the simplest reinforcement learning algorithm; modern robotics uses deep reinforcement learning, neural networks, etc.

### 8. Assessment

**Final Competition** — see section 5d above.

**Milestone Assignment: Phase 3 — Autonomous Complete** — see section 5d above.

### 9. Instructor Tips

* **Pre-train a demo:** Train the instructor's robot on a track before class (~50 runs) so you can show a well-trained Q-Learning robot in action. Watching a robot learn from scratch is cool but slow — showing the end result first motivates students through the training process.
* **Competition logistics:** With 5–6 robots and multiple categories, the competition can take 30+ minutes. Time-box each attempt (3 minutes max). Run students simultaneously if the track allows. Have a helper handle timing.
* **Emotional energy:** This is the last class. Make it celebratory. Take photos. Acknowledge every student's contribution. The relationships and confidence built matter more than the technical skills.
* **Take-home success:** Make sure every student leaves with a working robot and all code blocks. If a student's robot has issues, offer to fix it after class or schedule a follow-up session at Makersmiths.
* **Q-Learning expectations:** Set realistic expectations — Q-Learning won't outperform a well-tuned PID on a simple track. Its value is in adaptation and the concept. The teaching goal is exposure to reinforcement learning, not building a state-of-the-art controller.

### 10. Resources & References

* [Model-Free Reinforcement Learning][18] — overview of model-free RL approaches
* [Q-Learning in Python][19] — Q-Learning tutorial
* [Autonomous Control & MPC][14] — overview of other control techniques
* [Fuzzy Logic for Line Following][20] — academic paper on fuzzy logic LFR control
* [Pure Pursuit Controller][21] — learn-by-doing pure pursuit explanation
* [Odometry][22] — Purdue SIGBots odometry wiki
* [Makersmiths][01] — course host makerspace
* [Advanced Line Following Robot][09] — Instructables guide for continued learning

---

## Appendix A: Lesson Plan Development Prompt & Q&A

### Original Prompt

The following prompt was used to generate this lesson plan (reproduced verbatim from the instructor's prompt document):

> Along with CLAUDE.md, read only @input/\*.md and @docs/\*.md files.
> Create a course lesson plan document using the lesson_plan_generator skill.
> Place your creation in the file @docs/lfr-lesson-plan.md.
>
> Within the document you create, include this prompt,
> and all question you ask me, along with my responses.
> Place this in the document as an appendix and reference it at the beginning of the document
> and anywhere else in the text when its a useful reference.
>
> In a subsequent steps, I expect this document will used to help prepare
> the course design and materials developed for the course.
> Think Very Hard about what must be specified in this document so a robust course design & robot development plan
> can be created for the Line Following Robot.
>
> I expect there will be some issues,
> so use the AskUserQuestions tool for all things that require further clarification.

### Instructor Q&A

All questions asked during lesson plan generation and the instructor's responses:

| # | Question | Answer | Implication |
|:--|:---------|:-------|:------------|
| 1 | Speed Sensor — two types in BOM? | One is alternate | Use 2 sensors total (1/wheel). Flag in BOM that second type is alternate. |
| 2 | 8×AA vs 9V Battery? | Both used — see spec §2.4 | **Resolved:** 9V clip → Kitronik board (within 3.0–10.8V). 8×AA → buck converter → 5V sensors. |
| 3 | Soldering plan? | I propose | Pre-solder Pico W headers (instructor prep). Motor leads soldered in Class 1 (good intro). Everything else: breadboard + jumper wires. |
| 4 | Code editor? | Everyone uses Mu | Younger students get pre-written code templates to modify; no block-based tools. |
| 5 | Track progression? | I propose | See [Track Progression](#track-progression) table. |
| 6 | Code block detail? | Functional description | Describe what each code block does, its inputs/outputs, how students interact — enough to drive a dev plan. |

### Unresolved Questions

These questions remain open and should be verified before or during the course:

1. **Pico W headers:** Does the Amazon Pico W in the BOM come with pre-soldered headers, or must the instructor solder them? (Assumed: instructor pre-solders — verify at purchase time.)
2. **Battery holder connector type:** Does the 8×AA holder have a barrel connector or bare leads? Affects whether soldering is needed. (Assumed: comes with wire leads needing connection — verify at purchase.)
3. **QTRX-MD-08RC mounting:** How does the sensor array physically mount under the chassis? Needs a bracket or standoffs. (Added to BOM — fabricate at Makersmiths via 3D print or laser cut.)
4. **Motor driver board pin mapping:** The Kitronik Robotics Board uses GP8 (SDA) and GP9 (SCL) for I2C to the PCA9685. All other GPIO pins are available. (Resolved in spec §2.2–§2.3.)
5. **Line width for tracks:** What line width should the Line Track Designer produce? Standard competition width is ~19 mm (¾ inch). (Assumed: ¾ inch black line on white paper — confirm.)

---

<!-- Reference-style links — educational/tutorial URLs only; see BOM for purchase links -->

[01]:https://makersmiths.org/
[02]:https://www.makerspaces.com/what-is-a-makerspace/
[03]:https://circuitpython.org/
[04]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[05]:https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython
[08]:https://circuitcanvas.com/
[09]:https://www.instructables.com/Advanced-Line-Following-Robot/
[10]:https://www.robotsforfun.com/webpages/robotcarchassis.html
[11]:https://en.wikipedia.org/wiki/Open-loop_controller
[12]:https://www.ntchip.com/electronics-news/difference-between-open-loop-and-closed-loop
[13]:https://en.wikipedia.org/wiki/Closed-loop_controller
[14]:https://www.mathworks.com/campaigns/offers/next/field-oriented-control-techniques-white-paper.html
[15]:https://en.wikipedia.org/wiki/Control_theory
[16]:https://www.emersonautomationexperts.com/2013/control-safety-systems/pid-control-history-and-advancements/
[17]:https://thekalmanfilter.com/kalman-filter-explained-simply/
[18]:https://www.geeksforgeeks.org/machine-learning/model-free-reinforcement-learning-an-overview/
[19]:https://www.geeksforgeeks.org/machine-learning/q-learning-in-python/
[20]:https://www.semanticscholar.org/paper/FUZZY-LOGIC-APPROACH-FOR-LINE-FOLLOWING-MOBILE-AN-Ismail-Zaman/94814e107c9607a4ae82286efa96989e79a955f1
[21]:https://learnbydoing.dev/pure-pursuit-controller/
[22]:https://wiki.purduesigbots.com/software/odometry
[23]:https://www.instructables.com/Make-a-FAST-Line-Follower-Robot-Using-PID/
[24]:https://www.arnabkumardas.com/line-follower-robot/line-follower-robot-rp2040-raspberry-pi-pico-qtr-8rc-pid-line-follower-robot-v1/
[25]:https://www.instructables.com/High-performance-Line-follower-Robot/
[32]:https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
