# matthewhester.com

Source for [matthewhester.com](https://matthewhester.com) — a Quarto
website for teaching and research notes by Matt Hester. Eventually
the public hub for two sibling course sites
(`math-software`, `intro-stats`) under the same domain.

## Stack

- [Quarto](https://quarto.org) for content and rendering
- Plain CSS in `styles.css` (no JS framework, no SCSS pipeline)
- GitHub Pages for hosting, with the custom domain set via `CNAME`
- GitHub Actions workflow at `.github/workflows/publish.yml`,
  currently `workflow_dispatch` only — see "Deployment" below

## Local development

Render the whole site:

```bash
quarto render
```

Or run a live preview server:

```bash
quarto preview
```

The rendered site is written to `_site/` (gitignored).

## Layout

```
.
├── _quarto.yml              # site config, navbar, theme, OG defaults
├── index.qmd                # homepage: title block + split hero + cards
├── about.qmd
├── teaching.qmd
├── research.qmd             # research interests + project descriptions
├── resources.qmd            # index of public resources
├── cv.qmd
├── contact.qmd
├── projects.qmd             # Phase 4A redirect stub → research.html
├── styles.css               # rock/crystal/climbing palette
├── assets/                  # images (raw/ is gitignored)
├── tools/process_images.py  # Pillow-based EXIF strip + resize
├── CNAME                    # custom domain for GitHub Pages
├── _site_planning/          # local-only planning notes
└── .github/workflows/
    └── publish.yml          # workflow_dispatch only (no auto-deploy)
```

## Deployment

**Nothing in this repo deploys automatically.** The workflow is set
to `on: workflow_dispatch` only — it runs only when manually
triggered from the GitHub Actions UI.

### Current state

- The repo is on GitHub at
  [matthewahester/matthewhester-site](https://github.com/matthewahester/matthewhester-site).
- The first deployment has not yet been run.
- DNS for `matthewhester.com` still points at the previous Google
  Site; switching is a separate, explicit step.
- The two sibling course sites (`/math-software/`, `/intro-stats/`)
  are linked from this site but **not yet served under this
  domain**. They live in their own repos and will be combined into
  one Pages artifact by a future workflow change.

### When ready to publish

1. Confirm `_quarto.yml`, content pages, and the `CNAME` file are
   what you want to ship.
2. Trigger the workflow manually from the Actions tab in GitHub.
3. Inspect the Actions run logs and the deployed Pages URL before
   touching DNS.
4. Only after the deployed site looks correct, update DNS at the
   registrar to point at GitHub Pages.
5. In **Settings → Pages**, verify the custom domain is
   `matthewhester.com` and "Enforce HTTPS" is enabled.

### Combined course-site deployment (planned)

The current workflow renders only the hub. A future change will
also check out the course-site repos, render them, and copy their
`_site/` outputs into `_site/math-software/` and `_site/intro-stats/`
before uploading a single Pages artifact. See
`_site_planning/DEPLOYMENT_ARCHITECTURE_PHASE5A.md` and
`_site_planning/PUBLISH_WORKFLOW_DRAFT_PHASE5A.md` for the planned
architecture and the proposed workflow YAML. Neither is wired up
yet.
