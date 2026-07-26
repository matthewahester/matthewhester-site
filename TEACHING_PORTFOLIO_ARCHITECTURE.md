# Teaching Portfolio Architecture

Status: approved
Owner: Matthew Hester
Scope: matthewhester.com teaching portfolio and course-collection pages

_Approved control document. Local planning only; not rendered into `_site/`._
_Saved: 2026-07-26._

## 1. Purpose

The public teaching site has three related but distinct purposes:

1. present Matt's current teaching;
2. provide durable public course resources;
3. help visitors understand how the courses relate to one another.

It is not a replacement for Blackboard or another LMS. Operational,
student-specific, graded, or section-specific information remains outside the
public site.

## 2. Information architecture

### Teaching overview

The main Teaching page remains the public overview.

It should contain:

- the teaching introduction;
- current courses, regardless of undergraduate or graduate level;
- a compact way to browse the public course collections;
- the existing undergraduate course presentation for now;
- a link and short introduction to the graduate collection;
- the Course Builder, teaching approach, and Math Assistance Center sections.

Do not create a separate undergraduate landing page in this tranche.

The existing undergraduate arrangement should not be broadly redesigned merely
for symmetry with the graduate collection.

### Graduate collection

Graduate courses receive a dedicated collection page within the same teaching
ecosystem.

The page should:

- explain the purpose and status of the graduate collection;
- provide a restrained curriculum or sequence view;
- use a single-column course presentation;
- distinguish real course sites from planned or developing courses;
- link back clearly to the Teaching overview.

A course should receive a full course entry or hero only when a public course
site exists or the course is in substantial development.

Planned courses may appear in a compact curriculum map, but they must not look
like published or currently offered courses.

Current graduate courses may also appear in the Current courses section of the
Teaching overview.

## 3. Visual system

Graduate courses belong to the same visual family as the undergraduate courses.

Retain:

- full-width, single-column course entries;
- the established hero proportions;
- generous spacing;
- the crystal or mineral-centered visual grammar;
- course-specific mathematical panels;
- accessible, descriptive alternative text;
- the existing typography and overall site restraint.

Do not convert the course collection into a dense multi-column card grid.

Graduate heroes should use a somewhat more formal mathematical register, but
they should not become uniformly dark, grey, intimidating, or visually separate
from the undergraduate collection.

Do not reuse an unrelated existing hero as a placeholder.

Do not generate the final Mathematical Statistics I hero during the initial
architecture tranche unless Matt separately approves that visual work.

## 4. Course status model

The public portfolio recognizes four course states:

### Current offering

A course tied to a presently scheduled section.

Display, where useful:

- Current offering
- academic term
- last substantive review date

Exact meetings, rooms, assignment dates, grades, announcements, and other
operational information remain in Blackboard or the authoritative university
system.

### Maintained public reference

A durable resource collection that is not currently representing a scheduled
section.

Display:

- Maintained public reference
- last substantive review date, when known

### In development

A course whose structure or materials are still being assembled.

Display:

- In development
- a clear statement that dates, policies, assessments, and materials may remain
  provisional

### Archived resource

A preserved course resource that is no longer actively maintained.

Display:

- Archived resource
- the last maintained or reviewed date, when known
- a warning that links, software instructions, or policies may be outdated

Status must be communicated in text, not by color alone.

## 5. Freshness and dates

Prefer the label:

> Last substantively reviewed

Do not use a generic file-modification date as though it represented a complete
content review.

Do not invent review dates.

Where review dates have not yet been curated, the site may show the truthful
course status without displaying a date.

Individual pages need separate review dates only when their accuracy is
especially time-sensitive, such as:

- software installation instructions;
- package or platform guidance;
- external resource collections;
- AI-use guidance;
- policy links.

Stable mathematical exposition does not require a conspicuous date on every
page.

## 6. Metadata

Course title, level, status, subtitle, review date, current term, hero path,
summary, and public URL should eventually have one authoritative metadata
source.

Prefer a lightweight YAML or equivalent registry compatible with the existing
Quarto structure.

Do not force a large rewrite of the current Teaching page solely to introduce
the registry. A staged migration is acceptable, but newly introduced graduate
metadata should not be duplicated across several files without necessity.

Generated counts are acceptable. Otherwise, avoid brittle prose such as an
exact hard-coded number of course sites.

## 7. Mathematical Statistics I

Initial public metadata:

- Course: Mathematical Statistics I
- Code: MATH 75063
- Subtitle: Probability, Likelihood, and Estimation
- Level: Graduate
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

It must not be presented as a current offering until the term, section, meeting,
calendar, and release decisions are actually settled.

Until a public course site exists, its graduate-page treatment should not
contain a broken or misleading course-site link.

## 8. Public/private boundary

The public site may contain:

- stable notes;
- reading and curriculum maps;
- open computational notebooks;
- non-sensitive demonstrations;
- durable course descriptions and public references.

The public site must not expose:

- rosters or student information;
- grades or submissions;
- private announcements;
- answer keys;
- protected assessment materials;
- section-specific material that belongs in Blackboard;
- provisional operational details presented as final.

## 9. Design boundaries

This work should remain professional, simple, and Quarto-friendly.

Do not introduce:

- a site-wide redesign;
- heavy JavaScript;
- flashy animation;
- a larger top-level navbar merely to expose the graduate page;
- an unrelated Resources page;
- a dense dashboard treatment;
- unnecessary new dependencies;
- broken links to course sites that do not yet exist.

## 10. Initial implementation tranche

The first tranche should establish the architecture rather than complete the
graduate portfolio.

It should:

1. add a dedicated Graduate Course Sites page;
2. link it naturally from the Teaching overview without expanding the main
   navbar unnecessarily;
3. replace the brittle exact portfolio count with durable wording or generated
   metadata;
4. replace the one-line graduate placeholder with a useful introduction and
   link;
5. present Mathematical Statistics I honestly as In development;
6. include a restrained initial curriculum-pathway treatment;
7. preserve the current undergraduate hero layout;
8. establish the beginning of the status and metadata model;
9. render and verify the site at desktop and narrow widths;
10. avoid publishing until Matt has reviewed the rendered first pass.
