#!/usr/bin/env python3
"""Cut the centre object out of a course hero and write a course-mark icon.

The course family's navbar mark is a single isolated object on transparency:
1254x1254 RGBA PNG, object centred with a little breathing room, no plate and no
background. The heroes the marks come from are 4:3 posters on a parchment field,
with the subject in the middle column and typeset panels down both sides.

WHY THIS IS NOT A COLOUR KEY
----------------------------
The obvious approach -- make every pixel near the parchment colour transparent --
produces a mark that looks perfect over cream and is full of holes over black,
because these subjects are PAINTED IN THE FIELD'S OWN COLOURS. The stone arch is
cream. The layered vessel is cream. The punched tape is cream. A colour key
cannot tell the tape from the paper behind it, so it removes both, and the damage
stays invisible until the mark is composited on the dark navbar where it actually
lives. The first version of this script did exactly that: a 181px gash through
the tape loop, 806 pinholes through the arch, and 5% of one subject's body area
transparent -- none of it visible over cream.

So the background is found by CONNECTIVITY, not by colour. Field-coloured pixels
are flooded inwards from the crop border: whatever the flood reaches is paper,
and whatever it cannot reach is subject, however pale. Cream sealed inside the
subject's own ink outlines is never reached, so it stays. Openwork still reads
correctly -- the gaps between the armillary's rings connect to the outside, so
they are paper and they go.

Two things the flood alone will not do:

  WATERCOLOUR SPATTER is not field-coloured, so the flood stops at it and it
  survives. Colour will not remove it either: the wash sits as far from the cream
  field as the brass does, and further than the sphere's own rings, so any
  tolerance that loses the wash loses the rings first. Nor will connectivity: it
  pools against the base and merges with it. What the wash has none of is ink, so
  it goes by distance from drawn line work (`--ink-radius`).

  THE ANTI-ALIASED EDGE of the subject is blended with cream in the source. Kept
  as-is it survives as a pale fringe -- a frosted outline that reads as a halo on
  a dark bar. So the matte is choked by a pixel (`--choke`) before it is feathered
  (`--soft`).

Nothing here is automatic enough to trust unseen. Every run also writes a
`-dark-preview.png` composite on the navbar's near-black, because that is the
only view that shows a halo, a hole, or spatter that should have gone. Judging
the mark over cream will tell you it is fine when it is not.

    python tools/make_course_icon.py SOURCE --name math-stats-1 \
        --bbox 0.30,0.05,0.74,0.79 --outdir assets/images/course-motifs/icons

Tuning, in the order worth trying:
    --bbox        when the subject is clipped or a side panel crept in
    --tol         how close to the field a pixel must be to count as paper.
                  RAISE if paper survives as a dirty plate around the subject;
                  LOWER if the flood leaks through an outline and eats the
                  subject's cream from the inside.
    --seal        close gaps in the subject's outline before the flood, which is
                  the other cure for that leak.
    --ink-radius  lower sheds more watercolour wash, higher keeps more.
    --min-area    higher drops more loose speckle and background line-art.
    --wash-reach  how far the painted ground may spread past the object. Set 0
                  for a hard-isolated mark with no ground at all. Do NOT chase a
                  cleaner ground with --ink-radius or --min-area: those cut into
                  the object, which is how two earlier rounds got gouged.
"""

import argparse
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ICON_PX = 1254            # every existing course mark is 1254x1254
DARK = (31, 31, 31)       # the navbar's near-black, for the preview composite


def parse_bbox(text):
    parts = [float(v) for v in text.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("bbox needs 4 comma-separated fractions")
    l, t, r, b = parts
    if not (0 <= l < r <= 1 and 0 <= t < b <= 1):
        raise argparse.ArgumentTypeError("bbox must be 0<=left<right<=1, 0<=top<bottom<=1")
    return l, t, r, b


def background_colour(rgb, frac=0.06):
    """Median of the four corner patches.

    The corners of a centre-column crop are always field, never subject, which
    makes this more reliable than a global mode -- a large pale subject can
    otherwise win the histogram and key itself out.
    """
    h, w = rgb.shape[:2]
    ph, pw = max(2, int(h * frac)), max(2, int(w * frac))
    patches = np.concatenate([
        rgb[:ph, :pw].reshape(-1, 3), rgb[:ph, -pw:].reshape(-1, 3),
        rgb[-ph:, :pw].reshape(-1, 3), rgb[-ph:, -pw:].reshape(-1, 3),
    ])
    return np.median(patches, axis=0)


def reachable_field(dist, tol, seal):
    """The paper: field-coloured pixels the crop border can actually reach.

    `seal` removes field-coloured specks and hairline channels first, so a single
    broken pixel in a drawn outline cannot let the flood through and hollow the
    subject out from the inside -- damage that looks like nothing at all when the
    result is viewed over cream.
    """
    fieldish = dist < tol
    if seal > 0:
        fieldish = ndimage.binary_opening(fieldish, structure=np.ones((seal, seal)))

    seed = np.zeros(fieldish.shape, dtype=bool)
    seed[0, :] = seed[-1, :] = seed[:, 0] = seed[:, -1] = True
    return ndimage.binary_propagation(seed & fieldish, mask=fieldish)


def ink_proximity(rgb, ink_level, radius):
    """Pixels within `radius` of drawn ink -- the test that sheds the wash.

    Per-pixel proximity, deliberately not a flood from a seed: a flood would run
    straight from the subject's base into the wash pooled against it.
    """
    gray = rgb.astype(np.float32).mean(axis=2)
    return ndimage.binary_dilation(gray < ink_level, iterations=max(1, radius))


def build_matte(rgb, tol, seal, ink_level, ink_radius, min_area_frac, choke, soft,
                wash_reach, wash_span, wash_max, erase=(), keep=0):
    bg = background_colour(rgb)
    dist = np.linalg.norm(rgb.astype(np.float32) - bg, axis=2)

    solid = ~reachable_field(dist, tol, seal)

    # Manual erasures, in crop-fraction coordinates. The flood and the gates are
    # global rules, and some defects are local facts: a caption fragment lying
    # against the subject, a wash lobe standing off one edge, a cut element like
    # the plumb-bob whose suspension line cannot survive. Erasing them here --
    # before components are counted and before the edge is feathered -- means
    # the cut edge gets the same soft treatment as every natural edge, and any
    # crumbs the cut strands are swept by the area rule.
    h, w = solid.shape
    for (el, et, er, eb) in erase:
        solid[int(et * h):int(eb * h), int(el * w):int(er * w)] = False

    # --- the drawn object, always fully opaque ------------------------------
    core = solid & ink_proximity(rgb, ink_level, ink_radius) if ink_radius > 0 else solid
    # The ink gate shaves the wash off the outside, but on its own it also bites
    # holes in the middle of any broad plain area -- the centre of a cream tile
    # is further from a drawn line than the radius allows. Put back anything it
    # removed that its own result encloses. Filling is safe ONLY because it is
    # intersected with `solid`: openwork gaps are background, never in `solid`,
    # so the armillary's rings and the arch's aperture cannot be filled in.
    core = core | (ndimage.binary_fill_holes(core) & solid)

    labels, n = ndimage.label(core)
    if n:
        areas = ndimage.sum(core, labels, range(1, n + 1))
        mask = np.zeros(n + 1, dtype=bool)
        if keep > 0:
            # Keep exactly the N largest pieces, regardless of area threshold.
            order = np.argsort(areas)[::-1][:keep]
            mask[order + 1] = True
        else:
            mask[1:] = areas >= min_area_frac * core.size
            if not mask[1:].any():      # nothing cleared the bar; keep the largest
                mask[int(np.argmax(areas)) + 1] = True
        core = mask[labels]

    # Choke, then feather. The choke drops the source's cream-blended edge pixel;
    # the feather turns the hard binary edge into a one-pixel ramp rather than a
    # staircase. The core is BINARY before feathering, which is the whole point:
    # interior alpha is 1 everywhere, so a pale subject cannot go see-through
    # however it is painted.
    if choke > 0:
        core = ndimage.binary_erosion(core, iterations=choke)
    alpha = ndimage.gaussian_filter(core.astype(np.float32), sigma=max(soft, 1e-3))

    # --- the watercolour ground, fading out on its own density --------------
    # Cutting the ground off with a hard mask is what made earlier marks look
    # torn: the wash is a soft bleed, and any binary boundary through it reads as
    # a jigsaw edge or a chopped selection. Two reviews called that out as the
    # main remaining defect, and every attempt to shed MORE of it by tightening
    # --ink-radius or --min-area instead bit chunks out of the object.
    #
    # So the ground is not cut, it is faded. Within `reach` px of the object,
    # unreached-by-flood pixels take an alpha from their own density -- a dense
    # stain stays visible, a thin bleed goes to nothing -- and beyond that reach
    # the ground is gone. The result ends where the paint ends instead of where
    # a mask edge fell.
    if wash_reach > 0 and wash_max > 0:
        band = ndimage.binary_dilation(core, iterations=wash_reach) & solid & ~core
        density = np.clip((dist - tol) / max(wash_span, 1e-6), 0.0, 1.0)
        ground = ndimage.gaussian_filter((band * density).astype(np.float32), sigma=2.0)
        alpha = np.maximum(alpha, np.clip(ground, 0.0, 1.0) * wash_max)

    return np.clip(alpha, 0.0, 1.0), int(n)


def trim_and_square(rgba, pad_frac):
    a = rgba[:, :, 3]
    ys, xs = np.nonzero(a > 8)
    if not len(ys):
        raise SystemExit("nothing survived the matte -- raise --tol or widen --bbox")
    top, bot, left, right = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    cropped = rgba[top:bot, left:right]

    h, w = cropped.shape[:2]
    side = int(max(h, w) * (1 + 2 * pad_frac))
    out = np.zeros((side, side, 4), dtype=np.uint8)
    y0, x0 = (side - h) // 2, (side - w) // 2
    out[y0:y0 + h, x0:x0 + w] = cropped
    return out, (w, h)


def report(icon):
    """Numbers for the two failures that are hard to see at a glance."""
    a = np.asarray(icon)[:, :, 3].astype(np.float32) / 255.0
    body = a > 0.02
    # Interior transparency is the cutout damage this script exists to avoid:
    # holes inside the subject read as black on the navbar and as nothing at all
    # over cream, so they hide from a look at the wrong background.
    holes = int((ndimage.binary_fill_holes(body) & ~body).sum())
    _, islands = ndimage.label(body)
    return float(body.mean()), holes, int(islands)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--name", required=True, help="slug; writes <slug>-icon.png")
    ap.add_argument("--bbox", type=parse_bbox, default=(0.30, 0.03, 0.75, 0.80),
                    help="fractional left,top,right,bottom of the subject column")
    ap.add_argument("--tol", type=float, default=26.0,
                    help="how close to the field colour still counts as paper")
    ap.add_argument("--seal", type=int, default=3,
                    help="close outline gaps before the flood, px")
    ap.add_argument("--ink", type=float, default=120.0, help="grey level counted as ink")
    ap.add_argument("--ink-radius", type=int, default=12,
                    help="keep only within this many px of ink; 0 disables")
    ap.add_argument("--min-area", type=float, default=0.0025,
                    help="drop components smaller than this fraction of the crop")
    ap.add_argument("--choke", type=int, default=1, help="pull the matte in, px")
    ap.add_argument("--wash-reach", type=int, default=45,
                    help="how far the watercolour ground may extend past the object, px; 0 cuts it")
    ap.add_argument("--wash-span", type=float, default=90.0,
                    help="density over which the ground fades to nothing")
    ap.add_argument("--wash-max", type=float, default=0.85,
                    help="most opaque the ground may get, 0-1")
    ap.add_argument("--soft", type=float, default=0.8, help="edge feather sigma, px")
    ap.add_argument("--pad", type=float, default=0.06, help="breathing room, fraction")
    ap.add_argument("--erase", type=parse_bbox, action="append", default=[],
                    help="fractional l,t,r,b rect (crop coords) to blank; repeatable")
    ap.add_argument("--keep", type=int, default=0,
                    help="keep exactly the N largest components; 0 uses --min-area")
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    src = Image.open(args.source).convert("RGB")
    W, H = src.size
    l, t, r, b = args.bbox
    box = (int(l * W), int(t * H), int(r * W), int(b * H))
    rgb = np.asarray(src.crop(box))

    alpha, ncomp = build_matte(rgb, args.tol, args.seal, args.ink, args.ink_radius,
                               args.min_area, args.choke, args.soft,
                               args.wash_reach, args.wash_span, args.wash_max,
                               args.erase, args.keep)
    rgba = np.dstack([rgb, (alpha * 255).astype(np.uint8)])
    squared, subject_wh = trim_and_square(rgba, args.pad)

    icon = Image.fromarray(squared, "RGBA").resize((ICON_PX, ICON_PX), Image.LANCZOS)
    os.makedirs(args.outdir, exist_ok=True)
    icon_path = os.path.join(args.outdir, "%s-icon.png" % args.name)
    icon.save(icon_path, "PNG", optimize=True)          # PNG save carries no EXIF

    preview = Image.new("RGB", icon.size, DARK)
    preview.paste(icon, (0, 0), icon)
    preview_path = os.path.join(args.outdir, "%s-icon-dark-preview.png" % args.name)
    preview.save(preview_path, "PNG", optimize=True)

    coverage, holes, islands = report(icon)
    print("%s\n  crop %s  subject %s  components %d"
          "\n  coverage %.1f%%  interior holes %d px  islands %d\n  %s\n  %s"
          % (args.name, box, subject_wh, ncomp, coverage * 100, holes, islands,
             icon_path, preview_path))


if __name__ == "__main__":
    sys.exit(main())
