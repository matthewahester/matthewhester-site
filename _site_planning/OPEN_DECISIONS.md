# Open decisions — matthewhester.com

_Decisions that need a human call before next publication or design
pass. Local planning only; not rendered into `_site/`. Last updated:
2026-05-23 (end of Phase 4C)._

Each item lists the choices, the current state, and the trade-offs.
Resolve in order of urgency (publish-blockers first).

---

## 1. Which email(s) appear on the public contact page?

**Choices**

- **A.** Both: university (`mhester@ualr.edu`) for course/MAC matters
  + Gmail (`matthewahester@gmail.com`) for research/general.
- **B.** University email only.
- **C.** Gmail only.
- **D.** Add a future custom-domain address (e.g. `matt@matthewhester.com`)
  once the domain is live.

**Current state (Phase 4C):** A. Both, split by purpose.

**Trade-offs:**
- A is the most useful for visitors but doubles the surface area for
  inbound mail.
- B is institutionally cleanest but turns off non-university
  collaborators.
- C is informal and may confuse search-committee readers.
- D is desirable long-term but requires the domain + mail wiring.

---

## 2. Which boulder/landscape images, if any, represent each card?

**Choices**

- **A.** Keep all cards text-only (current state).
- **B.** Add one motif per card, picked intentionally one at a time in
  conversation; the processed motif files from Phase 4B are reused or
  replaced as needed.
- **C.** Use motifs only on the two featured-course cards, leaving the
  three category cards text-only.
- **D.** Use motifs only on the three category cards, leaving the
  featured-course cards to course-site visual identity.

**Current state (Phase 4C):** A. All text-only. Phase 4B processed
files (`motif-teaching-600.webp`, `motif-research-600.webp`,
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

## 3. Delete `projects.qmd` redirect stub?

**Choices**

- **A.** Delete now (the navbar no longer references it; nothing in
  the current QMD tree links to it; the redirect is for hypothetical
  external bookmarks only).
- **B.** Keep until the site has been live for some period after first
  publication, then delete.

**Current state (Phase 4C):** B by default — file remains as a
`<meta refresh>` stub.

**Trade-offs:**
- A is cleaner and removes a small bit of dead weight.
- B preserves any pre-launch bookmarks (low likelihood since the site
  isn't live).

---

## 4. Publish a CV PDF?

**Choices**

- **A.** Keep `cv.qmd` text-only (position + interests + placeholder
  for PDF).
- **B.** Generate a PDF from a LaTeX/Quarto source, drop into
  `assets/cv/` or `files/cv/`, and add a download link.
- **C.** Link an off-site PDF (institutional page, ORCID, Google
  Scholar PDF).

**Current state (Phase 4C):** A. Text-only with placeholder.

**Trade-offs:**
- A avoids version-control drift but doesn't give search committees a
  downloadable artifact.
- B is the standard, but requires maintaining a CV source.
- C is low effort if such a hosted PDF already exists and is current.

---

## 5. Deploy under GitHub Pages now or later?

**Choices**

- **A.** Stay on `workflow_dispatch` only; build locally, do not deploy.
- **B.** Flip the workflow trigger to `push: branches: [main]` and
  switch DNS off Google Sites to GitHub Pages.

**Current state (Phase 4C):** A. Workflow stays manual-only.

**Trade-offs:**
- A keeps the site behind the curtain until content is approved.
- B is the publication checkpoint — affects what people see when they
  go to `matthewhester.com`.

**Dependencies:** decisions 1, 3, 4, and probably 6 should be
resolved (or explicitly deferred) before B.

---

## 6. Add back-links from the course sites to the hub?

**Choices**

- **A.** Add a footer "← Matt Hester · matthewhester.com" to each
  course site's `_quarto.yml`.
- **B.** Leave course sites unchanged for now.

**Current state (Phase 4C):** B. Course sites untouched.

**Trade-offs:**
- A is a tiny edit but communicates the hub/spoke relationship to
  students who land directly on a course site URL.
- B respects the "do not touch course-site repos in this pass" rule.

---

## 7. Implement the combined-deploy pipeline?

**Choices**

- **A.** Implement now: hub workflow checks out each course-site repo,
  renders, and places the result under `_site/math-software/` and
  `_site/intro-stats/`. See `SITE_LINKING_PLAN.md` §3.
- **B.** Defer until publication is closer. Hub renders only the hub
  for now; course-site links remain broken until either A is built or
  the course sites get their own deploys.
- **C.** Per-course-site Pages deploy with reverse proxy / Cloudflare
  worker (rejected in Phase 4A; listed for completeness).

**Current state (Phase 4C):** B. Hub renders alone.

**Trade-offs:**
- A is the only way the homepage's `/math-software/` and
  `/intro-stats/` links resolve correctly once published.
- B keeps the hub buildable but means publish is incomplete until A
  is in place.

---

## Private notes (not for the public site)

- **"Bayesian Nutrition Observatory" / "BNO"** is the long-term
  internal name for the bias-aware nutrition evidence project. It is
  intentionally **not** on the public Research page. Reintroduce only
  if and when there are concrete public artifacts to point at; until
  then, the public framing is the more grounded "Bias-robust Bayesian
  reanalysis of nutrition intervention meta-analyses."
