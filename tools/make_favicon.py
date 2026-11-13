#!/usr/bin/env python3
"""Write the site favicon: the initials MH, light on the navbar's black.

The site had no favicon until 2026-11-13, so every browser tab showed the
browser's default icon. This draws a plain monogram in the two colors of
the navbar: obsidian (#1c1b19) ground, quartz (#f6f5f3) letters.

The letters are drawn as rectangles and parallelograms, not set in a font.
That keeps the mark square-edged at 16 px, makes the output identical on
any machine, and bakes no typeface into a committed image.

It writes one file, which ``_quarto.yml`` names as ``website.favicon``:

    assets/images/brand/favicon.png     96 x 96

96 px covers a 16 px tab icon up to 6x pixel density and a 32 px shortcut
icon at 3x. Drawn at ten times that size and reduced, so the diagonals of
the M are smooth. Run from the repo root:

    python tools/make_favicon.py

Deterministic and idempotent. Pillow is the only dependency.
"""
import os

from PIL import Image, ImageDraw

SIZE = 96
SCALE = 10                    # draw at 960 px, reduce to 96
GROUND = (28, 27, 25)         # --stone-900, the navbar
INK = (246, 245, 243)         # --stone-50, the navbar's text

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "images", "brand", "favicon.png")

# Geometry on the 960 px drawing, in px. Both letters share one cap height
# and one stroke. Together they are 660 wide, centered with 150 either side.
TOP, BOTTOM = 250, 710
STROKE = 84
M_LEFT, M_RIGHT = 150, 492
H_LEFT, H_RIGHT = 552, 810
M_APEX = 600                  # how far down the M's inner V comes


def draw_monogram():
    big = SIZE * SCALE
    img = Image.new("RGB", (big, big), GROUND)
    d = ImageDraw.Draw(img)

    # M: two stems and a V between them.
    d.rectangle([M_LEFT, TOP, M_LEFT + STROKE, BOTTOM], fill=INK)
    d.rectangle([M_RIGHT - STROKE, TOP, M_RIGHT, BOTTOM], fill=INK)
    mid = (M_LEFT + M_RIGHT) / 2
    half = STROKE * 0.56
    d.polygon([(M_LEFT, TOP), (M_LEFT + STROKE * 1.12, TOP),
               (mid + half, M_APEX), (mid - half, M_APEX)], fill=INK)
    d.polygon([(M_RIGHT, TOP), (M_RIGHT - STROKE * 1.12, TOP),
               (mid - half, M_APEX), (mid + half, M_APEX)], fill=INK)

    # H: two stems and a bar.
    d.rectangle([H_LEFT, TOP, H_LEFT + STROKE, BOTTOM], fill=INK)
    d.rectangle([H_RIGHT - STROKE, TOP, H_RIGHT, BOTTOM], fill=INK)
    bar_mid = (TOP + BOTTOM) / 2
    d.rectangle([H_LEFT, bar_mid - STROKE / 2, H_RIGHT, bar_mid + STROKE / 2], fill=INK)
    return img


def main():
    icon = draw_monogram().resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(OUT, "PNG", optimize=True)
    print("%s  %dx%d  %.1f KB" % (os.path.relpath(OUT, ROOT).replace(os.sep, "/"),
                                   SIZE, SIZE, os.path.getsize(OUT) / 1024))


if __name__ == "__main__":
    main()
