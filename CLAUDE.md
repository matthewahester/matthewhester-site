# CLAUDE.md — matthewhester.com

Notes for Claude Code (or any AI assistant) working in this repo. Keep
these in mind alongside the user's explicit instructions.

## What this repo is

A small Quarto website, live at
[matthewhester.com](https://matthewhester.com) on GitHub Pages. It is the
professional hub for Matt Hester (UA Little Rock): a landing page, a
teaching overview, the Course Library, a research summary, a short CV, and
a contact page.

The hub is also the umbrella for the public course sites. Each course site
lives in its own repo, checked out beside this one (`D:/Github/<course>/`),
and is served at `matthewhester.com/<course>/`. One manual workflow in this
repo renders the hub and every course repo and deploys them as a single
site. See "Build, deploy, DNS" below.

## Read these first

When starting work in this repo, skim:

- `SITE_VISION.md` — purpose, audience, tone, architecture.
- `BRAND_STYLE_BRIEF.md` — the rules of the look, palette, typography,
  image treatment.
- `IMAGE_ASSET_PLAN.md` — image folder structure, EXIF/privacy rules,
  alt-text style, processing helper.
- `TEACHING_PORTFOLIO_ARCHITECTURE.md` — approved control for the
  teaching pages: information architecture, the course status model,
  freshness/date rules, metadata, and the public/private boundary.
  Governs any teaching-page change.
- The header comment of `styles.css` — the design rules the stylesheet
  follows.

These are local planning files (excluded from the render list in
`_quarto.yml`) and should be updated as decisions evolve.

`SITE_LINKING_PLAN.md` and the notes under `_site_planning/` date from the
May 2026 launch. Read them as history, not as current state. `README.md`
describes the deployment as it runs now.

## Design intent

- **Minimal, professional, teaching/research oriented.** Closer to a
  monograph or field notebook than a marketing site, but with a
  stronger landing presence than a bare CV page.
- **Sharp and simple** (Matt, 2026-11-13). A white page, near-black ink,
  a black top bar, stone greys for rules and muted text, and one accent,
  iron. Edges are square and nothing has a shadow. A block is marked by a
  rule above it, not by a box. Every hub page sits in one 800 px column,
  and the navbar and footer share its edges. `BRAND_STYLE_BRIEF.md` gives
  the reasoning and the header of `styles.css` states the rules.
- **Restrained rock / crystal / climbing visual identity.** The portrait
  and the course artwork carry the color; the page around them stays
  plain. Do not introduce additional accent colors without explicit
  approval — the restraint is the design. A shadow, a rounded card, a
  tinted page, a second accent, or a sidebar would each change the look,
  so ask before adding one.
- **Quarto-native first.** Prefer Quarto features (navbar, callouts,
  page layouts, listings) over custom HTML/JS. No JS frameworks. No
  SCSS pipeline — plain CSS only.
- **No heavyweight JS.** No analytics scripts, no third-party widgets,
  no client-side search beyond what Quarto ships by default.

## Pages and navigation

Top-level pages (must stay in sync with the navbar in `_quarto.yml`):

- `index.qmd` — name and tagline in the title block, the portrait beside
  them, a short statement, three section links, featured course sites
- `about.qmd` — short professional bio
- `teaching.qmd` — teaching overview: current courses, teaching approach,
  MAC. **Not** a course directory
- `courses.qmd` — the Course Library, the canonical inventory of every
  public course record, plus the governed courseware note ("How these
  materials are built"). A standalone page in the same column as every
  other page, no sidebar. Renders `courses.yml` through Quarto's listing
  and `_listings/course-record.ejs`
- `research.qmd` — three research strands, the preprint, governed
  courseware, research interests
- `cv.qmd` — position summary, interests, selected work, talks,
  identifiers
- `contact.qmd` — professional contact only
- `404.qmd` — the page GitHub Pages serves for any missing address on the
  domain, course paths included. Not in the navbar, not in the site search

The navbar carries six items: About, Teaching, Courses, Research, CV,
Contact. The site name at the left of the bar is the home link, so there
is no "Home" item. `BRAND_STYLE_BRIEF.md` sets seven as the absolute
ceiling. `Courses` earns its slot because the Library is the canonical
inventory and must be reachable from anywhere. **Do not go past seven
items**, and do not add further teaching destinations —
`TEACHING_PORTFOLIO_ARCHITECTURE.md` sections 2 and 9.

`teaching-graduate.qmd` is a redirect stub. It was the separate graduate
page before the unified Course Library; section 10 of the architecture
control keeps the URL working and forbids it becoming a second catalog.
It redirects to `courses.html#category=Graduate` — Quarto's listing
deep-link hash, read by `quarto-listing.js` on load. Do not give it
course records of its own.

**One authoritative course source.** Course titles, codes, levels,
statuses, groupings, summaries, URLs, course marks, and **display order**
live in `courses.yml`. `tools/validate_courses.py` runs as a Quarto
pre-render step and fails the render on a registry violation, including a
course mark whose 2x or 3x file is missing.

The Library is a curriculum catalog, not an alphabetical inventory:
`courses.qmd` has no sort control, and sequence comes only from each
record's unique `order` integer. `_listings/course-record.ejs` groups
records into sections by level and kind. Leave gaps between `order`
values so a course can be inserted without renumbering.

Two hand-written **presentation** exceptions still restate registry
facts, both predating the registry and both scheduled for a later
migration tranche — do not add a third:

- `teaching.qmd` — the two current-course hero cards: 2 titles, 2 URLs,
  2 poster thumbnails, and re-worded summaries. The undergraduate hero
  collection that used to sit below them was deleted when Teaching and
  Courses were separated; the full collection lives only in the Library.
- `index.qmd` — the two featured course cards: 2 titles, 2 URLs, 2
  poster thumbnails.

`README.md` and this file also name course URLs, but as deployment and
repo-layout documentation rather than course presentation. No **graduate**
course fact appears outside `courses.yml`; every graduate record is
registry-driven.

**Teaching and Courses are separate surfaces.** No hub page has a
sidebar. Teaching had one until 2026-11-13, four anchors to its own
sections; it was removed so that every page shares one column.
`TEACHING_PORTFOLIO_ARCHITECTURE.md` section 2 still describes that
sidebar, and its rule stands if one ever returns: every entry is an
anchor to a section that actually lives on that page — never another
destination, never individual courses. The full course collection appears
only in the Library, and governed courseware (Course Builder in the
control document) has exactly one home, on `courses.qmd`. Do not re-add a
course directory or a governed courseware section to Teaching.

**The public name is governed courseware** (Matt, 2026-11-13: "governed
courseware is good"). "Course Builder" named the first version of the
system and is no longer on any page. The pages describe the system
instead of naming it: a human-governed course-authoring harness.
`research.html#course-builder` and `courses.html#course-builder` were the
two sections' addresses. Both are now `#governed-courseware`, and an empty
span in each heading keeps the old address working; leave the spans there.
The `.course-builder-note` class on the `courses.qmd` heading is a CSS
hook and keeps its name.

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

They resolve on the live site, because the publish workflow builds each
course repo into its subpath. They do not resolve in a local hub render,
which covers the hub only. Do not rewrite them to hub pages.

## Images

- Raw images stage in `assets/images/raw/` (gitignored).
- Processed, EXIF-stripped images live in:
  - `assets/images/brand/` — portrait, favicon, OG card
  - `assets/images/about/` — the About page image
  - `assets/images/processed/` — general motifs (none in use)
  - `assets/images/course-motifs/` — the course posters (`*-hero.png`),
    their web thumbnails (`thumbs/`), the course marks the Library shows
    (`marks/`), and the masters of five marks (`icons/`)
- Helpers in `tools/`, all Pillow:
  - `process_images.py` — general web-sized, metadata-free outputs
  - `make_portrait.py` — the homepage portrait on a pure white ground
  - `make_favicon.py` — the favicon
  - `make_hero_thumbs.py` — poster thumbnails for the home and Teaching
    cards
  - `make_course_icon.py` and `make_navbar_logo.py` — a course mark cut
    from its poster, and the 128 px copy a course site's navbar shows
  - `make_library_marks.py` — the Library's marks, sized alike and
    written at 80, 160 and 240 px
- **No location-revealing filenames** in committed assets (raw climbing
  files often include area names; rename on processing).
- **No identifiable third parties** in published images.
- **Every committed image needs alt text** (Quarto `fig-alt=`). The one
  exception in use is a decorative image beside text that already names
  it, such as a Library course mark, which carries `alt=""`.

See `IMAGE_ASSET_PLAN.md` for the full policy.

## Styles

- Color tokens, spacing, and component styles live in `styles.css`
  with comments explaining the palette choices. If you add a
  component, add a comment explaining the visual intent too.
- Three rules hold across the file: one accent (iron), one paper tone
  (white), one column (800 px, shared by the navbar and footer).
- Current components, in file order: navbar, the one-column page frame,
  title block, `.hero-split` (homepage hero), `.feature-grid` and
  `.feature-card` (homepage section links), `.course-hero-card` (poster
  cards), course status labels, the Course Library (sections, records,
  browse controls, listing controls), the About split, the research
  highlight, footer. `.hero` and `.feature-card-with-image` are unused
  hooks kept from earlier versions.
- Do not add SCSS, JS, or webfont `<link>` tags without an explicit
  decision.

## Build, deploy, DNS

- Local render: `quarto render` (writes to `_site/`, gitignored). It
  covers the hub only.
- Local preview: `quarto preview`.
- Deploy: `.github/workflows/publish.yml`, set to
  `on: workflow_dispatch` only. One run validates `courses.yml`, renders
  the hub and every course repo it checks out, assembles one Pages
  artifact, and deploys it. **Do not flip it to push-to-main without
  explicit instruction.** Dispatching it publishes the site, so it needs
  Matt's explicit word each time.
- The workflow installs the newest Quarto with no version pin, so the
  live build can be newer than a local one. After a deploy, check the
  live pages themselves, not only the files that changed.
- The `CNAME` file at the repo root must contain exactly
  `matthewhester.com` (no protocol, no trailing slash). Quarto copies
  it into the rendered site; the workflow also copies it explicitly.
- **Do not change DNS.** `matthewhester.com` points at GitHub Pages. Any
  DNS change is a separate, deliberate decision.

## Render notes (PowerShell)

`quarto render` writes progress to stderr, which PowerShell flags as
`NativeCommandError`. This is cosmetic — check Quarto's exit code,
not the warning. The `bash` tool is also available if you want to
avoid the warning.

## Editorial conventions (Phase 4C)

- **The section links on the homepage are intentionally text-only.** Do
  not silently re-add boulder/landscape motif images to them or to the
  course cards. The CSS rules (`.feature-card-with-image`,
  `.feature-card-img`) stay in `styles.css` for an intentional, per-card
  decision.
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
- Reintroducing shadows, rounded cards, a tinted page, or a sidebar
  without explicit approval.
- Inventing publications, talks, affiliations, or course content.
  Placeholders read as placeholders (use `TODO(Phase 4C)` HTML
  comments to flag them).
- Publishing images without stripping EXIF.
- Naming committed images after climbing locations.
- Re-adding card motif images without an explicit per-card decision.
- Reintroducing "BNO" or "Bayesian Nutrition Observatory" on public
  pages.
- Flipping the publish workflow trigger, or dispatching a deploy without
  Matt's word.
- Touching DNS.
