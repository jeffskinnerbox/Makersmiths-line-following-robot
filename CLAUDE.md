# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repo is a course-preparation workspace for a **Line Following Robot (LFR)** makerspace course at [Makersmiths](https://makersmiths.org/). The course runs 8 weeks (2 hrs/session), targeting students ages 12–18, starting June 15 2026. The course is not yet taught — all materials must be created before it starts.

The LFR evolves across ~13 Design Sessions: analog kit → Raspberry Pi Pico W + CircuitPython → IR sensor array → PID controller → Kalman filter → Q-Learning controller.

## Directory Layout

```
input/          # Instructor-supplied specs (read-only source of truth)
  my-vision.md      # Full course vision, hardware choices, design session sequence
  my-bom.md         # Bill of materials with sources and unit costs
  my-claude-prompts.md  # Reusable Claude prompts for generating course docs
docs/           # Generated course documents (see "Document Status" below)
lecture_notes/  # Generated reference documents (theory of operation, history, etc.)
.claude/
  commands/     # Slash commands: /create-syllabus, /create-lesson-plan, /create-plan
  skills/       # Auto-invoked skills (see below)
    shared/definitions.md  # Shared vocabulary — read before writing any course doc
```

## Skills

Skills in `.claude/skills/` are auto-invoked when requests match their description. Each has a `SKILL.md`.

| Skill | Produces |
|:------|:---------|
| `syllabus_generator` | Course syllabus (`docs/lfr-syllabus.md`) |
| `lesson_plan_generator` | Per-session lesson plans (`docs/lfr-lesson-plan.md`) |
| `bill_of_materials_generator` | BOM (`input/my-bom.md` is the source of truth) |
| `explainer` | Plain-language explanations of technical concepts |
| `history_and_application` | History & applications documents (`lecture_notes/`) |
| `theory_of_operation` | Theory of operation documents (`lecture_notes/`) |
| `pptx_maker` | PowerPoint presentations from any input file |

**Key rule:** Cost/pricing/sourcing belongs exclusively in the BOM. Syllabi and lesson plans reference component names but never purchase links or prices.

## Slash Commands

- `/create-syllabus` — generate course syllabus using `syllabus_generator` skill
- `/create-lesson-plan [spec-file]` — generate lesson plan using `lesson_plan_generator` skill
- `/pptx_maker [input-file]` — generate a PowerPoint from any doc (Markdown, CSV, JSON, etc.)

## Document Status

Generated docs in `docs/` and their current state:

| # | Document | File | Status |
|:--|:---------|:-----|:-------|
| 1 | Syllabus | `docs/lfr-syllabus.md` | Done |
| 2 | Lesson Plan | `docs/lfr-lesson-plan.md` | Done |
| 3 | Specification | `docs/lfr-specification.md` | Done |
| 4 | Development Plan | `docs/lfr-development-plan.md` | Done |
| 5 | Wiring Plan | `docs/lfr-wiring-plan.md` | Done |

## Workflow for Generating Course Documents

Follow the sequence in `input/my-claude-prompts.md`. Each step builds on prior docs — run them in order, each in a fresh `/clear` session:

1. Syllabus → `docs/lfr-syllabus.md` (from `input/*.md` only)
2. Lesson plan → `docs/lfr-lesson-plan.md` (from `input/*.md` + `docs/*.md`)
3. Specification → `docs/lfr-specification.md` (from `input/*.md` + `docs/*.md`)
4. Development plan → `docs/lfr-development-plan.md` (from `input/*.md` + `docs/*.md`)

Always start a new document generation session with:

```bash
/clear
/init
/model opus
/mode plan
/effort high
```

## Key Definitions

See `.claude/skills/shared/definitions.md` for authoritative definitions of:
- **Design Session** — one or more classes covering a major functional milestone
- **Class** — 2-hour in-person session at Makersmiths
- **Syllabus / Lesson Plan / BOM** — distinct documents that must stay consistent with each other

## Hardware Platform

- **MCU:** Raspberry Pi Pico W running CircuitPython
- **Motor driver:** Robotics Motor Driver Board for Pico
- **Line sensors:** IR Emitter/Phototransistor Pair (DS3–DS5) → QTRX-MD-08RC Reflectance Sensor Array (DS6+)
- **Speed sensing:** Speed Sensor Module (2×, one per wheel, added at DS9)
- **6 LFRs** total (5 students + 1 instructor demo unit)

## Line Track Designer (`src/track_designer/`)

CLI tool that generates printable PDF tile sheets for LFR floor tracks. **M1 complete.**

```bash
cd src/track_designer
python track_designer.py tiles                                          # list tile types
python track_designer.py validate tracks/simple_oval.json              # validate JSON
python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf --preview
python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf --line-width 25
../../.venv/bin/pytest tests/ -v                                        # run all tests
../../.venv/bin/pytest tests/ -v -k test_pdf_generates                  # run single test
```

Key files: `track_designer.py` (CLI), `tile_registry.py` (12 tile draw functions), `pdf_generator.py` (reportlab), `validator.py` + `schema.py` (jsonschema validation). Track JSONs in `tracks/`, generated PDFs in `output/`.

All 6 course tracks: `simple_oval`, `oval_tight`, `figure_eight`, `figure_eight_chicane`, `complex_course`, `competition_course`.

**Track JSON format** — a 2D grid of tile-type strings, max 4×3 tiles (each tile = one 8.5×11" page):

```json
{ "name": "Simple Oval", "description": "...", "grid_columns": 4, "grid_rows": 3,
  "line_width_mm": 19,
  "tiles": [["curve_ne","straight_h","straight_h","curve_nw"],
            ["straight_v","blank","blank","straight_v"],
            ["curve_se","straight_h","straight_h","curve_sw"]] }
```

Valid tile types: `blank`, `straight_h`, `straight_v`, `curve_ne/nw/se/sw`, `cross`, `chicane_lr`, `chicane_rl`, `start_h`, `sharp_90_ne`.

## Software to Be Built (pre-course)

| System | Status | Location |
|:-------|:-------|:---------|
| **Line Track Designer** | **M1 complete** | `src/track_designer/` |
| **LFR Firmware** (CircuitPython) — modular, each DS swaps a subsystem | **M2 + M3 Ph3.1 desktop complete** (hardware gates pending) | `src/firmware/` |
| **LFR Simulator** — Python + Pygame, 2D visual sim for instructor demos | Not started | `src/simulator/` (planned) |

## LFR Firmware (`src/firmware/`)

CircuitPython firmware for the Pico W. **M2 + M3 Phase 3.1 desktop complete** — all 57 desktop tests pass; hardware gates pending physical hardware session.

```bash
# Desktop tests (all phases)
.venv/bin/pytest src/firmware/tests/ -v

# Single phase — naming: test_phase{M}{P}.py (M=milestone, P=phase)
.venv/bin/pytest src/firmware/tests/test_phase21.py -v   # M2 Phase 2.1
.venv/bin/pytest src/firmware/tests/test_phase31.py -v   # M3 Phase 3.1

# Hardware tests — copy main.py to CIRCUITPY/main.py, monitor via Mu Editor serial console
# Motor/I2C verification: src/firmware/test_m02.py
```

Key files: `config.py` (DS3 factory functions), `main.py` (cooperative polling loop), `sensors/ir_pair.py`, `sensors/qtrx_array.py` (8-ch RC timing, GP0–GP7), `controllers/bang_bang.py`, `motors/kitronik.py` (direct PCA9685 register writes).
Tests in `tests/` stub CircuitPython modules (`busio`, `digitalio`, `board`, `analogio`, `microcontroller`) via `sys.modules` mocking in `conftest.py`. The `time` module is **not** stubbed — Python stdlib is used. At M5, `countio` will also need stubbing.

### Firmware Plugin Architecture

Each Design Session swaps one subsystem. To add a module for a new DS:

1. Create `sensors/foo.py`, `controllers/foo.py`, or `motors/foo.py` implementing the base class in the corresponding `base.py`
2. Update `config.py`: change the constant (`SENSOR`, `CONTROLLER`, etc.) and add/update the factory function
3. `main.py` never changes — it calls `config.get_sensor()`, `config.get_controller()`, `config.get_motor_driver()`, `config.get_web_server()`

**Base class contracts** (all values normalized -1.0 to +1.0):
- `LineSensor.read_position()` → float (-1.0 = line far left, 0.0 = centered, +1.0 = line far right)
- `Controller.update(position, dt)` → `(left_speed, right_speed)` floats
- `Controller.get_params()` / `set_params(dict)` / `param_definitions` — browser UI hooks for runtime tuning
- `MotorDriver.set_speeds(left, right)` → None

**Desktop test pattern for hardware sensors:** Extract all GPIO/timing I/O into a single internal method (e.g., `_read_raw_timings()`) and patch that method in tests with synthetic data. Never patch individual pin objects. See `sensors/qtrx_array.py` + `tests/test_phase31.py` as the reference implementation.

### CIRCUITPY Deployment

To deploy firmware to a Pico W, copy the entire firmware source tree to the CIRCUITPY drive:

```bash
# Full deployment (all files needed on the Pico)
cp src/firmware/main.py   /media/$USER/CIRCUITPY/main.py
cp src/firmware/config.py /media/$USER/CIRCUITPY/config.py
cp -r src/firmware/sensors      /media/$USER/CIRCUITPY/
cp -r src/firmware/controllers  /media/$USER/CIRCUITPY/
cp -r src/firmware/motors       /media/$USER/CIRCUITPY/
```

For hardware test only: copy `src/firmware/test_m02.py` → `CIRCUITPY/main.py` (no other files needed).

## Markdown Linting

The project uses `markdownlint-cli2` (configured in `.markdownlint-cli2.jsonc`). Config has `"fix": true`, so running it auto-fixes fixable issues in place. Key disabled rules: MD012 (multiple blanks), MD022 (blanks around headings), MD024 (duplicate headings), MD032 (blanks around lists), MD033 (inline HTML), MD041 (first-line heading), MD045 (alt text). Line length limit is 300.

```bash
markdownlint-cli2 docs/*.md lecture_notes/*.md
```

Do not run markdownlint on `input/` — those files are instructor-owned and not linted.

## File Naming Conventions

- Course docs: `docs/lfr-{type}.md` (e.g., `lfr-syllabus.md`, `lfr-lesson-plan.md`, `lfr-specification.md`, `lfr-development-plan.md`)
- Lecture notes: `lecture_notes/{doctype}-{topic}.md` (e.g., `theory-of-operation-mioyoow-line-follower.md`)
- `.bak` files are gitignored — safe to create per backup convention

## input/ Directory Convention

Files in `input/` are the instructor's source-of-truth specifications. Do not overwrite them without explicit instruction. Generated outputs go in `docs/` or `lecture_notes/`.
