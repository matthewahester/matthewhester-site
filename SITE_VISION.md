# Site vision — matthewhester.com

_Vision document, first written 2026-05-23 (Phase 4A). Local planning only;
not rendered into `_site/`._
_Sections 4 to 7 revised 2026-11-13 to match the live site. Sections 1 to 3
are unchanged._

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

### Pages

| Page         | File           | Purpose                                                           |
| ------------ | -------------- | ----------------------------------------------------------------- |
| Home         | `index.qmd`    | Name, portrait, short statement, three section links, featured course sites |
| About        | `about.qmd`    | Short professional bio + brief personal note                      |
| Teaching     | `teaching.qmd` | Current courses, teaching approach, MAC                           |
| Courses      | `courses.qmd`  | The Course Library: every public course record, from `courses.yml` |
| Research     | `research.qmd` | Research strands, the preprint, governed courseware, interests    |
| CV           | `cv.qmd`       | Position summary, interests, selected work, talks, identifiers    |
| Contact      | `contact.qmd`  | Professional contact only                                         |

The navbar carries the six pages after Home; the site name is the home
link. `404.qmd` is served for any missing address and is not in the navbar.

`projects.qmd` (Phase 3) was folded into `research.qmd`, and
`teaching-graduate.qmd` into the Course Library. Both remain as redirect
stubs so the old URLs keep working.

A Resources page was planned in Phase 4A and was not built. Software guides
and notes live on the course sites.

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

The course sites are separate repos, served under this domain at
`/<course>/`. The Course Library (`courses.qmd`, rendered from
`courses.yml`) is the one inventory of them. The homepage and the Teaching
page feature the current courses as poster cards.

The pattern is: _public course site exists_ → a linked record in the
Library; _no public site yet_ → an unlinked record that says so in words.
Status describes the public materials, not whether a course exists.

See [TEACHING_PORTFOLIO_ARCHITECTURE.md](TEACHING_PORTFOLIO_ARCHITECTURE.md)
for the approved rules and [README.md](README.md) for how the sites are
built into one deployment.

## 6. Visual system

Anchored in the rock/crystal/climbing identity, set sharp and simple since
2026-11-13. See [BRAND_STYLE_BRIEF.md](BRAND_STYLE_BRIEF.md) for the full
brief and its five rules. In short:

- **One column, one paper tone, one accent.** A white page, every hub page
  in the same 800 px column, iron for links.
- **Stylized portrait** as the homepage identity anchor, beside the name,
  set on the page with no card and not full-bleed.
- **Course posters and course marks** as the site's imagery. The boulder
  and landscape motifs are not in use.
- **Clean Quarto layout** — cosmo base, plain CSS, no SCSS pipeline, no JS.
- **High contrast** for body text on the white page.
- **Strong typography** — Inter for body, JetBrains Mono for code,
  no decorative display fonts.
- **No motion** — no hover lift, no scroll-triggered animations, no
  parallax.
- **No clutter** — every block earns its space, and a page does not
  explain how to read itself.

## 7. Deployment philosophy

- **Build locally first.** `quarto render` from the repo root. A local
  render covers the hub only; each course site renders from its own repo.
- **Preview in the browser** before considering anything live.
- **The site is live on GitHub Pages** at the custom domain, since the
  May 2026 launch. DNS points there. Do not touch DNS without a separate,
  deliberate decision.
- **Workflow stays on `workflow_dispatch` only.** No push-to-deploy.
- **A deploy is a checkpoint, not an automatic step.** Dispatching the
  workflow, switching its trigger, and any DNS or CNAME change are
  explicit decisions that the user makes, not the assistant.
- **Check the live site after a deploy.** The workflow installs the newest
  Quarto, which can be newer than the local one, so the live pages are the
  test.
