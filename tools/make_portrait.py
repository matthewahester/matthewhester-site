#!/usr/bin/env python3
"""Write the homepage portrait with a pure white ground.

The portrait is a painted figure on paper with loose watercolor edges. The
homepage sets it straight on the page, with no card or frame around it, so
the paper in the picture has to be the same white as the page. In the
source art it is not: the ground is 250 to 255 per channel, mostly 252 and
253. On a white page that prints the picture's rectangle as a faint grey
box around the figure. (It did not show while the picture sat in a white
card on a tinted page.)

This script resizes the source to 800 px wide and then moves the white
point down to 250: every channel is scaled by 255/250 and clipped. The
ground becomes 255 everywhere and the rest of the picture is 2 percent
brighter, which is not visible. Nothing is cut out and no alpha is made, so
the soft painted edge still fades into the paper as painted.

It writes the two files the site already uses, with the same sizes and
quality settings as ``tools/process_images.py --target brand``:

    assets/images/brand/portrait-matt-hester-800.webp
    assets/images/brand/portrait-matt-hester-800.jpg

Run from the repo root. The source is staged in ``assets/images/raw/``,
which is not committed (see IMAGE_ASSET_PLAN.md):

    python tools/make_portrait.py assets/images/raw/Hester_profile_art_2026.png

Deterministic and idempotent. Saves carry no EXIF. Pillow is the only
dependency.
"""
import os
import sys

from PIL import Image, ImageOps

WIDTH = 800
WHITE_POINT = 250        # source ground is 250-255; this and above become 255
JPEG_QUALITY = 85        # as tools/process_images.py
WEBP_QUALITY = 82

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_STEM = os.path.join(ROOT, "assets", "images", "brand", "portrait-matt-hester-800")


def ground_report(img, edge=12):
    """Lowest channel value in a border strip: 255 means a clean ground."""
    w, h = img.size
    strips = [img.crop((0, 0, w, edge)), img.crop((0, h - edge, w, h)),
              img.crop((0, 0, edge, h)), img.crop((w - edge, 0, w, h))]
    return min(min(lo for lo, _ in s.getextrema()) for s in strips)


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: make_portrait.py SOURCE.png")
    src = ImageOps.exif_transpose(Image.open(argv[1])).convert("RGB")
    if src.width > WIDTH:  # never upscale
        src = src.resize((WIDTH, max(1, round(src.height * WIDTH / src.width))), Image.LANCZOS)
    before = ground_report(src)
    table = [min(255, round(v * 255 / WHITE_POINT)) for v in range(256)]
    out = src.point(table * 3)
    clean = Image.new("RGB", out.size)   # a fresh image carries no metadata
    clean.paste(out)
    clean.save(OUT_STEM + ".webp", "WEBP", quality=WEBP_QUALITY, method=6, exif=b"")
    clean.save(OUT_STEM + ".jpg", "JPEG", quality=JPEG_QUALITY, optimize=True,
               progressive=True, exif=b"")
    for ext in (".webp", ".jpg"):
        path = OUT_STEM + ext
        saved = Image.open(path).convert("RGB")
        print("%s  %dx%d  %5.0f KB  lowest border value %d (source after resize: %d)" % (
            os.path.relpath(path, ROOT).replace(os.sep, "/"), saved.width, saved.height,
            os.path.getsize(path) / 1024, ground_report(saved), before))


if __name__ == "__main__":
    main(sys.argv)
