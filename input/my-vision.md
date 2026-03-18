
# 1 My Vision for a Line Following Robot Course at Makersmiths

I'm preparing for a makerspace course concerning the building & testing of a Line Following Robot (LFR).
Below is my vision of the courses goals, audience, structure, tools needed, and the course activities over time.

## Line Following Robot Course
This course has not been offered in the past so all materials need for this course must be created.
This includes the

### High Level Course Description

This hands-on course that takes students on a multi-iteration design journey,
transforming a simple $12 analog line-following robot kit
into a sophisticated microcontroller-based robot equipped with
sensor arrays, PID control, Kalman filters, and reinforced learning algorithm.
Students begin by assembling and understanding a basic kit that uses light-dependent resistors and analog comparators,
then progressively upgrade the hardware & software through each design iteration
— mirroring how real engineering teams evolve products.

Starting at around the iteration 3,
The students replace the analog brain with a
microcontroller and write code in CircuitPython,
and potentially using Claude AI as a coding assistant.
The course emphasizes hands-on learning over lectures,
mental models over math,
learning by experimenting instead of theory,
and iterative problem-solving over getting it right the first time.
Each iteration follows a consistent pattern:
identify weaknesses in the current design, propose and implement improvements, then test how it performs.

The course is self-paced within structured phases,
accommodating students ranging from age 12 through adults.
Students keep their robot kits after the course.
Periodic friendly competitions provide motivation
and fun but there are no grades
— completion of milestone assignments and active participation are what matter.
By the end, students will have built a competition-capable line following robot
and gained foundational skills in electronics, programming, motor control systems, and robotics.

The class for the course is expected to meet once a week for 2 hours, for a total of 8 weeks.
All required materials (hardware, software) will be purchased in advance.
All software used on the LFR, and other required software & hardware,
should also be developed and tested prior to the start of the course.
Today is March 16 and the course is expected to begin on June 15th.

### Course Target Audience

The target students range in age of 12 to 18, but there might be younger students too.
There could also be adults (parents most likely) helping the younger student,
and some adult students without children.
I believe the first class will likely have 2 students 12 to 14 old, 2 students 14 to 18 old
and 3 adult, two of which are parent and who assist the students.
The students will have some coding experience (Scratch) or basic Python experience, but not with hardware.
Students keep their robots at course end.

I'm assuming parents will not be building their own LFR,
only the student, and the instructor will have a LFR.
This means we have a total of 6 LFR to be built during the course

### Course Overall Structure

There will be a single class instructor, who is also the developer supporting this project.
There is not a fixed class schedule; the number of classes used is driven by the courses goals.

### Course Line Track Designer

Testing and experimenting with the LFR will take place on line tracks laid out via 11in by 8.5in paper tiles.
There will likely be a need for create multiple, custom line tracks.
A "Line Track Designer" software program will be necessary to generate the tracks,
ideally written in Python and runs on Ubuntu.

The Makerspace does have a flat floor area large enough for a line track of
4 × 3 tile track (~44 inches by 25.5 inches) with robot clearance on all sides.

### Course LFR Simulator

A Python coded 2D visual simulation of the LFR on a track defined by the Line Track Designer.
The simulate is an instructor & developer tool, not used by the students,
but could be use for class demonstrations too.
For example, using the simulator,
I would like to show how adjusting the PID tuning parameters effect the behavior of the LFR
or how the Reflectance Sensor Array improves performance of the LFR.

### Course Bill of Materials (BOM)
See the `input/my-bom.md` file

The [Raspberry Pi Pico W][06] has [26 pinouts designated as GPIO/PIO/PWM][38].
When the Raspberry Pi Pico W is installed in the Robotics Motor Driver Board,
some of those pins are used but ~18 are unoccupied and can be used for the LFR evolving design.

[CircuitPython][26] will be used to do all the coding on the Raspberry Pi Pico W.
The simulator should be written in [Python][39] and run in a Linux OS.
A Ubuntu computer and a laptop can be used as needed for the development and teaching of the course.

### Course Activities

The steps expressed below are not necessarily individual classes.
So the number of classes is likely to be greater/less than the number of steps.
I think of the above steps as "Design Sessions" where the LFR takes an important
change of direction to extract greater capability from the LFR.

1. The course kickoff with the instructor demonstrating a very simple LFR,
   specifically the [MiOYOOW Line Following Robot Car Kit][01].
   The instructor will discuss the MiOYOOW kit's theory of operation in detail with the students.
   The objective is to explain & show the students what a very simple LFR design can do.
   The instructor will also point out the strengths and limitation of this simple LFR.
   The students are then told that they will create their own simple LFR
   but using a more powerful platform and over a series of classes.
   Their LFR will evolve, over several design sessions, to include increasing capabilities
   which will making it a more effective LFR.
   The instructor will further motivate the students by
   describing how there exists many LFR competitive events around the world they could join.
   The instructor will also discuss, at a very high level,
   increased capabilities that will be given to their LFR via the multiple design session.
1. The students are then give the [Emo Smart Robot Car Chassis Kit][02]
   as there starting point for their LFR design.
   The student will keep this LFR at the end of the course.
   The students first task is to [assemble this kit][25].
1. The student needs more than this car chassis kit to create a LFR,
   so students will also be given
   [8 x AA Battery Holder][03] to power sensors via the 5V Buck Converter,
   [Raspberry Pi Pico W][06] to create a more powerful brain,
   [Robotics Motor Driver Board][04] to enable variable motor speed & direction,
   [IR Emitter/Phototransistor Pair][05] for improved line sensing,
   [400 Pin Solderless Prototype Board][24] to make the electronic interconnections easier,
   and [5V Buck Converter Module][08] to power the 5 volt digital devices.
   The instructor will guide the students on how to add these hardware items to the car chassis kit.
   We will call this the modified car chassis kit.
   The instructor will also tell how these items are potentially superior to those on the MiOYOOW kit.
1. When the modified car chassis kit is fully outfitted with the additional hardware,
   the instructor explain how the Raspberry Pi Pico W will need similar logic used by the MiOYOOW kit.
   This means the Raspberry Pi Pico W needs to programmed with [CircuitPython][26],
   using the [CircuitPython flashing process][27] and the instructor will discuss how this is done.
   The instructor will discuss the logic required for operating the IR Emitter/Phototransistor Pair,
   and controlling the motors.
1. The students will then build & test their version of a simple LFR,
   mimicking the behavior of the MiOYOOW kit demonstration by the instructor earlier.
   They will do this on the floor with a test track created via Line Track Designer software tool.
   The students should explore all the strengths and weakness of their current design.
   The should discuss what should be changed or added to get better results.
1. Via the LFR testing done in the previous step,
   it should be clear that the line sensing design for the modified car chassis kit
   has been programmed to have basically the same limitations as the MiOYOOW kit.
   We haven't yet taken advantage of the increased capabilities of our design,
   such as handling more sophisticated sensors or more complete motor control (e.g. variable speed and direction).
   To improve the sensor, student will remove the IR Emitter/Phototransistor Pair
   will replace it with the [QTRX-MD-08RC Reflectance Sensor Array][07] for more effective line detection.
   The instructor will explain the theory of operation for the QTRX-MD-08RC so the students
   understand the Raspberry pi Pico W logic that will be used.
   Students will test their design on the floor test track, and should see improves.
   The LFR does better following the line but it its speed is still rather slow.
1. The instructor will discuss with the students how to increase over all speed
   via logic changes on the Raspberry Pi Pico W.
   The instructor will discuss how the use of better line sensing
   could allow us to increase the speed of the LFR.
   Also discuss how dynamic speed control produce could produce better results
   (e.g. increase speed when the LFR is going straight, slow down on curves).
1. To control the speed of our LFR design remotely, we will have the Raspberry Pi Pico W,
   acting as a WiFi access point,
   hosting a WiFi website where a user interface can provide provide dynamic speed control.
   The LFR WiFi Access Point will have a unique SSID,
   with a default webpage, where dynamic speed controls will be supported.
   This user interface will gain increasing functionality in future changes to our design,
   but for now, we'll just set the speed of the LFR.
1. In the next build of the LFR, we will use dynamic speed control that was explored
   in the discussion in the previous step.
   We will first need to install [Speed Sensor Module][09] on each wheel
   and wire them to the Raspberry Pi Pico W.
   We use the logic to change speed & direction created earlier,
   but now we measure that speed/direction via the Speed Sensor Module.
   We'll use a [open-loop feedback control algorithm][28] on the Raspberry Pi Pico W to adjust the speed dynamically.
   The instructor will discuss [open-loop vs. closed-loop feedback control][29] with the students.
   Using a Line track on the floor, students can experiment with different
   speed settings to explore how to get improvements.
   The students will discover that manually setting the speed is helpful
   but what they really needs is the dynamics to be controlled by the LFR itself
   to make it responsive to the nature of the line.
   The LFR needs automatic control.  It needs to be autonomous.
   Instructor should introduce the topics of
   [feedback][33], [autonomous control][32], [control theory][31], [the history of PID controllers][30], etc.
1. From the discussion in the previous step,
   the student should anticipate the development of a PID controller for their LFR.
   Raspberry Pi Pico W logic will be supplied which will control the LFR speed & direction.
   The three tuning parameters for the PID will be tunable via the WiFi user interface webpage.
   Using the line track on the floor,
   students will use the manual trial-and-error and/or the Ziegler-Nichols
   tuning methods to set these tuning parameters.
   The students will be shown how sensor noise and other random events is effecting the car's performance
   and the topic of noise filtering will be introduced.
   The students will be given a basic understanding how [Kalman filters][34]
   can reduce the effects of noise and disturbances
1. The instructor will review the design discussion from the previous step
   and discuss how we will install the Kalman filter.
   The LFR will modified to include Kalman filtering
   and the LFR will be tested on a line following track.
   The strengths and short comings of this design will be discussed.
1. To fully define our control options for the LFR,
   the instructor will discuss the concepts of
   [active disturbance rejection control (ADRC),
   model predictive control (MPC),
   and reinforcement learning (RL)][32]
   using examples from current applications.
   The topic of Reinforcement Learning, Q-Learning in particular,
   will be given special emphasis,
   and the instructor will be disused it as a potential solution
   to the current solutions weaknesses.
   The topics discussed in the previous step concludes with the decision to build a
   [Model-free reinforcement learning][11] LFR using the [Q-Learning algorithm][12].
   The LFR will be outfitted with a Q-Learning Controller and tested.
1. The topics discussed in the previous step concludes with the
   decision to build a [Pure Pursuit Controller][13]
   but this controller will require an ability to look ahead for a point on the line
   and the use of [odometry][14] which are beyond our scope at this time.
   or [Fuzzy Logic Controller][36].
   The instructor close out the course letting the LFR go home with the students
   asking them to think more about how to improve the LFR for a competitive event.

Examples of LFRs:

* [Advanced Line Following Robot][19]
* [Make a FAST Line Follower Robot Using PID!][20]
* [Line Follower Robot : RP2040 Raspberry Pi Pico – QTR-8RC – PID Line Follower Robot V1][21]
* [High Performance Line Follower Robot][37]

Examples of LFR Simulators:

* [line-follower-simulator][16]
* [Line Follower Robot Simulator][17]
* [RobotraceSim — Line-Follower Robot Simulator][18]

Examples of Line Track Designers:

* [Line Track Designer][15]
* [Line-Track-Designer][22]
* [Customizable Line Following Tracks that you can print yourself Other NXT Tutorials][23]

[01]:https://www.amazon.com/MiOYOOW-Soldering-Electronics-Following-Competition/dp/B07ZH4XLQ3?th=1
[02]:https://www.amazon.com/gp/product/B01LXY7CM3/ref=ewc_pr_img_1
[03]:https://www.amazon.com/Thicken-Battery-Holder-Standard-Connector/dp/B07WP1CYYW?th=1
[04]:https://www.pishop.us/product/robotics-board-for-raspberry-pi-pico/
[05]:https://www.amazon.com/Infrared-Avoidance-Transmitting-Receiving-Photoelectric/dp/B07PFCC76N?th=1
[06]:https://www.amazon.com/Raspberry-Pi-Pico-Wireless-Bluetooth/dp/B0B5H17CMK
[07]:https://www.pololu.com/product/4348
[08]:https://www.amazon.com/dp/B0F1WB3LJ5?th=1
[09]:https://www.amazon.com/DAOKAI-Comparator-Measuring-Optocoupler-Detection/dp/B0B2NSQJDL
[11]:https://www.geeksforgeeks.org/machine-learning/model-free-reinforcement-learning-an-overview/
[12]:https://www.geeksforgeeks.org/machine-learning/q-learning-in-python/
[13]:https://learnbydoing.dev/pure-pursuit-controller/
[14]:https://wiki.purduesigbots.com/software/odometry
[15]:https://line-track-designer.readthedocs.io/en/latest/index.html
[16]:https://github.com/yanvgf/line-follower-simulator
[17]:https://github.com/Samarthnv05/line_follower_sim
[18]:https://github.com/Koyoman/robotrace_Sim
[19]:https://www.instructables.com/Advanced-Line-Following-Robot/
[20]:https://www.instructables.com/Make-a-FAST-Line-Follower-Robot-Using-PID/
[21]:https://www.arnabkumardas.com/line-follower-robot/line-follower-robot-rp2040-raspberry-pi-pico-qtr-8rc-pid-line-follower-robot-v1/
[22]:https://github.com/Quentin18/Line-Track-Designer
[23]:https://robotsquare.com/2012/11/28/line-following/
[24]:https://www.amazon.com/DEYUE-breadboard-Set-Prototype-Board/dp/B07LFD4LT6
[25]:https://www.robotsforfun.com/webpages/robotcarchassis.html
[26]:https://circuitpython.org/
[27]:https://learn.adafruit.com/pico-w-wifi-with-circuitpython/installing-circuitpython
[28]:https://en.wikipedia.org/wiki/Open-loop_controller
[29]:https://www.ntchip.com/electronics-news/difference-between-open-loop-and-closed-loop
[30]:https://www.emersonautomationexperts.com/2013/control-safety-systems/pid-control-history-and-advancements/
[31]:https://en.wikipedia.org/wiki/Control_theory
[32]:https://www.mathworks.com/campaigns/offers/next/field-oriented-control-techniques-white-paper.html
[33]:https://en.wikipedia.org/wiki/Closed-loop_controller
[34]:https://thekalmanfilter.com/kalman-filter-explained-simply/
[36]:https://www.semanticscholar.org/paper/FUZZY-LOGIC-APPROACH-FOR-LINE-FOLLOWING-MOBILE-AN-Ismail-Zaman/94814e107c9607a4ae82286efa96989e79a955f1
[37]:https://www.instructables.com/High-performance-Line-follower-Robot/
[38]:https://pip-assets.raspberrypi.com/categories/686-raspberry-pi-pico-w/documents/RP-008312-DS-1-pico-w-datasheet.pdf?disposition=inline
[39]:https://www.python.org/
