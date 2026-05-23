# Site linking plan — matthewhester.com + course sites

_Phase 4A. Local planning only; not rendered into `_site/`._
_Last updated: 2026-05-23._

This plan defines how `matthewhester.com` (the main hub) relates to
the public course sites at `matthewhester.com/math-software/` and
`matthewhester.com/intro-stats/`.

## 1. The three sites involved

| Role          | Repo                              | Eventual URL                                | Status                |
| ------------- | --------------------------------- | ------------------------------------------- | --------------------- |
| Main hub      | `D:/Github/matthewhester-site/`   | `https://matthewhester.com/`                | Scaffolded; not live  |
| Math Software | `D:/Github/math-software/`        | `https://matthewhester.com/math-software/`  | Scaffolded; not live  |
| Intro Stats   | `D:/Github/intro-stats/`          | `https://matthewhester.com/intro-stats/`    | Scaffolded; not live  |

Each of the three is a **standalone Quarto site** with its own
`_quarto.yml`, content tree, and styles. None of them currently
deploys to a live URL; the path-prefix mapping is encoded only in
each site's `site-url` field.

## 2. Recommended model: hub + standalone course sites

The hub at `/` is the entry point. The course sites are siblings that
deploy under subdirectories. Operationally:

- **Three independent repos**, three independent deploys.
- The main site is the only thing served from `/`.
- Course sites are served from `/math-software/` and `/intro-stats/`.
- Each site has its own visual language that is **visibly related** to
  the hub but not literally shared.

This avoids the operational pain of stitching three Quarto projects into
a single render while keeping URLs clean for students.

### Alternatives considered

- **Monorepo Quarto project** — one giant `_quarto.yml` that renders
  everything. Cleaner cross-references, much messier ownership and
  navigation. Rejected for Phase 4A; revisit if cross-site search
  becomes a real need.
- **External hosting per course** (each on its own GH Pages repo at its
  own domain or default Pages URL). Works fine but pushes the URLs out
  of `matthewhester.com/...` and weakens the hub identity. Rejected.

## 3. Deployment mechanism

Each course-site repo deploys its `_site/` into a subdirectory of the
main site's deploy. There are two viable ways to do this:

1. **Per-repo Pages deploys with path mapping** — each repo deploys to
   its own GH Pages, served at the same custom domain via path-based
   routing. This requires either (a) per-subpath Pages support, which
   GitHub does not natively provide, or (b) a thin reverse-proxy /
   Cloudflare worker in front. Complex.

2. **Main site pulls course sites at build** — the main site's
   workflow runs `quarto render` on the hub, then checks out each
   course repo, renders it, and copies the result into
   `_site/math-software/` and `_site/intro-stats/`. The published
   artifact is one combined `_site/` tree. Simpler, more deterministic,
   and keeps a single Pages deploy.

**Phase 4A recommendation: option 2.** It is not implemented yet
(workflow is still single-repo render only); the implementation is a
Phase 4B/5 task. Until then, course sites are previewed locally only.

The hub-side workflow would look like:

```yaml
# Pseudo-pattern, not committed yet
- uses: actions/checkout@v4
  with:
    repository: matthewahester/math-software
    path: course-math-software
- run: quarto render course-math-software --output-dir ../_site/math-software
```

## 4. Cross-links

### Hub → course sites
- Homepage: featured-course-site cards link to `/math-software/` and
  `/intro-stats/` with their site icons / motifs.
- Teaching page: course list links to the same URLs, plus short
  course descriptions.
- Resources page: optionally link to specific resource pages within
  course sites (e.g. `/math-software/resources/software-setup`).

### Course sites → hub
- Each course site's navbar or footer should include a "← Matt Hester"
  link back to `https://matthewhester.com/`.
- Each course site's `index.qmd` opening paragraph already credits
  "Matt Hester" with a link — keep that link pointed at the hub.

### Course site ↔ course site
- Not linked directly. Students enter through the hub or via a direct
  course URL given in the syllabus.

## 5. Visual relationship

- **Shared palette tokens.** The rock/crystal palette in the hub's
  `styles.css` should be mirrored in each course site's `styles.css`
  (already partially true). The simplest path is to copy the `:root`
  block; a future option is to extract a small shared `palette.css`
  that all three repos symlink or vendor.
- **Distinct course motif images** keep each site visually anchored
  to its course while still feeling like part of the same family.
- **Identical typography + footer style** across all three sites.
- **No shared JS, no shared build pipeline** — keep each repo
  independently buildable.

## 6. What to add to course sites (later passes, not now)

After the hub is content-complete:

- Add a "← Matt Hester · matthewhester.com" link to the footer of
  each course site's `_quarto.yml`.
- Audit each course site's `styles.css` against the hub's palette
  tokens and align where they have drifted.
- Add an OG card per course site once the hub OG card exists, using
  the same visual template.

## 7. What should not be linked publicly yet

- **Private syllabi** in `D:/My Drive School/Teaching/courses/.../`
  stay private. Public course-site syllabi are sanitized versions.
- **Blackboard / LMS pages** are never linked from the public site.
- **Grades, rosters, accommodations, student submissions** are
  never published.
- **Applied Statistics I (`stat_35203_applied_statistics`)** has no
  public site yet. Listed on the Teaching page as a course-without-
  public-site; no outbound link until a public site exists and is
  approved for release.
- **DNS** is not switched in Phase 4A. The cross-domain story is
  vacuously fine because nothing is live yet.
