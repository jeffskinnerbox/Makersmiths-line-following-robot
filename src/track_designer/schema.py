"""JSON schema for track definition files."""

TRACK_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "grid_columns", "grid_rows", "tiles"],
    "additionalProperties": False,
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "description": {"type": "string"},
        "grid_columns": {"type": "integer", "minimum": 1, "maximum": 4},
        "grid_rows": {"type": "integer", "minimum": 1, "maximum": 3},
        "line_width_mm": {"type": "number", "minimum": 5, "maximum": 50},
        "tiles": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
    },
}

VALID_TILE_TYPES = {
    "blank",
    "straight_h",
    "straight_v",
    "curve_ne",
    "curve_nw",
    "curve_se",
    "curve_sw",
    "cross",
    "chicane_lr",
    "chicane_rl",
    "start_h",
    "sharp_90_ne",
}
