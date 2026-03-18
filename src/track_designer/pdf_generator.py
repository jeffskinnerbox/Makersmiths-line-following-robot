"""PDF generation for track tile sheets using reportlab."""

from pathlib import Path

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.units import inch, mm
from reportlab.pdfgen.canvas import Canvas

from tile_registry import TILE_REGISTRY

PAGE_W, PAGE_H = landscape(letter)   # 792 x 612 pts (11 x 8.5 in)
MARGIN = 0.25 * inch                  # small margin so registration marks are visible

DEFAULT_LINE_WIDTH_MM = 19


def _label(c: Canvas, text: str, x: float, y: float) -> None:
    c.saveState()
    c.setFont("Helvetica", 8)
    c.drawString(x, y, text)
    c.restoreState()


def _registration_marks(
    c: Canvas, x: float, y: float, w: float, h: float, label: str
) -> None:
    """Draw corner crosshair marks and a grid-position label."""
    arm = 8  # pts
    c.saveState()
    c.setStrokeColorRGB(0.4, 0.4, 0.4)
    c.setLineWidth(0.5)
    for cx, cy in [(x, y), (x + w, y), (x, y + h), (x + w, y + h)]:
        c.line(cx - arm, cy, cx + arm, cy)
        c.line(cx, cy - arm, cx, cy + arm)
    # Grid position label (bottom-left corner, above margin)
    _label(c, label, x + 4, y + 4)
    c.restoreState()


def generate_pdf(
    track: dict,
    output_path: str | Path,
    preview: bool = False,
    line_width_mm: float | None = None,
) -> int:
    """Generate a tile-sheet PDF for the given track definition.

    Returns the number of tile pages written (excludes the optional preview page).
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lw_mm = line_width_mm or track.get("line_width_mm", DEFAULT_LINE_WIDTH_MM)
    lw_pts = lw_mm * mm

    tiles = track["tiles"]
    rows = track["grid_rows"]
    cols = track["grid_columns"]
    name = track.get("name", "Track")

    c = Canvas(str(output_path), pagesize=landscape(letter))

    # ------------------------------------------------------------------
    # Optional preview page (full grid on one page, scaled to fit)
    # ------------------------------------------------------------------
    if preview:
        _render_preview(c, tiles, rows, cols, name, lw_pts)
        c.showPage()

    # ------------------------------------------------------------------
    # One tile per page, reading order (left-to-right, top-to-bottom)
    # ------------------------------------------------------------------
    tile_pages = 0
    tile_w = PAGE_W - 2 * MARGIN
    tile_h = PAGE_H - 2 * MARGIN

    for r in range(rows):
        for col in range(cols):
            tile_type = tiles[r][col]
            if tile_type == "blank":
                continue  # skip blank tiles
            draw_fn = TILE_REGISTRY[tile_type][1]
            x, y = MARGIN, MARGIN
            draw_fn(c, x, y, tile_w, tile_h, lw_pts)
            label = f"{name} — R{r + 1}C{col + 1} [{tile_type}]"
            _registration_marks(c, x, y, tile_w, tile_h, label)
            c.showPage()
            tile_pages += 1

    c.save()
    return tile_pages


def _render_preview(
    c: Canvas,
    tiles: list[list[str]],
    rows: int,
    cols: int,
    name: str,
    lw_pts: float,
) -> None:
    """Render all tiles scaled to fit the full grid on one page."""
    avail_w = PAGE_W - 2 * MARGIN
    avail_h = PAGE_H - 2 * MARGIN - 24  # leave room for title

    cell_w = avail_w / cols
    cell_h = avail_h / rows

    # Scale line width proportionally (full tile is ~792 pts wide; preview cell is smaller)
    scale = min(cell_w / (PAGE_W - 2 * MARGIN), cell_h / (PAGE_H - 2 * MARGIN))
    preview_lw = max(lw_pts * scale, 0.5)

    # Title
    _label(c, f"PREVIEW: {name}", MARGIN, PAGE_H - MARGIN - 16)

    for r in range(rows):
        for col in range(cols):
            tile_type = tiles[r][col]
            # Preview origin: rows drawn top-to-bottom
            px = MARGIN + col * cell_w
            py = MARGIN + (rows - 1 - r) * cell_h
            draw_fn = TILE_REGISTRY[tile_type][1]
            draw_fn(c, px, py, cell_w, cell_h, preview_lw)
            _label(c, f"R{r + 1}C{col + 1}", px + 2, py + 2)
