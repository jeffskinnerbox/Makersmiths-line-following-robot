"""Tile type registry: maps tile type strings to reportlab drawing functions.

Each drawing function signature:
    draw_tile(canvas, x, y, w, h, line_width_pts)

Where (x, y) is the bottom-left corner of the tile in points,
w/h are tile width/height in points, and line_width_pts is the
track line width in points.

Coordinate system: reportlab uses bottom-left origin.
Edge centers (the connection points every path tile must use):
    left   = (x,       y + h/2)
    right  = (x + w,   y + h/2)
    bottom = (x + w/2, y)
    top    = (x + w/2, y + h)

All curves use cubic Bezier so that connection points are exact
regardless of tile aspect ratio (fixes arc overshoot on non-square tiles).
KAPPA ≈ 0.5523 is the standard control-point offset for a quarter-ellipse.
"""

from reportlab.lib.colors import black, Color
from reportlab.pdfgen.canvas import Canvas

KAPPA = 0.5523  # Bezier approximation for quarter-circle/ellipse
BORDER_COLOR = Color(0.7, 0.7, 0.7)
BORDER_DASH = [6, 4]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _set_line(c: Canvas, lw: float) -> None:
    c.setStrokeColor(black)
    c.setLineWidth(lw)


def _draw_border(c: Canvas, x: float, y: float, w: float, h: float) -> None:
    c.saveState()
    c.setStrokeColor(BORDER_COLOR)
    c.setLineWidth(0.5)
    c.setDash(BORDER_DASH)
    c.rect(x, y, w, h, fill=0, stroke=1)
    c.restoreState()


def _bezier_curve(c: Canvas, x0, y0, x1, y1, x2, y2, x3, y3, lw: float) -> None:
    """Draw a single cubic Bezier segment."""
    _set_line(c, lw)
    p = c.beginPath()
    p.moveTo(x0, y0)
    p.curveTo(x1, y1, x2, y2, x3, y3)
    c.drawPath(p, stroke=1, fill=0)


# ---------------------------------------------------------------------------
# Tile drawing functions
# ---------------------------------------------------------------------------

def draw_blank(c, x, y, w, h, lw):
    _draw_border(c, x, y, w, h)


def draw_straight_h(c, x, y, w, h, lw):
    _draw_border(c, x, y, w, h)
    _set_line(c, lw)
    my = y + h / 2
    c.line(x, my, x + w, my)


def draw_straight_v(c, x, y, w, h, lw):
    _draw_border(c, x, y, w, h)
    _set_line(c, lw)
    mx = x + w / 2
    c.line(mx, y, mx, y + h)


def draw_curve_ne(c, x, y, w, h, lw):
    """Bottom-center → right-center  (NW oval corner: arc bulges upper-left / outward)."""
    _draw_border(c, x, y, w, h)
    hw, hh = w / 2, h / 2
    # P0 bottom-center, tangent upward (+y); P3 right-center, tangent rightward (+x)
    _bezier_curve(
        c,
        x + hw,         y,              # P0
        x + hw,         y + hh*KAPPA,  # CP1: above P0
        x + w - hw*KAPPA, y + hh,      # CP2: left of P3
        x + w,          y + hh,        # P3
        lw,
    )


def draw_curve_nw(c, x, y, w, h, lw):
    """Bottom-center → left-center  (NE oval corner: arc bulges upper-right / outward)."""
    _draw_border(c, x, y, w, h)
    hw, hh = w / 2, h / 2
    # P0 bottom-center, tangent upward (+y); P3 left-center, tangent leftward (-x)
    _bezier_curve(
        c,
        x + hw,      y,             # P0
        x + hw,      y + hh*KAPPA, # CP1: above P0
        x + hw*KAPPA, y + hh,      # CP2: right of P3
        x,           y + hh,       # P3
        lw,
    )


def draw_curve_se(c, x, y, w, h, lw):
    """Top-center → right-center  (SW oval corner: arc bulges lower-left / outward)."""
    _draw_border(c, x, y, w, h)
    hw, hh = w / 2, h / 2
    # P0 top-center, tangent downward (-y); P3 right-center, tangent rightward (+x)
    _bezier_curve(
        c,
        x + hw,           y + h,              # P0
        x + hw,           y + h - hh*KAPPA,  # CP1: below P0
        x + w - hw*KAPPA, y + hh,            # CP2: left of P3
        x + w,            y + hh,            # P3
        lw,
    )


def draw_curve_sw(c, x, y, w, h, lw):
    """Top-center → left-center  (SE oval corner: arc bulges lower-right / outward)."""
    _draw_border(c, x, y, w, h)
    hw, hh = w / 2, h / 2
    # P0 top-center, tangent downward (-y); P3 left-center, tangent leftward (-x)
    _bezier_curve(
        c,
        x + hw,       y + h,             # P0
        x + hw,       y + h - hh*KAPPA, # CP1: below P0
        x + hw*KAPPA, y + hh,           # CP2: right of P3
        x,            y + hh,           # P3
        lw,
    )


def draw_cross(c, x, y, w, h, lw):
    _draw_border(c, x, y, w, h)
    _set_line(c, lw)
    mx, my = x + w / 2, y + h / 2
    c.line(x, my, x + w, my)
    c.line(mx, y, mx, y + h)


def draw_chicane_lr(c, x, y, w, h, lw):
    """S-curve: left-center → right-center, looping up then down.
    Connects (x, y+h/2) to (x+w, y+h/2) with horizontal tangents at both ends."""
    _draw_border(c, x, y, w, h)
    _bezier_curve(
        c,
        x,         y + h/2,    # P0: left midpoint
        x + w/3,   y + 3*h/4,  # CP1: pull upward in left half
        x + 2*w/3, y + h/4,    # CP2: pull downward in right half
        x + w,     y + h/2,    # P3: right midpoint
        lw,
    )


def draw_chicane_rl(c, x, y, w, h, lw):
    """S-curve: left-center → right-center, looping down then up.
    Connects (x, y+h/2) to (x+w, y+h/2) with horizontal tangents at both ends."""
    _draw_border(c, x, y, w, h)
    _bezier_curve(
        c,
        x,         y + h/2,    # P0: left midpoint
        x + w/3,   y + h/4,    # CP1: pull downward in left half
        x + 2*w/3, y + 3*h/4,  # CP2: pull upward in right half
        x + w,     y + h/2,    # P3: right midpoint
        lw,
    )


def draw_start_h(c, x, y, w, h, lw):
    """Horizontal straight with perpendicular start/finish marker."""
    _draw_border(c, x, y, w, h)
    _set_line(c, lw)
    my = y + h / 2
    c.line(x, my, x + w, my)
    mx = x + w / 2
    c.saveState()
    c.setLineWidth(lw * 0.4)
    c.line(mx, y + h * 0.1, mx, y + h * 0.9)
    c.restoreState()


def draw_sharp_90_ne(c, x, y, w, h, lw):
    """Sharp 90° right-angle turn: bottom-center to right-center (no arc)."""
    _draw_border(c, x, y, w, h)
    _set_line(c, lw)
    mx, my = x + w / 2, y + h / 2
    c.line(mx, y, mx, my)
    c.line(mx, my, x + w, my)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

TILE_REGISTRY: dict[str, tuple[str, object]] = {
    "blank":         ("Empty tile, no line",             draw_blank),
    "straight_h":    ("Horizontal straight",             draw_straight_h),
    "straight_v":    ("Vertical straight",               draw_straight_v),
    "curve_ne":      ("NE curve: bottom-center → right-center", draw_curve_ne),
    "curve_nw":      ("NW curve: bottom-center → left-center",  draw_curve_nw),
    "curve_se":      ("SE curve: top-center → right-center",    draw_curve_se),
    "curve_sw":      ("SW curve: top-center → left-center",     draw_curve_sw),
    "cross":         ("Crossover intersection",          draw_cross),
    "chicane_lr":    ("S-curve: left-center to right-center, up then down", draw_chicane_lr),
    "chicane_rl":    ("S-curve: left-center to right-center, down then up", draw_chicane_rl),
    "start_h":       ("Horizontal start/finish line",    draw_start_h),
    "sharp_90_ne":   ("Sharp 90° NE turn (no arc)",      draw_sharp_90_ne),
}
