"""pytest suite for Phase 1.1 test-gates."""

import json
import sys
from pathlib import Path

import pytest

# Allow importing from parent package directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from schema import VALID_TILE_TYPES
from tile_registry import TILE_REGISTRY
from validator import validate_file, validate_track
from pdf_generator import generate_pdf


TRACKS_DIR = Path(__file__).parent.parent / "tracks"
SIMPLE_OVAL = TRACKS_DIR / "simple_oval.json"

# ---------------------------------------------------------------------------
# Tile registry
# ---------------------------------------------------------------------------

def test_tile_registry_count():
    assert len(TILE_REGISTRY) == 12

def test_tile_registry_matches_valid_set():
    assert set(TILE_REGISTRY.keys()) == VALID_TILE_TYPES

def test_all_tile_draw_functions_callable():
    for name, (desc, fn) in TILE_REGISTRY.items():
        assert callable(fn), f"draw function for '{name}' is not callable"

# ---------------------------------------------------------------------------
# JSON parsing & schema validation
# ---------------------------------------------------------------------------

def test_simple_oval_is_valid():
    errors = validate_file(SIMPLE_OVAL)
    assert errors == [], f"Validation errors: {errors}"

def test_missing_required_field():
    bad = {
        "name": "Bad Track",
        "grid_columns": 2,
        "grid_rows": 1,
        "tiles": [["straight_h", "straight_h"]],
        # missing "description"
    }
    errors = validate_track(bad)
    assert any("description" in e for e in errors)

def test_grid_too_large_columns():
    bad = {
        "name": "x", "description": "x",
        "grid_columns": 5, "grid_rows": 1,
        "tiles": [["straight_h"] * 5],
    }
    errors = validate_track(bad)
    assert errors  # schema rejects columns > 4

def test_grid_too_large_rows():
    bad = {
        "name": "x", "description": "x",
        "grid_columns": 1, "grid_rows": 4,
        "tiles": [["straight_h"]] * 4,
    }
    errors = validate_track(bad)
    assert errors  # schema rejects rows > 3

def test_unknown_tile_type():
    bad = {
        "name": "x", "description": "x",
        "grid_columns": 1, "grid_rows": 1,
        "tiles": [["banana"]],
    }
    errors = validate_track(bad)
    assert any("banana" in e for e in errors)

def test_row_column_mismatch():
    bad = {
        "name": "x", "description": "x",
        "grid_columns": 2, "grid_rows": 1,
        "tiles": [["straight_h"]],  # only 1 col, expected 2
    }
    errors = validate_track(bad)
    assert any("column" in e for e in errors)

def test_tile_row_count_mismatch():
    bad = {
        "name": "x", "description": "x",
        "grid_columns": 1, "grid_rows": 2,
        "tiles": [["straight_h"]],  # only 1 row, expected 2
    }
    errors = validate_track(bad)
    assert any("row" in e for e in errors)

def test_invalid_json_file(tmp_path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("not valid json {{{")
    errors = validate_file(bad_file)
    assert any("JSON" in e for e in errors)

def test_missing_file():
    errors = validate_file("/nonexistent/path/track.json")
    assert any("File error" in e or "error" in e.lower() for e in errors)

# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def test_pdf_generates(tmp_path):
    import json
    track = json.loads(SIMPLE_OVAL.read_text())
    out = tmp_path / "simple_oval.pdf"
    pages = generate_pdf(track, out)
    assert out.exists()
    assert out.stat().st_size > 1000  # non-trivial PDF

def test_pdf_page_count(tmp_path):
    import json
    track = json.loads(SIMPLE_OVAL.read_text())
    out = tmp_path / "simple_oval.pdf"
    pages = generate_pdf(track, out)
    # simple_oval: 4 corners + 4 straights (top/bottom) + 2 straight_v (sides) = 10
    assert pages == 10

def test_pdf_page_count_with_preview(tmp_path):
    import json
    track = json.loads(SIMPLE_OVAL.read_text())
    out = tmp_path / "preview.pdf"
    pages = generate_pdf(track, out, preview=True)
    assert pages == 10  # return value excludes preview page

def test_pdf_output_dir_created(tmp_path):
    import json
    track = json.loads(SIMPLE_OVAL.read_text())
    out = tmp_path / "subdir" / "nested" / "out.pdf"
    generate_pdf(track, out)
    assert out.exists()

def test_line_width_override(tmp_path):
    import json
    track = json.loads(SIMPLE_OVAL.read_text())
    out = tmp_path / "wide.pdf"
    pages = generate_pdf(track, out, line_width_mm=30)
    assert out.exists()
    assert pages == 10
