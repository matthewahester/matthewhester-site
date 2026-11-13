#!/usr/bin/env python3
"""Write the small navbar copy of a course mark.

A course mark is a 1254x1254 RGBA PNG on transparency (see
tools/make_course_icon.py). The course sites show it in the navbar at
``max-height: 1.5rem``, about 25 px tall, on every page. Naming the master
itself as the navbar ``logo`` therefore sent a 1.2 to 2.7 MB image with the
first view of every course site (measured on the live sites, 2026-11-12).

This script writes a 128 px copy beside each master, ``<stem>-128.png``.
That copy is what a course site's ``_quarto.yml`` names as ``logo:``. The
master stays where it is, as the source; once nothing references it, Quarto
no longer copies it into ``_site/``.

128 px covers a 25 px slot up to about 5x pixel density. PNG keeps the
transparency the dark navbar needs, and a PNG save carries no EXIF.

Deterministic and idempotent. Never upscales. Give it one mark or several:

    python tools/make_navbar_logo.py ../statistical-inference/assets/icon.png

Pillow is the only dependency (already used by the other image tools here).
"""
import os
import sys

from PIL import Image

LOGO_PX = 128


def logo_path(master_path):
    stem, _ = os.path.splitext(master_path)
    return "%s-%d.png" % (stem, LOGO_PX)


def make_logo(master_path):
    master = Image.open(master_path).convert("RGBA")
    w, h = master.size
    scale = LOGO_PX / max(w, h)
    logo = master
    if scale < 1:  # never upscale
        # Pillow premultiplies alpha for an RGBA resize, so the transparent
        # field does not bleed a fringe into the mark's edge.
        logo = master.resize((max(1, round(w * scale)), max(1, round(h * scale))),
                             Image.LANCZOS)
    dst = logo_path(master_path)
    logo.save(dst, "PNG", optimize=True)
    return dst, (w, h), logo.size


def main(argv):
    if len(argv) < 2:
        raise SystemExit("usage: make_navbar_logo.py MASTER.png [MASTER.png ...]")
    for master_path in argv[1:]:
        dst, src_size, out_size = make_logo(master_path)
        print("%s\n  %dx%d %6.0f KB  ->  %dx%d %5.1f KB  %s" % (
            master_path, src_size[0], src_size[1], os.path.getsize(master_path) / 1024,
            out_size[0], out_size[1], os.path.getsize(dst) / 1024, dst))


if __name__ == "__main__":
    main(sys.argv)
