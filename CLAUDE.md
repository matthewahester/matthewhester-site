# CLAUDE.md — matthewhester.com

Notes for Claude Code (or any AI assistant) working in this repo. Keep
these in mind alongside the user's explicit instructions.

## What this repo is

A small Quarto website that will publish to GitHub Pages at the custom
domain [matthewhester.com](https://matthewhester.com). It hosts a
professional landing page, teaching index, research summary, and a
small set of public resources for Matt Hester (UA Little Rock).

Phase 4A (2026-05-23) reframed the site as a **professional hub**, not
a static CV page. The hub links out to standalone public course sites
(`/math-software/`, `/intro-stats/`), each in its own repo.

## Read these first

When starting work in this repo, skim:

- `SITE_VISION.md` — purpose, audience, tone, architecture.
- `BRAND_STYLE_BRIEF.md` — palette, typography, image treatment.
- `IMAGE_ASSET_PLAN.md` — image folder structure, EXIF/privacy rules,
  alt-text style, processing helper.
- `SITE_LINKING_PLAN.md` — relationship to the course-site repos.
- `_site_planning/main_site_status.md` — current state, render notes,
  deployment safety.

These are local planning files (excluded from the render allowlist in
`_quarto.yml`) and should be updated as decisions evolve.

## Design intent

- **Minimal, professional, teaching/research oriented.** Closer to a
  monograph or field notebook than a marketing site, but with a
  stronger landing presence than a bare CV page.
- **Restrained rock / crystal / climbing visual identity.** Stone-toned
  palette in `styles.css`, with one muted iron accent. Do not
  introduce additional accent colors without explicit approval — the
  restraint is the design.
- **Quarto-native first.** Prefer Quarto features (navbar, callouts,
  page layouts, listings) over custom HTML/JS. No JS frameworks. No
  SCSS pipeline — plain CSS only.
- **No heavyweight JS.** No analytics scripts, no third-party widgets,
  no client-side search beyond what Quarto ships by default.

## Pages and navigation

Top-level pages (must stay in sync with the navbar in `_quarto.yml`):

- `index.qmd` — split hero + three category cards + featured course sites
- `about.qmd` — short professional bio
- `teaching.qmd` — current courses, public vs LMS distinction, MAC
- `research.qmd` — interests, projects, publications, talks, collaborators
- `resources.qmd` — software guides, statistics notes, cross-links
- `cv.qmd` — position summary, interests, PDF link
- `contact.qmd` — professional contact only

`projects.qmd` is a redirect stub left in place to preserve the old
URL; its content has been folded into `research.qmd`. Do not revive
`projects.qmd` as a real page without an explicit decision.

## Featured-card and course-site links

The homepage and Teaching page link to course sites under
`matthewhester.com/<course>/`. These subpaths are intentional:

| Link                            | URL                       | Source repo                         |
| ------------------------------- | ------------------------- | ----------------------------------- |
| Intro to Mathematical Software  | `/math-software/`         | `D:/Github/math-software/`          |
| Intro to Statistics             | `/intro-stats/`           | `D:/Github/intro-stats/`            |

Until a combined-deploy pipeline lands (see `SITE_LINKING_PLAN.md`),
these URLs do not resolve in production. Do not silently rewrite
them to existing top-level pages.

## Images

- Raw images stage in `assets/images/raw/` (gitignored).
- Processed, EXIF-stripped images live in:
  - `assets/images/brand/` — portrait, logo, favicon, OG card
  - `assets/images/processed/` — general motifs
  - `assets/images/course-motifs/` — course-specific
- Use `tools/process_images.py` (Pillow) to produce web-sized,
  metadata-free outputs.
- **No location-revealing filenames** in committed assets (raw climbing
  files often include area names; rename on processing).
- **No identifiable third parties** in published images.
- **Every committed image needs alt text** (Quarto `fig-alt=`).

See `IMAGE_ASSET_PLAN.md` for the full policy.

## Styles

- Color tokens, spacing, and component styles live in `styles.css`
  with comments explaining the palette choices. If you add a
  component, add a comment explaining the visual intent too.
- Current components: `.hero` (legacy single-column intro panel),
  `.hero-split` (homepage two-column hero), `.feature-grid`,
  `.feature-card`, `.feature-card.course-card`, navbar/footer
  overrides.
- Do not add SCSS, JS, or webfont `<link>` tags without an explicit
  decision.

## Build, deploy, DNS

- Local render: `quarto render` (writes to `_site/`, gitignored).
- Local preview: `quarto preview`.
- CI: `.github/workflows/publish.yml` is set to
  `on: workflow_dispatch` only. **Do not flip it back to push-to-main
  without explicit instruction.** Phase 4A is a pilot; nothing is
  published yet.
- The `CNAME` file at the repo root must contain exactly
  `matthewhester.com` (no protocol, no trailing slash). Quarto copies
  it into the rendered site; the workflow also copies it explicitly.
- **Do not change DNS.** `matthewhester.com` currently points at a
  Google Site; switching is a separate, deliberate decision.

## Render notes (PowerShell)

`quarto render` writes progress to stderr, which PowerShell flags as
`NativeCommandError`. This is cosmetic — check Quarto's exit code,
not the warning. The `bash` tool is also available if you want to
avoid the warning.

## Editorial conventions (Phase 4C)

- **Cards on the homepage are intentionally text-only.** Do not
  silently re-add boulder/landscape motif images to category cards or
  course cards. The Phase 4B processed motifs remain on disk under
  `assets/images/course-motifs/` for future intentional selection,
  one card at a time. The CSS rules (`.feature-card-with-image`,
  `.feature-card-img`) stay in `styles.css` for that day.
- **"Bayesian Nutrition Observatory" / "BNO" is a private name.** It
  is the internal codename for the long-term nutrition evidence
  project, but it is **not** on the public Research page. The public
  framing is "Bias-robust Bayesian reanalysis of nutrition
  intervention meta-analyses." Do not reintroduce BNO branding on
  public-facing pages without explicit approval; mention it only in
  local planning files.
- **Contact split**: university (`mhester@ualr.edu`) for course/MAC
  matters, Gmail (`matthewahester@gmail.com`) for research/general.
  Do not collapse the two into one bucket. Currently enrolled
  students are routed to Blackboard, not either email.

## Things to avoid

- Adding JavaScript, analytics, or external trackers.
- Adding new top-level pages without updating the navbar.
- Changing the accent color or introducing new ones in `styles.css`
  without explicit approval.
- Inventing publications, talks, affiliations, or course content.
  Placeholders read as placeholders (use `TODO(Phase 4C)` HTML
  comments to flag them).
- Publishing images without stripping EXIF.
- Naming committed images after climbing locations.
- Re-adding card motif images without an explicit per-card decision.
- Reintroducing "BNO" or "Bayesian Nutrition Observatory" on public
  pages.
- Flipping the publish workflow trigger.
- Touching DNS.
