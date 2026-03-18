
# My Claude Code Prompts
Start with the following after entering Claude Code:

```bash
# clear claude code's contest
/clear

# initialize the CLAUDE.md file
/init

# set model to opus
/model opus

# use planning mode
/plan

# work hard
/effort high
```

## Creation of a Course Syllabus
### 1st Claude Code Prompt
Read the @input/*.md files only.
From this, you are to create a course syllabus document using the syllabus_generator skill.
Place your document in the file @docs/lfr-syllabus.md.

Within the document you create, include this prompt,
and all question you ask me, along with my responses.
Place this in the document as an appendix and reference it at the beginning of the document
and anywhere else in the text when its a useful reference.

In a subsequent steps, I expect this document will used to help prepare
the course design and materials developed for the course.
Think Very Hard about what must be specified in this document so a robust course design & robot development plan
can be created for the Line Following Robot.

I expect there will be some issues,
so use the AskUserQuestions tool for all things that require further clarification.

#### Finishing Prompt
Review all @input/*.md and @docs/*.md files and make sure the are consistent and correct.

---

## Creation of a Course Lesson Plan
Start with the following:

```bash
# clear claude code's contest
/clear

# initialize the CLAUDE.md file
/init

# set model to opus
/model opus

# use planning mode
/plan

# work hard
/effort high
```

### 2nd Claude Code Prompt
Along with CLAUDE.md, read only @input/*.md and @docs/*.md files.
Create a course lesson plan document using the lesson_plan_generator skill.
Place your creation in the file @docs/lfr-lesson-plan.md.

Within the document you create, include this prompt,
and all question you ask me, along with my responses.
Place this in the document as an appendix and reference it at the beginning of the document
and anywhere else in the text when its a useful reference.

In a subsequent steps, I expect this document will used to help prepare
the course design and materials developed for the course.
Think Very Hard about what must be specified in this document so a robust course design & robot development plan
can be created for the Line Following Robot.

I expect there will be some issues,
so use the AskUserQuestions tool for all things that require further clarification.

#### Finishing Prompt
Review all @input/*.md and @docs/*.md files and make sure the are consistent and correct.

---

## Creation of the Specification Document
Start with the following:

```bash
# clear claude code's contest
/clear

# initialize the CLAUDE.md file
/init

# set model to opus
/model opus

# use planning mode
/plan

# work hard
/effort high
```


### 3rd Claude Code Prompt

Along with CLAUDE.md, read only @input/*.md and @docs/*.md files.
Create a specification document, reflecting the incrementally development in the Line Following Robot (LFR) course.
I need this this specification document to help prepare me for delivering the course and all software required for the course.
I want all the components implied bellow (both hardware and software) to be built and tested in advance of the course.
Place your creation in the file @docs/lfr-specification.md.

I want the LFR software to be built in a modular form, such that, a software subsystem in step N
can be pulled out a replaced with a new subsystem in step N+1 (e.g. PID Controller replaced with Q-Learning Controller)
Make sure you include the Line Track Designer and LFR Simulators software in this specification document.
I plan to build and test all software prior to the start of the course.
Think harder about the software architecture and testing of the of this project.

Within the document you create, include this prompt,
all question you ask me, along with my responses.
Place this in an appendix and reference it at the beginning of the development plan
and anywhere else in the text when its a useful reference.

In a subsequent steps, I need this this specification document to help prepare a detailed development plan.
Think Very Hard about what must be specified in the specification document so a robust development plan can be created.

I expect there will be some issues,
so use the AskUserQuestions tool for all things that require further clarification.

#### Finishing Prompt
Review all @input/*.md and @docs/*.md files and make sure the are consistent and correct.

---

## Creation of the Development Plan Document
Start with the following:

```bash
# clear claude code's contest
/clear

# initialize the CLAUDE.md file
/init

# use planning mode
/mode plan
```


### 4th Claude Code Prompt

Along with CLAUDE.md, read only @input/*.md and @docs/*.md files.
Create create a development plan, to be called @docs/lfr-development-plan.md,
describing how & when thing are to be created / build.
The development plan must reflecting the incrementally build approach outline in the Line Following Robot (LFR) course.

Make sure to cover the all major software components and their build order,
key technical decisions to resolve upfront (e.g., which Python GUI library for the simulator),
a rough phasing that mirrors your courses Design Sessions,
and any external dependencies or risks (like CircuitPython library availability for the QTRX sensor).

I want to build the LFR via a phased plan, and at the end of each build phase,
three to eight tests, I'll call these "test-gates",
will be performed to validate what has been created within that phase.
Do not move onto the next phase until all test-gates pass.

Within this phased plan, there will be a sets of sequenced phases, when completed successfully,
are called a milestone.
A milestone will contain all the required software for a specific class day within the course.

Produce the plan as a living document so it can be update as the project evolves,
not just a one-time artifact.
I want it to serves as an ongoing reference rather than going stale after the first few sessions.
Given the scope of this project — firmware, a simulator, a track designer, and incremental design sessions —
I want this plan to save significant back-and-forth with Claude Code over the course of development.

Within the document you create, include this prompt,
all question you ask me, along with my responses.
Place this in an appendix and reference it at the beginning of the development plan
and anywhere else in the text when its a useful reference.

Think Hard about what must be done to create a robust plan.

I expect there will be some issues,
so use the AskUserQuestions tool for all things that require further clarification.

#### Finishing Prompt
Review all @input/*.md and @docs/*.md files and make sure the are consistent and correct.

---

## Working With Claude Code
Start with the following:

```bash
# clear claude code's contest
/clear

# initialize the CLAUDE.md file
/init

# use planning mode
/mode plan
```


### Claude Code Interaction

I asked Claude Code to guide me on what needs to be done and it stepped me through the development plan (aka `lfr-development-plan.md`)

---









1st Claude Code Prompt
Preparing a MakerSpace course syllabus for students from age 12 to 18.
There could also be adults helping the student, and some adult students without children.
The students are to build a Line Following Robot as outlined in the documents in this directory system.
Create a Markdown file for me titled "Syllabus: Evolving Design of Line Following Robot".

The essential components of the syllabus are:

* Course Description: A 5-15 sentence overview of the content and scope.
* Learning Objectives/Outcomes: A list of measurable, actionable skills or knowledge students will gain
  (e.g., "By the end of this course, students will be able to...").
  Identify what students should know or be able to do by the end of the course.
* Prerequisites: Required prior courses or knowledge.
* Course Structure/Format: Description of how the class will be taught
  (e.g., lecture, seminar, hands-on lab, hybrid, flipped)
* Lessons Breakdown: Start with the final learning goals and assessments, then design the lessons to support them.
  Break the course into weekly or daily topics and modules. A clear, week-by-week, or topic-by-topic outline.
* Recommended/Supplemental Studies: Identify required textbooks, software, or readings, videos, etc.
* Technology Requirements: Hardware/software needed (e.g., tools, specific software, etc.).
* Assignment Descriptions: There is no grading, quizzes, etc.,
  but there will be periodic competitions where students will try for the fastest, most agile, etc. robot built by the students.

*Claude Code Prompt:
In today's industry, what is the definition of a robot?  Give me a definition/description that would be widely agreed upon.*

*Claude Code Prompt:
What is a good definition of automaton and how does it differ from a robot?*

*Claude Code Prompt:
Give me some examples of elaborate mechanical figures from the 1700s that could "write" with a pen or do other operations?*

*Claude Code Prompt:
What are the definitions for Open-Loop and Closed-Loop Systems?*

*Claude Code Prompt:
I have purchased the following item: "MiOYOOW Line Following Robot Car Kit".  Here is the link to the purchasing
website: <https://www.amazon.com/MiOYOOW-Soldering-Electronics-Following-Competition/dp/B0732Z1FZC?th=1>.  I want
you to write a description of how this car operates suitable for a high school student.  Assume very basic
understanding of electronics.  Make the description less than 100 words.
I will call this the "Theory of Operation" for this car.*

*Claude Code Prompt:
This Theory of Operation is very good but could you improve it if I remove the word count limitation?*

*Claude Code Prompt:
I would like to evolve the MiOYOOW Line Following Robot Car so that it becomes a more effective robot.
Specifically, I would like to change the LDR sensors (e.g. more sensors, different type of sensors, etc.)
to get better overall performance (e.g. less wandering off the line, navigate successfully sharp turns in the line, etc.).
Recommended what I could do.*

*Claude Code Prompt:
I plan to teach a makerspace class for 12+ year old.
The topic is a Line Following Robot that I wish to evolve its capabilities from IR sensor pair,
to IR sensor array, to using PID controller, to finely a Q-Learning controller.
I want to use simple brush motors and a Raspberry Pi Pico.
I need a kit solution that I can use and incrementally build up the capabilities over a series of classes.
Can you give me a list of candidate kits that I could potentially use?*
