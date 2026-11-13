#!/usr/bin/env python3
"""Write the course marks the Course Library shows beside each record.

A course mark is the single object cut out of a course's poster: a
1254x1254 RGBA PNG on transparency (see tools/make_course_icon.py). Each
course site shows its mark in the navbar. The Library shows the same mark
at the left of the course's row, in a slot 80 px wide on a wide screen and
56 px on a phone (``.course-record-has-thumb`` in styles.css).

Before 2026-11-13 a Library row carried a 224 px thumbnail of the whole
poster. At that size, and at 108 px on a phone, the poster's lettering and
side panels could not be read, so the row showed a small busy picture. The
mark is one clear object and needs no frame.

WHY THE MARKS ARE REDRAWN FOR THE LIBRARY AND NOT ONLY SHRUNK

The masters were made one at a time, so the object sits differently in
each. It covers from 57% to 92% of the canvas width, and its centre lies up
to 14% of the canvas below the middle. Shrunk as they are and stacked in a
column, the marks came out at different sizes and on different centres. A
browser reducing a larger file to 80 px also drew them soft. So this script
does three things to every master.

1. FINDS THE OBJECT. The master is laid on white, as the Library shows it.
   The object is every pixel visibly different from white, and its bounding
   box is measured. (Laying it on white matters for the five graduate marks,
   whose cut-outs include pale paper.)

2. GIVES EVERY OBJECT THE SAME OPTICAL SIZE ON THE SAME CENTRE.
   - The bounding box gets the same area in every mark: BOX_SIDE squared, in
     slot pixels. A tall crystal and a round rock then carry about the same
     mass, which fitting both to the same height or width does not do.
   - A dense, dark object is drawn a little smaller and an open, pale one a
     little larger (0.92 to 1.08 across the present 15), because at equal
     box area the dense one looks bigger. The two exponents were set by eye
     on those 15 marks on 2026-11-13; they are not derived from anything.
   - Neither side of the box may pass MAX_SIDE, which leaves one clear pixel
     inside the slot's edge.
   - The centre of the box goes to the centre of the slot.

3. WRITES EXACT PIXEL SIZES, so no browser has to resample at the common
   screen densities. Per course, into ``assets/images/course-motifs/marks/``:

       <slug>-mark.webp       80 px   lossless   1x screens
       <slug>-mark-2x.webp   160 px   quality 90 2x screens
       <slug>-mark-3x.webp   240 px   quality 90 3x screens

   The 80 px file is lossless because a lossy WebP stores colour at half
   resolution, which shows as colour bleed on an image this small. Each size
   is reduced from the master in one step and given a light unsharp mask.

``courses.yml`` names the 80 px file in each record's ``image``. The Library
template (``_listings/course-record.ejs``) derives the other two names from
it, and ``tools/validate_courses.py`` fails the render if either is missing.
The three files of a mark therefore always travel together: these names are
a contract between this script, the template and the validator.

WHERE THE MASTERS ARE. Ten of them live in the course repos, checked out
beside this one, because the course sites are where they were first used.
Five live here, under ``assets/images/course-motifs/icons/``. The table
below is the one place that says which is which. A master that is missing
stops the run; nothing is skipped silently.

Deterministic and idempotent. Run from the repo root, with the course repos
checked out as siblings:

    python tools/make_library_marks.py

Pillow is the only dependency (already used by the other image tools here).
"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageFilter

# The slot. SLOT_PX is the width of the Library's image column in CSS pixels
# (styles.css, .course-record-has-thumb) and the side of the 1x file.
SLOT_PX = 80
MAX_SIDE = SLOT_PX - 2
# (pixel density, file-name suffix, lossless). The suffixes are the contract
# with _listings/course-record.ejs and tools/validate_courses.py.
SIZES = ((1, "", True), (2, "-2x", False), (3, "-3x", False))
QUALITY = 90
METHOD = 6

# Finding and sizing the object. See point 1 and point 2 of the docstring.
INK_FLOOR = 24          # of 255: how far from white a pixel must be to count
BOX_SIDE = 66.0         # square root of the object's box area, in slot pixels
FILL_REF, FILL_POWER = 0.63, -0.20     # share of the box the object covers
INK_REF, INK_POWER = 0.40, -0.08       # mean darkness of the box, 0 to 1

# Unsharp mask applied after each reduction: (radius in output pixels, percent).
SHARPEN = (0.5, 50)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKS = os.path.join(ROOT, "assets", "images", "course-motifs", "marks")
HERE = os.path.join("assets", "images", "course-motifs", "icons")

# (slug, master path relative to this repo's root). The slug matches the
# course's hero thumbnail, <slug>-hero-480.webp, so the two stay paired.
MASTERS = [
    ("intro-stats", os.path.join("..", "intro-stats", "assets", "figures", "intro-stats-icon.png")),
    ("intro-math-software", os.path.join("..", "math-software", "assets", "intro-math-software-icon.png")),
    ("intro-probability", os.path.join("..", "intro-probability", "assets", "icon.png")),
    ("statistical-inference", os.path.join("..", "statistical-inference", "assets", "icon.png")),
    ("statistical-modeling", os.path.join("..", "statistical-modeling", "assets", "icon.png")),
    ("applied-statistics", os.path.join("..", "applied-statistics", "assets", "icon.png")),
    ("statistical-design", os.path.join("..", "statistical-design", "assets", "icon.png")),
    ("bayesian-statistics", os.path.join("..", "bayesian-statistics", "assets", "icon.png")),
    ("nonparametrics", os.path.join("..", "nonparametrics", "assets", "icon.png")),
    ("modern-sas", os.path.join("..", "modern-sas", "assets", "icon.png")),
    ("math-stats-1", os.path.join(HERE, "math-stats-1-icon.png")),
    ("math-stats-2", os.path.join(HERE, "math-stats-2-icon.png")),
    ("computational-statistics", os.path.join(HERE, "computational-statistics-icon.png")),
    ("bayesian-modeling", os.path.join(HERE, "bayesian-modeling-icon.png")),
    ("causal-inference", os.path.join(HERE, "causal-inference-icon.png")),
]


def find_object(master):
    """Where the object is, how much of its box it covers, and how dark it is.

    Measured on white, because that is what a visitor sees. A pixel's ink is
    its distance from white: 255 minus its lightest channel.
    """
    white = Image.new("RGBA", master.size, (255, 255, 255, 255))
    red, green, blue = Image.alpha_composite(white, master).convert("RGB").split()
    ink = ImageChops.invert(ImageChops.darker(ImageChops.darker(red, green), blue))
    box = ink.point(lambda v: 255 if v > INK_FLOOR else 0).getbbox()
    if box is None:
        raise SystemExit("A master is blank on white: nothing to draw.")
    hist = ink.crop(box).histogram()
    pixels = sum(hist)
    fill = sum(hist[INK_FLOOR + 1:]) / pixels
    mean_ink = sum(level * count for level, count in enumerate(hist)) / (255.0 * pixels)
    return box, fill, mean_ink


def object_scale(box, fill, mean_ink):
    """Slot pixels per master pixel. Point 2 of the docstring."""
    width, height = box[2] - box[0], box[3] - box[1]
    weight = (fill / FILL_REF) ** FILL_POWER * (mean_ink / INK_REF) ** INK_POWER
    return min(MAX_SIDE / max(width, height), BOX_SIDE * weight / math.sqrt(width * height))


def draw(master, box, scale, side):
    """The object at `scale`, centred in a transparent square `side` pixels wide."""
    centre_x, centre_y = (box[0] + box[2]) / 2.0, (box[1] + box[3]) / 2.0
    half = SLOT_PX / scale / 2.0    # master pixels from the centre to the slot's edge
    # The slot usually reaches past the master's own canvas, so widen it first.
    pad = int(math.ceil(half)) + 2
    wide = Image.new("RGBA", (master.size[0] + 2 * pad, master.size[1] + 2 * pad), (0, 0, 0, 0))
    wide.paste(master, (pad, pad))
    window = (centre_x - half + pad, centre_y - half + pad,
              centre_x + half + pad, centre_y + half + pad)
    # Work on premultiplied colour (mode RGBa): then neither the reduction nor
    # the unsharp mask can drag the colour of clear pixels into the edge.
    out = wide.convert("RGBa").resize((side, side), Image.LANCZOS, box=window)
    mask = ImageFilter.UnsharpMask(radius=SHARPEN[0], percent=SHARPEN[1], threshold=0)
    bands = [band.filter(mask) for band in out.split()]
    alpha = bands[3]
    # Premultiplied colour can never exceed its own alpha.
    out = Image.merge("RGBa", [ImageChops.darker(band, alpha) for band in bands[:3]] + [alpha])
    out = out.convert("RGBA")
    # Fully clear pixels carry white. A lossy encoder smears colour a little
    # across the object's edge; this way it smears toward the page's colour.
    clear = out.getchannel("A").point(lambda v: 255 if v == 0 else 0)
    out.paste(Image.new("RGBA", out.size, (255, 255, 255, 0)), (0, 0), clear)
    return out


def make_mark(slug, master_path):
    master = Image.open(master_path).convert("RGBA")
    box, fill, mean_ink = find_object(master)
    scale = object_scale(box, fill, mean_ink)
    written = []
    for density, suffix, lossless in SIZES:
        dst = os.path.join(MARKS, "%s-mark%s.webp" % (slug, suffix))
        mark = draw(master, box, scale, SLOT_PX * density)
        # exact=True keeps the white under the clear pixels as written.
        if lossless:
            mark.save(dst, "WEBP", lossless=True, quality=100, method=METHOD, exact=True)
        else:
            mark.save(dst, "WEBP", quality=QUALITY, method=METHOD, exact=True)
        written.append(dst)
    return box, scale, written


def main():
    missing = [(slug, rel) for slug, rel in MASTERS
               if not os.path.isfile(os.path.join(ROOT, rel))]
    if missing:
        for slug, rel in missing:
            sys.stderr.write("missing master for %s: %s\n" % (slug, rel))
        raise SystemExit("No marks written. Check out the course repos beside this one.")
    os.makedirs(MARKS, exist_ok=True)
    print("%-26s %-14s %s" % ("mark", "object, px", "files (KB): 1x, 2x, 3x"))
    for slug, rel in MASTERS:
        box, scale, written = make_mark(slug, os.path.join(ROOT, rel))
        print("%-26s %-14s %s" % (
            slug,
            "%.0f x %.0f" % ((box[2] - box[0]) * scale, (box[3] - box[1]) * scale),
            ", ".join("%.1f" % (os.path.getsize(path) / 1024) for path in written)))
    print("%d marks, %d files, in %s" % (
        len(MASTERS), len(MASTERS) * len(SIZES), os.path.relpath(MARKS, ROOT).replace(os.sep, "/")))


if __name__ == "__main__":
    main()
