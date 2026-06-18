#!/usr/bin/env python3
"""Regenerate course-card hero THUMBNAILS for the teaching hub.

The full hero PNGs in ``assets/images/course-motifs/<name>-hero.png`` are the
preserved masters (~2.3 MB each, ~1450 px wide). The teaching hub only ever
shows them as small course cards (measured max render ~385 px desktop, ~553 px
on the home page, up to ~460 px on a 1-col mobile), so loading the masters —
or even a single oversized thumbnail — wastes bandwidth. This script writes two
WebP candidates per hero to ``course-motifs/thumbs/``: a 480 px 1x
(``<name>-hero-480.webp``) and an 800 px 2x (``<name>-hero.webp``). The cards in
``teaching.qmd`` / ``index.qmd`` reference both via ``srcset``/``sizes`` so the
browser picks the right one for the viewport and pixel density.

Deterministic and idempotent. Never upscales. Strips metadata (WebP save
carries none). Run from the repo root:

    python tools/make_hero_thumbs.py

Pillow is the only dependency (already used by tools/process_images.py).
Course landing pages keep their own larger ~1400 px WebP web-heroes in their
own repos; this script is hub-card thumbnails only.
"""
import glob
import os
from PIL import Image

# (suffix, width): the 800px keeps the historical unsuffixed name as the 2x
# candidate; the 480px is the 1x candidate. Never upscales.
THUMB_VARIANTS = [("-480", 480), ("", 800)]
QUALITY = 90
METHOD = 6

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTIFS = os.path.join(ROOT, "assets", "images", "course-motifs")
THUMBS = os.path.join(MOTIFS, "thumbs")


def main():
    os.makedirs(THUMBS, exist_ok=True)
    masters = sorted(glob.glob(os.path.join(MOTIFS, "*-hero.png")))
    if not masters:
        raise SystemExit(f"No *-hero.png masters found in {MOTIFS}")
    for src in masters:
        stem = os.path.splitext(os.path.basename(src))[0]
        master = Image.open(src)
        w, h = master.size
        for suffix, width in THUMB_VARIANTS:
            dst = os.path.join(THUMBS, stem + suffix + ".webp")
            im = master
            if width < w:  # never upscale
                im = master.resize((width, round(h * width / w)), Image.LANCZOS)
            im.convert("RGB").save(dst, "WEBP", quality=QUALITY, method=METHOD)
            print(f"{stem + suffix:38s} {im.size[0]}x{im.size[1]}  "
                  f"{os.path.getsize(dst) / 1024:6.0f} KB")


if __name__ == "__main__":
    main()
