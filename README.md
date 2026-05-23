# matthewhester.com

Source for [matthewhester.com](https://matthewhester.com) — a Quarto website
for teaching and research notes by Matt Hester.

## Stack

- [Quarto](https://quarto.org) for content and rendering
- Plain CSS in `styles.css` (no JS framework, no SCSS pipeline)
- GitHub Pages for hosting, with the custom domain set via `CNAME`
- GitHub Actions workflow at `.github/workflows/publish.yml` builds and
  deploys on every push to `main`

## Local development

Render the whole site:

```bash
quarto render
```

Or run a live preview server:

```bash
quarto preview
```

The rendered site is written to `_site/` (ignored from git).

## Layout

```
.
├── _quarto.yml              # site config, navbar, theme
├── index.qmd                # homepage with feature cards
├── about.qmd
├── teaching.qmd
├── projects.qmd
├── cv.qmd
├── contact.qmd
├── styles.css               # restrained rock/crystal/climbing palette
├── assets/brand/            # logos, favicons, brand artifacts
├── CNAME                    # custom domain for GitHub Pages
└── .github/workflows/
    └── publish.yml          # build + deploy to gh-pages
```

## Deploying

Push to `main`. The workflow builds with Quarto and publishes the result to
GitHub Pages. The custom domain is enforced via the `CNAME` file at the repo
root (Quarto copies it into the rendered site).

For the domain to resolve, the `matthewhester.com` DNS records must point
at GitHub Pages and the repository's Pages settings must list the same
custom domain.
