# Image asset plan — matthewhester.com

_Phase 4A. Local planning only; not rendered into `_site/`._
_Last updated: 2026-05-23._

How images get from raw originals on disk into the public site without
leaking metadata, identifying other people, or echoing exact climbing
locations.

The intended workflow is **ad-hoc and human-in-the-loop**, not a batch
pipeline. Most images will be picked one at a time in conversation with
the assistant; `tools/process_images.py` exists as a small helper, not
as automation.

## 1. Folder structure

```
assets/
  images/
    raw/              # gitignored; full-size originals, with EXIF intact
    processed/        # optimized web images (committed)
    brand/            # portrait, logo, favicon, OG card (committed)
    course-motifs/    # course-specific images for cards / banners (committed)
  css/                # reserved; styles.css currently lives at repo root
  icons/              # reserved for SVG icons if needed later
```

Brand assets live under `assets/images/brand/`. The older top-level
`assets/brand/` redirect-stub folder was removed in Phase 5F.

## 2. Privacy and licensing

These rules apply to every image before it lands in `processed/`,
`brand/`, or `course-motifs/`:

1. **EXIF / GPS metadata is stripped.** No exceptions. `process_images.py`
   does this; if processing manually, verify with `exiftool -a -G1` or
   equivalent and re-strip.
2. **No identifiable people other than Matt Hester** without explicit
   per-image approval. Group shots, climbing partners in the background,
   etc. — crop them out or pick a different image.
3. **No climbing-area names in published filenames or alt text.** Raw
   files like `Alum Creek 072023.jpg` are renamed to neutral descriptors
   like `sandstone-face-01.jpg` before publication. Location stays in
   the raw filename only.
4. **No locations inferred from metadata or visual landmarks** in alt
   text or surrounding copy. "Textured sandstone face with quartz
   vein," not "Glazypeau crystals."
5. **Drone imagery** (`DJI_*` files) gets extra scrutiny — drone shots
   often reveal more identifying landscape than handheld shots. Use
   only crops that don't reveal exact approach paths or private land.
6. **License clarity.** All photos are Matt Hester's own work; no
   third-party imagery is published without explicit license + attribution.

## 3. Raw vs published policy

- **Raw originals** live in `assets/images/raw/`, which is gitignored
  via the repo `.gitignore`. They are also mirrored in
  `D:/My Drive Personal/Climbing/Favorite Photos/` (climbing) and
  `D:/My Drive Personal/Personal/` (portrait). Treat `raw/` as a
  staging area, not as the canonical archive.
- **Processed images** in `processed/`, `brand/`, and `course-motifs/`
  are committed and shipped with the site. Once processed, they are
  considered public; never re-add an unsanitized version on top of a
  processed one.
- **Old raw files** that have been processed can be deleted from
  `assets/images/raw/` to keep the staging area small. Originals
  remain in the Google Drive folders.

## 4. Recommended sizes

| Use                         | Width  | Aspect    | Format                  |
| --------------------------- | ------ | --------- | ----------------------- |
| Homepage portrait           | 800px  | 4:5       | WebP + JPEG fallback    |
| Section / category card     | 600px  | 3:2       | WebP + JPEG fallback    |
| Course-card motif           | 600px  | 3:2 or 1:1| WebP + JPEG fallback    |
| Page banner (optional)      | 1600px | 4:1       | WebP + JPEG fallback    |
| OG card (`og-card.png`)     | 1200×630 | fixed   | PNG (per OG spec)       |
| Favicon                     | 32×32  | square    | ICO + SVG               |
| Thumbnail (listings)        | 320px  | 1:1       | WebP + JPEG fallback    |

The processing helper writes both a WebP (`<name>.webp`) and a JPEG
(`<name>.jpg`) fallback at each target width so consumers can pick.

## 5. Alt-text strategy

Every committed image carries alt text in the Quarto source. Style guide:

- **One sentence**, present tense, factual.
- **No location names.** "Textured sandstone face with horizontal break,"
  not "Alum Creek roof."
- **No emotional adjectives** ("beautiful," "dramatic").
- **Decorative images** (`role="presentation"` / `alt=""`) are reserved
  for purely ornamental cases. Almost everything on this site is
  contentful and gets real alt text.
- **Portrait** is always "Stylized portrait of Matt Hester." If the
  portrait changes to a photographic version, switch to "Photograph of
  Matt Hester."

## 6. Asset roles — Phase 4B picks

Source folders:

- Climbing: `D:/My Drive Personal/Climbing/Favorite Photos/` (37+ images,
  Arkansas sandstone / quartz sites).
- Portrait: `D:/My Drive Personal/Personal/` (`Hester_profile_art.png`,
  which the user moved into the repo as part of Phase 4B and was
  re-staged into `assets/images/raw/`).

| Slot                        | Raw source (under `raw/`)       | Processed output                                  | Alt text used                                                       |
| --------------------------- | ------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| Homepage portrait           | `Hester_profile_art.png`        | `brand/portrait-matt-hester-800.{webp,jpg}`       | Stylized illustrated portrait of Matt Hester.                       |
| Site-wide OG card           | `drone-landscape.jpg`           | `brand/og-default-og.{webp,jpg}` (1200×630 crop)  | _(site fallback; per-page OG falls through to page first image)_    |
| Teaching card               | `drone-landscape.jpg`           | `course-motifs/motif-teaching-600.{webp,jpg}`     | Wide aerial view of a forested landscape with exposed rock features. |
| Research card               | `roof-overhang.jpg`             | `course-motifs/motif-research-600.{webp,jpg}`     | Underside of a steep rock overhang with complex texture and shadow. |
| Resources card              | `crystals-closeup.jpg`          | `course-motifs/motif-resources-600.{webp,jpg}`    | Close-up of quartz crystals embedded in stone.                      |
| Math Software course card   | `structured-face.jpg`           | `course-motifs/course-math-software-600.{webp,jpg}` | Geometrically structured rock face with crisp horizontal breaks.    |
| Intro Stats course card     | `branching-block.jpg`           | `course-motifs/course-intro-stats-600.{webp,jpg}` | Boulder with branching cracks splitting the face into distinct regions. |

**Raw filenames in `raw/` were renamed at the copy step** to neutral
descriptors (no climbing-area names). The original Google Drive
filenames are preserved at the source folders for personal reference.

**Privacy and metadata verification (Phase 4B):**

- Raw originals at `assets/images/raw/` are gitignored.
- All processed outputs verified with Pillow: `exif_keys=0`.
- No identifiable third parties in selected images, to the best of
  filename-based judgement. **User to confirm** none of the selected
  images contain other climbers visible enough to identify — most
  selections are landscape / boulder / texture shots, not action shots.
- Filenames in `brand/` and `course-motifs/` contain no location
  references.

**What remains placeholder:**

- No favicon — see `_quarto.yml` `TODO(Phase 4C)`.

Image curation remains an ad-hoc, in-chat process. Phase 4B picks are
filename-based best guesses; swap any image by dropping a new raw file
in `raw/` and rerunning `tools/process_images.py` with the same `--name`.

## 7. Processing helper

`tools/process_images.py` is a small Pillow-based script that:

- reads from `assets/images/raw/`,
- strips all EXIF metadata,
- resizes to a configurable set of target widths,
- writes WebP + JPEG to `assets/images/processed/`,
- and never overwrites a file in `raw/`.

Run from the repo root:

```bash
python tools/process_images.py <input> [--target brand|card|motif|banner|thumb] [--name <slug>]
```

Where `<input>` is a path to a single file in `raw/`. The `--name`
flag lets you rename in the same step, which is the easiest way to drop
the climbing-location filename. See the script's header for full
options.

Pillow is the only dependency:

```bash
pip install Pillow
```

If Pillow is unavailable, fall back to ImageMagick:

```bash
magick mogrify -strip -resize 800x -quality 85 -format jpg <input>
```
