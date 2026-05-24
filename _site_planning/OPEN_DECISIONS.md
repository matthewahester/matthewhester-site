# Open decisions — matthewhester.com

_Decisions still needing a human call. Resolved items are listed at
the bottom for audit trail. Local planning only; not rendered into
`_site/`. Last updated: 2026-05-24 (end of Phase 5F)._

---

## Still open

### 1. Which boulder/landscape images, if any, represent each card?

**Choices**

- **A.** Keep all cards text-only (current state).
- **B.** Add one motif per card, picked intentionally one at a time
  in conversation; the processed motif files from Phase 4B are reused
  or replaced as needed.
- **C.** Use motifs only on the two featured-course cards, leaving the
  three category cards text-only.
- **D.** Use motifs only on the three category cards, leaving the
  featured-course cards to course-site visual identity.

**Current state (Phase 5F):** A. All cards text-only. Phase 4B
processed files (`motif-teaching-600.webp`, `motif-research-600.webp`,
`motif-resources-600.webp`, `course-math-software-600.webp`,
`course-intro-stats-600.webp`) remain on disk, unreferenced.

**Trade-offs:**
- A is honest about the fact that the image picks have not been
  curated.
- B/C/D require eyeballing each image and confirming it suits its
  slot. The Phase 4B picks were filename-based guesses.

**Privacy note:** none of the processed motifs have been confirmed
free of identifiable third parties. That confirmation is a precondition
for B/C/D.

---

### 2. Publish a CV PDF?

**Choices**

- **A.** Keep `cv.qmd` text-only (position + interests + placeholder
  for PDF).
- **B.** Generate a PDF from a LaTeX/Quarto source, drop into
  `assets/cv/` or `files/cv/`, and add a download link.
- **C.** Link an off-site PDF (institutional page, ORCID, Google
  Scholar PDF).

**Current state (Phase 5F):** A. Text-only with placeholder.

**Trade-offs:**
- A avoids version-control drift but doesn't give search committees a
  downloadable artifact.
- B is the standard, but requires maintaining a CV source.
- C is low effort if such a hosted PDF already exists and is current.

---

### 3. Switch the deploy workflow to push-on-main?

**Choices**

- **A.** Keep `on: workflow_dispatch:` only (current state). Every
  publish is a deliberate human action.
- **B.** Add `on: push: branches: [main]` so every commit to main
  redeploys automatically.

**Current state (Phase 5F):** A. Manual-only. Each deploy is
triggered explicitly via `gh workflow run publish.yml ...` or the
Actions UI.

**Trade-offs:**
- A makes accidental publish impossible; cost is a manual click
  whenever you want a deploy.
- B is the standard hands-off pattern; cost is that every
  half-finished commit on main goes live.
- B also depends on confidence that course-repo updates and hub
  updates compose cleanly — if either course repo introduces a
  render failure, the next push-triggered run breaks production.

**Dependencies:** stable course-repo content + a few successful
hands-off-feeling deploys before flipping.

---

### 4. Future custom-domain email at `@matthewhester.com`?

**Choices**

- **A.** Defer indefinitely; current contact is
  `mhester@ualr.edu` (university) + `matthewahester@gmail.com`
  (research/general).
- **B.** Set up MX records + mailbox at the apex once a
  mail-hosting plan is chosen.

**Current state (Phase 5F):** A. No MX records on the zone (verified
during Phase 5D.1 DNS inventory).

**Trade-offs:** purely a future-self decision; no urgency.

---

## Resolved

### ~~Which email(s) appear on the public contact page?~~

**Resolved (Phase 4C, confirmed live Phase 5D):** **A. Both, split by
purpose.** University (`mhester@ualr.edu`) handles course/MAC matters;
Gmail (`matthewahester@gmail.com`) handles research and general
professional contact. Currently enrolled students are routed to
Blackboard. Live on `https://matthewhester.com/contact.html`.

### ~~Delete `projects.qmd` redirect stub?~~

**Resolved (Phase 5F):** **B. Keep.** The redirect stub is harmless
404 insurance and adds essentially zero weight to the artifact. No
external bookmarks point at `/projects.html` today, but the cost of
keeping is small enough that the safer default wins.

### ~~Deploy under GitHub Pages now or later?~~

**Resolved (Phase 5C, completed Phase 5D.2):** **B. Deploy.** Combined
GitHub Pages workflow built and triggered in Phase 5C; DNS cutover
completed in Phase 5D.2; HTTP live at `http://matthewhester.com/`.
HTTPS pending Let's Encrypt issuance as of 2026-05-24.

### ~~Add back-links from the course sites to the hub?~~

**Resolved (Phase 5B):** **A. Add.** Each course site's `_quarto.yml`
now includes a centered `page-footer` link to
`https://matthewhester.com/`. Committed in:
- `math-software` `cb228dd`
- `intro-stats` `61ba087`

### ~~Implement the combined-deploy pipeline?~~

**Resolved (Phase 5C):** **A. Implement now.** Hub workflow checks
out both course repos at deploy time and copies their `_site/`
outputs into the hub's `_site/{math-software,intro-stats}/`. One
combined GitHub Pages artifact. Workflow committed in `59078bf`;
action versions bumped to Node 24 in `30add62`.

---

## Private notes (not for the public site)

- **"Bayesian Nutrition Observatory" / "BNO"** is the long-term
  internal name for the bias-aware nutrition evidence project. It is
  intentionally **not** on the public Research page. Reintroduce only
  if and when there are concrete public artifacts to point at; until
  then, the public framing is the more grounded "Bias-robust Bayesian
  reanalysis of nutrition intervention meta-analyses."
