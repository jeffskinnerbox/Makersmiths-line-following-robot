# Course Syllabus: Evolving Design of a Line Following Robot

* **Organization:** [Makersmiths][01] — a community [makerspace][02] in Leesburg, Virginia
* **Format:** Hands-on workshop, 2 hours per class, weekly meetings
* **Audience:** Students ages 12–18 (adults welcome as helpers or independent learners)
* **Classes:** 8 core classes + up to 2 stretch classes (10 max)
* **Start Date:** June 15, 2026
* **Instructor:** 1 volunteer instructor who also develops pre-course software
* **Reference:** See [Appendix A](#appendix-a-course-development-prompt--qa) for the original course development prompt and all instructor Q&A

---

## 1. Course Description

This hands-on course takes students on a multi-iteration design journey, transforming a simple analog line-following robot into a sophisticated microcontroller-based robot equipped with a sensor array, PID controller, Kalman filter, and reinforcement learning algorithm. Students begin by watching the instructor demonstrate a basic MiOYOOW Line Following Robot Car Kit — a simple kit that uses light-dependent resistors and analog comparators — then build their own robot from an Emo Smart Robot Car Chassis Kit and progressively upgrade it through each design session.

Starting at Design Session 3, students replace the analog brain with a Raspberry Pi Pico W and write code in [CircuitPython][03], using the [Mu Editor][04] as their primary coding tool. The course emphasizes hands-on learning over lectures, mental models over math, learning by experimenting instead of theory, and iterative problem-solving over getting it right the first time. Each design session follows a consistent pattern: identify weaknesses in the current design, propose and implement improvements, then test how it performs.

The course is self-paced within structured phases, accommodating students ranging from age 12 through adults. Students keep their robot kits after the course. Periodic friendly competitions (roughly every other class) provide motivation and fun, but there are no grades — completion of milestone assignments, active participation, and a simple build journal are what matter. By the end, students will have built a competition-capable line following robot and gained foundational skills in electronics, programming, motor control systems, and robotics.

All required materials (hardware, software) are purchased in advance by the instructor. See the Bill of Materials for costs, quantities, and sourcing details.

---

## 2. Learning Objectives

By the end of this course, students will be able to:

### Hardware & Electronics

* Assemble a robot car chassis from a kit and identify its mechanical components (motors, wheels, battery holder, frame)
* Wire electronic components (sensors, motor driver board, buck converter, breadboard) to a microcontroller
* Install and replace sensors on a robot — from a simple IR emitter/phototransistor pair to a multi-sensor reflectance array
* Attach speed sensors to wheels and connect them to the microcontroller for feedback

### Programming

* Write and flash [CircuitPython][03] programs onto a Raspberry Pi Pico W using the [Mu Editor][04]
* Read sensor values (digital and analog) and use them to control motor speed and direction
* Implement a line-following algorithm that reacts to sensor input
* Modify and tune code parameters through a WiFi-based browser interface

### Robotics Concepts

* Explain what a line following robot does and why it matters in real-world robotics
* Compare sensor technologies (IR pair vs. reflectance sensor array) and explain when each is appropriate
* Describe the difference between open-loop and closed-loop control in plain language
* Tune a PID controller using trial-and-error and observe how each parameter affects robot behavior
* Explain what a Kalman filter does (smooths noisy sensor data) without needing the underlying math
* Describe what Q-Learning is (the robot learns from experience) and observe it improving over time

### Design & Problem-Solving

* Follow an iterative design process: identify a problem, propose a fix, build it, test it, document it
* Keep a build journal documenting design decisions, test results, and observations
* Participate in friendly competitions that test robot speed, consistency, and line-following accuracy
* Troubleshoot hardware and software issues by systematic observation and testing

---

## 3. Prerequisites

### Required

* **Age:** 12 or older (younger students may participate with an adult partner)
* **Math:** Basic arithmetic only — all advanced concepts (PID, Kalman, Q-Learning) are taught as mental models with tunable knobs, not formulas
* **Attendance:** Commit to attending all scheduled classes; each class builds on the previous one
* **Laptop:** Students must bring their own laptop — Windows, Mac, or Linux (no Chromebooks); must have a USB port and WiFi capability

### Recommended but Not Required

* Some coding experience (Scratch, basic Python, or similar)
* Curiosity about how things work
* Willingness to experiment and learn from mistakes

### Provided by the Course

* All electronic components and hardware (students keep their robot at course end)
* All software tools (free to install)
* Soldering equipment and hand tools (provided by [Makersmiths][01])
* Step-by-step build guides and instructor-provided code blocks for complex sections
* Line tracks for testing (printed on standard paper using the Line Track Designer tool)

---

## 4. Technology Requirements

### Hardware Per Student

| Component | When Introduced | Notes |
|:----------|:---------------|:------|
| Emo Smart Robot Car Chassis Kit | Class 1 | Base platform; students keep at course end |
| 8 x AA Battery Holder | Class 2 | 12V power source for motors |
| 9V Battery Clip Connector | Class 2 | 9V power source |
| Raspberry Pi Pico W | Class 2 | Microcontroller running CircuitPython |
| Robotics Motor Driver Board | Class 2 | Motor speed and direction control |
| IR Emitter/Phototransistor Pair | Class 2 | Initial line sensor (replaced at Class 4) |
| 5V Buck Converter Module | Class 2 | Powers 5V digital devices from battery |
| 400 Pin Solderless Prototype Board | Class 2 | Breadboard for wiring connections |
| QTRX-MD-08RC Reflectance Sensor Array | Class 4 | 8-sensor array for precise line detection |
| Speed Sensor Module (×2) | Class 7 | One per wheel; measures wheel rotation speed |

> **Note:** For costs, quantities, and sourcing details, see the Bill of Materials (BOM). The BOM is the single source of truth for all purchasing information.

### Demonstration Unit (Instructor Only)

| Component | Notes |
|:----------|:------|
| MiOYOOW Line Following Robot Car Kit | Pre-assembled demo for Class 1 kickoff |

### Shared Tools (Provided by Makersmiths)

* Soldering iron, solder, flux, solder wick, solder sucker
* WiFi with internet access
* Flat floor area for line track testing (~44 × 25.5 inches minimum)
* White 8.5 × 11 inch paper for printed line tracks

### Student-Provided

* Laptop computer (Windows, Mac, or Linux — no Chromebooks)
* Protective eye gear (for soldering sessions)
* Build journal (physical notebook or digital — see [Assignment Descriptions](#8-assignment-descriptions))

### Software (All Free)

| Software | Purpose |
|:---------|:--------|
| [CircuitPython][03] | Programming language for the Raspberry Pi Pico W |
| [CircuitPython Installation Guide][05] | How to flash CircuitPython onto the Pico W |
| [Mu Editor][04] | Primary code editor for writing and uploading CircuitPython programs |
| [Piper Make][06] | Block-based coding alternative for beginners |
| [BIPES][07] | Block-based coding platform for MicroPython/CircuitPython |
| [Circuit Canvas][08] | Online tool for creating circuit wiring diagrams |

---

## 5. Course Structure & Format

### Class Flow

Each 2-hour class follows this general structure:

| Time | Activity | Description |
|:-----|:---------|:------------|
| 0:00–0:10 | Review & Q&A | Recap previous class, answer questions, review build journals |
| 0:10–0:25 | Mini-Lecture | Introduce new concept or component using demos and mental models |
| 0:25–1:30 | Guided Build | Hands-on assembly, wiring, coding, and testing with instructor support |
| 1:30–1:50 | Testing & Documentation | Run robots on line track, record observations in build journal |
| 1:50–2:00 | Wrap-Up | Summarize what was accomplished, preview next class, competition results (if applicable) |

> Competitions replace part of the Testing & Documentation block when scheduled.

### Course Phases

| Phase | Classes | Focus | Design Sessions |
|:------|:--------|:------|:----------------|
| **Phase 1: Foundation** | 1–3 | Build it, make it move | DS1–DS5 |
| **Phase 2: Smart Control** | 4–7 | Better sensing, speed control, WiFi | DS6–DS9 |
| **Phase 3: Autonomous** | 8–10* | PID, Kalman, Q-Learning | DS10–DS13 |

*Classes 9–10 are stretch classes if needed.

### Pacing & Age Differentiation

This course accommodates a mixed-age classroom (ages 12 through adult):

* **Younger students (12–14):** Receive pre-built code templates and step-by-step wiring guides with diagrams. Buddy-paired with an adult helper when available. Focus on assembly, testing, and observing behavior.
* **Older students (15–18):** Encouraged to modify code, experiment with parameter values, and attempt challenge extensions (e.g., tuning PID values independently before instructor guidance).
* **Adults (helpers and independent learners):** Support younger students while working on their own robots. May explore deeper technical concepts or alternative coding approaches.
* **Self-paced within structure:** All students work through the same design sessions, but faster students can attempt bonus challenges while others catch up. No student is left behind — the instructor adjusts pacing based on the slowest builder.
* **Makerspace access:** Students may access [Makersmiths][01] facilities outside of class time only when coordinated with the instructor.

---

## 6. Lessons Breakdown

### Phase 1: Foundation — Build It, Make It Move (Classes 1–3)

**Class 1 — Course Kickoff: MiOYOOW Demo & Chassis Assembly**
*Design Sessions 1 & 2*

* Welcome, introductions, and course overview — what students will build and why
* Instructor demonstrates the MiOYOOW Line Following Robot Car Kit: how it works, what it can do, and its limitations
* Discussion: What is a line following robot? Why do they matter? Brief look at [competitive LFR events][09]
* Students receive their Emo Smart Robot Car Chassis Kit and begin [assembly][10]
* Identify mechanical components: motors, wheels, battery holder, frame, caster wheel
* Preview of the design journey: how their robot will evolve over the coming weeks
* **Take-home:** Start your build journal — sketch your chassis, note what you learned

---

**Class 2 — Upgrading the Brain: Pico W + Motor Driver + IR Sensors**
*Design Session 3*

* Install the Raspberry Pi Pico W onto the Robotics Motor Driver Board
* Wire the 8 x AA Battery Holder, 9V Battery Clip Connector, and 5V Buck Converter Module
* Connect the IR Emitter/Phototransistor Pair for basic line sensing
* Use the 400 Pin Solderless Prototype Board for wiring connections
* [Flash CircuitPython][05] onto the Pico W and verify it works
* Install and configure the [Mu Editor][04] on student laptops
* Write first program: read sensor values and print them to the console
* Instructor explains how the IR sensor pair works compared to the MiOYOOW's LDR sensors
* **Mini-Challenge #1: Motor Test** — Who can make their robot drive in a straight line for 3 feet?
* **Build journal:** Document your wiring, sketch the circuit

---

**Class 3 — First Line Follower: Code, Flash, Test**
*Design Sessions 4 & 5*

* Write line-following logic: if left sensor sees line, turn right; if right sensor sees line, turn left
* Flash the program and test on a printed line track
* Observe behavior: What works? What doesn't? Why does the robot wobble or lose the line?
* Students explore strengths and weaknesses of the two-sensor design
* Group discussion: What would make this better? (More sensors? Faster reactions? Variable speed?)
* Compare performance to the MiOYOOW demo from Class 1
* **Mini-Challenge #2: First Run** — Complete one lap of the test track (any speed, just finish!)
* **Milestone Assignment: Phase 1 — Foundation Complete** — Robot assembled, programmed, and follows a line. Build journal entry with wiring diagram, code description, and test observations.

---

### Phase 2: Smart Control — Better Sensing, Speed Control, WiFi (Classes 4–7)

**Class 4 — Sensor Array Upgrade**
*Design Session 6*

* Remove the IR Emitter/Phototransistor Pair
* Install the QTRX-MD-08RC Reflectance Sensor Array — an 8-sensor array for precise line detection
* Instructor explains how the array works: each sensor returns a value, the combined reading tells you exactly where the line is
* Mental model: think of the sensor array as 8 tiny eyes instead of 2
* Write code to read the array and calculate a line position value
* Test on the line track — observe how much smoother the robot follows the line
* Discussion: The robot follows better, but it's still slow. How can we make it faster?
* **Build journal:** Compare IR pair vs. sensor array results, sketch the new wiring

---

**Class 5 — Variable Speed & Better Line Following**
*Design Session 7*

* Discussion: How can better line sensing let us increase speed?
* Implement variable speed: go faster on straight sections, slow down on curves
* Use the sensor array's position value to scale motor speed — more centered = faster, off-center = slower
* Tune speed parameters by trial and error on the test track
* Introduction to the idea of dynamic speed control — the robot adjusts itself instead of running at one fixed speed
* **Mini-Challenge #3: Speed Run** — Fastest lap time while staying on the line
* **Build journal:** Record your speed settings and lap times

---

**Class 6 — WiFi Access Point & Browser Control UI**
*Design Session 8*

* Configure the Raspberry Pi Pico W as a WiFi Access Point with a unique SSID
* Instructor provides code block for the WiFi AP and browser-based user interface
* Students connect their laptop to the robot's WiFi network
* Use a web browser to view sensor data and adjust speed settings in real time
* Discussion: Why is remote control useful? (Tuning without reprogramming, real-time monitoring)
* Test on the line track while adjusting speed via the browser interface
* Preview: This interface will gain more controls in future classes (PID tuning knobs)
* **Build journal:** Screenshot or sketch the browser interface, note how remote tuning changed performance

---

**Class 7 — Speed Sensors + Closed-Loop Feedback**
*Design Session 9*

* Install Speed Sensor Module on each wheel (2 total) and wire to the Pico W
* Instructor explains what the speed sensors measure (wheel rotation speed via IR optocoupler)
* Write code to read speed sensor values and display them in the browser interface
* Implement [open-loop speed control][11]: set a target speed and measure actual speed
* Discussion: [Open-loop vs. closed-loop control][12] — why knowing your actual speed matters
* Experiment: Set different speeds and observe how well the robot hits the target
* Students discover that manual speed setting helps, but the robot needs to control itself to handle curves and straightaways automatically
* Instructor introduces the concepts of [feedback control][13], [autonomous control][14], and [control theory][15]
* Brief history: [How PID controllers were invented and where they're used today][16]
* **Mini-Challenge #4: Consistency** — Most consistent lap times across 3 runs
* **Milestone Assignment: Phase 2 — Smart Control Complete** — Sensor array installed, variable speed working, WiFi interface operational, speed sensors reporting. Build journal entry comparing performance at each upgrade step.

---

### Phase 3: Autonomous — PID, Kalman, Q-Learning (Classes 8–10)

**Class 8 — PID Controller: Tuning for Performance**
*Design Session 10*

* Instructor introduces the PID controller as three tuning knobs: how far off am I? (P), how long have I been off? (I), how fast am I drifting? (D)
* Mental model: P is the steering wheel, I is the memory, D is the anticipation
* Instructor provides PID controller code block — students load it onto their robot
* Use the WiFi browser interface to tune the three PID parameters in real time
* Tuning methods: start with P only, then add D, then add I (manual trial-and-error)
* Discuss the [Ziegler-Nichols tuning method][16] as a systematic alternative
* Test on the line track — observe how each knob changes robot behavior
* Discussion: The robot is much better now, but noisy sensor readings still cause jittery movement
* Instructor introduces the concept of sensor noise and why filtering matters
* Preview: Next class we'll add a filter to smooth out that noise
* **Build journal:** Record your PID tuning values and describe what each change did

---

**Class 9* — Kalman Filter: Smoothing the Noise**
*Design Session 11*

* Review: What is sensor noise? Why does it cause problems for the PID controller?
* Instructor introduces the [Kalman filter][17] as a "smart averaging" tool — it trusts the sensor reading and the prediction, then blends them
* Mental model: Like a weather forecast — you combine what the thermometer says now with what you expected based on yesterday
* Instructor provides Kalman filter code block — students add it to their robot's sensor pipeline
* Before/after comparison: Run the robot with and without the filter, observe the difference
* Tune filter parameters via the WiFi interface
* Discussion: What else could we improve? The robot follows the line smoothly but doesn't learn from experience
* Instructor introduces the idea of the robot learning on its own — [reinforcement learning][18]
* **Mini-Challenge #5: Smooth Operator** — Smoothest line following (least wobble) over 3 laps
* **Build journal:** Compare filtered vs. unfiltered performance, note your filter settings

---

**Class 10* — Q-Learning + Course Wrap-Up & Final Competition**
*Design Sessions 12 & 13*

* Instructor explains [reinforcement learning][18] and [Q-Learning][19] using everyday examples: the robot tries different actions, gets rewards for good behavior, and gradually learns the best strategy
* Mental model: Like training a pet — reward good behavior, ignore bad behavior, and over time the pet figures it out
* Brief overview of other control approaches: [active disturbance rejection control, model predictive control][14], and [fuzzy logic control][20] — what they are and where they're used (awareness only, not implemented)
* Instructor provides Q-Learning controller code block — students load it and let the robot train on the track
* Watch the robot improve over multiple training runs
* Discussion: What worked best? PID? Kalman + PID? Q-Learning? Each approach has trade-offs
* Mention of advanced techniques beyond this course: [Pure Pursuit Controller][21] (requires look-ahead and [odometry][22])
* **Final Competition** — Students compete in multiple categories:
  * Fastest lap
  * Most consistent (least variation across 3 laps)
  * Smoothest (least wobble)
  * Best build journal
  * People's choice (voted by all participants)
* Course wrap-up: What did we learn? How could we keep improving? Where do LFR competitions happen?
* Students take their robots home
* **Milestone Assignment: Phase 3 — Autonomous Complete** — PID tuned, Kalman filter added, Q-Learning tested. Final build journal entry reflecting on the full design journey from analog kit to autonomous robot.

*Classes 9–10 are stretch classes. If the course stays at 8 classes, PID tuning (Class 8) serves as the capstone, and Kalman + Q-Learning are presented as take-home exploration topics with provided code blocks.

---

## 7. Recommended & Supplemental Studies

### Line Following Robot Examples

* [Advanced Line Following Robot][09] — Instructables guide to building a capable LFR
* [Make a FAST Line Follower Robot Using PID!][23] — Instructables PID-based LFR build
* [Line Follower Robot: RP2040 Raspberry Pi Pico – QTR-8RC – PID Line Follower Robot V1][24] — Pico-based LFR with PID control
* [High Performance Line Follower Robot][25] — Instructables guide to high-performance LFR design

### LFR Simulators

* [line-follower-simulator][26] — Python-based LFR simulator
* [Line Follower Robot Simulator][27] — Another Python LFR simulator
* [RobotraceSim — Line-Follower Robot Simulator][28] — Robotrace-style simulator

### Line Track Designers

* [Line Track Designer][29] — Python tool for generating line tracks
* [Line-Track-Designer][30] — Another track designer tool
* [Customizable Line Following Tracks][31] — Printable line following track designs

### Control Theory & Algorithms

* [Open-Loop Controller][11] — Wikipedia overview of open-loop control
* [Open-Loop vs. Closed-Loop Control][12] — Comparison of control approaches
* [Closed-Loop Controller (Feedback)][13] — Wikipedia overview of feedback control
* [Control Theory][15] — Wikipedia introduction to control theory
* [History of PID Controllers][16] — How PID control was invented and evolved
* [Kalman Filter Explained Simply][17] — Plain-language Kalman filter explanation
* [Model-Free Reinforcement Learning][18] — GeeksForGeeks overview of model-free RL
* [Q-Learning in Python][19] — GeeksForGeeks Q-Learning tutorial

### Hardware References

* [Raspberry Pi Pico W Datasheet][32] — Pinout and specifications
* [Emo Smart Robot Car Chassis Assembly Guide][10] — Step-by-step chassis build
* [CircuitPython Installation on Pico W][05] — How to flash CircuitPython

### Software & Coding Tools

* [CircuitPython][03] — Official CircuitPython site
* [Mu Editor Installation][04] — Getting started with Mu Editor
* [Piper Make][06] — Block-based coding for beginners
* [BIPES][07] — Block-based integrated platform for embedded systems
* [Circuit Canvas][08] — Online tool for creating circuit wiring diagrams
* [MicroPython][33] — MicroPython official site
* [Python REPL Guide][34] — For experienced coders who prefer the command line
* [Block-Based Coding Overview][35] — Introduction to visual programming

### Other Resources

* [Makersmiths][01] — Course host makerspace
* [What is a Makerspace?][02] — Overview of makerspaces
* [Python][36] — Official Python site
* [Autonomous Control & MPC][14] — MathWorks overview of control techniques
* [Fuzzy Logic for Line Following][20] — Academic paper on fuzzy logic LFR control
* [Pure Pursuit Controller][21] — Learn-by-doing pure pursuit explanation
* [Odometry][22] — Purdue SIGBots odometry wiki

---

## 8. Assignment Descriptions

### Ongoing: Build Journal

Every student keeps a simple build journal (physical notebook or digital document) throughout the course. After each class, write or sketch:

* What you built or changed today
* What worked and what didn't
* Any measurements or test results (lap times, sensor readings, tuning values)
* Questions you still have

There is no required length or format — a few sentences and a sketch is fine. The journal is yours to keep as a reference for future projects. The instructor will briefly review journals at the start of each class.

### Milestone Assignments

One milestone per phase. These are completion-based — no grades, no rubrics. You pass the milestone when your robot works and your journal documents the journey.

| Milestone | After Class | What to Demonstrate |
|:----------|:-----------|:-------------------|
| **Phase 1: Foundation Complete** | Class 3 | Robot assembled, programmed with basic line-following code, completes a lap on the test track. Build journal has wiring diagram, code description, and test observations. |
| **Phase 2: Smart Control Complete** | Class 7 | Sensor array installed and reading, variable speed working, WiFi interface operational, speed sensors reporting data. Build journal compares performance at each upgrade step. |
| **Phase 3: Autonomous Complete** | Class 10* | PID controller tuned, Kalman filter added (if reached), Q-Learning tested (if reached). Final build journal entry reflecting on the full design journey. |

*If the course ends at Class 8, the Phase 3 milestone covers PID tuning only.

### Competitions

Friendly competitions happen roughly every other class. Rules for all competitions:

* **Multiple attempts allowed** — best run counts
* **No elimination** — everyone participates in every competition
* **Age brackets:** 12–14, 15–18, Adults (if enough participants per bracket)
* **Awards:** Recognition only (e.g., certificates, bragging rights) — no prizes that create unfair advantage

| Competition | Class | Challenge |
|:------------|:------|:----------|
| Mini-Challenge #1: Motor Test | 2 | Drive in a straight line for 3 feet |
| Mini-Challenge #2: First Run | 3 | Complete one lap of the test track (any speed) |
| Mini-Challenge #3: Speed Run | 5 | Fastest lap time while staying on the line |
| Mini-Challenge #4: Consistency | 7 | Most consistent lap times across 3 runs |
| Mini-Challenge #5: Smooth Operator | 9* | Smoothest line following (least wobble) over 3 laps |
| Final Competition | 10* | Multiple categories: fastest, most consistent, smoothest, best journal, people's choice |

*Competitions in Classes 9–10 occur only if the course extends to stretch classes. If the course is 8 classes, Class 8 includes a modified final competition covering fastest lap, most consistent, and best build journal.

---

## Appendix A: Course Development Prompt & Q&A

### Original Prompt

The following prompt was used to generate this syllabus (reproduced verbatim from the instructor's prompt document):

> Read the @input/*.md file only.
> From this, you are to create a course syllabus document using the syllabus_generator skill.
> Place your document in the file @docs/lfr-syllabus.md.
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

All questions asked during syllabus generation and the instructor's responses:

| # | Question | Answer |
|:--|:---------|:-------|
| 1 | Your vision says "8 weeks, 2 hrs/week" but also lists ~12 Design Sessions and says "the number of classes is driven by the course goals." How should the syllabus handle this? | 8 class target, stretch OK |
| 2 | What competitions should the syllabus include? The vision mentions "periodic friendly competitions" but gives no specifics. | Every other class |
| 3 | Students must bring a laptop (listed in BOM under Tools). Any OS constraints? CircuitPython tools work on Windows/Mac/Linux but NOT Chromebook. | Win/Mac/Linux required |
| 4 | What math level should the syllabus assume? PID tuning and Kalman filters involve math concepts. | Black-box / mental models |
| 5 | Should students keep a build journal as an ongoing assignment? If so, what format? | Simple notebook (physical or digital) |
| 6 | Which code editor should the syllabus recommend as the primary tool for students writing CircuitPython? | Mu Editor |
| 7 | The BOM lists optional items (I2C Rotary Encoder Board, OLED Display). Should the syllabus include these as part of the course or mention them as take-home extras? | Omit entirely |
| 8 | Can students access the Makersmiths facility outside of class time to work on their robots? | Only coordinated with the instructor |

---

<!-- Reference-style links — educational/tutorial URLs only; see BOM for purchase links -->

[01]:https://makersmiths.org/
[02]:https://www.makerspaces.com/what-is-a-makerspace/
[03]:https://circuitpython.org/
[04]:https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor
[05]:https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython
[06]:https://www.playpiper.com/pages/piper-make?srsltid=AfmBOooPN66GibaOclgxc1JwWyIwzxgq-43qIoW0lPFQahqRiIQIw7jy
[07]:https://bipes.net.br/ide/
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
[26]:https://github.com/yanvgf/line-follower-simulator
[27]:https://github.com/Samarthnv05/line_follower_sim
[28]:https://github.com/Koyoman/robotrace_Sim
[29]:https://line-track-designer.readthedocs.io/en/latest/index.html
[30]:https://github.com/Quentin18/Line-Track-Designer
[31]:https://robotsquare.com/2012/11/28/line-following/
[32]:https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
[33]:https://micropython.org/
[34]:https://realpython.com/python-repl/
[35]:https://subjectguides.york.ac.uk/coding/scratch
[36]:https://www.python.org/
