"""Process a single raw image into web-ready assets.

Reads one image from assets/images/raw/ (or anywhere readable), strips
all EXIF/metadata, resizes (or center-crops) to a target, and writes
WebP + JPEG to assets/images/processed/ (or a chosen --out-dir).
Never overwrites the raw file.

Usage:
    python tools/process_images.py <input> [--target {brand,card,motif,banner,thumb}]
                                            [--name <slug>] [--all-widths]
                                            [--out-dir <dir>]
    python tools/process_images.py <input> --crop {og,square,square-lg}
                                            [--name <slug>] [--out-dir <dir>]

Width targets (preserve native aspect ratio):
    brand   -> 800
    card    -> 600
    motif   -> 600 + 320 (thumb)
    banner  -> 1600
    thumb   -> 320

Crop targets (center-crop to a fixed aspect/resolution):
    og        -> 1200 x  630  (Open Graph card)
    square    ->  600 x  600
    square-lg -> 1200 x 1200

Dependency: Pillow.  pip install Pillow
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.stderr.write(
        "Pillow is required: pip install Pillow\n"
        "Fallback (single file): magick mogrify -strip -resize 800x -quality 85 <file>\n"
    )
    sys.exit(1)


REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "assets" / "images" / "processed"

TARGETS: dict[str, list[int]] = {
    "brand": [800],
    "card": [600],
    "motif": [600, 320],
    "banner": [1600],
    "thumb": [320],
}

CROP_TARGETS: dict[str, tuple[int, int]] = {
    "og": (1200, 630),
    "square": (600, 600),
    "square-lg": (1200, 1200),
}

JPEG_QUALITY = 85
WEBP_QUALITY = 82


def _load_clean(src: Path) -> Image.Image:
    """Open `src`, apply EXIF orientation, then drop all metadata."""
    img = Image.open(src)
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")
    return img


def _drop_metadata(img: Image.Image) -> Image.Image:
    """Re-create the image without any info dict (drops EXIF/ICC/XMP).

    Saves below also pass `exif=b""` so EXIF cannot leak even if a
    future Pillow version preserves it through `paste`.
    """
    clean = Image.new(img.mode, img.size)
    clean.paste(img)
    return clean


def strip_and_resize(src: Path, width: int) -> Image.Image:
    """Open `src`, fix orientation, drop metadata, resize to `width` (preserve aspect)."""
    img = _load_clean(src)
    if img.width > width:
        ratio = width / img.width
        new_size = (width, max(1, round(img.height * ratio)))
        img = img.resize(new_size, Image.LANCZOS)
    return _drop_metadata(img)


def strip_and_crop(src: Path, target_w: int, target_h: int) -> Image.Image:
    """Open `src`, drop metadata, center-crop to the given aspect, resize to exact size."""
    img = _load_clean(src)
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        # source is too wide — crop columns from the sides
        new_w = int(round(src_h * target_ratio))
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    elif src_ratio < target_ratio:
        # source is too tall — crop rows from the top/bottom
        new_h = int(round(src_w / target_ratio))
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    img = img.resize((target_w, target_h), Image.LANCZOS)
    return _drop_metadata(img)


def write_outputs(img: Image.Image, out_stem: Path, suffix: str) -> list[Path]:
    """Write WebP + JPEG, using `<stem>-<suffix>.{webp,jpg}` naming."""
    out_stem.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    jpg_path = out_stem.with_name(f"{out_stem.name}-{suffix}.jpg")
    webp_path = out_stem.with_name(f"{out_stem.name}-{suffix}.webp")
    # Force empty EXIF on save so nothing leaks even if metadata sneaks back in.
    img.save(jpg_path, format="JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True, exif=b"")
    img.save(webp_path, format="WEBP", quality=WEBP_QUALITY, method=6, exif=b"")
    written.extend([jpg_path, webp_path])
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="Path to a raw image file.")
    parser.add_argument("--target", choices=sorted(TARGETS), default=None,
                        help="Preset width set (resize, preserving aspect).")
    parser.add_argument("--crop", choices=sorted(CROP_TARGETS), default=None,
                        help="Center-crop to a fixed aspect/resolution (overrides --target).")
    parser.add_argument("--name", default=None,
                        help="Output basename (without extension). Defaults to the input stem.")
    parser.add_argument("--all-widths", action="store_true",
                        help="With --target: emit every width in the preset.")
    parser.add_argument("--out-dir", type=Path, default=PROCESSED_DIR,
                        help=f"Output directory (default: {PROCESSED_DIR}).")
    args = parser.parse_args()

    # Resolve to absolute paths so output reporting is stable regardless
    # of where the script was invoked from.
    args.input = args.input.resolve()
    args.out_dir = args.out_dir.resolve()
    src: Path = args.input
    if not src.is_file():
        parser.error(f"Input not found: {src}")
    if src.parent == args.out_dir:
        parser.error("Refusing to read from the output directory.")
    if args.target is None and args.crop is None:
        args.target = "card"  # back-compat default

    base = args.name or src.stem
    # Normalize the name: lowercase, spaces → hyphens, strip non-safe chars.
    safe = (
        base.lower()
        .replace(" ", "-")
        .replace("_", "-")
    )
    safe = "".join(ch for ch in safe if ch.isalnum() or ch in "-")
    if not safe:
        parser.error("Output name reduces to empty after sanitization.")

    out_stem = args.out_dir / safe
    written: list[Path] = []

    if args.crop is not None:
        target_w, target_h = CROP_TARGETS[args.crop]
        img = strip_and_crop(src, target_w, target_h)
        suffix = args.crop  # e.g. "og", "square"
        written.extend(write_outputs(img, out_stem, suffix))
    else:
        widths = TARGETS[args.target]
        if not args.all_widths:
            widths = widths[:1]
        for w in widths:
            img = strip_and_resize(src, w)
            written.extend(write_outputs(img, out_stem, str(w)))

    for p in written:
        try:
            print(p.relative_to(REPO_ROOT))
        except ValueError:
            print(p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
