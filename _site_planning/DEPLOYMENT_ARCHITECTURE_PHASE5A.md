# Deployment architecture — Phase 5A

_Read-only architecture and readiness pass. Local planning only; not
rendered into `_site/`. Last updated: 2026-05-23._

Goal: publish all three sites under one custom domain.

```
https://matthewhester.com/                ← matthewhester-site (hub)
https://matthewhester.com/math-software/  ← math-software course site
https://matthewhester.com/intro-stats/    ← intro-stats course site
```

**No DNS, workflow, push, or course-site changes were made in this
pass.** This document records inspection findings and proposes an
architecture; the draft workflow and local-test plan live in sibling
files.

## 1. Repo inventory

### matthewhester-site (hub)

| Field | Value |
| --- | --- |
| Path | `D:/Github/matthewhester-site/` |
| Git | repo on `main`, 2 commits, pushed |
| Remote | `https://github.com/matthewahester/matthewhester-site.git` |
| `_quarto.yml output-dir` | `_site` |
| `site-url` | `https://matthewhester.com` |
| CNAME | present, exactly `matthewhester.com` |
| Workflow | `.github/workflows/publish.yml`, `on: workflow_dispatch` only |
| Render | succeeds, exit 0 |
| Uncommitted | 3 local-only planning files (intentional, gitignored or untracked-by-design) |

### math-software

| Field | Value |
| --- | --- |
| Path | `D:/Github/math-software/` |
| Git | **NOT a git repo** (no `.git` directory) |
| Remote | n/a |
| `_quarto.yml output-dir` | `_site` |
| `site-url` | `https://matthewhester.com/math-software/` ✓ already configured |
| CNAME | none ✓ (no conflict) |
| Workflow | none |
| Render | succeeds, exit 0 (18 qmd files) |
| Sitemap | URLs already prefixed with `/math-software/` ✓ |
| Absolute hrefs in rendered HTML | none ✓ (verified by grep) |
| `_site_planning/` excluded from render | yes ✓ |
| Mentions of "Blackboard" | 8 source files, used as "see LMS for X" pointers (not links into private content) |

### intro-stats

| Field | Value |
| --- | --- |
| Path | `D:/Github/intro-stats/` |
| Git | repo on `main`, 3 commits, **no remote configured** |
| Remote | n/a |
| `_quarto.yml output-dir` | `_site` |
| `site-url` | `https://matthewhester.com/intro-stats/` ✓ already configured |
| CNAME | none ✓ |
| Workflow | none |
| Render | succeeds, exit 0 (23 qmd files) |
| Sitemap | URLs already prefixed with `/intro-stats/` ✓ |
| Absolute hrefs in rendered HTML | none ✓ |
| `.gitignore` | strict — excludes `bank/`, `builder/`, `_source_material/`, `private/`, `keys/`, `answer_keys/`, `exams/`, `quizzes/`, plus filename patterns (`*_key.*`, `*answer_key*`, `*.RData`, `*.rds`) |
| Uncommitted | none (clean working tree) |

## 2. Prerequisites before any combined deploy can work

The proposed architecture assumes the hub workflow uses
`actions/checkout` to pull each course repo. That requires the course
repos to exist on GitHub. Currently:

- `matthewahester/matthewhester-site` exists and is up to date.
- `matthewahester/math-software` — **status unknown** (no local
  `.git`, no remote to query; `gh` CLI not installed locally so we
  can't verify GitHub-side).
- `matthewahester/intro-stats` — **status unknown** (local repo has
  no remote configured).

### What needs to happen first (Phase 5B candidates)

For **math-software**:
1. `git init` in `D:/Github/math-software/`.
2. Create the repository `matthewahester/math-software` on GitHub
   (public).
3. Add remote, stage everything the public site should ship (respect
   the existing `.gitignore` but consider adopting the stricter
   intro-stats pattern for private assessment material).
4. Initial commit and push.

For **intro-stats**:
1. Create the repository `matthewahester/intro-stats` on GitHub
   (public).
2. Add remote.
3. Push the existing 3 commits.

These steps **do not require any workflow or hub changes**; they can
land independently of Phase 5B/C.

## 3. Proposed combined-deploy architecture

### Pattern

The **hub repo's workflow** is the single owner of the published
artifact. It checks out the course repos as sibling working trees,
renders each, and assembles the combined `_site/` tree before
uploading to GitHub Pages.

Visually:

```
hub repo workflow runtime
├── checkout matthewhester-site                   → ./
├── checkout matthewahester/math-software         → ./course-math-software/
├── checkout matthewahester/intro-stats           → ./course-intro-stats/
│
├── quarto render          (hub)                  → _site/
├── quarto render          (course-math-software) → course-math-software/_site/
├── quarto render          (course-intro-stats)   → course-intro-stats/_site/
│
├── cp -r course-math-software/_site/. _site/math-software/
├── cp -r course-intro-stats/_site/.    _site/intro-stats/
│
├── ensure _site/CNAME exists
├── upload-pages-artifact path: _site
└── deploy-pages
```

Per-site `_site/` directories never nest — the **contents** of each
course site's `_site/` are copied into the subdirectory of the hub's
`_site/`. (Using `cp -r src/. dst/` copies contents; using
`cp -r src/ dst/` would copy the directory itself and produce
`_site/math-software/_site/...`, the nested mistake to avoid.)

### Why this pattern (vs alternatives)

- **Per-repo Pages with path-based routing** (each course site
  deploys to its own Pages, then a reverse proxy or Cloudflare
  Worker routes `/math-software/*` to one and `/intro-stats/*` to
  another). Rejected: extra infrastructure (proxy / Worker), extra
  config to keep in sync, harder to debug.
- **Per-course-site Pages on distinct subdomains** (`math-software.
  matthewhester.com`, `intro-stats.matthewhester.com`). Rejected:
  fragments the URL identity of the hub, doubles the DNS surface.
- **Monorepo all three sites into one Quarto project**. Rejected:
  course repos lose ownership and standalone buildability.

### Design decisions

**Checkout reference.** Use `actions/checkout@v4` with
`repository: matthewahester/<course>` and `ref: main`. Pin to `main`
explicitly so a stray feature branch never lands in production.

**Authentication.** If both course repos are **public**, the default
`GITHUB_TOKEN` is sufficient — `actions/checkout` can read public
repos without elevated permissions. **No PAT needed.** If either
course repo is private, switch to a PAT stored as a workflow secret.
Recommendation: keep them public (they are intended to be).

**Render isolation.** Render each repo in its own working directory.
Quarto's `_site/` is per-project (the hub's `_site/` is at the hub
root; each course repo's `_site/` is inside that course's checkout).
No risk of two `quarto render` invocations stepping on each other.

**Copy direction.** Always copy course `_site/contents` → hub
`_site/<course>/`. Never the reverse. Use `cp -r src/. dst/` (with
the trailing `.`) or `cp -r src/* dst/` to avoid the
`_site/math-software/_site/...` nesting bug.

**CNAME handling.** Hub's CNAME is the only one that matters —
GitHub Pages reads `_site/CNAME` at the root only. Course-site
CNAMEs at `_site/math-software/CNAME` would be ignored, but to keep
the artifact tidy, the workflow should `rm -f` any per-course CNAME
files before uploading.

**Search and site_libs.** Quarto bundles a per-site `site_libs/`
folder and per-site `search.json`. Under the combined artifact,
these live at:

```
_site/site_libs/                       ← hub's
_site/search.json                      ← hub's
_site/math-software/site_libs/         ← course's, self-contained
_site/math-software/search.json        ← course's, scoped to course
_site/intro-stats/site_libs/           ← course's, self-contained
_site/intro-stats/search.json          ← course's, scoped to course
```

No path collision; each Quarto site references its own `site_libs/`
via relative paths that work correctly inside the subdirectory.
Cross-site search is **not** provided (each search box only finds
content within its own site). That is an acceptable trade-off for
Phase 5; cross-site search would require a custom JS index.

**Avoiding nested `_site/_site`.** The course-checkout paths
(`course-math-software/`, `course-intro-stats/`) are sibling
directories at the workflow root, not inside the hub's `_site/`.
The only thing that ever enters `_site/math-software/` is the
**contents** of `course-math-software/_site/`, not the course
checkout itself.

**Course repo independence.** Each course repo still renders
locally with `quarto render` from its own root. The only thing the
hub workflow adds is the subdirectory copy at deploy time. Authors
can keep working in each course repo as today.

**Relative links / absolute links / `site-url`.** Both course sites
already have `site-url` set to the subdirectory URL, and grep finds
zero absolute `href="/..."` patterns in either rendered HTML. So no
edits to course-site sources are required for subdirectory
deployment to work cleanly.

**Workflow stays manual-only.** The new workflow keeps `on:
workflow_dispatch:`. First-pass deploys are triggered explicitly
from the Actions UI. Once we've confirmed several manual deploys
produce a healthy site, the decision to switch to `push: branches:
[main]` is a separate, deliberate change.

### Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| A course render fails on CI but works locally (R/Python missing on runner) | Add `r-lib/actions/setup-r@v2` or `actions/setup-python@v5` steps if needed; CI logs will tell us on first manual run |
| Course repo is renamed/deleted on GitHub mid-deploy | Hub workflow fails loudly; no partial deploy because `deploy-pages` runs only after `build` succeeds |
| Course site accidentally publishes private content | Each course repo has a CLAUDE.md with privacy rules and a gitignore that excludes private folders; protected by repo hygiene, not workflow |
| Workflow accidentally publishes broken site | Workflow is manual-only at first; CI logs available before users see live site |
| Pages settings already point at hub's gh-pages output → adding course content might break in unexpected ways | Verify by reading GH Pages settings before first combined deploy; do one full deploy with only manual trigger; rollback by re-running an older workflow run |

## 4. Safe publication sequence

Run **after** the combined-deploy workflow is staged, committed, and
pushed. Do **not** perform any of these steps in Phase 5A.

1. Commit the new `.github/workflows/publish.yml` to the hub repo
   locally.
2. Push to GitHub.
3. Open the repo's **Actions** tab and manually trigger
   `Publish to GitHub Pages` via `workflow_dispatch`.
4. Watch the run logs. Confirm every step succeeds (checkout × 3,
   render × 3, copy × 2, upload, deploy).
5. Find the deployed Pages URL in the run output (usually
   `https://matthewahester.github.io/matthewhester-site/` if the
   custom domain isn't yet active, or `https://matthewhester.com/`
   if it is).
6. Visit the Pages URL and confirm:
   - the homepage loads (`/`),
   - `/math-software/` loads and looks like the course site,
   - `/intro-stats/` loads and looks like the course site,
   - images, CSS, and per-site search boxes all work,
   - `https://<pages-url>/CNAME` returns `matthewhester.com`.
7. **Only after** the above checks pass, switch DNS at the registrar:
   point `matthewhester.com` (and the `www.` CNAME if used) at the
   GitHub Pages targets. Document the previous DNS state so it can
   be rolled back.
8. In the GitHub repo's **Settings → Pages**, confirm the custom
   domain is `matthewhester.com` and "Enforce HTTPS" is checked
   (it usually appears after DNS has propagated and Let's Encrypt
   has issued a cert).

DNS propagation can take from minutes to a day. If anything goes
sideways during DNS cutover, revert the registrar change immediately
— GitHub Pages settings can stay as they are.

## 5. Remote inspection limits

`gh` CLI is **not installed locally**, so remote inspection of the
three repos and their Pages / Actions settings is limited to what
the local `git` client can see (remote URL, last fetched commits).
Anything that needs the GitHub API (Pages config, Actions run
history, repo visibility, branch protection) is out of scope for
this pass.

If `gh` is installed later (`winget install GitHub.cli`), the useful
read-only commands are:

```bash
gh repo view matthewahester/matthewhester-site
gh repo view matthewahester/math-software        # may 404 today
gh repo view matthewahester/intro-stats          # may 404 today
gh api repos/matthewahester/matthewhester-site/pages
gh run list --repo matthewahester/matthewhester-site --limit 10
```

None of these change state.

## 6. Files produced by this pass

- `DEPLOYMENT_ARCHITECTURE_PHASE5A.md` (this file)
- `PUBLISH_WORKFLOW_DRAFT_PHASE5A.md` — proposed workflow YAML
- `LOCAL_COMBINED_BUILD_TEST_PLAN.md` — local simulation steps

`.github/workflows/publish.yml` was **not** modified. No course-site
repo was touched. No commits, no pushes, no DNS changes.
