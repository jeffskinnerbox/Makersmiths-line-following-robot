# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repo is a course-preparation workspace for a **Line Following Robot (LFR)** makerspace course at [Makersmiths](https://makersmiths.org/). The course runs 8 weeks (2 hrs/session), targeting students ages 12–18, starting June 15 2026. The course is not yet taught — all materials must be created before it starts.

The LFR evolves across ~12 Design Sessions: analog kit → Raspberry Pi Pico W + CircuitPython → IR sensor array → PID controller → Kalman filter → Q-Learning controller.

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

## Software to Be Built (pre-course)

| System | Status | Location |
|:-------|:-------|:---------|
| **Line Track Designer** | **M1 complete** | `src/track_designer/` |
| **LFR Firmware** (CircuitPython) — modular, each DS swaps a subsystem | **M2 desktop complete** (hardware gates pending) | `src/firmware/` |
| **LFR Simulator** — Python + Pygame, 2D visual sim for instructor demos | Not started | `src/simulator/` (planned) |

## LFR Firmware (`src/firmware/`)

CircuitPython firmware for the Pico W. **M2 desktop phases complete** — all 13 desktop test-gates pass; hardware gates (motor spin, IR reads, oval lap) pending physical hardware session.

```bash
# Desktop tests (all phases)
.venv/bin/pytest src/firmware/tests/ -v

# Single phase
.venv/bin/pytest src/firmware/tests/test_phase21.py -v

# Hardware tests — copy main.py to CIRCUITPY/main.py, monitor via Mu Editor serial console
# Motor/I2C verification: src/firmware/test_m02.py
```

Key files: `config.py` (DS3 factory functions), `main.py` (cooperative polling loop), `sensors/ir_pair.py`, `controllers/bang_bang.py`, `motors/kitronik.py` (direct PCA9685 register writes).
Tests in `tests/` stub CircuitPython modules (`busio`, `digitalio`, `board`, etc.) via `sys.modules` mocking in `conftest.py`.

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
