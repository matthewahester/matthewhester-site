#!/usr/bin/env python3
"""Regenerate course-card hero THUMBNAILS for the teaching hub.

The full hero PNGs in ``assets/images/course-motifs/<name>-hero.png`` are the
preserved masters (~2.3 MB each, ~1450 px wide). The teaching hub only ever
shows them as small course cards, so loading the masters wastes bandwidth.
This script writes ~800 px WebP thumbnails to ``course-motifs/thumbs/`` which
the cards in ``teaching.qmd`` / ``index.qmd`` reference instead.

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

THUMB_WIDTH = 800
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
        dst = os.path.join(THUMBS, stem + ".webp")
        im = Image.open(src)
        w, h = im.size
        if THUMB_WIDTH < w:  # never upscale
            im = im.resize((THUMB_WIDTH, round(h * THUMB_WIDTH / w)),
                           Image.LANCZOS)
        im.convert("RGB").save(dst, "WEBP", quality=QUALITY, method=METHOD)
        kb_src = os.path.getsize(src) / 1024
        kb_dst = os.path.getsize(dst) / 1024
        print(f"{stem:34s} {im.size[0]}x{im.size[1]}  "
              f"{kb_dst:6.0f} KB  (master {kb_src:6.0f} KB)")


if __name__ == "__main__":
    main()
