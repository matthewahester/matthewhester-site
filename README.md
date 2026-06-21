# matthewhester.com

Source for [matthewhester.com](https://matthewhester.com) — the public
Quarto hub for Matt Hester's teaching and research, and the umbrella that
assembles ten sibling course-material sites under the same domain.

The site is **live** at [matthewhester.com](https://matthewhester.com),
served from GitHub Pages over HTTPS with the custom domain set via `CNAME`.

## Stack

- [Quarto](https://quarto.org) for content and rendering
- Plain CSS in `styles.css` (no JS framework, no SCSS pipeline)
- GitHub Pages for hosting, with the custom domain set via `CNAME`
- GitHub Actions workflow at `.github/workflows/publish.yml`,
  `workflow_dispatch` (manual) only — see "Deployment" below

## Local development

Render the hub:

```bash
quarto render
```

Or run a live preview server:

```bash
quarto preview
```

The rendered hub is written to `_site/` (gitignored). A local hub render
covers only the hub pages; the course sites live in their own repos and are
combined at deploy time (see "Combined course-site deployment").

## Layout

```
.
├── _quarto.yml              # site config, navbar, theme, OG defaults
├── index.qmd                # homepage: title block + split hero + cards
├── about.qmd
├── teaching.qmd             # ten-site course-material portfolio
├── research.qmd             # research strands + Course Builder + preprint
├── cv.qmd
├── contact.qmd
├── projects.qmd             # redirect stub → research.html (404 insurance)
├── styles.css               # rock/crystal/climbing palette
├── assets/                  # images (raw/ is gitignored)
├── tools/                   # Pillow image helpers (process, hero thumbs)
├── CNAME                    # custom domain for GitHub Pages
├── _site_planning/          # local-only planning notes (not rendered)
└── .github/workflows/
    └── publish.yml          # workflow_dispatch only (manual deploy)
```

## Course sites

The hub links to and — at deploy time — assembles ten public course-material
sites, each maintained in its own public repo under
[`matthewahester/`](https://github.com/matthewahester) and served under this
domain:

| Path | Repo |
|---|---|
| `/math-software/`         | `matthewahester/math-software` |
| `/intro-stats/`           | `matthewahester/intro-stats` |
| `/bayesian-statistics/`   | `matthewahester/bayesian-statistics` |
| `/intro-probability/`     | `matthewahester/intro-probability` |
| `/statistical-inference/` | `matthewahester/statistical-inference` |
| `/statistical-modeling/`  | `matthewahester/statistical-modeling` |
| `/modern-sas/`            | `matthewahester/modern-sas` |
| `/statistical-design/`    | `matthewahester/statistical-design` |
| `/applied-statistics/`    | `matthewahester/applied-statistics` |
| `/nonparametrics/`        | `matthewahester/nonparametrics` |

Two are current courses (`math-software`, `intro-stats`); the other eight are
assembled course-material sites. The course repos have no workflows of their
own — the hub workflow checks them out and renders them at deploy time.

## Deployment

**Nothing in this repo deploys automatically.** The workflow is
`on: workflow_dispatch` only — it runs when manually triggered from the
GitHub Actions UI (or via
`gh workflow run publish.yml --repo matthewahester/matthewhester-site --ref main`).

A single workflow run:

1. checks out the hub and all ten public course repos;
2. sets up Quarto (and R only if a rendered repo ships executable `{r}`
   chunks);
3. renders the hub and each course site;
4. copies each course `_site/.` into `_site/<course>/`;
5. ensures the root `CNAME` and drops any nested ones;
6. uploads one combined Pages artifact and deploys it.

### Combined course-site deployment

The hub and the ten course sites are combined into a **single** Pages
artifact by the steps above: the hub renders to `_site/`, and each course
site's `_site/` output is copied into a matching `_site/<course>/`
subdirectory before the artifact is uploaded. This is why a course site
appears at `matthewhester.com/<course>/` even though it has no workflow of
its own.

### Notes

- DNS for `matthewhester.com` points at GitHub Pages; the cutover from the
  earlier landing page is complete and the apex serves this site.
- Switching the workflow to deploy on push to `main` is a possible future
  change. Until the workflow itself says otherwise, deploys stay manual.
- After any deploy, confirm the Pages run is green and spot-check the live
  hub and a course path before relying on it.
