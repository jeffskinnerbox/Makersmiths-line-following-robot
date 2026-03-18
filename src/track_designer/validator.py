"""Track definition validation: schema + tile type + grid dimension checks."""

import json
from pathlib import Path

import jsonschema

from schema import TRACK_SCHEMA, VALID_TILE_TYPES


def load_track(json_path: str | Path) -> dict:
    with open(json_path) as f:
        return json.load(f)


def validate_track(data: dict) -> list[str]:
    """Validate track data. Returns list of error strings (empty = valid)."""
    errors = []

    # Schema validation
    try:
        jsonschema.validate(data, TRACK_SCHEMA)
    except jsonschema.ValidationError as e:
        errors.append(f"Schema error: {e.message}")
        return errors  # Can't safely continue if schema is broken

    cols = data["grid_columns"]
    rows = data["grid_rows"]
    tiles = data["tiles"]

    # Row count
    if len(tiles) != rows:
        errors.append(f"tiles has {len(tiles)} rows, expected {rows}")

    # Column count + tile type check
    for r, row in enumerate(tiles):
        if len(row) != cols:
            errors.append(f"Row {r} has {len(row)} columns, expected {cols}")
        for c, tile in enumerate(row):
            if tile not in VALID_TILE_TYPES:
                errors.append(f"Unknown tile type '{tile}' at row {r}, col {c}")

    return errors


def validate_file(json_path: str | Path) -> list[str]:
    """Load and validate a track JSON file."""
    try:
        data = load_track(json_path)
    except json.JSONDecodeError as e:
        return [f"JSON parse error: {e}"]
    except OSError as e:
        return [f"File error: {e}"]
    return validate_track(data)
