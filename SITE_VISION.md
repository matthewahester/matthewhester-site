# Site vision — matthewhester.com

_Phase 4A vision document. Local planning only; not rendered into `_site/`._
_Last updated: 2026-05-23._

This document defines what matthewhester.com is _for_, who it's for, and the
constraints that should keep it from drifting into either a generic faculty
page or a marketing brochure. It is the durable answer to "should this go
on the site?" — keep edits here when the answer changes.

## 1. Purpose

A small set of overlapping roles, in priority order:

1. **Professional landing page.** A single, durable place to point colleagues,
   collaborators, students, and search committees. The 30-second answer to
   "who is Matt Hester and what does he work on?"
2. **Teaching hub.** Index of current and recent courses, with links out to
   the public course sites that hold the actual material.
3. **Research hub.** Project-level summaries (Bayesian methods, publication
   bias, applied meta-analysis), with paths into preprints, code, talks.
4. **Public resource hub.** Small, durable resources — software guides,
   Quarto/R/LaTeX notes — that are useful beyond a single semester.
5. **Pointer to public course sites.** Subdirectory links to
   `/math-software/`, `/intro-stats/`, and any future public course site.

Explicitly _not_ the site's purpose: hosting student-facing course logistics
(LMS does that), publishing photos for their own sake, or acting as a blog.
A Notes/Blog section may appear later — see §4.

## 2. Audience

In rough order of how much each one shapes the design:

- **Students** finding their way to a public course site or syllabus link.
- **Colleagues and collaborators** (statistics, applied math, ed-research,
  nutrition-and-health methods) looking for project context, code, or a
  current CV.
- **Search committees and administrators** doing a quick scan of teaching
  identity, research interests, and recent work.
- **General readers** who landed via a talk, a preprint, or a citation and
  want to know who the author is.

The site is _not_ optimized for casual social-media traffic, lead generation,
or any "personal brand" funnel.

## 3. Tone

- **Professional** but not corporate; **academic** but not stiff.
- **Mathematically literate** — assume the reader knows what "Bayesian
  meta-analysis" or "publication bias" means; don't over-explain, but
  don't lapse into jargon for its own sake.
- **Approachable** — short sentences, plain English over Latinate
  equivalents, no buzzwords ("synergy", "leverage", "passionate").
- **Visually distinctive but not gimmicky** — the rock/crystal motif (see
  [BRAND_STYLE_BRIEF.md](BRAND_STYLE_BRIEF.md)) is a quiet signature,
  never a theme park.
- **Honest** — placeholders read as placeholders, not as completed work.
  Do not invent publications, talks, or affiliations.

## 4. Site architecture

### Pages (Phase 4A)

| Page         | File           | Purpose                                                           |
| ------------ | -------------- | ----------------------------------------------------------------- |
| Home         | `index.qmd`    | Split hero + three category cards + featured course sites         |
| About        | `about.qmd`    | Short professional bio + brief personal note                      |
| Teaching     | `teaching.qmd` | Current courses, public-site vs LMS distinction, MAC              |
| Research     | `research.qmd` | Interests, projects, publications, talks, collaborators           |
| Resources    | `resources.qmd`| Software guides, Quarto/R/LaTeX notes, cross-links to course sites|
| CV           | `cv.qmd`       | PDF link + position summary + interests                           |
| Contact      | `contact.qmd`  | Professional contact only                                         |

`projects.qmd` (Phase 3) was folded into `research.qmd` as the "Projects"
section. The old page is removed; if cross-references appear, redirect to
`research.qmd`.

### Possible later pages

Add only when there is real content to fill them, never as scaffolding:

- **Notes / Blog** — short technical posts; only worth adding if there
  are at least 3–5 posts in the queue.
- **Talks** — listing of recent presentations with slides/abstracts.
- **Projects** — a more granular project gallery if Research outgrows
  the project section.
- **Students** — current advisees, completed theses, MAC tutor team.

Each one of these is a deliberate decision, not a default.

## 5. Public course links

Two public course sites are scaffolded and Phase 4A links to them as
featured cards on the homepage and from the Teaching page:

- **Intro to Mathematical Software** — `D:/Github/math-software/`,
  configured for `https://matthewhester.com/math-software/`.
- **Intro to Statistics** — `D:/Github/intro-stats/`, configured for
  `https://matthewhester.com/intro-stats/`.

A third, **Applied Statistics I**, may get a public site later but is
currently private (Blackboard only). It will appear on the Teaching page
as a course-without-public-site until that changes.

The pattern is: _public course site exists_ → link out from Home + Teaching;
_no public site yet_ → list on Teaching with a short description and no link.

See [SITE_LINKING_PLAN.md](SITE_LINKING_PLAN.md) for the technical
linking model (subdirectory deploy, shared visual language, back-links).

## 6. Visual system

Anchored in the existing rock/crystal/climbing palette already in
`styles.css`. See [BRAND_STYLE_BRIEF.md](BRAND_STYLE_BRIEF.md) for the
full brief. Quick summary of what Phase 4A adds on top of Phase 3:

- **Stylized portrait** as the homepage identity anchor (right side of
  the split hero, not full-bleed).
- **Stylized boulder/landscape images** as section and course motifs
  (small card images, never decorative wallpaper).
- **Clean Quarto layout** — cosmo base, plain CSS, no SCSS pipeline, no JS.
- **High contrast** for body text on the off-white stone background.
- **Strong typography** — Inter for body, JetBrains Mono for code,
  no decorative display fonts.
- **Restrained animations** — only the existing card-hover micro-motion;
  no scroll-triggered animations, no parallax.
- **No clutter** — every block earns its space.

## 7. Deployment philosophy

- **Build locally first.** `quarto render` from the repo root.
- **Preview in the browser** before considering anything live.
- **Do not touch DNS in Phase 4A.** `matthewhester.com` currently points
  at a Google Site; switching is a separate, deliberate step.
- **Workflow stays on `workflow_dispatch` only.** No push-to-deploy until
  the site is approved for first publication.
- **Choose Pages vs Netlify vs other later.** The current CI is wired for
  GitHub Pages and that is the path of least resistance, but the
  decision is not final.
- **First publish is a checkpoint, not an automatic step.** Switching the
  trigger back to push, configuring DNS, and verifying the CNAME on the
  Pages side are all explicit decisions that the user makes, not the
  assistant.
