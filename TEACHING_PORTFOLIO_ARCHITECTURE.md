# Teaching Portfolio Architecture

Status: approved
Owner: Matthew Hester
Scope: matthewhester.com teaching portfolio, Course Library, and course records

_Approved control document. Local planning only; not rendered into `_site/`._
_Saved: 2026-07-26. Revised: 2026-07-26 (unified Course Library model)._

## 1. Purpose

The public teaching site has three related but distinct purposes:

1. present Matt's current teaching;
2. provide durable public course resources;
3. help visitors understand how the courses relate to one another.

It is not a replacement for Blackboard or another LMS. Operational,
student-specific, graded, or section-specific information remains outside the
public site.

## 2. Information architecture

The portfolio has exactly two teaching destinations. They do different jobs
and must not drift into being two catalogs of the same thing.

### Teaching

The Teaching page is the personal teaching overview and curated showcase. It
carries the teaching introduction, the current courses, a showcase of course
work worth seeing first, the Course Builder, teaching approach, and Math
Assistance Center sections, and a clear link to the Course Library.

Teaching answers "who is this person as a teacher, and what are they teaching
now." It is allowed to be selective. It is not required to list everything.

### Course Library

The Course Library is the canonical inventory of all public course materials.
It holds undergraduate and graduate records together in one place, ordered by
curriculum grouping rather than split by level.

The Library answers "what exists, and what state is it in." It is required to
be complete. Every course record the site publishes lives here.

Do not maintain a separate undergraduate landing page and a separate graduate
landing page. Level is a property of a record, not a destination.

### Course Library display invariants

The Library is a catalog, not an administrative inventory. These hold whatever
the record count is:

1. **One page, both levels.** Undergraduate and graduate materials live on the
   same page.
2. **Structure before filtering.** The default presentation communicates
   curriculum structure. A visitor who never touches a control still sees an
   organized collection, not one flat alphabetical list.
3. **Sections, not destinations.** Undergraduate and graduate collections are
   visible as sections of that page.
4. **Two treatments, one registry.** Published course sites and non-published
   curriculum records share the registry but not their visual treatment.
5. **Discovery without dominance.** Search and filtering are available without
   taking over the page. The opening viewport, at any width, belongs to the
   catalog rather than to a filter matrix.
6. **Curated order.** Sequence is an editorial decision recorded in the
   registry. It is never alphabetical by accident and never delegated to a
   visitor-facing sort menu.
7. **Controls that survive growth.** Sidebars and filter controls must still
   be useful at 25 to 30 courses. A control whose size grows with the course
   count is a defect.

Curriculum directions are never interleaved among published course sites in
the default presentation.

### Navigation

The complete inventory is reachable through a site-wide `Courses` navigation
item, from anywhere on the site, not only through the Teaching sidebar.

Sidebars navigate major pages and sections. They must not enumerate every
individual course. A sidebar that grows with the course count is a defect: the
portfolio is expected to reach roughly 25 to 30 records, and the navigation
must not grow with it.

## 3. Visual system

All course presentation belongs to the same stone-and-crystal visual family.

Full course heroes remain appropriate for:

- individual public course sites;
- current courses;
- selected showcase entries on the Teaching page.

The complete Library uses compact, single-column course records. It must stay
readable and scannable at roughly 25 to 30 entries, which full heroes cannot
do. The Library gets more horizontal room than the prose column so records do
not sit in a narrow strip beside unused whitespace.

Two record treatments, driven by kind:

- **A published course site** is a media row: a legible hero thumbnail, the
  title and optional code, one line of level, grouping, and status, one
  sentence of summary, and an unambiguous link. Thumbnails stay compact at
  narrow widths rather than expanding into full heroes, which would triple the
  page height for no gain.
- **A course without public materials, and a curriculum direction**, are
  text-only rows. No reserved blank image area, no hover or link affordance,
  no focusable wrapper, a concise description, and a clear material status.

Library summaries are concise catalog descriptions. They may only restate
claims already in the registry; the Library is not where curriculum content
gets written.

Retain throughout:

- single-column course presentation, never a dense multi-column card grid;
- generous spacing and the existing typography;
- the crystal or mineral-centered visual grammar where artwork appears;
- accessible, descriptive alternative text;
- overall site restraint.

Placeholder records get a restrained text treatment. A placeholder must never
look like a published course site or an announced offering, and must carry no
hover or link affordance, because there is nothing to click.

Do not reuse an unrelated existing hero as a placeholder. Do not generate
graduate hero artwork during architecture work; heroes and course content are
developed separately through the curriculum agent.

## 4. Course records

Every record has a *kind* and a *status*. The two are independent and both
must be truthful.

### Record kind

- **Course site** — a public course-material site exists at a real URL. The
  record links to it.
- **Course** — a real course that exists in the catalog, whose public
  materials do not exist or are still being assembled. The record does not
  link anywhere.
- **Curriculum direction** — a planning-stage area of the curriculum. Not a
  scheduled course, not an adopted requirement, not an in-development course
  site. The record does not link anywhere.

Only a Course site record may be clickable.

### Public-material status

Status describes the public materials, not the course's existence:

- **Current offering** — tied to a presently scheduled section. May show the
  academic term and last substantive review date.
- **Maintained public reference** — a durable resource collection not
  currently representing a scheduled section. May show a review date.
- **In development** — materials are still being assembled. Must carry a clear
  statement that dates, policies, assessments, and materials remain
  provisional.
- **No public materials yet** — the course is real, but nothing public exists.
- **Curriculum direction** — the record describes direction only.
- **Archived resource** — preserved but no longer maintained. Shows the last
  maintained date when known, and a warning that links, software instructions,
  or policies may be outdated.

Status must be communicated in text, not by color alone.

Exact meetings, rooms, assignment dates, grades, and announcements remain in
Blackboard or the authoritative university system.

## 5. Freshness and dates

Prefer the label "Last substantively reviewed".

Do not use a generic file-modification date as though it represented a
complete content review. Do not invent review dates. Where review dates have
not been curated, show the truthful status without a date.

Individual pages need separate review dates only when their accuracy is
especially time-sensitive: software installation instructions, package or
platform guidance, external resource collections, AI-use guidance, policy
links. Stable mathematical exposition does not require a conspicuous date.

## 6. Metadata

There is one authoritative course registry. Title, code, level, kind, status,
curriculum grouping, summary, public URL, hero or thumbnail, and review date
live there and nowhere else.

Pages read the registry. They do not restate its contents. If a course's
title, status, summary, or URL appears in two files, that is a defect.

The registry is a lightweight YAML file consumed by Quarto's native listing
facility. Do not introduce a build step, a client-side framework, or a new
dependency to read it.

Display order is part of the metadata. Each record carries a unique positive
integer `order`, and that field alone decides sequence. Leave gaps between
values so a course can be inserted without renumbering.

The registry's invariants are enforced, not merely documented. A validator
runs as a pre-render step and fails the render before publication on: a
missing, non-integer, non-positive, or duplicated `order`; an out-of-enum
level, kind, or status; a `categories` list that does not exactly equal
`[level, status, group]`; a duplicate title or public path; a `site` record
with no path; a non-site record exposing a public course path; a kind/status
pair that cannot both be true; or a malformed image path or review date.

Unknown values are omitted, never invented. A missing code, URL, prerequisite,
date, or review date is simply absent from the record.

Generated counts are acceptable. Avoid brittle prose such as an exact
hard-coded number of course sites.

Two hand-written presentation exceptions remain, both predating the registry:
the undergraduate hero collection on the Teaching page, and the two featured
course cards on the home page. Both restate titles, course URLs, and
thumbnails. They are grandfathered, not licensed: no new page may restate
registry facts, and migrating these two to registry-driven rendering is a
later tranche rather than a reason to redesign either page.

No graduate course fact may live outside the registry.

## 7. Graduate seeding

The graduate portion of the Library is seeded only from what the existing
governing materials already support. Do not invent the eventual graduate
curriculum to fill the page, and do not manufacture the remaining courses the
curriculum may eventually contain.

### Mathematical Statistics I

- Course: Mathematical Statistics I
- Code: MATH 75063
- Subtitle: Probability, Likelihood, and Estimation
- Level: Graduate
- Kind: Course
- Status: In development

The public site must keep three things distinct.

First, the sequence itself exists. Mathematical Statistics I is the first
course in the existing graduate mathematical-statistics sequence and the
common theoretical foundation for the graduate curriculum around it.
Mathematical Statistics II is the second course in that sequence. Both are
established catalog courses and may be described as such.

Second, the public materials do not yet exist. What is in development is the
public course-material collection for MATH 75063, not the course. The status
label therefore stays In development, and the treatment must say plainly that
dates, policies, assessments, and readings remain provisional.

Third, the broader curriculum is direction rather than adopted curriculum.
Later work in regression and generalized linear models, computational
statistics, Bayesian modeling, and causal inference rests on the estimation
and likelihood theory this course builds. Those are planning-stage rebuilds
and proposed pilots. Present them as curriculum direction only, and do not
imply that they are scheduled offerings, that they have been adopted, or that
Matt is assigned to teach them.

It must not be presented as a current offering until the term, section,
meeting, calendar, and release decisions are actually settled.

### Mathematical Statistics II

May be identified as the established second catalog course in the sequence. It
must not appear to have public materials while none exist: kind Course, status
No public materials yet, no link.

### Curriculum directions

Regression and generalized linear models, computational statistics, Bayesian
modeling, and causal inference may appear as curriculum-direction records
only. They are not scheduled courses, adopted requirements, or in-development
course sites.

## 8. Public/private boundary

The public site may contain stable notes, reading and curriculum maps, open
computational notebooks, non-sensitive demonstrations, and durable course
descriptions and public references.

The public site must not expose rosters or student information, grades or
submissions, private announcements, answer keys, protected assessment
materials, section-specific material that belongs in Blackboard, or
provisional operational details presented as final.

## 9. Design boundaries

This work remains professional, simple, and Quarto-friendly.

Do not introduce a site-wide redesign, heavy JavaScript, a client-side
application framework, flashy animation, a dense dashboard treatment,
unnecessary new dependencies, or broken links to course sites that do not yet
exist.

Use Quarto's existing listing, search, and filter facilities before writing
anything custom. Filter and search controls must be keyboard reachable and
labeled.

The navbar stays concise. `Courses` earns a top-level slot because it is the
canonical inventory; further teaching destinations do not.

## 10. Compatibility routes

Published URLs are promises. When a page's role changes, its old URL keeps
working.

`teaching-graduate.html` was the separate graduate destination. It remains a
valid public URL and resolves into the graduate portion of the Course Library.
It must not survive as a competing second catalog.

The ten existing public course-site URLs are fixed. Do not rename or retarget
them.

## 11. Tranches

Architecture is established before content is filled in.

Completed:

1. a dedicated graduate page, the four-state status model, and the first
   honest In development record;
2. the unified Course Library: registry, canonical inventory page, site-wide
   `Courses` navigation, reduced sidebar, and the graduate compatibility
   route.

Deferred, in no fixed order:

- choosing which courses become the smaller featured selection on Teaching;
- migrating the Teaching hero presentation to registry-driven rendering;
- graduate course content, syllabi, and hero artwork, through the curriculum
  agent;
- curated substantive-review dates;
- the remaining graduate records, as the curriculum is actually decided.
