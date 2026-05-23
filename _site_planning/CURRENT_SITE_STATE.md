# Current site state — matthewhester.com

_Snapshot for handoff / review. Local planning only; not rendered into
`_site/`. Last updated: 2026-05-23 (end of Phase 4C)._

## Repo

- Path: `D:/Github/matthewhester-site/`
- Eventual domain: `matthewhester.com`
- Stack: Quarto 1.8.26, Bootstrap (cosmo theme), plain `styles.css`,
  no JS
- Remote: `https://github.com/matthewahester/matthewhester-site.git`

## Render status

- Last render: 2026-05-23, end of Phase 4C, `quarto render` from repo
  root → exit 0, 8 qmd files → `_site/`.
- PowerShell `NativeCommandError` around progress output is cosmetic;
  trust the exit code.

## Main pages and navbar

Top-level pages (and the order they appear in the navbar):

| Page      | File             | Role                                                                  |
| --------- | ---------------- | --------------------------------------------------------------------- |
| Home      | `index.qmd`      | Title block (H1 + subtitle) + split-hero (intro + portrait) + cards   |
| About     | `about.qmd`      | Short professional bio + brief personal note                          |
| Teaching  | `teaching.qmd`   | Current courses, public-site vs LMS distinction, MAC                  |
| Research  | `research.qmd`   | Interests + projects + (placeholder) publications/talks               |
| Resources | `resources.qmd`  | Software guides, statistics notes, cross-links to course sites        |
| CV        | `cv.qmd`         | Position summary + interests + PDF placeholder                        |
| Contact   | `contact.qmd`    | University vs general professional channels + Blackboard pointer      |

Not in the navbar but still in the repo:

- `projects.qmd` — Phase 4A redirect stub (`<meta refresh>` → `research.html`).
  Hand-delete when comfortable that nothing links to `/projects.html`.

## Visual identity status

- **Palette:** rock/crystal/climbing tokens in `styles.css`
  (`--stone-50 / 100 / 200 / 400 / 700 / 900`, `--crystal-blue`,
  `--iron-accent`, `--moss-quiet`). Unchanged since Phase 3.
- **Type:** Inter (body + headings), JetBrains Mono (code). System
  fallback chain in `_quarto.yml`.
- **Hero:** Quarto title block (single H1) above a two-column split
  with intro prose + page links on the left and the stylized portrait
  on the right. Collapses to single-column ≤720px with the portrait
  above the text.
- **Cards:** all text-only as of Phase 4C. `.feature-card` for category
  cards, `.feature-card.course-card` for course links (warmer left
  edge). CSS rules for image-bearing cards
  (`.feature-card-with-image`, `.feature-card-img`) remain in
  `styles.css` for the day a card image is intentionally selected.
- **No JS**, no analytics, no third-party widgets.

## Current image policy

- **Raw originals** stage in `assets/images/raw/` (gitignored).
- **Processed images:**
  - `assets/images/brand/`: `portrait-matt-hester-800.{webp,jpg}`,
    `og-default-og.{webp,jpg}` (1200×630 OG card), plus the orphaned
    `portrait-placeholder.svg`.
  - `assets/images/course-motifs/`: five 600px motif/course images
    produced in Phase 4B, currently **unreferenced** in any QMD.
- **No location-revealing filenames** in committed assets.
- **EXIF stripped** on all processed outputs (verified
  `exif_keys=0` in Phase 4B).
- **Helper:** `tools/process_images.py` (Pillow).
- **Card images are intentionally not wired** as of Phase 4C — see
  the Phase 4C summary below.

## Deployment posture (unchanged)

- `.github/workflows/publish.yml` is `on: workflow_dispatch` only.
- `CNAME` at repo root is exactly `matthewhester.com` (no trailing
  newline-stripping needed; Quarto copies it into `_site/`).
- DNS is **unchanged**: `matthewhester.com` still points at the old
  Google Site. Switching is a separate, explicit decision.

## What changed in Phase 4C

Editorial cleanup, no structural changes:

- **Homepage cards** are now text-only. The Phase 4B image-on-card
  variant is intentionally not used; the processed motif files remain
  on disk for future intentional selection.
- **Hero portrait** is unchanged — still
  `assets/images/brand/portrait-matt-hester-800.webp`.
- **Research page rewritten.** "Bayesian Nutrition Observatory (BNO)"
  branding removed from the public page; the rewritten page covers
  five interest areas and four project lines using grounded,
  non-overbranded headings. BNO is preserved only as a private
  planning note (this file + `OPEN_DECISIONS.md`), not on the public
  site.
- **Contact page restructured.** University email
  (`mhester@ualr.edu`), general professional email
  (`matthewahester@gmail.com`), and GitHub are now separate channels.
  Blackboard pointer added for currently enrolled students.
- **CV link fixed.** `cv.qmd` no longer points at the removed
  `Projects` page; it now points to `Research`.
- **Handoff packet** created: this file,
  `_site_planning/OPEN_DECISIONS.md`,
  `_site_planning/SITE_REVIEW_PACKET.md`.
- **No DNS, deploy, or course-site changes.**

## Open decisions

See [`OPEN_DECISIONS.md`](OPEN_DECISIONS.md). Short list:

1. Publish Gmail, school email, or both? (Currently: both.)
2. Which boulder images, if any, should represent which course?
3. Delete `projects.qmd` redirect stub now or after first publish?
4. Publish CV PDF, or keep it text-only on the page?
5. Deploy under GitHub Pages now or later?
6. Add back-links from course sites to the hub?
7. Implement the combined-deploy pipeline for course-site
   subdirectories?

## What ChatGPT (or any reviewer) should inspect

See [`SITE_REVIEW_PACKET.md`](SITE_REVIEW_PACKET.md). Short list:

- All seven top-level QMD pages + `styles.css` + `_quarto.yml`.
- `CLAUDE.md`, `SITE_VISION.md`, `BRAND_STYLE_BRIEF.md`,
  `SITE_LINKING_PLAN.md` for design intent and constraints.
- `_site_planning/CURRENT_SITE_STATE.md` (this file) and
  `_site_planning/OPEN_DECISIONS.md` for current posture and what's
  still open.
- Optionally `IMAGE_ASSET_PLAN.md` if image policy is the focus.
