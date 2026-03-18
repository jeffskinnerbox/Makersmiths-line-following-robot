#!/usr/bin/env python3
"""Line Track Designer CLI.

Usage:
    python track_designer.py tiles
    python track_designer.py validate tracks/simple_oval.json
    python track_designer.py generate tracks/simple_oval.json -o output/simple_oval.pdf [--preview] [--line-width MM]
"""

import argparse
import sys
from pathlib import Path

from pdf_generator import generate_pdf
from tile_registry import TILE_REGISTRY
from validator import load_track, validate_file


def cmd_tiles(_args: argparse.Namespace) -> int:
    print(f"{'Tile Type':<20}  Description")
    print("-" * 60)
    for name, (desc, _) in TILE_REGISTRY.items():
        print(f"{name:<20}  {desc}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_file(args.json)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"OK: {args.json} is valid")
    return 0


def cmd_generate(args: argparse.Namespace) -> int:
    errors = validate_file(args.json)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    track = load_track(args.json)
    lw = args.line_width if args.line_width else None
    pages = generate_pdf(track, args.output, preview=args.preview, line_width_mm=lw)

    preview_note = " (+ 1 preview page)" if args.preview else ""
    print(f"Generated {args.output}: {pages} tile page(s){preview_note}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="track_designer.py",
        description="Line Track Designer — generate printable LFR test tracks",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # tiles
    sub.add_parser("tiles", help="List all available tile types")

    # validate
    v = sub.add_parser("validate", help="Validate a track JSON file")
    v.add_argument("json", help="Path to track JSON file")

    # generate
    g = sub.add_parser("generate", help="Generate a PDF from a track JSON file")
    g.add_argument("json", help="Path to track JSON file")
    g.add_argument("-o", "--output", required=True, help="Output PDF path")
    g.add_argument("--preview", action="store_true", help="Include full-grid overview as page 1")
    g.add_argument("--line-width", type=float, metavar="MM", help="Override line width in mm")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    handlers = {"tiles": cmd_tiles, "validate": cmd_validate, "generate": cmd_generate}
    sys.exit(handlers[args.command](args))


if __name__ == "__main__":
    main()
